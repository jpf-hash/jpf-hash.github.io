#!/usr/bin/env python3
"""Migrate articles from old Hexo blog to new one - improved version."""

import json
import os
import re

OLD_BLOG_DIR = "D:/Environment/AIworks/jpf-hash.github.io"
NEW_POSTS_DIR = "D:/Environment/AIworks/hexo-blog/source/_posts"

def clean_html_to_markdown(html):
    """Convert HTML content to clean Markdown."""
    if not html:
        return ""

    content = html

    # Remove Hexo-specific elements
    content = re.sub(r'<h1 class="article-title">.*?</h1>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="article-meta">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="article-info">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<span class="article-date">.*?</span>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="article-tag">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="article-header">.*?</div>', '', content, flags=re.DOTALL)

    # Remove navigation and footer elements
    content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL)

    # Handle code blocks - preserve language info
    content = re.sub(
        r'<pre><code class="language-(\w+)">(.*?)</code></pre>',
        lambda m: f'\n```{m.group(1)}\n{m.group(2).strip()}\n```\n',
        content, flags=re.DOTALL
    )
    content = re.sub(
        r'<pre><code>(.*?)</code></pre>',
        lambda m: f'\n```\n{m.group(1).strip()}\n```\n',
        content, flags=re.DOTALL
    )

    # Handle inline code
    content = re.sub(r'<code>(.*?)</code>', r'`\1`', content, flags=re.DOTALL)

    # Handle headings
    for i in range(6, 0, -1):
        content = re.sub(
            rf'<h{i}[^>]*>(.*?)</h{i}>',
            lambda m, level=i: f'\n{"#" * level} {m.group(1).strip()}\n',
            content, flags=re.DOTALL
        )

    # Handle paragraphs
    content = re.sub(r'<p>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)

    # Handle lists
    content = re.sub(r'<li>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\1\n', content, flags=re.DOTALL)
    content = re.sub(r'<ol[^>]*>(.*?)</ol>', r'\1\n', content, flags=re.DOTALL)

    # Handle blockquotes
    content = re.sub(r'<blockquote>(.*?)</blockquote>', lambda m: f'> {m.group(1).strip()}\n', content, flags=re.DOTALL)

    # Handle images - use relative paths
    content = re.sub(
        r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*/?>',
        lambda m: f'![{m.group(2)}]({m.group(1)})',
        content
    )
    content = re.sub(
        r'<img[^>]*src="([^"]*)"[^>]*/?>',
        lambda m: f'![image]({m.group(1)})',
        content
    )

    # Handle links
    content = re.sub(
        r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
        lambda m: f'[{m.group(2).strip()}]({m.group(1)})',
        content, flags=re.DOTALL
    )

    # Handle emphasis
    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<b>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<i>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)

    # Handle line breaks
    content = re.sub(r'<br\s*/?>', '\n', content)
    content = re.sub(r'<hr\s*/?>', '\n---\n', content)

    # Handle tables (basic)
    content = re.sub(r'<table[^>]*>(.*?)</table>', '\n[表格内容]\n', content, flags=re.DOTALL)

    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)

    # Decode HTML entities
    entities = {
        '&amp;': '&', '&lt;': '<', '&gt;': '>',
        '&quot;': '"', '&#39;': "'", '&nbsp;': ' ',
        '&hellip;': '…', '&mdash;': '—', '&ndash;': '–',
        '&copy;': '©', '&reg;': '®'
    }
    for entity, char in entities.items():
        content = content.replace(entity, char)

    # Clean up whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'[ \t]+', ' ', content)
    content = re.sub(r'\n \n', '\n\n', content)

    # Remove anchor links from headings
    content = re.sub(r'\[#[^\]]*\]', '', content)

    # Remove empty lines at the beginning
    content = content.strip()

    return content

def extract_article_content(html_path):
    """Extract article content from HTML file."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Try to find article content
        content_html = None

        # Pattern 1: article-entry div
        match = re.search(
            r'<div class="article-entry"[^>]*>(.*?)</div>\s*(?:<!--|<div class="(?:article-info|article-tag|article-nav)")',
            html, re.DOTALL
        )
        if match:
            content_html = match.group(1)
        else:
            # Pattern 2: Look for content between specific markers
            match = re.search(r'<div class="article-entry"[^>]*>(.*)', html, re.DOTALL)
            if match:
                content_html = match.group(1)
                # Find the end
                end_match = re.search(r'</div>\s*(?:<!--|<div class="(?:article-info|article-tag|article-nav))', content_html)
                if end_match:
                    content_html = content_html[:end_match.start()]

        if content_html:
            return clean_html_to_markdown(content_html)

    except Exception as e:
        print(f"Error extracting {html_path}: {e}")

    return ""

def create_post(title, date, tags, content, path):
    """Create a markdown post file."""
    # Clean title for filename
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

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write('\n')
        if content:
            f.write(content)
        else:
            f.write(f"<!-- 请补充内容 -->\n")
            f.write(f"<!-- 原文路径: {path} -->\n")

    return filename

def main():
    # Read content.json
    with open(os.path.join(OLD_BLOG_DIR, 'content.json'), 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Found {len(articles)} articles to migrate")

    # Clear existing posts
    for f in os.listdir(NEW_POSTS_DIR):
        if f.endswith('.md'):
            os.remove(os.path.join(NEW_POSTS_DIR, f))

    # Process each article
    success_count = 0
    for article in articles:
        title = article['title']
        date = article['date']
        path = article['path']
        tags = [tag['name'] for tag in article.get('tags', [])]

        # Find HTML file
        html_path = os.path.join(OLD_BLOG_DIR, path, 'index.html')

        if os.path.exists(html_path):
            content = extract_article_content(html_path)
            filename = create_post(title, date, tags, content, path)
            if content:
                success_count += 1
                print(f"[OK] {filename}")
            else:
                print(f"[EMPTY] {filename}")
        else:
            filename = create_post(title, date, tags, "", path)
            print(f"[SKIP] {filename}")

    print(f"\nMigration complete! {success_count}/{len(articles)} articles extracted successfully.")

if __name__ == '__main__':
    main()
