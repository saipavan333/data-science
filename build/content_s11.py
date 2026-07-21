# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Almost every analysis eventually asks 'do these two things move together?' &mdash; ad spend and "
 "sales, study time and grades, price and demand. ~Correlation~ puts a single number on that. But "
 "it is one of the most over-trusted numbers in all of data work: it only sees straight lines, it "
 "can hide a wild shape behind a tidy value, and &mdash; most famously &mdash; it is not "
 "causation. This lesson gives you the tool *and* its warning label."))

p.append(B.h2("What correlation measures", kicker="Concept"))
p.append(B.concept(
 "The ~correlation coefficient~ (Pearson's r) is a single number from &minus;1 to +1 summarizing "
 "the **linear** relationship between two numeric variables:\n\n"
 "- The **sign** is the direction: positive means they rise together, negative means one rises as "
 "the other falls.\n"
 "- The **magnitude** is the strength: &plusmn;1 is a perfect straight line, 0 is no *linear* "
 "relationship.\n\n"
 "Under the hood it's standardized ~covariance~ &mdash; covariance measures whether two variables "
 "vary together, and dividing by their standard deviations rescales it to the clean &minus;1..+1 "
 "range so different pairs are comparable."))
p.append(B.figure(IMG+"s11_scatter_r.png",
 "**What different r values look like** &mdash; and the crucial last panel: a strong U-shaped "
 "relationship with r &asymp; 0. Pearson's r only measures *straight-line* association, so it is "
 "blind to curves.",
 "Six scatterplots showing correlations from +0.9 to -0.9 and a U-shape with r near zero."))

p.append(B.h2("Pearson vs. Spearman", kicker="Concept · two flavors"))
p.append(B.concept(
 "~Pearson's r~ measures *linear* association on the raw values. ~Spearman's &rho;~ (rho) "
 "measures *monotonic* association by first converting each variable to ranks &mdash; so it asks "
 "'as one goes up, does the other consistently go up (or down)?' without requiring a straight "
 "line. Use Spearman when the relationship is curved-but-consistent, or when you have ordinal data "
 "or outliers (ranks tame extreme values)."))
p.append(B.figure(IMG+"s11_pearson_spearman.png",
 "**Curved but monotonic.** As x rises, y always rises &mdash; just not linearly. Pearson "
 "under-rates it; Spearman, working on ranks, captures the near-perfect ordering.",
 "A monotonic curved relationship where Spearman exceeds Pearson."))

p.append(B.h2("Always plot first: Anscombe's quartet", kicker="Concept · the cautionary tale"))
p.append(B.concept(
 "In 1973 the statistician Francis Anscombe built four datasets with *identical* summary "
 "statistics &mdash; same means, same variances, same correlation (r = 0.82), same regression "
 "line &mdash; that look nothing alike. It is the single most persuasive argument for plotting "
 "your data before trusting any summary number."))
p.append(B.figure(IMG+"s11_anscombe.png",
 "**Four datasets, one set of statistics.** A clean line, a curve, a line with one outlier, and "
 "a near-vertical cluster with a single leverage point &mdash; all with the same r. The summary "
 "numbers are identical; the stories are opposite.",
 "Anscombe's quartet: four very different datasets with identical summary statistics."))

p.append(B.h2("Correlation is not causation", kicker="Concept · the famous warning"))
p.append(B.concept(
 "This is the one everyone quotes and many still forget. Two variables can correlate strongly "
 "while neither causes the other. The usual culprit is a ~confounder~ &mdash; a hidden third "
 "variable driving both."))
p.append(B.figure(IMG+"s11_confounder.png",
 "**The classic example.** Ice-cream sales and drownings rise together, but eating ice cream "
 "doesn't drown anyone. Summer heat (the confounder) drives both. The correlation is real; the "
 "causal story is wrong.",
 "Confounder diagram: summer heat causes both ice-cream sales and drownings."))
p.append(B.concept(
 "There are three ways a correlation can fool you: a ~confounder~ drives both (above); ~reverse "
 "causation~ (maybe Y causes X, not X causes Y); or pure ~coincidence~ (with enough variables, "
 "some will correlate by chance &mdash; 'spurious correlations'). Establishing real causation "
 "needs more than a correlation &mdash; ideally a randomized experiment (Track 6) or careful "
 "causal methods (Track 7). For now, the discipline is simply: **never write 'causes' when all "
 "you have is 'correlates.'**"))

