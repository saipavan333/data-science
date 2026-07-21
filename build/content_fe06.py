# -*- coding: utf-8 -*-
import builder as B
p=[]
p.append(B.why(
 "Feature-engineering questions separate people who've *shipped* models from people who've only "
 "*trained* them. Interviewers probe two things: can you turn raw data into signal (encoding, "
 "transforms, dates, text), and &mdash; the one they really care about &mdash; can you **avoid "
 "leakage**? Fluency on both says \"I can be trusted with a model that touches production.\""))
p.append(B.h2("Say these out loud", kicker="Rapid-fire drill"))
p.append(B.interview_check([
 "Why does feature quality often matter **more** than model choice on tabular data?",
 "Which models need **feature scaling**, and which don't &mdash; why?",
 "A feature is heavily **right-skewed**. What do you do, and why?",
 "**One-hot vs. label** encoding &mdash; when is each right, and what's the classic bug?",
 "How would you encode a **high-cardinality** feature like zip code?",
 "What is **target encoding**, and why is it dangerous?",
 "Why encode `hour` and `month` with **sin/cos**?",
 "Explain **bag-of-words vs. TF&ndash;IDF**.",
 "Define **data leakage** and give two distinct kinds.",
 "Why must every learned transform be **fit on train only** &mdash; and how does a Pipeline enforce "
 "it?",
], title="The feature-engineering drill")
)
p.append(B.practice([
 {"q":"CASE: A candidate proudly reports a churn model with 99% accuracy. As the interviewer, what "
      "do you ask &mdash; and what are you testing?",
  "sol":"You're testing whether they can **smell leakage**. Good questions: *\"What features are in "
        "it &mdash; is any of them known only *after* churn happens (a cancellation date, a final "
        "invoice, an exit-survey field)?\"*; *\"How did you split &mdash; and did you fit your "
        "scalers/encoders/selectors on the whole dataset or inside the train fold?\"*; *\"Is the data "
        "temporal &mdash; did you split by time or randomly?\"*; *\"What's the base rate, and how does "
        "99% compare to a majority-class baseline?\"* The signal you want: the candidate treats "
        "near-perfect accuracy on a genuinely hard problem as a **red flag to investigate**, "
        "immediately reaches for target leakage and train/test contamination, and knows the fix "
        "(audit features for future information, wrap transforms in a Pipeline, split by time). A "
        "candidate who just celebrates the 99% has failed the question."},
 {"q":"CASE: \"You have a raw events table: user_id, event_type, timestamp, amount. Design features "
      "to predict whether a user will purchase in the next 7 days.\" Walk through it.",
  "sol":"First, **fix the prediction point** and only use data **before** it (guarding against "
        "temporal leakage). Then engineer across a few families: **recency** &mdash; days since last "
        "event / last purchase (usually the strongest signal); **frequency** &mdash; counts of "
        "events and purchases in trailing 7/30/90-day windows; **monetary** &mdash; sum/mean/max "
        "`amount` per window (log-transformed, since money is skewed); **behavioral mix** &mdash; "
        "share of each `event_type`, ratios like purchases-per-session; **temporal** &mdash; hour/"
        "day-of-week of typical activity (cyclically encoded), tenure = days since first event. "
        "Encode any categorical `event_type` by one-hot (low cardinality). **Crucially**, compute "
        "every windowed feature strictly up to the prediction date, split by **time**, and fit all "
        "transforms inside the training fold via a Pipeline. The narrative they want: RFM-style "
        "thinking (recency/frequency/monetary) + disciplined, leakage-free construction."},
]))
p.append(B.callout("note","The through-line of the whole track",
 "Feature engineering is where **domain knowledge becomes math** and where **discipline prevents "
 "disaster**. Surface the signal a model can't invent (ratios, cycles, recency, distinctive words); "
 "encode categories honestly; and &mdash; above all &mdash; fit every learned transform on train "
 "only so nothing leaks. The candidate who builds strong features *and* refuses to be fooled by a "
 "leaky 99% is the one who gets hired.", "&#9670;"))
LESSONS={"fe-06-interview":"\n".join(p)}
print("content_fe06 OK — chars:", len(LESSONS["fe-06-interview"]))
