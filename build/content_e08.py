# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Numbers get histograms and means; **categories** &mdash; region, channel, plan, product "
 "&mdash; need their own toolkit. You count them, turn counts into proportions, and study how one "
 "category relates to another. Categorical EDA is where you discover *which groups dominate*, "
 "*which combinations are common*, and *whether a category is associated with an outcome* &mdash; "
 "questions behind nearly every business decision."))

p.append(B.h2("Counts and proportions", kicker="Concept · one category"))
p.append(B.concept(
 "The first thing to do with a categorical column is count its values. `value_counts()` gives the "
 "tally per category; adding `normalize=True` turns those into **proportions** (shares), which "
 "are usually more meaningful than raw counts &mdash; '40% of orders are from the North' lands "
 "better than '1,203 orders.' Visualize counts with a **bar chart** (sorted, from Lesson 3.3)."))

p.append(B.h2("Two categories: grouped vs. stacked bars", kicker="Concept · two categories"))
p.append(B.concept(
 "To compare a value across **two** categorical dimensions at once &mdash; say revenue by "
 "category *and* channel &mdash; you have two bar layouts, and the right one depends on your "
 "question:"))
p.append(B.figure(IMG+"s_eda_bars_gs.png",
 "**Grouped vs. stacked.** Grouped bars place the sub-categories side by side &mdash; best for "
 "**comparing within** a group (which channel wins in Electronics?). Stacked bars sum them "
 "&mdash; best for **reading the total** per group (which category sells most overall?).",
 "Grouped bar chart beside a stacked bar chart of the same two-category data."))

p.append(B.h2("The crosstab (contingency table)", kicker="Concept · the relationship"))
p.append(B.concept(
 "To study the **relationship between two categorical variables**, build a ~crosstab~ (a "
 "contingency table): a grid counting how often each combination occurs. `pd.crosstab(a, b)` "
 "makes it, and a heatmap renders it readable. Crucially, normalizing the crosstab turns counts "
 "into **rates** &mdash; e.g., the return rate per region &mdash; which is what you usually want "
 "to compare."))
p.append(B.figure(IMG+"s_eda_crosstab.png",
 "**A crosstab as a heatmap.** Orders by region &times; channel: South leans Mobile, the West "
 "leans Web. Color makes the pattern pop, and normalizing the table would turn these counts into "
 "comparable percentages.",
 "A heatmap of order counts by region and channel."))
p.append(B.note(
 "A crosstab is exactly the input to the ~chi-square test~ from Lesson 1.10: EDA reveals an "
 "apparent association between two categories (e.g., region and returns), and the chi-square test "
 "tells you whether it's more than chance. Explore first, then test."))

p.append(B.h2("High-cardinality categories", kicker="Pitfall"))
p.append(B.concept(
 "Some categorical columns have **hundreds or thousands** of unique values &mdash; zip code, "
 "product ID, free-text city. Plotting all of them is hopeless, and they choke many models. The "
 "standard moves: show the **top-N** and bucket the long tail into an **'Other'** category, or "
 "group by a higher level (zip &rarr; state). You'll meet more powerful encodings in Track 6, but "
 "in EDA, top-N-plus-Other keeps charts and tables readable."))

p.append(B.h2("Explore categories in code", kicker="Worked example"))
p.append(B.concept(
 "Counts, proportions, and a crosstab turned into a rate &mdash; the everyday categorical EDA "
 "moves in a few lines."))
_c,_o=_run(r'''
import pandas as pd

df = pd.DataFrame({
    "region":   ["North","South","North","West","South","North","West","South","North","West"],
    "returned": [False, True, False, False, True, False, True, True, False, False],
})

# Counts and shares for one category
print("orders per region:")
print(df["region"].value_counts().to_string())
print("\nshare of orders (%):")
print((df["region"].value_counts(normalize=True) * 100).round(0).to_string())

# Crosstab of two categories, then turned into a RETURN RATE per region
ct = pd.crosstab(df["region"], df["returned"])
print("\ncrosstab (counts):")
print(ct.to_string())
rate = pd.crosstab(df["region"], df["returned"], normalize="index")[True] * 100
print("\nreturn rate by region (%):")
print(rate.round(0).to_string())
''')
p.append(B.code_example(_c,_o,filename="categorical.py"))

p.append(B.keypoints([
 "Count a category with `value_counts()`; add `normalize=True` for **proportions**, which usually "
 "communicate better than raw counts.",
 "Two categories on a bar chart: **grouped** to compare within a group, **stacked** to read the "
 "total per group.",
 "A ~crosstab~ (`pd.crosstab`) shows the relationship between two categoricals; normalize it for "
 "**rates**, and visualize as a heatmap.",
 "A crosstab feeds the **chi-square test** (Lesson 1.10): explore the association, then test it.",
 "For **high-cardinality** columns, show **top-N + 'Other'** or roll up to a coarser level.",
]))

