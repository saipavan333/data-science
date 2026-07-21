# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]
p.append(B.why(
 "Two data types hide enormous signal behind a format models can't read: **dates** and **text**. A "
 "raw timestamp is a meaningless big integer to a model; raw text is not a number at all. But buried "
 "in them are some of your best features &mdash; the *hour* a purchase happened, whether it's a "
 "*weekend*, how many *days since* a user signed up, the *words* in a review. Extracting these is "
 "often the difference between a mediocre model and a great one."))
p.append(B.h2("Dates: explode the timestamp into parts", kicker="Datetime features"))
p.append(B.concept(
 "A raw datetime is useless as one number, but it's a treasure chest of features. Pull out the "
 "**components** that plausibly matter, plus **durations** relative to other events:\n\n"
 "- **Calendar parts**: year, month, day, day-of-week, hour, week-of-year, quarter.\n"
 "- **Flags**: is_weekend, is_holiday, is_month_end, is_business_hours.\n"
 "- **Durations**: days_since_signup, hours_since_last_purchase, account_age &mdash; often the "
 "strongest of all, because *recency* drives so much behaviour."))
p.append(B.h2("The cyclical trap — and its fix", kicker="Why hour 23 ≠ far from hour 0"))
p.append(B.concept(
 "Time is **circular**, but integers are a straight line. Encode `hour` as 0&ndash;23 and the model "
 "thinks 23:00 and 00:00 are **23 apart** &mdash; maximally distant &mdash; when they're actually one "
 "hour apart. Same for December&rarr;January, Sunday&rarr;Monday. The fix is **cyclical encoding**: "
 "map the value onto a circle with sine and cosine, so the ends meet:"))
p.append(B.figure(IMG+"s_fe_cyclical.png",
 "**Cyclical encoding.** Mapping `hour` to `(sin(2&pi;h/24), cos(2&pi;h/24))` places the hours on a "
 "circle, so **23:00 and 00:00 land right next to each other** &mdash; as they should. Raw integers "
 "would put them 23 apart. Use the same trick for month, day-of-week, and any cyclic feature.",
 "A unit circle with 24 hour points; 23:00 and 00:00 highlighted as adjacent."))
_c,_o=_run(r'''
import numpy as np
def cyc(h, period=24):
    return np.sin(2*np.pi*h/period), np.cos(2*np.pi*h/period)

def dist(a, b):
    (sa, ca), (sb, cb) = cyc(a), cyc(b)
    return round(float(np.hypot(sa-sb, ca-cb)), 2)

print(f"raw integer 'distance' 23 vs 0 : {abs(23-0)}            <- looks far")
print(f"cyclical distance     23 vs 0 : {dist(23, 0)}   <- actually adjacent")
print(f"cyclical distance     12 vs 0 : {dist(12, 0)}   <- truly opposite (noon vs midnight)")
''')
p.append(B.code_example(_c,_o,filename="cyclical.py"))
p.append(B.h2("Text: from words to numbers", kicker="Bag-of-words & TF-IDF"))
p.append(B.concept(
 "For classic tabular models, the simplest useful text features are **counts of words**:\n\n"
 "- **Bag-of-words**: one column per word in the vocabulary; each cell counts how often that word "
 "appears. Order is thrown away, but for many tasks (spam, topic, sentiment) word *presence* is "
 "enough.\n"
 "- **TF&ndash;IDF**: weight each word by how often it appears in this document (**TF**) but "
 "**down-weight** words common across *all* documents (**IDF**). So \"the\" and \"and\" get "
 "near-zero weight while distinctive words like \"refund\" or \"lawsuit\" stand out &mdash; usually a "
 "clear win over raw counts.\n\n"
 "Plus cheap, robust hand-features: text length, word count, count of `!`, share of capital letters "
 "&mdash; often startlingly predictive for spam and urgency."))
p.append(B.tip(
 "Bag-of-words and TF&ndash;IDF are still excellent **baselines** &mdash; fast, interpretable, and "
 "hard to beat on small text datasets. Modern **embeddings** (from transformer models) capture "
 "*meaning* and word order and win on large, nuanced tasks, but they're heavier and less "
 "interpretable. Start with TF&ndash;IDF; reach for embeddings when the task and data justify it."))
