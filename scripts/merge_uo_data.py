# -*- coding: utf-8 -*-
"""
Unit Lab 数据合并 v1：hyper_chara_data.json → uo-data.json
1. 成长类型 JP→键 映射（タフネス→Toughness 等）
2. 按英文名匹配 70 角色，写入 growth1/growth2/起始装备/可转职职业
3. 交叉验证：用公式重算 Lv50（转职职业+成长类型）与 HyperWiki 列表对比
"""
import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# JP 成长类型名 → uo-data growthTypes 键（实测与 HyperWiki 表一致）
JP_GT = {
    'タフネス': 'Toughness',      # Hardy
    'アタッカー': 'Attacker',      # Offensive
    'ディフェンダー': 'Defender',  # Defensive
    'テクニカル': 'Technical',    # Precise
    'ハイラック': 'HighLuck',      # Lucky
    'スレイヤー': 'Slayer',       # Keen
    'ガーディアン': 'Guardian',   # Guardian
    'スピードスター': 'Speedster',  # Go-Getter
    'オールマイティ': 'AllRounder',  # All-Rounder
}

STAT_KEYS = ['hp', 'pAtk', 'pDef', 'mAtk', 'mDef', 'acc', 'eva', 'crit', 'guard', 'spd']


def norm_name(s):
    """去重音字符 + 小写，用于模糊匹配英文名"""
    if not s:
        return ''
    # 拉丁重音 → 基础字母
    accents = {'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'à': 'a', 'á': 'a', 'â': 'a',
               'ï': 'i', 'î': 'i', 'ö': 'o', 'ô': 'o', 'ü': 'u', 'û': 'u', 'ç': 'c'}
    out = ''.join(accents.get(ch, ch) for ch in s)
    return out.lower().strip()


def main():
    uo = json.load(open('../assets/uo-data.json', encoding='utf-8'))
    hyper = json.load(open('hyper_chara_data.json', encoding='utf-8'))

    # 1. 建立英文名索引（uo-data 角色）
    uo_by_name = {}
    for key, ch in uo['characters'].items():
        uo_by_name[norm_name(ch.get('name', key))] = key

    # 2. 合并
    merged = 0
    unmatched = []
    report = []
    for c in hyper:
        en = c.get('en_name', '')
        key = uo_by_name.get(norm_name(en))
        if not key:
            unmatched.append({'jp': c['jp'], 'en': en})
            continue
        ch = uo['characters'][key]
        g1 = JP_GT.get(c.get('gt1'))
        g2 = JP_GT.get(c.get('gt2'))
        ch['growth1'] = g1
        ch['growth2'] = g2
        # 起始装备（保留英文名原字段；此处存 JP 名，附带原名备查）
        ch['startingEquipJP'] = c.get('equip', [])
        ch['slotsJP'] = c.get('slots', [])
        ch['initClsJP'] = c.get('init_cls')
        ch['advClsJP'] = c.get('adv_cls')
        ch['lv50Ref'] = c.get('stats', {})   # HyperWiki 满级参考值（验证用）
        merged += 1
        report.append({'key': key, 'en': en, 'g1': g1, 'g2': g2,
                       'cls': f"{c.get('init_cls')}→{c.get('adv_cls')}"})

    print(f'合并成功: {merged}/70')
    if unmatched:
        print('未匹配:', unmatched)

    # 3. 交叉验证：用公式重算 Lv50 对比 HyperWiki 列表
    exp = uo['expTable']['50']
    clsTbl = uo['classes']
    gtA = uo['growthTypes']['A']
    gtB = uo['growthTypes']['B']
    ok = 0
    fails = []
    for r in report:
        key = r['key']
        ch = uo['characters'][key]
        g1, g2 = r['g1'], r['g2']
        ref = ch.get('lv50Ref', {})
        # 转职职业：advCls 优先，なし 则用 initCls
        adv = ch.get('advClsJP')
        if adv and adv != 'なし' and adv in clsTbl:
            cls_jp = adv
        else:
            cls_jp = ch.get('initClsJP')
        cls = clsTbl.get(cls_jp)
        if not cls or not g1 or not g2 or not ref:
            continue
        a1, a2 = gtA.get(g1), gtA.get(g2)
        b1, b2 = gtB.get(g1), gtB.get(g2)
        if not a1 or not a2:
            continue
        calc = {}
        for i, sk in enumerate(STAT_KEYS):
            A = round((a1[i] + a2[i]) / 2) + cls[sk]
            B = round((b1[i] + b2[i]) / 2)
            v = round(exp[sk] / 100 * A + B)
            if sk == 'acc':
                v += 100
            calc[sk] = v
        diff = {sk: abs(calc[sk] - ref[sk]) for sk in STAT_KEYS if sk in ref}
        if all(d <= 1 for d in diff.values()):
            ok += 1
        else:
            fails.append({'key': key, 'cls': cls_jp, 'calc': calc, 'ref': ref, 'diff': diff})

    print(f'验证通过: {ok}/{len(report)}')
    if fails:
        print(f'验证失败: {len(fails)}')
        for f in fails[:10]:
            print(' ', f['key'], f['cls'], 'diff=', f['diff'])

    # 4. 保存
    uo['meta']['charGrowth'] = 'collected from hyperwiki.jp/unicorn/chara (2026-08-29)'
    with open('../assets/uo-data.json', 'w', encoding='utf-8') as f:
        json.dump(uo, f, ensure_ascii=False, indent=1)
    print('已保存 assets/uo-data.json')


if __name__ == '__main__':
    main()
