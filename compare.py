# compare.py
# Side-by-side comparison + micro-benchmark
# BAD vs GOOD system

import time
from collections import Counter

import bad_system
import good_system


TEXT = "Trend XYZ is going viral on TikTok: chunky sneakers, metallic laces, bright outsole."
RUNS = 5


def run_bad(n: int):
    results = []
    start = time.perf_counter()

    for _ in range(n):
        out = bad_system.pipeline(TEXT)
        results.append(out)

    duration = time.perf_counter() - start
    return results, duration


def run_good(n: int):
    cfg = good_system.PipelineConfig()
    results = []
    start = time.perf_counter()

    for _ in range(n):
        out = good_system.run_pipeline(TEXT, cfg)
        results.append(out)

    duration = time.perf_counter() - start
    return results, duration


def summarize_bad(results):
    scores = [r["score"] for r in results]
    actions = [r["action"] for r in results]

    return {
        "unique_scores": len(set(scores)),
        "score_values": scores,
        "unique_actions": len(set(actions)),
        "action_counts": dict(Counter(actions)),
    }


def summarize_good(results):
    scores = [r.score for r in results]
    actions = [r.action for r in results]

    return {
        "unique_scores": len(set(scores)),
        "score_values": scores,
        "unique_actions": len(set(actions)),
        "action_counts": dict(Counter(actions)),
    }


def print_report(title, summary, duration):
    print(f"\n=== {title} ===")
    print(f"runs: {RUNS}")
    print(f"time: {duration:.4f} sec")
    print("unique_scores:", summary["unique_scores"])
    print("scores:", summary["score_values"])
    print("unique_actions:", summary["unique_actions"])
    print("action_counts:", summary["action_counts"])
    print("========================")


def main():
    print("\nComparing BAD vs GOOD system on the same input...\n")

    bad_results, bad_time = run_bad(RUNS)
    good_results, good_time = run_good(RUNS)

    bad_summary = summarize_bad(bad_results)
    good_summary = summarize_good(good_results)

    print_report("BAD SYSTEM", bad_summary, bad_time)
    print_report("GOOD SYSTEM", good_summary, good_time)

    print("\nInterpretation:")
    print("- BAD system shows score drift and/or action instability.")
    print("- GOOD system is deterministic: same input -> same output.")
    print("- Time difference is irrelevant here; predictability is the point.\n")


if __name__ == "__main__":
    main()
