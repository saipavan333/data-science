# -*- coding: utf-8 -*-
import builder as B
p=[]

p.append(B.why(
 "You've built the whole statistical foundation &mdash; data types, distributions, sampling, the "
 "CLT, estimation, testing, and correlation. This lesson is your **self-test and interview prep**: "
 "the exact questions data-science teams ask to probe statistical maturity, with model answers. "
 "Cover the question, answer it out loud, then reveal the model answer and compare. If you can do "
 "that for every item here, Track 4 has done its job."))

p.append(B.callout("tip","How statistics shows up in DS interviews",
 "Statistics appears in three places: rapid **concept checks** ('explain a p-value'), **applied "
 "judgment** ('which test would you use, and what would you check?'), and **product/case "
 "questions** where you must reason about uncertainty in a metric. Interviewers care less about "
 "memorized formulas than whether you can explain ideas **simply** and spot the common traps. "
 "Answer in plain language first, then add precision.", "&#10022;"))

p.append(B.h2("Core concept questions", kicker="Bank 1 · explain it simply"))
p.append(B.concept(
 "Try each one aloud before revealing the answer. Aim for a crisp two-to-three sentence response "
 "&mdash; the way you'd actually say it in a room."))
p.append(B.practice([
 {"q":"Explain a p-value to a non-technical stakeholder.",
  "sol":"*'If there were really no effect, the p-value is how often we'd see a result at least "
        "this strong just by random chance. A small p-value (say below 0.05) means our result "
        "would be a fluke only rarely, so we doubt the no-effect explanation.'* Then add the "
        "guardrail: it is **not** the probability the null is true, and **not** a measure of how "
        "big or important the effect is."},
 {"q":"What's the difference between standard deviation and standard error?",
  "sol":"**Standard deviation** measures the spread of individual data points (how much do "
        "customers vary?). **Standard error** measures the spread of a *statistic* like the mean "
        "(how much would the sample mean wobble if we resampled?). SE = SD/&radic;n, so it shrinks "
        "as the sample grows &mdash; which is why bigger samples give more precise estimates."},
 {"q":"State the Central Limit Theorem and why it matters.",
  "sol":"The distribution of the **sample mean** becomes approximately **normal** as the sample "
        "size grows, **regardless of the population's shape**, centered at &mu; with spread "
        "&sigma;/&radic;n. It matters because it lets us use normal-based confidence intervals and "
        "tests on almost any data. Caveat: it's about the *mean*, not individual values, and needs "
        "a reasonable n (rule of thumb &ge; 30)."},
 {"q":"Interpret a 95% confidence interval correctly &mdash; and state the common wrong "
      "interpretation.",
  "sol":"**Correct:** if we repeated the study many times and built such an interval each time, "
        "about 95% of them would contain the true value. **Wrong:** 'there's a 95% probability the "
        "true value is in *this* interval' &mdash; once computed, the interval either contains the "
        "(fixed) truth or not; the 95% describes the long-run success rate of the *procedure*."},
 {"q":"What are Type I and Type II errors, and what is power?",
  "sol":"A **Type I error** is a false positive: rejecting a true null (flagging an effect that "
        "isn't real); its rate is &alpha;. A **Type II error** is a false negative: missing a real "
        "effect; its rate is &beta;. **Power = 1 &minus; &beta;** is the chance of detecting a real "
        "effect. Lowering &alpha; trades against power; the way to improve both is more data."},
 {"q":"When would you report the median instead of the mean?",
  "sol":"When the data is **skewed or has outliers** &mdash; income, prices, wait times. The mean "
        "is pulled by extreme values (it's a balance point), while the median (the middle) is "
        "robust. If mean and median disagree a lot, that itself signals skew, and you should plot "
        "the distribution."},
 {"q":"What's the difference between correlation and causation, and how would you establish "
      "causation?",
  "sol":"**Correlation** is two variables moving together; **causation** is one driving the other. "
        "Correlation can arise without causation via a **confounder** (a hidden cause of both), "
        "**reverse causation**, or **coincidence**. To establish causation, run a **randomized "
        "experiment** (random assignment breaks the link to confounders) or, when you can't "
        "experiment, use **causal-inference methods** (controlling for confounders, matching, "
        "diff-in-diff)."},
 {"q":"A result is statistically significant. Why might it still not matter?",
  "sol":"Significance only says the effect is **unlikely to be pure chance**, not that it's "
        "**large or important**. With a big enough sample, even a trivial difference (a 0.01% lift) "
        "becomes significant because the standard error shrinks toward zero. Always pair the "
        "p-value with the **effect size** and its confidence interval, and ask whether the "
        "magnitude is meaningful for the decision."},
]))

