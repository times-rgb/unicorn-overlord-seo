import json, re, os, sys

# 读取保存的 fandom 页面 JSON
with open(os.path.join(os.environ['TEMP'], 'fandom_chars.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

html = data['parse']['text']['*']

# 找到 Playable Characters 主区域（H2 之后）
main_start = html.find('id="Playable_Characters"')
main_html = html[main_start:]

# 提取每个阵营小节：h3 + 其后的 gallery 块
# faction header: <h3>...<span class="mw-headline" id="XXX">NAME</span>...
sections = re.findall(r'<h3>.*?<span class="mw-headline" id="([^"]+)">([^<]+)</span>', main_html)

result = {}
for i, (fid, fname) in enumerate(sections):
    # 该小节内容：从当前 h3 到下一个 h3
    start = main_html.find(f'<h3>', main_html.find(fid))
    end = main_html.find('<h3>', start + 10) if i + 1 < len(sections) else len(main_html)
    seg = main_html[start:end]

    items = []
    # 每个 gallery item
    for m in re.finditer(r'<div class="wikia-gallery-item".*?(?=<div class="wikia-gallery-item"|$)', seg, re.S):
        block = m.group(0)
        # 图片 URL（data-src 或 src 非懒加载）
        img = re.search(r'data-src="([^"]+)"', block) or re.search(r'<img[^>]+src="([^"]+)"', block)
        # alt = "Name Class1/Class2"
        alt = re.search(r'alt="([^"]*)"', block)
        # caption 里的名字 + 职业链接
        cap = re.search(r'lightbox-caption[^>]*>(.*?)</div>', block, re.S)
        name = ''
        classes = []
        if cap:
            cap_html = cap.group(1)
            nm = re.search(r'>([^<]+)<br', cap_html)
            if nm:
                name = nm.group(1).strip()
            classes = re.findall(r'title="([^"]+)"', cap_html)
        if not name and alt:
            name = alt.group(1).split(' ')[0]
        items.append({
            'name': name,
            'classes': classes,
            'img': img.group(1) if img else ''
        })
    result[fname.strip()] = items

# 输出精简 JSON 到文件（UTF-8）
out = {k: v for k, v in result.items() if v}
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fandom_chars.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('已写入:', out_path)
for k, v in out.items():
    print(k, '->', len(v), '人')
