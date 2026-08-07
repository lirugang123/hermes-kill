#!/usr/bin/env python3
"""
报告生成器
生成爬取结果报告
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, project_name: str = "Hermes Kill"):
        self.project_name = project_name
        self.report_data = {
            "project": project_name,
            "generated_at": datetime.now().isoformat(),
            "summary": {},
            "details": {}
        }
    
    def add_summary(self, **kwargs):
        """添加摘要信息"""
        self.report_data["summary"].update(kwargs)
    
    def add_detail(self, key: str, value):
        """添加详细信息"""
        self.report_data["details"][key] = value
    
    def generate_text_report(self) -> str:
        """生成文本报告"""
        lines = [
            "=" * 60,
            f"{self.project_name} - Crawl Report",
            f"Generated: {self.report_data['generated_at']}",
            "=" * 60,
            "",
            "Summary:",
            "-" * 40
        ]
        
        for key, value in self.report_data["summary"].items():
            lines.append(f"  {key}: {value}")
        
        lines.extend([
            "",
            "Details:",
            "-" * 40
        ])
        
        for key, value in self.report_data["details"].items():
            lines.append(f"  {key}:")
            if isinstance(value, dict):
                for k, v in value.items():
                    lines.append(f"    {k}: {v}")
            else:
                lines.append(f"    {value}")
        
        lines.append("=" * 60)
        return "\n".join(lines)
    
    def generate_json_report(self) -> str:
        """生成JSON报告"""
        return json.dumps(self.report_data, indent=2, ensure_ascii=False)
    
    def generate_csv_report(self, data: List[Dict]) -> str:
        """生成CSV报告"""
        if not data:
            return ""
        
        import pandas as pd
        df = pd.DataFrame(data)
        return df.to_csv(index=False)
    
    def save_report(
        self,
        output_dir: str = "reports",
        format: str = "text"
    ) -> str:
        """保存报告"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            filepath = f"{output_dir}/report_{timestamp}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.generate_json_report())
        elif format == "csv":
            filepath = f"{output_dir}/report_{timestamp}.csv"
            # CSV需要额外数据
            filepath = None
        else:
            filepath = f"{output_dir}/report_{timestamp}.txt"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.generate_text_report())
        
        if filepath:
            logger.info(f"Report saved to {filepath}")
        
        return filepath or ""
    
    def print_report(self):
        """打印报告"""
        print(self.generate_text_report())

def main():
    """主函数"""
    reporter = ReportGenerator()
    
    # 添加数据
    reporter.add_summary(
        total_urls=100,
        success_count=95,
        failed_count=5,
        success_rate="95%"
    )
    
    reporter.add_detail("top_sites", {
        "example.com": 50,
        "test.com": 30,
        "demo.com": 20
    })
    
    # 生成报告
    reporter.print_report()
    
    # 保存报告
    filepath = reporter.save_report()
    print(f"\nReport saved to: {filepath}")

if __name__ == "__main__":
    main()
