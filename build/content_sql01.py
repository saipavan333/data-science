# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Here is a fact nobody tells beginners loudly enough: in almost every data job, the data does "
 "**not** arrive as a tidy CSV. It lives in a ~database~ &mdash; often billions of rows across many "
 "tables &mdash; and the only way to get it out is ~SQL~. That's why practically every data-science "
 "and analytics interview has a dedicated **SQL round**. The good news: the core of SQL is small, "
 "surprisingly readable, and you can be genuinely useful with it in an afternoon. This lesson teaches "
 "the one statement you'll write more than any other &mdash; `SELECT` &mdash; and by the end you'll be "
 "running real queries against a real table, right here in the page."))

p.append(B.h2("What SQL is, in one breath", kicker="Concept"))
p.append(B.concept(
 "~SQL~ (Structured Query Language, say it \"sequel\" or spell it out &mdash; both are fine) is the "
 "language for asking questions of data stored in ~tables~. A table is just a grid, exactly like a "
 "spreadsheet: each ~row~ is one record (one order, one user) and each ~column~ is one field (amount, "
 "country). A ~database~ is a collection of such tables that a ~query~ reads from.\n\n"
 "The thing that makes SQL easy to learn is that it's ~declarative~: you describe **what** you want, "
 "not **how** to fetch it. You say \"give me the customer and amount for orders over 100, biggest "
 "first\" &mdash; and the database figures out the efficient way to do it. You'll spend your time "
 "describing results, not writing loops."))

p.append(B.h2("The five clauses of a SELECT", kicker="Concept · the whole lesson in one picture"))
p.append(B.concept(
 "Ninety percent of everyday SQL is one statement &mdash; `SELECT` &mdash; built from a handful of "
 "~clauses~ that always appear in the same order. Learn these five and you can already answer real "
 "questions:"))
p.append(B.figure(IMG+"s_sql_select.png",
 "**The anatomy of a SELECT.** `SELECT` names the columns, `FROM` names the table, `WHERE` keeps "
 "only matching rows, `ORDER BY` sorts them, and `LIMIT` caps how many come back. Read top to bottom, "
 "it's almost an English sentence.",
 "A SELECT query with SELECT, FROM, WHERE, ORDER BY and LIMIT clauses, each explained, and a "
 "plain-English reading of the query."))
p.append(B.concept(
 "A few conventions from that picture: keywords like `SELECT` and `WHERE` are traditionally written in "
 "**UPPERCASE** (SQL doesn't require it, but it makes queries readable). `*` is a shortcut meaning "
 "*every column*. Text values go in **single quotes** (`'US'`), numbers don't (`100`). And a statement "
 "ends with a semicolon `;`."))

p.append(B.h2("Run your first queries", kicker="Worked example · real SQL, live"))
p.append(B.concept(
 "Let's actually run SQL. We'll use `sqlite3` &mdash; a tiny database that's built into Python (and "
 "into this page), so there's nothing to install and you can click **Run**. First we create a small "
 "`orders` table and look at everything in it with `SELECT * FROM orders`:"))
_c,_o=_run(r'''
import sqlite3
db = sqlite3.connect(":memory:")   # a throwaway in-memory database

db.executescript("""
CREATE TABLE orders (
    id INTEGER, customer TEXT, category TEXT,
    amount REAL, country TEXT
);
INSERT INTO orders VALUES
 (101,'Ada',  'Electronics',240,'US'),
 (102,'Blake','Apparel',     45,'US'),
 (103,'Chen', 'Electronics',220,'CA'),
 (104,'Diego','Home',       130,'MX'),
 (105,'Ada',  'Apparel',    190,'US'),
 (106,'Priya','Electronics',510,'CA'),
 (107,'Blake','Home',       160,'US'),
 (108,'Chen', 'Electronics',300,'US');
""")

def run(sql):                      # run a query, print it as a table
    cur  = db.execute(sql)
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()
    w = [max(len(str(v)) for v in [col, *(r[i] for r in rows)])
         for i, col in enumerate(cols)]
    show = lambda vals: "  ".join(str(v).ljust(w[i]) for i, v in enumerate(vals))
    print(show(cols))
    print(show(["-" * n for n in w]))
    for r in rows:
        print(show(r))

run("SELECT * FROM orders")        # <- the SQL. everything else is just plumbing.
''')
p.append(B.code_example(_c,_o,filename="explore_orders.py"))
p.append(B.concept(
 "That `run()` helper is just there to print results nicely &mdash; ignore it and keep your eye on the "
 "**SQL string**, which is the part that matters. Now let's ask a real question instead of dumping the "
 "whole table: *who placed the three biggest US orders over $100?* That's all five clauses working "
 "together:"))
