(function () {
  var U = window.UO;
  var ids = ['front-left', 'front-center', 'front-right', 'back-left', 'back-right'];
  var params = new URLSearchParams(location.search);
  var team = U.defaultTeam;
  try {
    if (params.get('team')) team = JSON.parse(decodeURIComponent(escape(atob(params.get('team')))));
    else if (localStorage.uoteam) team = JSON.parse(localStorage.uoteam);
  } catch (e) {}

  function safe(t) { return t.map(function (x) { return U.units[x] ? x : 'empty'; }); }
  team = safe(team);

  // ===== 漏斗统计埋点（GA4）=====
  var used = false;
  function track(eventName) {
    if (typeof gtag === 'function') {
      gtag('event', eventName, { page_path: location.pathname });
    }
  }
  function trackUse() {
    if (!used) { used = true; track('team_builder_use'); } // 北极星：首次开始组队
  }

  function render() {
    ids.forEach(function (id, i) {
      var el = document.getElementById(id), u = U.units[team[i]];
      el.innerHTML = '<label>' + id.replace('-', ' ').toUpperCase() + '</label>' +
        '<select data-index="' + i + '">' +
        Object.entries(U.units).map(function (kv) {
          return '<option value="' + kv[0] + '" ' + (kv[0] === team[i] ? 'selected' : '') + '>' + kv[1].name + '</option>';
        }).join('') +
        '</select><div class="role">' + u.className + ' · ' + u.role + '</div>';
    });
    document.querySelectorAll('select').forEach(function (x) {
      x.onchange = function (e) {
        trackUse(); // 用户第一次改动单位 = 进入"啊哈时刻"前兆
        team[+e.target.dataset.index] = e.target.value;
        render();
      };
    });
  }

  function message(s) { document.getElementById('notice').textContent = s; }

  render();
  document.getElementById('team-name').value = 'Alain Frontline';

  document.getElementById('save').onclick = function () {
    trackUse();
    track('team_builder_save');
    localStorage.uoteam = JSON.stringify(team);
    localStorage.uoteamName = document.getElementById('team-name').value;
    message('Saved locally in this browser.');
  };

  document.getElementById('share').onclick = function () {
    track('team_share'); // 裂变：生成分享链接
    var code = btoa(unescape(encodeURIComponent(JSON.stringify(team))));
    var url = location.origin + '/team-builder/?team=' + encodeURIComponent(code);
    history.replaceState({}, '', url);
    navigator.clipboard.writeText(url).then(function () {
      message('Share URL copied to clipboard.');
    }).catch(function () {
      message('Share URL generated—copy it from the address bar.');
    });
  };

  document.getElementById('reset').onclick = function () {
    team = U.defaultTeam.slice();
    render();
    message('Restored recommended formation.');
  };
})();
