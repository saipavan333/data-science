/* ============================================================================
   THE DATA SCIENCE MASTERCLASS — app behaviour
   Learn · Practice · Quiz · Revise.  No build step, no external deps.
   Progress + revision saved in localStorage; Pyodide loaded lazily on first Run.
   ========================================================================== */
(function () {
  "use strict";

  var LS_DONE = "dsm.progress.v1";
  var LS_LAST = "dsm.last.v1";

  function getDone() {
    try { return new Set(JSON.parse(localStorage.getItem(LS_DONE) || "[]")); }
    catch (e) { return new Set(); }
  }
  function saveDone(set) {
    try { localStorage.setItem(LS_DONE, JSON.stringify(Array.from(set))); } catch (e) {}
  }
  function qs(s, r) { return (r || document).querySelector(s); }
  function qsa(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  window.addEventListener("pageshow", function () { window.scrollTo(0, 0); });

  document.addEventListener("DOMContentLoaded", function () {
    setupSidebar();
    highlightAll();
    setupQuizzes();
    setupRunners();
    recordVisit();
    setupProgress();
    setupReadbar();
    setupCmdk();
    setupKeys();
    setupRevise();
    setupHero();
    setupLabs();
    setupWidgets();
    window.scrollTo(0, 0);
  });

  /* ----------------------------- Sidebar -------------------------------- */
  function setupSidebar() {
    var btn = qs(".menu-btn"), sb = qs(".sidebar"), scrim = qs(".scrim");
    function close() { if (sb) sb.classList.remove("open"); if (scrim) scrim.classList.remove("show"); }
    if (btn && sb) btn.addEventListener("click", function () {
      sb.classList.toggle("open"); if (scrim) scrim.classList.toggle("show");
    });
    if (scrim) scrim.addEventListener("click", close);
    var active = qs(".nav-lessons a.active");
    if (active) {
      var det = active.closest("details.nav-track");
      if (det) det.open = true;
      try { active.scrollIntoView({ block: "center" }); } catch (e) {}
    }
  }

  /* ------------------------- Syntax highlight --------------------------- */
  var KW = /\b(?:def|class|return|if|elif|else|for|while|in|is|not|and|or|import|from|as|with|try|except|finally|lambda|pass|break|continue|global|nonlocal|yield|raise|assert|del|async|await|None|True|False)\b/;
  var BI = /\b(?:print|len|range|sum|min|max|abs|round|sorted|enumerate|zip|list|dict|set|tuple|int|float|str|bool|map|filter|open|type|isinstance|format|np|pd|plt|sns|stats|sm)\b/;
  function escapeHtml(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function highlightPython(raw) {
    var re = /(#[^\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b\d+\.?\d*\b)/g;
    var out = "", last = 0, m;
    while ((m = re.exec(raw)) !== null) {
      out += styleWords(raw.slice(last, m.index));
      if (m[1]) out += '<span class="tok-com">' + escapeHtml(m[1]) + "</span>";
      else if (m[2]) out += '<span class="tok-str">' + escapeHtml(m[2]) + "</span>";
      else if (m[3]) out += '<span class="tok-num">' + escapeHtml(m[3]) + "</span>";
      last = re.lastIndex;
    }
    out += styleWords(raw.slice(last));
    return out;
  }
  function styleWords(chunk) {
    var esc = escapeHtml(chunk);
    esc = esc.replace(/([A-Za-z_][A-Za-z0-9_]*)(\s*\()/g, function (full, name, tail) {
      if (KW.test(name)) return '<span class="tok-kw">' + name + "</span>" + tail;
      if (BI.test(name)) return '<span class="tok-bi">' + name + "</span>" + tail;
      return '<span class="tok-fn">' + name + "</span>" + tail;
    });
    esc = esc.replace(KW, function (w) { return '<span class="tok-kw">' + w + "</span>"; });
    esc = esc.replace(new RegExp(BI.source, "g"), function (w) { return '<span class="tok-bi">' + w + "</span>"; });
    return esc;
  }
  function highlightAll() {
    qsa(".codecard pre code").forEach(function (code) {
      if (code.dataset.hl) return;
      var raw = code.textContent;
      code.dataset.raw = raw;
      code.innerHTML = highlightPython(raw);
      code.dataset.hl = "1";
    });
  }

  /* ------------------------------ Quizzes ------------------------------- */
  function setupQuizzes() {
    qsa(".quiz").forEach(function (quiz) {
      var items = qsa(".qitem", quiz), total = items.length, done = 0, correct = 0;
      var prog = qs(".qprog", quiz);
      if (prog) prog.textContent = "0 / " + total + " answered";
      items.forEach(function (item) {
        var opts = qsa(".qopt", item), explain = qs(".qexplain", item);
        opts.forEach(function (opt) {
          opt.addEventListener("click", function () {
            if (item.classList.contains("locked")) return;
            item.classList.add("locked");
            var chosenRight = opt.dataset.correct === "1", correctLetter = "", correctWhy = "";
            opts.forEach(function (o) {
              if (o.dataset.correct === "1") { o.classList.add("correct"); correctLetter = o.dataset.letter || ""; correctWhy = o.dataset.why || ""; }
              else if (o === opt) o.classList.add("wrong");
              else o.classList.add("dim");
            });
            if (explain) {
              explain.innerHTML = chosenRight
                ? '<div class="qx ok"><b>✓ Correct.</b> ' + (opt.dataset.why || "") + "</div>"
                : '<div class="qx no"><b>✗ Not quite.</b> ' + (opt.dataset.why || "") + "</div>" +
                  '<div class="qx ok"><b>✓ ' + correctLetter + " is the answer.</b> " + correctWhy + "</div>";
              explain.classList.add("show");
            }
            done++; if (chosenRight) correct++;
            if (prog) prog.textContent = done + " / " + total + " answered" + (done === total ? "  ·  " + correct + " correct" : "");
          });
        });
      });
    });
  }

  /* ----------------------- Progress + completion ------------------------ */
  function recordVisit() {
    var id = document.body.getAttribute("data-lesson");
    if (!id) return;
    var titleEl = qs(".lesson-title"), tagEl = qs(".lesson-tag");
    var rec = { id: id, title: titleEl ? titleEl.textContent.trim() : id,
      track: tagEl ? tagEl.textContent.replace(/[^\w\s&.\/-]/g, "").trim() : "",
      href: "lessons/" + id + ".html" };
    try { localStorage.setItem(LS_LAST, JSON.stringify(rec)); } catch (e) {}
  }

  function readyLessonLinks() {
    return qsa(".nav-lessons a").filter(function (a) { return !qs(".pill", a); });
  }

  function setupProgress() {
    var done = getDone();

    // sidebar: mark done + meter
    var readyLinks = readyLessonLinks();
    var totalReady = readyLinks.length, doneReady = 0;
    readyLinks.forEach(function (a) { if (done.has(a.dataset.lid)) { a.classList.add("done"); doneReady++; } });
    var pcount = qs("#side-pcount"), pfill = qs("#side-pfill");
    if (pcount) pcount.textContent = doneReady + " / " + totalReady;
    if (pfill) pfill.style.width = (totalReady ? (doneReady / totalReady * 100) : 0) + "%";

    // topbar mark button
    var mark = qs("#mark-btn");
    if (mark) {
      var id = mark.dataset.lesson;
      renderMark(mark, done.has(id));
      mark.addEventListener("click", function () {
        var d = getDone();
        if (d.has(id)) d.delete(id); else { d.add(id); toast("✓ Lesson complete — nicely done."); }
        saveDone(d);
        renderMark(mark, d.has(id));
        setupProgress(); // refresh meters
      });
    }

    // homepage: per-track bars + chips + continue card
    qsa(".tcard").forEach(function (card) {
      var chips = qsa(".chip[data-lid]", card).filter(function (c) { return !c.classList.contains("soon"); });
      var dn = 0;
      chips.forEach(function (c) { if (done.has(c.dataset.lid)) { c.classList.add("done"); dn++; } });
      var fill = qs(".tpfill", card), n = qs(".tpn", card);
      if (fill) fill.style.width = (chips.length ? dn / chips.length * 100 : 0) + "%";
      if (n) n.textContent = chips.length ? (dn + " / " + chips.length + " done") : "coming soon";
    });
    renderContinue(done, totalReady, doneReady);
  }

  function renderMark(btn, isDone) {
    btn.classList.toggle("done", isDone);
    var ico = qs(".mc-ico", btn), txt = qs(".mc-txt", btn);
    if (ico) ico.innerHTML = isDone ? "✓" : "○";
    if (txt) txt.textContent = isDone ? "Completed" : "Mark complete";
  }

  function ringSvg(pct) {
    var R = 26, C = 2 * Math.PI * R, off = C * (1 - pct / 100);
    return '<svg width="64" height="64" viewBox="0 0 64 64">' +
      '<defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">' +
      '<stop offset="0" stop-color="#6E67FF"/><stop offset="0.5" stop-color="#A46BFF"/>' +
      '<stop offset="1" stop-color="#1FC6D8"/></linearGradient></defs>' +
      '<circle class="rtrack" cx="32" cy="32" r="' + R + '" fill="none" stroke-width="6"/>' +
      '<circle class="rfill" cx="32" cy="32" r="' + R + '" fill="none" stroke="url(#rg)" stroke-width="6" ' +
      'stroke-dasharray="' + C.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '"/></svg>' +
      '<div class="rtxt">' + Math.round(pct) + '%</div>';
  }

  function renderContinue(done, totalReady, doneReady) {
    var wrap = qs("#continue-wrap");
    if (!wrap) return;
    var all = readyLessonLinks().map(function (a) {
      var det = a.closest("details.nav-track"), tn = det ? qs("summary span:nth-child(2)", det) : null;
      return { id: a.dataset.lid, title: a.textContent.trim(), href: a.getAttribute("href"),
        track: tn ? tn.textContent.trim() : "" };
    });
    var next = all.find(function (l) { return !done.has(l.id); });
    var last = null; try { last = JSON.parse(localStorage.getItem(LS_LAST) || "null"); } catch (e) {}
    var lastValid = last && !done.has(last.id) && all.some(function (l) { return l.id === last.id; });
    var target = lastValid ? all.find(function (l) { return l.id === last.id; }) : next;
    var pct = totalReady ? doneReady / totalReady * 100 : 0;
    var ring = qs("#home-ring"); if (ring) ring.innerHTML = ringSvg(pct);
    var link = qs("#continue-link"), tt = qs("#continue-title"), sub = qs("#continue-sub");
    if (!target) {
      if (tt) tt.textContent = "You’re all caught up — every open lesson done!";
      if (sub) sub.textContent = doneReady + " of " + totalReady + " lessons complete.";
      if (link) link.setAttribute("href", "#path");
      var resume = qs(".continue-card .cta"); if (resume) resume.textContent = "Review →";
    } else {
      if (tt) tt.textContent = target.title;
      if (sub) sub.textContent = (lastValid ? "Resume · " : "Up next · ") + target.track +
        "  —  " + doneReady + "/" + totalReady + " done";
      if (link) link.setAttribute("href", target.href);
    }
    wrap.style.display = "";
  }

  function toast(msg) {
    var t = qs("#toast"); if (!t) return;
    t.innerHTML = '<span class="tk">✓</span>' + msg.replace(/^✓\s*/, "");
    t.classList.add("show");
    clearTimeout(t._t); t._t = setTimeout(function () { t.classList.remove("show"); }, 2600);
  }

  /* -------------------------- Reading progress -------------------------- */
  function setupReadbar() {
    var bar = qs("#readbar"); if (!bar) return;
    function upd() {
      var el = document.documentElement;
      var h = el.scrollHeight - el.clientHeight;
      bar.style.width = (h > 0 ? Math.min(100, el.scrollTop / h * 100) : 0) + "%";
    }
    window.addEventListener("scroll", upd, { passive: true });
    window.addEventListener("resize", upd); upd();
  }

  /* --------------------------- Command palette -------------------------- */
  function setupCmdk() {
    var box = qs("#cmdk"), input = qs("#cmdk-input"), list = qs("#cmdk-list");
    if (!box || !input || !list) return;
    var done = getDone();
    var index = qsa(".nav-lessons a").map(function (a) {
      var det = a.closest("details.nav-track"), tn = det ? qs("summary span:nth-child(2)", det) : null;
      return { title: a.textContent.replace(/soon$/i, "").trim(), href: a.getAttribute("href"),
        track: tn ? tn.textContent.trim() : "", soon: !!qs(".pill", a), id: a.dataset.lid };
    });
    var sel = 0, shown = [];
    function render(q) {
      q = (q || "").toLowerCase().trim();
      shown = index.filter(function (it) {
        return !q || it.title.toLowerCase().indexOf(q) !== -1 || it.track.toLowerCase().indexOf(q) !== -1;
      }).slice(0, 60);
      if (!shown.length) { list.innerHTML = '<div class="cmdk-empty">No lessons match “' + q + '”</div>'; return; }
      sel = 0;
      list.innerHTML = shown.map(function (it, i) {
        var mark = done.has(it.id) ? " ✓" : (it.soon ? ' <span class="ctrk" style="color:var(--faint)">soon</span>' : "");
        return '<div class="cmdk-item' + (i === 0 ? " sel" : "") + '" data-href="' + it.href + '">' +
          '<span class="cnum">' + it.track.split(" ")[0] + "</span>" +
          '<span class="cttl">' + it.title + mark + "</span>" +
          '<span class="ctrk">' + it.track.replace(/^\d+\s*/, "") + "</span></div>";
      }).join("");
      qsa(".cmdk-item", list).forEach(function (el) {
        el.addEventListener("click", function () { go(el.dataset.href); });
      });
    }
    function open() { box.classList.add("show"); input.value = ""; render(""); setTimeout(function () { input.focus(); }, 30); }
    function close() { box.classList.remove("show"); }
    function go(href) { if (href) location.href = href; }
    function move(d) {
      var items = qsa(".cmdk-item", list); if (!items.length) return;
      items[sel] && items[sel].classList.remove("sel");
      sel = (sel + d + items.length) % items.length;
      items[sel].classList.add("sel");
      items[sel].scrollIntoView({ block: "nearest" });
    }
    input.addEventListener("input", function () { render(input.value); });
    box.addEventListener("click", function (e) { if (e.target === box) close(); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") { e.preventDefault(); if (shown[sel]) go(shown[sel].href); }
      else if (e.key === "Escape") close();
    });
    [qs("#cmdk-btn"), qs("#side-search")].forEach(function (b) { if (b) b.addEventListener("click", open); });
    window._openCmdk = open; window._cmdkOpen = function () { return box.classList.contains("show"); };
  }

  /* ------------------------- Keyboard shortcuts ------------------------- */
  function setupKeys() {
    document.addEventListener("keydown", function (e) {
      var tag = (e.target.tagName || "").toLowerCase(), typing = tag === "input" || tag === "textarea";
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); if (window._openCmdk) window._openCmdk(); return; }
      if (typing || (window._cmdkOpen && window._cmdkOpen())) return;
      if (e.key === "ArrowRight") { var n = qs(".lesson-nav a.next"); if (n) location.href = n.getAttribute("href"); }
      else if (e.key === "ArrowLeft") { var p = qs(".lesson-nav a.prev"); if (p) location.href = p.getAttribute("href"); }
    });
  }

  /* --------------------------- Flashcard deck --------------------------- */
  function setupRevise() {
    var btn = qs("#revise-btn"), deck = qs("#deck");
    if (!btn || !deck) return;
    var cards = qsa(".keypoints li").map(function (li) { return li.innerHTML; });
    if (!cards.length) { btn.style.display = "none"; return; }
    var queue = [], idx = 0, total = 0;
    var q = qs("#dk-q"), count = qs("#dk-count");
    function start() { queue = cards.slice(); total = queue.length; idx = 0; deck.classList.add("show"); show(); }
    function show() {
      if (!queue.length) {
        count.textContent = "Revision complete";
        q.innerHTML = '<span style="color:var(--green)">✓</span>&nbsp; Nicely done — you recalled every key point. Come back tomorrow to lock it in.';
        return;
      }
      count.textContent = "Card " + (total - queue.length + 1) + " of " + total + "  ·  active recall";
      q.innerHTML = '<div style="font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);font-family:var(--font);font-weight:600;margin-bottom:12px">Can you explain this in your own words?</div>' + queue[0];
    }
    function close() { deck.classList.remove("show"); }
    btn.addEventListener("click", start);
    qs("#dk-got").addEventListener("click", function () { queue.shift(); show(); });
    qs("#dk-again").addEventListener("click", function () { if (queue.length) { queue.push(queue.shift()); } show(); });
    qs("#dk-close").addEventListener("click", close);
    deck.addEventListener("click", function (e) { if (e.target === deck) close(); });
  }

  /* ----------------------- Hero: living data field ---------------------- */
  function setupHero() {
    var cv = qs("#hero-canvas"); if (!cv) return;
    var ctx = cv.getContext("2d"), W = 0, H = 0, dpr = 1, parts = [], raf = 0, t = 0;
    var mouse = { x: -1e9, y: -1e9, on: false };
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion:reduce)").matches;

    function bell(nx) { var d = (nx - 0.5) / 0.19; return Math.exp(-0.5 * d * d); }
    function curveY(nx) { return H * 0.92 - bell(nx) * H * 0.6; }
    function mix(a, b, tt) { return [a[0] + (b[0] - a[0]) * tt | 0, a[1] + (b[1] - a[1]) * tt | 0, a[2] + (b[2] - a[2]) * tt | 0]; }
    var C1 = [110, 103, 255], C2 = [164, 107, 255], C3 = [31, 198, 216];
    function color(nx, a) { var c = nx < 0.5 ? mix(C1, C2, nx / 0.5) : mix(C2, C3, (nx - 0.5) / 0.5); return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")"; }

    function init() {
      var N = Math.round(Math.min(190, Math.max(60, W / 8)));
      parts = [];
      for (var i = 0; i < N; i++) {
        var nx = Math.random();
        parts.push({ nx: nx, hx: nx * W, hy: curveY(nx) + (Math.random() - 0.5) * 26,
          x: Math.random() * W, y: Math.random() * H, vx: 0, vy: 0,
          r: Math.random() * 1.7 + 1.1, seed: Math.random() * 6.28, sp: 0.4 + Math.random() * 0.7 });
      }
    }
    function resize() {
      var r = cv.getBoundingClientRect(); if (!r.width) return;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = r.width; H = r.height; cv.width = W * dpr; cv.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); init();
    }
    function guide() {
      ctx.beginPath();
      for (var g = 0; g <= 1.0001; g += 0.02) { var X = g * W, Y = curveY(g); g === 0 ? ctx.moveTo(X, Y) : ctx.lineTo(X, Y); }
      ctx.strokeStyle = "rgba(130,140,210,0.16)"; ctx.lineWidth = 1.4; ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, H * 0.92); ctx.lineTo(W, H * 0.92);
      ctx.strokeStyle = "rgba(120,130,200,0.10)"; ctx.lineWidth = 1; ctx.stroke();
    }
    function draw(anim) {
      ctx.clearRect(0, 0, W, H); guide();
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        if (anim) {
          var tx = p.hx + Math.sin(t * p.sp + p.seed) * 11, ty = p.hy + Math.cos(t * p.sp * 0.9 + p.seed) * 9;
          if (mouse.on) {
            var dx = p.x - mouse.x, dy = p.y - mouse.y, d2 = dx * dx + dy * dy;
            if (d2 < 15000 && d2 > 0.1) { var f = (15000 - d2) / 15000 * 2.6 / Math.sqrt(d2); p.vx += dx * f; p.vy += dy * f; }
          }
          p.vx += (tx - p.x) * 0.02; p.vy += (ty - p.y) * 0.02; p.vx *= 0.9; p.vy *= 0.9;
          p.x += p.vx; p.y += p.vy;
        } else { p.x = p.hx; p.y = p.hy; }
        var a = 0.42 + bell(p.nx) * 0.5;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fillStyle = color(p.nx, a); ctx.fill();
        if (bell(p.nx) > 0.55) { ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 2.4, 0, 6.2832); ctx.fillStyle = color(p.nx, 0.06); ctx.fill(); }
      }
    }
    function frame() { t += 0.006; draw(true); raf = requestAnimationFrame(frame); }
    function stop() { if (raf) cancelAnimationFrame(raf); raf = 0; }

    var host = cv.parentElement;
    host.addEventListener("mousemove", function (e) { var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; mouse.on = true; });
    host.addEventListener("mouseleave", function () { mouse.on = false; mouse.x = mouse.y = -1e9; });
    window.addEventListener("resize", function () { resize(); if (reduce) draw(false); });
    document.addEventListener("visibilitychange", function () { if (document.hidden) stop(); else if (!reduce && !raf) frame(); });

    resize();
    if (reduce) { draw(false); } else { setTimeout(frame, 60); }
  }

  /* --------------------- Pyodide in-browser runner ---------------------- */
  var pyReady = null;
  function loadPyodideOnce(status) {
    if (pyReady) return pyReady;
    status("Loading Python runtime (first run only, ~10s)…");
    pyReady = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js";
      s.onload = function () {
        window.loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/" }).then(resolve).catch(reject);
      };
      s.onerror = function () { reject(new Error("Could not load Pyodide (need internet for in-browser runs).")); };
      document.head.appendChild(s);
    });
    return pyReady;
  }
  var PKG_HINTS = ["numpy", "pandas", "scipy", "matplotlib"];
  function neededPackages(code) {
    var pk = [];
    PKG_HINTS.forEach(function (p) { if (code.indexOf(p) !== -1) pk.push(p); });
    if (/sklearn|scikit/.test(code)) pk.push("scikit-learn");
    return pk;
  }
  function setupRunners() {
    qsa(".codecard .cc-run").forEach(function (btn) { btn.addEventListener("click", function () { runCard(btn); }); });
  }
  function runCard(btn) {
    var card = btn.closest(".codecard");
    var code = card.querySelector("pre code").dataset.raw || card.querySelector("pre code").textContent;
    var out = qs(".cc-output.live", card);
    if (!out) { out = document.createElement("div"); out.className = "cc-output live";
      out.innerHTML = '<div class="cc-out-label">Live output (Pyodide)</div><pre></pre>'; card.appendChild(out); }
    var pre = qs("pre", out);
    var imgHost = qs(".cc-imgs", out) || (function () { var d = document.createElement("div"); d.className = "cc-imgs"; out.appendChild(d); return d; })();
    imgHost.innerHTML = ""; pre.textContent = ""; btn.disabled = true;
    var orig = btn.innerHTML; btn.innerHTML = "Running…";
    var setStatus = function (t) { pre.textContent = t; };
    loadPyodideOnce(setStatus).then(function (py) {
      var pkgs = neededPackages(code);
      setStatus("Loading packages: " + (pkgs.join(", ") || "none") + " …");
      return py.loadPackage(pkgs).catch(function () { return null; }).then(function () {
        pre.textContent = "";
        py.setStdout({ batched: function (s) { pre.textContent += s + "\n"; } });
        py.setStderr({ batched: function (s) { pre.textContent += s + "\n"; } });
        var pre_code = "import matplotlib\nmatplotlib.use('AGG')\nimport matplotlib.pyplot as plt\nplt.close('all')\n";
        var post_code = "\nimport io, base64 as _b64\n_figs=[]\nfor _n in plt.get_fignums():\n" +
          "    _b=io.BytesIO(); plt.figure(_n).savefig(_b, format='png', dpi=110, bbox_inches='tight'); _b.seek(0)\n" +
          "    _figs.append(_b64.b64encode(_b.read()).decode())\n_figs\n";
        var figs;
        try { py.runPython(pre_code); py.runPython(code); figs = py.runPython(post_code); }
        catch (err) { pre.textContent += "\n" + (err && err.message ? err.message : err); return; }
        try {
          var arr = figs && figs.toJs ? figs.toJs() : figs;
          (arr || []).forEach(function (b64) {
            var img = document.createElement("img"); img.src = "data:image/png;base64," + b64;
            img.style.cssText = "max-width:100%;border-radius:8px;margin:10px 0;background:#fff;padding:6px;"; imgHost.appendChild(img);
          });
          if (figs && figs.destroy) figs.destroy();
        } catch (e) {}
        if (!pre.textContent.trim() && !imgHost.children.length) pre.textContent = "(ran with no printed output)";
      });
    }).catch(function (err) {
      pre.textContent = (err && err.message ? err.message : String(err)) + "\n\nTip: open the matching notebook in /notebooks to run this locally.";
    }).then(function () { btn.disabled = false; btn.innerHTML = orig; });
  }

  /* --------------------------- Interactive labs -------------------------- */
  var LAB_HARNESS = [
    "import sqlite3",
    "db = sqlite3.connect(':memory:')",
    "db.executescript(SETUP)",
    "cur = db.execute(USER_SQL)",
    "cols = [c[0] for c in cur.description] if cur.description else []",
    "rows = cur.fetchall()",
    "def _c(v):",
    "    if v is None: return ''",
    "    if isinstance(v, float) and v == int(v): return str(int(v))",
    "    return str(v)",
    "if cols:",
    "    w = [max(len(_c(x)) for x in [cols[i]] + [r[i] for r in rows]) for i in range(len(cols))]",
    "    print('  '.join(cols[i].ljust(w[i]) for i in range(len(cols))))",
    "    print('  '.join('-'*n for n in w))",
    "    for r in rows:",
    "        print('  '.join(_c(v).ljust(w[i]) for i, v in enumerate(r)))",
    "    if not rows:",
    "        print('(query ran, but returned no rows)')",
    "else:",
    "    print('(statement ran; no rows returned)')",
    "print('__CANON__' + ';'.join('|'.join(_c(v) for v in r) for r in rows))"
  ].join("\n");

  var PY_LAB_HARNESS = [
    "_g = {}",
    "exec(SETUP, _g)",
    "exec(USER_CODE, _g)",
    "def __cv(a):",
    "    if isinstance(a, bool): return str(a)",
    "    if isinstance(a, float): return format(round(a,4),'g')",
    "    if isinstance(a, int): return str(a)",
    "    if isinstance(a, (list, tuple)): return ','.join(__cv(x) for x in a)",
    "    try:",
    "        import numpy as _np",
    "        if isinstance(a, _np.floating): return format(round(float(a),4),'g')",
    "        if isinstance(a, _np.integer): return str(int(a))",
    "        if isinstance(a, _np.ndarray): return __cv(a.tolist())",
    "    except Exception: pass",
    "    try:",
    "        import pandas as _pd",
    "        if isinstance(a, (_pd.Series, _pd.DataFrame)): return a.to_string()",
    "    except Exception: pass",
    "    return str(a)",
    "if 'answer' in _g:",
    "    print(_g['answer'])",
    "    print('__CANON__' + __cv(_g['answer']))",
    "else:",
    "    print('(no variable named answer was set - assign your result to a variable called answer)')"
  ].join("\n");

  function setupLabs() {
    qsa(".lab").forEach(function (lab) {
      var codeEl = qs(".lab-code", lab), starter = codeEl.value;
      var outBox = qs(".lab-out", lab), outPre = qs(".lab-out pre", lab);
      var msg = qs(".lab-msg", lab), state = qs(".lab-state", lab);
      var setup = lab.getAttribute("data-setup"), expected = lab.getAttribute("data-expected");
      var lang = lab.getAttribute("data-lang") || "sql";
      function setMsg(kind, html) { msg.className = "lab-msg show " + kind; msg.innerHTML = html; }

      function exec(after) {
        var btns = qsa(".lab-btn", lab);
        btns.forEach(function (b) { b.disabled = true; });
        setMsg("info", "Running…");
        outBox.classList.add("show"); outPre.textContent = "";
        var needPkgs = lang === "py" ? neededPackages(setup + "\n" + codeEl.value) : [];
        loadPyodideOnce(function (t) { outPre.textContent = t; }).then(function (py) {
          return (needPkgs.length ? py.loadPackage(needPkgs).catch(function () { return null; }) : Promise.resolve()).then(function () { return py; });
        }).then(function (py) {
          var buf = "";
          py.setStdout({ batched: function (s) { buf += s + "\n"; } });
          py.setStderr({ batched: function (s) { buf += s + "\n"; } });
          py.globals.set("SETUP", setup);
          if (lang === "py") { py.globals.set("USER_CODE", codeEl.value); }
          else { py.globals.set("USER_SQL", codeEl.value); }
          try {
            py.runPython(lang === "py" ? PY_LAB_HARNESS : LAB_HARNESS);
          } catch (e) {
            outPre.textContent = String((e && e.message) || e);
            setMsg("no", "<b>That didn't run.</b> Read the error above — it names the line and the problem.");
            state.textContent = ""; state.className = "lab-state";
            return null;
          }
          var canon = null, vis = [];
          buf.split("\n").forEach(function (l) {
            if (l.indexOf("__CANON__") === 0) canon = l.slice(9); else vis.push(l);
          });
          outPre.textContent = vis.join("\n").replace(/\s+$/, "");
          return canon;
        }).then(function (canon) {
          if (canon !== null && canon !== undefined) after(canon);
        }).catch(function (e) {
          outPre.textContent = String((e && e.message) || e);
          setMsg("no", "Could not start the Python runtime (it needs an internet connection the first time).");
        }).then(function () {
          btns.forEach(function (b) { b.disabled = false; });
        });
      }

      qs(".lab-run", lab).addEventListener("click", function () {
        exec(function () { setMsg("info", "Ran. Compare it against the task, then press <b>Check my answer</b>."); });
      });
      qs(".lab-check", lab).addEventListener("click", function () {
        exec(function (canon) {
          if (canon === expected) {
            setMsg("ok", "<b>✓ Correct.</b> Your result matches exactly — that's the real answer, not a lookup. Well done.");
            state.textContent = "✓ solved"; state.className = "lab-state ok";
          } else {
            setMsg("no", "<b>Not yet.</b> The query ran, but the rows don't match what the task asked for. Check three things: the <b>columns</b> you selected, the <b>filter</b>, and the <b>sort order</b>. Hint and Solution are below when you want them.");
            state.textContent = "keep going"; state.className = "lab-state no";
          }
        });
      });
      qs(".lab-hint-btn", lab).addEventListener("click", function () {
        var h = qs(".lab-hint", lab); h.hidden = !h.hidden;
      });
      qs(".lab-sol-btn", lab).addEventListener("click", function () {
        var v = qs(".lab-sol", lab); v.hidden = !v.hidden;
      });
      qs(".lab-reset", lab).addEventListener("click", function () {
        codeEl.value = starter; outBox.classList.remove("show");
        msg.className = "lab-msg"; msg.innerHTML = "";
        state.textContent = ""; state.className = "lab-state";
      });
    });
  }


  /* ------------------------- Interactive widgets ------------------------ */
  var WIDGETS = {};

  /* NULL three-valued logic explorer */
  WIDGETS["null-logic"] = function (host) {
    var rows = [["Ada","pro"],["Blake",null],["Chen","pro"],["Diego","free"],["Sara",null],["Tom","free"]];
    var conds = [
      ["plan = 'pro'",      function (v) { return v === null ? null : v === "pro"; }],
      ["plan != 'pro'",     function (v) { return v === null ? null : v !== "pro"; }],
      ["plan IS NULL",      function (v) { return v === null; }],
      ["plan IS NOT NULL",  function (v) { return v !== null; }]
    ];
    var cur = 1;
    host.innerHTML =
      '<div class="w-row"><span class="w-lab">WHERE</span><span class="w-seg"></span></div>' +
      '<table class="w-tbl"><thead><tr><th>name</th><th>plan</th><th>condition evaluates to</th><th>row is</th></tr></thead><tbody></tbody></table>' +
      '<div class="w-out"></div>';
    var seg = qs(".w-seg", host), tb = qs("tbody", host), out = qs(".w-out", host);
    conds.forEach(function (c, i) {
      var b = document.createElement("button");
      b.textContent = c[0];
      b.addEventListener("click", function () { cur = i; render(); });
      seg.appendChild(b);
    });
    function render() {
      qsa("button", seg).forEach(function (b, i) { b.className = i === cur ? "on" : ""; });
      var kept = 0, dropped = 0, unknown = 0;
      tb.innerHTML = rows.map(function (r) {
        var v = r[1], res = conds[cur][1](v);
        var label = res === null ? "UNKNOWN" : (res ? "TRUE" : "FALSE");
        if (res === true) kept++; else dropped++;
        if (res === null) unknown++;
        return '<tr class="' + (res === true ? "keep" : "drop") + (v === null ? " nullrow" : "") + '">' +
          "<td>" + r[0] + "</td><td>" + (v === null ? "<b>NULL</b>" : "'" + v + "'") + "</td>" +
          "<td>" + label + "</td><td>" + (res === true ? "kept" : "dropped") + "</td></tr>";
      }).join("");
      out.className = "w-out " + (unknown ? "unknown" : "true");
      out.innerHTML = unknown
        ? "<b>" + unknown + " row(s) evaluated to UNKNOWN.</b> A comparison against NULL is never true — so <code>WHERE</code> silently <b>drops</b> them. Kept " + kept + ", dropped " + dropped + ". This is the bug that quietly loses rows in real reports."
        : "<b>Kept " + kept + ", dropped " + dropped + ".</b> No NULL was involved here, so every row resolved to a clean TRUE or FALSE.";
    }
    render();
  };

  /* Join visualiser */
  WIDGETS["joins"] = function (host) {
    var cust = [[1,"Ada"],[2,"Blake"],[3,"Chen"],[4,"Diego"]];
    var ords = [[101,1,240],[102,1,90],[103,2,45],[104,3,220],[105,9,60]];
    var kinds = ["INNER","LEFT","RIGHT","FULL"], cur = 0;
    var notes = {
      INNER: "Only rows that match on <b>both</b> sides. Diego (no orders) disappears, and order 105 (no such customer) disappears too.",
      LEFT:  "Every <b>customer</b> is kept. Diego survives with NULL order columns — this is how you find customers who never ordered.",
      RIGHT: "Every <b>order</b> is kept. The orphan order 105 survives with a NULL customer — how you find records pointing at something missing.",
      FULL:  "Everything from <b>both</b> sides. Diego <i>and</i> the orphan order both appear, each padded with NULLs."
    };
    host.innerHTML =
      '<div class="w-row"><span class="w-lab">JOIN TYPE</span><span class="w-seg"></span></div>' +
      '<table class="w-tbl"><thead><tr><th>customer</th><th>order id</th><th>amount</th></tr></thead><tbody></tbody></table>' +
      '<div class="w-out"></div>';
    var seg = qs(".w-seg", host), tb = qs("tbody", host), out = qs(".w-out", host);
    kinds.forEach(function (k, i) {
      var b = document.createElement("button");
      b.textContent = k;
      b.addEventListener("click", function () { cur = i; render(); });
      seg.appendChild(b);
    });
    function render() {
      qsa("button", seg).forEach(function (b, i) { b.className = i === cur ? "on" : ""; });
      var k = kinds[cur], res = [];
      cust.forEach(function (c) {
        var m = ords.filter(function (o) { return o[1] === c[0]; });
        if (m.length) m.forEach(function (o) { res.push([c[1], o[0], o[2]]); });
        else if (k === "LEFT" || k === "FULL") res.push([c[1], null, null]);
      });
      if (k === "RIGHT" || k === "FULL") {
        ords.forEach(function (o) {
          if (!cust.some(function (c) { return c[0] === o[1]; })) res.push([null, o[0], o[2]]);
        });
      }
      tb.innerHTML = res.map(function (r) {
        var isNull = r[0] === null || r[1] === null;
        return '<tr class="' + (isNull ? "nullrow" : "keep") + '">' + r.map(function (v) {
          return "<td>" + (v === null ? "<b>NULL</b>" : v) + "</td>";
        }).join("") + "</tr>";
      }).join("");
      out.className = "w-out";
      out.innerHTML = "<b>" + k + " JOIN &rarr; " + res.length + " rows.</b> " + notes[k] +
        " Notice Ada appears twice in every join — she has two orders, and that row-multiplication is the <b>fan-out</b> that silently double-counts sums.";
    }
    render();
  };

  /* Central Limit Theorem sampler */
  WIDGETS["clt"] = function (host) {
    var pops = {
      uniform: function () { return Math.random(); },
      skewed:  function () { return Math.min(1, -Math.log(1 - Math.random()) / 4); },
      bimodal: function () { var g = function (m, s) { var u = 0, v = 0; while (!u) u = Math.random(); while (!v) v = Math.random();
                 return m + s * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
                 return Math.max(0, Math.min(1, Math.random() < 0.5 ? g(0.25, 0.07) : g(0.75, 0.07))); }
    };
    var popKey = "skewed", n = 5, means = [], popSample = [];
    host.innerHTML =
      '<div class="w-row"><span class="w-lab">POPULATION</span><span class="w-seg"></span></div>' +
      '<div class="w-row"><span class="w-lab">SAMPLE SIZE n</span>' +
      '<input class="w-slider" type="range" min="1" max="50" value="5"><span class="w-val">5</span>' +
      '<button class="w-btn primary w-draw">Draw 500 samples</button>' +
      '<button class="w-btn w-reset">Reset</button></div>' +
      '<canvas class="w-canvas"></canvas><div class="w-out"></div>';
    var seg = qs(".w-seg", host), cv = qs("canvas", host), out = qs(".w-out", host);
    var slider = qs(".w-slider", host), val = qs(".w-val", host);
    Object.keys(pops).forEach(function (k) {
      var b = document.createElement("button");
      b.textContent = k;
      b.addEventListener("click", function () { popKey = k; means = []; makePop(); render(); });
      seg.appendChild(b);
    });
    slider.addEventListener("input", function () { n = +slider.value; val.textContent = n; means = []; render(); });
    qs(".w-draw", host).addEventListener("click", function () {
      for (var i = 0; i < 500; i++) {
        var s = 0; for (var j = 0; j < n; j++) s += pops[popKey]();
        means.push(s / n);
      }
      render();
    });
    qs(".w-reset", host).addEventListener("click", function () { means = []; render(); });
    function makePop() { popSample = []; for (var i = 0; i < 8000; i++) popSample.push(pops[popKey]()); }
    function hist(arr, bins, lo, hi) {
      var h = new Array(bins).fill(0);
      arr.forEach(function (v) { var b = Math.floor((v - lo) / (hi - lo) * bins); if (b >= 0 && b < bins) h[b]++; });
      return h;
    }
    function render() {
      qsa("button", seg).forEach(function (b) { b.className = b.textContent === popKey ? "on" : ""; });
      var r = cv.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
      var W = r.width, H = r.height;
      cv.width = W * dpr; cv.height = H * dpr;
      var x = cv.getContext("2d"); x.setTransform(dpr, 0, 0, dpr, 0, 0);
      x.clearRect(0, 0, W, H);
      var padL = 14, padR = 14, midY = H * 0.44, gap = 30;
      function panel(arr, top, bot, color, label, bins) {
        var h = hist(arr, bins, 0, 1), mx = Math.max.apply(null, h) || 1;
        var w = (W - padL - padR) / bins;
        for (var i = 0; i < bins; i++) {
          var bh = (h[i] / mx) * (bot - top);
          x.fillStyle = color;
          x.fillRect(padL + i * w, bot - bh, Math.max(1, w - 1), bh);
        }
        x.fillStyle = "#9AA6C0"; x.font = "600 11px Inter, sans-serif";
        x.fillText(label, padL, top - 6);
        x.strokeStyle = "rgba(154,166,192,.25)"; x.beginPath();
        x.moveTo(padL, bot + .5); x.lineTo(W - padR, bot + .5); x.stroke();
      }
      panel(popSample, 18, midY, "rgba(234,154,11,.75)", "The population (one draw = one value)", 60);
      if (means.length) {
        panel(means, midY + gap, H - 16, "rgba(110,103,255,.85)",
              "Distribution of the SAMPLE MEAN  (n = " + n + ", " + means.length + " samples)", 60);
      } else {
        x.fillStyle = "#6B7793"; x.font = "600 12px Inter, sans-serif";
        x.fillText("Press “Draw 500 samples” to build the sampling distribution ↓", padL, midY + gap + 22);
      }
      if (means.length > 30) {
        var m = means.reduce(function (a, b) { return a + b; }, 0) / means.length;
        var sd = Math.sqrt(means.reduce(function (a, b) { return a + (b - m) * (b - m); }, 0) / means.length);
        out.className = "w-out";
        out.innerHTML = "Mean of the sample means: <b>" + m.toFixed(3) + "</b> &middot; spread (SE): <b>" +
          sd.toFixed(3) + "</b>. " + (n === 1
            ? "At <b>n = 1</b> you are just redrawing the population — same shape, skew and all."
            : "Even though the population is <b>" + popKey + "</b>, the sample mean is piling into a <b>bell</b> — and it gets <b>narrower</b> as n grows. That is the Central Limit Theorem doing its work.");
      } else {
        out.className = "w-out";
        out.innerHTML = "Pick a population shape, set <b>n</b>, then draw samples. Watch what happens to the <b>bottom</b> histogram as you raise n — that is the whole idea behind confidence intervals and A/B tests.";
      }
    }
    makePop(); render();
    window.addEventListener("resize", function () { render(); });
  };


  /* p-value simulator */
  WIDGETS["pvalue"] = function (host) {
    var z = 2.1, alpha = 0.05;
    host.innerHTML =
      '<div class="w-row"><span class="w-lab">OBSERVED RESULT (standard errors from H0)</span>' +
      '<input class="w-slider" type="range" min="0" max="4" step="0.05" value="2.1"><span class="w-val">2.10</span></div>' +
      '<canvas class="w-canvas" style="height:300px"></canvas><div class="w-out"></div>';
    var cv = qs("canvas", host), out = qs(".w-out", host), slider = qs(".w-slider", host), val = qs(".w-val", host);
    function erf(x) { var s = x < 0 ? -1 : 1; x = Math.abs(x); var t = 1 / (1 + 0.3275911 * x);
      var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
      return s * y; }
    function phi(x) { return 0.5 * (1 + erf(x / Math.SQRT2)); }
    slider.addEventListener("input", function () { z = +slider.value; val.textContent = z.toFixed(2); render(); });
    function render() {
      var r = cv.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2), W = r.width, H = r.height;
      cv.width = W * dpr; cv.height = H * dpr; var x = cv.getContext("2d"); x.setTransform(dpr, 0, 0, dpr, 0, 0);
      x.clearRect(0, 0, W, H);
      var lo = -4, hi = 4, padB = 24, padT = 12;
      function X(v) { return (v - lo) / (hi - lo) * W; }
      function Y(d) { return H - padB - d * (H - padB - padT) / 0.4; }
      function pdf(v) { return Math.exp(-v * v / 2) / Math.sqrt(2 * Math.PI); }
      x.fillStyle = "rgba(239,62,104,.32)";
      [[-4, -z], [z, 4]].forEach(function (seg) {
        if (seg[1] <= seg[0]) return;
        x.beginPath(); x.moveTo(X(seg[0]), H - padB);
        for (var v = seg[0]; v <= seg[1]; v += 0.02) x.lineTo(X(v), Y(pdf(v)));
        x.lineTo(X(seg[1]), H - padB); x.closePath(); x.fill();
      });
      x.beginPath();
      for (var v = lo; v <= hi; v += 0.02) { var px = X(v), py = Y(pdf(v)); v === lo ? x.moveTo(px, py) : x.lineTo(px, py); }
      x.strokeStyle = "#6E67FF"; x.lineWidth = 2; x.stroke();
      x.strokeStyle = "rgba(154,166,192,.4)"; x.beginPath(); x.moveTo(0, H - padB); x.lineTo(W, H - padB); x.stroke();
      x.strokeStyle = "#EF3E68"; x.lineWidth = 1.5;
      [z, -z].forEach(function (v) { x.beginPath(); x.moveTo(X(v), padT); x.lineTo(X(v), H - padB); x.stroke(); });
      x.fillStyle = "#9AA6C0"; x.font = "600 11px Inter, sans-serif";
      x.fillText("if H0 is true, results cluster here", X(0) - 78, padT + 10);
      var pv = 2 * (1 - phi(Math.abs(z)));
      out.className = "w-out " + (pv < alpha ? "true" : "unknown");
      out.innerHTML = "Two-tailed p-value = <b>" + pv.toFixed(4) + "</b> (the shaded area). " +
        (pv < alpha
          ? "Below &alpha; = 0.05 &rarr; <b>reject H0</b>: statistically significant. Pure chance would produce something this extreme only <b>" + (pv * 100).toFixed(2) + "%</b> of the time."
          : "Above &alpha; = 0.05 &rarr; <b>fail to reject H0</b>: not enough evidence. Chance alone gives a result this extreme <b>" + (pv * 100).toFixed(1) + "%</b> of the time.");
    }
    render(); window.addEventListener("resize", render);
  };

  function setupWidgets() {
    qsa(".widget").forEach(function (w) {
      var kind = w.getAttribute("data-widget"), body = qs(".w-body", w), fn = WIDGETS[kind];
      if (!fn) return;
      body.innerHTML = "";
      try { fn(body); } catch (e) { body.textContent = "(this explorer could not load)"; }
    });
  }

})();
