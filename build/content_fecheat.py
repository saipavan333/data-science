# -*- coding: utf-8 -*-
import builder as B
p=[B.concept("Feature engineering on one page &mdash; encode, scale, transform, and above all "
 "**don't leak**. Press **Print**.")]
p.append(B.cheatsheet("Feature Engineering — one-page reference",
 "Where domain knowledge becomes math &mdash; and where discipline prevents disaster. The rule "
 "under everything: **fit transforms on train only.**",
 [
  ("Numeric", [
    ("standardize", "mean 0, std 1 (distance/gradient models)"),
    ("trees don't need scaling", "they split on thresholds"),
    ("log / sqrt", "tame right-skew (money, counts)"),
    ("clip / winsorize", "cap outliers; investigate first"),
  ]),
  ("Categorical", [
    ("ordinal", "has order &rarr; 0,1,2"),
    ("nominal", "no order &rarr; **one-hot**"),
    ("label-encode nominal", "**bug**: invents a fake order"),
    ("high cardinality", "frequency / target / hashing"),
    ("target encoding", "leaks &mdash; do out-of-fold only"),
  ]),
  ("Dates & text", [
    ("datetime parts", "hour, dow, month, is_weekend"),
    ("durations", "days_since_X (often strongest)"),
    ("cyclical", "sin/cos so 23:00 &asymp; 00:00"),
    ("text baseline", "bag-of-words &rarr; **TF-IDF**"),
  ]),
  ("Selection", [
    ("filter", "correlation / mutual information"),
    ("embedded", "**L1/Lasso** zeros; tree importance"),
    ("fewer, better", "noise features hurt + overfit"),
  ]),
  ("LEAKAGE (the deadly one)", [
    ("train-test contamination", "fit on all data before split"),
    ("target leakage", "a feature that's a label proxy / future"),
    ("temporal leakage", "random split on time data"),
    ("fix", "**Pipeline** &mdash; fit inside each fold"),
    ("smell test", "score too good? suspect leakage first"),
  ]),
 ]))
LESSONS={"fe-07-cheat":"\n".join(p)}
print("fecheat OK")
