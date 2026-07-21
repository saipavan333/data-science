# -*- coding: utf-8 -*-
import builder as B
p=[B.concept("MLOps on one page &mdash; ship it, version it, serve it, and watch it (because it "
 "decays). Press **Print**.")]
p.append(B.cheatsheet("MLOps — one-page reference",
 "Turning a model into a product: a model is **code + data + environment** &mdash; packaged "
 "skew-free, versioned, served within budget, and monitored.",
 [
  ("Lifecycle", [
    ("it's a loop", "data&rarr;train&rarr;eval&rarr;deploy&rarr;monitor&rarr;retrain"),
    ("pipeline", "same steps, run the same way, unattended"),
    ("training-serving skew", "preprocessing differs &rarr; silent corruption"),
    ("fix", "package fitted transforms **with** the model"),
  ]),
  ("Serialize & version", [
    ("joblib.dump/load", "save the **whole pipeline**"),
    ("never unpickle untrusted", "arbitrary code execution"),
    ("model = code+data+params", "version **all three**"),
    ("model registry", "what's deployed + lineage + rollback"),
  ]),
  ("Serving", [
    ("batch", "scheduled, stored &mdash; simple, enough usually"),
    ("online (API)", "millisecond, real-time &mdash; heavier"),
    ("latency = the tail", "judge **p95/p99**, not the mean"),
    ("cut latency", "simpler model, cache, precompute, batch"),
  ]),
  ("Monitoring & drift", [
    ("models decay untouched", "the world moves on"),
    ("data drift", "inputs' distribution shifts"),
    ("concept drift", "input&rarr;target relationship changes"),
    ("watch inputs", "early warning, **no labels** needed"),
    ("alarm &rarr; diagnose", "bug vs. real drift, then retrain"),
  ]),
  ("Safe rollout", [
    ("shadow", "run alongside, don't act &mdash; compare"),
    ("canary", "small traffic slice first"),
    ("A/B the intervention", "measure real business impact"),
  ]),
 ]))
LESSONS={"mlops-06-cheat":"\n".join(p)}
print("mlopscheat OK")
