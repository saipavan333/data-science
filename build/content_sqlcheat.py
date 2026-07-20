# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.concept(
 "Keep this open while you work. Everything in the SQL track, on one scannable page &mdash; the "
 "clause, what it does, and the shape of the query. Press **Print** for a paper copy to pin above "
 "your desk. If you can read this and picture the query, you know SQL."))
p.append(B.cheatsheet(
 "SQL for Data Analysis — one-page reference",
 "Clauses always run in this order: `FROM` &rarr; `WHERE` &rarr; `GROUP BY` &rarr; `HAVING` &rarr; "
 "`SELECT` &rarr; `ORDER BY` &rarr; `LIMIT`. That order explains most \"why doesn't this work?\" moments.",
 [
  ("The shape of a query", [
    ("SELECT cols", "which **columns** to return (`*` = all)"),
    ("FROM table", "which table to read"),
    ("WHERE cond", "keep **rows** matching a condition"),
    ("GROUP BY col", "one output **row per group**"),
    ("HAVING cond", "keep **groups** by an aggregate"),
    ("ORDER BY col DESC", "sort (`ASC` low&rarr;high, `DESC` high&rarr;low)"),
    ("LIMIT n", "return only the first n rows"),
  ]),
  ("Filtering rows (WHERE)", [
    ("a AND b, a OR b", "combine (`AND` binds tighter &mdash; use parens)"),
    ("col IN (1,2,3)", "value is in a set"),
    ("col BETWEEN x AND y", "inclusive range (both ends)"),
    ("name LIKE 'A%'", "text pattern (`%`=any, `_`=one char)"),
    ("col IS NULL", "test for missing (never `= NULL`)"),
    ("DISTINCT col", "unique values only"),
  ]),
  ("Aggregating (GROUP BY)", [
    ("COUNT(*)", "count **rows**"),
    ("COUNT(col)", "count **non-NULL** values"),
    ("SUM / AVG / MIN / MAX", "total / mean / smallest / largest (skip NULLs)"),
    ("GROUP BY category", "collapse to one row per category"),
    ("HAVING SUM(x) > 100", "filter groups by their aggregate"),
    ("COUNT(DISTINCT col)", "count distinct values"),
  ]),
  ("Joining tables", [
    ("a JOIN b ON a.id=b.aid", "**INNER**: only matching rows both sides"),
    ("a LEFT JOIN b ON …", "keep **all left** rows; NULLs where no match"),
    ("… WHERE b.id IS NULL", "anti-join: left rows with **no** match"),
    ("COUNT(b.id)", "count matches (0 for unmatched, unlike `*`)"),
    ("fan-out", "one-to-many join **multiplies** rows &mdash; check counts"),
  ]),
  ("Subqueries & CTEs", [
    ("WHERE x > (SELECT AVG(x) …)", "scalar subquery: compare to one value"),
    ("WHERE id IN (SELECT …)", "membership against a list"),
    ("WITH t AS (SELECT …) SELECT … FROM t", "**CTE**: name a step, read top-down"),
    ("NOT EXISTS (SELECT …)", "prefer over `NOT IN` when NULLs possible"),
  ]),
  ("Window functions", [
    ("SUM(x) OVER (PARTITION BY g)", "group total, **keeping** every row"),
    ("ROW_NUMBER() OVER (ORDER BY x)", "unique 1,2,3 (ties arbitrary)"),
    ("RANK() / DENSE_RANK()", "ties share rank (skip / no-skip)"),
    ("SUM(x) OVER (… ORDER BY t)", "running total"),
    ("LAG(x) / LEAD(x) OVER (…)", "previous / next row's value"),
    ("top-N per group", "rank in a **CTE**, then `WHERE rn <= N`"),
  ]),
  ("Reshape & clean", [
    ("CASE WHEN … THEN … ELSE … END", "if/else; put inside `SUM()` for a pivot"),
    ("COALESCE(a, b)", "first non-NULL (supply a default)"),
    ("NULLIF(x, 0)", "NULL when equal (avoids /0)"),
    ("CAST(x AS REAL)", "convert type"),
    ("strftime('%Y-%m', d)", "date part / truncate (SQLite)"),
    ("TRIM / LOWER / REPLACE / ||", "tidy & concatenate text"),
  ]),
  ("Interview reflexes", [
    ("WHERE vs HAVING", "rows before grouping vs groups after"),
    ("alias not usable in WHERE", "SELECT runs after WHERE &mdash; repeat it or use a CTE"),
    ("col != 'x' drops NULLs", "add `OR col IS NULL`"),
    ("narrate then type", "say the plan; ask if ties count"),
  ]),
 ]))
LESSONS={"sql-09-cheatsheet":"\n".join(p)}
print("content_sqlcheat OK — chars:", len(LESSONS["sql-09-cheatsheet"]))