_c2,_o2=_run(r'''
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE orders (id INTEGER, customer TEXT, category TEXT, amount REAL, country TEXT);
INSERT INTO orders VALUES
 (101,'Ada','Electronics',240,'US'),(102,'Blake','Apparel',45,'US'),
 (103,'Chen','Electronics',220,'CA'),(104,'Diego','Home',130,'MX'),
 (105,'Ada','Apparel',190,'US'),(106,'Priya','Electronics',510,'CA'),
 (107,'Blake','Home',160,'US'),(108,'Chen','Electronics',300,'US');
""")
def run(sql):
    cur  = db.execute(sql)
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()
    w = [max(len(str(v)) for v in [col, *(r[i] for r in rows)])
         for i, col in enumerate(cols)]
    show = lambda vals: "  ".join(str(v).ljust(w[i]) for i, v in enumerate(vals))
    print(show(cols)); print(show(["-" * n for n in w]))
    for r in rows: print(show(r))

run("""
    SELECT   customer, amount
    FROM     orders
    WHERE    amount > 100 AND country = 'US'
    ORDER BY amount DESC
    LIMIT    3
""")
''')
p.append(B.code_example(_c2,_o2,filename="top_us_orders.py"))
p.append(B.concept(
 "Trace how the clauses cooperated: `FROM orders` picked the table, `WHERE amount > 100 AND country = "
 "'US'` threw away every row that wasn't a US order above $100, `ORDER BY amount DESC` sorted the "
 "survivors highest-first, and `LIMIT 3` kept only the top three. Chen's $300 order leads; note that "
 "Ada appears twice because she has two qualifying orders &mdash; SQL returns rows, not people (grouping "
 "by person is the next lesson). Change `DESC` to `ASC`, or `'US'` to `'CA'`, hit Run, and watch the "
 "answer change."))

LAB_DB = """
CREATE TABLE orders (id INTEGER, customer TEXT, category TEXT, amount REAL, country TEXT);
INSERT INTO orders VALUES
 (101,'Ada','Electronics',240,'US'),(102,'Blake','Apparel',45,'US'),
 (103,'Chen','Electronics',220,'CA'),(104,'Diego','Home',130,'MX'),
 (105,'Ada','Apparel',190,'US'),(106,'Priya','Electronics',510,'CA'),
 (107,'Blake','Home',160,'US'),(108,'Chen','Electronics',300,'US');
"""
p.append(B.h2("Your turn - write your first query", kicker="Interactive lab"))
p.append(B.lab(
 "Return the `customer` and `amount` of every **Electronics** order, biggest first.",
 LAB_DB,
 "SELECT customer, amount FROM orders WHERE category = 'Electronics' ORDER BY amount DESC",
 starter="-- orders(id, customer, category, amount, country)\\nSELECT ",
 hint="Pick the two columns after SELECT, filter with WHERE category = 'Electronics', and sort with ORDER BY amount DESC.",
 title="Lab 1 - your first SELECT",
 explain="Text values need single quotes; DESC puts the largest amount first."))

p.append(B.keypoints([
 "~SQL~ is how you pull data out of ~databases~, where real-world data lives. It's a near-universal, "
 "interviewed job skill.",
 "Data sits in ~tables~ (rows = records, columns = fields). SQL is ~declarative~: you say **what** you "
 "want, not how to get it.",
 "A `SELECT` has five everyday clauses, always in this order: `SELECT` (columns) · `FROM` (table) · "
 "`WHERE` (filter rows) · `ORDER BY` (sort) · `LIMIT` (cap rows).",
 "`*` means every column; text literals need `'single quotes'`; `DESC` sorts high→low, `ASC` low→high.",
 "`WHERE` filters **rows** by a condition; `SELECT` chooses **columns**. Keeping those two straight is "
 "half of beginner SQL.",
]))

p.append(B.quiz([
 {"q":"What does this return?  `SELECT name, price FROM products WHERE price > 50 ORDER BY price ASC "
      "LIMIT 5;`",
  "options":[
   {"t":"The name and price of the 5 cheapest products that cost more than 50, cheapest first","correct":True,
    "why":"Correct. WHERE keeps products over 50, ORDER BY price ASC sorts them cheapest-first, and "
          "LIMIT 5 takes the first five of those — so, the five cheapest above 50."},
   {"t":"The 5 most expensive products over 50",
    "why":"That would need ORDER BY price DESC. With ASC the cheapest come first, so LIMIT 5 grabs the "
          "five cheapest (above 50), not the most expensive."},
   {"t":"All products over 50, with only 5 columns shown",
    "why":"LIMIT caps the number of *rows*, not columns. You get at most 5 rows, and exactly 2 columns "
          "(name, price)."},
   {"t":"Every product, sorted by price",
    "why":"The WHERE clause removes products priced 50 or below, and LIMIT 5 keeps only five rows — so "
          "it's not every product."}]},
 {"q":"In `SELECT * FROM orders`, what does the `*` mean?",
  "options":[
   {"t":"Return every column of the table","correct":True,
    "why":"Correct. `*` is shorthand for 'all columns'. It's handy for a quick look, though naming the "
          "columns you actually need is better practice in real queries."},
   {"t":"Return every row of the table",
    "why":"You do get every row here, but that's because there's no WHERE clause — not because of `*`. "
          "The `*` is about columns; it means 'all of them'."},
   {"t":"Multiply the columns together",
    "why":"`*` is arithmetic multiplication only inside an expression like `price * quantity`. Right "
          "after SELECT, it means 'all columns'."},
   {"t":"Select from all tables at once",
    "why":"It selects all *columns* from the one table named in FROM. Combining tables is done with "
          "JOINs, not `*`."}]},
 {"q":"You run `SELECT * FROM orders WHERE country = US` and get an error. What's wrong?",
  "options":[
   {"t":"Text values need single quotes: it should be country = 'US'","correct":True,
    "why":"Correct. Without quotes, SQL reads US as a column name, finds no such column, and errors. "
          "String literals must be quoted: `country = 'US'`. Numbers, like `amount > 100`, are not "
          "quoted."},
   {"t":"You must use == instead of = for comparison",
    "why":"Unlike Python, SQL uses a single `=` for equality in WHERE. The real problem is the missing "
          "quotes around US."},
   {"t":"WHERE can't be used with text columns",
    "why":"WHERE works fine with text — e.g. `WHERE country = 'US'`. The issue is purely the missing "
          "quotes around the literal."},
   {"t":"country must appear in SELECT to be used in WHERE",
    "why":"You can filter on any column whether or not it's selected. The error is the unquoted text "
          "value."}]},
]))

