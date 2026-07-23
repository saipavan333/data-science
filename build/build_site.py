# -*- coding: utf-8 -*-
"""build_site.py — assemble the whole site from curriculum + content modules."""
import os, sys, importlib, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SITE_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)

import builder as B
from curriculum import TRACKS
import hubs
from glossary import GLOSSARY

CONTENT = {}
for fname in sorted(os.listdir(HERE)):
    if fname.startswith("content_") and fname.endswith(".py"):
        mod = importlib.import_module(fname[:-3])
        CONTENT.update(getattr(mod, "LESSONS", {}))
print("Loaded %d lesson bodies: %s" % (len(CONTENT), ", ".join(sorted(CONTENT))))

FLAT = []
for t in TRACKS:
    T = len(t["lessons"])
    for i, ls in enumerate(t["lessons"]):
        ls["ready"] = ls["id"] in CONTENT
        ls["_track"] = t
        ls["_pos"] = (i + 1, T)
        FLAT.append((t, ls))

# Derive each track's status from how many of its lessons are actually built,
# so the homepage/sidebar badges can never go stale (all built -> "ready").
for t in TRACKS:
    nready = sum(1 for ls in t["lessons"] if ls["ready"])
    t["status"] = "ready" if nready == len(t["lessons"]) else ("build" if nready else "soon")

os.makedirs(os.path.join(ROOT, "lessons"), exist_ok=True)

LAB_INDEX = {}     # track_num -> [ {lesson_id, lesson_title, num, track_title, lab_title, lang}, ... ]
CHEAT_INDEX = []   # [ {num, lesson_id, title}, ... ]

def _index_resources(t, meta, body):
    for chunk in body.split('<div class="lab"')[1:]:
        opentag = chunk[:160]
        lang = "py" if 'data-lang="py"' in opentag else "sql"
        m = re.search(r'<span class="lab-title">(.*?)</span>', chunk)
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else "Interactive lab"
        LAB_INDEX.setdefault(t["num"], []).append({
            "lesson_id": meta["id"], "lesson_title": meta["title"], "num": meta["num"],
            "track_title": t["title"], "lab_title": title, "lang": lang})
    if 'class="cs-grid"' in body:
        CHEAT_INDEX.append({"num": t["num"], "lesson_id": meta["id"], "title": meta["title"]})

for idx, (t, ls) in enumerate(FLAT):
    prev = FLAT[idx - 1][1] if idx > 0 else None
    nxt = FLAT[idx + 1][1] if idx < len(FLAT) - 1 else None
    meta = {
        "id": ls["id"], "title": ls["title"], "lede": ls.get("lede", ""),
        "minutes": ls.get("minutes"), "level": "Beginner-friendly",
        "track_label": "Track %d · %s" % (t["num"], t["title"]),
        "num": ls.get("num", ""), "dots": ls["_pos"],
    }
    body = CONTENT[ls["id"]] if ls["id"] in CONTENT else B.placeholder_body(meta, t["title"], ls.get("outline"))
    _index_resources(t, meta, body)
    html = B.build_lesson_page(TRACKS, meta, body,
                               {"id": prev["id"], "title": prev["title"]} if prev else None,
                               {"id": nxt["id"], "title": nxt["title"]} if nxt else None,
                               t["title"])
    with open(os.path.join(ROOT, "lessons", ls["id"] + ".html"), "w", encoding="utf-8") as f:
        f.write(html)

