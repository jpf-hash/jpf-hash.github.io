---
title: "从零理解 GNN：手写第一个两层 GCN"
description: "从邻接矩阵、消息传递和对称归一化出发，用纯 PyTorch 手写两层 GCN，并通过 MLP 基线理解图结构究竟带来了什么。"
pubDatetime: 2026-07-28T09:30:00+08:00
tags: ["python", "机器学习", "深度学习", "GNN", "PyTorch", "笔记"]
category: "技术"
topic: "machine-learning"
status: "in-progress"
featured: false
draft: false
---

## Table of contents

## 为什么开始学习 GNN

普通神经网络擅长处理结构规则的数据，例如图像和序列。但很多现实问题天然是一张图：

- 社交网络中，用户是节点，关注关系是边；
- 分子中，原子是节点，化学键是边；
- 推荐系统中，用户和商品是节点，点击或购买行为是边；
- 论文网络中，论文是节点，引用关系是边。

这次练习的目标不是直接调用图神经网络库，而是先使用纯 PyTorch 手写一个最小的
GCN（Graph Convolutional Network），理解图结构究竟在哪里进入神经网络。

## GCN 与普通神经网络的区别

普通线性层可以写成：

```text
output = X @ W
```

- `X` 是输入特征；
- `W` 是模型需要学习的权重。

GCN 在这个基础上加入归一化后的图结构：

```text
output = A_norm @ X @ W
```

其中 `A_norm` 来自邻接矩阵，它规定了哪些节点可以互相传递信息，以及传递信息时使用
多大的权重。

因此，GCN 可以简单理解为：

> 保留普通神经网络的特征变换，同时让每个节点按照图结构聚合邻居信息。

## 用邻接矩阵表示图

考虑一条只有三个节点的链：

```text
0 -- 1 -- 2
```

邻接矩阵和节点特征如下：

```python
import torch

adj = torch.tensor([
    [0., 1., 0.],
    [1., 0., 1.],
    [0., 1., 0.],
])

x = torch.tensor([
    [1., 0.],  # 节点 0
    [2., 1.],  # 节点 1
    [0., 3.],  # 节点 2
])
```

`adj[i, j] == 1` 表示节点 `i` 和节点 `j` 之间存在边。这里：

```text
adj.shape = [3, 3]
x.shape   = [3, 2]
```

图中有 3 个节点，每个节点有 2 个特征。

## 为什么 `adj @ x` 可以聚合邻居信息

执行：

```python
neighbor_sum = adj @ x
```

得到：

```text
tensor([
    [2., 1.],
    [1., 3.],
    [2., 1.]
])
```

以节点 1 为例，它连接节点 0 和节点 2，所以计算的是：

```text
[1, 0] + [0, 3] = [1, 3]
```

邻接矩阵的每一行决定当前节点应该收集哪些节点的特征。因此，矩阵乘法
`adj @ x` 本质上就是一次邻居消息聚合。

## 自环与归一化

原始邻接矩阵只会聚合邻居信息，可能丢掉节点自己的特征。解决方法是加入单位矩阵：

```python
adj_self = adj + torch.eye(adj.size(0))
```

这相当于给每个节点添加一条指向自己的边，也就是自环。

不同节点的邻居数量可能不同。如果直接求和，邻居较多的节点容易得到更大的数值。
经典 GCN 使用对称归一化：

```text
A_norm = D^(-1/2) @ (A + I) @ D^(-1/2)
```

纯 PyTorch 实现如下：

```python
def normalize_adjacency(adj):
    adj_self = adj + torch.eye(
        adj.size(0),
        device=adj.device,
    )
    degree = adj_self.sum(dim=1)
    degree_inv_sqrt = degree.pow(-0.5)

    return (
        degree_inv_sqrt[:, None]
        * adj_self
        * degree_inv_sqrt[None, :]
    )
```

三个节点示例得到的矩阵为：

```text
tensor([
    [0.5000, 0.4082, 0.0000],
    [0.4082, 0.3333, 0.4082],
    [0.0000, 0.4082, 0.5000]
])
```

它仍然是对称矩阵，没有边的位置仍为 0。

## 手写一层 GCN

一层 GCN 的核心只有两步：

1. 使用线性层变换特征；
2. 使用归一化邻接矩阵聚合信息。

```python
import torch.nn as nn


class GCNLayer(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = nn.Linear(
            in_features,
            out_features,
            bias=False,
        )

    def forward(self, features, graph):
        return graph @ self.linear(features)
```

如果输入有 `N` 个节点：

```text
features:                 [N, in_features]
linear(features):         [N, out_features]
graph:                    [N, N]
graph @ linear(features): [N, out_features]
```

GCN 层不会改变节点数量，但可以改变每个节点的特征维度。

## 两层 GCN 与两跳信息

两层模型可以写成：

