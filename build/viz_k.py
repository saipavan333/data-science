import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy import stats
from vstyle import *
rng=np.random.default_rng(6)

# 3.2 matplotlib anatomy: Figure vs Axes
fig=plt.figure(figsize=(10.5,5.6))
fig.patch.set_edgecolor(INDIGO); fig.patch.set_linewidth(0)
ax=fig.add_axes([0.30,0.20,0.45,0.58])
m=np.arange(1,8); y=[3,5,4,6,8,7,9]
ax.plot(m,y,color=TEAL,lw=2.4,marker="o",ms=6)
ax.set_title("Weekly signups",fontsize=12,fontweight="bold")
ax.set_xlabel("week"); ax.set_ylabel("signups")
# outer rectangle = the Figure
figrect=FancyBboxPatch((0.012,0.02),0.976,0.96,boxstyle="round,pad=0.0",transform=fig.transFigure,
    fill=False,edgecolor=INDIGO,lw=2.0,linestyle="--")
fig.add_artist(figrect)
def lab(x,y,txt,col,tx,ty):
    fig.text(tx,ty,txt,fontsize=11,color=col,ha="center",fontweight="bold")
    fig.add_artist(plt.matplotlib.patches.FancyArrowPatch((tx,ty-0.03),(x,y),transform=fig.transFigure,
        arrowstyle="->",color=col,lw=1.4,mutation_scale=12))
fig.text(0.05,0.93,"Figure  (the whole canvas)",fontsize=12,color=INDIGO,fontweight="bold")
fig.text(0.52,0.86,"Axes  (one plot inside the figure)",fontsize=11.5,color=TEAL,fontweight="bold",ha="center")
lab(0.52,0.78,"title",AMBER,0.86,0.74)
lab(0.30,0.49,"y-axis label",ROSE,0.13,0.50)
lab(0.52,0.20,"x-axis label",ROSE,0.52,0.10)
lab(0.62,0.62,"your data\n(the line)",GREEN,0.86,0.55)
fig.text(0.5,0.055,"fig, ax = plt.subplots()   then   ax.plot(...)   ax.set_title(...)   ax.set_xlabel(...)",
    ha="center",fontsize=10.5,color=INK_SOFT,family="monospace")
fig.savefig(IMG+"/s_eda_mpl_anatomy.png",facecolor="white",bbox_inches="tight",dpi=150); plt.close(fig)
print("chart  -> s_eda_mpl_anatomy.png")

# 3.4 distribution shapes gallery
fig,axes=plt.subplots(2,3,figsize=(11.5,6.2))
shapes=[("Normal (symmetric)",rng.normal(50,10,4000),INDIGO),
        ("Right-skewed",rng.exponential(12,4000),AMBER),
        ("Left-skewed",100-rng.exponential(12,4000),ROSE),
        ("Bimodal (two peaks)",np.concatenate([rng.normal(35,6,2000),rng.normal(70,6,2000)]),TEAL),
        ("Uniform (flat)",rng.uniform(0,100,4000),GREEN),
        ("Heavy-tailed (outliers)",rng.standard_t(2,4000)*10+50,"#7a5cc0")]
for ax,(name,data,c) in zip(axes.ravel(),shapes):
    ax.hist(data,bins=45,color=c,alpha=.45,edgecolor=c,lw=.3)
    ax.set_title(name,fontsize=11.5,color=c); ax.set_yticks([]); ax.set_xticks([]); despine(ax,left=False)
fig.suptitle("Six distribution shapes you must recognize on sight",fontsize=14,fontweight="bold",y=1.0,color=INK)
fig.tight_layout(rect=[0,0,1,0.95])
save(fig,"s_eda_shapes.png")

# 3.4 log transform before/after
fig,axes=plt.subplots(1,2,figsize=(11,4.2))
income=rng.lognormal(10.3,0.6,5000)/1000
axes[0].hist(income,bins=60,color=AMBER_BG,edgecolor=AMBER,lw=.4)
axes[0].set_title("Raw income: heavily right-skewed",color=AMBER,fontsize=12.5)
axes[0].set_xlabel("income ($000s)"); axes[0].set_yticks([]); despine(axes[0],left=False)
axes[0].set_xlim(0,np.quantile(income,0.99))
axes[1].hist(np.log10(income),bins=60,color=TEAL_BG,edgecolor=TEAL,lw=.4)
axes[1].set_title("log10(income): now roughly symmetric",color=TEAL,fontsize=12.5)
axes[1].set_xlabel("log10(income)"); axes[1].set_yticks([]); despine(axes[1],left=False)
fig.suptitle("A log transform tames right-skew: the long tail becomes a bell",fontsize=13.5,fontweight="bold",y=1.02,color=INK)
fig.tight_layout(rect=[0,0,1,0.93])
save(fig,"s_eda_logtransform.png")

# 3.4 QQ plots
fig,axes=plt.subplots(1,2,figsize=(11,4.4))
stats.probplot(rng.normal(0,1,500),dist="norm",plot=axes[0])
axes[0].set_title("Normal data: points hug the line",color=GREEN,fontsize=12.5)
stats.probplot(rng.exponential(1,500),dist="norm",plot=axes[1])
axes[1].set_title("Skewed data: points curve away",color=ROSE,fontsize=12.5)
for ax in axes:
    ax.get_lines()[0].set(marker="o",ms=3,color=INDIGO,alpha=.5)
    ax.get_lines()[1].set(color=INK_SOFT,lw=1.8)
    despine(ax); ax.set_xlabel("theoretical quantiles"); ax.set_ylabel("data quantiles")
fig.suptitle("The QQ plot: a quick eyeball test for normality",fontsize=13.5,fontweight="bold",y=1.02,color=INK)
fig.tight_layout(rect=[0,0,1,0.93])
save(fig,"s_eda_qq.png")
print("BATCH K DONE")
