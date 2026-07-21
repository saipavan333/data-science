# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
p=[]
p.append(B.why(
 "A model that's accurate but **unexplainable** is a liability: you can't debug it, defend it to a "
 "regulator, convince a stakeholder to act on it, or notice when it's right for the *wrong reasons* "
 "(the classic model that 'detects pneumonia' but really detects which hospital took the X-ray). "
 "**Interpretation** answers *\"why did the model predict that?\"* &mdash; and it's often the "
 "difference between a model that ships and one that dies in a review meeting. It's also where you "
 "catch leakage and bias that every metric missed."))
p.append(B.h2("Two questions: global and local", kicker="The interpretation split"))
p.append(B.concept(
 "Interpretation answers two different questions:\n\n"
 "- **Global** &mdash; *\"what does the model rely on overall?\"* Which features drive its "
 "predictions across all data.\n"
 "- **Local** &mdash; *\"why THIS prediction?\"* Why did *this* loan get rejected, *this* transaction "
 "get flagged.\n\n"
 "You need both. Global explanations build trust and catch a model leaning on a leaky or nonsensical "
 "feature; local explanations justify individual decisions (increasingly a **legal requirement** "
 "&mdash; people have a right to know why they were denied)."))
p.append(B.h2("Global: which features matter", kicker="Permutation importance & friends"))
p.append(B.concept(
 "The most trustworthy, model-agnostic global method is **permutation importance**: take a trained "
 "model, **shuffle one feature's values**, and measure how much performance drops. If scrambling a "
 "feature barely hurts, the model wasn't relying on it; if accuracy collapses, that feature was "
 "load-bearing. It works on *any* model and reflects what the model **actually uses**:"))
_c,_o=_run(r'''
import numpy as np
rng = np.random.default_rng(0)
n = 2000
x1 = rng.normal(size=n)          # the feature that truly drives y
x2 = rng.normal(size=n)          # an irrelevant feature
y  = 3*x1 + rng.normal(size=n)*0.5
pred = lambda a, b: 3*a          # the "fitted" model uses only x1
mse  = lambda t, p: float(np.mean((t-p)**2))

base = mse(y, pred(x1, x2))
imp_x1 = mse(y, pred(rng.permutation(x1), x2)) - base   # shuffle x1
imp_x2 = mse(y, pred(x1, rng.permutation(x2))) - base   # shuffle x2

print(f"baseline error:            {base:5.2f}")
print(f"importance of x1 (shuffled): {imp_x1:6.2f}   <- huge: model depends on x1")
print(f"importance of x2 (shuffled): {imp_x2:6.2f}   <- ~0: model ignores x2")
''')
p.append(B.code_example(_c,_o,filename="permutation_importance.py"))
p.append(B.pitfall(
 "**Don't trust a tree's built-in `feature_importances_` blindly.** The default (impurity-based) "
 "importance is **biased toward high-cardinality** features (many-valued numerics, IDs) &mdash; they "
 "get more chances to split, so they *look* important even when they're noise. Prefer **permutation "
 "importance** (measured on held-out data) for an honest global ranking, and remember importance "
 "shows **association the model uses**, not causation."))
p.append(B.concept(
 "To see *how* a feature moves predictions (not just how much it matters), use a **partial "
 "dependence plot (PDP)**: vary one feature across its range, hold others as they are, and plot the "
 "average predicted outcome. It reveals shape &mdash; is the effect linear, flat then rising, "
 "U-shaped? &mdash; which raw importance numbers can't show."))
p.append(B.h2("Local: why this one prediction?", kicker="SHAP & LIME"))
p.append(B.concept(
 "For a single prediction, **SHAP** (SHapley Additive exPlanations) is the modern standard. Rooted "
 "in cooperative game theory, it **fairly divides** a prediction among its features: *\"this loan "
 "was scored 0.3 below the baseline &mdash; income pushed it +0.2, but 4 recent missed payments "
 "pushed it &minus;0.5.\"* The attributions **add up** to the prediction, so they're consistent and "
 "auditable. **LIME** is a lighter cousin that fits a simple local model around one point. Either "
 "turns a black box into a per-decision explanation a human can check."))
