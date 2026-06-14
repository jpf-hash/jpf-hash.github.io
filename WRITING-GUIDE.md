# 博客写作指南

## 快速开始

1. 复制模板文件：
   ```bash
   cp src/content/posts/_TEMPLATE.md src/content/posts/你的文章标题.md
   ```

2. 编辑新文件，填写内容

3. 本地预览：
   ```bash
   pnpm dev
   # 打开 http://localhost:4321
   ```

4. 发布：
   ```bash
   git add .
   git commit -m "新文章：你的文章标题"
   git push origin main
   ```

## Frontmatter 字段说明

```yaml
---
title: "文章标题"           # 必填：文章标题
description: "文章描述"     # 必填：简短描述（显示在列表和搜索结果中）
pubDatetime: 2026-05-31T10:00:00+08:00  # 必填：发布日期时间
# modDatetime: 2026-05-31T12:00:00+08:00  # 可选：修改日期
tags: ["python", "机器学习"]  # 标签数组
category: "技术"             # 分类
featured: false              # true = 在首页精选区域显示
draft: false                 # true = 草稿，不会发布
# author: "jpf-hash"         # 可选：覆盖默认作者
---
```

## 可用分类

- `技术` — 技术文章
- `日记` — 个人随笔
- `工具` — 工具介绍
- `其他` — 其他内容

## 常用标签

- Python 相关：`python`, `pandas`, `numpy`, `matplotlib`
- 机器学习：`机器学习`, `深度学习`, `算法`, `分类`, `回归`
- 数据科学：`数据科学`, `数据分析`, `数据可视化`
- 工具：`git`, `linux`, `vim`, `docker`
- 其他：`随笔`, `教程`, `笔记`

## 文章结构建议

```markdown
---
frontmatter...
---

## Table of contents

<!-- 自动生成目录，不需要可删除 -->

## 引言

简要介绍文章主题

## 正文

主要内容，可以有多个 h2 标题

### 子标题

更详细的内容

## 总结

总结要点

## 参考资料

相关链接
```

## 可选模板

文章目录里还放了几个以下划线开头的模板文件，它们不会被发布：

- `src/content/posts/_technical-note-template.md`：技术笔记
- `src/content/posts/_project-review-template.md`：项目复盘
- `src/content/posts/_debug-note-template.md`：踩坑记录
- `src/content/posts/_paper-reading-template.md`：论文阅读

使用方式：

```bash
cp src/content/posts/_project-review-template.md src/content/posts/my-project-review.md
```

## 代码块

支持语法高亮和复制按钮：

````markdown
```python
# Python 代码
def hello():
    print("Hello!")
```

```javascript
// JavaScript 代码
console.log("Hello!");
```

```bash
# Shell 命令
npm install
```
````

## 图片

将图片放在 `public/images/` 目录下，然后引用：

```markdown
![图片描述](/images/your-image.png)
```

## 链接

```markdown
[链接文字](https://example.com)
```

## 表格

```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 内容1 | 内容2 | 内容3 |
```

## 注意事项

- 文件名会成为 URL 的一部分，建议使用英文和连字符
- 例如：`python-basics.md` → `/posts/python-basics`
- `draft: true` 的文章不会显示在网站上
- 发布后需要等待 GitHub Actions 部署完成（约 1-2 分钟）
