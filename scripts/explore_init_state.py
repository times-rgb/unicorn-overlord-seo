# -*- coding: utf-8 -*-
"""解析 _opus_page.html 中的 __INITIAL_STATE__，定位 opus 正文数据"""
import re
import json

text = open('_opus_page.html', encoding='utf-8').read()

# 提取 window.__INITIAL_STATE__ = {...};
m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;', text, re.S)
if not m:
    print('NO __INITIAL_STATE__ found')
    raise SystemExit(1)

data = json.loads(m.group(1))
print('top keys:', list(data.keys())[:20])


def find_paragraphs_paths(obj, path='', depth=0, out=None):
    if out is None:
        out = []
    if depth > 12 or len(out) > 40:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'paragraphs' and isinstance(v, list):
                out.append(path + '/' + k + f'  len={len(v)}')
            find_paragraphs_paths(v, path + '/' + k, depth + 1, out)
    elif isinstance(obj, list):
        if obj and isinstance(obj[0], (dict, list)):
            find_paragraphs_paths(obj[0], path + '[0]', depth + 1, out)
    return out


paths = find_paragraphs_paths(data)
print('paragraphs paths:')
for p in paths[:40]:
    print('  ', p)
