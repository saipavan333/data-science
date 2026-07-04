# -*- coding: utf-8 -*-
import builder as B
from examples_run import EX

IMG = "../assets/img/"
p = []

p.append(B.why(
    "A ~distribution~ is the *shape* of a variable — it tells you which values are common, which "
    "are rare, and how likely any range is. Recognizing which distribution your data follows is "
    "a superpower: it lets you compute exact probabilities, flag anomalies, size experiments, and "
    "pick the right statistical method. This lesson teaches the four distributions you'll meet "
    "constantly and how to tell at a glance which one you're looking at."))

# ----------------------------------------------------- what is a dist ----- #
p.append(B.h2("What a distribution actually is", kicker="Concept · foundations"))
p.append(B.concept(
    "A ~random variable~ is just a number whose value is uncertain until observed — the result of "
    "a die roll, a customer's spend, tomorrow's ticket count. A distribution describes how "
    "probability is spread across that variable's possible values. There are two flavors, "
    "matching the discrete/continuous split from Lesson 1.2:\n\n"
    "- For a **discrete** variable, the ~PMF~ (probability mass function) gives the probability "
    "of *each exact value*. The bar heights add up to 1.\n"
    "- For a **continuous** variable, the ~PDF~ (probability density function) is a smooth curve, "
    "and probability is the **area under it** over a range. The probability of any single exact "
    "value is effectively zero — only ranges have probability."))
p.append(B.figure(
    IMG + "s5_pmf_pdf.png",
    "**Two kinds of distribution.** Left: a discrete PMF — each bar's *height* is the "
    "probability of that count. Right: a continuous PDF — the *area* under the curve over a "
    "range is the probability. This 'height vs. area' distinction trips up everyone once.",
    "Side-by-side PMF bars and a PDF curve with a shaded area."))

# ----------------------------------------------------- normal ------------- #
p.append(B.h2("The normal distribution (the bell curve)", kicker="Concept · the famous one"))
p.append(B.concept(
    "The ~normal distribution~ — the symmetric 'bell curve' — is the most important shape in "
    "statistics. It's fully described by two numbers: its ~mean~ &mu; (where the peak sits) and "
    "its ~standard deviation~ &sigma; (how wide it is). Heights, measurement errors, and "
    "averages of many small effects all tend toward it.\n\n"
    "Its most useful property is the ~empirical rule~, also called 68–95–99.7: in any normal "
    "distribution, about **68%** of values fall within &plusmn;1&sigma; of the mean, **95%** "
    "within &plusmn;2&sigma;, and **99.7%** within &plusmn;3&sigma;."))
p.append(B.figure(
    IMG + "s5_normal_empirical.png",
    "**The 68–95–99.7 rule.** Distances from the mean are measured in standard deviations. This "
    "is why a value more than 2&sigma; from the mean feels 'surprising' (only ~5% of data is out "
    "there) and 3&sigma; feels 'rare' (~0.3%).",
    "Normal curve with shaded bands at one, two, and three standard deviations."))
p.append(B.tip(
    "Measuring distance in standard deviations gives the ~z-score~: z = (x &minus; &mu;) / "
    "&sigma;. A z-score of 2 means 'two SDs above the mean.' Z-scores let you compare values "
    "from totally different scales — a test score and a height — on one common ruler, and they're "
    "the backbone of the hypothesis tests coming in Lesson 1.9."))

# ----------------------------------------------------- binomial ----------- #
p.append(B.h2("The binomial: counting successes", kicker="Concept · discrete #1"))
p.append(B.concept(
    "The ~binomial distribution~ answers: *in n independent yes/no trials, each with success "
    "probability p, how many successes do I get?* Think 10 emails each opened with probability "
    "0.2, or 100 visitors each converting with probability 0.05. Its two parameters are n (number "
    "of trials) and p (probability per trial)."))
p.append(B.figure(
    IMG + "s5_binomial.png",
    "**Binomial(n=10, p).** With small p the mass piles up near zero; with p=0.5 it's symmetric; "
    "with large p it shifts right. The most likely count sits around n&times;p.",
    "Three binomial PMFs for p = 0.2, 0.5, and 0.8."))

# ----------------------------------------------------- poisson ------------ #
p.append(B.h2("The Poisson: counting rare events over time", kicker="Concept · discrete #2"))
p.append(B.concept(
    "The ~Poisson distribution~ answers: *how many independent events happen in a fixed interval, "
    "when they occur at an average rate &lambda;?* Support tickets per hour, website crashes per "
    "day, typos per page. Its single parameter &lambda; (lambda) is both the average count and — "
    "neatly — its variance."))
