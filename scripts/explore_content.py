# -*- coding: utf-8 -*-
"""探查 module_content 结构"""
import re
import json

text = open('_opus_page.html', encoding='utf-8').read()
m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;', text, re.S)
data = json.loads(m.group(1))
mods = data['detail']['modules']
for mod in mods:
    if mod.get('module_type') == 'MODULE_TYPE_CONTENT':
        content = mod.get('module_content')
        print('module_content type:', type(content).__name__)
        if isinstance(content, dict):
            print('keys:', list(content.keys()))
            for k, v in content.items():
                if isinstance(v, list):
                    print(f'  {k}: list len={len(v)}')
                elif isinstance(v, dict):
                    print(f'  {k}: dict keys={list(v.keys())[:12]}')
                else:
                    print(f'  {k}: {str(v)[:60]}')
        break
