# -*- coding: utf-8 -*-
"""数据采集 v3：修正解析（stat-calc 数值行/类型名硬编码、growth 13列、exptable th+td、Fandom 类型名映射+起始属性）"""
import re
import json
import requests

BASE = 'https://hyperwiki.jp/unicorn/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}


def get(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.encoding = r.apparent_encoding
    return r.text


def clean(s):
    return re.sub(r'<[^>]+>', '', s).replace('&nbsp;', ' ').replace('\u3000', ' ').replace('&amp;', '&').strip()


def tds(tr):
    return [clean(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)]


TYPE_MAP = {
    'Aggressive': 'Attacker', 'Hardy': 'Toughness', 'Defensive': 'Defender',
    'Precise': 'Technical', 'Lucky': 'HighLuck', 'Slayer': 'Slayer',
    'Guardian': 'Guardian', 'Swift': 'Speedster', 'All-Rounder': 'AllRounder',
}
GT_ORDER = ['Toughness', 'Attacker', 'Defender', 'Technical', 'HighLuck', 'Slayer', 'Guardian', 'Speedster', 'AllRounder']

data = {'meta': {'game': 'Unicorn Overlord', 'collected': '2026-08-27',
                 'typeMap': TYPE_MAP, 'sources': ['hyperwiki.jp/unicorn/stat-calc', 'hyperwiki.jp/unicorn/exptable',
                                                  'hyperwiki.jp/unicorn/growth', 'unicornoverlord.fandom.com']}}

rows = [r for r in [tds(tr) for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', get(BASE + 'stat-calc/'), re.S)]
        if len(r) == 10 and all(re.match(r'^-?\d+$', x) for x in r)]
assert len(rows) >= 18, f'stat-calc rows: {len(rows)}'
A = {GT_ORDER[i]: [int(x) for x in rows[i]] for i in range(9)}
B = {GT_ORDER[i]: [int(x) for x in rows[9 + i]] for i in range(9)}
data['growthTypes'] = {'A': A, 'B': B}
print('growthTypes A:', len(A), 'B:', len(B))

exp = {}
for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', get(BASE + 'exptable/'), re.S):
    thm = re.search(r'<th[^>]*>(\d+)</th>', tr)
    td = tds(tr)
    if thm and len(td) == 12:
        lv = int(thm.group(1))
        v = [float(x) for x in td[1:12]]  # td[0]=exp 跳过；td[1:12]=hp..mov 11 项
        exp[lv] = {'hp': v[0], 'pAtk': v[1], 'pDef': v[2], 'mAtk': v[3], 'mDef': v[4], 'acc': v[5],
                   'eva': v[6], 'crit': v[7], 'guard': v[8], 'spd': v[9], 'mov': v[10]}
data['expTable'] = exp
print('expTable:', len(exp), 'Lv50:', exp.get(50))

classes = {}
for r in [tds(tr) for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', get(BASE + 'growth/'), re.S)]:
    if len(r) == 13 and r[0] and not re.match(r'^-?\d', r[0]):
        name = re.split(r'\s+', r[0])[0]
        try:
            v = [int(x) for x in r[1:12]]
            classes[name] = {'hp': v[0], 'pAtk': v[1], 'pDef': v[2], 'mAtk': v[3], 'mDef': v[4], 'acc': v[5],
                             'eva': v[6], 'crit': v[7], 'guard': v[8], 'spd': v[9], 'mov': v[10]}
        except ValueError:
            pass
data['classes'] = classes
print('classes:', len(classes))

CHARS = ['Alain', 'Scarlett', 'Yunifi', 'Josef', 'Clive']
fandom_chars = {}
for c in CHARS:
    try:
        u = f'https://unicornoverlord.fandom.com/api.php?action=parse&page={c}&format=json&prop=text'
        t = requests.get(u, headers=HEADERS, timeout=30).json()['parse']['text']['*']
        gt1 = re.search(r'Default Growth Type 1\s*</th>\s*<td[^>]*>([^<]+)', t)
        gt2 = re.search(r'Default Growth Type 2\s*</th>\s*<td[^>]*>([^<]+)', t)
        g1 = TYPE_MAP.get(clean(gt1.group(1)), clean(gt1.group(1))) if gt1 else None
        g2 = TYPE_MAP.get(clean(gt2.group(1)), clean(gt2.group(1))) if gt2 else None
        stats = {}
        NAME_KEY = {'HP': 'hp', 'Phys. ATK': 'pAtk', 'Phys. DEF': 'pDef', 'Mag. ATK': 'mAtk', 'Mag. DEF': 'mDef',
                    'Accuracy': 'acc', 'Evasion': 'eva', 'Crit. Rate': 'crit', 'Guard Rate': 'guard', 'Initiative': 'spd'}
        for m in re.finditer(r'<td[^>]*>([^<]+?)</td>\s*<td[^>]*>(-?\d+)%?</td>\s*<td[^>]*>([A-F])</td>', t):
            key = NAME_KEY.get(m.group(1).strip())
            if key:
                stats[key] = {'v': int(m.group(2)), 'l': m.group(3)}
        eqm = re.search(r'>Starting Equipment</td>\s*<td[^>]*>(.*?)</td>', t, re.S)
        equips = re.findall(r'\[\[([^\]|]+)', eqm.group(1)) if eqm else []
        fandom_chars[c.lower()] = {'name': c, 'growth1': g1, 'growth2': g2, 'baseStats': stats, 'startingEquip': equips}
        print(f'  {c}: {g1}/{g2} stats={len(stats)} equip={equips}')
    except Exception as e:
        print('  ERR', c, e)
data['characters'] = fandom_chars

with open('uo-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print('saved uo-data.json characters:', len(fandom_chars))
