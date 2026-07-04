# -*- coding: utf-8 -*-
import builder as B
from examples_run import EX

IMG = "../assets/img/"
p = []

p.append(B.why(
    "Nobody can stare at 10,000 numbers and understand them. So we compress a column down to a "
    "few numbers that capture its story. But a careless summary doesn't just lose detail — it "
    "can actively lie, hiding a skew or a fortune in outliers behind a single innocent-looking "
    "average. This lesson teaches the handful of summary numbers every analyst uses, and — just "
    "as important — exactly when each one deceives you."))

# ----------------------------------------------------- center ------------- #
p.append(B.h2("Center: what's a typical value?", kicker="Concept · part 1"))
p.append(B.concept(
    "The first question about any numeric column is *\"where's the middle?\"* There are three "
    "common answers, and they are **not** interchangeable:\n\n"
    "- The ~mean~ (average): add up all values and divide by how many there are. It uses every "
    "value, which makes it powerful — and fragile.\n"
    "- The ~median~: line the values up in order and take the middle one (with an even count, "
    "average the two middle values). Exactly half the data sits on each side.\n"
    "- The ~mode~: the most frequently occurring value. It's the only center that works for "
    "nominal categories (the most common city, say)."))
p.append(B.concept(
    "Here's the crucial difference. The mean is a *balance point* — every value pulls on it, so "
    "one giant value drags it. The median is a *position* — it only cares about order, so extreme "
    "values barely move it. Watch what happens when a distribution is **skewed** (stretched out "
    "to one side):"))
p.append(B.figure(
    IMG + "s3_mean_median.png",
    "**Left:** a symmetric distribution — mean and median sit together. **Right:** a "
    "right-skewed one (incomes) — the long tail of large values drags the **mean** above the "
    "**median**. The median still marks the typical person; the mean is pulled toward the rich "
    "few.",
    "Two histograms comparing mean and median for symmetric and right-skewed data."))
p.append(B.tip(
    "A quick diagnostic you'll use forever: if the **mean is much bigger than the median**, the "
    "data is right-skewed (a tail of large values). If the mean is much *smaller*, it's "
    "left-skewed. When they're close, the distribution is roughly symmetric. You can sense the "
    "shape from two numbers."))

# ----------------------------------------------------- spread ------------- #
p.append(B.h2("Spread: how much do values vary?", kicker="Concept · part 2"))
p.append(B.concept(
    "Center alone is dangerously incomplete. Two teams can both average a 50-minute delivery "
    "time, but if one is always 48–52 minutes and the other swings from 30 to 70, they are "
    "completely different operations. **Spread** measures that variability. The main tools:\n\n"
    "- ~Range~: max minus min. Simple, but defined entirely by the two most extreme points, so "
    "it's jumpy and outlier-sensitive.\n"
    "- ~Variance~: the average *squared* distance of each value from the mean. Squaring keeps "
    "negatives from cancelling positives and punishes big deviations.\n"
    "- ~Standard deviation~ (SD): the square root of the variance. This is the headline spread "
    "number because it's back in the **original units** — minutes, dollars — so you can read it "
    "as *\"the typical distance from the mean.\"*\n"
    "- ~IQR~ (interquartile range): the range of the **middle 50%** of the data (we'll define it "
    "precisely in a moment). It ignores the extremes, so it's robust like the median."))
p.append(B.formula(
    'variance &nbsp;<span class="var">s</span>&sup2; = '
    '<sup>1</sup>&frasl;<sub>(n &minus; 1)</sub> &sum; (x<sub>i</sub> &minus; x&#772;)&sup2;'
    '&nbsp;&nbsp;&nbsp;&nbsp; SD = &radic;<span class="var">s</span>&sup2;',
    "Read it as: take each value's distance from the mean x&#772;, square it, average those "
    "(dividing by n&minus;1 — see the deep dive), then square-root to get back to real units."))
p.append(B.figure(
    IMG + "s3_spread.png",
    "**Same mean, different spread.** Both teams average 50 minutes, but Team A's small SD means "
    "consistency, while Team B's large SD means you can't promise a delivery window. The shaded "
    "bands show &plusmn;1 SD around the mean.",
    "Two bell curves with the same center but different standard deviations."))

# ----------------------------------------------------- boxplot ------------ #
p.append(B.h2("The five-number summary and the boxplot", kicker="Concept · part 3"))
p.append(B.concept(
    "A ~percentile~ is the value below which a given percentage of the data falls — the 25th "
    "percentile is the value with a quarter of the data beneath it. Three percentiles are so "
    "useful they get names, the ~quartiles~: **Q1** (25th), **Q2** (50th, the median), and **Q3** "
    "(75th). With the min and max, those make the ~five-number summary~. The ~IQR~ is simply "
    "Q3 &minus; Q1 — the width of the middle half of the data.\n\n"
    "The ~boxplot~ draws all of this at once, and it's the single most useful chart for "
    "comparing distributions. Learn to read its anatomy:"))
