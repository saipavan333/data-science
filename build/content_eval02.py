# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
p=[]
p.append(B.why(
 "A model's score on the data it **trained** on is worthless &mdash; of course it does well on "
 "questions it has already seen the answers to. The entire point of evaluation is to estimate how "
 "the model will do on data it has **never seen**. Getting that estimate honest &mdash; and keeping "
 "it honest &mdash; is **validation strategy**, and it's where a huge fraction of real-world "
 "\"our model was great in testing and failed in production\" disasters are actually born."))
p.append(B.h2("Three roles: train, validate, test", kicker="The sacred split"))
p.append(B.concept(
 "Split your data into three jobs:\n\n"
 "- **Training set** &mdash; the model learns its parameters here.\n"
 "- **Validation set** &mdash; you compare models and tune hyperparameters here, choosing what works "
 "best.\n"
 "- **Test set** &mdash; a locked vault opened **once**, at the very end, for a single honest "
 "estimate of real-world performance.\n\n"
 "The **golden rule**: the test set is **sacred**. Every time you look at it and adjust *anything*, "
 "you leak a little of it into your choices, and its estimate becomes optimistic. Touch it once."))
p.append(B.pitfall(
 "**Tuning against your test set turns it into a training set.** If you try 40 models and pick the "
 "one with the best *test* score, that score is no longer an unbiased estimate &mdash; you've "
 "overfit to the test set by selection. That's exactly why the *validation* set exists (to absorb "
 "all your experimentation) and why the test set is opened only for the final, already-decided "
 "model."))
p.append(B.h2("Cross-validation: a better estimate from limited data", kicker="k-fold"))
p.append(B.concept(
 "A single train/validation split is **wasteful** (the validation rows never train the model) and "
 "**noisy** (you got lucky or unlucky with which rows landed in validation). **k-fold "
 "cross-validation** fixes both: split the data into k parts, then train k times, each time holding "
 "out a different part for validation. Average the k scores for a far more **stable** estimate, and "
 "every row gets used for both training and validation:"))
_c,_o=_run(r'''
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=600, n_features=8, random_state=0)
scores = cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=5)

print("per-fold accuracy:", np.round(scores, 3))
print(f"honest estimate:   {scores.mean():.3f}  ±  {scores.std():.3f}")
print("(report the mean AND the spread — one split could have landed anywhere in that range)")
''')
p.append(B.code_example(_c,_o,filename="cross_val.py"))
p.append(B.h2("Pick the CV that matches your data", kicker="Stratified, grouped, time-series"))
p.append(B.concept(
 "Plain k-fold assumes rows are interchangeable. Often they're not &mdash; match the scheme to the "
 "structure or you'll leak:\n\n"
 "- **Stratified k-fold** &mdash; keeps each fold's **class balance** equal to the whole. Essential "
 "for imbalanced classification (else a fold might contain almost no positives).\n"
 "- **Grouped k-fold** &mdash; keeps all rows from one **entity** (a patient, a user, a store) "
 "**together** in the same fold. Without it, the model sees the same patient in train *and* "
 "validation &mdash; leakage that inflates scores.\n"
 "- **Time-series CV** &mdash; always train on the **past**, validate on the **future** (expanding/"
 "rolling windows). A random split on temporal data lets the model peek at the future &mdash; "
 "invalid."))
p.append(B.warn(
 "The most common validation leak is a **random split on data that has groups or time**. If the same "
 "user, customer, or patient can appear in both train and test, or if you shuffle time-ordered rows, "
 "your estimate is optimistic and will not survive production. Ask *\"what's the unit that must not "
 "straddle the split?\"* before choosing a CV scheme."))
p.append(B.h2("Your turn — turn folds into an honest estimate", kicker="Interactive lab"))
p.append(B.pylab(
 "Cross-validation gives you one score **per fold**. Report the honest headline: compute the "
 "**mean** of the `fold_scores`, round to **3 decimals**, and assign to **`answer`**. (In practice "
 "you'd quote this mean *and* its spread.)",
 "import numpy as np\n"
 "fold_scores = np.array([0.82, 0.79, 0.85, 0.80, 0.84])\n",
 "answer = round(float(fold_scores.mean()), 3)",
 starter="import numpy as np\n# the honest CV estimate is the mean across folds (3 dp)\nanswer = ",
 hint="`fold_scores.mean()`, cast to float, round to 3 decimals. (The spread is `fold_scores.std()` "
      "&mdash; worth reporting too.)",
 title="Lab — the cross-validated estimate",
 preview="numpy loaded; five per-fold accuracies preloaded. First Run boots Python.",
 explain="The mean (**0.82**) is your best single estimate; the spread across folds (~0.02 here) "
         "tells you how much a *single* split could have misled you. Reporting mean ± spread is far "
         "more honest than one lucky number &mdash; that's the whole reason to cross-validate."))
