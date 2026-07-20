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
CREATE TABLE sales (region TEXT, month INTEGER, amount REAL);
INSERT INTO sales VALUES
 ('East',1,100),('East',2,140),('East',3,140),
 ('West',1,200),('West',2, 90),('West',3,260);
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
 "Here is the technique that shows up in almost every serious SQL interview and quietly powers most "
 "analytics: the ~window function~. `GROUP BY` answers \"what's the total per region?\" but "
 "**destroys** the individual rows to do it. A window function answers \"what's each sale, *and* its "
 "region's running total, *and* its rank within the region?\" &mdash; keeping **every row** while "
 "adding computed columns that see across the other rows. Once it clicks, a whole class of questions "
 "(running totals, rankings, top-N-per-group, month-over-month change) becomes easy."))

p.append(B.h2("The core idea: aggregate without collapsing", kicker="Concept · the aha")
)
p.append(B.concept(
 "A window function computes a value over a ~window~ &mdash; a set of rows related to the current row "
 "&mdash; **without** merging them into one. You write it as `func(...) OVER (PARTITION BY ... ORDER "
 "BY ...)`. The `OVER` clause is what makes it a window function; `PARTITION BY` splits the rows into "
 "independent groups (like `GROUP BY`, but the rows survive). Compare the two: `GROUP BY` gives one "
 "row per region; the window version keeps all six rows and *attaches* the region total to each:"))
_c,_o=_run(SETUP+'''
print(">>> GROUP BY: one row per region (rows collapsed)")
run("SELECT region, SUM(amount) AS region_total FROM sales GROUP BY region")
print()
print(">>> WINDOW: every row kept, region total added as a column")
run("""
    SELECT region, month, amount,
           SUM(amount) OVER (PARTITION BY region) AS region_total
    FROM sales
    ORDER BY region, month
""")
''')
p.append(B.code_example(_c,_o,filename="window_vs_groupby.py"))
p.append(B.concept(
 "Same totals (East 380, West 550) &mdash; but the window version keeps every sale next to its "
 "region total, so you could immediately compute each sale's **share** of its region "
 "(`amount * 1.0 / SUM(amount) OVER (PARTITION BY region)`) without a join. That \"keep the detail, "
 "add the context\" move is the whole point."))

p.append(B.h2("Ranking: ROW_NUMBER, RANK, DENSE_RANK", kicker="Concept")
)
p.append(B.concept(
 "Add `ORDER BY` inside `OVER` and you can **rank** rows. Three ranking functions differ only in how "
 "they treat **ties**:\n\n"
 "- ~ROW_NUMBER~ gives every row a unique number 1,2,3,… (ties broken arbitrarily).\n"
 "- ~RANK~ gives tied rows the **same** rank, then **skips** the next numbers (…3, 3, 5…).\n"
 "- ~DENSE_RANK~ gives tied rows the same rank but **does not skip** (…3, 3, 4…).\n\n"
 "Our East region has two months tied at 140, so the difference is visible:"))
_c,_o=_run(SETUP+'''
run("""
    SELECT region, month, amount,
           ROW_NUMBER() OVER (ORDER BY amount DESC) AS row_num,
           RANK()       OVER (ORDER BY amount DESC) AS rnk,
           DENSE_RANK() OVER (ORDER BY amount DESC) AS dense
    FROM sales
    ORDER BY amount DESC
""")
''')
p.append(B.code_example(_c,_o,filename="ranking.py"))
p.append(B.concept(
 "See the two 140 rows: `RANK` gives them both 3 and then jumps to 5; `DENSE_RANK` gives them 3 and "
 "then 4; `ROW_NUMBER` refuses to tie and assigns 3 and 4 arbitrarily. Which you want depends on the "
 "question &mdash; \"3rd highest distinct amount\" is `DENSE_RANK`, \"exactly one row per position\" "
 "is `ROW_NUMBER`."))

p.append(B.h2("Running totals and period-over-period: ORDER BY + LAG", kicker="Worked example")
)
p.append(B.concept(
 "Put `ORDER BY` inside `OVER` on a **running** aggregate and each row sees all rows *up to and "
 "including* itself &mdash; a ~running total~. And ~LAG~ fetches a value from the **previous** row in "
 "the window (LEAD, the next), which is how you compute month-over-month change without a self-join. "
 "Both partitioned by region so each region is independent:"))
