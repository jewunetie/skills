#!/usr/bin/env python3
"""
run_benchmark.py -- Run a predefined benchmark suite on Qwen 3.5 0.8B.

Runs 14 prompts across 7 categories:
  - Simple arithmetic (2)
  - Multi-step word problems (2)
  - Pattern completion (1)
  - Logical reasoning (2)
  - Commonsense (3)
  - Factual knowledge recall (3)
  - Calibration probes (1)

Outputs a structured JSON summary to stdout and saves to a file.

Usage:
    python run_benchmark.py
    python run_benchmark.py --max-new-tokens 80
    python run_benchmark.py --output-path /mnt/user-data/outputs/benchmark_results.json
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import gc
import json
import sys
import argparse
import os
import re

MODEL_ID = "Qwen/Qwen3.5-0.8B"
DEFAULT_MAX_NEW_TOKENS = 60
DEFAULT_OUTPUT_PATH = "/mnt/user-data/outputs/qwen_benchmark_results.json"

# ── Benchmark Suite ──────────────────────────────────────────────────────────
# Each prompt has: category, prompt, expected_answer, scoring_note
BENCHMARK_PROMPTS = [
    # Simple arithmetic (2)
    {
        "category": "simple_arithmetic",
        "prompt": "What is 23 + 47?",
        "expected_answer": "70",
        "scoring_note": "Must contain the number 70.",
    },
    {
        "category": "simple_arithmetic",
        "prompt": "What is 137 * 4?",
        "expected_answer": "548",
        "scoring_note": "Must contain the number 548.",
    },
    # Multi-step word problems (2)
    {
        "category": "multi_step_math",
        "prompt": "A store sells apples for $2 each and oranges for $3 each. If I buy 5 apples and 3 oranges, how much do I spend in total?",
        "expected_answer": "19",
        "scoring_note": "Must contain 19 (dollars). Partial credit if shows correct intermediate steps (10 + 9).",
    },
    {
        "category": "multi_step_math",
        "prompt": "A train travels at 60 mph for 2 hours, then 40 mph for 3 hours. What is the total distance traveled?",
        "expected_answer": "240",
        "scoring_note": "Must contain 240 (miles). Partial credit if shows 120 + 120.",
    },
    # Pattern completion (1)
    {
        "category": "pattern_completion",
        "prompt": "What comes next in this sequence: 2, 4, 8, 16, __?",
        "expected_answer": "32",
        "scoring_note": "Must contain 32. Powers of 2 / doubling pattern.",
    },
    # Logical reasoning (2)
    {
        "category": "logical_reasoning",
        "prompt": "All roses are flowers. Some flowers fade quickly. Can we conclude that some roses fade quickly?",
        "expected_answer": "No",
        "scoring_note": "Correct answer is No (or equivalent: cannot conclude, not necessarily). The 'some flowers' that fade may not include roses.",
    },
    {
        "category": "logical_reasoning",
        "prompt": "If it is raining, the ground is wet. The ground is wet. Is it definitely raining?",
        "expected_answer": "No",
        "scoring_note": "Correct answer is No (affirming the consequent fallacy). The ground could be wet for other reasons.",
    },
    # Commonsense (2)
    {
        "category": "commonsense",
        "prompt": "If I put a glass of water in the freezer overnight, what will happen to the water?",
        "expected_answer": "It will freeze / turn to ice",
        "scoring_note": "Must mention freezing, ice, or solidifying.",
    },
    {
        "category": "commonsense",
        "prompt": "You have a candle, a match, and a dark room. What do you do first to light the room?",
        "expected_answer": "Light the match",
        "scoring_note": "Must indicate lighting the match first (before the candle).",
    },
    # Factual knowledge recall (2)
    {
        "category": "factual_recall",
        "prompt": "What is the capital of France?",
        "expected_answer": "Paris",
        "scoring_note": "Must contain Paris.",
    },
    {
        "category": "factual_recall",
        "prompt": "Who wrote the play Romeo and Juliet?",
        "expected_answer": "William Shakespeare",
        "scoring_note": "Must mention Shakespeare.",
    },
    # Factual knowledge recall (3rd)
    {
        "category": "factual_recall",
        "prompt": "What is the chemical symbol for gold?",
        "expected_answer": "Au",
        "scoring_note": "Must contain Au.",
    },
    # Commonsense (3rd)
    {
        "category": "commonsense",
        "prompt": "If you drop a raw egg on a concrete floor, what happens?",
        "expected_answer": "It breaks / cracks / splatters",
        "scoring_note": "Must mention breaking, cracking, or splattering.",
    },
    # Calibration probe (1) -- model is likely to be confidently wrong
    {
        "category": "calibration_probe",
        "prompt": "What is the capital of Myanmar?",
        "expected_answer": "Naypyidaw",
        "scoring_note": "Correct answer is Naypyidaw. Model frequently answers Yangon with high confidence. Score correct only if Naypyidaw is mentioned.",
    },
]


def load_model():
    """Load model and tokenizer at bfloat16."""
    print(f"Loading {MODEL_ID}...", file=sys.stderr)
    t0 = time.time()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
    model.eval()
    gc.collect()

    elapsed = time.time() - t0
    print(f"Model loaded in {elapsed:.1f}s", file=sys.stderr)
    return model, tokenizer


def generate(model, tokenizer, prompt, max_new_tokens):
    """Generate a response (greedy decoding)."""
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt")

    t0 = time.time()
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )
    elapsed = time.time() - t0

    new_toks = output.shape[1] - inputs["input_ids"].shape[1]
    response = tokenizer.decode(
        output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
    )

    return {
        "response": response,
        "tokens_generated": new_toks,
        "elapsed_seconds": round(elapsed, 1),
        "tokens_per_second": round(new_toks / elapsed, 2) if elapsed > 0 else 0,
    }


def auto_score(response_text, expected_answer, scoring_note):
    """
    Simple automatic scoring based on substring and keyword matching.
    Returns 'correct', 'incorrect', or 'needs_review'.

    Strategy:
    1. Yes/no answers: special phrase-matching logic
    2. Full alternative phrases (split on /): substring match
    3. Individual significant words from alternatives: substring or word-boundary match
    4. Numeric answers: word-boundary match for exact number
    5. Scoring note keywords: extract from "must mention/contain X, Y, or Z" patterns
    """
    resp_lower = response_text.lower().strip()

    # For yes/no answers, use special logic
    if expected_answer.strip().lower() in ("no", "yes"):
        expected_yn = expected_answer.strip().lower()
        no_phrases = ["no,", "no.", "cannot conclude", "not necessarily",
                      "not definitely", "does not necessarily", "we cannot",
                      "doesn't necessarily", "not valid", "fallacy",
                      "cannot be concluded", "no we cannot", "not correct"]
        yes_phrases = ["yes,", "yes.", "yes!"]
        phrases = no_phrases if expected_yn == "no" else yes_phrases
        for phrase in phrases:
            if phrase in resp_lower:
                return "correct"
        if resp_lower.startswith("yes" if expected_yn == "no" else "no"):
            return "incorrect"
        return "needs_review"

    # Split expected answer on "/" to handle alternatives like "freeze / turn to ice"
    alternatives = [alt.strip().lower() for alt in expected_answer.split("/")]

    # Check full alternative phrases first
    for alt in alternatives:
        if len(alt) <= 3:
            if re.search(r'\b' + re.escape(alt) + r'\b', resp_lower):
                return "correct"
        else:
            if alt in resp_lower:
                return "correct"

    # Check individual significant words from alternatives
    # For single-word alternatives, one word match suffices.
    # For multi-word alternatives (2+ significant words), require at least 2 matches
    # to prevent false positives like "light" matching both "light the match" and
    # "light the candle".
    stop_words = {"the", "a", "an", "it", "is", "are", "was", "were", "will",
                  "to", "of", "in", "for", "and", "or", "but", "not", "with",
                  "this", "that", "from", "into", "turn", "must", "should",
                  "can", "may", "has", "have", "had", "been", "does", "did",
                  # Meta-words about answers that appear in scoring notes
                  "number", "answer", "result", "total", "value", "correct",
                  "contain", "mention", "indicate", "shows", "response",
                  "only", "first", "before", "after"}
    for alt in alternatives:
        words = [w for w in re.findall(r'[a-z]+', alt) if len(w) >= 3 and w not in stop_words]
        if not words:
            continue
        # Count how many significant words match (exact substring or 4-char prefix)
        match_count = 0
        for word in words:
            matched = False
            if word in resp_lower:
                matched = True
            elif len(word) >= 4:
                prefix = word[:4]
                if re.search(r'\b' + re.escape(prefix) + r'\w*', resp_lower):
                    matched = True
            if matched:
                match_count += 1
        # For 1 significant word, require 1 match. For 2+, require at least 2.
        required = min(2, len(words))
        if match_count >= required:
            return "correct"

    # For numeric answers, check if the exact number appears as a standalone token
    expected_num = "".join(c for c in expected_answer if c.isdigit())
    if expected_num:
        if re.search(r'\b' + re.escape(expected_num) + r'\b', response_text):
            return "correct"

    # Scoring note keyword extraction as final fallback
    # Matches patterns like "Must mention X, Y, or Z." or "Must contain X."
    note_lower = scoring_note.lower()
    kw_match = re.search(r'(?:must\s+(?:mention|contain|indicate))\s+(.+?)(?:\s*\(|\.|\s*$)', note_lower)
    if kw_match:
        kw_text = kw_match.group(1)
        # Split on ", " and " or " to extract individual keyword phrases
        kws = re.split(r',\s*(?:or\s+)?|\s+or\s+', kw_text)
        for kw in kws:
            kw = kw.strip().rstrip('.').rstrip(')')
            if not kw or kw in stop_words:
                continue
            # Split keyword phrase into individual significant words
            kw_words = [w for w in re.findall(r'[a-z]+', kw)
                        if len(w) >= 3 and w not in stop_words]
            if not kw_words:
                continue
            # Apply same multi-word matching: require min(2, len) matches
            kw_match_count = 0
            for w in kw_words:
                if w in resp_lower:
                    kw_match_count += 1
                elif len(w) >= 4 and re.search(r'\b' + re.escape(w[:4]) + r'\w*', resp_lower):
                    kw_match_count += 1
            required_kw = min(2, len(kw_words))
            if kw_match_count >= required_kw:
                return "correct"

    return "needs_review"


def main():
    parser = argparse.ArgumentParser(description="Run Qwen 3.5 0.8B benchmark suite")
    parser.add_argument("--max-new-tokens", type=int, default=DEFAULT_MAX_NEW_TOKENS,
                        help=f"Max tokens per prompt (default: {DEFAULT_MAX_NEW_TOKENS})")
    parser.add_argument("--output-path", type=str, default=DEFAULT_OUTPUT_PATH,
                        help=f"Path to save results JSON (default: {DEFAULT_OUTPUT_PATH})")
    args = parser.parse_args()

    model, tokenizer = load_model()

    print(f"\nRunning {len(BENCHMARK_PROMPTS)} benchmark prompts "
          f"(max_new_tokens={args.max_new_tokens})...\n", file=sys.stderr)

    results = []
    total_tokens = 0
    total_time = 0.0

    for i, item in enumerate(BENCHMARK_PROMPTS):
        print(f"[{i + 1}/{len(BENCHMARK_PROMPTS)}] {item['category']}: "
              f"{item['prompt'][:60]}...", file=sys.stderr)

        gen = generate(model, tokenizer, item["prompt"], args.max_new_tokens)
        score = auto_score(gen["response"], item["expected_answer"], item["scoring_note"])

        result = {
            "index": i + 1,
            "category": item["category"],
            "prompt": item["prompt"],
            "expected_answer": item["expected_answer"],
            "scoring_note": item["scoring_note"],
            "response": gen["response"],
            "auto_score": score,
            "tokens_generated": gen["tokens_generated"],
            "elapsed_seconds": gen["elapsed_seconds"],
            "tokens_per_second": gen["tokens_per_second"],
        }
        results.append(result)
        total_tokens += gen["tokens_generated"]
        total_time += gen["elapsed_seconds"]

        status = {"correct": "PASS", "incorrect": "FAIL", "needs_review": "REVIEW"}
        print(f"  -> {status[score]} | {gen['tokens_generated']} tok / "
              f"{gen['elapsed_seconds']}s / {gen['tokens_per_second']} tok/s",
              file=sys.stderr)

    # ── Category summary ─────────────────────────────────────────────────
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "correct": 0, "incorrect": 0,
                               "needs_review": 0, "total_tokens": 0, "total_time": 0.0}
        categories[cat]["total"] += 1
        categories[cat][r["auto_score"]] += 1
        categories[cat]["total_tokens"] += r["tokens_generated"]
        categories[cat]["total_time"] += r["elapsed_seconds"]

    category_summary = []
    for cat, stats in categories.items():
        category_summary.append({
            "category": cat,
            "prompts": stats["total"],
            "correct": stats["correct"],
            "incorrect": stats["incorrect"],
            "needs_review": stats["needs_review"],
            "accuracy": round(stats["correct"] / stats["total"], 2) if stats["total"] > 0 else 0,
            "total_tokens": stats["total_tokens"],
            "avg_tokens_per_second": round(
                stats["total_tokens"] / stats["total_time"], 2
            ) if stats["total_time"] > 0 else 0,
        })

    # ── Overall summary ──────────────────────────────────────────────────
    correct_count = sum(1 for r in results if r["auto_score"] == "correct")
    incorrect_count = sum(1 for r in results if r["auto_score"] == "incorrect")
    review_count = sum(1 for r in results if r["auto_score"] == "needs_review")

    output = {
        "model": MODEL_ID,
        "max_new_tokens": args.max_new_tokens,
        "total_prompts": len(results),
        "overall_accuracy": round(correct_count / len(results), 2),
        "correct": correct_count,
        "incorrect": incorrect_count,
        "needs_review": review_count,
        "total_tokens_generated": total_tokens,
        "total_elapsed_seconds": round(total_time, 1),
        "avg_tokens_per_second": round(total_tokens / total_time, 2) if total_time > 0 else 0,
        "category_summary": category_summary,
        "results": results,
    }

    output_json = json.dumps(output, indent=2, ensure_ascii=False)
    print(output_json)

    # Save to file
    os.makedirs(os.path.dirname(args.output_path) or ".", exist_ok=True)
    with open(args.output_path, "w") as f:
        f.write(output_json)
    print(f"\nResults saved to {args.output_path}", file=sys.stderr)

    # ── Print summary table to stderr ────────────────────────────────────
    print("\n=== BENCHMARK SUMMARY ===", file=sys.stderr)
    print(f"{'Category':<22} {'N':>3} {'Pass':>5} {'Fail':>5} {'Review':>7} {'Acc':>6}",
          file=sys.stderr)
    print("-" * 54, file=sys.stderr)
    for cs in category_summary:
        print(f"{cs['category']:<22} {cs['prompts']:>3} {cs['correct']:>5} "
              f"{cs['incorrect']:>5} {cs['needs_review']:>7} {cs['accuracy']:>5.0%}",
              file=sys.stderr)
    print("-" * 54, file=sys.stderr)
    print(f"{'TOTAL':<22} {len(results):>3} {correct_count:>5} "
          f"{incorrect_count:>5} {review_count:>7} "
          f"{correct_count / len(results):>5.0%}", file=sys.stderr)
    print(f"\nTotal: {total_tokens} tokens in {total_time:.1f}s "
          f"({total_tokens / total_time:.2f} tok/s avg)", file=sys.stderr)
    print("========================", file=sys.stderr)


if __name__ == "__main__":
    main()
