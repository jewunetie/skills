---
name: qwen-800m
description: Run the Qwen 3.5 0.8B language model locally in the Claude sandbox for inference and experimentation. Use this skill whenever the user asks to run Qwen locally, test a prompt on Qwen, run a small LLM, benchmark a small model, compare Claude's response to Qwen's, test Qwen 3.5 0.8B, run inference on a local model, experiment with a tiny language model, or any request involving running, testing, or benchmarking Qwen or small language models in the sandbox. Also trigger when the user wants to study calibration, hallucination, or reasoning differences between a small model and Claude, or asks "what would a small model say about this." Even casual mentions of "run Qwen" or "test on Qwen" should trigger this skill.
---

# Run Qwen 3.5 0.8B Locally

Run the Qwen 3.5 0.8B (752M parameter) language model directly in the Claude sandbox for interactive inference, prompt testing, benchmarking, and research experiments.

## Sandbox Constraints (Hard Limits)

These are validated through testing and are non-negotiable:

- **CPU only.** No GPU. `nvidia-smi` returns nothing.
- **9 GB RAM total.** The model at bfloat16 uses about 3 GB resident. Float32 will OOM and crash the container. **Never use float32.**
- **10 GB disk total.** CPU-only PyTorch + transformers + model weights consume about 5-6 GB. Do not install large additional packages.
- **2 vCPUs.** Generation speed is approximately 2.6 tokens/second. Budget time accordingly.
- **Container resets between tasks.** Dependencies and model weights must be re-downloaded each session. The setup script handles this.

## Token Budget Guidance

At 2.6 tok/s, generation time scales linearly:

| max_new_tokens | Approximate wall time |
|---|---|
| 40 | ~15 seconds |
| 60 | ~23 seconds |
| 80 | ~31 seconds |
| 120 | ~46 seconds |
| 200 | ~77 seconds |

Default to 80 tokens for single prompts, 60 for benchmark runs. The user can override.

## Setup (Run Once Per Session)

Before any inference, run the setup script. All script paths below are relative to this skill's installed directory (e.g., `/mnt/skills/user/qwen-800m/`). Resolve them to absolute paths before executing.

```bash
bash scripts/setup.sh
```

This installs CPU-only PyTorch, transformers, and accelerate, and verifies disk/RAM headroom. Takes 2-4 minutes depending on network speed. Watch for the "Setup complete" message before proceeding.

## Usage Modes

### Mode 1: Single Prompt

The user provides a prompt. Run it through Qwen and show the response with timing stats.

```bash
python scripts/run_inference.py --prompt "What is the capital of France?"
```

Optional flags: `--max-new-tokens 120`, `--temperature 0.7`, `--do-sample`

Present the output to the user showing: the response text, tokens generated, elapsed time, and tokens/second.

### Mode 2: Prompt Comparison

The user provides a prompt. Show both Claude's response and Qwen 0.8B's response so the user can compare.

1. First, answer the prompt yourself (as Claude) and hold the response.
2. Run the prompt through Qwen using Mode 1.
3. Present both responses side by side, clearly labeled.

### Mode 3: Benchmark Suite

Run the predefined benchmark across categories:

```bash
python scripts/run_benchmark.py
```

Optional flags: `--max-new-tokens 80`, `--output-path /mnt/user-data/outputs/benchmark_results.json`

This runs 14 prompts across 7 categories and outputs a structured summary with per-prompt scoring. Results go to both stdout and a JSON file.

### Mode 4: Custom Batch

The user provides a JSON file or a list of prompts. Run all of them:

```bash
python scripts/run_inference.py --batch-file /path/to/prompts.json
```

The batch file should be a JSON array of objects with at least a `"prompt"` field. Optional per-prompt `"max_new_tokens"` overrides are supported.

Output is a JSON array of results written to stdout and optionally to a file via `--output-path`.

## Known Model Behaviors

These observations come from validated testing and are useful context when interpreting results:

1. **Math:** Correctly handles simple arithmetic and some multi-step problems. Breaks problems into steps unprompted. Reasoning post-training would help most here.
2. **Logic:** Can identify set-theoretic structure in syllogisms. Often building toward correct conclusions but may hit token limits.
3. **Knowledge gaps:** Confidently states wrong answers with zero uncertainty (e.g., claims Yangon is the capital of Myanmar). This is a calibration problem, not a knowledge problem per se.
4. **Speed:** Consistent 2.6 tok/s on sandbox CPU across all prompt types.
5. **Harmless warnings:** The `pad_token_id` warning and the "fast path not available" warning appear every time and are safe to ignore. Do not try to suppress them.

## Workflow

For every invocation of this skill:

1. **Check if setup has been run this session.** If not, run `setup.sh` first.
2. **Run the appropriate script** based on the usage mode.
3. **Always show timing stats** (tokens generated, elapsed seconds, tokens/second). This is research context.
4. **For benchmark mode**, present results as a formatted table in the response AND save the JSON file.
5. **For comparison mode**, clearly label which response is Claude's and which is Qwen's. Do not editorialize unless the user asks for analysis.
