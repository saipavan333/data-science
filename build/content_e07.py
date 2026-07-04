# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "When you plot a single variable, its **shape** tells a story before you compute anything: where "
 "the typical value sits, whether there's a long tail, whether two groups are hiding inside one "
 "column. The shape also dictates which statistics and models are even valid &mdash; and when a "
 "shape is inconvenient, a simple ~transformation~ can fix it. Reading distributions is a core "
 "EDA skill that pays off in every later track."))

p.append(B.h2("Six shapes to recognize on sight", kicker="Concept"))
p.append(B.concept(
 "Most real distributions are a variation on six shapes. Learn to name them from a histogram:\n\n"
 "- ~Normal~ (symmetric bell): mean &asymp; median; the empirical rule applies (Lesson 1.5).\n"
 "- ~Right-skewed~: a long tail of large values (income, prices, wait times). Mean &gt; median; "
 "report the median.\n"
 "- ~Left-skewed~: a long tail of small values (e.g., exam scores near a ceiling). Mean &lt; "
 "median.\n"
 "- ~Bimodal~ (two peaks): a giant clue that **two subgroups are mixed together** &mdash; split "
 "and investigate.\n"
 "- ~Uniform~ (flat): every value about equally likely (often IDs or generated data).\n"
 "- ~Heavy-tailed~: a sharp peak with rare but extreme outliers (returns, failures) &mdash; "
 "averages can be dangerously unstable."))
p.append(B.figure(IMG+"s_eda_shapes.png",
 "**The six shapes.** Each implies different handling: skew &rarr; prefer the median; bimodal "
 "&rarr; find the hidden subgroups; heavy-tailed &rarr; beware unstable means and plan for "
 "outliers (Lesson 3.7).",
 "A gallery of normal, right-skewed, left-skewed, bimodal, uniform, and heavy-tailed histograms."))

p.append(B.h2("Checking normality: the QQ plot", kicker="Concept"))
p.append(B.concept(
 "Some methods (certain tests, and the residuals of linear models) assume roughly **normal** "
 "data, so you'll often want to check. A histogram gives a rough sense, but the sharper tool is "
 "the ~QQ plot~ (quantile&ndash;quantile plot): it plots your data's quantiles against the "
 "quantiles a perfect normal would have. If the data is normal, the points fall on a straight "
 "line; systematic curves away from the line reveal skew or heavy tails."))
p.append(B.figure(IMG+"s_eda_qq.png",
 "**Reading a QQ plot.** Left: normal data hugs the diagonal. Right: skewed data bends away in a "
 "characteristic curve. It's a faster, more sensitive normality check than squinting at a "
 "histogram.",
 "Two QQ plots: normal data on the line, skewed data curving away."))

p.append(B.h2("Transformations: taming skew", kicker="Concept"))
p.append(B.concept(
 "When a variable is heavily right-skewed, a ~transformation~ can reshape it into something "
 "symmetric &mdash; which makes patterns clearer to the eye and assumptions hold for models. The "
 "workhorse is the ~log transform~: because it compresses large values far more than small ones, "
 "it pulls in a long right tail and often turns it into a bell."))
p.append(B.figure(IMG+"s_eda_logtransform.png",
 "**The log transform in action.** Raw income is heavily right-skewed; `log10(income)` is roughly "
 "symmetric. Many naturally multiplicative quantities (income, population, prices) live more "
 "naturally on a log scale.",
 "Right-skewed income histogram beside its symmetric log-transformed version."))
p.append(B.warn(
 "Two cautions with logs. (1) `log(0)` is undefined and `log` of negatives is impossible &mdash; "
 "for data with zeros use `log1p(x)` (which computes log(1+x)), and for values that can be "
 "negative use a different transform. (2) After transforming, your numbers are in **log units**; "
 "remember to **back-transform** (exponentiate) before reporting, so stakeholders see real "
 "dollars, not log-dollars.", "&#9650;"))

p.append(B.h2("See a transform fix the skew", kicker="Worked example"))
p.append(B.concept(
 "We can put numbers on what the picture showed: ~skewness~ measures asymmetry (0 = symmetric, "
 "positive = right tail). Watch it collapse toward zero, and the mean and median converge, after "
 "a log transform."))
_c,_o=_run(r'''
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)

income = rng.lognormal(mean=10.3, sigma=0.6, size=5000) / 1000   # $000s, right-skewed

print(f"raw income : mean ${income.mean():.0f}k  median ${np.median(income):.0f}k  "
      f"skewness {stats.skew(income):+.2f}")

logged = np.log10(income)
print(f"log10      : mean {logged.mean():.2f}     median {np.median(logged):.2f}     "
      f"skewness {stats.skew(logged):+.2f}")

print("\nThe skew collapsed toward 0 and mean is now ~ median: the data is roughly symmetric.")
''')
p.append(B.code_example(_c,_o,filename="transform.py"))

p.append(B.keypoints([
 "Name a distribution from its histogram: **normal, right-skewed, left-skewed, bimodal, uniform, "
 "heavy-tailed**.",
 "**Skew &rarr; report the median**; **bimodal &rarr; hunt for two hidden subgroups**; "
 "**heavy-tailed &rarr; expect unstable means and outliers**.",
 "The ~QQ plot~ checks normality: points on the line = normal; curved away = skewed/heavy-tailed.",
 "A ~log transform~ tames right-skew (use `log1p` if there are zeros); it suits multiplicative "
 "quantities like income and prices.",
 "After transforming, **back-transform** before reporting so numbers are in real units.",
]))

