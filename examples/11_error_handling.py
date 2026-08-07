#!/usr/bin/env python3
"""
示例11: 错误处理
完善的错误处理和日志记录
"""

import logging
import traceback
from typing import Callable, Optional, Type, Tuple
from functools import wraps

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CrawlerException(Exception):
    """爬虫基础异常"""
    pass

class NetworkError(CrawlerException):
    """网络错误"""
    pass

class ParseError(CrawlerException):
    """解析错误"""
    pass

class RateLimitError(CrawlerException):
    """速率限制错误"""
    pass

class ErrorHandler:
    """错误处理器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def handle(self, func: Callable, *args, **kwargs):
        """处理函数调用"""
        try:
            result = func(*args, **kwargs)
            return result
        except NetworkError as e:
            logger.error(f"Network error: {e}")
            self.errors.append({'type': 'network', 'error': str(e)})
            return None
        except ParseError as e:
            logger.error(f"Parse error: {e}")
            self.errors.append({'type': 'parse', 'error': str(e)})
            return None
        except RateLimitError as e:
            logger.warning(f"Rate limit: {e}")
            self.warnings.append({'type': 'rate_limit', 'error': str(e)})
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.debug(traceback.format_exc())
            self.errors.append({'type': 'unknown', 'error': str(e)})
            return None
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            'errors': len(self.errors),
            'warnings': len(self.warnings),
            'error_details': self.errors[-10:],  # 最近10个
            'warning_details': self.warnings[-10:]
        }
    
    def clear(self):
        """清空记录"""
        self.errors.clear()
        self.warnings.clear()

def retry_on_error(max_retries: int = 3, exceptions: Tuple[Type[Exception], ...] = (Exception,)):
    """重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt}/{max_retries} failed: {e}")
                    
                    if attempt < max_retries:
                        import time
                        time.sleep(2 ** attempt)  # 指数退避
            
            logger.error(f"All {max_retries} attempts failed")
            raise last_exception
        
        return wrapper
    return decorator

@retry_on_error(max_retries=3, exceptions=(NetworkError,))
def fetch_with_retry(url: str) -> str:
    """带重试的获取"""
    import requests
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def main():
    """主函数"""
    handler = ErrorHandler()
    
    # 测试错误处理
    def failing_function():
        raise NetworkError("Connection timeout")
    
    result = handler.handle(failing_function)
    print(f"Result: {result}")
    print(f"Stats: {handler.get_stats()}")

if __name__ == "__main__":
    main()
