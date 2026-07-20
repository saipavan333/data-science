# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "The machine-learning interview round rarely asks you to code an algorithm from scratch. It tests "
 "something harder to fake: do you understand the **tradeoffs**, can you tell when a model is lying "
 "to you, and could you build one *without* fooling yourself? This lesson is the ML question bank "
 "&mdash; the recurring prompts with answers you can say out loud, plus one runnable reality-check "
 "that demolishes the most seductive trap in the field."))

p.append(B.h2("The one that trips everyone: \"99% accurate — are you happy?\"", kicker="Interview pattern"))
p.append(B.concept(
 "This is the most-asked ML judgement question, and the answer is almost always **\"not yet &mdash; "
 "it depends on the base rates.\"** If 90% of cases are one class, a model that blindly predicts "
 "that class is 90% accurate and completely useless. Always compare against a ~baseline~. Watch it: "
 "here the data is imbalanced (10% positive), so a do-nothing baseline already scores 0.90 &mdash; "
 "the real model has to beat *that*, not zero:"))
_c,_o=_run(r'''
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier

# imbalanced: only ~10% of cases are the positive class
X, y = make_classification(n_samples=600, weights=[0.9, 0.1], n_features=8, n_informative=5, random_state=4)
Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, test_size=0.25, random_state=4)

baseline = DummyClassifier(strategy="most_frequent").fit(Xtr, ytr)
print(f"baseline (always predict the majority class): {baseline.score(Xte, yte):.2f} accuracy")

rf = RandomForestClassifier(n_estimators=200, random_state=0)
print(f"random forest — 5-fold CV on train:          {cross_val_score(rf, Xtr, ytr, cv=5).mean():.2f}")
rf.fit(Xtr, ytr)
print(f"random forest — held-out test:               {rf.score(Xte, yte):.2f}")
''')
p.append(B.code_example(_c,_o,filename="baseline_check.py"))
p.append(B.concept(
 "The lazy baseline already hits 0.90 just by never predicting the rare class &mdash; so \"90% "
 "accurate\" would be *worthless* here, and even the forest's accuracy has to be read against that "
 "floor. On imbalanced data you stop quoting accuracy and switch to ~precision~, ~recall~, F1, or "
 "ROC-AUC (Track 10). **Always beat, and report against, a baseline.**"))

p.append(B.h2("Explain the bias–variance tradeoff", kicker="Interview pattern"))
p.append(B.concept(
 "Say it as a story. ~Bias~ is error from a model too **simple** to capture the real pattern (it "
 "underfits &mdash; a straight line through a curve). ~Variance~ is error from a model so **flexible** "
 "it fits the noise (it overfits &mdash; changes wildly with the data). Total error is the sum, and "
 "they trade off: reduce one and you tend to raise the other. The goal is the sweet spot in between. "
 "Then connect it to models: a single deep tree is high-variance; **bagging** (random forests) cuts "
 "that variance by averaging; **boosting** starts from high-bias shallow trees and cuts bias by "
 "sequential correction; ~regularization~ trades a little bias for less variance. Naming those levers "
 "shows you can *act* on the tradeoff, not just recite it."))

p.append(B.h2("\"How would you build and validate a model?\"", kicker="Interview pattern · the walk-through"))
p.append(B.concept(
 "They want a **process**, said calmly in order:\n\n"
 "1. **Frame it** &mdash; regression or classification? What's the target, and what's the *cost* of "
 "each kind of mistake?\n"
 "2. **Split first** &mdash; hold out a test set immediately (stratified or by time), and don't "
 "touch it.\n"
 "3. **Baseline** &mdash; a dummy/majority or simple model, so you know what \"good\" even means.\n"
 "4. **Build in a Pipeline** &mdash; preprocessing + model together, so scaling/imputing is fit per "
 "fold and can't leak.\n"
 "5. **Cross-validate** to compare models and **tune** hyperparameters &mdash; never on the test "
 "set.\n"
 "6. **Open the test set once** for a final, honest estimate.\n"
 "7. **Interpret & sanity-check** &mdash; which features drive it, does it beat the baseline, any "
 "leakage, does the error pattern make sense?\n\n"
 "That sequence &mdash; frame, split, baseline, pipeline, CV/tune, test-once, interpret &mdash; is "
 "the whole of applied ML, and reciting it in order signals you've actually shipped."))

