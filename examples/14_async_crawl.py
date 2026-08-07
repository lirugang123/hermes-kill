#!/usr/bin/env python3
"""
示例14: 异步爬取
使用asyncio进行高效并发爬取
"""

import asyncio
import aiohttp
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_url(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> Dict:
    """获取单个URL"""
    async with semaphore:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                html = await resp.text()
                return {
                    'url': url,
                    'status': resp.status,
                    'length': len(html),
                    'success': True
                }
        except Exception as e:
            return {
                'url': url,
                'status': 0,
                'error': str(e),
                'success': False
            }

async def async_crawl(urls: List[str], max_concurrent: int = 10) -> List[Dict]:
    """异步批量爬取"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常
        clean_results = []
        for r in results:
            if isinstance(r, Exception):
                logger.error(f"Task failed: {r}")
            else:
                clean_results.append(r)
        
        return clean_results

def main():
    """主函数"""
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/get",
        "https://httpbin.org/get",
    ] * 5  # 15个任务
    
    results = asyncio.run(async_crawl(urls, max_concurrent=5))
    
    print(f"Successfully crawled: {len([r for r in results if r['success']])}")
    print(f"Failed: {len([r for r in results if not r['success']])}")
    
    for r in results[:3]:
        print(f"  {r['url']}: {r['status']}")

if __name__ == "__main__":
    main()
