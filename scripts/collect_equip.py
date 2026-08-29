# -*- coding: utf-8 -*-
"""
Unit Lab 装备采集：抓 HyperWiki 8 类装备列表页
sword/axe/lance/bow/rod/shield/accessory/bigshield
每件: 名称(JP) / 物理 / 魔法 / 买价 / 效果文本 / 详情链接 / 槽位
产出: scripts/equipment_data.json
"""
import re
import json
import time
import sys
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}
PAGES = {
    'sword': 'https://hyperwiki.jp/unicorn/sword/',
    'axe': 'https://hyperwiki.jp/unicorn/axe/',
    'lance': 'https://hyperwiki.jp/unicorn/lance/',
    'bow': 'https://hyperwiki.jp/unicorn/bow/',
    'rod': 'https://hyperwiki.jp/unicorn/rod/',
    'shield': 'https://hyperwiki.jp/unicorn/shield/',
    'accessory': 'https://hyperwiki.jp/unicorn/accessory/',
    'bigshield': 'https://hyperwiki.jp/unicorn/bigshield/',
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def clean(s):
    return re.sub(r'<[^>]+>', '', s or '').replace('&nbsp;', ' ').replace('\u3000', ' ').strip()


def parse_effect(effect_text):
    """解析效果文本 → 简化加成 {stat: val}。如 'HPアップ[3]' → {'hp':3}"""
    bonus = {}
    if not effect_text:
        return bonus, effect_text
    m = re.search(r'(HP|物理|魔法|命中|回避|会心|ガード|行速)アップ\s*\[?([+\-]?\d+)\]?', effect_text)
    if m:
        stat = {'HP': 'hp', '物理': 'pAtk', '魔法': 'mAtk', '命中': 'acc',
                '回避': 'eva', '会心': 'crit', 'ガード': 'guard', '行速': 'spd'}[m.group(1)]
        bonus[stat] = int(m.group(2))
    return bonus, effect_text


def parse_page(slot, url):
    r = SESSION.get(url, timeout=60)
    r.encoding = r.apparent_encoding
    html = r.text
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.S)
    items = []
    for tr in rows:
        ths = re.findall(r'<th[^>]*>(.*?)</th>', tr, re.S)
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if not ths or not tds:
            continue
        name = clean(ths[0])
        # 详情链接在第一个 td 内
        link = re.search(r'href="([^"]+)"', tds[0])
        detail = link.group(1) if link else ''
        # 前 2 个 td 为 物理/魔法（accessory 可能没有），其余为买价+效果
        vals = [clean(t) for t in tds]
        def num(s):
            return int(s) if re.fullmatch(r'[+\-]?\d+', s) else None
        phys = num(vals[0]) if len(vals) > 0 else None
        magic = num(vals[1]) if len(vals) > 1 else None
        price = None
        effect = ''
        # 买价与效果：从剩余列里找纯数字=价格，其余拼为效果
        rest = vals[2:]
        for v in rest:
            n = num(v)
            if n is not None and price is None:
                price = n
            else:
                effect += (' ' + v if effect else v)
        bonus, _ = parse_effect(effect)
        items.append({'slot': slot, 'name': name, 'phys': phys, 'magic': magic,
                      'price': price, 'effect': effect, 'bonus': bonus, 'detail': detail})
    return items


def main():
    all_items = []
    for slot, url in PAGES.items():
        try:
            items = parse_page(slot, url)
        except Exception as e:
            print(f'[{slot}] 抓取失败: {e}')
            continue
        print(f'[{slot}] {len(items)} 件')
        for it in items[:3]:
            print('    ', it['name'], 'phys=', it['phys'], 'magic=', it['magic'],
                  'price=', it['price'], 'effect=', it['effect'][:40], 'bonus=', it['bonus'])
        all_items += items
        time.sleep(0.5)

    with open('equipment_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=1)
    print(f'\n共 {len(all_items)} 件装备，已保存 equipment_data.json')


if __name__ == '__main__':
    main()
