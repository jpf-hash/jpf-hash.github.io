---
title: "机器学习算法入门：KNN、决策树与随机森林"
description: "深入浅出地介绍三种经典的机器学习算法，包括原理、实现和应用场景。"
pubDatetime: 2026-05-29T10:00:00+08:00
tags: ["机器学习", "python", "算法", "分类"]
category: "技术"
featured: false
draft: false
---

## Table of contents

## 引言

机器学习是人工智能的核心，而算法是机器学习的基础。本文将介绍三种经典的监督学习算法：

- **KNN (K-Nearest Neighbors)** — K 近邻算法
- **决策树 (Decision Tree)** — 树形结构的分类器
- **随机森林 (Random Forest)** — 集成学习的代表

## KNN 算法

### 原理

KNN 是最简单的机器学习算法之一。它的核心思想是：

> 如果一个样本在特征空间中的 K 个最相似的样本中的大多数属于某一个类别，则该样本也属于这个类别。

### 实现

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# 加载数据
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)

# 创建 KNN 分类器
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# 预测
accuracy = knn.score(X_test, y_test)
print(f"准确率: {accuracy:.2f}")
```

### 优缺点

**优点：**
- 简单直观，易于理解
- 无需训练过程
- 适合多分类问题

**缺点：**
- 计算量大（需要计算与所有样本的距离）
- 对不平衡数据敏感
- 需要选择合适的 K 值

## 决策树

### 原理

决策树是一种树形结构的分类器，通过一系列的判断规则来对数据进行分类。

```
天气?
├── 晴天
│   └── 湿度?
│       ├── 高 → 不去
│       └── 正常 → 去
├── 阴天 → 去
└── 雨天
    └── 风?
        ├── 强 → 不去
        └── 弱 → 去
```

### 实现

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# 加载数据
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)

# 创建决策树
dt = DecisionTreeClassifier(max_depth=3, random_state=42)
dt.fit(X_train, y_train)

# 预测
accuracy = dt.score(X_test, y_test)
print(f"准确率: {accuracy:.2f}")

# 特征重要性
for name, importance in zip(iris.feature_names, dt.feature_importances_):
    print(f"{name}: {importance:.3f}")
```

### 优缺点

**优点：**
- 可解释性强（可以可视化）
- 能处理数值和类别特征
- 不需要特征缩放

**缺点：**
- 容易过拟合
- 对噪声数据敏感
- 不稳定（数据小变化可能导致树结构大变化）

## 随机森林

### 原理

随机森林是集成学习的代表，它通过构建多个决策树并综合它们的预测结果来提高模型的泛化能力。

> 随机森林 = 多个决策树 + 随机性 + 投票/平均

### 实现

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# 加载数据
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)

# 创建随机森林
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 预测
accuracy = rf.score(X_test, y_test)
print(f"准确率: {accuracy:.2f}")

# 特征重要性
for name, importance in zip(iris.feature_names, rf.feature_importances_):
    print(f"{name}: {importance:.3f}")
```

### 优缺点

**优点：**
- 泛化能力强
- 能处理高维数据
- 不容易过拟合
- 可以评估特征重要性

**缺点：**
- 训练时间较长
- 模型可解释性较差
- 内存消耗大

## 算法对比

| 特性 | KNN | 决策树 | 随机森林 |
|------|-----|--------|----------|
| 训练速度 | 快（无需训练） | 快 | 较慢 |
| 预测速度 | 慢 | 快 | 中等 |
| 可解释性 | 低 | 高 | 低 |
| 过拟合风险 | 中 | 高 | 低 |
| 适用场景 | 小数据集 | 需要解释 | 大数据集 |

## 总结

- **KNN** — 最简单，适合入门和小数据集
- **决策树** — 可解释性强，适合需要理解模型的场景
- **随机森林** — 性能强大，适合实际应用

选择算法时，需要考虑：
- 数据集大小
- 是否需要可解释性
- 计算资源限制
- 准确率要求

## 参考资料

- [Scikit-learn 官方文档](https://scikit-learn.org/)
- [机器学习实战](https://www.manning.com/books/machine-learning-in-action)
