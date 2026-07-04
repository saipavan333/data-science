# -*- coding: utf-8 -*-
"""
make_visuals.py — generate every diagram & chart for Track 1 (and the capstone).

Structural diagrams (workflows, taxonomies, decision trees) are rendered with
Graphviz; data charts with matplotlib. Everything is saved as PNG to
assets/img/ so each visual can be opened and visually inspected.
"""
import os, subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(os.path.dirname(HERE), "assets", "img")
os.makedirs(IMG, exist_ok=True)

# ---- palette (matches the site CSS) --------------------------------------- #
INDIGO, INDIGO_DK, INDIGO_BG = "#3b53d6", "#2a3da6", "#eef1fd"
TEAL, TEAL_BG = "#0e8f8a", "#e3f5f3"
AMBER, AMBER_BG = "#b7791f", "#fbf3e0"
ROSE, ROSE_BG = "#c2305a", "#fce8ee"
GREEN, GREEN_BG = "#1f8a4c", "#e6f5ec"
INK, INK_SOFT, INK_FAINT = "#1f2430", "#4a5160", "#79808f"
LINE = "#d8dce3"

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "font.size": 12.5, "font.family": "DejaVu Sans",
    "axes.edgecolor": INK_SOFT, "axes.linewidth": 1.0,
    "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlecolor": INK,
    "axes.labelcolor": INK_SOFT, "xtick.color": INK_SOFT, "ytick.color": INK_SOFT,
    "axes.grid": True, "grid.color": "#edeff3", "grid.linewidth": 1,
    "figure.dpi": 150, "savefig.dpi": 150, "savefig.bbox": "tight",
})

def despine(ax, left=True, bottom=True):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(left)
    ax.spines["bottom"].set_visible(bottom)

def save(fig, name):
    path = os.path.join(IMG, name)
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print("  chart  ->", name)

# ---- Graphviz helper ------------------------------------------------------ #
GV_HEAD = '''digraph G {
  graph [bgcolor="white", fontname="Helvetica", rankdir=%s, ranksep=%s, nodesep=%s, pad=0.25];
  node  [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=12,
         color="%s", fillcolor="%s", fontcolor="%s", margin="0.20,0.12", penwidth=1.3];
  edge  [color="#8a93a6", penwidth=1.4, arrowsize=0.85, fontname="Helvetica",
         fontsize=10.5, fontcolor="%s"];
'''

def dot(body, name, rankdir="TB", ranksep="0.55", nodesep="0.4",
        ncolor="#cdd7fb", nfill=INDIGO_BG, nfont=INK):
    src = (GV_HEAD % (rankdir, ranksep, nodesep, ncolor, nfill, nfont, INK_SOFT)) + body + "\n}\n"
    p = subprocess.run(["dot", "-Tpng", "-Gdpi=170"], input=src.encode(),
                       capture_output=True)
    if p.returncode != 0:
        raise RuntimeError("graphviz error for %s:\n%s" % (name, p.stderr.decode()))
    with open(os.path.join(IMG, name), "wb") as f:
        f.write(p.stdout)
    print("  diagram->", name)

np.random.seed(7)

# ========================================================================== #
#  LESSON 1.1 — the data science workflow                                    #
# ========================================================================== #
def v_workflow():
    body = '''
  Q  [label="1. Question\\n(a decision to inform)", fillcolor="%s", color="#cdd7fb"];
  D  [label="2. Get data", fillcolor="%s", color="#cdd7fb"];
  C  [label="3. Clean &\\nprepare", fillcolor="%s", color="#cdd7fb"];
  E  [label="4. Explore\\n(EDA)", fillcolor="%s", color="#bfe7e3"];
  M  [label="5. Model /\\ntest", fillcolor="%s", color="#bfe7e3"];
  I  [label="6. Interpret\\n(quantify uncertainty)", fillcolor="%s", color="#bfe7e3"];
  A  [label="7. Communicate\\n& decide", fillcolor="%s", color="#cdd7fb"];
  Q -> D -> C -> E -> M -> I -> A;
  A -> Q [label="  new questions", style=dashed, constraint=false, color="#b6bccb"];
''' % (INDIGO_BG, INDIGO_BG, INDIGO_BG, TEAL_BG, TEAL_BG, TEAL_BG, INDIGO_BG)
    dot(body, "s1_workflow.png", rankdir="TB", ranksep="0.4", nodesep="0.3")

