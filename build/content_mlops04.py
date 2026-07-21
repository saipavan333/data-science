# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]
p.append(B.why(
 "Here's the truth that separates ML from ordinary software: **your model gets worse over time even "
 "if you never touch it.** Ordinary code does the same thing forever; a model was trained on a "
 "snapshot of a world that keeps changing &mdash; customers shift, competitors launch, fraud tactics "
 "evolve &mdash; so its accuracy silently **decays**. Deploying without monitoring is flying blind. "
 "This lesson is how you watch a live model's health and catch the rot before it costs you."))
p.append(B.h2("Why models decay: drift", kicker="The world moves on"))
p.append(B.concept(
 "Two kinds of change erode a deployed model:\n\n"
 "- **Data drift** (covariate shift): the **inputs** change distribution. A new marketing campaign "
 "brings younger users than the model trained on; a sensor ages and reads differently. The "
 "relationship may still hold, but the model now sees inputs it wasn't trained for.\n"
 "- **Concept drift**: the **relationship** between inputs and target changes. What predicted fraud "
 "last year doesn't this year because fraudsters adapted; buying behaviour shifts after a pandemic. "
 "The old mapping is simply **wrong** now.\n\n"
 "Either way, a model that scored 0.90 at launch quietly slides &mdash; and nothing errors out to "
 "tell you."))
p.append(B.figure(IMG+"s_mlops_drift.png",
 "**Models decay and must be refreshed.** Live accuracy drifts down after deployment as the world "
 "changes; when monitoring detects it crossing an **alert threshold**, you **retrain** on fresh data "
 "and recover &mdash; then the slow decay begins again. Maintenance, not a one-time launch.",
 "Live accuracy declining over weeks, crossing an alert threshold, then jumping back up after retraining."))
p.append(B.h2("What to monitor", kicker="Three layers"))
p.append(B.concept(
 "You can't watch everything, so watch these, in order of how fast they warn you:\n\n"
 "- **Operational health** &mdash; latency, error rate, uptime, throughput. (Is the service even "
 "up?)\n"
 "- **Input drift** &mdash; are the incoming feature distributions still like training? This warns "
 "you **early**, *before* accuracy visibly drops, and needs no labels.\n"
 "- **Prediction & performance** &mdash; are the output distributions stable, and &mdash; once "
 "true labels arrive &mdash; is accuracy holding? This is the ground truth, but often **delayed** "
 "(you may not learn who actually churned for weeks)."))
p.append(B.concept(
 "A common early-warning check compares a feature's **live** distribution to its **training** "
 "distribution. A simple, robust version is the **standardized mean shift** &mdash; how far the live "
 "mean has moved, in training standard deviations. Small = stable; large = investigate:"))
_c,_o=_run(r'''
import numpy as np
train = np.array([50,52,48,51,49,53,47,50,52,48,51,49,50,52,48], dtype=float)  # training feature
live  = np.array([58,61,57,60,59,62,56,60,58,61], dtype=float)                 # recent production

shift = abs(live.mean() - train.mean()) / train.std()
print(f"train mean {train.mean():.1f}, live mean {live.mean():.1f}")
print(f"standardized shift: {shift:.2f} std  ->  {'DRIFT — investigate' if shift>1 else 'stable'}")
''')
p.append(B.code_example(_c,_o,filename="drift_check.py"))
p.append(B.tip(
 "The point of drift detection is to warn you **before** performance visibly craters &mdash; "
 "especially valuable because true labels are often **delayed**. Input-drift alarms need no labels "
 "at all, so they're your earliest signal. When an alarm fires, you investigate: is it a real world "
 "change (retrain), a data-pipeline bug (fix the pipeline), or just noise (tune the threshold)?"))
p.append(B.h2("Closing the loop: retraining", kicker="Keep the model fresh"))
p.append(B.concept(
 "When monitoring signals meaningful decay, you **retrain** on recent data and redeploy &mdash; the "
 "feedback arrow that closes the ML lifecycle loop. Retraining can be **scheduled** (every week/"
 "month), **triggered** by a drift/performance alert, or **continuous** in fast-moving domains. "
 "Whichever, treat the new model like any release: validate it, compare it to the current one, and "
 "roll it out safely (canary / shadow) so a bad retrain can't silently make things worse."))