p.append(B.quiz([
 {"q":"A histogram of a single column shows two clear, separate peaks. What's the most useful "
      "interpretation?",
  "options":[
   {"t":"Two distinct subgroups are likely mixed together — split the data and investigate","correct":True,
    "why":"Correct. Bimodality usually means the column blends two populations (e.g., two "
          "customer types, two machines). Faceting or grouping by a suspected variable often "
          "reveals them &mdash; a real EDA insight."},
   {"t":"The data is normally distributed",
    "why":"A normal distribution has a single peak. Two peaks indicate a mixture, not normality."},
   {"t":"There's a data-entry error you should delete",
    "why":"Two peaks rarely mean an error &mdash; they usually mean two real subgroups. "
          "Investigate, don't delete."},
   {"t":"You must log-transform it",
    "why":"A log transform fixes right-skew, not bimodality. For two peaks, find and separate the "
          "subgroups."}]},
 {"q":"You plan to report a 'typical' value for a heavily right-skewed variable and want to "
      "visualize its shape clearly. What's a good move?",
  "options":[
   {"t":"Report the median, and consider a log transform (or log axis) to see the shape","correct":True,
    "why":"Correct. The median resists the long tail (Lesson 1.3), and a log transform/axis "
          "spreads out the bunched small values so the distribution's shape is readable."},
   {"t":"Report the mean and use a linear axis",
    "why":"The mean is inflated by the right tail (misleading as 'typical'), and a linear axis "
          "crushes the small values together. Median + log is better."},
   {"t":"Delete the large values so it looks normal",
    "why":"Deleting real data to force a shape is dishonest and loses information. Transform the "
          "axis/variable instead, and report the robust median."},
   {"t":"Switch to a pie chart",
    "why":"A pie can't show a distribution at all. Use a histogram (optionally log-scaled) and the "
          "median."}]},
 {"q":"On a QQ plot, the points curve upward away from the straight reference line at the right "
      "end. What does that indicate?",
  "options":[
   {"t":"The data has a heavier/longer right tail than a normal distribution — it's right-skewed","correct":True,
    "why":"Correct. Points bending above the line at the upper end mean the data's high values are "
          "more extreme than a normal would produce &mdash; a right-skew/heavy right tail."},
   {"t":"The data is perfectly normal",
    "why":"Perfectly normal data falls *on* the line. Systematic curvature away from it signals "
          "non-normality (here, right skew)."},
   {"t":"There are exactly two subgroups",
    "why":"That's bimodality, seen better on a histogram. A QQ plot's upward curve indicates skew/"
          "heavy tails, not subgroups."},
   {"t":"The sample size is too small to tell",
    "why":"A clear systematic curve (not just noise at the ends) indicates skew regardless; it's a "
          "shape signal, not a sample-size artifact."}]},
]))

p.append(B.practice([
 {"q":"You have a `price` column with many zeros (free items) and a long right tail. You want to "
      "log-transform it for a clearer histogram. What's the catch and the fix?",
  "sol":"`log(0)` is undefined, so a plain `np.log(price)` will produce `-inf`/NaN for every free "
        "item. The fix is `np.log1p(price)` (which computes log(1 + price), so zeros map to 0 "
        "cleanly), or add a small constant before logging. Remember the result is in log units, "
        "so back-transform with `expm1` (or exp) before reporting actual prices."},
 {"q":"Why might you transform a variable before *modeling*, not just for a prettier chart?",
  "sol":"Many models (and the inference around them) assume things a skewed variable violates: "
        "linear regression assumes a roughly linear relationship and normal-ish, equal-variance "
        "residuals (Track 4/7). Logging a right-skewed predictor or target can **linearize** a "
        "multiplicative relationship, **stabilize the variance**, and **reduce the leverage of "
        "extreme values** &mdash; making the model fit better and its assumptions hold. (You then "
        "interpret coefficients in percentage/multiplicative terms and back-transform predictions.)"},
]))

p.append(B.deepdive(
 B.concept(
  "**Beyond log: the power-transform family.** The log is one of a family of ~power "
  "transforms~. ~Box&ndash;Cox~ automatically finds the best power (square root, log, reciprocal, "
  "&hellip;) to make positive data as normal as possible; ~Yeo&ndash;Johnson~ extends it to data "
  "with zeros and negatives. scikit-learn's `PowerTransformer` applies these in a modeling "
  "pipeline. The square root is a milder option than log for moderate right-skew (and is natural "
  "for count data).") +
 B.concept(
  "**Eyeball first, test second.** There are formal normality tests (Shapiro&ndash;Wilk, "
  "Anderson&ndash;Darling), but with large samples they flag even trivial, harmless departures "
  "from normality as 'significant' &mdash; so a histogram and QQ plot, judged with common sense, "
  "are usually more useful than a p-value. Ask 'is it normal *enough* for what I'm doing?' rather "
  "than 'is it exactly normal?' (which real data never is).") +
 B.concept(
  "**Why skew matters downstream.** Heavy right skew concentrates influence in a few huge values, "
  "which can dominate a mean, inflate a correlation, and give outliers outsized pull on a fitted "
  "model (Lesson 3.7 and Track 4). Recognizing and, where appropriate, transforming skewed "
  "variables during EDA prevents a cascade of misleading results later &mdash; it's cheap "
  "insurance taken early."),
 title="Deep dive: power transforms (Box–Cox), eyeballing vs. normality tests, and why skew matters"))

p.append(B.callout("note","Interview-ready",
 "Be ready for *\"this feature is very skewed &mdash; what would you do?\"* Answer: confirm with a "
 "histogram/QQ plot, report the **median** for 'typical,' and consider a **log (or Box-Cox) "
 "transform** to symmetrize it for visualization and modeling &mdash; mentioning `log1p` for "
 "zeros and back-transforming for interpretation. Recognizing **bimodality as hidden subgroups** "
 "is another strong signal.", "&#9670;"))

LESSONS={"eda-07-distributions":"\n".join(p)}
