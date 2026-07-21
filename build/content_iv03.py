# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "The statistics round doesn't test whether you can *run* a t-test &mdash; it tests whether you "
 "**understand** what it means, so you won't misuse it on the job. Interviewers ask you to explain "
 "p-values in plain English, reason through a probability puzzle, or spot why an analysis is flawed. "
 "This bank drills the concepts that recur, crisply answered &mdash; and the payoff is that clear "
 "understanding *sounds* like seniority."))
p.append(B.h2("The concept questions", kicker="Explain, don't recite"))
p.append(B.interview_check([
 "Explain a **p-value** to a non-technical stakeholder.",
 "What is the **Central Limit Theorem**, and why does it matter?",
 "What does a **95% confidence interval** actually mean (and not mean)?",
 "**Type I vs Type II error** &mdash; and what is **statistical power**?",
 "**Correlation vs causation** &mdash; and how do you get causation?",
 "When is the **mean** misleading, and what do you use instead?",
 "What's the difference between **probability and likelihood**?",
 "Explain the **bias&ndash;variance tradeoff**.",
 "What is **selection bias**? Give an example.",
 "**Bayes' theorem** &mdash; walk through the disease-test problem.",
], title="The statistics deep-dive drill")
)
p.append(B.h2("Worked answer — the p-value", kicker="The one you'll definitely be asked"))
p.append(B.concept(
 "*\"A p-value answers one question: if there were **no real effect**, how surprising would a result "
 "this extreme be? It's the probability of seeing data at least this striking **assuming the null "
 "hypothesis is true**. A small p-value (say &lt; 0.05) means such data would be rare by chance "
 "alone, so we have evidence against 'no effect.' A large one means chance could easily explain it.\"*"
 "\n\nThen show the discipline of what it is **not**: it is **not** the probability the null is true, "
 "**not** the probability your result was a fluke, and it says **nothing** about **effect size** or "
 "importance. That list of caveats is what separates understanding from memorisation."))
p.append(B.h2("Worked answer — the Bayes disease-test puzzle", kicker="Base rates trip everyone"))
p.append(B.concept(
 "*\"A disease affects 1 in 1,000. A test is 99% accurate. You test positive &mdash; what's the "
 "chance you have it?\"* The intuitive \"99%\" is badly wrong, because the **base rate** is tiny. "
 "Out of 100,000 people: ~100 have it (99 test positive), but ~99,900 don't and **1%** of them "
 "&mdash; ~999 &mdash; **also** test positive. So of ~1,098 positives, only 99 are real: **&asymp;9%**. "
 "The false positives from the huge healthy group swamp the few true cases. Reasoning through base "
 "rates like this &mdash; rather than trusting the '99%' &mdash; is exactly what the question "
 "tests."))
p.append(B.h2("Your turn — simulate the birthday paradox", kicker="Interactive lab"))
p.append(B.pylab(
 "A famous puzzle: in a room of just **23** people, how likely is it that **two share a birthday**? "
 "Intuition says \"rare\"; simulation says otherwise. Over many random rooms of 23, compute the "
 "fraction that contain **at least one shared birthday**, round to **2 decimals**, and assign to "
 "**`answer`**.",
 "import numpy as np\n"
 "rng = np.random.default_rng(0)\n"
 "trials = 50000\n"
 "rooms = rng.integers(0, 365, size=(trials, 23))   # 50k rooms of 23 birthdays\n",
 "s = np.sort(rooms, axis=1)\n"
 "has_shared = (np.diff(s, axis=1) == 0).any(axis=1)\n"
 "answer = round(float(has_shared.mean()), 2)",
 starter="import numpy as np\n# for each room, is there a duplicate birthday? then take the mean\nanswer = ",
 hint="Sort each room's birthdays, and a duplicate exists where consecutive sorted values are equal "
      "(`np.diff(...) == 0`). `.any(axis=1)` per room, then `.mean()`.",
 title="Lab — the birthday paradox",
 preview="numpy loaded; 50,000 random rooms of 23 birthdays preloaded. First Run boots Python.",
 explain="About **0.51** &mdash; a better-than-even chance with only 23 people! It feels impossible "
         "because we intuitively think about matches to *our own* birthday, but there are "
         "23&times;22/2 = 253 *pairs* that could match. This gap between intuition and the math is "
         "exactly why interviewers love probability puzzles &mdash; and why simulating is a great way "
         "to check your reasoning."))
