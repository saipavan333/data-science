# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "If you enter a machine-learning competition on ~tabular~ data (rows and columns, like a "
 "spreadsheet), the winning solution is almost always ~gradient boosting~ &mdash; XGBoost, LightGBM, "
 "or CatBoost. It is the professional's default for structured data: more accurate than a random "
 "forest on most problems, and the model you'll reach for again and again at work. The idea behind "
 "it is genuinely clever and worth understanding, not just importing."))

p.append(B.h2("Fix your mistakes, one tree at a time", kicker="Concept"))
p.append(B.concept(
 "A random forest builds its trees **in parallel and independently**, then averages them. Boosting "
 "does the opposite: it builds trees **one after another, in sequence**, and each new tree is trained "
 "specifically to correct the ~errors~ the current ensemble still makes. Tree 1 makes a rough "
 "prediction; you measure what it got wrong (the ~residuals~); tree 2 is trained to predict *those "
 "errors*; you add a shrunken slice of it to the running total; repeat hundreds of times. Each tree "
 "is usually **shallow** (a \"weak learner\"), but chained together they compose into a very "
 "accurate model. Watch the fit sharpen as trees accumulate:"))
p.append(B.figure(IMG+"s_ml_boosting.png",
 "**Gradient boosting improves by fixing residuals.** One shallow tree (left) is a crude staircase; "
 "after 10 trees (middle) it tracks the true curve; after 150 (right) it's very close &mdash; and "
 "starting to chase noise, a hint that more trees isn't always better. The green dashed line is the "
 "true pattern.",
 "Three panels showing a gradient-boosting fit to a sine curve with 1, 10, and 150 trees, improving each time."))

p.append(B.h2("Bagging vs boosting: opposite cures", kicker="Concept · the key contrast")
)
p.append(B.concept(
 "This contrast is a favourite interview question, so hold it clearly:\n\n"
 "- A ~random forest~ (bagging) averages many **deep, independent, high-variance** trees to cut "
 "**variance**. The trees don't talk to each other.\n"
 "- ~Gradient boosting~ chains many **shallow, dependent, high-bias** trees, each fixing the last's "
 "mistakes, to cut **bias**. Order matters; you can't parallelise it the same way.\n\n"
 "Boosting's power comes with a sharper edge: because each tree chases the current errors, it "
 "**can overfit** if you let it run too long or learn too fast. The ~learning rate~ (how big a slice "
 "of each new tree you add) is the main safety valve &mdash; smaller means slower, steadier, usually "
 "better, but you need more trees. Learning rate and number of trees are traded off against each "
 "other."))

p.append(B.h2("Fit it, and feel the learning rate", kicker="Worked example"))
p.append(B.concept(
 "Same three-line API. Here we hold the number of trees fixed and vary only the learning rate, and "
 "watch a too-high rate overfit &mdash; a big train score with a sagging test score:"))
_c,_o=_run(r'''
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

X, y = make_classification(n_samples=600, n_features=10, n_informative=6, random_state=1)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=1)

for lr in [0.05, 0.3, 1.0]:
    gb = GradientBoostingClassifier(n_estimators=150, learning_rate=lr, max_depth=3, random_state=0).fit(Xtr, ytr)
    print(f"learning_rate={lr:<4}  ->  train {gb.score(Xtr, ytr):.2f}   test {gb.score(Xte, yte):.2f}")
''')
p.append(B.code_example(_c,_o,filename="gradient_boosting.py"))
p.append(B.concept(
 "The slow learner (0.05) trains modestly but generalises best; crank the rate to 1.0 and the model "
 "nearly memorises the training set while its **test** score slips &mdash; overfitting, live. In "
 "practice you use a **small** learning rate with **many** trees and stop early when the validation "
 "score stops improving."))

