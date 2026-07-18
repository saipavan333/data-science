import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from vstyle import *

# ---- s8_ci_concept: fix title/label/annotation overlaps ----
np.random.seed(7)
mu, sigma, n = 100.0, 15.0, 40
se = sigma/np.sqrt(n); K = 25
fig, ax = plt.subplots(figsize=(10.5, 5.6))
miss = 0
for i in range(K):
    s = np.random.normal(mu, sigma, n); m = s.mean()
    lo, hi = m-1.96*se, m+1.96*se
    covers = lo <= mu <= hi; miss += (not covers)
    c = INDIGO if covers else ROSE
    ax.plot([lo,hi],[i,i], color=c, lw=2.4, solid_capstyle="round"); ax.plot(m,i,"o",color=c,ms=4)
ax.plot([mu,mu], [-0.7, K+0.7], color=INK, lw=1.8, ls="--")  # shortened so it clears the bottom caption
ax.set_ylim(-2.4, K+2.4); ax.set_yticks([]); despine(ax, left=False)
ax.set_xlabel("each study's estimated mean with its 95% confidence interval")
ax.set_title(f"What '95% confidence' means: {K-miss} of {K} intervals capture the truth",
             loc="left", pad=30)
ax.text(mu, K+1.1, "true mean μ (usually unknown)", ha="center", va="bottom", color=INK, fontsize=10.5)
ax.text(0.0, -2.0, f"{miss} interval misses (red) — about the 5% we expect to miss by chance",
        transform=ax.get_yaxis_transform(), color=ROSE, fontsize=10.5, va="center")
# place the note in data x near left
ax.text(ax.get_xlim()[0]+0.3, -2.0, "", )  # noop to keep xlim
save(fig, "s8_ci_concept.png")

# ---- s9_errors: CORRECT labels (power in H0-false+Reject) + fix title spacing ----
fig, ax = plt.subplots(figsize=(9.0, 5.4))
ax.set_xlim(-0.05, 2.05); ax.set_ylim(-0.15, 2.62); ax.axis("off")
# (col,row): col0 = H0 FALSE (effect real), col1 = H0 TRUE (no effect); row1 = Reject, row0 = Fail
cells = {
 (0,1):(GREEN_BG, GREEN, "Correct\n(true positive)\n= POWER"),
 (1,1):(ROSE_BG,  ROSE,  "TYPE I ERROR\nfalse positive (α)\nflag an effect that isn't real"),
 (0,0):(AMBER_BG, AMBER, "TYPE II ERROR\nfalse negative (β)\nmiss a real effect"),
 (1,0):(GREEN_BG, GREEN, "Correct\n(true negative)"),
}
for (col,row),(bg,fg,txt) in cells.items():
    ax.add_patch(FancyBboxPatch((col,row),0.96,0.96, boxstyle="round,pad=0.02",
                 facecolor=bg, edgecolor=fg, linewidth=1.8))
    ax.text(col+0.48, row+0.48, txt, ha="center", va="center", color=fg, fontsize=10.5, fontweight="bold")
ax.text(0.48, 2.02, "H0 actually FALSE\n(effect is real)", ha="center", va="bottom", fontsize=10.5, color=INK)
ax.text(1.48, 2.02, "H0 actually TRUE\n(no effect)", ha="center", va="bottom", fontsize=10.5, color=INK)
ax.text(-0.02, 1.48, "Reject H0", ha="right", va="center", fontsize=10.5, color=INK, rotation=90)
ax.text(-0.02, 0.48, "Fail to\nreject H0", ha="right", va="center", fontsize=10.5, color=INK, rotation=90)
ax.text(1.0, 2.52, "Two ways to be wrong: Type I and Type II errors", ha="center", va="center",
        fontsize=14, fontweight="bold", color=INK)
save(fig, "s9_errors.png")
print("FIX B DONE  (ci misses kept dynamic)")
