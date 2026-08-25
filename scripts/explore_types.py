# -*- coding: utf-8 -*-
"""探查 para_type=3 和 RICH 节点"""
import re
import json
from collections import Counter

text = open('_opus_page.html', encoding='utf-8').read()
m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;', text, re.S)
data = json.loads(m.group(1))
mods = data['detail']['modules']
paras = None
for mod in mods:
    if mod.get('module_type') == 'MODULE_TYPE_CONTENT':
        paras = mod['module_content']['paragraphs']
        break

# para_type=3 样例
for p in paras:
    if p.get('para_type') == 3:
        print('para_type=3 sample:', json.dumps(p, ensure_ascii=False)[:400])
        break

# 所有 text.nodes 里的 node.type 分布 + RICH 样例
node_types = Counter()
rich_sample = None
for p in paras:
    if p.get('text') and p['text'].get('nodes'):
        for n in p['text']['nodes']:
            node_types[n.get('type')] += 1
            if n.get('type') == 'TEXT_NODE_TYPE_RICH' and rich_sample is None:
                rich_sample = n
print('node types:', dict(node_types))
if rich_sample:
    print('RICH sample:', json.dumps(rich_sample, ensure_ascii=False)[:300])
