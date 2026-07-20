# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "Every data scientist eventually meets a machine with **no graphical interface** &mdash; a cloud "
 "server, a training box, a colleague's Docker container. The **command line** is how you drive it. "
 "It's also the fastest way on Earth to answer *\"how many rows is this 4&nbsp;GB file?\"* or "
 "*\"which values are in this column?\"* &mdash; without ever opening the file. The terminal isn't "
 "nostalgia; it's a **data tool**, and fluency here is one of the quiet signals that separates people "
 "who *use* data tools from people who *build* with them."))

p.append(B.h2("Getting around — the five verbs", kicker="Navigation"))
p.append(B.concept(
 "A filesystem is a tree; the command line lets you walk it. Five commands cover 90% of movement:"))
p.append(B.code_example(
 "pwd                 # print working directory — 'where am I?'\n"
 "ls -lh              # list files, long form, human-readable sizes\n"
 "cd projects/churn   # change directory (cd .. goes up one)\n"
 "mkdir -p data/raw   # make folders (-p creates parents as needed)\n"
 "cp a.csv data/      # copy;  mv renames/moves;  rm deletes (careful!)",
 "$ pwd\n/home/you/projects/churn\n$ ls -lh\n-rw-r--r--  1 you  staff   4.2G  Jul 20 09:14  events.csv\n-rw-r--r--  1 you  staff   2.1K  Jul 20 09:10  README.md",
 filename="terminal"))
p.append(B.warn(
 "~rm~ has **no undo** and **no trash** on the command line &mdash; a deleted file is gone. Never run "
 "`rm -rf` with a path you haven't triple-checked, and never with a variable you're not 100% sure of "
 "(`rm -rf $DIR/` when `$DIR` is empty deletes `/`). This is the one place to slow down."))

p.append(B.h2("Reading a file without opening it", kicker="The data superpower"))
p.append(B.concept(
 "This is where the terminal beats every spreadsheet. You can inspect a file **too big to open** in "
 "seconds &mdash; peek at the top, count the rows, find a value:"))
p.append(B.code_example(
 "head -3 events.csv        # first 3 lines (see the header + shape)\n"
 "tail -2 events.csv        # last 2 lines\n"
 "wc -l events.csv          # count lines (rows)\n"
 "grep \"signup\" events.csv  # every line containing 'signup'\n"
 "cut -d, -f2 events.csv    # pull column 2 (comma-delimited)",
 "$ head -3 events.csv\nuser_id,event,ts\n1042,signup,2026-07-19T10:02\n1042,purchase,2026-07-19T10:31\n\n$ wc -l events.csv\n 8123456 events.csv",
 filename="terminal"))

p.append(B.h2("Pipes — small tools, chained", kicker="The Unix philosophy"))
p.append(B.concept(
 "The magic is the **pipe** (`|`): it feeds one command's output into the next. Each tool does one "
 "thing; you compose them into an answer. The classic *\"count the distinct values in a column, most "
 "common first\"* is a one-liner &mdash; no Python, no pandas:"))
p.append(B.code_example(
 "cut -d, -f2 events.csv | sort | uniq -c | sort -rn | head\n"
 "#  ^ column 2         ^sort  ^count   ^by count  ^top",
 "$ cut -d, -f2 events.csv | sort | uniq -c | sort -rn | head\n 4120233 view\n 2891004 click\n  812440 purchase\n  299779 signup",
 filename="terminal"))
p.append(B.tip(
 "Read a pipeline **left to right** as a sentence: *take column 2, sort it, count runs of each value, "
 "sort those counts descending, show the top.* You just did a `GROUP BY ... COUNT ORDER BY` on a "
 "multi-gigabyte file with five tiny programs and no memory blow-up &mdash; because each tool "
 "**streams** its input."))
p.append(B.figure(IMG+"s_tool_git.png",
 "Preview of the next lesson's mental model &mdash; but notice the same idea: **stages connected by "
 "arrows.** The command line teaches you to think in flows, and Git formalises it.",
 "The Git flow: working directory to staging to local repo to remote.") if False else "")

p.append(B.h2("Try the thinking — a pipeline in Python", kicker="Interactive lab"))
p.append(B.pylab(
 "The CLI pattern `cut | sort | uniq -c | sort -rn | head -1` finds the **most common value**. "
 "Reproduce its logic in Python: given the `events` list of rows, count how often each `event` "
 "appears and assign the **most common event name** (a string) to **`answer`**.",
 "events = [\n"
 "  ('1042','signup'), ('1042','purchase'), ('7','view'), ('7','view'),\n"
 "  ('7','click'), ('9','view'), ('9','click'), ('9','purchase'),\n"
 "  ('12','view'), ('12','view'), ('12','view'), ('3','signup'),\n"
 "]\n",
 "from collections import Counter\n"
 "counts = Counter(ev for _uid, ev in events)\n"
 "answer = counts.most_common(1)[0][0]",
 starter="# events is a list of (user_id, event) tuples\n# count events, pick the most common name\nanswer = ",
 hint="`collections.Counter` with `.most_common(1)` mirrors `uniq -c | sort -rn | head -1`. "
      "`most_common(1)` returns `[(name, count)]` &mdash; take `[0][0]` for the name.",
 title="Lab — 'uniq -c | sort -rn' in Python",
 preview="`events` (list of (user_id, event) tuples) is preloaded. First Run may take a moment to boot Python.",
 explain="`view` appears most (4 times). `Counter` **is** the pipeline &mdash; the same "
         "count-then-rank idea, whether you express it in five shell tools or one Python line."))

