# -*- coding: utf-8 -*-
"""
英文内容数据（事实重写自 lzlzmc 的 B 站攻略《圣兽之王》全队友收集及最强配队推荐）
角色名用 {slug|DisplayName} 标记，生成器会替换为指向 /characters/{slug}/ 的链接。
图片用 img 序号引用本地 /assets/article/img_XXX.jpg
"""

PAGE = {
    "title": "All 70 Companions & Best Team Compositions | Unicorn Overlord",
    "desc": "Complete Unicorn Overlord companion recruitment guide for all 70 units, pro farming tips, world map, and the strongest team builds — T0 formations with gear, tactics and PVP lineups.",
}

# ---------- 小技巧 ----------
TIPS = [
    {
        "h": "Quick tip: browse every shop from the map",
        "p": ["Open the map and use the Triangle / R2 toggle on any town that has items — it reveals all shop stock including revival requests. Huge for finding items and finishing revival quests late game."],
        "imgs": [1, 2, 3, 4],
    },
    {
        "h": "Getting onto the three early islands",
        "p": ["How to reach the three small starting islands in-game, as shown."],
        "imgs": [5],
    },
    {
        "h": "Mining (挖矿)",
        "p": [
            "After digging a while a special attack unlocks with 1/2/3 rings, as shown. Ring 1 is too small, ring 3 takes too long — use ring 2 to keep finding hourglasses while you keep digging.",
            "Each nation's mine yields 5 treasure maps. Albion's mine, at 500 depth, can dig up every nation's extra 6th treasure map (the Flower Weapon set).",
            "You only get one map per dig. For farming Philbus stone, use ring 3 at Albion (better drop rate); ring 2 is best if you want hourglasses to unlock maps first.",
        ],
        "imgs": [6, 7, 8],
    },
    {
        "h": "Where to trade for the Ideal Hand Mirror",
        "p": ["Albion, southwest: Fortress City Pedzen. Southwest of the city a winged nun will trade an unlimited number of Ideal Hand Mirrors for 30 medals each."],
        "imgs": [9, 10],
    },
    {
        "h": "Yahna's stone tablets",
        "p": [
            "1. Cornia — note in the ruins east of Gulpante Town, southwest of Fortress City Youquet Castle. Touch the tablets in order: Minotaur → Mermaid → Griffin → Unicorn.",
            "2. Drakenhold — note in a small coastal ruin, eight horse steps west of Nestasheft Town in the south desert. Order: Scorpion → Reaper → Cockatrice → Wyvern.",
            "3. Elheim — note in the deep forest ruins west of the stone bridge that Eltolinde opens, west of Yannis Town. Order: Fairy → Hellhound → Dead → Golem.",
            "4. Bastorias — note in a ruin south of Dworpys Port Town at the far west. Order: Rat → Eagle → Wolf → Bear. Each needs a boat from a nearby town (Rat = Zaganvo, Bear = Old Capital Bastalisa).",
            "5. Albion — note in the big ruins south of Schulavorte Town (boat from Lunokayu in west Elheim). Order: Snake → Seahorse → Goat → Octopus.",
        ],
        "imgs": [],
    },
    {
        "h": "Sprinting",
        "p": ["Hold Circle (PS) / B (Switch) while moving to sprint — this also works while mining."],
        "imgs": [],
    },
    {
        "h": "Special treasure map",
        "p": ["Albion, the back lane of Fortress City Rajan: talk to the cat beastman for the quest. The 'treasure of Elheim' is the sacred tree — finish the quest at the tree north of Aras Fort."],
        "imgs": [],
    },
    {
        "h": "Money farming",
        "p": ["Before clearing the game: {gammel|Gammel} (unit 30) joins with the Miser's Bracelet; Albion map 1 gives the Gold Goblet. Stack both for +400% squad gold, then farm the highest Ancient Magical Circle in central Cornia — about 30k G a run (60k if you clear everything at low level). Use the gold to buy Philbus stones once the mine drop rate falls."],
        "imgs": [],
    },
    {
        "h": "Colosseum coin farming",
        "p": [
            "Always play online mode — it refreshes at 8:00 AM and gives 200 tokens a day for capped battle attempts. Fight 3–5 unit teams and pick the ones with the most coins; 2-unit teams are flag squads that need multi-hit attackers like Swordmasters.",
            "Offline: switch to Free Battle with R1 and clear from the first fight down — about 750 coins total. Pick your own squad as opponent, hold R2 to fast-forward, skip the battle after the enemy speech, then move on. ~5000 coins/hour while watching something.",
        ],
        "imgs": [],
    },
    {
        "h": "Class codex unlocks",
        "p": [
            "Scarlett's alternate class codex: see the video (video link in the source guide).",
            "Cleric (beaked): hire a Cleric at Emvol Sim Fortress in north Cornia, then promote with medals.",
            "Thief (masked): hire a Thief at the Thief Fortress in Drakenhold's south desert, then promote with medals.",
        ],
        "imgs": [],
    },
]

