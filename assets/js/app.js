/* ============================================================================
   Data Science Mentor — App behaviour
   Quiz engine · syntax highlight · Pyodide runner · nav · scroll-to-top
   No build step, no external deps (Pyodide is loaded lazily on first Run).
   ========================================================================== */
(function () {
  "use strict";

  /* ---------- Always land at the top of a freshly opened lesson ---------- */
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  window.addEventListener("pageshow", function () { window.scrollTo(0, 0); });

  document.addEventListener("DOMContentLoaded", function () {
    setupSidebar();
    highlightAll();
    setupQuizzes();
    setupRunners();
    window.scrollTo(0, 0);
  });

  /* ----------------------------- Sidebar -------------------------------- */
  function setupSidebar() {
    var btn = document.querySelector(".menu-btn");
    var sb = document.querySelector(".sidebar");
    var scrim = document.querySelector(".scrim");
    if (btn && sb) {
      btn.addEventListener("click", function () {
        sb.classList.toggle("open");
        if (scrim) scrim.classList.toggle("show");
      });
    }
    if (scrim && sb) {
      scrim.addEventListener("click", function () {
        sb.classList.remove("open");
        scrim.classList.remove("show");
      });
    }
    // Open the track that contains the active lesson; scroll it into view.
    var active = document.querySelector(".nav-lessons a.active");
    if (active) {
      var det = active.closest("details.nav-track");
      if (det) det.open = true;
      try { active.scrollIntoView({ block: "center" }); } catch (e) {}
    }
  }

  /* ------------------------- Syntax highlight --------------------------- */
  var KW = /\b(?:def|class|return|if|elif|else|for|while|in|is|not|and|or|import|from|as|with|try|except|finally|lambda|pass|break|continue|global|nonlocal|yield|raise|assert|del|async|await|None|True|False)\b/;
  var BI = /\b(?:print|len|range|sum|min|max|abs|round|sorted|enumerate|zip|list|dict|set|tuple|int|float|str|bool|map|filter|open|type|isinstance|format|np|pd|plt|sns|stats|sm)\b/;

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightPython(raw) {
    // Master tokenizer: comments & strings first so nothing inside them is re-styled.
    var re = /(#[^\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b\d+\.?\d*\b)/g;
    var out = "";
    var last = 0;
    var m;
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
    // chunk has no strings/comments; escape then style keywords, builtins, calls.
    var esc = escapeHtml(chunk);
    esc = esc.replace(/([A-Za-z_][A-Za-z0-9_]*)(\s*\()/g, function (full, name, tail) {
      if (KW.test(name)) return '<span class="tok-kw">' + name + "</span>" + tail;
      if (BI.test(name)) return '<span class="tok-bi">' + name + "</span>" + tail;
      return '<span class="tok-fn">' + name + "</span>" + tail;
    });
    esc = esc.replace(KW, function (w) { return '<span class="tok-kw">' + w + "</span>"; });
    esc = esc.replace(new RegExp(BI.source, "g"), function (w) {
      return '<span class="tok-bi">' + w + "</span>";
    });
    return esc;
  }

  function highlightAll() {
    document.querySelectorAll(".codecard pre code").forEach(function (code) {
      if (code.dataset.hl) return;
      var raw = code.textContent;
      code.dataset.raw = raw;          // keep pristine source for the runner
      code.innerHTML = highlightPython(raw);
      code.dataset.hl = "1";
    });
  }

  /* ------------------------------ Quizzes ------------------------------- */
  function setupQuizzes() {
    document.querySelectorAll(".quiz").forEach(function (quiz) {
      var items = quiz.querySelectorAll(".qitem");
      var total = items.length;
      var done = 0, correct = 0;
      var prog = quiz.querySelector(".qprog");
      if (prog) prog.textContent = "0 / " + total + " answered";

      items.forEach(function (item) {
        var opts = item.querySelectorAll(".qopt");
        var explain = item.querySelector(".qexplain");
        opts.forEach(function (opt) {
          opt.addEventListener("click", function () {
            if (item.classList.contains("locked")) return;
            item.classList.add("locked");
            var chosenRight = opt.dataset.correct === "1";
            var correctLetter = "", correctWhy = "";
            opts.forEach(function (o) {
              if (o.dataset.correct === "1") {
                o.classList.add("correct");
                correctLetter = o.dataset.letter || "";
                correctWhy = o.dataset.why || "";
              } else if (o === opt) {
                o.classList.add("wrong");
              } else {
                o.classList.add("dim");
              }
            });
            if (explain) {
              var html;
              if (chosenRight) {
                html = '<div class="qx ok"><b>✓ Correct.</b> ' + (opt.dataset.why || "") + "</div>";
              } else {
                html = '<div class="qx no"><b>✗ Not quite.</b> ' + (opt.dataset.why || "") + "</div>" +
                       '<div class="qx ok"><b>✓ ' + correctLetter + " is the answer.</b> " + correctWhy + "</div>";
              }
              explain.innerHTML = html;
              explain.classList.add("show");
            }
            done++; if (chosenRight) correct++;
            if (prog) prog.textContent = done + " / " + total + " answered" +
              (done === total ? "  ·  " + correct + " correct" : "");
          });
        });
      });
    });
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
        window.loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/" })
          .then(resolve).catch(reject);
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
    document.querySelectorAll(".codecard .cc-run").forEach(function (btn) {
      btn.addEventListener("click", function () { runCard(btn); });
    });
  }

  function runCard(btn) {
    var card = btn.closest(".codecard");
    var code = card.querySelector("pre code").dataset.raw || card.querySelector("pre code").textContent;
    var out = card.querySelector(".cc-output.live");
    if (!out) {
      out = document.createElement("div");
      out.className = "cc-output live";
      out.innerHTML = '<div class="cc-out-label">Live output (Pyodide)</div><pre></pre>';
      card.appendChild(out);
    }
    var pre = out.querySelector("pre");
    var imgHost = out.querySelector(".cc-imgs") || (function () {
      var d = document.createElement("div"); d.className = "cc-imgs"; out.appendChild(d); return d;
    })();
    imgHost.innerHTML = "";
    pre.textContent = "";
    btn.disabled = true;
    var orig = btn.innerHTML;
    btn.innerHTML = "Running…";
    var setStatus = function (t) { pre.textContent = t; };

    loadPyodideOnce(setStatus).then(function (py) {
      var pkgs = neededPackages(code);
      setStatus("Loading packages: " + (pkgs.join(", ") || "none") + " …");
      return py.loadPackage(pkgs).catch(function () { return null; }).then(function () {
        pre.textContent = "";
        py.setStdout({ batched: function (s) { pre.textContent += s + "\n"; } });
        py.setStderr({ batched: function (s) { pre.textContent += s + "\n"; } });
        var pre_code = "import matplotlib\nmatplotlib.use('AGG')\nimport matplotlib.pyplot as plt\nplt.close('all')\n";
        var post_code =
          "\nimport io, base64 as _b64\n_figs=[]\nfor _n in plt.get_fignums():\n" +
          "    _b=io.BytesIO(); plt.figure(_n).savefig(_b, format='png', dpi=110, bbox_inches='tight'); _b.seek(0)\n" +
          "    _figs.append(_b64.b64encode(_b.read()).decode())\n_figs\n";
        var figs;
        try {
          py.runPython(pre_code);
          py.runPython(code);
          figs = py.runPython(post_code);
        } catch (err) {
          pre.textContent += "\n" + (err && err.message ? err.message : err);
          return;
        }
        try {
          var arr = figs && figs.toJs ? figs.toJs() : figs;
          (arr || []).forEach(function (b64) {
            var img = document.createElement("img");
            img.src = "data:image/png;base64," + b64;
            img.style.cssText = "max-width:100%;border-radius:8px;margin:10px 0;background:#fff;padding:6px;";
            imgHost.appendChild(img);
          });
          if (figs && figs.destroy) figs.destroy();
        } catch (e) {}
        if (!pre.textContent.trim() && !imgHost.children.length) pre.textContent = "(ran with no printed output)";
      });
    }).catch(function (err) {
      pre.textContent = (err && err.message ? err.message : String(err)) +
        "\n\nTip: open the matching notebook in /notebooks to run this locally.";
    }).then(function () {
      btn.disabled = false;
      btn.innerHTML = orig;
    });
  }
})();
