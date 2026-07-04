import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from vstyle import *
np.random.seed(7)

# 1.8 (a) confidence interval coverage — the canonical CI picture
mu, sigma, n = 100.0, 15.0, 40
se = sigma/np.sqrt(n); K = 25
fig, ax = plt.subplots(figsize=(10.5, 5.2))
miss = 0
for i in range(K):
    s = np.random.normal(mu, sigma, n); m = s.mean()
    lo, hi = m-1.96*se, m+1.96*se
    covers = lo <= mu <= hi
    miss += (not covers)
    c = INDIGO if covers else ROSE
    ax.plot([lo,hi],[i,i], color=c, lw=2.4, solid_capstyle="round")
    ax.plot(m, i, "o", color=c, ms=4)
ax.axvline(mu, color=INK, lw=1.8, ls="--")
ax.text(mu, K+0.4, "true mean μ (usually unknown)", ha="center", color=INK, fontsize=11)
ax.set_yticks([]); despine(ax, left=False)
ax.set_xlabel("estimated mean with 95% confidence interval")
ax.set_title(f"What '95% confidence' means: {K-miss} of {K} intervals catch the truth",
             loc="left")
ax.text(0.015, 0.04, f"{miss} miss (red) ≈ the 5% we expect to miss",
        transform=ax.transAxes, color=ROSE, fontsize=10.5)
save(fig, "s8_ci_concept.png")

# 1.8 (b) anatomy of a confidence interval / margin of error
fig, ax = plt.subplots(figsize=(10.5, 4.2))
est = 100; me = 1.96*se
xs = np.linspace(est-4*se, est+4*se, 400)
y = np.exp(-0.5*((xs-est)/se)**2); y = y/y.max()
ax.plot(xs, y, color=INDIGO_DK, lw=2.2)
ax.fill_between(xs, y, where=(xs>=est-me)&(xs<=est+me), color=INDIGO_BG)
ax.axvline(est, color=ROSE, lw=2.2)
ax.set_ylim(-0.32, 1.15); ax.set_yticks([])
despine(ax, left=False)
ax.annotate("point estimate (x̄)", xy=(est,1.0), xytext=(est, 1.12), ha="center",
            color=ROSE, fontsize=11)
# bracket
ax.plot([est-me, est+me], [-0.12,-0.12], color=INK_SOFT, lw=2)
for xx in (est-me, est+me): ax.plot([xx,xx],[-0.16,-0.08], color=INK_SOFT, lw=2)
ax.annotate("", xy=(est, -0.12), xytext=(est+me, -0.12),
            arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.8))
ax.text(est+me/2, -0.23, "margin of error\n= 1.96 × SE", ha="center", color=TEAL, fontsize=10.5)
ax.text(est-me, -0.27, f"{est-me:.0f}", ha="center", color=INK_SOFT, fontsize=10.5)
ax.text(est+me, -0.27, f"{est+me:.0f}", ha="center", color=INK_SOFT, fontsize=10.5)
ax.set_title("Anatomy of a 95% confidence interval: estimate ± margin of error", loc="left")
ax.set_xlabel("metric value")
save(fig, "s8_margin.png")

# 1.9 (a) hypothesis-testing logic (graphviz)
dot('''
 H [label="1. State hypotheses\\nH0: no effect (skeptic)\\nH1: there is an effect", fillcolor="#eef1fd", color="#cdd7fb"];
 A [label="2. Assume H0 is true\\n(innocent until proven guilty)", fillcolor="#eef1fd", color="#cdd7fb"];
 T [label="3. Compute a test statistic\\nhow far is the data from H0?", fillcolor="#e3f5f3", color="#bfe7e3"];
 P [label="4. Find the p-value\\nP(data this extreme | H0 true)", fillcolor="#e3f5f3", color="#bfe7e3"];
 D [label="p < α ?\\n(α usually 0.05)", shape=diamond, style="filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 R [label="Reject H0\\n'statistically significant'", fillcolor="#e6f5ec", color="#bfe0c8"];
 F [label="Fail to reject H0\\n(not 'H0 is true')", fillcolor="#fce8ee", color="#e7b9c6"];
 H -> A -> T -> P -> D;
 D -> R [label="yes"];
 D -> F [label="no"];
''', "s9_logic.png", rd="TB", rs="0.45", ns="0.5")