# ========================================================================== #
#  LESSON 1.2 — data type taxonomy + decision tree                           #
# ========================================================================== #
def v_taxonomy():
    body = '''
  Data [label="A variable\\n(one column of data)", fillcolor="#e9ecf6", color="#c7cee0"];
  Cat  [label="Categorical\\n(labels / groups)", fillcolor="%s", color="#ecd9ad"];
  Num  [label="Numerical\\n(quantities)", fillcolor="%s", color="#bfe7e3"];
  Nom  [label="Nominal\\nno natural order\\ne.g. city, browser, color", fillcolor="%s", color="#ecd9ad"];
  Ord  [label="Ordinal\\nordered labels\\ne.g. S < M < L, rating 1-5", fillcolor="%s", color="#ecd9ad"];
  Dis  [label="Discrete\\ncountable, whole\\ne.g. # of purchases", fillcolor="%s", color="#bfe7e3"];
  Con  [label="Continuous\\nmeasurable, any value\\ne.g. revenue, time on site", fillcolor="%s", color="#bfe7e3"];
  Data -> Cat; Data -> Num;
  Cat -> Nom; Cat -> Ord;
  Num -> Dis; Num -> Con;
''' % (AMBER_BG, TEAL_BG, AMBER_BG, AMBER_BG, TEAL_BG, TEAL_BG)
    dot(body, "s2_taxonomy.png", rankdir="TB", ranksep="0.5", nodesep="0.35")

def v_decision_vartype():
    body = '''
  q1 [label="Do arithmetic on it\\nthat makes sense?\\n(can you average it?)", shape=diamond,
      style="filled", fillcolor="%s", color="#ecd9ad"];
  q2 [label="Is there a\\nnatural order?", shape=diamond, style="filled",
      fillcolor="%s", color="#ecd9ad"];
  q3 [label="Only whole\\ncounts possible?", shape=diamond, style="filled",
      fillcolor="%s", color="#bfe7e3"];
  nom [label="NOMINAL\\n(unordered category)", fillcolor="%s", color="#ecd9ad"];
  ord [label="ORDINAL\\n(ordered category)", fillcolor="%s", color="#ecd9ad"];
  dis [label="DISCRETE\\n(count)", fillcolor="%s", color="#bfe7e3"];
  con [label="CONTINUOUS\\n(measurement)", fillcolor="%s", color="#bfe7e3"];
  q1 -> q2 [label="No"];
  q1 -> q3 [label="Yes"];
  q2 -> nom [label="No"];
  q2 -> ord [label="Yes"];
  q3 -> dis [label="Yes"];
  q3 -> con [label="No"];
''' % (AMBER_BG, AMBER_BG, TEAL_BG, AMBER_BG, AMBER_BG, TEAL_BG, TEAL_BG)
    dot(body, "s2_decision.png", rankdir="TB", ranksep="0.5", nodesep="0.55")

