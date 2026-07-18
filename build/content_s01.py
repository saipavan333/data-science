# -*- coding: utf-8 -*-
import builder as B
from examples_run import EX

IMG = "../assets/img/"
p = []

# ----------------------------------------------------------------- why ---- #
p.append(B.why(
    "Every analysis you will ever do exists to help someone **make a decision** — ship the "
    "feature or not, trust the number or not, spend the budget here or there. A data scientist "
    "is the person who turns messy, incomplete data into a decision someone can act on with "
    "confidence. This first lesson gives you the map: the workflow you'll repeat for the rest "
    "of your career, and why ~statistics~ is the engine that makes the whole thing trustworthy."))

# ----------------------------------------------------------- the job ------ #
p.append(B.h2("What a data scientist actually does", kicker="The big picture"))
p.append(B.concept(
    "Forget the hype for a moment. Stripped down, ~data science~ is a simple loop: a question "
    "comes from the business, you go get data, you wrestle it into shape, you look at it, you "
    "test an idea, you figure out how sure you can be, and you tell someone what to do. Then a "
    "new question appears and the loop turns again.\n\n"
    "Here is the whole job in one picture. Memorize this shape — every project you ever touch is "
    "a trip around it."))
p.append(B.figure(
    IMG + "s1_workflow.png",
    "**The data science workflow.** The blue steps are mostly *engineering and judgment*; the "
    "green steps — explore, model/test, and interpret — are where **statistics** lives. The "
    "dashed arrow is the truth of the job: answers create new questions.",
    "Flowchart of the data science workflow from question to decision, looping back."))
p.append(B.concept(
    "A few of those words deserve a quick definition now; we'll go deep on each later:\n\n"
    "- ~EDA~ (exploratory data analysis): looking at data with summaries and charts to learn "
    "its shape, spot problems, and form hypotheses — *before* any modeling.\n"
    "- ~Model~: a simplified description of how the data behaves, used to predict or to explain "
    "(a trend line, a classifier, a forecast).\n"
    "- ~Inference~: reasoning from a limited sample of data back to the larger world, while "
    "honestly stating how uncertain that reasoning is."))
p.append(B.tip(
    "Notice that *building a model* is one small box in step 5. Beginners think data science is "
    "mostly modeling. In reality the green steps — exploring, testing, and quantifying "
    "uncertainty — are where good judgment separates a real data scientist from someone who can "
    "call `.fit()`. That judgment is statistics. So that is where we start."))

# ----------------------------------------------------- why statistics ----- #
p.append(B.h2("Why statistics is the engine", kicker="Motivation"))
p.append(B.concept(
    "Let's make the need for statistics concrete. Suppose your team changed the checkout button "
    "and ran the old version (**A**) against the new one (**B**). Here is the kind of tiny "
    "analysis you'll write on day one — load the data, aggregate it, and compute the result."))
p.append(B.code_example(EX["s11_ab"][0], EX["s11_ab"][1], filename="why_statistics.py"))
p.append(B.concept(
    "Button **B** converted at 8.1% versus 7.3% for A — an **11.7% relative lift**. Ship it, "
    "right?\n\n"
    "Not so fast. Those numbers came from a *sample* of a few thousand visitors on a few days. "
    "If you had watched a different week, you'd have gotten slightly different numbers. So the "
    "real question isn't *\"is B bigger here?\"* — it obviously is. The question is: *\"is B "
    "genuinely better, or did random luck hand us this gap?\"* That single question — telling "
    "**signal** from **noise** — is what statistics answers, and it is the most valuable skill "
    "you will build in this entire course."))
p.append(B.pitfall(
    "The most expensive mistake in data work is treating a number from a sample as if it were "
    "the exact truth about the world. A conversion rate, an average, a correlation — each one "
    "wobbles depending on which data happened to land in your sample. Statistics is the "
    "discipline of saying *how much* it wobbles, so you don't bet the company on noise."))

# ------------------------------------------------------- the map ---------- #
p.append(B.h2("How this course is built", kicker="Your path"))
p.append(B.concept(
    "The eleven tracks aren't a random pile of topics — they're stacked so each one rests on the "
    "one before it. Roughly, they map onto the workflow you just saw:\n\n"
    "- **Get & clean data** &rarr; Track 1 (Python, NumPy & Pandas).\n"
    "- **Explore** &rarr; Track 5 (EDA & Visualization), powered by Track 4 (Statistics).\n"
    "- **Model / test** &rarr; Tracks 8–8 (Machine Learning, A/B Testing, Feature Engineering, "
    "Evaluation, Causal Inference).\n"
    "- **Interpret & decide** &rarr; Track 12 (Communication), then Tracks 14–11 (Interview "
    "prep and Capstones) prove you can do the whole loop yourself.\n\n"
    "We begin with **Statistics & Probability** because it is the language every later track "
    "speaks. Build it solid here and everything above it gets easier."))

# ------------------------------------------------------- key points ------- #
p.append(B.keypoints([
    "A data scientist exists to turn data into a **decision** — not to build models for their "
    "own sake.",
    "The **workflow** — question &rarr; get data &rarr; clean &rarr; explore &rarr; model/test "
    "&rarr; interpret &rarr; communicate — repeats on every project.",
    "Any number computed from data is a **sample**, and samples **wobble**. The core job of "
    "statistics is separating real **signal** from random **noise**.",
    "We start with statistics because it is the foundation the other ten tracks are built on.",
]))