# 1.9 (b) p-value as tail area
fig, ax = plt.subplots(figsize=(10.5, 4.4))
xs = np.linspace(-4,4,500); y = np.exp(-xs**2/2)/np.sqrt(2*np.pi)
ax.plot(xs, y, color=INDIGO_DK, lw=2.2)
zobs = 2.1
ax.fill_between(xs, y, where=(xs>=zobs), color=ROSE, alpha=.55)
ax.fill_between(xs, y, where=(xs<=-zobs), color=ROSE, alpha=.55)
ax.axvline(zobs, color=ROSE, lw=2)
ax.set_yticks([]); despine(ax, left=False)
ax.set_title("The p-value is the tail area: how often pure chance beats your result", loc="left")
ax.set_xlabel("test statistic (standard errors from H0)")
ax.annotate(f"observed = {zobs} SE", xy=(zobs, 0.05), xytext=(zobs+0.3, 0.22),
            color=ROSE, fontsize=11, arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.3))
ax.text(0, 0.16, "if H0 were true,\nresults usually land here", ha="center", color=INK_SOFT, fontsize=10.5)
ax.annotate("p-value\n(both tails)", xy=(2.7, 0.012), xytext=(3.0, 0.12), color=ROSE, fontsize=10.5,
            ha="center", arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.2))
save(fig, "s9_pvalue.png")

# 1.9 (c) Type I / Type II error matrix
fig, ax = plt.subplots(figsize=(8.8, 5.0))
ax.set_xlim(0,2); ax.set_ylim(0,2); ax.axis("off")
cells = {(0,1):(GREEN_BG,GREEN,"Correct\n(true negative)"),
         (1,1):(ROSE_BG,ROSE,"TYPE I ERROR\nfalse positive (α)\nflag an effect that isn't real"),
         (0,0):(AMBER_BG,AMBER,"TYPE II ERROR\nfalse negative (β)\nmiss a real effect"),
         (1,0):(GREEN_BG,GREEN,"Correct\n(true positive)\n= POWER")}
for (col,row),(bg,fg,txt) in cells.items():
    ax.add_patch(FancyBboxPatch((col,row),0.96,0.96, boxstyle="round,pad=0.02",
                 facecolor=bg, edgecolor=fg, linewidth=1.8))
    ax.text(col+0.48, row+0.48, txt, ha="center", va="center", color=fg, fontsize=10.5, fontweight="bold")
ax.text(0.48, 2.06, "H0 actually FALSE\n(effect is real)", ha="center", fontsize=10.5, color=INK)
ax.text(1.48, 2.06, "H0 actually TRUE\n(no effect)", ha="center", fontsize=10.5, color=INK)
ax.text(-0.06, 1.48, "Reject H0", ha="right", va="center", fontsize=10.5, color=INK, rotation=90)
ax.text(-0.06, 0.48, "Fail to\nreject H0", ha="right", va="center", fontsize=10.5, color=INK, rotation=90)
ax.set_title("Two ways to be wrong: Type I and Type II errors", loc="center", fontsize=14)
save(fig, "s9_errors.png")

# 1.9 (d) power diagram
fig, ax = plt.subplots(figsize=(10.5, 4.6))
xs = np.linspace(-4,7,700)
h0 = np.exp(-0.5*xs**2)/np.sqrt(2*np.pi)
delta = 3.0
h1 = np.exp(-0.5*(xs-delta)**2)/np.sqrt(2*np.pi)
crit = 1.645
ax.plot(xs, h0, color=INDIGO_DK, lw=2); ax.plot(xs, h1, color=TEAL, lw=2)
ax.fill_between(xs, h0, where=(xs>=crit), color=ROSE, alpha=.5)
ax.fill_between(xs, h1, where=(xs<=crit), color=AMBER, alpha=.45)
ax.fill_between(xs, h1, where=(xs>=crit), color=GREEN, alpha=.30)
ax.axvline(crit, color=INK_SOFT, lw=1.6, ls="--")
ax.text(0, 0.43, "H0\n(no effect)", ha="center", color=INDIGO_DK, fontsize=10.5)
ax.text(delta, 0.43, "H1\n(real effect)", ha="center", color=TEAL, fontsize=10.5)
ax.text(crit, -0.045, "critical value", ha="center", color=INK_SOFT, fontsize=9.5)
ax.annotate("α: Type I\n(false alarm)", xy=(2.0,0.02), xytext=(2.0,0.20), color=ROSE, fontsize=10,
            ha="center", arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.2))
ax.annotate("β: Type II\n(missed effect)", xy=(0.9,0.02), xytext=(-1.8,0.22), color=AMBER, fontsize=10,
            ha="center", arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.2))
ax.annotate("power = 1 − β\n(detect real effect)", xy=(4.4,0.04), xytext=(5.0,0.27), color=GREEN,
            fontsize=10, ha="center", arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2))
ax.set_yticks([]); despine(ax, left=False); ax.set_ylim(-0.06, 0.5)
ax.set_title("Significance (α) vs power (1 − β): the two distributions of a test", loc="left")
ax.set_xlabel("test statistic")
save(fig, "s9_power.png")
print("BATCH B DONE")
