# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "People don't remember tables; they remember **stories**. A dozen well-structured facts vanish from "
 "memory by the elevator; a single clear narrative &mdash; *\"here's where we were, here's what we "
 "found, here's what we should do\"* &mdash; sticks and spreads. Turning analysis into a story isn't "
 "dumbing it down; it's the difference between a report that gets **acted on** and one that gets "
 "filed. This lesson is how to build that narrative."))
p.append(B.h2("The narrative arc", kicker="Context → complication → resolution"))
p.append(B.concept(
 "Every persuasive data story follows the same three-beat arc &mdash; the same one screenwriters and "
 "consultants use:\n\n"
 "- **Context** &mdash; the shared starting point everyone agrees on. *\"Our free-trial conversion "
 "has been flat at 8% for a year.\"*\n"
 "- **Complication** &mdash; the tension, the surprising finding, the thing that changed. *\"But we "
 "discovered trials that use Feature A convert at 22% &mdash; and 70% of users never find it.\"*\n"
 "- **Resolution** &mdash; what to do about it. *\"If we surface Feature A during onboarding, we "
 "project conversion rises to ~14%. Here's the plan.\"*\n\n"
 "Context sets the stage, the complication creates the *\"oh!\"*, and the resolution gives them "
 "somewhere to go. Miss the complication and it's boring; miss the resolution and it's a problem "
 "with no exit. The arc is what turns numbers into momentum."))
p.append(B.h2("One message per exhibit", kicker="The headline is the point"))
p.append(B.concept(
 "The most common presentation sin is the **data dump**: ten charts, each showing 'everything,' none "
 "making a point. The fix is a discipline: **every slide, chart, or section makes exactly one "
 "point**, and that point is its **headline**. Don't title a slide *\"Regional Revenue Data\"* "
 "(a topic); title it *\"The West drove 80% of Q3 growth\"* (the message). If someone read only your "
 "headlines, top to bottom, they should get the entire story. The chart is merely the *evidence* for "
 "the headline &mdash; not a puzzle for the audience to solve."))
p.append(B.pitfall(
 "**\"Here's all the data, you decide\"** feels safe and humble &mdash; and it's an abdication. You "
 "are the person who spent two weeks in this data; the audience spent two minutes. Handing them "
 "twelve unlabeled charts and no conclusion isn't neutrality, it's making *them* do the synthesis "
 "you were hired to do. Have a **point of view**, state it, and support it. (You can and should note "
 "uncertainty &mdash; but a recommendation with caveats beats a data dump with none.)"))
p.append(B.h2("The 'so what' chain, again — because it's everything", kicker="Finding → meaning → action"))
p.append(B.concept(
 "The engine inside every good data story is the chain from **finding &rarr; implication &rarr; "
 "action**. Keep asking *\"so what?\"* until you reach something a human can **do**:\n\n"
 "*\"Retention dropped 5 points\"* &mdash; so what? &mdash; *\"...concentrated entirely in users who "
 "hit the new paywall\"* &mdash; so what? &mdash; *\"...they're churning before experiencing the "
 "product's value\"* &mdash; so what? &mdash; **\"...so we should move the paywall later in the "
 "journey; here's the test to prove it.\"**\n\n"
 "Each *\"so what\"* climbs from raw fact toward a decision. Stop climbing too early and you've "
 "handed someone a worry with no handle; climb all the way and you've handed them a lever."))
