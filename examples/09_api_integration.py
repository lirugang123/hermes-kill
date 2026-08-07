#!/usr/bin/env python3
"""
示例9: API集成
集成第三方API获取数据
"""

import requests
import json
from typing import Dict, List, Optional

class API Integrator:
    """API集成器"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.session = requests.Session()
    
    def github_search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索GitHub仓库"""
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": limit
        }
        
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json().get("items", [])
    
    def get_github_user(self, username: str) -> Dict:
        """获取GitHub用户信息"""
        url = f"https://api.github.com/users/{username}"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        
        return response.json()
    
    def get_weather(self, city: str) -> Dict:
        """获取天气信息"""
        # 使用免费的天气API
        url = "http://wttr.in"
        params = {"format": "j1"}
        
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    
    def get_news(self, category: str = "top", language: str = "zh") -> List[Dict]:
        """获取新闻"""
        # 使用新闻API
        url = f"https://newsapi.org/v2/{category}"
        params = {
            "language": language,
            "pageSize": 10
        }
        
        if self.api_key:
            params["apiKey"] = self.api_key
        
        response = self.session.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json().get("articles", [])
        return []
    
    def search_images(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索图片"""
        # 使用Unsplash API
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": limit
        }
        
        if self.api_key:
            params["client_id"] = self.api_key
        
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json().get("results", [])
    
    def translate(self, text: str, target_lang: str = "en") -> str:
        """翻译文本"""
        # 使用免费翻译API
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": text
        }
        
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        return "".join([item[0] for item in result[0]])

def main():
    """主函数"""
    api = API Integrator()
    
    # 测试GitHub搜索
    print("Searching GitHub for 'python'...")
    repos = api.github_search("python", limit=5)
    for repo in repos[:3]:
        print(f"  - {repo['full_name']} ({repo['stargazers_count']} stars)")
    
    # 测试天气
    print("\nGetting weather for Beijing...")
    weather = api.get_weather("Beijing")
    print(f"  Temperature: {weather['current']['temp']}°C")
    
    # 测试翻译
    print("\nTranslating text...")
    translated = api.translate("你好世界", "en")
    print(f"  Translated: {translated}")

if __name__ == "__main__":
    main()
