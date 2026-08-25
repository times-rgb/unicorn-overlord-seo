# -*- coding: utf-8 -*-
"""探查 detail.modules 各模块，找到 opus 正文模块"""
import re
import json

text = open('_opus_page.html', encoding='utf-8').read()
m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;', text, re.S)
data = json.loads(m.group(1))
detail = data['detail']
mods = detail['modules']
print('module count:', len(mods))
for i, mod in enumerate(mods):
    mtype = mod.get('module_type')
    keys = list(mod.keys())
    # 找模块里的 opus
    opus = None
    for k, v in mod.items():
        if isinstance(v, dict) and 'opus' in v:
            opus = v['opus']
            break
    info = f'[{i}] type={mtype} keys={keys[:8]}'
    if opus:
        info += f' OPUS! keys={list(opus.keys())[:12]}'
        s = opus.get('summary')
        if s and isinstance(s, dict):
            info += f' summary.keys={list(s.keys())} paras={len(s.get("paragraphs") or []) if isinstance(s.get("paragraphs"), list) else "?"}'
    print(info)
