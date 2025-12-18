# good_system.py
# A small, boring, debuggable, testable version of the same pipeline.

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Dict, Any
import re
import time


# -----------------------------
# Configuration (no magic nums)
# -----------------------------
@dataclass(frozen=True)
class PipelineConfig:
    max_keywords_short: int = 2
    max_keywords_long: int = 3
    long_text_token_threshold: int = 17

    mod_base: int = 7
    extra_mod_from_text_len: int = 13

    action_mod: int = 5
    buy_more_stock_rule_value: int = 0  # (score % action_mod) == len(keywords) -> BUY
    panic_reorder_threshold: int = 42

    simulate_latency_sec: float = 0.05  # still explicit


# -----------------------------
# Small utilities (pure)
# -----------------------------
def tokenize(text: str) -> List[str]:
    # Keep it deterministic and simple
    text = text.strip().lower()
    if not text:
        return []
    # Words only, drop punctuation deterministically
    return re.findall(r"[a-z0-9]+", text)


def extract_keywords(text: str, cfg: PipelineConfig) -> List[str]:
    tokens = tokenize(text)
    if not tokens:
        return ["empty"]

    k = cfg.max_keywords_long if len(tokens) > cfg.long_text_token_threshold else cfg.max_keywords_short
    return tokens[:k]


def score_keywords(keywords: List[str], text: str, cfg: PipelineConfig) -> int:
    # No randomness, no hidden dependencies
    base = sum((len(w) % cfg.mod_base) for w in keywords)
    base += (len(text) % cfg.extra_mod_from_text_len)
    return base


def recommend_action(keywords: List[str], score: int, cfg: PipelineConfig) -> str:
    if (score % cfg.action_mod) == len(keywords):
        return "BUY_MORE_STOCK"
    if score > cfg.panic_reorder_threshold:
        return "PANIC_REORDER"
    return "WAIT_AND_SEE"


# -----------------------------
# Orchestration (side-effects outside)
# -----------------------------
@dataclass(frozen=True)
class PipelineResult:
    keywords: List[str]
    score: int
    action: str
    meta: Dict[str, Any]


def run_pipeline(
    text: str,
    cfg: PipelineConfig,
    clock: Callable[[], float] | None = None,
) -> PipelineResult:
    # Optional latency simulation (explicit + injectable clock if you want)
    if cfg.simulate_latency_sec > 0:
        time.sleep(cfg.simulate_latency_sec)

    keywords = extract_keywords(text, cfg)
    score = score_keywords(keywords, text, cfg)
    action = recommend_action(keywords, score, cfg)

    return PipelineResult(
        keywords=keywords,
        score=score,
        action=action,
        meta={
            "text_len": len(text),
            "token_count": len(tokenize(text)),
            "note": "This system is intentionally boring and maintainable.",
        },
    )


def demo():
    cfg = PipelineConfig()

    samples = [
        "Trend XYZ is going viral on TikTok: chunky sneakers, metallic laces, bright outsole.",
        "Quiet luxury is fading; loud logos are back with neon accents.",
        "Berlin winter fit: long coats, muted colors, but bold sneakers.",
        "",
    ]

    print("Running the GOOD system (deterministic)...\n")
    for t in samples:
        res = run_pipeline(t, cfg)
        print("=== GOOD REPORT ===")
        print("keywords:", res.keywords)
        print("score:", res.score)
        print("action:", res.action)
        print("meta:", res.meta)
        print("===============\n")

    print("Run it twice with the same input: you should get the same output every time.\n")


if __name__ == "__main__":
    demo()
