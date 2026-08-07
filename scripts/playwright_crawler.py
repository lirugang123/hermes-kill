#!/usr/bin/env python3
"""
Playwright浏览器自动化爬取器
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Optional

from playwright.sync_api import sync_playwright, Page, Browser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlaywrightCrawler:
    """Playwright浏览器爬取器"""
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
    
    def crawl(self, url: str, selectors: Optional[dict] = None) -> dict:
        """爬取页面并提取指定元素"""
        results = {}
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.set_default_timeout(self.timeout)
            
            try:
                page.goto(url, wait_until="networkidle")
                
                # 提取标题
                results["title"] = page.title()
                
                # 提取内容
                if selectors:
                    for key, selector in selectors.items():
                        try:
                            element = page.query_selector(selector)
                            if element:
                                results[key] = element.text_content()
                            else:
                                results[key] = None
                        except Exception as e:
                            logger.error(f"Failed to extract {key}: {e}")
                            results[key] = None
                
                # 提取所有链接
                links = page.query_selector_all('a[href]')
                results["links"] = [link.get_attribute('href') for link in links]
                
                # 提取图片
                images = page.query_selector_all('img')
                results["images"] = [img.get_attribute('src') for img in images]
                
            except Exception as e:
                logger.error(f"Failed to crawl {url}: {e}")
                results["error"] = str(e)
            finally:
                browser.close()
        
        return results
    
    def scrape_with_js(self, url: str) -> str:
        """执行JavaScript后获取页面内容"""
        content = ""
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            try:
                page.goto(url, wait_until="networkidle")
                
                # 等待动态内容加载
                page.wait_for_timeout(2000)
                
                # 执行JavaScript
                content = page.evaluate("""
                    () => {
                        return document.body.innerText;
                    }
                """)
                
            except Exception as e:
                logger.error(f"Failed to scrape {url}: {e}")
            finally:
                browser.close()
        
        return content

def main():
    """主函数"""
    crawler = PlaywrightCrawler()
    
    url = "https://example.com"
    selectors = {
        "main_content": ".main-content",
        "article": "article",
        "header": "header"
    }
    
    logger.info(f"Crawling {url}...")
    result = crawler.crawl(url, selectors)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