p.append(B.h2("Measure it in code", kicker="Worked example"))
p.append(B.concept(
 "Watch Pearson and Spearman behave on three relationships &mdash; a clean line, a monotonic "
 "curve, and a U-shape &mdash; and see why a single coefficient is never the whole story."))
_c,_o=_run(r'''
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)

x       = rng.uniform(-3, 3, size=300)
linear  = 2*x + rng.normal(0, 1.0, 300)        # straight line
curved  = np.exp(x) + rng.normal(0, 1.0, 300)  # always increasing, but curved
ushape  = x**2 + rng.normal(0, 1.0, 300)       # strong, but not monotonic

print(f"{'relationship':18s} {'Pearson r':>10s} {'Spearman rho':>13s}")
for name, y in [("linear", linear), ("monotonic-curved", curved), ("U-shaped", ushape)]:
    pr = stats.pearsonr(x, y)[0]
    sr = stats.spearmanr(x, y)[0]
    print(f"{name:18s} {pr:>+10.2f} {sr:>+13.2f}")
print("\nLinear: both high.  Curved: Spearman > Pearson.  U-shape: BOTH ~0 -> you must plot it.")
''')
p.append(B.code_example(_c,_o,filename="correlation.py"))
p.append(B.concept(
 "The U-shape is the punchline: a strong, obvious relationship that *both* coefficients score near "
 "zero. No single correlation number can be trusted without a picture &mdash; which is why every "
 "EDA (Track 5) starts with scatterplots."))

p.append(B.widget("correlation", "Feel what a correlation looks like", "Slide r from &minus;1 to +1 and watch the scatter tighten toward a line or dissolve into a cloud &mdash; a picture of what each value of r actually means."))
p.append(B.keypoints([
 "~Pearson's r~ (&minus;1 to +1) measures **linear** association: sign = direction, magnitude = "
 "strength; it is **blind to curves**.",
 "~Spearman's &rho;~ works on **ranks** and captures any **monotonic** relationship; prefer it "
 "for curved-but-consistent data, ordinal data, or outliers.",
 "**Always plot.** Anscombe's quartet proves identical summary stats can hide wildly different "
 "data.",
 "**Correlation &ne; causation.** Beware ~confounders~, reverse causation, and coincidence.",
 "Proving causation needs experiments (Track 6) or causal methods (Track 7) &mdash; not a "
 "correlation coefficient.",
]))

p.append(B.quiz([
 {"q":"A study finds neighborhoods with more firefighters per capita have more fire damage. A "
      "reporter concludes 'firefighters cause fire damage.' What's the real explanation?",
  "options":[
   {"t":"A confounder — bigger areas have both more fires (more damage) and more firefighters","correct":True,
    "why":"Correct. Population/area size drives both more fires and more firefighters. The "
          "correlation is real, but the causal claim ignores the confounder."},
   {"t":"Firefighters genuinely cause damage and should be reduced",
    "why":"That's the causation trap. The link is explained by a confounder (area size), not by "
          "firefighters causing damage &mdash; cutting them would be disastrous."},
   {"t":"The correlation must be a calculation error",
    "why":"The correlation can be perfectly real; the error is the *causal* interpretation, not "
          "the math."},
   {"t":"Damage causes firefighters to appear",
    "why":"While responders do arrive at fires, the steady per-capita staffing pattern across "
          "neighborhoods is better explained by area size (a confounder) than by reverse "
          "causation."}]},
 {"q":"You compute Pearson's r = 0.05 between two variables and conclude 'they're unrelated.' What "
      "should you do before believing that?",
  "options":[
   {"t":"Plot a scatterplot — r near 0 only rules out a *linear* relationship, not a curved one","correct":True,
    "why":"Right. Pearson's r misses non-linear patterns (recall the U-shape with r&asymp;0). A "
          "scatterplot reveals curves or clusters that the coefficient hides."},
   {"t":"Trust it — r near 0 means no relationship of any kind",
    "why":"r near 0 only means no *linear* relationship. A strong curved (e.g., U-shaped) "
          "relationship can have r&asymp;0, so you must plot."},
   {"t":"Switch to a bigger font",
    "why":"Presentation won't reveal a hidden non-linear pattern; a scatterplot (or Spearman) "
          "will."},
   {"t":"Conclude one variable causes the other",
    "why":"You can't even claim a relationship yet, let alone causation. Plot first."}]},
 {"q":"When is Spearman's &rho; clearly preferable to Pearson's r?",
  "options":[
   {"t":"When the relationship is consistently increasing (or decreasing) but curved, or there are "
        "outliers","correct":True,
    "why":"Correct. Spearman uses ranks, so it captures monotonic-but-curved relationships and is "
          "robust to outliers, where Pearson (which needs linearity) underperforms."},
   {"t":"Whenever you want a bigger coefficient",
    "why":"Spearman isn't a trick to inflate numbers; it's appropriate when the relationship is "
          "monotonic/curved or has outliers, where it's simply more faithful."},
   {"t":"Only when the data is perfectly linear",
    "why":"For perfectly linear data Pearson is ideal; Spearman's advantage shows up for "
          "monotonic-curved or outlier-prone data."},
   {"t":"Never — Pearson is always better",
    "why":"Pearson is blind to non-linear monotonic patterns and sensitive to outliers; in those "
          "cases Spearman is the better choice."}]},
]))