p.append(B.h2("Your turn — tune the learner", kicker="Interactive lab"))
p.append(B.pylab(
 "The train/test split is loaded and `GradientBoostingClassifier` is imported. Train a booster with "
 "**200 trees**, **learning_rate 0.05**, and **max_depth 3**, then assign to **`answer`** its "
 "**test** accuracy, rounded to 2 decimals.",
 "from sklearn.datasets import make_classification\n"
 "from sklearn.model_selection import train_test_split\n"
 "from sklearn.ensemble import GradientBoostingClassifier\n"
 "X, y = make_classification(n_samples=600, n_features=10, n_informative=6, random_state=1)\n"
 "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=1)\n",
 "gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.05, max_depth=3, random_state=0).fit(Xtr, ytr)\n"
 "answer = round(float(gb.score(Xte, yte)), 2)",
 starter="# split loaded; GradientBoostingClassifier imported\ngb = \nanswer = ",
 hint="Pass `n_estimators=200, learning_rate=0.05, max_depth=3, random_state=0` to "
      "`GradientBoostingClassifier(...)`, `.fit(Xtr, ytr)`, then `.score(Xte, yte)`.",
 title="Lab — a slow, steady booster",
 preview="train/test split loaded; `GradientBoostingClassifier` imported. First Run loads scikit-learn.",
 explain="A small learning rate with many trees is the reliable recipe &mdash; steady gains, less "
         "overfitting than a fast learner."))

p.append(B.keypoints([
 "~Gradient boosting~ builds trees **sequentially**, each new one trained to correct the ~residuals~ "
 "(errors) the ensemble still makes.",
 "It combines many **shallow** trees (weak learners) to reduce **bias** &mdash; the opposite of a "
 "forest, which averages deep trees to reduce **variance**.",
 "The ~learning rate~ shrinks each tree's contribution; **small rate + many trees** is the reliable "
 "recipe (they trade off).",
 "It can **overfit** if run too long or too fast &mdash; use a small learning rate and stop early on "
 "a validation score.",
 "In practice you'll use ~XGBoost~ / ~LightGBM~ / ~CatBoost~ &mdash; the go-to winners for tabular "
 "data.",
]))

p.append(B.quiz([
 {"q":"What is each new tree in gradient boosting trained to do?",
  "options":[
   {"t":"Correct the errors (residuals) that the trees built so far still make","correct":True,
    "why":"Correct. Boosting is sequential error-correction: each tree focuses on what the current "
          "ensemble got wrong, and a shrunken slice of it is added to the running prediction."},
   {"t":"Predict the target independently, to be averaged with the others",
    "why":"That's bagging / random forests. Boosting's trees are dependent — each one builds on the "
          "previous trees' mistakes, not averaged independently."},
   {"t":"Split the data into training and test sets",
    "why":"That's cross-validation, unrelated. Each boosting tree fits the current residuals."},
   {"t":"Scale the features",
    "why":"Tree-based models don't need scaling. Each boosting tree targets the remaining errors."}]},
 {"q":"How do bagging (random forest) and boosting mainly differ?",
  "options":[
   {"t":"Bagging averages independent deep trees to cut variance; boosting chains shallow trees "
        "sequentially to cut bias","correct":True,
    "why":"Correct. Opposite strategies on the bias-variance tradeoff: forests reduce variance by "
          "averaging; boosting reduces bias by sequential correction."},
   {"t":"They're the same thing with different names",
    "why":"They're genuinely different: parallel independent averaging vs sequential dependent "
          "error-correction, targeting variance vs bias respectively."},
   {"t":"Boosting uses only one tree",
    "why":"Boosting uses many trees (often hundreds) — just added sequentially, each shallow."},
   {"t":"Bagging can't be parallelized",
    "why":"Bagging IS naturally parallel (independent trees); boosting is the sequential one."}]},
 {"q":"Your booster gets train 0.99, test 0.80 with learning_rate=1.0 and 500 trees. Best first fix?",
  "options":[
   {"t":"Lower the learning rate (and/or reduce trees / depth) — it's overfitting from learning too "
        "fast for too long","correct":True,
    "why":"Correct. A high learning rate with many trees is a classic overfit. A smaller rate (with "
          "early stopping) makes the model learn more gradually and generalize better."},
   {"t":"Raise the learning rate to 2.0",
    "why":"That learns even faster and overfits more — the opposite of what's needed."},
   {"t":"Add 5000 more trees at the same rate",
    "why":"More trees at a high rate deepens the overfit. You'd lower the rate and use early stopping."},
   {"t":"Remove the test set",
    "why":"The test set is what revealed the problem; removing it just hides the overfitting."}]},
]))