p.append(B.h2("Your turn — establish the baseline", kicker="Interactive lab"))
p.append(B.pylab(
 "The imbalanced split is loaded, with `DummyClassifier` imported. Fit a baseline that **always "
 "predicts the majority class** on the training data, then assign to **`answer`** its accuracy on "
 "the **test** set, rounded to 2 decimals. (This is the number any real model must beat.)",
 "from sklearn.datasets import make_classification\n"
 "from sklearn.model_selection import train_test_split\n"
 "from sklearn.dummy import DummyClassifier\n"
 "X, y = make_classification(n_samples=600, weights=[0.9,0.1], n_features=8, n_informative=5, random_state=4)\n"
 "Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, test_size=0.25, random_state=4)\n",
 "baseline = DummyClassifier(strategy='most_frequent').fit(Xtr, ytr)\n"
 "answer = round(float(baseline.score(Xte, yte)), 2)",
 starter="# split loaded; DummyClassifier imported\nbaseline = \nanswer = ",
 hint="`DummyClassifier(strategy='most_frequent').fit(Xtr, ytr)`, then `.score(Xte, yte)` and "
      "`round(float(...), 2)`.",
 title="Lab — what does 'good' even mean?",
 preview="imbalanced train/test split loaded; `DummyClassifier` imported. First Run loads scikit-learn.",
 explain="If the majority-class baseline already scores ~0.90, then '90% accurate' is worthless "
         "&mdash; which is exactly why you always establish a baseline first."))

p.append(B.keypoints([
 "**Accuracy alone can lie** &mdash; on imbalanced data a do-nothing ~baseline~ scores high; always "
 "compare against it, and use precision/recall/AUC when classes are skewed.",
 "**Bias&ndash;variance**: too simple = underfit (high bias); too flexible = overfit (high variance); "
 "forests cut variance (bagging), boosting cuts bias, regularization trades between them.",
 "**Trees need no scaling**; distance/gradient models (k-means, logistic, SVMs) do.",
 "The build process: **frame &rarr; split &rarr; baseline &rarr; pipeline &rarr; CV/tune &rarr; test "
 "once &rarr; interpret.**",
 "Guard against ~leakage~ (fit preprocessing inside CV) and **never tune or select on the test "
 "set**.",
]))

