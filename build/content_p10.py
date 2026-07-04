# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Lesson 2.5 taught you to *think in arrays*. This lesson adds the array tools you'll actually "
 "reach for every week: aggregating along a chosen direction, generating random data for "
 "simulations (the engine behind every Track 1 demo), and reshaping and transforming arrays. "
 "These are the moves behind Pandas, scikit-learn, and the statistics you've already learned "
 "&mdash; so they pay off everywhere."))

p.append(B.h2("Aggregating along an axis", kicker="Concept · the one that confuses everyone"))
p.append(B.concept(
 "A 2-D array has two directions, and aggregations like `.sum()` and `.mean()` take an `axis` "
 "argument to say *which way to collapse*. The mnemonic that finally makes it stick: **axis is "
 "the dimension that disappears.** `M.sum(axis=0)` collapses the rows, leaving one value per "
 "**column** (a column total). `M.sum(axis=1)` collapses the columns, leaving one value per "
 "**row**. With no axis, it collapses everything to a single number."))
p.append(B.figure(IMG+"s_np_axis.png",
 "**axis=0 vs axis=1.** axis=0 runs *down* the rows to give per-column results; axis=1 runs "
 "*across* the columns to give per-row results. The named axis is the one that vanishes from the "
 "output shape.",
 "A 2D grid with axis=0 producing column sums and axis=1 producing row sums."))

p.append(B.h2("Random numbers (done right)", kicker="Concept · simulation fuel"))
p.append(B.concept(
 "Random data drives simulations, sampling, shuffling, and the resampling behind the bootstrap "
 "(Lesson 1.8). The modern way is a ~generator~: `rng = np.random.default_rng(seed)`, then draw "
 "from it &mdash; `rng.normal(mean, sd, size)`, `rng.uniform(...)`, `rng.integers(low, high, "
 "size)`, `rng.choice(options, size)`. Passing a ~seed~ makes the 'random' numbers **reproducible**"
 ": the same seed gives the same sequence every run, which is essential for results others can "
 "verify (and why every example in this course seeds its generator)."))

p.append(B.h2("Reshaping and handy functions", kicker="Concept"))
p.append(B.concept(
 "A few more array tools you'll use constantly:\n\n"
 "- ~reshape~ rearranges the same data into a new shape: `a.reshape(3, 4)` (use `-1` to let NumPy "
 "infer a dimension).\n"
 "- ~where~ is a vectorized if/else: `np.where(a > 0, \"pos\", \"neg\")`.\n"
 "- ~clip~ caps values to a range: `np.clip(a, 0, 100)` (winsorizing, Lesson 3.7).\n"
 "- `np.unique`, `np.concatenate`, `np.argmax`/`np.argsort` round out the toolkit."))

p.append(B.h2("Arrays in anger", kicker="Worked example"))
p.append(B.concept(
 "Generate reproducible random data, aggregate it by axis, and transform it with `where` and "
 "`clip` &mdash; the array operations behind real analysis code."))
_c,_o=_run(r'''
import numpy as np
rng = np.random.default_rng(0)              # seeded -> reproducible

M = rng.integers(0, 10, size=(3, 4))        # a 3x4 array of random ints 0-9
print(M)
print("column means (axis=0):", M.mean(axis=0).round(1))   # one per column
print("row sums    (axis=1):", M.sum(axis=1))              # one per row
print("grand total (no axis):", M.sum())

# Vectorized transforms — no loops
print("flag >=5    :\n", np.where(M >= 5, 1, 0))            # if/else over the array
print("clipped 2..7:\n", np.clip(M, 2, 7))                 # cap values into a range
''')
p.append(B.code_example(_c,_o,filename="numpy_deeper.py"))
p.append(B.concept(
 "Every line operates on the whole array: aggregations choose a direction with `axis`, and "
 "`where`/`clip` transform element-wise without a single loop. This is the array fluency that "
 "makes Pandas (a labeled layer over NumPy) feel natural &mdash; `df.mean(axis=0)` is this exact "
 "idea on a DataFrame."))

p.append(B.keypoints([
 "`axis` is **the dimension that disappears**: `axis=0` &rarr; per-**column** result, `axis=1` "
 "&rarr; per-**row** result, no axis &rarr; one number.",
 "Generate randomness with `rng = np.random.default_rng(seed)`; a **seed** makes results "
 "**reproducible**.",
 "Draw with `rng.normal/uniform/integers/choice`; this fuels simulation, sampling, and the "
 "bootstrap.",
 "~reshape~ rearranges data (use `-1` to infer a dim); ~where~ is vectorized if/else; ~clip~ "
 "caps to a range.",
 "These NumPy operations are exactly what Pandas runs under the hood &mdash; the same `axis` idea "
 "applies to DataFrames.",
]))