# ========================================================================== #
#  LESSON 1.3 — center & spread                                              #
# ========================================================================== #
def v_mean_median():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3))
    # symmetric
    x = np.random.normal(50, 10, 4000)
    ax = axes[0]
    ax.hist(x, bins=40, color=INDIGO_BG, edgecolor=INDIGO, linewidth=.6)
    ax.axvline(np.mean(x), color=INDIGO_DK, lw=2.4, label="Mean = %.1f" % np.mean(x))
    ax.axvline(np.median(x), color=TEAL, lw=2.4, ls="--", label="Median = %.1f" % np.median(x))
    ax.set_title("Symmetric: mean ≈ median")
    ax.legend(frameon=False, fontsize=11)
    ax.set_yticks([]); despine(ax, left=False)
    ax.set_xlabel("Exam score")
    # right-skewed (incomes)
    y = np.random.lognormal(mean=10.3, sigma=0.55, size=4000) / 1000
    y = y[y < 200]
    ax = axes[1]
    ax.hist(y, bins=50, color=AMBER_BG, edgecolor=AMBER, linewidth=.6)
    ax.axvline(np.mean(y), color=ROSE, lw=2.4, label="Mean = %.0fk" % np.mean(y))
    ax.axvline(np.median(y), color=TEAL, lw=2.4, ls="--", label="Median = %.0fk" % np.median(y))
    ax.set_title("Right-skewed: mean > median")
    ax.legend(frameon=False, fontsize=11)
    ax.set_yticks([]); despine(ax, left=False)
    ax.set_xlabel("Household income ($000s)")
    ax.annotate("a few large incomes\npull the mean right", xy=(np.mean(y), 230),
                xytext=(np.mean(y) + 45, 360), fontsize=10.5, color=INK_SOFT,
                ha="center", arrowprops=dict(arrowstyle="->", color=INK_FAINT, lw=1.3))
    fig.suptitle("The mean follows the tail; the median resists it",
                 fontsize=15, fontweight="bold", color=INK, y=1.02)
    save(fig, "s3_mean_median.png")

def v_boxplot():
    fig, ax = plt.subplots(figsize=(11, 4.3))
    data = np.concatenate([np.random.normal(60, 12, 300), [108, 112, 15]])
    ax.boxplot(data, vert=False, widths=0.5, patch_artist=True,
               medianprops=dict(color=ROSE, lw=2.6),
               boxprops=dict(facecolor=INDIGO_BG, edgecolor=INDIGO, lw=1.6),
               whiskerprops=dict(color=INK_SOFT, lw=1.5),
               capprops=dict(color=INK_SOFT, lw=1.5),
               flierprops=dict(marker="o", markerfacecolor=ROSE, markeredgecolor=ROSE,
                               markersize=6, alpha=.7))
    q1, med, q3 = np.percentile(data, [25, 50, 75])
    iqr = q3 - q1
    right_cap = data[data <= q3 + 1.5 * iqr].max()
    ax.set_ylim(0.3, 2.12); ax.set_xlim(0, 120); ax.set_yticks([])
    despine(ax, left=False, bottom=True)
    box_top = 1.25
    def lab(x, text, tx, ty, color=INK_SOFT):
        ax.annotate(text, xy=(x, box_top + .01), xytext=(tx, ty), ha="center",
                    fontsize=10.5, color=color,
                    arrowprops=dict(arrowstyle="->", color=INK_FAINT, lw=1.2))
    lab(med, "Median = %.0f\n(50th pct)" % med, 60, 1.95, ROSE)
    lab(q1, "Q1 = %.0f\n(25th pct)" % q1, 42, 1.72)
    lab(q3, "Q3 = %.0f\n(75th pct)" % q3, 81, 1.72)
    ax.annotate("whisker: last point\nwithin 1.5×IQR of the box", xy=(right_cap, 1.07),
                xytext=(101, 1.55), fontsize=9.8, color=INK_SOFT, ha="center",
                arrowprops=dict(arrowstyle="->", color=INK_FAINT, lw=1.1))
    ax.annotate("", xy=(q1, 0.64), xytext=(q3, 0.64),
                arrowprops=dict(arrowstyle="<->", color=TEAL, lw=2))
    ax.text((q1 + q3) / 2, 0.5, "IQR = Q3 − Q1 = %.0f" % iqr, ha="center",
            color=TEAL, fontsize=11, fontweight="bold")
    ax.annotate("outliers\n(beyond 1.5×IQR)", xy=(110, 0.93), xytext=(96, 0.5),
                fontsize=10, color=ROSE, ha="center",
                arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.2))
    ax.set_title("Anatomy of a boxplot", loc="left")
    ax.set_xlabel("Customer age")
    save(fig, "s3_boxplot.png")

