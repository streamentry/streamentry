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
    document.querySelectorAll(".toc-link.is-active").forEach(function (node) {
      node.classList.remove("is-active");
      node.removeAttribute("aria-current");
    });
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
  var headings = [];
  var ptocLinks = [];
  var ticking = false;

  function refreshScrollSpyTargets() {
    headings = Array.prototype.slice.call(
      document.querySelectorAll(
        "main .prose h2[id], main .prose h3[id], main .prose h4[id], main .prose .faq-card h1[id]"
      )
    );
    ptocLinks = Array.prototype.slice.call(
      document.querySelectorAll(".ptoc-item a")
    );
  }

  refreshScrollSpyTargets();

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
  var revealObserver = null;
  if (!reduceMotion && "IntersectionObserver" in window) {
    revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
  }

  function observeRevealTargets(scope) {
    if (!revealObserver) return;
    var candidates = (scope || document).querySelectorAll(revealSelector);
    candidates.forEach(function (element, index) {
      if (element.classList.contains("is-in")) return;
      element.classList.add("reveal");
      element.style.transitionDelay = Math.min(index % 4, 3) * 40 + "ms";
      revealObserver.observe(element);
    });
  }

  observeRevealTargets(document);

  /* Prevent summary links from toggling the disclosure on desktop. */
  document.querySelectorAll(".toc-group summary a, .toc-group summary span").forEach(
    function (element) {
      element.addEventListener("click", function (event) {
        if (event.detail !== 0) event.stopPropagation();
      });
    }
  );

  /* ----------------------------------------------------------- audio player */

  var SPEEDS = [1, 1.25, 1.5, 0.8];
  var SPEED_KEY = "hdb-audio-speed";
  var pageSyncController = null;

  function formatTime(seconds) {
    if (!isFinite(seconds) || seconds < 0) return "--:--";
    var total = Math.floor(seconds);
    var hrs = Math.floor(total / 3600);
    var mins = Math.floor((total % 3600) / 60);
    var secs = total % 60;
    var mm = mins < 10 ? "0" + mins : String(mins);
    var ss = secs < 10 ? "0" + secs : String(secs);
    if (hrs > 0) {
      return hrs + ":" + mm + ":" + ss;
    }
    return mm + ":" + ss;
  }

  function readStoredSpeed() {
    try {
      var val = parseFloat(localStorage.getItem(SPEED_KEY) || "1");
      if (SPEEDS.indexOf(val) !== -1) return val;
    } catch (error) {
      /* ignore storage errors */
    }
    return 1;
  }

  function saveStoredSpeed(speed) {
    try {
      localStorage.setItem(SPEED_KEY, String(speed));
    } catch (error) {
      /* ignore storage errors */
    }
  }

  function formatSpeed(speed) {
    return (speed % 1 === 0 ? speed.toFixed(1) : String(speed)) + "×";
  }

  function replaceProsePreservingPlayer(currentArticle, nextArticle, playerEl) {
    var nextPlayer = nextArticle.querySelector("[data-audio-player]");
    var beforeNodes = [];
    var afterNodes = [];
    var seenPlayer = false;

    Array.prototype.slice.call(nextArticle.childNodes).forEach(function (node) {
      if (nextPlayer && (node === nextPlayer || node.contains(nextPlayer))) {
        seenPlayer = true;
        return;
      }
      if (!seenPlayer) {
        beforeNodes.push(document.importNode(node, true));
      } else {
        afterNodes.push(document.importNode(node, true));
      }
    });

    Array.prototype.slice.call(currentArticle.childNodes).forEach(function (node) {
      if (node !== playerEl) {
        currentArticle.removeChild(node);
      }
    });

    beforeNodes.forEach(function (node) {
      currentArticle.insertBefore(node, playerEl);
    });
    afterNodes.forEach(function (node) {
      currentArticle.appendChild(node);
    });
  }

  function syncReaderPageToSlug(slug, pushHistory) {
    if (!slug || body.classList.contains("page-landing")) return;
    if (currentSlug() === slug && pushHistory !== false) return;

    var targetUrl = base + slug + "/index.html";
    if (pageSyncController && typeof pageSyncController.abort === "function") {
      pageSyncController.abort();
    }
    if ("AbortController" in window) {
      pageSyncController = new AbortController();
    }

    fetch(targetUrl, {
      credentials: "same-origin",
      signal: pageSyncController ? pageSyncController.signal : undefined,
    })
      .then(function (response) {
        if (!response.ok) throw new Error("Failed to load chapter page");
        return response.text();
      })
      .then(function (htmlText) {
        var parser = new DOMParser();
        var nextDoc = parser.parseFromString(htmlText, "text/html");
        var currentArticle = document.querySelector("main .prose");
        var nextArticle = nextDoc.querySelector("main .prose");
        var playerEl = document.querySelector("[data-audio-player]");
        if (!currentArticle || !nextArticle || !playerEl) return;

        replaceProsePreservingPlayer(currentArticle, nextArticle, playerEl);

        if (nextDoc.title) {
          document.title = nextDoc.title;
        }
        if (nextDoc.body && nextDoc.body.className) {
          body.className = nextDoc.body.className;
        }
        var topbarTitle = document.querySelector(".topbar-title");
        var nextTopbarTitle = nextDoc.querySelector(".topbar-title");
        if (topbarTitle && nextTopbarTitle) {
          topbarTitle.textContent = nextTopbarTitle.textContent;
        }

        var mainColumn = document.querySelector(".main-column");
        var currentPager = document.querySelector(".pager");
        var nextPager = nextDoc.querySelector(".pager");
        if (currentPager && nextPager) {
          currentPager.replaceWith(document.importNode(nextPager, true));
        } else if (currentPager && !nextPager) {
          currentPager.remove();
        } else if (!currentPager && nextPager && mainColumn) {
          var foot = mainColumn.querySelector(".site-foot");
          mainColumn.insertBefore(document.importNode(nextPager, true), foot);
        }

        var layout = document.querySelector(".layout");
        var currentPtoc = document.querySelector(".page-toc");
        var nextPtoc = nextDoc.querySelector(".page-toc");
        if (currentPtoc && nextPtoc) {
          currentPtoc.replaceWith(document.importNode(nextPtoc, true));
        } else if (currentPtoc && !nextPtoc) {
          currentPtoc.remove();
        } else if (!currentPtoc && nextPtoc && layout) {
          layout.appendChild(document.importNode(nextPtoc, true));
        }

        if (pushHistory !== false && window.history && window.history.pushState) {
          window.history.pushState({ slug: slug }, document.title, targetUrl);
        }

        markActiveNav(slug);
        refreshScrollSpyTargets();
        observeRevealTargets(currentArticle);
        window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
        updateProgress();
      })
      .catch(function (error) {
        if (error && error.name === "AbortError") return;
      });
  }

  function initAudioPlayer(playerEl) {
    var audio = playerEl.querySelector("[data-audio-element]");
    if (!audio) return null;

    var playBtn = playerEl.querySelector("[data-play-toggle]");
    var playIcon = playerEl.querySelector("[data-play-icon]");
    var pauseIcon = playerEl.querySelector("[data-pause-icon]");
    var prevBtn = playerEl.querySelector("[data-prev-track]");
    var nextBtn = playerEl.querySelector("[data-next-track]");
    var skipBackBtn = playerEl.querySelector("[data-skip-back]");
    var skipFwdBtn = playerEl.querySelector("[data-skip-forward]");
    var seekBar = playerEl.querySelector("[data-seek-bar]");
    var curTimeEl = playerEl.querySelector("[data-current-time]");
    var durTimeEl = playerEl.querySelector("[data-duration]");
    var speedBtn = playerEl.querySelector("[data-speed-btn]");
    var speedLabel = playerEl.querySelector("[data-speed-label]");
    var activeTitleEl = playerEl.querySelector("[data-active-title]");
    var downloadLink = playerEl.querySelector("[data-download-link]");
    var downloadSize = playerEl.querySelector("[data-download-size]");
    var playAllBtn = playerEl.querySelector("[data-player-play-all]");

    var playlist = [];
    try {
      playlist = JSON.parse(playerEl.getAttribute("data-playlist") || "[]");
    } catch (error) {
      playlist = [];
    }

    var activeSlug = playerEl.getAttribute("data-slug") || "";
    var currentIndex = 0;
    for (var i = 0; i < playlist.length; i += 1) {
      if (playlist[i].slug === activeSlug) {
        currentIndex = i;
        break;
      }
    }

    var currentSpeed = readStoredSpeed();
    audio.playbackRate = currentSpeed;
    if (speedLabel) speedLabel.textContent = formatSpeed(currentSpeed);

    var isScrubbing = false;
    var listeners = [];

    function notifyCards() {
      var item = playlist[currentIndex];
      var slug = item ? item.slug : activeSlug;
      var playing = !audio.paused && !audio.ended;
      listeners.forEach(function (fn) {
        fn(slug, playing, audio.currentTime > 0 && !audio.ended);
      });
    }

    function setPlayingState(playing) {
      playerEl.classList.toggle("is-playing", playing);
      if (playIcon) playIcon.classList.toggle("is-hidden", playing);
      if (pauseIcon) pauseIcon.classList.toggle("is-hidden", !playing);
      if (playBtn) {
        playBtn.setAttribute(
          "aria-label",
          playing ? "Tạm dừng sách nói" : "Phát sách nói"
        );
      }
      notifyCards();
    }

    function updateNavButtons() {
      if (prevBtn) prevBtn.disabled = currentIndex <= 0;
      if (nextBtn) nextBtn.disabled = currentIndex >= playlist.length - 1;
    }

    function updateMediaSession() {
      if (!("mediaSession" in navigator)) return;
      var item = playlist[currentIndex];
      var title = item
        ? item.label
          ? item.label + " — " + item.title
          : item.title
        : playerEl.getAttribute("data-title") || document.title;
      var author = playerEl.getAttribute("data-author") || "";
      var book = playerEl.getAttribute("data-book") || "";
      try {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: title,
          artist: author,
          album: book,
        });
        navigator.mediaSession.setActionHandler("play", function () {
          audio.play().catch(function () {});
        });
        navigator.mediaSession.setActionHandler("pause", function () {
          audio.pause();
        });
        navigator.mediaSession.setActionHandler("seekbackward", function () {
          audio.currentTime = Math.max(0, (audio.currentTime || 0) - 15);
        });
        navigator.mediaSession.setActionHandler("seekforward", function () {
          if (isFinite(audio.duration)) {
            audio.currentTime = Math.min(audio.duration, (audio.currentTime || 0) + 15);
          } else {
            audio.currentTime = (audio.currentTime || 0) + 15;
          }
        });
        navigator.mediaSession.setActionHandler(
          "previoustrack",
          currentIndex > 0
            ? function () {
                playTrackByIndex(currentIndex - 1, true);
              }
            : null
        );
        navigator.mediaSession.setActionHandler(
          "nexttrack",
          currentIndex < playlist.length - 1
            ? function () {
                playTrackByIndex(currentIndex + 1, true);
              }
            : null
        );
      } catch (error) {
        /* ignore unsupported MediaSession actions */
      }
    }

    function applyTrackMetadata(item) {
      if (!item) return;
      activeSlug = item.slug;
      playerEl.setAttribute("data-slug", item.slug);
      playerEl.setAttribute("data-title", item.title);
      var displayTitle = item.label ? item.label + " — " + item.title : item.title;
      if (activeTitleEl) {
        activeTitleEl.textContent = displayTitle;
        activeTitleEl.setAttribute("title", displayTitle);
      }
      var audioUrl = base + "assets/audio/" + item.filename;
      if (downloadLink) {
        downloadLink.setAttribute("href", audioUrl);
        if (item.downloadName) {
          downloadLink.setAttribute("download", item.downloadName);
        }
      }
      if (downloadSize && item.sizeLabel) {
        downloadSize.textContent = "(" + item.sizeLabel + ")";
      }
      updateNavButtons();
      updateMediaSession();
      notifyCards();
    }

    function playTrackByIndex(index, autoPlay, syncOptions) {
      if (index < 0 || index >= playlist.length) return;
      var item = playlist[index];
      var changed = index !== currentIndex || activeSlug !== item.slug;
      currentIndex = index;
      applyTrackMetadata(item);

      var targetSrc = base + "assets/audio/" + item.filename;
      if (changed || audio.getAttribute("src") !== targetSrc) {
        audio.setAttribute("src", targetSrc);
        audio.load();
        if (curTimeEl) curTimeEl.textContent = "00:00";
        if (durTimeEl) durTimeEl.textContent = "--:--";
        if (seekBar) seekBar.value = "0";
      }

      audio.playbackRate = currentSpeed;

      var shouldSyncPage = !syncOptions || syncOptions.syncPage !== false;
      if (shouldSyncPage && !body.classList.contains("page-landing")) {
        syncReaderPageToSlug(item.slug, !syncOptions || syncOptions.pushHistory !== false);
      }

      if (autoPlay) {
        var playPromise = audio.play();
        if (playPromise && typeof playPromise.catch === "function") {
          playPromise.catch(function () {
            setPlayingState(false);
          });
        }
      } else {
        setPlayingState(false);
      }
    }

    function togglePlay() {
      if (audio.paused || audio.ended) {
        audio.playbackRate = currentSpeed;
        var p = audio.play();
        if (p && typeof p.catch === "function") {
          p.catch(function () {
            setPlayingState(false);
          });
        }
      } else {
        audio.pause();
      }
    }

    if (playBtn) {
      playBtn.addEventListener("click", togglePlay);
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        if (audio.currentTime > 5) {
          audio.currentTime = 0;
          return;
        }
        if (currentIndex > 0) {
          playTrackByIndex(currentIndex - 1, true);
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        if (currentIndex < playlist.length - 1) {
          playTrackByIndex(currentIndex + 1, true);
        }
      });
    }

    if (skipBackBtn) {
      skipBackBtn.addEventListener("click", function () {
        audio.currentTime = Math.max(0, (audio.currentTime || 0) - 15);
      });
    }

    if (skipFwdBtn) {
      skipFwdBtn.addEventListener("click", function () {
        if (isFinite(audio.duration)) {
          audio.currentTime = Math.min(audio.duration, (audio.currentTime || 0) + 15);
        } else {
          audio.currentTime = (audio.currentTime || 0) + 15;
        }
      });
    }

    if (speedBtn) {
      speedBtn.addEventListener("click", function () {
        var idx = SPEEDS.indexOf(currentSpeed);
        currentSpeed = SPEEDS[(idx + 1) % SPEEDS.length];
        audio.playbackRate = currentSpeed;
        if (speedLabel) speedLabel.textContent = formatSpeed(currentSpeed);
        saveStoredSpeed(currentSpeed);
      });
    }

    if (playAllBtn) {
      playAllBtn.addEventListener("click", function () {
        playTrackByIndex(0, true);
      });
    }

    if (seekBar) {
      seekBar.addEventListener("input", function () {
        isScrubbing = true;
        if (isFinite(audio.duration) && audio.duration > 0) {
          var target = (parseFloat(seekBar.value) / 100) * audio.duration;
          if (curTimeEl) curTimeEl.textContent = formatTime(target);
        }
      });
      seekBar.addEventListener("change", function () {
        if (isFinite(audio.duration) && audio.duration > 0) {
          audio.currentTime = (parseFloat(seekBar.value) / 100) * audio.duration;
        }
        isScrubbing = false;
      });
    }

    audio.addEventListener("loadedmetadata", function () {
      audio.playbackRate = currentSpeed;
      if (durTimeEl) durTimeEl.textContent = formatTime(audio.duration);
      updateMediaSession();
    });

    audio.addEventListener("durationchange", function () {
      if (durTimeEl && isFinite(audio.duration)) {
        durTimeEl.textContent = formatTime(audio.duration);
      }
    });

    audio.addEventListener("timeupdate", function () {
      if (!isScrubbing) {
        if (curTimeEl) curTimeEl.textContent = formatTime(audio.currentTime);
        if (seekBar && isFinite(audio.duration) && audio.duration > 0) {
          seekBar.value = ((audio.currentTime / audio.duration) * 100).toFixed(2);
        }
      }
    });

    audio.addEventListener("play", function () {
      audio.playbackRate = currentSpeed;
      setPlayingState(true);
      updateMediaSession();
    });

    audio.addEventListener("pause", function () {
      if (!audio.ended) {
        setPlayingState(false);
      }
    });

    audio.addEventListener("ended", function () {
      if (currentIndex >= 0 && currentIndex + 1 < playlist.length) {
        playTrackByIndex(currentIndex + 1, true);
      } else {
        setPlayingState(false);
        if (seekBar) seekBar.value = "0";
        if (curTimeEl) curTimeEl.textContent = "00:00";
      }
    });

    updateNavButtons();

    return {
      getSlug: function () {
        var item = playlist[currentIndex];
        return item ? item.slug : activeSlug;
      },
      isPlaying: function () {
        return !audio.paused && !audio.ended;
      },
      togglePlay: togglePlay,
      playIndex: function (index, autoPlay, syncOptions) {
        playTrackByIndex(index, autoPlay, syncOptions);
      },
      playSlug: function (slug, autoPlay, syncOptions) {
        for (var j = 0; j < playlist.length; j += 1) {
          if (playlist[j].slug === slug) {
            playTrackByIndex(j, autoPlay, syncOptions);
            return true;
          }
        }
        return false;
      },
      onChange: function (fn) {
        listeners.push(fn);
      },
    };
  }

  var playerElement = document.querySelector("[data-audio-player]");
  var playerApi = playerElement ? initAudioPlayer(playerElement) : null;

  if (playerApi) {
    var cards = Array.prototype.slice.call(
      document.querySelectorAll("[data-audio-card]")
    );
    var landingPlayAll = document.querySelector("[data-download-play-all]");

    if (landingPlayAll) {
      landingPlayAll.addEventListener("click", function () {
        playerApi.playIndex(0, true);
        if (playerElement) {
          playerElement.scrollIntoView({
            behavior: reduceMotion ? "auto" : "smooth",
            block: "nearest",
          });
        }
      });
    }

    if (cards.length) {
      cards.forEach(function (card) {
        var slug = card.getAttribute("data-slug") || "";
        var cueBtn = card.querySelector("[data-cue-track]");
        var titleBtn = card.querySelector("[data-cue-title]");

        function triggerCard() {
          if (!slug) return;
          if (playerApi.getSlug() === slug) {
            playerApi.togglePlay();
          } else {
            playerApi.playSlug(slug, true);
          }
        }

        if (cueBtn) cueBtn.addEventListener("click", triggerCard);
        if (titleBtn) titleBtn.addEventListener("click", triggerCard);
      });

      playerApi.onChange(function (activeSlug, isPlaying, hasProgress) {
        cards.forEach(function (card) {
          var slug = card.getAttribute("data-slug") || "";
          var isCurrent = slug === activeSlug;
          card.classList.toggle("is-active", isCurrent);
          var dot = card.querySelector("[data-active-dot]");
          if (dot) dot.classList.toggle("is-hidden", !isCurrent);
          var playIcon = card.querySelector("[data-card-play-icon]");
          var pauseIcon = card.querySelector("[data-card-pause-icon]");
          var cueBtn = card.querySelector("[data-cue-track]");
          var labelSpan = cueBtn ? cueBtn.querySelector("span") : null;
          if (playIcon) playIcon.classList.toggle("is-hidden", isCurrent && isPlaying);
          if (pauseIcon) pauseIcon.classList.toggle("is-hidden", !(isCurrent && isPlaying));
          if (labelSpan) {
            if (isCurrent && isPlaying) {
              labelSpan.textContent = "Tạm dừng";
            } else if (isCurrent && hasProgress) {
              labelSpan.textContent = "Tiếp tục";
            } else {
              labelSpan.textContent = "Nghe";
            }
          }
        });
      });
    }

    window.addEventListener("popstate", function () {
      if (body.classList.contains("page-landing")) return;
      var slug = currentSlug();
      if (!slug) return;
      playerApi.playSlug(slug, playerApi.isPlaying(), {
        syncPage: true,
        pushHistory: false,
      });
    });

    if (
      window.location.hash === "#audio-player" ||
      window.location.search.indexOf("autoplay=1") !== -1
    ) {
      playerApi.togglePlay();
    }
  }

  syncThemeButton();
})();
