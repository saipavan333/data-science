# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Everything so far has been ~supervised~: you had labelled examples and learned to predict the "
 "label. But often you have **no labels at all** &mdash; just a pile of customers, transactions, or "
 "documents &mdash; and the question is \"what natural groups are hiding in here?\" That's "
 "~unsupervised learning~, and its workhorse is ~clustering~: finding groups of similar things "
 "without anyone telling you what the groups are. It powers customer segmentation, anomaly "
 "detection, and the first exploratory look at any unlabelled dataset."))

p.append(B.h2("k-means: the idea in one breath", kicker="Concept"))
p.append(B.concept(
 "~k-means~ is the clustering algorithm you'll meet first and use most. You tell it how many groups "
 "you want (`k`), and it finds `k` ~centroids~ (group centres) by repeating two simple steps until "
 "nothing changes:\n\n"
 "1. **Assign** every point to its **nearest** centroid.\n"
 "2. **Move** each centroid to the **average** of the points assigned to it.\n\n"
 "That's it &mdash; assign, move, assign, move. Each round can only tighten the groups, so it "
 "settles quickly. The result is `k` clusters where every point belongs to the nearest centre:"))
p.append(B.figure(IMG+"s_ml_kmeans.png",
 "**k-means clustering with k = 4.** Each point is coloured by the centroid (the black &times;) it "
 "ended up closest to. No labels were used &mdash; the structure came purely from which points sit "
 "near each other.",
 "A 2-D scatter of four coloured clusters, each with a black X marking its centroid."))
p.append(B.concept(
 "Run the loop yourself below. The centres start in random spots; each **Step** does one round of "
 "\"assign then move.\" Watch them slide into the three groups and lock in place &mdash; and notice "
 "that a different random start can occasionally settle into a slightly different answer:"))
p.append(B.widget("kmeans", "Step through k-means, one iteration at a time",
 "The big &times; marks are the centres. Each **Step**: (1) every point takes the colour of its "
 "nearest centre, then (2) each centre jumps to the average of its points. Press it a few times and "
 "watch them converge; press **New random start** to see how the starting position can change where "
 "it lands.", height=400))

p.append(B.h2("The hard part: choosing k", kicker="Concept · the real question")
)
p.append(B.concept(
 "k-means needs you to pick `k` up front &mdash; but the whole point is that you *don't know* how "
 "many groups there are. Two standard ways to choose: the ~elbow method~ plots the within-cluster "
 "spread (~inertia~) against `k` and looks for the \"elbow\" where adding groups stops helping much; "
 "the ~silhouette score~ measures how well-separated the clusters are (higher is better) for each "
 "`k`. Neither gives a magic answer &mdash; clustering is ~exploratory~, and the \"right\" `k` is "
 "often the one that yields groups a human finds **useful and interpretable**, not just "
 "mathematically tidy."))

p.append(B.h2("Cluster, then measure and choose", kicker="Worked example"))
p.append(B.concept(
 "`k-means` is one line. Here we cluster some data, read the inertia, and sweep a few values of `k` "
 "to see the elbow &mdash; inertia always falls as `k` rises, but the *drops* get small past the "
 "true number of groups:"))
_c,_o=_run(r'''
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.9, random_state=5)

km = KMeans(n_clusters=4, n_init=10, random_state=0).fit(X)
print(f"cluster sizes: {[int((km.labels_ == c).sum()) for c in range(4)]}")
print(f"inertia (total within-cluster spread): {km.inertia_:.0f}")
print()
print("elbow sweep — inertia for each k:")
for k in range(2, 7):
    m = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print(f"  k={k}:  inertia = {m.inertia_:7.0f}")
''')
p.append(B.code_example(_c,_o,filename="kmeans.py"))
p.append(B.concept(
 "See the drop from k=3 to k=4 versus k=4 to k=5: inertia keeps falling, but the **improvement "
 "flattens** right after 4 &mdash; the elbow &mdash; matching the four groups we generated. That "
 "flattening is your signal that more clusters are just carving up already-tight groups."))

