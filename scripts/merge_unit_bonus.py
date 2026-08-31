# -*- coding: utf-8 -*-
"""unit_bonus_data.json → uo-data.json 的 unitBonus 字段"""
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

uo = json.load(open('../assets/uo-data.json', encoding='utf-8'))
ub = json.load(open('unit_bonus_data.json', encoding='utf-8'))
uo['unitBonus'] = ub
with open('../assets/uo-data.json', 'w', encoding='utf-8') as f:
    json.dump(uo, f, ensure_ascii=False, indent=1)
print(f'unitBonus 合并: {len(ub)} 职业')
