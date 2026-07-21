# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
p=[]
p.append(B.why(
 "Models speak **numbers**, but data is full of **categories**: country, plan type, device, product "
 "ID. You can't feed the word \"California\" into a regression &mdash; you must encode it. Do it "
 "naively and you either invent a fake ordering the model believes, or explode a million-category "
 "column into a million useless columns. Encoding categoricals well &mdash; and without leaking "
 "&mdash; is one of the most consequential choices in a tabular pipeline."))
p.append(B.h2("Nominal vs. ordinal — the first fork", kicker="Is there a real order?"))
p.append(B.concept(
 "Before encoding, ask: do the categories have a **meaningful order**?\n\n"
 "- **Ordinal** (ordered): `low < medium < high`, `bronze < silver < gold`. Map to ordered integers "
 "(0, 1, 2) &mdash; the order carries real information the model can use.\n"
 "- **Nominal** (unordered): `red, green, blue`; `NY, SF, LA`. There's **no** order, so mapping to "
 "1, 2, 3 is a *lie* &mdash; the model would infer that `blue (3) > red (1)` and that green sits "
 "exactly between, which is nonsense."))
p.append(B.pitfall(
 "The classic beginner bug: **label-encoding a nominal feature** (`NY&rarr;0, SF&rarr;1, LA&rarr;2`) "
 "and feeding it to a linear or distance model. You've secretly told the model LA is \"twice\" SF "
 "and that these cities lie on a line &mdash; a fake ordering it will dutifully exploit. For "
 "unordered categories, use **one-hot encoding** instead."))
p.append(B.h2("One-hot encoding — the workhorse for nominal", kicker="One column per category"))
p.append(B.concept(
 "**One-hot encoding** turns one categorical column into several **binary** columns, one per "
 "category, with a single 1 marking the active value. No fake order is implied &mdash; each category "
 "is its own independent indicator:"))
_c,_o=_run(r'''
import pandas as pd
df = pd.DataFrame({"city": ["NY", "SF", "NY", "LA"],
                   "plan": ["free", "pro", "pro", "free"]})
enc = pd.get_dummies(df, columns=["city", "plan"]).astype(int)
print(enc.to_string(index=False))
''')
p.append(B.code_example(_c,_o,filename="one_hot.py"))
p.append(B.concept(
 "Each original column became one indicator per category. `city` (3 values) &rarr; 3 columns; `plan` "
 "(2 values) &rarr; 2 columns. A model can now weight each category independently, with no invented "
 "ordering. (Statisticians often **drop one** column per feature &mdash; the *dummy trap* &mdash; "
 "since it's implied by the others; for most ML models it's optional, but it matters for linear "
 "models with an intercept.)"))
p.append(B.h2("When one-hot explodes: high cardinality", kicker="Thousands of categories"))
p.append(B.concept(
 "One-hot is perfect for a handful of categories. But `zip_code` (40,000 values) or `product_id` "
 "(millions) would create tens of thousands of mostly-zero columns &mdash; slow, memory-hungry, and "
 "prone to overfitting. For **high-cardinality** features, reach for:\n\n"
 "- **Frequency encoding**: replace each category with how often it appears. Cheap, one column, "
 "often surprisingly effective.\n"
 "- **Target (mean) encoding**: replace each category with the *average target* for that category "
 "(e.g. the mean conversion rate for each city). Compact and powerful &mdash; but **dangerous**: it "
 "looks at the label.\n"
 "- **Hashing**: hash categories into a fixed number of buckets &mdash; bounded width, at the cost "
 "of occasional collisions."))
p.append(B.warn(
 "**Target encoding leaks if you're not careful.** Because it uses the target, computing a category's "
 "mean over *all* rows (including the one you're predicting) hands the model the answer &mdash; "
 "test-set performance looks brilliant and collapses in production. It must be computed with "
 "**cross-fold / out-of-fold** schemes (each row encoded using *other* rows' targets) and fit on "
 "**train only**. When in doubt, prefer one-hot or frequency encoding; use target encoding only with "
 "leakage-safe machinery."))
