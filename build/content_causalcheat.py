# -*- coding: utf-8 -*-
import builder as B
p=[B.concept("Causal inference on one page &mdash; the danger, the diagram rules, and the methods. "
 "Press **Print**.")]
p.append(B.cheatsheet("Causal Inference — one-page reference",
 "Observational numbers don't speak for themselves: **draw your assumptions, adjust for the right "
 "things, and name what must be true.**",
 [
  ("The core danger", [
    ("correlation &ne; causation", "a third cause can fake it"),
    ("confounder", "common cause of X **and** Y"),
    ("counterfactual", "the unobserved 'what if' &mdash; the whole problem"),
    ("randomization", "gold standard: severs confounders"),
  ]),
  ("DAG rules", [
    ("fork (Z&rarr;X, Z&rarr;Y)", "confounder &mdash; **adjust** for Z"),
    ("chain (X&rarr;M&rarr;Y)", "mediator &mdash; **don't** adjust (total effect)"),
    ("collider (X&rarr;C&larr;Y)", "adjusting **creates** bias"),
    ("backdoor criterion", "close all backdoors, open no colliders"),
    ("\"control for everything\"", "**wrong** &mdash; can add bias"),
  ]),
  ("Methods (no experiment)", [
    ("matching / propensity", "compare like-with-like on confounders"),
    ("regression adjustment", "put confounders in the model"),
    ("difference-in-differences", "(treated &Delta;) &minus; (control &Delta;)"),
    ("instrumental variable", "a quasi-random nudge to X"),
    ("regression discontinuity", "compare just-above vs just-below a cutoff"),
  ]),
  ("The assumption each needs", [
    ("matching / regression", "no **unmeasured** confounding"),
    ("diff-in-diff", "**parallel trends** (check pre-period)"),
    ("IV", "relevance + exclusion restriction"),
    ("RDD", "continuity at the cutoff"),
  ]),
  ("Selection bias", [
    ("it's a collider", "conditioning on how data was selected"),
    ("example", "studying only admitted/converted units"),
    ("tell", "an effect that flips in the selected sample"),
  ]),
 ]))
LESSONS={"causal-05-cheat":"\n".join(p)}
print("causalcheat OK")
