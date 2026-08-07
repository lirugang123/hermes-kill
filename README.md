# Hermes Kill — 多功能爬虫工具包

## 概述

Hermes Kill 是一个整合多种爬虫技术的实用工具包，专为 Hermes Agent 设计。本仓库包含原创的 `web-crawler-toolkit` 技能，提供场景化的网页数据采集方案。

## 技能介绍

### 技能名称
`web-crawler-toolkit`

### 版本
1.0.0

### 作者
lirugang123

### 许可
MIT

## 用途

本技能适用于以下场景：

- **批量网页数据采集**：从多个URL提取结构化数据
- **反爬网站处理**：应对各种反爬虫机制
- **JavaScript渲染页面**：处理动态加载的内容
- **大规模数据抓取**：高效处理大量URL
- **搜索引擎数据提取**：获取搜索结果并解析内容

## 核心功能

### 1. 多工具整合

| 工具 | 用途 | 优势 |
|------|------|------|
| curl + 正则 | 静态页面抓取 | 快速、轻量、无依赖 |
| Playwright | 浏览器自动化 | 支持JS渲染、登录态 |
| Firecrawl MCP | 大规模爬取 | 26个工具、稳定可靠 |
| 9router | 任务分发 | 并发控制、队列管理 |

### 2. 场景化方案

**静态HTML页面**
- 推荐使用：curl + Python正则
- 适用场景：服务端渲染、无登录要求
- 优势：速度快、资源消耗低

**JavaScript渲染页面**
- 推荐使用：Playwright
- 适用场景：SPA应用、动态内容
- 优势：完整浏览器环境

**大规模爬取任务**
- 推荐使用：Firecrawl MCP
- 适用场景：全站爬取、批量处理
- 优势：26个工具、MCP集成

### 3. 反爬策略

**请求头伪装**
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Accept': 'text/html,application/xhtml+xml...',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
```

**频率控制**
```python
import random, time
time.sleep(random.uniform(1, 3))
```

**IP轮换**
```python
proxies = ['http://proxy1:8080', 'http://proxy2:8080']
proxy = random.choice(proxies)
```

**Cookie管理**
```python
# 保存和恢复Cookie
cookies = context.cookies()
context.add_cookies(cookies)
```

### 4. 性能优化

**并发控制**
- ThreadPoolExecutor管理并发
- 可配置worker数量
- 自动错误处理

**缓存策略**
- LRU缓存减少重复请求
- URL哈希作为缓存键
- 可配置缓存大小

**重试机制**
- 指数退避策略
- 可配置重试次数
- 自动跳过失败任务

## 代码示例

### 轻量级抓取（curl + Python）

```python
import urllib.request
import re

def crawl_simple(url, patterns):
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0...'}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
    
    results = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, html)
        results[field] = match.group(1) if match else None
    return results

# 使用示例
data = crawl_simple(
    'https://example.com',
    {'title': r'<title>(.*?)</title>'}
)
```

### 浏览器自动化（Playwright）

```python
from playwright.sync_api import sync_playwright

def crawl_with_browser(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        content = page.inner_text('.main-content')
        browser.close()
        return content
```

### Firecrawl MCP集成

```bash
# 单页抓取
mcp__mcp_firecrawl__firecrawl_scrape \
  --url "https://example.com" \
  --formats markdown

# 搜索抓取
mcp__mcp_firecrawl__firecrawl_search \
  --query "site:example.com topic" \
  --limit 10
```

## 文件结构

```
hermes-kill/
├── README.md              # 本文件
└── web-crawler-toolkit/
    └── SKILL.md           # 技能定义文件（424行）
```

## 安装使用

### 本地安装

技能文件已包含在仓库中，可直接使用：

```bash
# 查看技能
hermes skill show web-crawler-toolkit

# 测试技能
hermes skill test web-crawler-toolkit
```

### 仓库克隆

```bash
# SSH方式（推荐）
git clone git@github.com:lirugang123/hermes-kill.git

# HTTPS方式
git clone https://github.com/lirugang123/hermes-kill.git
```

## 技术栈

- **Python 3.11+**：主要开发语言
- **Playwright**：浏览器自动化
- **Firecrawl MCP**：网页爬取
- **9router**：任务分发
- **SQLite**：数据存储

## 依赖工具

- Firecrawl MCP（26个工具）
- Playwright v1.62.0
- 9router v0.5.50
- Python requests
- Python re（正则表达式）

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

## 更新日志

### v1.0.0（2026-08-07）
- 初始版本发布
- 整合Firecrawl/Playwright/9router
- 提供完整反爬策略
- 包含可运行代码示例

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- GitHub: [lirugang123](https://github.com/lirugang123)
- 邮箱: lirugang123@qq.com

## 致谢

感谢以下开源项目：
- [Firecrawl](https://github.com/firecrawl/firecrawl)
- [Playwright](https://github.com/microsoft/playwright)
- [9router](https://github.com/xxx/9router)

---

**Made with ❤️ by lirugang123**
