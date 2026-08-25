# -*- coding: utf-8 -*-
"""
生成英文页 guides/complete-team-recruitment/index.html
读 recruitment_data.py（英文内容）+ fandom_chars.json（角色 slug/阵营/头像）→ 拼 HTML
角色 {slug|Name} 标记 → 链接到 /characters/{slug}/
"""
import json
import os
import re
import html
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.join(SCRIPT_DIR, '..')

# ---------- 角色索引 ----------
def slugify(name):
    nfkd = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return s.lower()

fandom = json.load(open(os.path.join(SCRIPT_DIR, 'fandom_chars.json'), encoding='utf-8'))
CHAR_INDEX = {}  # slug -> {name, faction}
for faction, chars in fandom.items():
    for c in chars:
        slug = slugify(c['name'])
        CHAR_INDEX[slug] = {'name': c['name'], 'faction': faction}

# ---------- 英文内容 ----------
import importlib.util
spec = importlib.util.spec_from_file_location('rd', os.path.join(SCRIPT_DIR, 'recruitment_data.py'))
rd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rd)

LINK_RE = re.compile(r'\{([a-z0-9-]+)\|([^}]+)\}')


def links(text):
    def rep(m):
        slug, disp = m.group(1), m.group(2)
        if slug in CHAR_INDEX:
            return '<a href="/characters/%s/">%s</a>' % (slug, html.escape(disp))
        return disp
    return LINK_RE.sub(rep, text)


def shot(n, alt=''):
    return '<img class="shot" src="/assets/article/img_%03d.jpg" alt="%s" loading="lazy">' % (n, html.escape(alt))


def member(slug):
    info = CHAR_INDEX.get(slug)
    if not info:
        return '<span class="member"><b>%s</b></span>' % slug.title()
    name = info['name']
    img = '/assets/chars/%s_%s.webp' % (info['faction'], name)
    return '<a class="member" href="/characters/%s/"><img src="%s" alt="%s" loading="lazy"><b>%s</b></a>' % (slug, img, name, name)


# ---------- 组装各章节 ----------
def build_tips():
    out = ['<h2 id="tips">Pro Tips &amp; Farming</h2>']
    for i, t in enumerate(rd.TIPS):
        out.append('<h3>%s</h3>' % html.escape(t['h']))
        for p in t['p']:
            out.append('<p>%s</p>' % links(p))
        if t['imgs']:
            out.append('<div class="imgs">' + ''.join(shot(n, 'screenshot %d' % n) for n in t['imgs']) + '</div>')
    return '\n'.join(out)


def build_world():
    out = ['<h2 id="world">World Map &amp; Leveling Order</h2>']
    out.append('<div class="imgs">' + ''.join(shot(n, 'world map') for n in rd.WORLD_MAP['imgs']) + '</div>')
    rows = ''.join(
        '<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td></tr>' % tuple(html.escape(x) for x in r)
        for r in rd.WORLD_MAP['rows'])
    out.append('<table><tr><th>Region</th><th>Name</th><th>Position</th><th>Level</th></tr>%s</table>' % rows)
    return '\n'.join(out)


def build_recruit():
    out = ['<h2 id="recruit">All 70 Companions — Recruitment</h2>']
    out.append('<p class="subnote">Every playable unit in join order, with the stage, location and any story choices required. Tap any name to open that unit\'s page.</p>')
    for group in rd.RECRUIT:
        out.append('<h3 id="recruit-%s">Units %s</h3>' % (group['h'].split()[1].replace('–', '-'), html.escape(group['h'].split()[1])))
        for it in group['items']:
            notes = ''
            if it['notes']:
                notes = '<ul class="notes">' + ''.join('<li>%s</li>' % links(n) for n in it['notes']) + '</ul>'
            out.append(
                '<div class="ritem"><div class="rinfo">'
                '<span class="rnum">#%s</span> <b>%s</b>'
                '<p><b>Location:</b> %s</p>'
                '<p><b>Join:</b> %s</p>%s'
                '</div>%s</div>'
                % (html.escape(it['n']), html.escape(it['name']),
                   links(it['place']), links(it['how']), notes,
                   shot(it['img'], it['name']) if it.get('img') else '')
            )
    return '\n'.join(out)


