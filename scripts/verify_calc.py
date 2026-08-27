# -*- coding: utf-8 -*-
"""计算引擎验证：用 uo-data.json + HyperWiki 公式，验证 Alain High Lord Lv50 满级属性"""
import json

d = json.load(open('uo-data.json', encoding='utf-8'))
exp = d['expTable']
gtA = d['growthTypes']['A']
gtB = d['growthTypes']['B']
classes = d['classes']

# 职业英→日 成长率名映射（覆盖主要职业）
CLS_JP = {
    'Lord': 'ロード', 'High Lord': 'ハイロード', 'Fighter': 'ファイター', 'Vanguard': 'ヴァンガード',
    'Soldier': 'ソルジャー', 'Sergeant': 'サージェント', 'Knight': 'ナイト', 'Great Knight': 'グレートナイト',
    'Paladin': 'パラディン', 'Priestess': 'プリーステス', 'High Priestess': 'ハイプリーステス',
    'Snow Ranger': 'スノーレンジャー', 'Cleric': 'クレリック', 'Bishop': 'ビショップ',
    'Thief': 'シーフ', 'Rogue': 'ローグ', 'Wizard': 'ウィザード', 'Witch': 'ウィッチ',
    'Hunter': 'ハンター', 'Sniper': 'スナイパー', 'Shooter': 'シューター', 'Shield Shooter': 'シールドシューター',
    'Hoplite': 'ホプリタイ', 'Legionnaire': 'カタフラクト', 'Wing Shield': 'フェザーシールド', 'Elf Augur': 'エルフアウグル',
    'Elven Augur': 'エルフアウグル', 'Feather Bow': 'フェザーボウ', 'Feather Sword': 'フェザーソード', 'Feather Rod': 'フェザーロッド',
}
STAT_KEYS = ['hp', 'pAtk', 'pDef', 'mAtk', 'mDef', 'acc', 'eva', 'crit', 'guard', 'spd', 'mov']


def calc(character, cls_en, level=50, use_dew=False):
    g1, g2 = character['growth1'], character['growth2']
    jp = CLS_JP.get(cls_en)
    if jp not in classes:
        return None, f'职业映射缺失: {cls_en}'
    g = classes[jp]
    lv = exp.get(str(level))
    if not lv:
        return None, f'等级缺失: {level}'
    out = {}
    # 10 维补正（不含 mov）
    for i, k in enumerate(STAT_KEYS[:10]):
        A_avg = round((gtA[g1][i] + gtA[g2][i]) / 2)
        B_avg = round((gtB[g1][i] + gtB[g2][i]) / 2)
        base = round(lv[k] / 100 * (A_avg + g[k]) + B_avg)
        if k == 'acc':
            base += 100  # 命中显示修正
        out[k] = base
    out['mov'] = g['mov']
    if use_dew:  # 全药（每种 5 瓶）: hp+10 pAtk+5 pDef+5 mAtk+5 mDef+5 acc+10 eva+10 crit+5 guard+5 spd+5
        dew = {'hp': 10, 'pAtk': 5, 'pDef': 5, 'mAtk': 5, 'mDef': 5, 'acc': 10, 'eva': 10, 'crit': 5, 'guard': 5, 'spd': 5, 'mov': 0}
        for k in STAT_KEYS:
            out[k] = out[k] + dew.get(k, 0)
    return out, None


# 验证 1: Alain High Lord Lv50（期望 104/45/39/43/42/152/67/21/30/44）
alain = d['characters']['alain']
r, err = calc(alain, 'High Lord', 50)
print('Alain High Lord Lv50:', r)
expct = {'hp': 104, 'pAtk': 45, 'pDef': 39, 'mAtk': 43, 'mDef': 42, 'acc': 152, 'eva': 67, 'crit': 21, 'guard': 30, 'spd': 44}
if r and not err:
    ok = all(r[k] == expct[k] for k in expct)
    print('  vs 期望:', expct)
    print('  校验:', '✅ 全对' if ok else '❌ 有差 ' + str({k: (r[k], expct[k]) for k in expct if r[k] != expct[k]}))

# 验证 2: Alain Lord Lv1（对照 Fandom 起始属性 31/11/8/11/11/124/32/10/14/18）
r, err = calc(alain, 'Lord', 1)
print('Alain Lord Lv1:', r, err)
expct1 = {'hp': 31, 'pAtk': 11, 'pDef': 8, 'mAtk': 11, 'mDef': 11, 'acc': 124, 'eva': 32, 'crit': 10, 'guard': 14, 'spd': 18}
if r and not err:
    ok = all(r[k] == expct1[k] for k in expct1)
    print('  校验:', '✅ 全对' if ok else '❌ ' + str({k: (r[k], expct1[k]) for k in expct1 if r[k] != expct1[k]}))

# 验证 3: Alain High Lord Lv50 全药
r, err = calc(alain, 'High Lord', 50, use_dew=True)
print('Alain Lv50 全药:', r, err)

# 验证 4: Josef Paladin Lv50（无期望，输出参考）
josef = d['characters']['josef']
r, err = calc(josef, 'Paladin', 50)
print('Josef Paladin Lv50:', r, err)
