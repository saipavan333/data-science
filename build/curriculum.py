# -*- coding: utf-8 -*-
"""curriculum.py — the whole learning path, in dependency order.

Ordered so nothing is ever used before it is taught: do things (Python, SQL, tooling),
describe things (statistics, EDA), reason under uncertainty (experiments, causality),
model (ML, features, evaluation), ship (MLOps, communication), then prove it
(capstones, interview bank).
"""

TRACKS = [
    # ===================================================================== #
    {
        "num": 1, "id": "python", "title": "Foundations — Data Science & Python",
        "status": "ready",
        "desc": "Start here. What the job actually is, then Python from zero: the language, NumPy, and pandas — enough to load, clean, reshape and aggregate real data fluently.",
        "lessons": [
            {"id": "stats-01-what-is", "num": "1.1",
             "title": "What Data Science Is — and the Path Ahead",
             "lede": "The job in one picture, the workflow you'll repeat for life, and why statistics is the engine under all of it.",
             "minutes": 12, "ready": True
            },
            {"id": "py-01-setup", "num": "1.2",
             "title": "Python for Data, From Zero",
             "lede": "Assuming zero coding: variables, types, conditionals, loops, functions, and collections — each shown, run, and explained before the next builds on it.",
             "minutes": 26
            },
            {"id": "py-07-functions", "num": "1.3",
             "title": "Writing Functions & Clean Code",
             "lede": "Reusable functions, default arguments, and graceful error handling with try/except — the leap to code you can trust.",
             "minutes": 20
            },
            {"id": "py-08-strings", "num": "1.4",
             "title": "Working with Text & Strings",
             "lede": "Index, slice, and clean text — and apply string methods to a whole column at once with pandas' .str accessor.",
             "minutes": 18
            },
            {"id": "py-09-datetime", "num": "1.5",
             "title": "Dates & Times",
             "lede": "Parse dates, extract calendar parts with .dt, and do date arithmetic — without the classic timestamp bugs.",
             "minutes": 18
            },
            {"id": "py-02-numpy", "num": "1.6",
             "title": "NumPy: Thinking in Arrays",
             "lede": "Vectorized thinking — operate on whole arrays at once — that makes data code fast and short.",
             "minutes": 20
            },
            {"id": "py-10-numpy2", "num": "1.7",
             "title": "NumPy Deeper: Random, Axes & Reshaping",
             "lede": "Aggregate along axes, generate reproducible random data, and reshape and transform arrays.",
             "minutes": 20
            },
            {"id": "py-03-pandas-intro", "num": "1.8",
             "title": "Pandas: Series & DataFrames",
             "lede": "The spreadsheet-in-code you'll live in: Series, DataFrames, selecting, and filtering with boolean masks.",
             "minutes": 20
            },
            {"id": "py-11-io", "num": "1.9",
             "title": "Loading & Saving Data",
             "lede": "Read messy real-world files robustly (encodings, dtypes, dates) and save clean results.",
             "minutes": 18
            },
            {"id": "py-04-clean", "num": "1.10",
             "title": "Cleaning Messy Data",
             "lede": "Missing values, types, duplicates, and the 80% of the job nobody shows you.",
             "minutes": 22
            },
            {"id": "py-05-reshape", "num": "1.11",
             "title": "Reshaping & Aggregating",
             "lede": "groupby, pivot, melt, and joins — turning rows into answers.",
             "minutes": 22
            },
            {"id": "py-06-interview", "num": "1.12",
             "title": "Track 1 Interview Check",
             "lede": "Pandas and SQL questions teams ask, with model answers.",
             "minutes": 15
            },
            {"id": "py-12-cheatsheet", "num": "1.13",
             "title": "Python, NumPy & Pandas Cheatsheet",
             "lede": "The Foundations track on one printable page \u2014 Python, NumPy and pandas essentials.",
             "minutes": 6, "ready": True
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 2, "id": "sql", "title": "SQL for Data Analysis",
        "status": "build",
        "desc": "The query language behind almost every data job: pull, filter, group, and join data straight from a database. A core skill — you will use it on day one of the job.",
        "lessons": [
            {"id": "sql-01-select", "num": "2.1",
             "title": "SELECT: Asking a Database a Question",
             "lede": "Tables, and the five clauses of a SELECT — SELECT, FROM, WHERE, ORDER BY, LIMIT — run live against a real table in the page.",
             "minutes": 22, "ready": True
            },
            {"id": "sql-02-filter", "num": "2.2",
             "title": "Filtering & Sorting in Depth",
             "lede": "Say exactly which rows you want: AND/OR/NOT, IN, BETWEEN, LIKE, and the NULL trap.",
             "minutes": 20, "ready": False,
             "outline": [
                 "Combining conditions with AND / OR / NOT and parentheses",
                 "IN, BETWEEN, and LIKE for sets, ranges, and text patterns",
                 "NULL logic: IS NULL / IS NOT NULL and why = NULL never matches",
                 "Sorting on multiple keys, and DISTINCT",
             ]
            },
            {"id": "sql-03-aggregate", "num": "2.3",
             "title": "Aggregating with GROUP BY",
             "lede": "Turn millions of rows into one number per group: COUNT, SUM, AVG, and HAVING.",
             "minutes": 22, "ready": False,
             "outline": [
                 "The aggregate functions: COUNT, SUM, AVG, MIN, MAX",
                 "GROUP BY: one result row per group",
                 "HAVING vs WHERE (filtering groups vs rows)",
                 "The split-apply-combine parallel to pandas groupby",
             ]
            },
            {"id": "sql-04-joins", "num": "2.4",
             "title": "Joining Tables",
             "lede": "Real data lives across many tables — combine them on a key with INNER, LEFT, RIGHT, and FULL joins.",
             "minutes": 24, "ready": False,
             "outline": [
                 "Why data is split across tables (normalization)",
                 "Keys: primary and foreign",
                 "INNER vs LEFT/RIGHT/FULL, with the Venn picture",
                 "The fan-out trap and how to sanity-check row counts",
             ]
            },
            {"id": "sql-05-subqueries", "num": "2.5",
             "title": "Subqueries & CTEs",
             "lede": "Build a query in readable steps with WITH (CTEs) and nested SELECTs.",
             "minutes": 20, "ready": False,
             "outline": [
                 "Subqueries in WHERE and FROM",
                 "Common Table Expressions (WITH)",
                 "Writing top-down, readable, debuggable SQL",
                 "Correlated subqueries (intro)",
             ]
            },
            {"id": "sql-06-window", "num": "2.6",
             "title": "Window Functions",
             "lede": "The interview favorite: running totals, rankings, and row-by-row context with OVER and PARTITION BY.",
             "minutes": 24, "ready": False,
             "outline": [
                 "OVER and PARTITION BY: aggregates without collapsing rows",
                 "ROW_NUMBER, RANK, DENSE_RANK",
                 "Running totals and moving averages",
                 "LAG / LEAD for period-over-period change",
             ]
            },
            {"id": "sql-07-case-dates", "num": "2.7",
             "title": "CASE, Dates & Cleaning in SQL",
             "lede": "In-query logic and tidying: CASE WHEN, date functions, and COALESCE.",
             "minutes": 20, "ready": False,
             "outline": [
                 "CASE WHEN for buckets and conditional columns",
                 "Date/time functions and truncation",
                 "COALESCE and NULL handling",
                 "Casting types and basic string cleaning",
             ]
            },
            {"id": "sql-08-interview", "num": "2.8",
             "title": "Track 2 Interview Check",
             "lede": "The SQL screen, decoded: the recurring problem patterns with worked answers.",
             "minutes": 18, "ready": False,
             "outline": [
                 "The 'nth highest' problem",
                 "Group-and-filter with HAVING",
                 "A window-function walkthrough",
                 "Debugging a query out loud",
             ]
            },
            {"id": "sql-09-cheatsheet", "num": "2.9",
             "title": "SQL Cheatsheet & Quick Reference",
             "lede": "The whole track on one printable page \u2014 every clause, what it does, and the query shape.",
             "minutes": 6, "ready": True
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 3, "id": "toolkit", "title": "The Data Scientist's Toolkit",
        "status": "soon",
        "desc": "The professional habits that make your work trustworthy and reproducible: the command line, Git, environments, and project structure.",
        "lessons": [
            {"id": "tool-01-cli", "num": "3.1",
             "title": "The Command Line, Without Fear",
             "lede": "Navigate, move files, and run programs from the terminal — the interface every data tool assumes you know.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Why the terminal, and a mental model of the shell",
                 "Navigating and manipulating files (cd, ls, cp, mv, rm)",
                 "Running scripts, pipes, and redirection",
                 "A survival cheat-sheet",
             ]
            },
            {"id": "tool-02-git", "num": "3.2",
             "title": "Version Control with Git & GitHub",
             "lede": "Track every change, never lose work, and collaborate — the non-negotiable professional skill.",
             "minutes": 24, "ready": False,
             "outline": [
                 "Why version control (and what a commit really is)",
                 "The core loop: add, commit, push, pull",
                 "Branches and merges",
                 "GitHub, pull requests, and a portfolio that recruiters read",
             ]
            },
            {"id": "tool-03-envs", "num": "3.3",
             "title": "Virtual Environments & Dependencies",
             "lede": "Make your code run the same on any machine — the cure for 'works on mine'.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Why isolated environments",
                 "venv / conda basics",
                 "requirements.txt and pinning versions",
                 "Reproducible setups",
             ]
            },
            {"id": "tool-04-notebooks", "num": "3.4",
             "title": "Notebooks vs Scripts & Project Structure",
             "lede": "When to explore in a notebook, when to write a script, and how to lay a project out.",
             "minutes": 16, "ready": False,
             "outline": [
                 "Strengths and traps of notebooks",
                 "Refactoring a notebook into modules",
                 "A sane project layout",
                 "Config, data, and secrets",
             ]
            },
            {"id": "tool-05-repro", "num": "3.5",
             "title": "Reproducibility & Reading Docs",
             "lede": "Seeds, deterministic pipelines, and the underrated skill of reading documentation.",
             "minutes": 16, "ready": False,
             "outline": [
                 "Random seeds and deterministic runs",
                 "Logging over print",
                 "How to read official docs fast",
                 "Asking answerable questions",
             ]
            },
            {"id": "tool-06-interview", "num": "3.6",
             "title": "Track 3 Interview Check",
             "lede": "The workflow and collaboration questions behind the technical ones.",
             "minutes": 12, "ready": False,
             "outline": [
                 "'Walk me through your Git workflow'",
                 "'How do you make analysis reproducible?'",
             ]
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 4, "id": "stats", "title": "Statistics & Probability",
        "status": "ready",
        "desc": "The ideas behind every method: data, uncertainty, distributions, sampling, estimation, and testing. Start here.",
        "lessons": [
            {"id": "stats-02-data-types", "num": "4.1",
             "title": "Types of Data & Variables",
             "lede": "Before you analyze anything you must know what kind of thing you're looking at. Get this wrong and every later step breaks.",
             "minutes": 14, "ready": True
            },
            {"id": "stats-03-summary", "num": "4.2",
             "title": "Describing Data: Center & Spread",
             "lede": "Mean, median, variance, percentiles — the handful of numbers that summarize a column, and exactly when each one lies to you.",
             "minutes": 18, "ready": True
            },
            {"id": "stats-04-probability", "num": "4.3",
             "title": "Probability: The Language of Uncertainty",
             "lede": "Events, conditional probability, independence, and Bayes — the grammar you need to reason about chance without fooling yourself.",
             "minutes": 20, "ready": True
            },
            {"id": "stats-05-distributions", "num": "4.4",
             "title": "Distributions: Normal, Binomial & Friends",
             "lede": "A distribution is a shape that tells you which values are likely. Learn the four you'll meet constantly and how to recognize each.",
             "minutes": 20, "ready": True
            },
            {"id": "stats-06-sampling", "num": "4.5",
             "title": "Populations, Samples & Sampling Variability",
             "lede": "Why a sample is never the whole truth, and how to measure how much it wobbles from sample to sample.",
             "minutes": 16, "ready": False,
             "outline": [
                 "Population vs. sample vs. statistic vs. parameter",
                 "Random sampling and why it matters; sources of bias",
                 "The sampling distribution of the mean",
                 "Standard error: the spread of a statistic, derived and simulated",
                 "Worked example: estimating average order value from a sample",
             ]
            },
            {"id": "stats-07-clt", "num": "4.6",
             "title": "The Central Limit Theorem",
             "lede": "The single idea that lets us put error bars on almost anything.",
             "minutes": 16, "ready": False,
             "outline": [
                 "What the CLT actually claims (and what it doesn't)",
                 "Simulation: sums of dice, exponential waits, skewed incomes → normal",
                 "Why n≈30 is a rule of thumb, not a law",
                 "How the CLT powers confidence intervals and tests",
             ]
            },
            {"id": "stats-08-estimation-ci", "num": "4.7",
             "title": "Estimation & Confidence Intervals",
             "lede": "Turning a single sample into an honest range, and saying out loud what that range does and does not mean.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Point estimates and their standard error",
                 "Building a confidence interval from the CLT",
                 "The correct interpretation (and the tempting wrong one)",
                 "Bootstrap confidence intervals with code",
                 "Reporting estimates to a stakeholder",
             ]
            },
            {"id": "stats-09-hypothesis", "num": "4.8",
             "title": "Hypothesis Testing: The Logic",
             "lede": "Null and alternative, test statistic, p-value, and the two ways you can be wrong — the reasoning, not the recipe.",
             "minutes": 20, "ready": False,
             "outline": [
                 "The courtroom analogy: assume innocence (the null)",
                 "Test statistic and the null distribution",
                 "p-values: the precise definition, said three ways",
                 "Type I and Type II errors; significance and power",
                 "Why 'fail to reject' is not 'prove the null'",
             ]
            },
            {"id": "stats-10-tests", "num": "4.9",
             "title": "Choosing the Right Test",
             "lede": "A decision tree from your data to the correct test, with runnable examples for the tests you'll actually use.",
             "minutes": 22, "ready": False,
             "outline": [
                 "One-sample, two-sample, and paired t-tests",
                 "Chi-square for categorical associations",
                 "Nonparametric alternatives (Mann–Whitney, Wilcoxon)",
                 "A which-test-when decision tree",
                 "Assumptions, and what to do when they fail",
             ]
            },
            {"id": "stats-11-correlation", "num": "4.10",
             "title": "Correlation — and Its Traps",
             "lede": "Pearson vs. Spearman, what r does and doesn't capture, and the famous datasets that prove a single number can deceive.",
             "minutes": 16, "ready": False,
             "outline": [
                 "Covariance → correlation, intuitively and in code",
                 "Pearson vs. Spearman: linear vs. monotonic",
                 "Anscombe's quartet and the Datasaurus: always plot first",
                 "Correlation is not causation (a bridge to Track 8)",
             ]
            },
            {"id": "stats-12-interview", "num": "4.11",
             "title": "Track 4 Interview Check",
             "lede": "The statistics questions data-science teams actually ask, with model answers you can say out loud.",
             "minutes": 15, "ready": False,
             "outline": [
                 "Explain a p-value to a non-technical stakeholder",
                 "What is the difference between standard deviation and standard error?",
                 "When would you use median over mean?",
                 "Walk through the CLT and why it matters",
                 "Interpreting a confidence interval correctly",
             ]
            },
            {"id": "stats-13-cheatsheet", "num": "4.12",
             "title": "Statistics & Probability Cheatsheet",
             "lede": "Every statistical idea in the track on one printable page.",
             "minutes": 6, "ready": True
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 5, "id": "eda", "title": "EDA & Visualization",
        "status": "ready",
        "desc": "Explore data systematically and tell the truth with charts.",
        "lessons": [
            {"id": "eda-01-mindset", "num": "5.1",
             "title": "The EDA Mindset",
             "lede": "A repeatable first-hour routine for meeting any new dataset.",
             "minutes": 16
            },
            {"id": "eda-06-toolkit", "num": "5.2",
             "title": "The Plotting Toolkit: Matplotlib & Seaborn",
             "lede": "How to actually make charts: the figure/axes model, and seaborn's one-line statistical plots.",
             "minutes": 18
            },
            {"id": "eda-02-charts", "num": "5.3",
             "title": "Choosing the Right Chart",
             "lede": "A decision from your question to the chart that answers it — and why bars beat pies.",
             "minutes": 18
            },
            {"id": "eda-07-distributions", "num": "5.4",
             "title": "Reading Distributions & Transformations",
             "lede": "Recognize distribution shapes on sight, check normality with QQ plots, and tame skew with transforms.",
             "minutes": 20
            },
            {"id": "eda-08-categorical", "num": "5.5",
             "title": "Exploring Categorical Data",
             "lede": "Counts, proportions, grouped vs stacked bars, and crosstabs that reveal how categories relate.",
             "minutes": 18
            },
            {"id": "eda-09-timeseries", "num": "5.6",
             "title": "Time-Series EDA",
             "lede": "Separate trend from seasonality and noise, smooth with rolling means, and never shuffle time.",
             "minutes": 20
            },
            {"id": "eda-10-outliers", "num": "5.7",
             "title": "Outliers & Anomalies",
             "lede": "Detect extremes (IQR, z-score), then decide: an error to fix, or the signal you're hunting?",
             "minutes": 18
            },
            {"id": "eda-03-truth", "num": "5.8",
             "title": "Telling the Truth With Charts",
             "lede": "Truncated axes, cherry-picked ranges, and the other ways charts mislead — and how to stay honest.",
             "minutes": 18
            },
            {"id": "eda-04-multivariate", "num": "5.9",
             "title": "Seeing Many Variables at Once",
             "lede": "Faceting, correlation heatmaps, and pair plots to read several variables together.",
             "minutes": 18
            },
            {"id": "eda-05-interview", "num": "5.10",
             "title": "Track 5 Interview Check",
             "lede": "The 'explore this dataset' and 'critique this chart' questions teams ask, with model answers.",
             "minutes": 15
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 6, "id": "ab", "title": "Experimentation & A/B Testing",
        "status": "soon",
        "desc": "Design experiments, compute power, run tests right, and avoid the classic traps.",
        "lessons": [
            {"id": "ab-01-why", "num": "6.1",
             "title": "Why Experiment? Causation You Can Trust",
             "lede": "Randomization is the closest thing to a truth machine we have.",
             "minutes": 16, "ready": False,
             "outline": [
                 "Correlation vs. causation recap",
                 "Randomization and counterfactuals",
                 "When you can and can't experiment",
             ]
            },
            {"id": "ab-02-design", "num": "6.2",
             "title": "Designing an A/B Test",
             "lede": "Metric, hypothesis, unit of randomization, and guardrails.",
             "minutes": 20, "ready": False,
             "outline": [
                 "Choosing a primary metric",
                 "Randomization unit",
                 "Guardrail metrics",
                 "Sample ratio mismatch",
             ]
            },
            {"id": "ab-03-power", "num": "6.3",
             "title": "Power & Sample Size",
             "lede": "How many users you need before you start — done right.",
             "minutes": 20, "ready": False,
             "outline": [
                 "Effect size, alpha, power",
                 "The sample-size formula",
                 "Minimum detectable effect",
                 "Duration and peeking",
             ]
            },
            {"id": "ab-04-analyze", "num": "6.4",
             "title": "Analyzing & Interpreting Results",
             "lede": "p-values done right, confidence intervals, and decisions.",
             "minutes": 20, "ready": False,
             "outline": [
                 "The test and the CI",
                 "Practical vs. statistical significance",
                 "Multiple testing",
                 "Novelty and primacy effects",
             ]
            },
            {"id": "ab-05-pitfalls", "num": "6.5",
             "title": "The Pitfalls Catalog",
             "lede": "Peeking, p-hacking, Simpson's paradox, and twyman's law.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Peeking and sequential testing",
                 "Multiple comparisons",
                 "Simpson's paradox",
                 "Trustworthiness checks",
             ]
            },
            {"id": "ab-06-interview", "num": "6.6",
             "title": "Track 6 Interview Check",
             "lede": "The product-sense + experimentation case bank.",
             "minutes": 15, "ready": False,
             "outline": [
                 "'Design an experiment for feature X'",
                 "'The test is flat — what now?'",
             ]
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 7, "id": "causal", "title": "Causal Inference",
        "status": "soon",
        "desc": "Correlation vs. causation, confounders, and the methods that get you closer to 'because'.",
        "lessons": [
            {"id": "causal-01-why", "num": "7.1",
             "title": "Correlation vs. Causation",
             "lede": "Why the most important question is the hardest.",
             "minutes": 18, "ready": False,
             "outline": [
                 "The counterfactual",
                 "Confounding, defined",
                 "Spurious correlations",
             ]
            },
            {"id": "causal-02-dags", "num": "7.2",
             "title": "Causal Diagrams (DAGs)",
             "lede": "Drawing your assumptions so you can reason about them.",
             "minutes": 20, "ready": False,
             "outline": [
                 "Nodes, edges, paths",
                 "Confounders, mediators, colliders",
                 "What to control for",
             ]
            },
            {"id": "causal-03-methods", "num": "7.3",
             "title": "Basic Causal Methods",
             "lede": "Matching, regression adjustment, diff-in-diff.",
             "minutes": 22, "ready": False,
             "outline": [
                 "Adjustment and matching",
                 "Propensity scores",
                 "Difference-in-differences",
                 "Instrumental variables (intro)",
             ]
            },
            {"id": "causal-04-interview", "num": "7.4",
             "title": "Track 7 Interview Check",
             "lede": "Causal reasoning case questions.",
             "minutes": 12, "ready": False,
             "outline": [
                 "Spotting a confounder",
                 "'We can't run an A/B test — now what?'",
             ]
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 8, "id": "ml", "title": "Classical Machine Learning",
        "status": "build",
        "desc": "Regression, classification, trees & ensembles, clustering, and how to pick and validate a model.",
        "lessons": [
            {"id": "ml-01-what", "num": "8.1",
             "title": "What Machine Learning Really Is",
             "lede": "Supervised vs. unsupervised, features and targets, fit vs. generalize.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Learning from data, defined",
                 "Supervised / unsupervised",
                 "Train/validation/test",
                 "The bias–variance idea",
             ]
            },
            {"id": "ml-02-linreg", "num": "8.2",
             "title": "Linear Regression From Scratch",
             "lede": "The workhorse, fully understood: fit, residuals, assumptions.",
             "minutes": 22, "ready": False,
             "outline": [
                 "Line of best fit and least squares",
                 "Interpreting coefficients",
                 "Residual diagnostics",
                 "Regularization preview",
             ]
            },
            {"id": "ml-03-logreg", "num": "8.3",
             "title": "Classification & Logistic Regression",
             "lede": "Predicting categories and probabilities.",
             "minutes": 20, "ready": False,
             "outline": [
                 "From regression to probability",
                 "The sigmoid and odds",
                 "Decision thresholds",
                 "Worked churn example",
             ]
            },
            {"id": "ml-04-trees", "num": "8.4",
             "title": "Decision Trees & Random Forests",
             "lede": "Flexible models that need no scaling — and how ensembles tame them.",
             "minutes": 22, "ready": False,
             "outline": [
                 "How a tree splits",
                 "Overfitting and pruning",
                 "Bagging and random forests",
                 "Feature importance",
             ]
            },
            {"id": "ml-05-boosting", "num": "8.5",
             "title": "Gradient Boosting",
             "lede": "The model that wins most tabular problems.",
             "minutes": 20, "ready": False,
             "outline": [
                 "Boosting intuition",
                 "XGBoost/LightGBM in practice",
                 "Key hyperparameters",
             ]
            },
            {"id": "ml-06-clustering", "num": "8.6",
             "title": "Clustering & Unsupervised Learning",
             "lede": "Finding structure when there's no label.",
             "minutes": 18, "ready": False,
             "outline": [
                 "k-means",
                 "Choosing k",
                 "Hierarchical clustering",
                 "Pitfalls",
             ]
            },
            {"id": "ml-07-selection", "num": "8.7",
             "title": "Model Selection & Cross-Validation",
             "lede": "Choosing a model without fooling yourself.",
             "minutes": 20, "ready": False,
             "outline": [
                 "k-fold cross-validation",
                 "Hyperparameter search",
                 "Leakage",
                 "The model-zoo decision tree",
             ]
            },
            {"id": "ml-08-interview", "num": "8.8",
             "title": "Track 8 Interview Check",
             "lede": "Core ML questions and case prompts.",
             "minutes": 15, "ready": False,
             "outline": [
                 "Bias–variance tradeoff",
                 "When trees over linear?",
                 "Explain cross-validation",
             ]
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 9, "id": "fe", "title": "Feature Engineering",
        "status": "soon",
        "desc": "Build, encode, and select the features that actually move a model.",
        "lessons": [
            {"id": "fe-01-what", "num": "9.1",
             "title": "What Makes a Good Feature",
             "lede": "Signal, leakage, and the art of representation.",
             "minutes": 16, "ready": False,
             "outline": [
                 "Features as representations",
                 "Leakage, the cardinal sin",
                 "Signal vs. noise",
             ]
            },
            {"id": "fe-02-numeric", "num": "9.2",
             "title": "Numeric Transforms",
             "lede": "Scaling, binning, logs, and interactions.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Standardize vs. normalize",
                 "Log and power transforms",
                 "Binning",
                 "Interactions",
             ]
            },
            {"id": "fe-03-categorical", "num": "9.3",
             "title": "Encoding Categories",
             "lede": "One-hot, target, and the high-cardinality problem.",
             "minutes": 18, "ready": False,
             "outline": [
                 "One-hot and ordinal",
                 "Target/mean encoding (and leakage)",
                 "Hashing",
             ]
            },
            {"id": "fe-04-datetime-text", "num": "9.4",
             "title": "Dates, Text & Aggregates",
             "lede": "Squeezing features from timestamps, strings, and groups.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Datetime parts and cycles",
                 "Text → numbers (TF-IDF)",
                 "Group aggregate features",
                 "Lag features for time series",
             ]
            },
            {"id": "fe-05-selection", "num": "9.5",
             "title": "Feature Selection",
             "lede": "Fewer, better features: filter, wrapper, embedded.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Why fewer can be better",
                 "Filter/wrapper/embedded methods",
                 "Stability",
             ]
            },
            {"id": "fe-06-interview", "num": "9.6",
             "title": "Track 9 Interview Check",
             "lede": "Feature-engineering case questions.",
             "minutes": 12, "ready": False,
             "outline": [
                 "Spotting leakage in a scenario",
                 "Encoding a high-cardinality column",
             ]
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 10, "id": "eval", "title": "Model Evaluation & Interpretation",
        "status": "soon",
        "desc": "Metrics, validation, calibration, and explaining a model honestly.",
        "lessons": [
            {"id": "eval-01-metrics", "num": "10.1",
             "title": "Picking the Right Metric",
             "lede": "Why accuracy lies, and what to use instead.",
             "minutes": 20, "ready": False,
             "outline": [
                 "Confusion matrix",
                 "Precision, recall, F1",
                 "ROC-AUC vs. PR-AUC",
                 "Regression metrics",
                 "A metric decision tree",
             ]
            },
            {"id": "eval-02-validation", "num": "10.2",
             "title": "Validation Done Right",
             "lede": "Splits that don't lie — including time and groups.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Train/val/test discipline",
                 "Cross-validation variants",
                 "Temporal and group splits",
             ]
            },
            {"id": "eval-03-calibration", "num": "10.3",
             "title": "Calibration & Thresholds",
             "lede": "When a 0.7 should mean 70%.",
             "minutes": 16, "ready": False,
             "outline": [
                 "Reliability diagrams",
                 "Platt/isotonic",
                 "Choosing a threshold for a decision",
             ]
            },
            {"id": "eval-04-interpret", "num": "10.4",
             "title": "Explainability",
             "lede": "Feature importance, partial dependence, and SHAP — used carefully.",
             "minutes": 20, "ready": False,
             "outline": [
                 "Global vs. local explanations",
                 "Permutation importance",
                 "Partial dependence",
                 "SHAP intuition",
             ]
            },
            {"id": "eval-05-interview", "num": "10.5",
             "title": "Track 10 Interview Check",
             "lede": "Evaluation and interpretation questions.",
             "minutes": 12, "ready": False,
             "outline": [
                 "'Model is 99% accurate — are you happy?'",
                 "Explaining a model to a PM",
             ]
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 11, "id": "mlops", "title": "Putting Models to Work",
        "status": "soon",
        "desc": "The last mile that turns a trained model into something that actually runs, serves predictions, and keeps working — an intro to deployment and MLOps.",
        "lessons": [
            {"id": "mlops-01-pipeline", "num": "11.1",
             "title": "From Notebook to Pipeline",
             "lede": "Package the messy notebook steps into one repeatable train-and-predict pipeline.",
             "minutes": 20, "ready": False,
             "outline": [
                 "The train/predict split in code",
                 "scikit-learn Pipelines",
                 "Avoiding train/serve skew",
                 "Saving the whole pipeline, not just the model",
             ]
            },
            {"id": "mlops-02-serialize", "num": "11.2",
             "title": "Saving, Loading & Versioning a Model",
             "lede": "Persist a trained model safely and know which version is in production.",
             "minutes": 16, "ready": False,
             "outline": [
                 "Serialization (joblib/pickle) and its pitfalls",
                 "Versioning models and data",
                 "Model cards and metadata",
             ]
            },
            {"id": "mlops-03-serve", "num": "11.3",
             "title": "A Simple Prediction API",
             "lede": "Wrap a model in a tiny web service so other systems can ask it for predictions.",
             "minutes": 22, "ready": False,
             "outline": [
                 "Request → features → prediction → response",
                 "A minimal FastAPI service",
                 "Batch vs real-time",
                 "Latency and testing",
             ]
            },
            {"id": "mlops-04-monitor", "num": "11.4",
             "title": "Monitoring & Drift",
             "lede": "Models rot quietly — watch inputs and performance so you catch it.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Data drift vs concept drift",
                 "What to log and alert on",
                 "Retraining triggers",
                 "Feedback loops",
             ]
            },
            {"id": "mlops-05-interview", "num": "11.5",
             "title": "Track 11 Interview Check",
             "lede": "The 'how would you deploy this?' questions, answered simply.",
             "minutes": 12, "ready": False,
             "outline": [
                 "'How would you put this model in production?'",
                 "'How do you know it still works?'",
             ]
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 12, "id": "comm", "title": "Communication & Storytelling",
        "status": "soon",
        "desc": "Turn analysis into a decision a stakeholder will actually act on.",
        "lessons": [
            {"id": "comm-01-audience", "num": "12.1",
             "title": "Start From the Decision",
             "lede": "Who decides what, and what would change their mind.",
             "minutes": 14, "ready": False,
             "outline": [
                 "The decision-first framing",
                 "Audience and altitude",
                 "BLUF: bottom line up front",
             ]
            },
            {"id": "comm-02-narrative", "num": "12.2",
             "title": "Structuring the Story",
             "lede": "Situation, complication, question, answer.",
             "minutes": 16, "ready": False,
             "outline": [
                 "The SCQA pattern",
                 "One chart, one message",
                 "Headline as takeaway",
             ]
            },
            {"id": "comm-03-deck", "num": "12.3",
             "title": "The Stakeholder-Ready Deck",
             "lede": "From notebook to a deck an exec acts on.",
             "minutes": 18, "ready": False,
             "outline": [
                 "Executive summary",
                 "Show the evidence, hide the plumbing",
                 "Recommendation and risks",
                 "Anticipating questions",
             ]
            },
            {"id": "comm-04-interview", "num": "12.4",
             "title": "Track 12 Interview Check",
             "lede": "Communication and behavioral prompts.",
             "minutes": 12, "ready": False,
             "outline": [
                 "'Explain your hardest project'",
                 "Tailoring to a non-technical audience",
             ]
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 13, "id": "capstone", "title": "Capstones",
        "status": "build",
        "desc": "End-to-end analyses that actually run — your portfolio proof.",
        "lessons": [
            {"id": "cap-01-eda", "num": "13.1",
             "title": "Capstone A — EDA & Insight Report",
             "lede": "A complete exploratory analysis of a realistic e-commerce dataset, ending in a stakeholder-ready insight. Runs end to end.",
             "minutes": 30, "ready": True
            },
            {"id": "cap-02-abtest", "num": "13.2",
             "title": "Capstone B — Rigorous A/B-Test Analysis",
             "lede": "Design, power, analysis, and a go/no-go recommendation.",
             "minutes": 30, "ready": False,
             "outline": [
                 "The experiment and data",
                 "Sanity checks (SRM)",
                 "Effect size and CI",
                 "Recommendation memo",
             ]
            },
            {"id": "cap-03-model", "num": "13.3",
             "title": "Capstone C — Predictive Model, Honestly Evaluated",
             "lede": "A churn model with leakage checks, honest metrics, and interpretation.",
             "minutes": 30, "ready": False,
             "outline": [
                 "Framing and target",
                 "Validation design",
                 "Model and metrics",
                 "Interpretation and caveats",
             ]
            },
            {"id": "cap-04-present", "num": "13.4",
             "title": "Capstone D — The Stakeholder Presentation",
             "lede": "Turn one capstone into a deck that drives a decision.",
             "minutes": 20, "ready": False,
             "outline": [
                 "From analysis to narrative",
                 "Building the deck",
                 "The ask",
             ]
            },
        ],
    },
    # ===================================================================== #
    {
        "num": 14, "id": "interview", "title": "Interview Bank",
        "status": "soon",
        "desc": "What data-science teams actually ask in 2026 — SQL, statistics, ML, case studies, and product sense, with model answers.",
        "lessons": [
            {"id": "iv-01-overview", "num": "14.1",
             "title": "How DS Interviews Work in 2026",
             "lede": "The five rounds and what each is really testing.",
             "minutes": 14, "ready": False,
             "outline": [
                 "The modern loop",
                 "What each round signals",
                 "How to prepare efficiently",
             ]
            },
            {"id": "iv-02-sql", "num": "14.2",
             "title": "SQL Question Bank",
             "lede": "Joins, windows, and the patterns that recur.",
             "minutes": 22, "ready": False,
             "outline": [
                 "Aggregations and joins",
                 "Window functions",
                 "Date logic",
                 "10 worked problems",
             ]
            },
            {"id": "iv-03-stats", "num": "14.3",
             "title": "Statistics & Probability Bank",
             "lede": "The concept questions, answered crisply.",
             "minutes": 20, "ready": False,
             "outline": [
                 "p-values, power, CIs",
                 "Distributions and the CLT",
                 "Brain-teasers done calmly",
             ]
            },
            {"id": "iv-04-ml", "num": "14.4",
             "title": "Machine Learning Bank",
             "lede": "From bias–variance to deployment.",
             "minutes": 20, "ready": False,
             "outline": [
                 "Modeling tradeoffs",
                 "Metrics and validation",
                 "Debugging a bad model",
             ]
            },
            {"id": "iv-05-case", "num": "14.5",
             "title": "Case Studies & Product Sense",
             "lede": "Open-ended business problems, structured.",
             "minutes": 22, "ready": False,
             "outline": [
                 "A framework for cases",
                 "Metric definition",
                 "Diagnosing a metric drop",
                 "Designing an experiment",
             ]
            },
            {"id": "iv-06-behavioral", "num": "14.6",
             "title": "Behavioral & Closing",
             "lede": "Stories that land, questions to ask.",
             "minutes": 12, "ready": False,
             "outline": [
                 "STAR stories",
                 "Conflict and ambiguity",
                 "Questions for your interviewer",
             ]
            },
        ],
    },
]
