# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "Technical skill gets you *into* the final round; the **behavioral** interview decides whether you "
 "get the **offer**. It answers the question every team quietly asks: *\"do we want to work with this "
 "person for the next few years?\"* Candidates underprepare for it because it feels 'soft' &mdash; "
 "and lose offers to people with weaker technical skills but clearer, more compelling stories. A "
 "little structure fixes that entirely."))
p.append(B.h2("The STAR method", kicker="Structure every story"))
p.append(B.concept(
 "The antidote to rambling, vague answers is **STAR** &mdash; structure every behavioral story in "
 "four beats:\n\n"
 "- **Situation** &mdash; the context, briefly. *\"Our churn model was retraining weekly but silently "
 "failing.\"*\n"
 "- **Task** &mdash; your specific responsibility. *\"I owned model reliability, so it was on me to "
 "fix it.\"*\n"
 "- **Action** &mdash; what **you** did (say \"I,\" not \"we\"), with reasoning. *\"I traced it to a "
 "schema change, added validation and monitoring, and set up alerts.\"*\n"
 "- **Result** &mdash; the outcome, **quantified**. *\"Retraining went from ~70% to 100% reliable, "
 "and we caught the next break in minutes instead of weeks.\"*\n\n"
 "STAR keeps you concise and makes your **contribution and impact** unmistakable &mdash; the two "
 "things the interviewer is actually listening for."))
p.append(B.h2("The questions to prepare", kicker="Have a story for each"))
p.append(B.interview_check([
 "Tell me about a **project you're proud of**. (impact, your role)",
 "Describe a time you had a **conflict** with a teammate/stakeholder. (maturity)",
 "Tell me about a **failure** or a mistake. (ownership, learning)",
 "A time you dealt with an **ambiguous** problem. (structuring)",
 "A time your **analysis changed a decision**. (impact)",
 "How do you handle **competing priorities / tight deadlines**?",
 "A time you had to **explain something technical** to a non-technical audience.",
 "Why this **company / role**? (genuine motivation)",
 "A time you **disagreed with data** or pushed back on a request.",
 "What are the **best questions to ask the interviewer**?",
], title="The behavioral drill")
)
p.append(B.h2("What they're really listening for", kicker="And the red flags"))
p.append(B.concept(
 "Behind the questions, interviewers assess **ownership, collaboration, communication, and "
 "self-awareness**. Show them: take credit for *your* actions (\"I\") while crediting the team; on a "
 "**failure** question, own the mistake and emphasise what you **learned and changed** (never "
 "\"I don't really have failures\"); on **conflict**, show you sought to understand the other side "
 "and reached a good outcome, not that you 'won.'\n\n"
 "The **red flags** that sink candidates: **blaming others** for failures, vague impact (\"it went "
 "well\" &mdash; quantify it), badmouthing past employers, taking sole credit for team work, and "
 "having **no questions** for the interviewer (reads as disinterest)."))
p.append(B.tip(
 "Prepare **5&ndash;6 flexible stories** from your experience &mdash; a proud project, a failure, a "
 "conflict, an ambiguous problem, a leadership/initiative moment &mdash; each with quantified "
 "results. Most behavioral questions are variations you can map onto one of these. And always bring "
 "**genuine questions** for them (about the team's challenges, how success is measured, what they're "
 "building) &mdash; it signals real interest and turns the interview into a conversation."))
