# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Almost every big product decision comes down to one question: *\"if we ship this change, will the "
 "metric actually go up &mdash; **because** of the change?\"* Correlation can't answer that, because "
 "the users who happen to see a feature are rarely comparable to those who don't. The ~randomized "
 "experiment~ &mdash; the ~A/B test~ &mdash; is the closest thing we have to a truth machine: it is "
 "how Netflix, Amazon, and every serious tech company decide what to build. This track makes you "
 "fluent in running and reading them, and it's one of the most-tested skills in product data-science "
 "interviews."))

p.append(B.h2("Correlation can't tell you 'because'", kicker="Concept"))
p.append(B.concept(
 "You already met this in the statistics track: ~correlation is not causation~. The reason is "
 "~confounding~ &mdash; a lurking third variable that drives **both** things you're comparing. Ice "
 "cream sales and drownings rise together, but neither causes the other; summer heat drives both:"))
p.append(B.figure(IMG+"s11_confounder.png",
 "**A confounder creates a fake link.** Summer heat pushes up *both* ice-cream sales and drownings, "
 "so they move together without either causing the other. In product terms: your most engaged users "
 "self-select into trying a new feature, so the feature *looks* great even if it does nothing.",
 "A causal diagram: summer heat causes both ice-cream sales and drownings, which are correlated but not causal."))
p.append(B.concept(
 "This is the trap with **observational** data. Say you compare users who used a new feature against "
 "those who didn't, and the feature-users have higher retention. Did the feature cause it? Probably "
 "not &mdash; the kind of person who tries new features was **already** more engaged. That "
 "~selection bias~ is a confounder, and it wrecks naive comparisons."))

p.append(B.h2("Randomization: the truth machine", kicker="Concept · the whole idea")
)
p.append(B.concept(
 "Here's the magic. If you **randomly** assign each user to see version A (control) or version B "
 "(treatment), then &mdash; on average &mdash; the two groups are **identical in every way**, "
 "measured or not: same engagement mix, same age, same everything, because the coin flip doesn't "
 "care. So the *only* systematic difference between the groups is the change you made. Any gap in "
 "the metric can now be attributed to that change. Randomization doesn't remove confounders one by "
 "one &mdash; it **balances all of them at once**, including the ones you never thought to measure. "
 "That is why the randomized experiment is the gold standard for causality. Watch it work:"))
_c,_o=_run(r'''
import numpy as np
rng = np.random.default_rng(0)
n = 5000
# every user has hidden "engagement" that affects BOTH their behaviour and the outcome (a confounder)
engagement = rng.normal(0, 1, n)
true_effect = 0.10   # the change really adds only +0.10

# OBSERVATIONAL: engaged users self-select into using the new feature
chose = (engagement + rng.normal(0, 0.5, n) > 0.5).astype(int)
outcome_obs = 2*engagement + true_effect*chose + rng.normal(0, 1, n)
naive = outcome_obs[chose == 1].mean() - outcome_obs[chose == 0].mean()

# RANDOMIZED: assign by coin flip, independent of engagement
assigned = rng.integers(0, 2, n)
outcome_rct = 2*engagement + true_effect*assigned + rng.normal(0, 1, n)
experiment = outcome_rct[assigned == 1].mean() - outcome_rct[assigned == 0].mean()

print(f"true effect of the change      : +{true_effect:.2f}")
print(f"naive observational comparison : {naive:+.2f}   <- confounding makes it look huge")
print(f"randomized A/B estimate        : {experiment:+.2f}   <- recovers the truth")
''')
p.append(B.code_example(_c,_o,filename="randomization.py"))
p.append(B.concept(
 "The naive comparison is wildly wrong &mdash; it credits the feature with a huge effect that's "
 "really just engaged users being engaged. The randomized estimate lands right on the true +0.10. "
 "**Same data-generating world, opposite conclusions** &mdash; and the only difference is whether "
 "assignment was random. This is the entire reason A/B tests exist."))

