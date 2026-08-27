# -*- coding: utf-8 -*-
"""GEO 抽查：提取角色页首屏 lede + H2 结构，对照「直接答案/列表化/语义层级」"""
import os
import re

root = r'G:\CODEX\projects\my-website\characters'
targets = ['alain', 'yunifi', 'scarlett', 'gammel']

for slug in targets:
    p = os.path.join(root, slug, 'index.html')
    if not os.path.exists(p):
        print(slug, 'MISSING')
        continue
    t = open(p, encoding='utf-8').read()
    # title
    title = re.search(r'<title>(.*?)</title>', t)
    # lede
    lede = re.search(r'<p class="lede">(.*?)</p>', t, re.S)
    # h2 列表
    h2s = re.findall(r'<h2>(.*?)</h2>', t, re.S)
    # 首屏 200 字符（h1 之后）
    h1m = re.search(r'<h1>(.*?)</h1>', t, re.S)
    print('=' * 60)
    print('##', slug, '|', (title.group(1) if title else '?'))
    if lede:
        l = re.sub(r'<[^>]+>', '', lede.group(1)).strip()
        print('LEDE:', l[:300])
    print('H2s:', h2s[:8])
    print('首屏字数(h1后):', len(re.sub(r'<[^>]+>', '', t[h1m.end():h1m.end() + 2500]).replace('\n', '').strip()))
