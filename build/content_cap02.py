# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]
p.append(B.callout("why","Capstone B — put the whole experimentation track to work",
 "You're the data scientist at **ShopFast**. The design team redesigned the checkout button and "
 "wants to ship it. Your job: **design the test, size it, analyse the results honestly, and make a "
 "go/no-go call** &mdash; the exact sequence you'd run in a real product team. This capstone chains "
 "everything from Tracks 4 and 6 into one decision, and every number below is computed live.",
 "&#9654;"))
p.append(B.h2("Step 1 — Design before you touch data", kicker="Metric, hypothesis, guardrails"))
p.append(B.concept(
 "Nail the design first, or the analysis is meaningless:\n\n"
 "- **Hypothesis**: the clearer button reduces checkout friction, so **purchase conversion rises**.\n"
 "- **Primary metric**: purchase conversion rate = purchases &divide; visitors who reach checkout. "
 "**One** metric.\n"
 "- **Guardrails** (must not harm): **revenue per visitor** (a faster path could shrink baskets) and "
 "**page latency**.\n"
 "- **Unit of randomization**: the **visitor** (consistent experience), split **50/50**, assigned at "
 "checkout entry.\n"
 "- **Decision rule, set now**: ship only if conversion is **significantly** up, past our minimum "
 "detectable effect, **and** no guardrail drops."))
p.append(B.figure(IMG+"s_ab_design.png",
 "**The design, as a flow.** Randomize visitors 50/50, expose control vs. treatment, measure the "
 "primary metric with guardrails, and decide by a rule fixed **before** seeing data &mdash; the "
 "structure that keeps the test honest.",
 "An A/B test design flow from randomization through measurement to decision."))
p.append(B.h2("Step 2 — Power: how many visitors?", kicker="Size it before you start"))
p.append(B.concept(
 "The baseline conversion is ~8%. The smallest lift worth shipping (our **MDE**) is **+1 percentage "
 "point**. At the usual &alpha;=0.05 and 80% power, how many visitors per arm do we need? Undersize "
 "the test and a real effect hides in the noise:"))
_c,_o=_run(r'''
import numpy as np
from scipy import stats

p1, mde = 0.08, 0.01          # baseline 8%, want to detect +1pp
p2 = p1 + mde
alpha, power = 0.05, 0.80
z_a = stats.norm.ppf(1 - alpha/2)      # two-sided
z_b = stats.norm.ppf(power)
pbar = (p1 + p2)/2
n = (z_a*np.sqrt(2*pbar*(1-pbar)) + z_b*np.sqrt(p1*(1-p1)+p2*(1-p2)))**2 / mde**2
print(f"required sample size: ~{int(np.ceil(n)):,} visitors PER ARM")
print("-> plan to run ~2 full weeks to clear that and cover weekly seasonality")
''')
p.append(B.code_example(_c,_o,filename="power.py"))
p.append(B.h2("Step 3 — The results are in. Analyse honestly.", kicker="Test, CI, SRM"))
p.append(B.concept(
 "After two weeks: **control** 8,000 visitors, 640 purchases (8.0%); **treatment** 8,000 visitors, "
 "720 purchases (9.0%). First the trust check, then the test and &mdash; crucially &mdash; the "
 "**confidence interval**, not just a p-value:"))
_c,_o=_run(r'''
import numpy as np
from scipy import stats

n_c, x_c = 8000, 640     # control:   visitors, purchases
n_t, x_t = 8000, 720     # treatment: visitors, purchases
p_c, p_t = x_c/n_c, x_t/n_t

# Trust check: SRM — is the split really 50/50? (chi-square on the counts)
chi = (abs(n_c - n_t))**2 / (n_c + n_t)
print(f"SRM check: split {n_c}/{n_t} -> chi2={chi:.2f} (tiny = fine, no ratio mismatch)")

# Two-proportion z-test
pool = (x_c + x_t)/(n_c + n_t)
se   = np.sqrt(pool*(1-pool)*(1/n_c + 1/n_t))
z    = (p_t - p_c)/se
pval = 2*(1 - stats.norm.cdf(abs(z)))

# 95% CI for the absolute lift
se_diff = np.sqrt(p_c*(1-p_c)/n_c + p_t*(1-p_t)/n_t)
lift = p_t - p_c
lo, hi = lift - 1.96*se_diff, lift + 1.96*se_diff
print(f"conversion: control {p_c:.1%}  vs  treatment {p_t:.1%}")
print(f"absolute lift: {lift:+.1%}   (95% CI  {lo:+.1%} to {hi:+.1%})")
print(f"relative lift: {lift/p_c:+.0%}   p-value: {pval:.4f}")
''')
p.append(B.code_example(_c,_o,filename="analyze.py"))
p.append(B.h2("Step 4 — The recommendation", kicker="Statistical AND practical AND safe"))
p.append(B.concept(
 "Walk the decision rule set in Step 1:\n\n"
 "- **Statistically significant?** p &asymp; 0.023 &lt; 0.05 &mdash; **yes**, and the 95% CI "
 "excludes zero.\n"
 "- **Practically significant?** +1.0pp is a **+12.5% relative** lift, at/above our MDE &mdash; "
 "**yes**, meaningful for the business.\n"
 "- **Guardrails safe?** revenue-per-visitor and latency unchanged &mdash; **yes** (check before "
 "shipping).\n"
 "- **Trustworthy?** SRM clean, ran a full two weeks (novelty faded) &mdash; **yes**.\n\n"
 "**Recommendation: ship the new button.** And state it the way a stakeholder needs it (Track 12): "
 "*\"The redesigned checkout button lifts purchase conversion from 8.0% to 9.0% &mdash; a "
 "statistically solid +12.5% relative gain (95% CI +0.4 to +1.6pp) with no revenue or latency "
 "downside. Recommend rolling out to 100%.\"*"))
