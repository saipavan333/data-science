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
CREATE TABLE customers (
    id INTEGER, name TEXT, country TEXT, spend REAL, plan TEXT
);
INSERT INTO customers VALUES
 (1,'Ada',  'US',240,'pro'),
 (2,'Blake','US', 95, NULL),
 (3,'Chen', 'CA',220,'pro'),
 (4,'Diego','MX',130,'free'),
 (5,'Priya','CA',510,'pro'),
 (6,'Sara', 'US',180, NULL),
 (7,'Tom',  'UK', 60,'free'),
 (8,'Wei',  'CA',300,'pro');
""")
def run(sql):
    cur  = db.execute(sql)
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()
    w = [max(len(str(v)) for v in [col, *(r[i] for r in rows)] + [""])
         for i, col in enumerate(cols)]
    show = lambda vals: "  ".join(str(v).ljust(w[i]) for i, v in enumerate(vals))
    print(show(cols)); print(show(["-"*n for n in w]))
    for r in rows: print(show(r))
'''

p.append(B.why(
 "The first table you ever query at work will have millions of rows. Almost no real question wants "
 "all of them &mdash; it wants *the ones that matter*: the US customers who spent over $100 last "
 "month, the orders that failed, the accounts with no plan set. The `WHERE` clause is how you say "
 "exactly which rows you mean. Getting fluent here is the difference between an analyst who dumps a "
 "spreadsheet and one who answers the actual question &mdash; and it hides one of the most famous "
 "bugs in all of SQL, the ~NULL~ trap, which quietly deletes rows you meant to keep."))

p.append(B.h2("The WHERE toolkit: AND, OR, NOT — and parentheses", kicker="Concept"))
p.append(B.concept(
 "`WHERE` keeps only the rows for which a condition is **true**. You combine conditions with the "
 "~logical operators~ `AND` (both must hold), `OR` (either may hold), and `NOT` (flip it). The one "
 "rule that trips everyone up: `AND` binds **tighter** than `OR` &mdash; SQL evaluates all the "
 "`AND`s first, exactly like &times; before + in arithmetic. So `A OR B AND C` means `A OR (B AND "
 "C)`, which is often *not* what you meant. When in doubt, add **parentheses** and say precisely "
 "what you want. Here is the same query with and without them, on a small `customers` table:"))
_c,_o=_run(SETUP + '''
print(">>> country = 'US' OR country = 'CA' AND spend > 250   (AND binds first!)")
run("SELECT name, country, spend FROM customers WHERE country='US' OR country='CA' AND spend>250")
print()
print(">>> (country = 'US' OR country = 'CA') AND spend > 250   (parentheses fix it)")
run("SELECT name, country, spend FROM customers WHERE (country='US' OR country='CA') AND spend>250")
''')
p.append(B.code_example(_c,_o,filename="where_precedence.py"))
p.append(B.concept(
 "Read the two results. Without parentheses, `AND` ran first, so the query returned *every* US "
 "customer **plus** the CA customers over $250 &mdash; probably not the intent. With parentheses it "
 "returns customers from US or CA **and** over $250. Same words, different answer. Parentheses are "
 "free; ambiguity is expensive."))

p.append(B.h2("Sets, ranges, and patterns: IN, BETWEEN, LIKE", kicker="Concept"))
p.append(B.concept(
 "Three shortcuts save you from long chains of `OR` and `AND`:\n\n"
 "- ~IN~ tests membership in a set: `country IN ('US','CA','UK')` is the tidy way to write three "
 "`OR`s.\n"
 "- ~BETWEEN~ is an **inclusive** range: `spend BETWEEN 100 AND 250` means `spend >= 100 AND spend "
 "<= 250` &mdash; both ends are included, which is easy to forget.\n"
 "- ~LIKE~ matches text ~patterns~ using two wildcards: `%` stands for any run of characters "
 "(including none) and `_` for exactly one character. `name LIKE 'A%'` finds names starting with A; "
 "`'%a%'` finds names containing a lowercase a; `'_a%'` finds names whose second letter is a."))
_c,_o=_run(SETUP + '''
print(">>> country IN ('US','UK')  AND  spend BETWEEN 100 AND 250")
run("SELECT name, country, spend FROM customers WHERE country IN ('US','UK') AND spend BETWEEN 100 AND 250")
print()
print(">>> name LIKE '%a%'   (name contains a lowercase 'a')")
run("SELECT name FROM customers WHERE name LIKE '%a%'")
''')
p.append(B.code_example(_c,_o,filename="in_between_like.py"))

p.append(B.h2("The NULL trap — the bug that silently drops rows", kicker="Concept · the big one"))
p.append(B.concept(
 "Databases use ~NULL~ to mean **unknown / not recorded** &mdash; it is *not* zero and *not* an empty "
 "string. Here two customers have no `plan` set (`NULL`). Now the surprise: in SQL, any comparison "
 "with `NULL` is neither true nor false &mdash; it is a third value, ~unknown~. And `WHERE` keeps "
 "only rows that are **true**. So `WHERE plan = 'pro'` skips the NULLs (fine), but so does `WHERE "
 "plan != 'pro'` &mdash; the customers with an unknown plan fall through **both** filters and vanish "
 "from your results. Watch it happen:"))
_c,_o=_run(SETUP + '''
print(">>> plan = 'pro'")
run("SELECT name, plan FROM customers WHERE plan = 'pro'")
print()
print(">>> plan != 'pro'   (notice: Blake and Sara, whose plan is NULL, are NOT here)")
run("SELECT name, plan FROM customers WHERE plan != 'pro'")
print()
print(">>> plan IS NULL   (the ONLY way to catch them)")
run("SELECT name, plan FROM customers WHERE plan IS NULL")
''')
p.append(B.code_example(_c,_o,filename="null_trap.py"))
p.append(B.warn(
 "You can never test `NULL` with `=`, `!=`, `<`, or `>` &mdash; those all evaluate to *unknown* and "
 "the row is dropped. To include or find missing values you must use `IS NULL` or `IS NOT NULL`. If "
 "you want \"everyone not on pro, including unknowns\", write `WHERE plan IS NULL OR plan != 'pro'`. "
 "Forgetting this quietly biases counts and averages &mdash; and it is one of the most common SQL "
 "interview questions.", "&#9650;"))

p.append(B.widget("null-logic", "See the NULL trap happen, row by row",
 "Switch the `WHERE` condition and watch which rows survive. The two customers with a **NULL** "
 "plan are dropped by *both* `= 'pro'` **and** `!= 'pro'` &mdash; because a comparison against "
 "NULL is neither true nor false. Only `IS NULL` can catch them."))

p.append(B.h2("Sorting and de-duplicating: ORDER BY & DISTINCT", kicker="Concept"))
p.append(B.concept(
 "~ORDER BY~ sorts the result. You can sort by several keys and pick a direction for each: `ORDER "
 "BY country ASC, spend DESC` groups rows by country alphabetically, and *within* each country puts "
 "the biggest spenders first. `ASC` (ascending, the default) runs low&rarr;high; `DESC` runs "
 "high&rarr;low. ~DISTINCT~ removes duplicate rows from the output &mdash; `SELECT DISTINCT country "
 "FROM customers` lists each country once, which is the quick way to ask \"what values actually "
 "appear in this column?\""))
_c,_o=_run(SETUP + '''
print(">>> ORDER BY country ASC, spend DESC")
run("SELECT name, country, spend FROM customers ORDER BY country ASC, spend DESC")
print()
print(">>> SELECT DISTINCT country")
run("SELECT DISTINCT country FROM customers ORDER BY country")
''')
p.append(B.code_example(_c,_o,filename="order_distinct.py"))


LAB_DB = """
CREATE TABLE customers (id INTEGER, name TEXT, country TEXT, spend REAL, plan TEXT);
INSERT INTO customers VALUES
 (1,'Ada','US',240,'pro'),(2,'Blake','US',95,NULL),(3,'Chen','CA',220,'pro'),
 (4,'Diego','MX',130,'free'),(5,'Priya','CA',510,'pro'),(6,'Sara','US',180,NULL),
 (7,'Tom','UK',60,'free'),(8,'Wei','CA',300,'pro');
