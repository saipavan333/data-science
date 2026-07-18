import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from vstyle import *
def cells(ax, vals, x0=0, y0=0, w=0.95, h=0.95, gap=0.12, fc=INDIGO_BG, ec=INDIGO,
          fs=14, fmt=str, hi=None, hfc=AMBER_BG, hec=AMBER, idx=False):
    hi = hi or set()
    for i,v in enumerate(vals):
        x=x0+i*(w+gap)
        f,e = (hfc,hec) if i in hi else (fc,ec)
        ax.add_patch(Rectangle((x,y0),w,h,facecolor=f,edgecolor=e,lw=1.8))
        ax.text(x+w/2,y0+h/2,fmt(v),ha="center",va="center",fontsize=fs,color=INK,fontweight="bold")
        if idx: ax.text(x+w/2,y0-0.22,str(i),ha="center",va="top",fontsize=11,color=INK_FAINT)

# list/dict with consistent code text (3 keys)
fig, ax = plt.subplots(figsize=(11,3.6)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(-1,3)
ax.text(0,2.6,"list — ordered, accessed by POSITION", fontsize=12.5, color=INDIGO_DK, fontweight="bold")
ax.text(0,2.15,'prices = [12, 45, 7, 30]', fontsize=11.5, color=INK_SOFT, family="monospace")
cells(ax, [12,45,7,30], x0=0.2, y0=0.7, idx=True)
ax.text(0.5,-0.75,"prices[2]  →  7", fontsize=11, color=AMBER, family="monospace")
ax.text(6.4,2.6,"dict — accessed by KEY", fontsize=12.5, color=TEAL, fontweight="bold")
ax.text(6.4,2.15,'user = {"name":"Ada", "age":36, "city":"Austin"}', fontsize=10.5, color=INK_SOFT, family="monospace")
for i,(k,v) in enumerate([("'name'","'Ada'"),("'age'","36"),("'city'","'Austin'")]):
    y=1.4-i*0.62
    ax.add_patch(FancyBboxPatch((6.4,y-0.22),1.5,0.46,boxstyle="round,pad=0.02",facecolor=TEAL_BG,edgecolor=TEAL,lw=1.4))
    ax.text(7.15,y,k,ha="center",va="center",fontsize=12,color=INK,family="monospace")
    ax.annotate("",xy=(9.1,y),xytext=(7.95,y),arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.4))
    ax.add_patch(FancyBboxPatch((9.15,y-0.22),1.5,0.46,boxstyle="round,pad=0.02",facecolor=INDIGO_BG,edgecolor=INDIGO,lw=1.4))
    ax.text(9.9,y,v,ha="center",va="center",fontsize=12,color=INK,family="monospace")
ax.text(6.4,-0.75,'user["age"]  →  36', fontsize=11, color=AMBER, family="monospace")
ax.set_title("Two everyday containers: lists index by number, dicts look up by key", loc="left", fontsize=14)
save(fig,"s_py_listdict.png")

# index/mask with decluttered bottom row
fig, axes = plt.subplots(2,1, figsize=(10.5,4.4)); fig.subplots_adjust(hspace=0.6)
a=np.array([10,25,8,42,17,33,5,29])
for ax in axes: ax.axis("off"); ax.set_xlim(-0.3,8.6); ax.set_ylim(-0.9,1.3)
cells(axes[0],a,x0=0,y0=0,idx=True,hi={2,3,4},w=0.9,gap=0.13)
axes[0].set_title("Slicing  a[2:5]  →  positions 2, 3, 4  (the stop index is excluded)", loc="left", fontsize=12.5)
mask=a>20
cells(axes[1],a,x0=0,y0=0,idx=False,hi=set(np.where(mask)[0]),w=0.9,gap=0.13)
axes[1].set_title("Boolean mask  a[a > 20]  →  keep where the test is True", loc="left", fontsize=12.5)
for i,m in enumerate(mask):
    axes[1].text(i*(0.9+0.13)+0.45,-0.45,"True" if m else "False",ha="center",fontsize=9.5,
                 color=GREEN if m else INK_FAINT, fontweight="bold")
save(fig,"s_np_index.png")
print("FIX D DONE")
