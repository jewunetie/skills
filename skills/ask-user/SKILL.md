---
name: ask-user
description: Use this skill whenever you need to elicit context, preferences, constraints, or choices from the user before proceeding. This is the default mechanism for all user-facing elicitation. The skill picks the best available tool, choosing a rich inline form (with cards, free-text, file uploads, multi-select, dates, sliders, and multi-round flows) when the visualizer is loaded, falling back to ask_user_input_v0 for choice questions, and prose for everything else. Trigger this any time you would otherwise ask a clarifying question in prose, call ask_user_input_v0 directly, or write a numbered list of questions for the user. This includes requests where intent is underspecified, decisions between options, gathering preferences for a recommendation, confirming assumptions before producing a deliverable, or collecting form-like data. Replaces ask_user_input_v0 as the default elicitation mechanism.
---

# Ask User

The default mechanism for asking the user for context, preferences, or choices. The skill picks the best elicitation tool that actually works in the current session, calibrates how much elicitation to do based on stakes, prioritizes which questions are worth asking, and adapts the question structure to the chosen tool.

This skill replaces direct calls to `ask_user_input_v0` and supersedes prose-style clarifying questions for any case where you would normally ask the user a structured question.

## Quick reference

The full flow when this skill triggers:

1. Run the infer-first check. If the answer is determinable from context, do not ask. State the assumption and proceed.
2. Calibrate by stakes. Decide how much elicitation rigor is justified by what the answer authorizes you to do.
3. Construct questions. Rank by expected information gain. Default to one question per turn. Use challenge mode for high-effort work that may be misframed.
4. Probe the visualizer with `visualize:read_me`. Silent if it fails.
5. Pick a mechanism (A, B, or C) based on the probe result and the elicitation needs.
6. Construct and call. If the call fails, fall back to the next mechanism.
7. Parse the response. If the user asked a question back via the bidirectional clarification field, answer first and re-render. If follow-ups are needed, run the same flow again with a fresh probe.

## When to use

Use this skill when:

- The user's request is underspecified and you need their input to proceed.
- You are about to write clarifying questions in prose. Stop and use this skill instead.
- You are about to call `ask_user_input_v0` directly. Stop and use this skill instead.
- You need to confirm assumptions before producing a deliverable that takes meaningful work.
- You are mid-task and have hit ambiguity that requires user input. See "Mid-task elicitation" below.

Do not use this skill when:

- The answer is already in context, in past chats, or inferable from stated preferences. The infer-first check is non-negotiable.
- The conversation is in active back-and-forth and a single follow-up question fits naturally as prose. Forms have setup overhead.
- The work is low-stakes and reversible (see stakes calibration below). Producing a useful first attempt and letting the user redirect is often better than asking.
- The user is venting, processing emotions, or asking for your opinion. Forms collect data; they are not for emotional or deliberative dialogue.

## Calibrate by stakes

Before picking a mechanism, decide how much elicitation rigor is justified by what the answer authorizes you to do. Three tiers:

**Low-stakes, reversible.** Drafts, suggestions, exploratory work the user reviews and can redo. Skip elicitation: infer, produce a useful first attempt, let the user redirect. Cost of wrong: the user types a follow-up. Cost of asking: the user types more than they would have, plus a delay.

**Medium-stakes.** Work that takes meaningful effort to redo, or has minor downstream consequences. One question, prefer one-tap confirm patterns (see Path A Extension 2 inference confirmation). Keep the rest inferred.

**High-stakes, irreversible.** External actions, financial transactions, deletions, sending communications, anything the user cannot easily undo. Full form with explicit confirms on every consequential parameter. Consider re-confirming the whole plan before action. For the highest stakes, switch to suggest-only mode: prepare the action and have the user execute it themselves rather than acting on their behalf.

Match elicitation density to the tier. Heavy elicitation on low-stakes work is friction. Light elicitation on high-stakes work is recklessness.

## Infer first

Before constructing any elicitation, run this check:

1. Scan the current conversation for stated preferences, constraints, prior answers, and explicit context.
2. If `conversation_search` or `recent_chats` is available, search past chats for prior context on the same topic.
3. Read uploaded files for context the user expects you to use.
4. Only ask about things you genuinely cannot determine.

If you can infer everything, skip the elicitation, state the assumption explicitly, and proceed. When you do infer some answers, include them as options and communicate the inference in the rationale (Path A Extension 2). The user confirms or corrects with a single tap.

