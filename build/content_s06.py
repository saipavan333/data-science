# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Every number you will ever report &mdash; an average order value, a conversion rate, a churn "
 "figure &mdash; is computed from a **sample**, not the whole world. Pull a different sample and "
 "the number shifts. If you can't say *how much* it would shift, you can't say whether a "
 "difference is real. This lesson makes that wobble precise, and it's the hinge the rest of "
 "statistics swings on."))

p.append(B.h2("Population, sample, parameter, statistic", kicker="Concept · four words"))
p.append(B.concept(
 "Four terms, used precisely from here on:\n\n"
 "- The ~population~ is everyone or everything you care about (all your customers, all possible "
 "visitors). Usually too big to measure fully.\n"
 "- A ~sample~ is the subset you actually observe.\n"
 "- A ~parameter~ is a number describing the *population* &mdash; the true mean &mu; (mu) or true "
 "standard deviation &sigma; (sigma). It is **fixed but unknown**.\n"
 "- A ~statistic~ is the matching number computed from your *sample* &mdash; the sample mean "
 "x&#772; (x-bar) or sample SD s. It is **known but varies** from sample to sample.\n\n"
 "The entire game of inference is using the statistic you *can* see to estimate the parameter "
 "you *can't*, while being honest about the gap."))
p.append(B.figure(IMG+"s6_popsample.png",
 "**The inference loop.** You can't measure the population, so you take a random sample, compute "
 "a statistic, and reason back to the parameter &mdash; carrying an estimate of your uncertainty "
 "the whole way.",
 "Diagram: population to sample to inference and back."))

p.append(B.h2("Sampling variability and the sampling distribution", kicker="Concept · the key idea"))
p.append(B.concept(
 "Here's the thought experiment that unlocks everything. Imagine repeating your study many times "
 "&mdash; each time drawing a fresh sample of the same size and computing its mean. Those means "
 "won't all be equal; they'll scatter. The distribution of a statistic over all those imagined "
 "repetitions is called the ~sampling distribution~.\n\n"
 "It has two beautiful properties, shown below: it is **centered on the true parameter** (so the "
 "sample mean is right *on average*), and it is **much narrower than the population** (averaging "
 "cancels out individual extremes)."))
p.append(B.figure(IMG+"s6_sampling_dist.png",
 "**Left:** a skewed population. **Right:** the distribution of the sample mean for samples of "
 "30. It clusters tightly around the true mean even though individual values are all over the "
 "place. That tightening is what lets a sample speak for the whole.",
 "A skewed population beside the much narrower distribution of its sample mean."))

p.append(B.h2("Standard error: the size of the wobble", kicker="Concept · the number that matters"))
p.append(B.concept(
 "The spread of that sampling distribution has a name: the ~standard error~ (SE). It measures how "
 "much your statistic would bounce around from sample to sample. For a sample mean it has a "
 "clean formula:"))
p.append(B.formula(
 'SE = <sup>&sigma;</sup>&frasl;<sub>&radic;n</sub>',
 "the population SD divided by the square root of the sample size n"))
p.append(B.warn(
 "Do not confuse ~standard deviation~ and ~standard error~. The **SD** describes the spread of "
 "individual data points (how varied are customers?). The **SE** describes the spread of a "
 "*statistic* (how much would the sample *mean* wobble?). SE = SD / &radic;n, so the SE is always "
 "smaller, and it shrinks as you collect more data.", "&#9650;"))
p.append(B.figure(IMG+"s6_se_vs_n.png",
 "**The &radic;n law and its cruel arithmetic.** Error falls as 1/&radic;n, so to *halve* your "
 "uncertainty you need *four times* the data. This is why precision gets expensive fast.",
 "Curve of standard error decreasing as sample size grows."))

