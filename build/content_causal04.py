# -*- coding: utf-8 -*-
import builder as B
p=[]

p.append(B.why(
 "Causal reasoning is the **most senior-sounding** skill you can show. Anyone can run a regression; "
 "the person who says *\"but that coefficient isn't causal &mdash; here's the confounder, and here's "
 "how I'd actually estimate the effect\"* is the one who gets trusted with decisions. Product-sense "
 "and analytics interviews probe exactly this: can you tell a real effect from a mirage, and design "
 "a way to measure it when you can't run a clean A/B test?"))

p.append(B.h2("Say these out loud", kicker="Rapid-fire drill"))
p.append(B.interview_check([
 "Explain **correlation vs. causation** with an example a non-technical stakeholder would get.",
 "What is a **confounder**? Draw the ice-cream/drownings diagram.",
 "Why is **randomization** the gold standard &mdash; what exactly does it fix?",
 "What's the **fundamental problem of causal inference**?",
 "Fork, chain, collider &mdash; which do you **adjust** for, and which must you **not**?",
 "Why can \"controlling for more variables\" make an analysis **worse**?",
 "What is **selection bias**, and how is it a collider in disguise?",
 "Walk me through **difference-in-differences** and its key assumption.",
 "You can't A/B test feature X &mdash; give me **three** ways you'd still estimate its effect.",
 "An observational study claims X causes Y. What's your **checklist** before believing it?",
], title="The causal-inference drill")
)

p.append(B.practice([
 {"q":"CASE: \"Our data shows users who enable notifications retain 40% better. Should we force-enable "
      "notifications for everyone?\" Give a full causal answer.",
  "sol":"**Resist the leap.** The 40% is almost certainly **confounded by self-selection**: users who "
        "*choose* to enable notifications are already more engaged/committed, and that engagement "
        "drives *both* the opt-in and the retention. So notifications and retention share a common "
        "cause &mdash; the correlation is partly (maybe mostly) spurious, and force-enabling for "
        "lukewarm users may not transfer the retention (and could backfire via annoyance). **How I'd "
        "actually settle it:** a **randomized encouragement / experiment** &mdash; randomly prompt a "
        "subset to enable notifications (or randomly default them on) and compare retention to a "
        "held-out control; that severs the self-selection arrow. If experimentation is impossible, "
        "I'd **adjust** for measured engagement (matching/regression) as a weaker estimate and be "
        "explicit that unmeasured motivation could still bias it. **Recommendation:** don't ship a "
        "forced change off a confounded correlation &mdash; test it first."},
 {"q":"CASE: \"We rolled out a new onboarding flow to all EU users last month; the US kept the old "
      "one. EU activation went up 9 points. Did the new flow work?\" How would you analyze it?",
  "sol":"This is a **difference-in-differences** setup: EU = treated, US = control, known switch date. "
        "The 9-point EU rise **overstates** the effect if activation was trending up everywhere, so I "
        "wouldn't credit it all to the flow. **DiD:** compute (EU after &minus; EU before) &minus; "
        "(US after &minus; US before) &mdash; subtracting the US change removes the shared background "
        "trend, leaving the flow's own effect. **Crucially, defend parallel trends:** plot EU and US "
        "activation for several months *before* the rollout and confirm they moved in parallel; if "
        "they already diverged, DiD is invalid. I'd also watch for **confounds coinciding with the "
        "rollout** (an EU-only marketing push, a holiday, seasonality differences) and check "
        "segment/​SRM-style sanity. Conclusion: the flow 'worked' only to the extent of the "
        "*difference-in-differences*, conditional on parallel pre-trends &mdash; not the raw 9 "
        "points."},
]))

p.append(B.callout("note","The through-line of the whole track",
 "Causal inference is a **discipline of humility**: observational numbers don't speak for themselves, "
 "so you draw your assumptions (the DAG), pick the design whose assumption you can defend, and say "
 "out loud what would have to be true for your estimate to hold. Randomize when you can; when you "
 "can't, approximate it carefully and never dress up a correlation as a cause. That judgement is "
 "worth more to a business than any model.", "&#9670;"))

LESSONS={"causal-04-interview":"\n".join(p)}
print("content_causal04 OK — chars:", len(LESSONS["causal-04-interview"]))