p.append(B.why(
 "Local explanations are also your **bias and leakage detector**. If SHAP shows a hiring model "
 "leaning on a feature correlated with a protected attribute, or a churn model whose top driver is a "
 "field only populated *after* churn, you've caught a serious problem no accuracy score would ever "
 "reveal. Interpretation isn't just for stakeholders &mdash; it's how you audit your own model."))
p.append(B.h2("Your turn — permutation importance by hand", kicker="Interactive lab"))
p.append(B.pylab(
 "Compute the **permutation importance** of feature `x1`: the increase in error when `x1` is "
 "shuffled. Using the provided `predict`, the baseline error, and the pre-shuffled `x1_shuffled`, "
 "compute `perm_error &minus; base_error`, round to **1 decimal**, and assign to **`answer`**. A "
 "big number means the model leans on `x1`.",
 "import numpy as np\n"
 "rng = np.random.default_rng(0)\n"
 "n = 2000\n"
 "x1 = rng.normal(size=n)\n"
 "y  = 3*x1 + rng.normal(size=n)*0.5\n"
 "x1_shuffled = rng.permutation(x1)     # x1 with its rows scrambled\n"
 "predict = lambda col: 3*col            # the fitted model uses x1\n"
 "mse = lambda t, p: float(np.mean((t-p)**2))\n"
 "base_error = mse(y, predict(x1))\n",
 "perm_error = mse(y, predict(x1_shuffled))\n"
 "answer = round(perm_error - base_error, 1)",
 starter="import numpy as np\n# perm_error = mse(y, predict(x1_shuffled)); importance = perm_error - base_error\nanswer = ",
 hint="Call `mse(y, predict(x1_shuffled))` for the shuffled error, then subtract `base_error`; round "
      "to 1 dp.",
 title="Lab — importance = how much shuffling hurts",
 preview="numpy loaded; y, predict, base_error, and x1_shuffled preloaded. First Run boots Python.",
 explain="Shuffling `x1` sends the error soaring (~18), because the model's predictions depend "
         "entirely on it &mdash; that gap **is** the feature's importance. Shuffle an irrelevant "
         "feature and the error barely moves. That contrast is the whole idea of permutation "
         "importance."))
