# -*- coding: utf-8 -*-
import builder as B
IMG="../assets/img/"; p=[]

p.append(B.why(
 "EDA and visualization show up in nearly every data-science interview &mdash; as a take-home, a "
 "live 'explore this dataset' exercise, or a 'critique this chart' question &mdash; because they "
 "test whether you can actually *think* with data, not just run models. This lesson is your "
 "self-test: the questions teams ask, with model answers. Cover each, answer it aloud, then "
 "reveal and compare."))

p.append(B.callout("tip","What the EDA/viz rounds test",
 "Three things: a **systematic approach** to an unfamiliar dataset (not flailing), **chart "
 "judgment** (the right visual for the question, honestly drawn), and **skepticism** (spotting "
 "misleading charts, confounders, and patterns that are just noise). Structured, look-first, "
 "honest answers win.", "&#10022;"))

p.append(B.h2("Approach & chart-choice questions", kicker="Bank 1"))
p.append(B.practice([
 {"q":"'Here's a dataset you've never seen. Walk me through what you do first.'",
  "sol":"Walk the EDA checklist, out loud: (1) **shape & types** (`df.shape`, `df.dtypes`, "
        "`df.head()`); (2) **data quality** &mdash; missing values, duplicates, impossible "
        "values; (3) **univariate** &mdash; distributions of key variables, with histograms/"
        "boxplots; (4) **bivariate** &mdash; relationships via groupby, scatters, a correlation "
        "heatmap; (5) **form hypotheses** to test. Emphasize that you **plot as you go** and write "
        "down questions &mdash; you're exploring to understand and to find problems, not jumping "
        "to a model."},
 {"q":"'What chart would you use to compare a metric across 8 categories, and why not a pie "
      "chart?'",
  "sol":"A **sorted bar chart**: comparison across categories is exactly what bars are for, and "
        "sorting makes the ranking instant. Not a pie because humans judge **lengths** far more "
        "accurately than **angles/areas** &mdash; with 8 slices a pie is unreadable, while bars "
        "let you rank and compare precisely. (If labels are long, use horizontal bars.)"},
 {"q":"'You see mean income = \\$95k but median = \\$61k. What does that tell you, and how would "
      "you visualize it?'",
  "sol":"The mean far above the median signals a **right-skewed** distribution &mdash; a few very "
        "high earners pull the mean up (Lesson 1.3). Report the **median** as 'typical.' Visualize "
        "with a **histogram** (you'll see the long right tail) or a **boxplot** (the outliers "
        "appear beyond the upper whisker). Consider a **log scale** to make the skewed shape "
        "readable."},
 {"q":"'How would you explore relationships among ~10 numeric variables?'",
  "sol":"Start with a **correlation heatmap** to scan all pairs for strong (red/blue) "
        "relationships and clusters, then draw **scatter plots** (or a **pair plot**) for the "
        "interesting pairs to see the actual shape. Caveat openly: correlation is **linear and "
        "pairwise**, so confirm with scatters and watch for non-linearity. If there are far more "
        "variables, mention **dimensionality reduction (PCA)**."}]))

p.append(B.h2("Skeptic & integrity questions", kicker="Bank 2"))
p.append(B.practice([
 {"q":"'Critique this chart: a bar chart of quarterly sales whose y-axis starts at 95.'",
  "sol":"The **truncated y-axis** is the flaw: a bar encodes value as length, so starting at 95 "
        "exaggerates a small (~5%) change into a visually huge jump &mdash; technically accurate "
        "numbers, misleading framing. Fix: **start the bar axis at zero**; if you must emphasize a "
        "small change, annotate the percentage or use an honest line chart. I'd also check the "
        "axis labels/units and whether the time range is cherry-picked."},
 {"q":"'A line shows a steep 3-month decline. Are you worried?'",
  "sol":"First ask to see the **full time range** &mdash; a 3-month window can be **cherry-picked** "
        "to make a minor dip look like a collapse, when the longer series may be flat or rising. "
        "I'd also check for **seasonality** (is this dip normal for the season?), confirm the "
        "**axis isn't truncated**, and look at the **absolute magnitude** of the change before "
        "concluding anything."},
 {"q":"'In aggregate, users who get a discount spend more, so discounts work. Do you buy it?'",
  "sol":"Not yet &mdash; this is correlation, not causation, and likely **confounded**: big "
        "spenders may simply receive more discounts (reverse/selection), or a hidden variable "
        "(loyalty, season) drives both. I'd **facet** by customer tier to check for **Simpson's "
        "paradox**, and ultimately propose a **randomized experiment** (Track 5) &mdash; randomly "
        "give some users a discount and compare &mdash; to establish whether discounts actually "
        "*cause* higher spend."}]))

