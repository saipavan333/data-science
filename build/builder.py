# -*- coding: utf-8 -*-
"""builder.py — the static-site engine for Data Science Mentor."""
import re

LETTERS = "ABCDEFGHIJ"

_ENTITY = re.compile(r'&(#\d+;|#x[0-9a-fA-F]+;|[A-Za-z][A-Za-z0-9]*;)')

def esc(s):
    """Escape <, >, and stray & — but keep real entities (&times;, &#772;)."""
    s = str(s).replace("\x01", "")
    s = _ENTITY.sub("\x01\\1", s)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return s.replace("\x01", "&")

def attresc(s):
    return str(s).replace("&", "&amp;").replace('"', "&quot;")

def inline(text):
    codes = []
    def stash(m):
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)
    text = re.sub(r"`([^`]+)`", stash, text)
    text = text.replace("\\$", "$")          # \$ -> $ (un-escape dollars)
    text = esc(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"~([^~]+)~", r'<span class="term">\1</span>', text)
    text = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", text)
    def unstash(m):
        return '<code class="inline">%s</code>' % esc(codes[int(m.group(1))])
    return re.sub(r"\x00(\d+)\x00", unstash, text)

def fmt(text):
    text = text.strip("\n")
    out = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        if all(re.match(r"^\s*-\s+", l) for l in lines):
            lis = "".join("<li>%s</li>" % inline(re.sub(r"^\s*-\s+", "", l)) for l in lines)
            out.append("<ul>%s</ul>" % lis)
        elif all(re.match(r"^\s*\d+\.\s+", l) for l in lines):
            lis = "".join("<li>%s</li>" % inline(re.sub(r"^\s*\d+\.\s+", "", l)) for l in lines)
            out.append("<ol>%s</ol>" % lis)
        else:
            out.append("<p>%s</p>" % inline(" ".join(l.strip() for l in lines)))
    return "\n".join(out)

def h2(title, kicker=None):
    k = '<span class="kicker">%s</span>' % esc(kicker) if kicker else ""
    return "<h2>%s%s</h2>" % (k, esc(title))

def h3(title):
    return "<h3>%s</h3>" % esc(title)

def concept(text):
    return fmt(text)

def callout(kind, title, text, icon=""):
    ic = (icon + " ") if icon else ""   # icon is trusted markup
    return ('<div class="callout %s"><div class="ctitle">%s%s</div>%s</div>'
            % (kind, ic, esc(title), fmt(text)))

def why(text, icon="&#9678;", title="Why this matters"):
    return callout("why", title, text, icon)

def tip(text, icon="&#10022;", title="Mentor's tip"):
    return callout("tip", title, text, icon)

def warn(text, icon="&#9650;", title="Watch out"):
    return callout("warn", title, text, icon)

def pitfall(text, icon="&#10007;", title="Common pitfall"):
    return callout("pitfall", title, text, icon)

def note(text, icon="&#8250;", title="Note"):
    return callout("note", title, text, icon)

def figure(src, caption, alt=""):
    return ('<figure class="fig"><img src="%s" alt="%s" loading="lazy">'
            '<figcaption>%s</figcaption></figure>'
            % (src, attresc(alt or caption), inline(caption)))

def formula(expr_html, note_text=None):
    n = "<br><small>%s</small>" % inline(note_text) if note_text else ""
    return '<div class="formula">%s%s</div>' % (expr_html, n)

def keypoints(items, title="Key points to remember"):
    lis = "".join("<li>%s</li>" % inline(i) for i in items)
    return ('<div class="keypoints"><h3>&#9733; %s</h3><ul>%s</ul></div>'
            % (esc(title), lis))

def code_example(code, output="", filename="example.py", runnable=True, out_label="Output"):
    code = code.strip("\n")
    run = ('<button class="cc-run" title="Run this in your browser with Pyodide">'
           '&#9654; Run</button>') if runnable else ""
    out_html = ""
    if output:
        out_html = ('<div class="cc-output"><div class="cc-out-label">%s</div><pre>%s</pre></div>'
                    % (esc(out_label), esc(output.strip("\n"))))
    return ('<div class="codecard"><div class="cc-head">'
            '<span class="cc-dots"><i></i><i></i><i></i></span>'
            '<span class="cc-name">%s</span>%s</div>'
            '<pre><code>%s</code></pre>%s</div>'
            % (esc(filename), run, esc(code), out_html))

