# -*- coding: utf-8 -*-
"""扫描 Codex + Copilot 技能目录，生成 Skill 清单 markdown 到交付包"""
import os
import re

OUT = r'G:\CODEX\战棋站复刻知识包-UNICORN-OVERLORD-v2\04-Skill清单\skills.md'

SOURCES = [
    ('Codex 专用（SEO 建站全家桶）', r'C:\Users\Admin\.codex\skills'),
    ('VS Code Copilot（个人/团队技能）', r'C:\Users\Admin\.copilot\skills'),
]

def read_skill(path):
    md = os.path.join(path, 'SKILL.md')
    if not os.path.exists(md):
        return None
    txt = open(md, encoding='utf-8', errors='ignore').read()
    m = re.search(r'^---\s*\n(.*?)\n---', txt, re.S | re.M)
    fm = m.group(1) if m else ''
    name = re.search(r'^name:\s*(.+)$', fm, re.M)
    desc = re.search(r'^description:\s*(.+)$', fm, re.M)
    return {
        'name': name.group(1).strip() if name else os.path.basename(path),
        'desc': desc.group(1).strip() if desc else '',
    }

lines = []
lines.append('# Skill 收录清单（复刻知识包）')
lines.append('')
lines.append('> 生成日期：2026-08-26｜来源：本机已安装技能目录')
lines.append('')
total = 0
for title, folder in SOURCES:
    lines.append(f'## {title}  `{folder}`')
    lines.append('')
    dirs = sorted([d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))])
    items = []
    for d in dirs:
        if d == '.system':
            continue
        info = read_skill(os.path.join(folder, d))
        if info:
            items.append(info)
            total += 1
    if not items:
        lines.append('（无）')
    for it in items:
        lines.append(f'- **{it["name"]}**')
        if it['desc']:
            lines.append(f'  - {it["desc"]}')
    lines.append('')

lines.append(f'**合计收录：{total} 个技能**')
open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))
print('saved', OUT, 'skills:', total)
