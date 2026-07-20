# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "The most common way an A/B test fails is silent: the change **really works**, but you didn't send "
 "enough users to prove it, so the result comes back \"not significant\" and a good idea gets killed. "
 "That's an ~underpowered~ test. The fix is to compute how many users you need **before** you launch "
 "&mdash; a five-minute calculation that decides whether your two-week experiment can possibly "
 "succeed. Getting this right is what separates experiments that answer the question from experiments "
 "that waste two weeks."))

p.append(B.h2("Four quantities, locked together", kicker="Concept"))
p.append(B.concept(
 "Sample-size planning is a relationship between four numbers &mdash; fix any three and the fourth is "
 "determined:\n\n"
 "- ~significance~ `&alpha;` &mdash; your false-positive rate, usually 0.05 (the chance of calling a "
 "non-effect real).\n"
 "- ~power~ `1 - &beta;` &mdash; the chance of **detecting** a real effect, usually targeted at 0.80 "
 "(so a 20% chance of missing it).\n"
 "- the ~effect size~ you want to catch &mdash; the ~minimum detectable effect~ (MDE).\n"
 "- the ~sample size~ `n` per group.\n\n"
 "Power and significance are two sides of the same picture &mdash; the two ways to be wrong:"))
p.append(B.figure(IMG+"s9_power.png",
 "**Significance (&alpha;) vs power (1&minus;&beta;).** Under the null (left curve) the shaded tail "
 "is &alpha;, your false-positive rate. When there's a real effect (right curve), ~power~ is the "
 "share of that curve past the threshold &mdash; the chance you actually detect it. Bigger samples "
 "narrow both curves and push power up.",
 "Two overlapping bell curves showing alpha (false positive) and power (detecting a real effect)."))

p.append(B.h2("The minimum detectable effect drives everything", kicker="Concept · the key lever")
)
p.append(B.concept(
 "The ~minimum detectable effect~ (MDE) is the **smallest** improvement you'd care to detect. It is "
 "the dominant lever on sample size, and the relationship is brutal: because the noise shrinks like "
 "1/&radic;n (Lesson 4.5), detecting an effect **half** as small needs roughly **four times** as many "
 "users. So \"let's detect any tiny lift\" can mean needing millions of users you don't have. Set the "
 "MDE to the smallest effect that would actually change your decision &mdash; not smaller. Feel this "
 "tradeoff live: pick a reality, set the users per arm, and run the experiment. With too few users, "
 "even a **real** 2-point lift often comes back \"not significant\":"))
p.append(B.widget("abtest", "Run your own A/B test — feel what sample size buys you",
 "Set whether B is truly better or truly identical, choose how many users per arm, and hit **Run**. "
 "With few users the confidence intervals are wide and a real effect often looks \"not significant\" "
 "(underpowered) &mdash; slide the users up and the test starts catching it. Flip to \"no real "
 "difference\" and re-run a few times to watch the occasional **false positive** appear by chance.",
 height=470))

p.append(B.h2("Computing the number", kicker="Worked example"))
p.append(B.concept(
 "For a conversion-rate test, the standard formula turns your four choices into users-per-arm. You "
 "rarely memorise it &mdash; you run it &mdash; but seeing it makes the levers concrete:"))
_c,_o=_run(r'''
import math
from scipy import stats

p1    = 0.10     # current conversion rate (baseline)
mde   = 0.02     # smallest lift worth detecting: +2 percentage points
alpha = 0.05     # significance (false-positive rate)
power = 0.80     # power (chance of detecting a true effect)

p2  = p1 + mde
z_a = stats.norm.ppf(1 - alpha/2)   # 1.96 for alpha = 0.05
z_b = stats.norm.ppf(power)         # 0.84 for 80% power
n   = (z_a + z_b)**2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)**2

print(f"baseline {p1:.0%}, detect a +{mde:.0%} lift, {power:.0%} power, {alpha:.0%} significance")
print(f"  -> users needed PER ARM: {math.ceil(n):,}   (total {2*math.ceil(n):,})")

# now ask to detect a much smaller +0.5pp lift instead
mde2 = 0.005; p2b = p1 + mde2
n2   = (z_a + z_b)**2 * (p1*(1-p1) + p2b*(1-p2b)) / (p2b - p1)**2
print(f"detecting a tiny +{mde2:.1%} lift instead: {math.ceil(n2):,} per arm  (~{n2/n:.0f}x more users)")
''')
p.append(B.code_example(_c,_o,filename="sample_size.py"))
p.append(B.concept(
 "A +2pp lift needs a few thousand per arm; asking to detect a +0.5pp lift &mdash; a quarter the "
 "size &mdash; explodes to tens of thousands, ~16&times; more. **That** is why you set the MDE "
 "deliberately: chase an effect too small and your test needs more traffic than you'll ever have. "
 "Once you have `n`, divide by your daily eligible traffic to get the **duration** &mdash; and run "
 "for at least that long."))

