#!/usr/bin/env python3
"""
中间件示例
请求/响应处理中间件
"""

import time
import logging
from typing import Callable, Dict, Any
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def timing_middleware(func: Callable) -> Callable:
    """计时中间件"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper

def caching_middleware(cache: Dict) -> Callable:
    """缓存中间件"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in cache:
                logger.debug(f"Cache hit for {key[:50]}")
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper
    return decorator

def logging_middleware(func: Callable) -> Callable:
    """日志中间件"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@timing_middleware
@logging_middleware
def fetch_data(url: str) -> dict:
    """获取数据"""
    time.sleep(0.1)  # 模拟网络延迟
    return {"url": url, "data": "sample"}

def main():
    """主函数"""
    cache = {}
    
    # 使用缓存中间件
    cached_fetch = caching_middleware(cache)(fetch_data)
    
    # 测试
    result1 = cached_fetch("https://example.com")
    result2 = cached_fetch("https://example.com")  # 应该命中缓存
    
    print(f"Result 1: {result1}")
    print(f"Result 2: {result2}")
    print(f"Cache size: {len(cache)}")

if __name__ == "__main__":
    main()
