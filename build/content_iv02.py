# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "**SQL is the most-tested technical skill in data-science interviews** &mdash; more reliably than "
 "Python, more than ML. Almost every loop has a live SQL round, and it's where nervous candidates "
 "lose offers on questions they *could* do calmly. The good news: interview SQL is a small set of "
 "**recurring patterns**. Drill these and the round becomes free points."))
p.append(B.h2("The patterns that recur", kicker="Learn these cold"))
p.append(B.concept(
 "Almost every SQL interview question is one of these, or a combination:\n\n"
 "- **Aggregation + GROUP BY / HAVING** &mdash; \"revenue per category,\" \"users with &gt; 5 "
 "orders.\" (`HAVING` filters *after* grouping.)\n"
 "- **JOINs** &mdash; combining tables; know INNER vs LEFT cold, and what a missing match yields "
 "(NULLs).\n"
 "- **Window functions** &mdash; the senior signal: `ROW_NUMBER/RANK` for **top-N-per-group** and "
 "**deduplication**, `SUM() OVER` for **running totals**, `LAG/LEAD` for period-over-period.\n"
 "- **Self-joins** &mdash; comparing rows in the same table (employees to managers, consecutive "
 "events).\n"
 "- **Date logic** &mdash; truncating to month, date differences, cohort/retention windows.\n"
 "- **Subqueries / CTEs** &mdash; \"the Nth highest,\" \"above-average X,\" broken into readable "
 "steps."))
p.append(B.h2("Say the patterns out loud", kicker="Rapid-fire"))
p.append(B.interview_check([
 "Find the **second-highest** salary. (subquery or `DENSE_RANK`)",
 "Get the **top 3 products by sales in each category**. (`ROW_NUMBER`/`RANK` partitioned)",
 "Compute a **running total** of daily revenue. (`SUM() OVER (ORDER BY ...)`)",
 "**Deduplicate** rows, keeping the most recent per user. (`ROW_NUMBER` + filter)",
 "Find users who did **event A but not event B**. (`LEFT JOIN ... WHERE B IS NULL`, or `NOT "
 "EXISTS`)",
 "**Month-over-month** growth. (`LAG` over ordered months)",
 "**INNER vs LEFT JOIN** &mdash; when does each drop rows?",
 "`WHERE` vs `HAVING` &mdash; what's the difference?",
 "Why can `COUNT(col)` and `COUNT(*)` differ? (NULLs)",
 "Compute a **funnel / retention** rate across steps.",
], title="The SQL screen drill")
)
p.append(B.h2("Worked pattern — top-N per group", kicker="The window-function classic"))
p.append(B.concept(
 "\"Top 3 products by revenue **in each category**\" is the single most common window-function "
 "question. The pattern: number the rows *within* each group, then keep the low numbers:"))
p.append(B.code_example(
 "SELECT category, product, revenue\n"
 "FROM (\n"
 "  SELECT category, product, revenue,\n"
 "         ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn\n"
 "  FROM sales\n"
 ") ranked\n"
 "WHERE rn <= 3\n"
 "ORDER BY category, revenue DESC;",
 "-- PARTITION BY restarts the numbering for each category;\n"
 "-- ORDER BY revenue DESC makes rn=1 the top seller. Keep rn <= 3.",
 filename="top_n_per_group.sql"))
p.append(B.tip(
 "Know the difference between the three ranking windows: **`ROW_NUMBER`** gives a unique number "
 "(ties broken arbitrarily), **`RANK`** leaves gaps after ties (1,1,3), **`DENSE_RANK`** doesn't "
 "(1,1,2). \"Second-highest *distinct* salary\" wants **`DENSE_RANK`**; \"exactly 3 rows per group\" "
 "wants **`ROW_NUMBER`**. Picking the right one unprompted is a senior tell."))
p.append(B.h2("Your turn — the classic 'second-highest salary'", kicker="Interactive lab"))
p.append(B.lab(
 "The most famous SQL interview question: return the **second-highest salary** in the `employees` "
 "table as a single value. (Hint: the max salary that is **below** the overall max.)",
 "CREATE TABLE employees (name TEXT, salary INTEGER);\n"
 "INSERT INTO employees VALUES ('Ada',95000),('Blake',72000),('Chen',110000),"
 "('Diego',88000),('Sara',110000),('Tom',72000);",
 "SELECT MAX(salary) AS second_highest\n"
 "FROM employees\n"
 "WHERE salary < (SELECT MAX(salary) FROM employees);",
 starter="-- return the second-highest salary as one value\nSELECT ",
 hint="Take MAX(salary) among rows where salary is strictly less than the overall MAX(salary). "
      "(Note Chen and Sara tie at the top &mdash; the second-highest *distinct* salary is 95000.)",
 title="Lab — second-highest salary",
 explain="The subquery finds the top salary (110000); the outer MAX finds the largest salary below "
         "it (95000). Because two people tie at 110000, this 'below the max' approach correctly "
         "returns the second-highest *distinct* value &mdash; a subtlety `DENSE_RANK() = 2` also "
         "handles. Naming that tie-handling out loud is what impresses."))
