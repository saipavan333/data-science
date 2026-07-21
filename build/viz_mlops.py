# -*- coding: utf-8 -*-
import numpy as np, matplotlib.pyplot as plt
from vstyle import save, despine, dot, INDIGO, TEAL, AMBER, ROSE, GREEN, INK, INK_SOFT, INK_FAINT
IMG="/sessions/zen-pensive-thompson/mnt/data-science-academy/assets/img"

# 11.1 — the ML lifecycle loop
dot(r'''
 d [label="Collect &\nprepare data", fillcolor="#eef1fd", color="#cdd7fb"];
 t [label="Train\nmodel", fillcolor="#e3f5f3", color="#a9ddd8"];
 e [label="Evaluate\n(offline)", fillcolor="#fbf3e0", color="#e9cf9a"];
 s [label="Deploy &\nserve", fillcolor="#e6f5ec", color="#b0dcc0"];
 m [label="Monitor\n(live)", fillcolor="#fce8ee", color="#eab6c6"];
 d -> t -> e -> s -> m;
 m -> t [label="  drift detected -> retrain", style=dashed, color="#c2305a", fontcolor="#c2305a", constraint=false];
''', "s_mlops_lifecycle.png", rd="LR", rs="0.62", ns="0.4")

# 11.4 — model decay + retrain
fig,ax=plt.subplots(figsize=(8.2,4.5))
t=np.arange(0,21)
perf=np.piecewise(t.astype(float),
    [t<12, t>=12],
    [lambda t: 0.90-0.010*t, lambda t: 0.90-0.010*(t-12)])
ax.plot(t[t<=12],perf[t<=12],'-o',color=INDIGO,lw=2.6,ms=5)
ax.plot(t[t>=12],perf[t>=12],'-o',color=INDIGO,lw=2.6,ms=5)
ax.plot([11,12],[perf[11],perf[12]],':',color=INK_FAINT,lw=1.6)  # retrain jump
ax.axvline(12,color=GREEN,ls="--",lw=1.8)
ax.annotate("retrain\n(fresh data)",(12,0.905),xytext=(13.4,0.88),fontsize=10.5,color=GREEN,fontweight="bold",
            arrowprops=dict(arrowstyle="->",color=GREEN,lw=1.6))
ax.annotate("performance decays\nas the world drifts",(6,0.84),xytext=(1.6,0.70),fontsize=10.5,color=ROSE,
            arrowprops=dict(arrowstyle="->",color=ROSE,lw=1.6))
ax.axhline(0.80,color=AMBER,ls=":",lw=1.6)
ax.text(0.3,0.805,"alert threshold",fontsize=9.6,color=AMBER,fontweight="bold")
ax.set_xlabel("weeks since deploy"); ax.set_ylabel("live accuracy")
ax.set_ylim(0.66,0.94); ax.set_xlim(-0.5,20.5)
ax.set_title("Models decay: monitor, alert, retrain — the loop never ends",fontsize=13)
despine(ax); save(fig,"s_mlops_drift.png")
print("done")
