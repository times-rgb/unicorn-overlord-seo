# -*- coding: utf-8 -*-
"""扫描全站所有页面的导航栏，统计不一致"""
import os
import re

root = r'G:\CODEX\projects\my-website'
patterns = {}

for dp, dn, fn in os.walk(root):
    for f in fn:
        if f.endswith('.html'):
            p = os.path.join(dp, f)
            t = open(p, encoding='utf-8').read()
            m = re.search(r'<header class="nav".*?</header>', t, re.S)
            if not m:
                patterns.setdefault('NO_HEADER', []).append(os.path.relpath(p, root))
                continue
            nav = m.group(0)
            # 提取导航内所有 a 的 href（仅 nav 部分）
            links = re.findall(r'<a href="([^"]+)"[^>]*>', nav)
            key = '|'.join(links)
            patterns.setdefault(key, []).append(os.path.relpath(p, root))

print('不同导航形态:', len(patterns))
for key, files in patterns.items():
    print('---', key)
    print('    页面数:', len(files), '示例:', files[0], '...' if len(files) > 1 else '')
