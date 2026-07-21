# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "\"What should I control for?\" is *the* question in observational analysis &mdash; and the last "
 "lesson showed it has a dangerous wrong answer (\"everything\"). A **causal diagram** (a DAG &mdash; "
 "directed acyclic graph) turns it into a set of readable rules. You draw the arrows you believe "
 "exist, and the diagram *tells you* which variables to adjust for and which to leave alone. It's the "
 "single most useful thinking tool in causal inference, and it takes about ten minutes to learn the "
 "core of."))

p.append(B.h2("Three building blocks — and that's nearly all of it", kicker="Fork, chain, collider"))
p.append(B.concept(
 "Every causal diagram is built from three elementary patterns of three variables. Learn how each "
 "one transmits or blocks association, and you can read any DAG:"))
p.append(B.figure(IMG+"s_causal_dags.png",
 "**The three structures.** **Fork** (Z is a common cause of X and Y): Z is a **confounder** &mdash; "
 "**adjust for it**. **Chain** (X&rarr;M&rarr;Y): M is a **mediator** on the causal path &mdash; "
 "**don't** adjust if you want the total effect. **Collider** (X and Y both cause C): C is a common "
 "**effect** &mdash; adjusting for it **creates** a fake association.",
 "Three DAGs: a fork with Z causing X and Y, a chain X to M to Y, and a collider X and Y both into C."))
p.append(B.concept(
 "The rules that fall out of these three:\n\n"
 "- **Fork &mdash; confounder (Z &rarr; X, Z &rarr; Y).** Z opens a **backdoor path** X &larr; Z "
 "&rarr; Y that leaks non-causal association. **Adjust for Z** to close it. *This is the one you "
 "must not miss.*\n"
 "- **Chain &mdash; mediator (X &rarr; M &rarr; Y).** M carries the effect. If you want the **total** "
 "effect of X, **leave M alone**; adjusting for it blocks the very pathway you're trying to measure.\n"
 "- **Collider &mdash; common effect (X &rarr; C &larr; Y).** A collider path is **naturally "
 "blocked**. Adjusting for C (or selecting on it) **opens** it and invents a spurious X&ndash;Y "
 "correlation. **Do not adjust for colliders.**"))

p.append(B.h2("The rule: close every backdoor, open no new ones", kicker="The backdoor criterion"))
p.append(B.concept(
 "A **backdoor path** is any non-causal path from X to Y that starts with an arrow *into* X (like "
 "X &larr; Z &rarr; Y). These paths carry confounding association. The ~backdoor criterion~ says: to "
 "estimate the causal effect of X on Y, **adjust for a set of variables that blocks every backdoor "
 "path &mdash; without adjusting for any mediator or collider.** Do that, and what's left is the "
 "clean causal effect. The DAG is what lets you *see* the backdoor paths and pick the right "
 "adjustment set."))
p.append(B.warn(
 "The seductive mistake is **\"more controls = safer.\"** The collider says otherwise. Throwing every "
 "available column into a regression can **open** collider paths and **block** mediators, biasing the "
 "estimate in ways no amount of data fixes. Controls are a scalpel, not a fire hose &mdash; the DAG "
 "tells you where to cut."))

p.append(B.h2("See a collider create a correlation from nothing", kicker="The spookiest bias"))
p.append(B.concept(
 "Take two things that are **genuinely unrelated** &mdash; say an actor's *talent* (X) and their "
 "*looks* (Y). Now select on a common effect: to get *hired*, you need talent **or** looks (C = "
 "talent + looks). Look only at **hired** actors and a fake **negative** correlation appears &mdash; "
 "the plain ones must be talented to have made it, the untalented ones must be beautiful. Nothing "
 "connects talent and looks in reality; conditioning on the collider **manufactured** the link:"))
