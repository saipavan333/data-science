# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "The test finished and B is up 1.1%. Ship it? Not so fast. Reading an experiment correctly is where "
 "careful analysts earn their keep: separating a **real** effect from noise, a ~statistically "
 "significant~ result from a ~practically~ meaningful one, and resisting the urge to slice the data "
 "until something looks good. This lesson turns raw counts into a decision you can defend &mdash; "
 "and it's the analysis half of every A/B-test interview question."))

p.append(B.h2("The two-proportion test", kicker="Concept"))
p.append(B.concept(
 "For a conversion-rate test you have four numbers: users and conversions in each arm. The analysis "
 "asks: is the gap between the two rates bigger than you'd expect from chance alone? That's a "
 "~two-proportion z-test~ &mdash; the same hypothesis-testing logic from Lesson 4.8, applied to two "
 "rates. You compute the difference, its ~standard error~, turn that into a z-score and a ~p-value~, "
 "and &mdash; most importantly &mdash; a ~confidence interval~ on the lift itself:"))
_c,_o=_run(r'''
import numpy as np
from scipy import stats

# observed results of the experiment
nA, xA = 12000, 1140   # control:   12,000 users, 1,140 converted
nB, xB = 12000, 1272   # treatment: 12,000 users, 1,272 converted
pA, pB = xA/nA, xB/nB
diff = pB - pA

# p-value: pooled standard error (assumes the null — no difference)
pool = (xA + xB) / (nA + nB)
se_test = np.sqrt(pool*(1-pool) * (1/nA + 1/nB))
z = diff / se_test
pval = 2 * (1 - stats.norm.cdf(abs(z)))

# confidence interval on the lift: unpooled standard error
se_ci = np.sqrt(pA*(1-pA)/nA + pB*(1-pB)/nB)
lo, hi = diff - 1.96*se_ci, diff + 1.96*se_ci

print(f"control {pA:.1%}   treatment {pB:.1%}   lift {diff:+.1%}")
print(f"p-value: {pval:.4f}   ->  {'significant' if pval < 0.05 else 'not significant'} at 0.05")
print(f"95% CI on the lift: [{lo:+.1%}, {hi:+.1%}]")
''')
p.append(B.code_example(_c,_o,filename="analyze_ab.py"))
p.append(B.concept(
 "A +1.1% lift, p = 0.005 (unlikely to be chance), and a 95% CI of roughly [+0.3%, +1.9%] that "
 "**excludes zero** &mdash; a real, positive effect. Notice we report the **interval**, not just the "
 "point estimate: the truth is plausibly anywhere in that range, and the width tells you how precise "
 "your estimate is."))

p.append(B.h2("The confidence interval is the real answer", kicker="Concept · report this, not just p")
)
p.append(B.figure(IMG+"s8_ci_concept.png",
 "**A confidence interval is the honest summary of an experiment.** Each line is a plausible-values "
 "range for the true effect. If your lift's CI sits entirely above zero, you have a real positive "
 "effect; if it straddles zero, the test is inconclusive; and a wide CI means \"we don't yet know "
 "precisely &mdash; maybe run longer.\"",
 "Many confidence intervals around a true value, most capturing it, illustrating what 95% confidence means."))
p.append(B.concept(
 "A p-value alone throws away the most useful information &mdash; *how big* is the effect and how "
 "sure are we? The ~confidence interval~ on the lift keeps both. Three readings: **CI entirely above "
 "0** &rarr; a real positive effect (ship, if it clears your bar); **CI straddles 0** &rarr; "
 "inconclusive (you couldn't distinguish it from no effect); **CI very wide** &rarr; imprecise, "
 "likely underpowered, consider running longer. Report the interval, and the decision usually makes "
 "itself."))

p.append(B.h2("Statistical vs practical significance", kicker="Concept · the trap of huge N")
)
p.append(B.pitfall(
 "With a big enough sample, **even a trivial effect becomes statistically significant** &mdash; "
 "because the standard error shrinks toward zero, a +0.01% lift can hit p < 0.05. But a 0.01% lift "
 "may not be worth the engineering cost, the added complexity, or the guardrail risk. ~Statistical "
 "significance~ says \"the effect is probably real\"; ~practical significance~ asks \"is it big "
 "enough to *matter*?\" Always compare the confidence interval against a pre-set **practical "
 "threshold** (the MDE from Lesson 6.3). A result can be significant and useless, or non-significant "
 "yet promising &mdash; the p-value can't tell those apart, but the effect-size interval can."))

p.append(B.h2("Don't torture the data: multiple testing", kicker="Concept")
)
p.append(B.concept(
 "The other way to fool yourself is to test **many** things and celebrate whatever crossed 0.05. "
 "Check 20 metrics, or slice by 10 user segments, and at &alpha; = 0.05 you *expect* about one false "
 "positive by pure chance &mdash; the ~multiple comparisons~ problem. Defences: decide your **one** "
 "primary metric and any segments **before** the test (pre-registration); and if you must test many, "
 "**correct** the threshold (e.g. ~Bonferroni~: divide &alpha; by the number of tests). \"We dug "
 "around and found a significant lift in left-handed users in Canada\" is almost always noise, not a "
 "discovery."))

