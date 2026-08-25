# -*- coding: utf-8 -*-
"""探查 paragraphs 结构与图片节点"""
import re
import json

text = open('_opus_page.html', encoding='utf-8').read()
m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;', text, re.S)
data = json.loads(m.group(1))
mods = data['detail']['modules']
paras = None
for mod in mods:
    if mod.get('module_type') == 'MODULE_TYPE_CONTENT':
        paras = mod['module_content']['paragraphs']
        break

print('total paras:', len(paras))
# 统计 para_type 分布
from collections import Counter
types = Counter(p.get('para_type') for p in paras)
print('para_type dist:', dict(types))

# 前 8 个段落的结构
for i, p in enumerate(paras[:8]):
    print(f'--- [{i}] para_type={p.get("para_type")} keys={list(p.keys())}')
    print('   ', json.dumps(p, ensure_ascii=False)[:300])
