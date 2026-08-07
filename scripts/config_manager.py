#!/usr/bin/env python3
"""
配置管理器
管理应用配置
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config/settings.yaml"):
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        # 加载环境变量
        load_dotenv()
        
        # 加载配置文件
        config_path = Path(self.config_file)
        if config_path.exists():
            self.config = self._parse_config(config_path)
            logger.info(f"Loaded config from {self.config_file}")
        else:
            self.config = {}
            logger.warning(f"Config file not found: {self.config_file}")
    
    def _parse_config(self, path: Path) -> Dict:
        """解析配置文件"""
        if path.suffix == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif path.suffix == '.yaml' or path.suffix == '.yml':
            try:
                import yaml
                with open(path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except ImportError:
                logger.error("PyYAML not installed")
                return {}
        else:
            logger.error(f"Unsupported config format: {path.suffix}")
            return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        # 检查环境变量
        if value is None or value == "":
            env_value = os.getenv(key.upper())
            if env_value:
                return env_value
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """保存配置"""
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.config_file.endswith('.json'):
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        elif self.config_file.endswith('.yaml'):
            try:
                import yaml
                with open(config_path, 'w', encoding='utf-8') as f:
                    yaml.dump(self.config, f, default_flow_style=False)
            except ImportError:
                logger.error("PyYAML not installed")
        
        logger.info(f"Config saved to {self.config_file}")
    
    def get_all(self) -> Dict:
        """获取所有配置"""
        return self.config.copy()
    
    def reload(self):
        """重新加载配置"""
        self._load_config()
        logger.info("Config reloaded")

def main():
    """主函数"""
    config = ConfigManager()
    
    # 获取配置
    api_key = config.get('api_keys.firecrawl', 'default_key')
    logger.info(f"API Key: {api_key[:10]}...")
    
    # 设置配置
    config.set('test_key', 'test_value')
    config.save()
    
    # 显示所有配置
    print(json.dumps(config.get_all(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
