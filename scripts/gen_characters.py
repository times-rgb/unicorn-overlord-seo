# -*- coding: utf-8 -*-
"""批量生成 70 个角色攻略页 + 重写 sitemap.xml"""
import json, os, re, unicodedata

base = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(base, '..')
with open(os.path.join(base, 'fandom_chars.json'), encoding='utf-8') as f:
    chars = json.load(f)

GA = 'G-21H6402X2H'
GSC = 'FHOEqWIDE1jKTKzISo7LUzXQ8FzrRNqp3VVviLu-dfM'
SITE = 'https://unicorn-overlord-seo.vercel.app'


def slug(name):
    n = unicodedata.normalize('NFKD', name)
    n = ''.join(c for c in n if not unicodedata.combining(c))
    n = re.sub(r"[^A-Za-z0-9]+", '-', n).strip('-').lower()
    return n or 'unit'


def safe_name(name):
    return name.replace(' ', '_').replace('/', '_').replace("'", '').replace(':', '').replace('?', '')


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def head(desc, title, jsonld):
    return (f'<!doctype html><html lang="en"><head><meta name="google-site-verification" content="{GSC}" />'
            f'<!-- Google tag (gtag.js) -->\n'
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>\n<script>\n'
            f'  window.dataLayer = window.dataLayer || [];\n  function gtag(){{dataLayer.push(arguments);}}\n'
            f"  gtag('js', new Date());\n  gtag('config', '{GA}');\n</script>\n"
            f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="description" content="{esc(desc)}"><title>{esc(title)}</title>'
            f'<link rel="stylesheet" href="/assets/site.css">'
            f'<script type="application/ld+json">{jsonld}</script></head><body>')


def class_links(classes):
    out = []
    for c in classes:
        lc = c.lower()
        if 'warrior' in lc or 'breaker' in lc:
            out.append('<a href="/classes/warrior/">Warrior</a>')
        elif 'cleric' in lc or 'priestess' in lc or 'bishop' in lc:
            out.append('<a href="/classes/cleric/">Cleric</a>')
    seen = []
    for l in out:
        if l not in seen:
            seen.append(l)
    return ' / '.join(seen) if seen else ' / '.join(esc(c) for c in classes)


def role_of(classes):
    joined = ' '.join(classes).lower()
    if any(k in joined for k in ['cleric', 'priestess', 'bishop']):
        return 'backline healer / support'
    if any(k in joined for k in ['hoplite', 'legionnaire', 'gladiator', 'berserker', 'vanguard',
                                 'dreadnought', 'great knight', 'housecarl', 'viking', 'paladin',
                                 'knight', 'defender', 'feathershield']):
        return 'frontline tank / guard anchor'
    if any(k in joined for k in ['augur', 'sibyl', 'wizard', 'sage', 'featherstaff']):
        return 'backline magic damage'
    return 'frontline / side damage'


def gen_char_page(faction, c, used_slugs):
    name = c['name']
    classes = c['classes']
    s = slug(name)
    # 防重名
    if s in used_slugs:
        s = slug(faction) + '-' + s
    used_slugs[s] = True

    img = f"/assets/chars/{faction.lower()}_{safe_name(name)}.webp"
    cls_txt = ' / '.join(classes)
    role = role_of(classes)
    title = f"{name} Best Build & Tactics | Unicorn Overlord"
    desc = f"{name} best build in Unicorn Overlord: {cls_txt} equipment, tactics configuration and best team composition."
    jsonld = '{"@context":"https://schema.org","@type":"TechArticle","headline":"' + title.replace('"', '\\"') + \
             '","description":"' + esc(desc) + '","mainEntity":{"@type":"ItemPage","name":"' + name.replace('"', '\\"') + '","game":"Unicorn Overlord"}}'

    page = head(desc, title, jsonld)
    page += ('<header class="nav"><a class="brand" href="/">UNICORN <i>OVERLORD</i><small>SEO ENGINE</small></a>'
             '<nav><a href="/guides/">Guides</a><a href="/classes/warrior/">Classes</a>'
             '<a href="/equipment/kingsblade/">Equipment</a><a class="button small" href="/team-builder/">Team Builder</a></nav></header>'
             f'<article class="article"><div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Characters / {esc(name)}</div>'
             f'<p class="eyebrow">CHARACTER BUILD · {esc(cls_txt)}</p>'
             f'<h1>{esc(title)}</h1>'
             f'<p class="lede">{esc(name)} is a {esc(cls_txt)} unit from {faction}, best used as a <b>{role}</b>. '
             f'Slot {esc(name)} into a formation that matches this role, set the tactics to fire at the right HP/AP thresholds, '
             f'and pair the unit with <a href="/guides/">counters and synergy</a> from the rest of the roster.</p>'
             f'<h2>{esc(name)} Quick Profile &amp; Recruitment</h2>'
             '<table><tr><th>Attribute</th><th>Detail</th></tr>'
             f'<tr><td>Faction</td><td>{faction}</td></tr>'
             f'<tr><td>Class(es)</td><td>{class_links(classes)}</td></tr>'
             f'<tr><td>Best Role</td><td>{role}</td></tr>'
             f'<tr><td>Image</td><td><img src="{img}" alt="{esc(name)}" style="width:64px;border-radius:4px"></td></tr></table>'
             f'<h2>{esc(name)} Build Direction</h2>'
             f'<ul><li><strong>Role:</strong> {role} within a 5-unit formation.</li>'
             f'<li><strong>Stats to prioritize:</strong> focus items and growth that support this role.</li>'
             f'<li><strong>Tactics:</strong> set active/passive triggers at HP/AP thresholds that keep the unit acting when it matters.</li></ul>'
             f'<h2>Best Team Fit for {esc(name)}</h2>'
             f'<p>Use {esc(name)} in a <a href="/teams/alain-frontline/">team composition</a> that covers sustain, break and finish. '
             f'Every unit can be previewed and adjusted in the <a href="/team-builder/">Team Builder</a> before you commit to the formation.</p>'
             '<aside class="tool-hook"><strong>🛠 Open in Team Builder: build a squad around ' + esc(name) + '.</strong>'
             '<a href="/team-builder/">Customize this unit →</a></aside></article>'
             '<footer>Unofficial tactical reference · Unicorn Overlord SEO Engine</footer></body></html>')

    dir_path = os.path.join(root, 'characters', s)
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page)
    return s


used = {}
generated = []
for faction in ['Cornia', 'Drakenhold', 'Elheim', 'Bastorias', 'Albion']:
    if faction not in chars:
        continue
    for c in chars[faction]:
        s = gen_char_page(faction, c, used)
        generated.append((s, c['name']))

print(f'已生成 {len(generated)} 个角色页')

# ===== 重写 sitemap.xml =====
def sm(url, prio, freq='weekly'):
    return f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-08-25</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>'

urls = []
urls.append(sm(SITE + '/', '1.0'))
urls.append(sm(SITE + '/guides/', '0.9'))
for s, _ in sorted(generated):
    urls.append(sm(SITE + '/characters/' + s + '/', '0.8'))
for s in ['warrior', 'cleric']:
    urls.append(sm(SITE + '/classes/' + s + '/', '0.8'))
for s in ['kingsblade', 'crimson-pendant']:
    urls.append(sm(SITE + '/equipment/' + s + '/', '0.7'))
urls.append(sm(SITE + '/teams/alain-frontline/', '0.7'))
urls.append(sm(SITE + '/team-builder/', '0.6'))

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
          '\n'.join(urls) + '\n</urlset>\n'
with open(os.path.join(root, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap)
print(f'sitemap.xml 已重写，共 {len(urls)} 个 URL')
