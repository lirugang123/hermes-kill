#!/usr/bin/env python3
"""
9router任务分发器
用于批量爬取任务调度
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Optional
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CrawlTask:
    """爬取任务"""
    url: str
    priority: int = 0
    retries: int = 0
    max_retries: int = 3
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class TaskRouter:
    """任务路由器"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.task_queue: List[CrawlTask] = []
        self.results: dict = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def add_task(self, task: CrawlTask):
        """添加任务"""
        self.task_queue.append(task)
        logger.info(f"Added task: {task.url} (priority: {task.priority})")
    
    def add_tasks(self, tasks: List[CrawlTask]):
        """批量添加任务"""
        for task in tasks:
            self.add_task(task)
        logger.info(f"Added {len(tasks)} tasks")
    
    def process_task(self, task: CrawlTask, processor: Callable) -> dict:
        """处理单个任务"""
        try:
            result = processor(task.url)
            self.results[task.url] = {
                "status": "success",
                "result": result,
                "retries": task.retries
            }
            logger.info(f"Task completed: {task.url}")
            return result
        except Exception as e:
            task.retries += 1
            logger.warning(f"Task failed: {task.url} (retry {task.retries}/{task.max_retries})")
            
            if task.retries < task.max_retries:
                self.add_task(task)
                return {"error": str(e), "retried": True}
            else:
                self.results[task.url] = {
                    "status": "failed",
                    "error": str(e),
                    "retries": task.retries
                }
                return {"error": str(e), "retried": False}
    
    def run_batch(self, processor: Callable, urls: List[str]):
        """批量运行任务"""
        # 创建任务
        tasks = [CrawlTask(url=url) for url in urls]
        self.add_tasks(tasks)
        
        # 使用线程池处理
        futures = []
        for task in self.task_queue:
            future = self.executor.submit(self.process_task, task, processor)
            futures.append(future)
        
        # 等待所有任务完成
        for future in as_completed(futures):
            try:
                result = future.result()
                logger.debug(f"Result: {result}")
            except Exception as e:
                logger.error(f"Future exception: {e}")
        
        return self.results
    
    def run_async(self, processor: Callable, urls: List[str]):
        """异步批量运行"""
        async def _run():
            tasks = [self._async_task(url, processor) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return dict(zip(urls, results))
        
        return asyncio.run(_run())
    
    async def _async_task(self, url: str, processor: Callable):
        """异步处理单个任务"""
        try:
            result = await asyncio.to_thread(processor, url)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        total = len(self.task_queue)
        success = sum(1 for r in self.results.values() if r.get("status") == "success")
        failed = sum(1 for r in self.results.values() if r.get("status") == "failed")
        
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": f"{success/total*100:.1f}%" if total > 0 else "0%"
        }

def main():
    """主函数"""
    router = TaskRouter(max_workers=3)
    
    # 示例：批量爬取
    urls = [
        "https://example.com/1",
        "https://example.com/2",
        "https://example.com/3"
    ]
    
    # 定义处理器
    def process_url(url):
        logger.info(f"Processing {url}")
        return {"url": url, "content": "sample"}
    
    # 运行批处理
    results = router.run_batch(process_url, urls)
    
    # 打印统计
    stats = router.get_stats()
    logger.info(f"Stats: {stats}")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    import json
    main()
