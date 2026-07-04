# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Statistics told you *what* to compute; now you need a tool to actually do it. That tool is "
 "~Python~ &mdash; the language data science runs on. We assume **zero** prior coding here: every "
 "idea is shown, run, and explained before the next one builds on it. By the end you'll read and "
 "write the small set of Python that the rest of this course &mdash; NumPy, Pandas, modeling "
 "&mdash; is built from."))

# ---- how to run ----
p.append(B.h2("How you run Python", kicker="Orientation"))
p.append(B.concept(
 "You write Python as plain text and run it; whatever you `print(...)` shows up as output. You'll "
 "do this in one of two places:\n\n"
 "- A ~script~ &mdash; a file ending in `.py` that runs top to bottom all at once.\n"
 "- A ~notebook~ (a `.ipynb` file, like the capstone) &mdash; a page of **cells** you run one at "
 "a time, seeing each result immediately. Notebooks are where most data analysis happens because "
 "you can explore step by step.\n\n"
 "Every code box below is real and runnable: press **&#9654; Run** to execute it right here in "
 "your browser, or copy it into a notebook. The grey **Output** panel shows exactly what it "
 "prints. Try changing a number and running again &mdash; that's how you learn."))

# ---- values & types ----
p.append(B.h2("Values, types, and variables", kicker="Step 1 · the atoms"))
p.append(B.concept(
 "A ~value~ is a single piece of data, and every value has a ~type~. The four you'll use "
 "constantly:\n\n"
 "- ~int~ &mdash; whole numbers like `3` or `-10`\n"
 "- ~float~ &mdash; decimals like `87.5`\n"
 "- ~str~ &mdash; text ('strings'), always in quotes: `\"Austin\"`\n"
 "- ~bool~ &mdash; a truth value, either `True` or `False`\n\n"
 "A ~variable~ is just a name that points at a value, created with `=` (read it as 'gets'). And "
 "an ~f-string~ &mdash; a string with an `f` in front &mdash; lets you drop values neatly into "
 "text. Run this:"))
_c,_o=_run(r'''
# A variable is a NAME for a value. Python infers the type automatically.
city      = "Austin"     # str  (text, in quotes)
n_orders  = 3            # int  (whole number)
total     = 87.5         # float (decimal)
is_member = True         # bool (True or False)

print(city, n_orders, total, is_member)
print("the type of city is", type(city))
print("the type of total is", type(total))

# An f-string drops values into text. {total:.2f} shows 2 decimal places.
print(f"{city}: {n_orders} orders worth ${total:.2f}")
''')
p.append(B.code_example(_c,_o,filename="values.py"))
p.append(B.note(
 "The `#` starts a ~comment~ &mdash; Python ignores everything after it on the line. Comments are "
 "notes for humans; use them to explain *why*, not just *what*."))

# ---- operators ----
p.append(B.h2("Arithmetic and comparisons", kicker="Step 2 · doing things to values"))
p.append(B.concept(
 "Python is a calculator with names. Beyond `+ - * /`, two operators surprise beginners: `//` is "
 "**whole-number** division (drops the remainder) and `%` ('modulo') is **the remainder** itself "
 "&mdash; handy for 'is this even?' or 'every 10th row.' ~Comparisons~ (`>`, `<`, `==`, `!=`) "
 "don't compute a number; they produce a **bool**, which is exactly what the decisions in Step 3 "
 "run on."))
_c,_o=_run(r'''
a, b = 7, 2          # assign two variables at once

print("add", a + b, "| subtract", a - b, "| multiply", a * b)
print("divide", a / b, "| whole-divide", a // b, "| remainder", a % b)

# A comparison returns a bool (True / False), not a number:
print("is a greater than b?", a > b)
print("are they equal?", a == b)     # note: == compares, = assigns
''')
p.append(B.code_example(_c,_o,filename="operators.py"))
p.append(B.warn(
 "`=` and `==` are different and mixing them up is the #1 beginner bug. A single `=` **assigns** "
 "(`x = 5` means 'let x be 5'); a double `==` **compares** (`x == 5` asks 'is x equal to 5?', "
 "giving True or False). Use `==` inside `if` conditions.", "&#9650;"))

# ---- if/elif/else ----
p.append(B.h2("Making decisions: if / elif / else", kicker="Step 3 · choosing a path"))
p.append(B.concept(
 "Often you want different actions depending on a condition. ~if~ runs a block **only when** its "
 "condition is True; ~elif~ ('else if') checks another condition if the first was False; ~else~ "
 "catches everything left. Python decides what's 'inside' a block by ~indentation~ &mdash; the "
 "spaces at the start of a line &mdash; following the `:` at the end of the `if` line. Same "
 "indent = same block."))
