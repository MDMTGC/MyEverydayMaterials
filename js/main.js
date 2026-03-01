/* ═══════════════════════════════════════════════════════════════════════════
   Everyday Materials — Main JS
   Theme toggle, search/filter, sticky header, back-to-top
   No external dependencies — pure vanilla JS
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var THEME_KEY = 'mem-theme';

  // ─── Theme System ──────────────────────────────────────────────────────────

  function getPreferredTheme() {
    var saved = localStorage.getItem(THEME_KEY);
    if (saved === 'dark' || saved === 'light') return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
  }

  // Apply immediately (before DOMContentLoaded) to minimise flash
  applyTheme(getPreferredTheme());

  // Respect system changes while the page is open
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    // Only auto-switch if the user hasn't manually set a preference this session
    if (!localStorage.getItem(THEME_KEY)) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  // ─── Inject Theme Toggle Button ────────────────────────────────────────────

  function injectThemeToggle() {
    var btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Toggle dark mode');
    btn.innerHTML =
      '<svg class="icon-sun" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>' +
      '<svg class="icon-moon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

    btn.addEventListener('click', function () {
      var current = document.documentElement.getAttribute('data-theme') || 'light';
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });

    // Place inside .header-right if available, otherwise append to header
    var target = document.querySelector('.header-right') || document.querySelector('header');
    if (target) {
      target.appendChild(btn);
      return;
    }

    // Homepage: no header — float inside the hero
    var hero = document.querySelector('.hero');
    if (hero) {
      btn.classList.add('theme-toggle--hero');
      hero.appendChild(btn);
    }
  }

  // ─── Sticky Header Scroll Effect ──────────────────────────────────────────

  function initStickyHeader() {
    var header = document.querySelector('header');
    if (!header) return;

    function onScroll() {
      if (window.scrollY > 10) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // set initial state
  }

  // ─── Back to Top ──────────────────────────────────────────────────────────

  function initBackToTop() {
    // Only on article pages
    if (!document.querySelector('article')) return;

    var btn = document.createElement('button');
    btn.className = 'back-to-top';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Back to top');
    btn.title = 'Back to top';
    btn.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>';

    document.body.appendChild(btn);

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    function onScroll() {
      if (window.scrollY > 400) {
        btn.classList.add('is-visible');
      } else {
        btn.classList.remove('is-visible');
      }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ─── Search / Filter ──────────────────────────────────────────────────────

  function initSearchFilter() {
    var grid = document.querySelector('.connection-grid');
    if (!grid) return;

    // Don't inject search on article pages (they have a small "Explore" hub)
    if (document.querySelector('article')) return;

    var cards = grid.querySelectorAll('.connect-link');
    if (cards.length < 5) return;

    // Build search bar
    var wrapper = document.createElement('div');
    wrapper.className = 'search-bar';
    wrapper.innerHTML =
      '<svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>' +
      '<input class="search-input" type="search" placeholder="Filter materials\u2026" aria-label="Filter materials" autocomplete="off" spellcheck="false" />' +
      '<button class="search-clear" type="button" aria-label="Clear search" hidden>\u00d7</button>';

    // Insert above the grid
    var hub = grid.closest('.connection-hub');
    if (hub) {
      hub.insertBefore(wrapper, grid);
    } else {
      grid.parentNode.insertBefore(wrapper, grid);
    }

    var input = wrapper.querySelector('.search-input');
    var clearBtn = wrapper.querySelector('.search-clear');

    // "No results" message
    var noResults = document.createElement('p');
    noResults.className = 'search-empty';
    noResults.textContent = 'No materials found.';
    noResults.hidden = true;
    grid.parentNode.insertBefore(noResults, grid.nextSibling);

    function filter(query) {
      var q = query.toLowerCase().trim();
      var visible = 0;

      for (var i = 0; i < cards.length; i++) {
        var text = cards[i].textContent.toLowerCase();
        var match = !q || text.indexOf(q) !== -1;
        cards[i].hidden = !match;
        if (match) visible++;
      }

      noResults.hidden = visible > 0;
      clearBtn.hidden = !q;
    }

    input.addEventListener('input', function () {
      filter(this.value);
    });

    clearBtn.addEventListener('click', function () {
      input.value = '';
      filter('');
      input.focus();
    });

    // Keyboard shortcut: press "/" to focus search (common UX pattern)
    document.addEventListener('keydown', function (e) {
      if (
        e.key === '/' &&
        document.activeElement !== input &&
        document.activeElement.tagName !== 'INPUT' &&
        document.activeElement.tagName !== 'TEXTAREA'
      ) {
        e.preventDefault();
        input.focus();
      }
    });
  }

  // ─── Boot ─────────────────────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', function () {
    injectThemeToggle();
    initStickyHeader();
    initBackToTop();
    initSearchFilter();
  });
})();