def home_inner():
    n_tracks = len(TRACKS)
    n_lessons = sum(len(t["lessons"]) for t in TRACKS)
    n_ready = sum(1 for _, ls in FLAT if ls["ready"])
    first_ready = next((ls["id"] for _, ls in FLAT if ls["ready"]), FLAT[0][1]["id"])

    hero = (
        '<section class="hero"><canvas id="hero-canvas" aria-hidden="true"></canvas>'
        '<div class="eyebrow"><span class="dot"></span>A self-paced masterclass '
        '&middot; learn &middot; practice &middot; revise</div>'
        '<h1>Become a <span class="grad">job-ready data scientist</span>.</h1>'
        '<p class="sub">One honest path, taught the way it should be: every idea in plain English, '
        'proven with code you run right here on the page, then drilled with quizzes, practice, and '
        'spaced revision until it truly sticks.</p>'
        '<div class="hero-cta"><a class="cta" href="lessons/%s.html">Start learning &#8594;</a>'
        '<a class="cta ghost" href="#path">Explore the %d tracks</a></div>'
        '<div class="hero-badges">'
        '<div class="hb"><b>%d</b><span>Tracks, in order</span></div>'
        '<div class="hb"><b>%d</b><span>Lessons</span></div>'
        '<div class="hb"><b>%d</b><span>Built to gold standard</span></div>'
        '<div class="hb"><b>&#8734;</b><span>Live, runnable code</span></div>'
        '</div></section>' % (first_ready, n_tracks, n_tracks, n_lessons, n_ready))

    cont = (
        '<div class="continue" id="continue-wrap" style="display:none">'
        '<a class="continue-card" id="continue-link" href="#">'
        '<div class="ring" id="home-ring"></div>'
        '<div class="cc-txt"><div class="cc-k">Pick up where you left off</div>'
        '<div class="cc-title" id="continue-title">&mdash;</div>'
        '<div class="cc-sub" id="continue-sub">&mdash;</div></div>'
        '<span class="cta" style="pointer-events:none">Resume &#8594;</span></a></div>')

    how = (
        '<div class="section-label">The learning method &mdash; a loop that makes it stick</div>'
        '<div class="how">'
        '<div class="step"><div class="n">1</div><h4>Learn</h4>'
        '<p>Every idea in plain English, motivation first &mdash; each term defined before it is '
        'ever used. No formula dumped on you cold.</p></div>'
        '<div class="step"><div class="n">2</div><h4>Practice</h4>'
        '<p>Runnable code on realistic data (press <b>Run</b>), plus exercises with fully worked '
        'solutions you can check yourself against.</p></div>'
        '<div class="step"><div class="n">3</div><h4>Quiz</h4>'
        '<p>Check yourself instantly. Wrong answers explain <i>why</i> they are wrong, so every '
        'mistake teaches you something.</p></div>'
        '<div class="step"><div class="n">4</div><h4>Revise</h4>'
        '<p>Spaced-repetition flashcards built from each lesson&rsquo;s key points turn '
        'understanding into lasting memory.</p></div>'
        '</div>')

    cards = ['<div class="section-label" id="path">The learning path &mdash; %d tracks, in order</div>' % n_tracks,
             '<p class="muted" style="margin-top:2px">Each track builds on the one before it. '
             'Nothing depends on something taught later &mdash; so you are never lost.</p>',
             '<div class="roadmap">']
    badge_map = {"ready": ("ready", "Ready"),
                 "build": ("build", "In progress"),
                 "soon": ("soon", "On the path")}
    for t in TRACKS:
        bcls, blabel = badge_map.get(t["status"], ("soon", "On the path"))
        chips = ""
        for ls in t["lessons"]:
            cls = "chip" if ls["ready"] else "chip soon"
            chips += ('<a class="%s" data-lid="%s" href="lessons/%s.html">'
                      '<span class="cn">%s</span>%s</a>'
                      % (cls, ls["id"], ls["id"], ls.get("num", ""), B.esc(ls["title"])))
        nready = sum(1 for ls in t["lessons"] if ls["ready"])
        cards.append(
            '<div class="tcard" data-status="%s" data-track="%s">'
            '<div class="tindex">%d</div>'
            '<div><h3><a href="lessons/%s.html">%s</a>'
            '<span class="badge %s">%s</span></h3>'
            '<div class="tdesc">%s</div>'
            '<div class="tprog"><div class="tpbar"><div class="tpfill"></div></div>'
            '<span class="tpn" data-total="%d">0 / %d</span></div>'
            '<div class="chips">%s</div></div></div>'
            % (t["status"], t["num"], t["num"], t["lessons"][0]["id"], B.esc(t["title"]),
               bcls, blabel, B.esc(t["desc"]), len(t["lessons"]), len(t["lessons"]), chips))
    cards.append("</div>")

    mentor = (
        '<div style="max-width:1100px;margin:36px auto 0;padding:0 26px">'
        '<div class="callout why">'
        '<div class="ctitle">&#9670; A word from your mentor</div>'
        '<p>The order matters. Most people drown because they jump to machine learning before '
        'they can read a distribution or trust a sample. We will not do that. We build the '
        'foundation until it is sturdy, then everything above it becomes easy. Take your time. '
        'Run the code. Get the quizzes wrong and read why. Revise. That is the work &mdash; and it '
        'is how you become genuinely great at this.</p></div></div>')

    foot = ('<div class="foot"><p><b>Data Science Masterclass.</b> A self-paced course built for '
            'real understanding &mdash; learn, practice, quiz, revise. Press <b>Ctrl&nbsp;K</b> any '
            'time to jump to any lesson. Code runs in your browser (click <b>Run</b>) or in the '
            'matching notebooks under <code class="inline">/notebooks</code>. Your progress is saved '
            'on this device.</p></div>')

    return hero + cont + how + "".join(cards) + mentor + foot

sidebar_home = B.render_sidebar(TRACKS, None, "lessons/", "index.html")
home_top = B.topbar('<span class="cur">Home</span>', mark=False)
home_html = B.page("Data Science Masterclass — zero to job-ready", home_inner(),
                   sidebar_home, "", desc="A self-paced masterclass from zero to a job-ready data "
                   "scientist: statistics, Python, SQL, ML, experimentation, and more — learn, "
                   "practice, quiz, and revise.", body_class="home", top=home_top)
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(home_html)

# ---- resource hub pages: roadmap, glossary, labs, cheatsheets ----
_HUBS = [
    ("roadmap", "Path to Mastery", hubs.roadmap_inner(),
     "Your roadmap from beginner to the best in the industry: the three phases, how to study for "
     "mastery, a portfolio-project ladder, learning in public, specialization forks, and a weekly cadence."),
    ("glossary", "Glossary", hubs.glossary_inner(),
     "Every key term in the Data Science Masterclass, defined in one line — the same definitions that "
     "appear as inline tooltips throughout the lessons."),
    ("labs", "Interactive Labs", hubs.labs_inner(LAB_INDEX),
     "Every hands-on, in-browser Python and SQL lab in the course, linked to its lesson."),
    ("cheatsheets", "Cheatsheets", hubs.cheats_inner(CHEAT_INDEX, TRACKS),
     "Printable one-page references distilling each track to its essentials."),
]
for slug, label, inner, desc in _HUBS:
    sb = B.render_sidebar(TRACKS, slug, "lessons/", "index.html")
    top = B.topbar('<a href="index.html">Home</a><span class="crumb-sep">&rsaquo;</span>'
                   '<span class="cur">%s</span>' % label, mark=False)
    html = B.page("%s — Data Science Masterclass" % label, inner, sb, "",
                  desc=desc, body_class="hubpage", top=top)
    with open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8") as f:
        f.write(html)

print("Built %d lesson pages + homepage + %d hub pages into %s" % (len(FLAT), len(_HUBS), ROOT))
print("  labs indexed: %d across %d tracks | cheatsheets: %d"
      % (sum(len(v) for v in LAB_INDEX.values()), len(LAB_INDEX), len(CHEAT_INDEX)))
