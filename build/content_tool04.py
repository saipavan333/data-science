# -*- coding: utf-8 -*-
import builder as B
p=[]

p.append(B.why(
 "The **Jupyter notebook** is where data science thinks out loud: run a cell, see a chart, adjust, "
 "run again &mdash; a conversation with your data. It's the right tool for **exploration**, teaching, "
 "and sharing analysis. But its greatest strength &mdash; running cells in any order, keeping "
 "everything in memory &mdash; is also a **trap** that produces results nobody (including you) can "
 "reproduce. This lesson is how to get the good without the bad."))

p.append(B.h2("What a notebook actually is", kicker="Cells, kernel, state"))
p.append(B.concept(
 "A notebook is a list of **cells** (code or Markdown prose) attached to a **kernel** &mdash; a live "
 "Python process that remembers everything you've run. Run a code cell and its variables persist in "
 "the kernel's memory, available to every later cell. That persistence is what makes exploration "
 "fluid: load a big dataset once, then poke at it across many cells without reloading."))
p.append(B.code_example(
 "# Cell 1 — load once, stays in memory\n"
 "import pandas as pd\n"
 "df = pd.read_csv('events.csv')\n\n"
 "# Cell 2 — explore, re-run freely without reloading\n"
 "df['event'].value_counts().head()",
 "view        4120233\nclick       2891004\npurchase     812440\nsignup       299779\nName: event, dtype: int64",
 filename="notebook"))
p.append(B.tip(
 "Two productivity multipliers: **Markdown cells** turn a notebook into a narrated report (headings, "
 "explanation, conclusions between the code), and **magics** &mdash; `%timeit some_func()` to "
 "benchmark a line, `%matplotlib inline` for charts, `!pip install X` or `!ls` to run shell commands "
 "&mdash; give you a lab bench inside the page."))

p.append(B.h2("The hidden-state trap", kicker="The #1 notebook bug"))
p.append(B.pitfall(
 "Because the kernel remembers everything, a notebook can **look** correct while being impossible to "
 "reproduce. Two classic ways it lies:\n\n"
 "- **Out-of-order execution.** You run cell 5, then edit and run cell 2, then cell 8. The numbers on "
 "screen reflect a *history no one can retrace* &mdash; the execution counts (`In [17]`) jump around. "
 "A fresh run top-to-bottom may give different results, or crash.\n"
 "- **Zombie variables.** You define `df` in a cell, later **delete that cell**, but `df` still lives "
 "in the kernel &mdash; so later cells keep working *until you restart*, when they suddenly fail with "
 "`NameError`. The notebook depended on code that no longer exists.\n\n"
 "Both mean the notebook you *see* isn't the notebook that will *run*."))
p.append(B.concept(
 "The cure is a habit: before trusting or sharing any result, **Kernel &rarr; Restart & Run All**. "
 "This wipes memory and runs every cell top-to-bottom in order &mdash; exactly how someone else will "
 "run it. If it completes cleanly and reproduces your numbers, the notebook is honest. If it breaks, "
 "you just caught a hidden-state bug **before** it embarrassed you in a review. Do this religiously."))

p.append(B.h2("When NOT to use a notebook", kicker="Right tool, right job"))
p.append(B.concept(
 "Notebooks are for **exploration and narrative**. They're the *wrong* home for code that needs to be "
 "**reused, tested, or deployed** &mdash; shared functions, data pipelines, production model code. "
 "That belongs in **`.py` modules** you can import, unit-test, and version cleanly (notebook JSON "
 "makes ugly, unreviewable Git diffs). The mature pattern: **prototype** in a notebook, then "
 "**graduate** the keep-worthy logic into `.py` files that the notebook &mdash; and production "
 "&mdash; both import."))
p.append(B.why(
 "A good tell of a senior data scientist: their notebooks are clean narratives that call into "
 "tested library code, not 400-cell monsters where all the logic lives inline. The notebook shows "
 "the *story*; the `.py` modules hold the *engine*."))

p.append(B.keypoints([
 "A notebook = **cells** + a **kernel** (a live process that remembers every variable you've run) "
 "&mdash; great for exploration.",
 "**Markdown cells** narrate; **magics** (`%timeit`, `!shell`) add power inside the page.",
 "The **hidden-state trap**: out-of-order runs and zombie variables make results that can't be "
 "reproduced.",
 "Always **Restart & Run All** before trusting or sharing &mdash; it runs top-to-bottom the way "
 "others will.",
 "Explore in notebooks; **move reusable/production code into tested `.py` modules** the notebook "
 "imports.",
]))

