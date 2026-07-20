# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
p=[]

p.append(B.why(
 "A result you can't **reproduce** is a rumour, not a finding. If you rerun your analysis next month "
 "&mdash; or a colleague reruns it on their machine &mdash; and the numbers change, no one can trust "
 "any of it. Reproducibility is what turns *\"I got 0.83 once\"* into *\"anyone can get 0.83.\"* It "
 "rests on pinning **four things**: the **code**, the **data**, the **environment**, and the "
 "**randomness**. Miss any one and the result can quietly drift."))

p.append(B.h2("The four pillars", kicker="What must be pinned"))
p.append(B.concept(
 "Every reproducible analysis controls four sources of variation:\n\n"
 "- **Code** &mdash; versioned in Git, so you know *exactly* which code produced a number "
 "(lesson 3.2).\n"
 "- **Environment** &mdash; pinned packages via `requirements.txt`/lockfile, so the libraries behave "
 "identically (lesson 3.3).\n"
 "- **Data** &mdash; a fixed, identified snapshot (a versioned file or a query with a frozen "
 "as-of date), not \"whatever's in the table today.\"\n"
 "- **Randomness** &mdash; a fixed **random seed**, so every shuffle, split, and model init is "
 "repeatable.\n\n"
 "Pin all four and the same inputs *always* give the same output. Leave one floating and you'll spend "
 "a Friday hunting a number that changed for no visible reason."))

p.append(B.h2("Seeds: making 'random' repeatable", kicker="Pillar 4, hands-on"))
p.append(B.concept(
 "Computers don't produce true randomness &mdash; they produce a **deterministic sequence** from a "
 "starting **seed**. Set the same seed and you get the same \"random\" numbers every time. That's "
 "not cheating; it's how you make a train/test split, a shuffle, or a model's initialization "
 "**reproducible**:"))
_c,_o=_run(r'''
import numpy as np

# Same seed -> identical draws, every run, every machine
a = np.random.default_rng(42).normal(size=5)
b = np.random.default_rng(42).normal(size=5)
print("seed 42, run 1:", a.round(3))
print("seed 42, run 2:", b.round(3))
print("identical? ", np.allclose(a, b))

# A different seed -> a different (but also repeatable) sequence
c = np.random.default_rng(7).normal(size=5)
print("seed  7      :", c.round(3))
''')
p.append(B.code_example(_c,_o,filename="seeds.py"))
p.append(B.tip(
 "Prefer the modern `np.random.default_rng(seed)` **generator object** over the old global "
 "`np.random.seed()`. Passing an explicit generator (or `random_state=42` to scikit-learn's "
 "`train_test_split`, `KFold`, models, etc.) keeps randomness **local and explicit** &mdash; no "
 "spooky action where one library's shuffle changes another's results."))

p.append(B.h2("A project layout that reproduces itself", kicker="Structure = trust"))
p.append(B.concept(
 "Reproducibility is also a *filing* discipline. A predictable structure tells anyone (including "
 "future-you) exactly where things are and how to run them:"))
p.append(B.code_example(
 "churn/\n"
 "  README.md            # what this is + HOW TO RUN it (the key file)\n"
 "  requirements.txt     # pinned environment\n"
 "  .gitignore           # ignore data/, .venv/, .env\n"
 "  data/\n"
 "    raw/               # original, never-edited input (read-only)\n"
 "    processed/         # generated — reproducible from raw + code\n"
 "  src/                 # tested, importable .py logic\n"
 "  notebooks/           # exploration + narrative\n"
 "  models/              # saved model artifacts",
 "# Anyone can now: read README -> make env -> run -> get your numbers.",
 filename="project structure"))
p.append(B.pitfall(
 "Two structure sins that wreck reproducibility: **hard-coded absolute paths** "
 "(`C:\\Users\\me\\Desktop\\data.csv` won't exist on any other machine &mdash; use paths **relative** "
 "to the project root), and **editing raw data in place** (once you overwrite the original, the "
 "pipeline can't be rerun from scratch). Treat `data/raw/` as **read-only** and write everything "
 "derived to `data/processed/`, regenerable by code."))

p.append(B.h2("Your turn — prove a seed reproduces", kicker="Interactive lab"))
p.append(B.pylab(
 "Reproducibility in one line: with a **fixed seed**, the same computation always yields the same "
 "number. Using a generator seeded with **`123`**, draw **1000** samples from a standard normal, "
 "take their mean, round to **3 decimals**, and assign it to **`answer`**. Anyone who runs this "
 "&mdash; on any machine &mdash; must get the identical value.",
 "import numpy as np\n",
 "rng = np.random.default_rng(123)\n"
 "sample = rng.normal(size=1000)\n"
 "answer = round(float(sample.mean()), 3)",
 starter="import numpy as np\n# seed with 123, draw 1000 normal samples, mean, round to 3 dp\nanswer = ",
 hint="`rng = np.random.default_rng(123)` then `rng.normal(size=1000).mean()`, wrapped in "
      "`round(float(...), 3)`.",
 title="Lab — a fixed seed is a promise",
 preview="numpy is available. First Run boots Python; the value is fully determined by the seed.",
 explain="Everyone who seeds with 123 gets this exact mean &mdash; that's the whole point. Randomness "
         "with a fixed seed is **repeatable**, which is what makes a train/test split or a model run "
         "reproducible for reviewers."))

