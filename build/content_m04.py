# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "If someone asks *why* your model made a prediction, a ~decision tree~ can literally show them the "
 "chain of yes/no questions it asked &mdash; no other model is this readable. Trees need no feature "
 "scaling, handle mixtures of numbers and categories, and capture non-linear patterns for free. On "
 "their own they overfit badly &mdash; but bundle hundreds of them into a ~random forest~ and you "
 "get one of the most reliable, low-effort models in all of tabular machine learning. This lesson is "
 "the leap from a single interpretable model to the ensembles that win real problems."))

p.append(B.h2("How a tree makes a decision", kicker="Concept"))
p.append(B.concept(
 "A decision tree is a flowchart of yes/no questions. At each ~node~ it asks one question about one "
 "feature (\"is petal length &le; 2.5?\"), and you follow the branch that matches until you reach a "
 "~leaf~, which gives the prediction. Training is about **choosing the questions**: at every split "
 "the tree tries all features and thresholds and picks the one that best separates the classes "
 "&mdash; measured by ~Gini impurity~ or ~entropy~, both of which just score \"how mixed are the "
 "groups after this cut?\" Because every question is about a single feature, the boundaries a tree "
 "draws are always **straight and axis-aligned** &mdash; it carves the space into boxes:"))
p.append(B.figure(IMG+"s_ml_tree.png",
 "**A decision tree partitions the feature space into rectangles.** Each white edge is one split "
 "(one yes/no question). Every point that lands in a box gets that box's majority class. More "
 "questions &rarr; smaller boxes &rarr; a more flexible (and more overfit-prone) model.",
 "A 2-D scatter of three classes with axis-aligned rectangular decision regions from a decision tree."))

p.append(B.h2("The catch: trees memorize", kicker="Concept · the weakness")
)
p.append(B.concept(
 "A tree with no limit will keep splitting until **every training point sits in its own tiny box** "
 "&mdash; 100% accurate on the data it saw, and useless on new data. That's ~overfitting~ in its "
 "purest form (Lesson 8.1). You tame it by limiting the tree's flexibility: ~max_depth~ (how many "
 "questions deep), ~min_samples_leaf~ (don't make a box for fewer than N points), or ~pruning~ "
 "(grow, then cut back weak branches). A shallow tree underfits; a deep one overfits; the craft is "
 "finding the middle &mdash; which is exactly what cross-validation (Lesson 8.7) is for."))

p.append(B.h2("Random forests: wisdom of many trees", kicker="Concept · the fix")
)
p.append(B.concept(
 "Here's the beautiful idea. One deep tree is high-variance &mdash; wiggle the data and it changes "
 "completely. But if you train **hundreds** of trees, each on a random bootstrap sample of the rows "
 "**and** allowed to consider only a random subset of features at each split, you get hundreds of "
 "*different, imperfect* trees. Average their votes (~bagging~) and the errors cancel out while the "
 "signal reinforces &mdash; the ~random forest~. The randomness is the point: it **decorrelates** "
 "the trees so their mistakes are independent. The result routinely beats a single tuned tree, needs "
 "almost no tuning, resists overfitting, and even reports which features mattered most "
 "(~feature importances~) &mdash; all for a one-line change in code."))

p.append(B.h2("Fit both in scikit-learn", kicker="Worked example"))
p.append(B.concept(
 "Watch the single deep tree ace the training set and stumble on the test set, while the forest "
 "&mdash; same data, one extra word &mdash; generalises:"))
_c,_o=_run(r'''
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = make_classification(n_samples=400, n_features=6, n_informative=4, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

tree   = DecisionTreeClassifier(random_state=0).fit(Xtr, ytr)
forest = RandomForestClassifier(n_estimators=200, random_state=0).fit(Xtr, ytr)

print(f"one deep tree  ->  train {tree.score(Xtr, ytr):.2f}   test {tree.score(Xte, yte):.2f}")
print(f"random forest  ->  train {forest.score(Xtr, ytr):.2f}   test {forest.score(Xte, yte):.2f}")
''')
p.append(B.code_example(_c,_o,filename="trees_and_forests.py"))
p.append(B.concept(
 "The lone tree memorised the training data (perfect train score) but its **test** score is the "
 "honest one &mdash; and it's noticeably lower. The forest's train score is a touch less perfect, "
 "yet its **test** score is higher: it traded a little training accuracy for real generalisation. "
 "That gap between train and test, and closing it, is the whole game."))

