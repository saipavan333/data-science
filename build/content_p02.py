# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "There's a mental shift that separates slow, clunky data code from fast, elegant code: stop "
 "thinking about *one number at a time* and start thinking about *whole arrays at once*. "
 "~NumPy~ is the library that makes this possible, and it's the engine beneath Pandas, "
 "scikit-learn, and nearly every numerical tool in Python. Learn to think in arrays and your "
 "code gets shorter, clearer, and &mdash; as you'll see &mdash; dozens of times faster."))

p.append(B.h2("The array and vectorization", kicker="Concept · the big idea"))
p.append(B.concept(
 "A NumPy ~array~ (ndarray) is a grid of numbers, all the same type, stored compactly. Its "
 "superpower is ~vectorization~: you write one operation on the *whole array* and NumPy applies "
 "it to every element in fast, compiled code. No `for` loop, no bookkeeping &mdash; "
 "`prices * 0.9` discounts an entire array at once.\n\n"
 "This isn't just prettier; it's dramatically faster, because the loop happens in optimized C "
 "instead of interpreted Python:"))
p.append(B.figure(IMG+"s_np_speed.png",
 "**Vectorized vs. looped, same result.** Doubling a million numbers: the Python loop crawls; the "
 "NumPy expression `arr*2+1` finishes in a blink. The gap only widens with bigger data.",
 "Bar chart comparing a Python loop to a vectorized NumPy operation."))

p.append(B.h2("Broadcasting", kicker="Concept · shapes that fit"))
p.append(B.concept(
 "What happens when shapes don't match &mdash; an array plus a single number, or a matrix plus a "
 "row? NumPy uses ~broadcasting~: it automatically 'stretches' the smaller shape to fit the "
 "larger one, without actually copying data. It's how you add a scalar to every cell, or subtract "
 "a per-column average from a whole table, in one line."))
p.append(B.figure(IMG+"s_np_broadcast.png",
 "**Broadcasting in action.** A scalar is applied to every cell; a row is reused for every row. "
 "This is what lets you normalize or scale entire datasets with a single expression.",
 "Diagram of a scalar and a row broadcasting across a matrix."))

p.append(B.h2("Indexing, slicing, and boolean masks", kicker="Concept · selecting data"))
p.append(B.concept(
 "You select parts of an array three ways: by **position** (`a[0]`, `a[2:5]`), and &mdash; the "
 "one that changes everything &mdash; by a ~boolean mask~. Writing `a > 20` produces an array of "
 "True/False, and `a[a > 20]` keeps only the elements where it's True. That single idea *is* "
 "filtering, and it carries straight into Pandas as the way you select rows."))
p.append(B.figure(IMG+"s_np_index.png",
 "**Slicing vs. masking.** Slicing grabs a contiguous range by position; a boolean mask keeps "
 "elements that pass a test. Masking is how you'll filter data for the rest of your career.",
 "An array with a slice highlighted and a boolean mask highlighted."))

p.append(B.h2("Array thinking in code", kicker="Worked example"))
p.append(B.concept(
 "Watch a few lines replace the whole pure-Python block from last lesson &mdash; discount every "
 "order, filter the big ones with a mask, and aggregate, all without a single loop."))
_c,_o=_run(r'''
import numpy as np

amounts = np.array([180., 45., 220., 30., 95., 60.])

# Vectorized: 10% off every order at once — no loop.
discounted = amounts * 0.9
print("discounted:", np.round(discounted, 1))

# Boolean mask: keep only orders over $100.
big = amounts[amounts > 100]
print("orders over $100:", big, "| count:", big.size)

# Aggregations run over the whole array.
print(f"total ${amounts.sum():.0f} | mean ${amounts.mean():.1f} | max ${amounts.max():.0f}")
''')
p.append(B.code_example(_c,_o,filename="numpy_arrays.py"))
p.append(B.concept(
 "Every line operates on the array as a whole: no indices, no loops, no off-by-one risk. This "
 "array-first mindset is exactly what Pandas builds on &mdash; a DataFrame column *is* a NumPy "
 "array with a label, so everything here transfers directly to the next lesson."))

PLAB_SETUP = (
 "import numpy as np\n"
 "arr = np.array([12, 45, 7, 88, 33, 61, 5, 99, 21, 74])\n")
p.append(B.h2("Your turn — think in arrays", kicker="Interactive lab"))
p.append(B.pylab(
 "`arr` is a NumPy array of 10 numbers. Using a **boolean mask** (no loop), assign to **`answer`** "
 "the **average of only the values greater than 50**, rounded to 2 decimals.",
 PLAB_SETUP,
 "answer = round(float(arr[arr > 50].mean()), 2)",
 starter="# arr = np.array([12, 45, 7, 88, 33, 61, 5, 99, 21, 74])\nanswer = ",
 hint="`arr[arr > 50]` keeps the big values; take `.mean()`, wrap in `round(float(...), 2)`.",
 title="Lab — boolean mask + aggregate",
 preview="`arr` &rarr; a 10-element NumPy array, already loaded.",
 explain="The mask `arr > 50` selects the qualifying elements; `.mean()` averages just those."))

p.append(B.keypoints([
 "A NumPy ~array~ holds same-type numbers compactly; ~vectorization~ applies one operation to "
 "every element in fast compiled code.",
 "Vectorized code is **far faster** than Python loops (often 10&ndash;100&times;) and shorter.",
 "~Broadcasting~ stretches smaller shapes (a scalar, a row) to fit larger ones &mdash; no loops, "
 "no copies.",
 "A ~boolean mask~ (`a[a > 20]`) keeps elements that pass a test &mdash; this *is* filtering, and "
 "it carries into Pandas.",
 "Aggregations (`.sum()`, `.mean()`, `.max()`) run over the whole array (or along an `axis`).",
]))

