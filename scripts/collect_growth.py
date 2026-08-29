# -*- coding: utf-8 -*-
"""
数据采集 v1：抓 HyperWiki 职业成长率表（下/上级）→ growth.json
验证 Python 爬取日本站表格可行性。
后续扩展：stat-calc 公式 / exptable / 角色-职业 / 装备 / 技能 / Fandom 角色成长类型
"""
import re
import json
import requests

URL = 'https://hyperwiki.jp/unicorn/growth/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}

r = requests.get(URL, headers=HEADERS, timeout=30)
print('status:', r.status_code, 'len:', len(r.text))
r.encoding = r.apparent_encoding
html = r.text

# 统计列标题（第一行 th）
ths = re.findall(r'<th[^>]*>(.*?)</th>', html, re.S)
cols = [re.sub(r'<[^>]+>', '', t).strip() for t in ths]
print('列:', cols)

# 抓所有表格行（tr），提取 td
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.S)
data = []
for tr in rows:
    tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
    if not tds:
        continue
    cells = [re.sub(r'<[^>]+>', '', c).replace('&nbsp;', ' ').strip() for c in tds]
    data.append(cells)

print('总行数:', len(data))
# 按"下/上级"分组：找含"クラス一覧"的标题定位比较麻烦，先看行特征
print('前 4 行:')
for d in data[:4]:
    print('  ', d)
print('后 4 行:')
for d in data[-4:]:
    print('  ', d)

# 保存原始
with open('_growth_raw.json', 'w', encoding='utf-8') as f:
    json.dump({'cols': cols, 'rows': data}, f, ensure_ascii=False, indent=1)
print('saved _growth_raw.json')