p.append(B.h2("Your turn — train a forest", kicker="Interactive lab"))
p.append(B.pylab(
 "`Xtr, Xte, ytr, yte` (a train/test split) are loaded, and `RandomForestClassifier` is imported. "
 "Train a forest of **100** trees on the training data, then assign to **`answer`** its accuracy on "
 "the **test** set, rounded to 2 decimals.",
 "from sklearn.datasets import make_classification\n"
 "from sklearn.model_selection import train_test_split\n"
 "from sklearn.ensemble import RandomForestClassifier\n"
 "X, y = make_classification(n_samples=400, n_features=6, n_informative=4, random_state=0)\n"
 "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)\n",
 "rf = RandomForestClassifier(n_estimators=100, random_state=0).fit(Xtr, ytr)\n"
 "answer = round(float(rf.score(Xte, yte)), 2)",
 starter="# Xtr, Xte, ytr, yte loaded; RandomForestClassifier imported\nrf = \nanswer = ",
 hint="Fit with `RandomForestClassifier(n_estimators=100, random_state=0).fit(Xtr, ytr)`, then "
      "`rf.score(Xte, yte)` is test accuracy; wrap in `round(float(...), 2)`.",
 title="Lab — fit a random forest, score it honestly",
 preview="`Xtr/Xte/ytr/yte` split loaded; `RandomForestClassifier` imported. First Run loads "
         "scikit-learn (~15s).",
 explain="`.score` on the held-out test set is the number that predicts real-world performance "
         "&mdash; always report that one, not the training score."))

p.append(B.keypoints([
 "A ~decision tree~ is a flowchart of yes/no questions; each split is chosen to best separate the "
 "classes (~Gini~ / ~entropy~), giving **axis-aligned** boxes.",
 "Trees need **no feature scaling** and capture non-linearities &mdash; but an unrestricted tree "
 "**overfits** (memorises). Control it with `max_depth` / `min_samples_leaf` / pruning.",
 "A ~random forest~ trains many decorrelated trees (random rows **and** random features) and "
 "**averages** them &mdash; ~bagging~ &mdash; cutting variance and usually beating a single tree.",
 "Forests need little tuning, resist overfitting, and report ~feature importances~.",
 "Always judge by the **test** score: a tree's perfect training score means nothing on its own.",
]))

p.append(B.quiz([
 {"q":"Why does a single unrestricted decision tree tend to overfit?",
  "options":[
   {"t":"It keeps splitting until each training point is in its own leaf — perfect on training data, "
        "poor on new data","correct":True,
    "why":"Correct. With no depth or leaf-size limit, the tree memorizes the training set exactly, "
          "capturing noise as if it were signal, so it generalizes badly."},
   {"t":"Because trees require feature scaling and it wasn't scaled",
    "why":"Trees are scale-invariant — no scaling needed. Overfitting comes from unlimited splitting, "
          "not scaling."},
   {"t":"Because it can only draw curved boundaries",
    "why":"Trees draw straight, axis-aligned boundaries. Overfitting is about too many splits, not the "
          "boundary shape."},
   {"t":"Trees can't handle more than two classes",
    "why":"Trees handle many classes fine. The overfitting issue is unrestricted depth."}]},
 {"q":"What makes a random forest better than the single trees inside it?",
  "options":[
   {"t":"Its trees are decorrelated (random rows and random features), so averaging their votes "
        "cancels their independent errors","correct":True,
    "why":"Correct. Bagging plus random feature subsets makes the trees diverse; averaging many "
          "diverse, imperfect trees reduces variance far below any single tree."},
   {"t":"Each tree is individually more accurate than a normal tree",
    "why":"The individual trees are often weaker (they see only part of the data/features). The power "
          "comes from averaging many of them, not from each being stronger."},
   {"t":"It uses one very deep tree instead of many",
    "why":"A forest is many trees averaged; a single deep tree is exactly what it improves on."},
   {"t":"It scales the features automatically",
    "why":"Scaling isn't the mechanism (trees don't need it). Decorrelation + averaging is."}]},
 {"q":"A decision tree scores 1.00 on training data and 0.74 on test data. What should you conclude?",
  "options":[
   {"t":"It's overfitting; 0.74 is the honest estimate, and you should restrict the tree or use a "
        "forest","correct":True,
    "why":"Correct. The large train-minus-test gap is the signature of overfitting. Trust the test "
          "score, and reduce variance via depth limits or an ensemble."},
   {"t":"It's an excellent model — ship it on the 1.00",
    "why":"The 1.00 is memorization. On new data it performs at ~0.74, so shipping on the training "
          "score would disappoint."},
   {"t":"It's underfitting",
    "why":"Underfitting scores poorly on *both* sets. Perfect train + lower test is overfitting."},
   {"t":"The test set must be mislabeled",
    "why":"A train/test gap is expected from an unrestricted tree; no data problem is implied."}]},
]))