p.append(B.quiz([
 {"q":"For a 2-D array `M` of shape (rows=5, cols=3), what does `M.sum(axis=0)` return?",
  "options":[
   {"t":"An array of 3 values — one total per column (the rows are collapsed)","correct":True,
    "why":"Correct. axis=0 is the dimension that disappears (the rows), so you sum down each "
          "column, leaving one value per column &mdash; shape (3,)."},
   {"t":"An array of 5 values — one per row",
    "why":"That's axis=1 (collapsing columns). axis=0 collapses rows, giving one value per "
          "column (3 values)."},
   {"t":"A single number (the grand total)",
    "why":"That's `M.sum()` with no axis. Specifying axis=0 keeps the column dimension, giving 3 "
          "totals."},
   {"t":"The array unchanged, shape (5, 3)",
    "why":"Aggregating reduces a dimension. axis=0 removes the rows, returning shape (3,)."}]},
 {"q":"Why pass a seed to `np.random.default_rng(seed)`?",
  "options":[
   {"t":"To make the random sequence reproducible — the same seed gives the same numbers every "
        "run","correct":True,
    "why":"Correct. A fixed seed makes 'random' results repeatable, so others can verify your "
          "analysis and your simulations are deterministic. It's standard practice."},
   {"t":"To make the numbers more random",
    "why":"A seed doesn't increase randomness; it fixes the sequence so it's reproducible. The "
          "numbers are equally 'random' but repeatable."},
   {"t":"To make the code run faster",
    "why":"Seeding is about reproducibility, not speed."},
   {"t":"It's required or the generator won't work",
    "why":"A seed is optional &mdash; without one you get a different sequence each run. You add "
          "it specifically for reproducibility."}]},
 {"q":"What does `np.where(scores >= 60, \"pass\", \"fail\")` produce?",
  "options":[
   {"t":"An array the same shape as scores, with 'pass' where the score is >= 60 and 'fail' "
        "elsewhere","correct":True,
    "why":"Correct. `np.where(condition, a, b)` is a vectorized if/else: it picks `a` where the "
          "condition is True and `b` where it's False, element by element."},
   {"t":"A single True or False",
    "why":"`np.where` with three arguments returns a full array of choices, not one boolean. The "
          "condition alone (`scores >= 60`) would be the boolean array."},
   {"t":"Only the passing scores",
    "why":"It doesn't filter; it returns a value for *every* element ('pass' or 'fail'). Filtering "
          "would be `scores[scores >= 60]`."},
   {"t":"An error",
    "why":"It's valid and common &mdash; the vectorized if/else returns 'pass'/'fail' per "
          "element."}]},
]))

p.append(B.practice([
 {"q":"You have a 2-D array `sales` with shape (stores=4, months=12). Write expressions for "
      "(a) each store's yearly total and (b) the average across stores for each month.", "html": True,
  "sol": B.code_example('store_totals  = sales.sum(axis=1)    # collapse months -> one per store (4 values)\nmonth_avgs    = sales.mean(axis=0)   # collapse stores -> one per month (12 values)',
         filename="solution.py", runnable=False) + B.fmt(
         "Per **store** total sums across the 12 months, so collapse axis=1 (months disappear). "
         "Per **month** average collapses the 4 stores, so axis=0 (stores disappear). Remember: "
         "the named axis is the one that vanishes.")},
 {"q":"Write one line to draw 1,000 reproducible samples from a normal distribution with mean 50, "
      "SD 8.", "html": True,
  "sol": B.code_example('rng = np.random.default_rng(42)\nsample = rng.normal(50, 8, size=1000)',
         filename="solution.py", runnable=False) + B.fmt(
         "Create a seeded generator (so the draw is reproducible), then `rng.normal(mean, sd, "
         "size)` gives 1,000 values centered at 50 with spread 8 &mdash; exactly the kind of "
         "synthetic data the Track 1 simulations used to demonstrate the CLT and sampling.")},
]))

p.append(B.deepdive(
 B.concept(
  "**Broadcasting, revisited.** The axis idea and broadcasting (Lesson 2.5) team up constantly. "
  "To standardize a table column-by-column &mdash; subtract each column's mean and divide by its "
  "SD &mdash; you write `(M - M.mean(axis=0)) / M.std(axis=0)` in one line: the per-column "
  "statistics (shape `(cols,)`) broadcast across every row. This single expression is the "
  "~z-score standardization~ that scikit-learn's `StandardScaler` performs, and a preview of "
  "feature scaling in Track 6.") +
 B.concept(
  "**Views vs. copies, and why reshape is cheap.** `reshape` usually returns a ~view~ &mdash; the "
  "same data seen with a different shape, no copying &mdash; which is why it's nearly free even "
  "on huge arrays. Slicing is also a view, so modifying a slice can change the original (the "
  "array version of the reference trap from Lesson 2.1). When you need an independent array, call "
  "`.copy()`. Understanding views explains both NumPy's speed and its occasional 'why did my "
  "original change?' surprises.") +
 B.concept(
  "**The legacy random API.** You'll see older code using `np.random.seed(0)` and "
  "`np.random.rand(...)` (the global, legacy interface). It still works, but the modern "
  "`default_rng()` generator is preferred: it's faster, has better statistical properties, and "
  "avoids the hidden-global-state bugs of the old API. Recognize the old style in tutorials, but "
  "write the new one."),
 title="Deep dive: standardization via broadcasting, views vs. copies, and the modern RNG"))

p.append(B.callout("note","Interview-ready",
 "The classic NumPy interview check is `axis=0` vs `axis=1` &mdash; answer with the 'dimension "
 "that disappears' rule and a concrete example (column means are axis=0). Mentioning seeded "
 "generators for reproducibility, and that Pandas runs NumPy underneath (so the same axis logic "
 "applies to DataFrames), shows you understand the foundation, not just the surface.", "&#9670;"))

LESSONS={"py-10-numpy2":"\n".join(p)}
