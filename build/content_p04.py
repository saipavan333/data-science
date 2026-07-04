# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Here's the part nobody puts on a highlight reel: **most of data science is cleaning data**. "
 "Real datasets arrive with missing values, text where numbers should be, duplicates, and "
 "impossible entries. Skip this step and every downstream number is quietly wrong &mdash; a "
 "polished model trained on garbage. Cleaning well, and being able to *defend every choice*, is "
 "what separates a trustworthy analyst from a dangerous one."))

p.append(B.h2("The cleaning workflow", kicker="Method"))
p.append(B.concept(
 "Cleaning isn't random fixing; it's a repeatable sequence. Inspect first &mdash; you can't fix "
 "what you haven't seen &mdash; then work through types, missingness, duplicates, and outliers, "
 "documenting each decision."))
p.append(B.figure(IMG+"s_clean_flow.png",
 "**The cleaning pipeline.** The amber steps (missing data, outliers) are judgment calls you must "
 "be able to justify; the rest are mechanical but essential. Always end by validating and writing "
 "down what you did.",
 "Seven-step data cleaning workflow from load to validate."))

p.append(B.h2("Missing data", kicker="Concept · the central decision"))
p.append(B.concept(
 "Pandas marks missing values as ~NaN~ ('not a number') and you detect them with "
 "`df.isna().sum()`. The real question is never *how* to fill a gap but *whether* to &mdash; and "
 "the honest answer depends on **why** the value is missing and **how much** is gone. Three "
 "defensible moves, from the capstone:"))
p.append(B.figure(IMG+"s_clean_missing.png",
 "**Drop, impute, or flag.** Drop only when missingness is rare and unrelated to what you "
 "measure; impute (fill with median/mode/model) to keep your sample size; flag (label 'Unknown' "
 "or add a 'was-missing' column) when the missingness itself carries information.",
 "Decision diagram for handling missing values: drop, impute, or flag."))
p.append(B.pitfall(
 "Two missing-data traps. First, **don't blanket-drop** rows with any NaN (`dropna()` on a wide "
 "table can delete most of your data and bias the rest). Second, **don't impute before splitting "
 "for modeling** &mdash; filling with a mean computed over the whole dataset leaks information "
 "from the test set into training (a Track 7 theme). Match the remedy to the cause, and do it at "
 "the right time.", "&#10007;"))

p.append(B.h2("Types, duplicates, outliers, and strings", kicker="Concept · the usual suspects"))
p.append(B.concept(
 "The rest of cleaning is a checklist of common messes:\n\n"
 "- **Wrong types:** numbers stored as text, dates as strings. Fix with `pd.to_numeric(...)` and "
 "`pd.to_datetime(...)`.\n"
 "- **Duplicates:** `df.drop_duplicates()` &mdash; but clean the keys first, so ' Austin' and "
 "'austin ' are recognized as the same.\n"
 "- **Outliers / impossible values:** negative prices, a 200-year-old customer. Investigate, then "
 "drop true errors or cap (`clip`) extreme-but-real values.\n"
 "- **Messy strings:** stray whitespace and inconsistent case, fixed in one vectorized pass with "
 "`.str.strip()` and `.str.title()`/`.str.lower()`."))

p.append(B.h2("Clean a messy table", kicker="Worked example"))
p.append(B.concept(
 "Here's a deliberately dirty little dataset &mdash; inconsistent city casing, numbers as text, "
 "two date formats, a duplicate, and missing values. Watch it become trustworthy, step by step."))
