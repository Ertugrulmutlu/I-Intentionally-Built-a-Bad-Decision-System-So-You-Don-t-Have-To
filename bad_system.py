# bad_system.py
# I Intentionally Built a Bad AI System (So You Don’t Have To)
# This is intentionally full of anti-patterns.

import random
import time
import os

import global_state as GS


# ---- Anti-pattern: side-effects everywhere + hidden IO ----
def extract_keywords(text):
    print("[extract] extracting keywords...")  # side-effect (printing)
    os.makedirs("tmp", exist_ok=True)         # side-effect (filesystem)
    with open("tmp/log.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")                  # side-effect (logging raw input)

    # "keyword extraction" = nonsense heuristic + magic numbers
    tokens = text.replace(",", " ").replace(".", " ").split()
    if len(tokens) == 0:
        return ["EMPTY"]  # hidden contract

    # magic numbers: 3, 17
    k = 3 if len(tokens) > 17 else 2
    return tokens[:k]


# ---- Anti-pattern: implicit coupling to global state + random behavior ----
def score_keywords(keywords):
    GS.RUN_COUNT += 1  # global state mutation (not thread-safe)
    base = 0

    # magic numbers: 7, 13
    for w in keywords:
        base += (len(w) % 7)

    # hidden dependency: uses LAST_TEXT length if present
    if GS.LAST_TEXT is not None:
        base += (len(GS.LAST_TEXT) % 13)

    # random jitter (non-deterministic)
    base += random.randint(0, 2)

    GS.CURRENT_SCORE += base  # global accumulation (drifts forever)
    return GS.CURRENT_SCORE


# ---- Anti-pattern: recommendation depends on unrelated global state ----
def recommend_action(keywords, score):
    # hidden coupling: compares score with keyword count in a weird way
    if (score % 5) == len(keywords):  # magic number: 5
        action = "BUY_MORE_STOCK"
    elif score > 42:                  # magic number: 42 (lol)
        action = "PANIC_REORDER"
    else:
        action = "WAIT_AND_SEE"

    # side-effect: write action to file
    with open("tmp/action.txt", "w", encoding="utf-8") as f:
        f.write(action)

    GS.LAST_ACTION = action
    return action


# ---- Anti-pattern: orchestration mixes timing, IO, state, logic ----
def pipeline(text):
    GS.LAST_TEXT = text  # global state set

    # fake latency to look "real"
    time.sleep(0.05)     # magic number delay

    keywords = extract_keywords(text)
    GS.LAST_KEYWORDS = keywords  # global state set

    score = score_keywords(keywords)
    action = recommend_action(keywords, score)

    # side-effect: print "report"
    print("\n=== BAD REPORT ===")
    print("text_len:", len(text))
    print("run_count:", GS.RUN_COUNT)
    print("keywords:", keywords)
    print("score:", score)
    print("action:", action)
    print("==============\n")

    # returns inconsistent structure (sometimes helpful, sometimes not)
    return {
        "keywords": keywords,
        "score": score,
        "action": action,
        "note": "This system is intentionally bad."
    }


def demo():
    print("Running the intentionally bad system...\n")

    samples = [
        "Trend XYZ is going viral on TikTok: chunky sneakers, metallic laces, bright outsole.",
        "Quiet luxury is fading; loud logos are back with neon accents.",
        "Berlin winter fit: long coats, muted colors, but bold sneakers.",
        "",
    ]

    for t in samples:
        pipeline(t)

    print("Try running pipeline() twice with same input: you'll still get different outputs.\n")
    print("Now run this file multiple times. Your results will drift due to global accumulation.\n")


if __name__ == "__main__":
    demo()
