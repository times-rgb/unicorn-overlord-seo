# -*- coding: utf-8 -*-
import re
h = open(r'G:\CODEX\projects\my-website\guides\complete-team-recruitment\index.html', encoding='utf-8').read()
print('chars refs:', len(re.findall(r'/assets/chars/', h)))
print('member links:', len(re.findall(r'class="member"', h)))
print('members with img:', len(re.findall(r'class="member" href', h)))
print('tcards:', len(re.findall(r'class="tcard"', h)))
print('roster divs:', len(re.findall(r'class="roster"', h)))
# 队伍卡内成员
for m in re.findall(r'<div class="tcard">(.*?)</div></div></div>', h, re.S):
    name = re.search(r'<h3>(.*?)</h3>', m)
    mem = len(re.findall(r'class="member"', m))
    print('  team:', (name.group(1) if name else '?')[:40], 'members:', mem)