p.append(B.quiz([
 {"q":"A fraud model is 97% accurate. Fraud is 3% of transactions. Your reaction?",
  "options":[
   {"t":"Unimpressed — predicting 'not fraud' every time already scores 97%; I'd check precision/"
        "recall against a baseline","correct":True,
    "why":"Correct. With 3% positives, a do-nothing baseline is 97% accurate, so the headline number "
          "is meaningless. On imbalanced data you judge with precision, recall, F1, or AUC versus a "
          "baseline — not raw accuracy."},
   {"t":"Thrilled — 97% is excellent, ship it",
    "why":"97% is exactly what you get by never catching fraud. The metric is hiding total failure on "
          "the class you care about."},
   {"t":"It means 97% of frauds are caught",
    "why":"Accuracy isn't recall. 97% accuracy on 3% fraud is consistent with catching *zero* frauds."},
   {"t":"The model must be overfitting",
    "why":"The issue is the metric on imbalanced data, not necessarily overfitting. Accuracy is simply "
          "the wrong lens here."}]},
 {"q":"Which pairing correctly matches the ensemble to what it reduces?",
  "options":[
   {"t":"Random forest (bagging) reduces variance; gradient boosting reduces bias","correct":True,
    "why":"Correct. Forests average independent high-variance trees (variance down); boosting chains "
          "shallow high-bias trees, each fixing the last's errors (bias down)."},
   {"t":"Random forest reduces bias; boosting reduces variance",
    "why":"Reversed. Bagging targets variance; boosting targets bias."},
   {"t":"Both only reduce bias",
    "why":"They target opposite ends of the tradeoff — variance (bagging) and bias (boosting)."},
   {"t":"Neither affects bias or variance",
    "why":"Both are precisely tools for the bias-variance tradeoff, in opposite directions."}]},
 {"q":"What's the single most important rule about the test set?",
  "options":[
   {"t":"Open it once, at the very end — never use it to tune or select a model","correct":True,
    "why":"Correct. Any tuning or model selection on the test set leaks it and inflates your estimate. "
          "Use cross-validation on the training data for all choices; the test set gives one final "
          "honest number."},
   {"t":"Make it as large as possible, even 50%",
    "why":"Size is a secondary tradeoff. The cardinal rule is not to make decisions on it."},
   {"t":"Use it to pick the best of several models",
    "why":"That's exactly the leak to avoid — selecting on the test set biases the reported score."},
   {"t":"Standardize using its mean and std",
    "why":"That leaks test statistics into preprocessing. Fit scalers on training data only."}]},
]))

p.append(B.practice([
 {"q":"An interviewer asks: \"You have 50,000 rows and want to predict churn. Walk me through your "
      "approach.\" Give a crisp answer.",
  "sol":"\"First I'd **frame** it &mdash; binary classification, and the cost of a false negative "
        "(missed churner) vs false positive (wasted retention offer) drives my metric, likely recall "
        "or a cost-weighted score. I'd **split** out a stratified test set immediately and lock it "
        "away, check for **leakage** (drop features that only exist after churn). I'd set a "
        "**baseline** (majority class), build a **Pipeline** (preprocessing + model) so nothing "
        "leaks, and use **cross-validation** to compare a logistic-regression baseline against a "
        "gradient-boosted model and to **tune** it. Then I'd open the **test set once** for a final "
        "estimate, and **interpret** &mdash; feature importances, does it beat the baseline, does the "
        "error make business sense.\" That order is the answer."},
 {"q":"When would you prefer logistic regression over gradient boosting, even though boosting is "
      "usually more accurate?",
  "sol":"When **interpretability and trust** matter more than the last few points of accuracy: "
        "regulated settings (credit, insurance, healthcare) where you must **explain** each decision, "
        "where every coefficient is an auditable odds ratio; when you have **little data** (boosting "
        "overfits small sets); when you need a **fast, cheap** baseline or low-latency scoring; or "
        "when the relationship really is roughly linear in the log-odds. \"Most accurate\" isn't the "
        "only axis &mdash; explainability, data size, latency, and maintenance all count."},
]))

p.append(B.interview_check([
 "Explain the bias&ndash;variance tradeoff, and name a lever for each side.",
 "Bagging vs boosting &mdash; what does each reduce, and how?",
 "\"The model is 99% accurate\" &mdash; what do you ask before believing it?",
 "How do you prevent overfitting? (limit flexibility, more data, regularization, CV, early stopping)",
 "What is data leakage, and how does a Pipeline prevent it?",
 "Walk me through building and validating a model end to end.",
 "When would you choose an interpretable model over a more accurate one?",
], title="Say these out loud before your ML interview")
)

p.append(B.callout("note","Interview-ready",
 "The through-line of this whole track: models are easy to *run* and easy to *fool yourself with*. "
 "The senior signal is judgement &mdash; comparing to a baseline, reading the bias&ndash;variance "
 "tradeoff, refusing to trust accuracy on imbalanced data, and validating without leakage. Show that "
 "and the coding is a formality.", "&#9670;"))

LESSONS={"ml-08-interview":"\n".join(p)}
print("content_m08 OK — chars:", len(LESSONS["ml-08-interview"]))