def quiz(questions, title="Check your understanding"):
    items = ""
    for qi, q in enumerate(questions):
        opts = ""
        for oi, op in enumerate(q["options"]):
            corr = "1" if op.get("correct") else "0"
            opts += ('<div class="qopt" data-correct="%s" data-letter="%s" data-why="%s">'
                     '<span class="qletter">%s</span><div class="qtext">%s</div></div>'
                     % (corr, LETTERS[oi], attresc(inline(op.get("why", ""))),
                        LETTERS[oi], inline(op["t"])))
        items += ('<div class="qitem"><div class="qstem"><span class="qn">Q%d.</span>%s</div>'
                  '%s<div class="qexplain"></div></div>'
                  % (qi + 1, inline(q["q"]), opts))
    return ('<div class="quiz"><div class="qhead">&#9998; %s<span class="qprog"></span>'
            '</div>%s</div>' % (esc(title), items))

def practice(exercises, title="Practice"):
    body = ""
    for i, ex in enumerate(exercises):
        sol = ex["sol"] if ex.get("html") else fmt(ex["sol"])
        body += ('<div class="exercise"><div class="ex-q"><span class="exn">%d</span>%s</div>'
                 '<details class="sol"><summary>Show solution &amp; reasoning</summary>'
                 '<div class="sol-body">%s</div></details></div>'
                 % (i + 1, inline(ex["q"]), sol))
    return ('<details class="box practice" open><summary>&#9670; %s'
            '<span class="twist">&#9656;</span></summary>'
            '<div class="box-body">%s</div></details>' % (esc(title), body))

def deepdive(body_html, title="Deep dive"):
    return ('<details class="box deepdive"><summary>&#9678; %s'
            '<span class="twist">&#9656;</span></summary>'
            '<div class="box-body">%s</div></details>' % (esc(title), body_html))

def table(headers, rows, numeric=None, caption=None):
    numeric = numeric or []
    th = "".join('<th class="%s">%s</th>' % ("num" if i in numeric else "", esc(h))
                 for i, h in enumerate(headers))
    trs = ""
    for r in rows:
        tds = "".join('<td class="%s">%s</td>' % ("num" if i in numeric else "", inline(str(c)))
                      for i, c in enumerate(r))
        trs += "<tr>%s</tr>" % tds
    cap = ('<figcaption style="text-align:center">%s</figcaption>' % inline(caption)) if caption else ""
    return ('<div class="tbl-wrap"><table class="data"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>%s' % (th, trs, cap))

def interview_check(items, title="Interview check"):
    lis = "".join("<li>%s</li>" % inline(i) for i in items)
    return ('<div class="callout why"><div class="ctitle">&#9670; %s</div>'
            '<p>Before moving on, make sure you could answer these out loud:</p>'
            '<ul>%s</ul></div>' % (esc(title), lis))

def render_sidebar(tracks, active_id, link_base, index_href):
    total = sum(len(t["lessons"]) for t in tracks)
    parts = ['<a class="brand" href="%s"><span class="mark">DS</span>'
             '<span class="name">Data Science Masterclass<small>zero &#8594; job-ready</small>'
             '</span></a>' % index_href]
    parts.append('<button class="side-search" id="side-search">%s<span>Search lessons</span>'
                 '<span class="kbd">Ctrl K</span></button>' % _SEARCH_SVG)
    parts.append('<div class="side-prog"><div class="prow"><span class="plabel">Your progress</span>'
                 '<span class="pcount" id="side-pcount">0 / %d</span></div>'
                 '<div class="pbar"><div class="pfill" id="side-pfill"></div></div></div>' % total)
    for t in tracks:
        st = t.get("status", "soon")
        open_attr = ""
        lessons_html = ""
        for ls in t["lessons"]:
            cls = "active" if ls["id"] == active_id else ""
            pill = "" if ls.get("ready") else '<span class="pill">soon</span>'
            lessons_html += '<li><a class="%s" data-lid="%s" href="%s%s.html">%s%s</a></li>' % (
                cls, ls["id"], link_base, ls["id"], esc(ls["title"]), pill)
            if ls["id"] == active_id:
                open_attr = " open"
        parts.append(
            '<details class="nav-track" data-status="%s" data-track="%s"%s>'
            '<summary><span class="tnum">%s</span><span>%s</span>'
            '<span class="chev">&#9656;</span></summary>'
            '<ul class="nav-lessons">%s</ul></details>'
            % (st, t["num"], open_attr, t["num"], esc(t["title"]), lessons_html))
    parts.append('<div class="side-foot">Built as a masterclass &mdash; learn, practice, '
                 'quiz, and revise. Your progress saves on this device.</div>')
    return '<aside class="sidebar">%s</aside>' % "".join(parts)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
         '&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600'
         '&display=swap" rel="stylesheet">')

_SEARCH_SVG = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
               'stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"></circle>'
               '<path d="m21 21-4.3-4.3"></path></svg>')

