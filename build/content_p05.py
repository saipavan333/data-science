# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Raw rows rarely answer a question directly. 'What's revenue by category?' 'How do months "
 "compare?' 'What did each customer spend, with their region attached?' Answering these means "
 "**reshaping** and **aggregating** &mdash; turning a pile of rows into a summary that speaks. "
 "Three verbs do almost all of it: ~groupby~, ~pivot~/~melt~, and ~merge~. Master them and you "
 "can answer most business questions in a line or two."))

p.append(B.h2("groupby: split, apply, combine", kicker="Concept · the workhorse"))
p.append(B.concept(
 "~groupby~ is the single most used operation in data analysis. It follows one pattern: **split** "
 "the rows into groups by some key, **apply** a function to each group, and **combine** the "
 "results into one row per group. 'Average order value by category' is exactly this."))
p.append(B.figure(IMG+"s_pd_groupby.png",
 "**Split-apply-combine.** Group the rows by category, apply `sum` to each group, and combine "
 "into one tidy row per category. Swap `sum` for `mean`, `count`, `max`, or several at once with "
 "`.agg([...])`.",
 "Diagram of groupby splitting rows, applying sum, and combining into a summary."))

p.append(B.h2("Reshaping: pivot and melt", kicker="Concept · changing the layout"))
p.append(B.concept(
 "The *same* data can be laid out two ways. ~Long~ (or 'tidy') form has one row per observation "
 "&mdash; great for storage and most analysis. ~Wide~ form spreads a variable across columns "
 "&mdash; great for reading and for some charts. ~pivot~ goes long&rarr;wide; ~melt~ goes "
 "wide&rarr;long. You'll constantly switch between them."))
p.append(B.figure(IMG+"s_pd_pivot_melt.png",
 "**Pivot widens, melt lengthens.** Both hold identical information &mdash; only the shape "
 "changes. Reach for wide when a human needs to read it; keep it long when a computer needs to "
 "process it.",
 "Long and wide layouts of the same data linked by pivot and melt."))

p.append(B.h2("Joining tables: merge", kicker="Concept · combining sources"))
p.append(B.concept(
 "Real answers usually live across multiple tables &mdash; orders here, customer details there, "
 "product margins somewhere else. ~merge~ (a database ~join~) stitches two tables together on a "
 "shared **key** column. The ~how~ argument decides which rows survive when keys don't all "
 "match:"))
p.append(B.figure(IMG+"s_pd_joins.png",
 "**The four joins.** `inner` keeps only matching keys; `left` keeps all left rows (your main "
 "table) and attaches matches; `right` mirrors it; `outer` keeps everything. `left` is the "
 "everyday default &mdash; 'keep all my orders, add customer info where I have it.'",
 "Venn diagrams of inner, left, right, and outer joins."))
p.append(B.warn(
 "Check your row count after a merge. If the key isn't unique in the table you join *to*, rows "
 "can **multiply** (a one-to-many join), silently inflating sums and averages. A quick "
 "`len(df)` before and after &mdash; or `validate=\"many_to_one\"` &mdash; catches this common, "
 "costly bug.", "&#9650;"))

p.append(B.h2("Reshape and join in code", kicker="Worked example"))
p.append(B.concept(
 "Aggregate orders by category, then merge in each category's profit margin and compute profit "
 "&mdash; a miniature of real analytical work."))
_c,_o=_run(r'''
import pandas as pd

orders = pd.DataFrame({
    "category": ["Electronics", "Apparel", "Electronics", "Beauty", "Apparel"],
    "amount":   [180, 45, 220, 30, 95],
})

# 1) groupby: several aggregations at once.
summary = orders.groupby("category")["amount"].agg(["sum", "mean", "count"])
print(summary.to_string())

# 2) merge: attach each category's margin (a left join on 'category'), then compute profit.
margins = pd.DataFrame({"category": ["Electronics", "Apparel", "Beauty"],
                        "margin":   [0.25, 0.50, 0.60]})
joined = orders.merge(margins, on="category", how="left")
joined["profit"] = joined["amount"] * joined["margin"]
print("\n" + joined.to_string(index=False))
print(f"\ntotal profit: ${joined['profit'].sum():.2f}")
''')
p.append(B.code_example(_c,_o,filename="reshape_aggregate.py"))
p.append(B.concept(
 "That's the daily rhythm of analysis: **group** to summarize, **merge** to enrich, **compute** "
 "the metric that answers the question. Everything you did by hand in pure Python back in 2.1 is "
 "now a few declarative lines &mdash; and it scales to millions of rows."))

p.append(B.keypoints([
 "~groupby~ = **split** by a key, **apply** a function, **combine** into one row per group; use "
 "`.agg([...])` for several stats at once.",
 "~Long/tidy~ = one row per observation; ~wide~ spreads a variable across columns. ~pivot~ "
 "widens, ~melt~ lengthens.",
 "~merge~ joins tables on a **key**; `how=` picks **inner / left / right / outer**. `left` is the "
 "common default.",
 "**Check row counts around merges** &mdash; a non-unique key causes one-to-many row explosions "
 "that corrupt totals.",
 "These three verbs (group, reshape, join) answer most business questions in a line or two.",
]))