## Question construction

Once you know what you genuinely cannot infer, three sub-decisions remain.

### Rank by expected information gain

When multiple candidate questions remain after the infer-first check, rank them by which answer most narrows your downstream decisions.

For each candidate, mentally simulate two or three plausible answers and ask: do my actions branch differently across those answers? Questions where the answer changes everything beat questions where it barely changes anything.

Example. User asks for a workout plan. Candidates: (a) goal (strength vs cardio vs flexibility); (b) days per week; (c) equipment access. Question (a) determines what every other answer means: a strength plan and a cardio plan use different intensity scales and equipment lists. Question (a) has the highest information gain. Asking (b) first wastes the turn because (b) only matters once (a) is known.

Ask the highest-information-gain question first or alone. Drop low-information-gain questions even if they are easy to phrase.

### One question at a time, by default

The default is single-question elicitation. Render one question, get the answer, decide the next question based on that answer, render the next one. This adapts: later questions can change or disappear depending on earlier answers.

Use multi-question forms only when both:

1. The questions are genuinely independent. No answer changes another's relevance, wording, or set of valid options.
2. The user is on a high-bandwidth surface where parallel questions read well. Path A on desktop is fine; Path B on mobile is friction.

Adaptive sequencing usually produces shorter total interactions than batch elicitation, even though it takes more turns, because later questions get skipped or refined based on earlier answers.

### Challenge mode for high-effort goals

When the user request specifies the form ("write me an email," "build a landing page") rather than the goal ("drive signups," "introduce the product"), and the deliverable takes meaningful work, lead with a goal-clarifying question.

Pattern: "Before I [build the thing], what outcome are you trying to drive? That shapes [name two or three structural decisions]."

The goal question often outranks all detail questions on information gain, because the wrong goal produces a polished delivery of the wrong thing.

Apply selectively. For trivial requests, the goal is obvious. For very high-trust contexts where the user has thought through the goal already, meta-questions feel paternalistic. Reserve challenge mode for genuinely high-effort work where misalignment is costly to recover from.

## Mechanism selection

Three mechanisms in priority order. Pick the highest-priority one that fits the elicitation needs and is actually available.

### Mechanism A: Visualizer form (preferred when available)

The richest option. Supports cards, free-text inputs, file uploads, dates, sliders, multi-select with comma-join, rich layouts, and bidirectional clarification (Extension 6). Use when:

- The visualizer is loaded.
- AND the elicitation benefits from features the visualizer provides (free-text, file upload, sliders, dates, cards with subtitles), OR the elicitation has 4+ questions where ask_user_input_v0's three-question cap is limiting.

**Probe at every fresh elicitation moment.** The visualizer's availability tracks the user's platform, and the user can switch between mobile and desktop multiple times within a single conversation. State from earlier in the conversation is not authoritative.

**Exception: re-renders within the same turn.** When you are re-rendering a form in direct response to a bidirectional clarification (Extension 6) within the same conversational turn, the previous probe and successful render are sufficient evidence. The user just submitted moments ago; the platform cannot have switched between their submit and your response. Skip the redundant probe and re-render directly. This rule applies only to the immediate re-render that follows your answer to a clarification request, not to subsequent fresh elicitations later in the conversation.

**Probe via `visualize:read_me` first.** This is a silent call. If `read_me` fails with "Tool not found" or similar, the visualizer is unavailable in the current session: fall back to Mechanism B without attempting `show_widget`. If `read_me` succeeds, proceed to construct and call `show_widget`. If `show_widget` fails despite a successful probe (the two tools can fail independently), fall back to Mechanism B.

See "Path A details" below.

### Mechanism B: ask_user_input_v0 (fallback for choice questions)

Use when:

- The visualizer probe failed or `show_widget` errored at call time.
- AND the elicitation can be expressed entirely as choice questions (single select, multi select, or rank).

`ask_user_input_v0` supports up to three questions per call. It does not support free-text input, rationale fields, file uploads, dates, or sliders. Adapt using "Path B details" below.

### Mechanism C: Prose fallback

Use when:

- Neither A nor B works, OR
- The elicitation requires free text, file uploads, dates, sliders, or more than three questions, AND the visualizer probe failed.

A short numbered list of questions in chat, with rationale inline.

---

## Path A details: Visualizer form

When using Mechanism A, follow the patterns in this section.

### Setup

