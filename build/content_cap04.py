# -*- coding: utf-8 -*-
import builder as B
IMG="../assets/img/"; p=[]
p.append(B.callout("why","Capstone D — the analysis isn't done until the decision is made",
 "You built a churn model in Capstone C. Now the hard part: **getting the company to act on it.** "
 "You have 15 minutes with the **VP of Retention**. A brilliant model that produces a shrug changes "
 "nothing; a clearly-communicated one reshapes the retention budget. This capstone turns the model "
 "into a **decision**, applying every principle from Track 12.",
 "&#9654;"))
p.append(B.h2("Step 1 — Who's in the room, and what do they need?", kicker="Audience first"))
p.append(B.concept(
 "The VP of Retention doesn't care about your `class_weight` setting or your ROC curve's shape. They "
 "care about **who's going to churn, how many we can save, and what it costs**. So the message is "
 "framed in **their** terms &mdash; customers, dollars, and actions &mdash; not precision/recall. "
 "The model is the *engine*; the presentation is about the *outcome* it enables. (Save the "
 "methodology for the appendix and the technical review.)"))
p.append(B.h2("Step 2 — Lead with the answer (BLUF)", kicker="The Pyramid Principle"))
p.append(B.concept(
 "Don't build up to the recommendation over 20 slides. **State it first**, then support it:"))
p.append(B.figure(IMG+"s_comm_pyramid.png",
 "**Answer first.** Open with the recommendation and its impact; support it with the few arguments "
 "that matter; keep the model detail underneath for anyone who asks. The VP should know what you "
 "want them to do in the **first sentence**.",
 "The Pyramid Principle: recommendation on top, key arguments in the middle, model detail at the base."))
p.append(B.concept(
 "The opening line, done right:\n\n"
 "> *\"We can now identify the ~15% of customers most likely to churn **before** they leave, "
 "catching **~9 in 10** of them. If retention targets this list, we estimate saving **~1,200 "
 "customers a year &mdash; roughly \\$1.4M in retained revenue &mdash; for about \\$90k in offers.** "
 "I recommend we launch a targeted retention program against this model.\"*\n\n"
 "That single paragraph carries the decision, the mechanism, and the ROI. Everything after it "
 "*earns* the recommendation the VP already understands."))
p.append(B.h2("Step 3 — Wrap it in a story", kicker="Context → complication → resolution"))
p.append(B.concept(
 "Facts persuade better as a narrative (Track 12):\n\n"
 "- **Context**: *\"We lose about 15% of customers a year, and today we only react **after** they "
 "cancel &mdash; too late to save them.\"*\n"
 "- **Complication**: *\"But churn is predictable: the model flags would-be churners weeks early "
 "with strong accuracy (0.90 AUC), and it turns out a handful of signals &mdash; falling usage, "
 "recent support tickets, short tenure &mdash; drive most of it.\"*\n"
 "- **Resolution**: *\"So we can shift from **reactive** to **proactive**: hand retention a weekly "
 "ranked list, intervene early, and measure the saved revenue against offer cost.\"*\n\n"
 "That arc turns a model into a **change of strategy** &mdash; which is what actually gets funded."))
p.append(B.h2("Step 4 — One chart, one message", kicker="Show, don't dump"))
p.append(B.concept(
 "Resist showing the confusion matrix, the ROC curve, and five diagnostics. Pick the **one** chart "
 "that makes your case to *this* audience &mdash; and design it to deliver its message in a second:"))
p.append(B.figure(IMG+"s_comm_declutter.png",
 "**Decoration vs. communication.** For the VP, the winning chart isn't a ROC curve &mdash; it's "
 "something like *\"targeting the top 15% by risk captures ~90% of churn.\"* One highlighted point, a "
 "direct label, and the **takeaway as the title**. The technical charts belong in the appendix.",
 "A cluttered chart beside a clean one-message chart with a takeaway title."))
p.append(B.pitfall(
 "The engineer's instinct &mdash; *\"let me show you everything I built\"* &mdash; is exactly wrong "
 "in this room. Every extra chart dilutes the decision. The VP doesn't need to see the model work; "
 "they need to make a **call**. Show the one exhibit that supports the recommendation, put the rest "
 "in an appendix, and spend your minutes on the **decision and the plan**, not the diagnostics."))
p.append(B.h2("Step 5 — Anticipate the pushback", kicker="Close the decision"))
p.append(B.concept(
 "A good recommendation survives the obvious questions, so pre-empt them: *\"How confident are you?\"* "
 "(cross-validated 0.90 AUC, stable across folds); *\"What will it cost / what's the ROI?\"* (the "
 "dollar figures above); *\"How do we know it works?\"* (**run it as an experiment** &mdash; A/B the "
 "targeted intervention vs. a holdout, so we *measure* the saved revenue, tying back to Track 6). "
 "Ending on *\"here's how we'll prove it worked\"* turns your model from a claim into a testable "
 "plan &mdash; and makes the yes easy."))
