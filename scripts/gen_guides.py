# -*- coding: utf-8 -*-
import json, os

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, 'fandom_chars.json'), encoding='utf-8') as f:
    chars = json.load(f)

FACTIONS = ['Cornia', 'Drakenhold', 'Elheim', 'Bastorias', 'Albion']
FACTION_COLOR = {
    'Cornia': '#5357cf',
    'Drakenhold': '#c04848',
    'Elheim': '#4f9e6b',
    'Bastorias': '#8b5fc9',
    'Albion': '#d9a441',
}
FACTION_DESC = {
    'Cornia': 'The holy kingdom where the story begins.',
    'Drakenhold': 'The dragon-ruled land of the imperial east.',
    'Elheim': 'The forest realm of the elves.',
    'Bastorias': 'The snowy north of the beastkin.',
    'Albion': 'The winged sanctuary of the feather folk.',
}

# 特殊链接：有真实页面的角色
SPECIAL_LINK = {
    'Alain': '/characters/alain/',
    'Scarlett': '/teams/alain-frontline/',
    'Berenice': '/teams/alain-frontline/',
    'Clive': '/teams/alain-frontline/',
    'Josef': '/teams/alain-frontline/',
    'Rosalinde': '/teams/alain-frontline/',
}
DEFAULT_LINK = '/team-builder/'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def char_card(c, faction):
    name = c['name']
    cls = ' / '.join(c['classes'])
    link = SPECIAL_LINK.get(name, DEFAULT_LINK)
    safe = name.replace(' ', '_').replace('/', '_').replace("'", '').replace(':', '').replace('?', '')
    img = f'/assets/chars/{faction.lower()}_{safe}.webp'
    color = FACTION_COLOR[faction]
    return (f'<a class="char {faction.lower()}" href="{link}" title="{esc(name)} — open in Team Builder">'
            f'<img src="{img}" alt="{esc(name)} {esc(cls)}">'
            f'<div class="cap" style="background:{color}"><b>{esc(name)}</b>'
            f'<small>{esc(cls)}</small></div></a>')


def faction_section(faction):
    items = ''.join(char_card(c, faction) for c in chars[faction])
    return (f'<h3 id="{faction.lower()}" style="border-color:{FACTION_COLOR[faction]}">{faction} '
            f'<small class="fdesc">{FACTION_DESC[faction]}</small></h3>'
            f'<div class="char-grid">{items}</div>')


def toc():
    fac = ''.join(f'<li><a href="#{f.lower()}">{f}</a></li>' for f in FACTIONS)
    return (f'<nav class="toc"><span class="toctitle">Contents</span><ol>'
            f'<li><a href="#playable">Playable Characters</a><ul>{fac}</ul></li>'
            f'<li><a href="#classes">Class Guides</a></li>'
            f'<li><a href="#equipment">Equipment</a></li>'
            f'<li><a href="#teams">Teams</a></li>'
            f'<li><a href="#tools">Interactive Tools</a></li></ol></nav>')


chars_html = ''.join(faction_section(f) for f in FACTIONS)

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Browse all Unicorn Overlord characters by faction, plus class guides, equipment, team compositions and the interactive team builder."><title>Characters &amp; Guides Index | Unicorn Overlord SEO Engine</title><link rel="stylesheet" href="/assets/site.css"></head><body><header class="nav"><a class="brand" href="/">UNICORN <i>OVERLORD</i><small>SEO ENGINE</small></a><nav><a class="active" href="/guides/">Guides</a><a href="/characters/alain/">Characters</a><a href="/classes/warrior/">Classes</a><a href="/equipment/kingsblade/">Equipment</a><a class="button small" href="/team-builder/">Team Builder</a></nav></header><article class="article wiki"><div class="crumb"><a href="/">Home</a> / Guides</div><p class="eyebrow">SITE INDEX</p><h1>All Characters &amp; Guides | Unicorn Overlord</h1><p class="lede">Every character, class, item and formation on this site — organized like a wiki. Pick a faction to meet its roster, then open any unit in the <a href="/team-builder/">Team Builder</a>.</p>{toc()}
<h2 id="playable">Playable Characters</h2>
<p class="subnote">All <b>{sum(len(v) for v in chars.values())}</b> playable units, grouped by the five nations.</p>
{chars_html}
<h2 id="classes">Class Guides</h2>
<div class="cards"><a class="card" href="/classes/warrior/"><span>CLASS GUIDE</span><h3>Warrior: Stats, Promotion &amp; Counters</h3><p>Break guards, solve armored targets, protect the back line.</p><b>Explore class →</b></a></div>
<h2 id="equipment">Equipment</h2>
<div class="cards"><a class="card" href="/equipment/kingsblade/"><span>EQUIPMENT</span><h3>King'sblade Cornix</h3><p>Physical Attack +8 and AP +1 — when the slot is worth it.</p><b>Inspect gear →</b></a></div>
<h2 id="teams">Teams</h2>
<div class="cards"><a class="card" href="/teams/alain-frontline/"><span>FORMATION BLUEPRINT</span><h3>Alain Frontline Team</h3><p>Break, sustain and finish with a five-unit formation.</p><b>View formation →</b></a></div>
<h2 id="tools">Interactive Tools</h2>
<div class="cards"><a class="card feature" href="/team-builder/"><span>TOOL</span><h3>Team Builder</h3><p>Build, save and share your own Unicorn Overlord squads.</p><b>Open tool →</b></a></div>
</article><footer>Unofficial tactical reference · Unicorn Overlord SEO Engine</footer></body></html>"""

out = os.path.join(base, '..', 'guides', 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(page)
print('已生成:', os.path.normpath(out))
print('字符数:', len(page))
