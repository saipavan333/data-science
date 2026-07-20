# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Most real machine-learning questions aren't \"how much?\" &mdash; they're \"which one?\": will this "
 "customer **churn or stay**, is this transaction **fraud or legit**, will this email land as "
 "**spam or not**. That's ~classification~, and ~logistic regression~ is its workhorse: simple, fast, "
 "shockingly hard to beat, and &mdash; unlike many models &mdash; it hands you an honest "
 "**probability**, not just a label. Master it and you own the default first model for every "
 "yes/no problem you'll ever face."))

p.append(B.h2("From a line to a probability", kicker="Concept"))
p.append(B.concept(
 "Linear regression outputs any number from &minus;&infin; to +&infin;, but a probability has to sit "
 "between **0 and 1**. Logistic regression fixes that with one trick: it computes a linear score `z "
 "= a + b&middot;x` (exactly like linear regression), then squashes it through the ~sigmoid~ "
 "function, which bends any number into the 0&ndash;1 range:\n\n"
 "> P(y = 1) = 1 / (1 + e^(&minus;z))\n\n"
 "Big positive `z` &rarr; probability near 1; big negative `z` &rarr; near 0; `z = 0` &rarr; exactly "
 "0.5. The result is the smooth S-curve below &mdash; a *probability* of the positive class for "
 "every input:"))
p.append(B.figure(IMG+"s_ml_sigmoid.png",
 "**Logistic regression turns a score into a probability.** As hours studied rise, the sigmoid "
 "climbs from near 0 to near 1. Where it crosses 0.5 is the ~decision boundary~: inputs to the "
 "right are predicted PASS, to the left FAIL. The green and red dots are the actual outcomes.",
 "An S-shaped logistic curve of probability vs hours studied, with a 0.5 threshold and a decision boundary."))

p.append(B.h2("Reading the coefficients: odds and log-odds", kicker="Concept"))
p.append(B.concept(
 "Here's the subtle part interviewers probe. Logistic regression is **linear** &mdash; but linear in "
 "the ~log-odds~, not the probability. The ~odds~ of an event are `P / (1 &minus; P)` (a 0.8 "
 "probability is odds of 4-to-1); the log-odds are just their logarithm. The model says `log-odds = "
 "a + b&middot;x`, so a coefficient `b` is the change in **log-odds** per one-unit increase in `x`. "
 "The friendly version: `e^b` is the ~odds ratio~ &mdash; how the odds get **multiplied** for each "
 "unit of `x`. A coefficient of 0.7 means `e^0.7 &approx; 2`, i.e. each extra unit roughly **doubles "
 "the odds**. That's why you can't read a logistic coefficient as \"+0.7 probability\"; its effect on "
 "probability is an S-curve, biggest in the middle and flat at the ends."))

p.append(B.h2("The decision threshold — where probability becomes a choice", kicker="Concept · the lever"))
p.append(B.concept(
 "A probability isn't a decision. To *act*, you pick a ~threshold~: predict the positive class when "
 "`P &ge; threshold`, else negative. The default is 0.5, but it is a **business choice**, not a law. "
 "Lower it and you catch more true positives (higher ~recall~) at the cost of more false alarms "
 "(lower ~precision~); raise it and the opposite. For cancer screening you'd lower it (missing a "
 "case is terrible); for flagging accounts to ban you'd raise it (a false ban is costly). Drag the "
 "threshold and watch the tradeoff move &mdash; you can never max both at once:"))
p.append(B.widget("threshold", "Slide the decision threshold — watch precision and recall trade off",
 "Green dots are real positives, red are real negatives, placed by the model's predicted "
 "probability. Everything to the **right** of the line is predicted positive (ringed). Slide left "
 "to catch more real positives (recall &uarr;) but pick up false alarms (precision &darr;); slide "
 "right for the reverse. There is no setting that makes both perfect.", height=340))

p.append(B.h2("Fit one in scikit-learn", kicker="Worked example"))
p.append(B.concept(
 "Same three-line shape as linear regression &mdash; but now `.predict_proba` gives you the "
 "probability, and `.predict` applies the 0.5 threshold for you:"))
_c,_o=_run(r'''
import numpy as np
from sklearn.linear_model import LogisticRegression

hours  = np.array([1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5]).reshape(-1, 1)
passed = np.array([0,0,0,0,1,0,1,1,1,1,1,1])            # 1 = passed, 0 = failed

clf = LogisticRegression().fit(hours, passed)

print(f"coefficient (per hour): {clf.coef_[0][0]:.3f}   -> odds x{np.exp(clf.coef_[0][0]):.2f} per hour")
print(f"P(pass | studied 3h): {clf.predict_proba([[3]])[0][1]:.2f}")
print(f"P(pass | studied 5h): {clf.predict_proba([[5]])[0][1]:.2f}")
print(f"predicted class @ 5h: {clf.predict([[5]])[0]}   (1 = pass)")
print(f"accuracy on training data: {clf.score(hours, passed):.2f}")
''')
p.append(B.code_example(_c,_o,filename="logistic_regression.py"))
p.append(B.concept(
 "Read it back: each extra hour multiplies the **odds** of passing by about 3&times;; three hours of "
 "study gives a low pass probability, five hours a high one; and the model gets most of the training "
 "cases right. The probabilities are the real value here &mdash; a label throws away *how sure* the "
 "model is."))

