# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Most A/B \"wins\" that fail to replicate didn't die in the math &mdash; they died in a **trap**. "
 "The statistics can be flawless and the conclusion still wrong, because the experiment was peeked "
 "at, sliced until something sparkled, or pooled across groups that shouldn't be pooled. This lesson "
 "is the catalogue of ways experiments lie, and how seasoned analysts refuse to be fooled. Knowing "
 "these is what makes you *trustworthy* &mdash; and they're the \"what could go wrong?\" half of the "
 "interview."))

p.append(B.h2("Peeking: the slow-motion false positive", kicker="Pitfall 1")
)
p.append(B.concept(
 "The tempting sin: watch the p-value daily and stop the moment it dips below 0.05. The problem is "
 "that with no real effect, the p-value **wanders randomly**, and a random walk will cross 0.05 "
 "*eventually* if you keep looking. So ~peeking~ and stopping on the first significant result turns "
 "a 5% false-positive rate into something like 20&ndash;30%. Prove it to yourself: run many "
 "experiments with **no real difference** and check the false-positive rate of a **single** look at "
 "the end &mdash; it should sit right at the nominal 5%:"))
_c,_o=_run(r'''
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)

n_exp, n, p = 4000, 3000, 0.10   # 4000 A/A experiments, no real effect (both arms 10%)

xa = rng.binomial(n, p, n_exp)   # conversions, control
xb = rng.binomial(n, p, n_exp)   # conversions, treatment (same true rate!)
pool = (xa + xb) / (2*n)
se = np.sqrt(pool*(1-pool) * 2/n)
z = (xb - xa) / n / se
pval = 2 * (1 - stats.norm.cdf(np.abs(z)))

print(f"single look at the end -> false-positive rate: {(pval < 0.05).mean():.1%}")
print("(peeking every day and stopping at the first p<0.05 would push this toward ~25%)")
''')
p.append(B.code_example(_c,_o,filename="peeking.py"))
p.append(B.concept(
 "A single, planned look is **calibrated** &mdash; about 5% false positives, exactly as advertised. "
 "Peeking breaks that guarantee. Fix the sample size in advance and look once; if you genuinely need "
 "to stop early, use methods **built** for it (~sequential testing~ / alpha-spending)."))

p.append(B.h2("p-hacking and the garden of forking paths", kicker="Pitfall 2")
)
p.append(B.pitfall(
 "~p-hacking~ is torturing the data until it confesses: try 15 metrics, 8 segments, 3 date ranges, "
 "and \"with and without outliers,\" then report whatever crossed 0.05. Each choice is a coin flip, "
 "so *somewhere* in that garden of forking paths a false positive is almost guaranteed. A close "
 "cousin is ~HARKing~ (Hypothesizing After the Results are Known) &mdash; inventing the hypothesis "
 "to fit whatever you found, then presenting it as if you'd predicted it. The antidote is "
 "**pre-registration**: write down the primary metric, the segments, and the analysis **before** you "
 "see the data, and treat anything discovered afterwards as a *hypothesis for a new test*, not a "
 "result."))

p.append(B.h2("Simpson's paradox: pooling can flip the answer", kicker="Pitfall 3")
)
p.append(B.concept(
 "The most mind-bending trap: a trend that holds in **every** subgroup can **reverse** when you pool "
 "the groups together. Below, the outcome falls with X inside *each* segment &mdash; but ignore the "
 "segments and it appears to *rise*:"))
p.append(B.figure(IMG+"s_ab_simpson.png",
 "**Simpson's paradox.** Within Segment A and within Segment B the trend goes **down** (the solid "
 "lines). But pool all the points and the dashed line goes **up** &mdash; because Segment B sits "
 "higher *and* further right. The aggregate reverses the truth.",
 "A scatter where each segment trends downward but the pooled trend line goes upward."))
p.append(B.concept(
 "In an A/B test this bites when your arms have a **different mix** of users. If treatment happened "
 "to get more of a naturally-high-converting segment, it can look like a winner overall while losing "
 "in every segment (or vice versa). This is exactly why the ~SRM~ check (Lesson 6.2) and "
 "segment-level sanity checks matter: **before trusting a pooled number, confirm the groups are "
 "comparable and the effect is consistent across segments.** When in doubt, trust the within-segment "
 "story over the aggregate."))

p.append(B.h2("Novelty, primacy, and Twyman's law", kicker="Pitfalls 4 & 5")
)
p.append(B.concept(
 "Two more:\n\n"
 "- ~Novelty effect~: a new feature gets a temporary bump *because it's new* &mdash; users poke at "
 "it out of curiosity &mdash; and the lift fades. Its mirror, the ~primacy effect~, is an initial "
 "dip from users annoyed by change, which then recovers. A test that's **too short** measures the "
 "curiosity spike, not the steady state. Run long enough for the curve to flatten, and check whether "
 "the effect holds for users on their *tenth* exposure, not just their first.\n"
 "- ~Twyman's law~: *\"any figure that looks interesting or surprising is probably wrong.\"* A "
 "shocking +40% lift is far more likely a tracking bug, a broken split, or bot traffic than a real "
 "miracle. Great experimenters greet surprising wins with **suspicion first** &mdash; re-check the "
 "pipeline, the SRM, and an A/A test &mdash; and only then celebrate."))

