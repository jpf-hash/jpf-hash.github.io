# jpf-hash's Blog

一个关于机器学习、Python 和数据科学的技术博客。

## 技术栈

- [Astro](https://astro.build/) v6 — 现代静态站点生成器
- [Astro Paper](https://github.com/satnaing/astro-paper) v6 — 博客主题
- [Tailwind CSS](https://tailwindcss.com/) v4 — 实用优先的 CSS 框架
- [Pagefind](https://pagefind.app/) — 静态搜索方案
- [GitHub Pages](https://pages.github.com/) — 托管平台

## 本地开发

```bash
# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev

# 构建（包含 Pagefind 索引）
pnpm build

# 预览构建结果
pnpm preview
```

## 写文章

在 `src/content/posts/` 目录下创建 `.md` 或 `.mdx` 文件：

```markdown
---
title: "文章标题"
description: "文章描述"
pubDatetime: 2026-05-31T10:00:00+08:00
tags: ["python", "machine-learning"]
category: "技术"
featured: false
draft: false
---

文章内容...
```

### Frontmatter 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | ✅ | 文章标题 |
| description | string | ✅ | 文章描述 |
| pubDatetime | date | ✅ | 发布日期（ISO 8601） |
| modDatetime | date | ❌ | 修改日期 |
| tags | string[] | ❌ | 标签，默认 `["others"]` |
| category | string | ❌ | 分类，默认 `"未分类"` |
| featured | boolean | ❌ | 是否精选 |
| draft | boolean | ❌ | 是否草稿 |
| author | string | ❌ | 作者 |

### 文章目录

在文章中添加 `## 目录` 标题，会自动生成可折叠的目录。

## 部署

博客通过 GitHub Actions 自动部署到 GitHub Pages。推送到 `main` 分支即可触发部署。

## 项目结构

```
├── public/                    # 静态资源
├── src/
│   ├── assets/icons/          # SVG 图标
│   ├── components/            # Astro 组件
│   ├── content/
│   │   ├── pages/             # 独立页面（关于等）
│   │   └── posts/             # 博客文章
│   ├── i18n/                  # 国际化
│   ├── layouts/               # 布局组件
│   ├── pages/                 # 页面路由
│   ├── styles/                # 样式文件
│   └── utils/                 # 工具函数
├── astro-paper.config.ts      # 博客配置
└── astro.config.ts            # Astro 配置
```

## 许可证

MIT License