p.append(B.h2("Your turn — analyze a real result", kicker="Interactive lab"))
p.append(B.pylab(
 "An experiment observed **control: 8,000 users, 640 conversions** and **treatment: 8,000 users, "
 "720 conversions**. Run a two-proportion z-test (pooled standard error) and assign the **p-value** "
 "to **`answer`**, rounded to 4 decimals. Then judge: significant at 0.05?",
 "import numpy as np\n"
 "from scipy import stats\n"
 "nA, xA = 8000, 640\n"
 "nB, xB = 8000, 720\n",
 "pA, pB = xA/nA, xB/nB\n"
 "pool = (xA + xB) / (nA + nB)\n"
 "se = np.sqrt(pool*(1-pool) * (1/nA + 1/nB))\n"
 "z = (pB - pA) / se\n"
 "answer = round(float(2 * (1 - stats.norm.cdf(abs(z)))), 4)",
 starter="# nA,xA (control) and nB,xB (treatment) are loaded; numpy + scipy.stats imported\nanswer = ",
 hint="Rates `pA=xA/nA`, `pB=xB/nB`; pooled `pool=(xA+xB)/(nA+nB)`; "
      "`se=np.sqrt(pool*(1-pool)*(1/nA+1/nB))`; `z=(pB-pA)/se`; "
      "`p=2*(1-stats.norm.cdf(abs(z)))`.",
 title="Lab — is the lift significant?",
 preview="`nA,xA,nB,xB` loaded; numpy + scipy imported. First Run loads scipy (~15s).",
 explain="8% vs 9% on 8,000 users each gives a small p-value &mdash; a real, if modest, lift. Report "
         "the confidence interval too, and check the lift clears your practical bar before shipping."))

p.append(B.keypoints([
 "Analyze a conversion test with a ~two-proportion z-test~: difference in rates &divide; its "
 "~standard error~ &rarr; z &rarr; ~p-value~.",
 "**Report the ~confidence interval~ on the lift**, not just p: CI above 0 = real effect; CI "
 "straddling 0 = inconclusive; wide CI = imprecise.",
 "~Statistical significance~ (probably real) &ne; ~practical significance~ (big enough to matter) "
 "&mdash; with huge N, trivial effects go significant. Compare the CI to your practical threshold.",
 "~Multiple comparisons~: test 20 metrics/segments and ~1 crosses 0.05 by chance. Pre-register the "
 "primary metric; correct (~Bonferroni~) if testing many.",
 "A result can be significant and useless, or non-significant yet promising &mdash; the effect-size "
 "interval, not the p-value, tells them apart.",
]))

p.append(B.quiz([
 {"q":"Your A/B test shows a +0.02% lift, p = 0.001, on 50 million users. Ship it?",
  "options":[
   {"t":"Probably not — it's statistically significant but likely not practically significant; check "
        "if 0.02% clears your value/cost threshold","correct":True,
    "why":"Correct. Huge samples make tiny effects significant. A +0.02% lift may not justify the "
          "engineering, complexity, or guardrail risk. Statistical significance isn't the same as "
          "'worth shipping'; compare the effect to a practical threshold."},
   {"t":"Yes — p = 0.001 is extremely significant",
    "why":"A tiny p just says the effect is probably real, not that it's *big enough to matter*. "
          "0.02% may be practically worthless despite the tiny p."},
   {"t":"No — p must be below 0.0001 to ship anything",
    "why":"There's no universal p threshold for shipping. The issue here is practical significance "
          "(effect size), not a stricter p cutoff."},
   {"t":"Yes, because the sample is large",
    "why":"A large sample makes even trivial effects significant — that's the reason for caution, not "
          "for shipping."}]},
 {"q":"Why report the confidence interval on the lift, not just the p-value?",
  "options":[
   {"t":"The CI shows the effect's size and precision — whether it clears a practical bar and how "
        "sure you are — which p alone hides","correct":True,
    "why":"Correct. p only says 'probably not zero'. The CI tells you the plausible range of the true "
          "lift (is it big enough? how precise?), which is what the decision actually depends on."},
   {"t":"The CI is easier to compute than a p-value",
    "why":"Both come from the same standard error; ease isn't the point. The CI simply carries more "
          "decision-relevant information (size + precision)."},
   {"t":"A CI can never contain zero",
    "why":"A CI absolutely can contain zero — that's exactly the 'inconclusive' case. Its value is "
          "showing the effect's magnitude and uncertainty."},
   {"t":"Because p-values are always wrong",
    "why":"p-values aren't wrong, just incomplete. The CI complements them with effect size and "
          "precision."}]},
 {"q":"An analyst tests 20 secondary metrics with no correction and reports the two that hit p < 0.05 "
      "as wins. What's the problem?",
  "options":[
   {"t":"Multiple comparisons: with 20 tests at 0.05, ~1 false positive is expected by chance, so the "
        "'wins' may be noise","correct":True,
    "why":"Correct. Each test has a 5% false-positive chance; run 20 and you expect about one to cross "
          "0.05 even with no real effect. Pre-register the primary metric or correct alpha "
          "(Bonferroni) before claiming wins."},
   {"t":"Nothing — more metrics means more evidence",
    "why":"More *unplanned* tests means more chances for false positives, not more evidence. It "
          "inflates the family-wise error rate."},
   {"t":"The metrics should have been tested one experiment at a time",
    "why":"You can measure several metrics, but you must account for the multiple comparisons "
          "(pre-registration / correction), not treat each crossing of 0.05 as a discovery."},
   {"t":"0.05 is too strict a threshold",
    "why":"The threshold isn't too strict; the issue is testing many things and cherry-picking, which "
          "*loosens* the effective error rate."}]},
]))

