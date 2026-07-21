# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]
p.append(B.why(
 "Numeric columns look ready to use &mdash; they're already numbers &mdash; but raw numbers routinely "
 "**mislead** models. A feature measured in the millions dwarfs one measured in fractions; a "
 "heavy-tailed column lets a handful of giants dominate; an outlier drags a mean off a cliff. "
 "Shaping numeric features &mdash; **scaling**, **transforming**, **binning**, **taming outliers** "
 "&mdash; is often the cheapest accuracy you'll ever buy."))
p.append(B.h2("Scaling: put features on a level playing field", kicker="Standardize / normalize"))
p.append(B.concept(
 "Many models judge features by their **magnitude**. In a distance-based model (kNN, k-means) or a "
 "gradient-descent one (linear/logistic regression, neural nets), a feature ranging 0&ndash;1,000,000 "
 "will swamp one ranging 0&ndash;1 &mdash; not because it matters more, but because it's *bigger*. "
 "Two standard fixes:\n\n"
 "- **Standardization** (`StandardScaler`): subtract the mean, divide by the std &rarr; each feature "
 "has mean 0, std 1. The default choice.\n"
 "- **Min&ndash;max normalization** (`MinMaxScaler`): rescale to a fixed range like [0, 1]. Handy "
 "when you need bounded inputs.\n\n"
 "Fit the scaler's statistics on **train only**, then apply to test (the lesson-9.1 rule)."))
p.append(B.tip(
 "**Tree-based models don't need scaling.** Decision trees, random forests, and gradient boosting "
 "split on *thresholds* (\"is income &gt; 50k?\"), which don't care about units or magnitude. Scaling "
 "matters for **distance- and gradient-based** models. Knowing which camp your model is in saves "
 "pointless work &mdash; and is a common interview check."))
p.append(B.h2("Transforms: fix the shape, not just the scale", kicker="Log & friends"))
p.append(B.concept(
 "Money, counts, populations, and durations are usually **right-skewed** &mdash; a long tail of large "
 "values. Skew hurts models that assume roughly symmetric inputs and lets the tail dominate. A "
 "**log transform** compresses the tail and pulls the distribution toward symmetry:"))
p.append(B.figure(IMG+"s_fe_skew.png",
 "**Log transform.** The raw feature (left) is heavily right-skewed &mdash; the mean is dragged "
 "rightward by a few huge values. After `log(1 + x)` (right) the distribution is far more symmetric, "
 "so no handful of giants dominates and models behave far better.",
 "Two histograms: a right-skewed raw feature and its symmetric log-transformed version."))
p.append(B.concept(
 "Common transforms: **log** (for positive, right-skewed data &mdash; use `log1p` so zeros are "
 "safe), **square root** (gentler than log, works with zeros), and **Box&ndash;Cox / Yeo&ndash;"
 "Johnson** (which *search* for the best power transform automatically). See the skew collapse in "
 "code:"))
_c,_o=_run(r'''
import numpy as np
from scipy import stats
rng = np.random.default_rng(3)
x = rng.lognormal(mean=1.0, sigma=0.9, size=6000)   # heavy right tail

print(f"skew, raw:          {stats.skew(x):5.2f}   <- very skewed")
print(f"skew, log1p(x):     {stats.skew(np.log1p(x)):5.2f}   <- collapsed from ~5.6 to ~0.6")
''')
p.append(B.code_example(_c,_o,filename="log_transform.py"))
p.append(B.h2("Binning and outliers", kicker="When raw values fight you"))
p.append(B.concept(
 "- **Binning** turns a continuous feature into ranges (age &rarr; `18-25`, `26-40`, ...). It can "
 "capture non-linear effects for simple models and add robustness, at the cost of throwing away "
 "resolution. Use it when the relationship is genuinely step-like, not reflexively.\n"
 "- **Outliers** can wreck mean-based features and gradient models. Options: **clip / winsorize** "
 "(cap values at, say, the 1st and 99th percentiles), **transform** (a log often dissolves the "
 "problem), or **leave them** for tree models that don't care. What you must *not* do is delete rows "
 "silently &mdash; an 'outlier' may be your most important case (fraud, churn)."))
p.append(B.warn(
 "Never reflexively **drop** outliers. In fraud, health, and churn, the extreme rows are frequently "
 "the *signal*, not noise. Investigate first: is it a data-entry error (fix/remove) or a real "
 "extreme (keep, maybe clip/transform)? Deleting the tail can delete the very thing you're paid to "
 "predict."))
p.append(B.h2("Your turn — measure how a transform tames skew", kicker="Interactive lab"))
p.append(B.pylab(
 "The feature `x` has a heavy right tail. Apply a `log1p` transform, measure the **new skewness** "
 "with `scipy.stats.skew`, round to **2 decimals**, and assign to **`answer`**. (Raw skew is large "
 "and positive; the transform should sharply reduce it &mdash; from ~5.6 to under 1.)",
 "import numpy as np\n"
 "from scipy import stats\n"
 "rng = np.random.default_rng(3)\n"
 "x = rng.lognormal(mean=1.0, sigma=0.9, size=6000)\n",
 "answer = round(float(stats.skew(np.log1p(x))), 2)",
 starter="import numpy as np\nfrom scipy import stats\n# skew of log1p(x), rounded to 2 dp\nanswer = ",
 hint="`np.log1p(x)` applies log(1+x); wrap it in `stats.skew(...)`, cast to float, round to 2 dp.",
 title="Lab — skew before vs. after a log",
 preview="numpy + scipy loaded; skewed feature x preloaded. First Run boots Python and scipy.",
 explain="The raw feature's skew is huge (~5.6); after `log1p` it drops to ~0.6 &mdash; "
         "from severely to only mildly skewed (a pure `log` reaches ~0 but isn't zero-safe). That's why log transforms are the first reflex for money, counts, and "
         "any heavy-tailed feature feeding a linear or distance-based model."))