def v_spread():
    fig, ax = plt.subplots(figsize=(10.5, 4.3))
    xs = np.linspace(20, 80, 600)
    for sd, c, cb, name in [(4, TEAL, TEAL_BG, "Team A: SD = 4 (consistent)"),
                            (11, ROSE, ROSE_BG, "Team B: SD = 11 (erratic)")]:
        y = np.exp(-0.5 * ((xs - 50) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
        ax.plot(xs, y, color=c, lw=2.4, label=name)
        ax.fill_between(xs, y, where=(xs >= 50 - sd) & (xs <= 50 + sd), color=cb, alpha=.7)
    ax.axvline(50, color=INK_SOFT, lw=1.4, ls=":")
    ax.text(50, ax.get_ylim()[1] * .97, "same mean = 50", ha="center", va="top",
            fontsize=10.5, color=INK_SOFT)
    ax.set_title("Same average, very different spread", loc="left")
    ax.set_xlabel("Delivery time (minutes)"); ax.set_yticks([])
    ax.legend(frameon=False, fontsize=11, loc="upper right")
    despine(ax, left=False)
    save(fig, "s3_spread.png")

# ========================================================================== #
#  LESSON 1.4 — probability                                                  #
# ========================================================================== #
def v_venn():
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    ax.add_patch(Circle((-0.55, 0), 1.25, color=INDIGO, alpha=.22))
    ax.add_patch(Circle((0.55, 0), 1.25, color=TEAL, alpha=.22))
    ax.add_patch(Circle((-0.55, 0), 1.25, fill=False, ec=INDIGO, lw=2))
    ax.add_patch(Circle((0.55, 0), 1.25, fill=False, ec=TEAL, lw=2))
    ax.text(-1.35, 1.05, "A", fontsize=20, color=INDIGO_DK, fontweight="bold")
    ax.text(1.25, 1.05, "B", fontsize=20, color=TEAL, fontweight="bold")
    ax.text(-1.0, 0, "only A", ha="center", fontsize=12, color=INK_SOFT)
    ax.text(1.0, 0, "only B", ha="center", fontsize=12, color=INK_SOFT)
    ax.text(0, 0, "A ∩ B", ha="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(0, -1.75, "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)",
            ha="center", fontsize=14, color=INK)
    ax.text(0, -2.15, "subtract the overlap so it isn't counted twice",
            ha="center", fontsize=10.5, color=INK_FAINT, style="italic")
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 1.7)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Union, intersection, and not double-counting", color=INK)
    save(fig, "s4_venn.png")

def v_prob_tree():
    body = f'''
  P0 [label="1,000 people", fillcolor="#e9ecf6", color="#c7cee0"];
  S  [label="Has disease\\n1% of 1000 = 10", fillcolor="{ROSE_BG}", color="#e7b9c6"];
  H  [label="No disease\\n99% of 1000 = 990", fillcolor="{TEAL_BG}", color="#bfe7e3"];
  Sp [label="Tests +\\n90% of 10 = 9", fillcolor="{ROSE_BG}", color="#e7b9c6"];
  Sn [label="Tests −\\n1", fillcolor="#f4f5f8", color="#d8dce3"];
  Hp [label="Tests +\\n5% of 990 = 49.5", fillcolor="{ROSE_BG}", color="#e7b9c6"];
  Hn [label="Tests −\\n940.5", fillcolor="#f4f5f8", color="#d8dce3"];
  P0 -> S [label="prior 1%"];
  P0 -> H [label="99%"];
  S -> Sp [label="sensitivity 90%"];
  S -> Sn;
  H -> Hp [label="false-pos 5%"];
  H -> Hn;
'''
    dot(body, "s4_tree.png", rankdir="LR", ranksep="0.7", nodesep="0.3")

def v_bayes_bar():
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    true_pos, false_pos = 9, 49.5
    ax.barh([1], [true_pos], color=ROSE, edgecolor="white", label="Actually sick (9)")
    ax.barh([1], [false_pos], left=[true_pos], color="#f0c6d2", edgecolor="white",
            label="Healthy, false alarm (49.5)")
    ax.set_xlim(0, 60); ax.set_ylim(0.4, 1.6); ax.set_yticks([])
    ax.set_title("Of everyone who tests positive, how many are truly sick?", loc="left")
    despine(ax, left=False)
    ax.text(true_pos / 2, 1, "9", ha="center", va="center", color="white", fontweight="bold")
    ax.text(true_pos + false_pos / 2, 1, "49.5", ha="center", va="center",
            color=ROSE, fontweight="bold")
    ppv = true_pos / (true_pos + false_pos)
    ax.annotate("Only %.0f%% of positives\nare real (PPV)\n— because the disease is rare"
                % (100 * ppv), xy=(9, 1.32), xytext=(24, 1.34), fontsize=11, color=INK,
                ha="left", arrowprops=dict(arrowstyle="->", color=INK_FAINT, lw=1.3))
    ax.legend(frameon=False, fontsize=10.5, loc="lower right")
    ax.set_xlabel("Number of people (out of the ~58 who test positive)")
    save(fig, "s4_bayes.png")

