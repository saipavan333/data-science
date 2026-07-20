# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.concept(
 "The whole Foundations track on one page: Python the language, then NumPy and pandas &mdash; the "
 "three tools you'll touch every single day. Keep it open while you code; press **Print** for a "
 "desk copy."))
p.append(B.cheatsheet(
 "Python, NumPy & pandas — one-page reference",
 "Everything here runs in the lessons' **Run** buttons. Read a row, picture the code, and you're "
 "fluent.",
 [
  ("Variables & types", [
    ("x = 5", "assign; no type declared"),
    ("int, float, str, bool", "whole, decimal, text, True/False"),
    ("None", "\"nothing here\" (like SQL NULL)"),
    ("f\"total: {x}\"", "f-string: drop values into text"),
    ("type(x), len(s)", "the type / the length"),
  ]),
  ("Collections", [
    ("[1, 2, 3]", "**list** &mdash; ordered, editable"),
    ("{\"a\": 1}", "**dict** &mdash; look up by key"),
    ("(1, 2)", "tuple &mdash; fixed"),
    ("x[0], x[-1]", "first / last item"),
    ("x[1:3]", "slice (stop excluded)"),
    ("k in d", "membership test"),
  ]),
  ("Control flow", [
    ("if c: … elif …: … else:", "branch"),
    ("for x in seq:", "loop over items"),
    ("range(n)", "0 … n-1"),
    ("while cond:", "loop until false"),
    ("[f(x) for x in seq]", "list comprehension"),
  ]),
  ("Functions", [
    ("def f(a, b=1):", "define; `b` has a default"),
    ("return value", "send a result back"),
    ("lambda x: x*2", "tiny anonymous function"),
    ("try: … except E:", "handle errors gracefully"),
  ]),
  ("Strings", [
    (".strip()", "trim surrounding spaces"),
    (".lower() / .upper()", "change case"),
    (".split(\",\")", "text &rarr; list of parts"),
    (".replace(a, b)", "swap substrings"),
    ("s.str.…", "apply to a whole pandas column"),
  ]),
  ("NumPy (arrays)", [
    ("np.array([1,2,3])", "make an array"),
    ("arr.mean() / .sum() / .std()", "vectorized aggregates"),
    ("arr * 2 + 1", "operate on all elements at once"),
    ("arr[arr > 0]", "boolean mask &mdash; keep matches"),
    ("arr.reshape(2, 3)", "change shape"),
    ("axis=0 / axis=1", "down columns / across rows"),
  ]),
  ("pandas — select", [
    ("pd.read_csv(\"f.csv\")", "load a file into a DataFrame"),
    ("df.head(), df.shape, df.info()", "peek, size, types"),
    ("df[\"col\"]", "one column (a Series)"),
    ("df[df.x > 0]", "filter rows by a condition"),
    ("df.loc[r, \"col\"]", "select by label"),
    ("df.iloc[0]", "select by position"),
  ]),
  ("pandas — transform", [
    ("df.groupby(\"c\")[\"x\"].mean()", "split-apply-combine"),
    ("df.merge(other, on=\"id\")", "join two DataFrames"),
    ("df.sort_values(\"x\", ascending=False)", "sort"),
    ("df.dropna() / df.fillna(0)", "handle missing values"),
    ("df.pivot_table(...)", "reshape long &rarr; wide"),
    ("df.assign(y = df.x * 2)", "add a computed column"),
  ]),
 ]))
LESSONS={"py-12-cheatsheet":"\n".join(p)}
print("content_pycheat OK — chars:", len(LESSONS["py-12-cheatsheet"]))
