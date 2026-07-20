# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "You now know several models &mdash; but at work the question is always *\"which one, with which "
 "settings, and how well will it really do?\"* Answer that wrong and you'll ship a model that looked "
 "great in your notebook and falls apart in production. This lesson is the discipline that prevents "
 "that: ~cross-validation~ for an honest performance estimate, a clean way to **tune** without "
 "cheating, and the single most dangerous mistake in all of applied machine learning &mdash; "
 "~data leakage~. This is the craft that separates people who *run* models from people who can be "
 "**trusted** with them."))

p.append(B.h2("Why one split isn't enough", kicker="Concept"))
p.append(B.concept(
 "Back in Lesson 8.1 you held out a test set. But a **single** train/test split has two problems: it "
 "wastes data (the test rows never help training), and it's a coin-flip &mdash; a lucky or unlucky "
 "split can make a model look better or worse than it is, so you can't trust a small difference "
 "between two models. You want a performance estimate that uses **all** the data and doesn't hinge "
 "on one arbitrary split. That's what cross-validation gives you."))

p.append(B.h2("k-fold cross-validation", kicker="Concept · the workhorse")
)
p.append(B.concept(
 "~k-fold cross-validation~ splits the data into `k` equal ~folds~ (5 is standard). Then it trains "
 "`k` times: each round holds out **one** fold as the test set and trains on the other `k-1`, "
 "rotating so **every** fold gets its turn as the test set exactly once. You average the `k` scores "
 "for a stable estimate &mdash; and their spread tells you how much that estimate wobbles:"))
p.append(B.figure(IMG+"s_ml_kfold.png",
 "**5-fold cross-validation.** Each row is one training run: the amber fold is held out for testing, "
 "the blue folds train the model. Rotate through all five, average the five scores. Every row uses a "
 "different test fold, so every data point is tested on exactly once.",
 "Five rows of five folds each; in each row a different fold is highlighted as the test set."))

p.append(B.h2("Tuning without cheating", kicker="Concept · the validation trap")
)
p.append(B.concept(
 "Here's the trap that catches everyone once. You try 50 settings, keep whichever scores best on "
 "your test set, and report that score. But by **selecting** on the test set, you've fit to its "
 "noise &mdash; the number is now optimistic and won't hold. The rule: **the test set is opened "
 "once, at the very end, and never used to make a choice.** All model comparison and hyperparameter "
 "tuning happens with **cross-validation on the training data** (tools like ~GridSearchCV~ automate "
 "trying combinations, each scored by CV). Only after everything is locked do you touch the test set "
 "for a single final estimate."))

p.append(B.h2("Data leakage: the silent killer", kicker="Concept · the one that bites")
)
p.append(B.pitfall(
 "~Data leakage~ is when information from outside the training data sneaks into training, inflating "
 "your scores in a way that **vanishes in production**. The classic: you standardise or impute using "
 "statistics from the **whole** dataset *before* splitting &mdash; so the training folds have "
 "peeked at the test fold's mean. The fix is ironclad: **fit every preprocessing step on the "
 "training fold only**, inside the cross-validation loop &mdash; which is exactly what a scikit-learn "
 "~Pipeline~ enforces. Other leaks: a feature that's a proxy for the target (a \"days until churn\" "
 "column when predicting churn), or shuffling time-series data so the future trains on... itself."))

p.append(B.h2("Cross-validate in scikit-learn", kicker="Worked example"))
p.append(B.concept(
 "One function does the whole rotate-and-average dance. The individual fold scores and their spread "
 "are as informative as the mean:"))
_c,_o=_run(r'''
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=500, n_features=8, n_informative=5, random_state=2)

scores = cross_val_score(RandomForestClassifier(n_estimators=100, random_state=0), X, y, cv=5)

print("score per fold:", [f"{s:.3f}" for s in scores])
print(f"mean accuracy : {scores.mean():.3f}")
print(f"std (wobble)  : {scores.std():.3f}")
''')
p.append(B.code_example(_c,_o,filename="cross_validation.py"))
p.append(B.concept(
 "Five folds, five scores, one honest average &mdash; and the standard deviation tells you how much "
 "to trust it. If two models' CV means differ by less than this wobble, the difference probably "
 "isn't real. **This mean, not any single split, is the number you compare models by.**"))

