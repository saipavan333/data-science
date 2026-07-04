# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Sales by day, signups by week, server load by minute &mdash; an enormous share of real data is "
 "indexed by **time**, and it needs its own EDA. The goal is to pull apart what's a lasting "
 "~trend~, what's a repeating ~seasonal~ pattern, and what's just noise &mdash; and to do it "
 "without committing the cardinal sin of time data: shuffling away the order that gives it "
 "meaning."))

p.append(B.h2("The three components of a time series", kicker="Concept"))
p.append(B.concept(
 "A time series is usefully thought of as three layers added (or multiplied) together:\n\n"
 "- ~Trend~ &mdash; the long-run direction (slowly growing user base).\n"
 "- ~Seasonality~ &mdash; a pattern that repeats on a fixed period (higher sales every December, "
 "every weekend, every morning).\n"
 "- ~Residual~ (noise) &mdash; the irregular leftover once trend and seasonality are removed.\n\n"
 "Separating them &mdash; ~decomposition~ &mdash; turns a confusing squiggle into three readable "
 "stories, so you can answer 'are we *really* growing?' (trend) separately from 'is this just the "
 "usual December bump?' (seasonality)."))
p.append(B.figure(IMG+"s_eda_ts_components.png",
 "**Decomposition.** The messy *observed* series (top) is the sum of a smooth *trend*, a "
 "repeating *seasonal* wave, and random *residual* noise. Reading them apart is the heart of "
 "time-series EDA.",
 "A time series decomposed into observed, trend, seasonality, and residual panels."))

p.append(B.h2("Smoothing with rolling averages", kicker="Concept"))
p.append(B.concept(
 "Raw time series are jagged, and the noise hides the trend. A ~rolling average~ (moving average) "
 "smooths it: each point is replaced by the average of a **window** of nearby points "
 "(`series.rolling(7).mean()` for a 7-day window). A short window stays responsive but jumpy; a "
 "long window is smooth but lags. Choosing the window to match the seasonality (e.g., 7 days to "
 "smooth a weekly cycle) reveals the underlying trend."))
p.append(B.figure(IMG+"s_eda_rolling.png",
 "**Rolling averages reveal the trend.** The raw daily series (grey) is too noisy to read; the "
 "7-day mean follows the wiggles, and the 30-day mean exposes the steady climb underneath.",
 "A noisy daily series with 7-day and 30-day rolling means overlaid."))

p.append(B.h2("Resampling: changing the time grain", kicker="Concept"))
p.append(B.concept(
 "Often the raw grain is too fine. ~Resampling~ rolls a series up to a coarser period &mdash; "
 "daily to monthly, minutes to hours &mdash; aggregating as you go: `series.resample('ME').sum()` "
 "gives monthly totals. It's `groupby` for time, and it's how you turn a noisy event log into the "
 "clean monthly-revenue chart a stakeholder actually wants."))

p.append(B.h2("Resample and smooth in code", kicker="Worked example"))
p.append(B.concept(
 "Build a daily series with a trend and a monthly cycle, roll it up to monthly totals, and take a "
 "rolling mean &mdash; the two most common time-series EDA moves."))
_c,_o=_run(r'''
import pandas as pd, numpy as np
rng = np.random.default_rng(2)

days = pd.date_range("2025-01-01", periods=120, freq="D")
sales = pd.Series(
    50 + 0.3*np.arange(120)                      # upward trend
    + 10*np.sin(2*np.pi*np.arange(120)/30)       # ~monthly seasonal wave
    + rng.normal(0, 5, 120),                     # noise
    index=days)

# Resample daily -> monthly totals (groupby for time):
print("monthly totals:")
print(sales.resample("ME").sum().round(0).to_string())

# 7-day rolling mean smooths the noise (showing the last few days):
print("\n7-day rolling mean (last 4 days):")
print(sales.rolling(7).mean().tail(4).round(1).to_string())
''')
p.append(B.code_example(_c,_o,filename="timeseries.py"))
p.append(B.warn(
 "The cardinal rule of time data: **never shuffle it, and never let the future leak into the "
 "past.** When you later build models (Track 4/7), you must split train/test by **time** (train "
 "on earlier data, test on later) &mdash; a random split lets the model 'see the future,' giving "
 "fantastically optimistic results that collapse in production. Respecting time order starts in "
 "EDA.", "&#9650;"))

p.append(B.keypoints([
 "A time series = ~trend~ (long-run direction) + ~seasonality~ (fixed repeating pattern) + "
 "~residual~ (noise).",
 "~Decomposition~ separates the three so you can judge real growth apart from seasonal cycles.",
 "A ~rolling average~ (`.rolling(w).mean()`) smooths noise to reveal the trend; match the window "
 "to the cycle.",
 "~Resampling~ (`.resample('ME').sum()`) is groupby for time &mdash; roll a fine grain up to a "
 "coarser one.",
 "**Never shuffle time data**; split by time to avoid leaking the future into the past.",
]))

