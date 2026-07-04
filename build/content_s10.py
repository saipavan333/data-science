# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Last lesson gave you the *logic* of testing; this one gives you the *menu*. Reach for the wrong "
 "test and even a perfect calculation is meaningless. The good news: a short decision tree takes "
 "you from 'what does my data look like?' to 'here's the right test' almost every time."))

p.append(B.h2("The decision tree", kicker="Method · which test when"))
p.append(B.concept(
 "Three questions pick your test almost always: *Is the outcome numeric or categorical? Are you "
 "relating two variables or comparing groups? How many groups, and are they paired?* Follow the "
 "arrows:"))
p.append(B.figure(IMG+"s10_chooser.png",
 "**From data to the right test.** Numeric outcomes lead to correlation/regression or the "
 "t-test family (and ANOVA for 3+ groups); categorical outcomes lead to the chi-square test. "
 "Bookmark this &mdash; it answers most 'which test?' questions.",
 "Decision tree mapping data characteristics to the appropriate statistical test."))

p.append(B.h2("The t-test family", kicker="Concept · comparing means"))
p.append(B.concept(
 "The ~t-test~ compares averages. It comes in three flavors for three situations:\n\n"
 "- ~One-sample t-test~: is this group's mean different from a *known target*? (Is average "
 "delivery time different from the promised 30 minutes?)\n"
 "- ~Two-sample t-test~: do *two independent groups* have different means? (Do users on the old "
 "vs new design check out at different speeds?)\n"
 "- ~Paired t-test~: did the *same subjects* change between two conditions? (Did each user's time "
 "improve before vs after a redesign?)\n\n"
 "All three share one idea: judge the gap between means *relative to the noise*."))
p.append(B.figure(IMG+"s10_ttest.png",
 "**What the t-statistic measures.** It's the difference in means divided by the standard error "
 "&mdash; a signal-to-noise ratio. A 6-point gap is convincing if the groups are tight, "
 "unconvincing if they're spread out.",
 "Two group distributions with the difference in means marked and the t formula."))

p.append(B.h2("Chi-square for categories", kicker="Concept · comparing proportions"))
p.append(B.concept(
 "When the outcome is *categorical*, means don't apply &mdash; you compare counts. The "
 "~chi-square test~ of independence asks whether two categorical variables are *associated* by "
 "comparing the counts you observed against the counts you'd expect if they were unrelated. (Is "
 "return rate associated with region? Is clicking associated with which ad someone saw?)"))

p.append(B.h2("When assumptions fail: nonparametric tests", kicker="Concept · the backup plan"))
p.append(B.concept(
 "The t-test assumes the data is roughly normal (or the sample is large enough for the CLT) and "
 "isn't dominated by wild outliers. When those assumptions break &mdash; small, skewed, "
 "outlier-ridden samples &mdash; use a ~nonparametric~ alternative that works on *ranks* instead "
 "of raw values: the ~Mann&ndash;Whitney U test~ replaces the two-sample t-test, and the "
 "~Wilcoxon signed-rank test~ replaces the paired t-test. They trade a little power for robustness."))

p.append(B.h2("Run two tests for real", kicker="Worked example"))
p.append(B.concept(
 "Here's a two-sample t-test (numeric outcome, two groups) and a chi-square test (categorical "
 "association), both with `scipy`. Notice you mostly just pick the function the tree points to "
 "and read the p-value."))
_c,_o=_run(r'''
import numpy as np
from scipy import stats
rng = np.random.default_rng(8)

# TWO-SAMPLE t-TEST: checkout times (seconds) for the old vs new design.
old = rng.normal(42, 11, size=80)
new = rng.normal(38, 10, size=75)
t, p = stats.ttest_ind(old, new, equal_var=False)   # Welch's t-test (safe default)
print("Two-sample t-test (old vs new checkout time)")
print(f"  old mean = {old.mean():.1f}s   new mean = {new.mean():.1f}s")
print(f"  t = {t:.2f},  p = {p:.4f}  ->  {'significant' if p<0.05 else 'not significant'}")

# CHI-SQUARE: is being returned associated with region?  rows=region, cols=[returned, kept]
table = np.array([[150, 850],    # North
                  [ 90, 910],    # South
                  [165, 835]])   # West
chi2, pc, dof, _ = stats.chi2_contingency(table)
print("\nChi-square test (region vs returned)")
print(f"  chi2 = {chi2:.1f},  dof = {dof},  p = {pc:.4f}  ->  "
      f"{'associated' if pc<0.05 else 'no association'}")
''')
p.append(B.code_example(_c,_o,filename="choosing_tests.py"))
p.append(B.callout("warn","Check the assumptions before you trust the p-value",
 "Every test has fine print: observations should be **independent**; t-tests want roughly normal "
 "data **or** a large sample (CLT); chi-square wants a decent count in each cell (a common rule: "
 "expected counts &ge; 5). If the assumptions are badly violated, switch to a nonparametric test "
 "or a different method &mdash; a p-value from the wrong test is just a number.", "&#9650;"))

p.append(B.keypoints([
 "Pick a test from three questions: outcome **numeric or categorical**, **relate or compare**, "
 "and **how many groups / paired?**",
 "~t-test family~: one-sample (vs a target), two-sample (two independent groups), paired (same "
 "subjects twice). For **3+ groups** use ~ANOVA~.",
 "~Chi-square~ tests association between two **categorical** variables.",
 "~Correlation/regression~ relates two **numeric** variables.",
 "When normality/outlier assumptions fail, use **nonparametric** tests (Mann&ndash;Whitney, "
 "Wilcoxon) that work on ranks.",
]))

