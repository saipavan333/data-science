# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "MLOps questions are how interviewers find out whether you've actually **shipped** a model or only "
 "trained one in a notebook. They probe the unglamorous realities &mdash; skew, versioning, latency, "
 "drift &mdash; that decide whether ML creates value or quietly breaks. Strong answers here mark you "
 "as someone who can be trusted with a model that touches real users and real money."))
p.append(B.h2("Say these out loud", kicker="Rapid-fire drill"))
p.append(B.interview_check([
 "Walk me through the **ML lifecycle** &mdash; and why it's a loop, not a line.",
 "What is **training&ndash;serving skew**, and how do you prevent it?",
 "**Batch vs. online** serving &mdash; how do you decide which a problem needs?",
 "How do you **version** a model &mdash; and why isn't versioning code enough?",
 "Why is it dangerous to judge serving latency by the **mean**?",
 "Your model was great at launch and is worse now, with no code changes. **Why?**",
 "Explain **data drift vs. concept drift** with an example of each.",
 "Why monitor **input distributions** and not just accuracy?",
 "A drift alarm fires &mdash; do you retrain immediately? Walk me through it.",
 "How would you **roll out** a retrained model safely?",
], title="The MLOps drill")
)
p.append(B.practice([
 {"q":"CASE: \"We trained a great recommendation model. How do you get it in front of users and keep "
      "it working?\" Give an end-to-end answer.",
  "sol":"**Ship:** package the **whole pipeline** (preprocessing + model) as one artifact to avoid "
        "**training&ndash;serving skew**; **version** it in a registry with its data/params/"
        "environment. Decide **serving pattern** &mdash; if recommendations can be precomputed, run a "
        "**batch** job and serve from a lookup table (cheap, fast); if they need live context, stand "
        "up a **containerized API** behind autoscaling and watch **p95/p99** latency. **Roll out "
        "safely** with **shadow/canary** and ideally an **A/B test** measuring the real engagement "
        "metric, not just offline accuracy. **Keep it working:** monitor three layers &mdash; "
        "operational health, **input drift** (early, label-free), and performance once labels arrive "
        "&mdash; with alerts wired to a **retraining** path. The through-line: a model is a **living "
        "system** (code + data + environment) that must be packaged skew-free, versioned, served "
        "within a latency budget, released reversibly, and monitored so decay is caught and fixed."},
 {"q":"CASE: \"Our production model's accuracy dropped from 88% to 79% over three months. Diagnose "
      "and fix.\" How do you proceed?",
  "sol":"**Diagnose before acting.** First rule out **operational/pipeline** causes: did a feature "
        "start arriving in different units, a join break, a column go null, or the preprocessing "
        "diverge from training (**skew**)? These masquerade as 'accuracy drops' and must be *fixed*, "
        "not retrained around. If the plumbing is clean, check **drift**: compare recent **input "
        "distributions** to training (standardized shift / PSI) to spot **data drift**, and examine "
        "whether the **input&rarr;target relationship** changed (**concept drift**) &mdash; e.g. a "
        "new customer segment or an external shock. **Fix:** if it's genuine drift, **retrain** on "
        "recent, representative data, **validate** the new model against the current one, and roll it "
        "out via **shadow/canary** so a bad retrain can't make things worse. Then **institutionalise** "
        "it: add the drift monitor and alert that would have caught this at, say, 85% instead of 79%, "
        "and set a retraining cadence. The senior signal is *diagnose the cause* (bug vs. drift) "
        "before reaching for the retrain button."},
]))
p.append(B.callout("note","The through-line of the whole track",
 "MLOps is the discipline that turns a model into a **product**. A model is **code + data + "
 "environment**: package it so preprocessing can't drift between training and serving, version all "
 "three so you can reproduce and roll back, serve it at the latency the use case needs, and &mdash; "
 "above all &mdash; **monitor it**, because it decays even when you don't touch it. Research asks "
 "*\"is the model good?\"*; MLOps asks *\"will it still be good, in production, next month?\"* &mdash; "
 "and that's the question the business is really paying for.", "&#9670;"))
LESSONS={"mlops-05-interview":"\n".join(p)}
print("content_mlops05 OK — chars:", len(LESSONS["mlops-05-interview"]))