p.append(B.figure(IMG+"s_py_ifelse.png",
 "**How if / elif / else flows.** Python checks each condition top to bottom and takes the "
 "**first** branch that's True, skipping the rest. `else` runs only if none matched.",
 "Flowchart of if, elif, else choosing among Hot, Mild, and Cold."))
_c,_o=_run(r'''
temp = 22

if temp >= 30:
    label = "Hot"        # this line is indented -> it's inside the 'if'
elif temp >= 15:
    label = "Mild"
else:
    label = "Cold"

print(f"{temp} degrees is {label}")
''')
p.append(B.code_example(_c,_o,filename="conditions.py"))

# ---- for loop ----
p.append(B.h2("Repeating work: the for loop", kicker="Step 4 · do it for each item"))
p.append(B.concept(
 "Data means doing the same thing to many values, and the ~for loop~ is how. It walks through a "
 "sequence, and on each pass a ~loop variable~ holds the current item while the indented **body** "
 "runs. Read `for p in prices:` as 'for each p in prices, do the following.'"))
p.append(B.figure(IMG+"s_py_forloop.png",
 "**Anatomy of a for loop.** The keywords set it up, the loop variable takes each value in turn, "
 "and the indented body runs once per value &mdash; here, three times.",
 "Labeled for loop with an iteration trace running its body three times."))
_c,_o=_run(r'''
prices = [12, 45, 7, 30]

total = 0
for p in prices:          # p becomes 12, then 45, then 7, then 30
    total = total + p     # the indented body runs once per value
print("total:", total)

# range(n) produces 0, 1, ..., n-1 — useful for counting repetitions:
for i in range(3):
    print("step", i)
''')
p.append(B.code_example(_c,_o,filename="for_loop.py"))
p.append(B.note(
 "There's also a ~while~ loop, which repeats *as long as* a condition stays True (rather than "
 "once per item). In data work you'll reach for `for` far more often, so we lead with it; "
 "`while` is in the deep dive."))

# ---- functions ----
p.append(B.h2("Packaging logic: functions", kicker="Step 5 · name it once, reuse it"))
p.append(B.concept(
 "When you find yourself doing the same calculation repeatedly, wrap it in a ~function~: a named, "
 "reusable block. You ~define~ it with `def`, list any ~parameters~ (its inputs) in parentheses, "
 "and use ~return~ to send a value back. Then you ~call~ it by name whenever you need it."))
p.append(B.figure(IMG+"s_py_func.png",
 "**Anatomy of a function.** Define it once with `def`; later, feed it an input and it returns an "
 "output. Here, `to_celsius(98.6)` returns `37.0`.",
 "Labeled function definition with an input-to-output flow."))
_c,_o=_run(r'''
def to_celsius(f):               # f is the parameter (the input)
    return (f - 32) * 5 / 9      # return hands a value back to the caller

# Call it with different inputs; each call returns a result.
print(to_celsius(98.6))
print(to_celsius(32))
''')
p.append(B.code_example(_c,_o,filename="functions.py"))

# ---- collections ----
p.append(B.h2("Collections: lists and dicts", kicker="Step 6 · holding many values"))
p.append(B.concept(
 "Real data comes in groups, and two containers cover almost everything:\n\n"
 "- A ~list~ is an **ordered** sequence accessed by **position**, counting from **0**: "
 "`prices[0]` is the first item, `prices[-1]` the last, and a ~slice~ `prices[1:3]` takes "
 "positions 1 and 2 (the stop is **excluded**).\n"
 "- A ~dict~ (dictionary) maps **keys to values**, accessed by key: `user[\"age\"]`. Use it for "
 "labeled fields about one thing."))
p.append(B.figure(IMG+"s_py_listdict.png",
 "**Lists vs. dicts.** A list is looked up by numeric position; a dict by a named key. A table of "
 "data is really a *list of dicts* &mdash; the mental model the worked example below uses.",
 "A list indexed by position beside a dict accessed by key."))
_c,_o=_run(r'''
# LIST: ordered, accessed by position (starting at 0)
prices = [12, 45, 7, 30]
print("first:", prices[0], "| last:", prices[-1], "| middle two:", prices[1:3])
prices.append(99)                 # add an item to the end
print("after append:", prices, "| how many:", len(prices))

# DICT: accessed by key, not position
user = {"name": "Ada", "age": 36}
print("name:", user["name"])
user["city"] = "Austin"           # add a new key -> value pair
print(user)
''')
p.append(B.code_example(_c,_o,filename="collections.py"))

# ---- comprehensions ----
p.append(B.h2("The Pythonic shortcut: list comprehensions", kicker="Step 7 · loops, condensed"))
p.append(B.concept(
 "You now know loops and lists &mdash; so this last piece is just a shortcut for combining them. "
 "A ~list comprehension~ builds a new list from an old one in a single line. It does exactly what "
 "a `for` loop with `.append()` does; data scientists use it constantly because it's shorter and "
 "reads almost like English. It can filter, too, with an `if` at the end."))
