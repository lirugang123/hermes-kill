#!/usr/bin/env python3
"""
URL管理器
管理URL队列和去重
"""

import hashlib
import logging
from collections import deque
from pathlib import Path
from typing import List, Optional, Set
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLManager:
    """URL管理器"""
    
    def __init__(self, max_urls: int = 10000):
        self.max_urls = max_urls
        self.queue: deque = deque()
        self.seen: Set[str] = set()
        self.stats = {
            "total": 0,
            "added": 0,
            "processed": 0,
            "duplicate": 0
        }
    
    def _hash_url(self, url: str) -> str:
        """生成URL哈希"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _normalize_url(self, url: str) -> str:
        """标准化URL"""
        # 移除锚点
        url = url.split('#')[0]
        # 移除尾部斜杠
        url = url.rstrip('/')
        # 统一大小写
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(url)
        # 域名小写化
        normalized = urlunparse((
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
        return normalized
    
    def add(self, url: str) -> bool:
        """添加URL到队列"""
        normalized = self._normalize_url(url)
        url_hash = self._hash_url(normalized)
        
        self.stats["total"] += 1
        
        if url_hash in self.seen:
            self.stats["duplicate"] += 1
            logger.debug(f"Duplicate URL: {url}")
            return False
        
        if len(self.queue) >= self.max_urls:
            logger.warning(f"Queue full, dropping URL: {url}")
            return False
        
        self.queue.append(normalized)
        self.seen.add(url_hash)
        self.stats["added"] += 1
        
        logger.debug(f"Added URL: {url}")
        return True
    
    def add_batch(self, urls: List[str]) -> int:
        """批量添加URL"""
        added = 0
        for url in urls:
            if self.add(url):
                added += 1
        logger.info(f"Added {added}/{len(urls)} URLs")
        return added
    
    def get(self) -> Optional[str]:
        """获取下一个URL"""
        if self.queue:
            url = self.queue.popleft()
            self.stats["processed"] += 1
            return url
        return None
    
    def get_batch(self, count: int = 10) -> List[str]:
        """批量获取URL"""
        urls = []
        for _ in range(min(count, len(self.queue))):
            url = self.get()
            if url:
                urls.append(url)
        return urls
    
    def has_more(self) -> bool:
        """检查是否还有更多URL"""
        return len(self.queue) > 0
    
    def size(self) -> int:
        """获取队列大小"""
        return len(self.queue)
    
    def clear(self):
        """清空队列"""
        self.queue.clear()
        self.seen.clear()
        self.stats = {
            "total": 0,
            "added": 0,
            "processed": 0,
            "duplicate": 0
        }
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            **self.stats,
            "queue_size": len(self.queue),
            "seen_size": len(self.seen)
        }
    
    def save_state(self, filepath: str = "url_state.json"):
        """保存状态"""
        state = {
            "queue": list(self.queue),
            "seen": list(self.seen),
            "stats": self.stats
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        logger.info(f"Saved URL state to {filepath}")
    
    def load_state(self, filepath: str = "url_state.json"):
        """加载状态"""
        with open(filepath, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        self.queue = deque(state["queue"])
        self.seen = set(state["seen"])
        self.stats = state["stats"]
        logger.info(f"Loaded URL state from {filepath}")

def main():
    """主函数"""
    manager = URLManager()
    
    # 添加URL
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page1",  # 重复
        "https://EXAMPLE.COM/page3",  # 大小写不同
    ]
    
    manager.add_batch(urls)
    print(f"Stats: {manager.get_stats()}")
    
    # 获取URL
    while manager.has_more():
        url = manager.get()
        print(f"Processing: {url}")
    
    print(f"Final Stats: {manager.get_stats()}")

if __name__ == "__main__":
    main()
