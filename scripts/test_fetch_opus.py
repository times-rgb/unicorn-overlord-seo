# -*- coding: utf-8 -*-
"""测试能否直接抓取 B 站 opus 页面 HTML 并定位数据脚本"""
import requests
import re
import sys

url = 'https://www.bilibili.com/opus/916422313046442004'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
try:
    r = requests.get(url, headers=headers, timeout=20)
    print('status:', r.status_code, 'len:', len(r.text))
    text = r.text
    # 定位数据
    for marker in ['__pinia', '__INITIAL_STATE__', 'opus-detail', 'rich_text_nodes', 'paragraphs']:
        idx = text.find(marker)
        print(f'marker {marker}:', idx)
    # 保存 HTML
    with open('_opus_page.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('saved _opus_page.html')
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
