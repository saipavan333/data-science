# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "~Pandas~ is where you'll spend most of your data-science life. It's a spreadsheet that lives in "
 "code: NumPy's speed, plus labeled rows and columns and a deep toolbox for loading, cleaning, "
 "and reshaping real data. If you become fluent in one library, make it this one &mdash; every "
 "later track assumes it."))

p.append(B.h2("Series and DataFrame", kicker="Concept · the two objects"))
p.append(B.concept(
 "Pandas has exactly two core objects, and everything is built from them:\n\n"
 "- A ~Series~ is a one-dimensional labeled array &mdash; essentially a NumPy array with an "
 "**index** (row labels) bolted on. Think of it as a single column.\n"
 "- A ~DataFrame~ is a two-dimensional table &mdash; a collection of Series that share one index. "
 "Think of it as a whole spreadsheet: labeled columns, labeled rows."))
p.append(B.figure(IMG+"s_pd_dataframe.png",
 "**Anatomy of a DataFrame.** Columns have names, rows have an index, and each column is itself a "
 "Series. This labeling is the upgrade over a raw NumPy array: you refer to data by *meaning*, "
 "not just position.",
 "A labeled DataFrame with its index, columns, and one column highlighted as a Series."))

p.append(B.h2("Reading and inspecting data", kicker="Concept · first contact"))
p.append(B.concept(
 "You'll usually create a DataFrame by **reading a file**: `pd.read_csv(\"orders.csv\")` (and "
 "siblings `read_excel`, `read_sql`). The moment you load data, inspect it &mdash; the same "
 "first-contact ritual from the capstone:\n\n"
 "- `df.head()` &mdash; the first few rows\n"
 "- `df.shape` &mdash; (rows, columns)\n"
 "- `df.dtypes` / `df.info()` &mdash; the type of each column\n"
 "- `df.describe()` &mdash; quick summary statistics\n"
 "- `df.isna().sum()` &mdash; missing values per column"))

p.append(B.h2("Selecting data: columns, rows, and masks", kicker="Concept · the daily moves"))
p.append(B.concept(
 "Four selection patterns cover almost everything:\n\n"
 "- A **column**: `df[\"amount\"]` returns that Series.\n"
 "- By **label** with `.loc`: `df.loc[2, \"amount\"]` &mdash; row labeled 2, column 'amount'.\n"
 "- By **position** with `.iloc`: `df.iloc[0]` &mdash; the first row, regardless of its label.\n"
 "- By **boolean mask**: `df[df[\"amount\"] > 100]` &mdash; the rows where the test is True. This "
 "is the exact NumPy idea from last lesson, now filtering rows of a table."))
p.append(B.figure(IMG+"s_pd_loc_iloc.png",
 "**`loc` vs. `iloc`.** `loc` selects by the *label* in the index; `iloc` selects by integer "
 "*position*. They often differ &mdash; here label `\"a103\"` and position `2` happen to be the "
 "same row, but with a sorted or filtered index they won't be.",
 "A DataFrame showing loc selecting by label and iloc by position."))
p.append(B.warn(
 "The classic beginner mix-up: `.loc` is **label-based** and its slices are **inclusive** "
 "(`df.loc[0:2]` returns labels 0, 1, **and** 2), while `.iloc` is **position-based** and "
 "**exclusive** like normal Python (`df.iloc[0:2]` returns positions 0 and 1). When in doubt, ask "
 "yourself: am I using a *name* or a *position*?", "&#9650;"))

p.append(B.h2("A DataFrame, end to end", kicker="Worked example"))
p.append(B.concept(
 "Build a small DataFrame, inspect it, filter with a mask, and add a computed column &mdash; the "
 "core loop you'll repeat thousands of times."))
_c,_o=_run(r'''
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "category": ["Electronics", "Apparel", "Electronics", "Beauty", "Apparel"],
    "amount":   [180, 45, 220, 30, 95],
    "returned": [False, True, False, False, True],
})
print("shape:", df.shape)

# Filter rows with a boolean mask, then pick two columns.
big = df[df["amount"] > 100]
print("\norders over $100:")
print(big[["category", "amount"]].to_string(index=False))

# Add a computed column: net = amount unless the order was returned.
df["net"] = np.where(df["returned"], 0, df["amount"])
print("\nnet revenue per order:", df["net"].tolist(), "-> total $%d" % df["net"].sum())
''')
p.append(B.code_example(_c,_o,filename="pandas_intro.py"))
p.append(B.concept(
 "Notice how close this reads to plain English: *the rows where amount exceeds 100*, *net is zero "
 "if returned else the amount*. That readability, on top of NumPy speed, is why Pandas is the "
 "workhorse &mdash; and why the cleaning and reshaping in the next lessons feel natural."))

p.append(B.keypoints([
 "A ~Series~ is one labeled column; a ~DataFrame~ is a table of Series sharing an ~index~.",
 "Load with `pd.read_csv(...)`, then **inspect**: `.head()`, `.shape`, `.dtypes`/`.info()`, "
 "`.describe()`, `.isna().sum()`.",
 "Select a column with `df[\"col\"]`; rows by label with `.loc`, by position with `.iloc`.",
 "Filter rows with a **boolean mask**: `df[df[\"x\"] > k]` &mdash; the NumPy idea, applied to "
 "tables.",
 "`.loc` is label-based with **inclusive** slices; `.iloc` is position-based with **exclusive** "
 "slices.",
]))

