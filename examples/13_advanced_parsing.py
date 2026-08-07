#!/usr/bin/env python3
"""
示例13: HTML解析高级用法
"""

from bs4 import BeautifulSoup
import re

def parse_advanced(html: str) -> dict:
    """高级HTML解析"""
    soup = BeautifulSoup(html, 'lxml')
    
    result = {
        'meta_tags': {},
        'scripts': [],
        'stylesheets': [],
        'forms': [],
        'tables': []
    }
    
    # 提取meta标签
    for meta in soup.find_all('meta'):
        name = meta.get('name') or meta.get('property')
        content = meta.get('content', '')
        if name:
            result['meta_tags'][name] = content
    
    # 提取script标签
    for script in soup.find_all('script'):
        if script.string:
            result['scripts'].append(script.string.strip())
    
    # 提取stylesheet链接
    for link in soup.find_all('link', rel='stylesheet'):
        result['stylesheets'].append(link.get('href', ''))
    
    # 提取表单
    for form in soup.find_all('form'):
        result['forms'].append({
            'action': form.get('action', ''),
            'method': form.get('method', 'GET'),
            'inputs': [
                {'name': inp.get('name'), 'type': inp.get('type')}
                for inp in form.find_all('input')
            ]
        })
    
    # 提取表格
    for table in soup.find_all('table')[:5]:  # 限制数量
        rows = []
        for tr in table.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            rows.append(cells)
        result['tables'].append(rows)
    
    return result

if __name__ == "__main__":
    sample_html = '''
    <html>
        <head>
            <meta name="description" content="Test page">
            <script src="app.js"></script>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <form action="/submit" method="POST">
                <input type="text" name="username">
                <input type="password" name="password">
            </form>
            <table>
                <tr><th>Name</th><th>Age</th></tr>
                <tr><td>John</td><td>30</td></tr>
            </table>
        </body>
    </html>
    '''
    
    result = parse_advanced(sample_html)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
