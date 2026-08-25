# -*- coding: utf-8 -*-
"""探查 detail 结构，打印 key 树"""
import re
import json

text = open('_opus_page.html', encoding='utf-8').read()
m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;', text, re.S)
data = json.loads(m.group(1))
detail = data.get('detail')
print('detail type:', type(detail).__name__)
if isinstance(detail, dict):
    print('detail keys:', list(detail.keys()))
    # 找含 opus 的
    for k, v in detail.items():
        if isinstance(v, (dict, list)):
            print(f'  {k}: {type(v).__name__}', end=' ')
            if isinstance(v, dict):
                print(list(v.keys())[:15])
            else:
                print(f'len={len(v)}')
        else:
            print(f'  {k}: {str(v)[:80]}')
