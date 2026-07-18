# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Real questions are rarely about one variable. *Does the spend-vs-revenue relationship hold in "
 "every region? Which variables move together? What's driving returns?* Answering these means "
 "seeing **several variables at once** without drowning in a tangle. This lesson gives you three "
 "high-leverage techniques &mdash; faceting, correlation heatmaps, and pair plots &mdash; that "
 "turn many dimensions into a picture you can read."))

p.append(B.h2("Faceting: small multiples", kicker="Technique 1"))
p.append(B.concept(
 "~Faceting~ (also called ~small multiples~) means drawing the **same chart repeatedly**, once "
 "per group, on **shared axes**. Because the axes match, your eye compares the panels directly. "
 "It adds one categorical variable (the split) to whatever chart you were already using &mdash; "
 "a histogram per region, a trend line per product, a scatter per segment."))
p.append(B.figure(IMG+"s_eda_facets.png",
 "**Small multiples.** The same order-value histogram, split by region, on shared axes. The "
 "comparison is instant: the North's orders skew larger, the South's smaller. Shared scales are "
 "what make the panels honestly comparable.",
 "Three histograms of order value, one per region, on shared axes."))

p.append(B.h2("The correlation heatmap", kicker="Technique 2"))
p.append(B.concept(
 "When you have several numeric variables, you want every pairwise ~correlation~ (Lesson 4.10) at "
 "once. A ~heatmap~ of the correlation matrix does exactly that: each cell is a pair, colored by "
 "the strength and sign of their relationship. A diverging color scale (red&ndash;blue) makes "
 "positive and negative pop, and clusters of related variables jump out."))
p.append(B.figure(IMG+"s_eda_heatmap.png",
 "**Correlation heatmap.** Red = positive, blue = negative, intensity = strength. Here ad spend, "
 "sessions, and revenue move together (red), while bounce rate moves opposite (blue) &mdash; the "
 "whole story of four variables in one square.",
 "A correlation heatmap of four variables with annotated coefficients."))
p.append(B.warn(
 "A heatmap inherits all of correlation's caveats: it measures only **linear, pairwise** "
 "relationships, so it misses curves (a U-shape reads as ~0, Lesson 4.10) and says nothing about "
 "causation. Use it to *spot candidates* worth a closer scatter plot &mdash; not as the final "
 "word.", "&#9650;"))

p.append(B.h2("Pair plots (the scatter matrix)", kicker="Technique 3"))
p.append(B.concept(
 "A ~pair plot~ goes one level deeper than the heatmap: instead of a single number per pair, it "
 "draws the **actual scatter plot** for every pair of numeric variables, with each variable's "
 "distribution down the diagonal. Color the points by a category and you've added a fifth "
 "variable. It's the fastest way to *see* the shape of every relationship at once &mdash; and "
 "to catch the non-linearities a heatmap hides."))
p.append(B.figure(IMG+"s_eda_pairplot.png",
 "**Pair plot.** Every variable against every other (scatters off-diagonal, distributions on the "
 "diagonal), colored by plan. You can see relationships are roughly linear here, and that 'Pro' "
 "customers cluster at higher values &mdash; structure no single number could convey.",
 "A pair plot (scatter matrix) of three variables colored by plan."))

p.append(B.h2("The numbers behind the heatmap", kicker="Worked example"))
p.append(B.concept(
 "A heatmap is just a picture of the correlation matrix, which is one line of pandas. Compute it, "
 "and you can both read the numbers and feed them to a heatmap to visualize."))
_c,_o=_run(r'''
import pandas as pd, numpy as np
rng = np.random.default_rng(4)
n = 200
ad_spend = rng.uniform(5, 100, n)
sessions = 40 + 1.8*ad_spend + rng.normal(0, 18, n)
revenue  = 80 + 3.0*sessions + rng.normal(0, 90, n)
bounce   = 70 - 0.4*sessions + rng.normal(0, 8, n)
df = pd.DataFrame({"ad_spend": ad_spend, "sessions": sessions,
                   "revenue": revenue, "bounce_rate": bounce})

# The correlation matrix — the numbers a heatmap colors in:
print(df.corr().round(2).to_string())
# To visualize it:  import seaborn as sns;  sns.heatmap(df.corr(), annot=True, cmap="RdBu_r")
''')
p.append(B.code_example(_c,_o,filename="correlation_matrix.py"))
p.append(B.tip(
 "To add a **third** variable to a single scatter plot, you can map it to **color** or **point "
 "size** (a 'bubble chart') &mdash; but use this sparingly: from Lesson 5.2, people read position "
 "and length far better than color or area. Often two clear charts, or a faceted set, beat one "
 "overloaded chart trying to show four variables at once."))

p.append(B.keypoints([
 "~Faceting~ / small multiples: the **same chart per group on shared axes** &mdash; the eye "
 "compares panels directly.",
 "~Correlation heatmap~: every **pairwise** correlation at once; diverging colors show sign and "
 "strength.",
 "Heatmaps are **linear and pairwise only** &mdash; they miss curves and never imply causation; "
 "use them to find scatters worth drawing.",
 "~Pair plot~: the actual scatter for **every pair**, distributions on the diagonal, color for a "
 "category &mdash; see all relationships at once.",
 "Encode a 3rd variable with color/size only sparingly; clear small multiples often beat one "
 "overloaded chart.",
]))