p.append(B.keypoints([
 "Behavioral rounds decide the **offer** &mdash; they answer *\"do we want to work with this "
 "person?\"* Don't underprepare them.",
 "Structure every story with **STAR** (Situation, Task, Action, Result) &mdash; concise, and your "
 "contribution + **quantified** impact are unmistakable.",
 "Say **\"I\"** for your actions (while crediting the team); on **failures**, own it and emphasise "
 "the **lesson**.",
 "**Red flags**: blaming others, vague impact, badmouthing past employers, no questions for the "
 "interviewer.",
 "Prepare **5&ndash;6 flexible stories** with numbers, and bring **genuine questions** &mdash; it "
 "signals real interest.",
]))
p.append(B.quiz([
 {"q":"Asked \"tell me about a failure,\" what's the strongest approach?",
  "options":[
   {"t":"Describe a real mistake you owned, then focus on what you learned and changed as a result",
    "correct":True,
    "why":"Correct. This shows ownership and growth &mdash; exactly what the question probes. A "
          "genuine failure plus a concrete lesson (and how you apply it now) reads as maturity and "
          "self-awareness."},
   {"t":"Say you can't think of any real failures",
    "why":"A major red flag &mdash; it signals no self-awareness or no honesty. Everyone has "
          "failures; the point is showing what you learned."},
   {"t":"Describe a failure that was entirely someone else's fault",
    "why":"Blaming others is a classic red flag. Own your part and emphasise the lesson."},
   {"t":"Give a 'humblebrag' like 'I work too hard'",
    "why":"Transparent non-answers frustrate interviewers. Share a real mistake and real growth."}]},
 {"q":"Why does using 'I' vs 'we' matter in behavioral answers?",
  "options":[
   {"t":"The interviewer needs to know what YOU specifically did; 'we' hides your individual "
        "contribution","correct":True,
    "why":"Correct. Teams do projects, but they're hiring *you* &mdash; so they need your specific "
          "actions and decisions. Use 'I' for your contribution (while crediting the team) so your "
          "role is clear."},
   {"t":"'We' is grammatically incorrect in interviews",
    "why":"It's not about grammar &mdash; it's that 'we' obscures *your* individual contribution, "
          "which is what they're assessing."},
   {"t":"You should only ever say 'I' and never mention the team",
    "why":"Credit the team too &mdash; that shows collaboration. The point is to make *your* specific "
          "role clear, not to erase others."},
   {"t":"It doesn't matter which you use",
    "why":"It does: over-using 'we' is a common way strong contributors accidentally hide their own "
          "impact."}]},
]))
p.append(B.practice([
 {"q":"Use STAR to draft an answer to \"tell me about a time your analysis changed a decision.\" "
      "(Invent plausible details.)",
  "sol":"A strong answer is concise and hits all four beats with a quantified result. Example: "
        "**Situation** &mdash; \"Our team was about to invest heavily in a referral program based on "
        "the belief that referred users were our most valuable.\" **Task** &mdash; \"I was asked to "
        "validate that assumption before we committed the budget.\" **Action** &mdash; \"I ran a "
        "cohort analysis and found the raw LTV gap was largely **confounded** &mdash; referred users "
        "were also disproportionately from an existing high-value segment. I controlled for that, "
        "and the true referral lift was about a third of the headline. I presented it answer-first "
        "with the corrected numbers and a recommendation.\" **Result** &mdash; \"We rescoped the "
        "program to a cheaper pilot, avoided an estimated \\$400k of over-investment, and set up an "
        "A/B test to measure the real causal lift before scaling.\" Marking criteria: clear personal "
        "action ('I'), a real decision that *changed* because of the work, **quantified** impact, "
        "and ideally a glimpse of technical judgement (here, catching confounding) and communication "
        "(answer-first). Keep it under ~90 seconds spoken."},
]))
p.append(B.callout("note","The end of the road — and the start of yours",
 "You've reached the final lesson. Across fourteen tracks you've gone from \"what is data science\" "
 "to SQL, statistics, experimentation, machine learning, feature engineering, evaluation, MLOps, "
 "communication, and now the interview itself &mdash; the full arc of a job-ready data scientist. "
 "The technical skill earns the seat; the judgement and communication earn the trust; and the "
 "stories you've lived earn the offer. Go and be great &mdash; you're ready.", "&#9670;"))
LESSONS={"iv-06-behavioral":"\n".join(p)}
print("content_iv06 OK — chars:", len(LESSONS["iv-06-behavioral"]))
