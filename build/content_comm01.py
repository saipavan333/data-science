# -*- coding: utf-8 -*-
import builder as B
IMG="../assets/img/"; p=[]
p.append(B.why(
 "Here's a hard truth that surprises new data scientists: **the best analysis in the world is worth "
 "nothing if it doesn't change a decision.** Communication is the *last mile* &mdash; and it's where "
 "most data-science work quietly dies, not because the analysis was wrong, but because the audience "
 "never understood it, or the recommendation was buried on slide 34. Your influence is capped not by "
 "how good your models are, but by how well you can make someone *act* on them. This track is that "
 "skill, and it may be the highest-leverage one in the whole course."))
p.append(B.h2("Rule zero: know your audience", kicker="Different people, different needs"))
p.append(B.concept(
 "The same finding must be told three different ways depending on who's listening:\n\n"
 "- **Executives** want the **answer and its business implication**, fast. They have five minutes "
 "and care about the decision, not your methodology. Lead with *\"we should do X, here's the "
 "impact.\"*\n"
 "- **Technical peers** want the **how** &mdash; the method, assumptions, and validity &mdash; so "
 "they can trust and build on it. Here the rigour belongs front and centre.\n"
 "- **Business stakeholders** (marketing, ops, product) want **what it means for them and what to "
 "do** &mdash; concrete, in their language, tied to their goals.\n\n"
 "The single most common communication failure is showing executives a technical deep-dive, or "
 "giving engineers a vague summary. **Match the message to the listener** &mdash; same truth, "
 "different framing."))
p.append(B.h2("The Pyramid Principle: answer first", kicker="Lead with the conclusion"))
p.append(B.concept(
 "Analysts instinctively present the way they *worked*: here's the data, here's what I did, here's "
 "the analysis, and therefore (slide 34) here's the conclusion. That's **backwards** for "
 "decision-makers. The **Pyramid Principle** flips it: **state the answer first**, then the few key "
 "arguments that support it, then the data underneath &mdash; available if they want to dig, but not "
 "in the way:"))
p.append(B.figure(IMG+"s_comm_pyramid.png",
 "**The Pyramid Principle.** Lead with **the answer** (your recommendation), support it with **3 key "
 "arguments**, and put the **data and detail** underneath for anyone who wants to drill in. Busy "
 "decision-makers get what they need in the first sentence; the evidence is there but never blocks "
 "the message.",
 "A pyramid: the answer at the top, key supporting arguments in the middle, data and detail at the base."))
p.append(B.concept(
 "This is also called **BLUF** &mdash; *Bottom Line Up Front*. Instead of *\"We analysed 18 months of "
 "data across five cohorts, controlling for seasonality, and after adjusting for...\"*, you open "
 "with: **\"We should raise the free-trial length to 21 days &mdash; it would lift conversions ~15% "
 "with no revenue downside. Here's why.\"** The executive now knows the decision in one breath; every "
 "word after that is *earning* the conclusion they already have, not making them wait for it."))
p.append(B.tip(
 "A ruthless test for any report or email: **if the reader stopped after the first sentence, would "
 "they know what you want them to do?** If not, rewrite the opening. The conclusion is not a reward "
 "for reading to the end &mdash; it's the headline."))
p.append(B.h2("The 'so what?' — insight, not output", kicker="From number to meaning"))
p.append(B.concept(
 "A **finding** is not an **insight**. *\"Churn is 12% in the West region\"* is a finding &mdash; a "
 "fact. The insight is the **\"so what\"**: *\"Churn in the West is double every other region because "
 "of the delivery delays there &mdash; fixing logistics could save ~$2M/year.\"* Always push your "
 "output through the chain: **finding &rarr; why it matters &rarr; what to do**. If you can't "
 "articulate the \"so what,\" you have a number, not a message &mdash; and numbers without meaning "
 "get ignored."))
