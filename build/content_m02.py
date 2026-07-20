# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Linear regression is the workhorse you will fit a hundred times, and the foundation nearly every "
 "other model builds on. It answers the most common question in analytics &mdash; *\"if this goes "
 "up by one, what happens to that?\"* &mdash; with a single, honest line. It is also the most "
 "**interpretable** model there is: no black box, just a slope you can explain to your boss. Master "
 "it and you understand the skeleton of machine learning; every fancier model is a variation on the "
 "idea you meet here."))

p.append(B.h2("The line of best fit", kicker="Concept"))
p.append(B.concept(
 "~Linear regression~ models a numeric target `y` as a straight-line function of a feature `x`:\n\n"
 "> &#375; = a + b&middot;x\n\n"
 "`b` is the ~slope~ &mdash; how much the prediction changes for each one-unit increase in `x` "
 "(the effect you care about). `a` is the ~intercept~ &mdash; the prediction when `x` is zero. The "
 "little hat on `&#375;` means \"predicted\", to distinguish the model's guess from the actual "
 "value `y`. With more than one feature it becomes `&#375; = a + b&#8321;x&#8321; + b&#8322;x&#8322; "
 "+ &hellip;`, a weighted sum &mdash; but the intuition is the same."))
p.append(B.figure(IMG+"s_ml_linreg.png",
 "**Linear regression fits a line through a cloud of points.** Each dashed red segment is a "
 "~residual~ &mdash; the vertical gap between an actual point and the line's prediction. The "
 "best-fit line is the one that makes those gaps, squared and summed, as small as possible.",
 "Scatter plot of advertising spend vs sales with a best-fit line and dashed residual segments."))

p.append(B.h2("What \"best\" means: least squares", kicker="Concept · the heart of it"))
p.append(B.concept(
 "There are infinitely many lines you could draw; which one is *best*? For each data point, the "
 "~residual~ is `actual - predicted` = `y - &#375;`. A good line makes the residuals small overall. "
 "The standard recipe, ~ordinary least squares~, chooses `a` and `b` to minimise the **sum of the "
 "squared residuals** (`&Sigma;(y - &#375;)&sup2;`). Why *squared*? Two reasons: squaring makes "
 "every miss positive (so gaps above and below don't cancel out), and it **punishes big misses far "
 "more than small ones**, so the line refuses to sit far from any point. Drag the points below and "
 "watch the line re-solve to keep that squared error as small as it can:"))
p.append(B.widget("regression", "Drag the points — watch least squares re-solve the line",
 "Every time you move a point, the line instantly recomputes to minimise the sum of squared "
 "residuals (the dashed red gaps). Drag one point far off the trend: the whole line tilts toward "
 "it, because a big squared residual is expensive. That pull is exactly why outliers hurt linear "
 "regression.", height=440))

p.append(B.h2("Fit one in scikit-learn", kicker="Worked example"))
p.append(B.concept(
 "You will almost never compute `a` and `b` by hand &mdash; `scikit-learn` (Python's ML library) "
 "does it in three lines. Here we fit sales against advertising spend, read off the slope and "
 "intercept, check the fit, and make a prediction:"))
_c,_o=_run(r'''
import numpy as np
from sklearn.linear_model import LinearRegression

# advertising spend ($000s) -> sales ($000s)
X = np.array([1,2,3,4,5,6,7,8,9,10]).reshape(-1, 1)   # features must be 2-D: one column
y = np.array([2.1,3.9,3.2,5.8,5.1,7.4,7.9,7.2,9.6,9.1])

model = LinearRegression().fit(X, y)

print(f"slope    b = {model.coef_[0]:.3f}   (sales rise ~{model.coef_[0]:.2f}k per $1k of ad spend)")
print(f"intercept a = {model.intercept_:.3f}")
print(f"R^2        = {model.score(X, y):.3f}   (share of variation the line explains)")
pred = model.predict([[6.5]])[0]
print(f"predict spend = 6.5  ->  sales = {pred:.2f}k")
''')
p.append(B.code_example(_c,_o,filename="linear_regression.py"))
p.append(B.concept(
 "Read it like a sentence: each extra $1,000 of advertising is associated with about **$800 more "
 "sales** (the slope), the model explains **~91%** of the variation in sales (`R&sup2;` close to 1 "
 "is a tight fit), and it predicts a spend of 6.5 lands near $6,900 in sales. Three lines of code, "
 "and you can defend every number."))

