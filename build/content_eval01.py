# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]
p.append(B.why(
 "\"The model is 97% accurate\" is one of the most **dangerous** sentences in data science &mdash; "
 "because on the problems that matter most (fraud, disease, churn), a model that does **nothing** can "
 "score 97% by ignoring the rare thing you actually care about. Choosing the right **metric** is how "
 "you make sure the number you're optimising reflects the decision you're making. Get this wrong and "
 "everything downstream &mdash; tuning, model choice, the go/no-go call &mdash; optimises the wrong "
 "thing."))
p.append(B.h2("The accuracy trap", kicker="Why 97% can be worthless"))
p.append(B.concept(
 "If 3% of emails are spam, a model that labels **everything \"not spam\"** is 97% accurate &mdash; "
 "and catches **zero** spam. Accuracy rewards the majority class, so on **imbalanced** problems it "
 "hides total failure on the minority &mdash; which is usually the class you built the model for. To "
 "see past it, break predictions into the four outcomes of the **confusion matrix**:"))
p.append(B.figure(IMG+"s_eval_confusion.png",
 "**The confusion matrix.** Every prediction is a true/false positive/negative. This 97%-accurate "
 "spam filter looks great &mdash; but it **misses 20% of spam** (20 false negatives), which the "
 "accuracy number completely conceals. Precision and recall expose it.",
 "A 2x2 confusion matrix with TP=80, FP=10, FN=20, TN=890, and precision/recall/accuracy."))
p.append(B.h2("Precision vs. recall — the fundamental tradeoff", kicker="Which error hurts more?"))
p.append(B.concept(
 "The two numbers that matter more than accuracy:\n\n"
 "- **Precision** = of everything you flagged positive, what fraction really was? `TP/(TP+FP)`. "
 "Cost of a **false positive**.\n"
 "- **Recall** (sensitivity) = of all the real positives, what fraction did you catch? `TP/(TP+FN)`. "
 "Cost of a **false negative**.\n\n"
 "They **trade off**: flag more aggressively and recall rises but precision falls, and vice versa. "
 "*Which matters more is a business question, not a math one:* for **cancer screening** you want "
 "**recall** (missing a real case is catastrophic; a false alarm just means more tests). For "
 "**spam** or a **\"you're fired\" auto-email**, you want **precision** (a false positive is very "
 "costly). Always ask: *which mistake is worse here?*"))
p.append(B.concept(
 "When you need one number that balances both, use the **F1 score** &mdash; the *harmonic* mean of "
 "precision and recall: `F1 = 2 &middot; P &middot; R / (P + R)`. The harmonic mean punishes "
 "imbalance, so F1 is only high when **both** are high (a model with 99% precision and 2% recall has "
 "a terrible F1, unlike a plain average)."))
p.append(B.h2("ROC-AUC — grading every threshold at once", kicker="Threshold-independent"))
p.append(B.concept(
 "Precision and recall depend on **where you set the threshold**. The **ROC curve** sweeps every "
 "threshold and plots true-positive rate against false-positive rate; the **AUC** (area under it) "
 "summarises the model's ranking ability in one number &mdash; the probability it ranks a random "
 "positive above a random negative. 0.5 = coin flip, 1.0 = perfect:"))
p.append(B.figure(IMG+"s_eval_roc.png",
 "**ROC curve.** Each point is one threshold's (FPR, TPR). A model that ranks well bows toward the "
 "top-left; the diagonal is random guessing. **AUC** is the area beneath &mdash; a single, "
 "threshold-free score of how well the model *separates* the classes.",
 "An ROC curve bowing above the diagonal, AUC around 0.85, with one threshold marked as a point."))
p.append(B.warn(
 "**On heavy class imbalance, ROC-AUC can look flatteringly high** while the model is useless in "
 "practice, because a huge number of true negatives keeps the false-positive rate low. When "
 "positives are rare (fraud, rare disease), prefer the **precision&ndash;recall curve / PR-AUC**, "
 "which focuses on the positive class you care about and won't be lulled by an ocean of easy "
 "negatives."))
