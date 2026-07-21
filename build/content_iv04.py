# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "The ML round tests **judgement**, not whether you can call `.fit()`. Interviewers want to hear you "
 "reason about the bias&ndash;variance tradeoff, defend a metric choice, catch leakage, and design a "
 "model end to end. The through-line of every strong answer: models are easy to *run* and easy to "
 "*fool yourself with* &mdash; show that you know the difference."))
p.append(B.h2("The questions that recur", kicker="Concept + judgement"))
p.append(B.interview_check([
 "Explain the **bias&ndash;variance tradeoff**, with a lever for each side.",
 "How do you **prevent overfitting**? (more data, regularization, CV, simpler model, early stopping)",
 "What does **regularization** (L1/L2) do &mdash; and how do they differ?",
 "**Precision vs recall** &mdash; and when do you optimise each?",
 "What does **ROC-AUC** measure, and when do you prefer **PR-AUC**?",
 "**Bagging vs boosting** &mdash; what does each reduce (variance vs bias)?",
 "How do **random forests** and **gradient boosting** actually work?",
 "What is **data leakage**, and how do you prevent it?",
 "How do you handle **class imbalance**?",
 "\"The model is 99% accurate\" &mdash; what do you ask before believing it?",
 "Walk me through **building and validating** a model end to end.",
], title="The ML deep-dive drill")
)
p.append(B.h2("Worked answer — bias–variance", kicker="The concept behind most others"))
p.append(B.concept(
 "*\"Total error splits into **bias** (error from wrong assumptions &mdash; too simple a model, "
 "**underfitting**), **variance** (error from sensitivity to the training sample &mdash; too complex, "
 "**overfitting**), and irreducible noise. A model too simple has high bias and misses real patterns; "
 "too complex has high variance and memorises noise. The **tradeoff** is that reducing one often "
 "raises the other, and the goal is the sweet spot that minimises error on **unseen** data.\"* Then "
 "name **levers**: *increase* flexibility (more features, deeper trees) to cut bias; *decrease* it "
 "(regularization, pruning, more data, ensembling) to cut variance. Connecting the levers to the "
 "concept is what earns the point."))
p.append(B.h2("Worked answer — how gradient boosting works", kicker="Explain the mechanism"))
p.append(B.concept(
 "*\"Gradient boosting builds trees **sequentially**, each one correcting the **errors** of the "
 "ensemble so far. You start with a weak prediction, compute the residuals (what you got wrong), fit "
 "a small tree to those residuals, add it (scaled by a **learning rate**), and repeat. Because each "
 "tree attacks the current mistakes, boosting mainly reduces **bias**, building a strong model from "
 "many weak ones.\"* Contrast with **bagging / random forests**, which build many *independent* trees "
 "in **parallel** on bootstrapped samples and **average** them to reduce **variance**. The crisp "
 "\"sequential-fixes-bias vs parallel-averages-variance\" distinction is the senior tell."))
p.append(B.keypoints([
 "The ML round tests **judgement**: metric choice, leakage, validation, and the "
 "**bias&ndash;variance** tradeoff &mdash; not `.fit()` syntax.",
 "**Underfitting = high bias** (too simple); **overfitting = high variance** (too complex). Levers: "
 "add flexibility to cut bias; regularize/ensemble/more data to cut variance.",
 "**Bagging (random forests)** averages independent trees &rarr; &darr; variance; **boosting** adds "
 "sequential error-correcting trees &rarr; &darr; bias.",
 "On imbalanced data, **reject accuracy** &mdash; use recall/precision/PR-AUC and compare to the "
 "majority baseline.",
 "For \"how would you build X,\" give the **end-to-end workflow**: frame &rarr; leakage-safe features "
 "&rarr; split &rarr; baseline &rarr; model &rarr; honest metrics &rarr; interpret.",
]))
p.append(B.quiz([
 {"q":"Your model gets 99% train accuracy but 70% on validation. Diagnosis and fix?",
  "options":[
   {"t":"Overfitting (high variance) — reduce complexity, add regularization/data, or use "
        "cross-validation and simpler models","correct":True,
    "why":"Correct. A large train&ndash;validation gap is the signature of overfitting: the model "
          "memorised training noise. Reduce variance via regularization, more data, simpler models, "
          "pruning, or early stopping."},
   {"t":"Underfitting — make the model more complex",
    "why":"Underfitting shows *low* train accuracy too. Here train is high and validation low &mdash; "
          "that's overfitting, so you *reduce* complexity, not add it."},
   {"t":"The validation set is broken",
    "why":"A 29-point gap is the classic overfitting signature, not a broken split. Address variance "
          "first."},
   {"t":"Nothing — 70% is fine",
    "why":"The huge gap means it won't generalise reliably; you should reduce overfitting to close "
          "it."}]},
 {"q":"Which correctly pairs the ensemble method with what it primarily reduces?",
  "options":[
   {"t":"Random forest (bagging) reduces variance; gradient boosting reduces bias","correct":True,
    "why":"Correct. Bagging averages many independent trees to cut variance; boosting adds trees "
          "sequentially to correct errors, cutting bias. This distinction is a common interview "
          "check."},
   {"t":"Boosting reduces variance; bagging reduces bias",
    "why":"Reversed. Bagging (parallel averaging) targets variance; boosting (sequential correction) "
          "targets bias."},
   {"t":"Both reduce only variance",
    "why":"Boosting primarily reduces bias (it can even increase variance if overdone). They target "
          "different components."},
   {"t":"Neither affects bias or variance",
    "why":"Both directly shape the bias&ndash;variance decomposition &mdash; that's the point of "
          "ensembling."}]},
]))
p.append(B.practice([
 {"q":"\"How would you build a model to detect fraudulent transactions?\" Give a structured, "
      "end-to-end answer.",
  "sol":"**Clarify first:** what's the fraud rate (likely &lt;1% &mdash; severe imbalance), the cost "
        "of a missed fraud vs. a false alarm, and latency needs (real-time?). **Frame:** binary "
        "classification, but recall-heavy &mdash; missing fraud is costly. **Data/features "
        "(leakage-safe):** only signals known at transaction time &mdash; amount, velocity "
        "(transactions/hour), deviation from the user's norm, geo/device mismatch, time-of-day; drop "
        "anything populated after a fraud label. **Split by time** (train past, test future) to avoid "
        "temporal leakage. **Handle imbalance:** class weights / resampling, and **evaluate on "
        "PR-AUC, recall, and precision@k** &mdash; never accuracy. **Model:** start with a "
        "regularized logistic baseline, then gradient-boosted trees; wrap preprocessing in a "
        "**Pipeline**. **Threshold:** tune to the cost of each error (likely low threshold for high "
        "recall, with a human-review queue for flagged cases). **Interpret** with SHAP to confirm "
        "sensible drivers and catch leakage, **monitor for drift** (fraud is adversarial and shifts), "
        "and **A/B test** the intervention. The interviewer is listening for: clarifying questions, "
        "leakage/imbalance awareness, the right metrics, and end-to-end thinking &mdash; not a fancy "
        "model."},
]))
LESSONS={"iv-04-ml":"\n".join(p)}
print("content_iv04 OK — chars:", len(LESSONS["iv-04-ml"]))