_c,_o=_run(r'''
import pandas as pd
import numpy as np

raw = pd.DataFrame({
    "city":   [" Austin", "austin ", "Denver", None, "Reno"],
    "spend":  ["29.0", "29.0", "99", "0", None],     # numbers stored as text
    "signup": ["2025-01-05", "2025-01-05", "2025/02/11", "2025-03-01", "2025-03-02"],
})
print("missing per column:\n", raw.isna().sum().to_string(), "\n")

df = raw.copy()
df["city"]   = df["city"].str.strip().str.title()        # tidy strings first
df["spend"]  = pd.to_numeric(df["spend"])                # text -> float
df["signup"] = pd.to_datetime(df["signup"], format="mixed")   # text -> datetime
df = df.drop_duplicates()                                # now ' Austin'/'austin ' match
df["city"]   = df["city"].fillna("Unknown")              # FLAG missing city
df["spend"]  = df["spend"].fillna(df["spend"].median())  # IMPUTE missing spend

print(df.to_string(index=False))
print("\nfinal dtypes:", dict(df.dtypes.astype(str)))
''')
p.append(B.code_example(_c,_o,filename="cleaning.py"))
p.append(B.concept(
 "Five lines turned a treacherous table into a trustworthy one: consistent cities, real numbers "
 "and dates, the duplicate gone, and the two gaps handled *differently and deliberately* &mdash; "
 "the city flagged as Unknown, the spend imputed with the median. If a stakeholder asks why, you "
 "have an answer for each. That is gold-standard cleaning."))

p.append(B.keypoints([
 "**Inspect before you fix**: `.info()`, `.dtypes`, `.isna().sum()`, `.duplicated().sum()`.",
 "Missing data: **drop** (rare & unrelated), **impute** (keep n), or **flag** (missingness is "
 "informative) &mdash; never reflexively `dropna()` everything.",
 "Fix types with `pd.to_numeric` / `pd.to_datetime`; a numeric column read as text is the #1 "
 "real-world bug.",
 "Clean keys **before** `drop_duplicates`; use `.str` accessors to standardize text in one pass.",
 "Investigate outliers and impossible values &mdash; **document every cleaning decision** so it's "
 "defensible and reproducible.",
]))

p.append(B.quiz([
 {"q":"`df.isna().sum()` shows the `income` column is 40% missing. What's the most reckless next "
      "step?",
  "options":[
   {"t":"Call df.dropna() to remove every row with any missing value","correct":True,
    "why":"Correct &mdash; that's the reckless choice. Dropping all rows with any NaN can delete a "
          "huge share of data and bias the rest. With 40% missing in one column, you'd consider "
          "imputing, flagging, or whether the column is usable at all."},
   {"t":"Investigate why income is missing before deciding",
    "why":"This is the responsible first move, not a reckless one &mdash; understanding the cause "
          "guides whether to impute, flag, or drop."},
   {"t":"Consider imputing or flagging the missing values",
    "why":"This is a reasonable, deliberate option &mdash; not reckless. The dangerous move is "
          "blanket-dropping rows."},
   {"t":"Check whether 'missing income' is itself informative",
    "why":"A sensible consideration (missingness can be a signal), not the reckless option. "
          "Blanket dropna() is the trap."}]},
 {"q":"After `pd.read_csv`, `df[\"price\"].mean()` raises a type error and `df.dtypes` shows "
      "`price` as `object`. What's the cause and fix?",
  "options":[
   {"t":"The column was read as text; convert it with pd.to_numeric(df[\"price\"], "
        "errors=\"coerce\")","correct":True,
    "why":"Correct. `object` dtype means strings, so numeric operations fail. `pd.to_numeric` "
          "converts to numbers, with `errors=\"coerce\"` turning unparseable entries into NaN to "
          "clean next."},
   {"t":"The CSV is corrupt and must be re-downloaded",
    "why":"The data is fine; it was just parsed as text (often due to stray characters like '$' or "
          "commas). Convert the dtype rather than re-downloading."},
   {"t":"Means can't be computed in pandas; use a loop",
    "why":"`.mean()` works perfectly on numeric columns. The issue is the column's text dtype, "
          "fixed with pd.to_numeric."},
   {"t":"Drop the price column entirely",
    "why":"That discards valuable data for a simple type problem. Convert it instead."}]},
 {"q":"Why clean string columns (strip/lowercase) *before* calling `drop_duplicates()`?",
  "options":[
   {"t":"So values like ' Austin' and 'austin ' are recognized as the same and actually get "
        "deduplicated","correct":True,
    "why":"Correct. `drop_duplicates` compares values exactly, so whitespace/case differences hide "
          "true duplicates. Standardizing first lets them match and collapse."},
   {"t":"Because drop_duplicates only works on numbers",
    "why":"It works on any column type. The reason to clean first is that exact string matching "
          "won't catch inconsistently formatted duplicates."},
   {"t":"It isn't necessary; order never matters",
    "why":"Order matters here: deduping before standardizing leaves near-duplicates that differ "
          "only by case or spaces uncollapsed."},
   {"t":"To make the file smaller on disk",
    "why":"The goal is correct deduplication, not file size. Cleaning keys first ensures genuine "
          "duplicates are detected."}]},
]))

