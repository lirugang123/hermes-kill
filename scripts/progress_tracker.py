#!/usr/bin/env python3
"""
进度追踪器
追踪爬取进度
"""

import logging
import time
from typing import Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProgressTracker:
    """进度追踪器"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.description = description
        self.current = 0
        self.start_time = time.time()
        self.last_update = time.time()
        self.stats = {
            "speed": 0,  # items per second
            "eta": 0,    # estimated time available
            "percent": 0
        }
    
    def update(self, increment: int = 1):
        """更新进度"""
        self.current += increment
        now = time.time()
        
        # 计算速度（每5秒更新一次）
        if now - self.last_update >= 5:
            elapsed = now - self.start_time
            self.stats["speed"] = self.current / elapsed if elapsed > 0 else 0
            remaining = (self.total - self.current) / self.stats["speed"] if self.stats["speed"] > 0 else 0
            self.stats["eta"] = remaining
            self.stats["percent"] = (self.current / self.total * 100) if self.total > 0 else 0
            self.last_update = now
        
        self._print_progress()
    
    def _print_progress(self):
        """打印进度"""
        percent = self.stats["percent"]
        elapsed = time.time() - self.start_time
        
        # 格式化时间
        elapsed_str = self._format_time(elapsed)
        eta_str = self._format_time(self.stats["eta"]) if self.stats["eta"] > 0 else "calculating..."
        
        # 进度条
        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"\r[{bar}] {percent:.1f}% | {self.current}/{self.total} | "
              f"Speed: {self.stats['speed']:.1f}/s | "
              f"Elapsed: {elapsed_str} | "
              f"ETA: {eta_str}", end='', flush=True)
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def finish(self):
        """完成"""
        print()  # 换行
        elapsed = time.time() - self.start_time
        logger.info(f"Completed in {self._format_time(elapsed)}")
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            **self.stats,
            "current": self.current,
            "total": self.total
        }

class MultiProgressTracker:
    """多任务进度追踪器"""
    
    def __init__(self):
        self.trackers: dict = {}
    
    def add(self, name: str, total: int):
        """添加任务"""
        self.trackers[name] = ProgressTracker(total, name)
        logger.info(f"Added task: {name} (total: {total})")
    
    def update(self, name: str, increment: int = 1):
        """更新任务"""
        if name in self.trackers:
            self.trackers[name].update(increment)
    
    def finish(self, name: str):
        """完成任务"""
        if name in self.trackers:
            self.trackers[name].finish()
    
    def get_all_stats(self) -> dict:
        """获取所有统计"""
        return {name: t.get_stats() for name, t in self.trackers.items()}

def main():
    """主函数"""
    # 单任务示例
    tracker = ProgressTracker(100, "Crawling")
    
    for i in range(100):
        # 模拟工作
        time.sleep(0.01)
        tracker.update()
    
    tracker.finish()
    
    # 多任务示例
    multi = MultiProgressTracker()
    multi.add("Task A", 50)
    multi.add("Task B", 30)
    
    for i in range(50):
        multi.update("Task A")
        time.sleep(0.005)
    
    for i in range(30):
        multi.update("Task B")
        time.sleep(0.005)
    
    multi.finish("Task A")
    multi.finish("Task B")
    
    print("\nAll stats:", json.dumps(multi.get_all_stats(), indent=2))

if __name__ == "__main__":
    import json
    main()