p.append(B.practice([
 {"q":"Your teammate says \"trees need their features standardized like other models.\" Are they "
      "right? Explain.",
  "sol":"No. A tree splits on a **threshold of one feature at a time** (\"is x &le; 5?\"), and that "
        "decision is unchanged if you rescale the feature &mdash; the same rows still fall on each "
        "side. So decision trees (and forests) are ~scale-invariant~ and need **no** standardization, "
        "unlike distance- or gradient-based models (k-means, logistic regression, neural nets) where "
        "scaling matters a lot."},
 {"q":"You have a random forest that's slightly overfitting (train 0.99, test 0.83). Name two knobs "
      "you'd try and which direction, and why.",
  "sol":"Reduce each tree's flexibility and/or increase diversity: lower `max_depth` (or raise "
        "`min_samples_leaf`) so individual trees memorise less; and keep/lower `max_features` per "
        "split to decorrelate trees further. Adding **more** trees (`n_estimators`) won't fix "
        "overfitting but stabilises the average. The goal is to shrink the train&ndash;test gap "
        "&mdash; verify each change with cross-validation, not the training score."},
]))

p.append(B.deepdive(
 B.concept(
  "**Gini vs entropy &mdash; and why it rarely matters.** At each split the tree scores candidate "
  "cuts by how ~pure~ the resulting groups are. ~Gini impurity~ is the chance you'd mislabel a random "
  "point by the group's class mix (0 = pure); ~entropy~ is the information-theory version. In "
  "practice they give near-identical trees, so it's not a knob worth agonising over &mdash; depth and "
  "leaf-size limits matter far more.") +
 B.concept(
  "**Bias&ndash;variance, made physical.** A single deep tree is low-bias, **high-variance** (it "
  "changes wildly with the data). Bagging many such trees and averaging leaves the low bias but "
  "slashes the variance &mdash; that's *why* forests work, and it's the bias&ndash;variance tradeoff "
  "from Lesson 8.1 turned into an algorithm. ~Boosting~ (Lesson 8.5) attacks the *other* end: it "
  "combines high-bias **shallow** trees to reduce bias. Two ensembles, opposite strategies.") +
 B.concept(
  "**Feature importances lie a little.** Forests report how much each feature reduced impurity, which "
  "is handy but **biased toward high-cardinality features** (many split points) and misleading when "
  "features are correlated (importance gets split between them). For decisions that matter, prefer "
  "~permutation importance~ (shuffle a feature, measure the accuracy drop) &mdash; more on honest "
  "interpretation in Track 10."),
 title="Deep dive: Gini vs entropy, why forests reduce variance, and importance caveats"))

p.append(B.callout("note","Interview-ready",
 "Be ready to explain: a tree = axis-aligned yes/no splits chosen by impurity; it overfits unless "
 "limited; a **random forest** = many decorrelated trees (random rows + random features) averaged to "
 "cut **variance** (bagging). Contrast with **boosting** (Lesson 8.5), which combines shallow trees "
 "to cut **bias**. Bonus: trees need no scaling, and permutation importance beats built-in "
 "importance.", "&#9670;"))

LESSONS={"ml-04-trees":"\n".join(p)}
print("content_m04 OK — chars:", len(LESSONS["ml-04-trees"]))
