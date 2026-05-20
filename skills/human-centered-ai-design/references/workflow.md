# Workflow: Design Review and Design Generation

This file covers two workflows:

- **Review branch.** The user has an existing AI feature, design, or spec and wants it audited.
- **Generation branch.** The user is starting fresh and wants help designing an AI feature.

Both branches use the eight commitments from SKILL.md as scaffolding. They diverge in inputs, outputs, and how the commitments are applied.

## Step 0: Identify the branch

Before doing anything else, identify which branch fits:

- If the user has shared a design, spec, screenshot, description of an existing feature, or wireframes, use the **review branch**.
- If the user has shared a problem, user need, or use case but no specific design, use the **generation branch**.
- If the user has both (a problem and a partial design), ask which they want first. Reviewing the partial design is usually faster and surfaces gaps that inform generation.

If unclear, ask once: "Are you looking to audit an existing design, or to think through a new one from scratch?"

## Review branch

**Goal.** Produce a structured findings document that identifies strengths, gaps, and prioritized recommendations across the eight commitments.

### Step R1: Gather context

Ask for what is missing if the user has not provided it. The minimum viable context is:

- What the feature does (one or two sentences).
- Who the target user is (especially: novice, expert, professional, casual).
- What the stakes are (low: drafting; high: financial, medical, legal, irreversible).
- What is shown to the user when the AI runs (UI elements, output format, controls).
- What happens when the AI is wrong (recovery surface).

If the user has only shared a screenshot or short description, ask one focused follow-up rather than peppering them with questions. Pick the question that most affects the audit (usually: stakes, or what happens when wrong).

### Step R2: Run the eight-commitment audit

For each of the eight commitments, ask the diagnostic question and note findings. Do not score numerically; focus on specific observations. If a commitment does not apply to the design (for example, agentic-AI commitments on a non-agentic feature), say so explicitly and skip.

**Commitment 1: Justify AI's presence.**

- Diagnostic. Does this design use AI where AI adds unique value over a heuristic, rule, or manual control? Could a deterministic or retrieval system serve users better?
- Look for. Cases where AI is used for predictable, low-variance tasks; cases where the AI's nondeterminism causes user confusion.
- Source frame. PAIR User Needs + Defining Success; Apple HIG quality bar by feature type.

**Commitment 2: Set honest, accurate expectations.**

- Diagnostic. Are capabilities and limitations visible at every entry point? Does the design build on familiar mental models? Does it correct common GenAI misconceptions (it generates rather than retrieves; fluency is not accuracy)?
- Look for. Marketing-style descriptions of capability; absent or buried limitations; no onboarding for first-time use; no in-context teaching of variability.
- Source frame. Microsoft HAX Guidelines 1 and 2; PAIR Mental Models; IBM "Design for Mental Models."

**Commitment 3: Design for appropriate reliance.**

- Diagnostic. Are explanations, confidence cues, or citations being used as defaults? Are they treated as testable hypotheses or assumed to work? Is verification feasible (passage-level citations) or burdensome (document-level citations)?
- Look for. Citation lists that link to whole documents; numeric confidence scores presented to non-expert users; explanations without counter-explanations in high-trust contexts.
- Source frame. Microsoft Vorvoreanu et al. 2025; "The Amplifying Effect of Explainability in AI-assisted Decision-making in Groups" (CHI 2025); Tension 2 in `tensions.md`.

**Commitment 4: Preserve user agency.**

- Diagnostic. Are AI outputs editable, regenerable, dismissible? Is there a manual fallback path? Is co-creation supported, or is the AI replacing rather than augmenting?
- Look for. Locked outputs; no regenerate or refine controls; no non-AI path to complete the same task; surprise automation.
- Source frame. Apple HIG (Generative AI); IBM "Design for Co-Creation"; Microsoft HAX Guidelines 7 to 9.

**Commitment 5: Plan for failure.**

- Diagnostic. Have failure modes been enumerated? Are recovery flows specified? Does the design choose graceful fallback or explicit escalation appropriately for stakes?
- Look for. No clear behavior when the model fails; "I do not know" without an actionable next step; silent fallback in high-stakes contexts where escalation would be appropriate.
- Source frame. PAIR Errors + Graceful Failure; Microsoft HAX Playbook; Microsoft Copilot guidance on grounding refusals.

