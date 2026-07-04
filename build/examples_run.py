# -*- coding: utf-8 -*-
"""
examples_run.py — the single source of truth for every runnable worked example.

Each example's code is stored as a string AND executed here at import time, with
stdout captured. Content modules import EX[key] = (code, output), so the code
shown to the learner is *exactly* the code that ran, and the output is real.
If any example raised, the whole build fails — which is the point.
"""
import io, contextlib, textwrap

EX = {}

def run(key, code):
    code = textwrap.dedent(code).strip("\n")
    g = {}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code + "\n", "<example %s>" % key, "exec"), g)
    EX[key] = (code, buf.getvalue().rstrip("\n"))
    return EX[key]

# ----------------------------------------------------------------- 1.1 ---- #
run("s11_ab", r'''
import pandas as pd

# QUESTION: does the redesigned checkout button lift the purchase rate?
# DATA: three days of visitors and purchases for each button variant.
visits = pd.DataFrame({
    "variant":   ["A", "A", "A", "B", "B", "B"],
    "visitors":  [4012, 4015, 4030, 3998, 4007, 4001],
    "purchases": [286,  291,  302,  327,  318,  333],
})

# CLEAN/AGGREGATE: total visitors & purchases per variant, then the rate.
summary = visits.groupby("variant")[["visitors", "purchases"]].sum()
summary["purchase_rate"] = summary["purchases"] / summary["visitors"]
print(summary)

a, b = summary.loc["A", "purchase_rate"], summary.loc["B", "purchase_rate"]
print(f"\nA = {a:.3%}   B = {b:.3%}   relative lift = {b/a - 1:.1%}")
print("But is that lift REAL, or could random luck produce it? -> statistics.")
''')

# ----------------------------------------------------------------- 1.2 ---- #
run("s12_types", r'''
import pandas as pd

customers = pd.DataFrame({
    "customer_id":      [1001, 1002, 1003, 1004, 1005],   # label, not a quantity
    "city":             ["Austin", "Austin", "Denver", "Reno", "Denver"],
    "plan":             ["Free", "Pro", "Pro", "Enterprise", "Free"],
    "satisfaction_1to5":[4, 5, 3, 5, 2],                  # ordered rating
    "logins_last_week": [3, 12, 7, 25, 1],                # a count
    "monthly_spend":    [0.0, 29.0, 29.0, 99.0, 0.0],     # a measured amount
})

# Pandas stores a *storage* type (dtype). It does NOT know the *variable* type.
print(customers.dtypes)

# Both columns are int64, but only one mean is meaningful:
print(f"\nmean monthly_spend = ${customers.monthly_spend.mean():.2f}   <- meaningful (continuous)")
print(f"mean customer_id   = {customers.customer_id.mean():.1f}    <- MEANINGLESS (it's a label)")
''')

# ----------------------------------------------------------------- 1.3 ---- #
run("s13_describe", r'''
import pandas as pd

# Annual salaries on a small team ($000s). Notice the founder's pay.
salary = pd.Series([52, 55, 58, 61, 49, 63, 57, 60, 240], name="salary_k")

print(f"count   = {salary.size}")
print(f"mean    = {salary.mean():.1f}")
print(f"median  = {salary.median():.1f}")
print(f"std dev = {salary.std():.1f}")
q1, q3 = salary.quantile([0.25, 0.75])
print(f"IQR     = {q3 - q1:.1f}   (Q1={q1:.0f}, Q3={q3:.0f})")

# Remove the single outlier and watch which number barely moves.
core = salary[salary < 200]
print(f"\nwithout the 240 outlier:  mean = {core.mean():.1f}   median = {core.median():.1f}")
print("The mean fell by ~20; the median barely flinched. That is robustness.")
''')

# ----------------------------------------------------------------- 1.4 ---- #
run("s14_bayes", r'''
# A test is 90% sensitive and has a 5% false-positive rate.
# The disease affects 1% of people. You test positive. Should you panic?
N            = 100_000
prevalence   = 0.01     # P(disease)
sensitivity  = 0.90     # P(test+ | disease)
false_pos    = 0.05     # P(test+ | healthy)

sick     = N * prevalence
healthy  = N - sick
true_pos = sick * sensitivity
fake_pos = healthy * false_pos

ppv = true_pos / (true_pos + fake_pos)     # P(disease | test+)
print(f"Per {N:,} people:")
print(f"  sick AND test-positive    : {true_pos:>7,.0f}")
print(f"  healthy AND test-positive : {fake_pos:>7,.0f}")
print(f"  ---------------------------------------")
print(f"  P(actually sick | positive) = {ppv:.1%}")
print("Most positives are false alarms -- because the disease is rare to begin with.")
''')

# ----------------------------------------------------------------- 1.5 ---- #
run("s15_dist", r'''
from scipy import stats

# NORMAL: adult heights, mean 170 cm, sd 7 cm.
heights = stats.norm(loc=170, scale=7)
print("Normal  N(mean=170, sd=7):")
print(f"  P(163 < height < 177) = {heights.cdf(177) - heights.cdf(163):.3f}   <- the '68%' band")
print(f"  P(height > 184 cm)    = {heights.sf(184):.3f}")

# BINOMIAL: send 10 emails, each opened independently with probability 0.2.
opens = stats.binom(n=10, p=0.2)
print("Binomial  n=10, p=0.2:")
print(f"  P(exactly 3 opened)   = {opens.pmf(3):.3f}")
print(f"  P(5 or more opened)   = {opens.sf(4):.3f}")

# POISSON: support tickets arrive at 3 per hour on average.
tickets = stats.poisson(mu=3)
print("Poisson  lambda=3 per hour:")
print(f"  P(a quiet hour: 0)    = {tickets.pmf(0):.3f}")
print(f"  P(swamped: 6 or more) = {tickets.sf(5):.3f}")
''')

if __name__ == "__main__":
    for k, (code, out) in EX.items():
        print("=" * 70)
        print("KEY:", k)
        print("-" * 70)
        print(out)
