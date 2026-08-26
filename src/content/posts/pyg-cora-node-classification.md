---
title: "用 PyTorch Geometric 在 Cora 上完成节点分类"
description: "从 edge_index 和 PyG Data 出发，在 Cora 论文引用网络上比较 GCN 与 MLP，并通过隐藏维度、Dropout、层数和多个随机种子理解图结构的价值。"
pubDatetime: 2026-07-28T17:10:00+08:00
tags: ["python", "机器学习", "深度学习", "GNN", "PyTorch", "PyG", "节点分类"]
category: "技术"
topic: "data-ml"
status: "in-progress"
featured: false
draft: false
---

## 目录

## 从手写 GCN 到真实图数据

在上一篇[从零理解 GNN：手写第一个两层 GCN](/posts/gnn-from-scratch-first-gcn/)
中，我使用稠密邻接矩阵和纯 PyTorch 实现了一个小型 GCN。

这次继续使用 PyTorch Geometric（PyG），在真实的 Cora 论文引用网络上完成节点分类，
并回答几个更实际的问题：

- 真实图为什么使用 `edge_index`，而不是完整邻接矩阵？
- PyG 的 `Data` 对象保存了什么？
- 为什么训练、验证、测试需要严格分工？
- 隐藏维度、Dropout 和 GCN 层数会怎样影响结果？
- GCN 是否真的比不使用图结构的 MLP 更好？
- 为什么正式实验需要运行多个随机种子？

## `edge_index`：只保存真正存在的边

完整邻接矩阵的大小是：

```text
[节点数, 节点数]
```

当图有大量节点时，即使绝大多数节点之间没有连接，仍需要保存大量的 0。真实图通常
比较稀疏，因此 PyG 只保存实际存在的边。

考虑无向图：

```text
0 -- 1 -- 2
```

PyG 可以表示为：

```python
edge_index = torch.tensor([
    [0, 1, 1, 2],  # 消息发送者
    [1, 0, 2, 1],  # 消息接收者
])
```

`edge_index` 的形状是：

```text
[2, E]
```

- 第一行保存每条消息的发送节点；
- 第二行保存对应的接收节点；
- 每一列共同表示一条有向传播边；
- 无向关系通常保存为两个方向。

例如增加无向边 `0 -- 2`，需要同时加入：

```text
0 → 2
2 → 0
```

## PyG 的 `Data` 对象

PyG 使用 `Data` 将一张图需要的张量组织在一起：

```python
from torch_geometric.data import Data

graph = Data(
    x=node_features,
    edge_index=edge_index,
    y=labels,
)
```

节点分类中常见的字段包括：

```text
data.x          节点特征 [N, F]
data.edge_index 边列表   [2, E]
data.y          节点标签 [N]
data.train_mask 训练节点 [N]
data.val_mask   验证节点 [N]
data.test_mask  测试节点 [N]
```

掩码是布尔张量。某个位置为 `True`，表示对应节点属于该数据划分。

## Cora 论文引用网络

Cora 是一个经典节点分类数据集：

- 节点：论文；
- 边：论文之间的引用关系；
- 节点特征：论文的词袋特征；
- 标签：论文所属研究主题；
- 任务：根据少量已标记论文预测其他论文的类别。

加载代码：

```python
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import NormalizeFeatures

dataset = Planetoid(
    root="data/Planetoid",
    name="Cora",
    transform=NormalizeFeatures(),
)
data = dataset[0]
```

数据结构可以通过以下字段检查：

```python
print(data.x.shape)
print(data.edge_index.shape)
print(data.y.shape)
print(data.train_mask.sum())
print(data.val_mask.sum())
print(data.test_mask.sum())
```

训练、验证和测试掩码不能重叠。三者职责不同：

```text
训练集：学习模型参数
验证集：选择超参数和最佳模型
测试集：最终评价一次
```

如果根据测试集结果不断修改隐藏维度、Dropout 或模型结构，测试信息就间接参与了
调参，最终成绩会过度乐观。

## 使用 `GCNConv` 构建两层 GCN

手写 GCN 时，需要自己添加自环并归一化邻接矩阵。PyG 的 `GCNConv` 可以接收
`x` 和 `edge_index`，内部完成消息传播和归一化。

```python
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv


class CoraGCN(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_classes):
        super().__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, num_classes)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(
            x,
            p=0.5,
            training=self.training,
        )
        return self.conv2(x, edge_index)
```

两层模型执行两次消息传播，因此节点最远可以获得两跳范围内的信息。

## 使用验证集保存最佳模型

每轮训练只使用训练节点计算损失：

```python
train_loss = F.cross_entropy(
    logits[data.train_mask],
    data.y[data.train_mask],
)
```

更新参数后，切换到评估模式并计算验证损失：

```python
model.eval()

with torch.no_grad():
    logits = model(data.x, data.edge_index)
    val_loss = F.cross_entropy(
        logits[data.val_mask],
        data.y[data.val_mask],
    )
```

验证损失下降时保存模型参数。训练结束后恢复验证集上表现最好的版本，最后才计算测试
准确率。

这个过程可以避免直接使用测试集选模型，但它不意味着完全解决了过拟合。反复尝试大量
超参数仍然可能逐渐过拟合验证集。

## GCN 与 MLP 基线

