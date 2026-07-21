# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "There's a saying that has survived every wave of new algorithms: *\"applied machine learning is "
 "basically feature engineering.\"* The uncomfortable truth is that **which model you pick usually "
 "matters less than what you feed it.** A logistic regression on thoughtfully-built features will "
 "routinely beat a fancy model on raw columns. Features are where your **domain knowledge** enters "
 "the model &mdash; and on real tabular problems, that's where most of the winning happens. This "
 "track is the craft of turning raw data into signal a model can use."))
p.append(B.h2("What a feature actually is", kicker="Raw data ≠ features"))
p.append(B.concept(
 "A **feature** is a single measurable input column the model sees. The model never sees your raw "
 "data &mdash; it sees the *numbers you chose to compute from it*. A raw `signup_timestamp` is "
 "useless to a model as-is; but `day_of_week`, `hour`, `days_since_signup`, and `is_weekend` "
 "extracted from it can each carry real signal. **Feature engineering** is that translation step: "
 "raw records &rarr; a numeric table where every column is something the model can learn from."))
p.append(B.concept(
 "It matters because models are, at heart, simple: a linear model can only add up weighted inputs; a "
 "tree can only split on the columns you give it. If the signal is buried in a form the model can't "
 "express &mdash; a ratio it would need to *divide* to find, a seasonal cycle hidden in a raw "
 "timestamp &mdash; **no amount of training recovers it.** You have to surface it as a feature. "
 "That's why the same algorithm can go from useless to state-of-the-art purely on better features."))
p.append(B.why(
 "Concretely: predicting loan default, the raw columns `income` and `debt` are okay &mdash; but the "
 "**engineered** `debt_to_income = debt / income` is often the single strongest predictor, and a "
 "linear model can't invent it by itself (it can't multiply or divide its own inputs). One line of "
 "domain-informed feature code can beat weeks of model tuning."))
p.append(B.h2("The one rule that governs everything here", kicker="Fit on train, apply to test"))
p.append(B.concept(
 "Every transformation you *learn* from data &mdash; a mean to fill missing values, a scaler's "
 "mean/std, a category's target rate &mdash; must be **fit on the training set only**, then "
 "**applied** to validation/test. The moment a transform peeks at the test rows, information leaks "
 "backwards and your scores become fiction. This is ~data leakage~, the deadliest bug in applied ML, "
 "and it's why professionals wrap all of this in a **Pipeline** (lesson 9.5). Hold this rule in mind "
 "through the whole track &mdash; every technique that follows is subject to it."))
