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
CREATE TABLE employees (id INTEGER, name TEXT, dept TEXT, salary REAL);
INSERT INTO employees VALUES
 (1,'Ada',  'Engineering',150),
 (2,'Blake','Engineering',120),
 (3,'Chen', 'Engineering',150),
 (4,'Diego','Sales',       90),
 (5,'Priya','Sales',      130),
 (6,'Sara', 'Sales',      110),
 (7,'Tom',  'Marketing',   95);
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
 "The SQL screen is the most predictable round in the whole data-science interview &mdash; the same "
 "handful of **problem patterns** come up again and again, dressed in different stories. If you can "
 "recognise the pattern and write it calmly while talking through your reasoning, you pass. This "
 "lesson is the pattern bank: each one stated plainly, solved with a runnable query, and explained "
 "the way you'd say it out loud to an interviewer."))

p.append(B.h2("Pattern 1 — the Nth-highest value", kicker="Interview pattern"))
p.append(B.concept(
 "*\"Find the second-highest salary.\"* The trap is ties: if two people earn the top salary, \"second "
 "highest\" almost always means the second **distinct** value. That is exactly ~DENSE_RANK~ (same "
 "rank for ties, no gaps). Rank in a CTE, then filter outside &mdash; remember you can't filter a "
 "window function in `WHERE`:"))
_c,_o=_run(SETUP+'''
run("""
    WITH ranked AS (
        SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
        FROM employees
    )
    SELECT DISTINCT salary AS second_highest
    FROM ranked
    WHERE rnk = 2
""")
''')
p.append(B.code_example(_c,_o,filename="nth_highest.py"))
p.append(B.concept(
 "Two people earn 150, so `DENSE_RANK` gives both rank 1 and the next distinct salary (130) rank 2 "
 "&mdash; the answer. Say the tie-handling out loud; that's the part being tested. (The older "
 "textbook answer uses `LIMIT 1 OFFSET 1` on a `SELECT DISTINCT salary … ORDER BY salary DESC`, which "
 "also works and is worth mentioning.)"))

p.append(B.h2("Pattern 2 — top N per group", kicker="Interview pattern · the most-asked"))
p.append(B.concept(
 "*\"The two highest-paid people in each department.\"* This is the single most common SQL interview "
 "question. Shape: rank **within each group** using `PARTITION BY`, in a CTE, then filter the rank "
 "outside. Use `DENSE_RANK` if tied people should all be kept, `ROW_NUMBER` if you need exactly N "
 "rows:"))
_c,_o=_run(SETUP+'''
run("""
    WITH ranked AS (
        SELECT name, dept, salary,
               DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
        FROM employees
    )
    SELECT dept, name, salary, rnk
    FROM ranked
    WHERE rnk <= 2
    ORDER BY dept, rnk, name
""")
''')
p.append(B.code_example(_c,_o,filename="top_n_per_group.py"))
p.append(B.concept(
 "Engineering keeps Ada **and** Chen (both 150, rank 1) plus Blake at rank 2 &mdash; because "
 "`DENSE_RANK` honours the tie. Had the question said \"exactly two rows per department\", "
 "`ROW_NUMBER` would drop one of the tied pair arbitrarily. Ask the interviewer which they want; "
 "noticing the ambiguity scores points."))

p.append(B.h2("Pattern 3 — group, then filter the groups", kicker="Interview pattern"))
p.append(B.concept(
 "*\"Which departments have an average salary above 100, and how many people are in them?\"* A "
 "condition on a **group's aggregate** belongs in `HAVING`, never `WHERE`. This tests whether you "
 "understand execution order:"))
_c,_o=_run(SETUP+'''
run("""
    SELECT dept,
           COUNT(*)             AS headcount,
           ROUND(AVG(salary),1) AS avg_salary
    FROM employees
    GROUP BY dept
    HAVING AVG(salary) > 100
    ORDER BY avg_salary DESC
""")
''')
p.append(B.code_example(_c,_o,filename="having.py"))

