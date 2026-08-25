# -*- coding: utf-8 -*-
"""批量下载文章 78 张截图到 assets/article/img_XXX.jpg"""
import json
import os
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
imgs = json.load(open(os.path.join(SCRIPT_DIR, 'article_images.json'), encoding='utf-8'))
outdir = os.path.join(SCRIPT_DIR, '..', 'assets', 'article')
os.makedirs(outdir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
}

ok = 0
for img in imgs:
    n = img['n']
    url = img['url']
    ext = url.rsplit('.', 1)[-1].split('?')[0] or 'jpg'
    if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
        ext = 'jpg'
    path = os.path.join(outdir, f'img_{n:03d}.{ext}')
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        ok += 1
        continue
    try:
        r = requests.get(url, headers=headers, timeout=40)
        if r.status_code == 200 and r.content:
            with open(path, 'wb') as f:
                f.write(r.content)
            ok += 1
        else:
            print('FAIL', n, r.status_code, url[:80])
    except Exception as e:
        print('ERR', n, e, url[:80])

print('done, ok =', ok, '/', len(imgs))
