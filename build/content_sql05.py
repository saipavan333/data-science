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
CREATE TABLE orders (id INTEGER, customer TEXT, category TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'Ada',  'Electronics',240),
 (2,'Blake','Apparel',      45),
 (3,'Chen', 'Electronics',220),
 (4,'Ada',  'Home',        130),
 (5,'Priya','Electronics',510),
 (6,'Blake','Home',        160),
 (7,'Chen', 'Apparel',      90);
""")
def run(sql):
    cur=db.execute(sql); cols=[c[0] for c in cur.description]; rows=cur.fetchall()
    cell=lambda v:"NULL" if v is None else str(v)
    w=[max(len(cell(v)) for v in [c,*(r[i] for r in rows)]) for i,c in enumerate(cols)]
    show=lambda vals:"  ".join(cell(v).ljust(w[i]) for i,v in enumerate(vals))
    print(show(cols)); print(show(["-"*n for n in w]))
    for r in rows: print(show(r))
'''

p.append(B.why(
 "Some questions can't be answered in one flat pass: \"which orders are above **our average** order "
 "value?\" needs you to compute the average *first*, then compare each row to it. A ~subquery~ &mdash; "
 "a query nested inside another &mdash; lets one query use the result of another. And when a query "
 "grows into several such steps, a ~CTE~ (Common Table Expression) lets you write those steps "
 "**top-to-bottom, with names**, like paragraphs instead of nested brackets. Together they are how "
 "you build and *read* real analytical queries without losing your mind."))

p.append(B.h2("Subqueries: a query inside a query", kicker="Concept"))
p.append(B.concept(
 "A subquery is just a `SELECT` wrapped in parentheses, used as a value inside another query. Two "
 "everyday shapes:\n\n"
 "- A ~scalar subquery~ returns a **single value**, so you can compare against it. `WHERE amount > "
 "(SELECT AVG(amount) FROM orders)` compares every row to the one overall average.\n"
 "- A ~subquery with IN~ returns a **column of values** for a membership test. `WHERE customer IN "
 "(SELECT customer FROM orders WHERE category='Electronics')` keeps rows whose customer appears in "
 "that list.\n\n"
 "Both run the inner query first, then use its answer in the outer query:"))
_c,_o=_run(SETUP+'''
print(">>> orders above the overall average amount")
run("""
    SELECT customer, category, amount
    FROM orders
    WHERE amount > (SELECT AVG(amount) FROM orders)
    ORDER BY amount DESC
""")
print()
print(">>> every order by customers who have EVER bought Electronics")
run("""
    SELECT customer, category, amount
    FROM orders
    WHERE customer IN (SELECT customer FROM orders WHERE category = 'Electronics')
    ORDER BY customer
""")
''')
p.append(B.code_example(_c,_o,filename="subqueries.py"))
p.append(B.concept(
 "The first query needed the average before it could filter &mdash; impossible in one flat `WHERE` "
 "without the subquery. The second turned \"customers who bought Electronics\" into a list, then "
 "pulled **all** of their orders (including Ada's Home order and Chen's Apparel order), because they "
 "each appear in that Electronics list."))

p.append(B.h2("Subquery in FROM, and the readable upgrade: CTEs", kicker="Concept · the pro move"))
p.append(B.concept(
 "A subquery can also stand in for a **table** in the `FROM` clause (a ~derived table~) &mdash; you "
 "compute a summary, then query the summary. It works, but nested `FROM (SELECT ...)` gets hard to "
 "read. A ~CTE~ fixes that: `WITH name AS (SELECT ...)` defines a named, temporary result *before* "
 "the main query, so you read the steps in order. Here is the **same** question &mdash; \"customers "
 "whose total spend exceeds 300\" &mdash; written both ways:"))
_c,_o=_run(SETUP+'''
print(">>> derived table in FROM (works, but reads inside-out)")
run("""
    SELECT customer, total
    FROM (SELECT customer, SUM(amount) AS total FROM orders GROUP BY customer) AS by_cust
    WHERE total > 300
    ORDER BY total DESC
