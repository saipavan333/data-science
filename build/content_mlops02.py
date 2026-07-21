# -*- coding: utf-8 -*-
import builder as B
import io, contextlib, textwrap
def _run(code):
    code=textwrap.dedent(code).strip("\n"); g={}; buf=io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code+"\n","<ex>","exec"),g)
    return code, buf.getvalue().rstrip("\n")
p=[]
p.append(B.why(
 "You trained a great model &mdash; now how do you **keep** it, **ship** it, and know **which "
 "version** is running when something goes wrong? A model is a trained object that must be "
 "**serialized** to a file, **versioned** so you can reproduce and roll back, and **tracked** "
 "alongside the data and metrics that produced it. Skip this and you'll one day face the nightmare "
 "question &mdash; *\"which model is in production, and can we get the old one back?\"* &mdash; with "
 "no answer."))
p.append(B.h2("Serialization: a trained model is just a file", kicker="Pickle & joblib"))
p.append(B.concept(
 "Training produces an in-memory object full of learned parameters. **Serialization** writes it to "
 "disk so you can load it later without retraining. In Python, **`joblib`** (or `pickle`) is the "
 "standard for scikit-learn models &mdash; `joblib` is faster for the big NumPy arrays models "
 "contain:\n\n"
 "```\nimport joblib\njoblib.dump(pipeline, 'model_v3.joblib')   # save\nmodel = joblib.load('model_v3.joblib')     # load later, no retraining\n```\n\n"
 "Save the **whole pipeline** (preprocessing + model), not just the estimator &mdash; that's what "
 "prevents training&ndash;serving skew."))
p.append(B.warn(
 "**Never unpickle a file you don't trust.** `pickle`/`joblib` can execute arbitrary code on load, "
 "so loading a model file from an untrusted source is a security risk. Also, pickled models are tied "
 "to library **versions** &mdash; a model saved under scikit-learn 1.2 may not load under 1.5. Pin "
 "your environment (Toolkit track) and record the library versions **with** the model, or use a "
 "version-robust format for long-term storage."))
p.append(B.h2("Versioning: code is not enough", kicker="Model + data + metrics"))
p.append(B.concept(
 "Git versions your **code**, but a model's behaviour depends on **three** things: the code, the "
 "**data** it trained on, and the **hyperparameters**. To reproduce or audit a model you must version "
 "all three. That's why teams use:\n\n"
 "- **Experiment tracking** (MLflow, Weights & Biases): logs each run's parameters, metrics, and the "
 "resulting model artifact &mdash; so you can compare runs and reproduce any of them.\n"
 "- **A model registry**: a catalogue of trained models with versions, stages (staging / "
 "production / archived), and lineage &mdash; the single source of truth for *what's deployed*.\n"
 "- **Data versioning** (DVC): pins *which* dataset produced a model, by hash."))
p.append(B.concept(
 "A simple, powerful idea underpins versioning: identify an artifact by a **hash of its content**, "
 "so a given version is unambiguous and tamper-evident. Two identical models hash the same; any "
 "change produces a new id:"))
_c,_o=_run(r'''
import hashlib
# a stand-in for a serialized model's bytes
weights = b"logreg;coef=[0.31,-1.20,0.84];intercept=0.10;sklearn=1.5.0"
version_id = hashlib.md5(weights).hexdigest()[:8]
print("model version id:", version_id, " (changes if ANY byte changes)")
''')
p.append(B.code_example(_c,_o,filename="version_hash.py"))
p.append(B.h2("Your turn — version a model by content hash", kicker="Interactive lab"))
p.append(B.pylab(
 "Give a serialized model a reproducible version id: compute the **MD5 hash** of the `weights` bytes "
 "and take the **first 8 hex characters**, assigning the string to **`answer`**. (Any change to the "
 "bytes must change the id.)",
 "import hashlib\n"
 "weights = b\"logreg;coef=[0.31,-1.20,0.84];intercept=0.10;sklearn=1.5.0\"\n",
 "answer = hashlib.md5(weights).hexdigest()[:8]",
 starter="import hashlib\n# md5 hex digest of `weights`, first 8 characters\nanswer = ",
 hint="`hashlib.md5(weights).hexdigest()` returns the full hex string; slice `[:8]` for the short id.",
 title="Lab — content-hash versioning",
 preview="hashlib is available; `weights` (model bytes) preloaded. First Run boots Python.",
 explain="This 8-char id is deterministic: the same bytes always hash the same, and changing any "
         "byte (a coefficient, the library version) yields a new id. That's the core idea behind "
         "content-addressed versioning &mdash; unambiguous, tamper-evident model identities you can "
         "track and roll back to."))