p.append(B.h2("Your turn — cluster and read the inertia", kicker="Interactive lab"))
p.append(B.pylab(
 "`X` is loaded (unlabelled data) and `KMeans` is imported. Fit k-means with **k = 3** (use "
 "`n_init=10, random_state=0`), then assign to **`answer`** the model's ~inertia~ rounded to the "
 "nearest whole number (`round(..., 0)` then `int(...)`).",
 "from sklearn.datasets import make_blobs\n"
 "from sklearn.cluster import KMeans\n"
 "X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.9, random_state=5)\n",
 "km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)\n"
 "answer = int(round(km.inertia_, 0))",
 starter="# X loaded (no labels); KMeans imported\nkm = \nanswer = ",
 hint="Fit `KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)`, then read `km.inertia_` and "
      "convert with `int(round(..., 0))`.",
 title="Lab — fit k-means, report inertia",
 preview="`X` &rarr; 300 unlabelled 2-D points; `KMeans` imported. First Run loads scikit-learn.",
 explain="Inertia is the total squared distance of points to their centre &mdash; with k=3 on "
         "four real groups it's higher than k=4 would give, which is why the elbow sits at 4."))

p.append(B.keypoints([
 "~Unsupervised learning~ finds structure with **no labels**; ~clustering~ groups similar points.",
 "~k-means~ repeats two steps until stable: **assign** each point to the nearest ~centroid~, then "
 "**move** each centroid to its points' average.",
 "You must choose `k` in advance; use the ~elbow method~ (inertia vs k) or ~silhouette score~ to "
 "guide it &mdash; but the useful `k` is often a judgement call.",
 "k-means assumes roughly round, similar-sized clusters and is **sensitive to feature scale** "
 "&mdash; standardise first.",
 "Different random starts can give different results; `n_init` runs it several times and keeps the "
 "best.",
]))

p.append(B.quiz([
 {"q":"What are the two repeating steps of k-means?",
  "options":[
   {"t":"Assign each point to its nearest centroid, then move each centroid to the mean of its "
        "assigned points","correct":True,
    "why":"Correct. Assign-then-move, repeated until the centroids stop shifting — that's the entire "
          "algorithm."},
   {"t":"Split the data into train and test, then fit a tree",
    "why":"That's supervised modelling. k-means has no labels and no train/test split; it alternates "
          "assignment and centroid updates."},
   {"t":"Compute the correlation, then drop the weakest feature",
    "why":"That's unrelated (feature selection). k-means assigns points and moves centres."},
   {"t":"Fit a line, then minimize squared residuals",
    "why":"That's linear regression. k-means minimizes distance to centroids via assign/move steps."}]},
 {"q":"Why do we standardize (scale) features before k-means?",
  "options":[
   {"t":"k-means uses distances, so a feature on a bigger numeric scale would dominate the clustering","correct":True,
    "why":"Correct. Nearest-centroid is a distance computation; an unscaled feature (e.g., income in "
          "thousands vs age in years) would swamp the others, so you standardize to give them equal "
          "footing."},
   {"t":"Because k-means can't handle negative numbers",
    "why":"It handles negatives fine. The issue is that differing scales distort the distance metric."},
   {"t":"To create the labels it needs",
    "why":"k-means is unsupervised — it needs no labels. Scaling is about fair distances, not labels."},
   {"t":"Scaling chooses k for you",
    "why":"Scaling doesn't pick k; the elbow/silhouette methods do. Scaling makes distances fair."}]},
 {"q":"Inertia keeps dropping as you increase k. Why isn't 'pick the k with lowest inertia' the right "
      "rule?",
  "options":[
   {"t":"Inertia always falls as k rises (k = n points gives 0), so you look for the elbow where the "
        "improvement flattens, not the minimum","correct":True,
    "why":"Correct. More clusters can only reduce within-cluster spread, so the minimum is trivially "
          "k = number of points. The elbow (diminishing returns) or silhouette gives a meaningful k."},
   {"t":"Inertia rises with k, so the lowest is best",
    "why":"Inertia falls with k, not rises. That's exactly why 'lowest inertia' is a trap."},
   {"t":"Inertia is random and meaningless",
    "why":"Inertia is a real, monotonic measure of within-cluster spread; it's just monotonic in k, "
          "so you use the elbow rather than the raw minimum."},
   {"t":"Because k must always be 2",
    "why":"k depends on the data; it isn't fixed at 2. The point is how to choose it sensibly."}]},
]))

