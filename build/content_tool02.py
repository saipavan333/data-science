# -*- coding: utf-8 -*-
import builder as B
IMG="../assets/img/"; p=[]

p.append(B.why(
 "**Git is not optional.** It's your infinite undo button, the only sane way to work with other "
 "people, and &mdash; through GitHub &mdash; your public portfolio. A hiring manager who sees a green "
 "commit history and clean repos already half-believes you. More practically: the day you overwrite "
 "three hours of work, Git is the difference between *\"git checkout\"* and *\"start over.\"* Learn "
 "the mental model once and it serves you for your whole career."))

p.append(B.h2("The mental model — four places your code lives", kicker="This is the whole thing"))
p.append(B.concept(
 "Almost every Git confusion dissolves once you can picture the **four areas** a change moves "
 "through. You *edit* in the working directory, *stage* the edits you want to keep together, "
 "*commit* them into permanent local history, and *push* that history to a remote like GitHub:"))
p.append(B.figure(IMG+"s_tool_git.png",
 "**The four areas.** `git add` stages your chosen edits; `git commit` seals them into local history "
 "with a message; `git push` sends history to GitHub; `git pull` brings others' commits back. A "
 "commit is a **snapshot**, not a diff &mdash; you can always return to exactly how things were.",
 "Working directory to staging area to local repository to remote, with add, commit, push, pull."))
p.append(B.concept(
 "Why the middle *staging* step exists: it lets you commit a **coherent slice** of your work "
 "(\"fix the date parser\") even if you also have unrelated half-finished edits open. Good history "
 "is made of small, self-contained commits &mdash; and staging is how you compose them."))

p.append(B.h2("The everyday loop", kicker="90% of your Git life"))
p.append(B.code_example(
 "git status                 # what's changed / staged? (run this constantly)\n"
 "git add churn_model.py     # stage one file  (git add -p to stage chunks)\n"
 "git commit -m \"Add churn baseline model\"   # seal it into history\n"
 "git push                   # send commits to GitHub\n"
 "git log --oneline -5       # recent history, one line each",
 "$ git status\nChanges not staged for commit:\n  modified:   churn_model.py\n$ git add churn_model.py\n$ git commit -m \"Add churn baseline model\"\n[main a1b2c3d] Add churn baseline model\n 1 file changed, 42 insertions(+)\n$ git push\n   f4e5d6a..a1b2c3d  main -> main",
 filename="terminal"))
p.append(B.tip(
 "Write commit messages in the **imperative** &mdash; *\"Add ROC curve\"*, *\"Fix leakage in "
 "pipeline\"* &mdash; as if completing the sentence *\"This commit will...\"*. Small, frequent, "
 "well-labelled commits are a gift to future-you, who will one day need to find exactly when a bug "
 "crept in (`git bisect` makes that a two-minute search &mdash; but only if your history is clean)."))

p.append(B.h2("Branches — work without fear", kicker="Parallel universes"))
p.append(B.concept(
 "A **branch** is a cheap, isolated line of development. You make one to try an idea; if it works you "
 "**merge** it back into `main`, if it doesn't you delete it &mdash; `main` never saw the mess. On a "
 "team, everyone branches, and changes come together through **pull requests** (a request to merge, "
 "plus a place to review):"))
p.append(B.code_example(
 "git checkout -b feature/add-xgboost   # create + switch to a branch\n"
 "#   ... edit, add, commit as usual ...\n"
 "git push -u origin feature/add-xgboost  # push the branch to GitHub\n"
 "#   ... open a Pull Request on GitHub, get review, merge ...\n"
 "git checkout main && git pull          # come back, get the merged work",
 "$ git checkout -b feature/add-xgboost\nSwitched to a new branch 'feature/add-xgboost'\n$ git push -u origin feature/add-xgboost\n * [new branch]  feature/add-xgboost -> feature/add-xgboost",
 filename="terminal"))

p.append(B.h2("Two files that save you", kicker=".gitignore & undo"))
p.append(B.pitfall(
 "**Never commit data, secrets, or virtual environments.** A committed API key is a security "
 "incident (it lives in history forever, even if you delete it later); a committed 2&nbsp;GB dataset "
 "bloats the repo for everyone. A `.gitignore` file lists what Git should ignore:\n\n"
 "```\n.env\n*.csv\ndata/\n.venv/\n__pycache__/\n.ipynb_checkpoints/\n```\n\n"
 "Set this up **before** your first commit &mdash; un-committing something after it's in history is "
 "far harder than never adding it."))
p.append(B.concept(
 "And the commands that turn a mistake into a shrug &mdash; matched to what you actually want:\n\n"
 "- **Discard un-staged edits** to a file: `git restore file.py` (back to the last commit).\n"
 "- **Unstage** something you `add`-ed too early: `git restore --staged file.py`.\n"
 "- **Undo a pushed commit safely**: `git revert <hash>` &mdash; it makes a *new* commit that "
 "reverses the old one, so shared history stays intact.\n\n"
 "Prefer `revert` over `reset` for anything you've already pushed &mdash; rewriting shared history "
 "breaks your teammates' repos."))

p.append(B.keypoints([
 "Git tracks four areas: **working dir &rarr; staging (`add`) &rarr; local history (`commit`) &rarr; "
 "remote (`push`)**. A commit is a **snapshot** you can always return to.",
 "The daily loop is **status &rarr; add &rarr; commit -m &rarr; push**; run `git status` constantly.",
 "**Branch** for every new idea; merge good ones via a **pull request**; delete the rest &mdash; "
 "`main` stays clean.",
 "**`.gitignore`** data, secrets (`.env`), and `.venv/` **before** your first commit &mdash; a "
 "committed secret lives in history forever.",
 "Undo safely: **`restore`** working edits, **`revert`** already-pushed commits (never `reset` "
 "shared history).",
]))