**Commitment 6: Generative AI specifics.**

- Diagnostic. (Skip if the feature is not generative AI.) Does the design handle generative variability (multiple drafts, regenerate)? Does it address the articulation barrier (prompt scaffolds, suggestions)? Are AI labels and citations present? Is provenance metadata embedded?
- Look for. Single-shot output with no comparison; no prompt scaffolding for new users; missing AI labels; no source provenance for content that will circulate.
- Source frame. IBM CHI 2024 (Design for Generative Variability, Co-Creation); Apple HIG; C2PA; Cluster 7 in `thematic-clusters.md`.

**Commitment 7: Agentic AI specifics.**

- Diagnostic. (Skip if the feature is not agentic.) Are proposal and commit separated for high-impact actions? Is autonomy tiered by reversibility? Are action traces visible at the right detail level? Does the agent pause for ambiguity?
- Look for. Silent execution of irreversible actions; verbose traces that hide errors; minimal traces that prevent debugging; no human approval for high-stakes commits.
- Source frame. Peng et al. UIST 2025 (Morae); Microsoft Research 2026; Google Cloud agentic patterns; Cluster 8 in `thematic-clusters.md`.

**Commitment 8: Sociotechnical context.**

- Diagnostic. Is there organizational accountability documented? Is provenance infrastructure in place (model cards, data cards, C2PA)? Are ethical taxonomies referenced? Are evaluation metrics human-centered or model-centric only?
- Look for. No model card or about-this-AI page; no monitoring of overreliance or underreliance; success metrics that are only model accuracy.
- Source frame. Microsoft Responsible AI Standard; Apple safety taxonomy; Mitchell et al. Model Cards; Stanford HAI human-centered metrics.

### Step R3: Identify and flag tensions

If the design touches one of the four tensions in `tensions.md`, flag it. Do not pick a side for the user; surface that this is a contested area and what the trade-offs are.

Common cases:

- The design uses anthropomorphic framing for novice users. Flag Tension 1.
- The design relies heavily on citations or confidence cues. Flag Tension 2.
- The design has agentic actions without clear approval gates. Flag Tension 3.
- The design uses cognitive forcing functions or friction. Flag Tension 4.

### Step R4: Produce the findings document

Use this exact structure:

```
# AI Design Review: [Feature Name]

## Context summary
[2 to 4 sentences. What the feature does, target user, stakes, current state.]

## Strengths
[Observations of what the design does well, organized by commitment. 3 to 6 items typical.]

## Gaps and risks
[Observations of what the design does poorly or omits, organized by commitment. 3 to 8 items typical.]

## Active tensions to navigate
[Which of the four tensions the design touches. Both sides briefly. No prescriptive answer.]

## Prioritized recommendations
[3 to 6 specific, actionable recommendations. Order by impact. Each recommendation cites the source frame from the commitment that motivated it.]

## What to test
[2 to 4 specific things to validate empirically rather than accept by default. Particularly relevant for trust-calibration aids per Tension 2.]
```

### Step R5: Fresh-eyes review

After producing the findings, do a fresh-eyes review. Check:

- Are claims attributed to specific sources?
- Are recommendations actionable and prioritized?
- Are tensions flagged where they apply (not just paying lip service)?
- Does the formatting match any conventions the user has expressed (for example, in user preferences)?

Present findings before considering the task complete.

## Generation branch

**Goal.** Produce a structured set of design considerations and recommendations grounded in the eight commitments. This is *not* a full design brief; it is a thinking aid for the user to write the actual deliverable.

### Step G1: Gather problem context

Ask for what is missing. The minimum viable context is:

- What the user is trying to accomplish (the user need, not the AI feature).
- Who the target user is (novice, expert, professional, casual).
- What the stakes are.
- What constraints exist (platform, regulatory, organizational).
- What alternatives have been considered (manual, rule-based, retrieval).

If only the user need is provided, ask one focused follow-up. The most useful question is usually about alternatives considered (because Commitment 1 starts with "is AI even right here?").

### Step G2: Apply Commitment 1 first (justify AI's presence)

Before proceeding, walk through whether AI is actually the right answer:

