---
name: human-centered-ai-design
description: Apply post-2024 state-of-the-art principles for designing human-centered AI systems. Use this skill whenever the user is designing, specing, reviewing, critiquing, or planning an AI feature or product; asking principled questions about AI UX (errors, hallucinations, trust calibration, explainability, onboarding, anthropomorphism, agentic autonomy, citations, content provenance); working through tradeoffs around automation level or human-in-the-loop oversight; asking "should I use AI for this"; or evaluating designs against frameworks like Google PAIR, Microsoft HAX, Apple HIG, IBM, Stanford CS 247A, CMU 05-318, or recent CHI and UIST work. Trigger proactively even when the user does not explicitly ask for design principles, as long as they are working on an AI product question. Do NOT use for ML model selection, prompt engineering tuning detached from product design, or general AI ethics discussions detached from product context.
---

# Human-Centered AI Design

Post-2024 state of the art for designing AI features and products. Synthesizes research-backed principles, patterns, and active disagreements from Google PAIR, Microsoft HAX, Apple HIG, IBM, Stanford CS 247A, CMU 05-318, Stanford HAI, and recent CHI and UIST publications.

## How to use this skill

Four modes are supported. Identify which one fits the user's question, then route accordingly:

1. **Reference lookup** ("What does the research say about X?"): Use the decision tree below to identify the relevant thematic cluster, then load only that section of `references/thematic-clusters.md`.
2. **Design review** ("Audit this AI feature"): Load `references/workflow.md` and follow the review branch.
3. **Design generation** ("Help me design an AI feature for X"): Load `references/workflow.md` and follow the generation branch.
4. **Tension navigation** (when the question hits one of the four active disagreements): Load `references/tensions.md` and present both sides rather than picking one.

When making any specific claim in your response, attribute it inline to its source (for example, "Microsoft HAX Guideline 11", "PAIR Mental Models chapter", "Vorvoreanu et al. 2025"). For a quick lookup of which framework covers what, use `references/sources.md`. Inline attribution is not optional; it is what distinguishes this skill from generic advice.

## The eight SOTA commitments

These are the layered design commitments that synthesize across all sources. Use them as the skeleton for any review or generation task. Each is a one-liner with a hook; cluster files contain the detail.

1. **Justify AI's presence.** Use AI only where it adds unique value over heuristics; default to augmentation over automation; raise the quality bar for proactive features.
2. **Set honest, accurate expectations.** Make capabilities and limitations visible at every entry point; build on familiar mental models; explicitly correct novice misconceptions about generative AI (it generates rather than retrieves; fluency is not accuracy).
3. **Design for appropriate reliance, not blind trust.** Treat explanations, confidence cues, and citations as testable hypotheses; assume mitigations may backfire; deploy verification-focused rather than persuasion-focused aids.
4. **Preserve user agency throughout.** Make outputs editable, regenerable, dismissible; provide manual fallbacks; support co-creation rather than replacement.
5. **Plan for failure as a first-class design surface.** Enumerate failure modes proactively (HAX Playbook approach); design recovery flows; choose between graceful fallback and explicit escalation based on stakes.
6. **For generative AI, design for variability, imperfection, and the articulation barrier.** Use prompt scaffolds, multiple drafts, structured edit controls, inline citations linked to source passages, AI labels, and provenance metadata.
7. **For agentic AI, separate proposal from commit and tier autonomy by reversibility.** Surface action traces at the right level of detail; pause proactively at ambiguous decision points; require human approval for irreversible high-stakes actions.
8. **Recognize the sociotechnical context.** Human-centered AI requires organizational accountability, provenance infrastructure, ethical taxonomies, and a shift from "what can the model do" to "what can people do well with this model."

## Decision tree: route the question to a thematic cluster

Most reference-lookup questions can be answered by loading a single cluster from `references/thematic-clusters.md`. The file is large (around 440 lines), so do not read it whole. Instead, read the table of contents at the top (lines 1 to 21) first, then use `view_range` to load only the section for the cluster you need (~30 to 50 lines per cluster).

| If the user is asking about... | Load this cluster |
|---|---|
| Should I use AI for X, augmentation vs automation, when not to use AI, deciding fit | Cluster 1: Determining when (and when not) to use AI |
| Onboarding, expectation-setting, anthropomorphism, mental models for generative AI | Cluster 2: Setting expectations and mental models |
| Showing AI presence, content provenance, explanations, why the AI did X, confidence and uncertainty display | Cluster 3: Explainability and transparency |
| Overreliance, underreliance, trust calibration, cognitive forcing functions, verification UX | Cluster 4: Trust calibration and appropriate reliance |
| Feedback collection, user controls, opt-out, regenerate or dismiss or correct, edit affordances | Cluster 5: Feedback and user control |
| Hallucinations, error handling, graceful failure, RAG grounding, refusal patterns | Cluster 6: Errors, failure, and hallucination handling |
| Chat UI, prompt design patterns, citations, streaming, multiple drafts, generative variability | Cluster 7: Generative-AI-specific patterns |
| Agents, agentic AI, autonomy levels, action traces, propose-vs-commit, oversight UI | Cluster 8: Agentic-AI patterns |
| Training data, model cards, data cards, bias, fairness, privacy, C2PA, watermarking | Cluster 9: Data practices and responsible AI foundations |
| Metrics, evaluation, monitoring, A/B testing, red-teaming, post-launch measurement | Cluster 10: Post-launch evaluation and continuous improvement |

For multi-cluster questions (such as "design a complete AI assistant"), prefer loading `references/workflow.md` over loading multiple clusters. The workflow file already pulls from all clusters in the right order.

## Tension navigation

Four disagreements are currently active in the post-2024 literature. If the user's question hits any of these, load `references/tensions.md` and present both sides rather than picking one:

1. Anthropomorphic vs tool-like framing (collaborator metaphor vs tool metaphor).
2. Confidence cues, explanations, and citations as trust calibrators vs as overreliance amplifiers.
3. Speed of agentic autonomy (productivity-maximalist vs human-centered camps).
4. Cognitive forcing functions as overreliance mitigators vs as friction that drives underreliance.

For each tension, the file gives both positions with sources, plus a decision heuristic for picking in context (the heuristic is usually: tier by stakes, test empirically).

## Concrete pattern catalog

When the user asks "what specific UI pattern should I use for X?", load `references/patterns.md`. It maps problems (articulation barrier, verification cost, agentic over-automation, generative variability, error recovery, citation reliability) to specific patterns. Each pattern has: what it is, when to use it, when it backfires, source attribution.

## File map

- `references/thematic-clusters.md`: Ten thematic clusters with consensus recommendations, key patterns, source attributions, and post-2024 updates. Read the TOC first; load one cluster at a time via `view_range`.
- `references/patterns.md`: Concrete UI pattern catalog organized by the problem each pattern solves.
- `references/tensions.md`: The four active disagreements with both sides, sources, and decision heuristics.
- `references/sources.md`: Source attribution map. Quick lookup for "what does framework X say about topic Y?".
- `references/workflow.md`: Combined design review and design generation workflow. Branches at step one based on whether the user is reviewing an existing design or generating a new one. Both branches use the eight commitments as scaffolding.
