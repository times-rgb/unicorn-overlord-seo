# -*- coding: utf-8 -*-
"""Team Builder 接入 Unit Lab：head 加 calc.js + 页面加「满级属性查看器」区"""
import re

p = r'G:\CODEX\projects\my-website\team-builder\index.html'
t = open(p, encoding='utf-8').read()

# 1. head 加 calc.js（data.js 后）
if '/assets/calc.js' not in t:
    t = t.replace('<script src="/assets/data.js"></script>',
                  '<script src="/assets/data.js"></script><script src="/assets/calc.js"></script>')
    print('已加 calc.js')

# 2. 在 </main> 前插入 Unit Lab 区（若还没有）
if 'ul-lab' not in t:
    ul_section = '''<section class="ul-lab" id="ul-lab"><div class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a> / Unit Lab</div><p class="eyebrow">UNIT LAB · NUMERIC SIMULATOR</p><h2>Level 50 Stat Lab</h2><p class="lede">See the exact level-50 stats of any unit — with and without full dews. More units are being added.</p><div class="ul-controls"><label>Unit
<select id="ul-unit"></select></label><label>Class
<select id="ul-class"></select></label><label>Level
<select id="ul-level"></select></label><label class="ul-dew"><input type="checkbox" id="ul-dew" checked> Full dews (all 11)</label></div><div id="ul-out"></div><p class="notice">Formulas from HyperWiki(JP): base = Round(Lv/100×A + B), accuracy +100 display, + dews.</p></section>'''
    # 找 </main> 或 </body> 前插入
    if '</main>' in t:
        t = t.replace('</main>', ul_section + '</main>')
    else:
        t = t.replace('</body>', ul_section + '</body>')
    print('已加 Unit Lab 区')

# 3. 加 Unit Lab 初始化脚本（</body> 前）
init_js = '''<script>
(async function () {
  const lab = window.UOLab;
  if (!lab) return;
  const data = await lab.loadUOData();
  const unitSel = document.getElementById('ul-unit');
  const clsSel = document.getElementById('ul-class');
  const lvSel = document.getElementById('ul-level');
  const dewChk = document.getElementById('ul-dew');
  const out = document.getElementById('ul-out');
  const units = Object.entries(data.characters).filter(([,c]) => c.growth1);
  units.sort((a,b) => a[1].name.localeCompare(b[1].name));
  units.forEach(([k,c]) => unitSel.add(new Option(c.name + ' (' + c.growth1 + '/' + c.growth2 + ')', k)));
  for (let lv = 50; lv >= 40; lv--) lvSel.add(new Option('Lv ' + lv, lv));
  // 职业（用角色默认 class，先给 Alain 的高/下级选项）
  function render() {
    const key = unitSel.value; if (!key) { out.innerHTML = ''; return; }
    const ch = data.characters[key];
    // 类选择：用已知英→日映射里的候选（简易：优先 High 级）
    const cand = Object.keys(lab.CLS_JP).filter(c => /High|Great|Saint|Master|Lord/.test(c));
    clsSel.innerHTML = '';
    cand.forEach(c => clsSel.add(new Option(c, c)));
    const cls = clsSel.value;
    const lv = parseInt(lvSel.value, 10);
    const stats = lab.calcUnit(data, key, cls, lv, dewChk.checked);
    out.innerHTML = lab.statsPanel(stats, cls + ' · ' + ch.name);
  }
  [unitSel, clsSel, lvSel, dewChk].forEach(el => el && el.addEventListener('change', render));
  render();
})();
</script>'''
if 'ul-unit' in t and 'async function' not in t.split('ul-lab')[1][:2000]:
    t = t.replace('</body>', init_js + '</body>')
    print('已加初始化脚本')

open(p, 'w', encoding='utf-8').write(t)
print('完成')