p.append(B.keypoints([
 "People remember **stories**, not tables &mdash; narrative is what makes analysis get **acted on**.",
 "Structure every data story as **context &rarr; complication &rarr; resolution**: the agreed "
 "starting point, the surprising finding, the recommended action.",
 "**One message per chart/slide**, and make it the **headline** (\"West drove 80% of growth,\" not "
 "\"Regional Revenue\"). Headlines alone should tell the whole story.",
 "Avoid the **data dump** &mdash; \"here's everything, you decide\" abdicates the synthesis you were "
 "hired for. Have a point of view.",
 "Drive everything with the **\"so what\" chain**: keep asking until you reach an action a human can "
 "take.",
]))
p.append(B.quiz([
 {"q":"Which slide title best follows the 'one message, and it's the headline' principle?",
  "options":[
   {"t":"\"Onboarding drop-off doubles after step 3 — we should cut it to two steps\"","correct":True,
    "why":"Correct. It states a single, specific message *and* points to the action &mdash; the "
          "headline carries the point, so the chart just proves it. Read alone, it advances the "
          "story."},
   {"t":"\"Onboarding Funnel Metrics\"",
    "why":"That's a topic label, not a message. It tells the audience what they're looking at but not "
          "what to conclude &mdash; they have to find the point themselves."},
   {"t":"\"Analysis of User Data (Q3)\"",
    "why":"Generic and message-free. A good headline states the *finding*, not the subject matter."},
   {"t":"\"Various Charts\"",
    "why":"Says nothing at all. Every exhibit should headline its single point."}]},
 {"q":"You present 12 detailed charts and conclude \"so, lots to think about — what do you all "
      "think?\" Why is this weak?",
  "options":[
   {"t":"It's a data dump that offloads synthesis onto the audience instead of delivering a point of "
        "view","correct":True,
    "why":"Correct. You have the deepest context; presenting everything with no conclusion makes the "
          "audience do your synthesis. Lead them to an insight and a recommendation (with caveats), "
          "not a pile of exhibits."},
   {"t":"12 charts is too few",
    "why":"The problem isn't quantity &mdash; it's the absence of a message and recommendation. Even "
          "one chart with a clear point beats twelve without."},
   {"t":"Asking for input is always wrong",
    "why":"Discussion is fine &mdash; *after* you've delivered a clear point of view. Opening with "
          "'you decide' and no synthesis is the weakness."},
   {"t":"Charts should never be shown to executives",
    "why":"Charts are great &mdash; when each makes one headlined point supporting your message. The "
          "issue is the dump, not the medium."}]},
]))
p.append(B.practice([
 {"q":"Structure a data story using context → complication → resolution for this situation: a "
      "subscription app whose revenue is up but whose active-user count is quietly falling.",
  "sol":"**Context** (shared ground): \"Revenue hit a record last quarter, up 12% &mdash; on the "
        "surface, our best quarter yet.\" **Complication** (the tension/insight): \"But that growth "
        "is masking a problem: monthly active users fell 8%, and revenue only rose because we raised "
        "prices. We're extracting more from a **shrinking** base &mdash; a trend that reverses "
        "hard.\" **Resolution** (the action): \"We should treat engagement, not price, as the Q4 "
        "priority: reinvest some of the pricing upside into the top-two retention drivers we "
        "identified, and set a target to return MAU to growth. Here's the proposed plan and the "
        "metric we'll watch.\" A strong answer makes the complication genuinely surprising (revenue "
        "up but health down) and lands on a concrete, decision-ready resolution &mdash; not just "
        "\"engagement is concerning.\""},
 {"q":"Run the 'so what' chain on this finding until it reaches an action: \"Support ticket volume "
      "rose 30% last month.\"",
  "sol":"**Finding:** support tickets +30%. *So what?* &rarr; \"...and 60% of the new tickets are "
        "about one thing: the new checkout flow.\" *So what?* &rarr; \"...users are confused by the "
        "redesigned payment step and can't complete purchases, so this is costing sales, not just "
        "support time.\" *So what?* &rarr; **\"...we should roll back or fix the checkout payment "
        "step this week, and A/B test the fix &mdash; every day it's live we're losing conversions "
        "and burning support capacity.\"** The chain travels from a raw volume number to a **root "
        "cause** to a **business consequence** to a **specific, time-bounded action**. A good answer "
        "doesn't stop at 'tickets are up' (a worry) &mdash; it climbs to something the team can "
        "actually do tomorrow."},
]))
p.append(B.deepdive(
 B.concept(
  "**Why narrative beats bullet points, cognitively.** A story supplies **causal links** &mdash; "
  "*this* happened *because* of *that*, *therefore* we should act &mdash; and the mind stores and "
  "recalls linked, causal information far better than isolated facts. Context&rarr;complication&rarr;"
  "resolution isn't a rhetorical trick; it mirrors how people naturally reason about change and what "
  "to do about it. It also creates a small amount of **tension** (the complication) that holds "
  "attention until the resolution releases it. This is why the same three facts land as a memorable "
  "recommendation when structured as a story and evaporate when listed as bullets: the structure "
  "does the cognitive work of making them *stick* and *mean something*.") +
 B.concept(
  "**Tailoring the story's altitude to the room.** The arc stays the same, but its **resolution** "
  "and detail change with the audience. For an **executive**, the resolution is a decision and its "
  "business impact (\"reallocate \\$2M, projected +15% conversions\"), with the complication stated "
  "in outcome terms. For a **product team**, the resolution is what to build and test next, and the "
  "complication is about user behaviour. For **technical peers**, you add the methodological "
  "complication (\"the naive analysis was confounded, here's how we corrected it\") because trust "
  "*is* the point for them. Same three beats, re-pitched. The master skill is holding one true "
  "narrative and choosing, for each audience, which parts to foreground &mdash; never distorting the "
  "facts, only re-aiming the emphasis toward the decision *they* own."),
 title="Deep dive: the cognitive science of narrative, and re-pitching the arc per audience"))
LESSONS={"comm-02-narrative":"\n".join(p)}
print("content_comm02 OK — chars:", len(LESSONS["comm-02-narrative"]))