p.append(B.keypoints([
 "Reproducibility = pinning **four pillars**: **code** (Git), **environment** (requirements/lock), "
 "**data** (a fixed snapshot), and **randomness** (a seed).",
 "A **seed** makes 'random' operations (splits, shuffles, model init) repeatable &mdash; same seed, "
 "same result, every machine.",
 "Prefer explicit `default_rng(seed)` / `random_state=` over the global `np.random.seed()`.",
 "Use a **predictable project layout** with a `README` that says *how to run it*; keep `data/raw/` "
 "**read-only**.",
 "Avoid **absolute paths** and **editing raw data in place** &mdash; both silently break reruns.",
]))

p.append(B.quiz([
 {"q":"Your model's accuracy is slightly different every time you run the exact same script. Most "
      "likely fix?",
  "options":[
   {"t":"Set a random seed (e.g. random_state=42) so the train/test split and model init are "
        "repeatable","correct":True,
    "why":"Correct. Un-seeded randomness in the split, shuffle, or initialization makes results wobble "
          "run to run. Fixing the seed pins that randomness so the number is reproducible."},
   {"t":"Buy a faster computer",
    "why":"Hardware speed doesn't change results. The variation comes from unseeded randomness."},
   {"t":"Run it more times and average — the randomness is unavoidable",
    "why":"For reproducibility you *pin* the randomness with a seed. (Averaging over seeds is a "
          "separate tactic for estimating variability, not for reproducibility.)"},
   {"t":"Upgrade pandas to the latest version",
    "why":"Version churn can cause drift, but the classic 'different every run of the *same* script' "
          "signature is an unset seed."}]},
 {"q":"Which practice most undermines reproducibility?",
  "options":[
   {"t":"Overwriting the original raw data file with your cleaned version","correct":True,
    "why":"Correct. Once the raw input is gone, no one can rerun the pipeline from scratch or audit "
          "your cleaning. Keep `data/raw/` read-only and write derived data elsewhere."},
   {"t":"Committing a pinned requirements.txt",
    "why":"That *supports* reproducibility &mdash; it lets others rebuild your exact environment."},
   {"t":"Writing a README that explains how to run the project",
    "why":"A run guide is a pillar of reproducibility, not a threat to it."},
   {"t":"Using a fixed random seed",
    "why":"A fixed seed is exactly what makes randomised steps reproducible."}]},
]))

p.append(B.practice([
 {"q":"A stakeholder asks you to reproduce a result you generated six months ago. What four things "
      "would you need to have preserved, and why each?",
  "sol":"**Code** at that point (a Git commit/tag) &mdash; so you run the *same* logic, not today's "
        "edited version. **Environment** (a pinned `requirements.txt`/lockfile) &mdash; so libraries "
        "behave as they did then (a pandas or sklearn change can shift results). **Data** &mdash; the "
        "exact input snapshot or a query frozen to that as-of date, since the live table has moved "
        "on. **Random seed** &mdash; so splits/shuffles/model init recreate identically. With all "
        "four preserved, the old number is regenerable; miss one and you can only *approximate* it."},
 {"q":"Explain why relative paths and a README matter for a project someone else will run.",
  "sol":"**Relative paths** (`data/raw/x.csv`, resolved from the project root) work on *any* machine; "
        "**absolute paths** (`/Users/me/...`) exist only on yours and break instantly on a "
        "collaborator's laptop or a server. A **README** removes guesswork: it states what the "
        "project is, how to build the environment, and the exact commands to reproduce the outputs "
        "&mdash; turning *\"ask the author\"* into *\"read three lines and run.\"* Together they make "
        "the repo **self-contained and runnable**, which is the practical definition of "
        "reproducible."},
]))

p.append(B.deepdive(
 B.concept(
  "**A spectrum, matched to stakes.** Reproducibility isn't one switch &mdash; it's levels you dial "
  "up as the cost of being wrong rises. *Minimum:* Git + `requirements.txt` + a seed. *Stronger:* a "
  "**lockfile** (exact transitive versions) and **data versioning** with a tool like **DVC**, which "
  "tracks large datasets by hash alongside your code so `git checkout` also pins *which data*. "
  "*Strongest:* a **Docker** image that freezes the OS and system libraries, and a one-command "
  "pipeline (a `Makefile` or workflow tool) so `make all` regenerates every output from raw inputs. "
  "A quick EDA needs level one; a regulated model in production earns level three.") +
 B.concept(
  "**True end-to-end reproducibility means: delete every generated file, run one command, and get "
  "byte-identical outputs.** That's a high bar, and worth aiming at for anything important. Even "
  "partial progress pays: a pinned environment plus seeds plus a `make`-style build script catches "
  "the overwhelming majority of *\"it changed and I don't know why\"* incidents &mdash; the failure "
  "mode that quietly erodes trust in a data team. Reproducibility is, in the end, a **trust** "
  "technology."),
 title="Deep dive: the reproducibility spectrum — lockfiles, DVC, Docker, and one-command pipelines"))

LESSONS={"tool-05-repro":"\n".join(p)}
print("content_tool05 OK — chars:", len(LESSONS["tool-05-repro"]))
