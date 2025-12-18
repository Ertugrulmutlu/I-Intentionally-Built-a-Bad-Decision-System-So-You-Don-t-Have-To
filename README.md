# Intentionally Bad vs Good Decision System

This repository demonstrates how **system design choices** — not models — can cause AI and decision-making pipelines to fail *silently*.

It contains two implementations of the **same task**:

> Input text → keyword extraction → scoring → action recommendation

One version is intentionally broken. The other is boring, deterministic, and maintainable.

---

## Why this exists

Most failures in AI systems are not caused by bad models, but by:

* hidden state
* non-determinism
* uncontrolled side-effects
* implicit coupling

This repo shows how those issues appear in practice — even when the code "works".

---

## Repository structure

```text
.
├── bad_system.py     # intentionally broken implementation (anti-patterns)
├── good_system.py    # deterministic and testable implementation
├── compare.py        # tiny benchmark: same input, repeated runs
└── README.md
```

---

## How to run

```bash
python compare.py
```

This runs the same input multiple times through both systems and prints a short benchmark comparing:

* output stability
* score drift
* action consistency

---

## What to look for

* **BAD system:** same input → different outputs over time
* **GOOD system:** same input → same output every run

The point is not performance, but **predictability and debuggability**.

---

## Related article

📖 Full explanation, benchmark analysis, and failure taxonomy:
👉 [https://dev.to/YOUR_USERNAME/YOUR_POST_SLUG](https://dev.to/YOUR_USERNAME/YOUR_POST_SLUG)

---

## Warning

The bad system is broken **by design**. Do not copy its architecture into production code.
