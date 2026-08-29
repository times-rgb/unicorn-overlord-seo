# -*- coding: utf-8 -*-
"""
Unit Lab 数据采集 v3：从 HyperWiki 抓全 74 角色成长类型 + 起始装备
来源1: /unicorn/chara/ 角色列表（满级属性，用于交叉验证）
来源2: /unicorn/chara/xxx/ 角色详情页（成長タイプ / 初期・上級クラス / 基本装備 / 装備枠）
产出: scripts/hyper_chara_data.json
"""
import re
import json
import time
import os
import sys
import requests

# Windows 控制台 GBK 问题：强制 stdout UTF-8，避免打印 ✓/日文报错
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}
BASE = 'https://hyperwiki.jp/unicorn'
CHARA_LIST = BASE + '/chara/'
OUT = 'hyper_chara_data.json'
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def get(url, retries=3):
    for attempt in range(retries):
        try:
            r = SESSION.get(url, timeout=30)
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            print(f'   [retry {attempt+1}] {e}')
            time.sleep(2 + attempt * 2)
    return None


def parse_chara_list():
    html = get(CHARA_LIST)
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.S)
    chars = []
    for tr in rows:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if len(tds) < 12:
            continue
        cells = [re.sub(r'<[^>]+>', '', c).replace('&nbsp;', ' ').strip() for c in tds]
        links = re.findall(r'href="([^"]+)"[^>]*>([^<]*)</a>', tr)
        detail = next((u for u, t in links if '/chara/' in u and '/class/' not in u), '')
        cls_url = next((u for u, t in links if '/class/' in u), '')
        stats = {
            'hp': int(cells[1]), 'pAtk': int(cells[2]), 'pDef': int(cells[3]),
            'mAtk': int(cells[4]), 'mDef': int(cells[5]), 'acc': int(cells[6]),
            'eva': int(cells[7]), 'crit': int(cells[8]), 'guard': int(cells[9]),
            'spd': int(cells[10]), 'mov': int(cells[11]),
        }
        chars.append({'jp': cells[0], 'stats': stats, 'cls_jp': cells[12].split()[0],
                      'detail': detail, 'cls_url': cls_url})
    return chars


def th_value(html, label):
    """<th>label</th>\n<td>...</td> 取第一个 td"""
    m = re.search(re.escape(label) + r'</th>\s*<td[^>]*>(.*?)</td>', html, re.S)
    if not m:
        return None
    return m.group(1)


def clean(s):
    return re.sub(r'<[^>]+>', '', s or '').replace('&nbsp;', ' ').strip()


def parse_detail(html):
    d = {}
    raw_init = th_value(html, '初期クラス')
    raw_adv = th_value(html, '上級クラス')
    raw_gt = th_value(html, '成長タイプ')
    raw_eq = th_value(html, '基本装備')
    raw_slots = th_value(html, '装備枠')
    d['init_cls'] = clean(raw_init).split()[0] if raw_init and clean(raw_init) else None
    d['adv_cls'] = clean(raw_adv).split()[0] if raw_adv and clean(raw_adv) else None
    # 成长类型：<br> 分隔两个
    if raw_gt:
        parts = [p for p in re.split(r'<br\s*/?>|\n', raw_gt) if clean(p)]
        d['gt1'] = clean(parts[0]) if parts else None
        d['gt2'] = clean(parts[1]) if len(parts) > 1 else (clean(parts[0]) if parts else None)
    else:
        d['gt1'] = d['gt2'] = None
    # 基本装備：ul>li>a 文本
    if raw_eq:
        d['equip'] = [clean(t) for t in re.findall(r'<a[^>]*>(.*?)</a>', raw_eq, re.S) if clean(t)]
    else:
        d['equip'] = []
    d['slots'] = [s.strip() for s in (clean(raw_slots).split('/') if raw_slots else []) if s.strip()]
    # Lv50 分职业满级表（验证用）：每行 クラス+11 属性
    d['lv50'] = {}
    m = re.search(r'Lv50.*?ステータス.*?</h2>\s*<table[^>]*>(.*?)</table>', html, re.S)
    if m:
        for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', m.group(1), re.S):
            ths = re.findall(r'<th[^>]*>(.*?)</th>', tr, re.S)
            tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
            vals = [clean(x) for x in ths + tds if clean(x)]
            if len(vals) == 12 and vals[0]:
                try:
                    d['lv50'][vals[0]] = {
                        'hp': int(vals[1]), 'pAtk': int(vals[2]), 'pDef': int(vals[3]),
                        'mAtk': int(vals[4]), 'mDef': int(vals[5]), 'acc': int(vals[6]),
                        'eva': int(vals[7]), 'crit': int(vals[8]), 'guard': int(vals[9]),
                        'spd': int(vals[10]), 'mov': int(vals[11]),
                    }
                except ValueError:
                    pass
    return d


def main():
    # 断点续传：已有完成角色跳过
    done = {}
    if os.path.exists(OUT):
        try:
            for c in json.load(open(OUT, encoding='utf-8')):
                if c.get('gt1'):
                    done[c['jp']] = c
        except Exception:
            pass
    print(f'断点续传：已有 {len(done)} 个角色')

    chars = parse_chara_list()
    print(f'角色列表: {len(chars)} 人')

    out = [done[c['jp']] for c in chars if c['jp'] in done]
    todo = [c for c in chars if c['jp'] not in done]
    print(f'待抓: {len(todo)} 人')

    for i, c in enumerate(todo):
        html = get(c['detail'])
        if not html:
            print(f'[{i+1}/{len(todo)}] {c["jp"]} 抓取失败，跳过')
            continue
        det = parse_detail(html)
        c.update(det)
        out.append(c)
        ok = '✓' if (c.get('gt1') and c.get('gt2')) else '✗'
        lv50 = list(c.get('lv50', {}).keys())
        print(f'[{i+1:2}/{len(todo)}] {c["jp"]:8} {ok} {c.get("gt1")}/{c.get("gt2")}  '
              f'cls={c.get("init_cls")}→{c.get("adv_cls")}  equip={c.get("equip")}  lv50_cls={lv50}')
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        time.sleep(0.6)

    # 按列表顺序重排
    order = [c['jp'] for c in chars]
    ordered = sorted(out, key=lambda x: order.index(x['jp']) if x['jp'] in order else 999)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
    print('\n完成，共', len(ordered), '人')

    missing = [c['jp'] for c in ordered if not (c.get('gt1') and c.get('gt2'))]
    print('缺成长类型:', missing if missing else '无 ✅')
    all_gt = set()
    for c in ordered:
        for k in ('gt1', 'gt2'):
            if c.get(k):
                all_gt.add(c[k])
    print('成长类型 JP 名全集:', sorted(all_gt))


if __name__ == '__main__':
    main()
