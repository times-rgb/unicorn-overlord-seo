/* ============================================================
   Unit Lab — 数值计算引擎（Unicorn Overlord）
   公式来源：HyperWiki(JP) stat-calc（确定性成长）
   基础 = Round(Lv基础/100 × 补正A + 补正B)
     补正A = Round((g1_A+g2_A)/2) + 职业成长率
     补正B = Round((g1_B+g2_B)/2)
   命中显示 = 计算值 + 100
   最终 = 基础 + 装备 + 药水 + 编成
   ============================================================ */
let UODATA = null;

async function loadUOData() {
  if (UODATA) return UODATA;
  const r = await fetch('/assets/uo-data.json');
  UODATA = await r.json();
  return UODATA;
}

const STAT_KEYS = ['hp', 'pAtk', 'pDef', 'mAtk', 'mDef', 'acc', 'eva', 'crit', 'guard', 'spd', 'mov'];
const STAT_LABEL = { hp: 'HP', pAtk: 'Phys ATK', pDef: 'Phys DEF', mAtk: 'Mag ATK', mDef: 'Mag DEF',
  acc: 'Accuracy', eva: 'Evasion', crit: 'Crit Rate', guard: 'Guard Rate', spd: 'Initiative', mov: 'Move' };

// 职业英→日 成长率名（兼容英文类名入参；新数据直接用日文键）
const CLS_JP = {
  'Lord': 'ロード', 'High Lord': 'ハイロード', 'Fighter': 'ファイター', 'Vanguard': 'ヴァンガード',
  'Soldier': 'ソルジャー', 'Sergeant': 'サージェント', 'Knight': 'ナイト', 'Great Knight': 'グレートナイト',
  'Paladin': 'パラディン', 'Priestess': 'プリーステス', 'High Priestess': 'ハイプリーステス',
  'Cleric': 'クレリック', 'Bishop': 'ビショップ', 'Thief': 'シーフ', 'Rogue': 'ローグ',
  'Wizard': 'ウィザード', 'Witch': 'ウィッチ', 'Sorceress': 'ソーサレス', 'Hunter': 'ハンター',
  'Sniper': 'スナイパー', 'Hoplite': 'ホプリタイ', 'Legionnaire': 'カタフラクト',
  'Elf Augur': 'エルフアウグル', 'Elven Augur': 'エルフアウグル',
  'Elven Archer': 'エルフアーチャー', 'Elven Fencer': 'エルフフェンサー', 'Housecarl': 'ハスカール',
  'Viking': 'バイキング', 'Sellsword': 'セルウォード', 'Landsknecht': 'ランツクネヒト',
  'Feather Bow': 'フェザーボウ', 'Feather Sword': 'フェザーソード', 'Feather Rod': 'フェザーロッド',
  'Feather Shield': 'フェザーシールド', 'Druid': 'ドルイド', 'Enchantress': 'エンチャントレス',
  'Warrior': 'ウォリアー', 'Berserker': 'バーサーカー', 'Shooter': 'シューター',
  'Shield Shooter': 'シールドシューター', 'Radiant Knight': 'ラディアントナイト', 'Dark Knight': 'ダークナイト',
  'Wereowl': 'ワーアウル', 'Werefox': 'ワーフォックス', 'Werewolf': 'ワーウルフ',
  'Werebear': 'ワーベア', 'Tactician': 'タクティシャン', 'Strategist': 'ストラテジスト',
  'Angelic Knight': 'エンジェリックナイト', 'Divine Shooter': 'ディバインシューター',
  'Snow Ranger': 'スノーレンジャー', 'Swordmaster': 'ソードマスター', 'Lancer': 'ランサー',
  'Sainted Knight': 'セインテッドナイト', 'Warlock': 'ウォーロック', 'Mage': 'メイジ', 'Archer': 'アーチャー',
};

// 每瓶药水加成（上限 5 瓶/属性）
const DEW_PER = { hp: 2, pAtk: 1, pDef: 1, mAtk: 1, mDef: 1, acc: 2, eva: 2, crit: 1, guard: 1, spd: 1, mov: 0 };
// 全药水（5 瓶）合计
const DEW_FULL = {};
for (const k in DEW_PER) DEW_FULL[k] = DEW_PER[k] * 5;

// 装备加成：按槽位语义映射（Fandom 实测：武器物攻/魔攻；盾物防/ガード率）
function equipStats(item) {
  const b = {};
  if (!item) return b;
  const slot = item.slot;
  if (['sword', 'axe', 'lance', 'bow', 'rod'].indexOf(slot) >= 0) {
    if (item.phys) b.pAtk = (b.pAtk || 0) + item.phys;
    if (item.magic) b.mAtk = (b.mAtk || 0) + item.magic;
  } else if (['shield', 'bigshield'].indexOf(slot) >= 0) {
    if (item.phys) b.pDef = (b.pDef || 0) + item.phys;       // 物防
    if (item.magic) b.guard = (b.guard || 0) + item.magic;   // ガード率
  }
  if (item.bonus) for (const k in item.bonus) b[k] = (b[k] || 0) + item.bonus[k];
  return b;
}

