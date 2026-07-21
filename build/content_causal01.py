# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Almost every question a business actually cares about is **causal**: *\"Will this discount "
 "**increase** retention? Does this drug **reduce** mortality? Would hiring more support staff "
 "**cause** higher satisfaction?\"* But the data you have is usually **observational** &mdash; you "
 "watched what happened, you didn't get to intervene. And observational data is riddled with a trap "
 "that has fooled scientists, journalists, and executives for centuries: **correlation is not "
 "causation.** This track is how you tell the difference &mdash; and it's some of the most valuable "
 "judgement a data scientist can offer."))

p.append(B.h2("The problem: things that move together needn't cause each other", kicker="Confounding"))
p.append(B.concept(
 "Ice-cream sales and drownings rise together across the year. Does ice cream cause drowning? Of "
 "course not &mdash; a third variable, **hot weather**, drives *both*. It's a **confounder**: a "
 "common cause that creates a correlation between two things that have no direct effect on each "
 "other. This single picture explains a huge share of bad conclusions in the wild:"))
p.append(B.figure(IMG+"s_causal_confound.png",
 "**Confounding.** Hot weather (Z) causes both ice-cream sales (X) and drownings (Y). So X and Y "
 "move together even though X has **no real effect** on Y. The correlation is real; the causation is "
 "an illusion. To recover the true X&rarr;Y effect, you must account for Z.",
 "A confounder Z pointing to both treatment X and outcome Y, with a dashed uncertain arrow from X to Y."))
p.append(B.concept(
 "Watch it happen in data. We *build* a world where X has **zero** effect on Y &mdash; both are "
 "driven only by a hidden confounder Z &mdash; then look at the naive correlation:"))
_c,_o=_run(r'''
import numpy as np
rng = np.random.default_rng(0)
n = 4000

Z = rng.normal(size=n)                 # hidden confounder (e.g. hot weather)
X = Z + rng.normal(size=n) * 0.5       # X is driven by Z
Y = Z + rng.normal(size=n) * 0.5       # Y is driven by Z  --  X does NOT affect Y

naive = np.corrcoef(X, Y)[0, 1]        # what a naive analyst sees
print(f"naive correlation of X and Y: {naive:.2f}   <- looks like a strong effect!")

# Now 'control for' Z: fit Y ~ 1 + X + Z and read the coefficient ON X
A = np.column_stack([np.ones(n), X, Z])
beta = np.linalg.lstsq(A, Y, rcond=None)[0]
print(f"effect of X on Y after adjusting for Z: {beta[1]:+.2f}   <- the truth: ~0")
''')
p.append(B.code_example(_c,_o,filename="confounding.py"))
p.append(B.pitfall(
 "The naive correlation was a strong **0.8** &mdash; and it was **entirely spurious**. Once we "
 "account for the confounder Z, the real effect of X on Y collapses to essentially **zero**. This is "
 "the whole danger of observational data: the number you see can be created by something you're not "
 "looking at. *\"We found users who did X had 30% higher retention\"* means nothing until you ask "
 "**what else is different** about those users."))

p.append(B.h2("Why you can never just 'see' the effect", kicker="The fundamental problem"))
p.append(B.concept(
 "Causation is about a **counterfactual**: what would have happened to *this same user* if we'd done "
 "the opposite? But we only ever observe **one** version of reality &mdash; the user either got the "
 "email or didn't. We can never see both outcomes for the same person, so the individual causal "
 "effect is literally **unobservable**. This is the ~fundamental problem of causal inference~, and "
 "every method in this track is a clever way to **estimate** the missing counterfactual from a "
 "*comparable* group."))
p.append(B.why(
 "This is why **randomization** (the A/B track) is the gold standard: randomly assigning X breaks "
 "every arrow *into* X, so the treated and untreated groups are comparable on **everything** "
 "&mdash; measured or not. The confounder's arrow to X is severed, and a plain difference in means "
 "becomes a *causal* effect. Causal inference is what you reach for when you **can't** randomize "
 "&mdash; and it works by trying to reconstruct that comparability from messy observational data."))