为了判断引用关系是否真正提供了信息，需要建立一个完全不使用 `edge_index` 的 MLP：

```python
class CoraMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_classes):
        super().__init__()
        self.linear1 = nn.Linear(input_dim, hidden_dim)
        self.linear2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.dropout(x, p=0.5, training=self.training)
        return self.linear2(x)
```

在随机种子 42、隐藏维度 16 的实验中：

| 模型 | 训练准确率 | 验证准确率 | 测试准确率 |
| ---- | ---------: | ---------: | ---------: |
| GCN  |      1.000 |      0.780 |      0.805 |
| MLP  |      1.000 |      0.544 |      0.566 |

GCN 的测试准确率比 MLP 高 `0.239`。两者都能完全拟合训练节点，但 GCN 的验证和
测试表现明显更好，说明 Cora 的论文引用关系提供了有用的结构信息。

## 实验一：隐藏维度 8 与 32

只改变隐藏维度，其他训练条件保持一致：

| 隐藏维度 | 训练准确率 | 验证准确率 | 测试准确率 |
| -------: | ---------: | ---------: | ---------: |
|        8 |      0.986 |      0.786 |      0.808 |
|       32 |      1.000 |      0.794 |      0.809 |

按照验证准确率，应选择隐藏维度 32。但两个配置的测试准确率只相差 `0.001`，不能据此
声称 32 维具有明显优势。

更大的隐藏维度提高了模型容量，但也可能增加计算量和过拟合风险。超参数选择应综合
验证结果、稳定性和模型成本。

## 实验二：Dropout 与过拟合

Dropout 在训练时随机屏蔽部分隐藏特征：

```python
x = F.dropout(
    x,
    p=dropout_p,
    training=self.training,
)
```

比较 `p=0.5` 与 `p=0.0`：

| Dropout | 训练准确率 | 验证准确率 | 训练-验证差距 | 测试准确率 |
| ------: | ---------: | ---------: | ------------: | ---------: |
|     0.5 |      1.000 |      0.780 |         0.220 |      0.805 |
|     0.0 |      1.000 |      0.786 |         0.214 |      0.798 |

这次单次实验中，不使用 Dropout 的验证准确率略高，但测试准确率略低。两组差距都很小，
不能通过单次结果断定 Dropout 是否更好。

Dropout 是正则化方法，不保证每次运行都提高准确率。更可靠的判断需要多个随机种子，
并同时观察训练与验证的差距。

## 实验三：一层 GCN

一层 GCN 只包含一个消息传递层：

```python
class OneLayerGCN(nn.Module):
    def __init__(self, input_dim, num_classes):
        super().__init__()
        self.conv = GCNConv(input_dim, num_classes)

    def forward(self, x, edge_index):
        return self.conv(x, edge_index)
```

实验结果：

```text
训练准确率：0.986
验证准确率：0.744
测试准确率：0.767
```

两层 GCN 的测试准确率约为 `0.81`，高于一层模型的 `0.767`。一种直观解释是：

```text
一层 GCN → 一次消息传播 → 一跳邻居
两层 GCN → 两次消息传播 → 最远两跳邻居
```

`edge_index` 本身没有层数。传播范围取决于模型连续使用了多少个消息传递层。

层数也不是越多越好。过多层可能使节点表示越来越相似，产生过度平滑。

## 实验四：多个随机种子

神经网络结果会受到参数初始化和 Dropout 随机性的影响。只报告一次运行结果，可能刚好
遇到特别好或特别差的初始化。

使用随机种子 `[0, 1, 2]` 重复实验：

| 模型 | 三次测试准确率      |  均值 | 标准差 |
| ---- | ------------------- | ----: | -----: |
| GCN  | 0.808、0.812、0.812 | 0.811 |  0.002 |
| MLP  | 0.570、0.577、0.573 | 0.573 |  0.003 |

GCN 不仅平均准确率比 MLP 高约 `0.238`，三次结果的标准差也很小。在这个实验设置中，
图结构带来的收益是稳定的。

三个随机种子适合入门练习，但正式实验通常应使用更多重复，并明确报告：

```text
数据划分
随机种子
超参数
均值
标准差
模型选择规则
```

## 这次实验学到的内容

- `edge_index` 用两行和若干列保存实际存在的消息传播边；
- PyG 的 `Data` 将节点特征、边、标签和数据掩码组织在一起；
- `GCNConv` 封装了自环、归一化、线性变换和消息传播；
- 超参数应该根据验证集选择，测试集只用于最终评价；
- Cora 上的 GCN 明显优于 MLP，说明引用关系具有预测价值；
- 隐藏维度增加不一定带来明显测试提升；
- Dropout 的作用不能通过一次实验简单判断；
- 一层 GCN 只获得一跳信息，两层 GCN 最远获得两跳信息；
- 多随机种子均值比单次结果更可靠，标准差反映模型稳定性。

## 下一步

下一阶段会在相同数据和评估流程下比较：

1. GCN：使用度归一化聚合邻居；
2. GraphSAGE：使用邻居聚合并支持归纳学习；
3. GAT：为不同邻居学习注意力权重。

重点不只是比较准确率，还要理解三种模型如何回答同一个问题：

> 一个节点应该从哪些邻居获得信息，又应该如何为这些信息分配权重？