_c,_o=_run(r'''
prices = [12, 45, 7, 30]

# The long way you already know: a loop that builds a new list.
doubled = []
for p in prices:
    doubled.append(p * 2)
print("with a loop:        ", doubled)

# The shortcut: a list comprehension. Same result, one line.
doubled = [p * 2 for p in prices]
print("with a comprehension:", doubled)

# Add an 'if' to keep only some items:
big = [p for p in prices if p > 20]
print("only values over 20:", big)
''')
p.append(B.code_example(_c,_o,filename="comprehensions.py"))
p.append(B.tip(
 "Read a comprehension right-to-left first: *for each p in prices* (the loop), *keep it if p > 20* "
 "(the filter), *and put p*2 in the new list* (the transform). If a comprehension ever gets hard "
 "to read, a plain `for` loop is perfectly fine &mdash; clarity beats cleverness."))

# ---- worked example ----
p.append(B.h2("Putting it together", kicker="Worked example"))
p.append(B.concept(
 "Here's a real micro-analysis that uses *everything* from this lesson: a list of dicts (the "
 "shape data arrives in), a function, a filtering comprehension, dict access, and an f-string. "
 "This is the pure-Python version of work that Pandas will soon do in one line &mdash; but seeing "
 "it spelled out makes Pandas feel like magic instead of mystery."))
_c,_o=_run(r'''
orders = [
    {"id": 1, "category": "Electronics", "amount": 180.0},
    {"id": 2, "category": "Apparel",     "amount":  45.0},
    {"id": 3, "category": "Electronics", "amount": 220.0},
    {"id": 4, "category": "Beauty",      "amount":  30.0},
]

def average(values):                         # a reusable helper
    return sum(values) / len(values)

all_amounts = [o["amount"] for o in orders]                              # every amount
elec        = [o["amount"] for o in orders if o["category"] == "Electronics"]  # filtered

print(f"{len(orders)} orders | total ${sum(all_amounts):.0f} | average ${average(all_amounts):.2f}")
print(f"electronics only: {elec} | average ${average(elec):.2f}")
''')
p.append(B.code_example(_c,_o,filename="putting_it_together.py"))

p.append(B.keypoints([
 "A ~variable~ names a value; core types are ~int~, ~float~, ~str~, ~bool~. `=` **assigns**, `==` "
 "**compares**.",
 "~if~ / ~elif~ / ~else~ choose a path; ~indentation~ (after the `:`) defines what's inside a "
 "block.",
 "A ~for loop~ runs its indented body once per item; the loop variable holds the current value.",
 "A ~function~ (`def` … `return`) packages reusable logic: feed it inputs, get an output back.",
 "~list~ = ordered, by **position** from 0 (slices exclude the stop); ~dict~ = by **key**. A "
 "~comprehension~ is a one-line loop-and-build.",
]))

