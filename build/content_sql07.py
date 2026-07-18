# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

SETUP='''
import sqlite3
db=sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE orders (id INTEGER, name TEXT, amount REAL, status TEXT, created TEXT);
INSERT INTO orders VALUES
 (1,'  Ada ', 240,'paid',    '2025-01-14'),
 (2,'BLAKE',   45,'refunded','2025-01-20'),
 (3,'chen',   220,'paid',    '2025-02-03'),
 (4,'Diego',  130, NULL,     '2025-02-18'),
 (5,'Priya',  510,'paid',    '2025-03-09'),
 (6,'Blake', NULL,'pending', '2025-03-22');
""")
def run(sql):
    cur=db.execute(sql); cols=[c[0] for c in cur.description]; rows=cur.fetchall()
    cell=lambda v:"NULL" if v is None else (str(int(v)) if isinstance(v,float) and v==int(v) else str(v))
    w=[max(len(cell(v)) for v in [c,*(r[i] for r in rows)]) for i,c in enumerate(cols)]
    show=lambda vals:"  ".join(cell(v).ljust(w[i]) for i,v in enumerate(vals))
    print(show(cols)); print(show(["-"*n for n in w]))
    for r in rows: print(show(r))
'''

p.append(B.why(
 "Raw tables are rarely in the shape a question wants. You need to bucket a number into "
 "\"small / medium / large\", pull the **month** out of a date to chart a trend, replace missing "
 "values with a sensible default, and tidy inconsistent text like `'  Ada '` and `'BLAKE'` so they "
 "match. Doing this **in SQL** &mdash; instead of exporting to a spreadsheet &mdash; keeps your work "
 "reproducible and close to the data. This lesson is the in-query logic-and-cleaning toolkit: "
 "`CASE`, date functions, `COALESCE`, `CAST`, and the string helpers."))

p.append(B.h2("CASE WHEN: if / else inside a query", kicker="Concept"))
p.append(B.concept(
 "~CASE~ is SQL's if/else. It tests conditions in order and returns the first match: `CASE WHEN "
 "amount >= 300 THEN 'large' WHEN amount >= 150 THEN 'medium' ELSE 'small' END`. You can use it to "
 "add a labelled column, and &mdash; the powerful part &mdash; **inside an aggregate** to count or "
 "sum only rows that meet a condition. Here it buckets each order, then counts orders per bucket:"))
_c,_o=_run(SETUP+'''
print(">>> label each order by size")
run("""
    SELECT name, amount,
           CASE WHEN amount >= 300 THEN 'large'
                WHEN amount >= 150 THEN 'medium'
                ELSE 'small' END AS size
    FROM orders
    WHERE amount IS NOT NULL
""")
print()
print(">>> count orders in each size bucket (CASE inside an aggregate)")
run("""
    SELECT
      SUM(CASE WHEN amount >= 300 THEN 1 ELSE 0 END) AS large,
      SUM(CASE WHEN amount >= 150 AND amount < 300 THEN 1 ELSE 0 END) AS medium,
      SUM(CASE WHEN amount < 150 THEN 1 ELSE 0 END) AS small
    FROM orders
""")
''')
p.append(B.code_example(_c,_o,filename="case_when.py"))
p.append(B.tip(
 "`SUM(CASE WHEN condition THEN 1 ELSE 0 END)` is the classic \"count rows meeting a condition\" "
 "trick, and `SUM(CASE WHEN condition THEN amount ELSE 0 END)` sums only those rows. Put several such "
 "expressions in one `SELECT` and you've built a **pivot table** &mdash; one row, a column per "
 "category &mdash; entirely in SQL.", "&#10022;"))

p.append(B.h2("Dates: pull them apart and group by them", kicker="Concept"))
p.append(B.concept(
 "Dates are usually stored as text (`'2025-03-09'`) or numbers; the database gives you functions to "
 "read the parts. In SQLite that's ~strftime~: `strftime('%Y', created)` is the year, `'%m'` the "
 "month, `'%Y-%m'` the year-month. Grouping by a truncated date is how you turn a pile of timestamps "
 "into a monthly trend:"))
