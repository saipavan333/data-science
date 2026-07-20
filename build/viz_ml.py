import numpy as np, matplotlib.pyplot as plt
from vstyle import *
np.random.seed(7)

# ---- s_ml_linreg: least-squares fit with residuals ----
x = np.array([1,2,3,4,5,6,7,8,9,10], dtype=float)
y = np.array([2.1,3.9,3.2,5.8,5.1,7.4,7.9,7.2,9.6,9.1])
b, a = np.polyfit(x, y, 1)          # slope, intercept
yhat = a + b*x

fig, ax = plt.subplots(figsize=(8.4,5.0))
# residual segments
for xi, yi, yp in zip(x, y, yhat):
    ax.plot([xi, xi], [yi, yp], color=ROSE, lw=1.6, ls=(0,(3,2)), zorder=1)
ax.plot(x, yhat, color=INDIGO, lw=2.6, zorder=2, label="best-fit line  $\\hat{y}=a+bx$")
ax.scatter(x, y, s=70, color=INDIGO_DK, zorder=3, edgecolor="white", linewidth=1.2, label="actual data")
# annotate one residual
i = 5
ax.annotate("residual = actual $-$ predicted",
            xy=(x[i], (y[i]+yhat[i])/2), xytext=(x[i]-3.1, y[i]+1.9),
            fontsize=11, color=ROSE,
            arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.4))
ax.scatter([x[i]],[yhat[i]], s=45, facecolor="white", edgecolor=INDIGO, zorder=4, linewidth=1.6)
ax.text(0.03, 0.94, "Least squares picks the line that makes the\nsum of the squared residuals as small as possible.",
        transform=ax.transAxes, fontsize=11, color=INK, va="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor=INDIGO_BG, edgecolor="#cdd7fb"))
ax.set_xlabel("advertising spend ($000s)"); ax.set_ylabel("sales ($000s)")
ax.set_title("Linear regression: the line of best fit and its residuals", loc="left", fontsize=13.5)
ax.legend(loc="lower right", frameon=True, fontsize=10.5)
ax.set_xlim(0,11); ax.set_ylim(0,12); despine(ax)
save(fig, "s_ml_linreg.png")
print("saved s_ml_linreg.png  (slope=%.3f intercept=%.3f)"%(b,a))