p.append(B.h2("Your turn — flag drift with a standardized shift", kicker="Interactive lab"))
p.append(B.pylab(
 "Detect input drift: compute the **standardized mean shift** of the live sample versus training "
 "&mdash; `|mean(live) &minus; mean(train)| / std(train)` &mdash; round to **2 decimals**, and "
 "assign to **`answer`**. A value above ~1 std would trigger an investigation.",
 "import numpy as np\n"
 "train = np.array([50,52,48,51,49,53,47,50,52,48,51,49,50,52,48], dtype=float)\n"
 "live  = np.array([58,61,57,60,59,62,56,60,58,61], dtype=float)\n",
 "answer = round(float(abs(live.mean() - train.mean()) / train.std()), 2)",
 starter="import numpy as np\n# standardized shift: |live.mean() - train.mean()| / train.std(), 2 dp\nanswer = ",
 hint="Compute `abs(live.mean() - train.mean())`, divide by `train.std()`, cast to float, round 2 dp.",
 title="Lab — a drift alarm",
 preview="numpy loaded; a training feature sample and a recent live sample preloaded. First Run boots Python.",
 explain="The live mean has jumped several training standard deviations &mdash; a large shift that "
         "should trigger investigation, likely well **before** accuracy visibly drops. Input-drift "
         "checks like this need no labels, which is why they're your earliest warning that the world "
         "has moved."))
