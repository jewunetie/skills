#!/usr/bin/env python3
"""
run_inference.py -- Load Qwen 3.5 0.8B and run inference on one or more prompts.

Usage:
    # Single prompt
    python run_inference.py --prompt "What is 23 + 47?"

    # Single prompt with options
    python run_inference.py --prompt "Write a haiku" --max-new-tokens 60 --do-sample --temperature 0.8

    # Batch from JSON file (array of {"prompt": "...", "max_new_tokens": N (optional)})
    python run_inference.py --batch-file prompts.json

    # Save output to file
    python run_inference.py --prompt "Hello" --output-path /mnt/user-data/outputs/result.json
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import gc
import json
import sys
import argparse
import os

MODEL_ID = "Qwen/Qwen3.5-0.8B"
DEFAULT_MAX_NEW_TOKENS = 80


def load_model():
    """Load model and tokenizer. Uses bfloat16 to stay within 9 GB RAM."""
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


def generate(model, tokenizer, prompt, max_new_tokens=DEFAULT_MAX_NEW_TOKENS,
             temperature=1.0, do_sample=False):
    """Generate a response for a single prompt. Returns a result dict."""
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt")

    t0 = time.time()
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature if do_sample else 1.0,
        )
    elapsed = time.time() - t0

    new_toks = output.shape[1] - inputs["input_ids"].shape[1]
    response = tokenizer.decode(
        output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
    )

    return {
        "prompt": prompt,
        "response": response,
        "tokens_generated": new_toks,
        "elapsed_seconds": round(elapsed, 1),
        "tokens_per_second": round(new_toks / elapsed, 2) if elapsed > 0 else 0,
        "max_new_tokens": max_new_tokens,
        "temperature": temperature,
        "do_sample": do_sample,
    }


def main():
    parser = argparse.ArgumentParser(description="Run Qwen 3.5 0.8B inference")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", type=str, help="Single prompt to run")
    group.add_argument("--batch-file", type=str, help="Path to JSON file with array of prompt objects")
    parser.add_argument("--max-new-tokens", type=int, default=DEFAULT_MAX_NEW_TOKENS,
                        help=f"Max tokens to generate (default: {DEFAULT_MAX_NEW_TOKENS})")
    parser.add_argument("--temperature", type=float, default=1.0,
                        help="Sampling temperature (default: 1.0)")
    parser.add_argument("--do-sample", action="store_true",
                        help="Enable sampling (default: greedy decoding)")
    parser.add_argument("--output-path", type=str, default=None,
                        help="Path to save JSON results")

    args = parser.parse_args()

    # Build prompt list
    is_batch = args.batch_file is not None
    prompts = []
    if args.prompt:
        prompts.append({"prompt": args.prompt})
    else:
        with open(args.batch_file, "r") as f:
            prompts = json.load(f)
        if not isinstance(prompts, list):
            print("ERROR: Batch file must contain a JSON array of objects.", file=sys.stderr)
            sys.exit(1)
        for idx, item in enumerate(prompts):
            if not isinstance(item, dict) or "prompt" not in item:
                print(f"ERROR: Batch item {idx} must be an object with a \"prompt\" field.",
                      file=sys.stderr)
                sys.exit(1)

    # Load model once
    model, tokenizer = load_model()

    # Run inference
    results = []
    for i, item in enumerate(prompts):
        prompt_text = item["prompt"]
        max_tok = item.get("max_new_tokens", args.max_new_tokens)
        temp = item.get("temperature", args.temperature)
        sample = item.get("do_sample", args.do_sample)

        print(f"\n--- Prompt {i + 1}/{len(prompts)} ---", file=sys.stderr)
        print(f"  {prompt_text[:80]}{'...' if len(prompt_text) > 80 else ''}", file=sys.stderr)

        result = generate(model, tokenizer, prompt_text,
                          max_new_tokens=max_tok, temperature=temp, do_sample=sample)
        results.append(result)

        print(f"  {result['tokens_generated']} tokens in {result['elapsed_seconds']}s "
              f"({result['tokens_per_second']} tok/s)", file=sys.stderr)

    # Output: single prompt -> object, batch -> always array (even if 1 item)
    output = results if is_batch else results[0]
    output_json = json.dumps(output, indent=2, ensure_ascii=False)
    print(output_json)

    if args.output_path:
        os.makedirs(os.path.dirname(args.output_path) or ".", exist_ok=True)
        with open(args.output_path, "w") as f:
            f.write(output_json)
        print(f"\nResults saved to {args.output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
