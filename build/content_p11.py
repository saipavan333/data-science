# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Every analysis begins by **loading data** and ends by **saving results** &mdash; and both are "
 "messier in real life than any tutorial admits. Files come with odd delimiters, wrong encodings, "
 "numbers stored as text, and dates as strings. Knowing how to read data robustly (and write it "
 "back cleanly) is a quietly essential skill that saves hours of confusion at the start and end "
 "of every project."))

p.append(B.h2("Reading data from anywhere", kicker="Concept"))
p.append(B.concept(
 "Pandas reads almost any source into a DataFrame with a `read_*` function: `pd.read_csv` (by far "
 "the most common), plus `read_excel`, `read_json`, and `read_sql`. From there you work in the "
 "DataFrame, and when done, write results back out."))
p.append(B.figure(IMG+"s_io_sources.png",
 "**Data in, results out.** Whatever the source &mdash; CSV, Excel, JSON, a database, an API "
 "&mdash; `pd.read_*` brings it into a DataFrame; you analyze; then `df.to_*` writes it back to "
 "share or reuse.",
 "Diagram of data sources flowing through pd.read_* into a DataFrame and out via df.to_*."))
p.append(B.concept(
 "`read_csv` looks simple but has powerful options that fix most real-world mess:\n\n"
 "- `sep=` &mdash; the delimiter (comma by default; use `\"\\t\"` for tabs, `\";\"` for some "
 "European files).\n"
 "- `parse_dates=[\"date\"]` &mdash; parse date columns to datetimes on load (no separate step).\n"
 "- `dtype={...}` &mdash; force a column's type (e.g., keep a zip code as text).\n"
 "- `na_values=[...]` &mdash; treat sentinels like `\"N/A\"`, `\"-\"`, `\"free\"` as missing.\n"
 "- `encoding=` &mdash; the character encoding (`\"utf-8\"` usually; `\"latin-1\"` for some "
 "legacy files).\n"
 "- `nrows=` / `usecols=` &mdash; read only some rows/columns (handy for peeking at a huge file)."))

p.append(B.h2("Inspect immediately after loading", kicker="Concept · the ritual"))
p.append(B.concept(
 "The instant data lands, run the first-contact checklist (Lessons 2.7 and 3.1): `df.shape`, "
 "`df.head()`, `df.dtypes`, `df.isna().sum()`. The single most common surprise is a column you "
 "expected to be numeric showing up as `object` (text) &mdash; catch it here, before it silently "
 "breaks a calculation downstream."))

p.append(B.h2("Saving your results", kicker="Concept"))
p.append(B.concept(
 "When your analysis is done, write it out with `df.to_csv(\"out.csv\", index=False)`, "
 "`df.to_parquet(...)`, or `df.to_excel(...)`. The `index=False` matters: without it, pandas "
 "writes the row index as an extra unnamed column that confuses whoever reads the file next. "
 "Choose the format by purpose: **CSV** for universal sharing, **Parquet** for fast, compact, "
 "type-preserving storage of large data, **Excel** when a non-technical stakeholder will open it."))

p.append(B.h2("Read with options, then save", kicker="Worked example"))
p.append(B.concept(
 "Here's a tiny CSV (built in memory so it runs anywhere) loaded with real-world options "
 "&mdash; parsing the date and treating `\"free\"` as missing &mdash; then written back out "
 "cleanly."))
_c,_o=_run(r'''
import pandas as pd
from io import StringIO

raw = StringIO(
    "order_id,date,amount\n"
    "1001,2025-01-05,19.99\n"
    "1002,2025-01-06,free\n"      # 'free' should be a missing value, not text
    "1003,2025-01-07,29.50\n")

df = pd.read_csv(raw,
                 parse_dates=["date"],     # date column -> real datetimes
                 na_values=["free"])       # treat 'free' as NaN
print(df)
print("\ndtypes:", dict(df.dtypes.astype(str)))   # amount is float, date is datetime

clean_csv = df.to_csv(index=False)         # index=False: no stray index column
print("\nsaved CSV:\n" + clean_csv)
''')
p.append(B.code_example(_c,_o,filename="loading_data.py"))
p.append(B.concept(
 "Two options did real work: `parse_dates` turned the date column into datetimes (so `.dt` works), "
 "and `na_values` turned `\"free\"` into a proper `NaN` so `amount` is numeric instead of text. "
 "Loading data *thoughtfully* &mdash; rather than `read_csv` and hope &mdash; prevents a whole "
 "class of downstream bugs."))

p.append(B.keypoints([
 "`pd.read_csv` (and `read_excel/json/sql`) load data; `df.to_csv/parquet/excel` save it.",
 "Key `read_csv` options: `sep`, `parse_dates`, `dtype`, `na_values`, `encoding`, `usecols`/"
 "`nrows`.",
 "**Inspect right after loading** (`.shape`, `.dtypes`, `.isna().sum()`); the #1 surprise is "
 "numbers loaded as text.",
 "When saving CSV, pass `index=False` to avoid writing a stray index column.",
 "Format by purpose: **CSV** to share, **Parquet** for fast/compact big data, **Excel** for "
 "non-technical readers.",
]))

