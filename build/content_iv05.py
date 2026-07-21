# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "The case round is where technical candidates most often stumble &mdash; not because they lack "
 "skill, but because the question is **open-ended** and they have no structure. *\"How would you "
 "measure the success of Stories?\"* *\"DAU dropped 8% &mdash; what happened?\"* *\"How many piano "
 "tuners are in Chicago?\"* These test whether you can turn business ambiguity into a **structured "
 "analysis**. Frameworks are your friend: they keep you calm, organised, and impossible to fluster."))
p.append(B.h2("The four case archetypes", kicker="Recognise, then apply a framework"))
p.append(B.concept(
 "Most product/case questions are one of four types, each with a go-to structure:\n\n"
 "- **Metric design** &mdash; *\"how would you measure success of X?\"* Frame: **goal &rarr; a "
 "single primary metric that captures it &rarr; guardrails &rarr; how you'd track it.**\n"
 "- **Metric diagnosis** &mdash; *\"metric Y dropped, why?\"* Frame: **is it real? (bug/logging) "
 "&rarr; segment it (where's the drop concentrated?) &rarr; internal vs external causes &rarr; "
 "hypothesize and check.**\n"
 "- **Experiment design** &mdash; *\"how would you test feature Z?\"* Frame: the DESIGN arc from "
 "Track 6 (hypothesis &rarr; metric + guardrails &rarr; unit &rarr; power &rarr; decision).\n"
 "- **Estimation / guesstimate** &mdash; *\"how big is market M?\"* Frame: **state assumptions "
 "&rarr; decompose into factors you can estimate &rarr; multiply &rarr; sanity-check.**"))
p.append(B.h2("Say the frameworks out loud", kicker="Rapid-fire"))
p.append(B.interview_check([
 "How would you measure the **success of a new feature** (e.g. Stories, a 'Save' button)?",
 "**Daily active users dropped 8% overnight** &mdash; walk me through diagnosing it.",
 "Pick a **north-star metric** for a ride-sharing app / marketplace / SaaS product.",
 "How would you decide whether to **launch feature X**? (experiment design)",
 "**Estimate** the number of ride requests in a city per day.",
 "A metric is up but the business feels worse &mdash; what's happening? (**proxy vs. true goal**)",
 "How would you detect and measure **cannibalization** between two products?",
 "What's the difference between a **north-star metric** and a **guardrail**?",
], title="The case / product-sense drill")
)
p.append(B.h2("Worked framework — diagnosing a metric drop", kicker="The most common case"))
p.append(B.concept(
 "*\"Daily active users fell 8% yesterday.\"* Resist guessing. Structure it:\n\n"
 "- **Is it real?** First suspect the **instrument**: a logging bug, a failed data pipeline, a "
 "tracking change, a redefinition. A shocking drop is often a measurement artifact (Twyman's law).\n"
 "- **Segment it.** *Where* is the drop concentrated &mdash; a platform (iOS vs Android), a region, "
 "an app version, new vs returning users? A drop isolated to one segment points straight at a "
 "cause (a broken release, an outage in one region).\n"
 "- **Internal vs external.** Internal: a bad deploy, a changed flow, a pricing change. External: a "
 "competitor, a holiday, seasonality, a news event, an app-store issue.\n"
 "- **Timing.** Sudden cliff &rarr; a specific event (deploy, outage). Gradual slide &rarr; a trend "
 "(drift, competition).\n\n"
 "You end with a **prioritized hypothesis** and how you'd confirm it &mdash; not a wild guess. The "
 "structure *is* the answer."))
p.append(B.tip(
 "In every case, **think out loud and state assumptions**. *\"I'll assume this is a consumer social "
 "app and we care about engagement, not revenue &mdash; tell me if that's wrong.\"* This lets the "
 "interviewer steer you, shows judgement, and buys thinking time. A structured wrong turn you can "
 "correct beats a confident leap to the wrong problem."))
p.append(B.h2("Worked framework — a guesstimate", kicker="Decompose, don't guess"))
p.append(B.concept(
 "*\"How many rides does a ride-share app do daily in a city of 5 million?\"* Never blurt a number "
 "&mdash; **decompose**: *\"Of 5M people, maybe 60% are adults with the app-owning demographic "
 "&asymp; 3M. Perhaps 10% are active users &asymp; 300k. An active user rides, say, 3&times;/week "
 "&asymp; 0.43/day &rarr; ~130k rides/day. Sanity check: that's ~1 ride per 40 people daily, which "
 "feels plausible for a mid-size market.\"* The **number doesn't matter** &mdash; interviewers grade "
 "your **decomposition, assumptions, and arithmetic**. State each assumption so they can adjust it, "
 "and always end with a sanity check."))