p.append(B.practice([
 {"q":"r = 0.7 between hours studied and exam score. Your friend says '49% of the score is "
      "explained by studying.' Where does 49% come from, and is the phrasing okay?",
  "sol":"49% is r&sup2; = 0.7&sup2; = 0.49, the ~coefficient of determination~ &mdash; the share "
        "of variance in exam score *linearly associated with* hours studied. The number is right, "
        "but 'explained by' overstates it: r&sup2; describes shared linear variation, not proven "
        "causation. Studying may help, but confounders (motivation, prior ability) could inflate "
        "the association. Safer: 'studying accounts for about 49% of the variation in scores, "
        "though this is association, not proof of cause.'"},
 {"q":"Give one plausible confounder, one reverse-causation story, and note why 'more data' alone "
      "can't fix a non-causal correlation between 'using our app more' and 'higher revenue.'",
  "sol":"**Confounder:** highly engaged customers both use the app more *and* spend more &mdash; "
        "engagement drives both. **Reverse causation:** big spenders use the app more *because* "
        "they're already invested, not the other way around. **Why more data won't fix it:** a "
        "bigger sample shrinks the *standard error*, making the correlation more precise &mdash; "
        "but precision isn't causation. Only a randomized experiment (nudge some users to use the "
        "app more and compare revenue) or a causal method can establish direction."},
]))

p.append(B.deepdive(
 B.concept(
  "**r&sup2;, the coefficient of determination.** Squaring the correlation gives r&sup2;, the "
  "proportion of variance in one variable that is *linearly associated* with the other. r = 0.7 "
  "&rarr; r&sup2; = 0.49, so about half the variation is shared linearly. It's a useful effect-"
  "size companion to r &mdash; but the word people reach for, 'explained,' smuggles in causation "
  "it hasn't earned.") +
 B.concept(
  "**Spurious correlations.** Search enough unrelated time series and some will correlate "
  "beautifully by pure chance &mdash; US cheese consumption and deaths by bedsheet entanglement, "
  "the famous examples. With many variables, high correlations *will* appear randomly, which is "
  "why a correlation needs a plausible mechanism and ideally a pre-registered hypothesis, not just "
  "a striking scatterplot found after the fact.") +
 B.concept(
  "**The road to causation.** To move from 'correlates' to 'causes' you need to rule out "
  "confounders and reverse causation. The gold standard is a ~randomized experiment~ (Track 6): "
  "randomly assigning the treatment breaks the link to confounders. When you can't experiment, "
  "~causal inference~ methods (Track 7) &mdash; controlling for confounders, matching, "
  "difference-in-differences &mdash; get you closer. This lesson is the doorway to both."),
 title="Deep dive: r-squared, spurious correlations, and the path from correlation to causation"))

p.append(B.callout("note","Interview-ready",
 "*\"What's the difference between correlation and causation?\"* and *\"how would you tell them "
 "apart?\"* are perennial. Define correlation as linear co-movement, give the ice-cream/drownings "
 "confounder, and name the three traps (confounding, reverse causation, coincidence). Then land "
 "the closer: to establish causation you randomize (an experiment) or use causal-inference methods "
 "&mdash; never a coefficient alone.", "&#9670;"))

LESSONS={"stats-11-correlation":"\n".join(p)}
