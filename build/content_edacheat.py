# -*- coding: utf-8 -*-
import builder as B
p=[B.concept("Exploratory Data Analysis on one page &mdash; the workflow, the right chart, and the "
 "traps. Press **Print**.")]
p.append(B.cheatsheet("EDA & Visualization — one-page reference",
 "The habit: **look before you model.** Understand shape, spot problems, find relationships &mdash; "
 "then decide.",
 [
  ("The workflow", [
    ("shape first", "rows, cols, dtypes, `.info()`"),
    ("missingness", "how much, and is it random?"),
    ("univariate", "one variable: distribution + outliers"),
    ("bivariate", "pairs: scatter, grouped bars"),
    ("multivariate", "correlation heatmap, pair plot"),
  ]),
  ("Pick the chart", [
    ("distribution", "**histogram** / box plot"),
    ("comparison", "**bar chart** (axis at zero)"),
    ("trend over time", "**line chart**"),
    ("relationship", "**scatter plot**"),
    ("composition", "stacked bar (rarely a pie)"),
  ]),
  ("Distributions", [
    ("right-skew", "long tail; mean > median"),
    ("log transform", "tames skew (money, counts)"),
    ("bimodal", "two peaks &rarr; two groups mixed?"),
    ("mean vs median", "median is **robust** to outliers"),
  ]),
  ("Outliers", [
    ("IQR rule", "beyond 1.5&times;IQR (robust)"),
    ("z-score rule", "|z| > 3 (assumes ~normal)"),
    ("don't auto-delete", "may be the signal (fraud, churn)"),
    ("investigate", "error vs. real extreme"),
  ]),
  ("Time series", [
    ("decompose", "trend + seasonal + residual"),
    ("rolling mean", "smooth to see the trend"),
    ("resample", "`.resample('W').mean()`"),
    ("never shuffle", "split by **time**, not randomly"),
  ]),
  ("Traps", [
    ("truncated y-axis", "exaggerates tiny differences"),
    ("correlation &ne; causation", "confounders lurk"),
    ("Simpson's paradox", "pooled can reverse subgroups"),
  ]),
 ]))
LESSONS={"eda-11-cheat":"\n".join(p)}
print("edacheat OK")