p.append(B.keypoints([
 "Interview SQL is a **small set of patterns**: GROUP BY/HAVING, JOINs, **window functions**, "
 "self-joins, date logic, subqueries/CTEs.",
 "**Window functions are the senior signal** &mdash; `ROW_NUMBER/RANK` for top-N-per-group and "
 "dedup, `SUM() OVER` for running totals, `LAG/LEAD` for period-over-period.",
 "Know **`ROW_NUMBER` vs `RANK` vs `DENSE_RANK`** (ties) and **`WHERE` vs `HAVING`** (before vs "
 "after grouping) cold.",
 "**Top-N-per-group**: number rows with `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`, then "
 "filter `rn <= N`.",
 "**Clarify** (dedup rules, tie handling, NULLs) before writing &mdash; and build complex queries "
 "in readable **CTEs**.",
]))
p.append(B.quiz([
 {"q":"You need exactly the top 3 rows per group, with ties broken arbitrarily so you never get more "
      "than 3. Which window function?",
  "options":[
   {"t":"ROW_NUMBER() — gives each row a unique number within the partition, so `rn <= 3` yields "
        "exactly 3","correct":True,
    "why":"Correct. ROW_NUMBER assigns unique consecutive numbers even for ties, so filtering rn <= 3 "
          "returns exactly three rows per group. RANK/DENSE_RANK could return more when there are ties "
          "at the boundary."},
   {"t":"RANK() — because it handles ties",
    "why":"RANK gives tied rows the same number and can return more than 3 rows if there's a tie at "
          "3rd. Use ROW_NUMBER when you need *exactly* N."},
   {"t":"DENSE_RANK() — no gaps",
    "why":"DENSE_RANK also assigns ties the same rank, so `<= 3` can return more than 3 rows. For "
          "*exactly* 3, use ROW_NUMBER."},
   {"t":"COUNT() OVER",
    "why":"That counts within a window; it doesn't rank rows for a top-N filter. You need "
          "ROW_NUMBER."}]},
 {"q":"What's the difference between WHERE and HAVING?",
  "options":[
   {"t":"WHERE filters rows before grouping; HAVING filters groups after aggregation","correct":True,
    "why":"Correct. WHERE can't reference aggregates (they don't exist yet); HAVING filters on "
          "aggregated results (e.g. `HAVING COUNT(*) > 5`) after GROUP BY."},
   {"t":"They're interchangeable",
    "why":"They're not: WHERE runs before grouping and can't use aggregates; HAVING runs after and "
          "can. Using the wrong one errors or filters at the wrong stage."},
   {"t":"HAVING is faster than WHERE",
    "why":"It's about *stage*, not speed &mdash; WHERE before grouping, HAVING after. (Filtering early "
          "with WHERE when possible is usually more efficient.)"},
   {"t":"WHERE only works on numbers",
    "why":"WHERE works on any column type. The real distinction is before-grouping (WHERE) vs "
          "after-aggregation (HAVING)."}]},
]))
p.append(B.practice([
 {"q":"Explain how you'd deduplicate a table to keep only the most recent row per user_id, and why "
      "your approach works.",
  "sol":"Use a **window function** to number each user's rows by recency, then keep the first: "
        "`SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) "
        "AS rn FROM t) x WHERE rn = 1`. **Why it works:** `PARTITION BY user_id` restarts the "
        "numbering for each user, and `ORDER BY updated_at DESC` makes `rn = 1` the most recent row "
        "for that user; filtering `rn = 1` keeps exactly one row each. I'd **clarify tie-handling** "
        "first (what if two rows share the latest timestamp? &mdash; add a tiebreaker like a primary "
        "key to the ORDER BY), and I'd use `ROW_NUMBER` (not RANK) so ties can't return two rows. "
        "This pattern &mdash; partition, order, filter rn=1 &mdash; is the canonical dedup, and "
        "naming the tie edge case is what signals real experience."},
]))
LESSONS={"iv-02-sql":"\n".join(p)}
print("content_iv02 OK — chars:", len(LESSONS["iv-02-sql"]))