p.append(B.keypoints([
 "Frame everything in the **audience's terms** &mdash; customers, dollars, actions &mdash; not "
 "precision/recall. The model is the engine; the outcome is the message.",
 "**Lead with the recommendation and its ROI (BLUF)** &mdash; the decision-maker should know the "
 "ask in the first sentence.",
 "Wrap it in a **story**: reactive-today (context) &rarr; churn-is-predictable (complication) &rarr; "
 "go-proactive (resolution).",
 "Show **one message-carrying chart**, takeaway as the title; technical diagnostics go in the "
 "**appendix**.",
 "**Pre-empt the pushback** (confidence, cost/ROI, proof) and close with an **experiment** to "
 "measure real impact.",
]))
p.append(B.quiz([
 {"q":"You have 15 minutes with the VP of Retention. Which opening is strongest?",
  "options":[
   {"t":"\"We can flag ~90% of churners before they leave; targeting them could save ~$1.4M/year for "
        "~$90k in offers — I recommend we launch a targeted program.\"","correct":True,
    "why":"Correct. It's BLUF: the recommendation, the mechanism, and the ROI in the first breath, in "
          "the VP's language (customers and dollars). Everything after earns a conclusion they "
          "already grasp."},
   {"t":"\"Let me walk you through our feature engineering and model selection process first.\"",
    "why":"That's methodology for a technical audience. The VP needs the decision and impact up "
          "front; method belongs in the appendix."},
   {"t":"\"We tested five models and the gradient boosting had the best ROC-AUC of 0.904.\"",
    "why":"Model-selection detail, framed in metrics the VP doesn't act on. Lead with the business "
          "outcome, not the leaderboard."},
   {"t":"\"Here are twelve charts of our churn analysis — what do you think?\"",
    "why":"A data dump that offloads the synthesis onto the VP. Deliver a recommendation with one "
          "supporting exhibit instead."}]},
 {"q":"The VP asks \"how do we know this will actually save customers?\" Best answer?",
  "options":[
   {"t":"\"Let's run it as an experiment — A/B the targeted intervention against a holdout and "
        "measure the retained revenue.\"","correct":True,
    "why":"Correct. It converts a model claim into a measurable result (Track 6): randomize the "
          "intervention, compare to a control, and quantify saved revenue. That's the rigorous, "
          "credible close &mdash; and it makes the 'yes' low-risk."},
   {"t":"\"The model has 0.90 AUC, so it definitely works.\"",
    "why":"AUC measures prediction quality, not that the *intervention* saves customers. You must "
          "test the action, not just the model."},
   {"t":"\"Trust me, the analysis is solid.\"",
    "why":"Asserting confidence isn't evidence. Propose an experiment that measures real business "
          "impact."},
   {"t":"\"We can't really know until we roll it out to everyone.\"",
    "why":"Full rollout with no control can't isolate the effect. A holdout/A-B design measures it "
          "without betting the whole base."}]},
]))
p.append(B.practice([
 {"q":"Write a 3-sentence executive summary of the churn project for the VP of Retention (assume the "
      "Capstone C results: ~0.90 AUC, ~90% of churners caught in the top-risk group).",
  "sol":"A strong answer leads with the ask and ROI, then the mechanism, then the proof plan &mdash; "
        "in business terms. Example: **\"We built a model that flags the ~15% of customers most "
        "likely to churn before they cancel, catching about 9 in 10 of them weeks in advance. If "
        "retention targets this weekly list with proactive offers, we estimate saving roughly 1,200 "
        "customers and \\$1.4M in annual revenue for about \\$90k in offer cost. I recommend we "
        "launch it as an A/B-tested program so we can measure the retained revenue directly &mdash; "
        "and scale it if the numbers hold.\"** Marking criteria: sentence 1 = the outcome/ask (not "
        "the method), sentence 2 = quantified impact vs. cost, sentence 3 = how we'll prove it. No "
        "jargon (AUC, recall) in the summary itself &mdash; that lives in the appendix. It should "
        "read as a **decision**, not a report."},
 {"q":"The VP says: \"This sounds expensive and I'm not convinced the model is right. Why should I "
      "fund it?\" Structure your response.",
  "sol":"Don't get defensive &mdash; **de-risk the ask**. **(1) Reframe cost as ROI:** \"The program "
        "is ~\\$90k in offers against ~\\$1.4M in revenue we're currently losing &mdash; even if the "
        "model is *half* as good as estimated, it pays for itself many times over.\" **(2) Address "
        "confidence honestly:** \"You're right to be skeptical &mdash; that's why the estimate is "
        "cross-validated and stable, and why I'm *not* asking you to bet the whole base.\" **(3) "
        "Shrink the commitment:** \"Let's fund a **small A/B pilot** &mdash; target the model's "
        "top-risk list for a fraction of customers, hold out a control, and measure actual saved "
        "revenue over 8 weeks. If it works, we scale; if it doesn't, we've spent little and "
        "learned.\" The communication skills: convert cost into **ROI**, meet skepticism with a "
        "**measurable test** rather than assertion, and lower the barrier to 'yes' by making the "
        "first step **small and reversible**. You're selling a *decision path*, not demanding blind "
        "faith."},
]))
p.append(B.callout("note","What this capstone — and this course — proves you can do",
 "You took a technical result and turned it into a **funded decision**: audience-framed, "
 "answer-first, wrapped in a story, supported by one honest chart, and closed with an experiment to "
 "prove it. Chain all four capstones together &mdash; explore (A), experiment (B), model (C), "
 "communicate (D) &mdash; and you've walked the entire arc of a professional data scientist: from "
 "raw data to a decision the business acts on. That arc is the job. You're ready.", "&#9670;"))
LESSONS={"cap-04-present":"\n".join(x for x in p if x)}
print("content_cap04 OK — chars:", len(LESSONS["cap-04-present"]))
