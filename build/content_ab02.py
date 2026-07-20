# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Most failed A/B tests don't fail in the analysis &mdash; they fail in the **design**, before a "
 "single user is bucketed. Pick a vanity metric, randomize the wrong unit, forget a guardrail, or "
 "skip the sanity checks, and no amount of clever statistics can rescue the result. This lesson is "
 "the pre-flight checklist a good experimenter runs *before* launching, so the number you get at the "
 "end actually means something."))

p.append(B.h2("The shape of an experiment", kicker="Concept"))
p.append(B.concept(
 "Every A/B test has the same skeleton: take eligible users, split them randomly, show each group a "
 "different version, measure the **same** metric for both, and compare &mdash; while watching that "
 "you didn't break anything else:"))
p.append(B.figure(IMG+"s_ab_design.png",
 "**The anatomy of an A/B test.** A random 50/50 split creates two comparable groups; control sees "
 "the current version, treatment sees the new one; you measure one **primary metric** for both and "
 "watch **guardrail metrics** so a win on one thing doesn't quietly break another.",
 "A flow: users randomly split 50/50 into control and treatment, each measured on the same primary metric plus guardrails."))
p.append(B.concept(
 "Designing one well comes down to four decisions, each a place people go wrong: the **primary "
 "metric**, the **hypothesis** (and how big an effect you care about), the **unit of "
 "randomization**, and the **guardrails**. Take them in turn."))

p.append(B.h2("1. One primary metric — chosen before you look", kicker="Concept")
)
p.append(B.concept(
 "Commit to a **single** ~primary metric~ that captures the change's goal, and write it down "
 "*before* the test. Why one? Because if you measure twenty metrics and celebrate whichever moved, "
 "you'll fool yourself with noise (that's the multiple-comparisons trap of Lesson 6.5). A good "
 "primary metric is ~sensitive~ (it can actually move in a two-week test), ~aligned~ with the real "
 "objective (not a ~vanity metric~ like raw pageviews), and ~measurable~ per user. \"Clicks\" is "
 "often a vanity metric; \"completed purchases per user\" is usually what you actually want. The one "
 "north-star metric a company optimizes across experiments is sometimes called the ~OEC~ &mdash; "
 "overall evaluation criterion."))

p.append(B.h2("2. Randomize the right unit", kicker="Concept · the subtle one")
)
p.append(B.pitfall(
 "The ~unit of randomization~ is *what* you flip the coin on &mdash; usually the **user**, not the "
 "session or the pageview. Randomize by pageview and the same person can see version A on one screen "
 "and B on the next: inconsistent, confusing, and it ~contaminates~ the comparison because a user "
 "experiences both arms. Randomize by **user** (a stable id) so each person consistently gets one "
 "version. Watch for ~interference~ too: in a social network or marketplace, treating one user can "
 "spill over onto their friends (control users see treated users' posts), breaking the assumption "
 "that the groups are independent."))

p.append(B.h2("3 & 4. Guardrails, and the sanity check that catches broken tests", kicker="Concept")
)
p.append(B.concept(
 "~Guardrail metrics~ are the things you must **not** harm while chasing the primary: page-load "
 "latency, revenue, error rate, unsubscribes. A checkout redesign that lifts conversions but tanks "
 "revenue-per-user is a loss, not a win &mdash; guardrails catch that.\n\n"
 "Then, before you trust *any* result, run the ~sample ratio mismatch~ (SRM) check. You intended a "
 "50/50 split; if the counts come back materially off &mdash; say 52/48 on a large test &mdash; your "
 "randomization or logging is **broken**, and the whole experiment is untrustworthy. A chi-square "
 "test flags it: if the split's p-value is tiny, stop and debug before reading the metric:"))
_c,_o=_run(r'''
from scipy import stats

# you intended a 50/50 split — here are the actual user counts that landed in each arm
control, treatment = 10342, 9871
total = control + treatment

result = stats.chisquare([control, treatment], [total/2, total/2])
print(f"observed split : {control} / {treatment}   ({control/total:.1%} / {treatment/total:.1%})")
print(f"SRM p-value    : {result.pvalue:.5f}")
print("rule: p < 0.001  ->  randomization is broken, do NOT trust the experiment")
''')
p.append(B.code_example(_c,_o,filename="sample_ratio_mismatch.py"))
p.append(B.concept(
 "A 51.2 / 48.8 split *feels* close, but on 20,000 users the SRM p-value is tiny &mdash; far too "
 "lopsided to be chance. Something is wrong (a broken redirect, a logging bug, bots landing in one "
 "arm), and any \"win\" here is an artifact. **SRM is the first thing a seasoned analyst checks**, "
 "before even glancing at the primary metric."))

