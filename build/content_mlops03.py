# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
p=[]
p.append(B.why(
 "Deploying a model means making its predictions **available** to whatever needs them &mdash; a "
 "nightly job, a website, a mobile app. The two big architectural choices (batch vs. real-time) and "
 "the metrics that matter (latency, throughput, and especially the **tail**) determine whether your "
 "model is a smooth part of the product or a bottleneck that times out under load. This is where data "
 "science meets systems engineering."))
p.append(B.h2("Batch vs. online serving", kicker="The first decision"))
p.append(B.concept(
 "How predictions reach their consumer splits into two patterns:\n\n"
 "- **Batch (offline) serving**: score a big pile of data on a schedule and store the results for "
 "later lookup. Predicting tomorrow's churn risk for every customer overnight, writing scores to a "
 "table the app reads. **Simple, robust, cheap** &mdash; and enough for most use cases.\n"
 "- **Online (real-time) serving**: expose the model behind an **API** that scores a single input "
 "**on demand**, in milliseconds. Fraud detection on a live transaction, recommendations on page "
 "load. **Powerful but far more demanding** &mdash; you now own an always-on, low-latency service.\n\n"
 "The mature first question is: *\"does this genuinely need to be real-time, or is a daily batch "
 "fine?\"* &mdash; because batch is dramatically cheaper and easier to operate."))
p.append(B.h2("Online serving: the model as an API", kicker="Request in, prediction out"))
p.append(B.concept(
 "Real-time serving wraps the model in a web service (commonly a **REST API**, e.g. with FastAPI): a "
 "request arrives with features, the service runs the **saved pipeline**, and returns a prediction "
 "as JSON. Package that service in a **container** (Docker) so it runs identically anywhere, and put "
 "it behind a load balancer to scale. The skeleton is small; the *operational* weight &mdash; "
 "uptime, scaling, latency &mdash; is the real work:"))
_c,_o=_run(r'''
# Sketch of a real-time prediction endpoint (FastAPI-style)
def predict_endpoint(request_json):
    features = parse(request_json)          # validate & shape the input
    x = pipeline.transform(features)        # SAME preprocessing as training
    prob = model.predict_proba(x)[0, 1]     # score it
    return {"probability": round(prob, 4)}  # return JSON, in milliseconds

# def parse/pipeline/model omitted — this is the shape, not a runnable service
print("request -> parse -> pipeline.transform -> model.predict -> JSON response")
''')
p.append(B.code_example(_c,_o,filename="serve_api.py"))
p.append(B.h2("The metric that bites: tail latency", kicker="p95 / p99, not the mean"))
p.append(B.concept(
 "Two numbers describe a serving system: **throughput** (requests handled per second) and "
 "**latency** (time per request). The trap is judging latency by the **average** &mdash; because "
 "users feel the **worst** requests, not the typical one. If the mean is 15 ms but 1 in 20 requests "
 "takes 200 ms, that **p95** of 200 ms is what causes timeouts and rage-quits. Always report the "
 "**tail** (p95, p99), not just the mean:"))
_c,_o=_run(r'''
import numpy as np
latencies_ms = np.array([12,15,11,140,13,12,16,14,200,12,13,15,11,12,18,13,17,12,150,14])

print(f"mean latency: {latencies_ms.mean():6.1f} ms   <- looks fine")
print(f"p95 latency:  {np.percentile(latencies_ms,95):6.1f} ms   <- what users actually feel")
print(f"p99 latency:  {np.percentile(latencies_ms,99):6.1f} ms   <- the timeouts live here")
''')
p.append(B.code_example(_c,_o,filename="tail_latency.py"))
p.append(B.tip(
 "Levers to cut latency when it matters: **smaller/simpler models** (a distilled or linear model may "
 "be 10&times; faster for a hair less accuracy), **precompute** features or predictions where "
 "possible (a hybrid of batch + online), **cache** frequent requests, and **batch** incoming "
 "requests to use hardware efficiently. The right trade of accuracy for speed is a *product* "
 "decision, not just a modelling one."))
p.append(B.h2("Your turn — measure the tail, not the mean", kicker="Interactive lab"))
p.append(B.pylab(
 "Users feel the slow requests. From the `latencies_ms` array, compute the **95th percentile** "
 "(`np.percentile`), round to **1 decimal**, and assign to **`answer`**. Notice how far it sits "
 "above the mean.",
 "import numpy as np\n"
 "latencies_ms = np.array([12,15,11,140,13,12,16,14,200,12,13,15,11,12,18,13,17,12,150,14])\n",
 "answer = round(float(np.percentile(latencies_ms, 95)), 1)",
 starter="import numpy as np\n# the p95 latency (95th percentile), rounded to 1 dp\nanswer = ",
 hint="`np.percentile(latencies_ms, 95)`, cast to float, round to 1 dp.",
 title="Lab — p95 latency",
 preview="numpy loaded; a sample of request latencies (ms) preloaded. First Run boots Python.",
 explain="The p95 towers over the ~30 ms mean, because a handful of 140&ndash;200 ms requests drive "
         "the tail &mdash; and those are exactly the ones that time out and frustrate users. That's "
         "why serving SLAs are written on **p95/p99**, never the average."))