Always call `visualize:read_me` with modules `["interactive", "elicitation"]` before building the form. This call serves two purposes: it probes whether the visualizer is currently loaded, and it returns the canonical SVG header, locked CSS classes, choice-input formats, and answer-return contract.

If `read_me` returns an error, the visualizer is unavailable. Fall back to Mechanism B. Do not attempt `show_widget` in this case.

### Form structure

The shell:

```html
<form class="elicit">
  <div class="elicit-header">
    <svg viewBox="0 0 20 20" fill="currentColor"><!-- canonical File icon, see read_me --></svg>
    <span>[Subject] details</span>
  </div>
  <div class="elicit-body">
    <!-- .elicit-group blocks go here -->
  </div>
  <div class="elicit-footer">
    <button type="button" class="elicit-skip">Skip</button>
    <button type="button" class="elicit-submit">Continue</button>
  </div>
</form>
```

Header subject is `[noun] details`. Pick the noun that names the elicitation object: "Trip details," "Recipe details," "Document details."

Choice formats available natively: plain pills (short labels), cards (with subtitles), preview tiles (with thumbnails), sliders, dates, textareas, file upload with paired textarea. Vary the format; an all-pills form reads flat.

### Extensions

The visualizer's elicitation system covers most needs natively. The following extensions address gaps.

#### Extension 1: Per-question rationale

Add a small muted rationale element directly below the question label when the question is non-obvious or its answer materially affects later questions.

```html
<div class="elicit-group">
  <label class="elicit-question">What is your typical workout intensity?</label>
  <p style="font-size: 12px; color: var(--color-text-tertiary); margin: 4px 0 12px 0;">This determines whether I recommend high-effort sessions or active recovery on each day.</p>
  <div class="elicit-pills" data-name="intensity" data-multi="false">
    <!-- pills -->
  </div>
</div>
```

Use sparingly. Rationale on every question makes the form verbose.

#### Extension 2: Inference confirmation

The native form does not support pre-selected options at render time. Setting `aria-pressed="true"` is overridden by the auto-wiring's init pass. Communicate the inference in the rationale and list the inferred answer first; the user confirms with a single tap.

```html
<div class="elicit-group">
  <label class="elicit-question">What is your cycle length?</label>
  <p style="font-size: 12px; color: var(--color-text-tertiary); margin: 4px 0 12px 0;">I am assuming 28 days based on what you said earlier. Tap that to confirm, or pick a different option.</p>
  <div class="elicit-pills" data-name="cycle_length" data-multi="false">
    <button type="button" class="elicit-pill" data-value="28 days">28 days</button>
    <button type="button" class="elicit-pill" data-value="24 days">24 days</button>
    <button type="button" class="elicit-pill" data-value="30 days">30 days</button>
    <button type="button" class="elicit-pill" data-value="Other" data-other>Other</button>
  </div>
  <input type="text" class="elicit-other" data-for="cycle_length" placeholder="Number of days" hidden>
</div>
```

#### Extension 3: Per-question optional flagging

Include an explicit "Skip this question" pill as the last option in groups where the question is genuinely optional.

#### Extension 4: Hybrid choice plus free-text note

Compose with two adjacent groups: a pills group for the choice and a textarea group for the note. The canonical fix for the failure mode where users keep rejecting option sets because each set lacks context.

#### Extension 5: Multi-round elicitation

The form submits once. Render round one, parse the answers, decide what follow-ups are actually needed, render round two. Branching lives in your reasoning, not in the form. This is also the default given the "one question at a time" pacing rule.

#### Extension 6: Bidirectional clarification (the user can ask back)

Forms are imperfect, and users sometimes need clarification on a question or option before they can answer. Without an in-form path to ask, the user has to abandon the form, type their question in chat, wait for an answer, and re-engage. This is friction the form is supposed to remove.

Add a textarea at the bottom of every Path A form labeled "Ask me something first." If the user fills it on submit, treat the text as a clarification request rather than a final answer.

```html
<div class="elicit-group">
  <label class="elicit-question">Ask me something first?</label>
  <p style="font-size: 12px; color: var(--color-text-tertiary); margin: 4px 0 12px 0;">Optional. If anything in the form is unclear, ask here and I will answer before you commit to choices.</p>
  <textarea class="elicit-textarea" data-name="ask_claude" placeholder="For example: What does option B mean specifically? How is this different from X?"></textarea>
</div>
```

When parsing the response, if `ask_claude` is non-empty:

