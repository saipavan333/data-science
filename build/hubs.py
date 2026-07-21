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


# ---------------------------------------------------------- Path to Mastery
def roadmap_inner():
    head = _hub_head(
        "Resource &middot; Your path",
        "The Path to Mastery",
        "The best data scientists in the world aren't the ones who know the most &mdash; they're the "
        "ones who've <b>shipped</b> the most, <b>explained</b> the most, and practiced at the edge of "
        "their ability for years. This course gives you the knowledge. This page gives you the "
        "<b>path</b>: how to turn 107 lessons into real mastery, and mastery into a career the field "
        "notices. Read it once now &mdash; then come back every month.",
        '<div class="hub-stats"><span><b>3</b> phases</span><span><b>6</b> portfolio projects</span>'
        '<span><b>1</b> habit that beats them all: consistency</span></div>')

    # --- three phases ---
    phases = [
        ("1", "Foundations", "Learn to see", "~8&ndash;12 weeks", "Tracks 1&ndash;5",
         "Python, SQL, statistics, EDA &mdash; the senses of a data scientist.",
         ["Pull and join data in SQL without reaching for the docs",
          "Clean and explore any dataset in pandas fluently",
          "Read a distribution, a confidence interval, and a p-value &mdash; and explain each in plain English",
          "Spot an outlier, a skew, and a misleading chart on sight"], "p1"),
        ("2", "Practitioner", "Learn to decide &amp; build", "~12&ndash;16 weeks", "Tracks 6&ndash;11",
         "Experimentation, causal inference, machine learning, feature engineering, evaluation, MLOps.",
         ["Design and analyse an A/B test end to end, and defend the call",
          "Tell correlation from causation &mdash; and know how to estimate a real effect",
          "Build a <b>leakage-free</b> model and evaluate it <b>honestly</b> (not with accuracy)",
          "Explain how you'd serve, monitor, and retrain it in production"], "p2"),
        ("3", "Professional &amp; beyond", "Learn to matter", "Ongoing", "Tracks 12&ndash;14 + real work",
         "Communication, capstones, interviews &mdash; then the real world, which never ends.",
         ["Turn a model into a decision a stakeholder will fund",
          "Walk into any data-science interview calm",
          "Ship 3+ real portfolio projects people can see",
          "Keep learning at the edge &mdash; the best never graduate"], "p3"),
    ]
    pcards = ""
    for num, name, tag, dur, tracks, desc, checks, cls in phases:
        li = "".join('<li>%s</li>' % c for c in checks)
        pcards += (
            '<div class="phase %s"><div class="phase-top"><span class="phase-n">%s</span>'
            '<div><div class="phase-name">%s</div><div class="phase-tag">%s</div></div></div>'
            '<div class="phase-meta"><span>%s</span><span>%s</span></div>'
            '<p class="phase-desc">%s</p>'
            '<div class="phase-check-h">You&rsquo;ve cleared it when you can:</div>'
            '<ul class="phase-check">%s</ul></div>' % (cls, num, name, tag, tracks, dur, desc, li))
    phases_sec = ('<section class="hub-sec"><h2 class="road-h2">The journey, in three phases</h2>'
                  '<p class="road-lead">Don&rsquo;t rush the foundations to reach the exciting parts &mdash; '
                  'everyone who does ends up stuck. Build each phase until it&rsquo;s sturdy, and the next '
                  'becomes easy.</p><div class="phase-grid">%s</div></section>' % pcards)

    # --- how to study ---
    steps = [
        ("Run everything, don&rsquo;t just read", "Do every lab. Execute every code block. Change the numbers and break it &mdash; understanding lives in your fingers, not your eyes."),
        ("Get the quizzes wrong on purpose", "A wrong answer you understand teaches more than a right one you guessed. Read <i>why</i> every option is wrong."),
        ("Hold the interview bar", "After each lesson ask: <b>&ldquo;Could I explain this to a smart friend, and pass an interview question on it?&rdquo;</b> If not, you haven&rsquo;t learned it yet."),
        ("Teach it back", "Write a paragraph, a post, or explain it out loud. Teaching is the fastest route to mastery &mdash; and, later, to being known."),
        ("Space it", "Use the flashcards. Review last week&rsquo;s tracks while learning this week&rsquo;s. Memory is built by <b>returning</b>, not cramming."),
    ]
    steps_html = "".join('<div class="mstep"><div class="mstep-n">%d</div><div><h4>%s</h4><p>%s</p></div></div>'
                         % (i + 1, s[0], s[1]) for i, s in enumerate(steps))
    study_sec = ('<section class="hub-sec"><h2 class="road-h2">How to study a lesson for <em>mastery</em></h2>'
                 '<p class="road-lead">Passive reading feels like progress and produces almost none. This is '
                 'the loop that actually sticks &mdash; and <b>60&ndash;90 focused minutes a day beats a '
                 'ten-hour Saturday binge</b> every time. Consistency compounds; intensity fades.</p>'
                 '<div class="mstep-list">%s</div></section>' % steps_html)

    # --- portfolio project ladder ---
    projects = [
        ("EDA &amp; insight report", "Beginner", "Take a public dataset (Kaggle, data.gov) and produce a clean notebook plus a <b>one-page write-up ending in a real recommendation</b>. Shows you can find signal and communicate it."),
        ("A/B test analysis", "Beginner+", "Design, power, and analyse an experiment (real or simulated): metric, hypothesis, sample size, test, and a <b>go/no-go call with guardrails</b>. Shows product judgement."),
        ("End-to-end model, honestly evaluated", "Intermediate", "Frame a problem, audit for leakage, build a Pipeline, evaluate on the <b>right</b> metrics, tune the threshold to costs, and interpret it with SHAP. The core of the job."),
        ("Causal study", "Intermediate+", "Estimate a real effect from observational data with diff-in-differences or matching &mdash; and <b>defend the assumption</b> it rests on. Almost no junior can do this; it sets you apart."),
        ("Shipped mini-product", "Advanced", "Put a model behind a small web app (Streamlit / FastAPI) that a stranger can actually use, with basic monitoring. Turning a notebook into software is the leap most never make."),
        ("Your signature project", "Advanced+", "Something in a domain you genuinely love, that shows <b>judgement</b>, not just skill. This is the one that gets remembered in interviews."),
    ]
    pj = ""
    for i, (name, level, desc) in enumerate(projects):
        pj += ('<div class="proj"><div class="proj-h"><span class="proj-n">%02d</span>'
               '<span class="proj-level">%s</span></div><div class="proj-name">%s</div>'
               '<p class="proj-desc">%s</p></div>' % (i + 1, level, name, desc))
    proj_sec = ('<section class="hub-sec"><h2 class="road-h2">The portfolio ladder &mdash; what actually gets you hired</h2>'
                '<p class="road-lead">Nobody is hired for the courses they finished; they&rsquo;re hired for '
                'what they&rsquo;ve <b>built and shown</b>. Climb this ladder alongside the tracks. <b>The '
                'rule:</b> every project lives on GitHub with a README that leads with the <b>result</b>, not '
                'the method &mdash; a recruiter should get the point in 30 seconds.</p>'
                '<div class="proj-grid">%s</div></section>' % pj)

    # --- learn in public + compete ---
    flywheel = [
        ("Commit in public", "A green GitHub history <i>is</i> a r&eacute;sum&eacute;. Real READMEs, small frequent commits."),
        ("Write one post per project", "&ldquo;What I built, what I learned.&rdquo; This is how people <b>find</b> you &mdash; it compounds for years."),
        ("Compete on Kaggle", "Even a top-20% finish teaches more than a course &mdash; then <b>read the winners&rsquo; solutions</b>. Free mentorship from the best on Earth."),
        ("Teach beginners", "Answer questions, explain concepts. Explaining forces mastery and quietly builds your reputation."),
    ]
    fw = "".join('<div class="fly"><div class="fly-name">%s</div><p>%s</p></div>' % (f[0], f[1]) for f in flywheel)
    public_sec = ('<section class="hub-sec"><h2 class="road-h2">Learn in public &mdash; the flywheel that makes you <em>known</em></h2>'
                  '<p class="road-lead">Two people with equal skill are not equal: the one who <b>builds in the '
                  'open</b> gets the opportunities. The loop is simple &mdash; <b>build &rarr; write &rarr; share '
                  '&rarr; get feedback &rarr; build better.</b> Run it twenty times and you&rsquo;re not '
                  'job-ready, you&rsquo;re <b>sought</b>.</p><div class="fly-grid">%s</div></section>' % fw)

    # --- specialization forks ---
    forks = [
        ("ML Engineer", "Production systems, scale, reliability.", "Double down on Feature Eng, Evaluation, MLOps + real software engineering.", "teal"),
        ("Applied Scientist / Research", "Depth, novel methods, papers.", "Go deep in Statistics, Causal, ML + mathematics + reading and reproducing papers.", "indigo"),
        ("Product / Analytics DS", "Metrics, experiments, influence.", "Master EDA, Experimentation, Communication + sharp business sense.", "amber"),
        ("GenAI / LLM Engineer", "The frontier: RAG, agents, evals.", "Fundamentals still rule, then add retrieval, fine-tuning, and evaluation of LLM systems.", "rose"),
    ]
    fk = ""
    for name, tag, how, col in forks:
        fk += ('<div class="fork fork-%s"><div class="fork-name">%s</div>'
               '<div class="fork-tag">%s</div><p>%s</p></div>' % (col, name, tag, how))
    fork_sec = ('<section class="hub-sec"><h2 class="road-h2">Then go deep &mdash; specialization forks</h2>'
                '<p class="road-lead">Broad foundations first &mdash; then pick <b>one thing to be known '
                'for</b> and go deeper than everyone around you, while staying literate in the rest. Generalists '
                'get interviews; specialists get chosen.</p><div class="fork-grid">%s</div></section>' % fk)

    # --- weekly cadence ---
    cadence = [
        ("Mon&ndash;Fri", "60&ndash;90 min", "One lesson a day &mdash; every lab run, every quiz attempted, mark it complete."),
        ("Twice a week", "20 min", "Flashcard review of <b>earlier</b> tracks, so nothing fades."),
        ("Saturday", "2&ndash;3 hrs", "Push your current <b>portfolio project</b> forward. Building, not consuming."),
        ("Sunday", "30 min", "Write a paragraph on what you learned, plan next week &mdash; then rest. Rest is part of the work."),
        ("Monthly", "&mdash;", "Reread this page, <b>ship one project</b>, and publish one thing."),
    ]
    cd = "".join('<div class="cad-row"><span class="cad-when">%s</span><span class="cad-dur">%s</span>'
                 '<span class="cad-what">%s</span></div>' % (c[0], c[1], c[2]) for c in cadence)
    cadence_sec = ('<section class="hub-sec"><h2 class="road-h2">A realistic weekly rhythm</h2>'
                   '<p class="road-lead">You don&rsquo;t need heroics. You need a rhythm you can keep for a '
                   'year. This is one that works:</p><div class="cad">%s</div></section>' % cd)

    # --- elite habits ---
    habits = [
        ("Verify, don&rsquo;t assume", "Recompute the number a second way. Distrust a result that looks too good. &ldquo;Should work&rdquo; is a draft, not a result."),
        ("Communicate", "The model is half the job; the <b>decision it drives</b> is the other half. Lead with the answer."),
        ("Stay slightly out of your depth", "Comfort is where growth stops. Always be reaching for the thing just past your reach."),
        ("Teach", "The fastest way to master something &mdash; and the surest way to become someone the field knows."),
        ("Show up", "The person who does 90 minutes daily for two years beats the genius who binges twice a month. It isn&rsquo;t close."),
    ]
    hb = "".join('<div class="habit"><h4>%s</h4><p>%s</p></div>' % (h[0], h[1]) for h in habits)
    habit_sec = ('<section class="hub-sec"><h2 class="road-h2">The habits that actually separate the top</h2>'
                 '<div class="habit-grid">%s</div></section>' % hb)

    charge = (
        '<section class="road-charge"><div class="charge-kicker">A word from your mentor</div>'
        '<p>Here&rsquo;s the honest truth: this course can make you <b>knowledgeable</b>, but only you can '
        'make yourself the <b>best</b> &mdash; by shipping, explaining, and practicing when it&rsquo;s boring '
        'and no one is watching. Knowledge is the easy 20%. The 80% is the <b>doing</b>, done consistently, '
        'in public, for years.</p>'
        '<p>You already have the rarest thing of all &mdash; the drive that built this whole course. Point '
        'that same energy at real projects and real audiences and you won&rsquo;t just get a job; '
        'you&rsquo;ll become someone the field <b>knows</b>.</p>'
        '<p class="charge-final">So start today. Pick a dataset. Open a lesson. Ship something small and '
        'ugly and real. Then do it again tomorrow. That&rsquo;s the whole secret &mdash; and you&rsquo;re '
        'already the kind of person who can keep it.</p></section>')

    return ('<div class="hub road-page">%s%s%s%s%s%s%s%s%s</div>'
            % (head, phases_sec, study_sec, proj_sec, public_sec, fork_sec, cadence_sec, habit_sec, charge))
