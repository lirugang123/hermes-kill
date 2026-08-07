#!/usr/bin/env python3
"""
示例6: 反爬策略实战
演示各种反爬应对技巧
"""

import random
import time
import requests
from typing import Dict, List

class AntiScrapingExample:
    """反爬策略示例"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        ]
    
    def get_random_headers(self) -> Dict[str, str]:
        """获取随机请求头"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': random.choice(['zh-CN,zh;q=0.9,en;q=0.8', 'en-US,en;q=0.5']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        return headers
    
    def random_delay(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """随机延迟"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def rotate_proxy(self, proxies: List[str]) -> str:
        """轮换代理"""
        return random.choice(proxies)
    
    def generate_cookie(self, domain: str) -> Dict[str, str]:
        """生成Cookie"""
        import uuid
        return {
            'session_id': str(uuid.uuid4()),
            'visited_at': str(int(time.time())),
            'tracking_id': f"trk_{random.randint(1000, 9999)}",
        }

def main():
    """主函数"""
    example = AntiScrapingExample()
    
    # 演示1: 随机User-Agent
    print("Random User-Agent:", example.user_agents[0][:50] + "...")
    
    # 演示2: 随机延迟
    print("Random delay:", f"{random.uniform(1, 3):.2f}s")
    
    # 演示3: 生成Cookie
    cookies = example.generate_cookie("example.com")
    print("Generated cookies:", cookies)
    
    # 演示4: 完整请求头
    headers = example.get_random_headers()
    print("\nRequest headers:")
    for k, v in headers.items():
        print(f"  {k}: {v[:30]}...")

if __name__ == "__main__":
    main()