p.append(B.quiz([
 {"q":"Given `a = np.array([5, 12, 3, 20, 8])`, what does `a[a >= 10]` return?",
  "options":[
   {"t":"array([12, 20]) — the elements where the mask is True","correct":True,
    "why":"Correct. `a >= 10` is [F, T, F, T, F]; indexing with that boolean mask keeps the "
          "elements at the True positions: 12 and 20."},
   {"t":"array([True, False, True, True, False]) — the mask itself",
    "why":"That's just `a >= 10`. Wrapping it as `a[...]` *applies* the mask, returning the "
          "elements (12, 20), not the booleans."},
   {"t":"array([5, 3, 8]) — the elements below 10",
    "why":"The mask `>= 10` keeps elements that are at least 10, not below it. Those are 12 and "
          "20."},
   {"t":"An error — you can't index with booleans",
    "why":"Boolean-mask indexing is a core NumPy feature; `a[a >= 10]` is valid and returns the "
          "passing elements."}]},
 {"q":"Why is `arr * 2` (NumPy) typically far faster than `[x*2 for x in arr]` (Python list) for a "
      "large array?",
  "options":[
   {"t":"NumPy runs the loop in optimized compiled C over compact memory, avoiding Python's "
        "per-element overhead","correct":True,
    "why":"Correct. Vectorized operations execute in fast compiled code on contiguous, same-type "
          "memory, sidestepping the interpreter overhead Python pays on every element."},
   {"t":"NumPy skips most of the elements to save time",
    "why":"No &mdash; it processes every element, just far more efficiently. It doesn't drop any "
          "data."},
   {"t":"Python lists are stored on disk while arrays are in memory",
    "why":"Both live in memory. The speed difference is compiled vectorized execution and compact "
          "storage, not disk vs memory."},
   {"t":"`arr * 2` only works on small arrays",
    "why":"It works on arrays of any size, and its advantage grows with size."}]},
 {"q":"You have a 2D array `M` (rows = customers, columns = months) and a 1D array `avg` of length "
      "= number of columns. What does `M - avg` do?",
  "options":[
   {"t":"Broadcasts avg across every row, subtracting each column's value from that column","correct":True,
    "why":"Correct. Broadcasting matches the 1D `avg` to each row of `M`, subtracting the "
          "per-column averages from every customer &mdash; a one-line normalization."},
   {"t":"Raises a shape error because the dimensions differ",
    "why":"Broadcasting is designed exactly for this: a (rows×cols) array minus a (cols,) array "
          "aligns on the columns, so it works without error."},
   {"t":"Subtracts avg only from the first row",
    "why":"Broadcasting applies avg to *every* row, not just the first."},
   {"t":"Subtracts the single number avg from every cell",
    "why":"`avg` is a row of values (one per column), not a scalar, so each column gets its own "
          "value subtracted, not one number everywhere."}]},
]))

p.append(B.practice([
 {"q":"In one vectorized line each: (a) add 5% tax to an array `prices`; (b) count how many "
      "values in `scores` are below 50.",
  "sol":"(a) `prices * 1.05` &mdash; broadcasting multiplies every price at once. (b) "
        "`(scores < 50).sum()` &mdash; the comparison makes a boolean array (True=1, False=0), and "
        "summing it counts the Trues. Both avoid explicit loops."},
 {"q":"Explain what `arr[arr > arr.mean()]` returns, step by step.",
  "sol":"Step 1: `arr.mean()` computes the average of the array. Step 2: `arr > arr.mean()` "
        "produces a boolean mask that's True wherever an element exceeds the average. Step 3: "
        "`arr[...]` applies that mask, returning **only the above-average elements**. It's a "
        "one-line 'keep the values bigger than the mean.'"},
]))

p.append(B.deepdive(
 B.concept(
  "**Why vectorization is fast.** A Python list can hold mixed types, so each element is a "
  "full Python object scattered in memory, and a loop pays interpreter overhead on every step. A "
  "NumPy array stores raw numbers of one type in a single contiguous block, so operations run as "
  "a tight compiled loop over cache-friendly memory &mdash; often 10&ndash;100&times; faster, and "
  "the foundation of all high-performance numerical Python.") +
 B.concept(
  "**The `axis` argument.** On a 2D array, aggregations take a direction: `M.sum(axis=0)` sums "
  "**down** the columns (one total per column), `M.sum(axis=1)` sums **across** the rows (one "
  "total per row), and no axis sums everything. The mnemonic: `axis` names the dimension that "
  "*disappears*. This same `axis` idea reappears throughout Pandas.") +
 B.concept(
  "**Views vs. copies.** Slicing an array usually returns a ~view~ &mdash; a window onto the same "
  "memory &mdash; so modifying the slice changes the original. Boolean-mask indexing returns a "
  "~copy~. When you need to be sure you're not mutating the source, call `.copy()` explicitly. "
  "This is the array-level version of the reference trap from the Python lesson."),
 title="Deep dive: why arrays are fast, the axis argument, and views vs. copies"))

p.append(B.callout("note","Interview-ready",
 "Expect *\"why use NumPy over plain Python lists?\"* &mdash; answer with vectorization "
 "(whole-array operations in compiled code), speed, and broadcasting, plus that it's the "
 "foundation under Pandas and ML libraries. Being able to filter with a boolean mask and explain "
 "`axis=0` vs `axis=1` quickly marks you as comfortable with real data code.", "&#9670;"))

LESSONS={"py-02-numpy":"\n".join(p)}