p.append(B.h2("See it in code", kicker="Worked example"))
p.append(B.concept(
 "Let's make the wobble concrete. We'll build a known population, take one realistic sample, then "
 "(because it's a simulation) cheat by repeating the study 1,000 times to watch the sample mean "
 "scatter &mdash; and confirm the spread matches the SE formula."))
_c,_o=_run(r'''
import numpy as np
rng = np.random.default_rng(0)

# A known population: 100,000 customers' order values (skewed, true mean ~50).
population = rng.gamma(shape=5.0, scale=10.0, size=100_000)
mu, sigma = population.mean(), population.std()
print(f"TRUE population mean  mu    = {mu:.2f}")

# Reality gives you ONE sample of 50 customers.
one_sample = rng.choice(population, size=50)
print(f"one sample's mean     x-bar = {one_sample.mean():.2f}   (off by {one_sample.mean()-mu:+.2f})")

# Simulation luxury: repeat the study 1,000 times and watch x-bar scatter.
means = np.array([rng.choice(population, 50).mean() for _ in range(1000)])
print(f"\nspread of those means (the standard ERROR) = {means.std():.2f}")
print(f"formula prediction  sigma/sqrt(n)          = {sigma/np.sqrt(50):.2f}   <- they match")
''')
p.append(B.code_example(_c,_o,filename="sampling.py"))
p.append(B.concept(
 "One sample landed a couple of units off the truth &mdash; that's sampling variability, not a "
 "mistake. The simulated spread of the means matches &sigma;/&radic;n almost exactly. In real "
 "life you only get the *one* sample, but the formula hands you the standard error anyway, which "
 "is the whole point: you can quantify your uncertainty from a single sample."))

p.append(B.keypoints([
 "A ~parameter~ (&mu;, &sigma;) describes the population and is fixed but unknown; a ~statistic~ "
 "(x&#772;, s) is computed from a sample and varies.",
 "The ~sampling distribution~ of the mean is **centered on &mu;** and far **narrower** than the "
 "population.",
 "The ~standard error~ SE = &sigma;/&radic;n is the spread of that sampling distribution &mdash; "
 "how much your estimate wobbles.",
 "**SD &ne; SE.** SD is the spread of data points; SE is the spread of a statistic, and it "
 "shrinks with more data.",
 "Because error falls as 1/&radic;n, **halving uncertainty needs 4&times; the data**.",
]))

p.append(B.quiz([
 {"q":"A colleague reports the average basket size from 64 orders as $42 with a standard "
      "deviation of $24. What is the approximate standard error of that mean?",
  "options":[
   {"t":"$3 — it's SD/&radic;n = 24/&radic;64 = 24/8","correct":True,
    "why":"Correct. SE = SD/&radic;n = 24/8 = $3. The standard error scales the data's spread "
          "down by the square root of the sample size."},
   {"t":"$24 — the standard error equals the standard deviation",
    "why":"That confuses SE with SD. The SD ($24) is the spread of individual orders; the SE is "
          "much smaller, SD/&radic;n = $3."},
   {"t":"$0.38 — it's SD divided by n",
    "why":"The formula divides by &radic;n, not n. Dividing by 64 understates the error; the "
          "correct divisor is &radic;64 = 8."},
   {"t":"You can't tell without the population size",
    "why":"For these purposes the SE depends on the SD and the *sample* size, not the (usually "
          "huge) population size. SE = 24/&radic;64 = $3."}]},
 {"q":"You currently estimate a metric with a standard error of 2.0 from 100 users. Roughly how "
      "many users would you need to get the standard error down to 1.0?",
  "options":[
   {"t":"About 400 — error falls as 1/&radic;n, so halving it needs 4&times; the data","correct":True,
    "why":"Right. SE &prop; 1/&radic;n, so to cut the error in half you multiply the sample by "
          "2&sup2; = 4. From 100 that's 400 users."},
   {"t":"About 200 — just double the sample",
    "why":"Doubling n only divides the error by &radic;2 &asymp; 1.41, not 2. You need 4&times;, "
          "i.e. 400."},
   {"t":"About 1,000 — ten times the data",
    "why":"That would over-shoot, cutting the error by &radic;10 &asymp; 3.2&times;. To halve it "
          "you need 4&times;, i.e. 400."},
   {"t":"About 110 — error falls linearly with n",
    "why":"Error falls with &radic;n, not linearly. A 10% bump barely moves it; halving requires "
          "4&times; the data."}]},
 {"q":"Which statement about the sampling distribution of the mean is correct?",
  "options":[
   {"t":"It is centered on the true population mean and narrower than the population","correct":True,
    "why":"Exactly. The sample mean is unbiased (centered on &mu;) and averaging shrinks the "
          "spread to SE = &sigma;/&radic;n, narrower than the population's &sigma;."},
   {"t":"It has the same spread as the population",
    "why":"No &mdash; averaging reduces spread. The sampling distribution's spread is &sigma;/"
          "&radic;n, much smaller than the population's &sigma;."},
   {"t":"It is centered on the sample, not the population",
    "why":"Each sample mean varies, but the *distribution* of sample means is centered on the "
          "true population mean &mu;."},
   {"t":"It only exists if the population is normal",
    "why":"It exists for any population; and by the Central Limit Theorem (next lesson) it becomes "
          "normal regardless of the population's shape."}]},
]))

