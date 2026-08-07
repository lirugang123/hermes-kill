#!/usr/bin/env python3
"""
示例7: 数据存储
使用SQLite存储爬取数据
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

class DataStore:
    """数据存储类"""
    
    def __init__(self, db_path: str = "data/crawler.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        """创建表"""
        cursor = self.conn.cursor()
        
        # 爬取记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crawls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                status_code INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 链接表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crawl_id INTEGER,
                url TEXT,
                text TEXT,
                FOREIGN KEY (crawl_id) REFERENCES crawls(id)
            )
        ''')
        
        # 图片表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crawl_id INTEGER,
                url TEXT,
                alt TEXT,
                FOREIGN KEY (crawl_id) REFERENCES crawls(id)
            )
        ''')
        
        self.conn.commit()
    
    def save_crawl(self, url: str, title: str = None, content: str = None, status_code: int = 200) -> int:
        """保存爬取记录"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO crawls (url, title, content, status_code)
                VALUES (?, ?, ?, ?)
            ''', (url, title, content, status_code))
            
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def save_links(self, crawl_id: int, links: List[Dict]):
        """保存链接"""
        cursor = self.conn.cursor()
        
        for link in links:
            cursor.execute('''
                INSERT INTO links (crawl_id, url, text)
                VALUES (?, ?, ?)
            ''', (crawl_id, link.get('url'), link.get('text')))
        
        self.conn.commit()
    
    def save_images(self, crawl_id: int, images: List[Dict]):
        """保存图片"""
        cursor = self.conn.cursor()
        
        for img in images:
            cursor.execute('''
                INSERT INTO images (crawl_id, url, alt)
                VALUES (?, ?, ?)
            ''', (crawl_id, img.get('url'), img.get('alt')))
        
        self.conn.commit()
    
    def get_crawl(self, url: str) -> Optional[Dict]:
        """获取爬取记录"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM crawls WHERE url = ?', (url,))
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'content': row[3],
                'status_code': row[4],
                'created_at': row[5],
                'updated_at': row[6]
            }
        return None
    
    def get_all_crawls(self, limit: int = 100) -> List[Dict]:
        """获取所有爬取记录"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM crawls ORDER BY created_at DESC LIMIT ?', (limit,))
        
        return [
            {
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'content': row[3],
                'status_code': row[4],
                'created_at': row[5],
                'updated_at': row[6]
            }
            for row in cursor.fetchall()
        ]
    
    def export_to_json(self, output_path: str = "data/export.json"):
        """导出到JSON"""
        crawls = self.get_all_crawls()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(crawls, f, indent=2, ensure_ascii=False)
        
        print(f"Exported {len(crawls)} records to {output_path}")
    
    def close(self):
        """关闭连接"""
        self.conn.close()

if __name__ == "__main__":
    store = DataStore()
    
    # 保存记录
    crawl_id = store.save_crawl(
        url="https://example.com",
        title="Example Domain",
        content="This domain is for use in illustrative examples...",
        status_code=200
    )
    
    # 保存链接
    store.save_links(crawl_id, [
        {'url': 'https://www.iana.org/domains/example', 'text': 'IANA'}
    ])
    
    # 查询
    result = store.get_crawl("https://example.com")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 导出
    store.export_to_json()
    
    store.close()
