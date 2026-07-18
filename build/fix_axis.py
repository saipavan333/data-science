import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from vstyle import *

fig,ax=plt.subplots(figsize=(10.6,6.0)); ax.axis("off")
ax.set_xlim(-2.3,5.7); ax.set_ylim(-1.7,5.0)
M=np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
for r in range(4):
    for c in range(3):
        ax.add_patch(Rectangle((c,3-r),0.9,0.9,facecolor=INDIGO_BG,edgecolor=INDIGO,lw=1.3))
        ax.text(c+0.45,3-r+0.45,str(M[r,c]),ha="center",va="center",fontsize=13,color=INK)

# --- axis=0 : collapses rows -> one sum PER COLUMN, shown at the bottom. Arrow points DOWN, left margin.
ax.annotate("",xy=(-0.7,-0.18),xytext=(-0.7,3.95),
            arrowprops=dict(arrowstyle="-|>",color=ROSE,lw=2.4))
colsum=M.sum(axis=0)
for c in range(3):
    ax.text(c+0.45,-0.62,str(colsum[c]),ha="center",va="center",color=ROSE,fontsize=13,fontweight="bold")
ax.text(-1.05,-0.95,"axis=0\ndown the columns",ha="center",va="top",color=ROSE,fontsize=11,fontweight="bold")

# --- axis=1 : collapses columns -> one sum PER ROW, shown at the right. Arrow points RIGHT, top margin.
ax.annotate("",xy=(3.1,4.25),xytext=(-0.05,4.25),
            arrowprops=dict(arrowstyle="-|>",color=TEAL,lw=2.4))
rowsum=M.sum(axis=1)
for r in range(4):
    ax.text(3.5,3-r+0.45,str(rowsum[r]),ha="center",va="center",color=TEAL,fontsize=13,fontweight="bold")
ax.text(3.95,4.25,"axis=1\nacross rows",ha="left",va="center",color=TEAL,fontsize=11,fontweight="bold")

ax.set_title("NumPy axis: the dimension that DISAPPEARS when you aggregate",loc="left",fontsize=13)
save(fig,"s_np_axis.png")
print("AXIS FIX DONE")
