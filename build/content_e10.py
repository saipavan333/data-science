# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "An ~outlier~ &mdash; a value far from the rest &mdash; is the most consequential point in your "
 "dataset, for two opposite reasons. It might be an **error** (a typo, a broken sensor) that will "
 "wreck your averages and models if you leave it. Or it might be the **signal you're hunting** "
 "&mdash; the fraud, the system failure, the whale customer &mdash; that you'd be insane to "
 "delete. EDA's job is to **find** outliers and help you **decide** which kind each one is, "
 "deliberately, never on autopilot."))

p.append(B.h2("Detecting outliers", kicker="Concept · finding them"))
p.append(B.concept(
 "Four complementary ways to flag suspicious points:\n\n"
 "- **Visually** &mdash; a boxplot shows points beyond its whiskers; a scatter plot exposes points "
 "off the cloud. Always look first.\n"
 "- The ~IQR rule~ &mdash; flag anything below Q1&minus;1.5&times;IQR or above Q3+1.5&times;IQR "
 "(the boxplot's fence, from Lesson 1.3). Robust, since it's based on quartiles, not the mean.\n"
 "- The ~z-score rule~ &mdash; flag points more than ~3 standard deviations from the mean "
 "(|z| &gt; 3). Simple, but assumes a roughly normal spread and is itself distorted by extreme "
 "outliers.\n"
 "- **Domain limits** &mdash; the best of all: a human age of 200 or a negative price is "
 "impossible *by definition*, no statistics required."))
p.append(B.figure(IMG+"s_eda_outliers.png",
 "**Two statistical flags.** Left: the IQR rule marks points beyond 1.5&times;IQR of the box. "
 "Right: the z-score rule marks points beyond &plusmn;3 SD. Here both catch the same extremes "
 "&mdash; but on skewed data they can disagree, which is why you also *look*.",
 "A boxplot flagging IQR outliers beside a z-score plot flagging points beyond 3 SD."))

p.append(B.h2("Deciding what to do", kicker="Concept · the judgment"))
p.append(B.concept(
 "Detection is the easy part; the decision is where judgment lives. Run each flagged point "
 "through one question first &mdash; *is this an error, or a real extreme?* &mdash; because the "
 "answer changes everything:"))
p.append(B.figure(IMG+"s_eda_outlier_decide.png",
 "**The outlier decision.** Impossible/error &rarr; fix or remove it (and document why). A real "
 "extreme &rarr; **keep it** &mdash; it may be the most important point in the data &mdash; and "
 "use robust methods, perhaps capping it. Unsure &rarr; investigate before touching it.",
 "Decision tree for handling an outlier: fix/remove, keep, or investigate."))
p.append(B.pitfall(
 "Never delete outliers reflexively to 'clean up' a chart or boost a model score. Deleting real "
 "extremes is how analysts miss fraud, hide system failures, and report a rosy average that the "
 "business never actually experiences. The default is **investigate and keep**; removal requires "
 "a justification you'd defend out loud.", "&#10007;"))

p.append(B.h2("Flag outliers two ways in code", kicker="Worked example"))
p.append(B.concept(
 "Detect the same data's outliers with both the IQR fence and the z-score rule, and compare what "
 "each catches &mdash; then the *human* decides what they mean."))
_c,_o=_run(r'''
import numpy as np
rng = np.random.default_rng(3)
data = np.append(rng.normal(50, 8, 200), [5, 95, 98])    # 200 normal points + 3 extremes

# IQR rule (robust: based on quartiles)
q1, q3 = np.percentile(data, [25, 75]); iqr = q3 - q1
lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
iqr_out = np.sort(data[(data < lo) | (data > hi)])
print(f"IQR fence [{lo:.0f}, {hi:.0f}]  ->  {len(iqr_out)} flagged: {np.round(iqr_out).astype(int)}")

# z-score rule (|z| > 3)
z = (data - data.mean()) / data.std()
z_out = np.sort(data[np.abs(z) > 3])
print(f"z-score |z|>3            ->  {len(z_out)} flagged: {np.round(z_out).astype(int)}")

print("\nBoth flag the extremes. Now the real work: are 5, 95, 98 errors -- or the signal?")
''')
p.append(B.code_example(_c,_o,filename="outliers.py"))

