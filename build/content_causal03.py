# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Sometimes you simply **can't** run an experiment: it would be unethical (you can't randomly assign "
 "smoking), impossible (you can't randomize a country's minimum wage), or too late (the feature "
 "already shipped to everyone). Causal inference offers a toolkit that **approximates** a randomized "
 "experiment from observational data &mdash; by finding or constructing a **comparable** group that "
 "shows what *would* have happened. None is as clean as randomization, and each rests on an "
 "assumption you must defend &mdash; but done carefully, they turn \"we can't experiment\" into \"we "
 "can still estimate.\""))

p.append(B.h2("Make the groups comparable — matching & adjustment", kicker="Method 1 & 2"))
p.append(B.concept(
 "If a confounder Z makes treated and untreated units different, the fix is to **compare like with "
 "like**:\n\n"
 "- **Matching / propensity scores.** Pair each treated unit with an untreated unit that has the "
 "*same* confounders (same age, spend, tenure...). With many confounders, summarise them into a "
 "single **propensity score** &mdash; the modelled probability of being treated &mdash; and match on "
 "that. Comparing units with equal propensity mimics a randomized split *within* each matched "
 "stratum.\n"
 "- **Regression adjustment.** Put the confounders into the model (`Y ~ X + Z1 + Z2 + ...`) and read "
 "the coefficient on X as the effect *holding confounders fixed* &mdash; exactly what you did in "
 "lesson 7.1. Simple and powerful, if you've measured and correctly specified the confounders."))
p.append(B.warn(
 "Both methods can only adjust for confounders you **measured**. They do nothing about *unobserved* "
 "confounding &mdash; the lurking variable you didn't record. That's their permanent Achilles' heel, "
 "and why a matched/adjusted estimate is \"causal **if** we've captured the important confounders,\" "
 "never an unconditional guarantee."))

p.append(B.h2("Borrow a trend — difference-in-differences", kicker="Method 3"))
p.append(B.concept(
 "When a policy or feature hits **one group but not another** at a known time, you can use the "
 "untreated group's change over the same period as the **counterfactual** &mdash; what would have "
 "happened to the treated group anyway. The causal effect is the *difference of the two "
 "differences*: how much the treated group changed, **minus** how much the control changed:"))
p.append(B.figure(IMG+"s_causal_did.png",
 "**Difference-in-differences.** The control's before&rarr;after change (grey) estimates the "
 "background trend. Project that trend onto the treated group (the dashed counterfactual). The gap "
 "between the treated group's **actual** after value and that counterfactual is the causal effect "
 "&mdash; the part of the treated change that the background trend *doesn't* explain.",
 "Diff-in-differences: control and treatment lines before and after, with the causal effect as the gap to the counterfactual."))
p.append(B.concept(
 "It's arithmetic once you see it: **DiD = (treated_after &minus; treated_before) &minus; "
 "(control_after &minus; control_before).** The magic is that any *fixed* difference between the "
 "groups (treated started higher) and any *shared* trend over time (both rose with the season) "
 "**cancel out** &mdash; leaving only the treatment's own effect."))
p.append(B.pitfall(
 "DiD lives or dies on the ~parallel-trends assumption~: absent the treatment, the two groups would "
 "have moved *in parallel*. You can't prove it (the counterfactual is unobserved), but you can make "
 "it **credible** by showing the groups moved in parallel for many periods **before** the treatment. "
 "If their pre-trends already diverged, DiD is measuring that divergence, not the treatment."))

p.append(B.h2("Two more, briefly — IV and RDD", kicker="Method 4 & 5"))
p.append(B.concept(
 "- **Instrumental variables (IV).** Find an ~instrument~: something that nudges treatment X but "
 "affects the outcome Y *only through* X, and is unrelated to the confounders. Randomised-ish "
 "'natural' nudges (a lottery, a policy quirk, distance to a clinic) create quasi-random variation "
 "in X you can exploit. Powerful, but valid instruments are rare and their assumptions are hard to "
 "verify.\n"
 "- **Regression discontinuity (RDD).** When treatment is assigned by a sharp **cutoff** on some "
 "score (scholarship if GPA &ge; 3.5; drug if risk-score &ge; threshold), units *just above* and "
 "*just below* the line are essentially identical by luck &mdash; so comparing them near the cutoff "
 "is almost a randomized experiment. Clean and credible, but only speaks to units *near* the "
 "threshold."))