p.append(B.quiz([
 {"q":"You want to check whether the relationship between ad spend and revenue looks the same in "
      "each of four regions. What's the cleanest view?",
  "options":[
   {"t":"Faceting: one scatter plot per region, on shared axes (small multiples)","correct":True,
    "why":"Correct. Small multiples put the same scatter side by side per region with matching "
          "axes, so you can directly compare whether the relationship holds across groups."},
   {"t":"A single correlation number for the whole dataset",
    "why":"One pooled number hides regional differences entirely &mdash; and can even reverse them "
          "(Simpson's paradox). Faceting reveals the per-group picture."},
   {"t":"A pie chart of revenue by region",
    "why":"A pie shows composition, not the ad-spend-to-revenue *relationship* within each region. "
          "Faceted scatters do."},
   {"t":"One scatter with all regions overlaid in the same color",
    "why":"Overlaying in one color hides which points belong to which region. Faceting (or at "
          "least color-coding) is needed to compare groups."}]},
 {"q":"A correlation heatmap shows r &asymp; 0 between two variables. Your colleague concludes "
      "'they're unrelated.' What's the caveat?",
  "options":[
   {"t":"r near 0 only rules out a *linear* relationship; a curved (e.g., U-shaped) relationship "
        "can still exist — plot the scatter","correct":True,
    "why":"Correct. Correlation (and thus the heatmap) captures only linear association. A strong "
          "non-linear relationship can have r&asymp;0, so confirm with a scatter (or pair plot)."},
   {"t":"Heatmaps are always wrong",
    "why":"Heatmaps are useful summaries; the caveat is specific &mdash; they show linear, "
          "pairwise correlation only, not all relationships."},
   {"t":"It proves the two variables are independent",
    "why":"Zero linear correlation does not prove independence; a non-linear dependence can exist. "
          "You must look at the scatter."},
   {"t":"It means one variable causes the other",
    "why":"r near 0 indicates little linear association, and correlation never implies causation "
          "regardless. This option is doubly wrong."}]},
 {"q":"What does a **pair plot** show that a correlation heatmap does not?",
  "options":[
   {"t":"The actual scatter (shape) of every pair, plus each variable's distribution — revealing "
        "non-linearities and clusters","correct":True,
    "why":"Correct. A heatmap reduces each pair to one number; a pair plot draws the full scatter, "
          "so you can see curves, clusters, and outliers a single coefficient would hide."},
   {"t":"Nothing — it's just a prettier heatmap",
    "why":"It's fundamentally more information: real scatters and diagonal distributions, not a "
          "single number per pair."},
   {"t":"The causal direction between variables",
    "why":"No visualization shows causal direction from observational data. A pair plot shows "
          "shapes of relationships, not causation."},
   {"t":"Only the distribution of one variable",
    "why":"That's a single histogram. A pair plot shows every pairwise scatter *and* every "
          "diagonal distribution at once."}]},
]))

p.append(B.practice([
 {"q":"You have 12 numeric columns and want a first sense of which ones move together. What do you "
      "compute and plot, and what's your follow-up step for any strong pair?",
  "sol":"Compute the **correlation matrix** (`df.corr()`) and draw a **heatmap** to scan all 66 "
        "pairs at once, looking for strong red/blue cells and clusters. **Follow-up:** for any "
        "strong (or surprising) pair, draw the **scatter plot** to confirm the relationship is "
        "real and roughly linear (not driven by an outlier or actually curved), since the heatmap "
        "only captures linear, pairwise association."},
 {"q":"Aggregated over all customers, 'discount' correlates with 'higher spend.' But you suspect "
      "the story differs by customer tier. How would you check, and what phenomenon are you "
      "guarding against?",
  "sol":"**Facet** the analysis by tier &mdash; e.g., a scatter of discount vs spend per tier on "
        "shared axes, or compute the correlation within each tier. You're guarding against "
        "**Simpson's paradox**: a relationship that holds in aggregate can weaken, vanish, or even "
        "*reverse* within subgroups (a confounding effect). Small multiples make such reversals "
        "visible, which a single pooled number would hide."},
]))

p.append(B.deepdive(
 B.concept(
  "**Simpson's paradox &mdash; why aggregated views can lie.** A trend visible in combined data "
  "can reverse inside every subgroup. The classic case: a treatment that looks worse overall but "
  "is better for both mild and severe patients, because severity (a confounder) is distributed "
  "unevenly. Faceting and grouped analysis are your defense &mdash; always ask whether a "
  "confounding variable (Lesson 4.10, and all of Track 7) might be hiding inside an aggregate. "
  "This is one of the most important reasons to look at subgroups, not just totals.") +
 B.concept(
  "**When there are too many variables to eyeball.** A pair plot of 5 variables is 25 panels; of "
  "20 variables it's 400 &mdash; unreadable. Beyond a handful of dimensions you reach for "
  "~dimensionality reduction~: techniques like ~PCA~ (principal component analysis) compress many "
  "correlated variables into a few summary axes that capture most of the variation, which you can "
  "then plot in 2-D. It's a preview of unsupervised learning (Track 8); for now, know that "
  "heatmaps and pair plots are your tools up to ~10 variables, and reduction takes over above "
  "that.") +
 B.concept(
  "**Clustering a heatmap.** With many variables, reordering the heatmap's rows and columns so "
  "that similar variables sit together (a 'clustered heatmap') turns a wall of numbers into "
  "visible blocks of related variables &mdash; a fast way to discover structure, and a staple of "
  "exploratory work in fields from genomics to finance."),
 title="Deep dive: Simpson's paradox, and seeing beyond a handful of variables (PCA, clustering)"))

p.append(B.callout("note","Interview-ready",
 "Expect *\"how would you explore relationships among many variables?\"* Name the trio: faceting "
 "for group comparisons, a correlation heatmap to scan all pairs, and a pair plot to see the "
 "actual shapes &mdash; then add the caveats (heatmaps are linear/pairwise; watch for Simpson's "
 "paradox; use PCA when there are too many variables). That breadth-plus-caution is what "
 "interviewers want.", "&#9670;"))

LESSONS={"eda-04-multivariate":"\n".join(p)}
