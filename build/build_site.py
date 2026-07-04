# -*- coding: utf-8 -*-
"""build_site.py — assemble the whole site from curriculum + content modules."""
import os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SITE_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)

import builder as B
from curriculum import TRACKS

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

os.makedirs(os.path.join(ROOT, "lessons"), exist_ok=True)

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
        '<section class="hero">'
        '<div class="eyebrow">Your personal mentor &middot; self-paced</div>'
        '<h1>From zero to a <span class="grad">job-ready data scientist</span>.</h1>'
        '<p class="sub">A single, honest path through the eleven things a data scientist must '
        'truly understand &mdash; each idea taught motivation-first, proven with runnable code on '
        'realistic data, and drilled with quizzes and practice. No corner cut.</p>'
        '<a class="cta" href="lessons/%s.html">Start Lesson 1.1 &#8594;</a>'
        '<a class="cta ghost" href="#path">See the whole path</a>'
        '</section>' % first_ready)

    stats = (
        '<div class="statgrid">'
        '<div class="s"><b>%d</b><span>Tracks, in dependency order</span></div>'
        '<div class="s"><b>%d</b><span>Lessons on the path</span></div>'
        '<div class="s"><b>%d</b><span>Built to the gold standard so far</span></div>'
        '<div class="s"><b>&#8734;</b><span>Re-runs &mdash; every example is live code</span></div>'
        '</div>' % (n_tracks, n_lessons, n_ready))

    how = (
        '<div class="section-label">How every lesson teaches you</div>'
        '<div class="how">'
        '<div class="step"><div class="n">1</div><h4>Why it matters</h4>'
        '<p>Each idea starts with the decision it informs &mdash; never a formula first.</p></div>'
        '<div class="step"><div class="n">2</div><h4>The idea, then proof</h4>'
        '<p>Plain-English concept, every term defined, then a runnable example on real-looking '
        'data.</p></div>'
        '<div class="step"><div class="n">3</div><h4>Pictures over paragraphs</h4>'
        '<p>Anything with structure gets a diagram &mdash; rendered and checked, never broken.</p>'
        '</div>'
        '<div class="step"><div class="n">4</div><h4>Practice &amp; defend</h4>'
        '<p>Quizzes with explained answers, exercises with worked solutions, and an interview '
        'check.</p></div>'
        '</div>')

    cards = ['<div class="section-label" id="path">The learning path</div>',
             '<p class="muted" style="margin-top:2px">Each track builds on the one before it. '
             'Nothing depends on something taught later.</p>',
             '<div class="roadmap">']
    badge_map = {"ready": ("ready", "Ready to learn"),
                 "build": ("build", "In progress"),
                 "soon": ("soon", "On the path")}
    for t in TRACKS:
        bcls, blabel = badge_map.get(t["status"], ("soon", "On the path"))
        chips = ""
        for ls in t["lessons"]:
            cls = "chip" if ls["ready"] else "chip soon"
            chips += ('<a class="%s" href="lessons/%s.html"><span class="cn">%s</span>%s</a>'
                      % (cls, ls["id"], ls.get("num", ""), B.esc(ls["title"])))
        cards.append(
            '<div class="tcard" data-status="%s">'
            '<div class="tindex">%d</div>'
            '<div><h3><a href="lessons/%s.html">%s</a>'
            '<span class="badge %s">%s</span></h3>'
            '<div class="tdesc">%s</div>'
            '<div class="chips">%s</div></div></div>'
            % (t["status"], t["num"], t["lessons"][0]["id"], B.esc(t["title"]),
               bcls, blabel, B.esc(t["desc"]), chips))
    cards.append("</div>")

    mentor = (
        '<div class="callout why" style="margin-top:30px">'
        '<div class="ctitle">&#9670; A word from your mentor</div>'
        '<p>The order matters. Most people drown because they jump to machine learning before '
        'they can read a distribution or trust a sample. We will not do that. We build the '
        'foundation until it is sturdy, then everything above it becomes easy. Take your time. '
        'Re-run the code. Get the quizzes wrong and read why. That is the work.</p></div>')

    foot = ('<div class="foot"><p><b>Data Science Mentor.</b> A self-paced course built for '
            'understanding. Open <code class="inline">index.html</code> any time to return here. '
            'Code runs in your browser (click <b>Run</b>) or in the matching notebooks under '
            '<code class="inline">/notebooks</code>.</p></div>')

    return hero + stats + how + "".join(cards) + mentor + foot

sidebar_home = B.render_sidebar(TRACKS, None, "lessons/", "index.html")
home_html = B.page("Data Science Mentor — zero to job-ready", home_inner(),
                   sidebar_home, "", desc="A self-paced, gold-standard path from zero to a "
                   "job-ready data scientist: statistics, Python, ML, experimentation, and more.")
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(home_html)

print("Built %d lesson pages + homepage into %s" % (len(FLAT), ROOT))
