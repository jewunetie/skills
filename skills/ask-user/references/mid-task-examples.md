# Worked Examples: Mid-task elicitation (Pausing for ambiguity)

These examples show how to pause during agentic execution when ambiguity surfaces in flight, distinct from upfront elicitation. The mechanism is the same as Path A or Path B, but the framing is different. Read this file when constructing a pause during work, not before.

For upfront elicitation patterns, see `path-a-examples.md` and `path-b-examples.md`.

## When to pause: the internal check

Before pausing, run an internal clarification check. At each step of the task, generate a few candidate clarification questions silently and ask: would the user's answer materially change my next action? If yes, pause. If no, proceed and note the choice in your action trace.

This is the Morae pattern (Peng et al., UIST 2025). The point of the internal check is to filter pauses to ones the user actually cares about, rather than pausing on every borderline case.

## Example 1: Mid-categorization pause

Scenario: You are processing a list of 50 receipts and assigning each a category. Halfway through, you hit a receipt for "Walmart $87.43" with no other detail. Walmart could be groceries, household supplies, electronics, or clothing.

**Internal check.** Multiple plausible categories exist. The category affects downstream tax handling. You have not received guidance on this specific case. Pause.

**Path A pause widget:**

```html
<form class="elicit">
  <div class="elicit-header">
    <svg viewBox="0 0 20 20" fill="currentColor"><!-- File icon, see read_me --></svg>
    <span>Receipt 24 details</span>
  </div>
  <div class="elicit-body">
    <div class="elicit-group">
      <label class="elicit-question">How should I categorize this Walmart receipt?</label>
      <p style="font-size: 12px; color: var(--color-text-tertiary); margin: 4px 0 12px 0;">Walmart $87.43, no item detail. I have processed 23 of 50 receipts. The category affects tax handling.</p>
      <div class="elicit-pills" data-name="category" data-multi="false">
        <button type="button" class="elicit-pill" data-value="Groceries">Groceries</button>
        <button type="button" class="elicit-pill" data-value="Household supplies">Household supplies</button>
        <button type="button" class="elicit-pill" data-value="Other">Other</button>
        <button type="button" class="elicit-pill" data-value="Apply this choice to all unspecified Walmart receipts">Apply this choice to all unspecified Walmart receipts</button>
      </div>
    </div>

    <div class="elicit-group">
      <label class="elicit-question">Ask me something first?</label>
      <textarea class="elicit-textarea" data-name="ask_claude" placeholder="Optional"></textarea>
    </div>
  </div>
  <div class="elicit-footer">
    <button type="button" class="elicit-skip">Skip</button>
    <button type="button" class="elicit-submit">Continue</button>
  </div>
</form>
```

Three things to notice:

1. **Brief context, not a re-explanation.** "Walmart $87.43, no item detail. 23 of 50 receipts." The user does not need a recap of the whole task.
2. **The "apply to all" option short-circuits future pauses.** If the user expects more Walmart receipts, picking this means you will not pause again on the same kind of ambiguity.
3. **Bidirectional clarification (Extension 6) is still present.** The user can ask "what does the IRS rule say about ambiguous Walmart receipts" and have you answer before they commit.

After the answer, resume processing receipts 25 through 50. Apply the user's policy to similar ambiguities downstream if they picked "apply to all."

## Example 2: Mid-tool-call pause

Scenario: You are using a code search tool to find references to a function across a codebase. The tool returns results from two repositories: the main repo (which the user clearly meant) and a vendor repo with a function of the same name. You need to know whether to include vendor matches.

**Internal check.** The user said "find all uses of `parseUserInput`." They probably meant the main repo. But including vendor matches changes the answer set in a way they might or might not want. Pause.

**Path B fallback (assume the visualizer is unavailable here):**

Chat message:

```
Found 47 matches for parseUserInput. 41 are in your main repo, 6 are in vendor/lodash-internal. Quick check before I show them.
```

Tool call:

```python
ask_user_input_v0(questions=[{
  "question": "Include vendor matches in the results?",
  "options": ["Main repo only", "Include vendor matches", "Apply this choice to all future searches in this session"]
}])
```

The "apply to all future searches" option is the recurring-ambiguity pattern: instead of pausing on every search, ask once and remember.

## Example 3: Pre-empting recurring ambiguity at task start

Scenario: User asks you to clean up a Notion database with 200 entries. You can see at task start that several columns have inconsistent formatting (mixed date formats, capitalization variations, occasional typos). Pausing on every entry would be hostile.

**Better pattern: ask once at the start about the policy, then apply it.**

This is upfront elicitation, not mid-task elicitation. The goal is to avoid mid-task pauses that the user would experience as spam.

```python
ask_user_input_v0(questions=[
  {
    "question": "How should I handle inconsistent date formats?",
    "options": ["Normalize all to YYYY-MM-DD", "Keep what is there, just fix obvious errors", "Stop and ask each time"]
  },
  {
    "question": "How should I handle obvious typos?",
    "options": ["Fix silently", "Fix and flag in a summary", "Skip, leave as is"]
  },
  {
    "question": "How should I handle capitalization inconsistencies?",
    "options": ["Title Case all entries", "Sentence case all entries", "Leave as is"]
  }
])
```

After this, do not pause again on date/typo/case ambiguities; apply the policies the user picked. Pause only for genuinely novel ambiguities the upfront elicitation did not cover.

## Choosing between mid-task pause and upfront policy

Pause mid-task when:

- The ambiguity is rare or one-off (does not recur across the task).
- The cost of being wrong is high relative to the cost of asking.
- You could not have predicted the ambiguity at task start.

Use upfront policy elicitation when:

- The ambiguity recurs across many similar items.
- Pausing each time would feel like spam.
- The class of decisions can be summarized in a small number of policy questions.

When in doubt, lean toward upfront policy for predictable recurring ambiguities and mid-task pause for genuinely novel ones.

## Resuming after a pause

After the user answers, resume immediately. Do not:

- Re-summarize what you have already done. The user did not forget.
- Ask follow-up questions about the rest of the task. They authorized that work at the start.
- Add commentary unless the answer warrants it (for example, if their choice surfaces a problem you should flag).

The user's mental model is that the task was paused for one specific reason; they expect to be back to "task is running" right after.