p.append(B.keypoints([
 "Split into **train** (learn), **validation** (tune/compare), and **test** (one final honest "
 "estimate).",
 "The **test set is sacred** &mdash; touch it once. Tuning against it turns it into a training set "
 "and inflates the score.",
 "**k-fold CV** gives a more stable, data-efficient estimate than one split &mdash; report **mean ± "
 "spread**.",
 "Match the scheme: **stratified** (imbalance), **grouped** (repeated entities), **time-series** "
 "(temporal) &mdash; or you leak.",
 "The classic leak: a **random split on grouped or time-ordered data** &mdash; ask what unit must "
 "not straddle the split.",
]))
p.append(B.quiz([
 {"q":"You tried 50 model configurations and picked the one with the best score on your test set. "
      "Why is that reported score misleading?",
  "options":[
   {"t":"By selecting the best of 50 on the test set, you overfit to it — the winning score is "
        "optimistic, not an unbiased estimate","correct":True,
    "why":"Correct. Choosing the max over many tries on the *test* set means the test data influenced "
          "your choice, so it's no longer unseen. Use the validation set (or nested CV) for "
          "selection and keep the test set for a single final check."},
   {"t":"50 is too few configurations to compare",
    "why":"The problem isn't too few &mdash; it's that selecting the best on the test set biases the "
          "estimate upward regardless of count."},
   {"t":"Nothing — picking the best test score is correct",
    "why":"That's the trap: repeated peeking + selection overfits the test set. It must be reserved "
          "for one final, pre-decided model."},
   {"t":"You should have used a larger test set",
    "why":"Size helps precision but doesn't fix the *selection bias* from tuning against the test "
          "set. Separate validation is the fix."}]},
 {"q":"You're predicting hospital readmission and each patient has several visits. Which CV scheme?",
  "options":[
   {"t":"Grouped k-fold, keeping all of a patient's visits in the same fold","correct":True,
    "why":"Correct. If a patient appears in both train and validation, the model learns that specific "
          "patient and the score is inflated &mdash; leakage. Grouped k-fold keeps each patient "
          "wholly within one fold."},
   {"t":"Plain random k-fold",
    "why":"That can put the same patient in train and validation, leaking patient-specific "
          "information and overstating performance."},
   {"t":"Time-series split",
    "why":"Useful if the question is temporal, but the key hazard here is *repeated patients*, which "
          "grouped k-fold addresses."},
   {"t":"A single 50/50 split",
    "why":"Still risks splitting a patient across sides, and wastes data; grouped k-fold is the right "
          "structural fix."}]},
]))
p.append(B.practice([
 {"q":"Explain why cross-validation is usually preferable to a single train/validation split, and one "
      "case where you might NOT use plain k-fold.",
  "sol":"**Why CV is better:** a single split wastes the validation rows (they never train the model) "
        "and is **noisy** &mdash; your estimate swings depending on which rows happened to land in "
        "validation. k-fold trains k times on different splits and **averages**, giving a more "
        "**stable, lower-variance** estimate that uses every row for both roles, plus a **spread** "
        "across folds that tells you how uncertain the estimate is. **When not to use plain k-fold:** "
        "when rows aren't exchangeable &mdash; **time-ordered** data (use forward-chaining time-series "
        "CV so you never train on the future), **grouped** data (use grouped k-fold so an entity "
        "doesn't straddle folds), or severe **imbalance** (use stratified k-fold so each fold keeps "
        "the class ratio). Plain k-fold silently leaks or destabilises in all three."},
 {"q":"What is nested cross-validation, and what problem does it solve?",
  "sol":"**Nested CV** runs two loops: an **inner** CV that selects hyperparameters, wrapped inside "
        "an **outer** CV that estimates performance. For each outer fold, you do a full inner-CV "
        "tuning on that fold's training portion, then score the chosen model on the outer fold's "
        "held-out data &mdash; which the tuning never touched. **Problem it solves:** if you tune and "
        "evaluate on the *same* CV, the reported score is optimistic because hyperparameters were "
        "chosen using the very data you're scoring on (selection leakage). Nested CV keeps model "
        "*selection* and performance *estimation* on separate data, yielding an **unbiased** estimate "
        "of the whole modelling-plus-tuning pipeline &mdash; at higher compute cost, which is why "
        "it's used when an honest estimate really matters (small data, research, high stakes)."},
]))
p.append(B.deepdive(
 B.concept(
  "**How big should each split be, and how many folds?** With plenty of data, a simple 60/20/20 "
  "train/val/test split is fine and cheap. As data shrinks, cross-validation earns its keep: **5- or "
  "10-fold** are the standard compromises (more folds &rarr; less bias, more variance and compute; "
  "**leave-one-out** is the extreme, often high-variance and rarely worth it). The deeper point is "
  "that evaluation itself has **variance** &mdash; report the spread across folds, and when comparing "
  "two models, ask whether their CV-score difference is larger than that fold-to-fold noise before "
  "declaring a winner.") +
 B.concept(
  "**The subtle enemy: overfitting to the validation set.** Even with a proper split, running dozens "
  "of experiments and always keeping the best validation score means you're slowly *fitting to the "
  "validation set* through selection &mdash; the 'garden of forking paths' from the experimentation "
  "track, wearing a modelling hat. Defenses: limit how much you sculpt to validation, use nested CV "
  "for an honest outer estimate, and above all keep the **test set truly untouched** until the end. "
  "A useful mental model: the test set is a **one-shot exam** &mdash; the moment you use it to make a "
  "decision, you've spent it, and any further use only tells you how well you've memorised the exam, "
  "not how well you'll do on new questions."),
 title="Deep dive: choosing fold count, evaluation variance, and overfitting the validation set"))
LESSONS={"eval-02-validation":"\n".join(p)}
print("content_eval02 OK — chars:", len(LESSONS["eval-02-validation"]))
