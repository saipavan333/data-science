# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Here is the single most important theorem in applied statistics. It is the reason we can put "
 "error bars on almost anything, run hypothesis tests, and trust the normal distribution even "
 "when our data is anything but normal. If Lesson 1.6 told you the sample mean wobbles, the "
 "~Central Limit Theorem~ tells you *exactly what shape* that wobble takes &mdash; and the answer "
 "is always the same bell."))

p.append(B.h2("What the theorem actually says", kicker="Concept"))
p.append(B.concept(
 "The ~Central Limit Theorem~ (CLT) says: if you take a large enough random sample and compute "
 "its **mean**, then the sampling distribution of that mean is approximately ~normal~ &mdash; "
 "**no matter what shape the original population has**. Skewed, bimodal, flat, lumpy: it doesn't "
 "matter. Average enough of it and the averages form a bell.\n\n"
 "More precisely, for a sample of size n from a population with mean &mu; and standard deviation "
 "&sigma;, the sample mean x&#772; is approximately Normal(&mu;, &sigma;/&radic;n). Three claims "
 "in one: the averages are **centered at &mu;**, their spread is the **standard error &sigma;/"
 "&radic;n** from last lesson, and their **shape is normal**."))
p.append(B.figure(IMG+"s7_clt.png",
 "**The CLT in one picture.** Three wildly different populations on top &mdash; uniform, skewed, "
 "bimodal. Average samples of 30 from each, many times, and every bottom panel is a bell. The "
 "population's shape is forgotten; only the bell remains.",
 "Three populations of different shapes whose sample means all become normal."))

p.append(B.h2("How big must n be?", kicker="Concept · the rule of thumb"))
p.append(B.concept(
 "The CLT is a statement about *large* samples, so a fair question is *how large?* Watch the "
 "shape emerge as n grows from a single, very skewed population:"))
p.append(B.figure(IMG+"s7_clt_n.png",
 "**Convergence in action.** At n=1 the sample 'mean' is just the population (skewed). By n=5 "
 "it's tamer; by n=30 it's essentially normal &mdash; and notice it also gets narrower, exactly "
 "as SE = &sigma;/&radic;n predicts.",
 "Sample-mean distributions for n=1, 5, 30 becoming progressively normal."))
p.append(B.tip(
 "The famous rule of thumb is **n &ge; 30** for the normal approximation to be good. Treat it as "
 "a guideline, not a law: a mildly skewed population is fine by n=15, while a brutally skewed or "
 "heavy-tailed one (rare giant values) may need hundreds. When in doubt, simulate &mdash; exactly "
 "as the charts above do."))

p.append(B.h2("See it converge in code", kicker="Worked example"))
p.append(B.concept(
 "A single die roll is uniform &mdash; every face equally likely, about as un-bell-shaped as it "
 "gets. Watch what happens to the *average* of several rolls as we increase how many we average, "
 "and confirm the spread follows the standard-error law."))
_c,_o=_run(r'''
import numpy as np
rng = np.random.default_rng(1)

die = np.array([1, 2, 3, 4, 5, 6])          # one roll: flat, not bell-shaped at all
print(f"population: a die roll  (mean={die.mean():.1f}, sd={die.std():.3f})\n")

# Average n rolls, 20,000 times, and look at the distribution of that average.
for n in (1, 2, 10, 30):
    sample_means = rng.choice(die, size=(20_000, n)).mean(axis=1)
    predicted_se = die.std() / np.sqrt(n)
    print(f"n={n:>2}:  mean of averages={sample_means.mean():.3f}   "
          f"sd of averages={sample_means.std():.3f}   (CLT predicts {predicted_se:.3f})")
print("\nThe averages stay centered at 3.5, their spread shrinks like sigma/sqrt(n),")
print("and their shape (not shown here, but see the charts) becomes a bell.")
''')
p.append(B.code_example(_c,_o,filename="clt_dice.py"))
p.append(B.concept(
 "The simulated spread of the averages tracks &sigma;/&radic;n at every sample size, and the "
 "center never budges from 3.5. That is the CLT doing its quiet, universal work &mdash; turning "
 "a flat die into a bell the moment you start averaging."))

p.append(B.callout("pitfall","What the CLT does NOT say",
 "Three traps. (1) It is about the **mean** (or sum), not individual values &mdash; averaging 30 "
 "incomes is normal-ish; a single income is still skewed. (2) It needs the population to have a "
 "**finite variance**; pathological heavy-tailed distributions (like the Cauchy) never settle "
 "into a bell. (3) 'Large n' depends on skew &mdash; n&ge;30 is a guideline, not a guarantee.",
 "&#10007;"))

p.append(B.keypoints([
 "The ~CLT~: the sampling distribution of the **mean** is approximately **normal** for large n, "
 "*whatever* the population shape.",
 "It is centered at &mu; with spread &sigma;/&radic;n &mdash; center, spread, and shape all in "
 "one theorem.",
 "**n &ge; 30** is the rule of thumb; heavier skew needs larger n, mild skew needs less.",
 "It applies to the **mean/sum**, not to individual data points.",
 "The CLT is *why* confidence intervals and most hypothesis tests work &mdash; it is the engine "
 "of the next two lessons.",
]))

