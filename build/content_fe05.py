# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]
p.append(B.why(
 "This lesson covers the technique that removes features (**selection**) and the bug that "
 "silently invents performance (**leakage**). Leakage is the **single most dangerous mistake in "
 "applied machine learning**: it makes your model look brilliant in validation and then fail in "
 "production, and it has sunk real projects, papers, and Kaggle careers. If you learn one thing "
 "defensively in this whole track, learn to smell leakage."))
p.append(B.h2("Feature selection: fewer, better features", kicker="Why less can be more"))
p.append(B.concept(
 "More features isn't always better. Irrelevant ones add **noise** the model can overfit to, slow "
 "training, and hurt interpretability &mdash; the *curse of dimensionality*. Three families of "
 "selection:\n\n"
 "- **Filter** &mdash; score each feature against the target independently (correlation, mutual "
 "information, a chi-square test) and keep the top ones. Fast, model-agnostic.\n"
 "- **Wrapper** &mdash; let a model choose, adding/removing features and measuring effect (e.g. "
 "recursive feature elimination). Powerful but slow.\n"
 "- **Embedded** &mdash; the model selects *while training*: **L1 (Lasso)** regularization drives "
 "useless coefficients to exactly zero; **tree importances** rank features. Often the best "
 "value-for-effort."))
p.append(B.h2("Data leakage: when your model sees the future", kicker="The deadliest bug"))
p.append(B.concept(
 "**Leakage** is when information that wouldn't be available at prediction time sneaks into training. "
 "Two flavours dominate:\n\n"
 "- **Train&ndash;test contamination**: fitting *any* learned transform (scaler, imputer, encoder, "
 "feature selector) on the **whole** dataset before splitting &mdash; so the test set leaks into the "
 "features. The fix is the picture below.\n"
 "- **Target leakage**: a feature that is really a **proxy for the label** or uses "
 "*future* information &mdash; e.g. `account_closed_date` when predicting churn, or "
 "`total_paid_this_year` when predicting whether they'll pay. It looks amazing and is a mirage."))
p.append(B.figure(IMG+"s_fe_leakage.png",
 "**Split first, then fit.** *Wrong* (top): fit scaling / feature selection on **all** the data, so "
 "it has already seen the test set &mdash; scores come out optimistic. *Right* (bottom): **split "
 "first**, fit every learned transform on the **training** fold only, then apply those fixed "
 "parameters to test. A Pipeline enforces this automatically.",
 "Two flows: wrong (fit on all data then split) vs right (split first, fit on train, apply to test)."))
p.append(B.h2("Watch leakage manufacture accuracy from pure noise", kicker="The demo that scares people"))
p.append(B.concept(
 "Here's the demonstration that makes leakage unforgettable. We generate **completely random** "
 "features and **random** labels &mdash; there is *no* signal, so honest accuracy must be ~50%. Then "
 "we select the \"best\" 20 features using the **whole** dataset before cross-validating. Watch the "
 "accuracy lie:"))
_c,_o=_run(r'''
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

rng = np.random.default_rng(0)
X = rng.normal(size=(200, 5000))         # 5000 PURE-NOISE features
y = rng.integers(0, 2, size=200)         # RANDOM labels -> no real signal

# WRONG: pick the 20 "best" features using ALL rows, THEN cross-validate
Xsel = SelectKBest(f_classif, k=20).fit_transform(X, y)
leaky = cross_val_score(LogisticRegression(max_iter=1000), Xsel, y, cv=5).mean()

# RIGHT: selection happens INSIDE each CV fold (train-only), via a Pipeline
pipe = Pipeline([("sel", SelectKBest(f_classif, k=20)),
                 ("clf", LogisticRegression(max_iter=1000))])
honest = cross_val_score(pipe, X, y, cv=5).mean()

print(f"LEAKY  accuracy (select before CV): {leaky:.0%}   <- on PURE NOISE!")
print(f"HONEST accuracy (select inside CV): {honest:.0%}   <- ~chance, the truth")
''')
p.append(B.code_example(_c,_o,filename="leakage_demo.py"))
p.append(B.pitfall(
 "Read that again: **~70% accuracy on data with no signal whatsoever.** The feature selector, by "
 "peeking at the labels of *all* rows (including the CV test folds) when choosing features, handed "
 "the model a cheat sheet. The honest pipeline &mdash; selecting inside each fold on train data only "
 "&mdash; correctly reports **chance**. If your validation score seems too good to be true, suspect "
 "leakage **first**."))