p.append(B.h2("Your turn — compute a difference-in-differences", kicker="Interactive lab"))
p.append(B.pylab(
 "A loyalty program launched in the **treated** region but not the **control** region. Using the "
 "before/after average-spend arrays, compute the **difference-in-differences** estimate of the "
 "program's effect &mdash; `(treated change) &minus; (control change)` &mdash; round to **1 "
 "decimal**, and assign to **`answer`**.",
 "import numpy as np\n"
 "treat_before = np.array([50, 52, 54, 51, 53])\n"
 "treat_after  = np.array([64, 67, 66, 65, 66])\n"
 "ctrl_before  = np.array([39, 41, 40, 42, 38])\n"
 "ctrl_after   = np.array([45, 47, 46, 44, 48])\n",
 "did = (treat_after.mean() - treat_before.mean()) - (ctrl_after.mean() - ctrl_before.mean())\n"
 "answer = round(float(did), 1)",
 starter="import numpy as np\n# DiD = (treated after - treated before) - (control after - control before)\nanswer = ",
 hint="Take `.mean()` of each of the four arrays; compute the treated change and the control change; "
      "subtract the second from the first; round to 1 dp.",
 title="Lab — difference-in-differences by hand",
 preview="numpy loaded; four arrays (treated/control × before/after) preloaded. First Run boots Python.",
 explain="The treated region rose ~13.6 while the control rose ~6 from the background trend &mdash; "
         "so the program's own effect is the **difference of differences**, about **7.6**. Subtracting "
         "the control's change is what removes the seasonal/background trend the program didn't cause."))

p.append(B.keypoints([
 "When you can't randomize, causal methods **approximate** an experiment by building a comparable "
 "counterfactual.",
 "**Matching / propensity scores** and **regression adjustment** compare like-with-like on "
 "**measured** confounders &mdash; blind to *unmeasured* ones.",
 "**Difference-in-differences** uses a control group's trend as the counterfactual: DiD = (treated "
 "&Delta;) &minus; (control &Delta;); relies on **parallel trends**.",
 "**Instrumental variables** exploit a quasi-random nudge to treatment; **RDD** exploits a sharp "
 "assignment **cutoff** &mdash; both credible but narrow.",
 "Every method rests on an **untestable assumption** (no unmeasured confounding / parallel trends) "
 "&mdash; state it and defend it.",
]))

p.append(B.quiz([
 {"q":"A state raised its minimum wage; a neighbouring state didn't. To estimate the employment "
      "effect, which design fits best?",
  "options":[
   {"t":"Difference-in-differences, using the neighbouring state as the control for the background "
        "trend","correct":True,
    "why":"Correct. One group treated at a known time, a comparable group untreated &mdash; the "
          "textbook DiD setup. The neighbour's before/after change estimates what would have happened "
          "absent the wage hike, assuming parallel trends."},
   {"t":"A randomized controlled trial",
    "why":"You can't randomly assign a state's minimum-wage law &mdash; that's exactly why you reach "
          "for a quasi-experimental design like DiD."},
   {"t":"Simple correlation of wage and employment across all states",
    "why":"Riddled with confounding (states differ in countless ways). DiD's before/after-with-control "
          "structure is what controls for fixed differences and shared trends."},
   {"t":"Propensity matching on the treated state alone",
    "why":"With a single treated state and a policy-level change, DiD against a comparable control is "
          "the natural fit; matching individuals doesn't address the state-level trend."}]},
 {"q":"What single assumption most threatens a difference-in-differences estimate?",
  "options":[
   {"t":"Parallel trends — that, without the treatment, the two groups would have changed by the same "
        "amount","correct":True,
    "why":"Correct. DiD credits the treated group's *extra* change to the treatment, which only holds "
          "if the groups would otherwise have moved in parallel. Diverging pre-trends invalidate it. "
          "Check pre-period parallelism to make it credible."},
   {"t":"That the sample is normally distributed",
    "why":"Normality isn't the crux of DiD; the identifying assumption is parallel trends between the "
          "groups."},
   {"t":"That treatment was randomly assigned",
    "why":"DiD is used precisely *because* treatment wasn't randomized; it doesn't require it &mdash; "
          "it requires parallel trends."},
   {"t":"That there are exactly two time periods",
    "why":"DiD generalises to many periods; the essential assumption is parallel trends, not the "
          "number of periods."}]},
]))

