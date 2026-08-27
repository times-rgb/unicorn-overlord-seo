# -*- coding: utf-8 -*-
import os
import re

root = r'G:\CODEX\projects\my-website'
old_pats = [
    r'<a href="/characters/alain/">Characters</a>',
    r'<a href="/classes/warrior/">Classes</a>',
    r'<a href="/equipment/kingsblade/">Equipment</a>',
]
left = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if f.endswith('.html'):
            t = open(os.path.join(dp, f), encoding='utf-8').read()
            for p in old_pats:
                if re.search(re.escape(p), t):
                    left += 1
print('旧导航链接残留:', left)

g = open(os.path.join(root, 'guides', 'index.html'), encoding='utf-8').read()
for a in ['id="playable"', 'id="classes"', 'id="equipment"']:
    print('guides 有', a, ':', a in g)

h = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
print('首页卡片仍链 alain(非导航):', '<a class="card" href="/characters/alain/">' in h)

a = open(os.path.join(root, 'characters', 'yunifi', 'index.html'), encoding='utf-8').read()
print('yunifi 页导航已改:', '<a href="/guides/#playable">Characters</a>' in a)
print('yunifi 页导航 Classes:', '<a href="/guides/#classes">Classes</a>' in a)
print('yunifi 页导航 Equipment:', '<a href="/guides/#equipment">Equipment</a>' in a)