p.append(B.quiz([
 {"q":"You want to compare the **return rate** (not raw count) across four regions. What do you "
      "compute?",
  "options":[
   {"t":"A crosstab of region x returned, normalized by row to get the rate per region","correct":True,
    "why":"Correct. `pd.crosstab(region, returned, normalize='index')` divides each region's "
          "counts by its row total, giving the return *rate* per region &mdash; comparable across "
          "regions of different sizes."},
   {"t":"A raw count of returns per region",
    "why":"Raw counts confound rate with region size &mdash; a big region can have more returns "
          "yet a lower rate. Normalize to compare rates fairly."},
   {"t":"A histogram of the region column",
    "why":"Histograms are for numeric distributions. For a rate across categories you need a "
          "(normalized) crosstab or grouped proportions."},
   {"t":"The mean of the region column",
    "why":"Region is categorical &mdash; you can't take its mean. You want the return rate within "
          "each region, via a normalized crosstab."}]},
 {"q":"You have revenue split by product category and by channel, and want to see which "
      "**category has the largest total**. Which bar layout?",
  "options":[
   {"t":"Stacked bars — the channels stack into one total-height bar per category","correct":True,
    "why":"Correct. Stacking sums the channels so each bar's full height is the category total, "
          "making the largest category obvious at a glance."},
   {"t":"Grouped bars",
    "why":"Grouped bars are best for comparing channels *within* a category, but you must mentally "
          "add the side-by-side bars to get a total. Stacking shows the total directly."},
   {"t":"A scatter plot",
    "why":"Scatter plots show relationships between two numeric variables, not category totals. "
          "Use a (stacked) bar chart."},
   {"t":"A pie chart per category",
    "why":"Pies are poor for comparison and wouldn't show totals across categories on one scale. "
          "Stacked bars do."}]},
 {"q":"A `product_id` column has 5,000 unique values. What's a sensible EDA move before plotting "
      "it?",
  "options":[
   {"t":"Show the top-N most frequent and bucket the rest into 'Other' (or roll up to a category)","correct":True,
    "why":"Correct. With thousands of categories, top-N + 'Other' (or grouping to a coarser level) "
          "keeps charts and tables readable while preserving the dominant signal."},
   {"t":"Plot all 5,000 bars",
    "why":"5,000 bars is unreadable. Summarize with top-N + 'Other' or a higher-level grouping."},
   {"t":"Take the mean of product_id",
    "why":"IDs are nominal labels (Lesson 1.2); their mean is meaningless. Summarize by frequency "
          "instead."},
   {"t":"Drop the column entirely",
    "why":"High cardinality isn't a reason to discard a potentially useful column; summarize it "
          "(top-N/Other) or encode it later (Track 6)."}]},
]))

p.append(B.practice([
 {"q":"Write one line to get the **percentage share** of each value in a `channel` column.",
  "sol":"`df[\"channel\"].value_counts(normalize=True).mul(100).round(1)`. `value_counts(normalize="
        "True)` gives proportions (summing to 1); multiplying by 100 and rounding yields readable "
        "percentage shares per channel."},
 {"q":"You crosstab `device` (Mobile/Desktop) against `converted` (True/False) and see Mobile has "
      "more conversions in absolute count. Why might that be misleading, and what do you compute "
      "instead?",
  "sol":"Absolute counts confound the **conversion rate** with **traffic volume** &mdash; Mobile "
        "may simply have far more visitors, so more conversions even at a *lower* rate. Compute "
        "the **rate** by normalizing the crosstab within each device "
        "(`normalize='index'`), giving conversion % for Mobile vs Desktop, which is the fair "
        "comparison. (Then a chi-square test, Lesson 1.10, checks if the difference is real.)"},
]))

p.append(B.deepdive(
 B.concept(
  "**Row vs. column normalization &mdash; and Simpson's paradox again.** `pd.crosstab(..., "
  "normalize=...)` accepts `'index'` (each **row** sums to 1 &mdash; rates *within* the row "
  "category), `'columns'` (each column sums to 1), or `'all'` (the whole table sums to 1). Pick "
  "the one matching your question; mixing them up produces confident nonsense. And remember "
  "Simpson's paradox: a relationship in a 2&times;2 crosstab can reverse once you add a third "
  "variable, so check important associations within subgroups.") +
 B.concept(
  "**Encoding categories for models (a Track 6 preview).** Charts and crosstabs are for "
  "*understanding* categories; models need them as numbers. The main routes are ~one-hot "
  "encoding~ (a 0/1 column per category &mdash; great for low cardinality) and ~target/frequency "
  "encoding~ (replace each category with a statistic, useful for high cardinality). Knowing during "
  "EDA whether a categorical column is low- or high-cardinality tells you which encoding headache "
  "is coming &mdash; and whether you'll need the 'top-N + Other' trick first.") +
 B.concept(
  "**Ordinal vs. nominal in charts.** If a category has a natural order (Lesson 1.2) &mdash; "
  "S/M/L, Bronze/Silver/Gold &mdash; keep that order on the axis rather than sorting by frequency, "
  "so the chart respects the meaning. For unordered (nominal) categories, sort by value so the "
  "ranking is obvious. The right ordering is part of telling the truth with a chart."),
 title="Deep dive: crosstab normalization, encoding categories, and ordered vs. unordered axes"))

p.append(B.callout("note","Interview-ready",
 "A frequent trap question: 'Group A had more conversions than B &mdash; is A better?' The mature "
 "answer separates **counts from rates**: normalize for traffic/size before comparing, then test "
 "the difference (chi-square). Mentioning crosstab normalization and the count-vs-rate distinction "
 "shows you won't be fooled by raw totals.", "&#9670;"))

LESSONS={"eda-08-categorical":"\n".join(p)}