_c,_o=_run(SETUP+'''
run("""
    SELECT region, month, amount,
           SUM(amount) OVER (PARTITION BY region ORDER BY month) AS running_total,
           amount - LAG(amount) OVER (PARTITION BY region ORDER BY month) AS vs_last_month
    FROM sales
    ORDER BY region, month
""")
''')
p.append(B.code_example(_c,_o,filename="running_and_lag.py"))
p.append(B.concept(
 "The running total climbs within each region and **resets** at the next region (that's the "
 "`PARTITION BY`). `vs_last_month` is `NULL` for month 1 (there is no previous row to subtract) and "
 "then shows the change: East +40 then +0; West &minus;110 then +170. This single pattern answers a "
 "huge share of real \"trend\" questions."))

LAB_DB = """
CREATE TABLE sales (region TEXT, month INTEGER, amount REAL);
INSERT INTO sales VALUES
 ('East',1,100),('East',2,140),('East',3,140),
 ('West',1,200),('West',2,90),('West',3,260);
"""
p.append(B.h2("Your turn - keep the rows, add the context", kicker="Interactive lab"))
p.append(B.lab(
 "For every row, add a column `region_total` = that row's region total, **without collapsing** the "
 "rows. Return region, month, amount, region_total; order by region then month.",
 LAB_DB,
 "SELECT region, month, amount, SUM(amount) OVER (PARTITION BY region) AS region_total FROM sales ORDER BY region, month",
 starter="-- a window function keeps every row\\nSELECT region, month, amount,\\n       ",
 hint="`SUM(amount) OVER (PARTITION BY region)` gives each row its region's total while keeping all rows.",
 title="Lab 1 - aggregate without collapsing"))
p.append(B.lab(
 "The interview classic: return the **top-selling month in each region** (region, month, amount). "
 "Use a window function in a CTE, then filter. Keep ties out by using ROW_NUMBER.",
 LAB_DB,
 "WITH r AS (SELECT region, month, amount, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) AS rn FROM sales) SELECT region, month, amount FROM r WHERE rn = 1 ORDER BY region",
 starter="WITH r AS (\\n    SELECT region, month, amount,\\n           ROW_NUMBER() OVER (...) AS rn\\n    FROM sales\\n)\\nSELECT ",
 hint="Rank within each region with ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC), then keep rn = 1 in the outer query (you cannot filter a window function in WHERE directly).",
 title="Lab 2 - top-N per group",
 explain="ROW_NUMBER ranks within each region; filtering rn = 1 outside the CTE gives each region's best month."))

p.append(B.keypoints([
 "A ~window function~ = `func(...) OVER (PARTITION BY … ORDER BY …)`: it computes across related rows "
 "**without collapsing** them (unlike `GROUP BY`).",
 "`PARTITION BY` makes independent groups; `ORDER BY` inside `OVER` defines order (needed for "
 "running totals, ranking, LAG/LEAD).",
 "Ties: ~ROW_NUMBER~ = unique 1,2,3; ~RANK~ = same then **skip**; ~DENSE_RANK~ = same, **no skip**.",
 "`SUM(...) OVER (PARTITION BY g ORDER BY t)` is a ~running total~; ~LAG~/~LEAD~ read the previous/"
 "next row for period-over-period change.",
 "You **can't** filter on a window result in `WHERE` (it's computed too late) &mdash; wrap it in a "
 "CTE/subquery and filter there (the top-N-per-group pattern).",
]))

