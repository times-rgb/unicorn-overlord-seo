# -*- coding: utf-8 -*-
import re, os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
html = open('guides/index.html', encoding='utf-8').read()
links = set(re.findall(r'href="/characters/([a-z0-9-]+)/"', html))
missing = [l for l in links if not os.path.isdir(os.path.join('characters', l))]
print('导航页角色链接数:', len(links))
print('缺失(404):', missing if missing else '无，全部有效')
# 校验 sitemap 里的角色 URL 与目录一致
sm = open('sitemap.xml', encoding='utf-8').read()
sm_links = set(re.findall(r'<loc>https://unicorn-overlord-seo\.vercel\.app/characters/([a-z0-9-]+)/</loc>', sm))
sm_missing = [l for l in sm_links if not os.path.isdir(os.path.join('characters', l))]
print('sitemap 角色 URL 数:', len(sm_links))
print('sitemap 缺失:', sm_missing if sm_missing else '无')
