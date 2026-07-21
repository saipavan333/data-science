# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]
p.append(B.why(
 "A model in a notebook helps **no one**. Value is created only when a model runs **reliably, on new "
 "data, without you babysitting it** &mdash; scoring transactions at 3 a.m., ranking feeds for "
 "millions, flagging fraud in real time. The gap between *\"it works in my notebook\"* and *\"it "
 "runs in production\"* is enormous, and bridging it &mdash; **MLOps** &mdash; is what turns a "
 "data-science *experiment* into a data-science *product*. This track is that bridge."))
p.append(B.h2("The ML lifecycle is a loop, not a line", kicker="The big picture"))
p.append(B.concept(
 "Productionizing a model isn't a one-time hand-off; it's a **cycle** that never really ends. You "
 "collect data, train, evaluate offline, deploy, and monitor &mdash; and monitoring feeds back into "
 "retraining as the world changes:"))
p.append(B.figure(IMG+"s_mlops_lifecycle.png",
 "**The ML lifecycle.** Data &rarr; train &rarr; evaluate &rarr; deploy &rarr; monitor &mdash; and "
 "when monitoring detects **drift**, you loop back to retrain on fresh data. A production model is a "
 "*living system* you keep healthy, not a file you ship once.",
 "The ML lifecycle loop: collect data, train, evaluate, deploy, monitor, and feed drift back to retraining."))
p.append(B.h2("From notebook to pipeline", kicker="Reproducible, automated steps"))
p.append(B.concept(
 "The first step to production is turning ad-hoc notebook cells into a **pipeline**: a defined, "
 "repeatable sequence &mdash; ingest &rarr; clean &rarr; engineer features &rarr; train (or score) "
 "&mdash; that runs the **same way every time**, by a schedule or a trigger, with no human clicking "
 "cells. Crucially, the **exact same feature-engineering code runs at training and at serving time**. "
 "If training scales a feature one way and serving does it another, predictions silently corrupt "
 "&mdash; the dreaded ~training&ndash;serving skew~."))
p.append(B.pitfall(
 "**Training&ndash;serving skew** is a top cause of \"great in the notebook, broken in production.\" "
 "It happens when the transformations applied to live data differ &mdash; even subtly &mdash; from "
 "those used in training: a different default fill value, a scaler recomputed on live data, a "
 "category the encoder never saw. The fix is to **package the fitted transforms with the model** (one "
 "pipeline object) and reuse it verbatim at serving &mdash; never re-implement preprocessing "
 "separately for production."))
p.append(B.concept(
 "This is exactly why the **Pipeline** object (from the feature-engineering track) matters in "
 "production: it bundles every fitted step &mdash; imputers, scalers, encoders, the model &mdash; "
 "into a single artifact. You fit it once on training data, save it, and at serving time call one "
 "`.predict()`; the identical preprocessing is guaranteed. See the serving-time reality &mdash; you "
 "apply the **saved** training parameters, never recompute on the incoming request:"))
_c,_o=_run(r'''
import numpy as np
# Parameters LEARNED at training time and saved with the model:
saved_mean, saved_std = 50.0, 10.0        # e.g. a fitted scaler

# A live request arrives. Transform it with the SAVED params (not recomputed!):
new_request = np.array([65.0, 45.0, 70.0])
scaled = (new_request - saved_mean) / saved_std
print("scaled request:", scaled.round(2), " -> feed to model.predict()")
''')
p.append(B.code_example(_c,_o,filename="serving_transform.py"))
p.append(B.h2("Your turn — transform a live request the right way", kicker="Interactive lab"))
p.append(B.pylab(
 "At serving time you must reuse the **training** scaler's saved parameters, never recompute on the "
 "incoming data. Standardize `new_request` with `saved_mean` and `saved_std`, take the **mean** of "
 "the result, round to **2 decimals**, and assign to **`answer`**.",
 "import numpy as np\n"
 "saved_mean, saved_std = 50.0, 10.0     # learned at training, shipped with the model\n"
 "new_request = np.array([65.0, 45.0, 70.0])\n",
 "answer = round(float(((new_request - saved_mean) / saved_std).mean()), 2)",
 starter="import numpy as np\n# scale new_request with the SAVED mean/std; take the mean; round 2 dp\nanswer = ",
 hint="`(new_request - saved_mean) / saved_std`, then `.mean()`, `float(...)`, round to 2 dp. Use the "
      "saved params, not new_request.mean().",
 title="Lab — serving reuses saved parameters",
 preview="numpy loaded; saved_mean, saved_std, and new_request preloaded. First Run boots Python.",
 explain="The request mean is 60, so `(60-50)/10 = 1.0`. Using the **saved** training parameters "
         "guarantees the live data is transformed exactly as training data was &mdash; the antidote "
         "to training-serving skew. Recomputing stats on each request would silently break "
         "predictions."))
