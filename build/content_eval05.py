# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "Evaluation is where interviewers separate the careful from the careless. Anyone can call `.fit()`; "
 "the trusted data scientist knows **why accuracy lies**, **how to validate without fooling "
 "themselves**, and **whether the probabilities mean anything**. These questions come up in almost "
 "every ML interview, and strong answers signal that you can be handed a model that touches real "
 "decisions."))
p.append(B.h2("Say these out loud", kicker="Rapid-fire drill"))
p.append(B.interview_check([
 "Why is **accuracy** a bad metric on imbalanced data &mdash; what do you use instead?",
 "Define **precision** and **recall**, and give a case where each is the priority.",
 "What does **ROC-AUC** measure, and when does **PR-AUC** beat it?",
 "**MAE vs. RMSE** &mdash; when do you prefer each?",
 "Why is the **test set sacred**, and what happens if you tune against it?",
 "Walk me through **k-fold CV** &mdash; and when would you use **stratified / grouped / time-series** "
 "instead?",
 "What is **model calibration**, and how do you check and fix it?",
 "Why is the **0.5 threshold** usually wrong, and how do you choose a better one?",
 "How do you find which **features a model relies on** &mdash; and why not trust tree "
 "`feature_importances_`?",
 "A model has great AUC but you don't trust it &mdash; what checks do you run?",
], title="The model-evaluation drill")
)
p.append(B.practice([
 {"q":"CASE: A teammate reports a churn classifier with 94% accuracy and wants to ship it. As "
      "reviewer, walk through how you'd pressure-test that number before agreeing.",
  "sol":"Attack it on four fronts. **(1) Base rate / metric:** what fraction actually churn? If "
        "~6% churn, 94% accuracy might just be predicting 'no one churns.' Ask for **precision, "
        "recall, and PR-AUC** on the churn class, and the **confusion matrix** &mdash; are we "
        "catching churners at all? **(2) Validation:** how was it split &mdash; a proper held-out "
        "**test set touched once**, or tuned against? Any **grouped/temporal leakage** (same customer "
        "or future data in train)? **(3) Leakage in features:** is any top feature known only "
        "*after* churn (a cancellation flag, final invoice)? I'd check **permutation importance / "
        "SHAP** to see what it leans on. **(4) Decision fit:** what threshold, and does it match the "
        "**cost** of a missed churner vs. a wasted retention offer &mdash; and are the probabilities "
        "**calibrated** if we act on them? Only after recall/PR-AUC look good, leakage is ruled out, "
        "validation is clean, and the operating point matches costs would I agree to ship. 94% "
        "accuracy alone tells me almost nothing."},
 {"q":"CASE: You must choose between Model A (AUC 0.91, poorly calibrated) and Model B (AUC 0.88, "
      "well calibrated) for a system that **prices** risk. Which and why?",
  "sol":"Because the system **acts on the probability value itself** (pricing = expected-cost "
        "arithmetic), **calibration matters as much as ranking**. Model A ranks slightly better but "
        "its probabilities are distorted, so every price built from them is systematically wrong. "
        "Two good paths: **(a)** take **Model A and recalibrate it** (Platt/isotonic on a held-out "
        "set) &mdash; this usually keeps most of its ranking edge *and* fixes the probabilities, "
        "often the best of both; or **(b)** if recalibration doesn't hold up, **prefer Model B**, "
        "whose trustworthy probabilities make correct prices, accepting the small AUC cost. What I "
        "would *not* do is ship Model A's raw probabilities into pricing just because its AUC is "
        "higher. The senior move is recognising that the **use case dictates the metric**: for "
        "pricing, a calibrated 0.88 beats a miscalibrated 0.91."},
]))
p.append(B.callout("note","The through-line of the whole track",
 "Evaluation is the discipline of **not fooling yourself**. Pick the metric that matches the "
 "decision (accuracy rarely does); validate so the estimate is honest (sacred test set, the right CV "
 "for your data's structure); check that probabilities mean what they say (calibration) and that the "
 "threshold matches your costs; and interpret the model to be sure it's right for the *right "
 "reasons*. A model is only as trustworthy as the evaluation behind it &mdash; and that trust is "
 "what you're really being hired to provide.", "&#9670;"))
LESSONS={"eval-05-interview":"\n".join(p)}
print("content_eval05 OK — chars:", len(LESSONS["eval-05-interview"]))
