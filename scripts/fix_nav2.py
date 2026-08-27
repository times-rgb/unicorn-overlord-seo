# -*- coding: utf-8 -*-
"""P0 导航统一修复：重建所有页面的 <header class="nav"> 为标准完整导航（5 项）"""
import os
import re

root = r'G:\CODEX\projects\my-website'

NAV = ('<header class="nav"><a class="brand" href="/">UNICORN <i>OVERLORD</i><small>SEO ENGINE</small></a>'
       '<nav><a href="/guides/">Guides</a><a href="/guides/#playable">Characters</a>'
       '<a href="/guides/#classes">Classes</a><a href="/guides/#equipment">Equipment</a>'
       '<a class="button small" href="/team-builder/">Team Builder</a></nav></header>')

changed = 0
no_header = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if f.endswith('.html'):
            p = os.path.join(dp, f)
            t = open(p, encoding='utf-8').read()
            if '<header class="nav"' not in t:
                no_header.append(os.path.relpath(p, root))
                continue
            new = re.sub(r'<header class="nav".*?</header>', NAV, t, flags=re.S)
            if new != t:
                open(p, 'w', encoding='utf-8').write(new)
                changed += 1

print('统一导航重建页面数:', changed)
print('无 header 的页面:', no_header if no_header else '无')
