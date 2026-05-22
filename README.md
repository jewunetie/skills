# skills

A personal Claude Code plugin containing 18 specialized skills for research, reasoning, writing, design, and development workflows.

## Installation

**Claude Code:**
```bash
/plugin marketplace add jewunetie/skills
/plugin install skills@jewun-skills
```

**OpenAI Codex:**
```bash
/plugin marketplace add jewunetie/skills
/plugin install skills@jewun-skills
```

> Note: all 18 skills are fully compatible with both runtimes. The `plan-audit` bundled subagent is Claude Code-only (Codex requires TOML agent format).

## Skills

| Skill | Description |
|---|---|
| `alphaxiv-paper-lookup` | Fetch structured AI-generated overviews of arxiv papers via alphaxiv.org |
| `ask-user` | Rich elicitation tool — forms, cards, multi-select, file uploads — for gathering user input |
| `cc-agent-sdk-workflows` | Build Python workflows and multi-agent pipelines with the Claude Agent SDK |
| `explain-concept` | Structured, pedagogically calibrated explanations of complex topics |
| `fresh-eyes-review` | Multi-pass self-review (surface, logic, cross-reference, regression) of produced work |
| `google-search-operators` | Advanced Google search operator syntax for precise, targeted web searches |
| `harness-codebase-design` | Design repositories for reliable AI agent assistance (CLAUDE.md, hooks, feedback loops) |
| `human-centered-ai-design` | Post-2024 principles for human-centered AI product design (PAIR, HAX, HIG frameworks) |
| `humanizer` | Strip AI-writing patterns and restore natural human voice in text |
| `improve-notes` | Clean up and structure meeting notes, optionally merging with a transcript |
| `interviewer` | Socratic stress-testing of plans and designs via relentless structured questioning |
| `osint-research` | Systematic open-source intelligence methodology for people, orgs, and topics |
| `pdf-vision` | Vision-based PDF reading that preserves layout, figures, tables, and multi-column structure |
| `plan-audit` | Blind-reconstruct a plan from code and diff it against the original to catch scope creep |
| `qwen-800m` | Run Qwen 3.5 0.8B locally in the Claude sandbox for inference and benchmarking |
| `solve` | Consulting-framework-driven structured problem solving for any domain |
| `visual-reasoning` | Iterative image manipulation (rotate, crop, enhance) for extracting hard-to-read visuals |
| `youtube-video` | Transcribe, analyze, and extract content from YouTube videos |

## Structure

```
.claude-plugin/
  plugin.json        # Claude Code plugin manifest
  marketplace.json   # Claude Code marketplace listing
.codex-plugin/
  plugin.json        # Codex plugin manifest
.agents/
  plugins/
    marketplace.json # Codex marketplace listing
skills/
  <skill-name>/
    SKILL.md         # Skill definition and trigger rules
    references/      # Supporting reference documents (where applicable)
    scripts/         # Helper scripts (where applicable)
    templates/       # Template files (where applicable)
    bundled-agents/  # Bundled agent prompts (where applicable)
```

## License

MIT