p.append(B.h2("Your turn — measure the honest false-positive rate", kicker="Interactive lab"))
p.append(B.pylab(
 "Simulate **A/A tests** &mdash; experiments where the two arms are **truly identical** (both "
 "convert at 10%). Over `n_exp` experiments with a **single** look each, compute the fraction that "
 "come out \"significant\" (p &lt; 0.05) and assign it to **`answer`**, rounded to 2 decimals. What "
 "number should an honest, single-look test produce?",
 "import numpy as np\n"
 "from scipy import stats\n"
 "rng = np.random.default_rng(1)\n"
 "n_exp, n, p = 4000, 3000, 0.10\n"
 "xa = rng.binomial(n, p, n_exp)\n"
 "xb = rng.binomial(n, p, n_exp)\n",
 "pool = (xa + xb) / (2*n)\n"
 "se = np.sqrt(pool*(1-pool) * 2/n)\n"
 "z = (xb - xa) / n / se\n"
 "pval = 2 * (1 - stats.norm.cdf(np.abs(z)))\n"
 "answer = round(float((pval < 0.05).mean()), 2)",
 starter="# xa, xb are A/A conversions (both true rate 0.10); numpy + scipy loaded\nanswer = ",
 hint="Compute the p-value for each experiment (pooled SE, two-sided), then take "
      "`(pval < 0.05).mean()` and round to 2 decimals.",
 title="Lab — a single look is calibrated",
 preview="`xa`, `xb` (A/A conversions), `n`, `n_exp` loaded; numpy + scipy imported. First Run loads scipy.",
 explain="It lands near 0.05 &mdash; a properly-run single-look test has exactly the false-positive "
         "rate you signed up for. Peeking and stopping early is what breaks that guarantee."))

p.append(B.keypoints([
 "~Peeking~ (checking repeatedly and stopping at the first p&lt;0.05) inflates false positives to "
 "~25%+; a **single planned look** is calibrated at 5%. Use sequential methods if you must stop "
 "early.",
 "~p-hacking~ / ~HARKing~: trying many metrics/segments/cutoffs and reporting whatever's significant. "
 "Fix: **pre-register** the primary metric and analysis.",
 "~Simpson's paradox~: a within-group trend can **reverse** when pooled &mdash; check the arms are "
 "comparable (SRM) and the effect is consistent across segments.",
 "~Novelty~/~primacy~ effects fade or reverse; run long enough to reach steady state.",
 "~Twyman's law~: a surprising result is probably a **bug** &mdash; re-check SRM, an A/A test, and "
 "the pipeline before believing it.",
]))

p.append(B.quiz([
 {"q":"You check your test's p-value every morning and plan to stop as soon as it's below 0.05. "
      "Why is that dangerous?",
  "options":[
   {"t":"The p-value wanders randomly, so with repeated looks it will cross 0.05 by chance even with "
        "no real effect — inflating false positives","correct":True,
    "why":"Correct. Each peek is another chance for the random p-value to dip below 0.05. Stopping at "
          "the first dip turns a 5% error rate into ~25%. Fix the sample size and look once (or use "
          "sequential methods)."},
   {"t":"It's fine — early significance just means a strong effect",
    "why":"Early results are the noisiest, and stopping on the first lucky dip is exactly how you "
          "manufacture false positives."},
   {"t":"Checking daily uses too much compute",
    "why":"The problem is statistical (inflated false positives from repeated looks), not "
          "computational."},
   {"t":"P-values can't be computed before the test ends",
    "why":"They can be computed anytime; the danger is *acting* on repeated peeks."}]},
 {"q":"Treatment beats control in every single user segment, but loses in the pooled numbers. What's "
      "going on?",
  "options":[
   {"t":"Simpson's paradox — the arms likely have a different segment mix, so pooling reverses the "
        "within-segment truth","correct":True,
    "why":"Correct. When the groups' composition differs (e.g., treatment got more low-converting "
          "users), the aggregate can flip the consistent within-segment result. Check SRM and trust "
          "the segment-level story."},
   {"t":"The segments must be mislabeled",
    "why":"No mislabeling needed — this is the genuine Simpson's paradox, driven by differing segment "
          "sizes/mix between arms."},
   {"t":"It's impossible; the pooled result must match the segments",
    "why":"It's famously possible: a trend in every subgroup can reverse when pooled. That's the whole "
          "paradox."},
   {"t":"Treatment is simply better; ignore the segments",
    "why":"The reverse — when pooled and segmented disagree, the segment-level (comparable) view is "
          "usually the trustworthy one; investigate the mix."}]},
 {"q":"Your test shows a stunning +35% lift on day one. Best first move?",
  "options":[
   {"t":"Be suspicious (Twyman's law) — re-check SRM, run an A/A / pipeline audit; it's likely a bug "
        "or novelty spike","correct":True,
    "why":"Correct. Surprising results are more often instrumentation errors, broken splits, or "
          "day-one novelty than real miracles. Verify the plumbing and let it reach steady state "
          "before believing it."},
   {"t":"Ship immediately to capture the huge win",
    "why":"A day-one +35% is a red flag, not a green light — likely a bug or novelty effect that will "
          "evaporate. Verify first."},
   {"t":"Assume the effect will only grow",
    "why":"Novelty effects typically *fade*, and outsized early numbers usually regress. Don't "
          "extrapolate a suspicious spike."},
   {"t":"Conclude the feature is worthless",
    "why":"You can't conclude anything yet — the point is to *investigate* the surprising number "
          "before drawing any conclusion."}]},
]))

