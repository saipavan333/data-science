# -*- coding: utf-8 -*-
import builder as B
IMG="../assets/img/"; p=[]

p.append(B.why(
 "*\"It works on my machine\"* is the most expensive sentence in data science. It usually means your "
 "code secretly depends on the exact package versions you happen to have installed &mdash; and the "
 "moment a colleague, a server, or future-you has different ones, it breaks. **Virtual environments** "
 "fix this by giving every project its own isolated set of packages, and a **requirements file** "
 "records them so anyone can rebuild the exact setup. This is the boundary between a script and "
 "**software people can trust**."))

p.append(B.h2("The problem: one global install, many projects", kicker="Why isolation"))
p.append(B.concept(
 "Install packages globally and every project shares one pile. Project A was built against pandas "
 "1.5; you `pip install` pandas 2.2 for Project B; now Project A silently breaks because a function "
 "changed. A **virtual environment** gives each project its **own** Python and its **own** packages, "
 "so their versions can't collide:"))
p.append(B.figure(IMG+"s_tool_env.png",
 "**Isolation.** Each project gets its own environment with its own package versions. Project A can "
 "keep pandas 1.5 while Project B uses 2.2 &mdash; they never see each other, so upgrading one can't "
 "break the other.",
 "Two isolated environments, ds-a with older package versions and ds-b with newer ones."))

p.append(B.h2("Create, activate, install", kicker="The venv workflow"))
p.append(B.concept(
 "Python ships with `venv`. Three moves: create an environment (a folder), **activate** it (so "
 "`python` and `pip` now point *inside* it), then install what you need &mdash; those installs land "
 "in the environment, not globally:"))
p.append(B.code_example(
 "python -m venv .venv          # create an env in a .venv/ folder\n"
 "source .venv/bin/activate     # activate  (Windows: .venv\\Scripts\\activate)\n"
 "pip install pandas scikit-learn   # installs INTO .venv, not globally\n"
 "python churn.py               # runs with exactly these packages\n"
 "deactivate                    # leave the env when done",
 "$ python -m venv .venv\n$ source .venv/bin/activate\n(.venv) $ pip install pandas scikit-learn\nSuccessfully installed pandas-2.2.2 scikit-learn-1.5.0 ...\n(.venv) $ ",
 filename="terminal"))
p.append(B.tip(
 "The `(.venv)` that appears in your prompt is Git-style peace of mind: it tells you *which* "
 "environment is active. Add `.venv/` to your **`.gitignore`** &mdash; you record the *recipe* "
 "(requirements), never the built environment itself, which is large and machine-specific."))

p.append(B.h2("Pinning: the recipe anyone can rebuild", kicker="requirements.txt"))
p.append(B.concept(
 "An environment is worthless to others unless they can recreate it. `pip freeze` writes the exact "
 "installed versions to a file; anyone (or any server) rebuilds the identical setup with one "
 "command:"))
p.append(B.code_example(
 "pip freeze > requirements.txt    # snapshot exact versions\n"
 "#   -- someone else, or a server, later: --\n"
 "python -m venv .venv && source .venv/bin/activate\n"
 "pip install -r requirements.txt  # rebuild the SAME environment",
 "$ cat requirements.txt\npandas==2.2.2\nscikit-learn==1.5.0\nnumpy==2.0.1",
 filename="terminal"))
p.append(B.warn(
 "Pin with `==` for anything you need to **reproduce** (analyses, deployed models). Loose "
 "specifications like `pandas>=2.0` are convenient but let versions drift, and *\"it worked last "
 "month\"* becomes a mystery. A pinned `requirements.txt` (or a lockfile) is what makes a result "
 "**reproducible** &mdash; the subject of lesson 3.5."))

p.append(B.keypoints([
 "A **virtual environment** gives each project its own isolated packages, so upgrading one project "
 "can't break another.",
 "Workflow: **`python -m venv .venv`** &rarr; **activate** &rarr; **`pip install`** (lands inside "
 "the env) &rarr; `deactivate`.",
 "**`.gitignore` the `.venv/`** &mdash; commit the *recipe*, not the built environment.",
 "**`pip freeze > requirements.txt`** snapshots exact versions; **`pip install -r`** rebuilds them "
 "elsewhere.",
 "**Pin with `==`** for anything that must be reproducible; loose ranges let versions silently "
 "drift.",
]))

