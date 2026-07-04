# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Sometimes the rules are too complex to write by hand. Nobody can enumerate every pattern that "
 "makes an email spam or a transaction fraudulent. ~Machine learning~ flips the script: instead "
 "of *you* writing the rules, you show a computer **examples** and let it learn the rules itself. "
 "That's the whole idea &mdash; and this lesson demystifies it, names its two big families, and "
 "introduces the one problem that haunts every model: telling real signal from noise."))

p.append(B.h2("What machine learning actually is", kicker="Concept"))
p.append(B.concept(
 "~Machine learning~ is the practice of building models that **learn patterns from data** in "
 "order to make predictions or find structure &mdash; rather than following rules a human wrote. "
 "A few terms you'll use constantly:\n\n"
 "- A ~feature~ is an input variable the model learns from (a column: square footage, day of "
 "week).\n"
 "- The ~target~ (or ~label~) is what you're trying to predict (the house price, spam/not).\n"
 "- ~Training~ is the process of fitting the model to examples; the result is a ~model~ that maps "
 "features &rarr; a prediction.\n\n"
 "Crucially, ML isn't magic or 'AI thinking' &mdash; under the hood it's **fitting a function to "
 "data**. Everything else is detail about *which* function and *how* you fit it."))

p.append(B.h2("The two big families", kicker="Concept"))
p.append(B.concept(
 "Almost all classical ML splits by one question: *does your data come with the answers?*\n\n"
 "- ~Supervised learning~ uses **labeled** data &mdash; each example has a known target. It "
 "splits again by what the target is: ~regression~ predicts a **number** (price, demand), "
 "~classification~ predicts a **category** (spam/not, churn/stay).\n"
 "- ~Unsupervised learning~ has **no labels** &mdash; you ask the data to reveal its own "
 "structure: ~clustering~ finds natural groups (customer segments), ~dimensionality reduction~ "
 "compresses many features into a few (PCA)."))
p.append(B.figure(IMG+"s_ml_map.png",
 "**The map of classical ML.** Supervised (you have the answers) divides into regression "
 "(numbers) and classification (categories); unsupervised (no answers) into clustering and "
 "dimensionality reduction. This course's Track 4 covers all four.",
 "Tree diagram of machine learning into supervised (regression, classification) and unsupervised "
 "(clustering, dimensionality reduction)."))

p.append(B.h2("The central problem: fit vs. generalize", kicker="Concept · the heart of ML"))
p.append(B.concept(
 "Here is the idea that, once you truly get it, makes all of ML click. The goal is **not** to do "
 "well on the data you trained on &mdash; it's to do well on **new, unseen** data. That's called "
 "~generalization~, and it's constantly threatened from two sides:\n\n"
 "- ~Underfitting~: the model is too simple to capture the real pattern (high ~bias~). It does "
 "poorly everywhere.\n"
 "- ~Overfitting~: the model is so flexible it memorizes the **noise** in the training data (high "
 "~variance~). It looks perfect on training data and fails on new data."))
p.append(B.figure(IMG+"s_ml_overfit.png",
 "**Underfit, good fit, overfit.** Left: a line too simple to follow the curve. Right: a "
 "wiggly curve that passes through every noisy point but has learned the noise, not the signal. "
 "Middle: the model that captures the trend and will generalize.",
 "Three panels showing an underfit line, a good fit, and an overfit wiggly curve on the same data."))
p.append(B.concept(
 "The tension between underfitting and overfitting is the ~bias&ndash;variance tradeoff~, and "
 "managing it &mdash; choosing a model just flexible enough &mdash; is the core craft of machine "
 "learning. Every technique in this track is, in some sense, a tool for finding that sweet spot."))

p.append(B.h2("How we catch overfitting: train / validation / test", kicker="Concept · the golden rule"))
p.append(B.concept(
 "If a model is graded on the data it studied, of course it scores well &mdash; it could just "
 "memorize. So we **hold out data the model never sees during training** and judge it on that. "
 "The standard is a three-way split:"))
p.append(B.figure(IMG+"s_ml_split.png",
 "**The data split.** Train to fit the model, validation to tune and compare options, and test "
 "&mdash; touched **once**, at the very end &mdash; to get an honest estimate of real-world "
 "performance.",
 "A dataset split into train (60%), validation (20%), and test (20%) with their roles."))
p.append(B.warn(
 "The golden rule of ML: **never let the model learn from the test set.** Not for training, not "
 "for tuning, not even for picking features. Every peek leaks information and inflates your "
 "estimate, so the model looks great in your notebook and disappoints in production. Split first, "
 "lock the test set away, and open it once. (We'll formalize this with cross-validation in Lesson "
 "4.7.)", "&#9650;"))

