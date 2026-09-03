/* ═══════════════════════════════════════════════════════════════════════════
   Everyday Materials — Main JS
   Theme toggle, search/filter, sticky header, back-to-top
   No external dependencies — pure vanilla JS
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  var THEME_KEY = 'mem-theme';

  // ─── HTML Escaping ─────────────────────────────────────────────────────────
  // search_index.json is generated at build time from our own trusted content,
  // not user input, so this isn't exploitable today -- but escaping before any
  // string gets joined into innerHTML is cheap, permanent insurance against a
  // future data source (a scraped field, a user-submitted correction) landing
  // in this same rendering path unsanitized.

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

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

    // Keyboard shortcuts
    document.addEventListener('keydown', function (e) {
      // "/" to focus search (common UX pattern)
      if (
        e.key === '/' &&
        document.activeElement !== input &&
        document.activeElement.tagName !== 'INPUT' &&
        document.activeElement.tagName !== 'TEXTAREA'
      ) {
        e.preventDefault();
        input.focus();
      }

      // Escape to clear search and blur
      if (e.key === 'Escape' && document.activeElement === input) {
        input.value = '';
        filter('');
        input.blur();
      }
    });
  }

  // ─── Mobile Navigation ──────────────────────────────────────────────────

  function initMobileNav() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.getElementById('site-nav');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      toggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });

    // Close nav when clicking a link (mobile)
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open menu');
      }
    });
  }

  // ─── Articles Dropdown ─────────────────────────────────────────────────

  function initDropdown() {
    var dropdown = document.getElementById('nav-dropdown');
    if (!dropdown) return;

    var btn = dropdown.querySelector('.site-nav-dropdown-toggle');
    if (!btn) return;

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = dropdown.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close on click outside
    document.addEventListener('click', function (e) {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && dropdown.classList.contains('is-open')) {
        dropdown.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  }

  // ─── Global Site Search ──────────────────────────────────────────────────

  function initGlobalSearch() {
    var searchInput = document.getElementById('header-search-input');
    var clearBtn = document.getElementById('header-search-clear');
    var backdrop = document.getElementById('search-backdrop');
    var dropdown = document.getElementById('search-dropdown');
    var resultsList = document.getElementById('search-results-list');
    var resultsCount = document.getElementById('search-results-count');

    if (!searchInput || !dropdown || !resultsList) return;

    var searchIndex = null;
    var isLoading = false;
    var selectedIndex = -1;

    // Load search index JSON dynamically
    function loadSearchIndex() {
      if (searchIndex || isLoading) return;
      isLoading = true;
      
      // Update count/placeholder while loading
      resultsList.innerHTML = '<div class="search-results-placeholder">Loading search index...</div>';

      fetch('/search_index.json')
        .then(function (response) {
          if (!response.ok) throw new Error('Search index failed to load');
          return response.json();
        })
        .then(function (data) {
          searchIndex = data;
          isLoading = false;
          resultsList.innerHTML = '<div class="search-results-placeholder">Type to search materials by name, category, or safety verdict...</div>';
          // If search input already has text, trigger immediate search
          if (searchInput.value.trim()) {
            performSearch(searchInput.value);
          }
        })
        .catch(function (error) {
          console.error(error);
          resultsList.innerHTML = '<div class="search-results-placeholder error">Failed to load search index. Please try again.</div>';
          isLoading = false;
        });
    }

    function showSearch() {
      backdrop.classList.add('is-visible');
      dropdown.classList.add('is-visible');
      backdrop.removeAttribute('hidden');
      dropdown.removeAttribute('hidden');
    }

    function hideSearch() {
      backdrop.classList.remove('is-visible');
      dropdown.classList.remove('is-visible');
      backdrop.setAttribute('hidden', '');
      dropdown.setAttribute('hidden', '');
      selectedIndex = -1;
    }

    function performSearch(query) {
      if (!searchIndex) return;

      var q = query.toLowerCase().trim();
      if (!q) {
        resultsList.innerHTML = '<div class="search-results-placeholder">Type to search materials by name, category, or safety verdict...</div>';
        resultsCount.textContent = '0 matches';
        clearBtn.hidden = true;
        return;
      }

      clearBtn.hidden = false;

      // Filter and rank results
      var matches = [];
      for (var i = 0; i < searchIndex.length; i++) {
        var item = searchIndex[i];
        var titleLower = item.title.toLowerCase();
        var descLower = item.description.toLowerCase();
        var verdictLower = item.verdict.replace('verdict-', '').toLowerCase();
        var catNameLower = item.category_name.toLowerCase();

        var score = 0;
        
        // Exact matches and starting matches get higher scores
        if (titleLower === q) {
          score += 100;
        } else if (titleLower.indexOf(q) === 0) {
          score += 50;
        } else if (titleLower.indexOf(q) !== -1) {
          score += 25;
        }

        if (descLower.indexOf(q) !== -1) {
          score += 5;
        }
        
        if (verdictLower === q) {
          score += 15;
        }

        if (catNameLower.indexOf(q) !== -1) {
          score += 10;
        }

        if (score > 0) {
          item._score = score;
          matches.push(item);
        }
      }

      // Sort by score (descending) then title (ascending)
      matches.sort(function (a, b) {
        if (b._score !== a._score) {
          return b._score - a._score;
        }
        return a.title.localeCompare(b.title);
      });

      // Render search result items
      if (matches.length === 0) {
        resultsList.innerHTML = '<div class="search-results-empty">No matching materials found. Try searching for "safe", "BPA", or a category.</div>';
        resultsCount.textContent = '0 matches';
        return;
      }

      resultsCount.textContent = matches.length + (matches.length === 1 ? ' match' : ' matches');

      var html = '';
      for (var j = 0; j < matches.length; j++) {
        var match = matches[j];
        var badgeCls = match.verdict.replace('verdict-', '');
        var badgeTxt = badgeCls.toUpperCase();

        html += '<a href="' + escapeHtml(match.url) + '" class="search-result-item" data-index="' + j + '">' +
          '  <div class="search-result-meta">' +
          '    <span class="search-result-category">' + escapeHtml(match.category_name) + '</span>' +
          '    <span class="status-badge status-badge--' + badgeCls + '">' + badgeTxt + '</span>' +
          '  </div>' +
          '  <div class="search-result-title">' + escapeHtml(match.title) + '</div>' +
          '  <div class="search-result-desc">' + escapeHtml(match.description) + '</div>' +
          '</a>';
      }
      resultsList.innerHTML = html;
      selectedIndex = -1;
    }

    // Lazy load index on focus
    searchInput.addEventListener('focus', function () {
      loadSearchIndex();
      showSearch();
    });

    searchInput.addEventListener('input', function () {
      performSearch(this.value);
    });

    clearBtn.addEventListener('click', function () {
      searchInput.value = '';
      performSearch('');
      searchInput.focus();
    });

    backdrop.addEventListener('click', function () {
      hideSearch();
    });

    // Handle Keyboard Navigation inside search dropdown
    document.addEventListener('keydown', function (e) {
      // Allow user to press '/' to focus search input if not inside input/textarea
      if (
        e.key === '/' &&
        document.activeElement !== searchInput &&
        document.activeElement.tagName !== 'INPUT' &&
        document.activeElement.tagName !== 'TEXTAREA'
      ) {
        e.preventDefault();
        searchInput.focus();
        return;
      }

      if (!dropdown.classList.contains('is-visible')) return;

      var items = resultsList.querySelectorAll('.search-result-item');

      if (e.key === 'Escape') {
        hideSearch();
        searchInput.blur();
        e.preventDefault();
      } else if (e.key === 'ArrowDown') {
        if (items.length > 0) {
          if (selectedIndex >= 0) {
            items[selectedIndex].classList.remove('is-selected');
          }
          selectedIndex = (selectedIndex + 1) % items.length;
          items[selectedIndex].classList.add('is-selected');
          items[selectedIndex].scrollIntoView({ block: 'nearest' });
        }
        e.preventDefault();
      } else if (e.key === 'ArrowUp') {
        if (items.length > 0) {
          if (selectedIndex >= 0) {
            items[selectedIndex].classList.remove('is-selected');
          }
          selectedIndex = selectedIndex - 1;
          if (selectedIndex < 0) {
            selectedIndex = items.length - 1;
          }
          items[selectedIndex].classList.add('is-selected');
          items[selectedIndex].scrollIntoView({ block: 'nearest' });
        }
        e.preventDefault();
      } else if (e.key === 'Enter') {
        if (selectedIndex >= 0 && items[selectedIndex]) {
          window.location.href = items[selectedIndex].getAttribute('href');
          e.preventDefault();
        }
      }
    });
  }

  // ─── Boot ─────────────────────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', function () {
    injectThemeToggle();
    initStickyHeader();
    initMobileNav();
    initDropdown();
    initBackToTop();
    initSearchFilter();
    initGlobalSearch();
  });
})();
