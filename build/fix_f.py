import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from vstyle import *
fig, axes = plt.subplots(1,4, figsize=(12,3.6))
specs=[("inner","keep matches only","lens"),
       ("left","all of left + matches","left"),
       ("right","all of right + matches","right"),
       ("outer","everything","both")]
for ax,(name,desc,mode) in zip(axes,specs):
    ax.set_xlim(-2.2,2.2); ax.set_ylim(-1.9,1.8); ax.set_aspect("equal"); ax.axis("off")
    if mode in ("left","both"):
        ax.add_patch(Circle((-0.6,0),1.1,facecolor=INDIGO,alpha=.32,ec="none"))
    if mode in ("right","both"):
        ax.add_patch(Circle((0.6,0),1.1,facecolor=TEAL,alpha=.32,ec="none"))
    if mode=="lens":
        lens=Circle((-0.6,0),1.1,facecolor="#5b6b86",alpha=.5,ec="none",transform=ax.transData)
        ax.add_patch(lens)
        lens.set_clip_path(Circle((0.6,0),1.1,transform=ax.transData))
    ax.add_patch(Circle((-0.6,0),1.1,fill=False,ec=INDIGO,lw=2))
    ax.add_patch(Circle((0.6,0),1.1,fill=False,ec=TEAL,lw=2))
    ax.text(-1.3,1.25,"left",color=INDIGO_DK,fontsize=10.5,fontweight="bold")
    ax.text(0.95,1.25,"right",color=TEAL,fontsize=10.5,fontweight="bold")
    ax.text(0,-1.45,name,ha="center",fontsize=12.5,color=INK,fontweight="bold")
    ax.text(0,-1.8,desc,ha="center",fontsize=9,color=INK_SOFT)
fig.suptitle("The four joins: which rows survive when you merge two tables on a key",
    fontsize=13.5, fontweight="bold", y=1.02, color=INK)
save(fig,"s_pd_joins.png")
print("FIX F DONE")
