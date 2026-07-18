# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Dates are everywhere in data &mdash; order dates, signups, timestamps, log entries &mdash; and "
 "they're a notorious source of bugs, because a date that arrives as the text `\"2025-03-14\"` is "
 "useless until Python understands it as a *moment in time*. Once it does, a world opens up: pull "
 "out the month or weekday, compute how many days between two events, and roll daily data up to "
 "monthly (the time-series EDA from Track 5). This lesson makes dates your friend."))

p.append(B.h2("Parsing: text into real dates", kicker="Concept"))
p.append(B.concept(
 "Data almost always arrives with dates as **strings**. The first step is to convert them into "
 "pandas ~datetime~ values with `pd.to_datetime(...)`, which understands most common formats "
 "automatically. Until you do this, a date column is just text &mdash; you can't sort it "
 "chronologically, subtract it, or extract parts from it. Always parse dates right after loading."))

p.append(B.h2("Extracting parts with .dt", kicker="Concept · the calendar toolbox"))
p.append(B.concept(
 "Once a column is real datetimes, the ~.dt accessor~ (the date cousin of `.str`) pulls calendar "
 "pieces out of every row at once: `.dt.year`, `.dt.month`, `.dt.day`, `.dt.hour`, "
 "`.dt.day_name()` (Monday&hellip;), `.dt.quarter`. These are how you create features like "
 "'month of purchase' or 'is it a weekend?' for analysis and modeling."))
p.append(B.figure(IMG+"s_py_datetime_parts.png",
 "**The .dt accessor.** One timestamp holds many calendar facts; `.dt` extracts each one as a "
 "column. This is the raw material for seasonal analysis and date-based features.",
 "A timestamp with arrows to its year, month, day, hour, weekday, and quarter via the .dt accessor."))

p.append(B.h2("Date arithmetic", kicker="Concept · durations"))
p.append(B.concept(
 "Subtracting two datetimes gives a ~Timedelta~ &mdash; a duration &mdash; whose `.days` (or "
 "`.total_seconds()`) you can read off: `(delivered - ordered).dt.days` is delivery time in days "
 "for a whole column. You can also add durations (`order_date + pd.Timedelta(days=30)`) and build "
 "ranges with `pd.date_range(...)`. Treating dates as quantities you can do math on is what makes "
 "questions like 'how long until churn?' answerable."))

p.append(B.h2("Parse, extract, and measure in code", kicker="Worked example"))
p.append(B.concept(
 "Convert text dates to real datetimes, pull out the month and weekday, and measure the span "
 "between the first and last order."))
_c,_o=_run(r'''
import pandas as pd

df = pd.DataFrame({"order_date": ["2025-01-05", "2025-03-14", "2025-12-25"]})
df["order_date"] = pd.to_datetime(df["order_date"])     # text -> real datetimes

df["month"]   = df["order_date"].dt.month               # extract calendar parts
df["weekday"] = df["order_date"].dt.day_name()
print(df.to_string(index=False))

span = df["order_date"].max() - df["order_date"].min()  # a Timedelta (duration)
print(f"\nfirst to last order: {span.days} days")
''')
p.append(B.code_example(_c,_o,filename="datetimes.py"))
p.append(B.warn(
 "The `.dt` accessor only works once the column is actually a datetime dtype &mdash; calling "
 "`.dt.month` on a column of date *strings* raises an error. The fix is always the same: "
 "`pd.to_datetime(...)` first, then check with `df.dtypes` (you want `datetime64`, not "
 "`object`). Parsing dates is part of the cleaning ritual from Lesson 1.10.", "&#9650;"))

p.append(B.keypoints([
 "Dates arrive as **text**; convert with `pd.to_datetime(...)` before doing anything time-aware.",
 "The ~.dt accessor~ extracts calendar parts column-wide: `.dt.year/month/day/hour`, "
 "`.dt.day_name()`, `.dt.quarter`.",
 "Subtracting datetimes gives a ~Timedelta~; read `.dt.days` for durations, and add "
 "`pd.Timedelta(days=n)` for date math.",
 "`.dt` requires a **datetime dtype** &mdash; check `df.dtypes` shows `datetime64`, not "
 "`object`.",
 "A datetime index unlocks `resample()` for rolling daily &rarr; monthly (Track 5 time-series).",
]))

