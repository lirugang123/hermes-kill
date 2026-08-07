#!/usr/bin/env python3
"""
示例2: 使用Playwright爬取JS渲染页面
"""

from playwright.sync_api import sync_playwright
import json

def crawl_js_page(url: str) -> dict:
    """爬取JS渲染页面"""
    result = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # 访问页面
            page.goto(url, wait_until='networkidle')
            
            # 等待内容加载
            page.wait_for_timeout(2000)
            
            # 提取标题
            result['title'] = page.title()
            
            # 提取主要文本内容
            content = page.inner_text('body')
            result['content_preview'] = content[:500] + "..." if len(content) > 500 else content
            
            # 提取所有链接
            links = page.query_selector_all('a[href]')
            result['links'] = [link.get_attribute('href') for link in links]
            
            # 提取所有图片
            images = page.query_selector_all('img')
            result['images'] = [img.get_attribute('src') for img in images]
            
            # 执行JavaScript
            data = page.evaluate("""
                () => {
                    return {
                        userAgent: navigator.userAgent,
                        language: navigator.language,
                        screen: `${screen.width}x${screen.height}`
                    };
                }
            """)
            result['browser_info'] = data
            
        finally:
            browser.close()
    
    return result

if __name__ == "__main__":
    url = "https://example.com"
    result = crawl_js_page(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))
