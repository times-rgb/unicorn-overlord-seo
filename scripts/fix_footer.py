# -*- coding: utf-8 -*-
"""全站 footer 加 Changelog 小链接（方案 B：小角落入口）"""
import os

root = r'G:\CODEX\projects\my-website'
OLD = '<footer>Unofficial tactical reference · Unicorn Overlord SEO Engine</footer>'
NEW = '<footer>Unofficial tactical reference · <a href="/version-history/">Changelog</a> · Unicorn Overlord SEO Engine</footer>'

changed = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if f.endswith('.html'):
            p = os.path.join(dp, f)
            t = open(p, encoding='utf-8').read()
            if OLD in t:
                t = t.replace(OLD, NEW)
                open(p, 'w', encoding='utf-8').write(t)
                changed += 1
print('footer 加 Changelog 链接页面数:', changed)
