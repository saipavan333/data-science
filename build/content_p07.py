# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "In Lesson 2.1 you met functions in miniature. As your analyses grow, two things happen: you "
 "find yourself **repeating the same logic**, and your code **crashes** on the one weird row you "
 "didn't expect. The cure for both is here &mdash; functions that package logic for reuse, and "
 "error handling that lets a program stumble gracefully instead of falling over. This is the leap "
 "from 'a script that ran once' to 'code you can trust.'"))

p.append(B.h2("Functions, a little deeper", kicker="Concept · reusable logic"))
p.append(B.concept(
 "A ~function~ packages logic behind a name so you write it once and reuse it. Beyond the basics "
 "from 2.1, three features make functions powerful:\n\n"
 "- ~Default arguments~: give a parameter a fallback value so callers can omit it &mdash; "
 "`def greet(name, greeting=\"Hello\")`.\n"
 "- ~Keyword arguments~: call with names for clarity &mdash; `greet(name=\"Ada\")` &mdash; which "
 "also lets you skip past defaults.\n"
 "- Returning **multiple values**: `return lo, hi` hands back a tuple you can unpack with "
 "`lo, hi = ...`.\n\n"
 "A one-line ~docstring~ just under `def` documents what the function does &mdash; a small habit "
 "that makes code (and your future self) far happier."))

p.append(B.h2("Handling errors: try / except", kicker="Concept · don't crash"))
p.append(B.concept(
 "When code might fail &mdash; converting bad text to a number, opening a missing file &mdash; "
 "wrap it in a ~try/except~ block. Python *tries* the risky code; if an ~exception~ (error) "
 "occurs, it jumps to the matching `except` instead of crashing. Optional `else` runs when no "
 "error happened, and `finally` runs **no matter what** (for cleanup)."))
p.append(B.figure(IMG+"s_py_tryexcept.png",
 "**The try/except flow.** Risky code runs; if it errors, `except` handles it gracefully; "
 "`finally` always runs; and the program keeps going instead of stopping dead.",
 "Flowchart of try, except, else, and finally."))
p.append(B.warn(
 "Catch **specific** exceptions (`except ValueError:`), not a bare `except:`. A bare except "
 "swallows *every* error &mdash; including typos and bugs in your own code &mdash; hiding "
 "problems you needed to see. Name the error you actually expect, and let the unexpected ones "
 "surface.", "&#9650;"))

p.append(B.h2("Organizing code: modules & imports", kicker="Concept · structure"))
p.append(B.concept(
 "A ~module~ is just a `.py` file full of functions and values; ~importing~ it gives you access "
 "to that code. You already do this with `import pandas as pd` and `from math import sqrt`. "
 "Python's vast ~standard library~ (batteries included &mdash; `math`, `datetime`, `json`, "
 "`random`, &hellip;) and the wider ecosystem (NumPy, pandas, scikit-learn) are all imported the "
 "same way. As your project grows, you split your own code into modules and import across them, "
 "keeping each file focused."))

p.append(B.h2("Reusable, crash-resistant code", kicker="Worked example"))
p.append(B.concept(
 "Two small functions that show defaults, a docstring, and graceful error handling &mdash; the "
 "building blocks of dependable code."))
_c,_o=_run(r'''
def safe_average(values, default=0.0):
    """Return the mean of values, or `default` if the list is empty."""
    if not values:                  # an empty list is 'falsy' (Lesson 2.1)
        return default
    return sum(values) / len(values)

print(safe_average([10, 20, 30]))
print(safe_average([], default=-1))     # uses the default-arg fallback

def parse_price(text):
    """Convert text to a float, or None if it can't be parsed."""
    try:
        return float(text)
    except ValueError:              # catch ONLY the expected error
        return None

for t in ["19.99", "free", "5"]:
    print(f"{t!r:>7}  ->  {parse_price(t)}")
''')
p.append(B.code_example(_c,_o,filename="functions_errors.py"))
p.append(B.concept(
 "`safe_average` never divides by zero because it handles the empty case; `parse_price` never "
 "crashes on bad text because it catches `ValueError` and returns `None` to signal failure. "
 "Defensive little functions like these are what keep a 5-million-row pipeline from dying on row "
 "4,000,001."))

p.append(B.keypoints([
 "A ~function~ packages reusable logic; ~default arguments~ make parameters optional, and you can "
 "`return` multiple values as a tuple.",
 "Add a one-line ~docstring~ under `def` to document what a function does.",
 "Wrap risky code in ~try/except~ to handle errors gracefully; `finally` always runs.",
 "Catch **specific** exceptions, never a bare `except:` (which hides real bugs).",
 "A ~module~ is a `.py` file; `import` brings its code in &mdash; from the standard library or "
 "your own files.",
]))

