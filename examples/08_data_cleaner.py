#!/usr/bin/env python3
"""
示例8: 数据清洗
清洗和格式化爬取的数据
"""

import re
import html
from typing import List, Dict, Optional
from datetime import datetime

class DataCleaner:
    """数据清洗器"""
    
    def __init__(self):
        self.stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of'}
    
    def clean_text(self, text: str) -> str:
        """清洗文本"""
        if not text:
            return ""
        
        # 解码HTML实体
        text = html.unescape(text)
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', text)
        
        return text.strip()
    
    def extract_sentences(self, text: str) -> List[str]:
        """提取句子"""
        sentences = re.split(r'[。！？.!?\n]', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """提取关键词"""
        # 简单词频统计
        words = re.findall(r'[\u4e00-\u9fa5a-zA-Z]+', text.lower())
        words = [w for w in words if w not in self.stop_words and len(w) > 1]
        
        from collections import Counter
        word_counts = Counter(words)
        
        return [word for word, count in word_counts.most_common(top_n)]
    
    def extract_dates(self, text: str) -> List[str]:
        """提取日期"""
        # 匹配多种日期格式
        patterns = [
            r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?',
            r'\d{1,2}[-/]月[-/]\d{1,2}[-/]?\d{2,4}',
            r'\d{4}年\d{1,2}月'
        ]
        
        dates = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        return list(set(dates))
    
    def extract_emails(self, text: str) -> List[str]:
        """提取邮箱"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return list(set(re.findall(pattern, text)))
    
    def extract_phones(self, text: str) -> List[str]:
        """提取电话"""
        patterns = [
            r'1[3-9]\d{9}',
            r'\d{3,4}[-.]?\d{7,8}',
            r'\+?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{4}'
        ]
        
        phones = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            phones.extend(matches)
        
        return list(set(phones))
    
    def normalize_url(self, url: str) -> str:
        """标准化URL"""
        # 移除协议
        url = re.sub(r'^https?://', '', url)
        # 移除www
        url = re.sub(r'^www\.', '', url)
        # 移除尾部斜杠
        url = url.rstrip('/')
        return url
    
    def deduplicate(self, items: List[str]) -> List[str]:
        """去重"""
        return list(dict.fromkeys(items))
    
    def clean(self, data: Dict) -> Dict:
        """清洗完整数据"""
        cleaned = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                cleaned[key] = self.clean_text(value)
            elif isinstance(value, list):
                cleaned[key] = [self.clean_text(item) if isinstance(item, str) else item for item in value]
            else:
                cleaned[key] = value
        
        return cleaned

def main():
    """主函数"""
    cleaner = DataCleaner()
    
    # 测试文本清洗
    raw_text = """
    <div class="article">
        <h1>Test Article</h1>
        <p>This is a <strong>test</strong> paragraph with special characters: @#$%^&*()</p>
        <p>Contact: test@example.com or call 123-456-7890</p>
        <p>Date: 2026-08-07</p>
    </div>
    """
    
    cleaned = cleaner.clean_text(raw_text)
    print(f"Cleaned text: {cleaned[:100]}...")
    
    # 提取信息
    print(f"Keywords: {cleaner.extract_keywords(cleaned)}")
    print(f"Dates: {cleaner.extract_dates(cleaned)}")
    print(f"Emails: {cleaner.extract_emails(cleaned)}")
    print(f"Phones: {cleaner.extract_phones(cleaned)}")

if __name__ == "__main__":
    main()
