import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
from vstyle import *

def minitable(ax, cols, rows, x0, y0, cw=1.4, ch=0.5, fc="white", hfc="#f0f2f8", ec="#d8dce3", fs=10.5):
    for j,c in enumerate(cols):
        ax.add_patch(Rectangle((x0+j*cw,y0),cw,ch,facecolor=hfc,edgecolor=ec,lw=1.1))
        ax.text(x0+j*cw+cw/2,y0+ch/2,c,ha="center",va="center",fontsize=fs,fontweight="bold",color=INK_SOFT)
    for i,r in enumerate(rows):
        yy=y0-(i+1)*ch
        for j,v in enumerate(r):
            ax.add_patch(Rectangle((x0+j*cw,yy),cw,ch,facecolor=fc,edgecolor=ec,lw=1.0))
            ax.text(x0+j*cw+cw/2,yy+ch/2,str(v),ha="center",va="center",fontsize=fs,color=INK)

# --- 2.5 split-apply-combine ---
fig, ax = plt.subplots(figsize=(11.5,5.0)); ax.axis("off"); ax.set_xlim(0,15); ax.set_ylim(-0.5,6)
minitable(ax, ["category","amt"], [["Electronics",180],["Apparel",45],["Electronics",220],["Beauty",30]],
          x0=0.2, y0=4.2, cw=1.6)
ax.text(0.2,5.2,"1. the data", fontsize=11, color=INK_SOFT, fontweight="bold")
ax.annotate("SPLIT\nby category", xy=(4.5,3.2), xytext=(3.7,3.2), fontsize=10.5, color=INDIGO_DK,
            ha="center", va="center", arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.4))
# groups
groups=[("Electronics",[180,220],TEAL,TEAL_BG),("Apparel",[45],AMBER,AMBER_BG),("Beauty",[30],ROSE,ROSE_BG)]
for k,(name,vals,c,cb) in enumerate(groups):
    yy=5.0-k*1.7
    ax.add_patch(FancyBboxPatch((5.0,yy-1.0),3.0,1.2,boxstyle="round,pad=0.04",facecolor=cb,edgecolor=c,lw=1.5))
    ax.text(6.5,yy-0.05,name,ha="center",fontsize=10.5,color=c,fontweight="bold")
    ax.text(6.5,yy-0.55,"amt = "+", ".join(map(str,vals)),ha="center",fontsize=10,color=INK)
ax.text(5.0,5.4,"2. split into groups", fontsize=11, color=INK_SOFT, fontweight="bold")
ax.annotate("APPLY sum()\n+ COMBINE", xy=(11.3,3.2), xytext=(9.4,3.2), fontsize=10.5, color=GREEN,
            ha="center", va="center", arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.4))
minitable(ax, ["category","total"], [["Electronics",400],["Apparel",45],["Beauty",30]], x0=11.3, y0=4.0, cw=1.7)
ax.text(11.3,5.0,"3. one row per group", fontsize=11, color=INK_SOFT, fontweight="bold")
ax.text(7.5,0.0,'df.groupby("category")["amt"].sum()', ha="center", fontsize=12.5, color=INK,
        family="monospace", bbox=dict(boxstyle="round,pad=0.4",facecolor="#f7f8fa",edgecolor="#d8dce3"))
ax.set_title("groupby = split · apply · combine", loc="left", fontsize=14)
save(fig,"s_pd_groupby.png")

# --- 2.5 pivot / melt (wide <-> long) ---
fig, ax = plt.subplots(figsize=(11,4.6)); ax.axis("off"); ax.set_xlim(0,13); ax.set_ylim(-0.5,5)
ax.text(0.2,4.4,"LONG (tidy): one row per observation", fontsize=11.5, color=TEAL, fontweight="bold")
minitable(ax, ["month","metric","value"],
          [["Jan","sales",100],["Jan","cost",60],["Feb","sales",120],["Feb","cost",70]],
          x0=0.2, y0=3.6, cw=1.5)
ax.text(8.0,4.4,"WIDE: one row per month", fontsize=11.5, color=INDIGO_DK, fontweight="bold")
minitable(ax, ["month","sales","cost"], [["Jan",100,60],["Feb",120,70]], x0=8.0, y0=3.6, cw=1.5)
ax.annotate("", xy=(7.9,2.7), xytext=(5.3,2.7), arrowprops=dict(arrowstyle="->",color=INDIGO,lw=2.0))
ax.text(6.6,2.95,"pivot →\n(long to wide)", ha="center", fontsize=10.5, color=INDIGO_DK)
ax.annotate("", xy=(5.3,2.0), xytext=(7.9,2.0), arrowprops=dict(arrowstyle="->",color=TEAL,lw=2.0))
ax.text(6.6,1.55,"← melt\n(wide to long)", ha="center", fontsize=10.5, color=TEAL)
ax.set_title("Reshaping: pivot widens, melt lengthens — same data, different layout", loc="left", fontsize=14)
save(fig,"s_pd_pivot_melt.png")

# --- 2.5 joins ---
fig, axes = plt.subplots(1,4, figsize=(12,3.4))
joins=[("inner","keep matches only",[(0,0)]),
       ("left","all of left + matches",[(-1,0),(0,0)]),
       ("right","all of right + matches",[(0,0),(1,0)]),
       ("outer","everything",[(-1,0),(0,0),(1,0)])]
for ax,(name,desc,shaded) in zip(axes,joins):
    ax.set_xlim(-2.2,2.2); ax.set_ylim(-1.8,1.8); ax.set_aspect("equal"); ax.axis("off")
    # shading by region: left-only, intersection, right-only
    if (-1,0) in shaded: ax.add_patch(Circle((-0.6,0),1.1,facecolor=INDIGO,alpha=.30,ec="none"))
    if (1,0) in shaded:  ax.add_patch(Circle((0.6,0),1.1,facecolor=TEAL,alpha=.30,ec="none"))
    if (0,0) in shaded:
        # intersection: draw both with clip is complex; approximate by a lens via overlapping alpha
        ax.add_patch(Circle((-0.6,0),1.1,facecolor=INDIGO,alpha=.22,ec="none"))
        ax.add_patch(Circle((0.6,0),1.1,facecolor=TEAL,alpha=.22,ec="none"))
    ax.add_patch(Circle((-0.6,0),1.1,fill=False,ec=INDIGO,lw=2))
    ax.add_patch(Circle((0.6,0),1.1,fill=False,ec=TEAL,lw=2))
    ax.text(-1.25,1.2,"left",color=INDIGO_DK,fontsize=10.5,fontweight="bold")
    ax.text(0.95,1.2,"right",color=TEAL,fontsize=10.5,fontweight="bold")
    ax.text(0,-1.4,f"{name}",ha="center",fontsize=12.5,color=INK,fontweight="bold")
    ax.text(0,-1.75,desc,ha="center",fontsize=9,color=INK_SOFT)
fig.suptitle("The four joins: which rows survive when you merge two tables on a key",
    fontsize=13.5, fontweight="bold", y=1.02, color=INK)
save(fig,"s_pd_joins.png")
print("BATCH F DONE")
