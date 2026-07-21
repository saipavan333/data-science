# -*- coding: utf-8 -*-
import builder as B
IMG="../assets/img/"; p=[]
p.append(B.why(
 "A chart has **one job**: deliver a single message to a reader's brain, fast. Most charts fail at "
 "it &mdash; not because the data is wrong, but because decoration, clutter, and rainbow colours "
 "bury the point. The good news: making charts that *communicate* is mostly **subtraction**, and a "
 "handful of principles will put you ahead of almost everyone. This is data visualization for "
 "**persuasion**, which is a different craft from the exploratory plotting in the EDA track."))
p.append(B.h2("Match the chart to the message", kicker="A tiny decision tree"))
p.append(B.concept(
 "Chart choice is mostly about what **relationship** you're showing &mdash; and a few defaults cover "
 "the vast majority of cases:\n\n"
 "- **Comparison** across categories &rarr; **bar chart** (the honest workhorse; start the axis at "
 "zero).\n"
 "- **Trend** over time &rarr; **line chart**.\n"
 "- **Relationship** between two variables &rarr; **scatter plot**.\n"
 "- **Composition** (parts of a whole) &rarr; a **stacked bar** &mdash; and usually **not** a pie "
 "(humans compare lengths far better than angles; pies fail past 2&ndash;3 slices).\n\n"
 "When in doubt, a plain bar or line almost always beats something fancier. Exotic chart types "
 "impress the maker and confuse the reader."))
p.append(B.h2("Decoration vs. communication", kicker="The power of subtraction"))
p.append(B.concept(
 "The single biggest upgrade to most charts is **removing things**. Every non-data pixel &mdash; "
 "heavy gridlines, 3D effects, drop shadows, a rainbow of colours, a redundant legend &mdash; is "
 "\"chartjunk\" that competes with your message. Compare the *same data* told two ways:"))
p.append(B.figure(IMG+"s_comm_declutter.png",
 "**Same data, two outcomes.** *Left*: rainbow bars, gridlines, a legend that just repeats the axis, "
 "and a topic title &mdash; the reader has to hunt for the point. *Right*: everything greyed except "
 "the **one bar that matters**, a direct value label, and the **takeaway as the title**. The clean "
 "version delivers its message in under a second.",
 "A cluttered rainbow bar chart beside a clean version with one highlighted bar and a takeaway title."))
p.append(B.concept(
 "The decluttering checklist: **remove** gridlines and borders you don't need; **kill** 3D and "
 "shadows always; **grey out everything and highlight only what carries the message** (colour is "
 "your most powerful tool &mdash; spend it on the *one* thing you want seen); **label directly** "
 "instead of forcing eyes to a legend; and make the **title the takeaway**, not the topic. Each of "
 "these is subtraction or redirection &mdash; you're removing noise so the signal lands."))
p.append(B.tip(
 "The \"**grey everything, highlight one**\" trick is the fastest way to make any chart communicate. "
 "Our eyes jump to the one saturated element among muted ones, so a single coloured bar (or line) in "
 "a field of grey *pre-attentively* tells the reader where to look before they've consciously read "
 "anything. Colour should mean *\"pay attention here\"* &mdash; never *\"I had five categories so I "
 "used five colours.\"*"))
p.append(B.h2("Honesty in charts", kicker="Don't mislead, even accidentally"))
p.append(B.pitfall(
 "Charts can lie without anyone intending it. The classic offenders: a **truncated y-axis** on a bar "
 "chart that turns a 2% difference into a visual landslide (bars must start at **zero**); "
 "**inconsistent scales** across compared charts; **cherry-picked time windows** that manufacture a "
 "trend; and **dual axes** rigged to imply a correlation. Your credibility is your most valuable "
 "asset &mdash; a chart that technically shows the data but *misleads the eye* will eventually be "
 "caught, and it takes your trustworthiness down with it. Design for the honest impression, not just "
 "the technically-defensible one."))