p.append(B.keypoints([
 "**Scale** features for distance- and gradient-based models (kNN, k-means, linear, NN); "
 "**standardization** (mean 0, std 1) is the default. **Trees don't need scaling.**",
 "Fit scalers/transforms on **train only**, then apply to test.",
 "**Right-skewed** features (money, counts) &rarr; **log/sqrt/Box-Cox** to restore symmetry (use "
 "`log1p` for zeros).",
 "**Binning** trades resolution for capturing step-like effects; use it deliberately, not "
 "reflexively.",
 "**Outliers**: clip/winsorize or transform &mdash; but **investigate before deleting**; the extreme "
 "row may be the signal.",
]))
p.append(B.quiz([
 {"q":"You're using k-nearest-neighbours with features `age` (0-100) and `income` (0-500,000). Why "
      "must you scale?",
  "options":[
   {"t":"kNN uses distances, so income's huge range would dominate the distance and age would barely "
        "count","correct":True,
    "why":"Correct. Euclidean distance is driven by the largest-magnitude feature; unscaled, income "
          "swamps age purely due to units. Standardizing puts them on equal footing so both "
          "contribute."},
   {"t":"kNN can't handle two features at once",
    "why":"kNN handles many features; the issue is that unscaled magnitudes distort the distance "
          "metric."},
   {"t":"Scaling makes kNN train faster",
    "why":"The reason is correctness of the distance, not speed."},
   {"t":"You don't need to — kNN is scale-invariant",
    "why":"The opposite: kNN is highly scale-*sensitive* because it's distance-based. Scaling is "
          "essential here."}]},
 {"q":"Which model can you feed raw, unscaled, skewed numeric features to with the least worry?",
  "options":[
   {"t":"Gradient-boosted trees — they split on thresholds, so magnitude and monotonic skew don't "
        "affect them","correct":True,
    "why":"Correct. Tree ensembles are invariant to feature scale and to any monotonic transform, so "
          "they tolerate unscaled, skewed inputs. (You might still transform for interpretability, but "
          "it's not required.)"},
   {"t":"k-means clustering",
    "why":"k-means is distance-based and very scale-sensitive &mdash; unscaled features distort the "
          "clusters."},
   {"t":"Logistic regression",
    "why":"A gradient/linear model that benefits from scaling and symmetric inputs; raw skewed "
          "features can hurt it."},
   {"t":"A neural network",
    "why":"NNs train far better on scaled inputs; unscaled magnitudes cause optimization trouble."}]},
]))
p.append(B.practice([
 {"q":"A `revenue` feature ranges from $0 to $2M and is extremely right-skewed. You'll feed it to a "
      "logistic regression. What do you do and why?",
  "sol":"Two moves. **(1) Transform** the skew: apply `log1p(revenue)` (log handles the heavy right "
        "tail and the +1 keeps zeros valid), turning a long-tailed feature into a roughly symmetric "
        "one so a few huge accounts don't dominate. **(2) Scale** it: logistic regression is "
        "gradient-based, so standardize (mean 0, std 1) &mdash; **fitting the log parameters and the "
        "scaler on the training set only**, then applying to test. Together this stops the feature "
        "from swamping others and helps the optimizer converge. (For a tree model, neither step is "
        "strictly needed.)"},
 {"q":"When is binning a continuous feature a good idea, and what's the cost?",
  "sol":"Binning helps when the relationship with the target is genuinely **step-like or "
        "non-monotonic** and you're using a model that can't easily capture that (e.g. a plain linear "
        "model), or when you want **robustness** to outliers and noise in the raw values, or for "
        "**interpretability** (\"18&ndash;25 vs 26&ndash;40\"). The cost is **lost resolution**: you "
        "throw away within-bin ordering and fine distinctions, which can *reduce* accuracy when the "
        "relationship is smooth &mdash; and results depend on where you place the bin edges. Flexible "
        "models (trees, boosting) usually find the right cut points themselves, so bin deliberately, "
        "not by default."},
]))
p.append(B.deepdive(
 B.concept(
  "**Standardize vs. normalize vs. robust-scale.** `StandardScaler` (z-score) assumes roughly "
  "bell-shaped data and is the default; `MinMaxScaler` maps to a fixed range and is useful when a "
  "model needs bounded inputs (some neural nets) but is **sensitive to outliers** (one extreme value "
  "squashes everyone else). `RobustScaler` centres on the median and scales by the interquartile "
  "range, so it shrugs off outliers &mdash; a good pick for heavy-tailed features you don't want to "
  "transform. Match the scaler to the data's shape, and remember all of them learn parameters that "
  "must be fit on train only.") +
 B.concept(
  "**Why symmetry helps at all.** Linear and distance models implicitly treat a unit of a feature as "
  "equally meaningful everywhere, and squared-error losses are dominated by large values. A "
  "right-skewed feature violates both: the tail's few giant values carry most of the leverage and "
  "distort coefficients. A log transform makes *multiplicative* differences additive (a jump from "
  "\\$1k to \\$10k becomes the same size as \\$10k to \\$100k), which often matches how the effect "
  "actually behaves &mdash; e.g. the *ratio* of incomes matters more than the raw dollar gap. So a "
  "log isn't just cosmetic; it frequently encodes the *right* notion of distance for the problem."),
 title="Deep dive: robust scaling, and why log makes multiplicative effects additive"))
LESSONS={"fe-02-numeric":"\n".join(x for x in p if x)}
print("content_fe02 OK — chars:", len(LESSONS["fe-02-numeric"]))
