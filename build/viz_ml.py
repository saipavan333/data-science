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

# ---- s_ml_sigmoid: logistic regression maps a score to a probability ----
from sklearn.linear_model import LogisticRegression
xs = np.array([1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5]).reshape(-1,1)
ys = np.array([0,0,0,0,1,0,1,1,1,1,1,1])
clf = LogisticRegression().fit(xs, ys)
grid = np.linspace(0.3, 7.2, 300).reshape(-1,1)
prob = clf.predict_proba(grid)[:,1]
boundary = -clf.intercept_[0]/clf.coef_[0][0]   # x where prob = 0.5

fig, ax = plt.subplots(figsize=(8.4,5.0))
ax.axhline(0.5, color=INK_FAINT, lw=1.3, ls=(0,(4,3)))
ax.axvline(boundary, color=AMBER, lw=1.8, ls=(0,(4,3)))
ax.plot(grid.ravel(), prob, color=INDIGO, lw=2.8, zorder=3,
        label="P(pass) $= \\dfrac{1}{1+e^{-z}}$")
ax.scatter(xs.ravel()[ys==0], ys[ys==0], s=70, color=ROSE, zorder=4,
           edgecolor="white", linewidth=1.1, label="actual: fail (0)")
ax.scatter(xs.ravel()[ys==1], ys[ys==1], s=70, color=GREEN, zorder=4,
           edgecolor="white", linewidth=1.1, label="actual: pass (1)")
ax.text(boundary+0.12, 0.06, "decision boundary\n(prob = 0.5)", color=AMBER, fontsize=10.5, va="bottom")
ax.text(0.35, 0.55, "threshold 0.5", color=INK_SOFT, fontsize=10)
ax.annotate("above the line → predict PASS", xy=(6.2,0.95), xytext=(3.5,0.72),
            fontsize=10.5, color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.3))
ax.annotate("below → predict FAIL", xy=(1.6,0.06), xytext=(3.2,0.24),
            fontsize=10.5, color=ROSE, arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.3))
ax.set_xlabel("hours studied"); ax.set_ylabel("probability of passing")
ax.set_title("Logistic regression: a score squashed into a probability", loc="left", fontsize=13.5)
ax.set_xlim(0.3,7.2); ax.set_ylim(-0.08,1.08); despine(ax)
ax.legend(loc="center right", frameon=True, fontsize=9.8)
save(fig, "s_ml_sigmoid.png")
print("saved s_ml_sigmoid.png  (boundary x=%.2f)"%boundary)