p.append(B.keypoints([
 "A deployed model **decays even if untouched**, because the world it was trained on keeps changing "
 "&mdash; deploying without monitoring is flying blind.",
 "**Data drift** = the inputs' distribution shifts; **concept drift** = the input&rarr;target "
 "relationship itself changes. Both silently erode accuracy.",
 "Monitor three layers: **operational** (latency/errors), **input drift** (early, label-free), and "
 "**performance** (ground truth, but often **delayed**).",
 "**Input-drift alarms warn you before accuracy visibly drops** &mdash; a simple check is the "
 "standardized shift in a feature's mean.",
 "Close the loop by **retraining** (scheduled / triggered / continuous) and rolling out the new "
 "model safely (canary/shadow).",
]))
p.append(B.quiz([
 {"q":"A fraud model that performed well six months ago is now missing obvious fraud, though nothing "
      "in the code changed. Best explanation?",
  "options":[
   {"t":"Concept drift — fraudsters adapted, so the input→fraud relationship changed and the old "
        "model is now outdated","correct":True,
    "why":"Correct. Fraud is adversarial: tactics evolve, so the mapping the model learned no longer "
          "holds (concept drift). The fix is retraining on recent data &mdash; and monitoring so you "
          "catch it sooner next time."},
   {"t":"The code must have a new bug",
    "why":"Nothing in the code changed; the *world* changed. This is drift, not a code regression."},
   {"t":"Models never degrade on their own",
    "why":"They do &mdash; that's the core lesson. A static model against a shifting world decays "
          "even with no code changes."},
   {"t":"The server needs more memory",
    "why":"Resources don't explain declining predictive quality. Adversarial concept drift does."}]},
 {"q":"Why is monitoring *input distributions* valuable even before you know if predictions were "
      "right?",
  "options":[
   {"t":"It's an early, label-free warning — inputs drifting signals trouble before delayed labels "
        "reveal a performance drop","correct":True,
    "why":"Correct. True labels (did they actually churn/default?) often arrive weeks later, so "
          "waiting for performance metrics is slow. Input-drift checks need no labels and warn you "
          "immediately that the world has shifted."},
   {"t":"Input distributions never change",
    "why":"They frequently do (that's data drift) &mdash; which is exactly why monitoring them is "
          "useful."},
   {"t":"It replaces the need to ever check accuracy",
    "why":"No &mdash; performance on real labels is the ground truth. Input drift is an *early* "
          "complement, not a replacement."},
   {"t":"Because inputs determine latency",
    "why":"Drift monitoring is about *distribution* change and predictive validity, not latency."}]},
]))
p.append(B.practice([
 {"q":"You're deploying a demand-forecasting model. Design a monitoring plan in three layers and say "
      "what each catches.",
  "sol":"**(1) Operational health** &mdash; track latency, error rate, uptime, and job success; "
        "catches outright failures (the pipeline broke, the service is down) fastest. **(2) Input "
        "drift** &mdash; monitor the distributions of key features (traffic, price, seasonality "
        "inputs) versus the training baseline, alerting on large standardized shifts or PSI; catches "
        "a **changing world early and without labels** (a new region, a price change, a demand "
        "regime shift). **(3) Prediction & performance** &mdash; watch the forecast distribution for "
        "sudden changes, and once actuals arrive, track forecast error (MAE/MAPE) against a "
        "threshold; this is the **ground truth** but **delayed**, since you only learn true demand "
        "later. Wire alerts on each, and connect performance/drift alarms to a **retraining** "
        "trigger. The layered design gives you fast failure alerts, early drift warnings, and "
        "eventual truth &mdash; each covering the others' blind spots."},
 {"q":"When a drift alarm fires, why shouldn't you always immediately retrain? What are the "
      "possibilities?",
  "sol":"Because an alarm signals *change*, not necessarily *model decay*, and retraining on bad data "
        "can make things **worse**. Investigate the cause first: **(a) a real world change** (new "
        "user mix, genuine behaviour shift) &rarr; retraining on fresh data is the right fix; **(b) a "
        "data-pipeline bug** (a feature started arriving in different units, a broken join, a nulled "
        "column) &rarr; the fix is repairing the **pipeline**, and retraining on the corrupted data "
        "would bake in the error; **(c) noise / a one-off event** (a holiday spike, a transient "
        "outage) &rarr; the right response may be to wait or tune the alert threshold, not retrain. "
        "So the response to an alarm is **diagnose, then act** &mdash; and when you do retrain, "
        "validate and roll out the new model safely (shadow/canary) rather than trusting it blindly."},
]))
p.append(B.deepdive(
 B.concept(
  "**Measuring drift, a bit more formally.** Beyond a standardized mean shift, teams use "
  "distribution-distance measures: the **Population Stability Index (PSI)** (a rule-of-thumb: <0.1 "
  "stable, 0.1&ndash;0.25 moderate shift, >0.25 significant), the **Kolmogorov&ndash;Smirnov** "
  "statistic for continuous features, and **KL/JS divergence**. For predictions, you watch the "
  "**output distribution** and, when labels arrive, performance metrics. No single number is "
  "definitive &mdash; the art is choosing sensible features to watch, baselines to compare against, "
  "and thresholds that alert on real shifts without crying wolf. Start simple (a few key features, "
  "clear thresholds) and add sophistication as you learn your system's normal fluctuations.") +
 B.concept(
  "**Safe rollout: shadow, canary, and A/B for models.** A retrained model shouldn't replace the old "
  "one in one risky switch. **Shadow deployment** runs the new model alongside the old on real "
  "traffic *without* acting on its predictions, so you can compare them safely. **Canary** routes a "
  "small slice of traffic to the new model and watches metrics before ramping up. And a true **A/B "
  "test** (the experimentation track, applied to models) measures whether the new model actually "
  "improves the business metric, not just offline accuracy. These let you catch a bad retrain "
  "&mdash; including one triggered by a drift alarm that turned out to be a pipeline bug &mdash; "
  "*before* it reaches all users. The lifecycle loop closes not with a reckless redeploy, but with a "
  "*measured, reversible* one."),
 title="Deep dive: PSI/KS drift measures, and shadow/canary/A-B model rollouts"))
LESSONS={"mlops-04-monitor":"\n".join(x for x in p if x)}
print("content_mlops04 OK — chars:", len(LESSONS["mlops-04-monitor"]))
