#!/usr/bin/env python3
"""
插件系统
可扩展的插件架构
"""

from typing import Dict, List, Callable, Any
from dataclasses import dataclass
import importlib

@dataclass
class Plugin:
    """插件定义"""
    name: str
    version: str
    description: str
    enabled: bool = True
    config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}

class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Callable]] = {}
    
    def register(self, plugin: Plugin):
        """注册插件"""
        self.plugins[plugin.name] = plugin
        print(f"Registered plugin: {plugin.name} v{plugin.version}")
    
    def unregister(self, name: str):
        """注销插件"""
        if name in self.plugins:
            del self.plugins[name]
            print(f"Unregistered plugin: {name}")
    
    def enable(self, name: str):
        """启用插件"""
        if name in self.plugins:
            self.plugins[name].enabled = True
            print(f"Enabled plugin: {name}")
    
    def disable(self, name: str):
        """禁用插件"""
        if name in self.plugins:
            self.plugins[name].enabled = False
            print(f"Disabled plugin: {name}")
    
    def register_hook(self, hook_name: str, func: Callable):
        """注册钩子"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(func)
        print(f"Registered hook: {hook_name}")
    
    def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """触发钩子"""
        results = []
        if hook_name in self.hooks:
            for func in self.hooks[hook_name]:
                try:
                    result = func(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Hook error: {e}")
        return results
    
    def get_plugins(self) -> List[Dict]:
        """获取所有插件"""
        return [
            {
                'name': p.name,
                'version': p.version,
                'enabled': p.enabled,
                'config': p.config
            }
            for p in self.plugins.values()
        ]

# 示例插件
class CrawlPlugin(Plugin):
    """爬取插件"""
    
    def __init__(self):
        super().__init__(
            name="crawl",
            version="1.0.0",
            description="Web crawling plugin"
        )
    
    def execute(self, url: str) -> dict:
        """执行爬取"""
        return {"url": url, "status": "crawled"}

def main():
    """主函数"""
    manager = PluginManager()
    
    # 注册插件
    crawl_plugin = CrawlPlugin()
    manager.register(crawl_plugin)
    
    # 注册钩子
    def before_crawl(url):
        print(f"Before crawling: {url}")
        return url
    
    def after_crawl(result):
        print(f"After crawling: {result}")
        return result
    
    manager.register_hook("before_crawl", before_crawl)
    manager.register_hook("after_crawl", after_crawl)
    
    # 触发钩子
    manager.trigger_hook("before_crawl", "https://example.com")
    
    # 执行插件
    result = crawl_plugin.execute("https://example.com")
    
    manager.trigger_hook("after_crawl", result)
    
    # 显示插件列表
    print("\nPlugins:")
    for plugin in manager.get_plugins():
        print(f"  - {plugin['name']} v{plugin['version']} ({'enabled' if plugin['enabled'] else 'disabled'})")

if __name__ == "__main__":
    main()
