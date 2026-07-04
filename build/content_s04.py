# -*- coding: utf-8 -*-
import builder as B
from examples_run import EX

IMG = "../assets/img/"
p = []

p.append(B.why(
    "Statistics is reasoning under uncertainty, and ~probability~ is the language that "
    "uncertainty is written in. Without it you can't say how likely a result is, can't design an "
    "experiment, and — most dangerously — can fall for confident-sounding conclusions that are "
    "flat wrong. By the end of this lesson you'll be able to do a calculation that the majority "
    "of doctors get wrong, and you'll see exactly why their intuition fails."))

# ----------------------------------------------------- basics ------------- #
p.append(B.h2("The vocabulary of chance", kicker="Concept · foundations"))
p.append(B.concept(
    "Start with the words, because they're used precisely:\n\n"
    "- An ~experiment~ is any process with an uncertain result (flip a coin, show a user an ad).\n"
    "- An ~outcome~ is one possible result (heads; the user clicks).\n"
    "- The ~sample space~ is the set of *all* possible outcomes.\n"
    "- An ~event~ is a collection of outcomes you care about (e.g., 'an even number' on a die is "
    "the event {2, 4, 6}).\n"
    "- The ~probability~ of an event is a number from 0 to 1 measuring how likely it is: 0 means "
    "impossible, 1 means certain, 0.5 means it happens about half the time over many repeats."))
p.append(B.concept(
    "Three rules cover most of what you'll need:\n\n"
    "1. **Bounds:** every probability is between 0 and 1, and the probabilities of all outcomes "
    "in the sample space add to exactly 1.\n"
    "2. **Complement:** the chance an event does *not* happen is 1 minus the chance it does. "
    "P(not A) = 1 &minus; P(A). (The chance of *at least one* success is often easiest computed "
    "as 1 minus the chance of none.)\n"
    "3. **Addition:** to find the chance of A *or* B, add their probabilities — but subtract the "
    "overlap so you don't count it twice."))
p.append(B.figure(
    IMG + "s4_venn.png",
    "**The addition rule.** P(A or B) double-counts the lens where A and B overlap, so we "
    "subtract P(A and B) once. If the events can't both happen (no overlap), the last term is "
    "zero and you just add.",
    "Venn diagram of two overlapping events showing the inclusion-exclusion addition rule."))

# ----------------------------------------------------- independence ------- #
p.append(B.h2("Independence and the multiplication rule", kicker="Concept · combining events"))
p.append(B.concept(
    "Two events are ~independent~ if knowing that one happened tells you **nothing** about the "
    "other. Separate coin flips are independent; today's and tomorrow's weather are not. For "
    "independent events, the chance that *both* happen is the product of their probabilities:"))
p.append(B.formula(
    'P(A and B) = P(A) &times; P(B)&nbsp;&nbsp;<small>(only when A and B are independent)</small>',
    "Two fair coins both landing heads: &frac12; &times; &frac12; = &frac14;. Five heads in a "
    "row: (&frac12;)&#8309; = 1/32 &asymp; 3%."))
p.append(B.pitfall(
    "Assuming independence when it doesn't hold causes real disasters. In the 2008 financial "
    "crisis, models treated mortgage defaults as roughly independent; in fact they were strongly "
    "linked, so 'one-in-a-million' joint losses happened. Before you multiply probabilities, ask "
    "hard: *could these really move together?*"))

# ----------------------------------------------------- conditional -------- #
p.append(B.h2("Conditional probability: updating on evidence", kicker="Concept · the key idea"))
p.append(B.concept(
    "Most real questions are *conditional*: given that something is true, how likely is something "
    "else? The ~conditional probability~ of A **given** B, written P(A | B), is the chance of A "
    "once you already know B happened:"))
p.append(B.formula(
    'P(A | B) = '
    '<sup>P(A and B)</sup>&frasl;<sub>P(B)</sub>',
    "In words: of all the times B happens, what fraction also have A? You've narrowed the world "
    "to B and are asking how much of that world is also A."))
p.append(B.concept(
    "This is where intuition starts to slip, and it slips hardest on a famous medical-testing "
    "puzzle. Suppose a disease affects **1%** of people. A test correctly flags **90%** of sick "
    "people (its ~sensitivity~) but also wrongly flags **5%** of healthy people (its "
    "~false-positive rate~). **You test positive. What's the chance you're actually sick?** Most "
    "people — including most physicians in published studies — guess around 80–90%. Let's trace "
    "every person through the test and see the truth."))
