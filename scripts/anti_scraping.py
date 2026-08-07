#!/usr/bin/env python3
"""
反爬策略模块
提供多种反爬应对方案
"""

import logging
import random
import time
from typing import Dict, List, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AntiScraping:
    """反爬策略"""
    
    def __init__(self):
        self.request_count = 0
        self.last_request_time = 0
    
    def get_random_user_agent(self) -> str:
        """获取随机User-Agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        ]
        return random.choice(user_agents)
    
    def get_random_headers(self) -> Dict[str, str]:
        """获取随机请求头"""
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(['zh-CN,zh;q=0.9,en;q=0.8', 'en-US,en;q=0.5', 'zh-CN,zh;q=0.9']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        return headers
    
    def random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """随机延迟"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        logger.debug(f"Delayed for {delay:.2f} seconds")
    
    def rate_limit(self, requests_per_second: float = 10.0):
        """速率限制"""
        min_interval = 1.0 / requests_per_second
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    def rotate_proxy(self, proxies: List[str]) -> Optional[str]:
        """轮换代理"""
        if proxies:
            proxy = random.choice(proxies)
            logger.info(f"Using proxy: {proxy}")
            return proxy
        return None
    
    def generate_cookie(self, domain: str) -> Dict[str, str]:
        """生成Cookie"""
        import uuid
        return {
            'session_id': str(uuid.uuid4()),
            'visited_at': datetime.now().isoformat(),
            'tracking_id': f"trk_{random.randint(1000, 9999)}",
        }
    
    def simulate_human_behavior(self):
        """模拟人类行为"""
        # 随机滚动
        scroll_delay = random.uniform(0.5, 2.0)
        time.sleep(scroll_delay)
        
        # 随机鼠标移动
        mouse_delay = random.uniform(0.1, 0.5)
        time.sleep(mouse_delay)
        
        # 随机点击
        if random.random() > 0.7:
            click_delay = random.uniform(0.2, 0.8)
            time.sleep(click_delay)

class ProxyManager:
    """代理管理器"""
    
    def __init__(self):
        self.proxies = []
        self.current_proxy = None
    
    def add_proxy(self, proxy: str):
        """添加代理"""
        self.proxies.append(proxy)
        logger.info(f"Added proxy: {proxy}")
    
    def get_proxy(self) -> Optional[str]:
        """获取代理"""
        if self.proxies:
            self.current_proxy = random.choice(self.proxies)
            return self.current_proxy
        return None
    
    def remove_proxy(self, proxy: str):
        """移除代理"""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            logger.info(f"Removed proxy: {proxy}")

def main():
    """主函数"""
    anti = AntiScraping()
    
    # 测试User-Agent
    print("User-Agent:", anti.get_random_user_agent())
    
    # 测试Headers
    headers = anti.get_random_headers()
    print("Headers:", json.dumps(headers, indent=2))
    
    # 测试Cookie
    cookies = anti.generate_cookie("example.com")
    print("Cookies:", json.dumps(cookies, indent=2))

if __name__ == "__main__":
    import json
    main()
