# Release v1.0.0

## 新增功能

- 多工具整合爬虫框架
- Firecrawl MCP集成
- Playwright浏览器自动化
- 反爬策略系统
- 并发控制机制
- 数据导出工具
- 定时任务调度
- 插件系统架构

## 工具清单

| 工具 | 版本 | 用途 |
|------|------|------|
| Firecrawl | MCP 26工具 | 大规模爬取 |
| Playwright | v1.62.0 | 浏览器自动化 |
| 9router | v0.5.50 | 任务分发 |
| requests | v2.31.0 | HTTP请求 |
| pandas | v2.0.0 | 数据处理 |

## 文件统计

- 总文件数: 100+
- 脚本文件: 25+
- 示例文件: 15+
- 文档文件: 20+
- 测试文件: 15+
- 配置文件: 10+

## 安装

```bash
git clone git@github.com:lirugang123/hermes-kill.git
cd hermes-kill
pip install -r requirements.txt
```

## 使用

```bash
# 基本爬取
python scripts/crawler.py

# 批量爬取
python scripts/batch_crawler.py

# 定时任务
python scripts/scheduler.py
```

## 许可证

MIT License