p.append(B.quiz([
 {"q":"After `pd.read_csv(\"sales.csv\")`, the `price` column is dtype `object` and sums "
      "concatenate instead of adding. Best fix at load time?",
  "options":[
   {"t":"Reload with options like na_values for bad entries (and/or pd.to_numeric afterward) so "
        "price parses as a number","correct":True,
    "why":"Correct. The column loaded as text because of non-numeric entries (e.g., 'N/A', '$'). "
          "Setting `na_values`/cleaning so it parses numeric &mdash; or `pd.to_numeric(..., "
          "errors='coerce')` after &mdash; restores a numeric column."},
   {"t":"Nothing — object columns add fine",
    "why":"Object (text) columns *concatenate* with `+`, they don't add. You must get the column "
          "to a numeric dtype."},
   {"t":"Delete the price column",
    "why":"That discards key data for a fixable parsing issue. Convert it instead."},
   {"t":"Re-export the file as Excel",
    "why":"Changing format doesn't fix non-numeric entries. Handle them with na_values / "
          "to_numeric so the column is numeric."}]},
 {"q":"Why pass `index=False` when calling `df.to_csv(...)`?",
  "options":[
   {"t":"To avoid writing the DataFrame's row index as an extra unnamed column","correct":True,
    "why":"Correct. By default `to_csv` writes the index as a leading column; `index=False` omits "
          "it, producing a clean file without a stray 'Unnamed: 0' column when re-read."},
   {"t":"To make the file smaller by dropping data",
    "why":"It doesn't drop your data columns &mdash; only the (usually unwanted) index column. The "
          "purpose is cleanliness, not compression."},
   {"t":"To sort the rows",
    "why":"`index=False` controls whether the index is written, not row order. Use `sort_values` "
          "to sort."},
   {"t":"It's required or to_csv fails",
    "why":"It's optional; without it the file still writes, just with an extra index column. You "
          "pass it for a clean output."}]},
 {"q":"You only need the first 1,000 rows and two columns of a 5 GB CSV just to inspect it. Which "
      "options help?",
  "options":[
   {"t":"nrows=1000 and usecols=[...] to read only part of the file","correct":True,
    "why":"Correct. `nrows` limits how many rows are read and `usecols` restricts to chosen "
          "columns &mdash; together they let you peek at a massive file without loading all of "
          "it."},
   {"t":"Read the whole 5 GB, then slice in pandas",
    "why":"That loads everything into memory first &mdash; slow and possibly impossible. Limit at "
          "read time with `nrows`/`usecols`."},
   {"t":"Convert to Excel first",
    "why":"Excel can't even hold 5 GB and would be slower. Use `nrows`/`usecols` on the CSV."},
   {"t":"There's no way to read part of a file",
    "why":"There is: `nrows`, `usecols`, and chunked reading all let you read part of a large "
          "file."}]},
]))

p.append(B.practice([
 {"q":"Write the `read_csv` call to load `data.csv` where the file is tab-separated, the `joined` "
      "column holds dates, and `\"-\"` means missing.", "html": True,
  "sol": B.code_example('df = pd.read_csv("data.csv",\n                 sep="\\t",\n                 parse_dates=["joined"],\n                 na_values=["-"])',
         filename="solution.py", runnable=False) + B.fmt(
         "`sep=\"\\t\"` reads tab-delimited data, `parse_dates=[\"joined\"]` turns that column "
         "into datetimes on load, and `na_values=[\"-\"]` converts the dash sentinels to NaN so "
         "they're treated as missing rather than text.")},
 {"q":"Your teammate's saved CSV opens with an extra first column called 'Unnamed: 0'. What "
      "happened, and how should they have saved it?", "html": True,
  "sol": B.fmt("They saved with `df.to_csv(\"file.csv\")` **without** `index=False`, so pandas "
         "wrote the row index as an unlabeled first column; on re-reading, that column shows up as "
         "'Unnamed: 0'. The fix is to save with `df.to_csv(\"file.csv\", index=False)`. (To "
         "recover the existing file, read it with `pd.read_csv(\"file.csv\", index_col=0)` to "
         "treat that column as the index, or just drop it.)")},
]))

p.append(B.deepdive(
 B.concept(
  "**The hidden traps of CSV.** CSV is universal but underspecified, which is why it bites: a "
  "**comma inside a field** ('Smith, Jr.') needs quoting or it splits into two columns; a "
  "**different encoding** garbles accented characters (fix with `encoding=`); a leading "
  "**byte-order mark (BOM)** can corrupt the first column name (use `encoding=\"utf-8-sig\"`); and "
  "**Excel auto-formatting** notoriously turns gene names and long IDs into dates or scientific "
  "notation. Reading with explicit `dtype` and `na_values`, and inspecting immediately, defends "
  "against all of these.") +
 B.concept(
  "**Why Parquet for serious data.** CSV stores everything as text, loses dtypes, and is large "
  "and slow to parse. ~Parquet~ is a binary, columnar format that **preserves types**, compresses "
  "well, and reads selected columns fast &mdash; often 5&ndash;10&times; smaller and quicker than "
  "the equivalent CSV. Use CSV for human-facing interchange, but reach for Parquet (`to_parquet`/"
  "`read_parquet`) for intermediate and large datasets in a pipeline.") +
 B.concept(
  "**Bigger than memory? Chunk or go out-of-core.** When a file won't fit in RAM, "
  "`pd.read_csv(..., chunksize=100_000)` yields the file in pieces you process one at a time, "
  "and tools like ~Dask~, ~Polars~, or a database handle datasets far beyond a single machine's "
  "memory. You don't need them yet, but knowing the escape hatch exists &mdash; and that the same "
  "DataFrame thinking largely carries over &mdash; means a big file is never a dead end."),
 title="Deep dive: CSV pitfalls, why Parquet, and handling files bigger than memory"))

p.append(B.callout("note","Interview-ready",
 "Real-world data questions reward the careful loader: 'I'd inspect dtypes right after read_csv, "
 "use `parse_dates` and `na_values` to handle dates and sentinels, and `dtype` to keep IDs as "
 "text.' Knowing the CSV traps (encodings, commas in fields, Excel mangling) and when to prefer "
 "Parquet signals you've wrangled actual messy data, not just clean tutorial files.", "&#9670;"))

LESSONS={"py-11-io":"\n".join(p)}