p.append(B.h2("Your turn — scale test data the leakage-free way", kicker="Interactive lab"))
p.append(B.pylab(
 "The rule: standardize the **test** set using the **training** set's mean and std &mdash; never "
 "statistics recomputed on test. Compute `mu` and `sd` from **`train`**, standardize **`test`** with "
 "them, and assign the **mean of the standardized test values** (rounded to **2 decimals**) to "
 "**`answer`**.",
 "import numpy as np\n"
 "train = np.array([10, 12, 14, 16, 18, 20], dtype=float)\n"
 "test  = np.array([13, 17, 21], dtype=float)\n",
 "mu, sd = train.mean(), train.std()\n"
 "answer = round(float(((test - mu) / sd).mean()), 2)",
 starter="import numpy as np\n# mu, sd from TRAIN only; standardize TEST with them; mean of result\nanswer = ",
 hint="`mu, sd = train.mean(), train.std()` (train only!), then `(test - mu)/sd`, take `.mean()`, "
      "round to 2 dp. Do NOT use test.mean()/test.std().",
 title="Lab — fit on train, apply to test",
 preview="numpy loaded; `train` and `test` arrays preloaded. First Run boots Python.",
 explain="The standardized test mean isn't 0 &mdash; and that's correct! Only the *training* set is "
         "centered to mean 0; the test set is transformed with the **same** train parameters, so its "
         "mean reflects how test differs from train. Recomputing stats on test would be leakage."))
