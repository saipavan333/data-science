# -*- coding: utf-8 -*-
import builder as B
p=[B.concept("The Data Scientist's Toolkit on one page &mdash; the command line, Git, environments, "
 "notebooks, and reproducibility. Press **Print** for a desk copy.")]
p.append(B.cheatsheet("The Toolkit — one-page reference",
 "The professional substrate under every model: **version your code, isolate your environment, run "
 "reproducibly, ship from the terminal.**",
 [
  ("Command line", [
    ("pwd / ls -lh / cd", "where am I / list / move"),
    ("head / tail / wc -l", "peek + count rows without opening"),
    ("grep / cut / sort / uniq -c", "search, pick a column, count values"),
    ("cmd1 | cmd2", "**pipe**: streams, so size doesn't matter"),
    ("rm", "**no undo** &mdash; triple-check paths"),
  ]),
  ("Git — four areas", [
    ("working dir &rarr; staging", "`git add`"),
    ("staging &rarr; history", "`git commit -m`"),
    ("history &rarr; remote", "`git push` (`git pull` back)"),
    ("git status", "run it constantly"),
    ("branch + PR", "isolate work; merge via review"),
    ("revert (not reset)", "undo **pushed** commits safely"),
  ]),
  ("Environments", [
    ("python -m venv .venv", "create isolated env"),
    ("source .venv/bin/activate", "activate (installs land inside)"),
    ("pip freeze > requirements.txt", "snapshot exact versions"),
    ("pip install -r requirements.txt", "rebuild it elsewhere"),
    (".gitignore", "`.env`, data/, `.venv/` &mdash; never commit"),
  ]),
  ("Notebooks", [
    ("kernel", "remembers every var you've run"),
    ("hidden-state trap", "out-of-order runs / zombie vars"),
    ("Restart & Run All", "before trusting or sharing"),
    ("move to .py", "reusable/tested/production code"),
  ]),
  ("Reproducibility", [
    ("4 pillars", "code + data + environment + seed"),
    ("random seed", "`default_rng(42)` &rarr; repeatable"),
    ("relative paths", "never `C:/Users/me/...`"),
    ("data/raw read-only", "regenerate processed from it"),
    ("README", "how to run it, in 3 lines"),
  ]),
 ]))
LESSONS={"tool-07-cheat":"\n".join(p)}
print("toolcheat OK")