p.append(B.quiz([
 {"q":"Your notebook shows a perfect result, but a colleague runs it top-to-bottom and it crashes. "
      "Most likely cause?",
  "options":[
   {"t":"Hidden state — you ran cells out of order or deleted a cell whose variable still lived in "
        "the kernel","correct":True,
    "why":"Correct. The on-screen result depended on execution history or a zombie variable that a "
          "clean top-to-bottom run doesn't reproduce. 'Restart & Run All' before sharing catches "
          "exactly this."},
   {"t":"Their Python is faster than yours",
    "why":"Speed doesn't cause a crash. The issue is that a fresh, in-order run exposes a hidden-state "
          "dependency yours had in memory."},
   {"t":"Notebooks can't be shared",
    "why":"They can &mdash; the problem is the notebook wasn't verified with a clean restart, so it "
          "carried hidden state."},
   {"t":"A package version — nothing to do with execution order",
    "why":"Possible in general, but the tell-tale 'works for me, crashes fresh' is the classic "
          "out-of-order / zombie-variable trap."}]},
 {"q":"Which code is best kept in a .py module rather than living inside a notebook?",
  "options":[
   {"t":"A reusable data-cleaning function that several notebooks and the production job all call",
    "correct":True,
    "why":"Correct. Shared, reused, testable, or deployed logic belongs in an importable, "
          "version-friendly `.py` module &mdash; notebooks are for exploration and narrative, not "
          "for housing the engine."},
   {"t":"A quick one-off chart to eyeball a distribution",
    "why":"That's exactly what notebooks are *for* &mdash; fast, throwaway exploration. Keep it in "
          "the notebook."},
   {"t":"Markdown notes explaining your findings",
    "why":"Narrative belongs in the notebook alongside the analysis &mdash; that's a strength, not "
          "something to move out."},
   {"t":"An experimental plot you're still tweaking",
    "why":"Interactive tweaking is the notebook's home turf; move code out only once it's stable and "
          "reused."}]},
]))

p.append(B.practice([
 {"q":"Give three concrete habits that keep notebooks reproducible.",
  "sol":"(1) **Restart & Run All** before trusting or sharing any result &mdash; it runs cells "
        "top-to-bottom on a clean kernel, the way others will. (2) **Keep cells in logical top-to-"
        "bottom order** and avoid editing-and-rerunning earlier cells after later ones depend on "
        "them; if you must, restart. (3) **Move reusable logic into imported `.py` modules** and "
        "**pin your environment** (requirements) so the notebook's dependencies are explicit. Bonus: "
        "clear outputs before committing, or use a tool like `nbstripout`, so Git diffs stay "
        "readable."},
 {"q":"Why do notebooks produce painful Git diffs, and what can you do about it?",
  "sol":"A `.ipynb` is **JSON** that stores code, outputs, execution counts, and image data inline, "
        "so even a one-character code change produces a huge, unreadable diff (and merge conflicts "
        "in output blobs). Mitigations: **strip outputs before committing** (`nbstripout` or Kernel "
        "&rarr; Clear Outputs), keep heavy/reusable code in `.py` files that diff cleanly, and for "
        "review, share the rendered notebook (nbviewer/HTML) while versioning the logic as modules. "
        "Tools like Jupytext can even pair a notebook with a plain-`.py` representation for sane "
        "diffs."},
]))

p.append(B.deepdive(
 B.concept(
  "**Notebooks in a serious workflow.** The ecosystem has grown up: **nbconvert** turns a notebook "
  "into HTML/PDF/slides for sharing; **papermill** *parameterises and executes* notebooks "
  "programmatically (run the same analysis for 50 clients by injecting parameters), which is how "
  "notebooks earn a place in scheduled pipelines; and **Jupytext** pairs each `.ipynb` with a plain "
  "`.py` twin so version control sees clean text. VS Code and modern IDEs also run notebook cells "
  "against `.py` files directly (`# %%` cell markers), giving you the exploratory feel with "
  "diff-friendly source.") +
 B.concept(
  "**The prototype-to-production arc.** A healthy project life-cycle: explore in a notebook &rarr; as "
  "logic stabilises, extract functions into `src/` modules with tests &rarr; the notebook becomes a "
  "thin narrative that *imports* those modules &rarr; production schedules the module code (not the "
  "notebook). Nothing about this throws away the notebook &mdash; it stays as living documentation of "
  "*how* the analysis was reasoned out. The skill is knowing when a cell has earned promotion from "
  "scratchpad to tested code."),
 title="Deep dive: nbconvert/papermill/Jupytext, VS Code cells, and prototype-to-production"))

LESSONS={"tool-04-notebooks":"\n".join(p)}
print("content_tool04 OK — chars:", len(LESSONS["tool-04-notebooks"]))