p.append(B.h2("Your turn — run the SRM check", kicker="Interactive lab"))
p.append(B.pylab(
 "An experiment intended a 50/50 split but observed **`control = 8210`** and **`treatment = 7954`** "
 "users. Run a chi-square sample-ratio-mismatch check (`scipy.stats.chisquare` against equal "
 "expected counts) and assign the **p-value** to **`answer`**, rounded to 4 decimals. Then judge: is "
 "this experiment trustworthy?",
 "from scipy import stats\n"
 "control, treatment = 8210, 7954\n"
 "total = control + treatment\n",
 "answer = round(float(stats.chisquare([control, treatment], [total/2, total/2]).pvalue), 4)",
 starter="# control, treatment, total are loaded; scipy.stats is imported as stats\nanswer = ",
 hint="`stats.chisquare([control, treatment], [total/2, total/2]).pvalue`, wrapped in "
      "`round(float(...), 4)`. A p below ~0.001 means the split is broken.",
 title="Lab — is the split broken?",
 preview="`control`, `treatment`, `total` loaded; `scipy.stats` imported. First Run loads scipy (~15s).",
 explain="If the SRM p-value is tiny, the randomization failed and you must fix the pipeline before "
         "trusting any metric &mdash; it's the experiment's smoke alarm."))

p.append(B.keypoints([
 "Design decides success: pick the **primary metric**, **hypothesis/MDE**, **randomization unit**, "
 "and **guardrails** before launch.",
 "Choose **one** ~primary metric~ up front &mdash; sensitive, aligned with the goal, not a ~vanity "
 "metric~. (Multiple metrics &rarr; multiple-comparisons noise.)",
 "Randomize by **user** (a stable id), not by session/pageview, or a user sees both versions and "
 "~contaminates~ the test; beware ~interference~/spillover.",
 "~Guardrail metrics~ (latency, revenue, errors) ensure a primary-metric win doesn't break something "
 "else.",
 "Always run the ~sample ratio mismatch~ (SRM) check first &mdash; a split far from intended means "
 "the experiment is **broken**, not a result.",
]))

p.append(B.quiz([
 {"q":"Why randomize by user rather than by pageview?",
  "options":[
   {"t":"So each person consistently sees one version; per-pageview flipping shows the same user both "
        "arms, contaminating the comparison","correct":True,
    "why":"Correct. Randomizing per pageview lets one user experience both A and B, which is "
          "inconsistent UX and breaks the clean between-groups comparison. A stable user id keeps each "
          "person in one arm."},
   {"t":"Because pageviews can't be counted",
    "why":"Pageviews are countable; the issue is that per-pageview assignment splits a single user "
          "across both arms, contaminating the test."},
   {"t":"To get a bigger sample",
    "why":"Pageviews would give *more* units, not fewer — but at the cost of contamination. The reason "
          "is consistency, not size."},
   {"t":"It removes the need for a control group",
    "why":"You still need a control group either way. The unit choice is about keeping each user in "
          "one consistent arm."}]},
 {"q":"Your A/B test intended 50/50 but shows a 51.5 / 48.5 split over 40,000 users, SRM p < 0.0001. "
      "What do you do?",
  "options":[
   {"t":"Stop and debug the randomization/logging before trusting any metric — the experiment is "
        "broken","correct":True,
    "why":"Correct. A tiny SRM p-value means the split is too lopsided to be chance, so assignment or "
          "logging is faulty. Any 'result' is an artifact until you find and fix the cause."},
   {"t":"Ignore it — 51.5% is basically 50%",
    "why":"On 40,000 users, 51.5% is far from 50% by chance (hence p < 0.0001). 'Looks close' is "
          "exactly the intuition SRM exists to override."},
   {"t":"Declare the winner faster since one group is bigger",
    "why":"A broken split invalidates the comparison; you can't declare anything until it's fixed."},
   {"t":"Add more users to fix the ratio",
    "why":"More users won't fix a systematic assignment bug; it just accumulates more corrupted data. "
          "Find the cause first."}]},
 {"q":"Which is the best primary metric for a checkout-redesign experiment?",
  "options":[
   {"t":"Completed purchases per user — it directly reflects the goal and is measurable per user","correct":True,
    "why":"Correct. It's aligned with what the redesign is *for* (buying), sensitive, and defined per "
          "randomization unit. A good primary metric captures the real objective."},
   {"t":"Total pageviews",
    "why":"A classic vanity metric — it can rise while purchases fall (more confusion = more clicks). "
          "It isn't aligned with the checkout goal."},
   {"t":"Every metric you can log, and celebrate whichever moves",
    "why":"That's the multiple-comparisons trap: with enough metrics something moves by chance. Commit "
          "to one primary metric up front."},
   {"t":"Time spent on the checkout page",
    "why":"Ambiguous — more time could mean engagement or confusion. It doesn't cleanly capture the "
          "objective the way completed purchases do."}]},
]))