# ========================================================================== #
#  LESSON 1.5 — distributions                                               #
# ========================================================================== #
def v_pmf_pdf():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    ax = axes[0]
    k = np.arange(0, 7)
    from math import comb
    p = [comb(6, i) * .5 ** 6 for i in k]
    ax.bar(k, p, color=INDIGO_BG, edgecolor=INDIGO, lw=1.3, width=.7)
    ax.set_title("Discrete → PMF\n(height = probability of each value)", fontsize=12.5)
    ax.set_xlabel("Heads in 6 coin flips"); ax.set_ylabel("Probability")
    despine(ax, left=False)
    ax = axes[1]
    xs = np.linspace(-4, 4, 400)
    y = np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi)
    ax.plot(xs, y, color=TEAL, lw=2.4)
    ax.fill_between(xs, y, where=(xs >= 0.5) & (xs <= 1.5), color=TEAL_BG)
    ax.set_title("Continuous → PDF\n(area = probability over a range)", fontsize=12.5)
    ax.set_xlabel("Standardized measurement"); ax.set_ylabel("Density")
    ax.annotate("P(0.5 < x < 1.5)\n= shaded area", xy=(1.0, .12), xytext=(1.8, .3),
                fontsize=10.5, color=INK_SOFT,
                arrowprops=dict(arrowstyle="->", color=INK_FAINT, lw=1.2))
    despine(ax, left=False)
    fig.suptitle("Two kinds of distribution: bars for counts, curves for measurements",
                 fontsize=14, fontweight="bold", y=1.04, color=INK)
    save(fig, "s5_pmf_pdf.png")

def v_normal_empirical():
    fig, ax = plt.subplots(figsize=(10.5, 4.6))
    xs = np.linspace(-4, 4, 600)
    y = np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi)
    ax.plot(xs, y, color=INDIGO_DK, lw=2.4)
    bands = [(-1, 1, TEAL, "68%"), (-2, -1, INDIGO, "13.5%"), (1, 2, INDIGO, "13.5%"),
             (-3, -2, AMBER, "2.35%"), (2, 3, AMBER, "2.35%")]
    for a, b, c, _ in bands:
        ax.fill_between(xs, y, where=(xs >= a) & (xs <= b), color=c, alpha=.20)
    for x in range(-3, 4):
        ax.axvline(x, color=INK_FAINT, lw=.8, ls=":")
    ax.text(0, .18, "68%", ha="center", color=TEAL, fontsize=13, fontweight="bold")
    ax.text(1.5, .06, "13.5%", ha="center", color=INDIGO_DK, fontsize=10.5)
    ax.text(-1.5, .06, "13.5%", ha="center", color=INDIGO_DK, fontsize=10.5)
    ax.text(2.5, .018, "2.35%", ha="center", color=AMBER, fontsize=9.5)
    ax.text(-2.5, .018, "2.35%", ha="center", color=AMBER, fontsize=9.5)
    ax.set_xticks(range(-3, 4))
    ax.set_xticklabels(["−3σ", "−2σ", "−1σ", "μ",
                        "+1σ", "+2σ", "+3σ"])
    ax.set_yticks([])
    ax.set_title("The normal distribution and the 68–95–99.7 rule", loc="left")
    ax.set_xlabel("Distance from the mean, in standard deviations")
    despine(ax, left=False)
    save(fig, "s5_normal_empirical.png")