p.append(B.figure(
    IMG + "s5_poisson.png",
    "**Poisson(&lambda;).** As the average rate &lambda; rises, the whole distribution shifts "
    "right and spreads out, and its shape starts to resemble a normal curve — a preview of a "
    "deep connection.",
    "Three Poisson PMFs for lambda = 1, 3, and 7."))

# ----------------------------------------------------- chooser ------------ #
p.append(B.h2("Which distribution when?", kicker="Method"))
p.append(B.concept(
    "You don't memorize formulas; you recognize situations. Walk any variable down this tree and "
    "you'll usually land on the right model. (Two more continuous shapes appear here: the "
    "~uniform~, where every value in a range is equally likely, and the ~exponential~, the "
    "right-skewed distribution of *waiting times* between Poisson events.)"))
p.append(B.figure(
    IMG + "s5_chooser.png",
    "**A which-distribution-when decision tree.** Start by asking discrete or continuous, then "
    "match the situation. Keep this as a reference — you'll reach for it whenever you model a new "
    "variable.",
    "Decision tree mapping situations to binomial, Poisson, normal, exponential, or uniform."))

# ----------------------------------------------------- worked example ----- #
p.append(B.h2("Computing real probabilities", kicker="Worked example"))
p.append(B.concept(
    "Once you've named the distribution, a library does the arithmetic. Here we use ~scipy~ "
    "(Python's scientific toolkit) to answer concrete questions with each of the three "
    "distributions. Notice the pattern: build the distribution with its parameters, then ask it "
    "for a probability."))
p.append(B.code_example(EX["s15_dist"][0], EX["s15_dist"][1], filename="distributions.py"))
p.append(B.concept(
    "Read the results back to the pictures. The normal answer **0.683** is exactly the 68% band "
    "from the empirical-rule chart (163 to 177 is &mu; &plusmn; 1&sigma;). The binomial **0.201** "
    "is the tall bar at 3 in the p=0.2 panel. The Poisson **0.050** says a totally quiet "
    "support hour is uncommon when you average 3 tickets. The shapes and the numbers are the "
    "same facts told two ways."))

p.append(B.keypoints([
    "A **distribution** describes how probability is spread over a variable's values: a **PMF** "
    "(bar heights) for discrete, a **PDF** (area under a curve) for continuous.",
    "**Normal(&mu;, &sigma;)** — symmetric bell; the **68–95–99.7 rule** covers &plusmn;1/2/3 "
    "SD; the **z-score** (x&minus;&mu;)/&sigma; measures distance in SDs.",
    "**Binomial(n, p)** — number of successes in n yes/no trials; centered near n&times;p.",
    "**Poisson(&lambda;)** — number of events in an interval at rate &lambda;; mean and variance "
    "both equal &lambda;.",
    "Choose a distribution by **recognizing the situation** (discrete vs continuous, then the "
    "mechanism), not by memorizing formulas.",
]))

p.append(B.quiz([
    {"q": "You model the number of customer-support tickets arriving per hour. Tickets are "
          "independent and arrive at an average rate of 4/hour. Which distribution fits best?",
     "options": [
        {"t": "Poisson(&lambda; = 4)",
         "correct": True,
         "why": "Right. Counting independent events in a fixed interval at a known average rate "
                "is the textbook Poisson setup, with &lambda; equal to that average rate."},
        {"t": "Binomial(n = 4, p = 0.5)",
         "why": "Binomial needs a fixed number of yes/no trials. Here there's no fixed n — any "
                "number of tickets could arrive — so Poisson, not binomial, is the fit."},
        {"t": "Normal(&mu; = 4)",
         "why": "Ticket counts are discrete and can't be negative; the normal is continuous and "
                "unbounded. (Poisson does start to look normal for large &lambda;, but at 4 the "
                "Poisson is the right model.)"},
        {"t": "Uniform between 0 and 4",
         "why": "Uniform would mean every count 0–4 is equally likely, which isn't how random "
                "arrivals behave — counts cluster near the average rate."}]},
    {"q": "Adult resting heart rate is roughly normal with mean 70 and SD 8 bpm. About what "
          "fraction of people have a resting heart rate between 62 and 78?",
     "options": [
        {"t": "About 68% — that range is the mean &plusmn; one standard deviation",
         "correct": True,
         "why": "62 and 78 are 70 &minus; 8 and 70 + 8, i.e., &mu; &plusmn; 1&sigma;. By the "
                "empirical rule, about 68% of a normal distribution lies within one SD of the "
                "mean."},
        {"t": "About 95%",
         "why": "95% corresponds to &mu; &plusmn; 2&sigma; (54 to 86). The given range is only "
                "&plusmn;1&sigma;, which is about 68%."},
        {"t": "About 50%",
         "why": "50% would be everything below the mean. A symmetric &plusmn;1&sigma; band around "
                "the mean covers about 68%, not 50%."},
        {"t": "Almost 100%",
         "why": "Nearly all (99.7%) of the data falls within &plusmn;3&sigma; (46 to 94). The "
                "&plusmn;1&sigma; band here is about 68%."}]},
    {"q": "For a continuous PDF (like the normal curve), what does the **height** of the curve at "
          "a single exact value represent?",
     "options": [
        {"t": "Density, not probability — only the area over a range gives a probability",
         "correct": True,
         "why": "Correct. For continuous variables, probability is area under the curve across a "
                "range; the probability of any single exact value is effectively zero, so the "
                "curve's height is a density, not a probability."},
        {"t": "The exact probability of that single value",
         "why": "That's true for a discrete PMF's bars, but not a continuous PDF. A single exact "
                "value has ~zero probability; you need a range (an area)."},
        {"t": "The cumulative probability up to that value",
         "why": "That's the CDF, a different function. The PDF height is the density at a point, "
                "not the running total."},
        {"t": "Always exactly 1",
         "why": "The total *area* integrates to 1, but the curve's height varies from point to "
                "point and is not itself a probability."}]},
]))