p.append(B.keypoints([
 "An ~outlier~ may be an **error** (remove/fix) or the **most important signal** (keep) &mdash; "
 "decide, don't auto-delete.",
 "Detect: **look** (boxplot/scatter), the ~IQR rule~ (beyond 1.5&times;IQR), the ~z-score rule~ "
 "(|z| &gt; 3), and **domain limits** (impossible values).",
 "The **IQR rule is robust** (quartile-based); the **z-score rule assumes ~normal** data and is "
 "itself skewed by outliers.",
 "Decision: error &rarr; fix/remove (document); real extreme &rarr; keep, use **robust stats**, "
 "maybe **cap (winsorize)**; unsure &rarr; investigate.",
 "Outliers have outsized influence on the mean, SD, correlation, and many models &mdash; that's "
 "why finding them matters.",
]))

p.append(B.quiz([
 {"q":"A fraud-detection dataset has a few transactions far larger than the rest. Your model "
      "scores better if you delete them. Should you?",
  "options":[
   {"t":"No — those extremes may be exactly the fraud you're trying to detect; deleting them "
        "defeats the purpose","correct":True,
    "why":"Correct. In anomaly detection the outliers are the signal. Removing them to flatter a "
          "metric throws away the very cases that matter. Investigate and keep."},
   {"t":"Yes — outliers always hurt models, so remove them",
    "why":"Outliers aren't always noise; here they're the target. Reflexive deletion is exactly "
          "the pitfall &mdash; you'd be deleting the fraud."},
   {"t":"Yes — a higher score is the goal",
    "why":"A score inflated by deleting the cases you're supposed to catch is meaningless. The "
          "goal is detecting fraud, which those points represent."},
   {"t":"Only if they exceed 3 standard deviations",
    "why":"The threshold doesn't change the principle: in fraud detection, extreme points are the "
          "signal, not noise to cut."}]},
 {"q":"Your data is heavily right-skewed. Which outlier rule is more trustworthy, and why?",
  "options":[
   {"t":"The IQR rule — it's based on quartiles, so it isn't distorted by the skew/extremes the "
        "way the mean and SD are","correct":True,
    "why":"Correct. The z-score uses the mean and SD, which extreme values inflate, so on skewed "
          "data it can mis-flag. The IQR rule, built on robust quartiles, behaves better."},
   {"t":"The z-score rule, because it always assumes normality",
    "why":"Assuming normality on clearly non-normal (skewed) data is exactly the weakness &mdash; "
          "the z-score becomes unreliable. Prefer the robust IQR rule."},
   {"t":"Neither can be used on skewed data",
    "why":"The IQR rule works fine (and is preferred) on skewed data; you can also transform "
          "first. It's the z-score that struggles."},
   {"t":"Both are identical on any data",
    "why":"They often disagree, especially on skewed data, because one uses quartiles and the "
          "other uses the mean/SD."}]},
 {"q":"You confirm an outlier is a **real** extreme value (not an error) but it's distorting your "
      "average. A reasonable option is to:",
  "options":[
   {"t":"Keep it but use robust statistics (median, IQR), or cap it (winsorize) — and report what "
        "you did","correct":True,
    "why":"Correct. For genuine extremes, switch to robust summaries or optionally cap/winsorize to "
          "limit influence, while documenting the choice. You preserve the truth without letting "
          "one point dominate."},
   {"t":"Silently delete it so the average looks nicer",
    "why":"Deleting a real value to improve a number is misleading. Use robust stats or transparent "
          "capping instead, and document it."},
   {"t":"Ignore it and report the distorted mean",
    "why":"Reporting a mean you know is distorted misleads stakeholders. Use a robust measure (the "
          "median) or cap, and be transparent."},
   {"t":"Change all the other values to match it",
    "why":"Altering legitimate data is fabrication. The right moves are robust statistics or "
          "documented capping."}]},
]))

