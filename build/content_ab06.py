# -*- coding: utf-8 -*-
import builder as B
p=[]

p.append(B.why(
 "At product companies &mdash; the ones that hire the most data scientists &mdash; the interview is "
 "**not** \"derive the t-test.\" It's *\"we're thinking of shipping X. How would you test it, and "
 "how would you know if it worked?\"* This is the **product-sense + experimentation case**, and it's "
 "where most candidates fall apart: not because they don't know statistics, but because they have no "
 "**framework**. This lesson gives you two frameworks and drills them on real cases, so you walk in "
 "with a structure instead of a blank page."))

p.append(B.h2("Framework 1 — \"Design an experiment for feature X\"", kicker="The case you WILL get"))
p.append(B.concept(
 "When they say *\"design an experiment,\"* don't start listing statistics. Walk the **DESIGN** arc "
 "out loud &mdash; it shows product judgement *and* rigour, in order:\n\n"
 "- **Goal & hypothesis** &mdash; what's the business goal, and what's your falsifiable hypothesis? "
 "*\"Bigger 'Buy' buttons increase purchases because they reduce friction.\"* State the direction.\n"
 "- **Metric** &mdash; pick **one primary** metric that captures the goal (e.g. purchase rate per "
 "visitor), plus 2&ndash;3 **guardrails** you refuse to harm (revenue, latency, refund rate).\n"
 "- **Unit & randomization** &mdash; randomize by **user** (not session &mdash; a user must get a "
 "consistent experience), 50/50, logged at first exposure.\n"
 "- **Size & duration** &mdash; a **power analysis** from the baseline rate and the **minimum "
 "detectable effect** the business cares about; run &ge; 1&ndash;2 full weeks to cover weekly "
 "seasonality and let novelty fade.\n"
 "- **Trust checks** &mdash; SRM (is the split really 50/50?), an A/A sanity check, instrumentation "
 "validation *before* reading results.\n"
 "- **Decision rule, set in advance** &mdash; ship if the primary metric is significant, positive, "
 "past the MDE, **and** no guardrail is hurt; otherwise iterate or kill. Decide the rule *before* "
 "you see the data.\n\n"
 "That's the whole answer skeleton. Everything else is detail you hang on these six pegs."))

p.append(B.deepdive(
 B.concept(
  "**Worked case: \"We want to add one-tap checkout. Design the experiment.\"**\n\n"
  "*\"**Goal**: lift completed purchases without hurting revenue quality. **Hypothesis**: one-tap "
  "reduces checkout abandonment, so purchase-per-visitor rises. **Primary metric**: completed "
  "purchases &divide; visitors in the checkout flow. **Guardrails**: revenue per visitor (a cheaper "
  "faster path could lower basket size), refund/chargeback rate (impulse buys), and error/latency "
  "rate. **Unit**: randomize by user, 50/50, assigned on entering checkout. **Size**: baseline "
  "purchase rate ~20%, we care about a +1pp absolute lift &rarr; power analysis gives ~N per arm; "
  "run two full weeks minimum. **Trust**: SRM check, confirm event logging on both arms with an A/A "
  "pre-test. **Decision**: ship only if purchase rate is significantly up by &ge;1pp AND revenue per "
  "visitor and refund rate are not down. If purchases rise but revenue/visitor falls, that's a "
  "**tradeoff to escalate**, not an automatic ship.\"*\n\n"
  "Notice what earns the offer: naming the **guardrail** that could quietly break (revenue quality), "
  "and refusing to call a purchase-rate win a win if it cannibalises revenue. That's senior "
  "judgement."),
 title="Worked case — one-tap checkout, narrated the way you'd say it"))

p.append(B.h2("Framework 2 — \"The test is flat (or negative). What now?\"", kicker="The follow-up that filters"))
p.append(B.concept(
 "The interviewer's favourite curveball. A weak candidate says \"then the feature doesn't work.\" A "
 "strong one runs a **diagnostic tree** &mdash; because \"flat\" has many causes, and only some mean "
 "\"the idea is bad\":\n\n"
 "- **Is the result trustworthy?** First suspect the *instrument*, not the idea (Twyman's law). "
 "Check **SRM**, event logging, and that users actually *received* the treatment (did the feature "
 "even render?). A flat result is often a **broken experiment**.\n"
 "- **Was it powered?** A flat p-value with a **wide** confidence interval means *\"we learned "
 "nothing,\"* not *\"no effect.\"* If the CI still contains effects you'd care about, you were "
 "**underpowered** &mdash; run longer / bigger, don't conclude.\n"
 "- **Is it flat *overall* but moving in *segments*?** Maybe it helps new users and hurts power "
 "users (they cancel out). Pre-registered segment analysis can reveal a **targeted** ship. (Beware "
 "post-hoc slicing &mdash; treat surprises as hypotheses.)\n"
 "- **Is it novelty wearing off, or primacy still fading?** Look at the effect **over time**. A "
 "day-one spike decaying to zero, or an early dip recovering, both masquerade as \"flat.\"\n"
 "- **Did it hit a guardrail?** \"Flat primary, but latency guardrail tripped\" is a **kill**, not a "
 "flat.\n\n"
 "The meta-point: *a null result is information*. The job is to figure out **which** kind of null it "
 "is, then decide: **iterate** (the idea's ok, execution off), **kill** (well-powered true null or "
 "guardrail hit), or **keep looking** (underpowered)."))

