import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from vstyle import *
rng=np.random.default_rng(0)

# 4.1 ML map (graphviz)
dot('''
 ml [label="MACHINE LEARNING\\nlearn patterns from data", fillcolor="#e9ecf6", color="#c7cee0"];
 sup [label="SUPERVISED\\ndata has labels (a known answer)", fillcolor="#eef1fd", color="#cdd7fb"];
 uns [label="UNSUPERVISED\\nno labels — find structure", fillcolor="#e3f5f3", color="#bfe7e3"];
 reg [label="Regression\\npredict a NUMBER\\ne.g. house price", fillcolor="#eef1fd", color="#cdd7fb"];
 cls [label="Classification\\npredict a CATEGORY\\ne.g. spam / not spam", fillcolor="#eef1fd", color="#cdd7fb"];
 clu [label="Clustering\\nfind natural groups\\ne.g. customer segments", fillcolor="#e3f5f3", color="#bfe7e3"];
 dim [label="Dimensionality reduction\\ncompress many features\\ne.g. PCA", fillcolor="#e3f5f3", color="#bfe7e3"];
 ml -> sup; ml -> uns;
 sup -> reg; sup -> cls;
 uns -> clu; uns -> dim;
''', "s_ml_map.png", rd="TB", rs="0.5", ns="0.35")

# 4.1 train/validation/test split
fig,ax=plt.subplots(figsize=(11,3.2)); ax.axis("off"); ax.set_xlim(0,100); ax.set_ylim(-1.4,1.6)
segs=[(0,60,INDIGO,"TRAIN (60%)","fit the model"),
      (60,80,TEAL,"VALIDATION (20%)","tune & compare models"),
      (80,100,ROSE,"TEST (20%)","judge ONCE, at the very end")]
for x0,x1,c,name,role in segs:
    ax.add_patch(FancyBboxPatch((x0+0.6,0),x1-x0-1.2,0.9,boxstyle="round,pad=0.02",facecolor=c,edgecolor="white",lw=2))
    ax.text((x0+x1)/2,0.45,name,ha="center",va="center",color="white",fontsize=12,fontweight="bold")
    ax.text((x0+x1)/2,-0.45,role,ha="center",va="center",color=c,fontsize=10.5)
ax.text(50,1.35,"Split your data BEFORE modeling",ha="center",fontsize=12.5,color=INK,fontweight="bold")
ax.annotate("never let the model see this\nuntil you're done",xy=(90,0),xytext=(90,-1.15),
    ha="center",fontsize=9.5,color=ROSE,arrowprops=dict(arrowstyle="->",color=ROSE,lw=1.2))
save(fig,"s_ml_split.png")

# 4.1 underfit / good fit / overfit
x=np.sort(rng.uniform(0,1,22)); y=np.sin(2*np.pi*x)+rng.normal(0,0.22,22)
grid=np.linspace(0,1,200)
fig,axes=plt.subplots(1,3,figsize=(11.5,4.0),sharey=True)
for ax,(deg,name,c) in zip(axes,[(1,"Underfit (too simple)",ROSE),(4,"Good fit (generalizes)",GREEN),(15,"Overfit (memorizes noise)",AMBER)]):
    coef=np.polyfit(x,y,deg); fit=np.polyval(coef,grid)
    ax.scatter(x,y,s=28,color=INDIGO,alpha=.7,edgecolors="white",lw=.5,zorder=3)
    ax.plot(grid,fit,color=c,lw=2.4)
    ax.set_title(name,color=c,fontsize=12); ax.set_ylim(-1.8,1.8); ax.set_xticks([]); ax.set_yticks([]); despine(ax)
    ax.set_xlabel(f"polynomial degree {deg}")
fig.suptitle("The central problem: fit the signal, not the noise — and generalize to new data",
    fontsize=13.5,fontweight="bold",y=1.02,color=INK)
fig.tight_layout(rect=[0,0,1,0.93]); save(fig,"s_ml_overfit.png")
print("BATCH M DONE")