p.append(B.h2("Regression metrics, briefly", kicker="MAE, RMSE, R²"))
p.append(B.concept(
 "For predicting numbers:\n\n"
 "- **MAE** (mean absolute error) &mdash; average size of the miss, in the target's units; robust to "
 "outliers.\n"
 "- **RMSE** (root mean squared error) &mdash; like MAE but **squares** errors first, so it "
 "**punishes big misses** much harder. Use it when large errors are especially bad.\n"
 "- **R&sup2;** &mdash; share of variance explained (1 = perfect, 0 = no better than predicting the "
 "mean); good for *\"how much signal did I capture?\"* but unitless.\n\n"
 "MAE vs RMSE is the same question in disguise: *how much do you care about the occasional large "
 "error?* A lot &rarr; RMSE; treat all errors proportionally &rarr; MAE. (Beware **MAPE** &mdash; "
 "percentage error blows up when actuals are near zero.)"))
p.append(B.h2("Your turn — compute F1 from predictions", kicker="Interactive lab"))
p.append(B.pylab(
 "From the `y_true` and `y_pred` arrays, compute the **F1 score** &mdash; count TP/FP/FN, form "
 "precision and recall, then `F1 = 2&middot;P&middot;R/(P+R)` &mdash; round to **2 decimals** and "
 "assign to **`answer`**.",
 "import numpy as np\n"
 "y_true = np.array([1,1,1,1, 0,0,0,0,0,0])\n"
 "y_pred = np.array([1,1,1,0, 0,0,0,0,1,0])\n",
 "tp = int(((y_pred==1) & (y_true==1)).sum())\n"
 "fp = int(((y_pred==1) & (y_true==0)).sum())\n"
 "fn = int(((y_pred==0) & (y_true==1)).sum())\n"
 "prec = tp/(tp+fp); rec = tp/(tp+fn)\n"
 "answer = round(2*prec*rec/(prec+rec), 2)",
 starter="import numpy as np\n# count tp, fp, fn with boolean masks; precision, recall, then F1\nanswer = ",
 hint="`tp = ((y_pred==1)&(y_true==1)).sum()`, similarly fp and fn; `prec=tp/(tp+fp)`, "
      "`rec=tp/(tp+fn)`; `F1 = 2*prec*rec/(prec+rec)`.",
 title="Lab — F1 from a confusion count",
 preview="numpy loaded; y_true and y_pred preloaded (4 real positives). First Run boots Python.",
 explain="Here TP=3, FP=1, FN=1 &rarr; precision 0.75, recall 0.75, F1 **0.75**. Because F1 is the "
         "*harmonic* mean, it collapses toward whichever of precision/recall is weaker &mdash; so you "
         "can't hide a bad recall behind a great precision."))