p.append(B.figure(
    IMG + "s3_boxplot.png",
    "**Anatomy of a boxplot.** The box spans Q1 to Q3 (the middle 50%); the line inside is the "
    "median; the whiskers reach the farthest points within 1.5&times;IQR of the box; dots beyond "
    "that are flagged as **outliers**. One glance tells you center, spread, skew, and oddities.",
    "An annotated boxplot showing Q1, median, Q3, IQR, whiskers, and outliers."))
p.append(B.note(
    "The *1.5&times;IQR* whisker rule is a widely used convention (due to John Tukey), not a law "
    "of nature — it's a practical fence for flagging points worth a second look, not proof that "
    "a point is an error. Always investigate flagged outliers; never delete them reflexively."))

# ----------------------------------------------------- worked example ----- #
p.append(B.h2("Watch robustness happen", kicker="Worked example"))
p.append(B.concept(
    "Let's compute every one of these on a tiny, realistic dataset: nine salaries on a small "
    "team where the founder earns far more than everyone else. Pay attention to how differently "
    "the mean and median react when we remove that one outlier."))
p.append(B.code_example(EX["s13_describe"][0], EX["s13_describe"][1], filename="describe.py"))
p.append(B.concept(
    "With the founder included, the **mean salary is \\$77k** — yet *eight of the nine people "
    "earn less than that*. The mean describes nobody. The **median of \\$58k** is a far more "
    "honest 'typical salary.' Remove the outlier and the mean lurches by \\$20k while the median "
    "moves less than a thousand. That gap *is* the meaning of robustness, and it's why median "
    "income, median home price, and median response time are reported instead of means."))
p.append(B.callout("warn", "Mean or median? A rule you can trust",
    "Use the **mean** for roughly symmetric data with no wild outliers — it's efficient and "
    "feeds into most statistical methods. Switch to the **median** when the data is skewed or "
    "has outliers (income, prices, wait times, anything with a long tail). When in doubt, report "
    "both and plot the distribution — if they disagree, the distribution is trying to tell you "
    "something.", "&#9888;"))

p.append(B.keypoints([
    "**Center**: mean (balance point, uses every value, outlier-sensitive), median (the middle, "
    "robust), mode (most common, the only center for categories).",
    "**mean &gt; median &rArr; right-skew**; mean &lt; median &rArr; left-skew; close &rArr; "
    "roughly symmetric.",
    "**Spread**: standard deviation = typical distance from the mean, in original units; IQR = "
    "width of the middle 50%, robust to outliers.",
    "The **five-number summary** (min, Q1, median, Q3, max) is drawn by a **boxplot**, which "
    "reveals center, spread, skew, and outliers at a glance.",
    "Pick **median + IQR** for skewed/outlier-prone data; **mean + SD** for symmetric data.",
]))

p.append(B.quiz([
    {"q": "A city reports that its **mean** household income is \\$95k but its **median** is "
          "\\$61k. What does this gap tell you?",
     "options": [
        {"t": "Incomes are right-skewed — a minority of very high earners pull the mean above "
              "the median",
         "correct": True,
         "why": "Right. Mean well above median is the signature of a right skew: a long tail of "
                "large values drags the mean up while the median stays at the typical household."},
        {"t": "Half the households earn exactly \\$95k",
         "why": "The mean isn't a 'half' point — that's the median. The mean is a balance point "
                "pulled by large values."},
        {"t": "There must be a data error; mean and median should match",
         "why": "They only match for symmetric data. A real gap is expected and informative for "
                "skewed quantities like income — not an error."},
        {"t": "Incomes are left-skewed",
         "why": "Left skew would put the mean *below* the median. Here the mean is higher, so the "
                "skew is to the right."}]},
    {"q": "You're reporting a 'typical' value for **page load time**, which has a few very slow "
          "outliers. Which summary best represents the typical user's experience?",
     "options": [
        {"t": "The median, because it's not dragged up by the rare very slow loads",
         "correct": True,
         "why": "Correct. Load times are right-skewed with slow outliers; the median reflects the "
                "typical experience, while the mean would be inflated by a few stragglers."},
        {"t": "The mean, because it uses all the data",
         "why": "Using all the data is exactly why the mean gets dragged upward by the slow "
                "outliers, overstating the typical user's wait."},
        {"t": "The range, because it shows the slowest load",
         "why": "The range describes the extremes, not a typical value, and is itself defined by "
                "the outliers."},
        {"t": "The mode, because load times repeat often",
         "why": "Continuous times rarely repeat exactly, so the mode is unstable and not a good "
                "'typical' summary here."}]},
    {"q": "Two products both have a mean rating of 4.0 stars. Product X has SD = 0.3; Product Y "
          "has SD = 1.4. What can you conclude?",
     "options": [
        {"t": "Ratings for X are tightly clustered near 4.0; Y's are far more polarizing/spread "
              "out",
         "correct": True,
         "why": "Exactly. Same mean, different SD: X's small SD means most ratings hug 4.0, while "
                "Y's large SD means lots of high and low ratings averaging to 4.0 — a very "
                "different product story."},
        {"t": "X and Y are essentially identical because the means match",
         "why": "Equal means hide very different spreads. Center without spread is an incomplete "
                "summary — that's the whole point of measuring variability."},
        {"t": "Y is the better product because its SD is larger",
         "why": "A larger SD just means more variability (more polarized opinions), which isn't "
                "inherently better — often it's worse for a product."},
        {"t": "X must have more ratings than Y",
         "why": "SD measures spread of values, not how many there are. Sample size isn't "
                "determined by the SD."}]},
]))

