#!/usr/bin/env python3
"""
数据处理器 - 清洗和转换爬取的数据
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """数据处理器"""
    
    def __init__(self):
        self.processed_data = []
    
    def clean_text(self, text: str) -> str:
        """清洗文本"""
        if not text:
            return ""
        
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除特殊字符
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', text)
        
        return text.strip()
    
    def extract_links(self, html: str) -> List[str]:
        """提取链接"""
        links = re.findall(r'href=["\']([^"\']+)["\']', html)
        return list(set(links))
    
    def extract_images(self, html: str) -> List[str]:
        """提取图片链接"""
        images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
        return list(set(images))
    
    def extract_emails(self, text: str) -> List[str]:
        """提取邮箱"""
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
        return list(set(emails))
    
    def extract_phone_numbers(self, text: str) -> List[str]:
        """提取电话号码"""
        phones = re.findall(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}', text)
        return list(set(phones))
    
    def convert_to_csv(self, data: List[Dict], output_path: str) -> str:
        """转换为CSV"""
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logger.info(f"Saved CSV to {output_path}")
        return output_path
    
    def convert_to_json(self, data: List[Dict], output_path: str) -> str:
        """转换为JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved JSON to {output_path}")
        return output_path
    
    def convert_to_excel(self, data: List[Dict], output_path: str) -> str:
        """转换为Excel"""
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        logger.info(f"Saved Excel to {output_path}")
        return output_path
    
    def process(self, raw_data: Dict) -> Dict:
        """处理原始数据"""
        processed = {
            "timestamp": datetime.now().isoformat(),
            "cleaned_content": self.clean_text(raw_data.get("content", "")),
            "links": self.extract_links(raw_data.get("html", "")),
            "images": self.extract_images(raw_data.get("html", "")),
            "emails": self.extract_emails(raw_data.get("content", "")),
            "phone_numbers": self.extract_phone_numbers(raw_data.get("content", ""))
        }
        
        self.processed_data.append(processed)
        return processed
    
    def export_all(self, output_dir: str = "output") -> Dict[str, str]:
        """导出所有数据"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        results = {}
        
        if self.processed_data:
            csv_path = f"{output_dir}/data_{timestamp}.csv"
            json_path = f"{output_dir}/data_{timestamp}.json"
            excel_path = f"{output_dir}/data_{timestamp}.xlsx"
            
            self.convert_to_csv(self.processed_data, csv_path)
            self.convert_to_json(self.processed_data, json_path)
            self.convert_to_excel(self.processed_data, excel_path)
            
            results = {
                "csv": csv_path,
                "json": json_path,
                "excel": excel_path
            }
        
        return results

def main():
    """主函数"""
    processor = DataProcessor()
    
    # 示例数据
    raw_data = {
        "content": "Contact us at support@example.com or call 123-456-7890",
        "html": '<a href="https://example.com">Link</a><img src="https://example.com/image.jpg">'
    }
    
    processed = processor.process(raw_data)
    print(json.dumps(processed, indent=2, ensure_ascii=False))
    
    # 导出
    results = processor.export_all()
    print(f"Exported to: {results}")

if __name__ == "__main__":
    import json
    main()
