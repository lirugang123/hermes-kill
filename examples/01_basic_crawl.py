#!/usr/bin/env python3
"""
示例1: 基础网页爬取
使用requests库爬取静态网页
"""

import requests
from bs4 import BeautifulSoup
import re

def crawl_basic(url: str) -> dict:
    """基础爬取"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    # 提取标题
    title = soup.title.string if soup.title else "No title"
    
    # 提取链接
    links = []
    for a in soup.find_all('a', href=True):
        links.append({
            'text': a.get_text(strip=True),
            'href': a['href']
        })
    
    # 提取图片
    images = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src:
            images.append(src)
    
    return {
        'url': url,
        'title': title,
        'links': links[:20],  # 限制数量
        'images': images[:10],
        'status': response.status_code
    }

if __name__ == "__main__":
    url = "https://example.com"
    result = crawl_basic(url)
    print(f"Title: {result['title']}")
    print(f"Links: {len(result['links'])}")
    print(f"Images: {len(result['images'])}")
