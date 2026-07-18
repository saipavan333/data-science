# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "A chart is a tool with one job: make the answer to a question **obvious at a glance**. Pick the "
 "right chart and a pattern leaps out; pick the wrong one and you bury the insight or, worse, "
 "imply something false. The good news is that choosing well isn't taste &mdash; it's a short "
 "decision based on *what question you're asking*. This lesson gives you that decision and the "
 "handful of charts that answer almost everything."))

p.append(B.h2("Match the chart to the question", kicker="Method"))
p.append(B.concept(
 "Don't start from 'what chart looks nice?' Start from 'what do I want to know?' Five question "
 "types cover the vast majority of data work, and each has a natural chart:"))
p.append(B.figure(IMG+"s_eda_chooser.png",
 "**From question to chart.** Distribution &rarr; histogram; comparison &rarr; bar; relationship "
 "&rarr; scatter; trend over time &rarr; line; composition &rarr; stacked/grouped bar. Identify "
 "your question and the chart follows.",
 "Decision tree mapping question types to chart types."))

p.append(B.h2("The five workhorses", kicker="Concept"))
p.append(B.concept(
 "You can go a very long way with just five chart types. Know what each is *for*:\n\n"
 "- ~Histogram~ &mdash; the **distribution** of one numeric variable (shape, center, spread, "
 "skew). A boxplot is its cousin when you care about outliers or comparing groups.\n"
 "- ~Bar chart~ &mdash; **comparison** of a value across categories. Sort the bars unless the "
 "categories have a natural order.\n"
 "- ~Scatter plot~ &mdash; the **relationship** between two numeric variables (the picture behind "
 "correlation, Lesson 4.10).\n"
 "- ~Line chart~ &mdash; a **trend** over time (or any ordered axis).\n"
 "- ~Boxplot~ &mdash; **spread and outliers**, especially compared across groups (Lesson 4.2)."))
p.append(B.figure(IMG+"s_eda_gallery.png",
 "**The five workhorses, each answering its kind of question.** Reach for the one whose job "
 "matches your question; the fancy chart types are rarely worth the loss of clarity.",
 "A gallery of histogram, bar, scatter, line, and box charts."))

p.append(B.h2("When NOT to use a pie chart", kicker="Pitfall"))
p.append(B.concept(
 "Pie charts are the most over-used, least effective common chart. The reason is human "
 "perception: we judge **lengths** accurately but **angles and areas** poorly. When slices are "
 "close in size, a pie makes you squint; a sorted bar chart makes the ranking instant."))
p.append(B.figure(IMG+"s_eda_pie.png",
 "**Bars beat pies.** Five near-equal shares are a blur as a pie but an obvious ranking as a "
 "sorted bar chart. Reserve pies for a few wildly different slices, if ever &mdash; a bar chart "
 "is almost always clearer.",
 "A hard-to-read pie beside a clear sorted bar chart of the same data."))

p.append(B.h2("Choose, then plot", kicker="Worked example"))
p.append(B.concept(
 "The question here is *'how does revenue compare across categories?'* &mdash; a **comparison**, "
 "so the chooser says **bar chart** (sorted). First the data, then the plotting code you'd run "
 "(press **Run** to render it in your browser)."))
_c,_o=_run(r'''
import pandas as pd

revenue = pd.Series({"Electronics": 399, "Apparel": 125, "Home": 118,
                     "Sports": 113, "Beauty": 47}, name="revenue_k")

# Comparison across categories -> sort, so the ranking is obvious:
print(revenue.sort_values(ascending=False).to_string())
''')
p.append(B.code_example(_c,_o,filename="choose_chart.py"))
p.append(B.code_example(
'''import matplotlib.pyplot as plt

# A sorted horizontal bar chart — ideal for comparing categories.
revenue.sort_values().plot.barh(color="#0e8f8a")
plt.xlabel("revenue ($000s)")
plt.title("Revenue by category")
plt.tight_layout()
plt.show()    # press Run to render it''',
 output="", filename="plot_bar.py", out_label="Output"))
p.append(B.note(
 "Sorting the bars is a small touch with a big payoff: the eye reads the ranking instantly. "
 "Horizontal bars (`.barh`) also keep long category labels readable. Little choices like these "
 "are the difference between a chart that informs and one that merely decorates."))

p.append(B.keypoints([
 "Choose a chart from your **question**: distribution &rarr; histogram; comparison &rarr; bar; "
 "relationship &rarr; scatter; trend &rarr; line; composition &rarr; stacked bar.",
 "Five workhorses cover most needs: **histogram, bar, scatter, line, boxplot**.",
 "**Sort bar charts** (unless categories have a natural order) so the ranking is obvious.",
 "**Avoid pie charts** &mdash; people compare lengths far better than angles; a sorted bar is "
 "clearer.",
 "Pick the chart that answers the question, not the one that looks fanciest.",
]))

