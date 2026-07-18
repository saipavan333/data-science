# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "A chart can be 100% accurate and still lie. The same true numbers, framed differently, can whisper "
 "'no change' or scream 'catastrophe.' As the person holding the data you have a duty to show it "
 "**honestly** &mdash; and just as importantly, to **spot** when a chart (yours or someone "
 "else's) is misleading. This lesson is the integrity half of visualization: the common "
 "deceptions and how to avoid them."))

p.append(B.h2("Start bars at zero", kicker="Deception #1"))
p.append(B.concept(
 "The most common chart deception is ~truncating the y-axis~ &mdash; starting it somewhere above "
 "zero. For a **bar chart** this is especially dishonest, because a bar's *length* is supposed to "
 "represent the value; cut off the bottom and you destroy that correspondence, magnifying tiny "
 "differences into huge ones."))
p.append(B.figure(IMG+"s_eda_truncate.png",
 "**The same four numbers, twice.** Left, the axis starts at 0 and you see the truth: a modest "
 "~5% rise. Right, the axis starts at 95 and the identical data looks like an explosive jump. "
 "Bars must start at zero.",
 "Two bar charts of identical data: honest (axis at 0) vs misleading (axis at 95)."))

p.append(B.h2("Show the whole context", kicker="Deception #2"))
p.append(B.concept(
 "The second classic trick is ~cherry-picking~ the range: zooming into the slice of time (or the "
 "subset of data) that tells the story you want, and hiding the rest. A blip becomes a "
 "'collapse'; a pause becomes a 'boom.'"))
p.append(B.figure(IMG+"s_eda_cherry.png",
 "**Context changes everything.** The full two-year series is trending up with one small dip. "
 "Zoom into just those few months and the same data reads as a dramatic collapse. Always ask: "
 "*what's outside the frame?*",
 "A rising full time series vs a cherry-picked window that looks like a crash."))

p.append(B.h2("Other traps to avoid (and to catch)", kicker="Concept"))
p.append(B.concept(
 "A handful of other ways charts mislead &mdash; worth knowing so you neither commit them nor "
 "fall for them:\n\n"
 "- ~Dual y-axes~: plotting two series on two different scales can manufacture a 'correlation' "
 "that's just a choice of axes. Use with great caution.\n"
 "- ~Area and 3-D distortion~: making a value 'twice as big' by doubling an icon's *width* "
 "actually quadruples its area; 3-D pies and bars warp the very lengths we rely on.\n"
 "- ~Bad color and ordering~: rainbow scales imply false categories, and unsorted bars hide the "
 "ranking.\n"
 "- ~Chartjunk~: gridlines, gradients, and decorations that add ink but no information, "
 "distracting from the data."))

p.append(B.h2("The numbers behind the deception", kicker="Worked example"))
p.append(B.concept(
 "Putting a real number on the truncated-axis chart shows just how large the distortion is "
 "&mdash; and gives you the honest figure to report instead."))
_c,_o=_run(r'''
vals = [97, 98, 99, 102]          # the four quarterly numbers from the chart

change = (vals[-1] - vals[0]) / vals[0]
print(f"Q1 = {vals[0]}   Q4 = {vals[-1]}")
print(f"actual change Q1 -> Q4 = {change:.1%}")
print("Truncating the axis at 95 makes the Q4 bar look several times taller than Q1,")
print("but the real rise is only about 5%. Same data; the framing is what lies.")
''')
p.append(B.code_example(_c,_o,filename="honest_numbers.py"))
p.append(B.warn(
 "The fix is a habit, not a rule-book: **bars start at zero**; **show enough context** that the "
 "reader can't be fooled by the frame; **label axes and units**; **sort** when there's no natural "
 "order; and let the data, not decoration, carry the message. When in doubt, ask a colleague "
 "'what does this chart make you believe?' and check it matches the truth.", "&#9650;"))

p.append(B.keypoints([
 "**Bar charts must start the value axis at zero** &mdash; truncating it exaggerates small "
 "differences (the #1 deception).",
 "**Show the full context**; cherry-picking a time window or subset can turn a blip into a "
 "'crash.'",
 "Beware **dual axes**, **area/3-D distortion**, **misleading color/order**, and **chartjunk**.",
 "Label axes and units; **sort** categories without a natural order.",
 "You have a duty to show data honestly &mdash; and to spot when a chart is framed to deceive.",
]))