_c,_o=_run(r'''
import numpy as np
rng = np.random.default_rng(1)
n = 20000

talent = rng.normal(size=n)
looks  = rng.normal(size=n)                    # independent of talent!
hired_score = talent + looks + rng.normal(size=n)*0.3   # collider: caused by BOTH

overall = np.corrcoef(talent, looks)[0, 1]
print(f"correlation in everyone:            {overall:+.2f}   <- ~0, truly unrelated")

sel = np.abs(hired_score - 2.0) < 0.25         # look only at 'hired' actors (high score)
among = np.corrcoef(talent[sel], looks[sel])[0, 1]
print(f"correlation among 'hired' actors:   {among:+.2f}   <- negative, out of thin air!")
''')
p.append(B.code_example(_c,_o,filename="collider.py"))
p.append(B.pitfall(
 "This is **selection bias** &mdash; and it's a collider in disguise. Any time your data is filtered "
 "by an outcome (\"we only have data on customers who *converted*,\" \"only patients sick enough to "
 "be *admitted*\"), you may be conditioning on a collider and reading correlations that don't exist "
 "in the population. *How the data was selected* is a causal assumption you must draw."))

p.append(B.h2("Your turn — measure the collider bias", kicker="Interactive lab"))
p.append(B.pylab(
 "`talent` and `looks` are **independent**. But `hired` (a boolean) is a **collider** &mdash; caused "
 "by both. Among only the **hired** actors (`hired == True`), compute the correlation between "
 "`talent` and `looks`, round to **2 decimals**, and assign it to **`answer`**. It should come out "
 "**negative**, even though they're unrelated overall.",
 "import numpy as np\n"
 "rng = np.random.default_rng(1)\n"
 "n = 20000\n"
 "talent = rng.normal(size=n)\n"
 "looks  = rng.normal(size=n)\n"
 "hired  = (talent + looks + rng.normal(size=n)*0.3) > 1.8   # collider (boolean)\n",
 "answer = round(float(np.corrcoef(talent[hired], looks[hired])[0, 1]), 2)",
 starter="import numpy as np\n# among rows where hired is True, correlate talent and looks\nanswer = ",
 hint="Index both arrays with the boolean mask: `talent[hired]`, `looks[hired]`, then "
      "`np.corrcoef(...)[0,1]` and round to 2 dp.",
 title="Lab — conditioning on a collider",
 preview="numpy loaded; talent, looks (independent) and hired (a collider) prebuilt. First Run boots Python.",
 explain="Negative &mdash; a correlation that **does not exist** in the full population appears the "
         "instant you restrict to 'hired'. This is why *how your sample was selected* is a causal "
         "assumption, and why you must never adjust for (or select on) a collider."))

p.append(B.keypoints([
 "A **DAG** encodes your causal assumptions as arrows; it tells you what to adjust for.",
 "**Fork** (Z&rarr;X, Z&rarr;Y): Z is a **confounder** &mdash; **adjust** for it to close the "
 "backdoor.",
 "**Chain** (X&rarr;M&rarr;Y): M is a **mediator** &mdash; **don't** adjust if you want the total "
 "effect.",
 "**Collider** (X&rarr;C&larr;Y): adjusting for or **selecting on** C **creates** a spurious "
 "association (selection bias).",
 "**Backdoor criterion**: block every backdoor path, adjust for **no** mediators or colliders "
 "&mdash; \"more controls\" is *not* always safer.",
]))

p.append(B.quiz([
 {"q":"You want the total causal effect of an ad campaign (X) on sales (Y). You believe X &rarr; "
      "website visits (M) &rarr; sales (Y). Should you control for website visits?",
  "options":[
   {"t":"No — visits are a mediator on the causal path; controlling for them removes part of the "
        "effect you're trying to measure","correct":True,
    "why":"Correct. The campaign works *through* visits, so visits are a mediator. Adjusting for a "
          "mediator blocks the causal pathway and shrinks the estimated total effect. Leave it alone "
          "(unless you specifically want the *direct* effect)."},
   {"t":"Yes — always control for everything you measured",
    "why":"That's the trap. Controlling for a mediator biases the total-effect estimate. Adjustment "
          "must be selective."},
   {"t":"Yes — visits are a confounder",
    "why":"Visits are *caused by* the campaign (a mediator), not a common cause of it. They sit on "
          "the path, so they're not a confounder."},
   {"t":"It makes no difference either way",
    "why":"It makes a big difference: adjusting for the mediator systematically understates the "
          "campaign's total effect."}]},
 {"q":"A study of hospitalized patients finds smoking is associated with *lower* COVID severity. A "
      "likely explanation?",
  "options":[
   {"t":"Collider/selection bias — being hospitalized is a common effect of both smoking and COVID "
        "severity, so conditioning on it can flip the association","correct":True,
    "why":"Correct. Hospitalization is caused by many risk factors; among the admitted, a smoker may "
          "be there for smoking-related reasons rather than severe COVID, inducing a spurious "
          "negative association. Classic collider bias from selecting on the admitted."},
   {"t":"Smoking must genuinely protect against COVID",
    "why":"Unlikely, and the pattern is a well-known artifact of conditioning on hospitalization (a "
          "collider). Don't take the selected-sample correlation at face value."},
   {"t":"The sample was too small",
    "why":"Size isn't the issue; the bias comes from *selecting on a collider* (hospitalization) and "
          "persists at any sample size."},
   {"t":"Confounding by age",
    "why":"Age is a confounder in general, but the specific 'flip among the hospitalized' signature "
          "is collider/selection bias from conditioning on admission."}]},
]))

