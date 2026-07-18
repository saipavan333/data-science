# -*- coding: utf-8 -*-
import builder as B
from examples_run import EX

IMG = "../assets/img/"
p = []

p.append(B.why(
    "Before you compute a single statistic or draw a single chart, you have to know **what kind "
    "of thing** each column is. The type of a variable decides which summaries make sense, which "
    "charts are honest, and which models are even allowed. Get it wrong and you'll do something "
    "absurd — like averaging zip codes — without noticing. This lesson gives you a reliable way "
    "to classify any column in seconds."))

# ----------------------------------------------------- vocabulary --------- #
p.append(B.h2("First, three words", kicker="Vocabulary"))
p.append(B.concept(
    "Picture a spreadsheet of customers. Each **row** is one customer; each **column** is one "
    "thing you measured about them.\n\n"
    "- A ~variable~ is a column — a single property that varies across rows (e.g., `city`, "
    "`monthly_spend`).\n"
    "- An ~observation~ is a row — one unit you measured (one customer).\n"
    "- A ~value~ is one cell — what a particular observation scored on a particular variable.\n\n"
    "When we ask *\"what type is this variable?\"* we are asking about a whole column, not a "
    "single cell."))

# ----------------------------------------------------- taxonomy ----------- #
p.append(B.h2("The two big families of data", kicker="Concept"))
p.append(B.concept(
    "Every variable is either ~categorical~ (it puts each observation into a group or label) or "
    "~numerical~ (it measures a quantity you can do arithmetic on). Each family splits once more, "
    "giving four types in total."))
p.append(B.figure(
    IMG + "s2_taxonomy.png",
    "**The four types of data.** Amber = categorical (labels); teal = numerical (quantities). "
    "Keep this tree in your head and you'll classify columns automatically.",
    "Taxonomy tree: data splits into categorical (nominal, ordinal) and numerical "
    "(discrete, continuous)."))
p.append(B.concept(
    "Read the four leaves carefully — the definitions matter:\n\n"
    "- ~Nominal~ — named categories with **no natural order**. City, browser, payment method. "
    "You can count how many fall in each group, but \"greater than\" is meaningless.\n"
    "- ~Ordinal~ — categories with a **meaningful order**, but the gaps between them aren't "
    "necessarily equal. T-shirt size (S < M < L), a 1–5 satisfaction rating, education level. "
    "You can rank them, but the distance from 'S' to 'M' isn't a fixed amount.\n"
    "- ~Discrete~ — numbers you get by **counting**, so only whole values are possible. Number "
    "of purchases, logins last week, items in a cart. You can't have 2.5 logins.\n"
    "- ~Continuous~ — numbers you get by **measuring**, which can take any value in a range. "
    "Revenue, weight, time on site. Between any two values there's always another."))

# ----------------------------------------------------- decision tree ------ #
p.append(B.h2("A 10-second test for any column", kicker="Method"))
p.append(B.concept(
    "When you meet a new column, run it through three questions. The diagram below is the whole "
    "decision; the questions are the diamonds."))
p.append(B.figure(
    IMG + "s2_decision.png",
    "**Which type is this variable?** Start at the top. *Can you average it sensibly?* sends you "
    "left (categorical) or right (numerical); two more questions pin down the exact type.",
    "Decision tree classifying a variable as nominal, ordinal, discrete, or continuous."))
p.append(B.tip(
    "The sharpest single test is the first diamond: *\"does averaging it mean anything?\"* The "
    "average of three cities is nonsense, so `city` is categorical. The average of three order "
    "values is a useful number, so `order_value` is numerical. This one question catches most "
    "mistakes."))

# ----------------------------------------------------- worked example ----- #
p.append(B.h2("The trap: storage type is not variable type", kicker="Worked example"))
p.append(B.concept(
    "Here's the mistake that bites beginners. When you load data, the tool (here, ~pandas~ — "
    "Python's table library, which we'll learn properly in Track 1) records a **storage type**, "
    "called a ~dtype~: is this column stored as integers, decimals, or text? That is *not* the "
    "same as the variable type you just learned. A column can be stored as integers yet be "
    "completely categorical."))