p.append(B.practice([
 {"q":"Explain, in one or two sentences each, why a random forest is hard to overfit but gradient "
      "boosting is easy to overfit.",
  "sol":"A **random forest** averages many *independent* trees; averaging can only reduce variance, "
        "so adding trees never makes it worse &mdash; it just stabilises. **Gradient boosting** adds "
        "trees that each chase the current *residuals*, so it keeps driving training error down and "
        "will eventually fit the noise if you don't limit it (small learning rate, early stopping, "
        "shallow trees)."},
 {"q":"A colleague uses `learning_rate=0.5` with `n_estimators=50`. You suspect a smaller rate would "
      "help. What must they change alongside it, and how would you decide the values?",
  "sol":"Learning rate and number of trees **trade off**: if you shrink the rate (say to 0.05), you "
        "must **increase** `n_estimators` (roughly 10&times;, to ~500) so the model still learns "
        "enough. Decide the pair by cross-validation with **early stopping** &mdash; keep a "
        "validation set, add trees until its score stops improving, and take that count. Small rate + "
        "early stopping almost always generalises better than a big rate with few trees."},
]))

p.append(B.deepdive(
 B.concept(
  "**Why \"gradient\" boosting.** Each round, the algorithm computes the ~gradient~ of the loss "
  "function with respect to the current predictions &mdash; for squared error that's literally the "
  "residual `y - &#375;`, which is why \"fit the next tree to the residuals\" is exact for "
  "regression. For classification the loss is log-loss and the \"residuals\" are its gradients, but "
  "the idea is identical: **each tree takes a step down the loss surface.** Boosting is gradient "
  "descent, where each step is a whole tree.") +
 B.concept(
  "**The knobs that matter, and how they interact.** `learning_rate` &times; `n_estimators` set the "
  "total learning (shrink one, grow the other); `max_depth` (often 3&ndash;8) controls how complex "
  "each weak learner is; `subsample` < 1 and `colsample` add randomness (\"stochastic\" boosting) "
  "that fights overfitting. The professional recipe: a **small learning rate**, **early stopping** "
  "on a validation set to pick the tree count, and modest depth &mdash; then tune the rest.") +
 B.concept(
  "**Why the libraries, not scikit-learn's version.** ~XGBoost~, ~LightGBM~, and ~CatBoost~ are "
  "boosting implementations engineered for speed and accuracy: clever handling of missing values, "
  "built-in regularization, histogram-based splits (LightGBM), and native categorical handling "
  "(CatBoost). For real tabular work you'll almost always reach for one of these over "
  "`GradientBoostingClassifier` &mdash; but the concept you learned here is exactly what they do "
  "under the hood."),
 title="Deep dive: why it's called gradient boosting, the key knobs, and XGBoost/LightGBM"))

p.append(B.callout("note","Interview-ready",
 "The money contrast: **bagging** (forests) averages independent trees to cut **variance**; "
 "**boosting** adds trees sequentially, each fixing the last's errors, to cut **bias** &mdash; and "
 "it overfits if run too fast/long, so you use a small learning rate with early stopping. Name "
 "XGBoost/LightGBM as the go-to tabular winners and you sound like you've shipped models.", "&#9670;"))

LESSONS={"ml-05-boosting":"\n".join(p)}
print("content_m05 OK — chars:", len(LESSONS["ml-05-boosting"]))