p.append(B.practice([
 {"q":"In one line, explain to a non-technical manager why a survey of 500 people can speak for a "
      "city of a million &mdash; and what the catch is.",
  "sol":"Because a random sample's average is centered on the truth and its wobble (standard "
        "error) depends on the *sample* size, not the city size &mdash; 500 random people pin the "
        "average down quite tightly. The catch is **random**: if the 500 aren't representative "
        "(e.g., only daytime mall-goers), no amount of math fixes the bias. Size controls variance; "
        "only good sampling controls bias."},
 {"q":"You measure SD = $30 on 25 orders. Give the standard error, then say how many orders you'd "
      "need to shrink the SE to $2.",
  "sol":"SE = 30/&radic;25 = 30/5 = **$6**. To reach SE = $2 you need &sigma;/&radic;n = 2, so "
        "&radic;n = 30/2 = 15, n = 15&sup2; = **225 orders**. (Sanity check: going from SE $6 to "
        "$2 is a 3&times; reduction, requiring 3&sup2; = 9&times; the data: 25 &times; 9 = 225.)"},
]))

p.append(B.deepdive(
 B.concept(
  "**Size fixes variance; only sampling fixes bias.** The standard error formula assumes a "
  "~random sample~ &mdash; every member of the population equally likely to be chosen. When that "
  "breaks, you get ~bias~: a systematic error that more data won't cure.") +
 B.concept(
  "Classic failures: ~selection bias~ (the 1936 *Literary Digest* poll sampled car and phone "
  "owners and confidently predicted the wrong US president from 2.4 million responses); "
  "~non-response bias~ (the people who answer differ from those who don't); and ~survivorship "
  "bias~ (studying only the survivors &mdash; reinforcing returning planes' bullet holes instead "
  "of the planes that never came back). In every case a *bigger* biased sample is just a "
  "more-confidently-wrong sample.") +
 B.concept(
  "The lesson: a small random sample beats a huge convenient one. Before trusting any statistic, "
  "ask not only *how big?* but *how was it drawn?*"),
 title="Deep dive: random sampling, and why bias is worse than variance"))

p.append(B.callout("note","Interview-ready",
 "The most common version is *\"what's the difference between standard deviation and standard "
 "error?\"* Answer crisply: SD measures the spread of individual data points; SE measures the "
 "spread of a *statistic* (like the mean), and equals SD/&radic;n. Bonus points for adding that "
 "SE shrinks with sample size, which is why bigger samples give more precise estimates.",
 "&#9670;"))

LESSONS={"stats-06-sampling":"\n".join(p)}
