import numpy as np, matplotlib.pyplot as plt
from vstyle import *
np.random.seed(8)

# 3.3 truncated y-axis
fig, ax = plt.subplots(1,2, figsize=(11,4.6))
cats=["Q1","Q2","Q3","Q4"]; vals=[97,98,99,102]
ax[0].bar(cats,vals,color=TEAL); ax[0].set_ylim(0,115); despine(ax[0])
ax[0].set_title("Honest: axis starts at 0",color=GREEN,fontsize=12.5)
ax[0].text(1.5,108,"a modest ~5% rise",ha="center",fontsize=10.5,color=INK_SOFT)
ax[1].bar(cats,vals,color=ROSE); ax[1].set_ylim(95,103); despine(ax[1])
ax[1].set_title("Misleading: axis starts at 95",color=ROSE,fontsize=12.5)
ax[1].annotate("the SAME numbers now\nlook like a huge jump",xy=(3,102),xytext=(1.1,101.4),
    fontsize=10.5,color=ROSE,ha="center",arrowprops=dict(arrowstyle="->",color=ROSE,lw=1.3))
fig.suptitle("The #1 chart deception: truncating the y-axis",fontsize=14,fontweight="bold",y=1.02,color=INK)
fig.tight_layout(rect=[0,0,1,0.93])
save(fig,"s_eda_truncate.png")

# 3.3 cherry-picked time window
months=np.arange(1,25)
series=100+0.5*months+np.array([0,1,-1,1,2,1,3,2,2,1,-4,-9,-6,-1,3,4,5,4,6,7,6,8,9,10])
fig, ax = plt.subplots(1,2, figsize=(11,4.4))
ax[0].plot(months,series,color=INDIGO_DK,lw=2,marker="o",ms=3)
ax[0].axvspan(10,14,color=ROSE_BG,alpha=.6)
ax[0].set_title("Full picture: trending up over 2 years",color=GREEN,fontsize=12.5)
ax[0].set_xlabel("month"); ax[0].set_ylabel("metric"); despine(ax[0])
ax[0].text(12,series.max()-1.5,"cherry-picked\nwindow",ha="center",va="top",fontsize=10,color=ROSE,fontweight="bold")
w=(months>=10)&(months<=14)
ax[1].plot(months[w],series[w],color=ROSE,lw=2.4,marker="o",ms=5)
ax[1].set_title("Cherry-picked: 'a collapse!'",color=ROSE,fontsize=12.5)
ax[1].set_xlabel("month"); despine(ax[1])
fig.suptitle("Cherry-picking the time range: a tiny dip framed as a catastrophe",
    fontsize=13.5,fontweight="bold",y=1.02,color=INK)
fig.tight_layout(rect=[0,0,1,0.93])
save(fig,"s_eda_cherry.png")
print("BATCH I DONE")