p.append(B.h2("Your turn — prove the cyclical fix", kicker="Interactive lab"))
p.append(B.pylab(
 "Encode hours cyclically as `(sin(2&pi;h/24), cos(2&pi;h/24))`. Compute the **Euclidean distance** "
 "between **hour 23** and **hour 0** in this encoding, round to **2 decimals**, and assign to "
 "**`answer`**. (As raw integers they're 23 apart; cyclically they should be tiny.)",
 "import numpy as np\n"
 "def cyc(h):\n"
 "    return np.array([np.sin(2*np.pi*h/24), np.cos(2*np.pi*h/24)])\n",
 "answer = round(float(np.linalg.norm(cyc(23) - cyc(0))), 2)",
 starter="import numpy as np\ndef cyc(h):\n    return np.array([np.sin(2*np.pi*h/24), np.cos(2*np.pi*h/24)])\n# distance between cyc(23) and cyc(0), rounded 2 dp\nanswer = ",
 hint="`np.linalg.norm(cyc(23) - cyc(0))` is the Euclidean distance between the two 2-D points; "
      "round to 2 dp.",
 title="Lab — cyclical distance, 23:00 vs 00:00",
 preview="numpy loaded; a `cyc(h)` helper returns the (sin, cos) encoding. First Run boots Python.",
 explain="About **0.26** &mdash; tiny, reflecting that 23:00 and 00:00 are one hour apart, versus a "
         "raw-integer gap of 23. That's the whole point of cyclical encoding: the clock's midnight "
         "seam disappears and the model sees time the way it actually works."))
