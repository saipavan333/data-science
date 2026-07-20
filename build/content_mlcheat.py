# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.concept(
 "The whole Classical ML track on one page: which model, what it does, and the workflow that keeps "
 "you honest. Press **Print** for a desk copy."))
p.append(B.cheatsheet(
 "Classical Machine Learning — one-page reference",
 "The process that matters more than any model: **frame &rarr; split &rarr; baseline &rarr; pipeline "
 "&rarr; cross-validate & tune &rarr; open the test set once &rarr; interpret.**",
 [
  ("The core idea", [
    ("supervised", "learn from labelled examples (predict a target)"),
    ("unsupervised", "find structure with no labels (clustering)"),
    ("regression", "predict a **number**"),
    ("classification", "predict a **category** (often a probability)"),
    ("generalize", "do well on **new** data, not training data"),
  ]),
  ("Regression", [
    ("LinearRegression()", "fit `y = a + b&middot;x`"),
    ("least squares", "minimise sum of squared residuals"),
    ("`.coef_` / `.intercept_`", "slope (effect per unit) / baseline"),
    ("R&sup2;", "share of variance explained (1 = perfect)"),
    ("residual plot", "check the OLS assumptions"),
  ]),
  ("Classification", [
    ("LogisticRegression()", "linear score &rarr; sigmoid &rarr; probability"),
    ("`.predict_proba()`", "the probability; `.predict()` applies 0.5"),
    ("coefficient", "change in log-odds; `e^b` = odds ratio"),
    ("threshold", "prob &rarr; class; move it to trade precision/recall"),
    ("precision / recall", "of predicted+, real+ / of real+, caught"),
  ]),
  ("Trees & ensembles", [
    ("DecisionTreeClassifier", "axis-aligned yes/no splits; **no scaling**"),
    ("overfits", "limit `max_depth` / `min_samples_leaf`"),
    ("RandomForest (bagging)", "avg many independent trees &rarr; &darr; **variance**"),
    ("GradientBoosting", "sequential trees fix errors &rarr; &darr; **bias**"),
    ("learning_rate", "small + many trees + early stopping"),
    ("XGBoost / LightGBM", "the tabular-data winners"),
  ]),
  ("Clustering (unsupervised)", [
    ("KMeans(n_clusters=k)", "assign to nearest centre, move centre, repeat"),
    ("choose k", "elbow (inertia) / silhouette + usefulness"),
    ("scale first", "k-means uses distances"),
    ("n_init", "many random starts, keep the best"),
    ("DBSCAN", "arbitrary shapes + finds outliers"),
  ]),
  ("Validation", [
    ("cross_val_score(m, X, y, cv=5)", "rotate k folds, average"),
    ("StratifiedKFold", "keep class balance (imbalanced data)"),
    ("GroupKFold / TimeSeriesSplit", "groups together / past&rarr;future"),
    ("GridSearchCV", "tune hyperparameters by CV"),
    ("compare by CV mean", "gap < CV spread = not real"),
  ]),
  ("Overfitting — cures", [
    ("more data", "the cleanest fix for variance"),
    ("simpler model / regularize", "constrain flexibility (Ridge/Lasso, depth)"),
    ("cross-validation", "detect it; tune against it"),
    ("early stopping", "stop when validation stops improving"),
  ]),
  ("Traps to name", [
    ("bias vs variance", "underfit (too simple) vs overfit (too flexible)"),
    ("data leakage", "test info in training &rarr; fit prep inside a Pipeline"),
    ("accuracy on imbalance", "beat a **baseline**; use precision/recall/AUC"),
    ("test set", "open **once**, never tune or select on it"),
  ]),
 ]))
LESSONS={"ml-09-cheatsheet":"\n".join(p)}
print("content_mlcheat OK — chars:", len(LESSONS["ml-09-cheatsheet"]))