""")
print()
print(">>> same thing as a CTE (reads top-to-bottom)")
run("""
    WITH by_cust AS (
        SELECT customer, SUM(amount) AS total
        FROM orders
        GROUP BY customer
    )
    SELECT customer, total
    FROM by_cust
    WHERE total > 300
    ORDER BY total DESC
""")
''')
p.append(B.code_example(_c,_o,filename="cte.py"))
p.append(B.tip(
 "Reach for a ~CTE~ the moment a query needs two or more steps. You can chain several &mdash; `WITH "
 "a AS (...), b AS (SELECT ... FROM a ...)` &mdash; each building on the last, and even reference a "
 "CTE more than once. It's the difference between a query a teammate can read in ten seconds and one "
 "they have to reverse-engineer.", "&#10022;"))

p.append(B.keypoints([
 "A ~subquery~ is a `SELECT` nested inside another query, run first and used as a value.",
 "A ~scalar subquery~ returns one value (use with `>`, `=`, …); a `WHERE col IN (SELECT …)` subquery "
 "returns a column for a membership test.",
 "A subquery in `FROM` is a ~derived table~ (must be aliased) &mdash; query a computed summary.",
 "A ~CTE~ (`WITH name AS (…)`) is the readable way to write multi-step queries top-to-bottom; chain "
 "several for complex logic.",
 "A ~correlated subquery~ references the outer row and re-runs per row &mdash; powerful but can be "
 "slow; a join or window function is often faster.",
]))

p.append(B.quiz([
 {"q":"Why must `WHERE amount > (SELECT AVG(amount) FROM orders)` use a subquery instead of `WHERE "
      "amount > AVG(amount)`?",
  "options":[
   {"t":"AVG(amount) is an aggregate over all rows; WHERE runs per-row and can't compute it there, so "
        "you isolate it in a subquery that runs first","correct":True,
    "why":"Correct. Aggregates collapse many rows; WHERE filters individual rows before aggregation "
          "happens. The subquery computes the single average first, then each row is compared to it."},
   {"t":"Both are identical; the subquery is just longer",
    "why":"`WHERE amount > AVG(amount)` is actually an error — you can't use a bare aggregate in "
          "WHERE. The subquery is what makes it valid."},
   {"t":"Subqueries run faster than aggregates",
    "why":"Speed isn't the reason; correctness is. The bare-aggregate form isn't allowed in WHERE at "
          "all."},
   {"t":"Because AVG needs a GROUP BY",
    "why":"AVG over the whole table needs no GROUP BY. The issue is that WHERE can't host an aggregate; "
          "the subquery solves it."}]},
 {"q":"What's the main reason to rewrite a nested `FROM (SELECT …)` as a `WITH … AS (…)` CTE?",
  "options":[
   {"t":"Readability — CTEs let you write and name the steps top-to-bottom instead of inside-out","correct":True,
    "why":"Correct. CTEs don't usually change the result; they make multi-step queries readable, "
          "nameable, reusable, and far easier to debug."},
   {"t":"CTEs always run faster",
    "why":"Performance is engine-dependent and often similar; the reliable win is clarity, not speed."},
   {"t":"Derived tables can't be aggregated",
    "why":"They can. The difference is style/readability, not capability."},
   {"t":"CTEs remove the need for GROUP BY",
    "why":"A CTE can contain a GROUP BY; it doesn't replace it. It just organizes the query."}]},
 {"q":"`WHERE customer IN (SELECT customer FROM orders WHERE category='Electronics')` returns…",
  "options":[
   {"t":"All orders placed by any customer who has at least one Electronics order","correct":True,
    "why":"Correct. The subquery builds the list of Electronics-buying customers; the outer query then "
          "returns every order by those customers, not just their Electronics orders."},
   {"t":"Only the Electronics orders",
    "why":"That would be a plain `WHERE category='Electronics'`. The IN-subquery widens it to all "
          "orders by those customers."},
   {"t":"Customers, not orders",
    "why":"The outer SELECT returns order rows; the subquery only supplies the customer list used for "
          "filtering."},
   {"t":"An error, because customer appears in both queries",
    "why":"Reusing a column name across the inner and outer query is fine and common; no error."}]},
]))

p.append(B.practice([
 {"q":"From `orders(customer, category, amount)`, write a query (using a subquery) for the orders "
      "whose amount is **greater than the average amount within their own category** — actually, "
      "simplify: greater than the overall maximum Apparel amount.",
  "sol":"`SELECT customer, category, amount FROM orders WHERE amount > (SELECT MAX(amount) FROM orders "
        "WHERE category='Apparel') ORDER BY amount DESC;` — the scalar subquery finds the biggest "
        "Apparel order (160), and the outer query keeps every order above it."},
 {"q":"Rewrite this as a CTE: `SELECT category, avg_amt FROM (SELECT category, AVG(amount) AS avg_amt "
      "FROM orders GROUP BY category) t WHERE avg_amt > 150;`",
  "sol":"`WITH cat_avg AS (SELECT category, AVG(amount) AS avg_amt FROM orders GROUP BY category) "
        "SELECT category, avg_amt FROM cat_avg WHERE avg_amt > 150;` — same logic, but the averaging "
        "step is named `cat_avg` and read first, top-to-bottom."},
]))

p.append(B.deepdive(
 B.concept(
  "**Correlated vs non-correlated subqueries.** The subqueries above are ~non-correlated~: the inner "
  "query is independent and runs **once**. A ~correlated subquery~ references a column from the outer "
  "row, so it conceptually re-runs **for every outer row** — e.g. `WHERE amount > (SELECT "
  "AVG(amount) FROM orders o2 WHERE o2.category = o.category)` compares each order to *its own "
  "category's* average. Powerful, but that per-row re-execution can be slow on big tables; a window "
  "function (`AVG(amount) OVER (PARTITION BY category)`) usually does the same job faster.") +
 B.concept(
  "**IN, NOT IN, and the NULL landmine.** `NOT IN (SELECT …)` behaves surprisingly if the subquery "
  "can return a `NULL`: because `x != NULL` is *unknown*, a single NULL in the list makes `NOT IN` "
  "return **no rows at all**. Prefer `NOT EXISTS` (or add `WHERE col IS NOT NULL` to the subquery) "
  "when you mean \"not present\". `EXISTS`/`NOT EXISTS` also read as true/false and often optimize "
  "better than `IN` for large sets.") +
 B.concept(
  "**CTEs scale to real pipelines.** Analysts routinely stack CTEs: `WITH cleaned AS (…), daily AS "
  "(SELECT … FROM cleaned …), ranked AS (SELECT … FROM daily …) SELECT * FROM ranked WHERE …`. Each "
  "step is testable on its own (just select from it), which is why CTEs are the backbone of readable "
  "analytics SQL and dbt-style models. A recursive form, `WITH RECURSIVE`, can even walk hierarchies "
  "like org charts — a topic for later."),
 title="Deep dive: correlated subqueries, the NOT IN / NULL trap, and stacking CTEs"))

p.append(B.callout("note","Interview-ready",
 "Expect \"when would you use a subquery vs a CTE vs a join?\" — subqueries and CTEs both let one "
 "query build on another's result; CTEs win for **readability** and multi-step logic; a join is "
 "usually better when you actually need columns from another table. Bonus points for naming the "
 "`NOT IN` + NULL trap and preferring `NOT EXISTS`.", "&#9670;"))

LESSONS={"sql-05-subqueries":"\n".join(p)}
print("content_sql05 OK — chars:", len(LESSONS["sql-05-subqueries"]))