p.append(B.quiz([
 {"q":"You load a CSV and `df[\"date\"].dt.month` raises an error. What's the likely cause and "
      "fix?",
  "options":[
   {"t":"The column is still text (object dtype); parse it with pd.to_datetime first","correct":True,
    "why":"Correct. `.dt` only works on datetime columns. Dates load as text by default, so "
          "`df[\"date\"] = pd.to_datetime(df[\"date\"])` first, then `.dt.month` works."},
   {"t":"The .dt accessor doesn't exist",
    "why":"`.dt` is a real pandas accessor &mdash; it just requires a datetime dtype. The error is "
          "from calling it on text."},
   {"t":"You must loop over rows to get months",
    "why":"No loop needed; once parsed to datetime, `.dt.month` vectorizes across the whole "
          "column."},
   {"t":"The CSV is corrupted",
    "why":"The data is fine; the column simply loaded as text. Parse it to datetime and `.dt` "
          "works."}]},
 {"q":"`(df[\"delivered\"] - df[\"ordered\"]).dt.days` computes what (assuming both are datetime "
      "columns)?",
  "options":[
   {"t":"The number of days between ordering and delivery, per row","correct":True,
    "why":"Correct. Subtracting two datetime columns yields a Timedelta per row; `.dt.days` reads "
          "off the whole-day duration &mdash; e.g., delivery time."},
   {"t":"The total number of rows",
    "why":"It returns a per-row duration in days, not a row count. `len(df)` would count rows."},
   {"t":"An error — you can't subtract dates",
    "why":"Subtracting datetimes is valid and gives a Timedelta. `.dt.days` extracts the day "
          "count."},
   {"t":"The dates concatenated as text",
    "why":"Because they're real datetimes (not strings), subtraction does date math, not "
          "concatenation."}]},
 {"q":"You want a 'is_weekend' feature from an `order_date` datetime column. Which approach works?",
  "options":[
   {"t":"Check df[\"order_date\"].dt.dayofweek >= 5 (Saturday=5, Sunday=6)","correct":True,
    "why":"Correct. `.dt.dayofweek` returns 0 (Monday) to 6 (Sunday), so `>= 5` flags weekends "
          "&mdash; a clean vectorized boolean feature."},
   {"t":"Subtract the dates from today",
    "why":"That gives an age in days, not whether the date is a weekend. Use `.dt.dayofweek`."},
   {"t":"Use .str.contains('Saturday')",
    "why":"`.str` is for text; a datetime column isn't text. Use the `.dt` accessor (e.g., "
          "`.dt.dayofweek` or `.dt.day_name()`)."},
   {"t":"It's not possible from a date",
    "why":"It's straightforward: `.dt.dayofweek >= 5` (or checking `.dt.day_name()`) gives the "
          "weekend flag."}]},
]))

p.append(B.practice([
 {"q":"You have a datetime column `signup`. Write expressions for (a) the signup year and (b) a "
      "boolean of whether each signup was in Q4.", "html": True,
  "sol": B.code_example('year   = df["signup"].dt.year\nis_q4  = df["signup"].dt.quarter == 4',
         filename="solution.py", runnable=False) + B.fmt(
         "`.dt.year` extracts the year column-wide; `.dt.quarter == 4` builds a boolean Series "
         "that's True for October&ndash;December signups &mdash; handy for seasonal cohort "
         "analysis.")},
 {"q":"A column `ts` of timestamps loaded as text. Write the two steps to (1) convert it and "
      "(2) verify the conversion worked.", "html": True,
  "sol": B.code_example('df["ts"] = pd.to_datetime(df["ts"])   # 1. parse text -> datetime\nprint(df["ts"].dtype)                 # 2. verify -> datetime64[ns]',
         filename="solution.py", runnable=False) + B.fmt(
         "Convert with `pd.to_datetime`, then confirm the dtype is `datetime64` (not `object`). "
         "If some values won't parse, add `errors=\"coerce\"` to turn the bad ones into `NaT` "
         "(the datetime version of NaN) rather than raising.")},
]))

p.append(B.deepdive(
 B.concept(
  "**Time zones &mdash; the deepest date rabbit hole.** A timestamp without a time zone is "
  "ambiguous: 9:00 where? pandas datetimes can be ~tz-naive~ (no zone) or ~tz-aware~ (anchored to "
  "UTC or a region). Mixing the two, or ignoring daylight-saving shifts, causes subtle off-by-an-"
  "hour bugs in logs and analytics. The professional habit: store and compute in **UTC**, and "
  "convert to a local zone only for display. Use `tz_localize` to attach a zone and `tz_convert` "
  "to change it.") +
 B.concept(
  "**Specifying formats and handling bad dates.** When dates come in an unusual or ambiguous "
  "layout (is `01/02/2025` January 2nd or February 1st?), pass an explicit `format=` to "
  "`pd.to_datetime` (e.g., `format=\"%d/%m/%Y\"`) so there's no guessing. For columns with some "
  "unparseable junk, `errors=\"coerce\"` converts the bad entries to `NaT` (Not a Time) instead "
  "of raising, letting you handle them as missing data afterward.") +
 B.concept(
  "**Under the hood: epoch time.** Computers often store a moment as a single number &mdash; "
  "~Unix/epoch time~, the seconds since midnight UTC on Jan 1, 1970. You'll meet it in logs and "
  "APIs; `pd.to_datetime(values, unit=\"s\")` turns those numbers into readable dates. Knowing "
  "this demystifies the giant integers that sometimes appear in 'date' columns, and connects to "
  "the time-series resampling and rolling tools from Track 5."),
 title="Deep dive: time zones, explicit formats & coercion, and epoch time"))

p.append(B.callout("note","Interview-ready",
 "Date handling questions favor the careful: 'parse to datetime first, then use `.dt`'; "
 "'subtracting dates gives a duration'; and the pro touch &mdash; 'store in UTC, convert for "
 "display' to avoid time-zone bugs. If a take-home has dates as text, the very first thing you "
 "do (and mention) is `pd.to_datetime` and a dtype check.", "&#9670;"))

LESSONS={"py-09-datetime":"\n".join(p)}