_c,_o=_run(SETUP+'''
run("""
    SELECT strftime('%Y-%m', created) AS month,
           COUNT(*)                   AS orders,
           COALESCE(SUM(amount), 0)   AS revenue
    FROM orders
    GROUP BY month
    ORDER BY month
""")
''')
p.append(B.code_example(_c,_o,filename="dates.py"))
p.append(B.note(
 "Every database spells date functions differently. SQLite uses `strftime(...)` and `date(...)`; most "
 "others use standard SQL like `EXTRACT(MONTH FROM created)` and `DATE_TRUNC('month', created)`. The "
 "**idea** &mdash; extract a part, or truncate to a period, then `GROUP BY` it &mdash; is identical "
 "everywhere; only the function name changes. Always confirm your engine's spelling.", "&#8250;"))

p.append(B.h2("Cleaning: COALESCE, CAST, and tidying text", kicker="Concept"))
p.append(B.concept(
 "Real columns have gaps and inconsistencies. The fixers:\n\n"
 "- ~COALESCE(a, b, ...)~ returns the first non-NULL argument &mdash; `COALESCE(status,'unknown')` "
 "replaces missing statuses with a label; `COALESCE(amount, 0)` treats a missing amount as zero.\n"
 "- ~CAST(x AS type)~ converts types &mdash; `CAST('90' AS REAL)` turns a numeric string into a "
 "number.\n"
 "- Text tidiers: ~TRIM~ removes surrounding spaces, `LOWER`/`UPPER` normalise case, `REPLACE` "
 "swaps substrings, and `||` concatenates. Here we clean the messy `name` column and fill the NULLs "
 "so equal-looking rows actually match:"))
_c,_o=_run(SETUP+'''
run("""
    SELECT
      LOWER(TRIM(name))            AS clean_name,
      COALESCE(status, 'unknown')  AS status,
      COALESCE(amount, 0)          AS amount
    FROM orders
    ORDER BY clean_name
""")
''')
p.append(B.code_example(_c,_o,filename="cleaning.py"))
p.append(B.concept(
 "After `LOWER(TRIM(name))`, `'  Ada '`, `'BLAKE'` (Blake) and `'Blake'` normalise so the two Blake "
 "rows finally read as the same person &mdash; essential before you `GROUP BY` a human-entered "
 "column. `COALESCE` turned Diego's missing status into `'unknown'` and order 6's missing amount into "
 "`0`, so downstream sums and filters behave."))

p.append(B.keypoints([
 "~CASE WHEN … THEN … ELSE … END~ is SQL's if/else &mdash; label rows, or put it **inside** SUM/"
 "COUNT to aggregate conditionally (and build pivots).",
 "Read date parts with `strftime('%Y-%m', col)` (SQLite) or `EXTRACT`/`DATE_TRUNC` (standard SQL); "
 "`GROUP BY` a truncated date for trends.",
 "~COALESCE(a,b,…)~ returns the first non-NULL &mdash; the clean way to supply defaults for missing "
 "values.",
 "~CAST(x AS REAL/INTEGER/TEXT)~ converts types; `TRIM`, `LOWER`/`UPPER`, `REPLACE`, `||` tidy text.",
 "Normalise human-entered text (`LOWER(TRIM(...))`) **before** grouping or joining on it, or "
 "duplicates won't match.",
]))

p.append(B.quiz([
 {"q":"What does `SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END)` compute?",
  "options":[
   {"t":"The total amount of only the paid orders","correct":True,
    "why":"Correct. For each row the CASE yields the amount when paid and 0 otherwise, so the SUM adds "
          "up only paid orders' amounts — conditional aggregation in one expression."},
   {"t":"The number of paid orders",
    "why":"That would be `SUM(CASE WHEN status='paid' THEN 1 ELSE 0 END)` (or COUNT with a filter). "
          "Using `amount` sums money, not a count."},
   {"t":"The total of all orders regardless of status",
    "why":"The ELSE 0 zeroes out non-paid orders, so unpaid amounts don't contribute."},
   {"t":"An error, because CASE can't go inside SUM",
    "why":"CASE inside an aggregate is valid and is the standard conditional-sum pattern."}]},
 {"q":"You want monthly revenue from a text `created` column like '2025-03-09' in SQLite. Which "
      "grouping key?",
  "options":[
   {"t":"GROUP BY strftime('%Y-%m', created)","correct":True,
    "why":"Correct. strftime('%Y-%m', created) truncates each date to its year-month, so grouping by "
          "it produces one row per month. (Include %Y so different years don't merge.)"},
   {"t":"GROUP BY created",
    "why":"That groups by the exact day, giving one row per distinct date, not per month."},
   {"t":"GROUP BY MONTH(created)",
    "why":"MONTH() isn't a SQLite function (that's other dialects), and using only the month would "
          "merge the same month across different years."},
   {"t":"GROUP BY amount",
    "why":"Grouping by amount buckets by price, not by time. You need a date-derived key."}]},
 {"q":"`COALESCE(amount, 0)` is used because…",
  "options":[
   {"t":"It replaces NULL amounts with 0 so sums/filters treat missing as zero","correct":True,
    "why":"Correct. COALESCE returns its first non-NULL argument, so a NULL amount becomes 0 — useful "
          "when 'no amount recorded' should count as zero downstream."},
   {"t":"It rounds amount to zero decimal places",
    "why":"That's ROUND. COALESCE is about NULL handling, not rounding."},
   {"t":"It removes rows where amount is NULL",
    "why":"It doesn't remove rows; it substitutes a value for NULL. To remove them you'd filter with "
          "`WHERE amount IS NOT NULL`."},
   {"t":"It casts amount to an integer",
    "why":"Type conversion is CAST. COALESCE just picks the first non-NULL value."}]},
]))

