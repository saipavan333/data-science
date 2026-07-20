import numpy as np, matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle
from vstyle import *
np.random.seed(3)

# ================= 8.4  s_ml_tree: decision tree partitions space =================
from sklearn.datasets import make_blobs
from sklearn.tree import DecisionTreeClassifier
Xb, yb = make_blobs(n_samples=200, centers=[(-2,-1),(2,1.2),(-1.5,2.2)], cluster_std=1.05, random_state=3)
tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xb, yb)
xx, yy = np.meshgrid(np.linspace(Xb[:,0].min()-1, Xb[:,0].max()+1, 400),
                     np.linspace(Xb[:,1].min()-1, Xb[:,1].max()+1, 400))
Z = tree.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
fig, ax = plt.subplots(figsize=(8.2,5.2))
ax.contourf(xx, yy, Z, alpha=0.22, cmap=ListedColormap([INDIGO, TEAL, AMBER]))
ax.contour(xx, yy, Z, colors="white", linewidths=1.4)
cols = np.array([INDIGO, TEAL, AMBER])
ax.scatter(Xb[:,0], Xb[:,1], c=cols[yb], s=34, edgecolor="white", linewidth=.6, zorder=3)
ax.text(0.02, 0.97, "A tree splits the space with straight, axis-aligned cuts\n(each cut is one yes/no question).",
        transform=ax.transAxes, fontsize=10.5, va="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#dfe3ec"))
ax.set_xlabel("feature 1"); ax.set_ylabel("feature 2")
ax.set_title("Decision tree: carving the feature space into boxes", loc="left", fontsize=13.5)
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values(): sp.set_edgecolor("#dfe3ec")
save(fig, "s_ml_tree.png"); print("saved s_ml_tree.png")

# ================= 8.5  s_ml_boosting: sequential improvement =================
from sklearn.ensemble import GradientBoostingRegressor
xr = np.sort(np.random.uniform(0, 6, 60))
yr = np.sin(xr) + np.random.normal(0, 0.18, xr.size)
grid = np.linspace(0, 6, 300)
fig, axes = plt.subplots(1, 3, figsize=(12.4, 4.0), sharey=True)
for ax, n in zip(axes, [1, 10, 150]):
    gb = GradientBoostingRegressor(n_estimators=n, max_depth=2, learning_rate=0.3, random_state=0).fit(xr.reshape(-1,1), yr)
    ax.scatter(xr, yr, s=22, color=INK_FAINT, alpha=.55, zorder=1)
    ax.plot(grid, gb.predict(grid.reshape(-1,1)), color=INDIGO, lw=2.6, zorder=2)
    ax.plot(grid, np.sin(grid), color=GREEN, lw=1.4, ls=(0,(4,3)), zorder=1)
    ax.set_title(("%d tree" % n) + ("" if n==1 else "s"), color=INDIGO_DK, fontsize=12.5)
    ax.set_xticks([]); ax.set_yticks([]); despine(ax, left=False, bottom=False)
    for sp in ax.spines.values(): sp.set_edgecolor("#dfe3ec")
axes[0].set_ylabel("y")
fig.suptitle("Gradient boosting: each new tree fixes the errors the last ones left behind",
             fontsize=13.5, fontweight="bold", x=0.02, ha="left")
axes[2].plot([], [], color=GREEN, ls=(0,(4,3)), label="true pattern"); axes[2].legend(loc="lower center", fontsize=9.5, frameon=True)
fig.tight_layout(rect=[0,0,1,0.93])
save(fig, "s_ml_boosting.png"); print("saved s_ml_boosting.png")

# ================= 8.6  s_ml_kmeans: clustering result =================
from sklearn.cluster import KMeans
Xk, _ = make_blobs(n_samples=280, centers=[(-3,-2),(3,-1),(0,3.2),(4,3)], cluster_std=0.95, random_state=5)
km = KMeans(n_clusters=4, n_init=10, random_state=0).fit(Xk)
fig, ax = plt.subplots(figsize=(8.2,5.2))
pal = np.array([INDIGO, TEAL, AMBER, ROSE])
ax.scatter(Xk[:,0], Xk[:,1], c=pal[km.labels_], s=34, edgecolor="white", linewidth=.5, zorder=2, alpha=.9)
ax.scatter(km.cluster_centers_[:,0], km.cluster_centers_[:,1], marker="X", s=280, c="#111726",
           edgecolor="white", linewidth=1.8, zorder=3, label="cluster centers")
ax.text(0.02, 0.97, "k-means finds k centers and assigns each point to its nearest one,\nthen repeats until the centers stop moving.",
        transform=ax.transAxes, fontsize=10.3, va="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#dfe3ec"))
ax.set_xlabel("feature 1"); ax.set_ylabel("feature 2")
ax.set_title("k-means clustering: structure with no labels (here, k = 4)", loc="left", fontsize=13.5)
ax.set_xticks([]); ax.set_yticks([]); ax.legend(loc="lower right", fontsize=10, frameon=True)
for sp in ax.spines.values(): sp.set_edgecolor("#dfe3ec")
save(fig, "s_ml_kmeans.png"); print("saved s_ml_kmeans.png")

# ================= 8.7  s_ml_kfold: k-fold cross-validation =================
fig, ax = plt.subplots(figsize=(9.2,4.2)); ax.axis("off")
k = 5; W = 10.0; H = 0.62; gap = 0.28
for row in range(k):
    y = (k-1-row)*(H+gap)
    for col in range(k):
        x = col*(W/k)
        is_test = (col == row)
        ax.add_patch(Rectangle((x, y), W/k-0.06, H,
                     facecolor=(AMBER if is_test else INDIGO_BG),
                     edgecolor=(AMBER if is_test else INDIGO), lw=1.3))
        ax.text(x + (W/k)/2 - 0.03, y + H/2, "TEST" if is_test else "train",
                ha="center", va="center", fontsize=9.5,
                color=("white" if is_test else INDIGO_DK), fontweight=("bold" if is_test else "normal"))
    ax.text(W+0.25, y+H/2, "round %d" % (row+1), va="center", fontsize=10, color=INK_SOFT)
ax.text(0, k*(H+gap)+0.15, "5-fold cross-validation: every row trains on 4 folds and tests on the held-out 1;\nrotate through all 5, then average the scores.",
        fontsize=11, color=INK, va="bottom")
ax.set_xlim(-0.2, W+2.0); ax.set_ylim(-0.2, k*(H+gap)+1.0)
save(fig, "s_ml_kfold.png"); print("saved s_ml_kfold.png")
print("ALL ML DIAGRAMS DONE")
