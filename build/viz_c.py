import numpy as np, matplotlib.pyplot as plt
from vstyle import *
np.random.seed(5)

# 1.10 (a) which-test-when decision tree
dot('''
 q0 [label="What is your OUTCOME\\nvariable?", shape=diamond, style="filled", fillcolor="#e9ecf6", color="#c7cee0"];
 qn [label="Numeric outcome:\\nrelate or compare?", shape=diamond, style="filled", fillcolor="#e3f5f3", color="#bfe7e3"];
 qg [label="Comparing how\\nmany groups?", shape=diamond, style="filled", fillcolor="#e3f5f3", color="#bfe7e3"];
 qp [label="Same subjects\\nmeasured twice?", shape=diamond, style="filled", fillcolor="#e3f5f3", color="#bfe7e3"];
 cor [label="CORRELATION /\\nREGRESSION\\n(Pearson r, linear fit)", fillcolor="#e3f5f3", color="#bfe7e3"];
 t1  [label="ONE-SAMPLE t-TEST\\n(mean vs a known value)", fillcolor="#e3f5f3", color="#bfe7e3"];
 t2  [label="TWO-SAMPLE t-TEST\\n(two independent groups)", fillcolor="#e3f5f3", color="#bfe7e3"];
 tp  [label="PAIRED t-TEST\\n(before/after, matched)", fillcolor="#e3f5f3", color="#bfe7e3"];
 an  [label="ANOVA\\n(3+ group means)", fillcolor="#e3f5f3", color="#bfe7e3"];
 chi [label="CHI-SQUARE TEST\\n(association of two\\ncategorical variables)", fillcolor="#fbf3e0", color="#ecd9ad"];
 q0 -> qn [label="numeric"];
 q0 -> chi [label="categorical"];
 qn -> cor [label="relate to another\\nnumeric variable"];
 qn -> qg [label="compare\\ngroup means"];
 qg -> t1 [label="1"];
 qg -> qp [label="2"];
 qg -> an [label="3+"];
 qp -> tp [label="yes"];
 qp -> t2 [label="no"];
''', "s10_chooser.png", rd="TB", rs="0.5", ns="0.35")

# 1.10 (b) what a t-test compares
fig, ax = plt.subplots(figsize=(10.5, 4.3))
xs = np.linspace(35, 75, 500)
for m,c,cb,name in [(50,TEAL,TEAL_BG,"Group A (mean 50)"),(56,ROSE,ROSE_BG,"Group B (mean 56)")]:
    y=np.exp(-0.5*((xs-m)/5)**2); ax.plot(xs,y,color=c,lw=2.4,label=name)
    ax.fill_between(xs,y,color=cb,alpha=.5)
ax.annotate("", xy=(50,1.06), xytext=(56,1.06), arrowprops=dict(arrowstyle="<->",color=INK_SOFT,lw=1.8))
ax.text(53,1.12,"difference in means", ha="center", color=INK, fontsize=10.5)
ax.set_ylim(0,1.25); ax.set_yticks([]); despine(ax,left=False)
ax.legend(frameon=False, loc="upper left"); ax.set_xlabel("outcome value")
ax.set_title("A t-test asks: is the gap between means big relative to the spread?", loc="left")
ax.text(65,0.5,"t = difference in means\n———————————\nstandard error", fontsize=10.5, color=INK_SOFT, ha="center")
save(fig,"s10_ttest.png")

# 1.11 (a) what correlation r looks like
fig, axes = plt.subplots(2,3, figsize=(11,6.4))
def corr_xy(r,n=200):
    x=np.random.normal(0,1,n); y=r*x+np.sqrt(max(1-r*r,0))*np.random.normal(0,1,n); return x,y
panels=[("r = +0.9",0.9),("r = +0.5",0.5),("r = 0.0",0.0),("r = -0.5",-0.5),("r = -0.9",-0.9),("nonlinear",None)]
for ax,(title,r) in zip(axes.ravel(),panels):
    if r is None:
        x=np.linspace(-3,3,200); y=x**2+np.random.normal(0,0.6,200)
        rr=np.corrcoef(x,y)[0,1]; title=f"U-shape: r = {rr:.2f}"
        c=AMBER
    else:
        x,y=corr_xy(r); c=INDIGO if r>=0 else ROSE if r<0 else INK_SOFT
        if r==0: c=INK_FAINT
    ax.scatter(x,y,s=10,color=c,alpha=.55,edgecolors="none")
    ax.set_title(title, fontsize=12, color=c); ax.set_xticks([]); ax.set_yticks([])
    despine(ax)