p.append(B.h2("Pattern 4 — aggregate without losing the rows", kicker="Interview pattern"))
p.append(B.concept(
 "*\"Show each employee alongside their department's total payroll and their share of it.\"* If you "
 "reach for `GROUP BY` you lose the individual rows; the answer is a **window function**, which keeps "
 "every row and attaches the group aggregate:"))
_c,_o=_run(SETUP+'''
run("""
    SELECT name, dept, salary,
           SUM(salary) OVER (PARTITION BY dept)                                AS dept_payroll,
           ROUND(100.0 * salary / SUM(salary) OVER (PARTITION BY dept), 1)     AS pct_of_dept
    FROM employees
    ORDER BY dept, salary DESC
""")
''')
p.append(B.code_example(_c,_o,filename="window_share.py"))

p.append(B.h2("Reading and debugging an unfamiliar query", kicker="Method"))
p.append(B.concept(
 "Interviewers often hand you a query and ask what it does, or why it's wrong. Read it in "
 "**execution order**, not top to bottom:\n\n"
 "1. `FROM` / `JOIN` &mdash; which tables, and on what key? (Is it one-to-many? Expect fan-out.)\n"
 "2. `WHERE` &mdash; which rows survive? (Any comparison against a nullable column silently drops "
 "NULLs.)\n"
 "3. `GROUP BY` &mdash; what is one output row now?\n"
 "4. `HAVING` &mdash; which groups survive?\n"
 "5. `SELECT` &mdash; which columns/aggregates are produced (and aliases created)?\n"
 "6. `ORDER BY` / `LIMIT` &mdash; final sort and cut.\n\n"
 "Then check the four bugs that account for most wrong answers in practice:"))
p.append(B.table(
 ["Symptom", "Likely cause", "Fix"],
 [["Rows mysteriously missing", "A `WHERE` comparison on a nullable column dropped the NULLs",
   "Use `IS NULL` / `IS NOT NULL`, or `COALESCE`"],
  ["Totals far too large", "Fan-out from a one-to-many join duplicated rows",
   "Aggregate before joining, or check row counts"],
  ["\"No such column\" on an alias", "Alias made in `SELECT` used in `WHERE`/`GROUP BY` (they run earlier)",
   "Repeat the expression, or wrap in a CTE"],
  ["Counts include empty groups as 1", "`COUNT(*)` after a `LEFT JOIN` counts the NULL-filled row",
   "Use `COUNT(child.id)` instead"]],
 caption="The four bugs behind most broken analytics queries"))

p.append(B.keypoints([
 "**Nth-highest** &rarr; `DENSE_RANK` in a CTE, filter `rnk = N` outside (ties give the same rank, no "
 "gaps).",
 "**Top-N per group** &rarr; `RANK`/`DENSE_RANK`/`ROW_NUMBER` `OVER (PARTITION BY g ORDER BY x DESC)` "
 "in a CTE, then `WHERE rnk <= N`. Clarify how ties should be treated.",
 "A condition on a **group aggregate** goes in `HAVING`; a condition on a **row** goes in `WHERE`.",
 "Need the aggregate **and** the detail rows? That's a window function, not `GROUP BY`.",
 "Debug by reading in execution order (`FROM`&rarr;`WHERE`&rarr;`GROUP BY`&rarr;`HAVING`&rarr;"
 "`SELECT`&rarr;`ORDER BY`) and checking for NULL drops, fan-out, and alias-scope errors.",
]))