p.append(B.code_example(EX["s12_types"][0], EX["s12_types"][1], filename="data_types.py"))
p.append(B.pitfall(
    "`customer_id` is stored as `int64`, so the computer will happily average it — and hand you "
    "`1003.0`, a meaningless number. IDs, zip codes, and survey codes like *1 = Free, 2 = Pro* "
    "are **nominal** variables wearing a numeric costume. Always classify a column by what it "
    "*means*, never by how it's stored."))

# ----------------------------------------------------- why it matters table  #
p.append(B.h2("Why the type decides everything downstream", kicker="Consequences"))
p.append(B.concept(
    "The type isn't trivia — it dictates the right tool at every later step. This table is a "
    "preview of the next several lessons:"))
p.append(B.table(
    ["Variable type", "Example", "A summary that fits", "A chart that fits"],
    [["Nominal", "payment method", "counts / most frequent (mode)", "bar chart"],
     ["Ordinal", "satisfaction 1–5", "median, counts per level", "ordered bar chart"],
     ["Discrete", "items in cart", "mean, median, counts", "bar chart / histogram"],
     ["Continuous", "revenue, time on site", "mean, median, std dev", "histogram / boxplot"]],
    caption="The variable type chooses your statistics and your charts. We'll justify every cell "
            "in the coming lessons."))

p.append(B.keypoints([
    "A **variable** is a column, an **observation** is a row, a **value** is a cell.",
    "Four types: **nominal** and **ordinal** (categorical), **discrete** and **continuous** "
    "(numerical).",
    "Best quick test: *does averaging it mean something?* If no &rarr; categorical; if yes "
    "&rarr; numerical. Then check order (nominal vs ordinal) or whole-vs-measured (discrete vs "
    "continuous).",
    "A column's **storage type (dtype) is not its variable type.** IDs and codes are nominal "
    "even when stored as numbers.",
    "The type you assign decides which summaries, charts, tests, and models are valid later.",
]))

p.append(B.quiz([
    {"q": "A column `zip_code` contains values like 78701, 80202, 89501. What type of variable "
          "is it?",
     "options": [
        {"t": "Nominal (categorical) — the numbers are just labels for places",
         "correct": True,
         "why": "Correct. Zip codes identify regions; their numeric size is meaningless "
                "(89501 isn't 'more' than 78701), and averaging them is nonsense. It's nominal "
                "wearing a numeric costume."},
        {"t": "Continuous — it's stored as numbers and can take many values",
         "why": "Being stored as numbers is a storage detail, not the variable type. You can't "
                "meaningfully average or order zip codes, so they aren't numerical."},
        {"t": "Discrete — zip codes are whole numbers",
         "why": "They are whole numbers, but 'discrete' means a meaningful *count*. A zip code "
                "isn't a quantity you counted; it's a label, which makes it nominal."},
        {"t": "Ordinal — larger zip codes come later",
         "why": "There's no meaningful ranking where a bigger zip code is 'more' of anything, so "
                "it isn't ordinal."}]},
    {"q": "Which of these is a **continuous** variable?",
     "options": [
        {"t": "The exact time (in seconds) a user spent on a page",
         "correct": True,
         "why": "Time is measured, not counted, and can take any value in a range (12.84 s is "
                "fine). That's the definition of continuous."},
        {"t": "The number of pages a user viewed",
         "why": "That's a count of whole pages — you can't view 3.5 pages — so it's discrete, "
                "not continuous."},
        {"t": "The user's membership tier (Bronze, Silver, Gold)",
         "why": "Those are ordered categories, so it's ordinal — categorical, not numerical."},
        {"t": "The user's country",
         "why": "Country is an unordered label, so it's nominal — not a numerical variable at "
                "all."}]},
    {"q": "A survey stores the answer to *\"How satisfied are you?\"* as 1, 2, 3, 4, or 5 "
          "(Very unsatisfied &hellip; Very satisfied). Why is reporting the **mean** of this "
          "column slightly dangerous?",
     "options": [
        {"t": "Because it's ordinal: the order is real, but the gaps between levels may not be "
              "equal, so an average can mislead",
         "correct": True,
         "why": "Exactly. With ordinal data you can rank but can't assume the distance from 1&rarr;2 "
                "equals 4&rarr;5. The mean treats those gaps as equal, which may not be true — the "
                "median is often safer."},
        {"t": "Because the values are stored as text, so the mean can't be computed",
         "why": "They're stored as numbers here, so the mean *can* be computed — the issue is "
                "whether it's *meaningful*, not whether it's possible."},
        {"t": "Because satisfaction is a nominal variable with no order",
         "why": "Satisfaction clearly has an order (5 is more satisfied than 1), so it's ordinal, "
                "not nominal."},
        {"t": "It isn't dangerous at all; the mean is always the best summary",
         "why": "The mean assumes equal spacing between values, which ordinal data doesn't "
                "guarantee, so it can be misleading here."}]},
]))