p.append(B.practice([
 {"q":"List the four ways to detect outliers covered here, and note one strength of each.",
  "sol":"1. **Visual** (boxplot/scatter) &mdash; fast, shows context and shape, catches what rules "
        "miss. 2. **IQR rule** (beyond 1.5&times;IQR) &mdash; robust, quartile-based, works on "
        "skewed data. 3. **z-score** (|z|&gt;3) &mdash; simple and intuitive for roughly normal "
        "data. 4. **Domain limits** &mdash; definitive: impossible values (negative price, age "
        "200) are errors by definition, no statistics needed. Use several together."},
 {"q":"A `delivery_time` column has values 12, 15, 14, 16, 13, and 9000 (minutes). Walk through "
      "detecting and deciding.",
  "sol":"**Detect:** 9000 is obvious visually and via both rules (far beyond the IQR fence and "
        ">3 SD). **Decide:** ask whether 9000 minutes (~6 days) is an **error** or a **real** "
        "delivery. Likely a data-entry/sensor error (a stuck timer, or seconds logged as minutes) "
        "&mdash; investigate the source. If confirmed an error, **fix** (e.g., correct the unit) or "
        "**remove** it and document why; never just silently drop it. If it turned out to be a "
        "genuine 6-day delivery, you'd **keep** it (it's an important service failure) and report "
        "the **median** delivery time, which the 9000 barely moves."},
]))

p.append(B.deepdive(
 B.concept(
  "**Robust statistics resist outliers by design.** The mean and standard deviation have a "
  "~breakdown point~ of 0% &mdash; a single extreme value can drag them anywhere. Their robust "
  "cousins survive: the **median** and **IQR** tolerate up to ~25&ndash;50% contamination, and "
  "the ~MAD~ (median absolute deviation) is a robust stand-in for the SD. When outliers are "
  "present and you can't remove them, reporting and modeling with robust statistics keeps your "
  "conclusions honest.") +
 B.concept(
  "**Winsorizing vs. trimming.** Two transparent ways to limit outlier influence without pretending "
  "they don't exist: ~trimming~ drops the most extreme few percent, while ~winsorizing~ **caps** "
  "them at a percentile (e.g., set everything above the 99th percentile equal to the 99th "
  "percentile). Winsorizing keeps every row but bounds the extremes &mdash; useful for stabilizing "
  "a mean or a model input. Either way, **state what you did**; a silent cap is just another way "
  "to mislead.") +
 B.concept(
  "**Multivariate outliers hide from one-variable rules.** A point can be perfectly normal on "
  "every single variable yet bizarre in *combination* &mdash; a 7-foot-tall person weighing 100 "
  "pounds is ordinary on height alone and weight alone, but the pair is an outlier. One-dimensional "
  "IQR/z-score checks miss these; you need scatter plots, pair plots (Lesson 3.9), or methods "
  "built for it (Mahalanobis distance, isolation forests in Track 4). It's a reminder that EDA "
  "must look at variables *together*, not just one at a time."),
 title="Deep dive: robust statistics, winsorizing vs. trimming, and multivariate outliers"))

p.append(B.callout("note","Interview-ready",
 "The trap is the candidate who says 'I remove outliers' reflexively. The strong answer: 'It "
 "depends &mdash; first I'd check whether each is an error or a real extreme. Errors I fix or "
 "drop with documentation; genuine extremes I keep, using robust statistics or transparent "
 "capping, because they're often the most important signal (fraud, failures).' Mentioning the "
 "IQR-vs-z-score robustness difference is a bonus.", "&#9670;"))

LESSONS={"eda-10-outliers":"\n".join(p)}
