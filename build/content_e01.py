# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Before you model, test, or present anything, you have to actually **understand the data in "
 "front of you**. ~Exploratory Data Analysis~ (EDA) is that systematic first look: you check the "
 "data's shape and quality, study each variable, look at how variables relate, and let what you "
 "see suggest the questions worth asking. Skip it and you build on sand &mdash; cleaning bugs, "
 "outliers, and wrong assumptions all slip through. This lesson gives you a repeatable EDA "
 "routine for any dataset."))

p.append(B.h2("What EDA is &mdash; and what it's for", kicker="Concept"))
p.append(B.concept(
 "~EDA~ is the open-ended investigation you do *before* committing to a model or a conclusion. "
 "Its three goals:\n\n"
 "- **Understand the data**: how big is it, what's each column, what's typical and what varies "
 "(everything from Track 4).\n"
 "- **Find problems**: missing values, wrong types, duplicates, impossible entries, outliers "
 "(everything from Track 1's cleaning).\n"
 "- **Generate questions**: spot patterns and oddities that become hypotheses to test later.\n\n"
 "EDA is *exploratory* &mdash; you're looking around with an open mind, not confirming a "
 "preset answer. That openness is the point: the data often surprises you."))

p.append(B.h2("The first-hour checklist", kicker="Method"))
p.append(B.concept(
 "Meeting a new dataset can feel overwhelming, so follow the same routine every time. It moves "
 "from the whole table down to single variables, then to relationships, then to questions:"))
p.append(B.figure(IMG+"s_eda_workflow.png",
 "**A repeatable EDA routine.** Always look at shape and quality first, then one variable at a "
 "time, then pairs of variables &mdash; and let what you find send you back for a closer look. "
 "The dashed loop is real: EDA is iterative.",
 "Flowchart: shape & types, missingness, univariate, bivariate, form hypotheses."))
p.append(B.concept(
 "Two terms for step 3 and 4: ~univariate~ analysis looks at **one variable at a time** (its "
 "distribution, center, spread, outliers); ~bivariate~ analysis looks at **two variables "
 "together** (how does spend relate to region? does return rate differ by channel?). Always do "
 "univariate first &mdash; you can't interpret a relationship until you understand each variable "
 "alone."))

p.append(B.h2("Run the checklist on real data", kicker="Worked example"))
p.append(B.concept(
 "Here's the routine in code, on a small orders table. Notice it's just the Track 4 summaries and "
 "Track 1 inspection tools, applied in a deliberate order &mdash; that ordering *is* the skill."))
_c,_o=_run(r'''
import pandas as pd

df = pd.DataFrame({
    "region":   ["North", "South", "North", "West", "South", "North"],
    "channel":  ["Web", "Mobile", "Web", "Store", "Mobile", "Web"],
    "amount":   [120, 45, 200, 30, 60, 95],
    "returned": [False, True, False, False, True, False],
})

# 1. Shape & types
print("shape:", df.shape)
# 2. Quality: missing values and duplicate rows
print("missing values:", int(df.isna().sum().sum()), "| duplicate rows:", int(df.duplicated().sum()))
# 3. Univariate: understand 'amount' on its own
print("amount -> mean ${:.0f}, min ${}, max ${}".format(df.amount.mean(), df.amount.min(), df.amount.max()))
# 3. Univariate: counts for a category
print("orders per region:", df.region.value_counts().to_dict())
# 4. Bivariate: does average amount differ by region?
print("avg amount by region:", df.groupby("region").amount.mean().round(0).to_dict())
''')
p.append(B.code_example(_c,_o,filename="eda_checklist.py"))
p.append(B.concept(
 "In six lines you now know: the table's size, that it's clean (no missing or duplicate rows), "
 "what a typical order looks like, where orders come from, and a hint of a **bivariate** pattern "
 "&mdash; the North's average order looks larger. That last line is a *question*, not a "
 "conclusion: is the difference real, or just six rows of noise? You'd answer it with the "
 "hypothesis test from Lesson 4.8. EDA hands testing its questions."))
p.append(B.tip(
 "Numbers alone can deceive &mdash; remember Anscombe's quartet from Lesson 4.10, where four "
 "datasets shared identical statistics but looked completely different. So EDA is never just "
 "`.describe()`; the moment a variable matters, **plot it**. That's exactly what the next two "
 "lessons are about."))

p.append(B.keypoints([
 "~EDA~ is the systematic first look: **understand** the data, **find problems**, **generate "
 "questions** &mdash; before any modeling.",
 "Follow the same routine every time: shape & types &rarr; missingness & duplicates &rarr; "
 "univariate &rarr; bivariate &rarr; hypotheses.",
 "~Univariate~ = one variable alone (do this first); ~bivariate~ = two variables together.",
 "EDA produces **questions to test**, not final answers &mdash; it feeds Track 4's inference.",
 "Summary numbers can hide the truth (Anscombe) &mdash; **always plot** what matters.",
]))