p.append(B.keypoints([
 "Explode raw **datetimes** into calendar parts (hour, day-of-week, month), **flags** (is_weekend), "
 "and **durations** (days_since_signup &mdash; often the strongest).",
 "Time is **circular**: encode cyclic features with **sin/cos** so 23:00 sits next to 00:00 (not 23 "
 "apart).",
 "Turn **text** into numbers with **bag-of-words** or, better, **TF&ndash;IDF** (down-weights common "
 "words); add cheap hand-features (length, `!` count).",
 "TF&ndash;IDF is a strong, interpretable **baseline**; **embeddings** win on large, meaning-heavy "
 "tasks at higher cost.",
 "All learned pieces (IDF weights, vocab) are fit on **train only**.",
]))
p.append(B.quiz([
 {"q":"You encode `month` as 1-12 and feed it to a model. Why might December&rarr;January behaviour "
      "be mismodelled?",
  "options":[
   {"t":"As integers, month 12 and month 1 look 11 apart, so the model can't see they're adjacent in "
        "the yearly cycle","correct":True,
    "why":"Correct. Months are cyclic; raw integers break the Dec&rarr;Jan seam, making the model "
          "treat consecutive months as maximally distant. Cyclical (sin/cos) encoding restores the "
          "adjacency."},
   {"t":"Months can't be used as features",
    "why":"They can &mdash; the issue is *how* you encode them. Cyclical encoding handles the wrap-"
          "around."},
   {"t":"You must one-hot months into 12 columns always",
    "why":"One-hot is one option, but it discards the cyclic *closeness* of adjacent months; sin/cos "
          "encoding preserves it more compactly."},
   {"t":"The model needs the year too",
    "why":"Adding year is orthogonal; the specific Dec&rarr;Jan problem is the cyclic wrap-around, "
          "fixed by cyclical encoding."}]},
 {"q":"For a spam classifier on short messages, why is TF-IDF usually preferred over raw word counts?",
  "options":[
   {"t":"It down-weights words common to all messages and up-weights distinctive ones, so signal "
        "words like 'free' or 'winner' stand out","correct":True,
    "why":"Correct. TF-IDF multiplies term frequency by inverse document frequency, muting ubiquitous "
          "words ('the', 'and') and emphasising rare, discriminative ones &mdash; typically a clear "
          "gain over raw counts for text classification."},
   {"t":"It captures word order and grammar",
    "why":"TF-IDF, like bag-of-words, ignores order; its advantage is *weighting*, not syntax "
          "(embeddings/transformers handle order)."},
   {"t":"It requires no training",
    "why":"IDF weights are learned from the corpus (on train only). The benefit is the weighting "
          "scheme, not a lack of fitting."},
   {"t":"It works only with neural networks",
    "why":"TF-IDF is a classic feature for linear models, trees, and SVMs &mdash; no neural network "
          "needed."}]},
]))
p.append(B.practice([
 {"q":"You're predicting food-delivery demand per hour. List five datetime-derived features you'd "
      "engineer and why each could matter.",
  "sol":"Strong candidates: **hour-of-day** (cyclically encoded) &mdash; demand peaks at lunch/dinner; "
        "**day-of-week** (cyclic or one-hot) &mdash; weekends differ from weekdays; **is_weekend / "
        "is_holiday** flags &mdash; step changes in behaviour; **is_business_hours** &mdash; office "
        "vs. home ordering; **days_since_last_order** per user &mdash; recency drives repeat demand; "
        "and context features like **is_raining** joined on the timestamp &mdash; weather spikes "
        "delivery. The reasoning thread: decompose the timestamp into the *human rhythms* "
        "(daily/weekly/seasonal cycles, holidays, recency) that actually drive the outcome &mdash; "
        "and encode the cyclic ones with sin/cos so the wrap-arounds behave."},
 {"q":"A colleague builds a TF-IDF vectorizer on the full dataset, then splits train/test. What's the "
      "leak, and does it matter much?",
  "sol":"The **IDF weights and the vocabulary** are *learned* statistics &mdash; fitting them on the "
        "full dataset means the test documents influenced the feature definitions (which words exist, "
        "how they're weighted), so information leaked from test into the features. It should be fit "
        "on **train only** and merely *applied* to test. Does it matter? Usually the effect is "
        "**modest** for IDF on large corpora (the weights are broadly similar), but it's still "
        "methodologically wrong and can matter on small datasets or when the vocabulary differs "
        "&mdash; and it's the *same discipline* that prevents far more dangerous leaks (like target "
        "encoding). So fix it on principle: wrap the vectorizer in a pipeline that fits inside the "
        "train fold."},
]))
p.append(B.deepdive(
 B.concept(
  "**Why sine *and* cosine, not just one.** A single sine can't identify an hour uniquely &mdash; "
  "sin is the same for two different times (e.g. it rises and falls symmetrically), so the model "
  "couldn't tell them apart. The **pair** (sin, cos) gives every angle a unique point on the unit "
  "circle, preserving both *which* time it is and *how close* any two times are. That's the minimal "
  "faithful embedding of a cycle: two columns that together encode position-on-a-loop, with the seam "
  "(23&rarr;0, Dec&rarr;Jan) automatically stitched.") +
 B.concept(
  "**The text-feature ladder, and when to climb it.** Rung 1: hand-features (length, punctuation, "
  "capital ratio) &mdash; trivial, robust, shockingly useful for spam/urgency. Rung 2: bag-of-words "
  "&mdash; presence of vocabulary. Rung 3: TF&ndash;IDF &mdash; weighted presence, the classic strong "
  "baseline. Rung 4: **embeddings** (word2vec, and today transformer sentence embeddings) &mdash; "
  "dense vectors capturing meaning and, with transformers, word order and context. Each rung adds "
  "power *and* cost/opacity. The professional move is to establish a TF&ndash;IDF baseline first "
  "&mdash; it's fast, interpretable, and frequently within a hair of the fancy approach &mdash; and "
  "only climb to embeddings when the data volume and task nuance clearly pay for it."),
 title="Deep dive: why (sin, cos) as a pair, and the text-feature ladder"))
LESSONS={"fe-04-datetime-text":"\n".join(x for x in p if x)}
print("content_fe04 OK — chars:", len(LESSONS["fe-04-datetime-text"]))
