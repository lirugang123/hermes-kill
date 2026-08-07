#!/usr/bin/env python3
"""
示例10: 定时任务
使用APScheduler进行定时爬取
"""

import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScheduledCrawler:
    """定时爬取器"""
    
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.tasks = {}
    
    def add_daily_task(self, name: str, func, hour: int = 9, minute: int = 0):
        """添加每日任务"""
        trigger = CronTrigger(hour=hour, minute=minute, timezone='Asia/Shanghai')
        self.scheduler.add_job(func, trigger, id=name, name=name)
        self.tasks[name] = {'type': 'daily', 'hour': hour, 'minute': minute}
        logger.info(f"Added daily task: {name} at {hour:02d}:{minute:02d}")
    
    def add_interval_task(self, name: str, func, seconds: int = 300):
        """添加间隔任务"""
        trigger = IntervalTrigger(seconds=seconds)
        self.scheduler.add_job(func, trigger, id=name, name=name)
        self.tasks[name] = {'type': 'interval', 'seconds': seconds}
        logger.info(f"Added interval task: {name} every {seconds}s")
    
    def add_cron_task(self, name: str, func, cron_expr: str):
        """添加cron任务"""
        trigger = CronTrigger.from_crontab(cron_expr, timezone='Asia/Shanghai')
        self.scheduler.add_job(func, trigger, id=name, name=name)
        self.tasks[name] = {'type': 'cron', 'expr': cron_expr}
        logger.info(f"Added cron task: {name} with expr: {cron_expr}")
    
    def start(self):
        """启动调度器"""
        logger.info("Starting scheduler...")
        self.scheduler.start()
    
    def shutdown(self):
        """关闭调度器"""
        logger.info("Shutting down scheduler...")
        self.scheduler.shutdown()
    
    def get_tasks(self) -> dict:
        """获取任务列表"""
        return self.tasks.copy()

def sample_task():
    """示例任务"""
    logger.info(f"Task executed at {datetime.now()}")
    # 这里添加实际的爬取逻辑
    print(f"[{datetime.now()}] Sample task running...")

def main():
    """主函数"""
    crawler = ScheduledCrawler()
    
    # 添加任务
    crawler.add_daily_task("morning_crawl", sample_task, hour=8, minute=30)
    crawler.add_interval_task("hourly_check", sample_task, seconds=3600)
    crawler.add_cron_task("weekend_crawl", sample_task, "0 10 * * 0,6")
    
    # 显示任务
    print("Scheduled tasks:")
    for name, config in crawler.get_tasks().items():
        print(f"  - {name}: {config}")
    
    # 启动（取消注释以运行）
    # crawler.start()

if __name__ == "__main__":
    main()