p.append(B.quiz([
 {"q":"You want total and average `revenue` for each `region`. Which call does it?",
  "options":[
   {"t":'df.groupby("region")["revenue"].agg(["sum", "mean"])',"correct":True,
    "why":"Correct. Group by region, select revenue, and apply both aggregations with `.agg`, "
          "giving one row per region with sum and mean columns."},
   {"t":'df["revenue"].sum()',
    "why":"That collapses the whole column to a single number, ignoring region. You need to group "
          "by region first."},
   {"t":'df.sort_values("region")',
    "why":"Sorting orders the rows but doesn't aggregate. You need groupby + agg to get per-region "
          "totals."},
   {"t":'df.pivot("region")',
    "why":"pivot reshapes existing values into a wide layout; it doesn't compute sums/means by "
          "group. Use groupby for aggregation."}]},
 {"q":"You `merge` your 1,000-row orders table with a products table, and suddenly have 1,400 "
      "rows. What most likely happened?",
  "options":[
   {"t":"The product key wasn't unique, so some orders matched multiple product rows (one-to-many "
        "explosion)","correct":True,
    "why":"Correct. If the join key repeats in the products table, each matching order row is "
          "duplicated per match, inflating the row count and any sums computed afterward."},
   {"t":"merge always adds 40% more rows",
    "why":"merge doesn't add rows by a fixed rate. Row growth means the key was non-unique on the "
          "right, causing one-to-many matches."},
   {"t":"An inner join created extra rows",
    "why":"Inner joins keep only matches and never invent rows beyond key multiplicity. The growth "
          "comes from a non-unique key, regardless of join type."},
   {"t":"The orders table was corrupted by the merge",
    "why":"The source isn't corrupted; the extra rows come from duplicate keys in the table you "
          "merged to. Check key uniqueness (or use validate=)."}]},
 {"q":"A table has columns `month`, `metric`, `value` (long form) and you want one column per "
      "metric, one row per month (wide form). Which operation?",
  "options":[
   {"t":"pivot — it spreads the metric values into columns","correct":True,
    "why":"Correct. pivot turns the distinct `metric` values into columns indexed by `month`, "
          "going from long to wide."},
   {"t":"melt — it would stack columns into rows",
    "why":"melt goes the other way (wide&rarr;long). You already have long form and want wide, so "
          "pivot is the tool."},
   {"t":"groupby — it aggregates but doesn't reshape into columns",
    "why":"groupby summarizes within groups; it doesn't spread a column's values into new columns. "
          "pivot does."},
   {"t":"merge — it joins two tables",
    "why":"merge combines separate tables on a key; here you're reshaping one table's layout, "
          "which is pivot."}]},
]))

p.append(B.practice([
 {"q":"Write one line to get the **number of orders** and **total amount** per `customer_id` from "
      "a DataFrame `orders`.",
  "sol":"`orders.groupby(\"customer_id\")[\"amount\"].agg([\"count\", \"sum\"])`. Group by "
        "customer, then apply both `count` (number of orders) and `sum` (total spent), producing "
        "one row per customer with two columns. (Use `.rename(columns=...)` if you want friendlier "
        "names.)"},
 {"q":"You need each order row to also show the customer's `region`, which lives in a separate "
      "`customers` table keyed by `customer_id`. Write the merge, and say which `how` to use and "
      "why.",
  "sol":"`orders.merge(customers[[\"customer_id\", \"region\"]], on=\"customer_id\", how=\"left\")`. "
        "Use **left** so you keep **every** order even if a customer record is missing &mdash; "
        "you don't want to silently drop orders just because their customer row is absent. After "
        "merging, check the row count is unchanged (the customer key should be unique)."},
]))

p.append(B.deepdive(
 B.concept(
  "**Tidy data.** Hadley Wickham's 'tidy data' principle: each **variable** is a column, each "
  "**observation** is a row, each **type of observational unit** is a table. Long/tidy form is the "
  "ideal storage and analysis layout because group, filter, and plot operations all assume it. "
  "Reshape to wide only at the end, for human eyes or a specific chart. Keeping data tidy upstream "
  "prevents a surprising amount of pain.") +
 B.concept(
  "**agg vs transform vs filter.** `groupby(...).agg(...)` returns one row per group (a summary). "
  "`groupby(...).transform(...)` returns a result aligned to the **original** rows &mdash; perfect "
  "for adding a 'group average' column next to each row (e.g., each order's amount minus its "
  "category's mean). `groupby(...).filter(...)` keeps or drops whole groups by a condition (e.g., "
  "only categories with more than 100 orders). Picking the right one avoids clumsy merges back "
  "onto the data.") +
 B.concept(
  "**Time resampling.** With a datetime index, `df.resample(\"M\").sum()` is a time-aware groupby "
  "&mdash; it buckets rows into months (or days, weeks, quarters) and aggregates. It's how you "
  "turn raw event logs into the monthly-revenue chart from the capstone, and it handles "
  "calendar quirks (different month lengths) for you."),
 title="Deep dive: tidy data, agg vs transform vs filter, and time resampling"))

p.append(B.callout("note","Interview-ready",
 "Live Pandas/SQL exercises lean on these verbs: 'total revenue per region,' 'top 3 products per "
 "category,' 'join these tables.' Narrate the split-apply-combine pattern for groupby, state which "
 "join `how` you'd use and why (usually left, to preserve your main table), and always mention "
 "checking row counts after a merge. The SQL parallels (GROUP BY, JOIN) come up in the next "
 "lesson.", "&#9670;"))

LESSONS={"py-05-reshape":"\n".join(p)}