p.append(B.practice([
    {"q": "Classify each column from a ride-sharing dataset: (a) `driver_rating` (1–5 stars); "
          "(b) `trip_distance_km`; (c) `payment_type` (cash, card, wallet); (d) `num_passengers`; "
          "(e) `pickup_zip`.",
     "sol": "(a) **Ordinal** — ordered ratings, but the gap between 4 and 5 stars isn't "
            "guaranteed equal to 1&rarr;2. (b) **Continuous** — a measured distance, any value in "
            "a range. (c) **Nominal** — unordered labels. (d) **Discrete** — a count of whole "
            "passengers. (e) **Nominal** — a zip is a place label, not a quantity, despite being "
            "numeric."},
    {"q": "A colleague computes the average of a `star_rating` column and also the average of an "
          "`account_id` column. One of these is reasonable and one is nonsense. Which is which, "
          "and what's the underlying rule?",
     "sol": "Averaging `star_rating` is *defensible but imperfect* — it's ordinal, so the mean "
            "assumes equal spacing between stars (many teams still report it, but the median is "
            "safer). Averaging `account_id` is **nonsense** — it's a nominal label, so its "
            "numeric value carries no quantity. The rule: only average variables where the "
            "*magnitude* of the number means something, i.e., numerical variables."},
]))

p.append(B.deepdive(
    B.concept(
        "Statisticians often use a finer, four-level scheme from psychologist S. S. Stevens "
        "(1946) called the ~levels of measurement~. It splits our 'numerical' family by asking "
        "whether the scale has equal intervals and a true zero:\n\n"
        "- ~Nominal~ — labels only (city). Equality is the only relation.\n"
        "- ~Ordinal~ — order, but unequal/unknown gaps (satisfaction 1–5).\n"
        "- ~Interval~ — equal gaps, but **no true zero**, so ratios are meaningless. Celsius "
        "temperature: 20°C isn't 'twice as hot' as 10°C, because 0°C isn't 'no heat'.\n"
        "- ~Ratio~ — equal gaps **and** a true zero, so ratios make sense. Revenue, weight, "
        "time, counts: $100 really is twice $50, because $0 means none.") +
    B.concept(
        "Why care? Because the level controls which operations are valid. You can rank ordinal "
        "data but shouldn't average it freely; you can add and subtract interval data but "
        "shouldn't take ratios; only ratio data supports the full toolkit including percentages "
        "and coefficients of variation. When an interviewer asks why you wouldn't say \"30°C is "
        "50% warmer than 20°C,\" this is the answer: temperature in Celsius is interval, not "
        "ratio."),
    title="Deep dive: the four levels of measurement (nominal, ordinal, interval, ratio)"))

p.append(B.callout("note", "Interview-ready",
    "Expect *\"what kinds of variables are there, and why does it matter?\"* Name the four types "
    "with an example each, then deliver the punchline interviewers want: the type determines "
    "which summary statistic, chart, and statistical test are valid — and that an ID stored as "
    "an integer is still categorical.", "&#9670;"))

LESSONS = {"stats-02-data-types": "\n".join(p)}