CMDK = ('<div class="cmdk" id="cmdk"><div class="cmdk-box">'
        '<div class="cmdk-in">%s<input id="cmdk-input" autocomplete="off" spellcheck="false" '
        'placeholder="Search every lesson &mdash; type a topic like &lsquo;p-value&rsquo; or &lsquo;join&rsquo;"><span class="esc">ESC</span></div>'
        '<div class="cmdk-list" id="cmdk-list"></div></div></div>' % _SEARCH_SVG)

TOAST = '<div class="toast" id="toast"></div>'

DECK = ('<div class="deck" id="deck"><div class="card"><button class="dk-close" id="dk-close" '
        'aria-label="Close">&times;</button><div class="dk-count" id="dk-count"></div>'
        '<div class="dk-q" id="dk-q"></div><div class="dk-actions">'
        '<button class="dk-btn" id="dk-again">Still fuzzy</button>'
        '<button class="dk-btn primary" id="dk-got">Got it &#8594;</button></div></div></div>')

def topbar(crumbs_html, lesson_id="", mark=True):
    mc = ('<button class="tb-btn" id="mark-btn" data-lesson="%s">'
          '<span class="mc-ico">&#9711;</span><span class="mc-txt">Mark complete</span></button>'
          % attresc(lesson_id)) if mark and lesson_id else ""
    return ('<div class="topbar"><button class="menu-btn" aria-label="Open lessons">&#9776;</button>'
            '<div class="crumbs">%s</div><div class="tb-spacer"></div>%s'
            '<button class="tb-btn" id="cmdk-btn">%s Search <span class="kbd">Ctrl K</span></button>'
            '</div>' % (crumbs_html, mc, _SEARCH_SVG))

def page(title, inner, sidebar, assets_prefix, desc="", body_class="", top="", lesson_id=""):
    return (
'<!DOCTYPE html>\n<html lang="en">\n<head>\n'
'<meta charset="utf-8">\n'
'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
'<title>%s</title>\n'
'<meta name="description" content="%s">\n'
'%s\n'
'<link rel="stylesheet" href="%sassets/css/styles.css">\n'
'</head>\n<body class="%s" data-lesson="%s">\n'
'<div class="readbar" id="readbar"></div>\n<div class="scrim"></div>\n<div class="app">\n%s\n'
'<div class="main">\n%s\n<main class="content">\n%s\n</main>\n</div>\n</div>\n'
'%s%s%s\n<script src="%sassets/js/app.js"></script>\n</body>\n</html>\n'
        % (esc(title), attresc(desc), FONTS, assets_prefix, attresc(body_class),
           attresc(lesson_id), sidebar, top, inner, CMDK, TOAST, DECK, assets_prefix))

def lesson_nav(prev, nxt):
    if prev:
        p = ('<a class="prev" href="%s.html"><span class="dir">&#8249; Previous</span>'
             '<span class="ttl">%s</span></a>' % (prev["id"], esc(prev["title"])))
    else:
        p = ('<span class="prev disabled" style="flex:1 1 0;border:1px solid var(--line);'
             'border-radius:var(--radius);padding:14px 18px;opacity:.4">'
             '<span class="dir">&#8249; Previous</span>'
             '<span class="ttl">Start of the path</span></span>')
    if nxt:
        n = ('<a class="next" href="%s.html"><span class="dir">Next &#8250;</span>'
             '<span class="ttl">%s</span></a>' % (nxt["id"], esc(nxt["title"])))
    else:
        n = ('<span class="next disabled" style="flex:1 1 0;border:1px solid var(--line);'
             'border-radius:var(--radius);padding:14px 18px;opacity:.4;text-align:right">'
             '<span class="dir">Next &#8250;</span>'
             '<span class="ttl">More coming soon</span></span>')
    return '<nav class="lesson-nav">%s%s</nav>' % (p, n)

def lesson_header(meta, track_title):
    crumbs = ('<div class="crumbs"><a href="../index.html">Home</a> &rsaquo; %s &rsaquo; '
              '<span>Lesson %s</span></div>' % (esc(track_title), esc(str(meta.get("num", "")))))
    tag = '<div class="lesson-tag">&#9670; %s</div>' % esc(meta["track_label"])
    title = '<h1 class="lesson-title">%s</h1>' % esc(meta["title"])
    lede = '<p class="lesson-lede">%s</p>' % inline(meta["lede"]) if meta.get("lede") else ""
    bits = []
    if meta.get("minutes"):
        bits.append('<span>%s min read</span>' % meta["minutes"])
    bits.append('<span>%s</span>' % esc(meta.get("level", "Beginner")))
    if meta.get("dots"):
        on, tot = meta["dots"]
        dots = "".join('<i class="%s"></i>' % ("on" if i < on else "") for i in range(tot))
        bits.append('<span>Lesson %s of %s in track <span class="dotline">%s</span></span>'
                    % (on, tot, dots))
    meta_row = '<div class="meta-row">%s</div>' % "".join(bits)
    return tag + title + lede + meta_row + '<hr class="rule">'