p.append(B.quiz([
 {"q":"You want to show how a single numeric variable &mdash; customer age &mdash; is "
      "distributed. Which chart?",
  "options":[
   {"t":"A histogram","correct":True,
    "why":"Correct. A histogram shows the distribution of one numeric variable: its shape, center, "
          "spread, and skew. (A boxplot is the alternative if you mainly care about outliers.)"},
   {"t":"A line chart",
    "why":"Line charts show a trend over an ordered axis like time. Age here isn't a time series; "
          "you want its distribution, so a histogram."},
   {"t":"A pie chart",
    "why":"Pie charts show composition of a whole into a few categories, not the distribution of a "
          "continuous variable like age."},
   {"t":"A scatter plot",
    "why":"A scatter plot needs two numeric variables to show a relationship. For one variable's "
          "distribution, use a histogram."}]},
 {"q":"A stakeholder gives you a pie chart of five market shares that look about equal (roughly "
      "17–23% each). What's the better chart, and why?",
  "options":[
   {"t":"A sorted bar chart — people compare bar lengths far more accurately than pie angles","correct":True,
    "why":"Correct. With near-equal slices a pie is a blur; a sorted bar chart turns the shares "
          "into lengths the eye ranks instantly. This is the classic pie-vs-bar lesson."},
   {"t":"A 3-D exploded pie, to make the slices pop",
    "why":"3-D and explosion distort areas further, making comparison *harder*. The fix is to "
          "switch to bars, not to add visual effects."},
   {"t":"A line chart of the five shares",
    "why":"A line chart implies an ordered/continuous axis (like time). Market shares across "
          "categories are a comparison &mdash; use a (sorted) bar chart."},
   {"t":"Keep the pie; it's fine",
    "why":"With slices this close, the pie fails at its one job (showing which is biggest). A "
          "sorted bar chart is clearly better."}]},
 {"q":"You want to see whether `ad_spend` and `revenue` move together across 200 campaigns. Which "
      "chart answers that directly?",
  "options":[
   {"t":"A scatter plot of ad_spend vs revenue","correct":True,
    "why":"Correct. A scatter plot shows the relationship between two numeric variables &mdash; "
          "the picture behind correlation. You'd see the shape, strength, and any outliers."},
   {"t":"Two separate bar charts",
    "why":"Separate bars don't reveal how the two move *together*. A scatter plot puts one on each "
          "axis so the relationship is visible."},
   {"t":"A histogram of revenue",
    "why":"A histogram shows revenue's distribution alone, not its relationship with ad_spend. Use "
          "a scatter plot for two-variable relationships."},
   {"t":"A pie chart",
    "why":"Pies show composition, not relationships between two numeric variables. A scatter plot "
          "is the right tool."}]},
]))

p.append(B.practice([
 {"q":"For each question, name the chart: (a) How has monthly revenue changed over the past two "
      "years? (b) Which of our five regions has the highest average order value? (c) Is there a "
      "relationship between session length and amount spent?",
  "sol":"(a) **Line chart** &mdash; a trend over time. (b) **Bar chart** (sorted) &mdash; a "
        "comparison across categories. (c) **Scatter plot** &mdash; a relationship between two "
        "numeric variables. Each follows directly from the question type in the chooser."},
 {"q":"You have order values that are heavily right-skewed with a few huge orders. You want to "
      "show their distribution *and* make the outliers visible. What would you plot, and what's "
      "one adjustment that helps with the skew?",
  "sol":"Plot a **histogram** to show the distribution and/or a **boxplot** to highlight the "
        "outliers explicitly (points beyond the whiskers, Lesson 4.2). Because the data is "
        "right-skewed, a helpful adjustment is a **log scale** on the value axis (or plotting "
        "log(amount)), which spreads out the cluster of small orders and tames the long tail so "
        "the shape is readable."},
]))

p.append(B.deepdive(
 B.concept(
  "**Encodings, ranked by how accurately we read them.** Research by Cleveland and McGill ranked "
  "the visual channels we use to encode numbers. We judge **position along a common scale** (e.g. "
  "dots on a shared axis, bar lengths) most accurately, then **length**, then **angle/slope**, "
  "and we're worst at **area and color intensity**. That single ranking explains most chart "
  "advice: bars (length/position) beat pies (angle); a scatter (position) beats a bubble chart's "
  "sizes (area); and using color for a precise quantity is a last resort. When you must show a "
  "number precisely, encode it as a position or a length.") +
 B.concept(
  "**A few more 'which chart' cases.** For the relationship between two *categorical* variables, "
  "a grouped/stacked bar or a heatmap of counts works. For many points that overlap ("
  "overplotting), add transparency, jitter, or switch to a 2-D density/hexbin. For "
  "distributions across many groups, small multiples of histograms or a row of boxplots/violins "
  "beats cramming everything onto one axis. The five workhorses are the foundation; these are the "
  "natural next steps once the basics are automatic."),
 title="Deep dive: why bars beat pies (the perception ranking) and a few more chart choices"))

p.append(B.callout("note","Interview-ready",
 "Expect *\"what chart would you use to show X?\"* Answer by naming the **question type** first "
 "(distribution / comparison / relationship / trend / composition), then the chart. If pies come "
 "up, explain that humans compare lengths better than angles, so a sorted bar chart is almost "
 "always clearer &mdash; a crisp, well-reasoned answer.", "&#9670;"))

LESSONS={"eda-02-charts":"\n".join(p)}
