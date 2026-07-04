# -*- coding: utf-8 -*-
import builder as B
p=[]

p.append(B.why(
 "Track 2 gave you the daily tools; this lesson is your **self-test and interview prep** for "
 "them. Data-science interviews almost always include hands-on data manipulation &mdash; in "
 "**Pandas**, **SQL**, or both &mdash; because they're what the job actually is. Cover each "
 "question, answer it, then reveal the model answer. The SQL&harr;Pandas table below is worth "
 "memorizing: the same handful of operations, two dialects."))

p.append(B.callout("tip","What the data-manipulation rounds test",
 "Interviewers want to see that you can **get data into shape fast and correctly**: filter, "
 "aggregate, join, and reshape, while avoiding the classic traps (wrong dtypes, one-to-many "
 "explosions, chained indexing). Many teams test **SQL** even for Python-heavy roles, so fluency "
 "translating between SQL and Pandas is a real edge.", "&#10022;"))

p.append(B.h2("SQL &harr; Pandas: the same verbs, two dialects", kicker="Reference · memorize this"))
p.append(B.table(
 ["Task", "SQL", "Pandas"],
 [["Filter rows", "WHERE amount > 100", 'df[df["amount"] > 100]'],
  ["Pick columns", "SELECT category, amount", 'df[["category", "amount"]]'],
  ["Sort", "ORDER BY amount DESC", 'df.sort_values("amount", ascending=False)'],
  ["Distinct", "SELECT DISTINCT region", 'df["region"].drop_duplicates()'],
  ["Aggregate by group", "GROUP BY region", 'df.groupby("region").agg(...)'],
  ["Filter groups", "HAVING count(*) > 100", '.groupby(...).filter(lambda g: len(g) > 100)'],
  ["Join", "JOIN c ON o.cid = c.cid", 'orders.merge(c, on="cid", how="left")'],
  ["Limit", "LIMIT 10", 'df.head(10)'],
  ["New column", "amount * 0.9 AS net", 'df["net"] = df["amount"] * 0.9']],
 caption="Most analysis is these nine moves. If you can map a question to a SQL clause, you can "
         "write the Pandas &mdash; and vice versa."))

p.append(B.h2("Pandas & data-wrangling questions", kicker="Bank 1"))
p.append(B.practice([
 {"q":"What's the difference between `.loc` and `.iloc`, including how their slices behave?",
  "sol":"`.loc` selects by **label** (the index/column names) and its slices are **inclusive** of "
        "the end label: `df.loc[0:2]` returns labels 0, 1, and 2. `.iloc` selects by integer "
        "**position** and its slices are **exclusive** like normal Python: `df.iloc[0:2]` returns "
        "positions 0 and 1. Rule of thumb: name &rarr; loc, position &rarr; iloc."},
 {"q":"How would you find the top 3 products by revenue within each category? (Describe the "
      "Pandas approach.)",
  "sol":"Aggregate revenue per (category, product), then take the top 3 per category: "
        "`rev = df.groupby([\"category\",\"product\"])[\"revenue\"].sum().reset_index()`, then "
        "`rev.sort_values(\"revenue\", ascending=False).groupby(\"category\").head(3)`. The "
        "`groupby(...).head(3)` after sorting gives the top 3 rows per group. (In SQL this is a "
        "window function: `ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) <= 3`.)"},
 {"q":"Your Pandas operation on a few million rows is painfully slow because it uses "
      "`df.apply(..., axis=1)` with a Python function. How do you speed it up?",
  "sol":"`apply(axis=1)` runs a Python function row-by-row &mdash; it loses vectorization. Rewrite "
        "the logic as **vectorized** array/Series operations (arithmetic, `np.where`, `.str`/`.dt` "
        "accessors, boolean masks) so it runs in compiled code. If you truly need conditional "
        "logic, `np.select` or `np.where` usually replaces a row-wise apply and runs 10&ndash;"
        "100&times; faster. Vectorize first; reach for apply only as a last resort."},
 {"q":"After reading a CSV, a numeric column behaves like text (e.g., sums concatenate). How do "
      "you diagnose and fix it?",
  "sol":"Diagnose with `df.dtypes` or `df.info()` &mdash; you'll see `object` instead of a numeric "
        "type. Fix with `df[\"col\"] = pd.to_numeric(df[\"col\"], errors=\"coerce\")`, which "
        "converts to numbers and turns any unparseable entries into NaN to handle next. The usual "
        "culprits are stray characters like `$`, commas, or spaces; strip them first if needed. "
        "Always check dtypes immediately after loading."}]))

