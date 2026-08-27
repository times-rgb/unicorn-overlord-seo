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

// 职业英→日 成长率名（覆盖主要职业）
const CLS_JP = {
  'Lord': 'ロード', 'High Lord': 'ハイロード', 'Fighter': 'ファイター', 'Vanguard': 'ヴァンガード',
  'Soldier': 'ソルジャー', 'Sergeant': 'サージェント', 'Knight': 'ナイト', 'Great Knight': 'グレートナイト',
  'Paladin': 'パラディン', 'Priestess': 'プリーステス', 'High Priestess': 'ハイプリーステス',
  'Snow Ranger': 'スノーレンジャー', 'Cleric': 'クレリック', 'Bishop': 'ビショップ',
  'Thief': 'シーフ', 'Rogue': 'ローグ', 'Wizard': 'ウィザード', 'Witch': 'ウィッチ',
  'Hunter': 'ハンター', 'Sniper': 'スナイパー', 'Shooter': 'シューター', 'Shield Shooter': 'シールドシューター',
  'Hoplite': 'ホプリタイ', 'Legionnaire': 'カタフラクト', 'Elf Augur': 'エルフアウグル', 'Elven Augur': 'エルフアウグル',
  'Feather Bow': 'フェザーボウ', 'Feather Sword': 'フェザーソード', 'Feather Rod': 'フェザーロッド', 'Feather Shield': 'フェザーシールド',
};

// 全药水（每种 5 瓶上限）加成
const DEW_FULL = { hp: 10, pAtk: 5, pDef: 5, mAtk: 5, mDef: 5, acc: 10, eva: 10, crit: 5, guard: 5, spd: 5, mov: 0 };

function calcUnit(data, charKey, clsEn, level, useDew, equipBonus) {
  const ch = data.characters[charKey];
  if (!ch || !ch.growth1) return null;
  const jp = CLS_JP[clsEn];
  const cls = data.classes[jp];
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
  if (useDew) for (const k in DEW_FULL) out[k] += DEW_FULL[k];
  if (equipBonus) for (const k in equipBonus) if (out[k] !== undefined) out[k] += equipBonus[k];
  return out;
}

// 生成卡牌风属性面板（RPG/TCG 风）
function statsPanel(ch, stats, clsEn, level, dew) {
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
  return '<div class="ul-card"><div class="ul-head"><img class="ul-ava" src="' + ava + '" alt="' + (ch ? ch.name : '') + '">' +
    '<div class="ul-id"><b>' + (ch ? ch.name : '?') + '</b><span>' + (clsEn || '') + ' · ' + ((ch && ch.faction) || '') + '</span>' +
    '<span class="ul-gt">' + ((ch && ch.growth1) || '?') + ' / ' + ((ch && ch.growth2) || '?') + '</span></div>' +
    '<div class="ul-lv">LV ' + level + (dew ? '<small>+ full dews</small>' : '<small>base</small>') + '</div></div>' +
    '<table class="ul-stats">' + rows + '</table>' +
    '<div class="ul-foot">Precise level-' + level + ' stats · formula from HyperWiki(JP)</div></div>';
}

window.UOLab = { loadUOData, calcUnit, statsPanel, STAT_LABEL, STAT_KEYS, CLS_JP, DEW_FULL };