p.append(B.deepdive(
 B.concept(
  "**Worked case: \"Your redesign test came back flat after a week. Walk me through it.\"**\n\n"
  "*\"First I'd distrust it. **SRM check** &mdash; is the traffic split actually 50/50? Then confirm "
  "the redesign **rendered** for the treatment arm and events fired (a flat result is often a "
  "logging bug). If the plumbing's clean, I look at **power**: one week may not have reached the "
  "planned sample size, and if the **confidence interval** still spans, say, &minus;1% to +3%, we "
  "genuinely can't conclude &mdash; I'd let it run to the pre-set size. I'd check the effect **over "
  "time** for novelty/primacy, and look at **pre-registered segments** &mdash; new vs returning "
  "users &mdash; in case a real effect in one group is being cancelled by another. Only after all "
  "that, if it's well-powered, the CI is tight around zero, and segments agree, I'd conclude **no "
  "meaningful effect** and recommend we iterate on the hypothesis rather than ship.\"*\n\n"
  "The signal: you treated \"flat\" as a **diagnosis problem**, suspected the instrument first, and "
  "distinguished *\"no effect\"* from *\"no information.\"* That's exactly the judgement the question "
  "is probing for."),
 title="Worked case — the flat redesign, diagnosed"))

p.append(B.h2("Rapid-fire — say these out loud", kicker="Drill"))
p.append(B.interview_check([
 "\"Design an experiment for &lt;feature&gt;\" &mdash; walk the DESIGN arc: goal/hypothesis &rarr; "
 "metric + guardrails &rarr; unit &rarr; size/duration &rarr; trust checks &rarr; decision rule.",
 "Why randomize by **user** and not by session?",
 "What's a **guardrail metric**, and can you give one for a checkout test?",
 "The test is **flat** &mdash; give me three different things that could mean.",
 "How do you pick the **primary metric**, and why only one?",
 "What is **SRM** and why is it the first thing you check?",
 "You got a **+30%** lift on day one &mdash; do you ship? (Twyman's law / novelty)",
 "Primary metric is up but a **guardrail** is down &mdash; what do you do?",
 "How long should a test run, and why not stop as soon as it's significant?",
 "When can you **not** run an A/B test, and what do you do instead? (ethics, network effects, rare "
 "events &rarr; quasi-experiments)",
], title="The A/B + product-sense drill")
)

p.append(B.practice([
 {"q":"CASE: \"Netflix wants to test a new personalized-artwork feature for movie thumbnails. Design "
      "the experiment.\" Give a full structured answer.",
  "sol":"**Goal/hypothesis**: personalized artwork increases engagement because more relevant "
        "thumbnails drive clicks &rarr; plays. **Primary metric**: something like *hours "
        "streamed per subscriber* (or plays per session) &mdash; the thing the business actually "
        "values, not just clicks (a clickbait thumbnail could raise clicks but lower satisfaction). "
        "**Guardrails**: completion rate / early-stops (did they click and immediately quit?), "
        "customer complaints, and infra latency for generating artwork. **Unit**: randomize by "
        "**subscriber**, 50/50, so a person sees a consistent experience across sessions and devices. "
        "**Size/duration**: power analysis from baseline streaming hours and the MDE product cares "
        "about; run &ge;2 weeks to cover the weekly cycle and let novelty fade. **Trust**: SRM, "
        "confirm artwork actually served, A/A pre-test. **Decision**: ship if streaming hours are "
        "significantly up past the MDE with no drop in completion rate or spike in complaints. "
        "**Nuance to voice**: guard against optimizing a **proxy** (clicks) at the expense of the "
        "**true goal** (satisfying streaming) &mdash; that's the trap this case is testing."},
 {"q":"CASE: \"We shipped a test, it was significant and positive, we launched to 100% &mdash; and a "
      "month later the metric is back to baseline. What happened and what should we have done?\"",
  "sol":"**What happened (likely):** a **novelty effect** &mdash; the lift was users reacting to "
        "something *new*, and it decayed as the novelty wore off. Other candidates: **primacy in "
        "reverse** (an early over-performance), **seasonality** (the test window coincided with a "
        "high period), the **winner's curse** (we shipped precisely because we got a lucky-high "
        "estimate, which then regressed), or an **external change** (a competitor, a holiday ending) "
        "confounded with the launch. **What we should have done:** (1) run the test **long enough** "
        "for the effect curve to flatten before trusting it; (2) look at the effect for users on "
        "their *n-th* exposure, not just first; (3) keep a small **long-term holdback** &mdash; a "
        "slice of users left on the old experience &mdash; so we can measure the *durable* cumulative "
        "effect after launch; (4) treat a surprisingly large win with **Twyman's-law** suspicion and "
        "replicate important launches. The holdback is the key senior move: it turns \"did it last?\" "
        "from a guess into a measurement."},
]))

p.append(B.callout("note","The through-line of the whole track",
 "Experimentation interviews reward **structure and judgement** over formulas. Have a framework for "
 "*designing* a test (goal &rarr; metric + guardrails &rarr; unit &rarr; power &rarr; trust &rarr; "
 "decision) and a framework for *interpreting* one (trust it? powered? segments? time? guardrails?). "
 "Name the guardrail that could quietly break, distinguish a **proxy** from the **true goal**, and "
 "treat a null as information. Do that and you'll out-answer people who know more statistics than "
 "you.", "&#9670;"))

LESSONS={"ab-06-interview":"\n".join(p)}
print("content_ab06 OK — chars:", len(LESSONS["ab-06-interview"]))
