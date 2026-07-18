# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
import matplotlib
matplotlib.use("Agg")
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "The last lesson said EDA means 'plot it' &mdash; so let's learn *how* to actually make a chart. "
 "Python's plotting rests on two libraries: ~matplotlib~, the powerful engine that draws "
 "everything (with full control), and ~seaborn~, a friendly layer on top that turns common "
 "statistical charts into one line. Knowing the small core of both means you can go from a "
 "DataFrame to a clear picture in seconds &mdash; the everyday motion of exploratory work."))

p.append(B.h2("The matplotlib mental model: Figure and Axes", kicker="Concept"))
p.append(B.concept(
 "Almost all confusion with matplotlib disappears once you hold two objects in your head:\n\n"
 "- The ~Figure~ is the whole canvas &mdash; the outer container, the image you save.\n"
 "- An ~Axes~ is **one plot** inside that figure (its plotting area, with its own title, x-axis, "
 "and y-axis). A figure can hold several Axes (that's how small multiples work).\n\n"
 "The clean way to start is `fig, ax = plt.subplots()`, which hands you both. You then call "
 "methods **on the Axes** &mdash; `ax.plot(...)`, `ax.set_title(...)`, `ax.set_xlabel(...)` "
 "&mdash; to build the chart."))
p.append(B.figure(IMG+"s_eda_mpl_anatomy.png",
 "**Figure vs. Axes.** The dashed box is the Figure (the whole canvas); the plot inside is one "
 "Axes, with its title and axis labels. You draw your data onto the Axes and label its parts.",
 "Anatomy of a matplotlib chart: the Figure containing an Axes, with title and axis labels."))

p.append(B.h2("Drawing the basic charts", kicker="Worked example"))
p.append(B.concept(
 "Every chart follows the same shape: get a figure and axes, draw your data, label everything, "
 "then show or save. Here's a histogram and a bar chart in pure matplotlib (press **Run** to see "
 "them render)."))
_c,_o=_run(r'''
import numpy as np
import matplotlib.pyplot as plt

values = np.random.default_rng(0).normal(50, 12, 500)

fig, ax = plt.subplots(figsize=(7, 4))     # 1. get the Figure and one Axes
ax.hist(values, bins=30, color="#3b53d6", edgecolor="white")   # 2. draw the data
ax.set_title("Distribution of scores")     # 3. label everything
ax.set_xlabel("score")
ax.set_ylabel("count")
plt.tight_layout()
plt.show()                                  # 4. show it (or fig.savefig("chart.png"))
''')
p.append(B.code_example(_c,_o,filename="matplotlib_hist.py"))
p.append(B.note(
 "`plt.subplots()` (the **object-oriented** style, drawing on `ax`) is the habit to build. You'll "
 "also see the shorter `plt.plot(...)` / `plt.hist(...)` 'pyplot' style in tutorials &mdash; it's "
 "fine for a quick one-off, but the explicit `fig, ax` approach scales cleanly to multiple plots "
 "and is easier to customize."))

p.append(B.h2("Seaborn: statistical charts in one line", kicker="Concept"))
p.append(B.concept(
 "~seaborn~ is built on matplotlib but speaks **DataFrames**. You hand it your data and the "
 "column names, and it produces a polished statistical chart &mdash; often with one call. Its "
 "killer feature is ~hue~: pass a categorical column and seaborn automatically colors and splits "
 "by it, adding a whole variable for free. The everyday functions mirror the chart-chooser: "
 "`histplot`, `barplot`, `scatterplot`, `boxplot`, `lineplot`."))
_c,_o=_run(r'''
import pandas as pd, numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
rng = np.random.default_rng(1)

df = pd.DataFrame({
    "ad_spend": rng.uniform(0, 100, 200),
    "revenue":  rng.uniform(0, 100, 200) * 5 + 100,
    "plan":     rng.choice(["Free", "Pro"], 200),
})

# One call: scatter of two columns, colored by a third (hue) — try doing that by hand!
sns.scatterplot(data=df, x="ad_spend", y="revenue", hue="plan")
plt.title("Revenue vs. ad spend, by plan")
plt.tight_layout()
plt.show()
''')
p.append(B.code_example(_c,_o,filename="seaborn_scatter.py"))
p.append(B.tip(
 "Rule of thumb: reach for **seaborn** first for standard statistical charts on a DataFrame "
 "(histograms, boxplots, scatter with `hue`, correlation heatmaps, pair plots) &mdash; it's "
 "faster and prettier by default. Drop to **matplotlib** when you need fine control: custom "
 "annotations, exact axis tweaks, combining several plots. Because seaborn *is* matplotlib "
 "underneath, you can always grab the axes and adjust."))

p.append(B.keypoints([
 "~Figure~ = the whole canvas; ~Axes~ = one plot inside it. Start with `fig, ax = "
 "plt.subplots()` and draw on `ax`.",
 "Every chart: get figure/axes &rarr; draw data &rarr; label (title, x, y) &rarr; `show()` or "
 "`savefig()`.",
 "Prefer the **object-oriented** style (`ax.plot`) over bare `plt.plot` &mdash; it scales to "
 "multiple plots.",
 "~seaborn~ speaks DataFrames: `sns.histplot/barplot/scatterplot/boxplot`, with `hue=` to split "
 "by a category for free.",
 "Use **seaborn** for quick statistical charts, **matplotlib** for fine control &mdash; they work "
 "together.",
]))

