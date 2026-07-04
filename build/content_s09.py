# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Back in Lesson 1.1 we found button B converted better than A &mdash; but couldn't say whether "
 "the gap was real or luck. ~Hypothesis testing~ is the formal machinery that answers exactly "
 "that question, on a firm logical footing, for almost any comparison you'll ever run. Master "
 "the *logic* here and the specific tests in the next lesson become plug-and-play."))

p.append(B.h2("The logic: assume innocence", kicker="Concept · the framework"))
p.append(B.concept(
 "Hypothesis testing works like a courtroom. We start by assuming *nothing interesting is "
 "happening* and ask the data to prove otherwise &mdash; beyond reasonable doubt.\n\n"
 "- The ~null hypothesis~ (H&#8320;) is the skeptic's default: **no effect, no difference** "
 "(button B is no better than A). This is 'innocent until proven guilty.'\n"
 "- The ~alternative hypothesis~ (H&#8321;) is the claim you'd act on: **there is an effect** "
 "(B differs from A).\n\n"
 "We then assume H&#8320; is true and ask: *if there really were no effect, how surprising would "
 "data like ours be?* If it's surprising enough, we reject H&#8320; in favor of H&#8321;."))
p.append(B.figure(IMG+"s9_logic.png",
 "**The testing pipeline.** State the hypotheses, assume the null, measure how far the data sits "
 "from it, convert that to a p-value, and compare to a threshold &alpha;. Every test you'll learn "
 "is a special case of this flow.",
 "Flowchart of hypothesis testing from hypotheses to decision."))

p.append(B.h2("Test statistic and p-value", kicker="Concept · the evidence"))
p.append(B.concept(
 "Two quantities turn 'is this surprising?' into a number:\n\n"
 "- The ~test statistic~ measures how far your data falls from what H&#8320; predicts, in units "
 "of standard error. A statistic of 2.5 means 'your result is 2.5 standard errors away from "
 "no-effect' &mdash; the same z-score idea from Lesson 1.5.\n"
 "- The ~p-value~ is the punchline: **the probability of seeing data at least as extreme as "
 "yours, if H&#8320; were true.** Small p-value &rarr; your result would be a freak event under "
 "no-effect &rarr; doubt is cast on H&#8320;."))
p.append(B.figure(IMG+"s9_pvalue.png",
 "**The p-value is a tail area.** Under H&#8320; the test statistic clusters around zero. Your "
 "observed value sits far out; the shaded tails beyond it are the p-value &mdash; how often pure "
 "chance would beat your result.",
 "Null distribution with shaded tails beyond the observed statistic representing the p-value."))
p.append(B.callout("pitfall","Three things a p-value is NOT",
 "(1) It is **not** the probability that H&#8320; is true &mdash; it assumes H&#8320; is true to "
 "begin with. (2) It is **not** the size or importance of an effect; a tiny, meaningless "
 "difference can have a tiny p-value with enough data. (3) A large p-value does **not** prove "
 "H&#8320;; 'we couldn't find an effect' is not 'there is no effect.'", "&#10007;"))

p.append(B.h2("Significance and the two ways to be wrong", kicker="Concept · decisions and errors"))
p.append(B.concept(
 "To decide, we set a threshold *before* looking: the ~significance level~ &alpha; (alpha), "
 "almost always 0.05. If p &lt; &alpha; we **reject H&#8320;** and call the result ~statistically "
 "significant~; otherwise we **fail to reject** it. Because we're deciding under uncertainty, two "
 "mistakes are possible:"))
p.append(B.figure(IMG+"s9_errors.png",
 "**The error matrix.** A ~Type I error~ (false positive, rate &alpha;) cries wolf &mdash; "
 "flagging an effect that isn't there. A ~Type II error~ (false negative, rate &beta;) misses a "
 "real effect. You can't drive both to zero at once.",
 "Two-by-two table of Type I and Type II errors versus the truth."))
p.append(B.concept(
 "Choosing &alpha; = 0.05 means accepting a 5% Type I error rate &mdash; we'll wrongly flag a "
 "non-effect about 1 time in 20. The flip side is ~power~ = 1 &minus; &beta;, the chance of "
 "*detecting* a real effect. The two are in tension, mediated by the critical value:"))
p.append(B.figure(IMG+"s9_power.png",
 "**Significance vs. power.** Move the critical line left and you catch more real effects (more "
 "power) but raise false positives (more &alpha;); move it right and the reverse. More data is "
 "what lets you reduce *both* &mdash; the deep reason experiments need enough sample size "
 "(Track 5).",
 "Two distributions showing the trade-off between alpha and power."))

