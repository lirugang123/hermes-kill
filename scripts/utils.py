#!/usr/bin/env python3
"""
工具函数库
常用工具函数集合
"""

import hashlib
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import urllib.parse

def generate_id(length: int = 16) -> str:
    """生成随机ID"""
    import secrets
    return secrets.token_hex(length // 2)

def hash_url(url: str) -> str:
    """生成URL哈希"""
    return hashlib.md5(url.encode()).hexdigest()

def parse_url(url: str) -> Dict[str, str]:
    """解析URL"""
    parsed = urllib.parse.urlparse(url)
    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment
    }

def sanitize_filename(filename: str) -> str:
    """清理文件名"""
    # 移除非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 限制长度
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def format_timestamp(timestamp: Union[int, float, str]) -> str:
    """格式化时间戳"""
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp).timestamp()
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def read_json(file_path: str) -> Dict:
    """读取JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(file_path: str, data: Any):
    """写入JSON文件"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def read_text(file_path: str) -> str:
    """读取文本文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_text(file_path: str, content: str):
    """写入文本文件"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def download_file(url: str, output_path: str) -> bool:
    """下载文件"""
    import requests
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def extract_domain(url: str) -> str:
    """提取域名"""
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc

def is_valid_url(url: str) -> bool:
    """验证URL"""
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def is_valid_email(email: str) -> bool:
    """验证邮箱"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    """验证手机号"""
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None

def delay(seconds: float):
    """延迟"""
    time.sleep(seconds)

def retry_on_failure(func, max_retries: int = 3, delay: float = 1.0):
    """失败重试"""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise
            time.sleep(delay)

class Timer:
    """计时器"""
    
    def __init__(self, name: str = "task"):
        self.name = name
        self.start_time = None
    
    def start(self):
        self.start_time = time.time()
        return self
    
    def stop(self) -> float:
        if self.start_time:
            elapsed = time.time() - self.start_time
            print(f"{self.name} took {elapsed:.2f} seconds")
            return elapsed
        return 0

def main():
    """主函数"""
    # 测试工具函数
    print("ID:", generate_id())
    print("Hash:", hash_url("https://example.com"))
    print("Domain:", extract_domain("https://example.com/path?query=1"))
    print("Valid URL:", is_valid_url("https://example.com"))
    print("Valid Email:", is_valid_email("test@example.com"))
    
    # 测试计时器
    timer = Timer("test")
    timer.start()
    time.sleep(1)
    timer.stop()

if __name__ == "__main__":
    main()