"""

p.append(B.h2("Your turn — write the queries yourself", kicker="Interactive lab"))
p.append(B.concept(
 "Reading SQL and *writing* SQL are different skills, and only one of them gets you hired. These labs "
 "run a **real database inside your browser**: type a query, press **Run** to see your rows, then "
 "**Check my answer** to compare them against the correct result. Nothing is graded by matching "
 "keywords &mdash; your actual returned rows have to match. Get it wrong as many times as you like; "
 "that is how it sticks."))
p.append(B.lab(
 "Return the **name** and **spend** of customers in the **US or Canada** who spent **more than 200**, "
 "biggest spender first.",
 LAB_DB,
 "SELECT name, spend FROM customers WHERE country IN ('US','CA') AND spend > 200 ORDER BY spend DESC",
 starter="-- table: customers(id, name, country, spend, plan)\nSELECT ",
 hint="Two conditions joined by `AND`: one uses `IN ('US','CA')`, the other is a plain `>`. "
      "Then sort with `ORDER BY spend DESC`.",
 title="Lab 1 — filter, then sort",
 explain="`IN` covers both countries in one clause, `AND` adds the spend test, and `DESC` puts the "
         "biggest first."))
p.append(B.lab(
 "Now the trap you just learned. Return the **name** and **plan** of every customer who is **not on "
 "the 'pro' plan** &mdash; and it must **include** the two customers whose plan is missing. Sort by "
 "name.",
 LAB_DB,
 "SELECT name, plan FROM customers WHERE plan IS NULL OR plan != 'pro' ORDER BY name",
 starter="-- careful: two customers have a NULL plan\nSELECT ",
 hint="Writing only `plan != 'pro'` silently drops the NULL rows, because `NULL != 'pro'` is "
      "*unknown*, not true. You must allow them explicitly with `plan IS NULL OR ...`.",
 title="Lab 2 — don't lose the NULLs",
 explain="This is the single most common SQL bug in the wild: the `IS NULL` branch is what rescues "
         "the rows that a plain inequality throws away."))

p.append(B.table(
 ["Operator", "Means", "Example"],
 [["`AND` / `OR` / `NOT`", "combine conditions (AND binds first)", "`a > 5 AND (b = 1 OR c = 1)`"],
  ["`IN (...)`", "value is in a set", "`country IN ('US','CA')`"],
  ["`BETWEEN x AND y`", "inclusive range (both ends)", "`spend BETWEEN 100 AND 250`"],
  ["`LIKE`", "text pattern (`%`=any, `_`=one)", "`name LIKE 'A%'`"],
  ["`IS NULL` / `IS NOT NULL`", "test for missing values", "`plan IS NULL`"],
  ["`ORDER BY`", "sort (ASC low&rarr;high, DESC high&rarr;low)", "`ORDER BY spend DESC`"],
  ["`DISTINCT`", "drop duplicate result rows", "`SELECT DISTINCT country`"]],
 caption="The everyday filtering & sorting toolkit"))

p.append(B.keypoints([
 "`WHERE` keeps rows where the condition is **true**. `AND` binds tighter than `OR` &mdash; use "
 "**parentheses** to say exactly what you mean.",
 "`IN` tests set membership; `BETWEEN` is an **inclusive** range (both ends); `LIKE` matches text "
 "with `%` (any run) and `_` (one character).",
 "~NULL~ means *unknown*. Comparisons with it (`=`, `!=`, `<`, `>`) are never true, so those rows "
 "are silently **dropped** &mdash; use `IS NULL` / `IS NOT NULL`.",
 "`ORDER BY col1 ASC, col2 DESC` sorts by several keys with a direction each.",
 "`DISTINCT` removes duplicate result rows &mdash; the fast way to see which values a column "
 "actually contains.",
]))

p.append(B.quiz([
 {"q":"Which rows does `WHERE country = 'US' OR country = 'CA' AND spend > 500` return?",
  "options":[
   {"t":"All US customers, plus CA customers who spent over 500","correct":True,
    "why":"Correct. `AND` binds tighter than `OR`, so this reads `country='US' OR (country='CA' AND "
          "spend>500)` — every US row, plus only the big-spending CA rows."},
   {"t":"US and CA customers who all spent over 500",
    "why":"That would need parentheses: `(country='US' OR country='CA') AND spend>500`. As written, "
          "the spend filter only applies to the CA branch."},
   {"t":"Only customers who spent over 500",
    "why":"The US branch has no spend condition, so US customers under 500 are included too."},
   {"t":"A syntax error",
    "why":"It's valid SQL; it just may not mean what you intended because AND is evaluated before OR."}]},
 {"q":"A column `plan` has some `NULL` values. `WHERE plan != 'free'` returns everyone whose plan "
      "isn't free — true or false?",
  "options":[
   {"t":"False — rows where plan is NULL are dropped, because NULL != 'free' is 'unknown', not true","correct":True,
    "why":"Correct. `NULL != 'free'` evaluates to *unknown*, and WHERE keeps only *true* rows, so the "
          "NULL-plan customers disappear. Use `WHERE plan IS NULL OR plan != 'free'` to include them."},
   {"t":"True — != returns everything that isn't exactly 'free'",
    "why":"It feels that way, but NULL comparisons are never true. Rows with a NULL plan are excluded "
          "by `!= 'free'`, which is the classic NULL trap."},
   {"t":"True, but only if the column is indexed",
    "why":"Indexes don't change NULL logic. Regardless of indexing, `NULL != 'free'` is unknown and "
          "those rows are dropped."},
   {"t":"False — != is not valid SQL",
    "why":"`!=` (and `<>`) are valid inequality operators. The real issue is three-valued logic with "
          "NULL."}]},
 {"q":"You want each region that appears in the table, listed once. Which query?",
  "options":[
   {"t":"SELECT DISTINCT region FROM t","correct":True,
    "why":"Correct. DISTINCT collapses duplicate result rows, so each region value appears exactly "
          "once."},
   {"t":"SELECT region FROM t",
    "why":"This lists the region of *every* row, so common regions repeat many times. You need "
          "DISTINCT (or GROUP BY region)."},
   {"t":"SELECT UNIQUE region FROM t",
    "why":"`UNIQUE` is a constraint keyword, not a SELECT modifier. The keyword you want is DISTINCT."},
   {"t":"SELECT region FROM t WHERE region IS NOT NULL",
    "why":"That filters out NULLs but still repeats every non-null region once per row. DISTINCT is "
          "what de-duplicates."}]},
]))

p.append(B.practice([
 {"q":"From a `customers(name, country, spend, plan)` table, write a query for the names and spend "
      "of customers in the US or Canada who spent between 150 and 400, biggest spender first.",
  "sol":"`SELECT name, spend FROM customers WHERE country IN ('US','CA') AND spend BETWEEN 150 AND "
        "400 ORDER BY spend DESC;` &mdash; `IN` handles the two countries, `BETWEEN` the inclusive "
        "range, and `ORDER BY spend DESC` sorts high to low. (Parentheses aren't needed here because "
        "there is only one `AND` level, but they never hurt.)"},
 {"q":"A colleague runs `SELECT COUNT(*) FROM customers WHERE plan = 'pro'` and separately `SELECT "
      "COUNT(*) FROM customers WHERE plan != 'pro'`, then is confused that the two counts don't add "
      "up to the total number of customers. Explain why, and how to account for everyone.",
  "sol":"Customers with a `NULL` plan satisfy **neither** condition &mdash; `NULL = 'pro'` and `NULL "
        "!= 'pro'` are both *unknown*, so those rows are dropped from both counts. The missing rows "
        "are exactly the ones with an unset plan. To cover everyone, add a third bucket "
        "`WHERE plan IS NULL`, or count it directly: the totals reconcile as "
        "`(plan='pro') + (plan!='pro') + (plan IS NULL) = all rows`."},
]))

p.append(B.deepdive(
 B.concept(
  "**Three-valued logic.** Ordinary logic has two values, true and false. SQL has **three**: true, "
  "false, and ~unknown~ (what any comparison with NULL produces). The rules follow intuition once you "
  "accept the third value: `true AND unknown = unknown`, `false AND unknown = false`, `true OR "
  "unknown = true`, `false OR unknown = unknown`. Because `WHERE` and `HAVING` keep only **true** "
  "rows, anything that comes out *unknown* is discarded &mdash; which is the entire reason the NULL "
  "trap exists. `IS NULL` is special precisely because it returns a real true/false, never unknown.") +
 B.concept(
  "**LIKE, case, and escaping.** In SQLite `LIKE` is case-insensitive for ASCII letters (`'a%'` "
  "matches 'Ada'), while `GLOB` is case-sensitive and uses `*`/`?` wildcards instead. If you need to "
  "match a literal `%` or `_`, use an escape character: `LIKE '100\\%' ESCAPE '\\'`. Different "
  "databases differ on case sensitivity, so never *assume* &mdash; test on your engine.") +
 B.concept(
  "**Why this touches performance.** A plain `WHERE country = 'US'` can use an ~index~ on `country` "
  "to jump straight to matching rows. But wrap the column in a function &mdash; `WHERE "
  "LOWER(country) = 'us'` &mdash; and the database usually can't use that index and must scan every "
  "row. Same for a leading-wildcard `LIKE '%us'`. You don't need to optimize yet, but the habit of "
  "filtering on the bare column (not a function of it) pays off the day your table gets big."),
 title="Deep dive: three-valued logic, LIKE and escaping, and why filters touch performance"))

p.append(B.callout("note","Interview-ready",
 "The NULL trap is a near-guaranteed question: *\"what does `WHERE col != 'x'` do to NULL rows?\"* "
 "&mdash; answer: drops them, because `NULL != 'x'` is *unknown*, not true; use `IS NULL`. The other "
 "favorite is operator precedence &mdash; be ready to explain why `A OR B AND C` needs parentheses. "
 "Say both cleanly and you signal real fluency, not just memorized keywords.", "&#9670;"))

LESSONS={"sql-02-filter":"\n".join(p)}
print("content_sql02 OK — chars:", len(LESSONS["sql-02-filter"]))