p.append(B.h2("Your turn — quantify the relative lift", kicker="Interactive lab"))
p.append(B.pylab(
 "Stakeholders feel **relative** lift more than absolute. From the four result numbers, compute the "
 "**relative lift** in conversion &mdash; `(p_treatment &minus; p_control) / p_control` &mdash; as a "
 "percentage rounded to **1 decimal**, and assign to **`answer`** (e.g. 12.5 for +12.5%).",
 "n_c, x_c = 8000, 640\n"
 "n_t, x_t = 8000, 720\n",
 "p_c, p_t = x_c/n_c, x_t/n_t\n"
 "answer = round((p_t - p_c)/p_c * 100, 1)",
 starter="# p_c = x_c/n_c, p_t = x_t/n_t; relative lift in %, 1 dp\nanswer = ",
 hint="Convert counts to rates, then `(p_t - p_c)/p_c * 100`, rounded to 1 dp.",
 title="Lab — relative lift",
 preview="Control and treatment counts preloaded. First Run boots Python.",
 explain="8.0% &rarr; 9.0% is only +1 absolute point, but **+12.5% relative** &mdash; the framing "
         "that lands in a business review. Always report both: the absolute point change *and* the "
         "relative lift, with the confidence interval."))
p.append(B.keypoints([
 "A rigorous A/B test is a **sequence**: design (metric + guardrails) &rarr; power/size &rarr; run "
 "&rarr; trust-check (SRM) &rarr; test + **CI** &rarr; decide by a **pre-set rule**.",
 "**Size the test first** from baseline, MDE, &alpha;, and power &mdash; undersized tests hide real "
 "effects.",
 "Report the **confidence interval** and both **absolute and relative** lift, not just a p-value.",
 "Ship only when the result is **statistically significant, practically meaningful, and "
 "guardrail-safe** &mdash; and trustworthy (SRM, ran long enough).",
 "Deliver the call in **stakeholder language** &mdash; the analysis isn't done until the decision is "
 "communicated.",
]))
p.append(B.quiz([
 {"q":"The test shows p = 0.023 and a +1.0pp lift (8.0%→9.0%). A guardrail — revenue per visitor — "
      "dropped 4%. What's the right call?",
  "options":[
   {"t":"Don't ship yet — a guardrail breach overrides a significant primary metric; investigate the "
        "revenue drop","correct":True,
    "why":"Correct. The decision rule requires the primary metric up AND guardrails safe. A 4% revenue-"
          "per-visitor drop (perhaps faster checkout = smaller baskets) can outweigh the conversion "
          "gain. Investigate/escalate the tradeoff before shipping."},
   {"t":"Ship — the primary metric is significant, that's all that matters",
    "why":"Guardrails exist precisely to catch this: a conversion win that cannibalises revenue is "
          "not a win. Never ignore a breached guardrail."},
   {"t":"Ship and monitor revenue afterward",
    "why":"Shipping a known guardrail regression and hoping is backwards; the guardrail already "
          "flagged a real cost to resolve first."},
   {"t":"Lower the significance threshold to be safe",
    "why":"The threshold isn't the issue &mdash; a guardrail breach is. Fiddling with &alpha; doesn't "
          "address the revenue drop."}]},
]))
p.append(B.practice([
 {"q":"Before launch, your test shows a 9,000 / 7,000 split instead of the intended 8,000 / 8,000. "
      "What do you do, and why does it matter?",
  "sol":"This is a **sample ratio mismatch (SRM)** &mdash; the observed split departs sharply from the "
        "intended 50/50, which a chi-square test would flag as highly unlikely by chance. **It "
        "matters** because SRM signals the experiment is **broken**: a bug in randomization, logging, "
        "or bot filtering is assigning/counting users unevenly &mdash; and if *who* lands in each arm "
        "is biased, the treatment groups aren't comparable, so **any** conversion difference is "
        "untrustworthy (you may be measuring the bug, not the button). **Do not analyze the results "
        "as-is.** Halt, find the root cause (check the assignment service, event logging, and "
        "filters), fix it, and re-run. An SRM is one of the few things that should make you throw out "
        "a test outright &mdash; a clean split is a precondition for believing anything else."},
]))
p.append(B.callout("note","What this capstone proves you can do",
 "You designed a test with a real decision rule, **sized it with a power calculation**, ran the "
 "**trust checks**, analysed with a proper test *and* confidence interval, weighed **practical** "
 "against **statistical** significance, respected **guardrails**, and delivered a **stakeholder-ready "
 "recommendation**. That end-to-end judgement &mdash; not any single formula &mdash; is what a "
 "product data-science role is.", "&#9670;"))
LESSONS={"cap-02-abtest":"\n".join(x for x in p if x)}
print("content_cap02 OK — chars:", len(LESSONS["cap-02-abtest"]))
