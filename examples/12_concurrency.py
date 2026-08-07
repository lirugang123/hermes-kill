#!/usr/bin/env python3
"""
示例12: 并发控制
使用信号量和队列控制并发
"""

import asyncio
import aiohttp
from asyncio import Semaphore
from typing import List, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConcurrencyController:
    """并发控制器"""
    
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.semaphore = Semaphore(max_concurrent)
        self.active_count = 0
        self.lock = asyncio.Lock()
    
    async def fetch_with_limit(self, session: aiohttp.ClientSession, url: str) -> dict:
        """带限制的获取"""
        async with self.semaphore:
            async with self.lock:
                self.active_count += 1
                logger.debug(f"Active tasks: {self.active_count}/{self.max_concurrent}")
            
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
            finally:
                async with self.lock:
                    self.active_count -= 1
    
    async def fetch_all(self, urls: List[str]) -> List[dict]:
        """批量获取"""
        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.fetch_with_limit(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return [r for r in results if not isinstance(r, Exception)]

class PriorityQueue:
    """优先级队列"""
    
    def __init__(self):
        self.queue = []
    
    def push(self, item: tuple):
        """添加项（优先级，项目）"""
        self.queue.append(item)
        self.queue.sort(key=lambda x: x[0])  # 按优先级排序
    
    def pop(self) -> tuple:
        """弹出最高优先级项"""
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def is_empty(self) -> bool:
        return len(self.queue) == 0
    
    def size(self) -> int:
        return len(self.queue)

def main():
    """主函数"""
    import asyncio
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]
    
    controller = ConcurrencyController(max_concurrent=2)
    
    async def run():
        results = await controller.fetch_all(urls)
        for r in results:
            print(f"{r['url']}: {r['status']}")
    
    asyncio.run(run())

if __name__ == "__main__":
    asyncio.run(main())
