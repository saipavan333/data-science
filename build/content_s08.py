# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "A single number pretends to a precision it doesn't have. 'Average checkout time is 42 seconds' "
 "sounds exact, but it came from a sample and would shift on a different day. A ~confidence "
 "interval~ replaces the false precision with an honest range &mdash; '42 seconds, give or take "
 "3' &mdash; and tells you how much to trust it. This is how a professional reports a number."))

p.append(B.h2("Point estimate vs. interval estimate", kicker="Concept"))
p.append(B.concept(
 "A ~point estimate~ is your single best guess for a parameter &mdash; usually just the sample "
 "statistic. The sample mean x&#772; = 42s is a point estimate of the true mean &mu;. It's "
 "necessary but incomplete: it carries no hint of how far off it might be.\n\n"
 "An ~interval estimate~ fixes that by reporting a range of plausible values. The most common "
 "kind is the ~confidence interval~ (CI): a range built from the data, with a stated "
 "~confidence level~ (usually 95%) describing how often such ranges capture the truth."))

p.append(B.h2("Building a confidence interval", kicker="Concept · the recipe"))
p.append(B.concept(
 "Every confidence interval has the same shape: take your estimate and add a cushion on each side "
 "for uncertainty. That cushion is the ~margin of error~."))
p.append(B.formula(
 'CI = x&#772; &plusmn; <span class="var">t*</span> &times; SE',
 "estimate ± (critical value × standard error). For 95% confidence and a decent sample size, "
 "t* &asymp; 1.96 — straight from the normal curve of the CLT."))
p.append(B.concept(
 "The three ingredients each have a job: the **standard error** (Lesson 1.6) sets the natural "
 "scale of the wobble; the **critical value** t* stretches it to the confidence you want (more "
 "confidence &rarr; wider interval); and the **estimate** centers it. Because the CLT makes "
 "x&#772; approximately normal, the 95% figure comes from the empirical rule: about 95% of a "
 "normal distribution lies within ~1.96 standard errors of the center."))
p.append(B.figure(IMG+"s8_margin.png",
 "**Anatomy of a 95% CI.** The bell is the sampling distribution of the mean; the shaded middle "
 "95% sets the margin of error of ±1.96 SE around the point estimate.",
 "A 95% confidence interval drawn under the sampling distribution of the mean."))

p.append(B.h2("What '95% confidence' actually means", kicker="Concept · the interpretation everyone botches"))
p.append(B.concept(
 "This is the most misunderstood idea in statistics, and interviewers know it. The confidence is "
 "a property of the **procedure**, not of any single interval. If you repeated your study many "
 "times and built a 95% CI each time, about 95% of those intervals would contain the true "
 "parameter. The picture makes it unmistakable:"))
p.append(B.figure(IMG+"s8_ci_concept.png",
 "**Confidence is about the long run.** Each horizontal bar is one study's 95% CI. Across many "
 "studies, ~95% capture the true mean (blue) and ~5% miss it (red). You never know which kind "
 "you got &mdash; that's why it's 'confidence,' not certainty.",
 "Many confidence intervals, about 95% of which contain the true mean."))
p.append(B.callout("pitfall","The interpretation trap",
 "It is **wrong** to say 'there's a 95% probability the true mean is in *this* interval.' Once "
 "computed, your interval either contains &mu; or it doesn't &mdash; the truth isn't random. The "
 "95% describes how often the *method* succeeds over many repetitions. Say: *'we're 95% confident "
 "the true value lies in this range,'* meaning the procedure that produced it works 95% of the "
 "time.", "&#10007;"))

p.append(B.h2("Compute one from real data", kicker="Worked example"))
p.append(B.concept(
 "Here's the whole calculation on a sample of 50 checkout times. Because we estimate the spread "
 "from the sample (we don't know the true &sigma;), the correct critical value comes from the "
 "~t-distribution~ &mdash; a slightly wider cousin of the normal that accounts for that extra "
 "uncertainty (more in the deep dive)."))