p.append(B.practice([
 {"q":"A `rating` column should be 1&ndash;5, but you find values of 0 and 99. Walk through how "
      "you'd decide what to do.",
  "sol":"First **investigate**: are 0 and 99 sentinel codes (e.g., 0 = 'no rating given', 99 = "
        "'N/A') or genuine entry errors? Check counts and context. If they're sentinels for "
        "missing, **convert them to NaN** and then handle as missing (flag or impute). If they're "
        "errors with no recoverable truth, **drop or null them**. Don't silently leave them &mdash; "
        "a mean rating of 7.3 from stray 99s would mislead everyone. Document the decision."},
 {"q":"Explain why imputing a missing value with the column mean computed over the *entire* "
      "dataset can be a problem when you're about to build a predictive model.",
  "sol":"It causes **data leakage**: the mean uses information from rows that will become your "
        "test set, so the test data secretly influences the training features. Your model then "
        "looks better in validation than it will in production. The fix (Track 7) is to compute "
        "imputation values on the **training split only** and apply them to validation/test &mdash; "
        "typically inside a pipeline so it happens automatically per fold."},
]))

p.append(B.deepdive(
 B.concept(
  "**NaN is contagious &mdash; usually helpfully.** Arithmetic with NaN yields NaN ("
  "`5 + NaN = NaN`), which stops corrupt values from masquerading as real ones. But aggregations "
  "are smart: `df[\"x\"].mean()` **skips** NaNs by default rather than returning NaN. Know which "
  "behavior you're getting &mdash; sometimes you *want* `skipna=False` to catch that data is "
  "missing rather than silently averaging a subset.") +
 B.concept(
  "**Imputation has hidden costs.** Filling missing values with the mean shrinks the variable's "
  "variance and weakens correlations &mdash; you've invented certainty that isn't there. Median is "
  "more robust for skewed data; mode suits categories; model-based imputation (predicting the "
  "missing value from other columns) is most faithful but most complex. Whatever you choose, "
  "consider adding a **'was-missing' indicator column** so the model can learn that missingness "
  "itself meant something.") +
 B.concept(
  "**The categorical dtype.** Columns with few repeated values (region, plan, status) can be cast "
  "to pandas' `category` dtype. It stores each label once and references it by code &mdash; saving "
  "memory on large data and signaling intent (this is a label, not free text). It also makes "
  "value-counts and grouping faster, a small habit that pays off at scale."),
 title="Deep dive: NaN propagation, the real cost of imputation, and the categorical dtype"))

p.append(B.callout("note","Interview-ready",
 "*\"How do you handle missing data?\"* is asked constantly. Don't say 'I drop it.' Say: it "
 "depends on *why* it's missing and *how much* &mdash; then lay out drop / impute / flag with a "
 "one-line rationale for each, and mention the leakage risk of imputing before a train/test split. "
 "That nuance is exactly what distinguishes a careful analyst.", "&#9670;"))

LESSONS={"py-04-clean":"\n".join(p)}