p.append(B.h2("Settle the Lesson 1.1 question", kicker="Worked example"))
p.append(B.concept(
 "Time to answer the cliffhanger: was button B *genuinely* better, or did chance hand us that "
 "lift? This is a ~two-proportion test~ &mdash; comparing two conversion rates. We assume "
 "H&#8320;: the rates are equal, then compute how surprising our observed gap would be."))
_c,_o=_run(r'''
import numpy as np
from scipy import stats

# Conversions from Lesson 1.1 (totals across the three days).
xa, na = 879, 12057      # variant A: 879 purchases of 12,057 visitors
xb, nb = 978, 12006      # variant B: 978 purchases of 12,006 visitors
pa, pb = xa/na, xb/nb

# H0: the two true conversion rates are equal. Pool them for the null SE.
pool = (xa + xb) / (na + nb)
se   = np.sqrt(pool*(1-pool)*(1/na + 1/nb))
z    = (pb - pa) / se                      # test statistic: gap in standard errors
pval = 2 * stats.norm.sf(abs(z))           # two-sided p-value

print(f"A = {pa:.3%}   B = {pb:.3%}   observed lift = {pb-pa:+.3%}")
print(f"test statistic z = {z:.2f}")
print(f"p-value = {pval:.4f}")
print("p < 0.05  ->  reject H0: the lift is unlikely to be pure chance." if pval < 0.05
      else "p >= 0.05 -> not enough evidence to call it real.")
''')
p.append(B.code_example(_c,_o,filename="ab_test.py"))
p.append(B.concept(
 "There's the answer. The gap is about 2.5 standard errors out, with a p-value near 0.012 "
 "&mdash; a result this large would happen by chance only ~1.2% of the time if the buttons were "
 "truly equal. We reject H&#8320;: button B's lift is **statistically significant**. Notice what "
 "we did *not* claim &mdash; that B is *hugely* better, or that we're 98.8% sure it's better. We "
 "claimed exactly one thing: chance alone is an unlikely explanation. (Whether a ~0.9-point lift "
 "is worth shipping is a business question &mdash; that's Track 5.)"))

p.append(B.keypoints([
 "Hypothesis testing assumes the ~null~ (H&#8320;: no effect) and asks whether the data is "
 "surprising enough to reject it.",
 "The ~p-value~ = P(data this extreme | H&#8320; true). Small p &rarr; the null is a poor "
 "explanation. It is **not** P(H&#8320; true) or the effect size.",
 "Reject H&#8320; if p &lt; &alpha; (usually 0.05); otherwise *fail to reject* &mdash; which is "
 "**not** proving H&#8320;.",
 "~Type I~ = false positive (rate &alpha;); ~Type II~ = false negative (rate &beta;); "
 "~power~ = 1 &minus; &beta;.",
 "Statistical significance is about *chance*, not *importance* &mdash; always ask the effect "
 "size too.",
]))

p.append(B.quiz([
 {"q":"A test returns p = 0.03 with &alpha; = 0.05. What is the correct conclusion?",
  "options":[
   {"t":"Reject H0: a result this extreme would occur only ~3% of the time if H0 were true","correct":True,
    "why":"Correct. p = 0.03 < 0.05, so we reject H0. The p-value is the chance of data this "
          "extreme *assuming H0*, and 3% is below our threshold."},
   {"t":"There is a 3% probability that H0 is true",
    "why":"A p-value is not the probability H0 is true. It's computed *assuming* H0 is true: the "
          "chance of data this extreme under that assumption."},
   {"t":"The effect is large and important",
    "why":"Significance is about chance, not magnitude. A tiny effect can be significant with a "
          "big sample; you must check the effect size separately."},
   {"t":"Fail to reject H0",
    "why":"Since p (0.03) is below &alpha; (0.05), we reject H0, not fail to reject."}]},
 {"q":"A medical screen flags a healthy patient as diseased. In hypothesis-testing terms (H0 = "
      "'healthy'), which error is that?",
  "options":[
   {"t":"A Type I error — a false positive, rejecting a true H0","correct":True,
    "why":"Right. H0 ('healthy') is actually true, but the test rejected it (flagged disease). "
          "Rejecting a true null is a Type I error, a false positive."},
   {"t":"A Type II error — a false negative",
    "why":"A Type II error is *failing* to flag a real effect. Here the patient is healthy but "
          "was flagged, which is a false positive (Type I)."},
   {"t":"Correct decision, since the test did something",
    "why":"Flagging a healthy patient is an error, not a correct decision &mdash; specifically a "
          "Type I (false positive)."},
   {"t":"Low statistical power",
    "why":"Power concerns detecting real effects (avoiding Type II errors). Flagging a healthy "
          "patient is a Type I error."}]},
 {"q":"An A/B test on a small sample gives p = 0.20, so the team says 'the two versions are "
      "equal.' What's the flaw?",
  "options":[
   {"t":"'Fail to reject H0' isn't proof of no difference — the test may just lack power to detect "
        "one","correct":True,
    "why":"Exactly. A non-significant result means insufficient evidence, not evidence of no "
          "effect. A small sample has low power, so a real difference could easily go undetected."},
   {"t":"p = 0.20 proves the versions are identical",
    "why":"A large p-value never proves H0. Absence of evidence isn't evidence of absence, "
          "especially with a small, low-power sample."},
   {"t":"They should lower &alpha; to 0.01",
    "why":"Lowering &alpha; makes it *harder* to reject H0, worsening the problem. They need more "
          "data (power), not a stricter threshold."},
   {"t":"p = 0.20 means a 20% effect",
    "why":"A p-value isn't an effect size. 0.20 is the probability of data this extreme under H0, "
          "not a 20% difference."}]},
]))