p.append(B.keypoints([
 "**Accuracy misleads on imbalanced data** &mdash; a do-nothing model can score high while missing "
 "every rare positive.",
 "**Precision** = correctness of positive predictions (false-positive cost); **recall** = coverage "
 "of real positives (false-negative cost). They **trade off**.",
 "*Which error is worse is a business call*: recall for cancer screening, precision for spam / "
 "high-stakes actions. **F1** balances both (harmonic mean).",
 "**ROC-AUC** grades ranking across all thresholds (0.5 random, 1.0 perfect) &mdash; but use "
 "**PR-AUC** when positives are rare.",
 "Regression: **MAE** (robust), **RMSE** (punishes big misses), **R&sup2;** (variance explained) "
 "&mdash; choose by how much large errors hurt.",
]))
p.append(B.quiz([
 {"q":"A fraud model flags 0.1% of transactions and is 99.9% accurate. Why might it still be "
      "useless?",
  "options":[
   {"t":"With fraud so rare, predicting 'not fraud' for everyone is ~99.9% accurate too — accuracy "
        "says nothing about catching fraud","correct":True,
    "why":"Correct. On extreme imbalance, accuracy is dominated by the majority class. You need "
          "recall (are we catching fraud?) and precision (are flags real?), or PR-AUC &mdash; not "
          "accuracy."},
   {"t":"99.9% is a low accuracy",
    "why":"It's high as a number, but meaningless here &mdash; the base rate of 'not fraud' is "
          "already ~99.9%, so the model may add nothing."},
   {"t":"Fraud models can't be evaluated",
    "why":"They can &mdash; with recall, precision, PR-AUC, and cost-based metrics suited to "
          "imbalance."},
   {"t":"It flags too few transactions",
    "why":"The flag rate isn't the core issue; accuracy simply can't reveal whether the flags are "
          "right or whether fraud is being missed."}]},
 {"q":"For a cancer-screening test, which metric do you most want to maximise, and why?",
  "options":[
   {"t":"Recall — missing a real cancer (false negative) is far more costly than a false alarm",
    "correct":True,
    "why":"Correct. A missed case can be fatal; a false positive leads to follow-up tests. So you "
          "prioritise recall (catch as many real cases as possible), accepting lower precision."},
   {"t":"Precision — avoid false alarms at all costs",
    "why":"Here a false alarm is far less costly than a missed cancer, so precision is secondary to "
          "recall."},
   {"t":"Plain accuracy",
    "why":"Accuracy hides the false-negative rate, which is exactly the catastrophic error in "
          "screening. Recall is the priority."},
   {"t":"Specificity only",
    "why":"Specificity (true-negative rate) ignores missed cases. Screening prioritises recall/"
          "sensitivity."}]},
]))
p.append(B.practice([
 {"q":"Explain when you'd report RMSE instead of MAE for a regression model, with an example.",
  "sol":"Report **RMSE** when **large errors are disproportionately bad**, because squaring the "
        "errors before averaging makes RMSE grow fast with big misses &mdash; so it *penalises* and "
        "*surfaces* outlier errors. Example: predicting **delivery time** or **structural load**, "
        "where being off by 60 minutes / a large margin once is much worse than being off by 5 "
        "minutes twelve times &mdash; RMSE captures that, MAE would treat them the same total. Use "
        "**MAE** when every error should count in proportion to its size and you want robustness to a "
        "few weird outliers (e.g. a median-style 'typical miss' in dollars). They can even disagree "
        "on which model is better, so pick the one matching your cost of error *before* comparing "
        "models."},
 {"q":"Your model has 95% precision but 30% recall. Describe in plain terms what that means and one "
      "scenario where it's acceptable.",
  "sol":"**Plain terms:** when the model says 'positive,' it's right 95% of the time (very few false "
        "alarms) &mdash; but it only *finds* 30% of the actual positives, missing 70% of them. It's "
        "**cautious**: it only flags cases it's very sure about. **Acceptable scenario:** a "
        "high-precision-first setting where acting on a positive is expensive or intrusive and "
        "missing some is tolerable &mdash; e.g. auto-suspending accounts for fraud (you must be "
        "*sure* before penalising a customer, and a human process catches the rest), or surfacing "
        "'definitely relevant' results where a few great hits beat many mediocre ones. The tradeoff "
        "is deliberate: you bought precision by sacrificing recall."},
]))
p.append(B.deepdive(
 B.concept(
  "**Why the harmonic mean for F1?** A plain average of precision and recall would rate a model with "
  "100% precision and 0% recall at 50% &mdash; flattering a useless model. The **harmonic** mean, "
  "2PR/(P+R), is dominated by the *smaller* value, so it's only high when **both** are high, and "
  "collapses toward zero if either does. That matches what we want from a single balance score. When "
  "the two errors aren't equally costly, use **F-beta**: F&beta; weights recall &beta; times as much "
  "as precision (F2 favours recall, F0.5 favours precision), letting you bake the business's error "
  "costs into one tunable number.") +
 B.concept(
  "**AUC's exact meaning, and its blind spots.** ROC-AUC equals the probability that the model scores "
  "a random positive higher than a random negative &mdash; a pure measure of **ranking/separation**, "
  "independent of any threshold or of calibration. That's its strength (compare models regardless of "
  "operating point) and its trap: a high AUC says the model *ranks* well, not that its probabilities "
  "are trustworthy (that's calibration, lesson 10.3) or that it's useful at *your* threshold. And "
  "under heavy imbalance the abundant true negatives keep FPR tiny, inflating AUC while precision is "
  "poor &mdash; which is why PR-AUC, focused on the positive class, is the honest choice for rare-"
  "event problems. Always pair a summary metric with the **operating point** you'll actually deploy."),
 title="Deep dive: F-beta and business-weighted errors, and what AUC does (and doesn't) tell you"))
LESSONS={"eval-01-metrics":"\n".join(x for x in p if x)}
print("content_eval01 OK — chars:", len(LESSONS["eval-01-metrics"]))
