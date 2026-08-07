#!/usr/bin/env python3
"""
Hermes Kill - Main Crawler Script
使用Firecrawl MCP进行网页爬取
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Optional

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FirecrawlCrawler:
    """基于Firecrawl MCP的网页爬取器"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.firecrawl.dev/v1"
    
    async def scrape(self, url: str, options: Optional[dict] = None) -> dict:
        """爬取单个页面"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": url,
            "formats": ["markdown", "html"],
            **(options or {})
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/scrape",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return {"error": str(e)}
    
    async def crawl(self, url: str, limit: int = 10, options: Optional[dict] = None) -> list:
        """爬取多个页面"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": url,
            "limit": limit,
            "scrapeOptions": {
                "formats": ["markdown"],
                **(options or {})
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/crawl",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            logger.error(f"Failed to crawl {url}: {e}")
            return []
    
    async def search(self, query: str, limit: int = 10) -> list:
        """搜索网页"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query,
            "limit": limit
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            logger.error(f"Failed to search {query}: {e}")
            return []

async def main():
    """主函数"""
    # 从环境变量读取API key
    import os
    api_key = os.getenv("FIRECRAWL_API_KEY")
    
    if not api_key:
        logger.error("FIRECRAWL_API_KEY not set")
        return
    
    crawler = FirecrawlCrawler(api_key)
    
    # 示例：爬取单个页面
    url = "https://example.com"
    logger.info(f"Scraping {url}...")
    
    result = await crawler.scrape(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