p.append(B.h2("When you can't randomize", kicker="Concept · the honest caveat")
)
p.append(B.concept(
 "Experiments aren't always possible or ethical: you can't randomly assign people to smoke, you "
 "can't A/B test a one-time pricing change on the same users, and some changes are too big or slow "
 "to test. When randomization is off the table, you fall back to ~causal inference~ methods (Track "
 "7) that try to *approximate* an experiment from observational data &mdash; harder, more assumption-"
 "laden, and never quite as trustworthy. So the rule of thumb: **if you can run an experiment, run "
 "it**; reach for the observational methods only when you truly can't."))

p.append(B.h2("Your turn — measure the causal effect", kicker="Interactive lab"))
p.append(B.pylab(
 "The randomized experiment's data is loaded: `assigned` (0 = control, 1 = treatment) and "
 "`outcome_rct` (each user's outcome). Compute the ~average treatment effect~ &mdash; the mean "
 "outcome of the treatment group minus the mean of the control group &mdash; and assign it to "
 "**`answer`**, rounded to 2 decimals.",
 "import numpy as np\n"
 "rng = np.random.default_rng(0)\n"
 "n = 40000\n"
 "engagement = rng.normal(0, 1, n)\n"
 "assigned = rng.integers(0, 2, n)\n"
 "outcome_rct = 2*engagement + 0.10*assigned + rng.normal(0, 1, n)\n",
 "answer = round(float(outcome_rct[assigned == 1].mean() - outcome_rct[assigned == 0].mean()), 2)",
 starter="# assigned (0/1) and outcome_rct are loaded\nanswer = ",
 hint="Use boolean masks: `outcome_rct[assigned == 1].mean()` minus `outcome_rct[assigned == 0].mean()`, "
      "then `round(float(...), 2)`.",
 title="Lab — the average treatment effect",
 preview="`assigned` (0/1) and `outcome_rct` arrays loaded. First Run loads NumPy.",
 explain="Because assignment was random, the two groups are comparable, so the simple difference in "
         "means is an unbiased estimate of the causal effect (&#8776; the true 0.10)."))

p.append(B.keypoints([
 "~Correlation is not causation~; the culprit is ~confounding~ &mdash; a hidden variable driving both "
 "things you compare (engaged users self-selecting into a feature).",
 "A ~randomized experiment~ (A/B test) assigns users to control/treatment **by chance**, so the "
 "groups are balanced on **everything** &mdash; measured and unmeasured.",
 "The only systematic difference left is the change itself, so a metric gap can be attributed to it "
 "&mdash; that's ~causality~.",
 "Randomization is the **gold standard**: if you can run an experiment, run it.",
 "When you can't randomize (ethics, feasibility), fall back to ~causal inference~ (Track 7) &mdash; "
 "weaker and more assumption-heavy.",
]))

p.append(B.quiz([
 {"q":"Users who enabled a new 'dark mode' have 20% higher retention. Can you conclude dark mode "
      "*causes* higher retention?",
  "options":[
   {"t":"No — the users who chose to enable it were probably already more engaged (selection bias / "
        "confounding)","correct":True,
    "why":"Correct. Self-selected feature users differ systematically from non-users, so the "
          "comparison is confounded. Only randomly assigning dark mode would isolate its causal "
          "effect."},
   {"t":"Yes — a 20% difference is too big to be chance",
    "why":"Size doesn't fix confounding. The groups aren't comparable (engaged users self-selected), "
          "so the gap can't be attributed to dark mode."},
   {"t":"Yes, as long as the sample is large",
    "why":"A huge sample makes a *confounded* estimate more precisely wrong, not correct. Randomization, "
          "not sample size, removes the bias."},
   {"t":"No, because retention can't be measured reliably",
    "why":"Retention is measurable; the problem is selection bias between choosers and non-choosers, "
          "which randomization would eliminate."}]},
 {"q":"Why does random assignment let you claim causality?",
  "options":[
   {"t":"On average it makes the groups identical on all variables (even unmeasured ones), so the "
        "only difference left is the treatment","correct":True,
    "why":"Correct. The coin flip is independent of every user characteristic, so both known and "
          "unknown confounders are balanced across groups — any outcome gap must come from the "
          "treatment."},
   {"t":"It increases the sample size",
    "why":"Randomization is about *how* users are assigned, not how many there are. Its power is "
          "balancing confounders, not adding data."},
   {"t":"It removes all randomness from the outcome",
    "why":"Outcomes are still noisy; randomization balances confounders across groups, it doesn't make "
          "outcomes deterministic."},
   {"t":"It guarantees the treatment works",
    "why":"It guarantees a *fair test*, not a positive result — the experiment can well show no effect."}]},
 {"q":"When is an observational causal-inference method (not an A/B test) the right choice?",
  "options":[
   {"t":"When randomizing is impossible or unethical (e.g., you can't assign people to smoke)","correct":True,
    "why":"Correct. Experiments are the gold standard, but when you literally can't randomize, you "
          "approximate one from observational data with causal-inference methods — accepting weaker, "
          "assumption-heavy conclusions."},
   {"t":"Always — observational methods are more rigorous than experiments",
    "why":"The reverse: a well-run experiment is the stronger evidence. Observational methods are the "
          "fallback when experiments aren't feasible."},
   {"t":"Whenever you have a large dataset",
    "why":"Dataset size doesn't make observation beat experiment. You prefer an experiment whenever "
          "you can run one."},
   {"t":"Never — you must always run an experiment",
    "why":"Sometimes you genuinely can't (ethics, one-off changes), and then observational causal "
          "methods are the honest fallback."}]},
]))