p.append(B.h2("Applied judgment & scenarios", kicker="Bank 2 · reason it through"))
p.append(B.practice([
 {"q":"You're given a dataset and asked 'is metric A different between two groups?' Walk through "
      "how you'd decide on and run a test.",
  "sol":"(1) Check the **outcome type** &mdash; numeric &rarr; compare means; categorical &rarr; "
        "chi-square. (2) For a numeric outcome and two independent groups, a **two-sample "
        "(Welch's) t-test**; if the same subjects appear in both, a **paired t-test**. (3) **Check "
        "assumptions**: independence, approximate normality or large n (CLT), outliers. (4) If "
        "assumptions fail (small, skewed), use a **nonparametric** test (Mann&ndash;Whitney). "
        "(5) Report the **effect size and CI**, not just the p-value, and state the practical "
        "implication."},
 {"q":"An A/B test shows a 2% lift with p = 0.30 on one week of data. The PM wants to ship. What "
      "do you say?",
  "sol":"p = 0.30 means we **can't rule out chance** &mdash; but 'not significant' is **not** "
        "'no effect.' A short test on one week may simply be **underpowered**, so a real 2% lift "
        "could be hiding in the noise. I'd estimate the **sample size/run time** needed to detect "
        "a 2% effect with adequate power, watch for novelty effects, and avoid 'peeking' decisions. "
        "Recommendation: keep running to the pre-planned sample size rather than shipping on "
        "inconclusive evidence."},
 {"q":"A stakeholder shows a striking correlation (r = 0.85) between two business metrics and "
      "wants to act on it. What questions do you ask first?",
  "sol":"First, **plot it** &mdash; r can hide curves and be driven by outliers (Anscombe). Then "
        "probe causation: is there a **confounder** driving both? Could it be **reverse "
        "causation**? Could it be **coincidence** (was this found by searching many pairs)? Ask "
        "whether there's a plausible **mechanism**. Before acting, I'd want a **controlled "
        "experiment** to confirm the intervention actually moves the target, since acting on a "
        "non-causal correlation can waste budget or backfire."},
 {"q":"How many users do you need for an experiment, conceptually, and what makes that number go "
      "up or down?",
  "sol":"Sample size grows with the **precision you need** and shrinks with the **effect size** "
        "you're trying to detect. Concretely it depends on: the **minimum effect** worth detecting "
        "(smaller effect &rarr; more users, because error falls only as 1/&radic;n), the "
        "**variability** of the metric (noisier &rarr; more users), the **significance level "
        "&alpha;**, and the **power** you want (typically 80%). To halve the detectable effect you "
        "need ~4&times; the data. (The exact formula is Track 6.)"},
]))

p.append(B.keypoints([
 "Lead with a **plain-language** answer, then add precision &mdash; clarity beats jargon in "
 "interviews.",
 "Know the **traps cold**: p-value &ne; P(H&#8320; true); 'not significant' &ne; 'no effect'; "
 "significance &ne; importance; correlation &ne; causation.",
 "**SE = SD/&radic;n**, and error falls as **1/&radic;n** (4&times; data to halve it).",
 "**CLT** justifies normal-based intervals and tests; the **median** beats the mean under skew.",
 "To claim **causation**, randomize (experiment) or use causal methods &mdash; never a "
 "coefficient.",
]))