p.append(B.quiz([
 {"q":"You accidentally committed and pushed a file with your database password. Best fix?",
  "options":[
   {"t":"Rotate the credential immediately, then remove it from history — a pushed secret is "
        "compromised the moment it's public","correct":True,
    "why":"Correct. Once pushed, assume it's leaked: **change the password now**. Deleting the file in "
          "a new commit isn't enough &mdash; it's still in history &mdash; so also scrub history "
          "(e.g. git-filter-repo) and add it to `.gitignore`. Rotation is the urgent part."},
   {"t":"Just delete the file in a new commit — that removes it",
    "why":"The secret still lives in the earlier commit in history and remains readable. And it's "
          "already public, so the credential must be rotated regardless."},
   {"t":"Nothing — it's in a private repo so it's fine",
    "why":"Private repos get shared, forked, and breached; secrets never belong in Git. Rotate and "
          "remove."},
   {"t":"Force-push to overwrite the remote and move on",
    "why":"Even if you scrub history, the credential was exposed and must be rotated. Force-pushing "
          "also breaks teammates' clones."}]},
 {"q":"What's the point of the staging area (git add) sitting between your edits and a commit?",
  "options":[
   {"t":"It lets you commit a coherent subset of your changes, so history is made of small, focused "
        "commits","correct":True,
    "why":"Correct. Staging lets you group *just* the edits that belong together into one commit, even "
          "if you have other unrelated changes open &mdash; giving you clean, reviewable history."},
   {"t":"It backs up your files to GitHub",
    "why":"That's `push`. Staging is purely local &mdash; it selects what goes into the next commit."},
   {"t":"It compresses your files",
    "why":"Staging is about *selecting* changes, not compression."},
   {"t":"It has no purpose; add and commit could be one step",
    "why":"The separation is deliberate: it's what lets you craft focused commits from a messy working "
          "directory."}]},
]))

p.append(B.practice([
 {"q":"Describe the full branch-based workflow to add a feature to a shared project, from creating "
      "the branch to it landing in main.",
  "sol":"`git checkout -b feature/x` to branch off `main`; make small **commits** as you work "
        "(`add` &rarr; `commit -m`); `git push -u origin feature/x` to publish the branch; open a "
        "**pull request** on GitHub; respond to review and push fixes (they update the PR); once "
        "approved, **merge** the PR into `main`; delete the branch; and locally `git checkout main "
        "&& git pull` to sync the merged work. This keeps `main` always-working and every change "
        "reviewed."},
 {"q":"A teammate pushed commits to main while you were working. Your push is rejected ('non-fast-"
      "forward'). What do you do?",
  "sol":"Your local `main` is behind the remote. **Pull first** &mdash; `git pull` (which fetches "
        "their commits and merges, or rebases yours on top). If your changes and theirs touched the "
        "same lines, Git flags a **merge conflict**: open the marked files, choose the correct "
        "combined version, remove the `<<<<<<< / ======= / >>>>>>>` markers, `git add` the resolved "
        "files, complete the merge, and *then* `git push`. The rejection is Git protecting you from "
        "silently overwriting their work."},
]))

p.append(B.deepdive(
 B.concept(
  "**Merge vs. rebase &mdash; two ways to combine history.** `git merge` ties two branches together "
  "with a *merge commit*, preserving exactly what happened (branchy but truthful). `git rebase` "
  "replays your commits on top of the latest `main`, producing a **linear**, tidy history &mdash; at "
  "the cost of rewriting your commits' identities. The rule that keeps teams sane: **rebase your own "
  "un-pushed local work** to tidy it, but **never rebase commits others may already have** (it "
  "rewrites shared history and breaks their repos). When in doubt, merge.") +
 B.concept(
  "**Reading and bisecting history.** `git log --oneline --graph` draws the branch structure; "
  "`git blame file.py` shows who last changed each line (and in which commit) &mdash; invaluable for "
  "*\"why is this here?\"*; and `git bisect` binary-searches your history to find the exact commit "
  "that introduced a bug, testing a handful of commits instead of hundreds. All three only work well "
  "if your commits are small and message-labelled &mdash; another reason commit hygiene pays off.") +
 B.concept(
  "**A realistic minimal workflow for solo projects.** You don't need the full team ceremony to "
  "benefit: `main` for known-good work, a short-lived branch per experiment, commit early and often "
  "with real messages, push to GitHub as backup + portfolio, and a `README` that says how to run it. "
  "That alone puts you ahead of most self-taught candidates &mdash; and it scales smoothly to team "
  "work when you get there."),
 title="Deep dive: merge vs. rebase, blame/bisect, and a workflow that scales from solo to team"))

p.append(B.callout("note","Interview-ready",
 "Expect *\"walk me through your Git workflow\"* and *\"how would you undo X?\"*. Show the mental "
 "model (four areas), the branch-and-PR loop, and &mdash; the senior tell &mdash; that you `revert` "
 "pushed commits rather than rewrite shared history, and never commit data or secrets. Judgement "
 "about *history and collaboration*, not memorised flags, is what they're listening for.", "&#9670;"))

LESSONS={"tool-02-git":"\n".join(p)}
print("content_tool02 OK — chars:", len(LESSONS["tool-02-git"]))
