# -*- coding: utf-8 -*-
"""
Unit Lab 数据采集 v2：从 Fandom api.php 批量抓 70 角色成长类型 + 起始装备
- 产出：scripts/fandom_growth.json（角色名 → growth1/growth2/起始属性/起始装备）
- 处理 Fandom 三种页面格式（标准 Stats 表 / infobox 模板 / 残缺页）
- 命名映射：Fandom(HyperWiki式) → uo-data.json 键（Toughness/Attacker/...）
  例：Hardy→Toughness, Offensive→Attacker, Go-Getter→Speedster, Keen→Slayer
- 抓不到的角色单独列出（宁缺毋滥，不瞎填）
"""
import re
import json
import time
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}
API = 'https://unicornoverlord.fandom.com/api.php'

# Fandom 实际显示的类型名 → uo-data.json 的 growthTypes 键
FANDOM_TO_UO = {
    'Hardy': 'Toughness',
    'Offensive': 'Attacker',
    'Defensive': 'Defender',
    'Precise': 'Technical',
    'Lucky': 'HighLuck',
    'Keen': 'Slayer',
    'Guardian': 'Guardian',
    'Go-Getter': 'Speedster',
    'All-Rounder': 'AllRounder',
    'AllRounder': 'AllRounder',  # 个别页无连字符
}

# 属性缩写（标准 Stats 表顺序）
STAT_ORDER = ['hp', 'pAtk', 'pDef', 'mAtk', 'mDef', 'acc', 'eva', 'crit', 'guard', 'spd']


def fetch_wikitext(page):
    r = requests.get(API, params={'action': 'parse', 'page': page, 'prop': 'wikitext',
                                  'format': 'json'}, headers=HEADERS, timeout=30)
    j = r.json()
    if 'error' in j:
        return None, j['error'].get('info', 'unknown')
    return j['parse']['wikitext']['*'], None


def parse_growth_standard(wt):
    """标准格式：!Default Growth Type 1 / 2"""
    g1 = re.search(r'Growth Type 1\s*\|\s*([^\n|]+)', wt)
    g2 = re.search(r'Growth Type 2\s*\|\s*([^\n|]+)', wt)
    return (g1.group(1).strip() if g1 else None,
            g2.group(1).strip() if g2 else None)


def parse_growth_infobox(wt):
    """infobox 模板：{{XCharacter|... growth=Hardy/Offensive ...}} 或类似字段"""
    for pat in [r'growth\s*=\s*([^|\n}]+)', r'Growth\s*=\s*([^|\n}]+)',
                r'growth_type\s*=\s*([^|\n}]+)', r'growthtypes\s*=\s*([^|\n}]+)']:
        m = re.search(pat, wt, re.I)
        if m:
            parts = [p.strip() for p in m.group(1).split('/') if p.strip()]
            if len(parts) >= 2:
                return parts[0], parts[1]
            if len(parts) == 1:
                return parts[0], parts[0]
    return None, None


def parse_starting_stats(wt):
    """标准格式的起始属性表：!HP | 31 | B"""
    stats = {}
    # 抓 "== Stats(*)" 之后的表格
    seg = re.search(r'==\s*Stats.*?==\s*\n(.*?)(?====|$)', wt, re.S)
    if not seg:
        return stats
    table = seg.group(1)
    # 行: !Stat Name | Starting Stat | Letter，和 !HP |31|B
    rows = re.findall(r'!\s*([^|\n]+?)\s*\|\s*([^\n|]+?)\s*\|', table)
    name_map = {
        'HP': 'hp', 'Phys. ATK': 'pAtk', 'Phys. DEF': 'pDef', 'Mag. ATK': 'mAtk',
        'Mag. DEF': 'mDef', 'Accuracy': 'acc', 'Evasion': 'eva',
        'Crit. Rate': 'crit', 'Guard Rate': 'guard', 'Initiative': 'spd',
    }
    for raw_name, raw_val in rows:
        key = name_map.get(raw_name.strip())
        if key:
            val = raw_val.strip().rstrip('%')
            try:
                stats[key] = int(float(val))
            except ValueError:
                pass
    return stats


def parse_starting_equip(wt):
    """== Starting Equipment == 段的 [[链接]]"""
    seg = re.search(r'==\s*Starting Equipment\s*==\s*\n(.*?)(?====|$)', wt, re.S)
    if not seg:
        return []
    return re.findall(r'\[\[([^\]|]+)', seg.group(1))


def map_type(raw):
    if not raw:
        return None
    return FANDOM_TO_UO.get(raw.strip(), None)


def main():
    # 读角色清单（以 uo-data.json 的 characters 为准）
    uo = json.load(open('../assets/uo-data.json', encoding='utf-8'))
    chars = uo['characters']
    # 兼容键名：Fandom 页名 = 角色显示名
    result = {}
    missing = []
    for key, ch in chars.items():
        page = ch.get('name', key)
        wt, err = fetch_wikitext(page)
        if wt is None:
            missing.append({'key': key, 'reason': 'fetch_error: ' + str(err)})
            print(f'[{key}] FETCH ERROR: {err}')
            continue
        g1r, g2r = parse_growth_standard(wt)
        if not g1r:
            g1r, g2r = parse_growth_infobox(wt)
        g1, g2 = map_type(g1r), map_type(g2r)
        entry = {
            'key': key,
            'name': page,
            'growth1_raw': g1r,
            'growth2_raw': g2r,
            'growth1': g1,
            'growth2': g2,
            'baseStats': parse_starting_stats(wt),
            'startingEquip': parse_starting_equip(wt),
        }
        result[key] = entry
        status = f'{g1}/{g2}' if g1 and g2 else 'MISSING'
        equip = len(entry['startingEquip'])
        print(f'[{key:14}] {status:12} equip={equip}')
        if not g1 or not g2:
            missing.append({'key': key, 'reason': 'no_growth_type', 'raw': f'{g1r}/{g2r}'})
        time.sleep(0.4)

    with open('fandom_growth.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print('\n=== 汇总 ===')
    got = sum(1 for v in result.values() if v['growth1'] and v['growth2'])
    print(f'抓到成长类型: {got}/{len(chars)}')
    if missing:
        print('缺失:')
        for m in missing:
            print('  ', m)
    else:
        print('无缺失 ✅')


if __name__ == '__main__':
    main()