p.append(B.practice([
 {"q":"From `orders(status, amount)`, write ONE query returning three columns: total revenue from "
      "`paid` orders, total from `refunded` orders, and the count of `pending` orders.",
  "sol":"`SELECT SUM(CASE WHEN status='paid' THEN amount ELSE 0 END) AS paid_rev, SUM(CASE WHEN "
        "status='refunded' THEN amount ELSE 0 END) AS refunded_rev, SUM(CASE WHEN status='pending' "
        "THEN 1 ELSE 0 END) AS pending_ct FROM orders;` — three conditional aggregates in one row "
        "(a mini pivot)."},
 {"q":"A `name` column contains `'  Ada '`, `'ada'`, and `'ADA'` for the same person, so `GROUP BY "
      "name` splits them. How do you fix it in the query?",
  "sol":"Group by a normalised expression: `SELECT LOWER(TRIM(name)) AS person, COUNT(*) FROM orders "
        "GROUP BY LOWER(TRIM(name));` — TRIM removes the surrounding spaces and LOWER folds the case, "
        "so all three collapse into one group. (Better still, clean the data at load time.)"},
]))

p.append(B.deepdive(
 B.concept(
  "**CASE evaluates in order — put specific conditions first.** SQL returns the first `WHEN` that is "
  "true, so `CASE WHEN amount >= 150 THEN 'medium' WHEN amount >= 300 THEN 'large' …` would label a "
  "500 order 'medium', because the first branch already matched. Order your thresholds from most "
  "specific/highest to lowest, and remember `CASE` with no `ELSE` returns `NULL` for unmatched rows.") +
 B.concept(
  "**How dates are really stored.** SQLite has no dedicated date type — dates live as ISO-8601 text "
  "('2025-03-09'), which sorts and compares correctly *because* of that format. Other databases have "
  "real `DATE`/`TIMESTAMP` types. Two portable habits: store dates in ISO format, and truncate with "
  "the engine's function (`DATE_TRUNC`, `strftime`) rather than slicing strings by hand, so time "
  "zones and month lengths are handled for you.") +
 B.concept(
  "**COALESCE vs IFNULL vs NULLIF, and CAST gotchas.** `COALESCE(a,b,c)` is standard and takes many "
  "arguments; `IFNULL(a,b)` is a two-argument SQLite shorthand; `NULLIF(a,b)` returns NULL when "
  "`a=b` (handy to avoid divide-by-zero: `x / NULLIF(y,0)`). With `CAST`, know that SQLite is lax "
  "about types (it will quietly store a string in a numeric column), while stricter databases reject "
  "bad casts — so validate inputs rather than trusting an implicit conversion."),
 title="Deep dive: CASE ordering, how dates are stored, and COALESCE/NULLIF/CAST"))

p.append(B.callout("note","Interview-ready",
 "Two things impress here: the `SUM(CASE WHEN … THEN 1 ELSE 0 END)` conditional-aggregation / pivot "
 "pattern, and knowing that date handling is dialect-specific (extract a part or truncate, then "
 "`GROUP BY`). Mention `NULLIF(denominator, 0)` to avoid divide-by-zero and you'll sound like someone "
 "who has shipped real queries.", "&#9670;"))

LESSONS={"sql-07-case-dates":"\n".join(p)}
print("content_sql07 OK — chars:", len(LESSONS["sql-07-case-dates"]))
