# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "In interviews &mdash; and on the job &mdash; communication is often the **deciding** signal. Two "
 "candidates can have identical technical skill; the one who can explain a model to a VP, defend a "
 "recommendation, and turn a result into a decision is the one who gets hired and promoted. "
 "Behavioural and case rounds probe this directly: *\"explain X to a non-technical stakeholder,\" "
 "\"present this result,\" \"tell me about a time your analysis changed a decision.\"* This is how "
 "you show you can create **impact**, not just output."))
p.append(B.h2("Say these out loud", kicker="Rapid-fire drill"))
p.append(B.interview_check([
 "Explain **p-value** (or **overfitting**, or **A/B testing**) to a **non-technical** executive in "
 "two sentences.",
 "You have 30 seconds with the CEO on your analysis &mdash; what do you say? (**BLUF**)",
 "Walk me through structuring a findings presentation. (**Pyramid**: answer &rarr; arguments &rarr; "
 "data)",
 "How do you turn a **finding** into an **insight**? (the 'so what' chain)",
 "Give the three beats of a **data story**. (context &rarr; complication &rarr; resolution)",
 "How do you tailor the **same result** for an exec vs. an engineer vs. a marketer?",
 "What's wrong with a **'here's all the data, you decide'** presentation?",
 "Name three ways to **declutter** a chart so it communicates.",
 "Why must bar charts **start at zero** &mdash; and name another way charts mislead.",
 "Tell me about a time your **analysis changed a decision** &mdash; what did you do to make that "
 "happen?",
], title="The communication drill")
)
p.append(B.practice([
 {"q":"CASE: An interviewer says, \"Explain what a p-value is to a marketing VP who never took "
      "statistics.\" Give your answer.",
  "sol":"Aim for a plain-language, decision-oriented explanation with no jargon: **\"A p-value "
        "answers one question: could this result be a fluke? Say we test a new email subject line "
        "and it gets more clicks. The p-value tells us how likely we'd see a gap *this big* purely by "
        "chance if the new subject line were actually no better. A **small** p-value (say under 0.05) "
        "means 'a fluke this size would be rare, so the difference is probably real &mdash; worth "
        "acting on.' A **large** p-value means 'this could easily be random noise &mdash; don't bet "
        "on it yet.' It's not proof, and it doesn't tell us how *big* or *valuable* the effect is "
        "&mdash; just how confident we can be that it's real.\"** Strong answers: use an example from "
        "*their* world, avoid 'null hypothesis'/'reject', and connect it to a **decision** (act vs. "
        "don't). The interviewer is testing whether you can translate rigour into plain language "
        "without distorting it."},
 {"q":"CASE: \"Present the result of an experiment that came back flat (no significant effect) to a "
      "product team that was hoping their feature was a winner.\" How do you handle it?",
  "sol":"Lead honestly and constructively, Pyramid-style. **Answer first:** \"The test didn't show a "
        "significant effect &mdash; we can't conclude this feature moved the metric, so I'd not ship "
        "it as-is.\" **Then the nuance that makes it useful, not deflating:** distinguish *\"no "
        "effect\"* from *\"no information\"* &mdash; was it **well-powered** (tight confidence "
        "interval around zero = a real null) or **underpowered** (wide interval = we learned little, "
        "run longer)? Check **segments** (did it help one group and hurt another, cancelling out?) "
        "and **guardrails**. **Resolution / next step:** frame the null as **learning**, not failure "
        "&mdash; \"here's what we now know, here's the cheaper hypothesis it points to, here's what "
        "I'd test next.\" The communication skills on display: deliver unwelcome news **clearly and "
        "early** (don't bury it), preserve the team's trust by being **rigorous rather than "
        "apologetic**, and always leave them with a **path forward**. Spinning a flat result as a "
        "win would be the wrong answer &mdash; honesty plus a next step is what they're looking for."},
]))
p.append(B.callout("note","The through-line of the whole track",
 "Communication is where analysis becomes **impact**. Know your audience and speak to *their* needs; "
 "lead with the **answer** (Pyramid/BLUF); wrap findings in a **story** (context &rarr; complication "
 "&rarr; resolution); push every number through the **'so what' chain** to an action; and build "
 "charts that deliver **one honest message** fast. The technical work earns you a seat at the table "
 "&mdash; communication is what lets you actually change what happens once you're there. Master it "
 "and you multiply the value of everything else in this course.", "&#9670;"))
LESSONS={"comm-04-interview":"\n".join(p)}
print("content_comm04 OK — chars:", len(LESSONS["comm-04-interview"]))
