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
})();
