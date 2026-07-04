import numpy as np, pandas as pd, matplotlib.pyplot as plt
import seaborn as sns
from vstyle import *
rng=np.random.default_rng(9)

# 3.5 grouped vs stacked bars
cats=["Electronics","Apparel","Home"]; web=[240,90,110]; mob=[150,160,70]
x=np.arange(len(cats)); w=0.38
fig,ax=plt.subplots(1,2,figsize=(11,4.4))
ax[0].bar(x-w/2,web,w,label="Web",color=INDIGO); ax[0].bar(x+w/2,mob,w,label="Mobile",color=TEAL)
ax[0].set_xticks(x); ax[0].set_xticklabels(cats); ax[0].set_title("Grouped: compare channels within a category",fontsize=12.5,color=INDIGO_DK)
ax[0].set_ylabel("revenue ($000s)"); ax[0].legend(frameon=False); despine(ax[0])
ax[1].bar(x,web,label="Web",color=INDIGO); ax[1].bar(x,mob,bottom=web,label="Mobile",color=TEAL)
ax[1].set_xticks(x); ax[1].set_xticklabels(cats); ax[1].set_title("Stacked: see the total per category",fontsize=12.5,color=TEAL)
ax[1].legend(frameon=False); despine(ax[1])
fig.suptitle("Grouped vs. stacked bars: comparison within, or totals across",fontsize=13.5,fontweight="bold",y=1.02,color=INK)
fig.tight_layout(rect=[0,0,1,0.93]); save(fig,"s_eda_bars_gs.png")

# 3.5 crosstab heatmap
regions=["North","South","East","West"]; channels=["Web","Mobile","Store"]
counts=np.array([[120,80,30],[60,140,20],[90,70,40],[110,50,60]])
fig,ax=plt.subplots(figsize=(7,5))
sns.heatmap(pd.DataFrame(counts,index=regions,columns=channels),annot=True,fmt="d",cmap="Blues",
            linewidths=1.2,linecolor="white",cbar_kws={"label":"number of orders"},annot_kws={"fontsize":12},ax=ax)
ax.set_title("Crosstab heatmap: orders by region x channel",loc="left",fontsize=13,pad=10)
ax.set_xlabel("channel"); ax.set_ylabel("region")
fig.tight_layout(); save(fig,"s_eda_crosstab.png")

# 3.6 time-series decomposition
t=np.arange(36)
trend=50+0.8*t
seasonal=9*np.sin(2*np.pi*t/12)
resid=rng.normal(0,3,36)
observed=trend+seasonal+resid
fig,axes=plt.subplots(4,1,figsize=(10.5,6.6),sharex=True)
for ax,(series,name,c) in zip(axes,[(observed,"Observed",INK),(trend,"Trend",INDIGO),
                                    (seasonal,"Seasonality",TEAL),(resid,"Residual (noise)",ROSE)]):
    ax.plot(t,series,color=c,lw=1.8,marker="o" if name=="Observed" else None,ms=3)
    if name in ("Seasonality","Residual (noise)"): ax.axhline(0,color=INK_FAINT,lw=.8,ls=":")
    ax.set_ylabel(name,fontsize=10.5,color=c); despine(ax)
axes[-1].set_xlabel("month")
fig.suptitle("Time-series decomposition: observed = trend + seasonality + residual",
    fontsize=13.5,fontweight="bold",y=0.99,color=INK)
fig.tight_layout(rect=[0,0,1,0.96]); save(fig,"s_eda_ts_components.png")

# 3.6 rolling average
days=np.arange(180)
raw=100+0.15*days+12*np.sin(2*np.pi*days/30)+rng.normal(0,9,180)
s=pd.Series(raw)
fig,ax=plt.subplots(figsize=(10.5,4.2))
ax.plot(days,raw,color="#c7cee0",lw=1,label="raw daily (noisy)")
ax.plot(days,s.rolling(7).mean(),color=TEAL,lw=2,label="7-day rolling mean")
ax.plot(days,s.rolling(30).mean(),color=ROSE,lw=2.4,label="30-day rolling mean")
ax.set_title("Rolling averages smooth the noise to reveal the trend",loc="left")
ax.set_xlabel("day"); ax.set_ylabel("metric"); ax.legend(frameon=False); despine(ax)
save(fig,"s_eda_rolling.png")

# 3.7 outlier detection (IQR boxplot + z-score)
data=np.concatenate([rng.normal(50,8,200),[12,95,98,5]])
fig,ax=plt.subplots(1,2,figsize=(11,4.2))
bp=ax[0].boxplot(data,vert=False,widths=.5,patch_artist=True,
    flierprops=dict(marker="o",markerfacecolor=ROSE,markeredgecolor=ROSE,markersize=7,alpha=.8),
    boxprops=dict(facecolor=INDIGO_BG,edgecolor=INDIGO),medianprops=dict(color=INDIGO_DK,lw=2),
    whiskerprops=dict(color=INK_SOFT),capprops=dict(color=INK_SOFT))
q1,q3=np.percentile(data,[25,75]); iqr=q3-q1
ax[0].set_yticks([]); ax[0].set_title("IQR rule: points beyond 1.5xIQR (red)",fontsize=12,color=ROSE); despine(ax[0],left=False)
ax[0].set_xlabel("value")
z=(data-data.mean())/data.std()
ax[1].scatter(data,np.zeros_like(data)+rng.uniform(-.4,.4,len(data)),s=18,
    c=[ROSE if abs(zz)>3 else INDIGO for zz in z],alpha=.7,edgecolors="none")
for k in (-3,3): ax[1].axvline(data.mean()+k*data.std(),color=AMBER,ls="--",lw=1.4)
ax[1].set_yticks([]); ax[1].set_ylim(-1,1); ax[1].set_title("z-score rule: |z| > 3 (red), bands at +/-3 SD",fontsize=12,color=AMBER); despine(ax[1],left=False)
ax[1].set_xlabel("value")
fig.suptitle("Two ways to flag outliers: the IQR fence and the z-score",fontsize=13.5,fontweight="bold",y=1.02,color=INK)
fig.tight_layout(rect=[0,0,1,0.93]); save(fig,"s_eda_outliers.png")

# 3.7 outlier decision (graphviz)
dot('''
 o [label="A point looks extreme", fillcolor="#e9ecf6", color="#c7cee0"];
 q1 [label="Is it impossible /\\na data error?", shape=diamond, style="filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 fix [label="FIX or REMOVE it\\n(and document why)", fillcolor="#fce8ee", color="#e7b9c6"];
 q2 [label="Is it a real but\\nextreme value?", shape=diamond, style="filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 keep [label="KEEP it — it may be\\nthe most important signal\\n(use robust stats; maybe cap)", fillcolor="#e6f5ec", color="#bfe0c8"];
 inv [label="INVESTIGATE\\nbefore deciding", fillcolor="#e3f5f3", color="#bfe7e3"];
 o -> q1;
 q1 -> fix [label="yes"];
 q1 -> q2 [label="no"];
 q2 -> keep [label="yes"];
 q2 -> inv [label="unsure"];
''', "s_eda_outlier_decide.png", rd="TB", rs="0.42", ns="0.5")
print("BATCH L DONE")
