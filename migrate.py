#!/usr/bin/env python3
"""Migrate articles from old Hexo blog to new one."""

import json
import os
import re
from html.parser import HTMLParser

OLD_BLOG_DIR = "D:/Environment/AIworks/jpf-hash.github.io"
NEW_POSTS_DIR = "D:/Environment/AIworks/hexo-blog/source/_posts"

class ArticleExtractor(HTMLParser):
    """Extract article content from Hexo HTML."""

    def __init__(self):
        super().__init__()
        self.in_article = False
        self.in_content = False
        self.depth = 0
        self.content = []
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'article':
            self.in_article = True
            self.depth = 0
        if self.in_article:
            self.depth += 1
            self.current_tag = tag
            if tag == 'div' and 'article-entry' in attrs_dict.get('class', ''):
                self.in_content = True

    def handle_endtag(self, tag):
        if self.in_article:
            self.depth -= 1
            if self.depth <= 0:
                self.in_article = False
                self.in_content = False

    def handle_data(self, data):
        if self.in_content and self.current_tag not in self.skip_tags:
            text = data.strip()
            if text:
                self.content.append(text)

def extract_article_content(html_path):
    """Extract text content from HTML file."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Try multiple patterns to find article content
        content_html = None

        # Pattern 1: article-entry div
        match = re.search(r'<div class="article-entry"[^>]*>(.*?)</div>\s*<!--\s*<div class="article-info"',
                         html, re.DOTALL)
        if match:
            content_html = match.group(1)
        else:
            # Pattern 2: article body
            match = re.search(r'<div class="article-body"[^>]*>(.*?)</div>\s*</article>',
                             html, re.DOTALL)
            if match:
                content_html = match.group(1)
            else:
                # Pattern 3: main content between article tags
                match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
                if match:
                    content_html = match.group(1)

        if content_html:
            # Convert HTML to markdown-like format
            content = content_html

            # Remove Hexo header/metadata sections
            content = re.sub(r'<h1 class="article-title">.*?</h1>', '', content, flags=re.DOTALL)
            content = re.sub(r'<div class="article-meta">.*?</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'<span class="article-date">.*?</span>', '', content, flags=re.DOTALL)
            content = re.sub(r'<div class="article-info">.*?</div>', '', content, flags=re.DOTALL)

            # Handle code blocks first
            content = re.sub(r'<pre><code class="([^"]*)">(.*?)</code></pre>',
                           lambda m: f'```{m.group(1).replace("language-", "")}\n{m.group(2)}\n```',
                           content, flags=re.DOTALL)

            # Handle headings
            for i in range(6, 0, -1):
                content = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>',
                               lambda m, level=i: f'{"#" * level} {m.group(1)}\n',
                               content, flags=re.DOTALL)

            # Handle other elements
            content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
            content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)
            content = re.sub(r'<br\s*/?>', '\n', content)
            content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>', r'![\2](\1)', content)
            content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', r'![image](\1)', content)
            content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
            content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL)
            content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
            content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
            content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
            content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
            content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n', content, flags=re.DOTALL)

            # Handle tables (basic)
            content = re.sub(r'<table[^>]*>(.*?)</table>', r'\n[表格内容]\n', content, flags=re.DOTALL)

            # Remove remaining HTML tags
            content = re.sub(r'<[^>]+>', '', content)

            # Clean up whitespace
            content = re.sub(r'\n{3,}', '\n\n', content)
            content = re.sub(r' +', ' ', content)

            # Decode HTML entities
            content = content.replace('&amp;', '&')
            content = content.replace('&lt;', '<')
            content = content.replace('&gt;', '>')
            content = content.replace('&quot;', '"')
            content = content.replace('&#39;', "'")

            return content.strip()
    except Exception as e:
        print(f"Error extracting {html_path}: {e}")
    return ""

def create_post(title, date, tags, content, path):
    """Create a markdown post file."""
    # Clean title for filename - keep Chinese characters
    safe_title = re.sub(r'[<>:"/\\|?*]', '-', title)
    safe_title = safe_title.strip()

    # Format date
    date_str = date.replace('T', ' ').replace('.000Z', '')

    # Create frontmatter
    frontmatter = f"""---
title: {title}
date: {date_str}
tags: [{', '.join(tags)}]
categories: []
---
"""

    # Create file
    filename = f"{safe_title}.md"
    filepath = os.path.join(NEW_POSTS_DIR, filename)

    # Check if file already exists
    if os.path.exists(filepath):
        print(f"Skipping (exists): {filename}")
        return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write('\n')
        if content:
            f.write(content)
        else:
            f.write(f"<!-- 请从旧博客迁移内容 -->\n")
            f.write(f"<!-- 原文路径: {path} -->\n")

    print(f"Created: {filename}")

def main():
    # Read content.json
    with open(os.path.join(OLD_BLOG_DIR, 'content.json'), 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Found {len(articles)} articles to migrate")

    # Process each article
    for article in articles:
        title = article['title']
        date = article['date']
        path = article['path']
        tags = [tag['name'] for tag in article.get('tags', [])]

        # Find HTML file
        html_path = os.path.join(OLD_BLOG_DIR, path, 'index.html')

        if os.path.exists(html_path):
            content = extract_article_content(html_path)
            create_post(title, date, tags, content, path)
        else:
            print(f"HTML not found for: {title}")
            create_post(title, date, tags, "", path)

    print(f"\nMigration complete! {len(articles)} articles created.")

if __name__ == '__main__':
    main()