p.append(B.keypoints([
 "**Feature selection** (filter / wrapper / embedded) trims noise features &mdash; L1 and tree "
 "importances are the best value-for-effort.",
 "**Leakage** = information at train time that won't exist at prediction time; it inflates "
 "validation and collapses in production.",
 "**Train&ndash;test contamination**: fit scalers/imputers/encoders/selectors on **train only**, "
 "then apply to test &mdash; **split first**.",
 "**Target leakage**: a feature that's a proxy for the label or uses the future (e.g. "
 "`closed_date` for churn) &mdash; drop it.",
 "Selecting features on the **whole** dataset can score ~70% **on pure noise** &mdash; if a result "
 "looks too good, **suspect leakage first**.",
]))
p.append(B.quiz([
 {"q":"A churn model gets 99.5% accuracy. Which feature is the most likely culprit for leakage?",
  "options":[
   {"t":"`account_cancellation_date` — it only exists *because* the user churned, so it's a proxy for "
        "the label","correct":True,
    "why":"Correct. A cancellation date is populated only for churned users and reflects information "
          "from *after* the prediction point &mdash; classic target leakage. Remove it (and audit "
          "anything else that's only known post-outcome)."},
   {"t":"`tenure_months` — how long they've been a customer",
    "why":"Tenure is known at prediction time and is a legitimate feature; it doesn't encode the "
          "future outcome."},
   {"t":"`monthly_plan_price`",
    "why":"Plan price is available before churn happens &mdash; a normal feature, not leakage."},
   {"t":"`num_support_tickets`",
    "why":"Ticket counts up to the prediction point are legitimate. The red flag is a field that "
          "exists only *because* the outcome occurred."}]},
 {"q":"Why must feature selection happen INSIDE cross-validation rather than once on the full "
      "dataset?",
  "options":[
   {"t":"Selecting on the full data lets the CV test folds influence which features are chosen, "
        "leaking their labels and inflating the score","correct":True,
    "why":"Correct. If selection sees every row's label (including future test folds), the chosen "
          "features are tuned to the test data &mdash; the demo hit ~70% on pure noise. Selection "
          "must be refit within each fold's training portion."},
   {"t":"It runs faster inside CV",
    "why":"It's actually more work inside CV; the reason is *correctness* &mdash; preventing the test "
          "folds from leaking into selection."},
   {"t":"CV requires exactly the same features each fold",
    "why":"Folds can legitimately select different features; the point is that selection must use "
          "only each fold's training data to avoid leakage."},
   {"t":"It doesn't matter where you select",
    "why":"It matters enormously &mdash; selecting on all data manufactures accuracy from noise, as "
          "the demo showed."}]},
]))
p.append(B.practice([
 {"q":"Give a checklist you'd run through to catch leakage before trusting a suspiciously good model.",
  "sol":"**(1) Audit each feature for the future:** is any value known only *after* the prediction "
        "point, or populated only when the outcome occurs (dates, totals, post-event flags)? Drop "
        "them. **(2) Check the pipeline boundary:** are all learned transforms (scaler, imputer, "
        "encoder, selector, TF-IDF) fit **inside** the CV/train fold, not on the full dataset? **(3) "
        "Respect time:** for temporal data, split by **time** (train on past, test on future), never "
        "randomly &mdash; and make sure no feature aggregates across the split. **(4) Sanity-check "
        "the score:** near-perfect accuracy on a hard problem is a leakage alarm, not a triumph. **(5) "
        "Look for ID/duplicate leakage:** the same entity in both train and test, or a row-order/"
        "index artifact correlated with the label. Running this list turns 'too good to be true' into "
        "'find the leak.'"},
 {"q":"You're predicting whether a loan will default, using data as of application time. Why is "
      "`number_of_late_payments` a leakage risk, and how do you fix it?",
  "sol":"It depends on **when** those late payments are counted. If the field tallies late payments "
        "over the **whole life of the loan** (including *after* application, as the borrower heads "
        "toward default), it encodes the future outcome &mdash; a borrower defaults *because* they "
        "missed payments, so the feature is a proxy for the label and will leak. **Fix:** restrict "
        "every feature to information available **strictly at or before the application/decision "
        "point** &mdash; e.g. late payments on *prior* loans up to application date only. Enforce this "
        "with a **time-aware split** and per-feature 'as-of' timestamps so nothing aggregates across "
        "the prediction moment. The principle: a feature is only legitimate if it would genuinely be "
        "known at the instant you make the prediction."},
]))
p.append(B.deepdive(
 B.concept(
  "**Temporal leakage is the sneakiest kind.** With any time-ordered data (transactions, sensor "
  "readings, user events), a **random** train/test split lets the model train on the future to "
  "predict the past &mdash; a luxury it will never have in production. You must split by **time** "
  "(train on earlier periods, validate on later ones), and ensure no feature secretly aggregates "
  "across that boundary (a 'total spend' or rolling mean that peeks forward). Even a global "
  "`StandardScaler` fit on all time periods leaks the future's distribution. Time-series cross-"
  "validation (expanding or rolling windows) exists precisely to make evaluation honest here.") +
 B.concept(
  "**Why the Pipeline is a correctness tool, not a convenience.** Wrapping every learned step "
  "(`imputer &rarr; scaler &rarr; encoder &rarr; selector &rarr; model`) in a scikit-learn "
  "**Pipeline** means that when you call `cross_val_score` or `GridSearchCV`, **each fold refits the "
  "entire chain on that fold's training data only** &mdash; making train&ndash;test contamination "
  "structurally impossible. Doing the steps by hand, it's fatally easy to fit a scaler or selector "
  "once on all the data and forget. So the Pipeline isn't just tidy code; it's the mechanism that "
  "*enforces* the fit-on-train-only rule across your whole feature-engineering stack. This is why "
  "'always use a Pipeline' is the standard senior advice &mdash; it turns a discipline you might "
  "forget into a guarantee the library keeps for you."),
 title="Deep dive: temporal leakage, time-aware splits, and Pipelines as leakage insurance"))
LESSONS={"fe-05-selection":"\n".join(x for x in p if x)}
print("content_fe05 OK — chars:", len(LESSONS["fe-05-selection"]))
