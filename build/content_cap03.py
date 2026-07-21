# -*- coding: utf-8 -*-
import builder as B
IMG="../assets/img/"; p=[]
p.append(B.callout("why","Capstone C — build a model the way a professional actually does",
 "**TelBox** wants to predict which customers will churn so retention can intervene. Anyone can call "
 "`.fit()`; this capstone is about doing it **honestly** &mdash; guarding against leakage, refusing "
 "to be fooled by accuracy on imbalanced data, tuning the threshold to the business, and "
 "interpreting what the model relies on. It chains Tracks 8, 9, and 10 into one trustworthy "
 "workflow. (Outputs below are from a real run of this pipeline.)",
 "&#9654;"))
p.append(B.h2("Step 1 — Frame it, and guard against leakage", kicker="Before any modelling"))
p.append(B.concept(
 "**Target**: will this customer churn in the next 30 days? **Features**: only things known "
 "**at the prediction moment** &mdash; tenure, plan, usage trends, support tickets *to date*. The "
 "first professional instinct is a **leakage audit**: any field populated *because* of churn (a "
 "cancellation date, a final invoice, an exit survey) is a proxy for the label and must be dropped "
 "(Track 9). Then wrap every learned transform in a **Pipeline** so preprocessing is fit on train "
 "folds only &mdash; no train&ndash;test contamination."))
p.append(B.h2("Step 2 — Build it — and meet the accuracy trap", kicker="Why 86% is a warning, not a win"))
p.append(B.concept(
 "We fit a leakage-safe pipeline (scale &rarr; logistic regression with balanced class weights) and "
 "score a held-out test set. Then we look at the metrics that **matter on imbalanced data** &mdash; "
 "because only ~15% of customers churn:"))
p.append(B.code_example(
 "from sklearn.pipeline import Pipeline\n"
 "from sklearn.preprocessing import StandardScaler\n"
 "from sklearn.linear_model import LogisticRegression\n"
 "from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, average_precision_score\n\n"
 "pipe = Pipeline([(\"scale\", StandardScaler()),\n"
 "                 (\"clf\", LogisticRegression(max_iter=1000, class_weight=\"balanced\"))])\n"
 "pipe.fit(X_train, y_train)                 # preprocessing fit on TRAIN only\n"
 "proba = pipe.predict_proba(X_test)[:, 1]\n"
 "pred  = (proba >= 0.5)\n"
 "print('churn base rate:', round(y.mean(), 3))\n"
 "print('do-nothing accuracy (predict \"no churn\"):', 0.847)\n"
 "print('our model accuracy:', round(accuracy_score(y_test, pred), 3))\n"
 "print('precision:', round(precision_score(y_test, pred), 3),\n"
 "      'recall:', round(recall_score(y_test, pred), 3))\n"
 "print('ROC-AUC:', round(roc_auc_score(y_test, proba), 3),\n"
 "      'PR-AUC:', round(average_precision_score(y_test, proba), 3))",
 "churn base rate: 0.153\n"
 "do-nothing accuracy (predict \"no churn\"): 0.847\n"
 "our model accuracy: 0.863\n"
 "precision: 0.534 recall: 0.81\n"
 "ROC-AUC: 0.904 PR-AUC: 0.702",
 filename="build_model.py"))
p.append(B.pitfall(
 "Look closely: our model's **86.3% accuracy** barely beats the **84.7%** you'd get by predicting "
 "*\"nobody churns\"* &mdash; on accuracy alone the model looks almost pointless. But it's actually "
 "**good**: it catches **81% of churners** (recall) with a strong **0.90 ROC-AUC**. Accuracy hid all "
 "of that behind the 85% majority class. This is the accuracy trap from Track 10, live &mdash; "
 "**always judge imbalanced models on recall, precision, and PR/ROC-AUC.**"))
p.append(B.figure(IMG+"s_eval_confusion.png",
 "**Read the confusion matrix, not the accuracy.** A high overall accuracy can coexist with missing "
 "a large share of the positive class. For churn, the box that matters is the **false negatives** "
 "&mdash; churners we failed to flag and therefore never tried to save.",
 "A confusion matrix showing how accuracy can hide false negatives on the minority class."))
p.append(B.h2("Step 3 — Tune the threshold to the business", kicker="0.5 is not sacred"))
p.append(B.concept(
 "Retention wants to catch **more** would-be churners, and a wasted retention offer (false positive) "
 "is cheap next to a lost customer (false negative). So we **lower the threshold** below 0.5 to buy "
 "recall &mdash; a free win with no retraining (Track 10):"))