def build_teams():
    out = ['<h2 id="teams">Best Team Compositions</h2>']
    out.append('<p class="subnote">All teams tested 70+ hours by the source author. Tap a unit\'s face to open their page.</p>')
    for p in rd.TEAM_INTRO['p']:
        out.append('<p>%s</p>' % links(p))
    for team in rd.TEAMS:
        roster = ''.join(member(s) for s in team['roster'])
        if team.get('extra'):
            roster += '<div class="extra">+ %s</div>' % links(team['extra'])
        tags = ''.join('<span class="chip">%s</span>' % html.escape(t) for t in team['tags'])
        gear_rows = ''
        for slug, g in team['gear']:
            name = CHAR_INDEX.get(slug, {}).get('name', slug.title())
            gear_rows += '<p><b>%s:</b> %s</p>' % (html.escape(name), links(g))
        if team.get('tactic_imgs'):
            gear_rows += '<div class="imgs">' + ''.join(shot(n, 'tactics screenshot') for n in team['tactic_imgs']) + '</div>'
        out.append(
            '<div class="tcard">'
            '<div class="thead"><span class="tier">%s</span><h3>%s</h3><div class="chips">%s</div></div>'
            '<div class="tbody">%s'
            '<div class="tmeta"><div class="roster">%s</div>'
            '<p class="pros"><b>Pros:</b> %s</p>'
            '<p class="cons"><b>Cons:</b> %s</p>'
            '<details class="gear"><summary>Gear &amp; tactics</summary>%s</details>'
            '</div></div></div>'
            % (html.escape(team['tier']), html.escape(team['title']), tags,
               shot(team['img'], team['title']), roster,
               links(team['pros']), links(team['cons']), gear_rows)
        )
    out.append('<h3>Honorable mentions</h3>')
    out.append('<div class="imgs">' + ''.join(shot(n, 'extra team') for n in rd.TEAMS_EXTRA['imgs']) + '</div>')
    out.append('<p>%s</p>' % links(rd.TEAMS_EXTRA['p']))
    return '\n'.join(out)


def build_pvp():
    out = ['<h2 id="pvp">PVP Lineups</h2>']
    out.append('<p>%s</p>' % links(rd.PVP['intro']))
    for key in ('offense', 'defense'):
        sec = rd.PVP[key]
        roster = ''.join(member(s) for s in sec['roster'])
        imgs = '<div class="imgs">' + ''.join(shot(n, sec['title']) for n in sec['imgs']) + '</div>'
        paras = ''.join('<p>%s</p>' % links(p) for p in sec['p'])
        out.append('<h3>%s</h3>' % html.escape(sec['title']))
        out.append('<div class="roster">%s</div>' % roster)
        out.append(imgs)
        out.append(paras)
    return '\n'.join(out)