p.append(B.h2("Your turn — cross-validate a model", kicker="Interactive lab"))
p.append(B.pylab(
 "`X`, `y`, `cross_val_score`, and `RandomForestClassifier` are loaded. Run **5-fold** "
 "cross-validation on a 100-tree random forest and assign to **`answer`** the **mean** accuracy "
 "across the folds, rounded to 2 decimals.",
 "from sklearn.datasets import make_classification\n"
 "from sklearn.ensemble import RandomForestClassifier\n"
 "from sklearn.model_selection import cross_val_score\n"
 "X, y = make_classification(n_samples=500, n_features=8, n_informative=5, random_state=2)\n",
 "scores = cross_val_score(RandomForestClassifier(n_estimators=100, random_state=0), X, y, cv=5)\n"
 "answer = round(float(scores.mean()), 2)",
 starter="# X, y, cross_val_score, RandomForestClassifier loaded\nscores = \nanswer = ",
 hint="`cross_val_score(RandomForestClassifier(n_estimators=100, random_state=0), X, y, cv=5)` "
      "returns 5 scores; take `.mean()` and `round(float(...), 2)`.",
 title="Lab — a 5-fold estimate",
 preview="`X`, `y` loaded; `cross_val_score` + `RandomForestClassifier` imported. First Run loads "
         "scikit-learn.",
 explain="The mean of the fold scores is a far more trustworthy estimate than any single split, and "
         "it's the number you'd use to compare against another model."))

p.append(B.keypoints([
 "A single train/test split wastes data and is a coin-flip; ~cross-validation~ gives a stable "
 "estimate using **all** the data.",
 "~k-fold CV~: split into `k` folds, train `k` times each holding out a different fold, then average "
 "the scores (and note their spread).",
 "**Tune and compare with CV on the training data**; open the ~test set~ **once**, at the very end. "
 "Selecting on the test set inflates your estimate.",
 "~Data leakage~ &mdash; letting test information into training (e.g., scaling before splitting) "
 "&mdash; inflates scores that then collapse in production. Fit preprocessing **inside** CV via a "
 "~Pipeline~.",
 "Compare models by their **CV mean**; a gap smaller than the CV spread probably isn't real.",
]))

p.append(B.quiz([
 {"q":"What does 5-fold cross-validation actually do?",
  "options":[
   {"t":"Splits data into 5 folds and trains 5 times, each holding out a different fold as the test "
        "set, then averages the 5 scores","correct":True,
    "why":"Correct. Every fold serves as the test set exactly once; averaging the five results gives a "
          "stable estimate that uses all the data."},
   {"t":"Trains the model 5 times on the same split to reduce randomness",
    "why":"The folds differ each round — that's the point. Repeating an identical split wouldn't test "
          "on different data."},
   {"t":"Splits the data into 5 features",
    "why":"Folds are subsets of rows, not features. CV rotates which rows are held out for testing."},
   {"t":"Picks the single best of 5 models to ship",
    "why":"CV estimates performance by averaging; it isn't a model-selection-by-best-fold. You refit "
          "on all data once settings are chosen."}]},
 {"q":"You standardize features using the mean/std of the whole dataset, then split into train/test. "
      "Why is this a problem?",
  "options":[
   {"t":"It's data leakage — the scaler saw the test set, so training peeked at test information and "
        "your score is optimistic","correct":True,
    "why":"Correct. Preprocessing must be fit on training data only. Using whole-dataset statistics "
          "lets the test fold influence training, inflating the estimate in a way that won't hold in "
          "production. Fit the scaler inside CV (a Pipeline)."},
   {"t":"It's fine — scaling never causes problems",
    "why":"Scaling with whole-data statistics before splitting is a textbook leak. It must be fit on "
          "the training portion only."},
   {"t":"It makes the model too slow",
    "why":"Speed isn't the issue; correctness is. The leak biases your performance estimate upward."},
   {"t":"Standardizing is never needed",
    "why":"Some models need it (k-means, logistic regression). The issue isn't whether to scale, but "
          "fitting the scaler on training data only."}]},
 {"q":"You try 40 hyperparameter combinations and report the one that scored best on your test set. "
      "What's wrong?",
  "options":[
   {"t":"You selected on the test set, so the reported score is optimistically biased and won't hold "
        "on new data","correct":True,
    "why":"Correct. Choosing the best of many by test-set score fits to that set's noise. Tune with "
          "cross-validation on the training data and touch the test set only once, at the end."},
   {"t":"Nothing — the test set is exactly for picking the best model",
    "why":"That's the trap. Using the test set to *choose* leaks it into your process; it's meant "
          "only for a single final, untouched estimate."},
   {"t":"40 combinations is too few to matter",
    "why":"The count isn't the issue; selecting on the test set at all is. Even a few choices bias the "
          "estimate."},
   {"t":"You should have used a bigger test set",
    "why":"Size doesn't fix the bias from selecting on it. Use validation/CV for selection instead."}]},
]))

