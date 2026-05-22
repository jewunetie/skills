# Worked Examples (Path B: ask_user_input_v0 fallback)

These are example patterns for when the visualizer is unavailable and the elicitation is shaped as choice questions. Each example shows the chat message that precedes the tool call (where rationale and inferences live, since `ask_user_input_v0` has no rationale field), the `ask_user_input_v0` call structure, and any notes on what to do with the response.

For Path A patterns (visualizer form), see `path-a-examples.md` instead. For elicitation that needs free-text input, file uploads, dates, or sliders when the visualizer is unavailable, see the SKILL.md "Path C details" section for the prose fallback.

## Constraint reminder

`ask_user_input_v0` accepts up to three questions per call. Each question accepts 2 to 4 short option labels. The `type` field controls behavior: `single_select` (default), `multi_select`, or `rank_priorities`.

If you have more than three questions, split into rounds (the Extension 5 mapping). If a question needs more than 4 options, consolidate or split into rounds. If you need free text, drop to Path C.

## Example 1: Single question with rationale folded in

Use when one question is enough and you want to communicate why you are asking.

**Chat message before the call:**

```
Quick question before I draft this.
```

**Tool call:**

```python
ask_user_input_v0(questions=[
  {
    "question": "Who is this status update for? This affects how much context I assume and what tone I aim for.",
    "options": ["Direct manager", "Whole team", "Exec leadership", "Client"]
  }
])
```

The rationale ("This affects how much context I assume...") lives inside the question text since there is no separate field. Keep the question and rationale together to roughly 25 words or fewer to stay tappable on mobile.

## Example 2: Multi-question with inference confirmation

Use when you have multiple questions AND you have an inferred answer for at least one of them. The chat message names the inference and its source. The inferred answer is listed first in the options. The user has an explicit escape hatch ("Skip, you decide") if the question itself is misframed.

**Chat message before the call:**

```
Two quick questions to make this useful.

For intensity, I am assuming moderate based on your past mentions of weights and HIIT. Pick something else if that is wrong.
```

**Tool call:**

```python
ask_user_input_v0(questions=[
  {
    "question": "What intensity level should I plan for?",
    "options": ["Moderate (weights, HIIT)", "Bodyweight only", "Advanced lifting", "Skip, you decide"]
  },
  {
    "question": "How many days per week?",
    "options": ["3 days", "4-5 days", "6+ days"]
  }
])
```

Notice the inferred answer ("Moderate") is listed first, the chat message names where the inference came from, and the user has a "Skip, you decide" escape hatch. This is the Path B equivalent of the "Let you decide based on cycle" pattern from Path A Example 2.

## Example 3: Per-question skip with multi-round follow-up

Use when some questions are optional. "Skip this question" goes in the option list. If follow-ups arise from the answers, call `ask_user_input_v0` again in a second round rather than trying to anticipate every branch up front.

**Round 1 chat message:**

```
First pass on cleanup questions.
```

**Round 1 tool call:**

```python
ask_user_input_v0(questions=[
  {
    "question": "Does 'QBR' refer to Quarterly Business Review?",
    "options": ["Yes, Quarterly Business Review", "No, different meaning", "Skip this question"]
  },
  {
    "question": "Should 'preform' be corrected to 'perform'?",
    "options": ["Yes, fix to perform", "No, leave as is", "Skip this question"]
  }
])
```

After the user answers round 1, parse the response. If their answers surface a follow-up question (for example, "No, different meaning" warrants asking what QBR actually stands for), make a second `ask_user_input_v0` call with round-2 questions. This is the Path B form of Extension 5 (multi-round elicitation).

## Example 4: When free text is essential, drop to Path C

Use when the elicitation cannot be expressed as choice questions because free text or open context is what would actually unblock the work.

Scenario: the user wants help writing something, and audience context is the real bottleneck. This is the Path A Extension 4 failure mode (user keeps rejecting option sets because each set lacks context). In Path A you would compose pills plus a textarea; in Path B without the visualizer, that composition is not possible.

**Wrong approach:**

```python
# Forcing free-text into a placeholder option does not work.
# The user has no way to type free text in the response.
ask_user_input_v0(questions=[{
  "question": "Pick a format and tell me about the audience in chat",
  "options": ["Email", "Slack", "Doc"]
}])
```

**Correct approach (Path C prose):**

```
Before I draft this, three things would help. Answer whichever ones you can.

1. **Format.** Email, Slack message, or doc?
2. **Audience.** Who is reading this? Tone and context-density depend on this.
3. **Anything else worth flagging?** Optional. Drop in any context about what they care about or what you want to emphasize.
```

This is the Path A Extension 4 pattern adapted to a no-visualizer world. Pills plus textarea in one form become prose questions where free text is natural.

## Receiving and parsing answers (Path B)

`ask_user_input_v0` returns the user's selections as their next message in this format:

```
Q: <question text>
A: <selected option>
```

Multiple questions stack in the same message, one Q/A pair each. For `multi_select`, the answer line shows the multiple selections joined.

Parse and proceed. If an answer is "Skip this question," treat it as the user opting out, then either infer the answer from context or state what you assumed inline so the user can correct it.