p.append(B.keypoints([
 "A model only creates value when it runs **reliably on new data, unattended** &mdash; that's "
 "**MLOps**.",
 "The ML lifecycle is a **loop**: data &rarr; train &rarr; evaluate &rarr; deploy &rarr; monitor "
 "&rarr; retrain &mdash; not a one-time hand-off.",
 "Turn notebook cells into a **pipeline**: the same steps, run the same way every time, "
 "automatically.",
 "The **same preprocessing must run at training and serving** &mdash; package fitted transforms with "
 "the model to avoid **training&ndash;serving skew**.",
 "At serving time, apply the model's **saved** parameters to incoming data; never recompute them "
 "per-request.",
]))
p.append(B.quiz([
 {"q":"Your model scores 0.92 in the notebook but gives garbage in production, though the code "
      "'looks the same.' Likeliest cause?",
  "options":[
   {"t":"Training–serving skew — the preprocessing applied to live data differs from what was used "
        "in training","correct":True,
    "why":"Correct. If the serving path re-implements or recomputes preprocessing differently (a "
          "different fill value, a scaler fit on live data, an unseen category), inputs reach the "
          "model in a different form than training &mdash; and predictions corrupt. Package and reuse "
          "the fitted pipeline."},
   {"t":"The production server is slower",
    "why":"Speed doesn't produce *wrong* predictions. Garbage outputs from 'same' code point to a "
          "preprocessing mismatch (skew)."},
   {"t":"The model file is corrupted",
    "why":"Possible but rare; the classic 'works in notebook, wrong in prod' signature is training-"
          "serving skew in the preprocessing."},
   {"t":"Notebooks always outperform production",
    "why":"They shouldn't &mdash; identical inputs give identical outputs. A gap means the inputs "
          "differ, i.e. skew."}]},
 {"q":"Why package fitted transformers and the model together as a single pipeline artifact?",
  "options":[
   {"t":"So the exact same preprocessing runs at serving as at training, with one predict call","correct":True,
    "why":"Correct. Bundling imputers/scalers/encoders with the model guarantees identical "
          "preprocessing in production and eliminates skew from re-implementing steps separately."},
   {"t":"To make the model file smaller",
    "why":"It often makes the artifact *larger*; the benefit is correctness/consistency, not size."},
   {"t":"Because models can't be saved on their own",
    "why":"They can &mdash; but saving the model alone risks the preprocessing diverging at serving. "
          "Bundling prevents that."},
   {"t":"To speed up training",
    "why":"Pipelines are about reproducible, skew-free serving, not training speed."}]},
]))
p.append(B.practice([
 {"q":"Describe the minimum steps to take a churn model from a working notebook to something that "
      "scores customers automatically every night.",
  "sol":"**(1) Refactor into a pipeline:** move the notebook's clean&rarr;feature&rarr;model steps "
        "into tested `.py` code, with all fitted transforms bundled in one pipeline object. **(2) "
        "Pin the environment** (requirements/lockfile) and **version the code** in Git and the "
        "**trained model artifact** (next lesson). **(3) Parameterise inputs/outputs** &mdash; read "
        "the day's customers from the warehouse, write scores back &mdash; using config, not "
        "hard-coded paths. **(4) Schedule it** (cron, Airflow, a cloud scheduler) to run nightly, "
        "loading the saved pipeline and calling `.predict()`. **(5) Add logging + monitoring** so a "
        "failure or a drop in score quality raises an alert. The essence: same code, same "
        "preprocessing, runs unattended on fresh data, observable when it breaks."},
 {"q":"Why is 'the ML lifecycle is a loop' more than a slogan &mdash; what does treating it as a line "
      "cost you?",
  "sol":"Treating deployment as the *finish line* ignores that a model's accuracy **decays** the "
        "moment the world starts differing from its training data (customer behaviour shifts, new "
        "products launch, seasonality turns). A 'line' mindset ships the model and walks away, so the "
        "silent decay goes unnoticed until it causes real damage (mispriced risk, missed fraud, angry "
        "users). Treating it as a **loop** means you build **monitoring** to detect drift, **alerts** "
        "to catch it, and a **retraining** path to refresh the model &mdash; keeping it healthy over "
        "time. The loop framing is what turns a one-off artifact into a durable, maintained system, "
        "and it's the single biggest mindset difference between research and production ML."},
]))
p.append(B.deepdive(
 B.concept(
  "**Batch vs. streaming pipelines.** Many production models run as **batch** jobs: on a schedule "
  "(nightly, hourly) they pull a chunk of data, score it, and write results &mdash; simple, robust, "
  "and enough for most business use cases (churn lists, risk scores, recommendations refreshed "
  "daily). Others must react in **real time** (fraud on a live transaction, ad ranking on page load), "
  "which needs a streaming or request/response architecture (next lesson). The engineering "
  "complexity jumps with latency requirements, so a mature first question is always: *does this "
  "actually need to be real-time, or is batch fine?* &mdash; because batch is far cheaper to build "
  "and operate.") +
 B.concept(
  "**Where MLOps borrows from software engineering &mdash; and where it's harder.** Pipelines, "
  "version control, testing, CI/CD, and monitoring all come straight from software engineering, and "
  "MLOps rightly adopts them. But ML adds problems ordinary software doesn't have: the artifact "
  "depends on **data** (which drifts) as much as code, 'correctness' is **statistical** not binary, "
  "and you must version **data and models**, not just source. That's why the field grew its own "
  "tooling &mdash; experiment trackers, model registries, feature stores, drift monitors &mdash; on "
  "top of classic DevOps. The mindset to carry in: a model is **code + data + environment**, and all "
  "three must be reproducible, versioned, and observed for it to be trustworthy in production."),
 title="Deep dive: batch vs. real-time pipelines, and how MLOps extends DevOps"))
LESSONS={"mlops-01-pipeline":"\n".join(x for x in p if x)}
print("content_mlops01 OK — chars:", len(LESSONS["mlops-01-pipeline"]))