p.append(B.keypoints([
 "A **feature** is an input column the model sees; the model learns from your *computed* features, "
 "never the raw data.",
 "On tabular problems, **feature quality usually beats model choice** &mdash; features are how domain "
 "knowledge enters the model.",
 "Models are simple: if the signal isn't expressible in the features (a needed ratio, a hidden "
 "cycle), **training can't recover it** &mdash; you must surface it.",
 "The governing rule: **fit every learned transform on train only, then apply to test** &mdash; or "
 "you leak.",
]))
p.append(B.quiz([
 {"q":"Why can engineering `debt_to_income = debt/income` help a linear model even though both `debt` "
      "and `income` are already columns?",
  "options":[
   {"t":"A linear model can only add weighted inputs — it can't divide two of its own features, so "
        "the ratio must be supplied explicitly","correct":True,
    "why":"Correct. The predictive signal lives in the *ratio*, a nonlinear combination the linear "
          "model can't form on its own. Handing it the ratio as a feature unlocks signal it otherwise "
          "cannot express."},
   {"t":"It doesn't help — the model already has both columns",
    "why":"Having the parts isn't the same as having the ratio: a linear model can't multiply or "
          "divide its inputs, so the ratio is genuinely new information to it."},
   {"t":"It always reduces overfitting",
    "why":"That's not the mechanism; the point is expressing a nonlinear signal (the ratio) the model "
          "couldn't otherwise represent."},
   {"t":"Because it doubles the number of features",
    "why":"More columns isn't the benefit &mdash; often you'd *drop* the raw parts. The value is "
          "surfacing an otherwise-inexpressible signal."}]},
 {"q":"You fill missing ages with the mean age computed over the ENTIRE dataset, then split into "
      "train/test. What's wrong?",
  "options":[
   {"t":"The mean used test rows, so test information leaked into training — inflating your scores",
    "correct":True,
    "why":"Correct. Any statistic learned from data (here, the mean) must come from train only. Using "
          "the full-dataset mean lets the test set influence the features, so measured performance is "
          "optimistic and won't hold in production."},
   {"t":"Nothing — the mean is a reasonable fill value",
    "why":"The fill *strategy* is fine; computing it over test rows is the leak. Fit the imputer on "
          "train, then apply to test."},
   {"t":"Mean imputation is never allowed",
    "why":"Mean imputation is fine &mdash; the bug is *where* the mean was computed (it must exclude "
          "test)."},
   {"t":"You should have used the median",
    "why":"Median vs mean is a separate choice; either way it must be computed on train only to avoid "
          "leakage."}]},
]))
p.append(B.practice([
 {"q":"A teammate says \"let's just throw the raw columns into gradient boosting; feature engineering "
      "is old-fashioned.\" Give a balanced response.",
  "sol":"There's a grain of truth &mdash; tree ensembles like gradient boosting handle raw numeric "
        "columns, monotonic transforms, and interactions far better than linear models, so they need "
        "*less* manual scaling and can find some interactions themselves. But feature engineering "
        "still wins where it counts: **encoding domain knowledge** the model can't infer (ratios, "
        "rates-per-period, business-defined flags), **representing structure** it can't parse (dates, "
        "text, geolocation, IDs), **handling categoricals** sensibly (high-cardinality encoding), and "
        "**preventing leakage** via disciplined pipelines. So it's not old-fashioned; the *emphasis* "
        "shifts &mdash; less hand-scaling, but domain features and correct data handling still "
        "routinely decide who wins. Deep learning on images/text learns features itself; on tabular "
        "business data, engineered features remain king."},
 {"q":"Explain, in one sentence each, why the 'fit on train only' rule applies to (a) scaling and "
      "(b) filling missing values.",
  "sol":"**(a) Scaling:** the scaler's mean and standard deviation are *learned* from data, so "
        "computing them over test rows lets the test distribution influence training &mdash; fit on "
        "train, apply those same numbers to test. **(b) Missing-value fill:** the fill value (mean/"
        "median/mode) is also *learned* from data, so it must be estimated on train only and then "
        "used to fill both train and test &mdash; otherwise the test set leaks into your features."},
]))
p.append(B.deepdive(
 B.concept(
  "**Where feature engineering is decisive vs. where models learn features themselves.** On "
  "**tabular** data &mdash; the bread and butter of most data-science jobs &mdash; engineered "
  "features plus a gradient-boosted tree is still the state of the art, and Kaggle competitions are "
  "won on features far more often than on exotic models. On **unstructured** data (images, audio, "
  "raw text), deep networks *learn* their own hierarchical features, and manual feature engineering "
  "has largely given way to representation learning. Knowing which regime you're in tells you where "
  "to spend your effort: hand-craft features for tabular problems; curate data and architectures for "
  "perceptual ones.") +
 B.concept(
  "**Feature engineering as a conversation with the problem.** The best features come from asking "
  "*\"what would a domain expert look at?\"* A fraud analyst looks at velocity (transactions per "
  "hour), deviation from a user's norm, and mismatches (billing vs. shipping country) &mdash; each "
  "becomes a feature. This is why feature engineering can't be fully automated away: it's where human "
  "understanding of the domain is translated into math. Tools like automated feature generation help, "
  "but they generate *candidates*; judgement about what's meaningful (and what leaks) still comes "
  "from you."),
 title="Deep dive: tabular vs. unstructured, and feature engineering as encoded domain knowledge"))
LESSONS={"fe-01-what":"\n".join(p)}
print("content_fe01 OK — chars:", len(LESSONS["fe-01-what"]))