# ---------- 页面骨架 ----------
GSC = '<meta name="google-site-verification" content="FHOEqWIDE1jKTKzISo7LUzXQ8FzrRNqp3VVviLu-dfM" />'
GA = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-21H6402X2H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-21H6402X2H');
</script>'''

TOC = '''<nav class="toc"><span class="toctitle">Contents</span><ol>
<li><a href="#tips">Pro Tips &amp; Farming</a></li>
<li><a href="#world">World Map</a></li>
<li><a href="#recruit">All 70 Companions</a><ul>
<li><a href="#recruit-1-10">Units 1-10</a></li><li><a href="#recruit-11-20">Units 11-20</a></li>
<li><a href="#recruit-21-29">Units 21-29</a></li><li><a href="#recruit-30-39">Units 30-39</a></li>
<li><a href="#recruit-40-50">Units 40-50</a></li><li><a href="#recruit-51-60">Units 51-60</a></li>
<li><a href="#recruit-61-70">Units 61-70</a></li></ul></li>
<li><a href="#teams">Best Team Compositions</a></li>
<li><a href="#pvp">PVP Lineups</a></li></ol></nav>'''

PAGE_STYLE = '''<style>
.article.wiki h3{margin-top:26px;border-bottom:1px solid var(--border,#3a3f4a);padding-bottom:6px}
.imgs{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}
.imgs .shot,.shot{max-width:100%;border:1px solid var(--border,#333);border-radius:6px}
.imgs .shot{width:220px}
.ritem{display:flex;gap:14px;align-items:flex-start;margin:14px 0;padding:10px;background:var(--card-bg,#1b1f27);border:1px solid var(--border,#333);border-radius:8px}
.ritem .rinfo{flex:1;min-width:0}
.ritem .rnum{display:inline-block;background:var(--accent-gold,#c9a45c);color:#111;font-weight:700;font-size:12px;padding:1px 8px;border-radius:999px;margin-right:6px}
.ritem .shot{width:200px;flex-shrink:0}
.ritem p{margin:4px 0}
.notes{margin:6px 0 0;padding-left:20px;color:var(--text-muted,#aab);font-size:14px}
.tcard{margin:18px 0;background:var(--card-bg,#1b1f27);border:1px solid var(--border,#333);border-radius:10px;overflow:hidden}
.thead{padding:12px 16px;border-bottom:1px solid var(--border,#333);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.thead h3{margin:0;border:0;padding:0;font-size:18px}
.tier{background:var(--accent-gold,#c9a45c);color:#111;font-weight:800;padding:3px 10px;border-radius:6px;font-size:13px}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{font-size:11px;border:1px solid var(--border,#444);border-radius:999px;padding:1px 9px;color:var(--text-muted,#aab)}
.tbody{display:flex;gap:16px;padding:14px 16px;flex-wrap:wrap}
.tbody .shot{width:320px;flex-shrink:0;align-self:flex-start}
.tmeta{flex:1;min-width:260px}
.roster{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
.member{display:flex;flex-direction:column;align-items:center;gap:4px;text-decoration:none;color:var(--text-main,#e8e8ee);font-size:13px;text-align:center}
.member img{width:52px;height:52px;object-fit:cover;border-radius:8px;border:1px solid var(--border,#333)}
.member b{max-width:76px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.extra{width:100%;font-size:13px;color:var(--text-muted,#aab)}
.tmeta p{margin:6px 0}
.pros,.cons{font-size:14px}
details.gear{margin-top:8px;border-top:1px dashed var(--border,#333);padding-top:6px}
details.gear summary{cursor:pointer;color:var(--accent-gold,#c9a45c);font-weight:600}
details.gear p{font-size:13px;color:var(--text-muted,#aab);margin:4px 0}
@media (max-width:640px){.tbody .shot{width:100%}.ritem{flex-direction:column}.ritem .shot{width:100%}}
</style>'''

SOURCE = (
    '<section style="margin-top:30px;padding:14px 16px;border:1px solid var(--border,#333);border-radius:10px;background:var(--card-bg,#1b1f27)">'
    '<h2 id="source">Source &amp; Credits</h2>'
    '<p><b>%s</b></p>'
    '<p><b>%s</b> Original Chinese guide by <a href="%s" rel="nofollow noopener" target="_blank">%s on Bilibili</a> · edited 2026-04-25.</p>'
    '</section>'
) % (html.escape(rd.SOURCE_NOTE['en']), html.escape(rd.SOURCE_NOTE['zh']),
     rd.SOURCE_NOTE['url'], html.escape(rd.SOURCE_NOTE['author']))

BODY = (
    '<article class="article wiki"><div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Complete Team Recruitment</div>'
    '<p class="eyebrow">COMPLETE RECRUITMENT &amp; TEAM BUILDING GUIDE</p>'
    '<h1>%s</h1>'
    '<p class="lede">Every one of the <b>70 playable companions</b> in Unicorn Overlord — where and how to recruit them — plus the <b>strongest team compositions</b> tested for 70+ hours, with gear and tactics programming. Open any unit\'s name or face to jump to their build page.</p>'
    '%s%s%s%s%s%s%s'
    '<footer style="margin-top:24px;font-size:12px;color:var(--text-muted,#889)">Unofficial fan reference · not affiliated with ATLUS/SEGA.</footer>'
    '</article>'
) % (
    html.escape(rd.PAGE['title']),
    TOC, build_tips(), build_world(), build_recruit(), build_teams(), build_pvp(), SOURCE
)

LD_JSON = ('{"@context":"https://schema.org","@type":"TechArticle",'
           '"headline":"%s","description":"%s",'
           '"mainEntity":{"@type":"ItemPage","name":"Unicorn Overlord Complete Guide","game":"Unicorn Overlord"}}') % (
    html.escape(rd.PAGE['title'], quote=True), html.escape(rd.PAGE['desc'], quote=True))

PAGE_HTML = (
    '<!doctype html><html lang="en"><head>%s%s'
    '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    '<meta name="description" content="%s">'
    '<title>%s</title>'
    '<link rel="stylesheet" href="/assets/site.css">'
    '<script type="application/ld+json">%s</script>'
    '%s</head><body>'
    '<header class="nav"><a class="brand" href="/">UNICORN <i>OVERLORD</i><small>SEO ENGINE</small></a>'
    '<nav><a class="active" href="/guides/">Guides</a><a href="/characters/alain/">Characters</a>'
    '<a href="/classes/warrior/">Classes</a><a href="/equipment/kingsblade/">Equipment</a>'
    '<a class="button small" href="/team-builder/">Team Builder</a></nav></header>'
    '%s'
    '<footer>Unofficial tactical reference · Unicorn Overlord SEO Engine</footer></body></html>'
) % (GSC, GA, html.escape(rd.PAGE['desc']), html.escape(rd.PAGE['title']), LD_JSON, PAGE_STYLE, BODY)

out_path = os.path.join(PROJECT, 'guides', 'complete-team-recruitment', 'index.html')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(PAGE_HTML)
print('saved', out_path, len(PAGE_HTML), 'bytes')