p.append(B.practice([
 {"q":"Model A has CV accuracy 0.812 &plusmn; 0.020; Model B has 0.818 &plusmn; 0.019. Which do you "
      "ship, and why?",
  "sol":"The gap (0.006) is **much smaller** than the fold-to-fold wobble (~0.02), so the difference "
        "is almost certainly noise, not a real edge &mdash; treat A and B as tied on accuracy. I'd "
        "choose on other grounds: **simplicity/interpretability**, training and inference **speed**, "
        "robustness, and maintenance cost. Chasing a 0.6% CV difference that's inside the noise is how "
        "you overfit your model *selection*."},
 {"q":"You're predicting whether a loan will default, using data that includes a `days_late` column. "
      "Your model scores 0.99. What would you check first?",
  "sol":"That score screams ~leakage~. `days_late` is essentially a **consequence** of defaulting "
        "(you only rack up late days if you're defaulting), so it's a proxy for the target that "
        "wouldn't be available *at prediction time* (when you decide to grant the loan). I'd remove "
        "any feature that couldn't exist at the moment of prediction, re-evaluate, and audit the rest "
        "for target proxies. A 0.99 on a hard real-world problem is a red flag, not a trophy."},
]))

p.append(B.deepdive(
 B.concept(
  "**Match the fold to the data.** Plain k-fold shuffles rows, which is wrong for some data. "
  "~Stratified~ k-fold keeps each fold's class balance equal to the whole (essential for imbalanced "
  "classification). ~Group~ k-fold keeps all rows from the same entity (a patient, a user) in the "
  "*same* fold, so the model can't memorise an individual and get tested on them. ~Time-series~ "
  "split always trains on the **past** and tests on the **future**, never shuffling time &mdash; "
  "because in production you only ever have the past. Using ordinary k-fold on grouped or temporal "
  "data is a subtle, common leak.") +
 B.concept(
  "**Tuning, and the trap inside the trap.** You search hyperparameters (~GridSearchCV~ tries a grid, "
  "~RandomizedSearchCV~ samples it), each candidate scored by CV. But if you then report that best "
  "CV score as your performance, you've *selected* on it &mdash; the same optimism, one level up. The "
  "clean answer is ~nested cross-validation~: an inner CV picks the settings, an outer CV estimates "
  "performance, so selection and evaluation never touch the same data. For most work, the simpler "
  "discipline &mdash; CV to tune, a locked-away test set opened once &mdash; is enough.") +
 B.concept(
  "**Pipelines aren't optional hygiene &mdash; they're the leak-proofing.** A scikit-learn "
  "`Pipeline` chains preprocessing (scaling, imputing, encoding) with the model into one object. "
  "When that pipeline is passed to `cross_val_score`, every step is re-fit on each training fold "
  "alone, so no test information ever leaks through preprocessing. Building a Pipeline from day one "
  "is the habit that makes leakage structurally impossible &mdash; a large part of why senior "
  "practitioners insist on it."),
 title="Deep dive: stratified/group/time-series CV, nested CV, and leak-proof Pipelines"))

p.append(B.callout("note","Interview-ready",
 "The trio interviewers want: **cross-validation** (rotate k folds, average &mdash; a stable "
 "estimate using all data); **never tune or select on the test set** (CV on training to tune, test "
 "opened once at the end); and **data leakage** (test info reaching training &mdash; e.g., scaling "
 "before splitting &mdash; fixed by fitting preprocessing inside a Pipeline within CV). Add "
 "time-series split for temporal data and you'll sound seasoned.", "&#9670;"))

LESSONS={"ml-07-selection":"\n".join(p)}
print("content_m07 OK — chars:", len(LESSONS["ml-07-selection"]))