p.append(B.figure(
    IMG + "s4_tree.png",
    "**Natural frequencies make it obvious.** Start with 1,000 people. Only 10 are sick, and "
    "9 of them test positive. But among the 990 healthy people, 5% — about 50 — *also* test "
    "positive. So positives come mostly from the huge healthy group.",
    "Probability tree splitting 1,000 people into sick/healthy then positive/negative test."))
p.append(B.figure(
    IMG + "s4_bayes.png",
    "**Of everyone who tests positive, only ~15% are truly sick.** This number — P(sick | "
    "positive) — is called the *positive predictive value*. It's low because the disease is "
    "rare: the ~base rate~ dominates the test's accuracy.",
    "Stacked bar showing 9 true positives versus ~50 false positives among all positive tests."))

# ----------------------------------------------------- worked example ----- #
p.append(B.h2("The same calculation, in code", kicker="Worked example"))
p.append(B.concept(
    "Trees are great for intuition; code makes it exact and reusable. Here is the whole "
    "computation — count the people in each bucket, then take the fraction of positives who are "
    "genuinely sick."))
p.append(B.code_example(EX["s14_bayes"][0], EX["s14_bayes"][1], filename="base_rates.py"))
p.append(B.callout("warn", "The base-rate lesson",
    "A test being '90% accurate' is almost meaningless on its own. When the thing you're "
    "screening for is **rare**, even a small false-positive rate generates a flood of false "
    "alarms that swamps the true cases. This same math governs fraud detection, spam filters, "
    "rare-disease screening, and security alerts — any time you hunt for something uncommon. "
    "Always ask for the base rate before trusting a positive.", "&#9888;"))

p.append(B.keypoints([
    "Probability is a number in [0, 1]; all outcomes in the sample space sum to 1; "
    "P(not A) = 1 &minus; P(A).",
    "**Addition (or):** P(A or B) = P(A) + P(B) &minus; P(A and B) — subtract the overlap.",
    "**Multiplication (and):** P(A and B) = P(A)&times;P(B) **only if** the events are "
    "independent. Question independence before multiplying.",
    "**Conditional:** P(A | B) = P(A and B) / P(B) — narrow the world to B, then ask how much is "
    "also A.",
    "P(A | B) is **not** the same as P(B | A). With rare conditions, the **base rate** dominates, "
    "so most positives can be false alarms.",
]))

p.append(B.quiz([
    {"q": "A test for a rare condition is '95% accurate.' You test positive. Why might your "
          "actual chance of having the condition still be low?",
     "options": [
        {"t": "Because the condition is rare, so false positives from the large healthy group "
              "can outnumber true positives",
         "correct": True,
         "why": "Exactly the base-rate effect. When few people truly have the condition, even a "
                "small false-positive rate applied to the large healthy majority produces more "
                "false alarms than true cases."},
        {"t": "Because 95% accuracy means the test is basically random",
         "why": "95% accuracy is quite good per-person; the issue isn't randomness, it's that a "
                "rare base rate makes false positives dominate the positive results."},
        {"t": "Because P(positive | condition) always equals P(condition | positive)",
         "why": "These are different quantities — confusing them is the core error. The test "
                "gives you P(positive | condition); you want P(condition | positive)."},
        {"t": "Because probabilities can exceed 1 for rare events",
         "why": "Probabilities are always between 0 and 1. The real reason is the base rate, not "
                "any breaking of the probability rules."}]},
    {"q": "You flip a fair coin 4 times. What's the probability of getting **at least one** "
          "heads? (Hint: use the complement.)",
     "options": [
        {"t": "15/16 — it's 1 minus the chance of zero heads, (1/2)^4 = 1/16",
         "correct": True,
         "why": "Right. 'At least one' is the complement of 'none.' P(no heads) = (1/2)^4 = 1/16, "
                "so P(at least one) = 1 &minus; 1/16 = 15/16. Using the complement avoids adding "
                "many cases."},
        {"t": "1/2, because each flip is 50/50",
         "why": "That's the chance for a single flip. Across 4 flips the chance of seeing heads "
                "at least once is much higher than 1/2."},
        {"t": "4/16, by adding 1/4 four times",
         "why": "Adding the per-flip probabilities double-counts overlaps (flips with multiple "
                "heads). The clean route is the complement: 1 &minus; P(none)."},
        {"t": "1, because heads is bound to come up eventually",
         "why": "It's very likely (15/16) but not certain — all-tails (1/16) is possible, so the "
                "probability is below 1."}]},
    {"q": "Which pair of events is most reasonably treated as **independent**?",
     "options": [
        {"t": "The result of one fair die roll and the result of a separate fair die roll",
         "correct": True,
         "why": "Correct. Separate physical rolls don't influence each other, so knowing one tells "
                "you nothing about the other — the definition of independence."},
        {"t": "Whether it rains today and whether it rains tomorrow",
         "why": "Weather is autocorrelated — a rainy today raises the chance of a rainy tomorrow "
                "— so these are dependent."},
        {"t": "A user's age and the products they buy",
         "why": "Buying behavior typically varies with age, so these are dependent, not "
                "independent."},
        {"t": "Two stocks in the same industry on the same day",
         "why": "Stocks in one industry tend to move together with sector news, making them "
                "dependent."}]},
]))