p.append(B.keypoints([
 "The stats round tests **understanding**, not computation &mdash; be able to **explain** concepts in "
 "plain English.",
 "**p-value** = P(data this extreme | null true); it is **not** P(null true), not P(fluke), and says "
 "nothing about **effect size**.",
 "**Base rates dominate** (Bayes): a 99%-accurate test for a 1-in-1000 disease still yields ~9% "
 "chance of disease given a positive.",
 "Know cold: **CLT** (sample means &rarr; normal), **CI** interpretation, **Type I/II &amp; power**, "
 "**correlation &ne; causation**.",
 "For probability puzzles, **reason about the structure** (pairs, base rates) &mdash; and you can "
 "**simulate** to check.",
]))
p.append(B.quiz([
 {"q":"Which is the correct plain-English meaning of 'p = 0.03'?",
  "options":[
   {"t":"If there were truly no effect, we'd see a result this extreme only ~3% of the time","correct":True,
    "why":"Correct. The p-value is computed *assuming the null is true* and measures how extreme the "
          "observed data is under that assumption. p = 0.03 = such data would be rare (~3%) if there "
          "were no real effect."},
   {"t":"There's a 3% chance the null hypothesis is true",
    "why":"A classic misinterpretation. The p-value is P(data | null), not P(null | data). It doesn't "
          "give the probability the null is true."},
   {"t":"There's a 97% chance our result is real and important",
    "why":"Wrong twice: p-values don't give the probability an effect is real, and say nothing about "
          "importance/effect size."},
   {"t":"The effect is large",
    "why":"A small p-value can accompany a tiny effect (especially with big samples). Significance "
          "&ne; magnitude."}]},
 {"q":"A disease affects 1 in 1,000; a test is 99% accurate. You test positive. Roughly your chance "
      "of having it?",
  "options":[
   {"t":"About 9% — false positives from the large healthy majority swamp the few true cases","correct":True,
    "why":"Correct. Per 100k people: ~99 true positives vs ~999 false positives (1% of ~99,900 "
          "healthy), so ~99/1098 &asymp; 9%. The low base rate makes a positive far less alarming "
          "than '99% accurate' suggests."},
   {"t":"About 99% — the test is 99% accurate",
    "why":"This ignores the base rate. With the disease so rare, most positives are false positives, "
          "giving only ~9%."},
   {"t":"About 50%",
    "why":"The Bayesian calculation gives ~9%, not 50% &mdash; the huge healthy group produces many "
          "more false positives than there are true cases."},
   {"t":"About 1% — that's the disease rate",
    "why":"1% is close to the *prior*; a positive test updates it upward to ~9% (still far from "
          "99%)."}]},
]))
p.append(B.practice([
 {"q":"An interviewer asks: \"What does a 95% confidence interval actually mean?\" Give a precise "
      "answer, including a common misinterpretation to avoid.",
  "sol":"**Precise meaning:** a 95% CI comes from a *procedure* that, if you repeated the whole "
        "sampling-and-interval process many times, would capture the true parameter in about 95% of "
        "those intervals. It expresses the **reliability of the method**, and for any single interval "
        "the true value is either in it or not. **Common misinterpretation to avoid:** \"there's a "
        "95% probability the true value lies in *this specific* interval.\" In frequentist terms "
        "that's incorrect &mdash; the parameter is fixed, not random, so a given interval either "
        "contains it or doesn't; the 95% refers to the long-run performance of the procedure, not a "
        "probability about one interval. (I'd add that a wide CI signals high uncertainty and is "
        "often *more* informative than a bare point estimate or p-value.) Nailing the "
        "procedure-vs-single-interval distinction is the mark of real statistical literacy."},
]))
LESSONS={"iv-03-stats":"\n".join(p)}
print("content_iv03 OK — chars:", len(LESSONS["iv-03-stats"]))
