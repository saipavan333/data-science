# -*- coding: utf-8 -*-
"""hubs.py — render the three resource hub pages: Glossary, Labs, Cheatsheets."""
import re
import builder as B
from glossary import GLOSSARY, CATEGORY

_CAT_ORDER = ["Foundations", "Python", "SQL", "Statistics", "EDA", "Experimentation",
              "Causal inference", "Machine learning", "Feature engineering",
              "Evaluation", "MLOps", "Communication", "Toolkit"]


def _hub_head(kicker, title, blurb, extra=""):
    return ('<header class="hub-head"><div class="hub-kicker">%s</div>'
            '<h1 class="hub-h1">%s</h1><p class="hub-blurb">%s</p>%s</header>'
            % (kicker, B.esc(title), blurb, extra))


# ------------------------------------------------------------------ Glossary
def glossary_inner():
    cats = {}
    for term, d in GLOSSARY.items():
        cats.setdefault(CATEGORY.get(term, "Foundations"), []).append((term, d))
    ordered = [c for c in _CAT_ORDER if c in cats] + [c for c in cats if c not in _CAT_ORDER]
    n = len(GLOSSARY)

    chips = "".join('<a class="gloss-chip" href="#cat-%d">%s</a>' % (i, B.esc(c))
                    for i, c in enumerate(ordered))
    head = _hub_head(
        "Resource &middot; Glossary",
        "The Glossary",
        "Every key term in the course, defined in one plain-English line. "
        "These same definitions pop up as <b>hover tooltips</b> on the dotted terms inside each lesson "
        "&mdash; this page is the whole map in one place.",
        '<input id="gloss-search" class="gloss-search" type="search" '
        'placeholder="Filter %d terms&hellip;" autocomplete="off"><div class="gloss-cats">%s</div>'
        % (n, chips))

    secs = []
    for i, c in enumerate(ordered):
        rows = ""
        for term, d in sorted(cats[c], key=lambda x: x[0]):
            rows += ('<div class="gloss-term" data-t="%s"><dt>%s</dt><dd>%s</dd></div>'
                     % (B.esc(term.lower()), B.esc(term), B.esc(d)))
        secs.append('<section class="gloss-sec" id="cat-%d"><h2 class="gloss-cat">%s'
                    '<span class="gloss-count">%d</span></h2><dl class="gloss-list">%s</dl></section>'
                    % (i, B.esc(c), len(cats[c]), rows))

    script = (
        '<script>(function(){var q=document.getElementById("gloss-search");if(!q)return;'
        'var terms=[].slice.call(document.querySelectorAll(".gloss-term"));'
        'var secs=[].slice.call(document.querySelectorAll(".gloss-sec"));'
        'q.addEventListener("input",function(){var v=q.value.trim().toLowerCase();'
        'terms.forEach(function(t){var txt=(t.getAttribute("data-t")+" "+t.textContent).toLowerCase();'
        't.style.display=(!v||txt.indexOf(v)>-1)?"":"none";});'
        'secs.forEach(function(s){var any=s.querySelector(".gloss-term:not([style*=\\"none\\"])");'
        's.style.display=any?"":"none";});});})();</script>')

    return '<div class="hub gloss-page">%s%s%s</div>' % (head, "".join(secs), script)


# ---------------------------------------------------------------------- Labs
def labs_inner(lab_index):
    total = sum(len(v) for v in lab_index.values())
    ntracks = len(lab_index)
    head = _hub_head(
        "Resource &middot; Interactive Labs",
        "Interactive Labs",
        "Every hands-on lab in the course, in one place. Each one runs real <b>Python or SQL in your "
        "browser</b> and checks your answer against a solution computed when the site was built &mdash; "
        "so it can never show you a wrong answer. Jump into any lab, and the lesson it belongs to is one "
        "click away (and back).",
        '<div class="hub-stats"><span><b>%d</b> labs</span><span><b>%d</b> tracks</span>'
        '<span><b>&#8734;</b> re-runnable</span></div>' % (total, ntracks))

    secs = []
    for num in sorted(lab_index):
        items = lab_index[num]
        tt = items[0]["track_title"]
        rows = ""
        for it in items:
            badge = ('<span class="lab-lang py">Python</span>' if it["lang"] == "py"
                     else '<span class="lab-lang sql">SQL</span>')
            rows += ('<a class="lab-card" href="lessons/%s.html#labs">%s'
                     '<span class="lab-card-body"><span class="lab-card-title">%s</span>'
                     '<span class="lab-card-lesson">%s &middot; %s</span></span>'
                     '<span class="lab-card-go">Open &#8594;</span></a>'
                     % (it["lesson_id"], badge, B.esc(it["lab_title"]),
                        it["num"], B.esc(it["lesson_title"])))
        secs.append('<section class="hub-sec"><h2 class="hub-trk"><span class="hub-tnum">%s</span>%s'
                    '<span class="hub-tcount">%d lab%s</span></h2><div class="lab-grid">%s</div></section>'
                    % (num, B.esc(tt), len(items), "" if len(items) == 1 else "s", rows))
    return '<div class="hub labs-page">%s%s</div>' % (head, "".join(secs))


# -------------------------------------------------------------- Cheatsheets
def cheats_inner(cheat_index, tracks):
    have = {c["num"] for c in cheat_index}
    head = _hub_head(
        "Resource &middot; Cheatsheets",
        "Cheatsheets",
        "One-page, printable references distilling each track to its essentials &mdash; the models, the "
        "syntax, the workflow. Open any sheet and hit <b>Print</b> for a desk copy.",
        '<div class="hub-stats"><span><b>%d</b> printable sheets</span></div>' % len(cheat_index))
    cards = ""
    for c in sorted(cheat_index, key=lambda x: x["num"]):
        cards += ('<a class="sheet-card" href="lessons/%s.html">'
                  '<div class="sheet-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                  'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" '
                  'width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg></div>'
                  '<div class="sheet-body"><div class="sheet-trk">Track %s</div>'
                  '<div class="sheet-title">%s</div></div><span class="sheet-go">&#8594;</span></a>'
                  % (c["lesson_id"], c["num"], B.esc(c["title"])))
    grid = '<div class="sheet-grid">%s</div>' % cards
    # note any tracks still lacking a cheatsheet (informational)
    missing = [t for t in tracks if t["num"] not in have
               and t["num"] not in (13, 14)]
    note = ""
    if missing:
        names = ", ".join("%s&nbsp;%s" % (t["num"], B.esc(t["title"])) for t in missing)
        note = ('<p class="hub-note">More cheatsheets are on the way for: %s.</p>' % names)
    return '<div class="hub cheats-page">%s%s%s</div>' % (head, grid, note)