p.append(B.practice([
    {"q": "A deck has 52 cards. Drawing one card, what is P(a heart **or** a King)? Show why you "
          "must subtract something.",
     "sol": "P(heart) = 13/52, P(King) = 4/52. But the **King of hearts** is in both sets, so "
            "adding 13/52 + 4/52 counts it twice. Subtract that one overlapping card: "
            "P(heart or King) = 13/52 + 4/52 &minus; 1/52 = **16/52 = 4/13**. This is the "
            "addition rule: subtract P(A and B) so the intersection isn't double-counted."},
    {"q": "Spam filter scenario: 20% of email is spam. The filter flags 98% of spam (true "
          "positives) and also flags 3% of real email (false positives). If a message is flagged, "
          "what's the chance it's actually spam? Use natural frequencies on 1,000 emails.",
     "sol": "Of 1,000 emails: 200 are spam, 800 are real. Flagged spam = 98% &times; 200 = 196. "
            "Flagged real = 3% &times; 800 = 24. Total flagged = 196 + 24 = 220. "
            "P(spam | flagged) = 196 / 220 &asymp; **89%**. Notice it's *high* here — unlike the "
            "disease case — because spam isn't rare (20% base rate), so true positives dominate. "
            "Same math, opposite conclusion, all because of the base rate."},
]))

p.append(B.deepdive(
    B.concept(
        "The calculation you just did is ~Bayes' theorem~ in disguise. Starting from the "
        "conditional-probability definition, P(A | B) = P(A and B) / P(B), and writing the "
        "overlap two ways, you get:") +
    B.formula(
        'P(A | B) = '
        '<sup>P(B | A) &middot; P(A)</sup>&frasl;<sub>P(B)</sub>',
        "posterior = (likelihood &times; prior) / evidence") +
    B.concept(
        "For the disease test: P(sick | +) = P(+ | sick)&middot;P(sick) / P(+). The numerator is "
        "0.90 &times; 0.01 = 0.009. The denominator P(+) totals both ways to test positive: "
        "0.009 + (0.05 &times; 0.99) = 0.0585. Dividing gives 0.009 / 0.0585 &asymp; 0.154 — the "
        "same 15.4% as the code. The ~prior~ P(sick) = 1% is the base rate; the test merely "
        "*updates* it to the ~posterior~ of 15%.") +
    B.concept(
        "This also names a courtroom blunder, the ~prosecutor's fallacy~: confusing P(evidence | "
        "innocent) with P(innocent | evidence). 'The chance of this DNA match in an innocent "
        "person is 1 in a million' does **not** mean 'the chance this person is innocent is 1 in "
        "a million' — you must weigh the base rate of who could have left it. The same swap that "
        "fools doctors has sent innocent people to prison."),
    title="Deep dive: Bayes' theorem and the prosecutor's fallacy"))

p.append(B.callout("note", "Interview-ready",
    "Base-rate questions are a data-science interview staple, often as the medical-test puzzle or "
    "a fraud-detection variant. Don't reach for the formula first — narrate **natural "
    "frequencies** ('imagine 1,000 people&hellip;'), which is clearer and harder to botch, then "
    "name it as Bayes' theorem and stress that P(A|B) &ne; P(B|A).", "&#9670;"))

LESSONS = {"stats-04-probability": "\n".join(p)}
