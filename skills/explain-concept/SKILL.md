---
name: explain-concept
description: >
  Help the user understand and internalize complex topics through a structured
  pedagogical approach calibrated to how they learn. Triggers on "explain X to me",
  "help me understand Y", "what is Z and why does it matter", "break down this
  concept", "teach me about W", "how does X work", "walk me through Y", "I keep
  hearing about X but do not really get it", "what is the intuition behind X", or
  any request where the user wants to build a mental model of something they do not
  yet understand. Also trigger when the user asks conceptual "why" questions about
  systems, architectures, or paradigms. Do NOT trigger on simple factual lookups
  ("when was X founded"), summarization requests, problem-solving or decision-making
  (use the solve skill), or requests where the user already understands the topic
  and wants information organized.
---

# Explain Concept

A pedagogical skill for helping the user understand complex topics. The user learns
best through concrete analogies that bridge to their existing knowledge, structured
decomposition with reasoning exposed, and interactive checkpoints where they can
restate concepts in their own words. They move quickly from understanding to
compressed reference material and value the ability to export a memo after the
conversation.

Before using this skill for the first time in a session, read `references/examples.md`
for worked examples at each tier. The examples demonstrate the tone, pacing, and
structure this skill produces.

## Process Order

On receiving a request to explain a concept:

1. **Detect tier.** Assess the topic's inherent complexity (see Tier System below).
2. **Research decision.** Based on the tier (see Research Protocol below). If research
   is needed, complete it before proceeding.
3. **Begin the pedagogical flow.** Step 1 includes the anchor assessment internally --
   whether to use an analogy or skip to a framing statement.

Do not announce the tier or the process. Just execute it naturally.

## Tier System

Classify based on the **topic's inherent complexity**, not the user's phrasing.
"How does X work" could be any tier depending on what X is.

### Quick Concept

**Signals:** Topic has a single core mechanism or idea. Can be understood without
understanding sub-systems. One mental model is sufficient.

**Examples of topics at this tier:** hash maps, idempotency, eventual consistency,
dependency injection, the difference between authentication and authorization.

**Flow:** Anchor (if helpful), then a brief direct explanation of the concept's
mechanism and why it matters, then compress. No decomposition into sub-components,
no checkpoint. A few paragraphs, conversational.

**Steps used:** 1 (Anchor), brief explanation (not a formal step -- just the natural
body of the response), then 5 (Compress). Steps 2-4 are skipped.

### Structured Explanation

**Signals:** Topic has 2-4 distinct components that interact. Understanding requires
grasping the relationships between parts, not just the parts themselves.

**Examples of topics at this tier:** RLHF, event-driven architecture, how grand jury
proceedings work, OAuth 2.0 flows, the difference between microservices and monoliths.

**Flow:** All five steps. Pause after decomposition for restating checkpoint.
Conversational with light formatting.

**Steps used:** All five (1 through 5).

### Deep Dive

**Signals:** Topic has multiple interacting sub-systems, competing schools of thought,
or requires understanding historical context to grasp current state. Would take an
expert more than 5 minutes to explain well.

**Examples of topics at this tier:** the US federal court system, transformer
architectures end-to-end, how prosecutors manage complex multi-defendant cases,
distributed consensus algorithms, the AI alignment landscape.

**Flow:** Research first (non-negotiable). All five steps at full depth. Pause after
decomposition. Delivered conversationally with checkpoint.

**Steps used:** All five, with research preceding Step 1.

**Default to Structured Explanation when uncertain.** Escalate to Deep Dive if
decomposition reveals more depth than expected. Drop to Quick Concept only when the
topic is genuinely contained.

## The Pedagogical Flow

### Step 1 -- Anchor

Start with a concrete analogy or comparison that bridges from something the user
already knows. The purpose is to make the new concept feel like a variation of
something familiar, giving the user a scaffold to hang new information on.

**Selecting the source domain:** Draw from whatever the user knows based on available
context -- memory, conversation history, the domain they are currently working in.
The user has deep familiarity with software engineering, product management, legal
technology, case management workflows, and startup operations. But do not restrict
to these -- if the user has demonstrated knowledge of a domain in conversation, it
is fair game.

