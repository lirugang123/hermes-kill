---
name: web-crawler-toolkit
description: "整合Firecrawl/Playwright/9router的多功能爬虫工具包 — 网页抓取、数据提取、批量处理、反爬策略"
version: 1.0.0
author: lirugang123
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [web-crawler, scraping, automation, firecrawl, playwright, data-extraction]
    related_skills: [firecrawl, automation]
---

# Web Crawler Toolkit — 多功能爬虫工具包

## 概述

整合多种爬虫技术的实用工具包，适用于不同场景的数据采集需求。区别于单一工具，本技能提供组合方案和反爬策略。

## 触发场景

- 需要批量抓取网页数据
- 处理有反爬机制的网站
- 需要JavaScript渲染的页面
- 批量处理多个URL
- 提取结构化数据

## 工具选择指南

| 场景 | 推荐工具 | 原因 |
|------|---------|------|
| 静态HTML页面 | curl + 正则 | 速度快，无依赖 |
| JavaScript渲染页面 | Playwright | 完整浏览器环境 |
| 大规模爬取 | Firecrawl MCP | 26个工具，稳定可靠 |
| 需要登录态 | 9router + Playwright | 支持Cookie管理 |
| 搜索引擎数据 | Firecrawl Search | 直接获取搜索结果 |

## 方案一：轻量级抓取（curl + Python）

适用于简单、无反爬的静态页面。

### 使用示例

```python
import urllib.request
import re
import json

def crawl_simple(url, patterns):
    """
    轻量级网页抓取
    patterns: 字典，键为字段名，值为正则表达式
    """
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    )
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    results = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, html)
        results[field] = match.group(1) if match else None
        
    return results

# 使用示例
data = crawl_simple(
    'https://example.com',
    {
        'title': r'<title>(.*?)</title>',
        'description': r'<meta name="description" content="(.*?)">',
        'price': r'price[^>]*>([\d.]+)'
    }
)
```

### 适用场景

- 服务端渲染的页面
- 无登录要求的公开数据
- 高频次抓取（需要速度）
- 数据量小的场景

## 方案二：浏览器自动化（Playwright）

适用于需要JavaScript渲染或登录态的页面。

### 基础使用

```python
from playwright.sync_api import sync_playwright

def crawl_with_browser(url, screenshots=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 访问页面
        page.goto(url, wait_until='networkidle')
        
        # 等待内容加载
        page.wait_for_selector('.content', timeout=10000)
        
        # 提取数据
        title = page.title()
        content = page.inner_text('.main-content')
        
        # 可选：截图
        if screenshots:
            page.screenshot(path='screenshot.png')
            
        browser.close()
        
        return {
            'title': title,
            'content': content
        }
```

### 高级技巧

**处理反爬检测：**

```python
# 模拟真实浏览器行为
page = browser.new_page(
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    viewport={'width': 1920, 'height': 1080}
)

# 添加随机延迟
import random
time.sleep(random.uniform(1, 3))

# 模拟滚动
page.evaluate('window.scrollBy(0, 1000)')
time.sleep(random.uniform(0.5, 1.5))
```

## 方案三：Firecrawl MCP集成

适用于大规模、稳定的数据采集。

### 工具清单（26个工具）

| 工具 | 用途 | 适用场景 |
|------|------|---------|
| scrape | 单页抓取 | 快速提取页面内容 |
| crawl | 多页爬取 | 站点级数据采集 |
| search | 搜索抓取 | 搜索引擎结果提取 |
| map | URL发现 | 站点结构分析 |
| extract | 结构化提取 | JSON格式数据提取 |

### 使用示例

```bash
# 单页抓取
mcp__mcp_firecrawl__firecrawl_scrape \
  --url "https://example.com" \
  --formats markdown

# 搜索抓取
mcp__mcp_firecrawl__firecrawl_search \
  --query "site:example.com topic" \
  --limit 10

# 批量爬取
mcp__mcp_firecrawl__firecrawl_crawl \
  --url "https://example.com" \
  --limit 50 \
  --scrape-options formats:markdown
```