p.append(B.quiz([
 {"q":"With `x = 8`, an `if x % 2 == 0:` block prints 'even' and its `else:` prints 'odd'. What "
      "gets printed?",
  "options":[
   {"t":"even — 8 % 2 is 0, so the condition is True","correct":True,
    "why":"Correct. `%` gives the remainder; 8 divided by 2 leaves 0, so `x % 2 == 0` is True and "
          "the if-branch runs, printing 'even'."},
   {"t":"odd — the else branch always runs",
    "why":"`else` runs only when the condition is False. Here it is True, so the if-branch runs."},
   {"t":"both 'even' and 'odd'",
    "why":"if/else are mutually exclusive: exactly one branch runs. The condition is True, so only "
          "'even' prints."},
   {"t":"an error, because % is invalid",
    "why":"`%` (remainder) is a valid operator; the code runs and prints 'even'."}]},
 {"q":"What does `[p * 2 for p in [5, 10, 15]]` evaluate to?",
  "options":[
   {"t":"[10, 20, 30]","correct":True,
    "why":"Correct. The comprehension produces p*2 for each value 5, 10, 15, giving [10, 20, 30]."},
   {"t":"[5, 10, 15, 5, 10, 15]",
    "why":"That repeats the list. A comprehension transforms each item (p*2); it does not duplicate."},
   {"t":"30",
    "why":"A comprehension returns a list, not a sum. You would get [10, 20, 30]; summing it is a "
          "separate step."},
   {"t":"[2, 2, 2]",
    "why":"Each element is p*2, not the literal 2. With p = 5, 10, 15 you get 10, 20, 30."}]},
 {"q":"Given `prices = [12, 45, 7, 30]`, what is `prices[-1]`?",
  "options":[
   {"t":"30 — negative indices count from the end, so -1 is the last item","correct":True,
    "why":"Correct. -1 is the last element (30), -2 the second-to-last, and so on."},
   {"t":"12 — the first item",
    "why":"The first item is prices[0] (12). prices[-1] is the last item, 30."},
   {"t":"an error — negative indices are not allowed",
    "why":"Negative indices are valid in Python; prices[-1] returns 30."},
   {"t":"[30] — a one-item list",
    "why":"Indexing returns the element 30; a slice like prices[-1:] would return the list [30]."}]},
 {"q":"A function written `def double(x): x * 2` has no `return`. After `result = double(5)`, what "
      "is `result`?",
  "options":[
   {"t":"None — without a return, a function hands back None","correct":True,
    "why":"Correct. It computes x*2 but never returns it, so Python returns None by default. Add "
          "`return x * 2` to fix it."},
   {"t":"10",
    "why":"It would be 10 only if the function returned x*2. With no return, the value is discarded "
          "and result is None."},
   {"t":"5",
    "why":"5 is the input. With no return statement, result is None, not the input."},
   {"t":"an error",
    "why":"It runs without error; it simply returns None because there is no return statement."}]},
]))
p.append(B.practice([
 {"q":"Write a `for` loop that prints a greeting like 'Hello, Ada!' for each name in "
      "`names = [\"Ada\", \"Linus\", \"Grace\"]`.", "html": True,
  "sol": B.code_example("for name in names:\n    print(f\"Hello, {name}!\")",
         filename="solution.py", runnable=False) + B.fmt(
         "The loop variable `name` takes each value in turn, and the indented f-string runs once "
         "per name, printing the greeting for Ada, then Linus, then Grace.")},
 {"q":"Write a function `is_adult(age)` that returns True if age is 18 or more, otherwise False. "
      "What does `is_adult(15)` return?", "html": True,
  "sol": B.code_example("def is_adult(age):\n    return age >= 18",
         filename="solution.py", runnable=False) + B.fmt(
         "Since `age >= 18` already evaluates to a bool, you can return it directly &mdash; no "
         "if/else needed. `is_adult(15)` returns **False**, because 15 >= 18 is False.")},
 {"q":"Rewrite this as one list comprehension: a loop over `nums` that appends `n` to a list "
      "`out` only when `n > 0`.", "html": True,
  "sol": B.code_example("out = [n for n in nums if n > 0]", filename="solution.py",
         runnable=False) + B.fmt("It keeps each `n` from `nums` where `n > 0` &mdash; the same "
         "result as the loop, in one readable line. (If a comprehension ever reads awkwardly, the "
         "plain loop is equally correct.)")},
]))
p.append(B.deepdive(
 B.concept(
  "**0-indexing and exclusive slices, precisely.** A list of length n has positions 0 through "
  "**n&minus;1**. A slice `a[start:stop]` includes `start` but **excludes** `stop`, so `a[0:2]` "
  "gives two items (positions 0 and 1). Negative indices count from the end (`a[-1]` is last). "
  "Almost every off-by-one bug traces back to these two rules.") +
 B.concept(
  "**Mutability and the reference trap.** Lists and dicts are ~mutable~ (changeable in place); "
  "ints, floats, strings, and bools are ~immutable~. Crucially, `b = a` makes `b` point at the "
  "**same** list as `a`, so `b.append(9)` also changes `a`. For an independent copy use "
  "`a.copy()`. This silent sharing is a classic source of 'why did my other variable change?' "
  "bugs.") +
 B.concept(
  "**`while` loops and `None`.** A ~while~ loop repeats *as long as* a condition holds: "
  "`while balance > 0: ...` &mdash; useful when you don't know the number of repetitions in "
  "advance (just ensure the condition eventually becomes False, or it loops forever). Separately, "
  "~None~ is Python's 'no value' marker, returned by functions that don't `return` anything and "
  "used for missing data; test for it with `x is None`, and keep it distinct from `0` or `\"\"`.") +
 B.concept(
  "**Truthiness.** In a condition, empty things are treated as False: `0`, `0.0`, `\"\"`, `[]`, "
  "`{}`, and `None`. So `if orders:` reads as 'if there are any orders.' Convenient, but watch the "
  "case where `0` is a legitimate value you didn't mean to treat as empty."),
 title="Deep dive: indexing rules, mutability, while loops, None, and truthiness"))

p.append(B.callout("note","Interview-ready",
 "Early screens often include a quick Python warm-up: FizzBuzz, reversing a list, counting word "
 "frequencies with a dict, or filtering with a comprehension. Know cold that indexing starts at "
 "0, slices exclude the stop, `=` assigns while `==` compares, and a function without `return` "
 "yields None. Clean, correct basics signal you can actually code.", "&#9670;"))

LESSONS={"py-01-setup":"\n".join(p)}