p.append(B.h2("Your turn — predict a probability", kicker="Interactive lab"))
p.append(B.pylab(
 "`hours` and `passed` are loaded and `LogisticRegression` is imported. Fit a model, then assign to "
 "**`answer`** the model's probability of passing after **4 hours** of study, rounded to 2 decimals. "
 "(It's the positive class's probability &mdash; index `[1]`.)",
 "import numpy as np\n"
 "from sklearn.linear_model import LogisticRegression\n"
 "hours  = np.array([1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5]).reshape(-1,1)\n"
 "passed = np.array([0,0,0,0,1,0,1,1,1,1,1,1])\n",
 "clf = LogisticRegression().fit(hours, passed)\n"
 "answer = round(float(clf.predict_proba([[4]])[0][1]), 2)",
 starter="# hours, passed loaded; LogisticRegression imported\nclf = \nanswer = ",
 hint="Fit with `LogisticRegression().fit(hours, passed)`, then "
      "`clf.predict_proba([[4]])[0][1]` is P(pass); wrap in `round(float(...), 2)`.",
 title="Lab — fit a classifier, read the probability",
 preview="`hours` (2-D), `passed` (0/1); `LogisticRegression` imported. First Run loads scikit-learn.",
 explain="`predict_proba` returns [P(fail), P(pass)]; index `[1]` is the pass probability the sigmoid "
         "produces at x = 4."))

p.append(B.keypoints([
 "~Classification~ predicts a category; ~logistic regression~ is the default first model, and it "
 "outputs a **probability**, not just a label.",
 "It computes a linear score `z = a + b&middot;x`, then the ~sigmoid~ `1/(1+e^(&minus;z))` squashes "
 "it into 0&ndash;1.",
 "It's linear in the ~log-odds~: a coefficient `b` means the **odds** get multiplied by `e^b` per "
 "unit of `x` (the ~odds ratio~) &mdash; not a fixed change in probability.",
 "A ~threshold~ turns the probability into a decision. 0.5 is the default, but lowering/raising it "
 "trades ~recall~ against ~precision~ &mdash; a business choice.",
 "In code: `LogisticRegression().fit(X, y)`, then `.predict_proba(...)` for probabilities and "
 "`.predict(...)` for labels.",
]))

p.append(B.quiz([
 {"q":"Why can't you just use linear regression to predict a yes/no outcome?",
  "options":[
   {"t":"Linear regression outputs any number, but a probability must stay between 0 and 1; logistic "
        "regression squashes the score with the sigmoid","correct":True,
    "why":"Correct. A line happily predicts 1.4 or -0.3, which are nonsense as probabilities. The "
          "sigmoid bends the linear score into a valid 0-1 probability."},
   {"t":"Linear regression can't be fit in scikit-learn",
    "why":"It can (LinearRegression). The issue isn't tooling — it's that a straight line produces "
          "values outside 0-1 and models the wrong thing for classification."},
   {"t":"Because classification has no features",
    "why":"Classification uses features just like regression. The difference is the target is a "
          "category, needing a probability output."},
   {"t":"Linear regression always overfits",
    "why":"Overfitting isn't the reason. The core problem is that a line isn't bounded to [0,1] and "
          "doesn't model class probability."}]},
 {"q":"A logistic model has coefficient b = 0.7 for a feature. What does that tell you?",
  "options":[
   {"t":"Each one-unit increase multiplies the odds of the positive class by about e^0.7 ≈ 2","correct":True,
    "why":"Correct. Logistic coefficients act on the log-odds, so exp(b) is the odds ratio — here "
          "each unit roughly doubles the odds. It is NOT a +0.7 change in probability."},
   {"t":"Each unit adds 0.7 to the probability",
    "why":"That's the linear-regression reading. In logistic regression the effect on probability is "
          "an S-curve; the constant multiplier is on the odds (e^0.7), not the probability."},
   {"t":"The probability is always 0.7",
    "why":"A coefficient isn't a probability. It describes how the odds change per unit of the feature."},
   {"t":"70% of predictions are correct",
    "why":"That would be accuracy, a separate quantity. The coefficient is about the feature's effect "
          "on the odds."}]},
 {"q":"A fraud model outputs probabilities. You lower the decision threshold from 0.5 to 0.2. What "
      "happens?",
  "options":[
   {"t":"You flag more transactions as fraud — catching more real fraud (higher recall) but with more "
        "false alarms (lower precision)","correct":True,
    "why":"Correct. A lower threshold labels more cases positive, so you catch more true fraud (recall "
          "up) but also wrongly flag more legit transactions (precision down) — the core tradeoff."},
   {"t":"The model becomes more accurate everywhere",
    "why":"Threshold changes trade precision against recall; they don't uniformly raise accuracy, and "
          "on imbalanced data accuracy can even fall."},
   {"t":"Nothing — the threshold doesn't affect predictions",
    "why":"The threshold is exactly what converts a probability into a yes/no decision, so moving it "
          "changes which cases are flagged."},
   {"t":"It retrains the model with new coefficients",
    "why":"Changing the threshold doesn't retrain anything; it only changes where you cut the same "
          "probabilities into classes."}]},
]))