p.append(B.practice([
 {"q":"A colleague ran a 3-day test, saw p = 0.048 on the afternoon of day 3, stopped, and declared a "
      "win. List two things wrong and what you'd do.",
  "sol":"Two problems: **(1) peeking / early stopping** &mdash; stopping the instant p dipped below "
        "0.05 (especially after watching it) inflates the false-positive rate well beyond 5%, so p = "
        "0.048 isn't trustworthy; **(2) too short** &mdash; three days likely captures a **novelty** "
        "spike, not the steady-state effect, and probably didn't reach the planned sample size "
        "(underpowered). What I'd do: honour a **pre-set** sample size / duration computed from a "
        "power analysis, run to it without acting on interim peeks, verify **SRM**, and only then "
        "read the result once &mdash; reporting the confidence interval, not just a borderline p."},
 {"q":"Explain how you'd design an experiment up front to make p-hacking essentially impossible for "
      "yourself.",
  "sol":"**Pre-register** everything before launch: the single **primary metric** and its success "
        "threshold (MDE), the exact **analysis** (test, one/two-sided), the **sample size / "
        "duration** from a power calc, and any **segments** you'll look at (with a multiple-comparison "
        "correction if more than one). Lock the ~test set~ of decisions before seeing data; run "
        "SRM/A-A trust checks; and treat *anything* discovered afterwards as a **new hypothesis** to "
        "be confirmed in a fresh experiment, never as a result from this one. With the choices fixed "
        "in advance, there are no forking paths left to exploit."},
]))

p.append(B.deepdive(
 B.concept(
  "**Why peeking inflates error, precisely.** Under the null, the test statistic follows a random "
  "walk. A single fixed look controls the false-positive rate at &alpha; because you evaluate the "
  "walk **once**. Every additional look is another opportunity for the walk to breach the threshold, "
  "so the *family-wise* error compounds &mdash; roughly, k independent looks push the false-positive "
  "rate toward `1 - (1-&alpha;)^k`. Principled fixes spend the &alpha; budget across looks: "
  "~alpha-spending~ (O'Brien-Fleming, Pocock) or ~group-sequential~ designs let you stop early while "
  "keeping the overall error at 5%. This is a whole subfield &mdash; the lesson is: don't improvise "
  "early stopping.") +
 B.concept(
  "**Interference breaks the core assumption.** Standard analysis assumes one user's treatment "
  "doesn't affect another's outcome (~SUTVA~). In social networks, marketplaces, and anything with "
  "shared resources, that fails &mdash; treating some users spills onto controls (they see treated "
  "friends' posts; treated buyers deplete shared inventory). The result is a biased effect estimate "
  "no sample size can fix. Remedies: **cluster-level** randomization (by region, community, or "
  "seller) so spillovers stay within a bucket, or specialised network-experiment designs.") +
 B.concept(
  "**The meta-pitfall: the winner's curse and publication bias, in-house.** Teams launch dozens of "
  "experiments and ship the ones that \"won.\" But among many noisy tests, the ones that cross the "
  "line are disproportionately the ones that got **lucky-high** &mdash; so shipped effects are "
  "systematically **overstated**, and aggregate impact never quite adds up to the sum of the wins. "
  "Mature programs counter this with **replication** of important wins, **holdback** groups that keep "
  "a slice of users on the old experience to measure long-run cumulative impact, and healthy "
  "skepticism toward any single significant result."),
 title="Deep dive: alpha-spending, interference/SUTVA, and the in-house winner's curse"))

p.append(B.callout("note","Interview-ready",
 "\"What could go wrong with this experiment?\" is a guaranteed question. Have the catalogue ready: "
 "**peeking** (inflates false positives &mdash; look once or go sequential), **p-hacking/multiple "
 "comparisons** (pre-register), **Simpson's paradox** (check SRM + segments), **novelty/primacy** "
 "(run to steady state), and **Twyman's law** (verify surprising results). Naming these unprompted "
 "signals real experience.", "&#9670;"))

LESSONS={"ab-05-pitfalls":"\n".join(p)}
print("content_ab05 OK — chars:", len(LESSONS["ab-05-pitfalls"]))
