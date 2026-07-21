# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "Knowing the **game** is half of winning it. Data-science interviews follow a predictable shape, "
 "and each round tests something specific &mdash; candidates who understand *what's really being "
 "probed* prepare the right things and answer in the right register. This bank is your map: the "
 "rounds, what each one wants, how to structure answers, and how the rest of this course feeds each "
 "stage. Walk in knowing the format and you'll out-prepare people who are simply 'good at "
 "statistics.'"))
p.append(B.h2("The five rounds", kicker="What each is really testing"))
p.append(B.concept(
 "A typical data-science loop has five stages, each with a different question behind the question:\n\n"
 "- **1. Recruiter screen** &mdash; *fit and basics.* Can you communicate, do your experience and "
 "motivation match, are salary/logistics aligned? Low technical bar; don't fumble the easy one.\n"
 "- **2. Technical screen** &mdash; *can you actually code and query?* Usually **SQL** and some "
 "Python/pandas, often live. Tests raw execution (Tracks 1&ndash;2).\n"
 "- **3. Statistics & ML deep-dive** &mdash; *do you understand, or just import?* Concept questions "
 "on stats, experimentation, and modelling &mdash; the *why*, not just the *how* (Tracks 4, 6, 8, "
 "10).\n"
 "- **4. Case / product sense** &mdash; *can you turn a vague business problem into an analysis?* "
 "Open-ended: design a metric, diagnose a drop, size a market, design an experiment (Tracks 5, 6, "
 "12).\n"
 "- **5. Behavioral** &mdash; *will we want to work with you?* Past projects, conflict, impact, "
 "values &mdash; told as structured stories (Track 12)."))
p.append(B.h2("How to answer — the meta-skills", kicker="True in every round"))
p.append(B.concept(
 "Independent of topic, a few habits mark a strong candidate:\n\n"
 "- **Clarify before you dive.** Restate the question and ask about scope/assumptions &mdash; "
 "rushing to answer the *wrong* question is the classic failure.\n"
 "- **Think out loud.** The interviewer is hiring your *reasoning*, not just your final answer. "
 "Narrate your approach; a good process with a small slip beats a silent correct guess.\n"
 "- **Structure first.** Lay out your plan (\"I'd look at three things: X, Y, Z\") before detail "
 "&mdash; it signals organised thinking and lets them redirect you early.\n"
 "- **State assumptions and tradeoffs.** \"Assuming this is a consumer app, I'd... but if it's B2B, "
 "I'd...\" shows judgement.\n"
 "- **Know when you don't know.** \"I'm not certain, here's how I'd find out\" beats bluffing every "
 "time."))
p.append(B.callout("tip","The single biggest lever",
 "**Clarify the question before answering.** In case and technical rounds alike, interviewers "
 "routinely leave the prompt vague *on purpose* &mdash; jumping straight to a solution for the "
 "problem you *assumed* is the most common way strong candidates fail. Thirty seconds of "
 "\"let me make sure I understand what we're optimising for\" changes everything.", "&#9654;"))
p.append(B.h2("Your prep map", kicker="Where this course meets each round"))
p.append(B.table(
 ["Round", "What it tests", "Prepare with"],
 [["Technical screen", "SQL &amp; Python execution", "Tracks 1&ndash;2 + Bank 14.2"],
  ["Stats &amp; ML deep-dive", "Conceptual understanding", "Tracks 4, 6, 8, 10 + Banks 14.3&ndash;14.4"],
  ["Case / product sense", "Structuring ambiguity", "Tracks 5, 6, 12 + Bank 14.5"],
  ["Behavioral", "Collaboration &amp; impact", "Track 12 + Bank 14.6"]],
 caption="Each interview round maps to tracks you've already worked through &mdash; this bank drills "
         "the question formats on top."))
p.append(B.keypoints([
 "DS interviews have **five rounds**: recruiter, technical (SQL/code), stats&amp;ML deep-dive, "
 "case/product sense, and behavioral &mdash; each testing something different.",
 "The technical screen tests **execution**; the deep-dive tests **understanding** (the *why*); the "
 "case tests **structuring ambiguity**; behavioral tests **collaboration**.",
 "**Clarify the question before answering** &mdash; solving the wrong problem is the top failure "
 "mode.",
 "**Think out loud and structure first** &mdash; they're hiring your reasoning, not just your final "
 "answer.",
 "**State assumptions and admit uncertainty** &mdash; \"here's how I'd find out\" beats bluffing.",
]))
p.append(B.quiz([
 {"q":"An interviewer asks a deliberately vague case question. What's the best first move?",
  "options":[
   {"t":"Clarify scope and what success means before proposing an approach","correct":True,
    "why":"Correct. Vagueness is often intentional. Restating the problem and pinning down "
          "assumptions/goals ensures you solve the *right* problem and signals structured thinking &mdash; "
          "the top thing they're assessing."},
   {"t":"Immediately give your best answer to show confidence",
    "why":"Rushing risks answering the wrong question. Clarify first &mdash; confident *and* wrong is "
          "the classic case-interview failure."},
   {"t":"Ask to switch to a different question",
    "why":"Ambiguity is the test, not a mistake to avoid. Engage by structuring and clarifying."},
   {"t":"Stay silent and work it out in your head",
    "why":"Silent problem-solving hides your reasoning &mdash; exactly what they want to see. Think "
          "out loud."}]},
 {"q":"The stats/ML deep-dive round is primarily testing what?",
  "options":[
   {"t":"Whether you understand concepts deeply — the 'why' behind methods, not just calling library "
        "functions","correct":True,
    "why":"Correct. This round probes conceptual depth (why regularization works, what a p-value means, "
          "bias&ndash;variance) to distinguish genuine understanding from rote tool use."},
   {"t":"How fast you can type code",
    "why":"That's the technical/coding screen. The deep-dive is about conceptual understanding, often "
          "with no coding at all."},
   {"t":"Your salary expectations",
    "why":"That's the recruiter screen. The deep-dive is purely technical understanding."},
   {"t":"Your ability to memorize formulas",
    "why":"It rewards understanding and judgement over memorization &mdash; you should be able to "
          "*explain* and *apply*, not recite."}]},
]))
p.append(B.practice([
 {"q":"You freeze on a technical question you don't fully know. What's the professional way to "
      "handle it?",
  "sol":"Don't bluff and don't shut down &mdash; **reason toward it out loud**. Say what you *do* "
        "know and how the pieces connect (\"I know it relates to X because...\"), state your best "
        "attempt while flagging uncertainty (\"I think it's Y, though I'm not fully sure\"), and "
        "&mdash; crucially &mdash; describe **how you'd find the answer** (\"in practice I'd check the "
        "docs / run a quick test / derive it from first principles like this...\"). Interviewers "
        "know you can't know everything; they're testing how you behave at the edge of your "
        "knowledge. A calm, honest, resourceful response often scores *better* than a memorised "
        "answer, because it shows exactly how you'll handle the unknowns of the actual job. What "
        "loses points is confident bluffing (they'll catch it) or freezing into silence."},
]))
LESSONS={"iv-01-overview":"\n".join(p)}
print("content_iv01 OK — chars:", len(LESSONS["iv-01-overview"]))
