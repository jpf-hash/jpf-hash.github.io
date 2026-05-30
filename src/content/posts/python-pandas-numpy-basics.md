---
title: "Python 数据科学入门：NumPy 与 Pandas 基础"
description: "NumPy 和 Pandas 是 Python 数据科学的两大基石。本文介绍它们的核心概念和常用操作。"
pubDatetime: 2026-05-30T14:00:00+08:00
tags: ["python", "数据科学", "numpy", "pandas"]
category: "技术"
featured: true
draft: false
---

## Table of contents

## 为什么学 NumPy 和 Pandas？

在数据科学领域，NumPy 和 Pandas 是两个最重要的 Python 库：

- **NumPy** — 高性能数值计算，提供多维数组对象
- **Pandas** — 数据处理和分析，提供 DataFrame 结构

## NumPy 基础

### 创建数组

```python
import numpy as np

# 从列表创建
arr = np.array([1, 2, 3, 4, 5])

# 创建特殊数组
zeros = np.zeros((3, 4))      # 3x4 全零数组
ones = np.ones((2, 3))        # 2x3 全一数组
random = np.random.rand(3, 3) # 3x3 随机数组

# 创建序列
seq = np.arange(0, 10, 2)    # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5) # [0, 0.25, 0.5, 0.75, 1]
```

### 数组操作

```python
# 形状操作
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)      # (2, 3)
print(arr.reshape(3, 2))  # 改变形状

# 索引和切片
print(arr[0, 1])      # 2（第0行第1列）
print(arr[:, 0])       # [1, 4]（所有行的第0列）

# 数学运算
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)           # [5, 7, 9]
print(a * b)           # [4, 10, 18]
print(np.dot(a, b))    # 32（点积）
```

## Pandas 基础

### Series 和 DataFrame

```python
import pandas as pd

# 创建 Series
s = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])

# 创建 DataFrame
df = pd.DataFrame({
    '姓名': ['Alice', 'Bob', 'Charlie'],
    '年龄': [25, 30, 35],
    '城市': ['北京', '上海', '广州']
})
```

### 数据读取

```python
# 读取 CSV
df = pd.read_csv('data.csv')

# 读取 Excel
df = pd.read_excel('data.xlsx')

# 读取 JSON
df = pd.read_json('data.json')
```

### 数据操作

```python
# 查看数据
print(df.head())       # 前5行
print(df.info())       # 数据信息
print(df.describe())   # 统计摘要

# 选择数据
print(df['姓名'])      # 选择列
print(df.iloc[0])      # 按位置选择行
print(df.loc[0:2])     # 按标签选择行

# 筛选数据
filtered = df[df['年龄'] > 25]

# 添加列
df['薪资'] = [10000, 15000, 20000]

# 分组统计
grouped = df.groupby('城市')['年龄'].mean()
```

## 实际应用示例

```python
import numpy as np
import pandas as pd

# 创建示例数据
np.random.seed(42)
data = pd.DataFrame({
    '日期': pd.date_range('2026-01-01', periods=100),
    '销售额': np.random.randint(1000, 5000, 100),
    '成本': np.random.randint(500, 3000, 100)
})

# 计算利润
data['利润'] = data['销售额'] - data['成本']

# 按月统计
monthly = data.resample('M', on='日期').agg({
    '销售额': 'sum',
    '成本': 'sum',
    '利润': 'sum'
})

print(monthly)
```

## 总结

NumPy 和 Pandas 是数据科学的基石：

- NumPy 适合数值计算，处理多维数组
- Pandas 适合数据分析，处理表格数据

掌握这两个库，你就有了数据科学的基础工具。

## 参考资料

- [NumPy 官方文档](https://numpy.org/doc/)
- [Pandas 官方文档](https://pandas.pydata.org/docs/)
