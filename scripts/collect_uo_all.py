# -*- coding: utf-8 -*-
"""数据采集 v4：全 70 人（Fandom 成长类型/起始属性/起始装备）+ 合并 fandom_chars.json 的阵营/头像/职业"""
import re
import json
import requests

BASE = 'https://hyperwiki.jp/unicorn/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}


def clean(s):
    return re.sub(r'<[^>]+>', '', s).replace('&nbsp;', ' ').replace('\u3000', ' ').replace('&amp;', '&').strip()


TYPE_MAP = {
    'Aggressive': 'Attacker', 'Hardy': 'Toughness', 'Defensive': 'Defender',
    'Precise': 'Technical', 'Lucky': 'HighLuck', 'Slayer': 'Slayer',
    'Guardian': 'Guardian', 'Swift': 'Speedster', 'All-Rounder': 'AllRounder',
    # Fandom 混名 → HyperWiki 9 种
    'Offensive': 'Attacker', 'Go-Getter': 'Speedster', 'Keen': 'Technical',
    'Toughness': 'Toughness', 'Defender': 'Defender', 'Technical': 'Technical',
    'HighLuck': 'HighLuck', 'High Luck': 'HighLuck', 'All Rounder': 'AllRounder', 'Speedster': 'Speedster',
}
NAME_KEY = {'HP': 'hp', 'Phys. ATK': 'pAtk', 'Phys. DEF': 'pDef', 'Mag. ATK': 'mAtk', 'Mag. DEF': 'mDef',
            'Accuracy': 'acc', 'Evasion': 'eva', 'Crit. Rate': 'crit', 'Guard Rate': 'guard', 'Initiative': 'spd'}

# 载入已有数据（公式/表）
d = json.load(open('uo-data.json', encoding='utf-8'))
# 载入 70 人基础（阵营/头像/职业）
fandom = json.load(open('fandom_chars.json', encoding='utf-8'))
name_meta = {}
for faction, chars in fandom.items():
    for c in chars:
        slug = c['name'].lower()
        name_meta[c['name']] = {'faction': faction, 'classes': c['classes']}
        # 头像：fandom img 或本地 webp
        name_meta[c['name']]['img'] = f'/assets/chars/{faction.lower()}_{c["name"]}.webp'

# 70 角色英文名
all_names = [c['name'] for _, chars in fandom.items() for c in chars]
print('总角色:', len(all_names))

chars = {}
ok = 0
for i, name in enumerate(all_names, 1):
    slug = name.lower()
    try:
        u = f'https://unicornoverlord.fandom.com/api.php?action=parse&page={name}&format=json&prop=text'
        t = requests.get(u, headers=HEADERS, timeout=30).json()['parse']['text']['*']
        gt1 = re.search(r'Default Growth Type 1\s*</th>\s*<td[^>]*>([^<]+)', t)
        gt2 = re.search(r'Default Growth Type 2\s*</th>\s*<td[^>]*>([^<]+)', t)
        g1 = TYPE_MAP.get(clean(gt1.group(1)), clean(gt1.group(1))) if gt1 else None
        g2 = TYPE_MAP.get(clean(gt2.group(1)), clean(gt2.group(1))) if gt2 else None
        # 起始属性（宽容：3 连 td = 名/值/评级）
        stats = {}
        seg = t[t.find('Starting Stat'):t.find('Starting Equipment')] if t.find('Starting Stat') >= 0 else ''
        cells = [clean(c) for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', seg, re.S)]
        for j in range(len(cells) - 2):
            k = NAME_KEY.get(cells[j])
            if k and re.match(r'^-?\d+%?$', cells[j + 1]) and re.match(r'^[A-F]$', cells[j + 2]):
                stats[k] = {'v': int(cells[j + 1].rstrip('%')), 'l': cells[j + 2]}
        # 起始装备
        eqm = re.search(r'>Starting Equipment</td>\s*<td[^>]*>(.*?)</td>', t, re.S)
        equips = re.findall(r'\[\[([^\]|]+)', eqm.group(1)) if eqm else []
        meta = name_meta.get(name, {})
        chars[slug] = {'name': name, 'faction': meta.get('faction'), 'img': meta.get('img'),
                       'classes': meta.get('classes', []), 'growth1': g1, 'growth2': g2,
                       'baseStats': stats, 'startingEquip': equips}
        if g1 and g2:
            ok += 1
        if i <= 5 or i % 15 == 0:
            print(f'  [{i}] {name}: {g1}/{g2} stats={len(stats)} fac={meta.get("faction")}')
    except Exception as e:
        print(f'  [{i}] ERR {name}: {e}')
        meta = name_meta.get(name, {})
        chars[slug] = {'name': name, 'faction': meta.get('faction'), 'img': meta.get('img'),
                       'classes': meta.get('classes', []), 'growth1': None, 'growth2': None,
                       'baseStats': {}, 'startingEquip': []}

d['characters'] = chars
with open('uo-data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print(f'saved uo-data.json 角色: {len(chars)}，有成长类型: {ok}')