p.append(B.keypoints([
 "A chart's job is **one message, fast** &mdash; persuasion visuals differ from exploratory ones.",
 "Match type to relationship: **bar** (comparison), **line** (trend), **scatter** (relationship), "
 "**stacked bar** (composition) &mdash; usually **not** a pie.",
 "The biggest upgrade is **subtraction**: remove chartjunk (gridlines, 3D, shadows, rainbow, "
 "redundant legends).",
 "**Grey everything, highlight the one thing** that carries the message; **label directly**; make "
 "the **title the takeaway**.",
 "Be **honest**: bars start at **zero**, consistent scales, no cherry-picked windows &mdash; a "
 "misleading chart costs your credibility.",
]))
p.append(B.quiz([
 {"q":"You want to show that one product line vastly outsells four others. Best design?",
  "options":[
   {"t":"A bar chart (axis from zero) with the winning bar highlighted in colour and the rest greyed, "
        "titled with the takeaway","correct":True,
    "why":"Correct. Bars compare magnitudes honestly; greying the others and colouring the winner "
          "directs the eye instantly; a takeaway title states the point. Clean, honest, one message."},
   {"t":"A 3D pie chart with all five slices in different colours",
    "why":"Pies make magnitude comparison hard (angles vs. lengths), 3D distorts them further, and "
          "five rainbow slices bury the message. Avoid."},
   {"t":"A bar chart with the y-axis starting at 90% of the top value to 'emphasise' the gap",
    "why":"Truncating the axis exaggerates differences and misleads &mdash; a credibility risk. Bars "
          "must start at zero."},
   {"t":"A table of the five numbers",
    "why":"A table doesn't leverage pre-attentive comparison; for 'one vastly outsells the rest,' a "
          "highlighted bar communicates far faster."}]},
 {"q":"Why is 'grey everything, highlight one' so effective?",
  "options":[
   {"t":"The eye is drawn pre-attentively to the single saturated element, so the reader sees the "
        "point before consciously reading","correct":True,
    "why":"Correct. A lone colour among greys pops out automatically (pre-attentive processing), "
          "directing attention to your message instantly. Colour becomes a spotlight, not "
          "decoration."},
   {"t":"Grey is the most attractive colour",
    "why":"It's not about aesthetics &mdash; it's that muting everything else makes the one coloured "
          "element pop, guiding the eye."},
   {"t":"It reduces the file size of the chart",
    "why":"Irrelevant to communication. The benefit is directing attention via contrast, not "
          "file size."},
   {"t":"Because colour-blind users can't see colours",
    "why":"Accessibility matters, but the principle here is that selective colour creates a "
          "pre-attentive focal point for everyone."}]},
]))
p.append(B.practice([
 {"q":"A colleague's slide shows a bar chart of monthly signups with a y-axis running from 4,800 to "
      "5,000, making a tiny change look dramatic, plus rainbow bars and heavy gridlines. List the "
      "problems and how you'd fix each.",
  "sol":"**Problems & fixes:** **(1) Truncated y-axis (4,800&ndash;5,000)** &mdash; visually inflates "
        "a ~4% change into a cliff; **fix:** start the axis at **zero** so the real magnitude shows "
        "(if the small change is genuinely the story, use a line chart or annotate the % change "
        "honestly). **(2) Rainbow bars** &mdash; colour with no meaning adds noise; **fix:** make all "
        "bars a single neutral colour and **highlight only** the month that matters. **(3) Heavy "
        "gridlines** &mdash; chartjunk competing with the data; **fix:** remove or lighten them to "
        "faint references. **(4) Likely a topic title** &mdash; **fix:** retitle with the takeaway "
        "(\"Signups flat for 6 months &mdash; growth has stalled\"). Bonus: **label the key value "
        "directly** instead of relying on axis reading. The theme: **subtract noise, tell the truth "
        "about magnitude, and put the message in the title.**"},
 {"q":"When would a table be a better choice than a chart, and why?",
  "sol":"A **table** wins when the audience needs to **look up or compare precise values**, when "
        "there are **few numbers** that each matter exactly, or when the data mixes **different "
        "units** that don't share a visual scale. Examples: a financial summary where the reader "
        "needs the exact figures (revenue, margin, headcount by division), a pricing sheet, or a "
        "small set of KPIs with their targets. Charts excel at showing **shape, trend, and "
        "comparison at a glance** &mdash; the *gestalt* of the data &mdash; but they blur exact "
        "values. So: if the message is \"notice this pattern/comparison,\" chart it (with one "
        "highlighted point); if the message is \"here are the specific numbers you'll reference,\" "
        "table it. And never use a chart merely to look sophisticated when three numbers in a "
        "sentence would be clearer."},
]))
p.append(B.deepdive(
 B.concept(
  "**The data-ink ratio, made practical.** Edward Tufte's idea: maximise the share of a chart's ink "
  "devoted to actual **data** versus decoration, and erase 'non-data ink' wherever it doesn't cost "
  "understanding. In practice that means faint or absent gridlines, no chart borders, no background "
  "fills, no 3D, thin axes, and direct labels instead of legends. You're not making the chart "
  "*prettier* for its own sake &mdash; you're removing everything the eye has to *filter out* to "
  "reach the signal. A useful drill: take any chart and ask of each element, *\"if I delete this, do "
  "I lose information?\"* If not, delete it. What remains communicates faster.") +
 B.concept(
  "**Colour is a language &mdash; use it deliberately.** Beyond 'highlight one thing,' a few rules "
  "keep colour honest and legible: use a **sequential** scale for ordered quantities (light&rarr;"
  "dark = low&rarr;high), a **diverging** scale when there's a meaningful midpoint (e.g. below/above "
  "target), and **categorical** colours only for genuinely unordered groups &mdash; sparingly, "
  "because more than ~6 becomes unreadable. Keep a **consistent** colour meaning across a deck (if "
  "blue = our product on slide 3, don't make it the competitor on slide 7). And design for "
  "**colour-blind** viewers (~8% of men): don't rely on red/green alone &mdash; add labels, "
  "patterns, or a colour-blind-safe palette. Treated as a language with grammar, colour guides "
  "understanding; sprinkled for decoration, it destroys it."),
 title="Deep dive: the data-ink ratio and using colour as a deliberate language"))
LESSONS={"comm-03-deck":"\n".join(x for x in p if x)}
print("content_comm03 OK — chars:", len(LESSONS["comm-03-deck"]))