p.append(B.quiz([
 {"q":"You're handed a brand-new dataset. According to the EDA routine, what should you look at "
      "*first*?",
  "options":[
   {"t":"The shape, column types, and a few rows — get oriented before anything else","correct":True,
    "why":"Correct. You can't analyze what you haven't oriented to. Shape, dtypes, and a peek at "
          "rows come first, before quality checks, distributions, or relationships."},
   {"t":"A machine-learning model to see what's predictable",
    "why":"Modeling comes much later. Jumping to a model before understanding and cleaning the "
          "data is how leakage, outliers, and wrong assumptions slip through."},
   {"t":"The correlation between every pair of columns",
    "why":"Relationships (bivariate) come after you understand each variable alone and have "
          "checked data quality. Correlations on dirty or misunderstood data mislead."},
   {"t":"A polished chart for the final presentation",
    "why":"Presentation is the very last step. EDA is private investigation first; communication "
          "(Track 12) comes after you understand the data."}]},
 {"q":"Why does the routine insist on **univariate** analysis before **bivariate**?",
  "options":[
   {"t":"You can't correctly interpret a relationship between two variables until you understand "
        "each one alone","correct":True,
    "why":"Right. If you don't know a variable's distribution, outliers, or scale, any "
          "relationship you read between two of them can be driven by artifacts you haven't "
          "noticed yet."},
   {"t":"Bivariate analysis is too slow to do first",
    "why":"It's not about speed. The order is logical: understand the parts before the "
          "interactions, so relationships are interpreted correctly."},
   {"t":"Univariate analysis is the only kind that matters",
    "why":"Bivariate (and multivariate) analysis is essential &mdash; it's just that it builds on "
          "univariate understanding, so univariate comes first."},
   {"t":"They measure the same thing",
    "why":"They don't: univariate describes one variable; bivariate describes how two relate. "
          "Both are needed, in that order."}]},
 {"q":"Your six-row example shows the North's average order is higher than the South's. What is "
      "the right EDA conclusion?",
  "options":[
   {"t":"It's an interesting question to investigate, not a proven fact — six rows could easily be "
        "noise","correct":True,
    "why":"Exactly the EDA mindset. A pattern in a tiny sample is a hypothesis to test (Lesson "
          "1.9), not a conclusion. EDA surfaces questions; inference answers them."},
   {"t":"The North definitely spends more; ship a North-focused campaign",
    "why":"Acting on a six-row difference treats noise as signal. EDA flags the pattern; you'd "
          "need a proper test (and more data) before concluding."},
   {"t":"There's a bug, because regions shouldn't differ",
    "why":"Differences across groups are expected and interesting, not a bug. The question is "
          "whether this one is real, which requires testing."},
   {"t":"Correlation proves the region causes higher spend",
    "why":"This isn't even established as real yet, and even if it were, correlation isn't "
          "causation (Lesson 4.10). It's a question to investigate."}]},
]))

p.append(B.practice([
 {"q":"List, in order, the five steps of the first-hour EDA checklist and one concrete pandas "
      "call for each.",
  "sol":"1. **Shape & types** &mdash; `df.shape`, `df.dtypes`, `df.head()`. 2. **Missingness & "
        "duplicates** &mdash; `df.isna().sum()`, `df.duplicated().sum()`. 3. **Univariate** "
        "&mdash; `df['x'].describe()`, `df['cat'].value_counts()`, a histogram. 4. **Bivariate** "
        "&mdash; `df.groupby('g')['x'].mean()`, a scatter or boxplot. 5. **Form hypotheses** "
        "&mdash; write down the questions the patterns suggest, to test later."},
 {"q":"A teammate runs `df.describe()`, sees nothing unusual, and declares the data 'clean and "
      "understood.' Why is that premature?",
  "sol":"`describe()` only shows summary statistics for numeric columns &mdash; it can miss "
        "missing-value patterns, duplicate rows, wrong dtypes, categorical issues, and (per "
        "Anscombe) very different distributions that share the same mean and SD. You must also "
        "check `.isna()`, `.duplicated()`, `.dtypes`, `value_counts()` for categories, and "
        "**plot** the variables. Summary numbers are a start, not a substitute for looking."},
]))

p.append(B.deepdive(
 B.concept(
  "**Exploratory vs. confirmatory analysis.** EDA (a term coined by John Tukey in 1977) is "
  "*exploratory*: you look for patterns with an open mind. ~Confirmatory~ data analysis tests a "
  "pre-specified hypothesis. The two must stay honest about which you're doing, because of a "
  "trap: if you explore freely and then run a significance test on the most striking pattern you "
  "found, the p-value is invalid &mdash; you've effectively run many implicit tests and reported "
  "the luckiest (the multiple-comparisons problem from Lesson 4.8). Best practice: explore on "
  "the data, but confirm surprising findings on fresh data or with a pre-registered test.") +
 B.concept(
  "**Look before you compute.** It is genuinely common for a single plot to overturn a "
  "conclusion that summary statistics supported &mdash; a bimodal distribution hiding behind a "
  "mean, an outlier inflating a correlation, a trend that's really two subgroups (Simpson's "
  "paradox, coming in Track 6). The discipline 'never trust a statistic you haven't plotted' is "
  "why visualization (the next lessons) is inseparable from EDA."),
 title="Deep dive: exploratory vs. confirmatory analysis, and why you must look"))

p.append(B.callout("note","Interview-ready",
 "A classic prompt is *\"here's a dataset &mdash; what do you do first?\"* Don't name a model. "
 "Walk the checklist: check shape and types, then data quality (missingness, duplicates, "
 "impossible values), then distributions of key variables, then relationships, and say you'd "
 "**plot** as you go and write down questions to test. That structured, look-first answer is "
 "exactly the maturity they're probing for.", "&#9670;"))

LESSONS={"eda-01-mindset":"\n".join(p)}