p.append(B.h2("Your turn — count the encoded columns", kicker="Interactive lab"))
p.append(B.pylab(
 "One-hot encode both categorical columns of `df` with `pd.get_dummies(df, columns=[\"city\", "
 "\"plan\"])` and assign the **number of resulting columns** to **`answer`** (an int). Think first: "
 "how many distinct cities, how many plans?",
 "import pandas as pd\n"
 "df = pd.DataFrame({\n"
 "    \"city\": [\"NY\", \"SF\", \"NY\", \"LA\", \"SF\", \"LA\", \"NY\"],\n"
 "    \"plan\": [\"free\", \"pro\", \"pro\", \"free\", \"free\", \"pro\", \"pro\"],\n"
 "})\n",
 "enc = pd.get_dummies(df, columns=[\"city\", \"plan\"])\n"
 "answer = int(enc.shape[1])",
 starter="import pandas as pd\n# one-hot encode city and plan; how many columns result?\nanswer = ",
 hint="`pd.get_dummies(df, columns=[...])` makes one column per distinct value. `.shape[1]` is the "
      "column count. 3 cities + 2 plans = ?",
 title="Lab — one-hot column count",
 preview="pandas loaded; df has `city` (3 values) and `plan` (2 values). First Run boots Python + pandas.",
 explain="3 cities + 2 plans = **5** columns. One-hot trades one categorical column for one binary "
         "column per category &mdash; fine for a few categories, but you can see how `zip_code` would "
         "explode into tens of thousands, which is why high-cardinality features need frequency or "
         "target encoding instead."))