p.append(B.practice([
 {"q":"An experiment reports: lift +0.4%, p = 0.21, 95% CI on the lift = [&minus;0.2%, +1.0%]. Write "
      "the one-paragraph readout you'd send your PM.",
  "sol":"\"The test is **inconclusive**. B is nominally +0.4% but that's not statistically significant "
        "(p = 0.21), and the 95% confidence interval &mdash; [&minus;0.2%, +1.0%] &mdash; **includes "
        "zero**, so we can't rule out no effect (or even a small negative one). The interval is also "
        "fairly wide, which suggests we're **underpowered**: we simply don't have enough data to tell "
        "a small win from nothing. Recommendation: either run longer to tighten the interval, or "
        "accept that any real effect is likely small (&le; ~1%) and decide whether that's worth "
        "shipping on other grounds.\" No overclaiming, effect size front and centre."},
 {"q":"Explain why a +5% lift with p = 0.30 and a +0.1% lift with p = 0.001 can *both* be the wrong "
      "thing to ship, for opposite reasons.",
  "sol":"The **+5%, p = 0.30** result is practically large but **not statistically reliable** &mdash; "
        "it might be a noisy fluke (probably underpowered), so shipping risks chasing a mirage; you'd "
        "run longer to confirm. The **+0.1%, p = 0.001** result is statistically rock-solid but "
        "**practically trivial** &mdash; a 0.1% gain may not justify the cost or complexity, so "
        "shipping spends effort on nothing. One fails statistical significance, the other fails "
        "practical significance; a good decision needs **both** &mdash; a real *and* meaningful "
        "effect."},
]))

p.append(B.deepdive(
 B.concept(
  "**Why two different standard errors.** For the **p-value** you assume the null is true (no "
  "difference), so you estimate one shared conversion rate and use a ~pooled~ standard error. For the "
  "**confidence interval** you're estimating the *actual* difference, so you use each group's own "
  "rate &mdash; an ~unpooled~ standard error. They're usually close, but using the right one for each "
  "purpose is the mark of someone who understands the machinery rather than copying a formula. For "
  "**ratio** or per-user metrics (revenue per user), the variance is trickier and needs the ~delta "
  "method~ or bootstrapping.") +
 B.concept(
  "**One-sided vs two-sided, and the sequential temptation.** Use a **two-sided** test by default: a "
  "change can hurt as easily as help, and you want to detect a *regression* too. A one-sided test "
  "doubles your effective false-positive rate for the direction you favour &mdash; a subtle form of "
  "p-hacking. And resist analysing early and often on a fixed-horizon test; if you truly need to peek "
  "and stop early, use methods **designed** for it (~sequential testing~, ~alpha-spending~, or "
  "Bayesian approaches), which control the error rate under repeated looks.") +
 B.concept(
  "**Trustworthiness before conclusions.** Before believing any effect, seasoned experimenters run a "
  "battery of sanity checks: the ~SRM~ (Lesson 6.2), a pre-period **A/A test** (split identically "
  "with *no* change &mdash; you should see no effect; if you do, your pipeline is biased), and "
  "checks that the effect is stable over time and consistent across major segments (a huge effect in "
  "one tiny segment driving the whole result is a red flag). Twyman's law: *any figure that looks "
  "interesting or surprising is probably wrong* &mdash; verify the plumbing before you trust the "
  "number."),
 title="Deep dive: pooled vs unpooled SE, one- vs two-sided & sequential, and trustworthiness checks"))

p.append(B.callout("note","Interview-ready",
 "Show judgement, not just a p-value: analyze with a **two-proportion test**, but **report the "
 "confidence interval on the lift**; separate **statistical** significance (probably real) from "
 "**practical** significance (big enough to matter &mdash; huge N makes trivial effects significant); "
 "and call out **multiple comparisons** when someone slices until something crosses 0.05. Bonus: A/A "
 "tests and SRM as trust checks.", "&#9670;"))

LESSONS={"ab-04-analyze":"\n".join(p)}
print("content_ab04 OK — chars:", len(LESSONS["ab-04-analyze"]))