p.append(B.keypoints([
 "Case questions are **open-ended by design** &mdash; recognise the archetype (**metric design, "
 "diagnosis, experiment, estimation**) and apply its framework.",
 "**Metric design**: goal &rarr; one primary metric &rarr; guardrails. **Diagnosis**: is-it-real "
 "&rarr; segment &rarr; internal/external &rarr; hypothesize.",
 "**Guesstimates**: state assumptions &rarr; decompose &rarr; multiply &rarr; sanity-check &mdash; "
 "the *number* doesn't matter, the *structure* does.",
 "**Clarify and state assumptions** out loud so the interviewer can steer you &mdash; solving the "
 "wrong problem confidently is the top failure.",
 "Beware **proxy vs. true goal** (winning clicks while losing satisfaction) &mdash; name the "
 "guardrail that protects the real objective.",
]))
p.append(B.quiz([
 {"q":"\"Signups dropped 20% this week.\" What's the best first step?",
  "options":[
   {"t":"Check whether it's real — tracking/logging bug, a redefinition, or a pipeline failure — "
        "before hunting for business causes","correct":True,
    "why":"Correct. A large sudden drop is frequently a measurement artifact. Verify the instrument "
          "(logging, pipeline, metric definition) first (Twyman's law), then segment to localise a "
          "real cause. Guessing a business reason first wastes the analysis."},
   {"t":"Immediately blame the latest marketing campaign",
    "why":"Jumping to one cause skips verification and segmentation. First confirm the drop is real, "
          "then localise it with data."},
   {"t":"Launch a new campaign to boost numbers",
    "why":"Acting before diagnosing risks masking or worsening the real issue. Diagnose "
          "structurally first."},
   {"t":"Wait a week to see if it recovers",
    "why":"Passive waiting forfeits the chance to catch a bug or a fixable cause. Investigate "
          "structurally now."}]},
 {"q":"You're asked to estimate a market size. What matters most to the interviewer?",
  "options":[
   {"t":"A clear decomposition with stated assumptions and a sanity check — not the exact final "
        "number","correct":True,
    "why":"Correct. Guesstimates test structured reasoning: how you break the problem into estimable "
          "factors, make explicit assumptions, and sanity-check the result. The precise number is "
          "unknowable and not the point."},
   {"t":"Getting the exact right number",
    "why":"There's no 'exact' answer they're checking against &mdash; they grade the reasoning, "
          "assumptions, and arithmetic, not a precise figure."},
   {"t":"Answering as fast as possible",
    "why":"Speed over structure leads to unjustifiable guesses. A clear, assumption-driven "
          "decomposition is what scores."},
   {"t":"Using a memorized statistic",
    "why":"They want to see you *build* the estimate from stated assumptions, not recite a number you "
          "can't derive."}]},
]))
p.append(B.practice([
 {"q":"\"How would you measure the success of a new 'Save for later' button on an e-commerce app?\" "
      "Give a structured answer.",
  "sol":"**Clarify the goal first:** is the button meant to drive *eventual purchases*, increase "
        "*engagement/return visits*, or reduce *decision friction*? Assume the goal is **more "
        "purchases via saved items**. **Primary metric:** conversion rate of saved items (or "
        "incremental purchases attributable to saving) &mdash; the outcome that maps to the goal, not "
        "just 'number of saves' (a vanity/usage metric). **Secondary/engagement:** save rate, return "
        "visits to the saved list, time-to-purchase. **Guardrails (must not harm):** overall "
        "conversion and revenue per visitor (saving could *delay* or *replace* a purchase &mdash; "
        "cannibalization risk), cart-abandonment, and latency. **How I'd validate:** run an **A/B "
        "test** exposing the button to a random half, and measure whether *purchases* rise without "
        "hurting the guardrails &mdash; because a feature people *use* (high save rate) isn't a "
        "success unless it moves the real goal. The key judgement on display: distinguishing a "
        "**usage/proxy** metric (saves) from the **true objective** (purchases), and protecting "
        "against cannibalization with a guardrail."},
]))
LESSONS={"iv-05-case":"\n".join(p)}
print("content_iv05 OK — chars:", len(LESSONS["iv-05-case"]))