**What makes a good anchor:**
- It maps mechanisms, not surface resemblance. "RLHF works like a product feedback
  loop -- you ship something, get user reactions, and iterate the product based on
  what they liked and disliked" is structural. "RLHF is like teaching a dog tricks"
  is decorative.
- It is specific enough to generate predictions. A good analogy lets the user
  anticipate how the new concept behaves before you explain it.
- It names its own limits. At the Structured and Deep Dive tiers, always include:
  "This analogy breaks down when..." so the user does not over-extend the mapping. At
  the Quick Concept tier, naming limits is optional when the analogy is brief and
  self-evident -- do not over-engineer a two-sentence bridge.

**Anchor escape hatch -- skip the anchor when any of these apply:**
- The user already has partial familiarity with the topic. An analogy could import
  wrong assumptions from the source domain that conflict with what they half-know.
- No structural analogy exists. If you can only find surface-level comparisons, they
  will do more harm than good.
- The topic is more fundamental than anything you could analogize to.

When skipping the anchor, begin with a crisp framing statement instead: one sentence
that captures the core tension or purpose of the concept. This is not a dictionary
definition -- it is a "here is the interesting problem this concept is responding to"
statement.

### Step 2 -- Landscape

Answer three orientation questions:
1. **What problem or need does this concept address?** Why does it exist?
2. **What are the major zones or categories within it?** Not detailed yet -- just the
   territories on the map.
3. **How does it relate to things the user already works with?** Connect to their
   context where natural.

This step is about motivation and map-drawing. Do not explain mechanisms yet. The
user should finish this step knowing *why the topic exists* and *what territory it
covers*, but not yet how any individual piece works.

### Step 3 -- Decompose with Reasoning

Now explain how each piece actually works. For each component identified in the
Landscape step:
- Explain its mechanism
- Explain why it matters (not just what it is, but what goes wrong without it)
- Explain how it connects to the other components

The shift from Step 2 to Step 3 is the shift from "here is the map" to "here is
what happens inside each region of the map."

Include concrete examples only when they naturally illuminate the concept. Do not
force examples as a required element -- some mechanisms are clearer through direct
explanation. When examples do appear, draw from the user's work context where
possible.

### Step 4 -- Restating Checkpoint

*Structured Explanation and Deep Dive tiers only. Skip for Quick Concept.*

Pause and invite the user to synthesize back in their own words. The prompt should
vary based on what the explanation covered. Choose the framing that best fits the
topic:

- If the explanation involved a core tension or trade-off: ask the user to
  characterize the trade-off.
- If it involved multiple competing approaches: ask which approach makes the most
  intuitive sense to them and why.
- If it involved a surprising or counterintuitive element: ask what part, if any,
  pushes against their initial intuition.
- If it involved a system with clear practical implications: ask how they see it
  connecting to what they are working on.
- If it involved a historical progression: ask what they think drove the evolution
  from one stage to the next.

Never use the same checkpoint phrasing twice in a conversation. The checkpoint should
feel like a natural conversational turn, not a pedagogical ritual. The goal is to
surface misunderstanding early, not to quiz.

**Wait for the user's response.** If they restate accurately, proceed to Step 5. If
something is off, correct the specific misunderstanding, re-anchor if needed, and
then proceed.

### Step 5 -- Compress