p.append(B.quiz([
 {"q":"Why put each project in its own virtual environment instead of installing everything globally?",
  "options":[
   {"t":"So each project can pin the package versions it needs without conflicting with other "
        "projects","correct":True,
    "why":"Correct. Isolation means Project A's pandas 1.5 and Project B's pandas 2.2 coexist "
          "peacefully &mdash; upgrading one never breaks the other, and each is independently "
          "reproducible."},
   {"t":"To make your code run faster",
    "why":"Environments are about *isolation and reproducibility*, not speed &mdash; the same code "
          "runs at the same speed."},
   {"t":"To reduce disk usage",
    "why":"Separate environments actually use *more* disk (duplicated packages); the payoff is "
          "isolation, not savings."},
   {"t":"Because pip requires it",
    "why":"pip works globally too; environments are a best practice you choose, not a pip "
          "requirement."}]},
 {"q":"A collaborator clones your repo but the code crashes with import errors. Most likely fix you "
      "should have enabled?",
  "options":[
   {"t":"Ship a requirements.txt so they can `pip install -r` the exact versions you used","correct":True,
    "why":"Correct. Import/version errors on a fresh clone almost always mean missing or mismatched "
          "packages. A pinned `requirements.txt` lets them rebuild your exact environment in one "
          "command."},
   {"t":"Commit your .venv/ folder so they get your packages",
    "why":"A built `.venv/` is large and machine-specific (wrong OS/paths) &mdash; it won't work on "
          "their machine. Commit the *recipe* (`requirements.txt`) instead."},
   {"t":"Tell them to install the latest of everything",
    "why":"'Latest' may differ from what you built against and reintroduce the mismatch. Pin exact "
          "versions."},
   {"t":"Send them your global Python install",
    "why":"Not portable or reproducible; the standard answer is a pinned requirements file."}]},
]))

p.append(B.practice([
 {"q":"Write the full sequence to start a new project 'fraud', install pandas and matplotlib in "
      "isolation, and record the versions for others.",
  "sol":"`mkdir fraud && cd fraud` &rarr; `python -m venv .venv` &rarr; `source .venv/bin/activate` "
        "(Windows: `.venv\\Scripts\\activate`) &rarr; `pip install pandas matplotlib` &rarr; "
        "`pip freeze > requirements.txt` &rarr; add `.venv/` to `.gitignore`. Now anyone can "
        "reproduce it with `python -m venv .venv && source .venv/bin/activate && pip install -r "
        "requirements.txt`."},
 {"q":"When would you reach for conda instead of venv + pip?",
  "sol":"When you need **non-Python** dependencies or specific system libraries &mdash; e.g. a "
        "particular CUDA/cuDNN for GPU deep learning, or heavy geospatial/scientific stacks (GDAL, "
        "certain BLAS builds) that are painful to compile. Conda manages those binary dependencies "
        "and Python versions together across OSes. For pure-Python projects, `venv` + `pip` (or "
        "modern tools like `uv`/`poetry`) is lighter and perfectly sufficient."},
]))

p.append(B.deepdive(
 B.concept(
  "**The tool landscape, briefly.** `venv`+`pip` is the built-in baseline. **conda** additionally "
  "manages non-Python binaries and Python itself (great for GPU/scientific stacks). **poetry** and "
  "the very fast **uv** add proper *dependency resolution* and **lockfiles** &mdash; a "
  "`poetry.lock`/`uv.lock` records not just your direct packages but every transitive dependency's "
  "exact version and hash, so an install is bit-for-bit repeatable. For serious projects, a lockfile "
  "beats a hand-maintained `requirements.txt`.") +
 B.concept(
  "**Environments end where the OS begins.** A virtual environment pins Python packages, but not the "
  "operating system, system libraries, or environment variables. When *those* matter &mdash; "
  "deploying a model, guaranteeing a teammate's setup exactly &mdash; you graduate to a **container** "
  "(Docker), which packages the whole userland. Think of it as a spectrum of reproducibility: "
  "`requirements.txt` &rarr; lockfile &rarr; Docker image, each pinning more of the world at more "
  "cost. Match the level to the stakes."),
 title="Deep dive: pip vs conda vs poetry/uv, lockfiles, and where Docker takes over"))

LESSONS={"tool-03-envs":"\n".join(p)}
print("content_tool03 OK — chars:", len(LESSONS["tool-03-envs"]))
