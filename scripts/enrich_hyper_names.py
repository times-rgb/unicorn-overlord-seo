# -*- coding: utf-8 -*-
"""
补充采集：从角色详情页抓 名前 字段（JP（EN）），得到英文名 → 写入 hyper_chara_data.json
断点续传：已有 en_name 的跳过
"""
import re
import json
import time
import os
import sys
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}
OUT = 'hyper_chara_data.json'
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def get(url, retries=3):
    for attempt in range(retries):
        try:
            r = SESSION.get(url, timeout=30)
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            print(f'   [retry {attempt+1}] {e}')
            time.sleep(2 + attempt * 2)
    return None


def parse_en_name(html):
    m = re.search(r'名前</th>\s*<td[^>]*>(.*?)</td>', html, re.S)
    if not m:
        return None
    raw = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    # 取括号里的英文名：JP（EN）或 JP(EN)
    m2 = re.search(r'[（(]([A-Za-z][^）)]*)[）)]', raw)
    if m2:
        return m2.group(1).strip()
    return raw.strip()


def main():
    data = json.load(open(OUT, encoding='utf-8'))
    todo = [c for c in data if not c.get('en_name')]
    print(f'待补英文名: {len(todo)}')
    for i, c in enumerate(todo):
        html = get(c['detail'])
        if not html:
            print(f'[{i+1}/{len(todo)}] {c["jp"]} 抓取失败')
            continue
        en = parse_en_name(html)
        c['en_name'] = en
        print(f'[{i+1}/{len(todo)}] {c["jp"]} → {en}')
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        time.sleep(0.6)
    print('完成')


if __name__ == '__main__':
    main()
