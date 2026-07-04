import numpy as np, pandas as pd, matplotlib.pyplot as plt
import seaborn as sns
from vstyle import *
rng=np.random.default_rng(4)
n=300
ad=rng.uniform(5,100,n)
sessions=40+1.8*ad+rng.normal(0,18,n)
revenue=80+3.0*sessions+rng.normal(0,90,n)
bounce=70-0.4*sessions+rng.normal(0,8,n)          # negatively related to sessions
plan=np.where(revenue>revenue.mean(),"Pro","Free")
df=pd.DataFrame({"ad_spend":ad,"sessions":sessions,"revenue":revenue,"bounce_rate":bounce,"plan":plan})

# 3.4 correlation heatmap
fig,ax=plt.subplots(figsize=(6.6,5.6))
corr=df[["ad_spend","sessions","revenue","bounce_rate"]].corr()
sns.heatmap(corr,annot=True,fmt=".2f",cmap="RdBu_r",center=0,vmin=-1,vmax=1,square=True,
            linewidths=1.2,linecolor="white",cbar_kws={"shrink":.78,"label":"correlation r"},
            annot_kws={"fontsize":12},ax=ax)
ax.set_title("Correlation heatmap: every pair at a glance",loc="left",fontsize=13.5,pad=10)
plt.setp(ax.get_xticklabels(),rotation=25,ha="right")
fig.tight_layout()
save(fig,"s_eda_heatmap.png")

# 3.4 small multiples / faceting
fig,axes=plt.subplots(1,3,figsize=(11,3.7),sharey=True,sharex=True)
regions={"North":110,"South":70,"West":90}
cols=[INDIGO,TEAL,AMBER]
for ax,(reg,mu),c in zip(axes,regions.items(),cols):
    vals=rng.gamma(4,mu/4,400)
    ax.hist(vals,bins=30,color=c,alpha=.55,edgecolor="white",lw=.3)
    ax.axvline(vals.mean(),color=c,lw=2)
    ax.set_title(reg,color=c,fontsize=12.5); ax.set_xlabel("order value ($)"); ax.set_yticks([])
    despine(ax,left=False)
axes[0].set_ylabel("number of orders")
fig.suptitle("Small multiples (faceting): the same chart, split by group, on shared axes",
    fontsize=13.5,fontweight="bold",y=1.03,color=INK)
fig.tight_layout(rect=[0,0,1,0.92])
save(fig,"s_eda_facets.png")

# 3.4 pair plot
sns.set_theme(style="white")
g=sns.pairplot(df[["ad_spend","sessions","revenue","plan"]],hue="plan",
               palette={"Free":INDIGO,"Pro":TEAL},diag_kind="hist",
               plot_kws=dict(s=16,alpha=.55,edgecolor="none"),height=1.9)
g.fig.suptitle("Pair plot: every variable vs every other, colored by plan",
    fontsize=13.5,fontweight="bold",y=1.03)
g.fig.savefig(IMG+"/s_eda_pairplot.png",facecolor="white",bbox_inches="tight",dpi=150)
plt.close(g.fig); print("chart  -> s_eda_pairplot.png")
print("BATCH J DONE")
