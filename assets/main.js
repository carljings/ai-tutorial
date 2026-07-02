/* AI 全栈教学 · 交互脚本 v3
 * 改进：侧边栏滚动位置记忆/恢复 + 交互优化
 */
(function () {
  'use strict';

  /* ========== 主题切换 ========== */
  var THEME_KEY = 'ai-tutorial-theme';
  function getTheme() { return localStorage.getItem(THEME_KEY) || 'light'; }
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem(THEME_KEY, t);
    var ic = document.querySelector('.theme-toggle .icon');
    var lb = document.querySelector('.theme-toggle .label');
    if (ic) ic.textContent = t === 'dark' ? '\u2600' : '\u{1F319}';
    if (lb) lb.textContent = t === 'dark' ? '\u4eae\u8272' : '\u6697\u8272';
  }
  // 立即应用主题（防闪烁）
  applyTheme(getTheme());

  /* ========== 注入顶部栏 ========== */
  var topbar = document.createElement('div');
  topbar.className = 'topbar';
  topbar.innerHTML =
    '<button class="theme-toggle" id="themeBtn" title="\u5207\u6362\u4eae\u8272/\u6697\u8272">' +
    '<span class="icon">\u{1F319}</span><span class="label">\u6697\u8272</span></button>';
  var layout = document.querySelector('.layout');
  if (layout && layout.parentNode) {
    layout.parentNode.insertBefore(topbar, layout);
  }
  applyTheme(getTheme()); // 更新按钮文字

  document.addEventListener('click', function (e) {
    if (e.target.closest('#themeBtn')) {
      applyTheme(getTheme() === 'dark' ? 'light' : 'dark');
    }
  });

  /* ========== 侧边栏滚动位置记忆/恢复（无动画） ========== */
  var SIDEBAR_SCROLL_KEY = 'ai-tutorial-sidebar-scroll';
  var sidebar = document.querySelector('.sidebar');

  if (sidebar) {
    // 页面加载时：静默恢复，无任何动画
    sidebar.style.scrollBehavior = 'auto';
    var saved = parseInt(localStorage.getItem(SIDEBAR_SCROLL_KEY) || '0', 10);
    sidebar.scrollTop = saved;

    // 滚动时保存位置（节流 150ms）
    var scrollTimer = null;
    sidebar.addEventListener('scroll', function () {
      if (scrollTimer) clearTimeout(scrollTimer);
      scrollTimer = setTimeout(function () {
        localStorage.setItem(SIDEBAR_SCROLL_KEY, sidebar.scrollTop.toString());
      }, 150);
    }, { passive: true });

    // 点击导航链接前保存当前位置
    sidebar.addEventListener('click', function (e) {
      var link = e.target.closest('a');
      if (link) {
        localStorage.setItem(SIDEBAR_SCROLL_KEY, sidebar.scrollTop.toString());
      }
    }, { passive: true });
  }

  /* ========== 阅读进度条 ========== */
  var bar = document.createElement('div');
  bar.className = 'progress';
  bar.style.width = '0%';
  document.body.appendChild(bar);

  var scrollTicking = false;
  function updateProgress() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var sc = max > 0 ? h.scrollTop / max : 0;
    bar.style.width = (sc * 100) + '%';
    scrollTicking = false;
  }
  window.addEventListener('scroll', function () {
    if (!scrollTicking) {
      requestAnimationFrame(updateProgress);
      scrollTicking = true;
    }
  }, { passive: true });
  updateProgress();

  /* ========== 回到顶部按钮 ========== */
  var toTop = document.createElement('button');
  toTop.className = 'back-to-top';
  toTop.innerHTML = '\u2191';
  toTop.title = '\u56de\u5230\u9876\u90e8';
  toTop.setAttribute('aria-label', '\u56de\u5230\u9876\u90e8');
  document.body.appendChild(toTop);

  toTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // 滚动超过 500px 才显示
  var toTopTicking = false;
  function updateToTop() {
    toTop.classList.toggle('visible', window.scrollY > 500);
    toTopTicking = false;
  }
  window.addEventListener('scroll', function () {
    if (!toTopTicking) {
      requestAnimationFrame(updateToTop);
      toTopTicking = true;
    }
  }, { passive: true });

  /* ========== 键盘快捷键 ========== */
  document.addEventListener('keydown', function (e) {
    // 忽略输入框中的按键
    if (e.target.matches('input, textarea, [contenteditable]')) return;

    // t: 切换主题
    if (e.key === 't' || e.key === 'T') {
      applyTheme(getTheme() === 'dark' ? 'light' : 'dark');
    }
    // ← : 上一章
    var prevLink = document.querySelector('.chapter-nav a:not(.next)');
    if (e.key === 'ArrowLeft' && prevLink && !e.metaKey && !e.ctrlKey) {
      // 保存侧边栏位置再跳转
      if (sidebar) localStorage.setItem(SIDEBAR_SCROLL_KEY, sidebar.scrollTop.toString());
      window.location.href = prevLink.href;
    }
    // → : 下一章
    var nextLink = document.querySelector('.chapter-nav a.next');
    if (e.key === 'ArrowRight' && nextLink && !e.metaKey && !e.ctrlKey) {
      if (sidebar) localStorage.setItem(SIDEBAR_SCROLL_KEY, sidebar.scrollTop.toString());
      window.location.href = nextLink.href;
    }
  });
})();
