# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.concept(
 "The entire Experimentation & A/B Testing track on one page &mdash; the design checklist, the "
 "numbers that matter, and the traps. Press **Print** for a desk copy to keep beside you when you "
 "design your next test."))
p.append(B.cheatsheet(
 "A/B Testing & Experimentation — one-page reference",
 "The arc that never changes: **hypothesis &rarr; metric + guardrails &rarr; randomization unit "
 "&rarr; power/size &rarr; trust checks &rarr; run to plan &rarr; decide by a pre-set rule.**",
 [
  ("Why experiment", [
    ("randomization", "the only clean way to get **causation**"),
    ("counterfactual", "what would've happened without the change"),
    ("A/B test", "randomly split users, change one thing, compare"),
    ("can't randomize?", "quasi-experiment (diff-in-diff, matching)"),
  ]),
  ("Design", [
    ("hypothesis", "falsifiable + a **direction** (X raises Y)"),
    ("primary metric", "**one**, captures the goal, sensitive"),
    ("guardrail", "must-not-harm (revenue, latency, refunds)"),
    ("unit", "randomize by **user**, not session"),
    ("split", "50/50, assigned at first exposure"),
    ("avoid proxy trap", "don't win clicks & lose the real goal"),
  ]),
  ("Power & size", [
    ("&alpha; (0.05)", "false-positive rate (Type I)"),
    ("power (0.8)", "chance to catch a real effect (1&minus;&beta;)"),
    ("MDE", "smallest effect worth detecting"),
    ("n &uarr; when", "smaller MDE, lower baseline, more power"),
    ("duration", "&ge; 1&ndash;2 full weeks (seasonality + novelty)"),
    ("rule of thumb", "n &asymp; 16 &middot; &sigma;&sup2; / MDE&sup2; per arm"),
  ]),
  ("Analyze", [
    ("two-prop z / t-test", "compare rates / means across arms"),
    ("p-value", "P(data this extreme | no real effect)"),
    ("confidence interval", "report it &mdash; size, not just yes/no"),
    ("stat vs practical", "significant &ne; big enough to ship"),
    ("multiple metrics", "correct &alpha; (Bonferroni / FDR)"),
    ("decision", "significant + past MDE + guardrails safe"),
  ]),
  ("Trust checks", [
    ("SRM", "split really 50/50? if not, **stop** &mdash; it's broken"),
    ("A/A test", "no diff expected; validates the pipeline"),
    ("instrumentation", "did treatment render & log? check first"),
    ("Twyman's law", "surprising result &rarr; probably a **bug**"),
  ]),
  ("The pitfalls", [
    ("peeking", "repeated looks inflate false positives &rarr; look **once**"),
    ("p-hacking", "many metrics/slices &rarr; **pre-register**"),
    ("Simpson's paradox", "pooled reverses segments &rarr; check the mix"),
    ("novelty / primacy", "early spike/dip fades &rarr; run to steady state"),
    ("interference", "spillover (networks/marketplace) &rarr; cluster randomize"),
    ("winner's curse", "shipped wins overstated &rarr; holdback + replicate"),
  ]),
  ("\"The test is flat\" checklist", [
    ("trustworthy?", "SRM, logging, did it render (Twyman)"),
    ("powered?", "wide CI = no info, not no effect &rarr; run longer"),
    ("segments?", "helps one group, hurts another (pre-registered)"),
    ("over time?", "novelty decaying / primacy recovering"),
    ("guardrail hit?", "flat primary + broken guardrail = **kill**"),
  ]),
 ]))
LESSONS={"ab-07-cheat":"\n".join(p)}
print("content_abcheat OK — chars:", len(LESSONS["ab-07-cheat"]))