p.append(B.keypoints([
 "Answer 'explore this dataset' with the **checklist** (shape &rarr; quality &rarr; univariate "
 "&rarr; bivariate &rarr; hypotheses), plotting as you go.",
 "Choose charts by **question type**; defend bars over pies with the length-vs-angle perception "
 "point.",
 "Flag the big chart deceptions: **truncated axes** (bars) and **cherry-picked ranges**.",
 "For many variables: **heatmap to scan, scatter/pair plot to confirm**; remember linear/pairwise "
 "limits.",
 "Be the **skeptic**: watch for confounders, Simpson's paradox, seasonality, and noise before "
 "believing a pattern.",
]))

p.append(B.quiz([
 {"q":"An interviewer shows a dashboard where revenue 'doubled' &mdash; but the bar chart's axis "
      "starts at 90% of the old value. The strongest critique?",
  "options":[
   {"t":"The truncated axis visually exaggerates the change; on a zero-based axis the rise is "
        "small","correct":True,
    "why":"Correct. Bars encode value as length, so a truncated axis inflates a small change. "
          "Redraw from zero to see the true (modest) rise &mdash; the classic deception."},
   {"t":"Revenue can't be shown with bars",
    "why":"Bars are fine for revenue comparison; the problem is the truncated axis, not the chart "
          "type."},
   {"t":"The chart needs more colors",
    "why":"Aesthetics aren't the issue. The misleading truncated axis is, regardless of color."},
   {"t":"Nothing — if the numbers are right, the chart is fine",
    "why":"Accurate numbers can still be framed dishonestly. A truncated bar axis misleads even "
          "with correct data."}]},
 {"q":"Best first move when handed an unfamiliar dataset in a live interview?",
  "options":[
   {"t":"Check shape, types, and data quality, then look at distributions — narrate the EDA "
        "checklist","correct":True,
    "why":"Correct. A calm, systematic checklist (orient, check quality, univariate, bivariate, "
          "hypotheses) shows maturity and avoids the leakage/outlier traps of jumping ahead."},
   {"t":"Immediately fit a model to see accuracy",
    "why":"Modeling before understanding/cleaning invites leakage and misleading results. Explore "
          "first."},
   {"t":"Make a polished dashboard",
    "why":"Presentation is last. First understand the data privately via EDA."},
   {"t":"Compute every pairwise correlation and stop there",
    "why":"Correlations are one bivariate step, not the whole approach &mdash; and they're linear/"
          "pairwise only. Follow the full checklist and plot."}]},
 {"q":"A pattern holds in the aggregate but reverses within every subgroup. This is:",
  "options":[
   {"t":"Simpson's paradox — a confounder makes the aggregated and subgroup stories disagree","correct":True,
    "why":"Correct. Simpson's paradox is exactly this reversal, driven by a confounding variable. "
          "Faceting/grouped analysis reveals it; it's a key reason to inspect subgroups."},
   {"t":"The central limit theorem",
    "why":"The CLT is about the sampling distribution of the mean becoming normal &mdash; unrelated "
          "to aggregate-vs-subgroup reversals."},
   {"t":"Overfitting",
    "why":"Overfitting is a modeling problem (fitting noise). The described reversal is Simpson's "
          "paradox, a confounding phenomenon."},
   {"t":"A truncated axis",
    "why":"That's a charting deception. The reversal across subgroups is Simpson's paradox."}]},
]))

p.append(B.callout("note","You've finished Track 3",
 "You can now meet any dataset with a systematic routine, choose and draw honest charts, see many "
 "variables at once, and catch the ways charts (and aggregates) mislead. Combined with Track 1's "
 "rigor and Track 2's tooling, you can take raw data all the way to a trustworthy picture &mdash; "
 "which is exactly what the EDA capstone asks you to do. Next, **Track 4 (Classical Machine "
 "Learning)** builds models on this foundation.", "&#9670;"))

LESSONS={"eda-05-interview":"\n".join(p)}