p.append(B.practice([
 {"q":"A marketing team clusters customers and asks \"which k is correct?\" How would you answer, "
      "practically?",
  "sol":"There's rarely a single mathematically \"correct\" k. I'd run k-means for a range of k, plot "
        "the **elbow** (inertia vs k) and **silhouette** scores to narrow the sensible range, then "
        "&mdash; crucially &mdash; pick the k whose clusters are **actionable and interpretable** to "
        "the team (e.g., segments they can each target differently). Clustering is exploratory: the "
        "best k is the one that produces useful groups, validated by the elbow/silhouette rather than "
        "chosen by them alone."},
 {"q":"You run k-means twice with the same k and get two different clusterings. Is something broken? "
      "How do you make it reliable?",
  "sol":"Nothing's broken &mdash; k-means only finds a **local** optimum, and the result depends on "
        "the random initial centroids, so different starts can converge differently. Make it reliable "
        "by running it multiple times and keeping the best (lowest-inertia) solution: scikit-learn "
        "does this via `n_init` (and smart `k-means++` initialisation). Setting `random_state` also "
        "makes a run reproducible."},
]))

p.append(B.deepdive(
 B.concept(
  "**What k-means optimises, and its blind spots.** Each round provably lowers the ~inertia~ &mdash; "
  "the total squared distance from points to their centroids &mdash; until it can't, so k-means "
  "always converges, but only to a **local** minimum (hence `n_init`). Its assumptions are strong: "
  "it likes clusters that are roughly **spherical, similar in size, and similar in density**. Give "
  "it long stringy shapes, nested rings, or very different-sized blobs and it fails &mdash; because "
  "\"nearest centroid\" carves space into straight-edged cells.") +
 B.concept(
  "**When k-means isn't the tool.** ~DBSCAN~ finds clusters of *arbitrary shape* by density and, "
  "bonus, labels sparse points as ~outliers~ &mdash; and it figures out the number of clusters "
  "itself (you set a neighbourhood size instead of k). ~Hierarchical clustering~ builds a tree of "
  "nested groups you can cut at any level, great when you want a hierarchy or don't want to commit "
  "to one k. Knowing *which* clusterer fits the shape of your data is the real skill.") +
 B.concept(
  "**Clustering is unsupervised, so validation is different.** With no labels there's no accuracy to "
  "check. You judge clusters by **internal** measures (silhouette, inertia), by **stability** (do "
  "the groups persist across resamples?), and above all by **usefulness** &mdash; do the segments "
  "lead to different, sensible actions? A statistically neat clustering that nobody can act on has "
  "failed; a rougher one that reveals \"these are our price-sensitive customers\" has succeeded."),
 title="Deep dive: what k-means optimises, DBSCAN & hierarchical, and validating clusters"))

p.append(B.callout("note","Interview-ready",
 "Explain k-means as assign-to-nearest-centroid then move-centroid-to-mean, repeated to convergence. "
 "Know that it needs `k` up front (elbow/silhouette to choose), is scale-sensitive (standardise), "
 "finds only a local optimum (so `n_init`), and assumes round similar-sized clusters &mdash; name "
 "**DBSCAN** for arbitrary shapes and outliers as the standard follow-up.", "&#9670;"))

LESSONS={"ml-06-clustering":"\n".join(p)}
print("content_m06 OK — chars:", len(LESSONS["ml-06-clustering"]))
