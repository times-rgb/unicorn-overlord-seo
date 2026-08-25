# -*- coding: utf-8 -*-
import json, os, time, urllib.request

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, 'fandom_chars.json'), encoding='utf-8') as f:
    chars = json.load(f)

out_dir = os.path.join(base, '..', 'assets', 'chars')
os.makedirs(out_dir, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

ok = 0
fail = []
for faction, items in chars.items():
    for c in items:
        name = c['name']
        img = c['img']
        # 文件名：阵营_名字.webp（防重名）
        safe = name.replace(' ', '_').replace('/', '_').replace("'", '').replace(':', '').replace('?', '')
        fname = f'{faction.lower()}_{safe}.webp'
        fpath = os.path.join(out_dir, fname)
        if os.path.exists(fpath) and os.path.getsize(fpath) > 1000:
            ok += 1
            continue
        try:
            data = None
            for attempt in range(4):
                try:
                    req = urllib.request.Request(img, headers=HEADERS)
                    with urllib.request.urlopen(req, timeout=25) as resp:
                        data = resp.read()
                    break
                except Exception:
                    if attempt < 3:
                        time.sleep(2 + attempt * 2)
            if data is None:
                raise RuntimeError('retries exhausted')
            with open(fpath, 'wb') as f:
                f.write(data)
            ok += 1
        except Exception as e:
            fail.append((faction, name, str(e)))
        time.sleep(0.5)

print(f'下载成功: {ok}/{sum(len(v) for v in chars.values())}')
if fail:
    print('失败:', len(fail))
    for f in fail[:10]:
        print('  ', f)
