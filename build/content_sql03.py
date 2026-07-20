# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

SETUP = '''
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE orders (
    id INTEGER, customer TEXT, category TEXT, amount REAL, country TEXT
);
INSERT INTO orders VALUES
 (101,'Ada',  'Electronics',240,'US'),
 (102,'Blake','Apparel',     45,'US'),
 (103,'Chen', 'Electronics',220,'CA'),
 (104,'Diego','Home',       130,'MX'),
 (105,'Ada',  'Apparel',    190,'US'),
 (106,'Priya','Electronics',510,'CA'),
 (107,'Blake','Home',       160,'US'),
 (108,'Chen', 'Electronics',300,'US'),
 (109,'Sara', 'Apparel',    NULL,'CA');
""")
def run(sql):
    cur  = db.execute(sql)
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()
    cell = lambda v: "NULL" if v is None else str(v)
    w = [max(len(cell(v)) for v in [col, *(r[i] for r in rows)]) for i, col in enumerate(cols)]
    show = lambda vals: "  ".join(cell(v).ljust(w[i]) for i, v in enumerate(vals))
    print(show(cols)); print(show(["-"*n for n in w]))
    for r in rows: print(show(r))
'''

p.append(B.why(
 "You will constantly be asked questions that begin with \"how many\", \"what's the total\", or "
 "\"what's the average … **per** …\": revenue per category, orders per customer, signups "
 "per country per week. Answering them means **collapsing many rows into one number per group** "
 "— and that is exactly what `GROUP BY` does. It is the single most useful pattern in analytics "
 "SQL, and the engine behind every dashboard you have ever seen. Master it and you can turn a "
 "million-row table into the two-line summary a decision actually needs."))

p.append(B.h2("First, aggregate the whole table", kicker="Concept"))
p.append(B.concept(
 "An ~aggregate function~ takes many rows and returns **one** value. The five you will use every day "
 "are `COUNT` (how many), `SUM` (total), `AVG` (mean), `MIN`, and `MAX`. Applied with no grouping, "
 "they summarise the entire table at once. One subtlety to notice up front: `COUNT(*)` counts "
 "**rows**, while `COUNT(amount)` counts only rows where `amount` is **not NULL** — and `SUM`/"
 "`AVG` also quietly skip NULLs. Our table has one order with a missing `amount`, so watch those two "
 "counts disagree:"))
_c,_o=_run(SETUP + '''
run("""
    SELECT COUNT(*)            AS n_rows,
           COUNT(amount)       AS n_with_amount,
           SUM(amount)         AS total,
           ROUND(AVG(amount),2) AS avg_amount,
           MIN(amount)         AS smallest,
           MAX(amount)         AS largest
    FROM orders
""")
''')
p.append(B.code_example(_c,_o,filename="aggregate_all.py"))
p.append(B.concept(
 "There are 9 rows but only 8 have an amount, so `COUNT(*)` and `COUNT(amount)` differ by one. The "
 "average is the total divided by **8**, not 9 — NULLs were left out, not treated as zero. That "
 "distinction (skip vs. treat-as-zero) changes the answer, and interviewers love to probe it."))

p.append(B.h2("GROUP BY: one row per group", kicker="Concept · the core move"))
p.append(B.concept(
 "~GROUP BY~ splits the rows into groups that share a value, runs the aggregate **inside each "
 "group**, and returns **one row per group**. `SELECT category, SUM(amount) FROM orders GROUP BY "
 "category` gives you the revenue of each category. The rule that keeps beginners honest: every "
 "column in your `SELECT` must either be **in the `GROUP BY`** or wrapped in an **aggregate** "
 "— anything else is ambiguous (which row's value would it show?). Here is revenue and order "
 "count per category, biggest first:"))
_c,_o=_run(SETUP + '''
run("""
    SELECT category,
           COUNT(*)            AS orders,
           SUM(amount)         AS revenue,
           ROUND(AVG(amount),1) AS avg_order
    FROM orders
    GROUP BY category
    ORDER BY revenue DESC
""")
''')
p.append(B.code_example(_c,_o,filename="group_by_category.py"))
p.append(B.figure(IMG+"s_pd_groupby.png",
 "**Split &middot; apply &middot; combine — the mental model behind every `GROUP BY`.** SQL "
 "splits the rows into groups by your key, applies the aggregate to each group, and combines the "
 "results into one row per group. (The picture shows it with pandas' `groupby`, but the idea is "
 "identical — `GROUP BY category` is the SQL spelling of exactly this.)",
 "Diagram: rows split into groups by category, an aggregate applied to each, combined into one row per group."))

p.append(B.h2("WHERE vs HAVING: filter rows, then filter groups", kicker="Concept"))
p.append(B.concept(
 "There are two different places to filter, and mixing them up is a top interview mistake. ~WHERE~ "
 "removes **rows** *before* grouping. ~HAVING~ removes **groups** *after* the aggregate is computed. "
 "So \"only US orders\" is a `WHERE` (it's about individual rows); \"only categories whose total "
 "revenue exceeds 400\" is a `HAVING` (it's about a group's aggregate). You can use both at once, "
 "and often do:"))
