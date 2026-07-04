import numpy as np, timeit, matplotlib.pyplot as plt
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

# --- 2.1 list vs dict ---
fig, ax = plt.subplots(figsize=(11,3.6)); ax.axis("off")
ax.set_xlim(0,12); ax.set_ylim(-1,3)
ax.text(0,2.6,"list — ordered, accessed by POSITION", fontsize=12.5, color=INDIGO_DK, fontweight="bold")
ax.text(0,2.15,'prices = [12, 45, 7, 30]', fontsize=11.5, color=INK_SOFT, family="monospace")
cells(ax, [12,45,7,30], x0=0.2, y0=0.7, idx=True)
ax.text(0.2+2*(0.95+0.12)+0.1,-0.75,"prices[2]  →  7", fontsize=11, color=AMBER, family="monospace")
# dict
ax.text(6.4,2.6,"dict — accessed by KEY", fontsize=12.5, color=TEAL, fontweight="bold")
ax.text(6.4,2.15,'user = {"name": "Ada", "age": 36}', fontsize=11.5, color=INK_SOFT, family="monospace")
pairs=[("'name'","'Ada'"),("'age'","36"),("'city'","'Austin'")]
for i,(k,v) in enumerate(pairs):
    y=1.4-i*0.62
    ax.add_patch(FancyBboxPatch((6.4,y-0.22),1.5,0.46,boxstyle="round,pad=0.02",facecolor=TEAL_BG,edgecolor=TEAL,lw=1.4))
    ax.text(7.15,y,k,ha="center",va="center",fontsize=12,color=INK,family="monospace")
    ax.annotate("",xy=(9.1,y),xytext=(7.95,y),arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.4))
    ax.add_patch(FancyBboxPatch((9.15,y-0.22),1.5,0.46,boxstyle="round,pad=0.02",facecolor=INDIGO_BG,edgecolor=INDIGO,lw=1.4))
    ax.text(9.9,y,v,ha="center",va="center",fontsize=12,color=INK,family="monospace")
ax.text(6.4,-0.75,'user["age"]  →  36', fontsize=11, color=AMBER, family="monospace")
ax.set_title("Two everyday containers: lists index by number, dicts look up by key", loc="left", fontsize=14)
save(fig,"s_py_listdict.png")

# --- 2.2 NumPy speed: loop vs vectorized (real timings) ---
n=1_000_000
pylist=list(range(n)); arr=np.arange(n)
loop=min(timeit.repeat(lambda:[x*2+1 for x in pylist], number=1, repeat=3))*1000
vec =min(timeit.repeat(lambda:arr*2+1, number=1, repeat=3))*1000
fig, ax = plt.subplots(figsize=(9,4.2))
bars=ax.bar(["Python loop\n(list comprehension)","NumPy vectorized\n(arr*2+1)"],[loop,vec],
            color=[ROSE,TEAL], width=.55)
ax.set_ylabel("time for 1,000,000 elements (ms)"); despine(ax)
for b,v in zip(bars,[loop,vec]):
    ax.text(b.get_x()+b.get_width()/2, v+max(loop,vec)*0.02, f"{v:.1f} ms", ha="center", fontsize=12, fontweight="bold", color=INK_SOFT)
ax.set_title(f"Same result, ~{loop/vec:.0f}× faster: vectorize instead of looping", loc="left")
save(fig,"s_np_speed.png")

# --- 2.2 broadcasting ---
fig, axes = plt.subplots(1,2, figsize=(11,4.2))
for ax in axes: ax.axis("off"); ax.set_xlim(0,8.5); ax.set_ylim(-0.5,4)
# panel 1: matrix + scalar
A=np.array([[1,2,3],[4,5,6],[7,8,9]])
def grid(ax,M,x0,y0,fc=INDIGO_BG,ec=INDIGO):
    for r in range(M.shape[0]):
        for c in range(M.shape[1]):
            ax.add_patch(Rectangle((x0+c*0.7,y0-r*0.7),0.66,0.66,facecolor=fc,edgecolor=ec,lw=1.4))
            ax.text(x0+c*0.7+0.33,y0-r*0.7+0.33,str(M[r,c]),ha="center",va="center",fontsize=11,color=INK)
grid(axes[0],A,0.2,3.2)
axes[0].text(2.6,1.9,"+",fontsize=22,color=INK_SOFT,ha="center")
axes[0].add_patch(Rectangle((3.1,1.6),0.66,0.66,facecolor=AMBER_BG,edgecolor=AMBER,lw=1.6))
axes[0].text(3.43,1.93,"10",ha="center",va="center",fontsize=12,color=INK)
axes[0].text(4.3,1.9,"=",fontsize=22,color=INK_SOFT,ha="center")
grid(axes[0],A+10,4.9,3.2,fc=GREEN_BG,ec=GREEN)
axes[0].set_title("array + scalar: the 10 is 'stretched' to every cell", fontsize=12.5)
# panel 2: matrix + row vector
grid(axes[1],A,0.2,3.2)
axes[1].text(2.6,1.9,"+",fontsize=22,color=INK_SOFT,ha="center")
for c,val in enumerate([10,20,30]):
    axes[1].add_patch(Rectangle((3.1+c*0.7,1.6),0.66,0.66,facecolor=AMBER_BG,edgecolor=AMBER,lw=1.6))
    axes[1].text(3.43+c*0.7,1.93,str(val),ha="center",va="center",fontsize=11,color=INK)
axes[1].text(5.5,1.9,"=",fontsize=22,color=INK_SOFT,ha="center")
grid(axes[1],A+np.array([10,20,30]),6.0,3.2,fc=GREEN_BG,ec=GREEN)
axes[1].set_title("array + row: the row is reused for every row", fontsize=12.5)
fig.suptitle("Broadcasting: NumPy stretches smaller shapes to fit — no loops, no copies",
    fontsize=14, fontweight="bold", y=1.02, color=INK)
save(fig,"s_np_broadcast.png")

# --- 2.2 indexing & boolean mask ---
fig, axes = plt.subplots(2,1, figsize=(10.5,4.2))
a=np.array([10,25,8,42,17,33,5,29])
for ax in axes: ax.axis("off"); ax.set_xlim(-0.3,8.6); ax.set_ylim(-0.8,1.4)
cells(axes[0],a,x0=0,y0=0,idx=True,hi={2,3,4},w=0.9,gap=0.13)
axes[0].set_title("Slicing  a[2:5]  → grabs positions 2,3,4  (stop is excluded)", loc="left", fontsize=12.5)
mask=a>20
cells(axes[1],a,x0=0,y0=0,idx=True,hi=set(np.where(mask)[0]),w=0.9,gap=0.13)
axes[1].set_title("Boolean mask  a[a > 20]  → keeps only the highlighted values", loc="left", fontsize=12.5)
for i,m in enumerate(mask):
    axes[1].text(i*(0.9+0.13)+0.45,-0.55,"T" if m else "F",ha="center",fontsize=10.5,
                 color=GREEN if m else INK_FAINT, fontweight="bold")
save(fig,"s_np_index.png")
print("BATCH D DONE  | loop=%.0fms vec=%.1fms speedup=%.0fx"%(loop,vec,loop/vec))
