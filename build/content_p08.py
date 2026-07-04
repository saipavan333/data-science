# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
IMG="../assets/img/"; p=[]

p.append(B.why(
 "An enormous share of real data is **text**: names, cities, product titles, email addresses, "
 "free-form notes. Before you can analyze it you have to clean and extract from it &mdash; "
 "standardize casing, trim whitespace, pull the domain out of an email, split a full name. This "
 "lesson gives you Python's string tools and, crucially, pandas' **vectorized** `.str` methods "
 "that apply them to a whole column at once."))

p.append(B.h2("A string is a sequence of characters", kicker="Concept"))
p.append(B.concept(
 "A ~string~ (`str`) behaves like a read-only list of characters: you index it (`word[0]`), slice "
 "it (`word[0:4]`), and check length with `len`. The same 0-based, stop-excluded rules from "
 "Lesson 2.1 apply, including negative indices from the end."))
p.append(B.figure(IMG+"s_py_string_anatomy.png",
 "**Indexing and slicing a string.** Positions run from 0; negative indices count from the end; "
 "`word[::-1]` reverses it. Strings are ~immutable~ &mdash; methods return a **new** string "
 "rather than changing the original.",
 "A string with positive and negative indices, slice examples, and common methods."))

p.append(B.h2("Essential string methods", kicker="Concept"))
p.append(B.concept(
 "A handful of methods cover most text cleaning. They all return a **new** string (the original "
 "is untouched):\n\n"
 "- `.strip()` removes surrounding whitespace; `.lower()` / `.upper()` / `.title()` fix casing.\n"
 "- `.replace(old, new)` swaps text; `.split(sep)` breaks a string into a list; `\"-\".join(parts)` "
 "stitches a list back together.\n"
 "- Tests: `.startswith(...)`, `.endswith(...)`, and `\"x\" in text` for containment.\n\n"
 "Combine them with f-strings (Lesson 2.1) and you can reshape almost any text."))

p.append(B.h2("Vectorized strings in pandas: .str", kicker="Concept · the daily tool"))
p.append(B.concept(
 "Looping over a text column would be slow and clumsy. Instead, pandas exposes every string "
 "method through the ~.str accessor~, applying it to the **whole column at once** (vectorized, "
 "Lesson 2.5): `df[\"city\"].str.strip().str.title()` cleans an entire column in one line. "
 "`.str.contains(...)`, `.str.split(...)`, and `.str.replace(...)` are the workhorses of text "
 "cleaning, and they chain just like regular string methods."))

p.append(B.h2("Clean a text column", kicker="Worked example"))
p.append(B.concept(
 "Standardize messy names, then pull structured pieces out of email addresses &mdash; all "
 "vectorized, no loops."))
_c,_o=_run(r'''
import pandas as pd

names = pd.Series(["  ada LOVELACE ", "Linus  Torvalds", "grace HOPPER  "])
clean = names.str.strip().str.title()          # trim, then Title Case — whole column at once
print("cleaned:", clean.tolist())

emails = pd.Series(["ada@dynamics.com", "linus@kernel.org", "grace@dynamics.com"])
print("domains:", emails.str.split("@").str[1].tolist())      # take part after '@'
print("from dynamics.com:", emails.str.endswith("dynamics.com").tolist())
print("count containing 'a':", int(names.str.contains("a", case=False).sum()))
''')
p.append(B.code_example(_c,_o,filename="strings.py"))
p.append(B.note(
 "Notice `names.str.split(\"@\").str[1]` &mdash; the first `.str` splits each string into a list, "
 "and the second `.str[1]` grabs element 1 from each list. Chaining `.str` is how you peel apart "
 "structured text column-wide."))

p.append(B.keypoints([
 "A ~string~ is an indexable, sliceable, **immutable** sequence &mdash; methods return a *new* "
 "string.",
 "Core methods: `.strip()`, `.lower()`/`.upper()`/`.title()`, `.replace()`, `.split()`/`join()`, "
 "`.startswith()`, `in`.",
 "In pandas, the ~.str accessor~ applies string methods to a **whole column** (vectorized) &mdash; "
 "no loops.",
 "Chain `.str` calls (`.str.split('@').str[1]`) to extract structured pieces from text.",
 "`.str.contains()` is the text version of a boolean mask for filtering rows.",
]))