# ---------- 世界地图 ----------
WORLD_MAP = {
    "imgs": [11],
    "rows": [
        ["CORNIA", "Kingdom of Cornia", "Center of the map", "LV1+"],
        ["DRAKENGARD", "Drakenhold (Dragon Kingdom)", "Southeast", "LV10+"],
        ["BASTORIAS", "Bastorias (Snow Kingdom)", "North", "LV25+"],
        ["ELHEIM", "Elheim (Elf Kingdom)", "Southwest", "LV15+"],
        ["ALBION", "Albion (Angel Kingdom)", "West", "LV30+"],
    ],
}

# ---------- 全队友收集 ----------
RECRUIT = [
    {
        "h": "Units 1–10",
        "imgs": [12, 13, 14, 15],
        "items": [
            {"n": "1–5", "name": "Main: The Unicorn Ring", "place": "The small island between west Cornia and east Albion.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 12},
            {"n": "6–8", "name": "Main: The Resolute Archers", "place": "Suligi Fortress, Ulvir Port Town, west Cornia coast.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 13},
            {"n": "9", "name": "Side: The Lone Rebel", "place": "Limitz Fortress, Kongjache Town, west Cornia coast.", "how": "Auto-join through story in the stage.", "notes": ["When {gammel|Gammel} begs for mercy, choose 'spare him' — he leaves and can be recruited in a later stage."], "img": 14},
            {"n": "10", "name": "Side: Hooves of the Tricorn", "place": "Mantoua Fortress, Sursud Port Town, southwest Cornia coast.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 15},
        ],
    },
    {
        "h": "Units 11–20",
        "imgs": [16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
        "items": [
            {"n": "11", "name": "Side: Winged Knight", "place": "Chandur Fortress, Terace Village, central Cornia.", "how": "Join via story choice inside the stage.", "notes": ["Spare {mandrin|Mandrin} when he begs; at the end {sharon|Sharon} asks to join — choose 'Welcome'."], "img": 16},
            {"n": "12", "name": "Main: Swamp Witch", "place": "Bellem Goria Village, Lebjue Village, south Cornia.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 17},
            {"n": "13", "name": "Side: Fortress City Babachimo Liberation", "place": "Fortress City Babachimo, central Cornia.", "how": "Auto-join after clearing the stage.", "notes": ["When Morten surrenders choose 'Take him in'."], "img": 18},
            {"n": "14", "name": "Side: A Mercenary's Trial", "place": "Colm Fortress, Reed Preley Town, south Cornia.", "how": "Join via story choice inside the stage.", "notes": ["At the end {berenice|Berenice} asks to join — choose 'Welcome'."], "img": 19},
            {"n": "15", "name": "Side: Claiming the Knight's Territory", "place": "Gromond Fortress, Fassen Town, Nord Plage Town, central Cornia.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 20},
            {"n": "16", "name": "Field: Ancient Magical Circle", "place": "Lonteria Fortress, southeast Cornia.", "how": "Join via story choice inside the stage.", "notes": ["{selvie|Selvie} asks to investigate — choose 'Agree to help'."], "img": 21},
            {"n": "17", "name": "Side: Punishing the Thieves", "place": "Zelcuba Fortress, Tishudne Town, Laklize Town, southeast Cornia.", "how": "Join via story choice inside the stage.", "notes": ["Move {mille|Millé} next to {nina|Nina} and talk; at the end Nina asks to join — choose 'Welcome'."], "img": 22},
            {"n": "18", "name": "Field: An Angel's Request", "place": "Churches everywhere (pink wing icon).", "how": "Join after meeting the conditions.", "notes": ["Don't refuse {sharon|Sharon} in the Winged Knight stage; trade 30 Sky Fragments with Augulis."], "img": 23},
            {"n": "19", "name": "Side: Ruins Magician", "place": "Will Fortress, northwest Cornia.", "how": "Join via story choice inside the stage.", "notes": ["A mage blocks the way — choose 'Force through'; when deciding {josef|Josef}'s fate choose 'Take him in'."], "img": 24},
            {"n": "20", "name": "Side: Helmet of Confusion", "place": "Emvol Sim Fortress, Webuir Town, Shubo Town, north Cornia.", "how": "Join via story choice inside the stage.", "notes": ["When {josef|Josef} asks your opinion choose 'Keep researching'."], "img": 25},
        ],
    },
    {
        "h": "Units 21–29",
        "imgs": [26, 27, 28, 29],
        "items": [
            {"n": "21", "name": "Side: What We Must Protect", "place": "Shipley Fortress, Sudo Town, Sandridge Town, northeast Cornia.", "how": "Join via story choice inside the stage.", "notes": ["Save Hans' companion Leca in the forest; talk to {clive|Clive} and choose 'Come with us'."], "img": 26},
            {"n": "22–23", "name": "Side: Noble Swordsman", "place": "Longraj Fortress, east Cornia.", "how": "Join via story choice inside the stage.", "notes": ["Bolt the west gate before the fight; have Alain's squad advance north and defeat {melisandre|Melisandre}; choose 'Take her in'. (Skip if you already gave away the Maiden's Ring.)"], "img": 27},
            {"n": "24–27", "name": "Main: Whereabouts of the Priestess", "place": "Fortress City Youquet, Avag Village, Gulpante Town, east Cornia.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 28},
            {"n": "28–29", "name": "Main: The Lost Forest / Side: Counterattack Horn", "place": "Verta Town, Piegenup Fortress, east Elheim (border with the witch village).", "how": "Auto-join after clearing the stage.", "notes": [], "img": 29},
        ],
    },
    {
        "h": "Units 30–39",
        "imgs": [30, 31, 32, 33, 34, 35, 36],
        "items": [
            {"n": "30–32", "name": "Side: The Drifting Thief", "place": "Choperse Fortress, Yannis Town, Kirkuka Town, inland east Elheim.", "how": "Auto-join via story inside the stage.", "notes": ["If you spared {gammel|Gammel} (Lone Rebel) and {mandrin|Mandrin} (Winged Knight), both can be recruited here."], "img": 30},
            {"n": "33", "name": "Side: The Half-Elf's Path", "place": "Rokurosu Town, Boinicla Port Town, east Elheim coast.", "how": "Join via story choice inside the stage.", "notes": ["Bring a fast squad (Griffin Rider) or use Warp Stones; keep the hostage Cleric alive until {ridiel|Ridiel}'s scene — if the Cleric dies she won't join."], "img": 31},
            {"n": "34", "name": "Side: Knight of Elheim", "place": "Salikotte Town, Mezza Fortress, Smutuka Town, south-central Elheim.", "how": "Join via story choice inside the stage.", "notes": ["Have {rosalinde|Rosalinde} talk to Ithilion first."], "img": 32},
            {"n": "35", "name": "Main: Bridge of Azure and Verdure", "place": "Korkeya Fortress, Laurhal City, central Elheim.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 33},
            {"n": "36", "name": "Side: Sunset Archer", "place": "Boitarafi Town, Merietra Town, north Elheim.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 34},
            {"n": "37", "name": "Liberation: Fortress City Vritan Liberation", "place": "Fortress City Vritan, southwest Elheim.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 35},
            {"n": "38–39", "name": "Liberation: Myia Pass Liberation", "place": "Myia Town, southwest Drakenhold.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 36},
        ],
    },
    {
        "h": "Units 40–50",
        "imgs": [37, 38, 39, 40, 41, 42, 43, 44],
        "items": [
            {"n": "40–42", "name": "Main: The Black-General", "place": "Westing Town, Heshultan Fortress, Dreibum Town, southwest Drakenhold.", "how": "Join via story choice inside the stage.", "notes": ["Talk to {primm|Primm} at the east fortress; have Primm talk to {aramis|Aramis}; have Alain talk to {berengaria|Berengaria} (she leaves after 'Another Prince' and returns in 'Heir of the Dragon Kingdom')."], "img": 37},
            {"n": "43", "name": "Side: Into the Dust", "place": "Gangfelder Town, Thief Fortress, south Drakenhold.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 38},
            {"n": "44–45", "name": "Side: Black Knight of the Hot Sands", "place": "Glabmund Village, Nestasheft Town, south Drakenhold.", "how": "44 auto-joins via story; 45 joins via story choice.", "notes": ["Have {aramis|Aramis} fight {gloucester|Gloucester} at the end; Gloucester won't join without Aramis in the squad."], "img": 39},
            {"n": "46", "name": "Liberation: Fortress City Adeputi Liberation", "place": "Fortress City Adeputi, west Drakenhold.", "how": "Join via story choice inside the stage.", "notes": ["When {jeremy|Jeremy} surrenders choose 'Spare him'."], "img": 40},
            {"n": "47", "name": "Side: Guardian of Order", "place": "Onpaleste Town, Noymot Fortress, central Drakenhold.", "how": "Join via story choice inside the stage.", "notes": ["Talk to {hilda|Hilda} with Primm's squad; then talk to her again at the east ruins and choose 'I need you'."], "img": 41},
            {"n": "48", "name": "Main: Another Prince / Colosseum Champion", "place": "Baumrath Colosseum, central Drakenhold.", "how": "Joins after becoming colosseum champion.", "notes": ["Use LV20 {travis|Travis} solo vs awakened {amalia|Amalia}: skills [Passive Steal / Guard Lock / Dodge], Steal aimed at highest PP enemy, Azure Crystal pendant for full PP — exhaust her PP and AP to win."], "img": 42},
            {"n": "49", "name": "Liberation: Any 4 Local Liberations", "place": "Any 4 local liberation battles in Drakenhold.", "how": "Joins after 4 local liberations.", "notes": ["Finish the 'Whereabouts of the Priestess' side quest to trigger Luno's disappearance; a knight named Roland helps 4 times — after the 4th he joins."], "img": 43},
            {"n": "50", "name": "Main: Heir of the Dragon Kingdom", "place": "Sordraga City, north Drakenhold.", "how": "Join via story choice inside the stage.", "notes": ["Recruit {aramis|Aramis} (Black-General) and {gloucester|Gloucester} (Hot Sands); clear the Kleinfelt Pass liberation but don't enter the main gate; reach {gilbert|Gilbert} via Hozant Fortress and Qiuzha Fortress; promise {virginia|Virginia} to help — Gilbert joins after the quest."], "img": 44},
        ],
    },
    {
        "h": "Units 51–60",
        "imgs": [45, 46, 47, 48, 49, 50, 51],
        "items": [
            {"n": "51–53", "name": "Main: Snowstorm Plains", "place": "Tingwakran Port Town, Sedrosha Fortress, Old Capital Bastalisa, east Bastorias.", "how": "Auto-join after clearing the stage.", "notes": ["Have {yunifi|Yunifi}'s squad talk to {ramona|Ramona}'s squad."], "img": 45},
            {"n": "54", "name": "Side: Path of the Beasts", "place": "Dachanani Town, Connadeau Fortress, Wastkugla Town, east Bastorias.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 46},
            {"n": "55", "name": "Liberation: Fortress City Solbac Quarto Liberation", "place": "Fortress City Solbac Quarto, south Bastorias.", "how": "Join via story choice inside the stage.", "notes": ["Recruit {nina|Nina} in 'Punishing the Thieves' first; after the stage have Nina talk to the unit and choose 'Take him in'."], "img": 47},
            {"n": "56–57", "name": "Side: Resisters and Compromisers", "place": "Central Bastorias (multiple towns/fortresses).", "how": "Join via story choice inside the stage.", "notes": ["Talk to {govil|Govil} west of Solbac Quarto and {bertrand|Bertrand} at the end of the road west of Prijasari; a new '!' opens a third route that recruits both at once. Send Griffin squads to grab the 6 sparkles."], "img": 48},
            {"n": "58", "name": "Liberation: Fortress City Pedzen Liberation", "place": "Fortress City Pedzen, southwest Albion.", "how": "Join via story choice inside the stage.", "notes": ["After the stage {scarlett|Scarlett} talks to {fodoquia|Fodoquia} — choose 'Save him'."], "img": 49},
            {"n": "59", "name": "Liberation: Fortress City Rajan Liberation", "place": "Fortress City Rajan, southeast Albion.", "how": "Join via story choice inside the stage.", "notes": ["After the stage Alain talks to {jerome|Jerome} — choose 'Recruit'."], "img": 50},
            {"n": "60", "name": "Side: Guardian of the Church", "place": "Tralosa Fortress, Gelezu Town, Daiagulf Town, east Albion.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 51},
        ],
    },
    {
        "h": "Units 61–70",
        "imgs": [52, 53, 54, 55],
        "items": [
            {"n": "61", "name": "Side: Flower of Remembrance", "place": "Birijan Hill Fortress, Okford Town, Hevenliba Town, central Albion.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 52},
            {"n": "62", "name": "Main: Road to the Cathedral", "place": "Orje Town, Banpu Town, Greyshell Fortress, Wins Abbey Town, Wochesta Fortress, Bisfaine Cathedral, central Albion.", "how": "Auto-join after clearing the stage.", "notes": [], "img": 53},
            {"n": "63–64", "name": "Main: Unicorn Overlord", "place": "Grancolinu Castle, dead center of Cornia.", "how": "Auto-join after clearing the stage.", "notes": ["Have {sanatio|Sanatio}'s squad talk to {nigel|Nigel}'s squad."], "img": 54},
            {"n": "65–70", "name": "Side: Revived Calamity Capital", "place": "Zenoyra Sanctuary, northwest Cornia.", "how": "Auto-join after clearing the stage.", "notes": ["Only unlocked on the True Ending route: give away the Maiden's Ring, upgrade all six sanctum rings, beat the final boss and free the soul for the True Ending."], "img": 55},
        ],
    },
]

# ---------- 最强配队 ----------
TEAM_INTRO = {
    "p": [
        "All gear upgrades below are done at the blacksmith between Okford Town and Hevenliba Town (central Albion) using Philbus stones (mined at ~450 depth in the Albion mine, or bought from any underground merchant for 50k G). The builds below assume full potions — about 20,000 colosseum coins total.",
        "In tactics programming, any skill not set is simply not used — this affects AP/PP totals. These lineups were tested over 70+ hours and dozens of runs; T1+ teams are worth feeding Dream Dew. Use the medal trade spot in the tips to stock Ideal Hand Mirrors.",
        "After the update, Dream Dew now gives random stat boosts and no longer breaks the stat cap.",
    ],
}

TEAMS = [
    {
        "tier": "T0",
        "title": "Snowfield Rangers — Two Princes",
        "tags": ["Dispel", "Guaranteed AoE", "Blind-proof", "Debuff-proof"],
        "img": 56,
        "roster": ["yunifi", "fodoquia", "gilbert", "dinah", "tatiana"],
        "pros": "On the highest difficulty it clears every PVE fight except the final boss. First volley of fast Frozen Arrow Rain with high-crit follow-ups, and a fast second volley. The fox's Valor skill jumps over enemies/teammates (no battering ram needed inside walls), the angel ignores terrain, the fox doubles move speed at night and outruns mounts with the Griffin speed buff. The Feather Shield Guard's skill self-casts Magic Reflection.",
        "cons": "Forms late; Yunifi's stats matter and her core skill unlocks at LV30. Before the snow nation, swap the Feather Shield Guard for any Iron Guard, the fox for an Officer, and sub a unit like {lhinalagos|Lhinalagos} with the Hunter's Bow for a budget version. Tatiana is picked over Sharon/Primm as Bishop because she is faster.",
        "gear": [
            ["yunifi", "King's Bow Bastoric (Bastorias Yahna tablets), Brave Eye Patch (40k G, Old Capital Bastalisa), Dream Crown (Albion map 5), Lionheart (from {morard|Morard} on join)."],
            ["fodoquia", "Zenoyra Knight Sword+ (colosseum offline rank 3), Dragonrock Ice Shield (from {amalia|Amalia}), Angel Plume (20 Sky Fragments), Lantern Ring (west of the sea near Rajan, Rex Tower)."],
            ["gilbert", "Sacred Sword (Cornia sanctum), Gambler's Coin (20k G, Fortress City Youquet), Black Swan Plume (from {mandrin|Mandrin}), Scarlet Stone Pendant (post 'Heir of the Dragon Kingdom')."],
            ["dinah", "Wind Lance Zephyros (wind gate from Huls Port), Wise Owl Scarf (Albion map 2), Scarlet Pendant ('Whereabouts of the Priestess' reward), Azure Crystal Pendant (40k G, west Bastorias merchant)."],
            ["tatiana", "Sacred Staff (Albion sanctum), White Cat-ear Hood (20 Sky Fragments), Crimson Crystal Pendant (40k G, Fortress City Rajan), Blue Stone Pendant (10k G, Fortress City Babachimo)."],
        ],
        "tactics": "Yunifi: Frozen Arrow Rain (no cond.), Sonic Arrow (fastest enemy), Mystic Arrow (armor enemies), Silver Magic Bullet, Triple Counter, Eagle Eye. Fodoquia: Dim Light (archer ally), Mystic Shield, Ride the Wind (back ally), Magic Reflection, Debuff Transfer (self debuffed), Self-sacrifice (back + archer ally). Gilbert: Defense Order (ally avg HP ≤50%), Attack Order, Vanishing Thrust (buffed enemy / archer / flier), Haste Order, Good Opportunity. Dinah: Poison Thrust (aligned enemy), Sharp Lance, Passive Lock, Swift Dispel (self PP≥2 vs archer / mage / enemy AP≥2), Moonlit Grace, Shadow Chase. Tatiana: Sacred Healing (back ally debuffed / front ally HP≤75%), Swift March (back archer ally).",
    },
    {
        "tier": "T0",
        "title": "Sixty-Two Rain — Elf Archer",
        "tags": ["Status-cure", "Guaranteed AoE", "Blind-proof", "Reflect-proof", "Dispel-proof"],
        "img": 57,
        "roster": ["yahna", "sharon", "monica", "ridiel"],
        "extra": "plus a recruited mercenary witch Louise (same witch class as Yahna, speed type)",
        "pros": "Very high damage ceiling (easily 2000+), forms early — everything except the elf archer is an early unit. The witch is the only unit with guaranteed hits, stacked into the front with dodge. The elf passive + healing skills clear debuffs on the whole squad and heal; even if the first Trinity Rain volley is blinded, the second volley cleanses and rebuffs before firing.",
        "cons": "Weak to Magic Reflection (handled below), flag-shield squads, the final boss shield, and extreme-speed teams. Loses to the Snowfield Rangers above, beats the six teams below.",
        "tactic_imgs": [58, 59, 60, 61, 62],
        "gear": [
            ["yahna", "Millennium Staff+ (30 Sky Fragments), Magic Soul (Bastorias map 4 or ~2000 colosseum coins), Ancient Crown (Bastorias map 5), Amethyst Pendant (Falcon Knight boss drop)."],
            ["sharon", "Lupine Staff (Albion map 6), Black Cat-ear Hood (2000 coins), Prickly Ribbon (30k G, Kuantipert), Crimson Crystal Pendant (40k G, west Bastorias)."],
            ["monica", "Gemstone Flower Sword (Cornia map 6), Blue Rose Shield+ (from {virginia|Virginia}), Familiar Collar (30k G, Lebjue Village), Crimson Pendant (from {amalia|Amalia})."],
            ["ridiel", "Wind Bow Apoliothes (wind gate east of Nestasheft), Royal Scarf (40k G, Old Capital Bastalisa), Black Swan Plume (20k G, Old Capital Bastalisa), Azure Crystal Pendant (offline colosseum rank 5)."],
            ["Louise", "Phantom Knight Staff+ (highest Ancient Magical Circle clear), Lips Wind Ring (wind gate east of the underground merchant), Azure Crystal Pendant (from {amalia|Amalia}), Royal Scarf (40k G, Old Capital Bastalisa)."],
        ],
        "tactics": "Yahna: Trinity Rain (no cond.), Repeat Casting. Sharon: Sacred Healing (front ally HP≤75% / back elf ally), Healing (back ally, highest magic), Swift March. Monica: Frontline Healing (front ally HP≤50%), Holy Sword (self 100% HP, no fliers), Fine Slash (no armor / no fliers) — these two prevent unfreezing the Feather Shield Guard; Line Heal (back ally), Witch Link, Royal Guard (self HP≤75%), Holy Guard (self debuffed), Line Barrier. Ridiel: Ice Arrow (armor + flier), Wind Arrow (lowest dodge), Selfless Healing, Swift Cure (back ally debuffed). Louise: Illusory Barrier (front ally), Quick March (back highest magic), Focus (back highest magic). Strategy note: pre-register tactics per class; save witch strategy slots 2/3 to swap loadouts (fast-march condition → PP≥4 ally when Yahna isn't lead; Pure Domain opener to prevent the bishop's cat-ear conflict).",
    },
    {
        "tier": "T0",
        "title": "Elf Sisters — Protagonist",
        "tags": ["Full dispel", "Guaranteed AoE", "Blind-proof", "Debuff-proof", "One-shots final boss"],
        "img": 63,
        "roster": ["alain", "rosalinde", "eltolinde", "selvie", "railanor"],
        "pros": "Forms by mid-game; gear comes later. All three damage dealers are status-immune; the Elf Sisters' dual Elemental Roar plus Alain's Spiral Blade deal huge damage. Railanor with high dodge can attack 2–3 rounds, gaining an AP per dodge. Strong in PVP too (unless the colosseum bans one Elf Sister).",
        "cons": "Loses to Snowfield Rangers and Sixty-Two Rain; beats the five below. Rosalinde's Spirit Wrath + removing Alain's Haste Order lets you stun the final boss before its shield and one-turn kill it.",
        "gear": [
            ["alain", "Unicorn Holy Sword (S rank, Tomb of the Kings), Azure Crest Shield+ (second copy from the broken bridge house), Unicorn Ring ('Unicorn and Maiden' main quest), Sniper Lens (from {celeste|Celeste})."],
            ["rosalinde", "Elf sisters' power + high dodge; Angel's power build. (Attack type via Ideal Hand Mirror.)"],
            ["eltolinde", "Same build direction as Rosalinde — dual Elemental Roar damage core."],
            ["selvie", "Speed build; enables early formation."],
            ["railanor", "High dodge stacking; speed/attack type via Ideal Hand Mirror."],
        ],
        "tactics": "Alain: Star Sword (for the final boss). Rosalinde: Spirit Wrath equipped for the final-boss stun. Remove Alain's Haste Order before the boss so the stun lands before the shield goes up. Standard: Elemental Roar chain from the Elf Sisters with Spiral Blade follow-ups.",
    },
    {
        "tier": "T0",
        "title": "Triple Knight — Archer",
        "tags": ["Status-cure", "Dispel", "AoE", "Dispel-proof knights"],
        "img": 64,
        "roster": ["clive", "rolf", "adel", "scarlett"],
        "extra": "plus Reno (unit 49)",
        "pros": "Forms early — sub {josef|Josef} for Reno before the latter unlocks. The three knights stack attack buffs via cheering early on; the archer handles air targets. Core equipment is buyable as soon as Elheim opens. Works from early to late game: enemies who blind/dark can't stop the cavalry charge; those who stop the charge can't stop the archer's AoE.",
        "cons": "Loses to the three teams above, beats the four below. Beats PVP flag squads; only fears extreme-speed teams, especially the speed Griffin squad.",
        "gear": [
            ["rolf", "Hunter's Bow+ (15k G, Fortress City Vritan), Crimson Crystal Pendant (2000 coins), Azure Crystal Pendant (1000 coins), Star Charm ('A Dream Within a Dream' clear)."],
            ["clive", "Defense build; core knight gear."],
            ["adel", "Defense build; knight gear + buffs."],
            ["scarlett", "Lucky build via Ideal Hand Mirror; healing core."],
            ["reno", "Defense build; second knight pillar."],
        ],
        "tactics": "Rolf: Arrow Rain (no cond.) + follow-ups. Knights: Cheer chain to stack attack; guard skills vs blind/dark; archer AoE to break the frontline the charge can't reach.",
    },
    {
        "tier": "T1",
        "title": "Dragon Rider Sisters — Lion Double-Jump",
        "tags": ["PVE strong", "Early form", "Charge-proof"],
        "img": 65,
        "roster": ["primm", "hilda", "morard", "nina"],
        "extra": "plus a recruited Feather Shield Guard Rudolf (speed type)",
        "pros": "Strong in PVE, forms early. An improved 'Dragon Rider Descends' that fixes the resource-hungry, one-fly-can't-kill, armor-immune problems — the hammer girl and lion solve it. The Dragon Rider's charge resists blind; by the time it charges, the Bishop has cleansed debuffs. The Feather Shield Guard's Self-sacrifice blocks hits and regens PP, so even with PP-eating accessories it keeps 4 PP for Magic Reflection and Debuff Transfer. 4-unit version: drop the lion.",
        "cons": "Not for PVP — too slow. Weaker than the top 4, stronger than the 3 below.",
        "gear": [
            ["primm", "King's Staff Albio (Albion Yahna tablets), Prickly Ribbon (30k G, Kuantipert), Black Swan Plume (20k G, Fortress City Drachodolina), Black Crystal Pendant (beat offline colosseum rank 1)."],
            ["hilda", "Attack build; hammer core."],
            ["morard", "Attack build; lion tank-core damage."],
            ["nina", "Attack build; second damage pillar."],
            ["Rudolf", "Speed type; defense/guard build."],
        ],
        "tactics": "Primm: Sacred Healing (back ally debuffed / front ally), Self-redemption (self HP≤50%), Swift Healing (other ally HP≤75%), Cleanse (back/front ally debuffed), Resurrection. Dragon Rider charge → cleanse timing → Feather Shield Guard self-sacrifice rotation.",
    },
    {
        "tier": "T1",
        "title": "Ailment Bea — Pursuit",
        "tags": ["Early form", "Dodge-core", "High PVE"],
        "img": 66,
        "roster": ["berengaria", "travis", "gloucester"],
        "extra": "plus two more units (Lis and Oshu)",
        "pros": "Forms as soon as you finish the dragon-kingdom desert. Bea's high dodge makes her pursuit very strong — multiple actions a round is normal, and misses refund her PP. Dodge 100 is the median: above it even Alain's Spiral Blade misses; below it you get hit. Cavalry keeps speed up; Bea's Valor drains energy and Gloucester's skill summons a damage circle.",
        "cons": "Fears ailment-clearing teams, White Knight status-resist teams, and elite flag squads. Not for PVP — wins only with luck; strong PVE.",
        "gear": [
            ["berengaria", "King's Axe Drangarush+ (Drakenhold Yahna tablets), Mirage Great Shield (Kirkuka Town), Pursuit Earrings (from {mandrin|Mandrin}), Hero Medal (from {amalia|Amalia})."],
            ["travis", "Speed build; AP/PP sustain."],
            ["gloucester", "All-round build; summons damage circle."],
        ],
        "tactics": "Bea: Death Spiral (enemy row of 3+, row of 2+, or statused enemy). Stack dodge; pursue with refunded PP; Gloucester's circle amplifies the damage window.",
    },
    {
        "tier": "T2",
        "title": "Rose Knights",
        "tags": ["PVE OK", "Cousin team", "Speed boost"],
        "img": 67,
        "roster": ["virginia", "monica", "miriam", "kitra", "sanatio"],
        "pros": "Built for the 'cousin' (Virginia). PVE-fine, not PVP. Forms early — sub a Bishop for Sanatio early. The Griffin cuts the backline, hammer + cousin take the frontline, Sanatio keeps healing. Its other job: summon it to use the group speed buff.",
        "cons": "Not for PVP — too slow. Weaker than the top 6, stronger than the one below.",
        "gear": [
            ["virginia", "King's Sword Cornix+ (Cornia Yahna tablets), guardian build."],
            ["monica", "Hammer frontline core."],
            ["miriam", "Guard build."],
            ["kitra", "Attack build."],
            ["sanatio", "Speed build; sustain healer."],
        ],
        "tactics": "Griffin flanks the backline, hammer and cousin break the front, Sanatio sustains; use the squad for its group speed buff.",
    },
    {
        "tier": "T2",
        "title": "Consort's Three Swordmasters",
        "tags": ["Anti-flag", "Anti-boss", "6x Meteor Slash"],
        "img": 68,
        "roster": ["melisandre", "aramis", "leah", "mille"],
        "extra": "plus Lenis (unit 60)",
        "pros": "Forms late. Built to beat PVP flag squads and the final-boss team — 6 Meteor Slashes nothing can tank. The Griffin archer locks the backline so it can't be burst; the front is taken down by the hammer girl. Must control speed or the three swordmasters tickle; the frontline moving first also blocks one blind. The first 3 Meteor Slashes soften, passive crit stacks to 100%, then the last 3 always hit.",
        "cons": "Struggles vs full armor, or if the front hammer can't break through — becomes a tickle squad.",
        "gear": [
            ["melisandre", "Attack build; Meteor Slash core."],
            ["aramis", "Attack build; second Meteor Slash."],
            ["leah", "Attack build; third Meteor Slash."],
            ["mille", "Speed build; agility control."],
            ["Lenis", "Speed build; Griffin archer backline lock."],
        ],
        "tactics": "Speed-tune the trio so all three act before the enemy; 3x Meteor Slash to soften → crit-stack to 100% → 3x guaranteed hits. Griffin archer locks the backline first.",
    },
]

# 最后两队（简版）
TEAMS_EXTRA = {
    "imgs": [69, 70],
    "p": "Two more squads — the Five Elders and the Elf Archer Martyr — are serviceable but far below the eight above, so the author didn't include their gear or tactics programming.",
}

# ---------- PVP ----------
PVP = {
    "intro": "Two recommended squads — one offense, one defense (the defense one is your online-mode defense slot). The offense squad shouldn't be used for defense. Since these are PVP-only, they strip gear from the teams above and use post-game units — not for PVE.",
    "offense": {
        "title": "T0 Offense: Flag Rat Snowfield Rangers",
        "imgs": [71, 72, 73],
        "roster": ["yunifi", "elgor"],
        "p": [
            "Fears nothing except Swordmaster squads and the Alcina/Druid/War-Owl stacked squad (multi-dispel + debuff). The rat's first skill adds +50 dodge — 200+ dodge dodges everything except guaranteed hits — plus the flag's 5 shields, so the frontline is nearly unkillable.",
            "Gear and tactics are in the screenshots; the pieces are all described above (Ctrl+F the item names). Yunifi uses the loadout from her team above. {elgor|Elgor} (the rat) needs 5 Life/Agility/Insight Dew and a speed Ideal Hand Mirror.",
        ],
    },
    "defense": {
        "title": "T0 Defense: Alcina Elf Team",
        "imgs": [74, 75, 76, 77, 78],
        "roster": ["alain", "alcina", "beaumont", "rosalinde"],
        "p": [
            "Based on Bilibili UP '局部小型气旋's squad — excellent as a defender. A 4-C team (everyone except Beaumont is a C-role): the opponent can't suppress all five, at most two. Beaumont joins at LV48 so two Miracle Fruits cap him; the other great shields are too low level.",
            "Everyone except Beaumont eats all 10 dew types (Alain and Rosalinde already did — farm Alcina and the extra unit). Beaumont gets Life/Defense/Protection/Perseverance/Agility Dew x5. Ideal Hand Mirrors: Alain 2x All-round, Beaumont 2x Tenacity, others 2x Attack.",
        ],
    },
}

SOURCE_NOTE = {
    "en": "Guide compiled from the Chinese guide 《圣兽之王》全队友收集及最强配队推荐（顶级编程优化） by Bilibili author lzlzmc (edited 2026-04-25), rewritten into English. Screenshots are in-game captures and remain in Chinese.",
    "zh": "内容整理自 B 站用户 lzlzmc 的原创攻略《圣兽之王》全队友收集及最强配队推荐（顶级编程优化）（编辑于 2026-04-25），已重写为英文。截图均为游戏内截图，保留中文。",
    "url": "https://www.bilibili.com/opus/916422313046442004",
    "author": "lzlzmc",
}