_c,_o=_run(SETUP + '''
run("""
    SELECT category,
           SUM(amount) AS us_revenue
    FROM orders
    WHERE country = 'US'          -- rows first: keep only US orders
    GROUP BY category
    HAVING SUM(amount) > 200      -- then groups: keep big-revenue categories
    ORDER BY us_revenue DESC
""")
''')
p.append(B.code_example(_c,_o,filename="where_vs_having.py"))
p.append(B.tip(
 "A quick test for which clause to use: if the condition could be checked on a **single raw row** "
 "(a country, a date, a status), it belongs in `WHERE`. If it needs a **group's aggregate** (a SUM, "
 "a COUNT, an AVG), it belongs in `HAVING`. `WHERE` runs first and is also faster, so filter rows "
 "there whenever you can.", "&#10022;"))

LAB_DB = """
CREATE TABLE orders (id INTEGER, customer TEXT, category TEXT, amount REAL, country TEXT);
INSERT INTO orders VALUES
 (101,'Ada','Electronics',240,'US'),(102,'Blake','Apparel',45,'US'),
 (103,'Chen','Electronics',220,'CA'),(104,'Diego','Home',130,'MX'),
 (105,'Ada','Apparel',190,'US'),(106,'Priya','Electronics',510,'CA'),
 (107,'Blake','Home',160,'US'),(108,'Chen','Electronics',300,'US'),
 (109,'Sara','Apparel',NULL,'CA');
"""
p.append(B.h2("Your turn — aggregate it yourself", kicker="Interactive lab"))
p.append(B.lab(
 "Return each **category** with its number of orders and total revenue, highest revenue first. "
 "Name the columns `category`, `orders`, `revenue`.",
 LAB_DB,
 "SELECT category, COUNT(*) AS orders, SUM(amount) AS revenue FROM orders GROUP BY category ORDER BY revenue DESC",
 starter="-- orders(id, customer, category, amount, country)\\nSELECT ",
 hint="`GROUP BY category`, then `COUNT(*)` and `SUM(amount)`. Sort with `ORDER BY revenue DESC`.",
 title="Lab 1 - revenue per category"))
p.append(B.lab(
 "Now filter the groups: return only the **countries** whose **total** revenue is above 400, with "
 "that total as `revenue`. Which clause filters a group total?",
 LAB_DB,
 "SELECT country, SUM(amount) AS revenue FROM orders GROUP BY country HAVING SUM(amount) > 400 ORDER BY revenue DESC",
 starter="-- filter on a GROUP's total, not a row\\nSELECT ",
 hint="A condition on `SUM(amount)` is about a group, so it belongs in `HAVING`, not `WHERE`.",
 title="Lab 2 - HAVING vs WHERE",
 explain="`HAVING SUM(amount) > 400` runs after grouping; `WHERE` couldn't see the total at all."))

p.append(B.keypoints([
 "An ~aggregate~ (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) turns many rows into one number.",
 "`COUNT(*)` counts **rows**; `COUNT(col)` counts **non-NULL** values; `SUM`/`AVG` **skip** NULLs "
 "(they are not treated as 0).",
 "~GROUP BY~ = **one result row per group**. Every selected column must be in the `GROUP BY` or "
 "inside an aggregate.",
 "~WHERE~ filters **rows before** grouping; ~HAVING~ filters **groups after** aggregating. Use both "
 "together freely.",
 "This is ~split &middot; apply &middot; combine~ — the same idea as pandas `groupby`.",
]))

