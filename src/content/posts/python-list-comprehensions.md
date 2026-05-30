---
title: "Python 列表推导式：优雅地创建列表"
description: "列表推导式是 Python 最强大的特性之一，让代码更简洁、更 Pythonic。"
pubDatetime: 2026-05-28T16:00:00+08:00
tags: ["python", "技巧", "代码优化"]
category: "技术"
featured: false
draft: false
---

## Table of contents

## 什么是列表推导式？

列表推导式（List Comprehension）是 Python 中创建列表的简洁语法。它可以将多行代码压缩成一行。

### 基本语法

```python
# 传统方式
squares = []
for x in range(10):
    squares.append(x ** 2)

# 列表推导式
squares = [x ** 2 for x in range(10)]
```

## 基础用法

### 简单转换

```python
# 字符串转大写
words = ['hello', 'world', 'python']
upper_words = [w.upper() for w in words]
# ['HELLO', 'WORLD', 'PYTHON']

# 数字运算
numbers = [1, 2, 3, 4, 5]
doubled = [n * 2 for n in numbers]
# [2, 4, 6, 8, 10]
```

### 带条件筛选

```python
# 筛选偶数
numbers = range(10)
evens = [x for x in numbers if x % 2 == 0]
# [0, 2, 4, 6, 8]

# 筛选长度大于3的单词
words = ['hi', 'hello', 'hey', 'python']
long_words = [w for w in words if len(w) > 3]
# ['hello', 'python']
```

## 进阶用法

### 嵌套循环

```python
# 展平二维列表
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 生成坐标对
coords = [(x, y) for x in range(3) for y in range(3)]
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
```

### 条件表达式

```python
# 使用 if-else
numbers = range(10)
labels = ['偶数' if x % 2 == 0 else '奇数' for x in numbers]
# ['偶数', '奇数', '偶数', '奇数', ...]

# 复杂条件
scores = [85, 92, 45, 78, 96, 60]
results = ['及格' if s >= 60 else '不及格' for s in scores]
```

### 函数调用

```python
# 应用函数
def square(x):
    return x ** 2

numbers = [1, 2, 3, 4, 5]
squared = [square(x) for x in numbers]

# 使用 lambda
squared = [(lambda x: x ** 2)(x) for x in numbers]

# 更简洁的方式
squared = [x ** 2 for x in numbers]
```

## 实际应用

### 数据处理

```python
# 提取字典中的特定字段
users = [
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 30},
    {'name': 'Charlie', 'age': 35}
]
names = [user['name'] for user in users]
# ['Alice', 'Bob', 'Charlie']

# 筛选并转换
adult_names = [user['name'] for user in users if user['age'] >= 30]
# ['Bob', 'Charlie']
```

### 文件处理

```python
# 读取文件行并去除空白
with open('data.txt', 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# 解析 CSV 行
csv_lines = ['Alice,25', 'Bob,30', 'Charlie,35']
users = [{'name': line.split(',')[0], 'age': int(line.split(',')[1])} 
         for line in csv_lines]
```

### 数学计算

```python
# 生成乘法表
multiplication = [i * j for i in range(1, 10) for j in range(1, 10)]

# 计算阶乘
factorials = [1]
[factorials.append(factorials[-1] * i) for i in range(1, 11)]
# [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
```

## 其他推导式

### 字典推导式

```python
# 创建字典
squares = {x: x ** 2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 反转字典
original = {'a': 1, 'b': 2, 'c': 3}
reversed_dict = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}
```

### 集合推导式

```python
# 去重
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = {x for x in numbers}
# {1, 2, 3, 4}
```

### 生成器表达式

```python
# 生成器（惰性计算）
sum_of_squares = sum(x ** 2 for x in range(1000000))
# 不会一次性创建所有元素，节省内存
```

## 性能对比

列表推导式通常比等效的 for 循环更快：

```python
import timeit

# for 循环
def with_loop():
    result = []
    for x in range(1000):
        result.append(x ** 2)
    return result

# 列表推导式
def with_comprehension():
    return [x ** 2 for x in range(1000)]

# 测试
print(timeit.timeit(with_loop, number=1000))        # 约 0.15 秒
print(timeit.timeit(with_comprehension, number=1000)) # 约 0.08 秒
```

## 最佳实践

### 保持简洁

```python
# ❌ 过于复杂
result = [x ** 2 if x > 0 else -x ** 2 if x < 0 else 0 for x in numbers]

# ✅ 拆分逻辑
def transform(x):
    if x > 0:
        return x ** 2
    elif x < 0:
        return -x ** 2
    return 0

result = [transform(x) for x in numbers]
```

### 避免副作用

```python
# ❌ 在推导式中修改外部状态
results = []
[results.append(x ** 2) for x in range(10)]  # 不推荐

# ✅ 直接赋值
results = [x ** 2 for x in range(10)]
```

### 可读性优先

```python
# ❌ 一行太长
result = [some_complex_function(x, y) for x in range(10) for y in range(10) if some_condition(x, y)]

# ✅ 换行显示
result = [
    some_complex_function(x, y)
    for x in range(10)
    for y in range(10)
    if some_condition(x, y)
]
```

## 总结

列表推导式是 Python 的强大特性：

- **简洁** — 一行代码完成多行逻辑
- **快速** — 比 for 循环更高效
- **Pythonic** — 符合 Python 风格

但要注意：
- 不要过度复杂化
- 保持代码可读性
- 适当拆分复杂逻辑

## 练习

```python
# 练习1：生成 1-100 中能被 3 整除的数的平方
# 练习2：将字符串列表转换为小写并去除空白
# 练习3：创建一个字典，键为 1-10，值为键的立方
```