p.append(B.h2("Your turn — unmask a confounded effect", kicker="Interactive lab"))
p.append(B.pylab(
 "The confounder Z drives both X and Y, and X has **no real effect** on Y. Prove it: fit the "
 "regression **Y ~ 1 + X + Z** and report the coefficient **on X** (the adjusted effect), rounded to "
 "**2 decimals**, as **`answer`**. Adjusting for Z should make the spurious effect vanish.",
 "import numpy as np\n"
 "rng = np.random.default_rng(0)\n"
 "n = 4000\n"
 "Z = rng.normal(size=n)\n"
 "X = Z + rng.normal(size=n) * 0.5\n"
 "Y = Z + rng.normal(size=n) * 0.5   # X does NOT cause Y\n",
 "A = np.column_stack([np.ones(n), X, Z])\n"
 "beta = np.linalg.lstsq(A, Y, rcond=None)[0]\n"
 "answer = round(float(beta[1]), 2)",
 starter="import numpy as np\n# build design matrix [1, X, Z], solve least squares for Y,\n# take the coefficient on X, round to 2 dp\nanswer = ",
 hint="`A = np.column_stack([np.ones(n), X, Z])`; `beta = np.linalg.lstsq(A, Y, rcond=None)[0]`; "
      "the intercept is `beta[0]`, the X coefficient is `beta[1]`.",
 title="Lab — controlling for the confounder",
 preview="numpy loaded; Z, X, Y prebuilt (X has no true effect on Y). First Run boots Python.",
 explain="The coefficient on X is essentially **0** &mdash; once you hold Z fixed, X and Y are "
         "unrelated, exactly as we built them. The naive correlation of 0.8 was pure confounding. "
         "*Adjusting for the right variable is how observational data starts to speak about causes.*"))

p.append(B.keypoints([
 "Most business questions are **causal** (\"will X *cause* Y?\"), but most data is **observational** "
 "&mdash; so **correlation &ne; causation**.",
 "A **confounder** is a common cause of both X and Y; it manufactures correlation with no real "
 "effect (ice cream &amp; drownings &larr; hot weather).",
 "The **fundamental problem**: you never see both counterfactual outcomes for the same unit, so a "
 "causal effect must be **estimated** from a comparable group.",
 "**Randomization** is the gold standard because it severs every arrow into X, making groups "
 "comparable on *everything* &mdash; measured or not.",
 "When you can't randomize, you must **adjust** for confounders &mdash; but only if you know (and "
 "measured) them.",
]))

p.append(B.quiz([
 {"q":"A report says \"employees who attended the leadership workshop were promoted 2&times; as "
      "often.\" Why is \"the workshop causes promotions\" premature?",
  "options":[
   {"t":"Ambitious, already-high-performing people are more likely to *both* attend and get promoted "
        "— ambition is a confounder","correct":True,
    "why":"Correct. Self-selection creates a confounder: the type of person who signs up is also the "
          "type who gets promoted anyway. Without accounting for that, the 2&times; is partly (maybe "
          "entirely) spurious."},
   {"t":"The sample size is probably too small",
    "why":"Sample size affects precision, not this bias. Even with millions of employees, "
          "self-selection confounding would remain."},
   {"t":"Promotions can't be measured objectively",
    "why":"Promotions are measurable; the problem is *confounding*, not measurement."},
   {"t":"It isn't premature — 2&times; is a large effect",
    "why":"Effect size doesn't establish causation. A large correlation can be entirely driven by a "
          "confounder like pre-existing ambition."}]},
 {"q":"Why does randomly assigning the treatment let you read a causal effect straight from a "
      "difference in means?",
  "options":[
   {"t":"Randomization makes the treated and control groups comparable on all variables — even "
        "unmeasured ones — so nothing but the treatment differs on average","correct":True,
    "why":"Correct. Random assignment severs every arrow *into* treatment, balancing confounders "
          "(known and unknown) across groups. Any average outcome difference is then attributable to "
          "the treatment."},
   {"t":"Randomization increases the sample size",
    "why":"It doesn't change sample size; it changes *comparability* by balancing confounders across "
          "arms."},
   {"t":"Because random numbers are unbiased",
    "why":"The mechanism is group *balance* on confounders, not a property of the random numbers "
          "themselves."},
   {"t":"It removes all noise from the outcome",
    "why":"Noise remains; randomization removes *systematic* differences (confounding), not "
          "variance."}]},
]))

