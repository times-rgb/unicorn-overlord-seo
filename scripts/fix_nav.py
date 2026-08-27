# -*- coding: utf-8 -*-
"""P0 导航修复：导航栏 Characters/Classes/Equipment 从单页改为指向 guides 列表锚点
只精确替换导航栏链接片段（带链接文字的完整 a 标签），不动首页/内容卡片的实体链接。"""
import os

ROOT = r'G:\CODEX\projects\my-website'

# (旧, 新) 精确匹配导航栏链接（导航内文字 = Characters/Classes/Equipment，唯一）
REPLACEMENTS = [
    ('<a href="/characters/alain/">Characters</a>', '<a href="/guides/#playable">Characters</a>'),
    ('<a href="/classes/warrior/">Classes</a>', '<a href="/guides/#classes">Classes</a>'),
    ('<a href="/equipment/kingsblade/">Equipment</a>', '<a href="/guides/#equipment">Equipment</a>'),
]

changed = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        if not fn.endswith('.html'):
            continue
        p = os.path.join(dirpath, fn)
        with open(p, encoding='utf-8') as f:
            content = f.read()
        orig = content
        for old, new in REPLACEMENTS:
            content = content.replace(old, new)
        if content != orig:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(content)
            changed.append(os.path.relpath(p, ROOT))

print('changed files:', len(changed))
for c in changed:
    print('  ', c)