p.append(B.practice([
    {"q": "For each scenario, name the distribution and its parameter(s): (a) the number of "
          "heads in 20 coin flips; (b) the number of meteors seen per hour during a shower "
          "averaging 15/hour; (c) the heights of adult women; (d) the outcome of rolling one "
          "fair six-sided die.",
     "sol": "(a) **Binomial(n = 20, p = 0.5)** — a fixed number of independent yes/no trials. "
            "(b) **Poisson(&lambda; = 15)** — independent events in a fixed interval at a known "
            "rate. (c) **Normal(&mu;, &sigma;)** — a continuous, roughly symmetric measurement. "
            "(d) **Uniform** over {1,…,6} — every outcome equally likely (the discrete uniform)."},
    {"q": "A landing page converts visitors at p = 0.10. In a batch of 50 visitors, what's the "
          "expected number of conversions, and roughly how would you describe the distribution of "
          "that count? (No exact computation needed.)",
     "sol": "This is **Binomial(n = 50, p = 0.10)**. The expected count is n&times;p = "
            "50 &times; 0.10 = **5 conversions**. The distribution is centered near 5, slightly "
            "right-skewed (since p is small and counts can't go below 0), and because n is "
            "moderately large it already looks bell-ish — foreshadowing how the binomial "
            "approaches a normal shape, which powers the experiment math in Track 5."},
]))

p.append(B.deepdive(
    B.concept(
        "**Standardizing with z-scores.** Any normal distribution can be converted to the "
        "~standard normal~ — mean 0, SD 1 — by the transformation z = (x &minus; &mu;) / &sigma;. "
        "This is why a single table (or one `scipy` call) handles every normal problem: you "
        "translate your value into 'how many SDs from the mean,' then look up the probability. "
        "A z of +1.96 marks the spot beyond which only 2.5% of the data lies — a number you'll "
        "see again and again in confidence intervals.") +
    B.concept(
        "**The distributions are secretly related.** The Poisson is the limit of the binomial "
        "when n is huge and p is tiny (many trials, rare success), with &lambda; = n&times;p — "
        "which is why both count events. And by the Central Limit Theorem (Lesson 1.7), *sums* of "
        "binomial or Poisson counts, and indeed averages of almost anything, drift toward the "
        "**normal** as the count grows. That's why the bell curve shows up everywhere: it is the "
        "natural shape of accumulated randomness.") +
    B.concept(
        "**The exponential's twist.** If events arrive Poisson with rate &lambda;, the *waiting "
        "time* between consecutive events follows an ~exponential~ distribution — continuous and "
        "right-skewed. Counts and waits are two views of the same random process: Poisson counts "
        "the events, exponential times the gaps."),
    title="Deep dive: z-scores, and how these distributions connect"))

p.append(B.callout("note", "Interview-ready",
    "Be ready to *\"name a distribution for this situation and justify it\"* — counts in fixed "
    "trials &rarr; binomial; events per interval &rarr; Poisson; a symmetric measurement or an "
    "average of many things &rarr; normal. Also expect *\"state the 68–95–99.7 rule\"* and "
    "*\"what's a z-score?\"* Crisp, correct answers here signal real fluency.", "&#9670;"))

LESSONS = {"stats-05-distributions": "\n".join(p)}