def build_lesson_page(tracks, meta, body_html, prev, nxt, track_title):
    sidebar = render_sidebar(tracks, meta["id"], "", "../index.html")
    crumbs = ('<a href="../index.html">Home</a> &rsaquo; <span>%s</span> &rsaquo; '
              '<span class="cur">Lesson %s</span>'
              % (esc(track_title), esc(str(meta.get("num", "")))))
    top = topbar(crumbs, lesson_id=meta["id"], mark=True)
    revise = ('<button class="revise-cta" id="revise-btn">&#9788; Revise this lesson '
              '&mdash; flashcards</button>')
    inner = lesson_header(meta, track_title) + body_html + revise + lesson_nav(prev, nxt)
    return page(meta["title"] + " · Data Science Masterclass", inner, sidebar, "../",
                desc=meta.get("lede", ""), body_class="lesson", top=top, lesson_id=meta["id"])

def placeholder_body(meta, track_title, outline):
    items = "".join("<li>%s</li>" % inline(x) for x in outline) if outline else ""
    return (
        '<div class="callout note"><div class="ctitle">&#9874; In development</div>'
        '<p>This lesson is part of the planned path and will be built to the same gold '
        'standard as the finished lessons &mdash; motivation-first concept, a runnable worked '
        'example, key points, a quiz, practice with worked solutions, and a deep dive. '
        'It is shown here so you can see the whole journey end to end.</p></div>'
        + (('<h2>What this lesson will cover</h2><ul>%s</ul>' % items) if items else ''))


# ---------------------------------------------------------------------------
# INTERACTIVE LAB ENGINE
# The learner edits real code, runs it in-browser (Pyodide + sqlite3), and is
# checked against an expected result that is COMPUTED HERE by executing the
# reference solution at build time — so a lab can never ship a wrong answer.
# ---------------------------------------------------------------------------

def _sql_canon(setup, sql):
    """Run `sql` against `setup` and return a canonical serialization of the rows."""
    import sqlite3
    db = sqlite3.connect(":memory:")
    db.executescript(setup)
    rows = db.execute(sql).fetchall()
    def c(v):
        if v is None:
            return ""
        if isinstance(v, float) and v == int(v):
            return str(int(v))
        return str(v)
    return ";".join("|".join(c(v) for v in r) for r in rows)

def lab(task, setup, solution, starter="", hint="", title="Your turn", explain=""):
    """An interactive SQL lab. `solution` is executed now to derive the expected answer."""
    expected = _sql_canon(setup, solution)          # raises at build time if the solution is wrong
    starter = starter or "-- write your query here\nSELECT "
    sol_block = ('<div class="lab-solcode"><pre><code>%s</code></pre></div>%s'
                 % (esc(solution.strip()), ("<p>%s</p>" % inline(explain)) if explain else ""))
    return (
      '<div class="lab" data-setup="%s" data-expected="%s">'
      '<div class="lab-head"><span class="lab-badge">&#9670; LAB</span>'
      '<span class="lab-title">%s</span>'
      '<span class="lab-state" aria-live="polite"></span></div>'
      '<div class="lab-task">%s</div>'
      '<div class="lab-editor"><textarea class="lab-code" spellcheck="false" rows="7">%s</textarea></div>'
      '<div class="lab-actions">'
      '<button class="lab-btn lab-run">&#9654; Run</button>'
      '<button class="lab-btn primary lab-check">Check my answer</button>'
      '<button class="lab-btn ghost lab-hint-btn">Hint</button>'
      '<button class="lab-btn ghost lab-sol-btn">Solution</button>'
      '<button class="lab-btn ghost lab-reset">Reset</button>'
      '</div>'
      '<div class="lab-msg"></div>'
      '<div class="lab-out"><div class="cc-out-label">Your result</div><pre></pre></div>'
      '<div class="lab-reveal lab-hint" hidden><b>Hint.</b> %s</div>'
      '<div class="lab-reveal lab-sol" hidden><b>Reference solution.</b>%s</div>'
      '</div>'
      % (attresc(setup), attresc(expected), esc(title), fmt(task), esc(starter),
         inline(hint or "Re-read the task and check which clause each requirement belongs in."),
         sol_block))