p.append(B.practice([
 {"q":"Explain a p-value to a non-technical stakeholder in one or two plain sentences, using the "
      "A/B test as the example.",
  "sol":"*'If the new button were really no better than the old one, we'd see a lift this big just "
        "by random luck only about 1 time in 80 (p &asymp; 0.012). That's unlikely enough that we "
        "don't think it's luck &mdash; the button probably does help.'* The key moves: frame it as "
        "the chance of the result *under the assumption of no effect*, avoid jargon, and translate "
        "the probability into an intuitive frequency."},
 {"q":"You run 20 independent A/A tests where there is truly no difference, using &alpha; = 0.05. "
      "About how many do you expect to come out 'significant,' and what does that teach you about "
      "running many tests?",
  "sol":"About **1** (20 × 0.05 = 1). Even with no real effect anywhere, a 5% false-positive rate "
        "means roughly one in twenty tests will look significant by chance. Lesson: if you run "
        "many tests (or peek repeatedly), some will 'hit' purely by luck &mdash; this is the "
        "multiple-comparisons problem, and it's why disciplined experimentation (Track 5) corrects "
        "for it."},
]))

p.append(B.deepdive(
 B.concept(
  "**One-sided vs. two-sided.** Our A/B test was ~two-sided~: we asked whether B *differs* from "
  "A in either direction, splitting the p-value across both tails. A ~one-sided~ test asks only "
  "whether B is *better*, putting all the probability in one tail (and so reaching significance "
  "more easily). Use one-sided only when a difference in the other direction would be "
  "genuinely irrelevant to your decision &mdash; and decide before seeing the data, never after, "
  "or you're just p-hacking.") +
 B.concept(
  "**Significance is not importance.** With a large enough sample, *any* non-zero difference "
  "becomes statistically significant, because the standard error shrinks toward zero. A button "
  "that lifts conversion by 0.001% can have p &lt; 0.001 at scale &mdash; statistically real, "
  "practically worthless. Always pair the p-value with the **effect size** and its confidence "
  "interval, and ask whether the magnitude matters to the business.") +
 B.concept(
  "**The &alpha;–power trade-off and sample size.** Lowering &alpha; cuts false positives "
  "but, holding data fixed, raises false negatives (lower power). The only way to improve both at "
  "once is more data &mdash; which is precisely why experiments need a sample-size calculation "
  "*before* launch. We'll do that math in Track 5 (Experimentation & A/B Testing)."),
 title="Deep dive: one- vs. two-sided tests, significance ≠ importance, and the α–power trade-off"))

p.append(B.callout("note","Interview-ready",
 "The number-one stats interview question is *\"explain a p-value to a non-technical person.\"* "
 "Use a plain-language version of 'the chance of a result this big if there were truly no "
 "effect,' translate the probability into a frequency ('about 1 in 80'), and proactively name a "
 "misconception you're avoiding (it's not the probability the null is true). Then mention you'd "
 "also report the effect size &mdash; significance isn't importance.", "&#9670;"))

LESSONS={"stats-09-hypothesis":"\n".join(p)}