function calcUnit(data, charKey, clsKey, level, dew, equipItems) {
  const ch = data.characters[charKey];
  if (!ch || !ch.growth1) return null;
  // clsKey 支持 JP 键（新数据）或英文名（经 CLS_JP 映射）
  const cls = data.classes[clsKey] || data.classes[CLS_JP[clsKey]];
  const lv = data.expTable[String(level)];
  if (!cls || !lv) return null;
  const g1 = data.growthTypes.A[ch.growth1], g2 = data.growthTypes.A[ch.growth2];
  const b1 = data.growthTypes.B[ch.growth1], b2 = data.growthTypes.B[ch.growth2];
  if (!g1 || !g2) return null;  // 类型未收录：不估算，宁缺毋滥
  const out = {};
  for (let i = 0; i < 10; i++) {
    const A = Math.round((g1[i] + g2[i]) / 2) + cls[STAT_KEYS[i]];
    const B = Math.round((b1[i] + b2[i]) / 2);
    let v = Math.round(lv[STAT_KEYS[i]] / 100 * A + B);
    if (STAT_KEYS[i] === 'acc') v += 100;
    out[STAT_KEYS[i]] = v;
  }
  out.mov = cls.mov;
  // 装备
  (equipItems || []).forEach(function (it) {
    const s = equipStats(it);
    for (const k in s) if (out[k] !== undefined) out[k] += s[k];
  });
  // 药水：true=全吃 | {stat:瓶数} | 0/null=不吃
  if (dew === true) {
    for (const k in DEW_FULL) out[k] += DEW_FULL[k];
  } else if (dew && typeof dew === 'object') {
    for (const k in DEW_PER) {
      const n = dew[k] | 0;
      if (n > 0) out[k] += DEW_PER[k] * Math.min(n, 5);
    }
  }
  return out;
}

// 生成卡牌风属性面板（RPG/TCG 风）
function statsPanel(ch, stats, clsLabel, level, dew, equipNames) {
  const ava = (ch && ch.img) || (ch ? '/assets/chars/' + (ch.faction || '') + '_' + ch.name + '.webp' : '');
  const maxes = { hp: 150, pAtk: 80, pDef: 70, mAtk: 80, mDef: 70, acc: 190, eva: 100, crit: 40, guard: 50, spd: 80, mov: 100 };
  const ic = { hp: '❤️', pAtk: '⚔️', pDef: '🛡️', mAtk: '🔮', mDef: '🛡', acc: '🎯', eva: '💨', crit: '💥', guard: '🗡️', spd: '⚡', mov: '👢' };
  let rows = '';
  for (const k of STAT_KEYS) {
    const w = stats ? Math.min(100, Math.round(stats[k] / maxes[k] * 100)) : 0;
    const col = w >= 75 ? 'gold' : w >= 45 ? 'silver' : 'dim';
    rows += '<tr><td class="ul-ic">' + ic[k] + '</td><td>' + STAT_LABEL[k] + '</td><td class="ul-val"><b>' + (stats ? stats[k] : '—') + '</b></td>' +
      '<td class="ul-bar"><i class="' + col + '" style="width:' + w + '%"></i></td></tr>';
  }
  const equipLine = (equipNames && equipNames.length) ? ' · ' + equipNames.join(' + ') : '';
  return '<div class="ul-card"><div class="ul-head"><img class="ul-ava" src="' + ava + '" alt="' + (ch ? ch.name : '') + '">' +
    '<div class="ul-id"><b>' + (ch ? ch.name : '?') + '</b><span>' + (clsLabel || '') + ' · ' + ((ch && ch.faction) || '') + '</span>' +
    '<span class="ul-gt">' + ((ch && ch.growth1) || '?') + ' / ' + ((ch && ch.growth2) || '?') + '</span></div>' +
    '<div class="ul-lv">LV ' + level + (dew ? '<small>+ dews</small>' : '<small>base</small>') + '</div></div>' +
    '<table class="ul-stats">' + rows + '</table>' +
    '<div class="ul-foot">Precise level-' + level + ' stats · HyperWiki formula' + equipLine + '</div></div>';
}

window.UOLab = { loadUOData, calcUnit, statsPanel, equipStats, STAT_LABEL, STAT_KEYS, CLS_JP, DEW_PER, DEW_FULL };