p.append(B.quiz([
 {"q":"An interviewer asks you to critique this statement: 'Our test wasn't significant (p = "
      "0.40), which proves the new feature has no effect.' Best response?",
  "options":[
   {"t":"Absence of evidence isn't evidence of absence — a non-significant result may just mean "
        "the test lacked power to detect a real effect","correct":True,
    "why":"Correct. 'Fail to reject' means insufficient evidence, not proof of no effect, "
          "especially if the sample was small/underpowered. You'd estimate the power and the "
          "detectable effect size before drawing conclusions."},
   {"t":"Agree — p = 0.40 proves there is no effect",
    "why":"A large p-value never *proves* the null. It only means the data didn't provide enough "
          "evidence against it; a real effect could be undetected due to low power."},
   {"t":"Agree — p > 0.05 means the effect is exactly zero",
    "why":"The effect isn't shown to be exactly zero; it's just not distinguishable from zero with "
          "this data. That's different from proving no effect."},
   {"t":"The test should have used a 0.40 significance threshold",
    "why":"&alpha; is set before the test (typically 0.05); you don't move it to match the "
          "p-value. The real issue is interpreting non-significance as proof."}]},
 {"q":"You report a metric as '42.0 seconds.' Your interviewer asks what's missing. What's the "
      "strongest answer?",
  "options":[
   {"t":"A measure of uncertainty — a confidence interval or standard error, since 42.0 came from "
        "a sample","correct":True,
    "why":"Right. A point estimate without its uncertainty is incomplete; reporting a CI (or SE) "
          "tells the stakeholder how precise '42.0' is and whether a difference is meaningful."},
   {"t":"More decimal places, like 42.0000 seconds",
    "why":"False precision adds digits, not information. What's missing is the *uncertainty* "
          "around the estimate, not more decimals."},
   {"t":"Nothing — a single number is a complete answer",
    "why":"A sample-based number always carries uncertainty; omitting it can lead to over-trusting "
          "small, noisy differences."},
   {"t":"The maximum value observed",
    "why":"The max describes an extreme, not the precision of the mean. The key omission is a "
          "confidence interval / standard error."}]},
 {"q":"Which answer best demonstrates statistical maturity when asked 'is this 3% lift real?'",
  "options":[
   {"t":"'Let me check whether it's statistically significant AND practically meaningful, with a "
        "confidence interval and adequate power'","correct":True,
    "why":"Correct. It combines significance (chance), effect size with a CI (precision and "
          "magnitude), and power/sample size (could we even detect it?) &mdash; the complete, "
          "mature framing."},
   {"t":"'3% is bigger than 0%, so yes'",
    "why":"That treats a sample number as exact truth, ignoring sampling variability &mdash; "
          "exactly the naivety the question is probing."},
   {"t":"'It depends on the p-value alone'",
    "why":"The p-value is necessary but not sufficient; you also need the effect size, its CI, and "
          "whether the test had power. Significance alone can mislead."},
   {"t":"'We need a machine-learning model to decide'",
    "why":"This is a straightforward inference question about a difference in rates &mdash; an "
          "experiment/test with a CI answers it; ML is unnecessary."}]},
]))

p.append(B.callout("note","You've finished Track 4",
 "If you can answer this bank out loud, you have the statistical foundation that the other ten "
 "tracks build on &mdash; and that data-science interviews are really testing. From here, "
 "**Track 1 (Python, NumPy &amp; Pandas)** turns these ideas into hands-on data skills, and the "
 "**capstone** lets you run a full analysis end to end. Well done &mdash; this is the hard part, "
 "and you've done it.", "&#9670;"))

LESSONS={"stats-12-interview":"\n".join(p)}