_c,_o=_run(r'''
import numpy as np
from scipy import stats
rng = np.random.default_rng(3)

# 50 checkout times in seconds (we don't know the true mean or SD).
sample = rng.normal(42, 11, size=50)
n      = len(sample)
xbar   = sample.mean()
s      = sample.std(ddof=1)          # sample SD (ddof=1 -> the n-1 from Lesson 1.3)
se     = s / np.sqrt(n)              # standard error of the mean

t_star = stats.t.ppf(0.975, df=n-1)  # 95% critical value from the t-distribution
margin = t_star * se
lo, hi = xbar - margin, xbar + margin

print(f"point estimate x-bar = {xbar:.1f} s")
print(f"standard error  SE   = {se:.2f} s   (t* = {t_star:.2f})")
print(f"95% confidence interval: [{lo:.1f}, {hi:.1f}]  =  {xbar:.1f} ± {margin:.1f} s")
''')
p.append(B.code_example(_c,_o,filename="confidence_interval.py"))
p.append(B.concept(
 "Report it like this: *'Average checkout time is about 42 seconds (95% CI: roughly 39 to 45).'* "
 "That one sentence gives the estimate **and** its uncertainty &mdash; everything a stakeholder "
 "needs to judge whether a 1-second 'improvement' is worth chasing."))

p.append(B.keypoints([
 "A ~point estimate~ is a single best guess; a ~confidence interval~ adds an honest range of "
 "plausible values.",
 "CI = estimate ± (critical value × standard error). For 95%, the critical value is &asymp; 1.96.",
 "**Correct meaning:** about 95% of intervals built this way capture the truth. **Wrong:** "
 "'95% probability the truth is in *this* interval.'",
 "Wider confidence &rarr; wider interval; larger n &rarr; smaller SE &rarr; narrower interval.",
 "When &sigma; is estimated from the sample (the usual case), use the **t-distribution** for the "
 "critical value.",
]))

p.append(B.quiz([
 {"q":"A report states: 'Average session length is 8.2 minutes (95% CI: 7.6 to 8.8).' Which "
      "interpretation is correct?",
  "options":[
   {"t":"If we repeated this study many times, about 95% of the intervals we'd build would "
        "contain the true average","correct":True,
    "why":"Correct. Confidence refers to the long-run success rate of the procedure, not the "
          "probability that this particular interval contains the truth."},
   {"t":"There is a 95% probability the true average is between 7.6 and 8.8",
    "why":"Tempting but wrong. Once computed, the interval either contains the fixed true mean or "
          "not. The 95% is about the method across many repetitions, not this one interval."},
   {"t":"95% of users have sessions between 7.6 and 8.8 minutes",
    "why":"The CI is about the *mean*, not individual users. Most users' session lengths spread "
          "far wider than the interval for the average."},
   {"t":"The true average is definitely in that range",
    "why":"Nothing is definite &mdash; about 5% of such intervals miss. Confidence is not "
          "certainty."}]},
 {"q":"You compute a 95% CI and want a *narrower* one without changing the confidence level. What "
      "works?",
  "options":[
   {"t":"Collect a larger sample — it shrinks the standard error","correct":True,
    "why":"Right. Width is driven by SE = s/&radic;n, so more data shrinks the SE and narrows the "
          "interval while keeping 95% confidence."},
   {"t":"Lower the confidence to 99%",
    "why":"Raising confidence to 99% makes the interval *wider*, not narrower (bigger critical "
          "value). To narrow it at the same confidence, get more data."},
   {"t":"Report the point estimate alone",
    "why":"That hides uncertainty rather than reducing it. The honest way to narrow a CI is more "
          "data."},
   {"t":"Round the numbers",
    "why":"Rounding changes presentation, not the underlying uncertainty or interval width."}]},
 {"q":"Two 95% CIs for a conversion rate: Team X reports [4.0%, 4.4%]; Team Y reports "
      "[2.1%, 6.3%]. What does the difference in width most likely reflect?",
  "options":[
   {"t":"Team X had a much larger sample, giving a smaller standard error","correct":True,
    "why":"Correct. A narrower interval at the same confidence usually means a smaller SE, which "
          "comes from a larger sample (or less variable data)."},
   {"t":"Team X is more confident in their result",
    "why":"Both are at 95% confidence. Width reflects precision (sample size/variability), not a "
          "higher confidence level."},
   {"t":"Team Y made a calculation error",
    "why":"A wide interval isn't an error &mdash; it's an honest signal of high uncertainty, "
          "typically from a small or noisy sample."},
   {"t":"Team Y's true value is more variable",
    "why":"The *true* rate is a fixed number; the interval width reflects the estimate's "
          "uncertainty (mostly sample size), not variability of the truth."}]},
]))

