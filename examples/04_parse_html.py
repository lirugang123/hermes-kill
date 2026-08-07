#!/usr/bin/env python3
"""
示例4: 解析HTML数据
使用正则和BeautifulSoup解析数据
"""

import re
from bs4 import BeautifulSoup

def parse_product_page(html: str) -> dict:
    """解析商品页面"""
    soup = BeautifulSoup(html, 'lxml')
    
    # 提取商品信息
    product = {
        'title': '',
        'price': '',
        'description': '',
        'images': [],
        'specs': {}
    }
    
    # 标题
    title_tag = soup.find('h1', class_=re.compile(r'product|title|name', re.I))
    if title_tag:
        product['title'] = title_tag.get_text(strip=True)
    
    # 价格
    price_tag = soup.find('span', class_=re.compile(r'price|cost', re.I))
    if price_tag:
        product['price'] = price_tag.get_text(strip=True)
    
    # 描述
    desc_tag = soup.find('div', class_=re.compile(r'description|detail', re.I))
    if desc_tag:
        product['description'] = desc_tag.get_text(strip=True)[:500]
    
    # 图片
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src:
            product['images'].append(src)
    
    # 规格参数
    specs_table = soup.find('table', class_=re.compile(r'spec|parameter', re.I))
    if specs_table:
        for row in specs_table.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                product['specs'][key] = value
    
    return product

def parse_article_page(html: str) -> dict:
    """解析文章页面"""
    soup = BeautifulSoup(html, 'lxml')
    
    article = {
        'title': '',
        'author': '',
        'date': '',
        'content': '',
        'tags': []
    }
    
    # 标题
    title_tag = soup.find('h1') or soup.find('title')
    if title_tag:
        article['title'] = title_tag.get_text(strip=True)
    
    # 作者
    author_tag = soup.find('span', class_=re.compile(r'author|writer', re.I))
    if author_tag:
        article['author'] = author_tag.get_text(strip=True)
    
    # 日期
    date_tag = soup.find('time') or soup.find('span', class_=re.compile(r'date', re.I))
    if date_tag:
        article['date'] = date_tag.get('datetime') or date_tag.get_text(strip=True)
    
    # 正文
    content_tag = soup.find('article') or soup.find('div', class_=re.compile(r'content|article', re.I))
    if content_tag:
        article['content'] = content_tag.get_text(strip=True)
    
    # 标签
    for tag in soup.find_all('a', class_=re.compile(r'tag|category', re.I)):
        article['tags'].append(tag.get_text(strip=True))
    
    return article

if __name__ == "__main__":
    # 测试商品解析
    sample_html = '''
    <html>
        <body>
            <h1 class="product-title">Test Product</h1>
            <span class="price">$99.99</span>
            <div class="description">This is a test product</div>
            <img src="https://example.com/image1.jpg">
            <img data-src="https://example.com/image2.jpg">
        </body>
    </html>
    '''
    
    product = parse_product_page(sample_html)
    print("Product:", product)