p.append(B.keypoints([
 "The last mile &mdash; making someone **act** &mdash; caps your impact more than model quality. "
 "Analysis that doesn't change a decision is wasted.",
 "**Know your audience**: executives want the answer + implication; technical peers want the method; "
 "stakeholders want what to do. Same truth, different framing.",
 "**Pyramid Principle / BLUF**: state the **answer first**, then key arguments, then supporting data "
 "&mdash; don't make decision-makers wait for the conclusion.",
 "Test any report: **if they read only the first sentence, do they know what to do?**",
 "Turn findings into insights via the **\"so what\" chain**: finding &rarr; why it matters &rarr; "
 "recommended action.",
]))
p.append(B.quiz([
 {"q":"You have 10 minutes with the CEO to present a pricing analysis. How should you open?",
  "options":[
   {"t":"With the recommendation and its business impact — \"We should lower the entry tier to $9; "
        "it lifts signups ~20% with neutral revenue\" — then support it","correct":True,
    "why":"Correct. Executives need the decision and its implication first (BLUF / Pyramid). Lead with "
          "the answer, then earn it with a few key arguments; keep methodology available but not up "
          "front."},
   {"t":"With your data sources and methodology, building up to the conclusion at the end",
    "why":"That's the analyst's working order, not the executive's needs. A busy CEO may leave before "
          "slide 34 &mdash; lead with the conclusion."},
   {"t":"With a detailed walkthrough of the model you built",
    "why":"Methodology is for technical peers. For the CEO, the *decision and impact* come first; "
          "method is backup detail."},
   {"t":"With an apology that the analysis is still preliminary",
    "why":"Undercuts your message and wastes the opening. State the recommendation and its confidence "
          "clearly instead."}]},
 {"q":"Which of these is an insight rather than just a finding?",
  "options":[
   {"t":"\"Mobile users convert 3× better than web, so shifting ad spend to mobile could add ~$500k/"
        "quarter — we should reallocate\"","correct":True,
    "why":"Correct. It carries the 'so what' chain: the fact (3&times;), why it matters (spend "
          "implication), and the action (reallocate). That's an insight that drives a decision."},
   {"t":"\"Mobile conversion rate is 3.1% and web is 1.0%\"",
    "why":"That's a finding &mdash; a bare fact with no implication or action. It needs the 'so what' "
          "to become an insight."},
   {"t":"\"We collected 2M sessions across both platforms\"",
    "why":"That's methodology/scope, not even a finding about the outcome. Far from an actionable "
          "insight."},
   {"t":"\"The data is statistically significant at p < 0.05\"",
    "why":"A validity statement, not an insight. It says the result is real, not what it *means* or "
          "what to *do*."}]},
]))
p.append(B.practice([
 {"q":"Rewrite this opening for a CFO audience: \"Over the past two quarters we pulled transaction "
      "logs, cleaned them, ran a cohort analysis controlling for seasonality and channel, tested "
      "several models, and found that customers acquired via referral have a retention curve that, "
      "when integrated, implies a higher lifetime value...\"",
  "sol":"Lead with the answer and its money implication, Pyramid-style: **\"Referral customers are "
        "worth ~40% more over their lifetime than paid-acquisition customers &mdash; we should shift "
        "budget toward the referral program, which could add roughly \\$3M in annual LTV. Three "
        "reasons: they retain longer, spend more per order, and cost less to acquire. (Methodology: "
        "two quarters of transaction data, cohort analysis controlling for seasonality and channel "
        "&mdash; details in the appendix.)\"** The rewrite states the recommendation and dollar impact "
        "in the first sentence, gives three supporting arguments, and demotes the methodology to a "
        "parenthetical/appendix &mdash; exactly the inversion the Pyramid Principle prescribes for a "
        "busy executive."},
 {"q":"Take a bare finding &mdash; \"Feature X is used by only 4% of users\" &mdash; and turn it into "
      "an insight with a 'so what' chain. (Invent plausible context.)",
  "sol":"Example: **Finding** &mdash; \"Feature X is used by only 4% of users.\" **Why it matters** "
        "&mdash; \"...yet it consumes 30% of our engineering maintenance time and appears in 0 of our "
        "top retention drivers.\" **So what / action** &mdash; \"We should either sunset Feature X or "
        "run one focused experiment to fix its discoverability; if that doesn't move usage, "
        "deprecating it frees ~1.5 engineers for higher-impact work.\" The point is to travel the "
        "chain from *fact* &rarr; *implication* (cost vs. value) &rarr; *recommended decision*. A "
        "good answer names the consequence of the 4% and proposes a concrete action &mdash; not just "
        "the statistic. (Any coherent context works; the skill is the finding&rarr;meaning&rarr;action "
        "structure.)"},
]))
p.append(B.deepdive(
 B.concept(
  "**Why answer-first feels wrong but works.** Presenting your conclusion first can feel like "
  "'giving away the ending' or seeming arrogant &mdash; analysts often want to *show their work* to "
  "earn trust. But decision-makers process top-down: they hold your conclusion in mind as a "
  "hypothesis and evaluate your evidence *against it*, which is far easier than assembling a "
  "conclusion themselves from a pile of facts. Leading with the answer also respects their time and "
  "signals confidence. The evidence still matters &mdash; it's right there in the pyramid's lower "
  "tiers &mdash; but it *supports* the message rather than *delaying* it. (The one exception: when "
  "you must first overcome strong disagreement, you may briefly build shared premises before "
  "landing the conclusion &mdash; but even then, get to it fast.)") +
 B.concept(
  "**The curse of knowledge is your biggest enemy.** After weeks inside a problem, everything is "
  "obvious *to you* &mdash; the acronyms, the caveats, the reason a particular cohort matters. Your "
  "audience has none of that context, and the single hardest communication skill is **remembering "
  "what they don't know**. Concretely: define terms the first time, replace jargon with plain "
  "language, lead with the point before the detail, and cut the fascinating-but-irrelevant nuances "
  "you fell in love with during the analysis. A useful habit is to draft your summary, then ask "
  "*\"what would a smart person outside my team not understand here?\"* &mdash; and fix each spot. "
  "Clarity for the audience, not completeness for yourself, is the goal."),
 title="Deep dive: why top-down persuades, and beating the curse of knowledge"))
LESSONS={"comm-01-audience":"\n".join(x for x in p if x)}
print("content_comm01 OK — chars:", len(LESSONS["comm-01-audience"]))