p.append(B.practice([
 {"q":"A PM says: \"Our email campaign works &mdash; people who opened it bought 3&times; more.\" "
      "What's the flaw, and how would you actually measure the campaign's effect?",
  "sol":"People who **open** marketing emails are already more interested/engaged buyers &mdash; a "
        "textbook confounder &mdash; so the 3&times; mixes the email's effect with who-opens-it "
        "selection bias. To measure the true effect, run a **randomized holdout**: randomly withhold "
        "the email from a control group and compare purchase rates between the randomly-assigned "
        "\"sent\" and \"not sent\" groups (not openers vs non-openers). That difference is the "
        "campaign's causal lift."},
 {"q":"Explain in one sentence why randomization balances confounders you never even measured.",
  "sol":"Because assignment is by pure chance &mdash; independent of every user attribute &mdash; each "
        "group ends up (on average) with the same mix of *all* characteristics, known and unknown, so "
        "no variable can systematically differ between control and treatment to bias the comparison."},
]))

p.append(B.deepdive(
 B.concept(
  "**The counterfactual: what causality actually means.** The causal effect for a single user is the "
  "difference between their outcome *with* the treatment and their outcome *without* it &mdash; but "
  "you only ever see **one** of those (the ~fundamental problem of causal inference~). You can't "
  "un-ring the bell for the same person. Randomization solves it at the **group** level: the "
  "randomly-assigned control group is a fair stand-in for \"what the treatment group *would* have "
  "done without the treatment\", so the difference in group averages estimates the average causal "
  "effect.") +
 B.concept(
  "**Why balance beats adjustment.** With observational data you can try to *adjust* for confounders "
  "&mdash; control for engagement, age, and so on &mdash; but you can only adjust for what you "
  "**measured and thought of**. Randomization balances the confounders you forgot, the ones you "
  "can't measure, and the ones nobody knows exist. That robustness to *unknown* confounders is the "
  "unique superpower of experiments, and why \"just add more control variables\" is never as safe as "
  "a coin flip.") +
 B.concept(
  "**Internal vs external validity.** An experiment has strong ~internal validity~ (within it, the "
  "effect is real and causal) but its ~external validity~ &mdash; whether the result generalises to "
  "other users, times, or contexts &mdash; is a separate question. A feature that wins for new users "
  "in December may not win for everyone year-round. Great experimenters distinguish \"is this effect "
  "real *here*?\" from \"will it hold *there*?\", and treat the second as its own investigation."),
 title="Deep dive: the counterfactual, why balance beats adjustment, and validity"))

p.append(B.callout("note","Interview-ready",
 "The core answer product-DS interviews want: correlation &ne; causation because of **confounding**; "
 "a **randomized** experiment balances all confounders (measured *and* unmeasured) so a metric gap "
 "is causal; prefer an experiment whenever you can run one, and fall back to causal-inference methods "
 "only when you can't. Name **selection bias** (openers vs non-openers) as the classic trap.", "&#9670;"))

LESSONS={"ab-01-why":"\n".join(p)}
print("content_ab01 OK — chars:", len(LESSONS["ab-01-why"]))