p.append(B.quiz([
 {"q":"A bar chart of quarterly sales (97, 98, 99, 102) starts its y-axis at 95, making Q4 look "
      "several times taller than Q1. What's wrong?",
  "options":[
   {"t":"Truncating the y-axis breaks the bar-length-equals-value correspondence, exaggerating a "
        "~5% change","correct":True,
    "why":"Correct. A bar encodes value as length, so the axis must start at 0. Starting at 95 "
          "turns a ~5% rise into a visually huge jump &mdash; technically accurate numbers, "
          "dishonest framing."},
   {"t":"Nothing — zooming in just shows detail",
    "why":"For bar charts, 'zooming in' by truncating the axis destroys the length-to-value "
          "mapping and misleads. Bars must start at zero."},
   {"t":"The colors are wrong",
    "why":"Color isn't the issue; the truncated axis is. The same chart with any colors would "
          "still exaggerate the difference."},
   {"t":"Bars can never show change over quarters",
    "why":"Bars are fine for comparing quarters; the problem is specifically the truncated axis, "
          "not the chart type."}]},
 {"q":"Is it ever acceptable to NOT start the y-axis at zero?",
  "options":[
   {"t":"Yes — for line charts of things like temperature or stock price, where zero is arbitrary "
        "and small changes are the point","correct":True,
    "why":"Correct. The zero rule is strongest for *bars* (length encodes value). For line charts "
          "tracking quantities where 0 isn't meaningful (body temperature, an index), a focused "
          "range is acceptable &mdash; just label it clearly and don't manufacture drama."},
   {"t":"No — every chart must always start at zero, no exceptions",
    "why":"Too absolute. The rule is essential for bars, but line charts of quantities where zero "
          "is arbitrary can use a focused range, honestly labeled."},
   {"t":"Yes — start anywhere you like; axes are just decoration",
    "why":"Axes are not decoration; they define meaning. Truncation is sometimes acceptable for "
          "lines, but never an 'anything goes' license &mdash; especially not for bars."},
   {"t":"Only if you're trying to make a point look bigger",
    "why":"That's exactly the dishonest use. A non-zero baseline is acceptable only when zero is "
          "genuinely arbitrary, not to exaggerate."}]},
 {"q":"A slide shows a steep 4-month 'collapse' in a metric. What's the first question to ask?",
  "options":[
   {"t":"What does the full time range look like? — the window may be cherry-picked","correct":True,
    "why":"Correct. A short window can make a minor dip look catastrophic. Seeing the full series "
          "(which might be trending up) reveals whether the 'collapse' is real or framing."},
   {"t":"Which font was used?",
    "why":"Irrelevant to whether the chart is honest. The key risk is a cherry-picked range, so "
          "ask to see the full context."},
   {"t":"Nothing — a downward line speaks for itself",
    "why":"A downward line over a chosen window can be deeply misleading. Always check what's "
          "outside the frame before believing a dramatic short-range trend."},
   {"t":"Can we make it 3-D?",
    "why":"3-D would distort it further. The right move is to widen the time range and see the "
          "full context."}]},
]))

p.append(B.practice([
 {"q":"Your manager asks you to 'make the 2% improvement look more impressive' by starting the bar "
      "chart's axis at the minimum value. How do you respond?",
  "sol":"Decline, and explain why: truncating a **bar** chart's axis breaks the length-to-value "
        "mapping and visually inflates a 2% change into something it isn't &mdash; that's "
        "misleading, and it destroys trust when noticed. Offer honest alternatives that still "
        "communicate the win: start at zero but **annotate** the +2% directly, show the trend "
        "over time as an honest line, or report the change as a clearly labeled number alongside. "
        "Persuasive *and* honest is always possible."},
 {"q":"Name three quick checks you'd run on any chart (yours or someone else's) to judge whether "
      "it's honest.",
  "sol":"(1) **Does the value axis start at zero?** &mdash; essential for bars. (2) **What's "
        "outside the frame?** &mdash; is the time range or subset cherry-picked? (3) **Are axes "
        "and units labeled, and is the encoding faithful?** &mdash; no dual-axis tricks, no "
        "area/3-D distortion, sorted bars, minimal chartjunk. A fourth good one: 'what does this "
        "chart make me believe, and is that actually true?'"},
]))

p.append(B.deepdive(
 B.concept(
  "**Data-ink and the integrity ratio.** Edward Tufte argued for maximizing the ~data-ink "
  "ratio~ &mdash; the share of a chart's ink that actually represents data &mdash; by erasing "
  "non-data decoration (heavy gridlines, backgrounds, 3-D effects, redundant labels). Less "
  "chartjunk means the data carries the message. He also defined the ~lie factor~: the size of "
  "an effect shown in the graphic divided by its size in the data. An honest chart has a lie "
  "factor of 1; a truncated-axis bar chart can push it to 5 or more.") +
 B.concept(
  "**The zero-baseline nuance.** The 'always start at zero' rule is really 'don't let the "
  "baseline distort the encoding.' For **bars**, whose length *is* the value, zero is mandatory. "
  "For **line charts**, which encode *change* via slope, a non-zero, focused range is often the "
  "honest choice &mdash; forcing a stock price or body-temperature chart to include zero would "
  "hide the very variation that matters. The test is intent and faithfulness: are you revealing "
  "the data, or manufacturing a story the numbers don't support?") +
 B.concept(
  "**Ethics is practical, not just moral.** Misleading charts aren't only wrong; they're "
  "*fragile*. The moment a smart stakeholder spots a truncated axis or a cherry-picked window, "
  "they stop trusting not just the chart but you and your whole analysis. Honest visualization is "
  "how a data scientist builds the credibility that makes their recommendations actually move "
  "decisions (the entire point of Track 12)."),
 title="Deep dive: data-ink, the lie factor, and the zero-baseline nuance"))

p.append(B.callout("note","Interview-ready",
 "A common exercise is *\"critique this chart.\"* Lead with the big two &mdash; is the bar axis "
 "truncated, and is the range cherry-picked? &mdash; then check labels, encoding faithfulness "
 "(no dual-axis or 3-D tricks), sorting, and chartjunk. Naming the *lie factor* or *data-ink "
 "ratio* signals you think about visualization integrity, not just aesthetics.", "&#9670;"))

LESSONS={"eda-03-truth":"\n".join(p)}
