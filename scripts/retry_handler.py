#!/usr/bin/env python3
"""
重试机制
实现指数退避重试
"""

import logging
import time
from typing import Callable, Optional, Type, Tuple
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}"
                    )
                    
                    if attempt < max_attempts:
                        logger.info(f"Retrying in {current_delay:.1f} seconds...")
                        time.sleep(current_delay)
                        current_delay *= backoff
            
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        
        return wrapper
    return decorator

class RetryHandler:
    """重试处理器"""
    
    def __init__(self, max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
        self.max_attempts = max_attempts
        self.delay = delay
        self.backoff = backoff
        self.attempts = 0
    
    def execute(self, func: Callable, *args, **kwargs):
        """执行带重试的函数"""
        self.attempts = 0
        current_delay = self.delay
        
        while self.attempts < self.max_attempts:
            try:
                self.attempts += 1
                result = func(*args, **kwargs)
                logger.info(f"Success on attempt {self.attempts}")
                return result
            except Exception as e:
                logger.warning(
                    f"Attempt {self.attempts}/{self.max_attempts} failed: {e}"
                )
                
                if self.attempts < self.max_attempts:
                    logger.info(f"Waiting {current_delay:.1f}s before retry...")
                    time.sleep(current_delay)
                    current_delay *= self.backoff
        
        raise Exception(f"Failed after {self.max_attempts} attempts")
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "max_attempts": self.max_attempts,
            "attempts_made": self.attempts,
            "success": self.attempts < self.max_attempts
        }

# 常用重试场景
@retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(ConnectionError, TimeoutError))
def fetch_with_retry(url: str) -> str:
    """带重试的HTTP请求"""
    import requests
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

@retry(max_attempts=5, delay=2.0, backoff=3.0)
def scrape_with_retry(url: str) -> dict:
    """带重试的爬取"""
    # 模拟爬取
    time.sleep(0.5)
    return {"url": url, "content": "sample"}

def main():
    """主函数"""
    handler = RetryHandler(max_attempts=3, delay=1.0)
    
    # 测试重试
    def failing_function():
        if not hasattr(failing_function, 'call_count'):
            failing_function.call_count = 0
        failing_function.call_count += 1
        
        if failing_function.call_count < 3:
            raise Exception(f"Failed attempt {failing_function.call_count}")
        
        return "Success!"
    
    result = handler.execute(failing_function)
    print(f"Result: {result}")
    print(f"Stats: {handler.get_stats()}")

if __name__ == "__main__":
    main()
