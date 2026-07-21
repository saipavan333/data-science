# -*- coding: utf-8 -*-
import builder as B
p=[B.concept("Model evaluation on one page &mdash; the right metric, honest validation, calibrated "
 "probabilities, and interpretation. Press **Print**.")]
p.append(B.cheatsheet("Model Evaluation — one-page reference",
 "The discipline of **not fooling yourself**: pick the metric that matches the decision, validate "
 "honestly, and check the model is right for the right reasons.",
 [
  ("Classification metrics", [
    ("accuracy", "**lies** on imbalanced data"),
    ("precision", "of predicted+, real+ (false-alarm cost)"),
    ("recall", "of real+, caught (miss cost)"),
    ("F1", "harmonic mean &mdash; both must be high"),
    ("ROC-AUC", "ranking, all thresholds (0.5=chance)"),
    ("PR-AUC", "use it when positives are **rare**"),
  ]),
  ("Regression metrics", [
    ("MAE", "average miss; robust to outliers"),
    ("RMSE", "squares errors &rarr; punishes big misses"),
    ("R&sup2;", "share of variance explained"),
  ]),
  ("Validation", [
    ("train / val / test", "learn / tune / one honest check"),
    ("test set is sacred", "touch it **once**"),
    ("k-fold CV", "stable estimate; report mean &plusmn; sd"),
    ("stratified", "keep class balance (imbalance)"),
    ("grouped / time-series", "no entity/future straddles the split"),
  ]),
  ("Calibration & threshold", [
    ("calibrated", "'p=0.9' happens ~90% of the time"),
    ("fix", "Platt / isotonic on held-out data"),
    ("0.5 is arbitrary", "set threshold by **error costs**"),
    ("lower thr", "&uarr; recall; **raise** &uarr; precision"),
  ]),
  ("Interpretation", [
    ("permutation importance", "shuffle a feature, measure drop"),
    ("beware tree importances", "biased to high-cardinality"),
    ("SHAP", "fair per-prediction attributions"),
    ("also a bug detector", "catches leakage / shortcuts"),
  ]),
 ]))
LESSONS={"eval-06-cheat":"\n".join(p)}
print("evalcheat OK")