```python
class GCN(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_classes):
        super().__init__()
        self.gcn1 = GCNLayer(input_dim, hidden_dim)
        self.gcn2 = GCNLayer(hidden_dim, num_classes)

    def forward(self, features, graph):
        hidden = torch.relu(
            self.gcn1(features, graph)
        )
        return self.gcn2(hidden, graph)
```

每一层 GCN 都进行一次邻居信息传播：

```text
1 层 GCN → 一跳邻居，也就是直接相连的节点
2 层 GCN → 两跳邻居，也就是邻居的邻居
K 层 GCN → 最远获得 K 跳范围的信息
```

例如：

```text
A -- B -- C
```

第一层更新后，B 的表示已经包含 C 的信息。第二层更新 A 时，B 会将混合后的表示
传给 A，因此信息可以沿着 `C → B → A` 传播。

“获得两跳信息”并不意味着完整保存远方节点的原始特征。信息会经过聚合、线性变换和
激活函数，不同节点的信息会被混合与压缩。

## 半监督节点分类

练习中构造了 6 个节点，其中 4 个用于训练，2 个用于测试：

```python
labels = torch.tensor([0, 0, 0, 1, 1, 1])

train_mask = torch.tensor([
    True, True, False,
    True, True, False,
])

test_mask = ~train_mask
```

整张图都会参与前向传播：

```python
logits = model(train_x, train_graph)
```

但只有训练节点参与损失计算：

```python
loss = F.cross_entropy(
    logits[train_mask],
    labels[train_mask],
)
```

这意味着测试节点的标签不会参与训练，但测试节点仍存在于图中，它的特征可以通过边
传给训练节点。

需要区分两件事：

```text
是否参与消息传递
是否参与损失计算
```

经典的半监督节点分类允许训练时看到整张图的结构和所有节点特征，但不能使用测试节点
的标签。这种设置通常称为直推学习。如果测试节点在真实场景中是未来才出现的节点，
训练时提前看到它的特征或边就可能造成数据泄漏。

## 训练结果

基础两层 GCN 的执行结果为：

```text
最终损失：0.0134
训练准确率：1.0
测试准确率：1.0
预测：[0, 0, 0, 1, 1, 1]
```

改变隐藏层维度后：

| 隐藏维度 | 最终损失 | 训练准确率 | 测试准确率 |
| -------: | -------: | ---------: | ---------: |
|        2 |   0.0310 |       1.00 |       1.00 |
|        4 |   0.0133 |       1.00 |       1.00 |
|       16 |   0.0020 |       1.00 |       1.00 |

扩大隐藏维度降低了训练损失，但没有提高准确率。这个数据集只有 6 个节点，任务非常
简单，因此不能据此得出隐藏维度越大越好的结论。

删除无向边 `0—1` 后，节点 0 成为孤立节点。三个隐藏维度仍然得到 100% 准确率，
说明当前任务主要依赖节点自身特征，删除这条边没有改变最终分类结果。

## 为什么必须与 MLP 比较

为了判断图结构是否真的有帮助，还需要训练一个不使用图传播的 MLP：

```python
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_classes):
        super().__init__()
        self.linear1 = nn.Linear(input_dim, hidden_dim)
        self.linear2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, features):
        hidden = torch.relu(self.linear1(features))
        return self.linear2(hidden)
```

MLP 不接收邻接矩阵，每个节点只使用自己的特征。实验结果为：

```text
MLP 最终损失：0.0015
MLP 训练准确率：1.0
MLP 测试准确率：1.0
预测：[0, 0, 0, 1, 1, 1]
```

MLP 和 GCN 都取得了 100% 准确率。这并不能证明 GCN 没有价值，而是说明这个人工
数据中的两类节点特征本身已经很容易区分：

```text
类别 0：第一个特征较大
类别 1：第二个特征较大
```

只看节点自身特征就足以完成分类，图结构没有提供不可替代的信息。

因此，评价 GNN 时必须设置不使用图结构的简单基线。如果 GNN 没有超过 MLP，就不能
直接声称图结构改善了预测。

## 这次练习真正学到的内容

- 邻接矩阵不仅表示边，还可以通过矩阵乘法控制信息传播；
- `A_norm @ X @ W` 可以理解为“邻居聚合 + 特征变换”；
- 自环让节点更新时保留自己的特征；
- 一层 GCN 传播一跳，两层 GCN 最远传播两跳；
- 测试节点可以参与消息传递，但测试标签不能参与训练；
- 训练损失更低不一定意味着测试效果更好；
- GNN 必须与 MLP 等不使用图结构的基线公平比较；
- 一个 6 节点人工数据集只适合验证代码和理解原理，不能用于证明模型优劣。

## 下一步

下一阶段会使用 PyTorch Geometric 和 Cora 论文引用网络完成真实的节点分类，并在
相同数据划分下比较：

1. MLP；
2. GCN；
3. GraphSAGE；
4. GAT。

除了准确率，还需要使用多个随机种子报告均值和标准差，并观察图结构什么时候真正
带来收益。
