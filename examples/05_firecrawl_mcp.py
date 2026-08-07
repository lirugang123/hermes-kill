#!/usr/bin/env python3
"""
示例5: 使用Firecrawl MCP
集成Firecrawl API进行爬取
"""

import asyncio
import json
import os

async def crawl_with_firecrawl(url: str, api_key: str):
    """使用Firecrawl爬取"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 单页爬取
    response = requests.post(
        "https://api.firecrawl.dev/v1/scrape",
        headers=headers,
        json={
            "url": url,
            "formats": ["markdown", "html"]
        },
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

async def crawl_multiple(urls: list, api_key: str):
    """批量爬取"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        "https://api.firecrawl.dev/v1/crawl",
        headers=headers,
        json={
            "urls": urls,
            "limit": len(urls),
            "scrapeOptions": {
                "formats": ["markdown"]
            }
        },
        timeout=60
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

async def search_with_firecrawl(query: str, api_key: str):
    """搜索"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        "https://api.firecrawl.dev/v1/search",
        headers=headers,
        json={
            "query": query,
            "limit": 10
        },
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

if __name__ == "__main__":
    api_key = os.getenv("FIRECRAWL_API_KEY")
    
    if not api_key:
        print("Please set FIRECRAWL_API_KEY environment variable")
        exit(1)
    
    # 测试单页爬取
    result = asyncio.run(crawl_with_firecrawl("https://example.com", api_key))
    print(json.dumps(result, indent=2, ensure_ascii=False))