p.append(B.quiz([
 {"q":"After `word = \"Data\"`, what is the value of `word` following `word.upper()`?",
  "options":[
   {"t":"Still \"Data\" — strings are immutable, so .upper() returns a NEW string you must "
        "capture","correct":True,
    "why":"Correct. `.upper()` doesn't change `word` in place; it returns \"DATA\". To keep it you "
          "must assign: `word = word.upper()`. Forgetting this is a classic beginner bug."},
   {"t":"\"DATA\" — .upper() changes word in place",
    "why":"Strings are immutable; `.upper()` returns a new string and leaves `word` as \"Data\" "
          "unless you reassign it."},
   {"t":"An error",
    "why":"`.upper()` is valid and returns \"DATA\"; it just doesn't mutate `word`."},
   {"t":"\"data\"",
    "why":".upper() uppercases; .lower() would give \"data\". Either way `word` itself is "
          "unchanged unless reassigned."}]},
 {"q":"You have a pandas Series `s` of city names with inconsistent spacing and casing. Which "
      "cleans the whole column at once?",
  "options":[
   {"t":'s.str.strip().str.title()',"correct":True,
    "why":"Correct. The `.str` accessor applies string methods to every element vectorized; "
          "chaining strip then title trims whitespace and standardizes casing column-wide."},
   {"t":"s.strip().title()",
    "why":"Those are plain string methods; on a Series you must go through `.str` (e.g., "
          "`s.str.strip()`). Calling `.strip()` directly on a Series raises an error."},
   {"t":"a Python for loop over each city",
    "why":"That works but is slow and unidiomatic. The vectorized `.str` accessor is faster and "
          "cleaner."},
   {"t":"s.replace(' ', '')",
    "why":"`Series.replace` replaces whole values, not substrings, and removing all spaces isn't "
          "the same as trimming/casing. Use `s.str.strip().str.title()`."}]},
 {"q":"What does `emails.str.split(\"@\").str[1]` produce for a Series of email addresses?",
  "options":[
   {"t":"The domain part (after the @) of each email","correct":True,
    "why":"Correct. `.str.split(\"@\")` makes a two-item list per email; `.str[1]` takes the "
          "second item (the domain) from each, vectorized across the column."},
   {"t":"The username (before the @)",
    "why":"That would be `.str[0]`. Index 1 is the second part, the domain."},
   {"t":"An error, because you can't chain .str",
    "why":"Chaining `.str` is valid and idiomatic: split, then index each resulting list with a "
          "second `.str`."},
   {"t":"The whole email unchanged",
    "why":"Splitting on '@' and taking index 1 returns just the domain, not the full address."}]},
]))

p.append(B.practice([
 {"q":"Given `full = \"Ada Lovelace\"`, write expressions to get the first name and the last "
      "name.", "html": True,
  "sol": B.code_example('parts = full.split(" ")     # ["Ada", "Lovelace"]\nfirst = parts[0]            # "Ada"\nlast  = parts[-1]           # "Lovelace"',
         filename="solution.py", runnable=False) + B.fmt(
         "`split(\" \")` breaks the name on the space into a list; index 0 is the first name and "
         "index -1 (the last element) is the surname &mdash; robust even if there's a middle name.")},
 {"q":"You want only the rows of a DataFrame `df` whose `email` column ends in '.edu'. Write the "
      "filter.", "html": True,
  "sol": B.code_example('df[df["email"].str.endswith(".edu")]',
         filename="solution.py", runnable=False) + B.fmt(
         "`df[\"email\"].str.endswith(\".edu\")` builds a boolean mask (True for .edu addresses), "
         "and `df[mask]` keeps those rows &mdash; the text equivalent of the boolean filtering "
         "from Lesson 2.7. Add `na=False` if the column may contain missing values.")},
]))

p.append(B.deepdive(
 B.concept(
  "**Regular expressions: pattern power.** When simple methods aren't enough &mdash; extracting "
  "all phone numbers, validating an email format, pulling the year out of messy text &mdash; you "
  "reach for ~regular expressions~ (regex): a mini-language for describing text patterns. In "
  "pandas, `.str.extract(r'(\\d{4})')` pulls the first 4-digit run from each string, and "
  "`.str.contains(r'^\\d+$')` tests a pattern. Regex is famously cryptic, so use it when plain "
  "methods fall short &mdash; but knowing it exists (and that `.str` speaks it) unlocks serious "
  "text wrangling.") +
 B.concept(
  "**Unicode and encodings.** Text is stored as bytes, and the mapping from bytes to characters "
  "is an ~encoding~ &mdash; almost always ~UTF-8~ today. Trouble appears when a file was saved in "
  "a different encoding (you'll see garbled characters like '&Atilde;&copy;' where '&eacute;' "
  "should be), which you fix by telling the reader the right encoding "
  "(`pd.read_csv(..., encoding=\"latin-1\")`). It's a frequent real-world headache, and Lesson "
  "2.11 returns to it.") +
 B.concept(
  "**Splitting into columns.** `.str.split(sep, expand=True)` returns a **DataFrame** instead of "
  "a column of lists &mdash; perfect for turning 'City, State' into two clean columns in one "
  "step. Combined with `.str.strip()` to tidy the pieces, it's the standard way to parse "
  "semi-structured text (addresses, names, codes) into proper columns you can analyze."),
 title="Deep dive: regular expressions, encodings, and splitting text into columns"))

p.append(B.callout("note","Interview-ready",
 "Take-homes are full of messy text. Show you reach for vectorized `.str` methods rather than "
 "loops, and mention regex (`.str.extract`/`.str.contains`) for pattern extraction. If asked to "
 "parse names, emails, or addresses, narrate split-and-index or `split(expand=True)` into "
 "columns &mdash; and note that strings are immutable, so methods return new values you must "
 "assign.", "&#9670;"))

LESSONS={"py-08-strings":"\n".join(p)}