p.append(B.quiz([
 {"q":"Sales spike every December and you want to know whether **underlying** demand is actually "
      "growing year over year. What helps most?",
  "options":[
   {"t":"Decompose the series (or compare the trend component) to separate growth from the "
        "seasonal December spike","correct":True,
    "why":"Correct. Decomposition isolates the trend from seasonality, so you can see real "
          "year-over-year growth without the recurring December bump confusing you."},
   {"t":"Look only at December each year",
    "why":"That conflates seasonal peak with trend and ignores the rest of the year. Decomposing "
          "(or a rolling annual view) separates trend from seasonality properly."},
   {"t":"Take the overall average of all days",
    "why":"A single average hides both trend and seasonality. You need to separate the components, "
          "not collapse them."},
   {"t":"Shuffle the dates and re-plot",
    "why":"Shuffling destroys the time order that trend and seasonality live in &mdash; the one "
          "thing you must never do with time data."}]},
 {"q":"You apply a 7-day rolling mean to daily data with a strong weekly cycle. What's the main "
      "effect?",
  "options":[
   {"t":"It averages out the weekly ups and downs, exposing the slower underlying trend","correct":True,
    "why":"Correct. A window equal to the cycle length (7 days) cancels the weekly pattern, "
          "leaving the smoother trend visible."},
   {"t":"It makes the data more jagged",
    "why":"Rolling means *smooth* data, reducing jaggedness, not increasing it."},
   {"t":"It deletes a week of data permanently",
    "why":"It doesn't delete data; the first few points are just undefined until the window fills. "
          "The series length is preserved."},
   {"t":"It removes the long-term trend",
    "why":"A rolling mean preserves the trend while smoothing short-term noise/seasonality; it "
          "doesn't remove the trend."}]},
 {"q":"Why must you split a time series by time (not randomly) when building a predictive model?",
  "options":[
   {"t":"A random split lets the model train on future points and 'see' information it wouldn't "
        "have in production — data leakage","correct":True,
    "why":"Correct. Randomly mixing past and future leaks future information into training, "
          "yielding over-optimistic scores that fail in real use. Train on earlier data, test on "
          "later."},
   {"t":"Random splits are fine for time series",
    "why":"They are specifically *not* fine: they leak the future into the past. Time series "
          "require chronological splits."},
   {"t":"Because time series can't be modeled at all",
    "why":"They can be modeled; you just must respect time order in validation (a time-based "
          "split)."},
   {"t":"To make the dataset larger",
    "why":"Splitting doesn't change dataset size. The reason is avoiding future-to-past leakage."}]},
]))

p.append(B.practice([
 {"q":"Write the pandas to turn a daily-indexed Series `s` into **weekly** averages.",
  "sol":"`s.resample(\"W\").mean()`. `resample(\"W\")` groups the daily points into weekly buckets "
        "and `.mean()` aggregates each week (use `.sum()` for weekly totals instead). The Series "
        "must have a datetime index for resampling to work."},
 {"q":"A colleague trains a sales-forecasting model, splits the data randomly into train/test, and "
      "reports 98% accuracy. Why are you skeptical?",
  "sol":"A **random split on time-series data leaks the future into the training set** &mdash; the "
        "model learns from days that come *after* some test days, effectively peeking at the "
        "future, so the 98% is wildly optimistic and won't hold in production. The fix is a "
        "**time-based split**: train on the earlier period, validate/test on the later period "
        "(and respect any seasonality). I'd re-evaluate with that honest setup."},
]))

p.append(B.deepdive(
 B.concept(
  "**Additive vs. multiplicative.** Decomposition can be ~additive~ (observed = trend + seasonal "
  "+ residual) when the seasonal swing is a roughly constant size, or ~multiplicative~ (observed "
  "= trend &times; seasonal &times; residual) when the swing **grows with the level** (holiday "
  "spikes that get bigger as the business grows). A telltale sign of the multiplicative case is a "
  "seasonal pattern that fans out over time &mdash; and a **log transform** (Lesson 3.4) converts "
  "it back to additive, which is one more reason logs are so useful.") +
 B.concept(
  "**Autocorrelation.** Time-series values are usually correlated with their own recent past "
  "&mdash; today looks like yesterday. ~Autocorrelation~ measures this at different lags, and the "
  "~ACF plot~ reveals both the strength of that memory and the seasonal period (a spike at lag 7 "
  "screams 'weekly cycle'). It's the time-series analog of the correlation heatmap, and the "
  "foundation of forecasting models like ARIMA.") +
 B.concept(
  "**Stationarity.** Many classical forecasting methods assume the series is ~stationary~ &mdash; "
  "its statistical properties (mean, variance) don't drift over time. Real series with trends and "
  "growing seasonality aren't stationary, so you make them so by **differencing** (modeling the "
  "change from one step to the next) and/or log-transforming. You don't need the machinery yet, "
  "but knowing the vocabulary &mdash; trend, seasonality, autocorrelation, stationarity &mdash; "
  "prepares you for forecasting work."),
 title="Deep dive: additive vs. multiplicative, autocorrelation, and stationarity"))

p.append(B.callout("note","Interview-ready",
 "Two things land well. First, decompose: 'I'd separate trend from seasonality before claiming "
 "growth.' Second, the leakage point: 'For time-series models I split by time, never randomly, to "
 "avoid leaking the future.' That single sentence about time-based validation signals real "
 "experience and is a very common interview check.", "&#9670;"))

LESSONS={"eda-09-timeseries":"\n".join(p)}
