#!/usr/bin/env python3
"""
示例15: 数据导出
将爬取数据导出为多种格式
"""

import json
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class DataExporter:
    """数据导出器"""
    
    def __init__(self, data: List[Dict]):
        self.data = data
    
    def export_json(self, output_path: str) -> str:
        """导出JSON"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        return output_path
    
    def export_csv(self, output_path: str) -> str:
        """导出CSV"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        if not self.data:
            return output_path
        
        fieldnames = list(self.data[0].keys())
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)
        
        return output_path
    
    def export_excel(self, output_path: str) -> str:
        """导出Excel"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(self.data)
        df.to_excel(output_path, index=False)
        
        return output_path
    
    def export_all(self, output_dir: str = "output") -> Dict[str, str]:
        """导出所有格式"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        results = {}
        
        json_path = f"{output_dir}/{timestamp}.json"
        csv_path = f"{output_dir}/{timestamp}.csv"
        excel_path = f"{output_dir}/{timestamp}.xlsx"
        
        results['json'] = self.export_json(json_path)
        results['csv'] = self.export_csv(csv_path)
        results['excel'] = self.export_excel(excel_path)
        
        return results

def main():
    """主函数"""
    # 示例数据
    data = [
        {'url': 'https://example.com/1', 'title': 'Page 1', 'status': 200},
        {'url': 'https://example.com/2', 'title': 'Page 2', 'status': 200},
        {'url': 'https://example.com/3', 'title': 'Page 3', 'status': 404},
    ]
    
    exporter = DataExporter(data)
    results = exporter.export_all()
    
    print("Exported files:")
    for fmt, path in results.items():
        print(f"  {fmt}: {path}")

if __name__ == "__main__":
    main()
