/* Hướng Đến Nhập Lưu — reading site behaviour (vanilla, progressive). */
(function () {
  "use strict";

  var root = document.documentElement;
  var body = document.body;
  var base = body.dataset.base || "";

  /* ------------------------------------------------------------------ theme */

  var media = window.matchMedia("(prefers-color-scheme: dark)");

  function themeIsDark() {
    var stored = root.dataset.theme;
    if (stored === "dark") return true;
    if (stored === "light") return false;
    return media.matches;
  }

  function syncThemeButton() {
    var button = document.querySelector(".theme-toggle");
    if (!button) return;
    var dark = themeIsDark();
    button.setAttribute("aria-pressed", dark ? "true" : "false");
    button.setAttribute(
      "title",
      dark ? "Chuyển sang chế độ sáng" : "Chuyển sang chế độ tối"
    );
  }

  function toggleTheme() {
    var next = themeIsDark() ? "light" : "dark";
    root.dataset.theme = next;
    try {
      localStorage.setItem("hdb-theme", next);
    } catch (error) {
      /* storage unavailable — session-only theme is fine */
    }
    syncThemeButton();
  }

  media.addEventListener("change", function () {
    if (!root.dataset.theme) syncThemeButton();
  });

  /* --------------------------------------------------------- sidebar drawer */

  function setNav(open) {
    if (open) {
      root.dataset.nav = "open";
    } else {
      delete root.dataset.nav;
    }
    var scrim = document.querySelector(".scrim");
    if (scrim) scrim.hidden = !open;
    document.body.style.overflow = open ? "hidden" : "";
  }

  document.addEventListener("click", function (event) {
    var trigger = event.target.closest("[data-action]");
    if (!trigger) return;
    var action = trigger.dataset.action;
    if (action === "open-sidebar") setNav(true);
    if (action === "close-sidebar") setNav(false);
    if (action === "theme") toggleTheme();
    if (action === "search") openSearch();
    if (action === "search-close") closeSearch();
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && root.dataset.nav === "open") setNav(false);
    if (
      event.key === "/" &&
      !isTyping(event.target) &&
      !(event.metaKey || event.ctrlKey)
    ) {
      event.preventDefault();
      openSearch();
    }
    if (event.key.toLowerCase() === "k" && (event.metaKey || event.ctrlKey)) {
      event.preventDefault();
      openSearch();
    }
  });

  function isTyping(element) {
    if (!element) return false;
    var tag = element.tagName;
    return tag === "INPUT" || tag === "TEXTAREA" || element.isContentEditable;
  }

  /* ---------------------------------------------------------------- search */

  var indexPromise = null;
  var dialog = document.querySelector(".search-dialog");
  var input = document.getElementById("search-input");
  var results = document.getElementById("search-results");
  var activeIndex = -1;
  var currentItems = [];

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(base + "assets/search-index.json", {
        credentials: "same-origin",
      })
        .then(function (response) {
          if (!response.ok) throw new Error("search index unavailable");
          return response.json();
        })
        .then(function (data) {
          return data.entries || [];
        })
        .catch(function () {
          return [];
        });
    }
    return indexPromise;
  }

  function normalize(value) {
    return value
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d")
      .toLowerCase();
  }

  function openSearch() {
    if (!dialog) return;
    if (!dialog.open) dialog.showModal();
    setNav(false);
    loadIndex();
    if (input) {
      input.value = "";
      input.focus();
    }
    renderResults("");
  }

  function closeSearch() {
    if (dialog && dialog.open) dialog.close();
  }

  function escapeHtml(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function highlight(text, query) {
    var safe = escapeHtml(text);
    if (!query) return safe;
    var idx = normalize(text).indexOf(normalize(query));
    if (idx < 0) return safe;
    var start = text.slice(0, idx);
    var match = text.slice(idx, idx + query.length);
    var end = text.slice(idx + query.length);
    return (
      escapeHtml(start) +
      "<mark>" +
      escapeHtml(match) +
      "</mark>" +
      escapeHtml(end)
    );
  }

  function renderResults(query) {
    if (!results) return;
    var trimmed = query.trim();
    if (!trimmed) {
      results.innerHTML =
        '<p class="search-empty">Gõ tên chương, thuật ngữ hoặc câu hỏi. Gợi ý: “Nhập lưu”, “duyên khởi”, “an toàn”.</p>';
      currentItems = [];
      activeIndex = -1;
      return;
    }
    loadIndex().then(function (entries) {
      var needle = normalize(trimmed);
      var matches = [];
      for (var i = 0; i < entries.length; i += 1) {
        var entry = entries[i];
        if (entry.n.indexOf(needle) === -1) continue;
        var titleHit = normalize(entry.t).indexOf(needle) !== -1 ? 0 : 1;
        matches.push({ entry: entry, rank: titleHit });
      }
      matches.sort(function (a, b) {
        return a.rank - b.rank;
      });
      matches = matches.slice(0, 40);
      currentItems = matches;
      activeIndex = matches.length ? 0 : -1;
      if (!matches.length) {
        results.innerHTML =
          '<p class="search-empty">Không tìm thấy “' +
          escapeHtml(trimmed) +
          '”. Thử một từ ngắn hơn.</p>';
        return;
      }
      var html = "";
      matches.forEach(function (item, index) {
        var entry = item.entry;
        html +=
          '<a class="search-item' +
          (index === activeIndex ? " is-active" : "") +
          '" href="' +
          base +
          entry.p +
          "/index.html#" +
          entry.a +
          '" role="option">' +
          "<small>" +
          (entry.p.indexOf("chuong") === 0 ? "Chương" : "Mục") +
          "</small>" +
          "<strong>" +
          highlight(entry.t, trimmed) +
          "</strong>" +
          '<span>' +
          highlight(entry.d.slice(0, 160), trimmed) +
          "</span></a>";
      });
      results.innerHTML = html;
    });
  }

  function moveActive(delta) {
    if (!currentItems.length) return;
    activeIndex = (activeIndex + delta + currentItems.length) % currentItems.length;
    var nodes = results.querySelectorAll(".search-item");
    nodes.forEach(function (node, index) {
      node.classList.toggle("is-active", index === activeIndex);
    });
    if (nodes[activeIndex]) {
      nodes[activeIndex].scrollIntoView({ block: "nearest" });
    }
  }

  if (input) {
    var debounce = null;
    input.addEventListener("input", function () {
      window.clearTimeout(debounce);
      debounce = window.setTimeout(function () {
        renderResults(input.value);
      }, 90);
    });
    input.addEventListener("keydown", function (event) {
      if (event.key === "ArrowDown") {
        event.preventDefault();
        moveActive(1);
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        moveActive(-1);
      } else if (event.key === "Enter") {
        event.preventDefault();
        var node = results.querySelectorAll(".search-item")[activeIndex];
        if (node) node.click();
      }
    });
  }

  if (dialog) {
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) closeSearch();
    });
  }

  /* ------------------------------------------------------- active navigation */

  function currentSlug() {
    var path = window.location.pathname.replace(/index\.html$/, "");
    var parts = path.split("/").filter(Boolean);
    return parts.length ? parts[parts.length - 1] : "";
  }

  function markActiveNav(slug) {
    if (!slug) return;
    var link = document.querySelector('.toc-link[data-slug="' + slug + '"]');
    if (!link) return;
    link.classList.add("is-active");
    link.setAttribute("aria-current", "page");
    var details = link.closest("details");
    if (details) details.open = true;
    var parent = link.closest(".toc-group");
    while (parent) {
      var inner = parent.querySelector(":scope > details");
      if (inner) inner.open = true;
      parent = parent.parentElement.closest(".toc-group");
    }
    var group = link.closest(".toc-group");
    if (group) group.open = true;
  }

  markActiveNav(currentSlug());

  /* -------------------------------------------------------- scroll position */

  var progressBar = document.getElementById("progress-bar");
  var headings = Array.prototype.slice.call(
    document.querySelectorAll("main .prose h2[id], main .prose h3[id], main .prose h4[id], main .prose .faq-card h1[id]")
  );
  var ptocLinks = Array.prototype.slice.call(
    document.querySelectorAll(".ptoc-item a")
  );
  var ticking = false;

  function updateProgress() {
    var doc = document.documentElement;
    var scrollable = doc.scrollHeight - doc.clientHeight;
    var ratio = scrollable > 0 ? doc.scrollTop / scrollable : 0;
    if (progressBar) {
      progressBar.style.width = (ratio * 100).toFixed(2) + "%";
    }
    updateScrollSpy();
    ticking = false;
  }

  function updateScrollSpy() {
    if (!ptocLinks.length) return;
    var threshold = 140;
    var current = null;
    for (var i = 0; i < headings.length; i += 1) {
      if (headings[i].getBoundingClientRect().top - threshold <= 0) {
        current = headings[i].id;
      } else {
        break;
      }
    }
    ptocLinks.forEach(function (link) {
      link.classList.toggle("is-active", link.hash === "#" + current);
    });
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateProgress);
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  updateProgress();

  /* ------------------------------------------------------------- reveal-in */

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var revealSelector =
    ".practice-card, .caution, .source-line, .decision-node, .concept-node, .day-card, .reference-item";
  if (!reduceMotion && "IntersectionObserver" in window) {
    var candidates = document.querySelectorAll(revealSelector);
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    candidates.forEach(function (element, index) {
      element.classList.add("reveal");
      element.style.transitionDelay = Math.min(index % 4, 3) * 40 + "ms";
      observer.observe(element);
    });
  }

  /* Prevent summary links from toggling the disclosure on desktop. */
  document.querySelectorAll(".toc-group summary a, .toc-group summary span").forEach(
    function (element) {
      element.addEventListener("click", function (event) {
        if (event.detail !== 0) event.stopPropagation();
      });
    }
  );

  syncThemeButton();
})();