p.append(B.quiz([
 {"q":"You want every row where `country` equals 'US'. Which expression is correct?",
  "options":[
   {"t":'df[df["country"] == "US"]',"correct":True,
    "why":"Correct. `df[\"country\"] == \"US\"` builds a boolean mask, and `df[mask]` returns the "
          "rows where it's True &mdash; standard boolean filtering."},
   {"t":'df.loc["US"]',
    "why":"`.loc` selects by index *label*, not by a column's value. Unless 'US' is a row label, "
          "this fails; you want a boolean mask on the country column."},
   {"t":'df["country" == "US"]',
    "why":"This compares the string \"country\" to \"US\" (always False) before indexing &mdash; a "
          "classic bug. The comparison must be on the column: df[\"country\"] == \"US\"."},
   {"t":'df.iloc["US"]',
    "why":"`.iloc` takes integer positions, not strings. \"US\" is not a position, so this errors."}]},
 {"q":"`df.loc[0:2]` and `df.iloc[0:2]` on a default-indexed DataFrame return different numbers of "
      "rows. Why?",
  "options":[
   {"t":"`.loc` label-slicing is inclusive (rows 0,1,2); `.iloc` position-slicing is exclusive "
        "(rows 0,1)","correct":True,
    "why":"Correct. `.loc[0:2]` includes the end label 2 (three rows), while `.iloc[0:2]` follows "
          "normal Python and excludes position 2 (two rows)."},
   {"t":"They return the same rows; there's no difference",
    "why":"They differ precisely because `.loc` is inclusive of the end label and `.iloc` is "
          "exclusive of the end position."},
   {"t":"`.iloc` is inclusive and `.loc` is exclusive",
    "why":"It's the reverse: `.loc` (labels) is inclusive; `.iloc` (positions) is exclusive."},
   {"t":"`.loc` only works on strings",
    "why":"`.loc` works on whatever the index labels are (integers here). The real difference is "
          "inclusive vs exclusive slicing."}]},
 {"q":"What is a single column of a DataFrame, like `df[\"amount\"]`?",
  "options":[
   {"t":"A Series — a 1D labeled array sharing the DataFrame's index","correct":True,
    "why":"Correct. Each column is a Series: a one-dimensional labeled array. Operations on it "
          "(sum, mean, masks) are vectorized like NumPy."},
   {"t":"A Python list of the values",
    "why":"It's a pandas Series, not a plain list (though `.tolist()` can convert it). The Series "
          "keeps the index and supports vectorized operations."},
   {"t":"Another DataFrame with one column",
    "why":"Selecting with single brackets `df[\"amount\"]` returns a Series; double brackets "
          "`df[[\"amount\"]]` would return a one-column DataFrame."},
   {"t":"A NumPy array with no labels",
    "why":"Underneath it uses a NumPy array, but a Series adds an index (labels). Use `.values` or "
          "`.to_numpy()` to get the bare array."}]},
]))

p.append(B.practice([
 {"q":"Write the expression to select the `email` column only for rows where `active` is True.",
  "sol":"`df.loc[df[\"active\"], \"email\"]`. The boolean Series `df[\"active\"]` selects the rows, "
        "and `.loc[rows, \"email\"]` picks the column &mdash; returning the emails of active users "
        "as a Series. (`df[df[\"active\"]][\"email\"]` also works but chained indexing is best "
        "avoided; see the deep dive.)"},
 {"q":"You read a CSV and `df[\"price\"].sum()` returns a concatenated string like "
      "'19.9929.99...' instead of a number. What happened, and how do you check and fix it?",
  "sol":"The `price` column was read as **text** (dtype `object`), so `+` concatenates strings "
        "instead of adding. Check with `df.dtypes` (or `df.info()`); you'll see `object` rather "
        "than `float64`. Fix with `df[\"price\"] = pd.to_numeric(df[\"price\"], errors=\"coerce\")`, "
        "which converts to numbers (turning any unparseable entries into NaN to handle next). "
        "Always verify dtypes right after loading."},
]))

p.append(B.deepdive(
 B.concept(
  "**The index is a feature, not decoration.** A DataFrame's index can be meaningful &mdash; dates "
  "for a time series, customer IDs, a multi-level (hierarchical) index for grouped data. A good "
  "index makes lookups, joins, and time-based slicing fast and expressive (`df.loc[\"2025-03\"]` "
  "to grab March). Setting the right index with `set_index` is often the first step that makes "
  "later code clean.") +
 B.concept(
  "**Chained indexing and SettingWithCopyWarning.** Writing `df[df.x > 0][\"y\"] = 5` chains two "
  "indexing operations, and pandas can't tell if you're editing the original or a temporary copy "
  "&mdash; so the assignment may silently do nothing, and you get a `SettingWithCopyWarning`. The "
  "fix is a single `.loc`: `df.loc[df.x > 0, \"y\"] = 5`. When you genuinely want a separate "
  "DataFrame, call `.copy()` explicitly (the reference trap again).") +
 B.concept(
  "**Vectorized string and date accessors.** Pandas extends vectorization to text and time via "
  "`.str` and `.dt`: `df[\"city\"].str.strip().str.lower()` cleans an entire column at once, and "
  "`df[\"signup\"].dt.month` extracts the month from a whole date column. No loops &mdash; the "
  "same array-thinking from NumPy, now for strings and timestamps. You'll lean on these constantly "
  "in the next lesson."),
 title="Deep dive: the power of the index, chained-indexing pitfalls, and .str/.dt accessors"))

p.append(B.callout("note","Interview-ready",
 "Pandas questions are ubiquitous: 'filter these rows,' 'add this column,' 'what's the difference "
 "between loc and iloc?' Answer the last one crisply &mdash; loc is label-based and inclusive, "
 "iloc is position-based and exclusive &mdash; and always inspect dtypes after loading, since a "
 "numeric column read as text is the single most common real-world gotcha.", "&#9670;"))

LESSONS={"py-03-pandas-intro":"\n".join(p)}