p.append(B.h2("SQL questions", kicker="Bank 2"))
p.append(B.practice([
 {"q":"Write SQL for total revenue per region, only for regions with more than 1,000 orders, sorted high to low.", "html": True,
  "sol": B.code_example("SELECT region, SUM(revenue) AS total\nFROM orders\nGROUP BY region\nHAVING COUNT(*) > 1000\nORDER BY total DESC;", filename="query.sql", runnable=False) + B.fmt("Key points: **GROUP BY** region defines the groups, **SUM(revenue)** aggregates, **HAVING** filters *groups* (use HAVING, not WHERE, for conditions on aggregates), and **ORDER BY total DESC** sorts high to low. In Pandas: group, `agg`, then `query`/filter and `sort_values`.")},
 {"q":"What's the difference between WHERE and HAVING?",
  "sol":"**WHERE** filters individual **rows before** grouping; **HAVING** filters **groups "
        "after** aggregation. So `WHERE amount > 0` removes bad rows first, while `HAVING "
        "SUM(amount) > 1000` keeps only groups whose total exceeds 1,000. You can't put an "
        "aggregate like `SUM(...)` in a WHERE clause &mdash; that's exactly what HAVING is for."},
 {"q":"Explain the difference between an INNER JOIN and a LEFT JOIN with a quick example.",
  "sol":"An **INNER JOIN** returns only rows whose key matches in **both** tables; a **LEFT JOIN** "
        "returns **all** rows from the left table plus matches from the right (NULLs where there's "
        "no match). Example: joining `orders` to `customers` &mdash; INNER drops orders whose "
        "customer is missing; LEFT keeps every order, leaving customer fields NULL when absent. "
        "Use LEFT when the left table is your source of truth you must not lose."},
 {"q":"What does a window function like ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) do that "
      "GROUP BY can't?",
  "sol":"A **window function** computes across a set of rows **without collapsing them** &mdash; "
        "each row keeps its identity but gains a value computed over its 'window' (partition). "
        "`ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC)` numbers products within "
        "each category by revenue, so you can keep the top N per group &mdash; something plain "
        "GROUP BY (which returns one row per group) can't do. Windows also power running totals "
        "and rank comparisons."}]))

p.append(B.keypoints([
 "Know the **SQL&harr;Pandas** mapping cold: WHERE/`mask`, GROUP BY/`groupby`, JOIN/`merge`, "
 "ORDER BY/`sort_values`.",
 "**WHERE filters rows, HAVING filters groups**; aggregates go in HAVING, not WHERE.",
 "**INNER** keeps matches; **LEFT** keeps all left rows &mdash; pick by which table you can't "
 "afford to lose.",
 "Top-N-per-group needs a **window function** in SQL (`ROW_NUMBER() OVER (PARTITION BY ...)`) or "
 "`sort_values` + `groupby().head(n)` in Pandas.",
 "**Vectorize** instead of `apply(axis=1)`; check **dtypes** after loading and **row counts** "
 "after merges.",
]))

p.append(B.quiz([
 {"q":"An interviewer asks for 'average order value per customer, including customers who placed "
      "no orders.' Which join keeps the no-order customers?",
  "options":[
   {"t":"A LEFT JOIN from customers to orders (all customers, matched orders where they exist)","correct":True,
    "why":"Correct. Starting from customers and LEFT JOINing orders keeps every customer; those "
          "with no orders get NULLs (and an average you'd treat as 0 or NULL). INNER would drop "
          "them."},
   {"t":"An INNER JOIN, since it's faster",
    "why":"INNER keeps only customers who have at least one order, dropping exactly the no-order "
          "customers the question asks to include."},
   {"t":"No join is needed",
    "why":"The data spans two tables (customers and orders), so you must join them; the question "
          "is which type, and LEFT preserves all customers."},
   {"t":"A CROSS JOIN",
    "why":"A cross join pairs every customer with every order regardless of key &mdash; nonsense "
          "here. You want a LEFT JOIN on the customer key."}]},
 {"q":"Which is the strongest sign you're writing idiomatic, performant Pandas?",
  "options":[
   {"t":"You filter with boolean masks and compute with vectorized operations instead of "
        "row-by-row loops/apply","correct":True,
    "why":"Correct. Vectorized masks and column operations run in compiled code and read clearly "
          "&mdash; the hallmark of good Pandas. Row-wise loops/apply are the slow fallback."},
   {"t":"You use a for-loop over df.iterrows() for every transformation",
    "why":"`iterrows` is one of the slowest patterns in Pandas; idiomatic code vectorizes instead "
          "of looping over rows."},
   {"t":"You convert everything to Python lists first",
    "why":"That discards Pandas/NumPy's speed and labeled-data advantages. Stay in vectorized "
          "Series/DataFrame operations."},
   {"t":"You avoid groupby and merge entirely",
    "why":"groupby and merge are core, optimized tools &mdash; avoiding them usually means "
          "reinventing them slower and with more bugs."}]},
]))

p.append(B.callout("note","You've finished Track 2",
 "You can now load, clean, reshape, and aggregate real data in Python &mdash; and translate "
 "fluently to SQL. Combined with Track 1's statistical judgment, you have the two halves every "
 "data scientist needs: the **thinking** and the **tooling**. Next up, **Track 3 (EDA &amp; "
 "Visualization)** puts them together to explore data and tell the truth with charts.",
 "&#9670;"))

LESSONS={"py-06-interview":"\n".join(p)}