p.append(B.h2("Run the full duration — don't peek", kicker="Concept · the discipline")
)
p.append(B.warn(
 "Decide the sample size and duration up front, then **let it run**. Watching the p-value and "
 "stopping the moment it dips below 0.05 &mdash; ~peeking~ &mdash; massively inflates your "
 "false-positive rate, because a random walk will cross 0.05 *sometime* even with no real effect. "
 "It's the same reason bigger samples help: noise shrinks like 1/&radic;n, so early results are the "
 "most volatile. Plan `n`, run to `n`, then look **once**. (Sequential-testing methods exist for "
 "principled early stopping &mdash; Lesson 6.5.)", "&#9650;"))

p.append(B.h2("Your turn — size the experiment", kicker="Interactive lab"))
p.append(B.pylab(
 "Your baseline conversion is **8%** (`p1 = 0.08`) and you want to detect a **+1.5pp** lift "
 "(`mde = 0.015`) at 80% power and 5% significance. Using the two-proportion formula with "
 "`z_a = 1.96` and `z_b = 0.84`, compute the users needed **per arm** and assign it (rounded **up** "
 "to a whole number with `math.ceil`) to **`answer`**.",
 "import math\n"
 "p1, mde = 0.08, 0.015\n"
 "z_a, z_b = 1.96, 0.84\n",
 "p2 = p1 + mde\n"
 "n = (z_a + z_b)**2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)**2\n"
 "answer = math.ceil(n)",
 starter="# p1, mde, z_a, z_b loaded; math imported\np2 = \nn = \nanswer = ",
 hint="`p2 = p1 + mde`, then `n = (z_a+z_b)**2 * (p1*(1-p1) + p2*(1-p2)) / (p2-p1)**2`, and "
      "`answer = math.ceil(n)`.",
 title="Lab — how many users do you need?",
 preview="`p1`, `mde`, `z_a`, `z_b` loaded; `math` imported. Runs instantly (no heavy packages).",
 explain="Plugging in gives roughly 5,600 per arm &mdash; that many, times two, is what the "
         "experiment must collect before you can trust the result."))

p.append(B.keypoints([
 "Four linked quantities: ~significance~ `&alpha;` (0.05), ~power~ `1-&beta;` (0.80), the ~MDE~ "
 "(effect to detect), and ~sample size~ `n`. Fix three &rarr; the fourth follows.",
 "~Power~ is the chance of **detecting a real effect**; too few users = ~underpowered~ = you miss "
 "real wins.",
 "The ~MDE~ is the dominant lever: detecting an effect **half as small needs ~4&times; the users** "
 "(noise falls like 1/&radic;n).",
 "Compute `n` **before** launching; divide by daily traffic to get the required **duration**.",
 "Fix the sample size and duration in advance and **don't peek** &mdash; stopping early on a lucky "
 "p-value inflates false positives.",
]))

p.append(B.quiz([
 {"q":"An A/B test of a real improvement comes back 'not significant.' What's the most likely cause?",
  "options":[
   {"t":"The test was underpowered — too few users to detect the true effect","correct":True,
    "why":"Correct. A real effect that isn't detected usually means insufficient power (small sample "
          "and/or a small effect relative to noise). Compute the needed sample size before launching."},
   {"t":"The effect definitely doesn't exist",
    "why":"'Not significant' means 'not enough evidence', not 'no effect'. An underpowered test fails "
          "to detect real effects all the time."},
   {"t":"Alpha was set too low",
    "why":"Alpha (usually 0.05) mainly controls false positives; missing a real effect is a *power* "
          "(sample-size) problem, not an alpha one."},
   {"t":"You should lower the significance threshold to 0.10",
    "why":"Loosening alpha trades more false positives for a bit more power — a band-aid. The real fix "
          "is enough users (power)."}]},
 {"q":"You want to detect a lift half as large as originally planned, same power and significance. "
      "Roughly what happens to the required sample size?",
  "options":[
   {"t":"It roughly quadruples (~4x)","correct":True,
    "why":"Correct. Detectable effect scales like 1/sqrt(n), so halving the effect needs about 4x the "
          "users. Small MDEs get expensive fast."},
   {"t":"It roughly halves",
    "why":"Smaller effects need *more* data, not less. Halving the effect roughly quadruples the "
          "sample."},
   {"t":"It stays the same",
    "why":"Sample size depends strongly on the MDE; a smaller effect requires far more users."},
   {"t":"It doubles",
    "why":"The relationship is quadratic (via 1/sqrt(n)), so it's ~4x, not 2x."}]},
 {"q":"Why is it a problem to stop an experiment the moment its p-value first dips below 0.05?",
  "options":[
   {"t":"Repeatedly checking and stopping on a threshold inflates the false-positive rate — a random "
        "walk crosses 0.05 eventually even with no effect","correct":True,
    "why":"Correct. Peeking turns one test into many implicit tests; the p-value wanders and will dip "
          "below 0.05 by chance if you keep looking. Fix the sample size and analyze once (or use "
          "proper sequential methods)."},
   {"t":"It's fine — early significance just means a strong effect",
    "why":"Early results are the noisiest (small n), and stopping on the first dip is exactly how you "
          "manufacture false positives."},
   {"t":"Because the sample is too large by then",
    "why":"The problem is stopping *early* on a noisy peek, not having too much data."},
   {"t":"P-values can't be computed mid-experiment",
    "why":"They can be computed anytime; the issue is *acting* on repeated peeks, which inflates false "
          "positives."}]},
]))