p.append(B.practice([
 {"q":"Give your own example of two things that are correlated because of a confounder, and name the "
      "confounder.",
  "sol":"Many valid answers. Classic ones: **shoe size and reading ability** in children are "
        "correlated &mdash; confounder is **age** (older kids have bigger feet *and* read better). "
        "**Coffee drinking and heart disease** &mdash; confounder is **smoking** (smokers drink more "
        "coffee *and* have more heart disease). **Number of firefighters at a blaze and damage "
        "done** &mdash; confounder is **fire size**. In each, a common cause drives both variables, "
        "so they move together with no direct effect. The test: can you name a plausible third "
        "variable that causes *both*?"},
 {"q":"Your PM says \"users who use our mobile app spend 3&times; more than web-only users, so let's "
      "push everyone to mobile.\" What's your causal objection, and what would settle it?",
  "sol":"**Objection:** self-selection confounding &mdash; the most engaged, highest-intent customers "
        "*choose* to install the app, so they'd likely spend more *regardless* of platform. Mobile "
        "usage and spend share a common cause (engagement/intent), so the 3&times; is partly "
        "spurious; pushing lukewarm users to mobile may not transfer the spending. **What settles "
        "it:** a **randomized experiment** &mdash; randomly prompt a subset to adopt the app and "
        "compare spend to a held-out control (an *encouragement* design). Absent that, adjust for "
        "measured engagement/history (matching or regression) &mdash; but only randomization rules "
        "out the *unmeasured* confounders."},
]))

p.append(B.deepdive(
 B.concept(
  "**The potential-outcomes language.** Formally, each unit has two potential outcomes: Y(1) if "
  "treated and Y(0) if not. The individual effect is Y(1)&minus;Y(0) &mdash; but we only ever see "
  "*one* of them (the fundamental problem). What we *can* estimate is the **Average Treatment "
  "Effect**, ATE = E[Y(1)&minus;Y(0)], if the groups are comparable. The condition that makes it "
  "work is ~ignorability~ (a.k.a. *unconfoundedness*): given the confounders we've measured and "
  "adjusted for, treatment is 'as good as random.' Every observational method in this track is an "
  "attempt to make ignorability believable &mdash; and its Achilles' heel is always the confounder "
  "you *didn't* measure.") +
 B.concept(
  "**Adjustment is a double-edged sword.** \"Control for more variables\" sounds always-safe, but "
  "it isn't: controlling for the *wrong* variable can **introduce** bias rather than remove it. "
  "Adjust for a **confounder** &mdash; good. Adjust for a **mediator** (something *on* the causal "
  "path X&rarr;M&rarr;Y) and you erase part of the very effect you're measuring. Adjust for a "
  "**collider** and you conjure a fake correlation out of nothing. Knowing *which* variables to "
  "adjust for &mdash; not just throwing everything into a regression &mdash; is the whole art, and "
  "it's exactly what **causal diagrams** (the next lesson) were invented to make rigorous."),
 title="Deep dive: potential outcomes, the ATE, ignorability, and why 'control for everything' is wrong"))

p.append(B.callout("note","Where this is going",
 "You now have the core danger (confounding) and the gold standard (randomization). Next you'll "
 "learn to **draw** your causal assumptions as a diagram &mdash; which turns *\"what should I "
 "control for?\"* from a guessing game into a set of readable rules.", "&#9670;"))

LESSONS={"causal-01-why":"\n".join(x for x in p if x)}
print("content_causal01 OK — chars:", len(LESSONS["causal-01-why"]))