Once understanding is established (either confirmed through the checkpoint or
implicitly through a Quick Concept's contained scope), offer a compressed version.
This is the concept distilled into something the user can recall and use without
re-reading the full explanation.

The compressed version should be tight -- a few sentences or a short set of key
points. It is reference material, not a re-explanation. Optimize for recall and
future use.

After delivering the compressed version, offer to export a reference memo. Vary the
phrasing naturally -- do not use the same wording every time. The offer should feel
like a casual aside, not a scripted prompt.

## Export Memo (Optional Step 6)

This step lives outside the core pedagogical flow because it is optional, produces
a file rather than conversation, and can be invoked at any point after the explanation
is complete.

At any tier, after the explanation is complete, the user can request an exportable
reference memo as a markdown file.

**Value check before producing:** If the explanation was a single-turn Quick Concept
with no follow-up, tell the user that a memo would mostly restate what was just said
and ask if they still want one. Comply if they do. If the conversation involved
multi-turn refinement, corrections, follow-up threads, or "go deeper" expansions,
the memo is high-value and can be offered proactively.

**Memo structure:**

```
# [Concept Title]

## Summary
[One-sentence compressed version from Step 5]

## Core Analogy
[The anchor analogy and where it breaks down. Omit this section if no anchor was used.]

## Key Components
[The decomposition from Step 3, with reasoning preserved. Organized by component,
each with its mechanism, why it matters, and how it connects.]

## Examples
[Any concrete examples that came up in conversation. Omit if none were used.]

## Nuances and Corrections
[Anything refined through the restating checkpoint or follow-up turns. This section
captures what evolved during the dialogue. Omit if nothing was refined.]

## Open Questions
[Areas flagged for future exploration, or aspects the user noted they want to go
deeper on later. Omit if none.]
```

**Deep Dive file deduplication:** If the user requests a memo after a Deep Dive, the
memo is the single file output. There is no separate "explanation file" -- the memo
serves as the comprehensive, post-dialogue reference document that incorporates
everything from research through restating and follow-up.

Create the memo as a markdown file and save to `/mnt/user-data/outputs/`. If the
user specifically requests a different format (e.g., Word doc), use the appropriate
skill.

## Research Protocol

**Sequencing:** Research happens after tier detection but before the pedagogical flow
begins.

| Tier | Research rule |
|---|---|
| Quick Concept | Research only if the topic involves current or rapidly evolving information, or if you are not confident in accuracy. |
| Structured Explanation | Research if the topic has specialized, technical, or potentially outdated dimensions. Use judgment. |
| Deep Dive | Always research first. Non-negotiable. |

When researching, complete the research before starting Step 1. Do not interleave
research with explanation -- the user should receive a coherent explanation informed
by research, not a narration of your search process.

## Multi-Turn Behavior

When the user responds after any step:

- **"Go deeper on X."** Drill into that specific branch. Apply the pedagogical flow
  to the sub-concept: assess whether it needs its own anchor, decompose it, and
  checkpoint if it is complex enough. Build on the existing explanation rather than
  restarting.
- **"Actually, I forgot to mention..." or correction.** Integrate the new
  information. Reassess whether the anchor, decomposition, or compressed version
  needs updating. State what shifted and why.
- **"I disagree with the framing."** Ask what feels wrong. The user may have domain
  knowledge or context that changes the explanation. Reframe if warranted; hold the
  framing with reasoning if not.
- **"How does this relate to Y?"** Bridge the current concept to the new one. This
  may trigger a new Quick Concept explanation for Y or a comparison between the two.
- **Restating with errors.** Correct the specific misunderstanding gently. Re-anchor
  the specific component that was off, do not repeat the entire explanation.

In all cases, do not restart from scratch. Build on the existing explanation and
reference what was already covered.

## Behavioral Guardrails

- **Never start with a definition.** Start with the anchor or, if skipping the
  anchor, a framing statement about the problem the concept addresses. Definitions
  are for dictionaries; explanations are for understanding.
- **No decorative analogies.** If an analogy does not map mechanisms, do not use it.
  "Think of it like..." followed by a surface comparison is worse than no analogy.
- **Respect the tier.** Do not over-explain at Quick Concept. Resist the urge to be
  comprehensive when the user just needs a mental model. Do not under-explain at
  Deep Dive -- that tier exists because the topic genuinely requires depth.
- **Match vocabulary to the user's domain.** If explaining a biology concept, use
  engineering or product metaphors. If explaining an engineering concept in a legal
  tech context, use legal workflow metaphors. Meet the user where they are.
- **The checkpoint is not a quiz.** It is an invitation to think out loud. Frame it
  as collaborative, not evaluative.
- **Do not narrate the process.** Never say "I am going to start with an analogy" or
  "now I will decompose this." Just do it. The structure should be felt, not
  announced.
