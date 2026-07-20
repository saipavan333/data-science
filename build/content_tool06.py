# -*- coding: utf-8 -*-
import builder as B
p=[]

p.append(B.why(
 "The Toolkit track rarely gets its *own* interview &mdash; instead it shows up as **judgement** "
 "woven through every other answer. Say *\"I'd branch, add a test, and open a PR\"* or *\"I pin the "
 "environment and set a seed so it's reproducible\"* and an interviewer instantly reads you as "
 "someone who has shipped real work, not just trained models in a notebook. This check drills the "
 "sentences that signal **craft**."))

p.append(B.h2("Say these out loud", kicker="Rapid-fire drill"))
p.append(B.interview_check([
 "Walk me through your **Git workflow** on a shared project (branch &rarr; commit &rarr; PR &rarr; "
 "merge).",
 "What are the **four areas** a change moves through in Git, and which command moves it between "
 "each?",
 "How do you **undo** a commit you've already pushed &mdash; and why not just `reset`?",
 "Why does every project get its own **virtual environment**? What goes in `requirements.txt`?",
 "What's the **hidden-state trap** in notebooks, and how do you avoid it?",
 "When do you move code **out of a notebook** into a `.py` module?",
 "Name the **four pillars of reproducibility** and how you pin each.",
 "Why is a **random seed** necessary to reproduce a model's results?",
 "What must **never** be committed to Git, and how do you prevent it?",
 "Someone can't reproduce your six-month-old result &mdash; what do you check?",
], title="The toolkit / craft drill")
)

p.append(B.practice([
 {"q":"SCENARIO: You join a team and inherit a 600-cell notebook that 'only Priya can run.' It "
      "produces the weekly revenue model. How do you make it trustworthy?",
  "sol":"Diagnose it as a **reproducibility + structure** problem and fix it in layers. (1) **Pin the "
        "environment**: capture Priya's package versions into a `requirements.txt`/lockfile so anyone "
        "can rebuild it. (2) **Restart & Run All** on a clean kernel to surface hidden-state bugs "
        "(out-of-order cells, zombie variables) and fix them so it runs top-to-bottom. (3) **Extract "
        "logic** into tested `.py` modules under `src/`, leaving the notebook a thin narrative that "
        "imports them &mdash; now it's reviewable and diff-able. (4) **Version it** in Git with a "
        "`README` that states how to run it, **seed** the randomness, and pin the **data** snapshot. "
        "(5) Optionally schedule the module code so the weekly run doesn't depend on a human opening "
        "a notebook. The through-line: turn *\"only Priya can run it\"* into *\"anyone can run it "
        "with one command.\"*"},
 {"q":"SCENARIO: Your teammate force-pushed to main and your local repo is now a mess of conflicts. "
      "What went wrong culturally, and how do you recover?",
  "sol":"**Culturally:** force-pushing to a **shared** branch rewrites history everyone else has, "
        "which is exactly what you must never do &mdash; shared branches should only move forward, "
        "and changes should land via **reviewed PRs**, not direct force-pushes to `main`. "
        "**Recovery:** don't panic-delete; your commits still exist locally (and in `git reflog`). "
        "Fetch the rewritten remote, create a branch from your own work, and **rebase or "
        "cherry-pick** your commits onto the new `main` history, resolving conflicts deliberately; "
        "then open a PR. Going forward, **protect `main`** (require PRs + reviews, block force-push) "
        "so the failure can't recur. The senior signal is naming the *process* fix, not just the "
        "command sequence."},
]))

p.append(B.callout("note","The through-line of the whole track",
 "None of these tools train a model &mdash; and that's the point. Git, environments, notebooks, and "
 "reproducibility are the **professional substrate** that makes your modelling *trustworthy and "
 "shareable*. Interviewers probe them because they separate people who produce one-off numbers from "
 "people who ship work a team can build on. Show the habits &mdash; branch-and-PR, pinned envs, "
 "Restart & Run All, seeds and structure &mdash; and you signal that you're the second kind.",
 "&#9670;"))

LESSONS={"tool-06-interview":"\n".join(p)}
print("content_tool06 OK — chars:", len(LESSONS["tool-06-interview"]))
