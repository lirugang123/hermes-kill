#!/usr/bin/env python3
"""
缓存管理器
使用LRU缓存减少重复请求
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Optional, Any
from datetime import datetime, timedelta
from collections import OrderedDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LRUCache:
    """LRU缓存实现"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl = timedelta(seconds=ttl_seconds)
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: dict = {}
    
    def _generate_key(self, url: str) -> str:
        """生成缓存键"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get(self, url: str) -> Optional[Any]:
        """获取缓存"""
        key = self._generate_key(url)
        
        if key not in self.cache:
            return None
        
        # 检查是否过期
        if datetime.now() > self.timestamps[key]:
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        # 移动到末尾（最常用）
        self.cache.move_to_end(key)
        logger.debug(f"Cache hit: {url}")
        return self.cache[key]
    
    def set(self, url: str, data: Any):
        """设置缓存"""
        key = self._generate_key(url)
        
        # 如果已存在，先删除
        if key in self.cache:
            del self.cache[key]
        
        # 如果超过最大大小，删除最久未使用的
        if len(self.cache) >= self.max_size:
            oldest_key, _ = self.cache.popitem(last=False)
            del self.timestamps[oldest_key]
            logger.debug(f"Cache evicted: {oldest_key}")
        
        self.cache[key] = data
        self.timestamps[key] = datetime.now() + self.ttl
        logger.debug(f"Cache set: {url}")
    
    def delete(self, url: str):
        """删除缓存"""
        key = self._generate_key(url)
        if key in self.cache:
            del self.cache[key]
            del self.timestamps[key]
            logger.debug(f"Cache deleted: {url}")
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.timestamps.clear()
        logger.info("Cache cleared")
    
    def size(self) -> int:
        """获取缓存大小"""
        return len(self.cache)
    
    def stats(self) -> dict:
        """获取缓存统计"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl_seconds": self.ttl.total_seconds(),
            "hit_rate": "N/A"  # 需要额外跟踪
        }

class FileCache:
    """文件缓存（持久化）"""
    
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_path(self, url: str) -> Path:
        """获取缓存文件路径"""
        key = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / f"{key}.json"
    
    def get(self, url: str) -> Optional[Any]:
        """获取缓存"""
        path = self._get_path(url)
        
        if not path.exists():
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查是否过期（24小时）
            if datetime.fromisoformat(data["expires"]) < datetime.now():
                path.unlink()
                return None
            
            return data["data"]
        except Exception as e:
            logger.error(f"Failed to read cache: {e}")
            return None
    
    def set(self, url: str, data: Any, ttl_hours: int = 24):
        """设置缓存"""
        path = self._get_path(url)
        
        cache_data = {
            "data": data,
            "cached_at": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(hours=ttl_hours)).isoformat()
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
        
        logger.debug(f"File cache set: {url}")
    
    def delete(self, url: str):
        """删除缓存"""
        path = self._get_path(url)
        if path.exists():
            path.unlink()
            logger.debug(f"File cache deleted: {url}")
    
    def clear(self):
        """清空缓存"""
        for file in self.cache_dir.glob("*.json"):
            file.unlink()
        logger.info("File cache cleared")

def main():
    """主函数"""
    # 测试LRU缓存
    cache = LRUCache(max_size=100, ttl_seconds=3600)
    
    cache.set("https://example.com", {"content": "test"})
    result = cache.get("https://example.com")
    print(f"Cache result: {result}")
    print(f"Cache stats: {cache.stats()}")
    
    # 测试文件缓存
    file_cache = FileCache()
    file_cache.set("https://example.com", {"content": "test"})
    result = file_cache.get("https://example.com")
    print(f"File cache result: {result}")

if __name__ == "__main__":
    main()
