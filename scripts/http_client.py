#!/usr/bin/env python3
"""
HTTP客户端封装
提供统一的HTTP请求接口
"""

import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

import requests
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

@dataclass
class HttpResponse:
    """HTTP响应"""
    status_code: int
    headers: Dict[str, str]
    body: str
    url: str
    
    def json(self) -> Any:
        import json
        return json.loads(self.body)
    
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

class HttpClient:
    """HTTP客户端"""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Hermes-Kill/1.0',
            'Accept': 'application/json, text/html, */*',
        })
    
    def request(
        self,
        method: HttpMethod,
        url: str,
        **kwargs
    ) -> HttpResponse:
        """发送请求"""
        kwargs.setdefault('timeout', self.timeout)
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method.value,
                    url,
                    **kwargs
                )
                response.raise_for_status()
                
                return HttpResponse(
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    body=response.text,
                    url=response.url
                )
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt == self.max_retries - 1:
                    raise
        
        raise Exception("Max retries exceeded")
    
    def get(self, url: str, **kwargs) -> HttpResponse:
        """GET请求"""
        return self.request(HttpMethod.GET, url, **kwargs)
    
    def post(self, url: str, **kwargs) -> HttpResponse:
        """POST请求"""
        return self.request(HttpMethod.POST, url, **kwargs)
    
    def put(self, url: str, **kwargs) -> HttpResponse:
        """PUT请求"""
        return self.request(HttpMethod.PUT, url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> HttpResponse:
        """DELETE请求"""
        return self.request(HttpMethod.DELETE, url, **kwargs)
    
    def set_proxy(self, proxy: str):
        """设置代理"""
        self.session.proxies = {
            'http': proxy,
            'https': proxy
        }
    
    def set_headers(self, headers: Dict[str, str]):
        """设置请求头"""
        self.session.headers.update(headers)
    
    def close(self):
        """关闭会话"""
        self.session.close()

class AsyncHttpClient:
    """异步HTTP客户端"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            timeout=timeout,
            headers={
                'User-Agent': 'Hermes-Kill/1.0',
            }
        )
    
    async def request(self, method: str, url: str, **kwargs) -> HttpResponse:
        """发送异步请求"""
        response = await self.client.request(method, url, **kwargs)
        
        return HttpResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=response.text,
            url=str(response.url)
        )
    
    async def get(self, url: str, **kwargs) -> HttpResponse:
        """异步GET请求"""
        return await self.request('GET', url, **kwargs)
    
    async def post(self, url: str, **kwargs) -> HttpResponse:
        """异步POST请求"""
        return await self.request('POST', url, **kwargs)
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()

def main():
    """主函数"""
    client = HttpClient()
    
    # 测试GET请求
    response = client.get("https://httpbin.org/get")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.body[:200]}")
    
    # 测试POST请求
    response = client.post(
        "https://httpbin.org/post",
        json={"key": "value"}
    )
    print(f"POST Status: {response.status_code}")
    
    client.close()

if __name__ == "__main__":
    main()
