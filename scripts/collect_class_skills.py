# -*- coding: utf-8 -*-
"""
Unit Lab 技能采集：从 73 个职业详情页抓「習得するスキル」
每个职业: 主动/被动/勇者/领导 4 类技能（技能名 + 习得等级 + 效果）
产出: scripts/class_skills_data.json  { 职业JP名: {active:[],passive:[],brave:[],leader:[]} }
"""
import re
import json
import time
import os
import sys
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}
CLASS_LIST = 'https://hyperwiki.jp/unicorn/class/'
OUT = 'class_skills_data.json'
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


def clean(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s or '').replace('&nbsp;', ' ')).strip()


def get_class_list():
    html = get(CLASS_LIST)
    links = re.findall(r'href="(https://hyperwiki\.jp/unicorn/class/[^"]+)"[^>]*>([^<]*)</a>', html)
    seen = {}
    for url, text in links:
        t = clean(text)
        if t and t not in seen:
            seen[t] = url
    return seen


def parse_skill_table(table_html):
    """解析一张技能表：每行 th=技能名, td=习得, td=效果"""
    skills = []
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.S)
    for tr in rows:
        ths = re.findall(r'<th[^>]*>(.*?)</th>', tr, re.S)
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if not ths or len(tds) < 2:
            continue
        name = clean(ths[0])
        learn = clean(tds[0]) if tds else ''
        effect = clean(tds[1]) if len(tds) > 1 else ''
        if name:
            skills.append({'name': name, 'learn': learn, 'effect': effect})
    return skills


def parse_class_skills(html):
    """从职业页提取 blockWrap 里的 4 类技能"""
    result = {}
    # 找 習得するスキル 后的 blockWrap
    i = html.find('習得するスキル</span>')
    if i < 0:
        i = html.find('習得するスキル')
    j = html.find('<div class="blockWrap">', i)
    if j < 0:
        return result
    seg = html[j:]
    # 按 h3 标题切 4 块
    labels = {'アクティブスキル': 'active', 'パッシブスキル': 'passive',
              'ブレイブスキル': 'brave', 'リーダー効果': 'leader'}
    for label, key in labels.items():
        m = re.search(r'<h3>' + label + r'</h3>\s*<table[^>]*>(.*?)</table>', seg, re.S)
        if m:
            result[key] = parse_skill_table(m.group(1))
    return result


def main():
    # 断点续传
    done = {}
    if os.path.exists(OUT):
        try:
            done = json.load(open(OUT, encoding='utf-8'))
        except Exception:
            pass
    print(f'断点续传：已有 {len(done)} 个职业')

    classes = get_class_list()
    print(f'职业总数: {len(classes)}')
    todo = {k: v for k, v in classes.items() if k not in done}
    print(f'待抓: {len(todo)}')

    for i, (name, url) in enumerate(todo.items()):
        html = get(url)
        if not html:
            print(f'[{i+1}/{len(todo)}] {name} 抓取失败')
            continue
        sk = parse_class_skills(html)
        total = sum(len(v) for v in sk.values())
        done[name] = sk
        print(f'[{i+1:2}/{len(todo)}] {name:10} 技能 {total} (active={len(sk.get("active", []))}, '
              f'passive={len(sk.get("passive", []))}, brave={len(sk.get("brave", []))}, leader={len(sk.get("leader", []))})')
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(done, f, ensure_ascii=False, indent=1)
        time.sleep(0.5)

    print(f'\n完成，共 {len(done)} 个职业')
    # 覆盖检查：uo-data 里的职业键是否都有技能
    uo = json.load(open('../assets/uo-data.json', encoding='utf-8'))
    cls_keys = list(uo['classes'].keys())
    missing = [k for k in cls_keys if k not in done]
    print(f'uo-data {len(cls_keys)} 职业，缺技能数据的: {missing if missing else "无 ✅"}')


if __name__ == '__main__':
    main()