p.append(B.practice([
 {"q":"Your site gets 2,000 eligible visitors per day. A power calculation says you need 40,000 users "
      "per arm to detect the lift you care about. How long must the test run, and what are your "
      "options if that's too long?",
  "sol":"You need 80,000 users total (2 arms &times; 40,000). At 2,000/day that's **40 days**. If "
        "that's too long, your levers are: accept a **larger MDE** (only commit to detecting a bigger "
        "lift &mdash; fewer users), raise the **traffic allocation** to the test, reduce metric "
        "**variance** (e.g., a more sensitive metric or CUPED), or accept **lower power/higher "
        "alpha** (riskier). What you should *not* do is run 10 days and peek &mdash; that just "
        "produces an unreliable answer faster."},
 {"q":"A stakeholder says \"just make the test detect any improvement, however small.\" Why is that "
      "not a real plan?",
  "solhtml": False,
  "sol":"Because required sample size grows roughly like 1/MDE&sup2; &mdash; as the target effect "
        "shrinks toward zero, the users needed grows toward **infinity**. \"Detect anything\" implies "
        "an MDE near 0, i.e. essentially unlimited traffic and time. The disciplined move is to set "
        "the MDE to the **smallest effect that would actually change the decision** (ship / don't "
        "ship); effects smaller than that aren't worth the traffic to chase."},
]))

p.append(B.deepdive(
 B.concept(
  "**Where the formula comes from.** Detecting an effect means the treatment's sampling distribution "
  "sits far enough from the null's that they barely overlap at your chosen &alpha; and power. The "
  "gap you can resolve scales with the ~standard error~, which falls like `&sigma;/&radic;n` &mdash; "
  "so the needed `n` scales with `(z_&alpha; + z_&beta;)&sup2; &middot; variance / effect&sup2;`. "
  "Every term is a knob: stricter &alpha; or higher power raises the `z`'s (more users), a noisier "
  "metric raises the variance (more users), a smaller effect shrinks the denominator (many more "
  "users). It's the CLT (Lesson 4.6) turned into a budget.") +
 B.concept(
  "**Absolute vs relative MDE, and one- vs two-sided.** Be precise about whether your MDE is "
  "**absolute** (+2 percentage points, 0.10 &rarr; 0.12) or **relative** (+20%, 0.10 &rarr; 0.12 too "
  "here, but +20% of 0.05 is only 0.06) &mdash; teams miscommunicate this constantly and size the "
  "test wrong. Also decide one-sided vs two-sided: almost always use **two-sided** (0.05 split into "
  "two tails, `z = 1.96`), because a change could hurt as easily as help, and you want to catch "
  "both.") +
 B.concept(
  "**Don't run underpowered tests — or trust their nulls.** An underpowered experiment is doubly "
  "bad: it usually can't detect the effect (wasting the run), and on the rare occasion it *is* "
  "significant, the estimated effect is **exaggerated** (the ~winner's curse~ &mdash; only the "
  "luckily-large estimates cross the line). So a \"significant\" result from a tiny test is both less "
  "likely to replicate and likely overstated. The professional habit: power the test properly, or "
  "don't run it &mdash; and treat a null from an underpowered test as \"we learned nothing,\" not "
  "\"no effect.\""),
 title="Deep dive: where the sample-size formula comes from, MDE definitions, and the winner's curse"))

p.append(B.callout("note","Interview-ready",
 "Own the vocabulary: **power** = P(detect a real effect), targeted at 80%; **underpowered** tests "
 "miss real wins; the **MDE** dominates sample size (halve the effect &rarr; ~4&times; users); "
 "compute `n` **before** launching and **don't peek** (it inflates false positives). Bonus: absolute "
 "vs relative MDE, and the winner's curse on small tests.", "&#9670;"))

LESSONS={"ab-03-power":"\n".join(p)}
print("content_ab03 OK — chars:", len(LESSONS["ab-03-power"]))