p.append(B.practice([
 {"q":"Draw (in words) the DAG for: a scholarship (X) may raise graduation rates (Y); richer "
      "families (Z) are more likely to get the scholarship AND to graduate anyway. What must you "
      "adjust for, and why?",
  "sol":"The DAG: **Z &rarr; X**, **Z &rarr; Y**, and **X &rarr; Y** (the effect of interest). Family "
        "wealth Z is a **fork/confounder** creating a backdoor path X &larr; Z &rarr; Y. To estimate "
        "the scholarship's true effect you must **adjust for Z (family wealth)** to close that "
        "backdoor &mdash; otherwise part of the apparent graduation boost is just wealthier kids "
        "being wealthier. You would *not* adjust for anything on the path X&rarr;Y (e.g. a mediator "
        "like 'hours able to study'), since that would remove part of the scholarship's own effect."},
 {"q":"Explain, to a skeptical manager, why 'let's just add every column as a control' can make an "
      "analysis worse.",
  "sol":"Controls aren't free &mdash; they only help when the variable is a **confounder** (a common "
        "cause of treatment and outcome). Add a **mediator** (something the treatment causes on its "
        "way to the outcome) and you erase part of the real effect. Add a **collider** (something "
        "*caused by* both, or a selection filter) and you **invent** a correlation that isn't there. "
        "So blindly controlling for everything can bias the estimate in either direction, and no "
        "amount of extra data fixes a mis-specified adjustment set. The disciplined move is to draw "
        "the assumed causal diagram and adjust for exactly the set that closes the backdoors &mdash; "
        "no more, no less."},
]))

p.append(B.deepdive(
 B.concept(
  "**d-separation, in one idea.** A path between X and Y is **blocked** if it contains (a) a "
  "non-collider you *have* adjusted for, or (b) a collider you have *not* adjusted for. X and Y are "
  "'d-separated' (independent) given a set S if S blocks **every** path between them. The backdoor "
  "criterion is just d-separation applied to the non-causal (backdoor) paths: find an adjustment set "
  "S that blocks all of them while leaving the causal path X&rarr;...&rarr;Y open. Software (DAGitty, "
  "the `dowhy` library) will read your drawn DAG and *output* a valid adjustment set &mdash; turning "
  "a subtle logic problem into a checkbox.") +
 B.concept(
  "**M-bias &mdash; the trap that breaks 'when in doubt, control for it.'** Consider U1 &rarr; X, "
  "U1 &rarr; Z, U2 &rarr; Z, U2 &rarr; Y, where Z is a **pre-treatment** collider (caused by two "
  "hidden causes). Z happens *before* treatment and correlates with both X and Y, so it *looks* like "
  "a confounder you should adjust for &mdash; but adjusting for it **opens** the collider and creates "
  "bias where there was none. This is why 'it happened before treatment, so control for it' is not a "
  "safe rule, and why you genuinely need the diagram: the *role* of a variable, not its timing, "
  "decides whether adjusting helps or hurts."),
 title="Deep dive: d-separation, automated adjustment sets, and M-bias"))

LESSONS={"causal-02-dags":"\n".join(x for x in p if x)}
print("content_causal02 OK — chars:", len(LESSONS["causal-02-dags"]))