p.append(B.quiz([
 {"q":"In matplotlib, what's the difference between the Figure and an Axes?",
  "options":[
   {"t":"The Figure is the whole canvas; an Axes is one individual plot (with its own title and "
        "x/y axes) inside it","correct":True,
    "why":"Correct. A Figure can contain one or several Axes; each Axes is a single plot you draw "
          "on and label. Holding this distinction removes most matplotlib confusion."},
   {"t":"They're two names for the same thing",
    "why":"They're distinct: the Figure is the container/canvas, an Axes is a plot inside it. A "
          "figure can hold multiple axes (small multiples)."},
   {"t":"An Axes is the x-axis; the Figure is the y-axis",
    "why":"No &mdash; an Axes is an entire plot region (both axes plus the data), not a single "
          "axis line. The Figure is the whole canvas."},
   {"t":"The Figure holds the data; the Axes holds the title only",
    "why":"You draw data onto an Axes (e.g., ax.plot), and the Axes also carries the title and "
          "labels. The Figure is the overall canvas."}]},
 {"q":"You have a tidy DataFrame and want a scatter of `x` vs `y` colored by a `group` column, "
      "fast. What's the most efficient tool?",
  "options":[
   {"t":'seaborn: sns.scatterplot(data=df, x="x", y="y", hue="group")',"correct":True,
    "why":"Correct. seaborn is DataFrame-aware and `hue` colors/splits by a category automatically "
          "&mdash; one line for what would take a manual loop in bare matplotlib."},
   {"t":"A manual matplotlib loop, plotting each group separately",
    "why":"That works but is far more code. seaborn's `hue` does it in one line; reach for "
          "matplotlib loops only when you need unusual control."},
   {"t":"A pie chart",
    "why":"A pie shows composition, not a relationship between two numeric variables. You want a "
          "scatter (with hue for the group)."},
   {"t":"print(df) and read it",
    "why":"Reading raw rows won't reveal the relationship's shape or the group pattern; a scatter "
          "with hue will."}]},
]))

p.append(B.practice([
 {"q":"Write the four conceptual steps (in matplotlib) to produce any basic chart, with the call "
      "for each.",
  "sol":"1. **Create** figure & axes: `fig, ax = plt.subplots()`. 2. **Draw** the data: e.g. "
        "`ax.hist(values)`, `ax.bar(cats, vals)`, `ax.scatter(x, y)`, or `ax.plot(t, y)`. 3. "
        "**Label**: `ax.set_title(...)`, `ax.set_xlabel(...)`, `ax.set_ylabel(...)`. 4. **Output**: "
        "`plt.show()` to display, or `fig.savefig(\"chart.png\", dpi=150, bbox_inches=\"tight\")` "
        "to save."},
 {"q":"When would you choose plain matplotlib over seaborn?",
  "sol":"When you need **fine control** that seaborn's one-liners don't give: custom annotations "
        "and arrows, precise axis limits/ticks, unusual chart types, or carefully arranged "
        "multi-panel figures. Since seaborn is built on matplotlib, a common pattern is to draw "
        "with seaborn, then grab the axes and use matplotlib calls to fine-tune (titles, "
        "annotations, limits)."},
]))

p.append(B.deepdive(
 B.concept(
  "**Two interfaces, one library.** matplotlib has a ~pyplot~ (state-based) interface &mdash; "
  "`plt.plot()`, `plt.title()` act on the 'current' axes &mdash; and an ~object-oriented~ "
  "interface where you hold `fig` and `ax` objects and call methods on them. The pyplot style is "
  "quick for a single throwaway plot; the OO style is clearer and essential once you have "
  "multiple subplots (`fig, axes = plt.subplots(2, 2)` gives a grid you index like `axes[0, 1]`). "
  "Learn the OO style as your default &mdash; every small-multiples chart in this course uses it.") +
 B.concept(
  "**Saving figures well.** `fig.savefig(\"chart.png\", dpi=150, bbox_inches=\"tight\")` controls "
  "resolution (`dpi`) and trims surrounding whitespace (`bbox_inches`). Save as **PNG** for "
  "slides and the web, **SVG/PDF** for crisp, infinitely scalable vector graphics in reports. "
  "Set the size up front with `figsize=(width, height)` in inches &mdash; a chart designed at the "
  "size it'll be shown always looks better than one squished afterward.") +
 B.concept(
  "**The grammar of graphics.** seaborn (and libraries like plotnine/ggplot, Altair, and Plotly) "
  "lean on a deep idea: a chart is built by **mapping data columns to visual channels** &mdash; "
  "x, y, color (hue), size, facet. Once you think in those mappings ('put time on x, revenue on "
  "y, region on color, channel on facets'), choosing and building charts becomes systematic "
  "rather than fiddly. It's the same column-to-channel thinking behind the perception ranking "
  "from Lesson 5.3."),
 title="Deep dive: pyplot vs. object-oriented, saving figures, and the grammar of graphics"))

p.append(B.callout("note","Interview-ready",
 "You won't be quizzed on plotting syntax much, but take-homes are judged on whether your charts "
 "are **clear and labeled**. Demonstrate the habit: titles, axis labels with units, sensible "
 "figure size, seaborn for quick statistical plots. Being able to say 'Figure vs Axes' and 'use "
 "hue to add a category' signals real fluency.", "&#9670;"))

LESSONS={"eda-06-toolkit":"\n".join(p)}
