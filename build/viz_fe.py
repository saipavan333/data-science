# -*- coding: utf-8 -*-
import numpy as np, matplotlib.pyplot as plt, subprocess, os
from vstyle import save, despine, dot, INDIGO, INDIGO_BG, TEAL, TEAL_BG, AMBER, ROSE, ROSE_BG, GREEN, GREEN_BG, INK, INK_SOFT, INK_FAINT
IMG="/sessions/zen-pensive-thompson/mnt/data-science-academy/assets/img"

# 9.2 — skew + log transform (two histograms)
rng=np.random.default_rng(3)
x=rng.lognormal(mean=1.0, sigma=0.9, size=6000)
fig,axs=plt.subplots(1,2,figsize=(9.4,4.3))
axs[0].hist(x,bins=60,color=INDIGO,alpha=0.85,edgecolor="white",linewidth=0.3)
axs[0].set_title("Raw feature: right-skewed",fontsize=13)
axs[0].set_xlabel("value"); axs[0].set_ylabel("count")
axs[0].axvline(x.mean(),color=ROSE,lw=2,ls="--")
axs[0].text(x.mean()+1.0,axs[0].get_ylim()[1]*0.8,"mean dragged\nright by the tail",color=ROSE,fontsize=10)
lx=np.log1p(x)
axs[1].hist(lx,bins=60,color=TEAL,alpha=0.85,edgecolor="white",linewidth=0.3)
axs[1].set_title("After log transform: ~symmetric",fontsize=13)
axs[1].set_xlabel("log(1 + value)"); axs[1].set_ylabel("count")
for a in axs: despine(a)
fig.suptitle("A log transform tames a heavy right tail",fontsize=14,fontweight="bold",y=1.02)
save(fig,"s_fe_skew.png")

# 9.4 — cyclical encoding of hour-of-day on a circle
fig,ax=plt.subplots(figsize=(5.6,5.6))
hours=np.arange(24)
ang=2*np.pi*hours/24
xs,ys=np.sin(ang),np.cos(ang)
ax.plot(np.sin(np.linspace(0,2*np.pi,200)),np.cos(np.linspace(0,2*np.pi,200)),color="#e2e6ee",lw=1.5,zorder=1)
ax.scatter(xs,ys,s=70,color=INDIGO,zorder=3)
for h in [0,6,12,18]:
    a=2*np.pi*h/24
    ax.annotate(f"{h:02d}:00",(np.sin(a),np.cos(a)),textcoords="offset points",
                xytext=(0,0),ha="center",va="center",fontsize=8.5,color="white",fontweight="bold",zorder=4)
# highlight adjacency of 23:00 and 00:00
for h,c in [(23,ROSE),(0,GREEN)]:
    a=2*np.pi*h/24
    ax.scatter([np.sin(a)],[np.cos(a)],s=260,facecolor="none",edgecolor=c,lw=2.6,zorder=5)
ax.annotate("23:00 and 00:00 are\nADJACENT on the circle\n(but 23 vs 0 looks far as raw ints)",
            (0.02,1.16),ha="center",fontsize=10.5,color=INK,fontweight="bold")
ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.5,1.6); ax.set_aspect("equal")
ax.set_xlabel("sin(2π · hour / 24)"); ax.set_ylabel("cos(2π · hour / 24)")
ax.set_title("Cyclical encoding: map hour to (sin, cos)",fontsize=13,pad=26)
despine(ax)
save(fig,"s_fe_cyclical.png")

# 9.5 — leakage pipeline (wrong vs right)
dot(r'''
 subgraph cluster_w {label="WRONG  —  leaks test info"; style="rounded,filled"; fillcolor="#fce8ee"; color="#eab6c6"; fontname="Helvetica-Bold"; fontsize=12; fontcolor="#c2305a";
   w1 [label="ALL data", fillcolor="white", color="#eab6c6"];
   w2 [label="fit scaler /\nselect features\n(sees test!)", fillcolor="white", color="#eab6c6"];
   w3 [label="split &\nvalidate", fillcolor="white", color="#eab6c6"];
   w1 -> w2 -> w3 [color="#c2305a"];
 }
 subgraph cluster_r {label="RIGHT  —  fit on train only"; style="rounded,filled"; fillcolor="#e6f5ec"; color="#b0dcc0"; fontname="Helvetica-Bold"; fontsize=12; fontcolor="#1f8a4c";
   r1 [label="split FIRST", fillcolor="white", color="#b0dcc0"];
   r2 [label="fit scaler /\nselect on TRAIN", fillcolor="white", color="#b0dcc0"];
   r3 [label="apply to test\n& validate", fillcolor="white", color="#b0dcc0"];
   r1 -> r2 -> r3 [color="#1f8a4c"];
 }
''', "s_fe_leakage.png", rd="LR", rs="0.55", ns="0.35")
print("done")