p.append(B.keypoints([
 "Ask first: **ordinal** (has order &rarr; ordered integers) or **nominal** (no order &rarr; "
 "**one-hot**).",
 "**Label-encoding a nominal feature invents a fake ordering** &mdash; a classic bug for linear/"
 "distance models.",
 "**One-hot** makes one binary column per category (no fake order); great for **low** cardinality.",
 "**High-cardinality** (zip, product_id) &rarr; **frequency**, **target/mean**, or **hashing** "
 "encoding instead of one-hot.",
 "**Target encoding uses the label &mdash; it leaks** unless done out-of-fold and fit on train only.",
]))
p.append(B.quiz([
 {"q":"You encode `color` (red, green, blue) as red=0, green=1, blue=2 and feed it to a linear "
      "model. What have you done wrong?",
  "options":[
   {"t":"Invented a false ordering — the model now treats blue as '>' green '>' red and green as "
        "midway between, which is meaningless","correct":True,
    "why":"Correct. Colour is nominal (no order), so integer codes impose a fake ranking and spacing "
          "the linear model will exploit. Use one-hot encoding so each colour is an independent "
          "indicator."},
   {"t":"Nothing — integers are how models read categories",
    "why":"For *ordered* categories, yes; for unordered ones like colour, integer codes fabricate an "
          "order that doesn't exist."},
   {"t":"You should have used more integers",
    "why":"The count isn't the issue; imposing *any* numeric order on unordered categories is the "
          "error."},
   {"t":"Linear models can't use categorical data at all",
    "why":"They can &mdash; via one-hot encoding. The bug is the fake ordinal encoding, not "
          "categoricals per se."}]},
 {"q":"A `merchant_id` column has 80,000 distinct values. Why is one-hot a poor choice, and what's "
      "better?",
  "options":[
   {"t":"One-hot would create 80,000 sparse columns (slow, memory-heavy, overfit-prone); frequency or "
        "target encoding is more compact","correct":True,
    "why":"Correct. High cardinality makes one-hot explode into tens of thousands of mostly-zero "
          "columns. Frequency encoding (one column) or leakage-safe target encoding keeps it compact "
          "and often more predictive."},
   {"t":"One-hot can't encode IDs",
    "why":"It technically can &mdash; the problem is that 80,000 categories produce an unwieldy, "
          "overfit-prone matrix, so you choose a compact encoding instead."},
   {"t":"You should label-encode the IDs 0-79,999",
    "why":"That invents a meaningless order over IDs. Prefer frequency/target/hashing encodings for "
          "high cardinality."},
   {"t":"Drop the column — IDs are never useful",
    "why":"IDs can carry real signal (some merchants convert more); the fix is a compact encoding, "
          "not discarding it."}]},
]))
p.append(B.practice([
 {"q":"For each feature, name a sensible encoding: (a) `t_shirt_size` (S/M/L/XL), (b) `country` (~200 "
      "values), (c) `browser` (5 values), (d) `zip_code` (40,000 values).",
  "sol":"**(a) t_shirt_size** &mdash; **ordinal**: map S&lt;M&lt;L&lt;XL to 0,1,2,3; the order is "
        "real and useful. **(b) country** (~200) &mdash; borderline: one-hot is workable but wide; "
        "**frequency or target encoding** (leakage-safe) is often better, or group rare countries "
        "into an \"other\" bucket. **(c) browser** (5) &mdash; **one-hot**: low cardinality, "
        "unordered. **(d) zip_code** (40,000) &mdash; **high cardinality**: frequency or out-of-fold "
        "target encoding, or hashing; never one-hot (40k columns) and never a fake integer order. "
        "The through-line: ordered &rarr; ordinal ints; few unordered &rarr; one-hot; many unordered "
        "&rarr; compact encodings."},
 {"q":"Explain why target encoding can give amazing validation scores that vanish in production, and "
      "how to do it safely.",
  "sol":"Target encoding replaces each category with the mean of the **target** for that category. If "
        "you compute that mean over **all** rows &mdash; including the row you're about to predict "
        "&mdash; the feature literally contains information about that row's own label, so the model "
        "'cheats' and validation looks spectacular. In production (and on truly unseen data) that "
        "leak is gone and performance craters. **Safe version:** compute each row's encoding using "
        "**only other rows' targets** &mdash; an out-of-fold / cross-fold scheme &mdash; fit the "
        "encodings on **train only**, and add **smoothing** so rare categories fall back toward the "
        "global mean rather than trusting one or two examples. Wrapping it in a pipeline that respects "
        "the train/test boundary is what keeps it honest."},
]))
p.append(B.deepdive(
 B.concept(
  "**Why smoothing matters for target encoding.** A category seen **twice**, both of which happened "
  "to convert, gets a target-encoded value of 1.0 &mdash; a wild over-estimate from two data points. "
  "**Smoothing** shrinks each category's mean toward the global mean, weighted by how many examples "
  "it has: rare categories lean on the prior, common ones trust their own data. This tames the "
  "variance that makes naive target encoding overfit, and combined with out-of-fold computation it's "
  "what makes the technique safe and strong on high-cardinality features.") +
 B.concept(
  "**One-hot's hidden interactions with your model.** One-hot works beautifully for linear models "
  "(each category gets its own coefficient) but can *hurt* tree-based models on high cardinality: a "
  "tree splitting on a single sparse one-hot column isolates one category at a time, so it struggles "
  "to group categories and wastes depth &mdash; which is exactly why libraries like **LightGBM and "
  "CatBoost added native categorical handling** (CatBoost's whole selling point is built-in, "
  "leakage-safe ordered target encoding). So the 'best' encoding is partly a function of the model: "
  "one-hot for linear and low-cardinality; native handling or compact encodings for trees on "
  "high-cardinality features."),
 title="Deep dive: smoothing, out-of-fold target encoding, and encoding × model interactions"))
LESSONS={"fe-03-categorical":"\n".join(p)}
print("content_fe03 OK — chars:", len(LESSONS["fe-03-categorical"]))
