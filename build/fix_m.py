import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from vstyle import *
fig,ax=plt.subplots(figsize=(11,3.4)); ax.axis("off"); ax.set_xlim(0,100); ax.set_ylim(-1.6,1.7)
segs=[(0,60,INDIGO,"TRAIN","60%","fit the model"),
      (60,80,TEAL,"VALIDATION","20%","tune / compare"),
      (80,100,ROSE,"TEST","20%","judge — once")]
for x0,x1,c,name,pct,role in segs:
    cx=(x0+x1)/2
    ax.add_patch(FancyBboxPatch((x0+0.6,0),x1-x0-1.2,0.95,boxstyle="round,pad=0.02",facecolor=c,edgecolor="white",lw=2))
    ax.text(cx,0.62,name,ha="center",va="center",color="white",fontsize=12,fontweight="bold")
    ax.text(cx,0.28,pct,ha="center",va="center",color="white",fontsize=10.5)
    ax.text(cx,-0.42,role,ha="center",va="center",color=c,fontsize=10)
ax.text(50,1.45,"Split your data BEFORE modeling",ha="center",fontsize=12.5,color=INK,fontweight="bold")
ax.annotate("never let the model see the test set\nuntil you are completely done",xy=(90,-0.02),
    xytext=(72,-1.3),ha="center",fontsize=9.5,color=ROSE,arrowprops=dict(arrowstyle="->",color=ROSE,lw=1.2))
save(fig,"s_ml_split.png")
print("FIX M DONE")