p.append(B.practice([
 {"q":"A team wants to test a new recommendation carousel. They propose measuring clicks, scroll "
      "depth, time-on-page, add-to-carts, and purchases, and calling it a win if *any* improve. "
      "Critique the design.",
  "sol":"Two problems. First, testing five metrics and declaring victory if **any** moves is a "
        "**multiple-comparisons** trap &mdash; with five noisy metrics, one often crosses "
        "significance by pure chance, so 'a win' is likely a false positive. Commit to **one primary "
        "metric** up front (probably **purchases** or **add-to-carts per user**, whichever the "
        "carousel is really for). Second, the others should be kept as **secondary/guardrail** "
        "metrics for context, not as alternative ways to win. Decide the success criterion before "
        "seeing the data."},
 {"q":"In a two-sided marketplace, you A/B test a change for **buyers**. Why might randomizing buyers "
      "independently still violate the experiment's assumptions?",
  "sol":"~Interference~ (spillover). Buyers share a common pool of **sellers/inventory**, so treating "
        "some buyers can change the marketplace for the control buyers too &mdash; e.g., treated "
        "buyers snap up limited inventory, leaving control buyers worse off (or vice versa). That "
        "breaks the assumption that the control group is unaffected by the treatment, biasing the "
        "measured effect. Marketplaces often need **cluster-level** randomization (by region, or by "
        "seller) to contain the spillover."},
]))

p.append(B.deepdive(
 B.concept(
  "**Sensitivity and the metric's variance.** A metric you *can't move detectably* in a reasonable "
  "test is useless, no matter how meaningful. Revenue-per-user is noisy (a few big spenders dominate), "
  "so it often needs a huge sample; a ~proportion~ like conversion rate is far more sensitive. "
  "Practitioners sometimes use **variance-reduction** tricks (like ~CUPED~, which adjusts the metric "
  "using pre-experiment data) to detect smaller effects with the same users &mdash; a real edge when "
  "traffic is limited.") +
 B.concept(
  "**Novelty and primacy effects.** A shiny new feature can get a temporary bump *just because it's "
  "new* (users click it out of curiosity) &mdash; the ~novelty effect~ &mdash; which fades. "
  "Conversely, users annoyed by change can dip at first, then recover (~primacy~). Both mean an "
  "experiment that's too short can mis-measure the *steady-state* effect. Guard against it by running "
  "long enough to see the curve flatten, and by checking whether the effect holds for users seeing it "
  "for the first time vs. repeatedly.") +
 B.concept(
  "**Guardrails as a decision framework.** Mature experimentation treats the decision as: *ship if the "
  "primary metric improves significantly **and** no guardrail degrades beyond a set threshold.* This "
  "turns \"is it good?\" into an explicit, pre-registered rule &mdash; primary win + guardrail "
  "protection &mdash; which stops teams from cherry-picking a favourable metric after the fact. "
  "Writing that rule **before** the test is what makes the eventual decision honest."),
 title="Deep dive: metric sensitivity & CUPED, novelty/primacy, and guardrail decision rules"))

p.append(B.callout("note","Interview-ready",
 "Design questions are the heart of the product-DS interview. Nail: **one** primary metric (sensitive, "
 "aligned, not vanity) chosen up front; randomize by **user** to avoid contamination; **guardrail** "
 "metrics so a win doesn't break revenue/latency; and **check SRM first** &mdash; a split far from "
 "intended means the test is broken. Bonus: name interference/spillover in marketplaces and "
 "novelty effects.", "&#9670;"))

LESSONS={"ab-02-design":"\n".join(p)}
print("content_ab02 OK — chars:", len(LESSONS["ab-02-design"]))
