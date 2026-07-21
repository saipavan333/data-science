# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]
p.append(B.why(
 "Two things every practitioner assumes about a classifier's output &mdash; and both are often wrong. "
 "First, that `predict_proba` gives a **real probability** (it usually doesn't; \"0.9\" may not mean "
 "90%). Second, that the **0.5 threshold** is sacred (it's an arbitrary default that rarely matches "
 "your costs). Fixing these &mdash; **calibration** and **threshold selection** &mdash; is often the "
 "cheapest, highest-leverage improvement you can make to a deployed model, and it requires no "
 "retraining at all."))
p.append(B.h2("Calibration: does 'p = 0.9' happen 90% of the time?", kicker="Trustworthy probabilities"))
p.append(B.concept(
 "A model is **calibrated** if, among all the cases it says are 80% likely, about 80% actually are. "
 "Many strong models (boosted trees, SVMs, naive Bayes) are **not** calibrated &mdash; they rank "
 "cases well but their probabilities are distorted, often **overconfident** (pushed toward 0 and 1). "
 "A **reliability diagram** shows it: bin predictions by probability and plot predicted vs. observed "
 "frequency against the diagonal:"))
p.append(B.figure(IMG+"s_eval_calibration.png",
 "**Reliability diagram.** Perfect calibration is the diagonal. This model is **overconfident**: "
 "when it says 90%, the event happens only ~72% of the time. Its *rankings* may be fine (good AUC), "
 "but its *probabilities* can't be trusted as-is &mdash; a problem whenever you act on the number "
 "itself.",
 "A calibration curve below the diagonal at high probabilities, showing overconfidence."))
p.append(B.concept(
 "Why it matters: whenever the **probability itself drives a decision** &mdash; expected-value "
 "calculations, risk pricing, ranking by likelihood, thresholds tied to cost &mdash; miscalibration "
 "quietly corrupts everything downstream. Fixes (fit on a held-out set, never the training data): "
 "**Platt scaling** (fit a logistic curve to the scores) or **isotonic regression** (a flexible "
 "monotonic map). Neither changes the ranking or requires retraining the base model &mdash; they "
 "just repair the probability scale. Measure it with a **reliability diagram** or the **Brier "
 "score**."))
p.append(B.h2("Thresholds: 0.5 is just a default", kicker="Move it to fit your costs"))
p.append(B.concept(
 "Turning a probability into a decision needs a **threshold**, and 0.5 is an arbitrary starting "
 "point &mdash; not a law. Because precision and recall trade off as you slide it (lesson 10.1), the "
 "*right* threshold depends entirely on the **cost of each error**:\n\n"
 "- **Lower** the threshold (flag at, say, 0.2) &rarr; catch more positives (**higher recall**), "
 "more false alarms &mdash; good for cancer screening, fraud triage.\n"
 "- **Raise** it (flag only above 0.8) &rarr; fewer, surer positives (**higher precision**) &mdash; "
 "good for auto-blocking accounts or any costly action.\n\n"
 "You choose the threshold **after** training, on validation data, by optimising the metric or "
 "**expected cost** that reflects your problem &mdash; not by leaving it at 0.5 out of habit."))
p.append(B.tip(
 "Setting a threshold well is often a **bigger** win than squeezing another point of AUC out of the "
 "model &mdash; and it's free. If false negatives cost 10&times; what false positives do, encode "
 "that: pick the threshold that minimises `10&middot;FN + 1&middot;FP` on validation. You've now "
 "aligned the model with the *business*, not with an arbitrary 0.5."))
p.append(B.h2("Your turn — move the threshold, change the decision", kicker="Interactive lab"))
p.append(B.pylab(
 "You have predicted probabilities `probs`. A **lower** threshold flags more positives. Count how "
 "many cases are flagged positive at a threshold of **0.3** (i.e. `probs >= 0.3`) and assign that "
 "count to **`answer`** (an int). Compare it mentally to how many 0.5 would flag.",
 "import numpy as np\n"
 "probs = np.array([0.05, 0.22, 0.31, 0.44, 0.55, 0.62, 0.78, 0.91, 0.12, 0.36])\n",
 "answer = int((probs >= 0.3).sum())",
 starter="import numpy as np\n# how many probabilities are >= 0.3 ?\nanswer = ",
 hint="`(probs >= 0.3).sum()` counts the True values; wrap in `int(...)`.",
 title="Lab — threshold vs. how much you flag",
 preview="numpy loaded; ten predicted probabilities preloaded. First Run boots Python.",
 explain="At 0.3, **7** cases are flagged; at 0.5 only 4 would be. Lowering the threshold trades "
         "precision for recall &mdash; you catch more positives but accept more false alarms. The "
         "'right' threshold is wherever your cost of a miss vs. a false alarm balances, not a "
         "default 0.5."))