p.append(B.quiz([
 {"q":"How does a window function differ from GROUP BY?",
  "options":[
   {"t":"It computes an aggregate across related rows but keeps every original row (adds a column); "
        "GROUP BY collapses rows into one per group","correct":True,
    "why":"Correct. That's the defining difference — window functions preserve row-level detail and "
          "attach the aggregate as an extra column, so you keep both the detail and the context."},
   {"t":"It's just a faster GROUP BY that returns the same collapsed rows",
    "why":"It does not collapse rows — that's the whole point. It returns the same number of rows you "
          "started with, plus computed columns."},
   {"t":"It can only compute SUM, not ranks",
    "why":"Window functions include SUM/AVG/COUNT *and* ranking (ROW_NUMBER/RANK/DENSE_RANK) and "
          "offsets (LAG/LEAD)."},
   {"t":"It requires a GROUP BY to work",
    "why":"It uses OVER (PARTITION BY …); it does not need — and usually isn't combined with — a "
          "GROUP BY."}]},
 {"q":"Amounts are 260, 200, 140, 140, 100. Using `RANK() OVER (ORDER BY amount DESC)`, what rank "
      "does the 100 get?",
  "options":[
   {"t":"5 — RANK gives the two 140s rank 3 (tied) and then skips 4","correct":True,
    "why":"Correct. RANK assigns 1, 2, 3, 3, then skips 4 because two rows occupied rank 3, so the "
          "100 lands at 5. DENSE_RANK would give it 4 instead."},
   {"t":"4",
    "why":"That's DENSE_RANK's answer (no skipping). RANK skips after a tie, so the 100 is 5."},
   {"t":"3",
    "why":"3 is where the tied 140s sit. The 100 is below them, at rank 5 under RANK."},
   {"t":"It's random",
    "why":"Only ROW_NUMBER is arbitrary on ties. RANK is deterministic: 1,2,3,3,5 here."}]},
 {"q":"You wrote `... WHERE RANK() OVER (ORDER BY amount DESC) <= 3` and it errors. Why, and the fix?",
  "options":[
   {"t":"Window functions can't be used in WHERE (they're computed after WHERE); compute the rank in "
        "a CTE/subquery, then filter on it","correct":True,
    "why":"Correct. WHERE runs before window functions are evaluated, so the rank doesn't exist yet. "
          "Put the window function in a CTE (or subquery) and filter its result in the outer query — "
          "the standard top-N-per-group pattern."},
   {"t":"RANK needs a PARTITION BY to work",
    "why":"PARTITION BY is optional; the real problem is using a window function in WHERE at all."},
   {"t":"You must use DENSE_RANK in WHERE, not RANK",
    "why":"Neither can go in WHERE. The execution-order problem is the same for all window functions."},
   {"t":"The comparison should be = not <=",
    "why":"The operator isn't the issue; window functions simply aren't allowed in WHERE."}]},
]))

p.append(B.practice([
 {"q":"From `sales(region, month, amount)`, write a query that shows, for every row, that row's "
      "**rank within its region** by amount (highest = 1), keeping all rows.",
  "sol":"`SELECT region, month, amount, RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS "
        "rank_in_region FROM sales ORDER BY region, rank_in_region;` — PARTITION BY region ranks "
        "each region independently; every row is kept with its rank attached."},
 {"q":"Write a query for the **top 1 month per region** (the region's best-selling month). Why do "
      "you need a CTE?",
  "sol":"`WITH ranked AS (SELECT region, month, amount, ROW_NUMBER() OVER (PARTITION BY region ORDER "
        "BY amount DESC) AS rn FROM sales) SELECT region, month, amount FROM ranked WHERE rn = 1;` — "
        "you can't filter `rn = 1` in the same SELECT's WHERE (the window value isn't ready yet), so "
        "you compute it in a CTE and filter in the outer query."},
]))

p.append(B.deepdive(
 B.concept(
  "**The frame: which rows the window actually covers.** When you add `ORDER BY` inside `OVER`, the "
  "default ~frame~ is \"all rows from the start of the partition up to the current row\" (`RANGE "
  "BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`) — that's why `SUM(...) OVER (ORDER BY ...)` is a "
  "*running* total. Drop the `ORDER BY` and the frame becomes the **whole partition**, giving a "
  "constant group total on every row. You can also state frames explicitly, e.g. a 3-row moving "
  "average with `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`.") +
 B.concept(
  "**Top-N-per-group is the #1 interview pattern.** \"The 2 highest-paid employees in each "
  "department\", \"each customer's 3 most recent orders\" — all the same shape: `ROW_NUMBER()` (or "
  "`RANK`/`DENSE_RANK`) `OVER (PARTITION BY group ORDER BY key DESC)` inside a CTE, then `WHERE rn <= "
  "N` outside. Choose ROW_NUMBER for \"exactly N rows\", RANK/DENSE_RANK when ties should all be "
  "kept.") +
 B.concept(
  "**Window functions vs self-joins.** Everything here *can* be done with correlated subqueries or "
  "self-joins, but those re-scan the table per row and get slow and unreadable. Window functions do "
  "it in one pass and say the intent plainly. When you see \"running\", \"rank\", \"per-group top\", "
  "\"previous/next\", or \"share of total\", reach for a window function first."),
 title="Deep dive: window frames, the top-N-per-group pattern, and why windows beat self-joins"))

p.append(B.callout("note","Interview-ready",
 "This lesson *is* a SQL interview. Be ready to: explain window vs GROUP BY (keeps rows vs "
 "collapses); state ROW_NUMBER vs RANK vs DENSE_RANK on ties; and write **top-N-per-group** with a "
 "`ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)` in a CTE filtered by `rn <= N`. That last one is "
 "asked constantly &mdash; practice it until it's automatic.", "&#9670;"))

LESSONS={"sql-06-window":"\n".join(p)}
print("content_sql06 OK — chars:", len(LESSONS["sql-06-window"]))