p.append(B.keypoints([
 "Interpretation answers **global** (\"what does the model rely on?\") and **local** (\"why this "
 "prediction?\") &mdash; you need both.",
 "**Permutation importance** (shuffle a feature, measure the performance drop) is model-agnostic and "
 "reflects what the model **actually uses**.",
 "**Don't trust tree impurity `feature_importances_` blindly** &mdash; it's biased toward "
 "high-cardinality features; prefer permutation importance on held-out data.",
 "**Partial dependence plots** show the *shape* of a feature's effect; **SHAP** gives fair, additive "
 "**per-prediction** attributions (LIME is a lighter local method).",
 "Interpretation is also a **leakage/bias detector** &mdash; it catches models that are right for "
 "the wrong reasons.",
]))
p.append(B.quiz([
 {"q":"Why is permutation importance often more trustworthy than a tree's default "
      "`feature_importances_`?",
  "options":[
   {"t":"Impurity-based importance is biased toward high-cardinality features; permutation importance "
        "measures the actual performance drop on held-out data","correct":True,
    "why":"Correct. Many-valued features get more split opportunities and look important even when "
          "noise. Permutation importance directly measures how much shuffling a feature hurts real "
          "performance, so it's model-agnostic and less biased."},
   {"t":"Permutation importance is always faster to compute",
    "why":"It's usually *slower* (re-scoring per feature). Its advantage is honesty/unbiasedness, not "
          "speed."},
   {"t":"Tree importances can't be computed for regression",
    "why":"They can. The issue is the cardinality bias, not the task type."},
   {"t":"Permutation importance proves causation",
    "why":"Neither method proves causation &mdash; both reflect association the model uses. "
          "Permutation is just a less biased *importance* measure."}]},
 {"q":"A pneumonia-detection model has excellent AUC. Interpretation shows its top signal is a "
      "feature encoding which hospital took the scan. What have you learned?",
  "options":[
   {"t":"The model may be exploiting a shortcut (hospital correlates with disease prevalence) rather "
        "than real pathology — a generalisation and validity risk","correct":True,
    "why":"Correct. It's right for the wrong reason: it learned that certain hospitals (e.g. "
          "specialist referral centres) see sicker patients, not what pneumonia looks like. It will "
          "fail at a new hospital. Interpretation caught what AUC hid."},
   {"t":"Nothing — high AUC means the model is fine",
    "why":"AUC can't reveal *why* a model works. Here the 'why' is a spurious shortcut that won't "
          "transfer &mdash; a serious problem."},
   {"t":"Hospital ID is a great feature to keep",
    "why":"It's a leakage/shortcut feature that undermines validity and generalisation; you'd "
          "investigate and likely remove it."},
   {"t":"The model is deliberately biased",
    "why":"Not deliberate &mdash; it's an unintended shortcut. The lesson is that interpretation "
          "surfaces reliance on invalid signals."}]},
]))
p.append(B.practice([
 {"q":"A stakeholder asks \"why did the model deny this specific customer's loan?\" Which "
      "interpretation tool fits, and what would a good answer look like?",
  "sol":"This is a **local** explanation question &mdash; **SHAP** (or LIME) is the right tool, giving "
        "a per-prediction breakdown of how each feature pushed the score up or down from the baseline. "
        "A good answer is concrete and additive: *\"Relative to the average applicant, this decision "
        "was driven mostly by **debt-to-income of 55%** (pushed the score down a lot) and **two "
        "missed payments in the last 6 months** (down further), partly offset by a **long credit "
        "history** (up a little) &mdash; net, below the approval threshold.\"* It names the top "
        "contributing features with direction and rough magnitude, is faithful to the model, and is "
        "checkable &mdash; which is exactly what an auditor, a regulator, or the customer is owed. "
        "(Global importance alone couldn't answer this; it explains the model overall, not this "
        "person.)"},
 {"q":"Why can interpretation be as valuable for the data scientist as for the stakeholder?",
  "sol":"Because it's a **debugging and auditing** tool, not just a communication one. Global methods "
        "(permutation importance, PDPs) reveal when a model leans on a **leaky** feature (something "
        "known only after the outcome), a **spurious shortcut** (hospital ID standing in for disease), "
        "or a feature correlated with a **protected attribute** (a fairness risk) &mdash; problems "
        "that every accuracy metric happily hides. Local methods (SHAP) let you sanity-check "
        "individual predictions and spot cases where the model is right for the wrong reasons. So "
        "interpretation closes the loop: it tells you not just *how well* the model scores, but "
        "*whether you should trust the way it got there* &mdash; often catching issues before they "
        "become production incidents."},
]))
p.append(B.deepdive(
 B.concept(
  "**Why SHAP, specifically.** A prediction is a 'payout' and the features are 'players' who "
  "cooperated to produce it; SHAP borrows the **Shapley value** from game theory to divide that "
  "payout **fairly** &mdash; it's the unique attribution satisfying properties like *efficiency* "
  "(contributions sum to the prediction minus the baseline), *symmetry* (features with equal effect "
  "get equal credit), and *consistency* (if a model changes so a feature matters more, its "
  "attribution can't go down). Those guarantees are why SHAP became the standard: unlike ad-hoc "
  "importance hacks, its explanations are mathematically coherent and locally exact. The cost is "
  "compute (exact Shapley values are exponential), so libraries use fast approximations like "
  "TreeSHAP for tree models.") +
 B.concept(
  "**The accuracy&ndash;interpretability spectrum is real but shrinking.** A linear model or a small "
  "decision tree is **intrinsically** interpretable &mdash; you can read the coefficients or the "
  "splits &mdash; but may sacrifice accuracy. A boosted-tree ensemble or deep net is more accurate "
  "but opaque, so you reach for **post-hoc** tools (permutation importance, PDP, SHAP) to explain it. "
  "The right choice is contextual: in **high-stakes, regulated** settings (credit, healthcare, "
  "justice) you may *prefer* an intrinsically interpretable model even at some accuracy cost, because "
  "an unexplainable decision is unacceptable; elsewhere, a black box plus SHAP is fine. The mature "
  "stance is to treat interpretability as a **requirement to weigh**, not an afterthought &mdash; and "
  "to always run interpretation, if only to audit your own model before trusting it."),
 title="Deep dive: the game theory behind SHAP, and the accuracy–interpretability tradeoff"))
LESSONS={"eval-04-interpret":"\n".join(p)}
print("content_eval04 OK — chars:", len(LESSONS["eval-04-interpret"]))