- Answer the user's question in chat first, in plain prose. Keep the answer tight; the user wants to get back to the form.
- Re-render the form. Update the rationale text on any question whose answer is now clearer in light of your reply.
- Do not assume the user's other answers are final; they may have answered some fields under uncertainty before asking.

**State preservation across re-renders.** The form is stateless. When you re-render, all selections are lost; the user has to re-pick everything. This is friction. Mitigate it with two techniques on every re-render triggered by Extension 6:

1. **State the user's previous picks in the prose lead-in.** Example: "Your earlier picks were Goal=strength, Equipment=Machines+Cardio machines, Days=4 days, Schedule=afternoons on weekdays. Keep them or change based on the clarification." This lets the user see what they had without scrolling, and decide whether the clarification changes anything.
2. **Use the user's previous textarea content as the placeholder on re-rendered textareas.** This shows them what they had typed without auto-filling it (placeholders disappear on focus, so they can type fresh or just copy from memory). For example: `<textarea ... placeholder="afternoons on weekdays"></textarea>` if that was their previous note. This is not a true prefill, but it removes the "what did I say last time" friction.

For pills, prefilling with `aria-pressed="true"` does not work (the auto-wiring resets it). The prose summary is the only available reminder. Make it a habit, not an afterthought.

**Skip the probe on the re-render.** Per the Mechanism A exception: a re-render in direct response to a bidirectional clarification within the same conversational turn does not need a fresh probe. The user just submitted; the platform cannot have switched.

This pattern is mainstream practice in conversational elicitation (Juji guidance) and aligns with mixed-initiative dialogue (Hearst 1999 and continuing). Always include the textarea on Path A forms.

### Receiving the answers (Path A)

After submit, the next message arrives as:

```
[Subject] details — Question label: Value · Other label: Value, Value · ...
```

Multi-select values are comma-joined. Long textarea values are quoted or folded under `--- Full content ---`. If the user clicked the global Skip, the message is `(Skipped the form — proceed with defaults or ask me in plain text)`.

If `ask_claude` (Extension 6) is non-empty, treat the form as a clarification request and re-render after answering.

If a per-question skip pill was selected, proceed with the answered questions and either infer the rest or state your assumption inline.

---

## Path B details: ask_user_input_v0 fallback

When the visualizer is unavailable, fall back to `ask_user_input_v0`.

### Mapping from extensions

- **Single or multi select.** Native via `type: single_select` or `type: multi_select`.
- **Per-question rationale (Extension 1).** No rationale field. Communicate rationale in the chat message that precedes the tool call.
- **Inference confirmation (Extension 2).** State the inference in chat, then list the inferred answer first in options.
- **Per-question skip (Extension 3).** Add "Skip this question" as one of the option labels.
- **Hybrid pills plus free-text note (Extension 4).** `ask_user_input_v0` cannot do free-text. If the note is essential, drop to Mechanism C. If optional, ask the choice question via `ask_user_input_v0` and the free-text follow-up in prose.
- **Multi-round (Extension 5).** Call again with follow-ups based on the first round's answers.
- **Bidirectional clarification (Extension 6).** No free-text path. Workaround: include "I have a question first" as one option in the most relevant question. If the user picks it, prompt them in chat to type their question, answer it, and re-call `ask_user_input_v0` with the same questions (possibly with updated wording).
- **Free-text only, dates, sliders, file uploads.** `ask_user_input_v0` cannot handle these. Drop to Mechanism C.

### Cap on questions

Three questions per call. For larger needs, split into rounds (the multi-turn default applies here too).

### Receiving the answers (Path B)

`ask_user_input_v0` returns selections as the next user message in `Q: ... A: ...` format, one Q/A pair per question. For `multi_select`, the answer line shows multiple selections joined.

---

## Path C details: Prose fallback

When neither A nor B works, ask in prose. A short numbered list, each with rationale inline. The user can answer in any order; you parse what they said.

```
Before I draft this, three things would help. Answer whichever ones you can.

1. **Audience.** Who is reading this? Tone and context-density depend on this.
2. **Length.** Quick (3-4 sentences), medium (1-2 paragraphs), or detailed (multi-paragraph)?
3. **Anything else worth flagging?** Optional. Drop in any context about what they care about.
```

Cap at three to five questions; beyond that the user reads less carefully. Bidirectional clarification is naturally supported (the user can ask anything back in their reply).

---