p.append(B.h2("Watch overfitting happen", kicker="Worked example"))
p.append(B.concept(
 "Let's make it concrete with `scikit-learn` (Python's ML library). We fit polynomial models of "
 "increasing flexibility to noisy data and compare their score (R&sup2;, where 1.0 is perfect) on "
 "the **training** set vs. a held-out **test** set. Watch the gap between them explode as the "
 "model overfits."))
_c,_o=_run(r'''
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
rng = np.random.default_rng(0)

# True pattern is a smooth curve; the data has noise on top.
x = rng.uniform(0, 1, 80)
y = np.sin(2*np.pi*x) + rng.normal(0, 0.25, 80)
x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.3, random_state=0)

print(f"{'flexibility':<22}{'train R2':>10}{'test R2':>10}")
for degree, label in [(1, "degree 1  (underfit)"), (4, "degree 4  (good)"),
                      (15, "degree 15 (overfit)")]:
    poly = PolynomialFeatures(degree)
    Xtr = poly.fit_transform(x_tr.reshape(-1, 1))
    Xte = poly.transform(x_te.reshape(-1, 1))
    model = LinearRegression().fit(Xtr, y_tr)
    tr = r2_score(y_tr, model.predict(Xtr))
    te = r2_score(y_te, model.predict(Xte))
    print(f"{label:<22}{tr:>10.2f}{te:>10.2f}")
''')
p.append(B.code_example(_c,_o,filename="overfitting.py"))
p.append(B.concept(
 "Read the columns. The simple model (degree 1) scores poorly on **both** sets &mdash; it "
 "underfits. The flexible model (degree 15) scores high on **train** but its **test** score "
 "collapses &mdash; it memorized noise. The middle model generalizes best. **The test score is "
 "the one that matters**, because it's the only honest preview of new data. That single table is "
 "the whole discipline of model evaluation in miniature."))

p.append(B.keypoints([
 "~Machine learning~ = learning patterns from **examples** to predict or find structure, instead "
 "of hand-written rules. Under the hood it's **fitting a function**.",
 "**Supervised** (labeled): ~regression~ predicts a number, ~classification~ a category. "
 "**Unsupervised** (no labels): clustering, dimensionality reduction.",
 "The goal is ~generalization~ &mdash; doing well on **new** data, not the training data.",
 "~Underfit~ = too simple (high bias); ~overfit~ = memorizes noise (high variance). Managing the "
 "**bias&ndash;variance tradeoff** is the core craft.",
 "**Never train or tune on the test set.** Split into train/validation/test; judge on the test "
 "set **once**.",
]))

p.append(B.quiz([
 {"q":"A model scores 99% on its training data but 62% on held-out data. What's happening, and "
      "which number matters?",
  "options":[
   {"t":"It's overfitting — memorizing training noise; the 62% (held-out) is the honest estimate","correct":True,
    "why":"Correct. A big train-minus-test gap is the signature of overfitting. Performance on "
          "unseen data (62%) is what predicts real-world behavior; the 99% is the model grading "
          "its own homework."},
   {"t":"It's underfitting; the 99% is the real performance",
    "why":"Underfitting scores poorly on *both* sets. Here training is high and held-out is low "
          "&mdash; that's overfitting, and the held-out 62% is the trustworthy figure."},
   {"t":"The model is perfect; ship it on the 99%",
    "why":"The 99% reflects memorization, not generalization. On new data it performs at ~62%, so "
          "shipping on the training score would be a costly mistake."},
   {"t":"The two numbers should always be equal",
    "why":"They're rarely equal; a small gap is normal. A *large* gap signals overfitting, and the "
          "held-out score is the one to trust."}]},
 {"q":"You want to predict whether a customer will churn (yes/no) from their usage data. What kind "
      "of ML problem is this?",
  "options":[
   {"t":"Supervised classification — labeled data, predicting a category","correct":True,
    "why":"Correct. You have labeled examples (who churned) and you're predicting a category "
          "(churn / no churn), which is supervised classification."},
   {"t":"Supervised regression",
    "why":"Regression predicts a *number*. Churn yes/no is a category, so it's classification, not "
          "regression."},
   {"t":"Unsupervised clustering",
    "why":"Clustering has no labels and finds groups. Here you have a known target (churned or "
          "not), making it supervised classification."},
   {"t":"Dimensionality reduction",
    "why":"That compresses features without predicting a target. You're predicting churn, so it's "
          "supervised classification."}]},
 {"q":"Why must the test set be kept completely separate &mdash; never used for training or even "
      "tuning?",
  "options":[
   {"t":"Any use of it leaks information and inflates your performance estimate, so it no longer "
        "reflects truly unseen data","correct":True,
    "why":"Correct. The test set's value is being a stand-in for new data. The moment you train, "
          "tune, or select on it, it's no longer unseen, and your estimate becomes optimistically "
          "biased."},
   {"t":"It's a formality with no real effect",
    "why":"It has a large effect: leaking the test set routinely produces models that look great "
          "in development and fail in production. It's the golden rule for a reason."},
   {"t":"Because the test set is always smaller",
    "why":"Size isn't the point. The point is keeping it *unseen* so it honestly estimates "
          "real-world performance."},
   {"t":"To make training faster",
    "why":"Holding out the test set isn't about speed; it's about an unbiased performance estimate "
          "on data the model has never touched."}]},
]))