- What unique value does AI add over a heuristic, rule, or retrieval system?
- Is the task one with consensus on the "correct" way (favoring automation) or one with no agreed-upon correct approach (favoring augmentation)?
- What is the cost of AI errors compared to the benefit of AI successes?
- Is this a critical feature (high accuracy bar) or complementary (lower bar)?
- Should this be proactive (highest bar) or reactive (lower bar)?

If AI is not clearly the right answer, surface this explicitly. Do not power through to design just because the user asked for an AI feature. The most valuable thing this skill can do is sometimes to recommend not building the AI feature.

### Step G3: Walk through Commitments 2 to 8 as design generators

For each remaining commitment, generate specific design considerations for the user's context. Do not produce generic guidance; be specific to the user's user need, stakes, and constraints.

**Commitment 2 (mental models).** What capabilities and limitations should be visible? What familiar mental model can users build on? What GenAI misconceptions are likely in this user population? What onboarding pattern fits (in-stages, capability previews, plan-for-co-learning)?

**Commitment 3 (appropriate reliance).** What verification needs to happen? What aids are candidates (citations, confidence cues, explanations, counter-explanations)? Which should be A/B-tested rather than assumed? Are passage-level citations feasible?

**Commitment 4 (user agency).** What should be editable, regenerable, dismissible? What is the manual fallback? What is the co-creation surface?

**Commitment 5 (failure planning).** What are the likely failure modes? Use the HAX Playbook approach: enumerate transcription errors, false positives, ambiguity errors, context errors. For each, what is the recovery flow? Graceful fallback or explicit escalation, given the stakes?

**Commitment 6 (generative AI specifics, if applicable).** Multiple drafts? Regenerate controls? Edit affordances? Prompt scaffolds? AI labels? Provenance metadata? Apply only those relevant to the use case.

**Commitment 7 (agentic specifics, if applicable).** What actions are reversible vs irreversible? What is the autonomy tier per action (suggest-only, propose-and-approve, execute-with-rollback)? What action traces are needed? Where should the agent pause for ambiguity?

**Commitment 8 (sociotechnical context).** What documentation is needed (model card, data card)? What metrics will be monitored (overreliance signals, underreliance signals, decision quality)? What red-teaming is needed?

### Step G4: Identify tensions and decisions to validate

Surface which tensions apply and what the user will need to validate empirically. Tensions tend to surface around:

- Tone and framing (Tension 1).
- Trust-calibration aids (Tension 2).
- Autonomy levels (Tension 3, if agentic).
- Friction patterns (Tension 4).

For each tension flagged, give the user the decision heuristic and a worked example, but do not pick a side.

### Step G5: Produce the considerations document

Use this exact structure:

```
# AI Design Considerations: [User Need / Feature Name]

## Problem context
[2 to 4 sentences. User need, target user, stakes, constraints.]

## Should AI be used here?
[Output of Commitment 1 walkthrough. Be honest. If AI is not clearly right, say so.]

## Key design considerations by commitment
[For each applicable commitment 2 to 8: specific considerations for this context. Each consideration cites the source frame.]

## Tensions to navigate
[Which of the four tensions apply. Both sides briefly. Decision heuristic.]

## Concrete patterns to consider
[Reference specific patterns from `patterns.md` that apply. For each: what it solves, when it backfires.]

## Things to validate empirically
[3 to 5 specific design choices that should be A/B tested or user-researched rather than accepted by default.]

## Open questions
[Anything the user has not answered that affects the design. List them so the user knows what to think about next.]
```

### Step G6: Fresh-eyes review

Same as Step R5. Check attribution, actionability, tension flagging, formatting compliance.

## Notes for both branches

**Length.** Findings and considerations should be substantial but not exhaustive. Aim for around 400 to 800 words of body content (excluding headings). If the user wants more depth on a specific area, they will ask.

**Tone.** Direct, evidence-based, willing to push back. The skill's value is in honest assessment; sycophancy or over-caveating defeats the purpose.

**Source attribution.** Every claim should be traceable. If a claim cannot be sourced from `thematic-clusters.md` or `sources.md`, either find the source or omit the claim.

**Default to "test this" over "do this" when the literature is divided.** Especially for trust-calibration aids (Tension 2).