p.append(B.h2("Your turn — fit and predict", kicker="Interactive lab"))
p.append(B.pylab(
 "`X` (advertising spend, a 2-D array) and `y` (sales) are loaded, and `LinearRegression` is "
 "imported. Fit a model to `X` and `y`, then assign to **`answer`** the predicted sales when spend "
 "= **12**, rounded to 2 decimals.",
 "import numpy as np\n"
 "from sklearn.linear_model import LinearRegression\n"
 "X = np.array([1,2,3,4,5,6,7,8,9,10]).reshape(-1,1)\n"
 "y = np.array([2.1,3.9,3.2,5.8,5.1,7.4,7.9,7.2,9.6,9.1])\n",
 "model = LinearRegression().fit(X, y)\nanswer = round(float(model.predict([[12]])[0]), 2)",
 starter="# X and y are loaded; LinearRegression is imported\nmodel = \nanswer = ",
 hint="Fit with `LinearRegression().fit(X, y)`, then call `model.predict([[12]])` and take element "
      "`[0]`, wrapped in `round(float(...), 2)`.",
 title="Lab — fit a model, make a prediction",
 preview="`X` &rarr; spend (2-D), `y` &rarr; sales; `LinearRegression` imported. First Run loads "
         "scikit-learn (~15s).",
 explain="`.fit` finds the least-squares line; `.predict([[12]])` extrapolates it to a spend of 12 "
         "(&#8776; 11.31k sales)."))

p.append(B.keypoints([
 "~Linear regression~ predicts a number as `&#375; = a + b&middot;x`: `b` (~slope~) is the effect "
 "per unit of `x`; `a` (~intercept~) is the value at `x = 0`.",
 "A ~residual~ is `actual - predicted`. ~Ordinary least squares~ picks the line that minimises the "
 "**sum of squared residuals**.",
 "Squaring the residuals makes misses positive and **punishes large errors most** &mdash; which is "
 "why a single ~outlier~ can tilt the whole line.",
 "In code it is three lines: `LinearRegression().fit(X, y)`, then read `model.coef_` / "
 "`model.intercept_` and call `model.predict(...)`.",
 "~R&sup2;~ is the share of the target's variation the line explains (0 = useless, 1 = perfect) "
 "&mdash; a quick read on fit quality.",
]))

p.append(B.quiz([
 {"q":"A house-price regression gives slope b = 150 for square footage (price in $, size in sq ft). "
      "What does that mean?",
  "options":[
   {"t":"Each extra square foot is associated with about $150 more predicted price","correct":True,
    "why":"Correct. The slope is the change in the prediction per one-unit increase in the feature "
          "— here, +$150 of predicted price per additional square foot."},
   {"t":"A 150 sq ft house costs $1",
    "why":"The slope isn't a total price; it's the rate of change. It says price rises ~$150 for each "
          "additional square foot."},
   {"t":"The model is 150% accurate",
    "why":"Accuracy isn't measured by the slope. The slope is the estimated effect of the feature; "
          "fit quality is read from R^2 or an error metric."},
   {"t":"Square footage explains 150% of the price",
    "why":"That's not what a coefficient means, and explained variation (R^2) can't exceed 1 (100%)."}]},
 {"q":"Why does least squares use the *squared* residuals rather than just the raw residuals?",
  "options":[
   {"t":"Squaring keeps every miss positive and penalizes big errors far more than small ones","correct":True,
    "why":"Correct. Raw residuals (some positive, some negative) would cancel out; squaring makes them "
          "all positive and grows quadratically, so the fit works hard to avoid any large gap."},
   {"t":"Squaring makes the math impossible to solve",
    "why":"The opposite — squared error has a clean closed-form (and convex) solution, which is part "
          "of why it's the standard choice."},
   {"t":"Because residuals are always negative",
    "why":"Residuals can be positive or negative (points above or below the line). Squaring is what "
          "removes the sign so they don't cancel."},
   {"t":"To make the line pass through every point",
    "why":"A straight line generally can't pass through every point; least squares finds the best "
          "compromise, not a perfect fit."}]},
 {"q":"An R&sup2; of 0.30 on a linear model most likely means:",
  "options":[
   {"t":"The line explains only 30% of the target's variation — a weak linear fit","correct":True,
    "why":"Correct. R^2 is the fraction of variance explained; 0.30 means 70% is left unexplained, so "
          "the linear relationship is weak (or the true relationship isn't linear)."},
   {"t":"The model is 30% accurate on new data",
    "why":"R^2 measures variance explained on the data given, not accuracy on new data (and isn't a "
          "simple 'percent correct')."},
   {"t":"30% of the data points are outliers",
    "why":"R^2 says nothing directly about how many outliers there are; it's about how much variation "
          "the line captures."},
   {"t":"The slope is 0.30",
    "why":"R^2 and the slope are different quantities; a small R^2 doesn't fix the slope's value."}]},
]))