p.append(B.practice([
 {"q":"Classify each as regression, classification, clustering, or dimensionality reduction: "
      "(a) predict tomorrow's temperature; (b) group shoppers into segments with no predefined "
      "labels; (c) flag a transaction as fraud or legit; (d) compress 200 sensor readings into 5 "
      "summary numbers.",
  "sol":"(a) **Regression** &mdash; predicting a number (temperature). (b) **Clustering** &mdash; "
        "unsupervised grouping with no labels. (c) **Classification** &mdash; predicting a "
        "category (fraud / legit) from labeled examples. (d) **Dimensionality reduction** &mdash; "
        "compressing many features into a few (e.g., PCA)."},
 {"q":"Your teammate reports 95% accuracy but admits they tuned the model by repeatedly checking "
      "the test set and keeping whatever scored highest. Why is the 95% untrustworthy, and what "
      "should they have done?",
  "sol":"Repeatedly tuning against the test set **leaks** it into the modeling process: by "
        "selecting whatever happened to score best on those specific rows, they've fit to the "
        "test set's noise, so 95% is optimistically biased and won't hold on genuinely new data. "
        "They should tune on a **validation** set (or via cross-validation, Lesson 4.7) and touch "
        "the **test set only once**, at the very end, for a single honest estimate."},
]))

p.append(B.deepdive(
 B.concept(
  "**The bias&ndash;variance decomposition.** A model's expected error on new data splits into "
  "three parts: ~bias~&sup2; (error from the model being too simple to capture the truth), "
  "~variance~ (error from the model being so sensitive it changes wildly with the particular "
  "training sample), and ~irreducible noise~ (randomness no model can remove). Simple models have "
  "high bias, low variance; complex models the reverse. Total error is minimized in between "
  "&mdash; the 'good fit' panel. Almost every ML technique (regularization, ensembling, more "
  "data) is a lever on this tradeoff.") +
 B.concept(
  "**More data is the cleanest cure for variance.** Overfitting happens when a flexible model has "
  "too few examples to pin down the real pattern, so it latches onto noise. Adding data gives it "
  "less room to wiggle and pulls the test score up toward the training score. When you can't get "
  "more data, you constrain the model instead &mdash; simpler models, ~regularization~ (penalizing "
  "complexity, Track 4/6), or ~ensembling~ (averaging many models, Lesson 4.4) &mdash; all ways to "
  "reduce variance without raising bias too much.") +
 B.concept(
  "**ML vs. statistics &mdash; two cultures, one toolbox.** Classical statistics (Track 1) "
  "emphasizes *understanding* and *inference*: which factors matter, with what uncertainty, "
  "under stated assumptions. Machine learning emphasizes *prediction*: the most accurate output, "
  "judged by held-out performance, often with less concern for interpretability. They overlap "
  "heavily (linear regression lives in both worlds), and the best data scientists switch between "
  "the 'explain it' and 'predict it' mindsets depending on the goal &mdash; a theme we'll revisit "
  "in causal inference (Track 8)."),
 title="Deep dive: the bias–variance decomposition, curing variance, and ML vs. statistics"))

p.append(B.callout("note","Interview-ready",
 "Two near-certain questions live here. *\"Explain the bias&ndash;variance tradeoff\"* &mdash; "
 "underfitting (high bias, too simple) vs overfitting (high variance, memorizes noise), with the "
 "goal of generalizing to new data. And *\"why do we split into train/test?\"* &mdash; to estimate "
 "performance on unseen data honestly, never training or tuning on the test set. Crisp answers "
 "here signal you understand what modeling is actually for.", "&#9670;"))

LESSONS={"ml-01-what":"\n".join(p)}