p.append(B.quiz([
 {"q":"Daily call-center wait times are heavily right-skewed. You take samples of 50 days and "
      "record each sample's average wait. What shape will those 50-day averages follow?",
  "options":[
   {"t":"Approximately normal — the CLT applies to the sample mean regardless of the skew","correct":True,
    "why":"Correct. n=50 is comfortably large, so by the CLT the distribution of the sample mean "
          "is approximately normal even though individual wait times are skewed."},
   {"t":"Right-skewed, just like the individual wait times",
    "why":"Individual waits are skewed, but the CLT is about their *average*. Averaging 50 of them "
          "produces an approximately normal distribution of means."},
   {"t":"Uniform, because averaging flattens everything",
    "why":"Averaging doesn't flatten to uniform &mdash; it concentrates into a bell centered on "
          "the mean."},
   {"t":"Impossible to say without knowing the exact distribution",
    "why":"That's the power of the CLT: you *don't* need the exact shape. For large n the mean is "
          "approximately normal regardless."}]},
 {"q":"Which of these does the Central Limit Theorem let you treat as approximately normal?",
  "options":[
   {"t":"The average revenue across 200 randomly chosen orders","correct":True,
    "why":"Right. It's an average over a large sample, so the CLT makes its sampling distribution "
          "approximately normal."},
   {"t":"The revenue of one randomly chosen order",
    "why":"A single value isn't an average; the CLT says nothing about it. If order revenue is "
          "skewed, one order stays skewed."},
   {"t":"The list of individual incomes in a city",
    "why":"Those are raw data points, not a sampling distribution of a mean. Incomes are typically "
          "skewed and stay that way."},
   {"t":"Any dataset, as long as it's big",
    "why":"Big raw datasets keep their own shape. The CLT is specifically about the distribution "
          "of a *mean (or sum)* across repeated samples, not raw data."}]},
 {"q":"Why is the Central Limit Theorem so foundational for the rest of statistics?",
  "options":[
   {"t":"It lets us use the normal distribution to put error bars on estimates and run tests, "
        "even when the data isn't normal","correct":True,
    "why":"Exactly. Because sample means are approximately normal, we can compute confidence "
          "intervals and p-values with the normal (and related) distributions regardless of the "
          "raw data's shape &mdash; the basis of the next lessons."},
   {"t":"It proves that all real-world data is normally distributed",
    "why":"It says no such thing &mdash; raw data is often non-normal. It's about the distribution "
          "of the *mean*, which is what makes it useful."},
   {"t":"It removes the need to take samples at all",
    "why":"It doesn't eliminate sampling; it describes how sample means behave, which is why "
          "sampling works."},
   {"t":"It guarantees larger samples are always unbiased",
    "why":"Bias comes from *how* you sample, not size; the CLT is about the shape and spread of "
          "the sampling distribution, not bias."}]},
]))

p.append(B.practice([
 {"q":"A population has mean &mu;=100 and SD &sigma;=40. You take samples of size 64. Describe the "
      "sampling distribution of the mean: its center, its spread, and its shape.",
  "sol":"By the CLT the sample mean is approximately **Normal**, **centered at &mu; = 100**, with "
        "**standard error &sigma;/&radic;n = 40/&radic;64 = 40/8 = 5**. So x&#772; &asymp; "
        "Normal(100, 5). Using the empirical rule, about 95% of sample means would fall within "
        "&plusmn;2&times;5 = &plusmn;10 of 100, i.e. between 90 and 110."},
 {"q":"A friend says: 'I averaged 5 values from a super-skewed distribution, so by the CLT my "
      "average is perfectly normal.' What's wrong, and what would you change?",
  "sol":"Two issues. First, n=5 is small, and for a *heavily* skewed population the CLT hasn't "
        "kicked in yet &mdash; the distribution of the average is still noticeably skewed. Second, "
        "'perfectly' overstates it; the CLT gives an *approximation* that improves with n. The fix: "
        "increase the sample size (n&ge;30 as a starting point, more for strong skew), or simulate "
        "to check the shape rather than assuming it."},
]))

p.append(B.deepdive(
 B.concept(
  "**Why does it work?** Intuitively, a sample mean is a sum of many small, independent "
  "contributions. Each value nudges the average up or down a little; with many values, the "
  "up-nudges and down-nudges combine, and the *ways* to land near the middle vastly outnumber the "
  "ways to land at an extreme (you'd need almost all values to be high at once). That "
  "combinatorial pile-up in the middle is the bell curve. The same logic explains why so many "
  "natural quantities &mdash; heights, measurement errors, total noise &mdash; are normal: they "
  "are themselves sums of many small independent effects.") +
 B.concept(
  "**The fine print.** The CLT needs the contributions to be (roughly) independent and to come "
  "from a distribution with **finite variance**. The ~Cauchy distribution~ &mdash; a bell-looking "
  "curve with tails so heavy its variance is infinite &mdash; breaks the theorem: averaging "
  "Cauchy values gives you back a Cauchy, never a normal. Such distributions are rare in practice "
  "but are a favorite interview curveball, and a reminder that 'just average it' has limits.") +
 B.concept(
  "**The payoff.** Because x&#772; is approximately Normal(&mu;, &sigma;/&radic;n), we can say "
  "things like 'about 95% of sample means fall within 2 standard errors of the truth.' Flip that "
  "around and you get a ~confidence interval~ &mdash; the subject of the very next lesson."),
 title="Deep dive: why the bell appears, and the one distribution that breaks the CLT"))

p.append(B.callout("note","Interview-ready",
 "*\"Explain the Central Limit Theorem and why it matters\"* is a staple. Nail it in two "
 "sentences: the distribution of the sample mean becomes approximately normal as the sample grows, "
 "regardless of the population's shape, centered at &mu; with spread &sigma;/&radic;n. It matters "
 "because it lets us use normal-based confidence intervals and tests on almost any data. Mention "
 "n&ge;30 as a rule of thumb and that it's about the *mean*, not individual values.",
 "&#9670;"))

LESSONS={"stats-07-clt":"\n".join(p)}