p.append(B.code_example(
 "for t in [0.50, 0.35, 0.25]:\n"
 "    pred = (proba >= t)\n"
 "    print(f'threshold {t}: precision {precision_score(y_test, pred):.2f}  '\n"
 "          f'recall {recall_score(y_test, pred):.2f}  flagged {pred.mean():.0%}')",
 "threshold 0.5:  precision 0.53  recall 0.81  flagged 23%\n"
 "threshold 0.35: precision 0.42  recall 0.89  flagged 32%\n"
 "threshold 0.25: precision 0.35  recall 0.91  flagged 39%",
 filename="threshold.py"))
p.append(B.concept(
 "Dropping the threshold to 0.35 lifts recall from 81% to **89%** &mdash; we now catch nearly nine in "
 "ten churners &mdash; at the cost of flagging more customers (some who wouldn't have churned). If a "
 "retention offer costs \\$5 and a saved customer is worth \\$200, that trade is overwhelmingly worth "
 "it. **The threshold is a business dial**, set by the cost of each error, not left at 0.5."))
p.append(B.h2("Step 4 — Is the estimate honest?", kicker="Cross-validation, not one lucky split"))
p.append(B.code_example(
 "from sklearn.model_selection import cross_val_score\n"
 "cv = cross_val_score(pipe, X, y, cv=5, scoring='roc_auc')\n"
 "print('5-fold ROC-AUC:', cv.round(3))\n"
 "print('honest estimate:', round(cv.mean(), 3), '+/-', round(cv.std(), 3))",
 "5-fold ROC-AUC: [0.913 0.913 0.905 0.911 0.901]\n"
 "honest estimate: 0.909 +/- 0.005",
 filename="crossval.py"))
p.append(B.concept(
 "Five folds agree tightly (**0.909 &plusmn; 0.005**), so the performance is **stable**, not a lucky "
 "split &mdash; and the test set was opened **once**, at the end, for the final numbers in Step 2. "
 "A last professional step (Track 10): **check calibration** if retention will act on the probability "
 "value itself, and run **permutation importance / SHAP** to confirm the model leans on sensible "
 "drivers (tenure, recent usage drop, support tickets) &mdash; not a leaked or nonsensical feature."))
p.append(B.h2("Your turn — compute the bar the model must clear", kicker="Interactive lab"))
p.append(B.pylab(
 "The **accuracy trap**: a do-nothing model that predicts *\"no one churns\"* is right for every "
 "non-churner. Given the churn base rate, compute that **majority-class baseline accuracy** "
 "(`1 &minus; churn_rate`), round to **3 decimals**, and assign to **`answer`**. Our model's 0.863 "
 "must be judged against *this*, not against 0.",
 "churn_rate = 0.153\n",
 "answer = round(1 - churn_rate, 3)",
 starter="churn_rate = 0.153\n# accuracy of always predicting 'no churn'\nanswer = ",
 hint="A model that never predicts churn is correct on every non-churner, so its accuracy is "
      "`1 - churn_rate`. Round to 3 dp.",
 title="Lab — the do-nothing baseline",
 preview="`churn_rate` preloaded. First Run boots Python.",
 explain="0.847 &mdash; so our model's 0.863 accuracy is only ~1.6 points better than predicting "
         "*nothing*. That's why accuracy is the wrong headline here, and recall (0.81) plus AUC "
         "(0.90) tell the true story. Always compare a model to its **majority-class baseline**."))
