# -*- coding: utf-8 -*-
"""从角色数据配对 JP↔EN 职业名 → 存 uo-data.clsName（JP→EN 展示名）"""
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

uo = json.load(open('../assets/uo-data.json', encoding='utf-8'))

cls_map = {}
for key, ch in uo['characters'].items():
    ens = ch.get('classes', [])
    jps = ch.get('classJPs', [])
    for jp, en in zip(jps, ens):
        if jp not in cls_map:
            cls_map[jp] = en
        # 有 'なし' 之外的对不齐时，补记录
for key, ch in uo['characters'].items():
    init = ch.get('initClsJP')
    adv = ch.get('advClsJP')
    ens = ch.get('classes', [])
    if init and len(ens) >= 1:
        cls_map.setdefault(init, ens[0])
    if adv and adv != 'なし' and len(ens) >= 2:
        cls_map.setdefault(adv, ens[1])

uo['clsName'] = cls_map
with open('../assets/uo-data.json', 'w', encoding='utf-8') as f:
    json.dump(uo, f, ensure_ascii=False, indent=1)
print('JP→EN 职业名映射:', len(cls_map), '条')
for jp, en in list(cls_map.items())[:20]:
    print('  ', jp, '→', en)
# 是否覆盖所有 classJPs 用到的职业
all_jps = set()
for ch in uo['characters'].values():
    all_jps.update(ch.get('classJPs', []))
missing = all_jps - set(cls_map)
print('覆盖检查: 用到', len(all_jps), '个职业，缺', sorted(missing) if missing else '无')
