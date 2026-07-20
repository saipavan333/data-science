# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.concept(
 "Every statistical idea in the track, distilled to one scannable page &mdash; the term, and what it "
 "actually means. Statistics is a small number of ideas used over and over; this is all of them. "
 "Press **Print** for a copy by your desk."))
p.append(B.cheatsheet(
 "Statistics & Probability — one-page reference",
 "Read each row as \"term &mdash; the one-sentence meaning\". If you can explain every row out loud, "
 "you can pass the statistics round.",
 [
  ("Center & spread", [
    ("mean", "average; pulled by outliers"),
    ("median", "middle value; resists outliers"),
    ("variance, std", "typical distance from the mean"),
    ("IQR = Q3 - Q1", "middle 50%; robust spread"),
    ("skew", "which tail is longer"),
  ]),
  ("Probability", [
    ("P(A)", "chance of an event, 0 to 1"),
    ("P(A and B)", "both happen"),
    ("P(A|B)", "A **given** B already happened"),
    ("independent", "P(A|B) = P(A)"),
    ("Bayes", "flip a conditional using the base rate"),
  ]),
  ("Distributions", [
    ("Normal", "bell; **68-95-99.7** within 1-2-3 SD"),
    ("Binomial", "count of successes in n trials"),
    ("Poisson", "count of events in an interval"),
    ("PMF vs PDF", "bars for counts, curve for measures"),
  ]),
  ("Sampling & the CLT", [
    ("population vs sample", "everyone vs the few you measure"),
    ("parameter vs statistic", "true value vs your estimate"),
    ("standard error = &sigma;/&radic;n", "how much the mean wobbles"),
    ("CLT", "sample means &rarr; normal, whatever the population"),
    ("4&times; data &rarr; half the error", "SE shrinks like 1/&radic;n"),
  ]),
  ("Estimation", [
    ("point estimate", "single best guess (e.g. x&#772;)"),
    ("95% CI = est &plusmn; 1.96&middot;SE", "an honest range"),
    ("correct reading", "95% of such intervals cover the truth"),
    ("bootstrap", "resample to get a CI without a formula"),
  ]),
  ("Hypothesis testing", [
    ("H0 / H1", "no effect (skeptic) vs an effect"),
    ("p-value", "P(data this extreme | H0 true)"),
    ("&alpha; (e.g. 0.05)", "false-alarm rate you accept"),
    ("Type I / II", "false positive / missed effect"),
    ("power = 1 - &beta;", "chance of catching a real effect"),
    ("'fail to reject'", "not proof H0 is true"),
  ]),
  ("Choosing a test", [
    ("t-test", "compare 1 or 2 means"),
    ("paired t-test", "before/after on the same units"),
    ("chi-square", "association between categories"),
    ("Mann-Whitney / Wilcoxon", "nonparametric alternatives"),
  ]),
  ("Correlation & traps", [
    ("Pearson r", "**linear** strength, -1 to +1"),
    ("Spearman &rho;", "**monotonic** (rank) strength"),
    ("r near 0", "no *linear* trend (could still curve)"),
    ("always plot first", "Anscombe: same r, different data"),
    ("correlation &ne; causation", "confounders lurk"),
  ]),
 ]))
LESSONS={"stats-13-cheatsheet":"\n".join(p)}
print("content_statscheat OK — chars:", len(LESSONS["stats-13-cheatsheet"]))