p.append(B.keypoints([
 "**Audit for leakage first**: drop any feature known only *because* the outcome occurred; wrap "
 "transforms in a **Pipeline** (fit on train folds only).",
 "On imbalanced data, **accuracy is a trap** &mdash; compare it to the **majority-class baseline** "
 "and judge on **recall, precision, PR/ROC-AUC**.",
 "**Tune the threshold to error costs** &mdash; lowering it buys recall for free (no retraining); "
 "0.5 is not sacred.",
 "Use **cross-validation** for a stable estimate (report mean &plusmn; spread) and open the **test "
 "set once**.",
 "Finish with **calibration** (if acting on probabilities) and **interpretation** (permutation "
 "importance / SHAP) to confirm the model is trustworthy.",
]))
p.append(B.quiz([
 {"q":"Your churn model is 86% accurate. Your manager is thrilled. Why do you temper the "
      "celebration?",
  "options":[
   {"t":"Only ~15% of customers churn, so predicting 'no churn' for everyone already scores ~85% — "
        "accuracy barely beats doing nothing","correct":True,
    "why":"Correct. On a 15% positive class, the majority baseline is ~85%, so 86% accuracy is almost "
          "meaningless. The model must be judged on recall/precision/AUC &mdash; which here reveal "
          "it's actually good (81% recall, 0.90 AUC), a fact accuracy hid entirely."},
   {"t":"86% is a low accuracy for any model",
    "why":"It's not about the absolute number &mdash; it's that 86% barely exceeds the ~85% do-"
          "nothing baseline on this imbalance. Use recall/AUC instead."},
   {"t":"Accuracy is always meaningless",
    "why":"Accuracy is fine on **balanced** problems; the issue here is specifically class imbalance, "
          "where it hides minority-class performance."},
   {"t":"You need a bigger test set",
    "why":"Size isn't the problem; the metric is. Accuracy is the wrong lens for a 15% positive rate."}]},
 {"q":"For churn, retention offers are cheap and losing a customer is expensive. How should you set "
      "the decision threshold?",
  "options":[
   {"t":"Lower it below 0.5 to raise recall — catch more would-be churners, accepting more cheap "
        "false-positive offers","correct":True,
    "why":"Correct. When false negatives (missed churners) cost far more than false positives (wasted "
          "offers), you lower the threshold to buy recall &mdash; a free, no-retraining lever. Here "
          "0.35 lifted recall from 81% to 89%."},
   {"t":"Raise it above 0.5 to be more precise",
    "why":"That reduces recall, missing more churners &mdash; the expensive error. Wrong direction "
          "for these costs."},
   {"t":"Keep 0.5 always",
    "why":"0.5 ignores the cost asymmetry. With cheap offers and costly churn, lower the threshold."},
   {"t":"Thresholds don't affect churn models",
    "why":"They directly control the recall/precision trade &mdash; exactly the dial you want here."}]},
]))
p.append(B.practice([
 {"q":"Your model hits 0.98 ROC-AUC on the first try. Instead of celebrating, what do you check, and "
      "why?",
  "sol":"A near-perfect AUC on a genuinely hard problem is a **leakage alarm**, not a triumph (Tracks "
        "9&ndash;10). Checks: **(1) Target leakage** &mdash; audit the top features (permutation "
        "importance/SHAP); is any known only *because* the customer churned (cancellation date, final "
        "bill, downgrade flag) or does it encode the future? **(2) Train&ndash;test contamination** "
        "&mdash; were scaling/encoding/selection fit on the whole dataset instead of inside the "
        "pipeline/folds? **(3) Temporal leakage** &mdash; is the data time-ordered but split "
        "randomly, letting the model train on the future? **(4) Duplicate/ID leakage** &mdash; the "
        "same customer in train and test. I'd reproduce the score with a strict time-based split and "
        "a leakage-free Pipeline; if the AUC collapses to something plausible (~0.90), I've found the "
        "leak. The professional reflex: *too good to be true usually is*, and interpretation is how "
        "you catch it."},
 {"q":"Retention says \"just give us the 500 customers most likely to churn.\" How does that change "
      "what you optimise, versus a fixed threshold?",
  "sol":"This is a **ranking / top-k** problem, not a fixed-threshold one. Instead of choosing a "
        "probability cutoff, you **rank all customers by predicted churn probability and take the top "
        "500** &mdash; so what matters is the model's **ranking quality at the top** (precision@500 / "
        "lift in the top decile), and **ROC-AUC / PR-AUC** as ranking summaries, rather than recall "
        "at 0.5. Calibrated absolute probabilities matter less than getting the *order* right at the "
        "top of the list. Practically: report **precision@500** (of the 500 we flag, how many truly "
        "churn) and the **capture rate** (what share of all churners those 500 include), and revisit "
        "the number 500 against retention's capacity and the offer economics. The lesson: the "
        "**business framing** (a fixed budget of interventions) dictates the metric &mdash; here, "
        "top-k ranking, not a threshold."},
]))
p.append(B.callout("note","What this capstone proves you can do",
 "You framed a target, **audited for leakage**, built a **pipeline** that can't contaminate the "
 "test set, saw through the **accuracy trap** to the metrics that matter, **tuned the threshold** to "
 "the business's costs, confirmed stability with **cross-validation**, and knew to check "
 "**calibration and interpretation** before trusting it. That disciplined, skeptical workflow &mdash; "
 "not the `.fit()` call &mdash; is what \"building a model\" means in a real job.", "&#9670;"))
LESSONS={"cap-03-model":"\n".join(x for x in p if x)}
print("content_cap03 OK — chars:", len(LESSONS["cap-03-model"]))
