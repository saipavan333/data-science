import numpy as np, matplotlib.pyplot as plt
from vstyle import *
np.random.seed(11)
fig, axes = plt.subplots(2, 3, figsize=(11.5, 6.4))
fig.subplots_adjust(hspace=0.42)
pops = {"Uniform": np.random.uniform(0,1,200000),
        "Skewed (exponential)": np.random.exponential(1,200000),
        "Bimodal": np.concatenate([np.random.normal(-2,.6,100000), np.random.normal(2,.6,100000)])}
cols = [TEAL, AMBER, INDIGO]
for j,(name,popv) in enumerate(pops.items()):
    axes[0,j].hist(popv, bins=60, color=cols[j], alpha=.30, edgecolor=cols[j], linewidth=.3)
    axes[0,j].set_title(name, fontsize=12.5, color=cols[j]); axes[0,j].set_yticks([])
    despine(axes[0,j], left=False)
    sm = np.array([np.random.choice(popv,30).mean() for _ in range(3000)])
    axes[1,j].hist(sm, bins=40, color=cols[j], alpha=.55, edgecolor="white", linewidth=.4)
    axes[1,j].set_yticks([]); despine(axes[1,j], left=False); axes[1,j].set_xlabel("sample mean")
axes[0,0].set_ylabel("the population\nshape", fontsize=12, color=INK_SOFT)
axes[1,0].set_ylabel("mean of n=30\n(over 3000 samples)", fontsize=12, color=INK_SOFT)
axes[0,1].set_title("Skewed (exponential)\n", fontsize=12.5, color=AMBER)
fig.suptitle("The Central Limit Theorem: whatever the population shape, the mean of a sample becomes normal",
    fontsize=13.5, fontweight="bold", y=0.99, color=INK)
save(fig, "s7_clt.png")
print("fixed s7_clt")