p.append(B.quiz([
 {"q":"You want to know whether average order value differs between three store regions "
      "(North, South, West). Which test is appropriate?",
  "options":[
   {"t":"ANOVA — it compares means across three or more groups","correct":True,
    "why":"Correct. Comparing the means of 3+ independent groups is exactly what ANOVA is for. "
          "(Running multiple t-tests instead would inflate the false-positive rate.)"},
   {"t":"A two-sample t-test",
    "why":"A two-sample t-test compares exactly two groups. With three regions you'd need three "
          "separate tests, inflating Type I error &mdash; ANOVA handles all three at once."},
   {"t":"A chi-square test",
    "why":"Chi-square is for categorical outcomes (counts). Order value is numeric and you're "
          "comparing means, so ANOVA fits."},
   {"t":"A paired t-test",
    "why":"Paired tests need the same subjects measured twice. Three independent regions aren't "
          "paired, so ANOVA is right."}]},
 {"q":"A team measures each user's task time *before* and *after* a redesign &mdash; the same "
      "users in both conditions. Which test compares the two?",
  "options":[
   {"t":"A paired t-test — the same subjects are measured twice","correct":True,
    "why":"Right. Because each user appears in both conditions, the measurements are paired, and "
          "the paired t-test uses each user as their own control, which is more powerful."},
   {"t":"A two-sample (independent) t-test",
    "why":"That treats the groups as unrelated, ignoring that it's the same users twice. Pairing "
          "the measurements removes person-to-person variability and is the correct, more powerful "
          "choice."},
   {"t":"A chi-square test",
    "why":"Task time is numeric, not categorical counts, so chi-square doesn't apply."},
   {"t":"Correlation",
    "why":"Correlation relates two variables across subjects; here you're comparing the same "
          "measure before vs after, which is a paired comparison."}]},
 {"q":"Your sample is small (n=12), heavily skewed, and has a couple of extreme outliers. You want "
      "to compare two independent groups. What's the safest choice?",
  "options":[
   {"t":"A nonparametric test like Mann–Whitney U, which uses ranks","correct":True,
    "why":"Correct. With a small, skewed, outlier-heavy sample the t-test's normality assumption "
          "is shaky; a rank-based test like Mann&ndash;Whitney is robust to those problems."},
   {"t":"A two-sample t-test, since it always works",
    "why":"The t-test relies on approximate normality or a large sample. With n=12, heavy skew, "
          "and outliers, those don't hold, so its p-value is unreliable."},
   {"t":"A chi-square test",
    "why":"The outcome is numeric, not categorical counts, so chi-square is the wrong family."},
   {"t":"No test is valid, so give up",
    "why":"Nonparametric tests exist precisely for this situation &mdash; you can still test, just "
          "with a rank-based method."}]},
]))

p.append(B.practice([
 {"q":"For each question, name the test: (a) Is our app's mean rating different from the "
      "industry benchmark of 4.2? (b) Do clicks differ across four banner designs (click / no "
      "click)? (c) Do premium and free users differ in average session length?",
  "sol":"(a) **One-sample t-test** &mdash; one group's mean vs a known target (4.2). (b) "
        "**Chi-square test** &mdash; a categorical outcome (click / no click) across four design "
        "groups. (c) **Two-sample t-test** &mdash; comparing the mean of two independent groups "
        "(premium vs free)."},
 {"q":"A colleague ran six separate two-sample t-tests to compare six marketing variants, each at "
      "&alpha;=0.05, and found one 'significant.' Why is ANOVA (or a correction) the better "
      "approach, in one sentence?",
  "sol":"Running six tests at &alpha;=0.05 inflates the chance of at least one false positive to "
        "well above 5% (roughly 1&minus;0.95&#8310; &asymp; 26%), so a single 'hit' is likely by "
        "chance alone; ANOVA tests all variants together (or you apply a multiple-comparisons "
        "correction) to control that error rate."},
]))

p.append(B.deepdive(
 B.concept(
  "**The assumptions, spelled out.** The two-sample t-test assumes: (1) ~independence~ &mdash; "
  "observations don't influence each other (violated by repeated measures or clustered data); "
  "(2) ~approximate normality~ of the data *or* a large enough sample for the CLT to make the "
  "*means* normal; and (3) for the classic version, roughly equal variances &mdash; which is why "
  "~Welch's t-test~ (the `equal_var=False` we used) is the safer default, since it doesn't assume "
  "equal spread.") +
 B.concept(
  "**After ANOVA, then what?** ANOVA tells you *some* group differs, not *which* one. To find the "
  "culprit you run ~post-hoc~ pairwise comparisons (e.g., Tukey's HSD) that correct for the "
  "multiple looks. This two-step pattern &mdash; an overall test, then corrected pairwise tests "
  "&mdash; keeps your false-positive rate honest.") +
 B.concept(
  "**Parametric vs. nonparametric, in a phrase.** Parametric tests (t, ANOVA) assume a "
  "distributional shape and, when it holds, squeeze the most power from your data. Nonparametric "
  "tests (Mann&ndash;Whitney, Wilcoxon, Kruskal&ndash;Wallis) assume far less and shine on small, "
  "skewed, or ordinal data &mdash; trading a little power for robustness. When results from both "
  "agree, you can report with confidence."),
 title="Deep dive: assumptions, Welch's t-test, post-hoc tests, and parametric vs. nonparametric"))

p.append(B.callout("note","Interview-ready",
 "A frequent prompt is *\"which statistical test would you use here?\"* Narrate the decision tree "
 "out loud: outcome type &rarr; relate or compare &rarr; number of groups &rarr; paired or not. "
 "Name the test, then mention one assumption you'd check (independence, normality/large n, cell "
 "counts) and the nonparametric fallback. That structure shows you choose tests deliberately, not "
 "by reflex.", "&#9670;"))

LESSONS={"stats-10-tests":"\n".join(p)}