p.append(B.quiz([
 {"q":"A table has 100 rows; the `amount` column is NULL for 10 of them. What does `SELECT "
      "COUNT(*), COUNT(amount), AVG(amount) FROM t` tell you?",
  "options":[
   {"t":"COUNT(*) = 100, COUNT(amount) = 90, and AVG divides the total by 90","correct":True,
    "why":"Correct. COUNT(*) counts every row; COUNT(amount) counts only non-NULL amounts (90); and "
          "AVG sums the 90 real values and divides by 90 — NULLs are skipped, not zeroed."},
   {"t":"All three equal 100",
    "why":"COUNT(amount) and AVG ignore the 10 NULLs, so they are based on 90 values, not 100."},
   {"t":"AVG treats the 10 NULLs as 0, pulling the average down",
    "why":"That's the common misconception. SQL skips NULLs entirely in AVG/SUM; it does not treat "
          "them as zero, so they don't drag the mean down."},
   {"t":"The query errors because of the NULLs",
    "why":"Aggregates handle NULLs gracefully by skipping them; there is no error."}]},
 {"q":"You want categories whose **total** revenue is over 1000. Which clause filters that?",
  "options":[
   {"t":"HAVING SUM(amount) > 1000 — it filters groups after aggregating","correct":True,
    "why":"Correct. A total is a group aggregate, so it must be filtered after grouping, which is "
          "exactly what HAVING does."},
   {"t":"WHERE amount > 1000",
    "why":"WHERE runs on individual rows before grouping, so this would keep only single orders over "
          "1000 — not categories whose *total* exceeds 1000."},
   {"t":"WHERE SUM(amount) > 1000",
    "why":"You can't use an aggregate in WHERE — aggregates don't exist yet when WHERE runs. "
          "That's precisely why HAVING exists."},
   {"t":"ORDER BY SUM(amount) > 1000",
    "why":"ORDER BY sorts; it doesn't filter. You need HAVING to drop groups."}]},
 {"q":"`SELECT customer, category, SUM(amount) FROM orders GROUP BY customer` errors or misbehaves in "
      "strict SQL. Why?",
  "options":[
   {"t":"`category` is neither grouped nor aggregated, so which category to show is ambiguous","correct":True,
    "why":"Correct. Grouping by customer collapses each customer's rows into one, but a customer can "
          "have several categories — SQL can't pick one. Add category to GROUP BY, or aggregate "
          "it (e.g., COUNT(DISTINCT category))."},
   {"t":"You can't SUM and GROUP BY in the same query",
    "why":"You can — that's the normal pattern. The problem is the un-grouped, un-aggregated "
          "`category` column."},
   {"t":"GROUP BY must always be the first clause",
    "why":"Clause order is fixed (GROUP BY comes after WHERE), but that's not the issue here; the "
          "issue is the ambiguous `category` column."},
   {"t":"SUM only works on integer columns",
    "why":"SUM works on any numeric column, including REAL. The real issue is the ungrouped column."}]},
]))

p.append(B.practice([
 {"q":"From `orders(customer, category, amount, country)`, write a query giving each **country** its "
      "number of orders and total revenue, highest-revenue country first.",
  "sol":"`SELECT country, COUNT(*) AS orders, SUM(amount) AS revenue FROM orders GROUP BY country "
        "ORDER BY revenue DESC;` — group by the country column, count rows and sum amount within "
        "each group, then sort the groups by their total."},
 {"q":"Write a query that returns only the **customers who have placed more than one order**, with "
      "how many each has. Which clause enforces \"more than one\"?",
  "sol":"`SELECT customer, COUNT(*) AS n FROM orders GROUP BY customer HAVING COUNT(*) > 1 ORDER BY "
        "n DESC;` — the \"more than one\" test is on a **group's count**, so it goes in "
        "`HAVING`, not `WHERE`. (WHERE couldn't see COUNT(*) at all.)"},
]))

p.append(B.deepdive(
 B.concept(
  "**The execution order explains the rules.** SQL runs the clauses as `FROM` &rarr; `WHERE` &rarr; "
  "`GROUP BY` &rarr; `HAVING` &rarr; `SELECT` &rarr; `ORDER BY`. That single fact answers most "
  "\"why can't I …\" questions: `WHERE` can't use an aggregate (aggregates don't exist until "
  "`GROUP BY` runs, which is *after* `WHERE`); `HAVING` can (it runs after); and a column alias you "
  "define in `SELECT` isn't usable in `WHERE` or `GROUP BY` (they ran earlier) but usually *is* "
  "usable in `ORDER BY` (which runs last).") +
 B.concept(
  "**The three COUNTs.** `COUNT(*)` counts rows. `COUNT(col)` counts "
  "rows where `col` is non-NULL — handy for \"how many orders actually have a recorded amount?\" "
  "`COUNT(DISTINCT col)` counts *distinct* non-NULL values — \"how many different categories "
  "does this customer buy?\" Choosing the wrong one silently changes the number, so name to yourself "
  "which of the three a question is really asking.") +
 B.concept(
  "**Grouping by more than one key, and grouping NULLs.** `GROUP BY country, category` makes one row "
  "per (country, category) pair — a two-dimensional summary, the basis of a pivot table. And "
  "note that `GROUP BY` puts **all NULLs into a single group** (SQL treats them as \"the same "
  "unknown\" here, an exception to the usual rule that NULL never equals NULL). So a grouped result "
  "can contain a NULL group — often exactly the \"missing / unset\" bucket you want to inspect."),
 title="Deep dive: execution order, the three COUNTs, and multi-key / NULL grouping"))

p.append(B.callout("note","Interview-ready",
 "The classic prompt is *\"difference between WHERE and HAVING?\"* — WHERE filters rows before "
 "grouping, HAVING filters groups after aggregating, and you can't put an aggregate in WHERE because "
 "of execution order. Pair that with knowing `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)` and "
 "you'll handle the aggregation portion of any SQL screen cleanly.", "&#9670;"))

LESSONS={"sql-03-aggregate":"\n".join(p)}
print("content_sql03 OK — chars:", len(LESSONS["sql-03-aggregate"]))