p.append(B.keypoints([
 "**Batch** serving (scheduled, results stored) is simple and enough for most use cases; **online** "
 "serving (an API, millisecond latency) is powerful but operationally heavy &mdash; ask if you truly "
 "need real-time.",
 "Online serving wraps the **saved pipeline** in a service (REST API), usually **containerized** "
 "(Docker) for identical, scalable deployment.",
 "Judge serving by **throughput** and **latency** &mdash; but latency by the **tail (p95/p99)**, not "
 "the mean, because users feel the worst requests.",
 "Cut latency with **simpler models**, **precompute/cache**, and **request batching** &mdash; "
 "trading a little accuracy for speed is a product decision.",
 "The same fitted **preprocessing** must run in the serving path (avoid training&ndash;serving "
 "skew).",
]))
p.append(B.quiz([
 {"q":"Your prediction API has a mean latency of 20 ms but users complain it's slow. What do you "
      "check first?",
  "options":[
   {"t":"The tail latency (p95/p99) — a good mean can hide a slow tail that causes the timeouts users "
        "feel","correct":True,
    "why":"Correct. Users experience the *worst* requests, not the average. A 20 ms mean with a 300 "
          "ms p99 will feel slow and cause timeouts. Serving SLAs are written on the tail for exactly "
          "this reason."},
   {"t":"Retrain the model for higher accuracy",
    "why":"Accuracy is unrelated to perceived slowness. Investigate latency percentiles, not model "
          "quality."},
   {"t":"The mean is fine, so the users are wrong",
    "why":"The mean can look fine while the tail is terrible &mdash; that's precisely what users "
          "feel. Check p95/p99."},
   {"t":"Increase the batch size",
    "why":"Bigger batches can *raise* per-request latency for online serving. First diagnose the tail."}]},
 {"q":"For a daily 'customers likely to churn' report, which serving pattern is most appropriate?",
  "options":[
   {"t":"Batch scoring on a schedule, storing results for the report to read","correct":True,
    "why":"Correct. The need is periodic, not instantaneous, so a scheduled batch job that scores all "
          "customers and writes results is simplest, cheapest, and robust &mdash; no always-on API "
          "needed."},
   {"t":"A real-time API called per customer",
    "why":"Overkill for a daily report: it adds latency, uptime, and scaling burdens with no benefit "
          "when predictions are only needed once a day."},
   {"t":"Streaming inference on every event",
    "why":"Unnecessary complexity for a daily batch need; reserve streaming for genuinely real-time "
          "reactions."},
   {"t":"Manual scoring in a notebook each morning",
    "why":"Not reproducible or reliable; a scheduled batch pipeline is the professional version of "
          "'once a day.'"}]},
]))
p.append(B.practice([
 {"q":"A product team wants model predictions shown the instant a user opens a screen. Walk through "
      "the serving decisions you'd make.",
  "sol":"**(1) Confirm the latency need:** 'instant on open' implies **online** serving with a tight "
        "latency budget (say p99 < 100 ms). **(2) Consider a hybrid:** if predictions don't depend on "
        "just-arrived inputs, **precompute** them in batch and simply *look them up* on open &mdash; "
        "the fastest, cheapest path. If they need live inputs, build a real-time API. **(3) Build the "
        "service:** wrap the **saved pipeline** in a REST endpoint, **containerize** it, and put it "
        "behind autoscaling + a load balancer. **(4) Meet the tail:** measure **p95/p99**, and if "
        "needed cut latency with a **simpler/distilled model**, **caching** frequent inputs, and "
        "**request batching**. **(5) Monitor** latency and error rates with alerts. The key judgement "
        "is step 2 &mdash; a lot of 'real-time' needs are satisfied by precomputed lookups, avoiding "
        "the cost of true online inference."},
 {"q":"Explain why the average latency can be a dangerously misleading SLA, using a concrete "
      "example.",
  "sol":"Because averages **hide the tail**, and users (and upstream timeouts) are governed by the "
        "worst requests. Example: an endpoint serves 1,000 requests &mdash; 950 take 10 ms and 50 "
        "take 500 ms. The **mean** is ~34 ms (looks great), but **5% of every user's requests take "
        "half a second**, blowing past a 200 ms client timeout and producing visible failures and "
        "churn. If you'd promised '35 ms average,' you'd be technically right and practically wrong. "
        "That's why serving SLAs specify **p95/p99 latency** (e.g. 'p99 < 150 ms'): they bound the "
        "experience of nearly *all* requests, not a typical one. The average is the number that makes "
        "a slow service look acceptable."},
]))
p.append(B.deepdive(
 B.concept(
  "**Why tails are fat, and what makes them fatter.** Request latency is rarely bell-shaped; it's "
  "**right-skewed** with a long tail caused by garbage-collection pauses, cache misses, cold model "
  "loads, network hiccups, resource contention, and occasional big inputs. Worse, tails **compound**: "
  "if a page makes several model calls, the chance that *at least one* hits the slow tail rises fast "
  "&mdash; so a rare 1% slowness per call can make a noticeable fraction of *page loads* slow. This "
  "is why large systems obsess over p99 (and even p99.9), attack tail sources specifically, and use "
  "techniques like hedged requests and timeouts-with-fallbacks rather than chasing a better average.") +
 B.concept(
  "**The serving-stack ladder.** You don't have to hand-build everything: the ecosystem offers "
  "**model servers** (TensorFlow Serving, TorchServe, NVIDIA Triton, BentoML) that handle batching, "
  "versioning, and GPU use; **serverless** options (cloud functions) for spiky, low-volume traffic; "
  "and fully **managed endpoints** (SageMaker, Vertex AI) that trade cost for operational ease. The "
  "right rung depends on scale, latency, budget, and team size &mdash; a startup might ship a single "
  "FastAPI container, while a high-QPS system needs a dedicated model server with autoscaling. The "
  "engineering principle is the same as everywhere in MLOps: **match the operational complexity to "
  "the actual requirement**, and don't build a real-time fleet when a nightly batch and a lookup "
  "table would do."),
 title="Deep dive: why latency tails are fat and compounding, and the serving-stack options"))
LESSONS={"mlops-03-serve":"\n".join(x for x in p if x)}
print("content_mlops03 OK — chars:", len(LESSONS["mlops-03-serve"]))