def v_binomial():
    from math import comb
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.7), sharey=True)
    n = 10
    for ax, pp, c, cb in zip(axes, [0.2, 0.5, 0.8],
                             [TEAL, INDIGO, AMBER], [TEAL_BG, INDIGO_BG, AMBER_BG]):
        k = np.arange(0, n + 1)
        pmf = [comb(n, i) * pp ** i * (1 - pp) ** (n - i) for i in k]
        ax.bar(k, pmf, color=cb, edgecolor=c, lw=1.3)
        ax.set_title("p = %.1f" % pp, fontsize=12.5, color=c)
        ax.set_xlabel("successes in 10")
        despine(ax, left=(ax is axes[0]))
        ax.set_xticks(range(0, 11, 2))
    axes[0].set_ylabel("Probability")
    fig.suptitle("Binomial(n=10, p): count of successes in a fixed number of trials",
                 fontsize=14, fontweight="bold", y=1.05, color=INK)
    save(fig, "s5_binomial.png")

def v_poisson():
    from math import factorial, exp
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.7), sharey=True)
    for ax, lam, c, cb in zip(axes, [1, 3, 7],
                              [TEAL, INDIGO, ROSE], [TEAL_BG, INDIGO_BG, ROSE_BG]):
        k = np.arange(0, 18)
        pmf = [exp(-lam) * lam ** i / factorial(i) for i in k]
        ax.bar(k, pmf, color=cb, edgecolor=c, lw=1.2)
        ax.set_title("λ = %d / hour" % lam, fontsize=12.5, color=c)
        ax.set_xlabel("events in an hour")
        despine(ax, left=(ax is axes[0]))
    axes[0].set_ylabel("Probability")
    fig.suptitle("Poisson(λ): count of independent events in a fixed interval",
                 fontsize=14, fontweight="bold", y=1.05, color=INK)
    save(fig, "s5_poisson.png")

def v_dist_chooser():
    body = '''
  q0 [label="Is the variable\\ndiscrete or continuous?", shape=diamond, style="filled",
      fillcolor="#e9ecf6", color="#c7cee0"];
  qd [label="What are you\\ncounting?", shape=diamond, style="filled",
      fillcolor="%s", color="#bfe7e3"];
  qc [label="What does the\\nshape look like?", shape=diamond, style="filled",
      fillcolor="%s", color="#ecd9ad"];
  bin [label="BINOMIAL (n, p)\\nsuccesses in n trials\\ne.g. 3 of 10 emails opened", fillcolor="%s", color="#bfe7e3"];
  poi [label="POISSON (λ)\\nevents per interval\\ne.g. support tickets / hour", fillcolor="%s", color="#bfe7e3"];
  nor [label="NORMAL (μ, σ)\\nsymmetric bell\\ne.g. heights, measurement error", fillcolor="%s", color="#ecd9ad"];
  exp [label="EXPONENTIAL (λ)\\ntime until an event, right-skewed\\ne.g. time between sign-ups", fillcolor="%s", color="#ecd9ad"];
  uni [label="UNIFORM (a, b)\\nevery value equally likely\\ne.g. a fair random pick", fillcolor="%s", color="#ecd9ad"];
  q0 -> qd [label="Discrete\\n(counts)"];
  q0 -> qc [label="Continuous\\n(measures)"];
  qd -> bin [label="successes\\nin fixed n"];
  qd -> poi [label="events in\\nan interval"];
  qc -> nor [label="bell-shaped"];
  qc -> exp [label="wait time /\\nright-skewed"];
  qc -> uni [label="flat"];
''' % (TEAL_BG, AMBER_BG, TEAL_BG, TEAL_BG, AMBER_BG, AMBER_BG, AMBER_BG)
    dot(body, "s5_chooser.png", rankdir="TB", ranksep="0.6", nodesep="0.35")

if __name__ == "__main__":
    print("Generating Track 1 visuals into", IMG)
    v_workflow()
    v_taxonomy(); v_decision_vartype()
    v_mean_median(); v_boxplot(); v_spread()
    v_venn(); v_prob_tree(); v_bayes_bar()
    v_pmf_pdf(); v_normal_empirical(); v_binomial(); v_poisson(); v_dist_chooser()
    print("Done.")
