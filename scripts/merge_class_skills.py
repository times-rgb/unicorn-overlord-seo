# -*- coding: utf-8 -*-
"""把 class_skills_data.json 合并进 uo-data.json 的 classSkills 字段"""
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

uo = json.load(open('../assets/uo-data.json', encoding='utf-8'))
sk = json.load(open('class_skills_data.json', encoding='utf-8'))

uo['classSkills'] = sk
total = sum(sum(len(v) for v in c.values()) for c in sk.values())
print(f'classSkills 合并: {len(sk)} 职业, {total} 技能')
# 抽查
for k in ['ロード', 'ハイロード']:
    print(k, '=> active:', [s['name'] for s in sk.get(k, {}).get('active', [])])
with open('../assets/uo-data.json', 'w', encoding='utf-8') as f:
    json.dump(uo, f, ensure_ascii=False, indent=1)
print('已保存')