## 反爬策略指南

### 1. 请求头伪装

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}
```

### 2. 请求频率控制

```python
import time
import random

def rate_limit(min_delay=1, max_delay=3):
    """随机延迟，模拟人类行为"""
    time.sleep(random.uniform(min_delay, max_delay))
```

### 3. IP轮换

```python
# 使用代理池
proxies = [
    'http://proxy1:8080',
    'http://proxy2:8080',
    'http://proxy3:8080',
]

import random
proxy = random.choice(proxies)
```

### 4. Cookie管理

```python
# 保存和恢复Cookie
context = browser.new_context()

# 导出Cookie
cookies = context.cookies()
with open('cookies.json', 'w') as f:
    json.dump(cookies, f)

# 导入Cookie
context.add_cookies(json.load(open('cookies.json')))
```

## 批量处理方案

### 使用9router分发任务

```python
import json

# 读取URL列表
with open('urls.json') as f:
    urls = json.load(f)

# 使用9router分发
from nine_router import Router

router = Router()

for url in urls[:10]:  # 限制批次
    router.enqueue(url, callback=process_result)
    
router.run()
```

### 使用Firecrawl批量抓取

```python
# 批量抓取任务
batch_urls = ['url1', 'url2', 'url3']

# 异步批量处理
for url in batch_urls:
    result = firecrawl.scrape_url(url)
    save_result(result)
```

## 数据后处理

### 清洗和结构化

```python
import re
from datetime import datetime

def clean_text(text):
    """清洗HTML文本"""
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 规范化空白
    text = re.sub(r'\s+', ' ', text)
    # 移除多余空格
    text = text.strip()
    return text

def extract_date(text):
    """提取日期"""
    match = re.search(r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})', text)
    if match:
        return datetime.strptime(match.group(1), '%Y-%m-%d')
    return None
```

### 保存到数据库

```python
import sqlite3

def save_to_db(data, db_path='crawler.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawled_data (
            id INTEGER PRIMARY KEY,
            url TEXT,
            title TEXT,
            content TEXT,
            crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    for item in data:
        cursor.execute(
            'INSERT INTO crawled_data (url, title, content) VALUES (?, ?, ?)',
            (item['url'], item['title'], item['content'][:1000])
        )
    
    conn.commit()
    conn.close()
```

## 性能优化

### 并发控制

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def batch_crawl(urls, max_workers=5):
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(crawl, url): url for url in urls}
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error crawling {futures[future]}: {e}")
                
    return results
```

### 缓存策略

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def crawl_cached(url):
    """带缓存的抓取"""
    # URL作为缓存键
    return do_crawl(url)

def get_cache_key(url):
    """生成缓存键"""
    return hashlib.md5(url.encode()).hexdigest()
```

## 错误处理

### 重试机制

```python
import time

def crawl_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            return do_crawl(url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避
```

### 超时控制

```python
# 设置超时
timeout = 10  # 秒

# 在Playwright中
page.goto(url, timeout=timeout * 1000)  # 毫秒

# 在requests中
response = requests.get(url, timeout=timeout)
```

## 最佳实践

1. **遵守robots.txt**
   - 检查网站爬虫规则
   - 尊重爬虫协议

2. **控制请求频率**
   - 避免对目标网站造成压力
   - 使用随机延迟

3. **数据合法性**
   - 仅抓取公开数据
   - 不抓取个人隐私信息
   - 遵守网站服务条款

4. **错误恢复**
   - 实现重试机制
   - 记录失败任务
   - 支持断点续传

## 相关工具

- **Firecrawl MCP**: 26个爬虫工具
- **Playwright**: 浏览器自动化
- **9router**: 任务分发
- **curl**: 轻量级HTTP请求
- **Python requests**: HTTP库

## 参考资料

- Firecrawl官方文档: https://docs.firecrawl.dev
- Playwright文档: https://playwright.dev
- Python requests文档: https://docs.python-requests.org
