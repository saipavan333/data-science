import numpy as np, matplotlib.pyplot as plt
from vstyle import *
np.random.seed(11)

# 1.6 (a) population vs sample (graphviz)
dot('''
 Pop [label="POPULATION\\neveryone we care about\\nparameters: mu, sigma (fixed, unknown)", fillcolor="#eef1fd", color="#cdd7fb"];
 Smp [label="SAMPLE\\nthe few we actually measure\\nstatistics: x-bar, s (computed)", fillcolor="#e3f5f3", color="#bfe7e3"];
 Inf [label="INFERENCE\\nestimate the parameter\\n+ state our uncertainty", fillcolor="#fbf3e0", color="#ecd9ad"];
 Pop -> Smp [label="  random sampling"];
 Smp -> Inf [label="  compute statistic"];
 Inf -> Pop [label="  conclude about", style=dashed, color="#b6bccb"];
''', "s6_popsample.png", rd="LR", rs="0.7", ns="0.35")

# 1.6 (b) sampling distribution of the mean
pop = np.random.exponential(scale=20, size=200000)      # skewed population, mean=20
mu = pop.mean()
means = np.array([np.random.choice(pop, 30, replace=False).mean() for _ in range(3000)])
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].hist(pop, bins=60, color=AMBER_BG, edgecolor=AMBER, linewidth=.4)
ax[0].axvline(mu, color=ROSE, lw=2.2, label=f"mean mu = {mu:.0f}")
ax[0].set_title("The population (skewed)", loc="left"); ax[0].set_xlim(0,120)
ax[0].set_yticks([]); despine(ax[0], left=False); ax[0].legend(frameon=False); ax[0].set_xlabel("value")
ax[1].hist(means, bins=40, color=INDIGO_BG, edgecolor=INDIGO, linewidth=.5)
ax[1].axvline(mu, color=ROSE, lw=2.2)
ax[1].set_title("Distribution of the sample mean (n = 30)", loc="left")
ax[1].set_yticks([]); despine(ax[1], left=False); ax[1].set_xlabel("sample mean")
ax[1].annotate(f"centered at mu,\nbut much narrower\n(SE = sigma/√n)", xy=(mu, ax[1].get_ylim()[1]*.5),
    xytext=(mu+7, ax[1].get_ylim()[1]*.7), fontsize=10.5, color=INK_SOFT,
    arrowprops=dict(arrowstyle="->", color=INK_FAINT, lw=1.2))
fig.suptitle("One sample wobbles; the average of many samples clusters tightly around the truth",
    fontsize=13.5, fontweight="bold", y=1.03, color=INK)
save(fig, "s6_sampling_dist.png")

# 1.6 (c) standard error vs n
n = np.arange(2, 200); sigma = 20
fig, ax = plt.subplots(figsize=(10.5, 4.0))
ax.plot(n, sigma/np.sqrt(n), color=TEAL, lw=2.6)
for k in (10, 40, 160):
    ax.plot(k, sigma/np.sqrt(k), "o", color=ROSE, ms=7)
    ax.annotate(f"n={k}\nSE={sigma/np.sqrt(k):.1f}", xy=(k, sigma/np.sqrt(k)),
        xytext=(k+8, sigma/np.sqrt(k)+0.6), fontsize=10, color=INK_SOFT)
ax.set_title("Standard error shrinks like 1/√n — diminishing returns", loc="left")
ax.set_xlabel("sample size n"); ax.set_ylabel("standard error of the mean"); despine(ax)
ax.text(120, 11, "to halve the error\nyou need 4× the data", fontsize=10.5, color=INK_SOFT, style="italic")
save(fig, "s6_se_vs_n.png")

# 1.7 CLT: three populations -> sampling means all go normal (2x3 grid)
fig, axes = plt.subplots(2, 3, figsize=(11.5, 6.2))
pops = {
 "Uniform": np.random.uniform(0, 1, 200000),
 "Skewed (exponential)": np.random.exponential(1, 200000),
 "Bimodal": np.concatenate([np.random.normal(-2,.6,100000), np.random.normal(2,.6,100000)]),
}
cols = [TEAL, AMBER, INDIGO]
for j,(name,popv) in enumerate(pops.items()):
    axes[0,j].hist(popv, bins=60, color=cols[j], alpha=.30, edgecolor=cols[j], linewidth=.3)
    axes[0,j].set_title(name, fontsize=12.5, color=cols[j]); axes[0,j].set_yticks([])
    despine(axes[0,j], left=False)
    sm = np.array([np.random.choice(popv, 30).mean() for _ in range(3000)])
    axes[1,j].hist(sm, bins=40, color=cols[j], alpha=.55, edgecolor="white", linewidth=.4)
    axes[1,j].set_yticks([]); despine(axes[1,j], left=False)
axes[0,0].set_ylabel("the population", fontsize=12, color=INK_SOFT)
axes[1,0].set_ylabel("mean of n=30\n(3000 samples)", fontsize=12, color=INK_SOFT)
fig.suptitle("The Central Limit Theorem: whatever the population shape, the sample mean becomes normal",
    fontsize=14, fontweight="bold", y=0.99, color=INK)
fig.text(0.5, 0.5, "↓ take many samples of 30, average each ↓", ha="center", fontsize=11,
    color=INK_FAINT, style="italic")
save(fig, "s7_clt.png")

# 1.7 effect of n on convergence (one skewed pop)
fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.8))
base = np.random.exponential(1, 300000)
for ax,nn in zip(axes, [1, 5, 30]):
    sm = np.array([np.random.choice(base, nn).mean() for _ in range(4000)])
    ax.hist(sm, bins=40, color=INDIGO_BG, edgecolor=INDIGO, linewidth=.5)
    ax.set_title(f"n = {nn}", fontsize=13, color=INDIGO_DK); ax.set_yticks([]); despine(ax, left=False)
    ax.set_xlabel("sample mean")
axes[0].text(.5,.9,"still skewed\n(n=1 is just the population)",transform=axes[0].transAxes,
    fontsize=9.5,color=INK_SOFT,ha="center",va="top")
axes[2].text(.5,.9,"now bell-shaped",transform=axes[2].transAxes,fontsize=9.5,color=GREEN,ha="center",va="top")
fig.suptitle("Larger samples → the sampling distribution gets more normal and narrower",
    fontsize=13.5, fontweight="bold", y=1.04, color=INK)
save(fig, "s7_clt_n.png")
print("BATCH A DONE")