p.append(B.quiz([
 {"q":"Why is `DENSE_RANK` usually the right choice for \"the Nth-highest salary\"?",
  "options":[
   {"t":"It gives tied salaries the same rank without skipping numbers, so rank N is the Nth distinct "
        "salary","correct":True,
    "why":"Correct. With two people at the top, DENSE_RANK makes them both 1 and the next distinct "
          "salary 2 — matching what \"second highest\" normally means. RANK would skip to 3, and "
          "ROW_NUMBER would call one of the tied pair 'second'."},
   {"t":"It's the only ranking function allowed in a CTE",
    "why":"All ranking functions work in a CTE. The choice is purely about tie behaviour."},
   {"t":"It sorts faster than RANK",
    "why":"Performance isn't the reason; correctness on ties is."},
   {"t":"Because ROW_NUMBER can't be used with ORDER BY",
    "why":"ROW_NUMBER requires ORDER BY and works fine — it just breaks ties arbitrarily, which "
          "misreports the Nth-highest value."}]},
 {"q":"An interviewer asks for each employee shown next to their department's average salary — every "
      "employee row must remain. What do you use?",
  "options":[
   {"t":"A window function: AVG(salary) OVER (PARTITION BY dept)","correct":True,
    "why":"Correct. GROUP BY would collapse the employees into one row per department; the window "
          "function keeps all rows and attaches the department average to each."},
   {"t":"GROUP BY dept",
    "why":"That returns one row per department and loses the individual employees, which the question "
          "explicitly forbids."},
   {"t":"A HAVING clause",
    "why":"HAVING filters groups; it doesn't attach a group aggregate to detail rows."},
   {"t":"ORDER BY dept",
    "why":"Sorting doesn't compute the department average."}]},
 {"q":"A LEFT JOIN from `departments` to `employees` plus `COUNT(*)` reports 1 for an empty "
      "department. The fix?",
  "options":[
   {"t":"Use COUNT(e.id) — it skips the NULL-filled row, correctly giving 0","correct":True,
    "why":"Correct. After a LEFT JOIN an empty department still yields one row with NULL employee "
          "columns; COUNT(*) counts that row, while COUNT(e.id) ignores the NULL and returns 0."},
   {"t":"Switch to an INNER JOIN",
    "why":"That would remove empty departments entirely — but the question wants them shown with 0."},
   {"t":"Add HAVING COUNT(*) > 0",
    "why":"That hides empty departments rather than reporting 0 for them, and the count is still wrong."},
   {"t":"Use SUM(*) instead",
    "why":"`SUM(*)` isn't valid SQL. COUNT(e.id) is the standard fix."}]},
]))

p.append(B.practice([
 {"q":"Write a query returning the **highest-paid employee in each department** (name, dept, salary), "
      "keeping ties.",
  "sol":"`WITH r AS (SELECT name, dept, salary, DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary "
        "DESC) AS rnk FROM employees) SELECT dept, name, salary FROM r WHERE rnk = 1 ORDER BY dept;` "
        "— DENSE_RANK partitioned by dept ranks within each department; `rnk = 1` keeps the top "
        "earner(s), including everyone tied at the top."},
 {"q":"Write a query for departments with **more than 2 employees**, showing the headcount, and "
      "explain why the condition can't live in `WHERE`.",
  "sol":"`SELECT dept, COUNT(*) AS headcount FROM employees GROUP BY dept HAVING COUNT(*) > 2;` — "
        "`COUNT(*)` is a **group** aggregate that doesn't exist until after `GROUP BY` runs, and "
        "`WHERE` executes *before* grouping. Filtering groups is exactly what `HAVING` is for."},
]))

p.append(B.interview_check([
 "Explain the difference between `WHERE` and `HAVING` &mdash; and why an aggregate can't go in `WHERE`.",
 "Write \"top 2 per group\" from memory, and say how you'd handle ties.",
 "What does `WHERE col != 'x'` do to rows where `col` is NULL, and how do you include them?",
 "Difference between `INNER` and `LEFT JOIN`, and how you'd find rows with **no** match.",
 "When would you use a window function instead of `GROUP BY`?",
 "Walk through SQL's execution order and use it to explain why a `SELECT` alias fails in `WHERE`.",
], title="Say these out loud before your interview"))

p.append(B.callout("note","Interview-ready",
 "Two habits separate strong candidates: **narrate before you type** (\"I'll rank within each "
 "department, then filter the rank in an outer query\") and **ask one clarifying question** (\"should "
 "ties both be returned?\"). Interviewers are grading your reasoning far more than your syntax "
 "&mdash; and a query you can explain beats a clever one you can't.", "&#9670;"))

LESSONS={"sql-08-interview":"\n".join(p)}
print("content_sql08 OK — chars:", len(LESSONS["sql-08-interview"]))