p.append(B.keypoints([
 "**Serialize** a trained pipeline to a file with **joblib** (or pickle) &mdash; save the *whole* "
 "pipeline, not just the estimator.",
 "**Never unpickle untrusted files** (arbitrary code execution); pickled models are tied to library "
 "**versions** &mdash; record them.",
 "A model = **code + data + hyperparameters**; version **all three** to reproduce or audit it.",
 "Use **experiment tracking** (MLflow/W&B) for runs, a **model registry** for what's deployed, and "
 "**data versioning** (DVC) for which data.",
 "**Content hashing** gives artifacts unambiguous, tamper-evident version ids &mdash; the basis for "
 "reliable rollback.",
]))
p.append(B.quiz([
 {"q":"Production is misbehaving and you need to roll back to last week's model. What must you have "
      "set up to do this cleanly?",
  "options":[
   {"t":"Versioned, registered model artifacts (with the code/data/params that produced them) so you "
        "can redeploy a specific prior version","correct":True,
    "why":"Correct. A model registry with versioned artifacts and lineage lets you identify and "
          "redeploy exactly last week's model, and know how it was built. Without versioning, "
          "'the old model' may be irretrievable."},
   {"t":"A faster server",
    "why":"Rollback is about *which* model is deployed, not speed. You need versioned artifacts to "
          "revert to."},
   {"t":"Only the current model file",
    "why":"If you only kept the latest, the previous version is gone. Rollback requires retained, "
          "versioned artifacts."},
   {"t":"The training notebook",
    "why":"A notebook without pinned data/params/environment may not reproduce the old model. You "
          "need the versioned artifact (and its lineage), not just code."}]},
 {"q":"Why isn't versioning your Git code enough to reproduce a model?",
  "options":[
   {"t":"A model also depends on the training data and hyperparameters, which Git code alone doesn't "
        "capture","correct":True,
    "why":"Correct. Same code + different data or hyperparameters = different model. Reproducibility "
          "needs the data version and run parameters tracked alongside the code &mdash; hence "
          "experiment tracking and data versioning."},
   {"t":"Git can't store Python files",
    "why":"Git stores code fine; the gap is that a model's behaviour also depends on *data* and "
          "*params*, which code versioning doesn't pin."},
   {"t":"It is enough — code fully determines the model",
    "why":"It doesn't: the same training code produces different models on different data or with "
          "different hyperparameters. You must version those too."},
   {"t":"Models can't be reproduced at all",
    "why":"They can &mdash; if you version code, data, params, and environment together. Code alone "
          "is insufficient."}]},
]))
p.append(B.practice([
 {"q":"Your team keeps asking 'which model is in production and how was it trained?' and nobody's "
      "sure. What would you put in place?",
  "sol":"Introduce a **model registry + experiment tracking** as the single source of truth. Every "
        "training run (via MLflow/W&B or similar) logs its **hyperparameters, metrics, environment, "
        "and the data version** used, and outputs a **versioned model artifact**. Promising models "
        "are registered with a **version** and a **stage** (staging &rarr; production &rarr; "
        "archived), so 'what's in production' is a lookup, not a guess, and each version carries its "
        "**lineage** (the code commit, data hash, and params that made it). Add **content-hashed** "
        "artifact ids for tamper-evidence and clean rollback. Now the question answers itself: you "
        "can see exactly which version is live, reproduce it, compare it to alternatives, and revert "
        "safely &mdash; the baseline of a trustworthy ML operation."},
 {"q":"Give two concrete risks of the naive approach 'just pickle the model and email the file "
      "around.'",
  "sol":"**(1) Security:** unpickling executes arbitrary code, so a model file from an untrusted or "
        "tampered source can compromise the machine that loads it &mdash; emailing artifacts around "
        "invites this. **(2) Version fragility & ambiguity:** a pickle is tied to the exact library "
        "versions used to create it (a scikit-learn upgrade can make it fail to load), and an emailed "
        "file has **no version, no lineage, and no source of truth** &mdash; you can't tell which "
        "file is 'the' production model, how it was trained, or how to reproduce/roll back. Bonus "
        "risks: no access control, easy to lose, and preprocessing may be separated from the model. "
        "The fix is a registry with pinned environments and versioned, hashed artifacts."},
]))
p.append(B.deepdive(
 B.concept(
  "**Serialization formats beyond pickle.** Pickle/joblib are convenient but Python- and "
  "version-specific and unsafe to load from untrusted sources. For **portability and safety**, "
  "interchange formats exist: **ONNX** represents many models in a framework-neutral graph so they "
  "can run in other languages/runtimes and are less tied to a library version; **PMML** is an older "
  "XML standard for classic models; and framework-native formats (TensorFlow SavedModel, PyTorch's "
  "`state_dict`) are preferred for deep nets. For long-lived or cross-team models, an interchange "
  "format plus recorded library versions beats a bare pickle. Match the format to how long the model "
  "must live and where it must run.") +
 B.concept(
  "**A registry turns models into governed assets.** Beyond storing files, a model registry adds the "
  "**governance** production needs: stage transitions with approvals (who promoted this to "
  "production?), lineage (which run, data, and commit produced it), annotations (known limitations, "
  "intended use), and an audit trail. In regulated domains this isn't optional &mdash; you must be "
  "able to show *exactly* what model made a decision and how it was built. Even in unregulated ones, "
  "it's the difference between calmly rolling back a bad release and a frantic 3 a.m. hunt for a lost "
  "`.pkl`. Treat trained models with the same seriousness as production code: versioned, reviewed, "
  "and traceable."),
 title="Deep dive: portable formats (ONNX/PMML) and registries as model governance"))
LESSONS={"mlops-02-serialize":"\n".join(x for x in p if x)}
print("content_mlops02 OK — chars:", len(LESSONS["mlops-02-serialize"]))
