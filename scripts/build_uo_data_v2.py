# -*- coding: utf-8 -*-
"""
Unit Lab 数据组装 v2：把装备表 + 角色职业键合并进 uo-data.json
1. equipment: 556 件（slot/name/phys/magic/price/effect/bonus/detail）
2. 每个角色加 classJPs（可直接索引 data.classes 的 JP 职业键）
3. slot→装备类别 映射
"""
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 日文槽位 → 装备类别
SLOT_CAT = {
    '剣': 'sword', '斧': 'axe', '槍': 'lance', '弓': 'bow', '杖': 'rod',
    '盾': 'shield', '大盾': 'bigshield', 'アクセ': 'accessory',
    'アクセ１': 'accessory', 'アクセ２': 'accessory', 'アクセサリ': 'accessory',
}


def main():
    uo = json.load(open('../assets/uo-data.json', encoding='utf-8'))
    equip = json.load(open('equipment_data.json', encoding='utf-8'))

    # 1. 装备表（按槽位分类索引 + 扁平数组）
    uo['equipment'] = equip
    by_slot = {}
    for it in equip:
        by_slot.setdefault(it['slot'], []).append(it)
    uo['equipBySlot'] = {k: [i['name'] for i in v] for k, v in by_slot.items()}

    # 2. 每角色 classJPs
    n_class = 0
    for key, ch in uo['characters'].items():
        jps = []
        if ch.get('initClsJP'):
            jps.append(ch['initClsJP'])
        adv = ch.get('advClsJP')
        if adv and adv != 'なし' and adv not in jps:
            jps.append(adv)
        if jps:
            ch['classJPs'] = jps
            n_class += 1
    print(f'有 classJPs 的角色: {n_class}/70')

    # 3. 槽位映射
    uo['slotCat'] = SLOT_CAT

    with open('../assets/uo-data.json', 'w', encoding='utf-8') as f:
        json.dump(uo, f, ensure_ascii=False, indent=1)
    print('已保存 assets/uo-data.json')
    print('装备:', len(uo['equipment']), '件')
    print('各类别数量:', {k: len(v) for k, v in by_slot.items()})
    # 抽查一个角色
    for k in ['alain', 'josef', 'colm']:
        ch = uo['characters'][k]
        print(k, '=>', ch.get('growth1'), '/', ch.get('growth2'),
              'classJPs=', ch.get('classJPs'), 'equipJP=', ch.get('startingEquipJP'))


if __name__ == '__main__':
    main()