p.append(B.practice([
    {"q": "The values are 2, 3, 3, 4, 8. Compute by hand: mean, median, mode, and range. Then "
          "say which center best represents 'typical' and why.",
     "sol": "Mean = (2+3+3+4+8)/5 = 20/5 = **4.0**. Median = middle of the sorted list "
            "2,3,3,4,8 = **3**. Mode = **3** (appears twice). Range = 8 &minus; 2 = **6**. The "
            "value 8 pulls the mean up to 4.0, above the median of 3; with a small right skew "
            "like this the **median (3)** better represents a typical value."},
    {"q": "A dataset of response times (seconds) is 1.0, 1.1, 0.9, 1.2, 1.0, 40.0. Without a "
          "computer, argue whether mean+SD or median+IQR is the more honest summary, and roughly "
          "where each measure lands.",
     "sol": "The 40.0 is a glaring outlier (maybe a timeout). The **mean** is "
            "(1.0+1.1+0.9+1.2+1.0+40.0)/6 &asymp; 7.5 s — absurd, since five of six requests took "
            "about a second. The **SD** would be huge, also driven by the one point. The "
            "**median** is the average of the 3rd and 4th sorted values (1.0 and 1.1) &asymp; "
            "**1.05 s**, and the **IQR** stays around a few tenths of a second — both robust to "
            "the outlier. So **median + IQR** is far more honest here, and you'd separately "
            "investigate the 40-second request."},
]))

p.append(B.deepdive(
    B.concept(
        "**Why square the deviations?** When measuring spread, we want distances from the mean. "
        "If we just averaged the raw deviations (x<sub>i</sub> &minus; x&#772;), they'd always "
        "sum to zero — the positives and negatives cancel exactly. Squaring removes the sign and, "
        "as a bonus, penalizes large deviations more than small ones, which suits many natural "
        "processes. We then square-root at the end (the SD) to return to the original units.") +
    B.concept(
        "**Why divide by n &minus; 1, not n?** When you compute spread around the *sample* mean "
        "(rather than the unknown true mean), the data sits slightly closer to its own mean than "
        "to the truth, so dividing by n would systematically *underestimate* the real variance. "
        "Dividing by n &minus; 1 — the ~degrees of freedom~ — corrects that bias. Intuitively, "
        "one 'piece of information' was spent estimating the mean, leaving n &minus; 1 "
        "independent deviations. With large n the correction barely matters; with small n it "
        "matters a lot. This is why `pandas` and `numpy`'s `.std(ddof=1)` default differs from "
        "the naive formula.") +
    B.concept(
        "**A note on units.** Variance is in *squared* units (dollars-squared?!), which is why "
        "we rarely report it directly. The standard deviation, its square root, is in real units "
        "and is what you quote to a stakeholder."),
    title="Deep dive: why we square deviations, and the mystery of n &minus; 1"))

p.append(B.callout("note", "Interview-ready",
    "Two classics live here. *\"When would you use the median instead of the mean?\"* &mdash; "
    "when the data is skewed or has outliers, because the median is robust (give the income "
    "example). And *\"what's the difference between variance and standard deviation?\"* &mdash; "
    "SD is the square root of variance, expressed in the original units, which makes it "
    "interpretable as the typical distance from the mean.", "&#9670;"))

LESSONS = {"stats-03-summary": "\n".join(p)}
