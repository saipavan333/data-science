# -*- coding: utf-8 -*-
import builder as B
p=[B.concept("Communication on one page &mdash; how analysis becomes a decision. Press **Print**.")]
p.append(B.cheatsheet("Communication & Storytelling — one-page reference",
 "The last mile, where analysis becomes **impact**: know the audience, lead with the answer, tell a "
 "story, and let one honest chart carry it.",
 [
  ("Audience first", [
    ("executive", "the answer + business impact, fast"),
    ("technical peer", "the method, so they trust it"),
    ("stakeholder", "what it means + what to do"),
    ("same truth", "different framing per room"),
  ]),
  ("Structure (Pyramid / BLUF)", [
    ("answer first", "recommendation, then arguments, then data"),
    ("first-sentence test", "would they know the ask?"),
    ("finding &ne; insight", "add the **'so what'** &rarr; action"),
    ("so-what chain", "fact &rarr; why it matters &rarr; do this"),
  ]),
  ("Story arc", [
    ("context", "the shared starting point"),
    ("complication", "the surprising finding / tension"),
    ("resolution", "the recommended action"),
    ("no data dumps", "have a point of view"),
  ]),
  ("Charts that communicate", [
    ("one message", "and it's the **title** (a takeaway)"),
    ("subtract", "kill gridlines, 3-D, rainbow, chartjunk"),
    ("grey + highlight one", "colour = 'look here'"),
    ("label directly", "not via a legend"),
    ("bars start at zero", "or you mislead the eye"),
  ]),
  ("Match chart to message", [
    ("comparison", "bar &middot; **trend** line"),
    ("relationship", "scatter &middot; **composition** stacked bar"),
    ("precise lookups", "a table beats a chart"),
  ]),
 ]))
LESSONS={"comm-05-cheat":"\n".join(p)}
print("commcheat OK")