p.append(B.practice([
 {"q":"Using the `orders` table from the worked example, write a query that returns the customer and "
      "amount of every **Electronics** order, largest amount first.",
  "sol":"`SELECT customer, amount FROM orders WHERE category = 'Electronics' ORDER BY amount DESC;` "
        "&mdash; WHERE filters to the Electronics rows, ORDER BY amount DESC sorts them high-to-low. "
        "You'd get Priya 510, Chen 300, Ada 240, Chen 220. (No LIMIT, so all four come back.)"},
 {"q":"A teammate wants \"the 5 newest orders\" and writes: `SELECT * FROM orders ORDER BY LIMIT 5;`  "
      "It errors. What did they forget, and what's a correct version?",
  "sol":"`ORDER BY` needs to know *which column* to sort on — they left it blank. If a higher `id` "
        "means newer, a correct query is `SELECT * FROM orders ORDER BY id DESC LIMIT 5;` — sort by "
        "id, highest (newest) first, then keep 5. Always pair ORDER BY with a column (and usually a "
        "direction)."},
]))

p.append(B.deepdive(
 B.figure(IMG+"s_sql_runorder.png",
  "**Written order vs. execution order.** You type SELECT first, but the database runs FROM and WHERE "
  "before SELECT. That ordering explains several 'why doesn't this work?' moments.",
  "Five boxes showing SQL runs FROM, then WHERE, then SELECT, then ORDER BY, then LIMIT.") +
 B.concept(
  "**Execution order is not writing order.** Although you *write* `SELECT ... FROM ... WHERE ...`, the "
  "engine *runs* them as: `FROM` (get the table) → `WHERE` (filter rows) → `SELECT` (pick/compute "
  "columns) → `ORDER BY` (sort) → `LIMIT` (cut). The practical consequence: a new column or alias you "
  "create in `SELECT` doesn't exist yet when `WHERE` runs, so `WHERE my_alias > 5` fails. You'd repeat "
  "the expression in WHERE, or filter later with `HAVING` (a Track-topic for grouped queries).") +
 B.concept(
  "**NULL is not zero &mdash; it's 'unknown'.** Databases use ~NULL~ for missing values, and it behaves "
  "surprisingly: `amount > 100` is neither true nor false for a NULL amount, so those rows are silently "
  "**dropped** by WHERE. To find or keep missing values you must say `WHERE amount IS NULL` or `IS NOT "
  "NULL` &mdash; never `= NULL`, which never matches anything. Forgetting this quietly loses rows and is "
  "a classic bug (and interview question).") +
 B.concept(
  "**Two more everyday tools.** `DISTINCT` removes duplicate rows from a result &mdash; `SELECT DISTINCT "
  "country FROM orders` lists each country once. And `SELECT *` is fine for exploring, but in real code "
  "you should **name the columns** you want: it's faster, and it won't silently break when someone adds "
  "or reorders columns in the table. Comments use `--` for the rest of a line, and keywords are "
  "case-insensitive (`select` works), though UPPERCASE is the readable convention."),
 title="Deep dive: execution order, the NULL trap, DISTINCT, and SELECT * in the real world"))

p.append(B.callout("note","Interview-ready",
 "Expect a live SQL screen. The bread-and-butter task is exactly this lesson: *\"from this table, return "
 "these columns, filtered like so, sorted, top N.\"* Two favorite gotchas hide here &mdash; that `WHERE` "
 "runs before `SELECT` (so SELECT aliases aren't usable in WHERE), and that `NULL`s vanish from `WHERE` "
 "comparisons unless you use `IS NULL`. Say those two out loud correctly and you'll look seasoned.",
 "&#9670;"))

LESSONS={"sql-01-select":"\n".join(p)}
print("content_sql01 OK — body chars:", len(LESSONS["sql-01-select"]))
print("--- cell 1 output ---"); print(_o)
print("--- cell 2 output ---"); print(_o2)
