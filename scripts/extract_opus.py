# -*- coding: utf-8 -*-
"""
提取 B 站 opus《圣兽之王》全队友收集及最强配队推荐
输出：
  1. article_zh.md        —— 完整中文原文（标题/段落/图片引用）
  2. article_blocks.json  —— 按序块数组（h1/h2/p/img），供生成英文页
  3. article_images.json  —— 图片清单（URL + 宽高 + 序号）
"""
import re
import json
import os

HTML = '_opus_page.html'
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

text = open(HTML, encoding='utf-8').read()
m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;', text, re.S)
assert m, 'INITIAL_STATE not found'
data = json.loads(m.group(1))

paras = None
for mod in data['detail']['modules']:
    if mod.get('module_type') == 'MODULE_TYPE_CONTENT':
        paras = mod['module_content']['paragraphs']
        break
assert paras is not None, 'paragraphs not found'
print('paras:', len(paras))

blocks = []       # 结构块
md_lines = []     # markdown 中文原文
img_index = 0
img_map = {}      # url -> 序号

TITLE = '《圣兽之王》全队友收集及最强配队推荐（顶级编程优化）'


def node_text(n):
    """单个文本节点 -> 字符串（WORD=words, RICH=带链接）"""
    t = n.get('type')
    if t == 'TEXT_NODE_TYPE_WORD':
        w = n.get('word') or {}
        return w.get('words') or ''
    if t == 'TEXT_NODE_TYPE_RICH':
        r = n.get('rich') or {}
        txt = r.get('orig_text') or r.get('text') or ''
        url = r.get('jump_url')
        return f'[{txt}]({url})' if url else txt
    return ''


def nodes_to_text(nodes):
    return ''.join(node_text(n) for n in (nodes or []) if n)


for p in paras:
    pt = p.get('para_type')
    if pt == 8:  # heading
        h = p.get('heading') or {}
        level = h.get('level') or 1
        txt = nodes_to_text(h.get('nodes'))
        blocks.append({'type': f'h{level}', 'text': txt})
        md_lines.append(f"{'#' * level} {txt}")
    elif pt == 1:  # text
        txt = nodes_to_text((p.get('text') or {}).get('nodes'))
        if txt:
            blocks.append({'type': 'p', 'text': txt})
            md_lines.append(txt)
            md_lines.append('')
    elif pt == 2:  # pic
        pics = ((p.get('pic') or {}).get('pics')) or []
        for pic in pics:
            url = pic.get('url')
            if not url:
                continue
            img_index += 1
            img_map[url] = img_index
            w = pic.get('width')
            h = pic.get('height')
            blocks.append({'type': 'img', 'src': url, 'w': w, 'h': h, 'n': img_index})
            md_lines.append(f'![img{img_index}]({url})')
            md_lines.append('')
    elif pt == 3:  # line
        md_lines.append('---')
        md_lines.append('')
    else:
        print('WARN unknown para_type:', pt)

# 写中文原文 md
md_path = os.path.join(OUT_DIR, 'article_zh.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(f'# {TITLE}\n\n')
    f.write('> 来源：哔哩哔哩专栏 916422313046442004｜作者：lzlzmc｜编辑于 2026-04-25\n')
    f.write('> 原文链接：https://www.bilibili.com/opus/916422313046442004\n\n')
    f.write('\n'.join(md_lines))
print('saved', md_path)

# 写块 JSON
blocks_path = os.path.join(OUT_DIR, 'article_blocks.json')
with open(blocks_path, 'w', encoding='utf-8') as f:
    json.dump(blocks, f, ensure_ascii=False, indent=1)
print('saved', blocks_path, 'blocks:', len(blocks))

# 写图片清单
imgs_path = os.path.join(OUT_DIR, 'article_images.json')
img_list = []
for url, n in img_map.items():
    for b in blocks:
        if b.get('type') == 'img' and b.get('src') == url:
            img_list.append({'n': n, 'url': url, 'w': b.get('w'), 'h': b.get('h')})
            break
with open(imgs_path, 'w', encoding='utf-8') as f:
    json.dump(img_list, f, ensure_ascii=False, indent=1)
print('saved', imgs_path, 'images:', len(img_list))