# ------------------------------------------------------- quiz ------------- #
p.append(B.quiz([
    {"q": "A teammate says, *\"Variant B converted at 8.1% and A at 7.3%, so B is better — "
          "let's ship it.\"* What is the single most important question to ask first?",
     "options": [
        {"t": "Could this gap be the result of random chance in this particular sample?",
         "correct": True,
         "why": "Exactly. Both rates are estimates from a sample that wobbles. Before acting we "
                "must ask whether the difference is real signal or could easily be noise — the "
                "central question of statistical inference."},
        {"t": "Which button has the nicer color?",
         "why": "Aesthetics may matter to design, but the decision here is about whether the "
                "measured lift is trustworthy, which is a statistical question."},
        {"t": "Can we make button B even bigger?",
         "why": "That skips the real issue: we don't yet know if B's apparent advantage is real "
                "rather than a fluke of this sample."},
        {"t": "Nothing — 8.1% is larger than 7.3%, so the decision is already correct.",
         "why": "This is the classic trap: treating sample numbers as exact truth. The numbers "
                "would shift on a different week, so 'bigger here' is not yet 'genuinely better'."}]},
    {"q": "In the data science workflow, where does most of a project's *statistical judgment* "
          "actually get used?",
     "options": [
        {"t": "Exploring the data, testing ideas, and quantifying how uncertain the results are",
         "correct": True,
         "why": "Right. The 'green' steps — explore, model/test, interpret — are where you reason "
                "under uncertainty. That reasoning is statistics."},
        {"t": "Only in the final slide where you present to stakeholders",
         "why": "Communication matters, but the statistical thinking happens upstream, while "
                "exploring and testing — the slide just reports its conclusions."},
        {"t": "Entirely in the data-cleaning step",
         "why": "Cleaning is essential but is mostly engineering and judgment about data quality, "
                "not statistical inference."},
        {"t": "Nowhere — modern tools handle all the statistics automatically",
         "why": "Tools compute numbers, but deciding which analysis is valid, and how much to "
                "trust it, is human statistical judgment — the skill this course builds."}]},
]))

# ------------------------------------------------------- practice --------- #
p.append(B.practice([
    {"q": "In your own words, explain the difference between a question like *\"Is B's rate "
          "higher in our data?\"* and *\"Is B genuinely better than A?\"* Why does only the "
          "second one need statistics?",
     "sol": "The first question is about *this specific sample* and can be answered by simple "
            "arithmetic — just compare the two computed rates. The second question is about the "
            "*real world* (all visitors, including ones you didn't observe). Because your data is "
            "only a sample, the observed gap could be a real effect or could be random luck. "
            "Statistics is what lets you reason from the sample you have back to the world you "
            "care about, while stating how confident you can be. Only the second question makes "
            "that leap, so only it needs statistics."},
    {"q": "Map these four activities onto the workflow steps: (a) drawing a histogram of order "
          "values; (b) asking *\"why did revenue drop in March?\"*; (c) writing a memo "
          "recommending a price change; (d) removing duplicate rows from a spreadsheet.",
     "sol": "(b) is the **Question** step — every project starts here. (d) is **Clean & "
            "prepare**. (a) is **Explore (EDA)** — a chart to understand the data's shape. "
            "(c) is **Communicate & decide** — translating analysis into a recommendation. "
            "Notice none of these is 'build a machine-learning model' — most real data-science "
            "work lives in the other steps."},
]))

# ------------------------------------------------------- deep dive -------- #
p.append(B.deepdive(
    B.concept(
        "People use these four words loosely, and interviewers love to check whether you can "
        "keep them straight:\n\n"
        "- ~Statistics~ is the mathematical theory of learning from data under uncertainty — "
        "estimation, testing, and quantifying error. It is the foundation.\n"
        "- ~Data analysis~ is the practical activity of exploring and summarizing data to answer "
        "a question, often without heavy modeling.\n"
        "- ~Machine learning~ is a set of methods for building models that predict, by learning "
        "patterns from data automatically. It leans heavily on statistics.\n"
        "- ~Data science~ is the whole job — combining all of the above with engineering, "
        "domain knowledge, and communication to drive decisions.") +
    B.concept(
        "A useful way to see it: statistics asks *\"what can I conclude, and how sure am I?\"*; "
        "machine learning asks *\"what's the most accurate prediction I can make?\"* The best "
        "data scientists fluently switch between the two mindsets depending on whether the goal "
        "is **understanding** or **prediction** — a theme we'll return to in Tracks 8 and 8."),
    title="Deep dive: statistics vs. analysis vs. ML vs. data science"))

# --------------------------------------------------- interview ------------ #
p.append(B.callout("note",
    "Interview-ready",
    "A common warm-up question is *\"walk me through how you'd approach a data problem.\"* "
    "Answer with the workflow from this lesson — question, data, clean, explore, model/test, "
    "interpret, communicate — and emphasize that you'd quantify uncertainty before recommending "
    "a decision. It signals maturity far better than jumping straight to *\"I'd train a model.\"*",
    "&#9670;"))

LESSONS = {"stats-01-what-is": "\n".join(p)}