p.append(B.practice([
 {"q":"A churn model gives a customer P(churn) = 0.62. Your retention team can only call a limited "
      "number of customers, so false alarms are expensive. Would you use a 0.5 threshold, and what "
      "does 0.62 mean in plain terms?",
  "sol":"0.62 means the model estimates a **62% chance** this customer churns. Because calls are "
        "limited and false alarms costly, you'd likely **raise** the threshold above 0.5 (say 0.7) so "
        "you only call the customers the model is most confident about &mdash; trading some recall "
        "(you'll miss a few churners) for higher precision (the calls you do make are better spent). "
        "The right threshold comes from the cost of a wasted call vs. a lost customer, not from a "
        "default."},
 {"q":"Two features in a logistic model have coefficients +1.1 and &minus;0.4. Translate each into an "
      "odds statement, and say which pushes toward the positive class.",
  "sol":"`+1.1`: each unit multiplies the odds by `e^1.1 &approx; 3.0` &mdash; strongly **increases** "
        "the odds of the positive class. `&minus;0.4`: each unit multiplies the odds by `e^(-0.4) "
        "&approx; 0.67` &mdash; **decreases** the odds (to about two-thirds). Positive coefficients "
        "push toward the positive class, negative ones away; the magnitude (via `e^b`) says how "
        "strongly."},
]))

p.append(B.deepdive(
 B.concept(
  "**How it's actually fit: maximum likelihood, not least squares.** Linear regression minimises "
  "squared error; logistic regression can't (the sigmoid makes that non-convex and wrong-headed for "
  "probabilities). Instead it maximises the ~likelihood~ of the observed labels &mdash; equivalently, "
  "it minimises ~log-loss~ (cross-entropy), which punishes confident wrong predictions harshly "
  "(predicting 0.99 for something that was actually 0 costs a lot). There's no neat closed-form "
  "solution, so it's solved by iterative optimisation &mdash; but scikit-learn hides all of that "
  "behind `.fit`.") +
 B.concept(
  "**Accuracy lies on imbalanced data.** If 99% of transactions are legit, a model that predicts "
  "\"legit\" every time is 99% accurate and completely useless &mdash; it never catches fraud. This "
  "is why classification is judged with ~precision~, ~recall~, F1, and ROC-AUC rather than raw "
  "accuracy, and why the threshold matters so much. That whole toolkit is Track 10 (Model "
  "Evaluation); logistic regression is where the need for it first bites.") +
 B.concept(
  "**Beyond two classes, and staying honest.** For more than two categories, the same idea extends "
  "via ~softmax~ (multinomial logistic regression), giving a probability to each class that sums to "
  "1. And like linear regression, logistic regression is ~regularized~ by default in scikit-learn "
  "(the `C` parameter controls the strength) to stop coefficients blowing up when features are many "
  "or correlated &mdash; the bias&ndash;variance tradeoff again. Its enduring appeal is "
  "**interpretability**: every coefficient is an odds ratio you can explain and defend, which is why "
  "regulated industries (credit, insurance) still reach for it first."),
 title="Deep dive: maximum likelihood & log-loss, why accuracy misleads, and multiclass"))

p.append(B.callout("note","Interview-ready",
 "Nail three things: *why not linear regression* (a probability must be bounded 0&ndash;1 &mdash; the "
 "sigmoid does that); *what a coefficient means* (change in log-odds; `e^b` is the odds ratio, not a "
 "probability change); and *the threshold tradeoff* (lower &rarr; more recall, less precision). Bonus "
 "depth: it's fit by maximising likelihood / minimising log-loss, and accuracy is the wrong metric "
 "on imbalanced classes.", "&#9670;"))

LESSONS={"ml-03-logreg":"\n".join(p)}
print("content_m03 OK — chars:", len(LESSONS["ml-03-logreg"]))