p.append(B.keypoints([
 "**Calibrated** = 'p = 0.8' is right ~80% of the time. Many strong models (boosted trees, SVMs) "
 "are **overconfident** and need fixing.",
 "Check calibration with a **reliability diagram** / **Brier score**; fix with **Platt scaling** or "
 "**isotonic regression** on held-out data (ranking unchanged).",
 "Calibration matters whenever the **probability itself** drives a decision (expected value, "
 "pricing, cost-based thresholds).",
 "The **0.5 threshold is an arbitrary default** &mdash; choose it from your **error costs** on "
 "validation data.",
 "**Lower threshold &rarr; more recall**; **raise &rarr; more precision.** Tuning it is often a "
 "bigger, cheaper win than more model tuning.",
]))
p.append(B.quiz([
 {"q":"A gradient-boosted model has AUC 0.90 but its reliability diagram bows well below the "
      "diagonal at high probabilities. What does that mean and what do you do?",
  "options":[
   {"t":"It ranks well but is overconfident — recalibrate it (Platt/isotonic) on held-out data if "
        "you act on the probabilities","correct":True,
    "why":"Correct. High AUC means good ranking; the bowed reliability curve means the probabilities "
          "are inflated. If decisions use the probability value, apply post-hoc calibration &mdash; "
          "it fixes the scale without changing the ranking or retraining."},
   {"t":"The model is broken and must be retrained from scratch",
    "why":"No need &mdash; ranking is fine (AUC 0.90). Calibration is a cheap post-hoc fix, not a "
          "reason to retrain."},
   {"t":"AUC 0.90 means calibration is automatically fine",
    "why":"AUC measures ranking only; a well-ranking model can still be badly miscalibrated, exactly "
          "as shown."},
   {"t":"Lower the classification threshold to 0.3",
    "why":"That changes the operating point but doesn't fix distorted *probabilities* &mdash; "
          "calibration does."}]},
 {"q":"False negatives cost roughly 10&times; false positives. How should you set the decision "
      "threshold?",
  "options":[
   {"t":"Lower it below 0.5 to catch more positives, choosing the value that minimises expected cost "
        "on validation data","correct":True,
    "why":"Correct. When misses are far costlier than false alarms, you accept more false positives to "
          "raise recall &mdash; pick the threshold minimising 10&middot;FN + 1&middot;FP on held-out "
          "data. 0.5 is not special."},
   {"t":"Keep it at 0.5 — that's the correct default",
    "why":"0.5 ignores the 10:1 cost asymmetry. With costly misses you should lower the threshold."},
   {"t":"Raise it above 0.5 to be more confident",
    "why":"Raising it *reduces* recall, causing more of the expensive false negatives &mdash; the "
          "opposite of what the costs demand."},
   {"t":"Thresholds don't affect cost",
    "why":"They directly control the FP/FN mix, which is exactly what determines expected cost here."}]},
]))
p.append(B.practice([
 {"q":"A colleague uses a model's `predict_proba` output directly to price insurance risk. Why might "
      "you be worried, and what would you check?",
  "sol":"Because pricing acts on the **probability value itself**, not just the ranking &mdash; so if "
        "the model is **miscalibrated** (e.g. an overconfident boosted tree that says 0.9 when the "
        "true rate is 0.72), every price is systematically wrong, over- or under-charging whole "
        "segments. I'd **check calibration**: plot a **reliability diagram** on held-out data and "
        "compute the **Brier score**; if the curve departs from the diagonal, **recalibrate** with "
        "Platt scaling or isotonic regression (fit on a separate calibration set), then re-plot to "
        "confirm. Only once `p` genuinely means *p* should it drive prices. (Good ranking / AUC is "
        "necessary but not sufficient here.)"},
 {"q":"Give a concrete example where moving the threshold away from 0.5 is clearly the right call, "
      "and explain the direction.",
  "sol":"**Fraud triage for human review:** missing a fraudulent transaction (false negative) is far "
        "costlier than sending a legitimate one for a quick review (false positive). So **lower** the "
        "threshold well below 0.5 &mdash; flag anything with, say, &ge;0.15 probability &mdash; to "
        "maximise **recall** and catch more fraud, accepting more false alarms that a human queue "
        "filters out. Conversely, for **auto-suspending** accounts with no human in the loop, "
        "**raise** the threshold (only act above ~0.9) to protect **precision** and avoid wrongly "
        "penalising real customers. Same model, opposite thresholds &mdash; because the *cost of each "
        "error* differs, and that, not 0.5, is what sets the operating point."},
]))
p.append(B.deepdive(
 B.concept(
  "**Platt vs. isotonic &mdash; which calibrator?** **Platt scaling** fits a one-parameter logistic "
  "curve mapping scores to probabilities: simple, data-efficient, ideal when you have **little** "
  "calibration data or the distortion is roughly sigmoidal. **Isotonic regression** fits any "
  "monotonic step function: more flexible, can correct odd-shaped miscalibration, but needs **more** "
  "data and can overfit on small sets. Both are fit on a **held-out calibration set** (or via "
  "cross-validation), never the training data, and both preserve the model's ranking &mdash; so AUC "
  "is unchanged while the Brier score and reliability improve.") +
 B.concept(
  "**Metrics that judge probabilities, not just decisions.** Accuracy/precision/recall grade "
  "*thresholded* outputs; to grade the **probabilities themselves** use **proper scoring rules**: "
  "the **Brier score** (mean squared error between predicted probability and outcome) and **log "
  "loss** (which punishes confident wrong predictions harshly). A model can have great AUC yet a poor "
  "Brier score if it's miscalibrated. The professional habit is to report a **ranking** metric (AUC/"
  "PR-AUC), a **calibration** check (reliability diagram / Brier), *and* the **operating-point** "
  "metrics at your chosen threshold &mdash; three lenses, because each hides what the others reveal. "
  "Optimising one alone is how models look good in a notebook and disappoint in production."),
 title="Deep dive: Platt vs. isotonic calibration, and proper scoring rules (Brier, log loss)"))
LESSONS={"eval-03-calibration":"\n".join(x for x in p if x)}
print("content_eval03 OK — chars:", len(LESSONS["eval-03-calibration"]))