p.append(B.practice([
 {"q":"A sample of n=100 gives mean 50 with standard error 2. Write the approximate 95% "
      "confidence interval, and state its correct interpretation in one sentence.",
  "sol":"95% CI &asymp; 50 ± 1.96×2 = 50 ± 3.92, i.e. **[46.1, 53.9]**. Interpretation: *if we "
        "repeated this study many times and built such an interval each time, about 95% of them "
        "would contain the true mean* &mdash; so we're 95% confident the true mean is between "
        "about 46 and 54."},
 {"q":"Your boss says 'the CI is [10, 30], so there's a 95% chance the real number is 20.' Two "
      "things are wrong. What are they?",
  "sol":"(1) The CI doesn't put 95% probability on any single value &mdash; and certainly not on "
        "the midpoint 20 specifically; the point estimate is just the center, not a 95%-likely "
        "value. (2) The 95% isn't the probability the truth is in *this* interval at all; it's "
        "the long-run capture rate of the procedure. Correct phrasing: 'we're 95% confident the "
        "true value is between 10 and 30,' and the interval is wide, so our estimate is "
        "imprecise."},
]))

p.append(B.deepdive(
 B.concept(
  "**Why the t-distribution?** The clean '1.96' assumes you know the true standard deviation "
  "&sigma;. In reality you estimate it with the sample SD s, which is itself noisy &mdash; "
  "especially with small samples. The ~t-distribution~ accounts for that extra uncertainty by "
  "being slightly wider than the normal, with heavier tails. Its exact shape depends on the "
  "~degrees of freedom~ (n&minus;1): with few data points the tails are fat (critical value well "
  "above 1.96), and as n grows it converges to the normal. For n above ~30 the difference is "
  "small, which is why 1.96 is a fine shortcut for large samples.") +
 B.concept(
  "**The bootstrap: a CI with almost no math.** When a formula is hard or assumptions are shaky, "
  "you can build a CI by brute force. ~Resample~ your data with replacement to make a new "
  "pretend-sample of the same size, compute the statistic, and repeat thousands of times. The "
  "middle 95% of those bootstrap statistics *is* your 95% confidence interval. It works for "
  "medians, ratios, and other statistics with no neat formula, and it makes the 'imagine "
  "repeating the study' idea literal &mdash; you're simulating the sampling distribution from the "
  "one sample you have.") +
 B.concept(
  "**Confidence vs. width trade-off.** Want 99% confidence instead of 95%? The critical value "
  "jumps (from ~1.96 to ~2.58), so the interval widens. There's no free lunch: more confidence "
  "means a vaguer range. The only way to be both confident *and* precise is more data."),
 title="Deep dive: the t-distribution, the bootstrap, and the confidence–width trade-off"))

p.append(B.callout("note","Interview-ready",
 "*\"Interpret this confidence interval\"* is a near-guaranteed question. Give the correct "
 "long-run interpretation (about 95% of such intervals capture the truth) and explicitly flag "
 "the wrong one ('not a 95% probability the truth is in this specific interval'). Add that wider "
 "confidence or a smaller sample makes the interval wider. That precision signals real "
 "understanding.", "&#9670;"))

LESSONS={"stats-08-estimation-ci":"\n".join(p)}
