# Pattern Catalog: Concrete UI Patterns by Problem

This file maps the recurring problems in AI product design to specific UI patterns. For each pattern: what it is, when to use, when it backfires, source attribution.

Use this file when the user asks "what specific pattern should I use for X?" rather than "what does the research say about X?". For the latter, use `thematic-clusters.md`.

## Problem index

1. The articulation barrier (users do not know what to type)
2. Verification cost (users cannot easily check if outputs are correct)
3. Generative variability (same input yields different outputs)
4. Error recovery (something went wrong)
5. Over-automation (agents act without enough oversight)
6. Citation reliability (sources look credible but are not)
7. Onboarding friction (users do not understand the AI's capabilities)
8. Hallucination and ungrounded responses
9. Ambient AI presence (users do not know AI is involved)

## Problem 1: The articulation barrier

Users frequently cannot translate their intent into an effective prompt. Patterns below help users construct, refine, and reuse prompts.

### Prompt starters / conversation starters

**What it is.** Predefined prompts shown in zero or empty state. User taps to insert and optionally edits.

**When to use.** New-user onboarding; entry points for capability surfaces; whenever the input space is open-ended.

**When it backfires.** Generic starters that feel like marketing copy ("Tell me a fun fact!") rather than task-relevant scaffolds.

**Source.** Microsoft Copilot UX guidance; Shape of AI catalog; Smashing Magazine 2025.

### Prompt suggestions and example galleries

**What it is.** Curated examples paired with their actual outputs (DALL-E's example-and-prompt pairs are the canonical reference).

**When to use.** Creative tools where output style varies widely; technical tools where users need to learn the prompt vocabulary.

**When it backfires.** Examples that misrepresent capability (showing only best-case outputs); galleries that become stale as the model improves.

**Source.** IBM Weisz et al. (CHI 2024); PAIR Mental Models chapter.

### Reverse prompting

**What it is.** Derive a prompt from a desired output. Midjourney's "Describe" feature is the canonical example.

**When to use.** When users have an example they want to riff on but cannot describe in words.

**When it backfires.** When the source example contains protected or proprietary content that should not be reproduced.

**Source.** Shape of AI catalog.

### Style galleries and parametrization

**What it is.** UI controls (dropdowns, sliders, chips) for style, tone, length, persona, instead of requiring text-only specification.

**When to use.** Whenever the parameter space is bounded and known. Tone, length, formality, audience are good candidates.

**When it backfires.** When parameters multiply beyond what users can hold in working memory; when the controls force false precision (a tone slider with no labels).

**Source.** Smashing Magazine 2025 (Wroblewski and Sharma); IBM "Design for Co-Creation".

### Targeted prompt rewrite / aided prompt understanding

**What it is.** System annotates or shades prompt elements that may produce poor results, optionally offering rewrites.

**When to use.** Power-user tools where users want to understand and refine; agentic settings where prompts drive cascading actions.

**When it backfires.** When the rewrite feels paternalistic or removes user voice; when the system rewrites in ways the user cannot easily revert.

**Source.** UX Tigers (Nielsen, "Aided Prompt Understanding").

### Related and follow-up prompts

**What it is.** Suggested next questions after each AI response. Perplexity's pattern is canonical.

**When to use.** Conversational interfaces; research and exploration tools.

**When it backfires.** When suggestions feel like engagement bait rather than helpful continuations; when they distract users from the answer they just received.

**Source.** Industry observations (Perplexity, ChatGPT, Bing Chat).

### Custom instructions and persistent user context

**What it is.** Let users teach the AI about themselves persistently. ChatGPT Custom Instructions, Claude Projects, are canonical.

**When to use.** Repeated-use tools where preferences persist across sessions.

**When it backfires.** When users do not realize they have set instructions and are surprised by their effects; when instructions are over-applied to inappropriate contexts.

**Source.** IBM "Design for Mental Models"; PAIR (generative AI updates).

## Problem 2: Verification cost

Users cannot easily check whether AI outputs are correct. Patterns below reduce the cognitive load of verification.

### Inline numbered citations with passage-level previews

**What it is.** Numbered citations rendered inline with text; clicking expands to show the exact passage cited (not the whole document).

**When to use.** Any factual content; RAG-grounded responses; research tools.

**When it backfires.** When citations look credible but point to fabricated or wrong sources. Microsoft 2025 found that the *mere presence* of citations increases trust whether or not sources are accurate.

**Source.** Microsoft Copilot custom engine agents; Microsoft Vorvoreanu et al. 2025; ChatGPT Search; Perplexity.

### Source-link to exact passage, not document

**What it is.** Citation link jumps to the specific paragraph or sentence in the source, with the relevant passage highlighted.

**When to use.** Any time the source document is non-trivial in length.

**When it backfires.** When source highlighting is wrong (cites the right document but wrong passage). Worse than no link because it falsely signals confirmation.

**Source.** Microsoft "Fostering Appropriate Reliance" 2025: "The amount of manual work it takes to verify is not fair."

### Verification-focused explanations (vs background explanations)

**What it is.** Explanation shows *how to check* the answer, not just rationale. GPT-4V drawing the maze path so the user can verify the answer is the canonical example.

**When to use.** Any decision-support context; tasks where verification is feasible.

**When it backfires.** When the verification step is itself error-prone (do not give users a verification path that they cannot reliably execute).

**Source.** Microsoft Vorvoreanu et al. 2025; CHI 2025 explanation studies.

### Confidence indicators (use cautiously)

**What it is.** Visual or textual cues showing model confidence (color coding, "I am not fully sure", numeric percentages).

**When to use.** Only when validated empirically. Simple visual highlights (single color cue on a low-confidence span) are more effective than complex visualizations or numeric percentages.

**When it backfires.** Often. Numeric confidence is hard for non-experts to interpret. Confidence cues can increase trust even when miscalibrated.

**Source.** PAIR Explainability + Trust chapter; Kim et al. FAccT 2024; MDPI review (December 2025) of 84 HAIC studies.

## Problem 3: Generative variability

Same input yields different outputs. Users need to understand and harness this rather than be confused by it.

### Multiple drafts presented side-by-side

**What it is.** Generate two to four variations of an output and present them simultaneously for comparison.

**When to use.** Creative tasks (writing, design, image generation); when there is no single correct answer.

**When it backfires.** When users feel obliged to pick one when none fit; when the variations are too similar to be meaningfully distinct.

**Source.** IBM "Design for Generative Variability" (CHI 2024); Google Gemini draft-A-B-C; DALL-E grid; Adobe Firefly variations.

### Regenerate with reasons

**What it is.** Let users regenerate with optional rationale ("make it shorter", "more formal", "different angle"). The reason becomes input to the next generation.

**When to use.** Any output users will iterate on.

**When it backfires.** When regenerate is the only edit affordance and users actually need to manually edit a specific phrase.

**Source.** ChatGPT, Claude artifacts, Adobe Firefly; PAIR "Use friction to avoid overreliance".

### Granular edit controls

**What it is.** Make-shorter, make-longer, change-tone, regenerate-this-paragraph. Operate on user-selected text spans.

**When to use.** Long-form generation where users want to keep most of the output but adjust pieces.

**When it backfires.** When the controls are buried or non-discoverable; when applying one control invalidates surrounding context.

**Source.** Google Workspace AI features; Notion AI; IBM "Design for Co-Creation".

### Curation surfaces (favorites, history, collections)

**What it is.** Let users save, annotate, and organize generated outputs across sessions.

**When to use.** Generative tools used over time; situations where good outputs are valuable assets.

**When it backfires.** When the curation UI becomes a separate maze users have to navigate.

**Source.** IBM "Design for Generative Variability".

## Problem 4: Error recovery

The system has produced something wrong, unhelpful, or off-target.

### Manual failsafe (non-AI path)

**What it is.** Always provide a way to complete the task without AI. Keyword search alongside semantic search; manual form alongside conversational input.

**When to use.** Any user-facing AI feature, especially in early adoption.

**When it backfires.** When the manual path is so degraded that users do not really have a choice (false fallback).

**Source.** PAIR Errors + Graceful Failure chapter; Microsoft HAX Guideline 8.

### Refusal with actionable explanation

**What it is.** When confidence is low or sources are absent, refuse with a transparent reason and a path forward, not "I do not know."

**When to use.** Factual or decision-support contexts where wrong is worse than absent.

**When it backfires.** When refusals become so frequent users lose trust in the feature ("it never works").

**Source.** Microsoft Copilot Studio guidance; Apple HIG.

### Targeted correction affordances

**What it is.** Microsoft HAX Guideline 9: "Support efficient correction." Inline edit, "fix this", or thumbs-down with reason.

**When to use.** Any AI surface that produces output users will refine.

**When it backfires.** When correction signals do not feed back into model improvement (users feel ignored).

**Source.** Microsoft HAX Guidelines; PAIR Feedback + Control chapter.

### Graceful escalation (vs silent fallback)

**What it is.** When AI cannot complete a task at high stakes, escalate explicitly to a human path with audit trail rather than silently switching to a non-AI fallback.

**When to use.** Agentic systems; high-stakes contexts; regulated domains.

**When it backfires.** When escalation paths are slow or non-existent; when users learn the escalation path is theater.

**Source.** Google Cloud agentic patterns; Microsoft Copilot agents 2025.

## Problem 5: Over-automation in agents

Agents are taking actions users do not want, do not see, or cannot reverse.

### Propose-and-commit separation

**What it is.** Agent stores a structured action payload (e.g., "send email X to Y"); reviewer approves; only then is the tool call executed with idempotency keys and post-action verification.

**When to use.** Any high-impact action: financial, deletions, irreversible tool use, external communications.

**When it backfires.** When the approval step becomes ritualistic (users approve everything without reading).

**Source.** Google Cloud Architecture Center 2025; Codebridge "5 Agentic AI Design Patterns CTOs Must Evaluate" 2026.

### Risk-tiered autonomy modes

**What it is.** Three tiers: "suggest-only" (user must take action), "propose-and-approve" (user must confirm), "execute-with-rollback" (agent acts but can undo). Choose based on stakes and reversibility.

**When to use.** Any agentic system. The tier should be visible to the user and switchable per-task.

**When it backfires.** When the default tier is too aggressive for the user's risk tolerance.

**Source.** VentureBeat 2025; Codebridge 2026.

### Proactive pausing for ambiguity (Morae pattern)

**What it is.** Agent automatically detects decision points (multiple plausible options) and pauses to surface choices to the user.

**When to use.** UI agents; agents executing multi-step workflows where intermediate decisions matter.

**When it backfires.** When pausing is too frequent and breaks flow; when the agent's notion of "ambiguous" does not match the user's.

**Source.** Peng et al. "Morae" UIST 2025.

### Action traces at the right level of detail

**What it is.** Show what the agent did, in a digestible summary. Not a verbose log, not just a final result.

**When to use.** Any agentic system where users may want to verify or debug.

**When it backfires.** When traces are too detailed (users skim and miss errors) or too summary (users cannot diagnose problems).

**Source.** Microsoft Research "Overseeing Agents Without Constant Oversight" 2026.

### Asynchronous notification on long tasks

**What it is.** Agent works in the background and notifies on completion; user can keep chatting in the meantime.

**When to use.** Tasks that take longer than a few seconds; tasks that benefit from interruption-tolerance.

**When it backfires.** When users forget what they asked for; when notifications are lost.

**Source.** Microsoft Copilot custom engine agents.

## Problem 6: Citation reliability

Citations look credible but may be fabricated or wrong. This is a sub-problem of verification but warrants its own treatment because citations are now standard.

### Refuse ungrounded responses by default

**What it is.** System refuses to answer factual questions when no grounding source is available, rather than producing an ungrounded answer with no citation.

**When to use.** RAG-grounded products; any factual context.

**When it backfires.** When grounding is overly strict and refuses reasonable queries; when users are not told why their query was refused.

**Source.** Microsoft Copilot Studio's "Allow ungrounded responses" toggle (default-off).

### Two-step generation pattern

**What it is.** Separate factual data assembly (low-risk, deterministic) from formatting and styling (creative). Generate the facts first, then have the model arrange them.

**When to use.** Customer-facing factual content; reporting; document generation from data.

**When it backfires.** When the boundary between "factual" and "creative" is unclear.

**Source.** Lakshmanan, "Generative AI Design Patterns" 2024.

### Self-check / multi-candidate verification

**What it is.** Generate multiple candidate answers; have the model reflect on inconsistencies; surface the convergent answer (or surface the disagreement).

**When to use.** High-stakes factual queries; any context where wrong-with-confidence is worse than uncertain.

**When it backfires.** When all candidates make the same mistake (correlated errors).

**Source.** CHI 2025 "Think Twice Before Trusting" (T3); various 2024 to 2025 self-consistency papers.

## Problem 7: Onboarding friction

Users do not understand what the AI can do, how well it does it, or how to get started.

### Onboard in stages

**What it is.** Introduce features at the moment they become relevant, not in a long initial tutorial. Suggest a low-risk reversible action immediately so users can tinker.

**When to use.** Any AI feature with non-trivial capability; any complex generative tool.

**When it backfires.** When stages feel like nagging; when users want a comprehensive overview and cannot find one.

**Source.** PAIR Mental Models chapter.

### Capability previews (curated cards, sample outputs)

**What it is.** In zero state, show capability previews via curated cards with sample inputs and outputs.

**When to use.** Generative tools; chat interfaces with broad capability.

**When it backfires.** Same as prompt suggestions: cards that misrepresent capability.

**Source.** Microsoft Copilot UX; Shape of AI.

### Plan for co-learning

**What it is.** Frame the user-AI relationship as collaborative. Users teach the system over time and the system adapts. Make the first failure feel like a teaching moment rather than a betrayal.

**When to use.** Personalized AI features; tools used over long periods.

**When it backfires.** When the system does not actually learn (or learning is too slow to be visible) and "co-learning" feels like marketing.

**Source.** PAIR Mental Models chapter.

## Problem 8: Hallucination and ungrounded responses

The model produces fluent but wrong content.

### First-person uncertainty expressions

**What it is.** Phrases like "I am not completely sure, but..." or "I think this is correct, but you should verify."

**When to use.** Lower-stakes contexts where flagging uncertainty is more helpful than failing silently.

**When it backfires.** Microsoft 2025: uncertainty expressions are a double-edged sword. They can reduce confidence in the system overall, increase task time, or paradoxically be ignored.

**Source.** Kim et al. FAccT 2024; NN/g "AI Hallucinations: What Designers Need to Know" 2024.

### Explicit AI labels and content credentials

**What it is.** Visual badge on AI-generated content. Sparkle icon, "AI-generated" label, C2PA Content Credentials cryptographic provenance.

**When to use.** Any generated content presented to users; any context where legal compliance (EU AI Act) requires it.

**When it backfires.** When labels are so omnipresent users develop blindness; when labels are inconsistent across surfaces.

**Source.** Apple HIG Generative AI; Microsoft Teams SDK; C2PA 2.1 specification 2024.

### Cognitive forcing functions

**What it is.** Force users to think before consuming the AI's answer. Make their own first guess, confirm dialog, deliberate pause.

**When to use.** Decision-support contexts where overreliance is the dominant risk; high-stakes individual decisions.

**When it backfires.** Friction can drive underreliance (users abandon AI advice entirely). Users adapt and click through.

**Source.** Buçinca et al. 2021; replicated in CHI 2024 to 2025.

### Devil's-advocate explanations

**What it is.** System generates a counter-explanation alongside the supporting one. Users see why the AI might be wrong, not just why it might be right.

**When to use.** High-trust contexts where users would otherwise accept without scrutiny.

**When it backfires.** When counter-explanations are weak or formulaic (users learn to discount them).

**Source.** Suh et al. CHI 2025 HCXAI workshop.

## Problem 9: Ambient AI presence

AI is involved in producing some output, but users do not know.

### Visible AI labels at the surface where decisions are made

**What it is.** When AI suggests, summarizes, or filters, label that surface explicitly. Apple's sparkle icon, "Summarized by AI" headers, etc.

**When to use.** Any user-facing surface where AI shapes what the user sees.

**When it backfires.** Already covered (label fatigue, inconsistency).

**Source.** Apple HIG; Microsoft Copilot custom engine agents (automatic AI labels).

### Disclosure of training data and model behavior at the product level

**What it is.** Documented model card or "About this AI" page explaining training data, known limitations, and intended uses.

**When to use.** Products where users may want to understand the AI before relying on it; regulated domains.

**When it backfires.** When the disclosure is so technical it is unreadable; when it is buried in legal pages.

**Source.** Mitchell et al. "Model Cards" 2019; Pushkarna et al. "Data Cards" FAccT 2022; Apple Foundation Models documentation 2024 to 2025.

### Provenance metadata (machine-readable)

**What it is.** Cryptographically signed metadata embedded in generated content (image, audio, video, document).

**When to use.** Generated media; any content that may circulate beyond the originating platform.

**When it backfires.** When provenance can be stripped easily; when consumers do not know to look for it.

**Source.** C2PA 2.1 specification 2024; Google, Adobe, Microsoft, OpenAI joint adoption 2024 to 2025; EU AI Act compliance 2025.