p.append(B.practice([
 {"q":"You matched treated and control users on age, tenure, and past spend, and found a positive "
      "effect. A stakeholder asks \"so it's causal?\" How do you answer honestly?",
  "sol":"\"It's causal **under an assumption we can't fully verify**: that age, tenure, and past "
        "spend capture the *important* ways treated and control users differ &mdash; i.e. **no "
        "unmeasured confounding**. Matching balanced the confounders we *observed*, so within matched "
        "pairs the comparison mimics a randomized split. But if some *unmeasured* factor (say, "
        "intrinsic motivation) drives both taking the treatment and the outcome, the estimate is "
        "still biased. So: it's our best causal estimate given the data, I'd report the assumption "
        "explicitly, run a **sensitivity analysis** to see how strong an unmeasured confounder would "
        "have to be to overturn it, and note that only a randomized test would settle it "
        "definitively.\" Honesty about the assumption *is* the senior answer."},
 {"q":"Give an example of a plausible instrumental variable and explain the two properties it must "
      "satisfy.",
  "sol":"Example: to estimate the effect of **military service** on later earnings, the **Vietnam "
        "draft lottery number** is a classic instrument &mdash; it randomly nudged the probability of "
        "serving. The two properties: **(1) relevance** &mdash; the instrument must actually affect "
        "the treatment (a low draft number raised the chance of serving); and **(2) the exclusion "
        "restriction** &mdash; the instrument affects the outcome *only through* the treatment and is "
        "unrelated to confounders (your lottery number shouldn't affect later earnings except via "
        "whether you served). Relevance is testable; the exclusion restriction is an untestable "
        "judgement call &mdash; which is why credible instruments are rare and prized."},
]))

p.append(B.deepdive(
 B.concept(
  "**Propensity scores, a little deeper.** The propensity score e(Z) = P(treated | Z) collapses many "
  "confounders into one number. Its magic property (Rosenbaum-Rubin): if treatment is unconfounded "
  "given Z, it's also unconfounded given just e(Z) &mdash; so you can match, stratify, or weight on a "
  "single score instead of balancing dozens of variables. **Inverse-propensity weighting (IPW)** "
  "reweights the sample so treated and control look alike; **doubly-robust** estimators combine a "
  "propensity model *and* an outcome model, and stay unbiased if **either** one is correct &mdash; a "
  "useful insurance policy. The catch remains: the score is built only from *measured* confounders.") +
 B.concept(
  "**Choosing a method is choosing which assumption you can defend.** Randomize if you possibly can "
  "&mdash; it needs the fewest assumptions. Otherwise, pick the design whose key assumption is most "
  "credible in *your* setting: DiD when you have a clean comparison group and parallel pre-trends; "
  "RDD when a sharp cutoff assigns treatment; IV when a genuinely as-good-as-random nudge exists; "
  "matching/regression when you're confident you measured the confounders. Then **stress-test** the "
  "assumption: plot pre-trends for DiD, check covariate balance after matching, run sensitivity "
  "analyses for unmeasured confounding. The deliverable of good causal work is not just an estimate "
  "&mdash; it's an estimate *plus* an honest account of what has to be true for it to hold."),
 title="Deep dive: propensity scores, IPW, doubly-robust estimation, and choosing your assumption"))

p.append(B.callout("note","Interview-ready",
 "Name the method **and** its assumption in the same breath: DiD &rarr; parallel trends; matching/"
 "regression &rarr; no unmeasured confounding; IV &rarr; relevance + exclusion; RDD &rarr; continuity "
 "at the cutoff. Candidates who say *\"I'd use difference-in-differences, and I'd defend it by "
 "checking the pre-treatment trends are parallel\"* sound like they've done this for real.", "&#9670;"))

LESSONS={"causal-03-methods":"\n".join(x for x in p if x)}
print("content_causal03 OK — chars:", len(LESSONS["causal-03-methods"]))
