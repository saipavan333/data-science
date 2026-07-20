from vstyle import *
dot('''
 users [label="All eligible users", fillcolor="#eef1fd", color="#cdd7fb"];
 rand  [label="Randomly assign\\neach user 50 / 50", shape=diamond, style="filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 ctrl  [label="CONTROL (A)\\nsees the current version", fillcolor="#e9ecf6", color="#c7cee0"];
 treat [label="TREATMENT (B)\\nsees the new version", fillcolor="#eef1fd", color="#cdd7fb"];
 mp    [label="Measure the SAME\\nprimary metric for both", fillcolor="#e3f5f3", color="#bfe7e3"];
 mg    [label="Watch guardrail metrics\\n(latency, revenue, errors)", fillcolor="#fce8ee", color="#e7b9c6"];
 comp  [label="Compare: is B reliably\\nbetter, without breaking a guardrail?", fillcolor="#e6f5ec", color="#bfe0c8"];
 users -> rand;
 rand -> ctrl [label="50%"];
 rand -> treat [label="50%"];
 ctrl -> mp; treat -> mp;
 mp -> comp; mg -> comp;
 {rank=same; mp; mg;}
''', "s_ab_design.png", rd="TB", rs="0.5", ns="0.4")
print("saved s_ab_design.png")

# ---- s_ab_simpson: Simpson's paradox ----
import numpy as np, matplotlib.pyplot as plt
np.random.seed(4)
def grp(x0, x1, y0, slope, n=45):
    x = np.random.uniform(x0, x1, n)
    y = y0 + slope*(x-x0) + np.random.normal(0, 0.5, n)
    return x, y
xa, ya = grp(1, 4.5, 6.2, -0.55)     # group A: low x, negative within-slope
xb, yb = grp(5.5, 9.5, 9.4, -0.55)   # group B: high x, negative within-slope, shifted UP
fig, ax = plt.subplots(figsize=(8.4,5.2))
ax.scatter(xa, ya, s=42, color=INDIGO, edgecolor="white", linewidth=.6, zorder=3, label="Segment A")
ax.scatter(xb, yb, s=42, color=TEAL, edgecolor="white", linewidth=.6, zorder=3, label="Segment B")
# within-group trend lines (both negative)
for xg, yg, c in [(xa,ya,INDIGO),(xb,yb,TEAL)]:
    b1,b0 = np.polyfit(xg,yg,1); xs=np.array([xg.min(),xg.max()])
    ax.plot(xs, b0+b1*xs, color=c, lw=2.4, zorder=2)
# misleading aggregate trend (positive)
allx=np.concatenate([xa,xb]); ally=np.concatenate([ya,yb])
B1,B0=np.polyfit(allx,ally,1); xs=np.array([allx.min(),allx.max()])
ax.plot(xs, B0+B1*xs, color=ROSE, lw=2.6, ls=(0,(5,3)), zorder=2, label="ignoring the groups")
ax.annotate("within each segment,\nthe trend goes DOWN", xy=(3.2, 5.2), xytext=(3.0, 2.6),
            fontsize=10.5, color=INK, ha="center",
            arrowprops=dict(arrowstyle="->", color=INDIGO, lw=1.3))
ax.text(7.3, 10.05, "but pooled together it\nlooks like it goes UP", fontsize=10.5, color="#a3244e",
        ha="center", va="bottom", fontweight="bold")
ax.set_xlabel("value of X"); ax.set_ylabel("outcome")
ax.set_title("Simpson's paradox: the aggregate trend reverses the within-group trend", loc="left", fontsize=12.8)
ax.set_xlim(0.5,10); ax.set_ylim(2,11); despine(ax)
ax.legend(loc="lower right", fontsize=9.6, frameon=True)
save(fig, "s_ab_simpson.png"); print("saved s_ab_simpson.png")
