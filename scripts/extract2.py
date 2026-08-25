import json, os, re

with open(os.path.join(os.environ['TEMP'], 'fandom_chars.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

html = data['parse']['text']['*']
main_start = html.find('id="Playable_Characters"')
main = html[main_start:]

# 用 finditer 精确定位每个阵营 h3 的位置
pat = re.compile(r'<h3[^>]*>\s*<span class="mw-headline" id="([^"]+)">([^<]+)</span>')
matches = list(pat.finditer(main))

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, 'debug.txt'), 'w', encoding='utf-8') as dbg:
    dbg.write(f'找到阵营 h3 数量: {len(matches)}\n')
    for i, m in enumerate(matches):
        dbg.write(f'{i}: id={m.group(1)} name={m.group(2).strip()} pos={m.start()}\n')

result = {}
for i, m in enumerate(matches):
    fid, fname = m.group(1), m.group(2).strip()
    seg_start = m.start()
    seg_end = matches[i + 1].start() if i + 1 < len(matches) else len(main)
    seg = main[seg_start:seg_end]

    items = []
    parts = seg.split('<div class="wikia-gallery-item"')[1:]
    for part in parts:
        cut = part.find('<div class="wikia-gallery-item"')
        block = part[:cut] if cut != -1 else part
        img = re.search(r'data-src="([^"]+)"', block) or re.search(r'<img[^>]+src="([^"]+)"', block)
        cap = re.search(r'lightbox-caption[^>]*>(.*?)</div>', block, re.S)
        name = ''
        classes = []
        if cap:
            cap_html = cap.group(1)
            nm = re.search(r'>([^<]+)<br', cap_html)
            if nm:
                name = nm.group(1).strip()
            classes = re.findall(r'title="([^"]+)"', cap_html)
        if not name:
            alt = re.search(r'alt="([^"]*)"', block)
            if alt:
                name = alt.group(1).split(' ')[0]
        if name:
            items.append({'name': name, 'classes': classes, 'img': img.group(1) if img else ''})
    result[fname] = items

out = {k: v for k, v in result.items() if v}
out_path = os.path.join(base, 'fandom_chars.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

with open(os.path.join(base, 'debug.txt'), 'a', encoding='utf-8') as dbg:
    dbg.write('\n== 结果 ==\n')
    for k, v in out.items():
        dbg.write(f'{k}: {len(v)} 人 -> {[x["name"] for x in v][:6]}...\n')
print('done')
