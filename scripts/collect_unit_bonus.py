# -*- coding: utf-8 -*-
"""采集编成加成：unit-bonus 页 下/上级 职业 → 8项基础值"""
import requests
import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}
URL = 'https://hyperwiki.jp/unicorn/unit-bonus/'
# 表列序: クラス 物攻 防御 魔攻 魔防 命中 回避 会心 ガード
STATS = ['pAtk', 'pDef', 'mAtk', 'mDef', 'acc', 'eva', 'crit', 'guard']


def main():
    r = requests.get(URL, headers=HEADERS, timeout=60)
    r.encoding = r.apparent_encoding
    html = r.text

    result = {}
    # 全页扫描：th=职业名 + 8 个 td=加成（覆盖 下级/上级 两张表）
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.S):
        ths = [re.sub(r'<[^>]+>', '', t).strip() for t in re.findall(r'<th[^>]*>(.*?)</th>', tr, re.S)]
        tds = [re.sub(r'<[^>]+>', '', t).replace('&nbsp;', ' ').strip() for t in re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)]
        if not ths or len(tds) < 8:
            continue
        cls = ths[0]
        try:
            vals = [int(x) for x in tds[:8]]
        except ValueError:
            continue
        result[cls] = dict(zip(STATS, vals))

    with open('unit_bonus_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f'编成加成: {len(result)} 职业')
    for k in list(result)[:6]:
        print('  ', k, result[k])
    # 覆盖检查
    uo = json.load(open('../assets/uo-data.json', encoding='utf-8'))
    missing = [k for k in uo['classes'] if k not in result]
    print('uo-data 职业缺编成加成:', missing if missing else '无 ✅')


if __name__ == '__main__':
    main()