p.append(B.keypoints([
 "The terminal is how you drive **headless** machines (servers, containers) &mdash; unavoidable in "
 "real DS work.",
 "Navigate with **pwd / ls / cd / mkdir / cp&nbsp;·&nbsp;mv&nbsp;·&nbsp;rm**. `rm` has **no undo** "
 "&mdash; slow down.",
 "Inspect huge files instantly: **head / tail / wc -l / grep / cut** &mdash; no need to open them.",
 "The **pipe** `|` chains one-job tools into an answer; each tool **streams**, so size doesn't "
 "matter.",
 "`cut | sort | uniq -c | sort -rn` **is** a GROUP-BY-COUNT &mdash; think in flows.",
]))

p.append(B.quiz([
 {"q":"You're handed a 6&nbsp;GB CSV and asked \"how many rows?\" Fastest reliable move?",
  "options":[
   {"t":"`wc -l file.csv` in the terminal","correct":True,
    "why":"Correct. `wc -l` streams the file and counts lines in seconds without loading it into "
          "memory. Opening it in Excel or pandas could exhaust RAM."},
   {"t":"Open it in Excel and look at the last row number",
    "why":"Excel caps at ~1M rows and may refuse or truncate a 6 GB file entirely."},
   {"t":"`pd.read_csv('file.csv')` then `len(df)`",
    "why":"Loads the whole file into memory just to count rows &mdash; slow and may not fit in RAM. "
          "`wc -l` is instant."},
   {"t":"Count them by hand in a text editor",
    "why":"Most editors won't open a 6 GB file, and counting by hand is infeasible."}]},
 {"q":"What does `cut -d, -f2 data.csv | sort | uniq -c` produce?",
  "options":[
   {"t":"A count of how many times each distinct value of column 2 appears","correct":True,
    "why":"Correct. `cut` pulls column 2, `sort` groups equal values together, and `uniq -c` collapses "
          "each run to one line prefixed by its count &mdash; a GROUP BY / COUNT."},
   {"t":"The second row of the file",
    "why":"`-f2` selects the second *field* (column), not the second row, and the pipeline counts "
          "values."},
   {"t":"The file sorted by column 2 only",
    "why":"`sort` is a step, but `uniq -c` then counts occurrences &mdash; the output is value counts, "
          "not the sorted file."},
   {"t":"An error — you can't pipe cut into sort",
    "why":"Piping is exactly what these tools are built for; this is a standard idiom."}]},
]))

p.append(B.practice([
 {"q":"In one pipeline, print the 5 most common values of the 3rd (comma-separated) column of "
      "`log.csv`, each with its count.",
  "sol":"`cut -d, -f3 log.csv | sort | uniq -c | sort -rn | head -5`. Read it left to right: pull "
        "column 3, sort so identical values are adjacent, `uniq -c` counts each run, `sort -rn` "
        "orders by count descending (numeric), `head -5` keeps the top five. (Add `tail -n +2` after "
        "`cut` if you want to drop the header row first.)"},
 {"q":"Why is chaining small tools with pipes often better than writing one big script?",
  "sol":"Each tool does **one job well** and **streams** its input, so a pipeline uses almost no "
        "memory even on huge files, is easy to build up and inspect **one stage at a time**, and "
        "reuses battle-tested programs instead of new, buggy code. It's the **Unix philosophy**: "
        "compose simple, sharp tools rather than build monoliths. (When logic gets complex or needs "
        "tests, *then* reach for Python.)"},
]))

p.append(B.deepdive(
 B.concept(
  "**Beyond the basics, three tools pay for themselves.** `grep` (with `-i` case-insensitive, `-v` "
  "invert, `-c` count, `-E` regex) finds lines; `awk` does per-column logic (`awk -F, '$3>100'` keeps "
  "rows where column 3 exceeds 100 &mdash; a filter with no pandas); and `sed` does stream find/"
  "replace (`sed 's/,/\\t/g'` turns a CSV into a TSV). Together they cover a startling share of "
  "\"quick data question\" tasks.") +
 B.concept(
  "**Working on a remote machine.** `ssh user@host` opens a shell on a server; `scp file user@host:"
  "path` copies files to/from it; and redirects (`> out.txt` writes, `>> out.txt` appends, `2>&1` "
  "folds errors into output) let you capture results. A long job survives a dropped connection if you "
  "run it inside `tmux` or with `nohup ... &`. These four ideas &mdash; ssh, scp, redirects, tmux "
  "&mdash; are the daily reality of training models on hardware that isn't your laptop.") +
 B.concept(
  "**A caution on giant files.** Streaming tools (`wc`, `grep`, `cut`, `awk`) scale to any size "
  "because they never hold the whole file in memory. But `sort` **does** buffer (it may spill to "
  "disk), and anything that loads the file at once (an editor, `pandas.read_csv` without "
  "`chunksize`) will struggle. Knowing *which* operations stream and which don't is what lets you "
  "work confidently with data far bigger than RAM."),
 title="Deep dive: grep/awk/sed, working on remote servers, and what streams vs. what doesn't"))

LESSONS={"tool-01-cli":"\n".join(x for x in p if x)}
print("content_tool01 OK — chars:", len(LESSONS["tool-01-cli"]))