## Mid-task elicitation: pausing for ambiguity during work

Sometimes ambiguity surfaces during execution, not before. You are mid-categorization, mid-rewrite, or mid-tool-use, and the next step has multiple plausible interpretations. The mechanism is the same as upfront elicitation, but the framing differs.

### When to pause

At each step of an agentic task, internally ask: do multiple plausible interpretations of this step exist that would lead to materially different outcomes? If yes, and the cost of being wrong exceeds the cost of asking, pause. If no, or the difference is trivial and reversible, proceed.

This is the Morae pattern (Peng et al., UIST 2025): generate internal clarification questions silently, externalize them only when they identify critical ambiguity. Two failure modes: pausing too often (precision error, breaks flow) and missing pauses (recall error, silent mistakes). Lean toward pausing on consequential decisions and proceeding on cosmetic ones.

### How to pause

Probe for the visualizer, pick Path A or B, render an elicitation widget for the specific ambiguity. The framing differs from upfront elicitation:

- Make the context clear: "I am [mid-task]. The next step has [N options]. Which do you prefer?"
- Show what you are paused on, not what is finished. The user does not need to re-confirm decisions you have already made.
- Resume immediately after the answer. Do not collect more elicitation rounds than necessary.

### When not to pause

Pausing has a cost: it breaks the user's flow. Do not pause for choices that are easy to undo after task completion, choices where one option is dominant under stated preferences, or choices that recur frequently in similar form.

For frequently recurring ambiguities, prefer upfront elicitation: ask once at task start about how to handle a class of decisions, then apply that policy across the task.

See `references/mid-task-examples.md` for worked examples.

---

## Common mistakes to avoid

- Calling `ask_user_input_v0` directly without going through this skill's flow. The skill prescribes stakes calibration, information-gain ranking, and inference handling that bare calls miss.
- Asking a question that the conversation already answers. Run the infer-first check.
- Treating low-stakes and high-stakes elicitation the same. Match density to the tier.
- Asking questions in any order. Rank by expected information gain; the pivotal question goes first.
- Defaulting to multi-question batch forms. The default is one question per turn; batch is for genuinely independent questions on a high-bandwidth surface.
- Asking only detail questions when the user might have specified the wrong form. For high-effort work, lead with a goal-clarifying question (challenge mode).
- Adding rationale to every single question. Use Extension 1 sparingly.
- Setting `aria-pressed="true"` on a pill to prefill a selection. This does not work.
- Trying to add `<script>` for branching logic. Use multi-round elicitation instead.
- Putting the elicitation behind a wall of prose. Lead in with one short sentence.
- Restyling the locked shell elements (`.elicit-header`, `.elicit-body`, `.elicit-footer`, `.elicit-question`).
- Caching visualizer availability state from earlier in the conversation. Probe at every fresh elicitation moment. The within-turn re-render exception (Extension 6) does not extend to subsequent fresh elicitations.
- Calling `visualize:show_widget` without first probing via `visualize:read_me`. Failed `show_widget` renders the failure visibly; failed `read_me` is silent.
- Forcing users to abandon the form to ask a clarification. Always include the bidirectional clarification textarea (Extension 6).
- Re-rendering after a bidirectional clarification without surfacing the user's previous answers. The form is stateless; without a prose summary of their earlier picks and placeholders showing prior textarea content, the user has to recall what they had. Both techniques are mandatory on every Extension 6 re-render.
- Probing the visualizer redundantly on a within-turn re-render. The platform cannot switch between the user's submit and your response. Re-render directly.
- Asking everything upfront when ambiguity will surface mid-task. Use the mid-task pausing pattern for choices that only become apparent in flight.

## Worked examples

The reference files are split by mechanism and pattern. Load the one that matches what you are constructing.

- `references/path-a-examples.md` for visualizer-form patterns: single question, multi-question with rationale and inference confirmation, hybrid choice plus free-text note, optional questions via per-question skip, multi-round elicitation, file upload pattern, bidirectional clarification.
- `references/path-b-examples.md` for `ask_user_input_v0` fallback patterns: single question with rationale folded in, multi-question with inference confirmation, per-question skip with multi-round follow-up, and how to bridge to Path C when free text is essential.
- `references/mid-task-examples.md` for pausing patterns during agentic execution: ambiguity detection, framing the pause, resuming cleanly, batching recurring ambiguities into upfront policies.

Read the relevant file when constructing your elicitation so the patterns are fresh.