fig.suptitle("Pearson's r measures LINEAR strength & direction — and misses curves",
    fontsize=14, fontweight="bold", y=1.0, color=INK)
axes[1,2].text(0.5,-0.12,"strong relationship, but r≈0:\nr only sees straight lines",
    transform=axes[1,2].transAxes, ha="center", va="top", fontsize=9.5, color=AMBER)
save(fig,"s11_scatter_r.png")

# 1.11 (b) Anscombe's quartet
ax_x=[10,8,13,9,11,14,6,4,12,7,5]
A={1:[8.04,6.95,7.58,8.81,8.33,9.96,7.24,4.26,10.84,4.82,5.68],
   2:[9.14,8.14,8.74,8.77,9.26,8.10,6.13,3.10,9.13,7.26,4.74],
   3:[7.46,6.77,12.74,7.11,7.81,8.84,6.08,5.39,8.15,6.42,5.73]}
x4=[8,8,8,8,8,8,8,19,8,8,8]; y4=[6.58,5.76,7.71,8.84,8.47,7.04,5.25,12.50,5.56,7.91,6.89]
fig, axes = plt.subplots(1,4, figsize=(12,3.4), sharex=True, sharey=True)
data=[(ax_x,A[1],"I"),(ax_x,A[2],"II"),(ax_x,A[3],"III"),(x4,y4,"IV")]
for ax,(xx,yy,name) in zip(axes,data):
    xx=np.array(xx); yy=np.array(yy)
    ax.scatter(xx,yy,s=28,color=INDIGO,alpha=.8,edgecolors="white",linewidth=.5)
    xl=np.array([2,20]); ax.plot(xl,3+0.5*xl,color=ROSE,lw=1.8)
    ax.set_title(f"Dataset {name}", fontsize=11.5); despine(ax)
    ax.set_xlim(2,20); ax.set_ylim(2,14)
fig.suptitle("Anscombe's quartet: identical mean, variance, correlation (r=0.82) and fit line — utterly different data",
    fontsize=12.5, fontweight="bold", y=1.04, color=INK)
fig.text(0.5,-0.03,"The lesson: ALWAYS plot your data. Summary numbers alone can hide everything that matters.",
    ha="center", fontsize=10.5, color=INK_SOFT, style="italic")
save(fig,"s11_anscombe.png")

# 1.11 (c) Pearson vs Spearman
from scipy import stats
x=np.linspace(1,10,80); y=x**3+np.random.normal(0,15,80)
pr=stats.pearsonr(x,y)[0]; sr=stats.spearmanr(x,y)[0]
fig, ax = plt.subplots(figsize=(9,4.4))
ax.scatter(x,y,s=22,color=TEAL,alpha=.7,edgecolors="none")
ax.set_title("Monotonic but curved: Spearman catches it, Pearson under-rates it", loc="left")
ax.set_xlabel("x"); ax.set_ylabel("y = x³ + noise"); despine(ax)
ax.text(0.04,0.92,f"Pearson r  = {pr:.2f}  (linear)\nSpearman ρ = {sr:.2f}  (rank/monotonic)",
    transform=ax.transAxes, fontsize=11.5, color=INK, va="top",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#f7f8fa", edgecolor="#d8dce3"))
save(fig,"s11_pearson_spearman.png")

# 1.11 (d) confounder: correlation != causation
dot('''
 Z [label="SUMMER HEAT\\n(the confounder Z)", fillcolor="#fbf3e0", color="#ecd9ad"];
 X [label="ice-cream sales (X)", fillcolor="#eef1fd", color="#cdd7fb"];
 Y [label="drownings (Y)", fillcolor="#eef1fd", color="#cdd7fb"];
 Z -> X [label="causes"];
 Z -> Y [label="causes"];
 X -> Y [label="  correlated, but neither\\n  causes the other", style=dashed, dir=both, color="#c2305a", fontcolor="#c2305a"];
 {rank=same; X; Y;}
''', "s11_confounder.png", rd="TB", rs="0.8", ns="1.4")
print("BATCH C DONE")
