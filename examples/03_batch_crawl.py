#!/usr/bin/env python3
"""
示例3: 批量爬取任务
使用线程池并发爬取
"""

import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import time

async def fetch_session(session: aiohttp.ClientSession, url: str) -> dict:
    """异步获取页面"""
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

async def batch_crawl(urls: list, max_concurrent: int = 5) -> list:
    """批量爬取"""
    connector = aiohttp.TCPConnector(limit=max_concurrent)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_session(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]

def sync_batch_crawl(urls: list, max_workers: int = 5) -> list:
    """同步批量爬取"""
    import requests
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        def crawl(url):
            try:
                response = requests.get(url, timeout=10)
                return {
                    'url': url,
                    'status': response.status_code,
                    'length': len(response.text),
                    'success': True
                }
            except Exception as e:
                return {
                    'url': url,
                    'status': 0,
                    'error': str(e),
                    'success': False
                }
        
        results = list(executor.map(crawl, urls))
    
    return results

if __name__ == "__main__":
    urls = [
        "https://example.com/1",
        "https://example.com/2",
        "https://example.com/3",
    ]
    
    # 同步方式
    start = time.time()
    results = sync_batch_crawl(urls)
    print(f"Sync took {time.time() - start:.2f}s")
    
    for r in results:
        print(f"  {r['url']}: {r['status']}")