p.append(B.quiz([
 {"q":"What does `def scale(x, factor=2): return x * factor` let you do?",
  "options":[
   {"t":"Call scale(5) to get 10 (using the default), or scale(5, 3) to get 15","correct":True,
    "why":"Correct. `factor=2` is a default argument, so `scale(5)` uses 2 (returns 10), while "
          "`scale(5, 3)` overrides it (returns 15)."},
   {"t":"Only call it as scale(5, 2); the default is required",
    "why":"The default makes `factor` optional &mdash; `scale(5)` works and uses 2. You can also "
          "override it."},
   {"t":"Nothing — defaults aren't valid Python",
    "why":"Default arguments are standard Python and very common. `scale(5)` returns 10."},
   {"t":"Return two values, x and factor",
    "why":"It returns a single value, `x * factor`. Returning two would be `return x, factor`."}]},
 {"q":"Why prefer `except ValueError:` over a bare `except:`?",
  "options":[
   {"t":"A bare except catches every error — including bugs and typos — hiding problems you need "
        "to see","correct":True,
    "why":"Correct. Catching only the expected exception lets genuine, unexpected errors surface "
          "instead of being silently swallowed, which would mask real bugs."},
   {"t":"A bare except is faster",
    "why":"Speed isn't the issue; correctness is. A bare except hides unrelated errors, making "
          "bugs invisible. Catch the specific exception you expect."},
   {"t":"Bare except isn't valid Python",
    "why":"It is valid, just bad practice &mdash; it catches everything, including errors you "
          "didn't anticipate."},
   {"t":"There's no difference",
    "why":"There's a big difference: a bare except masks all errors; a specific one handles only "
          "what you expect and lets real bugs through to be noticed."}]},
 {"q":"In `try / except / finally`, when does the `finally` block run?",
  "options":[
   {"t":"Always — whether or not an error occurred","correct":True,
    "why":"Correct. `finally` runs in every case (success or exception), which is why it's used "
          "for cleanup like closing a file or releasing a resource."},
   {"t":"Only when an error occurs",
    "why":"That describes `except`. `finally` runs regardless of whether an error happened."},
   {"t":"Only when no error occurs",
    "why":"That's closer to `else`. `finally` runs in all cases."},
   {"t":"Never; it's optional",
    "why":"It's optional to write, but when present it always runs &mdash; that's its purpose."}]},
]))

p.append(B.practice([
 {"q":"Write a function `clamp(x, low=0, high=100)` that returns `x` limited to the range "
      "[low, high]. What does `clamp(150)` return?", "html": True,
  "sol": B.code_example('def clamp(x, low=0, high=100):\n    """Limit x to the range [low, high]."""\n    return max(low, min(x, high))',
         filename="solution.py", runnable=False) + B.fmt(
         "`min(x, high)` caps the top, `max(low, ...)` lifts the bottom. With defaults low=0, "
         "high=100, `clamp(150)` returns **100**, and `clamp(-5)` returns 0.")},
 {"q":"You're reading user-entered ages from a form; some are blank or text. Sketch how you'd "
      "convert each to an int without crashing, defaulting bad values to None.", "html": True,
  "sol": B.code_example('def to_age(text):\n    try:\n        return int(text)\n    except (ValueError, TypeError):\n        return None',
         filename="solution.py", runnable=False) + B.fmt(
         "`int(text)` raises `ValueError` for non-numeric text and `TypeError` for `None`; catching "
         "both returns `None` for any unparseable entry, so the program continues. You'd then "
         "decide how to handle the Nones (drop, flag, or impute &mdash; Lesson 2.9).")},
]))

p.append(B.deepdive(
 B.concept(
  "**Pure functions and side effects.** A ~pure function~ depends only on its inputs and returns "
  "a value without changing anything outside itself (no modifying global variables, no printing, "
  "no writing files). Pure functions are easy to test, reuse, and reason about, because calling "
  "them can't surprise you. ~Side effects~ (I/O, mutation) are necessary somewhere, but isolating "
  "them &mdash; keeping most functions pure and pushing side effects to the edges &mdash; is a "
  "hallmark of clean, reliable code.") +
 B.concept(
  "**DRY and type hints.** ~DRY~ ('Don't Repeat Yourself') is the principle behind functions: "
  "when you copy-paste logic a third time, extract it into a function so a fix happens in one "
  "place. ~Type hints~ &mdash; `def avg(values: list[float]) -> float:` &mdash; document the "
  "expected input and output types. Python doesn't enforce them at runtime, but they make code "
  "self-explanatory and let editors and tools catch mistakes early. Both habits scale a "
  "notebook into a maintainable codebase.") +
 B.concept(
  "**Raise vs. handle.** Sometimes the right move isn't to *handle* an error but to *raise* one: "
  "`raise ValueError(\"age must be positive\")` stops bad data from flowing silently downstream. "
  "The rule of thumb: **handle** errors you can sensibly recover from (a bad row you can skip or "
  "default), and **raise** for conditions that mean your assumptions are broken and continuing "
  "would produce garbage. Failing loudly and early beats a wrong answer computed quietly."),
 title="Deep dive: pure functions, DRY & type hints, and raise vs. handle"))

p.append(B.callout("note","Interview-ready",
 "Coding screens reward clean, defensive functions: clear names, a docstring, sensible defaults, "
 "and handling of the empty/edge case. If asked to parse or transform messy input, wrap the "
 "risky part in a specific `try/except` and explain that you'd fail loudly (`raise`) when "
 "continuing would corrupt results. That judgment &mdash; recover vs. raise &mdash; signals "
 "real engineering maturity.", "&#9670;"))

LESSONS={"py-07-functions":"\n".join(p)}