p.append(B.practice([
 {"q":"You fit a regression predicting monthly revenue from number of salespeople and get "
      "`intercept = 20000`, `slope = 8000`. In plain English, what does the model predict for a "
      "team of 5, and what does the intercept mean?",
  "sol":"Prediction = `20000 + 8000*5 = $60,000`. The **slope** says each additional salesperson is "
        "associated with about **$8,000 more** monthly revenue. The **intercept** ($20,000) is the "
        "model's prediction with **zero** salespeople &mdash; a baseline that may or may not be "
        "meaningful (extrapolating to x = 0 can be nonsense if you never observed a team that small; "
        "treat it as a math anchor, not gospel)."},
 {"q":"A colleague's regression line looks great (high R&sup2;) but one extreme point sits far from "
      "all the others. Why might that be a problem, and what would you check?",
  "sol":"Because least squares **squares** residuals, a single far-off point (a high-~leverage~ "
        "outlier) can pull the line toward itself and inflate or distort the slope &mdash; and it "
        "can even prop up R&sup2;. Check by **plotting** the data and the residuals, refitting "
        "**without** the point to see how much the slope moves, and deciding whether the point is a "
        "data error or a real (but rare) case that deserves separate treatment."},
]))

p.append(B.deepdive(
 B.concept(
  "**R&sup2;, precisely.** `R&sup2; = 1 - SS_res / SS_tot`, where `SS_res` is the sum of squared "
  "residuals from your line and `SS_tot` is the sum of squared deviations from just the mean of `y`. "
  "So R&sup2; asks: *how much better is my line than simply predicting the average every time?* "
  "1.0 means the line nails every point; 0 means it's no better than the mean; it can even go "
  "**negative** on new data if the model is worse than the mean. Crucially, a high R&sup2; on the "
  "**training** data says nothing about new data &mdash; that's why we hold out a test set (Lesson "
  "8.1).") +
 B.concept(
  "**The assumptions behind the honest version.** Ordinary least squares gives a fit no matter what, "
  "but its *inferences* (confidence intervals, p-values on the coefficients) rely on four "
  "assumptions: a genuinely ~linear~ relationship, ~independent~ observations, ~constant variance~ "
  "of the residuals (homoscedasticity), and roughly ~normal~ residuals. The single best way to check "
  "them is a **residual plot**: residuals scattered structurelessly around zero is healthy; a curve, "
  "a funnel, or clusters means an assumption is violated and your slope's error bars can't be "
  "trusted. Regression is a bridge from Track 4's statistics to modelling &mdash; the fit is easy, "
  "the honesty is the craft.") +
 B.concept(
  "**Where it goes next: regularization.** With many features, plain least squares can ~overfit~ "
  "&mdash; chasing noise by inflating coefficients. ~Ridge~ regression adds a penalty on the "
  "**squared** size of the coefficients, and ~Lasso~ penalises their **absolute** size (which drives "
  "some coefficients to exactly zero, doing feature selection for you). Both trade a little bias for "
  "a lot less variance &mdash; the bias&ndash;variance tradeoff from Lesson 8.1, made concrete. "
  "You'll meet them again in feature engineering (Track 9)."),
 title="Deep dive: R² exactly, the four OLS assumptions, and regularization"))

p.append(B.callout("note","Interview-ready",
 "Expect: *\"explain linear regression to a non-technical stakeholder\"* &mdash; a line whose slope "
 "is the effect of one thing on another, chosen to sit as close to the data as possible. Then "
 "*\"what does least squares minimise?\"* (sum of squared residuals) and *\"what's R&sup2;?\"* "
 "(fraction of variation explained). Bonus depth: name an assumption (constant-variance residuals) "
 "and why you'd plot residuals to check it.", "&#9670;"))

LESSONS={"ml-02-linreg":"\n".join(p)}
print("content_m02 OK — chars:", len(LESSONS["ml-02-linreg"]))
