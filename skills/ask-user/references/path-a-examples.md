# Worked Examples (Path A: Visualizer)

These are full HTML examples for elicitation patterns when the visualizer is available (Mechanism A in SKILL.md). Adapt them to the specific situation. Each example assumes you have already called `visualize:read_me` with the `interactive` and `elicitation` modules and are passing the resulting HTML to `visualize:show_widget`.

If the visualizer is unavailable in this session (Mechanism B fallback), do not use these examples directly. See SKILL.md "Path B details" for how to adapt the same elicitation needs to `ask_user_input_v0`.

The canonical File icon SVG in the header is fixed chrome and must be emitted byte-for-byte. It is reproduced below in each example for reference.

## Example 1: Single-question elicitation

Use when you need exactly one piece of information and a tappable form is faster than a prose question. Even a single question benefits from this format on mobile.

Scenario: the user said "help me write a quick post about our launch" and you need to know the audience.

```html
<form class="elicit">
  <div class="elicit-header">
    <svg viewBox="0 0 20 20" fill="currentColor"><path d="M11.586 2a1.5 1.5 0 0 1 1.06.44l2.914 2.914a1.5 1.5 0 0 1 .44 1.06V16.5a1.5 1.5 0 0 1-1.5 1.5h-9a1.5 1.5 0 0 1-1.492-1.347L4 16.5v-13A1.5 1.5 0 0 1 5.5 2zM5.5 3a.5.5 0 0 0-.5.5v13a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h-2.5A1.5 1.5 0 0 1 11 5.5V3zm7.04 10.304a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696m0-4a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696M12 5.5a.5.5 0 0 0 .5.5h2.293L12 3.207z"/></svg>
    <span>Post details</span>
  </div>
  <div class="elicit-body">
    <div class="elicit-group">
      <label class="elicit-question">Who is the audience for this post?</label>
      <div class="elicit-pills" data-name="audience" data-multi="false">
        <button type="button" class="elicit-pill" data-value="Existing customers">Existing customers</button>
        <button type="button" class="elicit-pill" data-value="Prospects">Prospects</button>
        <button type="button" class="elicit-pill" data-value="Industry peers">Industry peers</button>
        <button type="button" class="elicit-pill" data-value="Internal team">Internal team</button>
        <button type="button" class="elicit-pill" data-value="Other" data-other>Other</button>
      </div>
      <input type="text" class="elicit-other" data-for="audience" placeholder="Tell me who" hidden>
    </div>
  </div>
  <div class="elicit-footer">
    <button type="button" class="elicit-skip">Skip</button>
    <button type="button" class="elicit-submit">Continue</button>
  </div>
</form>
```

## Example 2: Multi-question form with rationale and inference confirmation

Use when several pieces of information are needed and some are inferable from context. This pattern combines plain pills, cards, inference confirmation via rationale, and rationale-driven option ordering.

Scenario: the user asked for a cycle-synced workout and nutrition plan. You inferred a 28-day cycle from an earlier message. Other values you do not know.

```html
<form class="elicit">
  <div class="elicit-header">
    <svg viewBox="0 0 20 20" fill="currentColor"><path d="M11.586 2a1.5 1.5 0 0 1 1.06.44l2.914 2.914a1.5 1.5 0 0 1 .44 1.06V16.5a1.5 1.5 0 0 1-1.5 1.5h-9a1.5 1.5 0 0 1-1.492-1.347L4 16.5v-13A1.5 1.5 0 0 1 5.5 2zM5.5 3a.5.5 0 0 0-.5.5v13a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h-2.5A1.5 1.5 0 0 1 11 5.5V3zm7.04 10.304a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696m0-4a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696M12 5.5a.5.5 0 0 0 .5.5h2.293L12 3.207z"/></svg>
    <span>Plan details</span>
  </div>
  <div class="elicit-body">
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

    <div class="elicit-group">
      <label class="elicit-question">What is your typical workout intensity?</label>
      <p style="font-size: 12px; color: var(--color-text-tertiary); margin: 4px 0 12px 0;">This affects which days I prescribe high-effort sessions versus active recovery.</p>
      <div class="elicit-pills" data-name="intensity" data-multi="false">
        <button type="button" class="elicit-pill" data-value="bodyweight"
          style="border-radius:12px; padding:14px 16px; display:flex; gap:12px; align-items:flex-start; text-align:left; min-width:180px; box-shadow:0 1px 2px rgba(0,0,0,0.04)">
          <i class="ti ti-walk" style="font-size:20px" aria-hidden="true"></i>
          <span>
            <span style="font-size:13px; font-weight:500">Bodyweight</span><br>
            <span style="font-size:11px; color:var(--color-text-tertiary)">Walking, yoga, mobility</span>
          </span>
        </button>
        <button type="button" class="elicit-pill" data-value="moderate"
          style="border-radius:12px; padding:14px 16px; display:flex; gap:12px; align-items:flex-start; text-align:left; min-width:180px; box-shadow:0 1px 2px rgba(0,0,0,0.04)">
          <i class="ti ti-barbell" style="font-size:20px" aria-hidden="true"></i>
          <span>
            <span style="font-size:13px; font-weight:500">Moderate</span><br>
            <span style="font-size:11px; color:var(--color-text-tertiary)">Weights, HIIT, running</span>
          </span>
        </button>
        <button type="button" class="elicit-pill" data-value="advanced"
          style="border-radius:12px; padding:14px 16px; display:flex; gap:12px; align-items:flex-start; text-align:left; min-width:180px; box-shadow:0 1px 2px rgba(0,0,0,0.04)">
          <i class="ti ti-flame" style="font-size:20px" aria-hidden="true"></i>
          <span>
            <span style="font-size:13px; font-weight:500">Advanced</span><br>
            <span style="font-size:11px; color:var(--color-text-tertiary)">Heavy lifting, sport-specific</span>
          </span>
        </button>
        <button type="button" class="elicit-pill" data-value="Let you decide based on cycle">
          Let you decide based on cycle
        </button>
      </div>
    </div>

    <div class="elicit-group">
      <label class="elicit-question">Any dietary restrictions?</label>
      <div class="elicit-pills" data-name="dietary_restrictions" data-multi="true">
        <button type="button" class="elicit-pill" data-value="None">None</button>
        <button type="button" class="elicit-pill" data-value="Vegetarian">Vegetarian</button>
        <button type="button" class="elicit-pill" data-value="Vegan">Vegan</button>
        <button type="button" class="elicit-pill" data-value="Pescatarian">Pescatarian</button>
        <button type="button" class="elicit-pill" data-value="Other" data-other>Other</button>
      </div>
      <input type="text" class="elicit-other" data-for="dietary_restrictions" placeholder="Tell me which" hidden>
    </div>
  </div>
  <div class="elicit-footer">
    <button type="button" class="elicit-skip">Skip</button>
    <button type="button" class="elicit-submit">Continue</button>
  </div>
</form>
```

Three things to notice in this example:

- The first question communicates the inference in the rationale and lists the inferred answer first. The user confirms with a single tap. True prefill (a pill rendering as pre-pressed) is not supported by the platform, so this is the honest workaround.
- The intensity question uses card format because each option benefits from a one-line subtitle. It also has a "Let you decide" escape hatch, which addresses the "the question is wrong, you should figure it out" failure mode.
- The dietary question is multi-select (`data-multi="true"`) because the user might pick more than one.

## Example 3: Hybrid choice plus free-text note

Use when an option choice alone often misses critical context the user wants to provide. The textarea catches that context up front so you do not iterate through three rejected option sets.

Scenario: the user asked for help making a presentation outline sound better. The category alone is not enough to give a good answer; context about the audience or situation is what determines the right tone.

```html
<form class="elicit">
  <div class="elicit-header">
    <svg viewBox="0 0 20 20" fill="currentColor"><path d="M11.586 2a1.5 1.5 0 0 1 1.06.44l2.914 2.914a1.5 1.5 0 0 1 .44 1.06V16.5a1.5 1.5 0 0 1-1.5 1.5h-9a1.5 1.5 0 0 1-1.492-1.347L4 16.5v-13A1.5 1.5 0 0 1 5.5 2zM5.5 3a.5.5 0 0 0-.5.5v13a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h-2.5A1.5 1.5 0 0 1 11 5.5V3zm7.04 10.304a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696m0-4a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696M12 5.5a.5.5 0 0 0 .5.5h2.293L12 3.207z"/></svg>
    <span>Presentation details</span>
  </div>
  <div class="elicit-body">
    <div class="elicit-group">
      <label class="elicit-question">What kind of presentation is this?</label>
      <div class="elicit-pills" data-name="presentation_type" data-multi="false">
        <button type="button" class="elicit-pill" data-value="Status update">Status update</button>
        <button type="button" class="elicit-pill" data-value="Demo">Demo</button>
        <button type="button" class="elicit-pill" data-value="Strategy review">Strategy review</button>
        <button type="button" class="elicit-pill" data-value="Pitch">Pitch</button>
        <button type="button" class="elicit-pill" data-value="Other" data-other>Other</button>
      </div>
      <input type="text" class="elicit-other" data-for="presentation_type" placeholder="Tell me" hidden>
    </div>

    <div class="elicit-group">
      <label class="elicit-question">Anything else I should know about the audience or context?</label>
      <p style="font-size: 12px; color: var(--color-text-tertiary); margin: 4px 0 12px 0;">Optional. The more context, the better I can match tone. For example: have they seen this work before, what is their relationship to the project, what do they care about.</p>
      <textarea class="elicit-textarea" data-name="presentation_context" placeholder="For example: clients who have not seen the app yet, internal team kickoff, board members evaluating renewal."></textarea>
    </div>
  </div>
  <div class="elicit-footer">
    <button type="button" class="elicit-skip">Skip</button>
    <button type="button" class="elicit-submit">Continue</button>
  </div>
</form>
```

The context textarea is the key element. It is the single most reliable fix for the "user keeps rejecting option sets" failure mode, because it surfaces the missing context before you generate the first option set.

## Example 4: Optional questions via per-question skip

Use when some questions are nice to have but should not block submission. The "Skip this question" pill records an explicit skip in the answer payload, distinguishing it from a question the user simply did not see.

Scenario: cleaning up meeting notes where some acronyms might not have known definitions.

```html
<form class="elicit">
  <div class="elicit-header">
    <svg viewBox="0 0 20 20" fill="currentColor"><path d="M11.586 2a1.5 1.5 0 0 1 1.06.44l2.914 2.914a1.5 1.5 0 0 1 .44 1.06V16.5a1.5 1.5 0 0 1-1.5 1.5h-9a1.5 1.5 0 0 1-1.492-1.347L4 16.5v-13A1.5 1.5 0 0 1 5.5 2zM5.5 3a.5.5 0 0 0-.5.5v13a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h-2.5A1.5 1.5 0 0 1 11 5.5V3zm7.04 10.304a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696m0-4a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696M12 5.5a.5.5 0 0 0 .5.5h2.293L12 3.207z"/></svg>
    <span>Notes details</span>
  </div>
  <div class="elicit-body">
    <div class="elicit-group">
      <label class="elicit-question">What does "PbK" refer to in your notes?</label>
      <div class="elicit-pills" data-name="pbk_meaning" data-multi="false">
        <button type="button" class="elicit-pill" data-value="Karpel case management system">Karpel case management system</button>
        <button type="button" class="elicit-pill" data-value="A different system">A different system</button>
        <button type="button" class="elicit-pill" data-value="Skip this question">Skip this question</button>
      </div>
    </div>

    <div class="elicit-group">
      <label class="elicit-question">Should "trail and preliminary date" be corrected to "trial"?</label>
      <div class="elicit-pills" data-name="trail_typo" data-multi="false">
        <button type="button" class="elicit-pill" data-value="Yes, fix to trial">Yes, fix to trial</button>
        <button type="button" class="elicit-pill" data-value="No, leave as is">No, leave as is</button>
        <button type="button" class="elicit-pill" data-value="Skip this question">Skip this question</button>
      </div>
    </div>

    <div class="elicit-group">
      <label class="elicit-question">Anything else worth flagging in the cleanup?</label>
      <textarea class="elicit-textarea" data-name="other_notes" placeholder="Optional. Leave blank if there is nothing."></textarea>
    </div>
  </div>
  <div class="elicit-footer">
    <button type="button" class="elicit-skip">Skip</button>
    <button type="button" class="elicit-submit">Continue</button>
  </div>
</form>
```

When you receive the answers, treat any "Skip this question" value as "use your best inference, flag the assumption inline." Do not re-ask the question in a follow-up form.

## Example 5: Multi-round elicitation

Round one asks the questions you can ask cold. Round two adapts to the answers. The model never tries to encode branching inside a single form.

**Round one:**

The user said "help me plan a trip." You render this form first:

```html
<!-- Header omitted for brevity, header subject: "Trip details" -->
<div class="elicit-body">
  <div class="elicit-group">
    <label class="elicit-question">Where are you going?</label>
    <textarea class="elicit-textarea" data-name="destination" placeholder="City, country, or region"></textarea>
  </div>
  <div class="elicit-group">
    <label class="elicit-question">When?</label>
    <input type="date" class="elicit-date" data-name="start_date">
  </div>
  <div class="elicit-group">
    <label class="elicit-question">How long?</label>
    <input type="range" data-name="trip_length" min="1" max="30" step="1" value="7">
  </div>
</div>
```

The user submits: `Trip details — Destination: Tokyo · Start date: 2026-06-15 · Trip length: 10`.

**Round two:**

Now that you know it is Tokyo for 10 days in June, ask follow-ups that are specific to that context. Render a new form:

```html
<!-- Header subject: "Tokyo trip details" -->
<div class="elicit-body">
  <div class="elicit-group">
    <label class="elicit-question">Have you been to Tokyo before?</label>
    <div class="elicit-pills" data-name="prior_visits" data-multi="false">
      <button type="button" class="elicit-pill" data-value="First time">First time</button>
      <button type="button" class="elicit-pill" data-value="Been once or twice">Been once or twice</button>
      <button type="button" class="elicit-pill" data-value="Familiar with the city">Familiar with the city</button>
    </div>
  </div>
  <div class="elicit-group">
    <label class="elicit-question">June is peak rainy season. Comfortable working around that?</label>
    <div class="elicit-pills" data-name="weather_tolerance" data-multi="false">
      <button type="button" class="elicit-pill" data-value="Fine with rain plans">Fine with rain plans</button>
      <button type="button" class="elicit-pill" data-value="Prefer outdoor focus">Prefer outdoor focus</button>
      <button type="button" class="elicit-pill" data-value="Mix of both">Mix of both</button>
    </div>
  </div>
</div>
```

The round-two questions only make sense once you know the destination and timing. Trying to encode "if Tokyo, ask about prior visits and rainy season" inside a single form would require branching logic that the shell does not support. The two-round pattern handles it cleanly.

## Example 6: File upload with textarea fallback

Use when the skill needs documents or data the user might have as a file. The native `.elicit-files` group includes a paired textarea so the user can paste content if they do not have a file handy.

```html
<div class="elicit-group">
  <label class="elicit-question">Upload the source document (or paste the relevant text below):</label>
  <div class="elicit-files" data-name="source_doc">
    <label class="elicit-dropzone">
      <svg viewBox="0 0 20 20" fill="currentColor"><path d="M16.5 13a.5.5 0 0 1 .5.5v2a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 3 15.5v-2a.5.5 0 0 1 1 0v2a.5.5 0 0 0 .5.5h11a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 1 .5-.5M10 3a.5.5 0 0 1 .374.168l4 4.5.059.082a.5.5 0 0 1-.732.65l-.075-.068L10.5 4.814V13.5a.5.5 0 0 1-1 0V4.814L6.374 8.332a.5.5 0 0 1-.748-.664l4-4.5.08-.071A.5.5 0 0 1 10 3"/></svg>
      <span>Choose file</span>
      <input type="file" multiple>
    </label>
  </div>
  <textarea class="elicit-textarea" data-name="source_doc_text" placeholder="Or paste the relevant content here"></textarea>
</div>
```

Selected files are attached to the conversation. On submit you will see `Source doc: filename.pdf (attached)` in the payload and can read the file via the conversation's attachments. If the user already uploaded the file before invoking the skill, skip this group entirely.

## Example 7: Bidirectional clarification (the user can ask back)

Use whenever you render a Path A form. This is not optional; every Path A form should include the "Ask me something first" textarea so the user can clarify questions in-place rather than abandoning the form.

This example shows the pattern attached to the cycle-tracking form from Example 2. The new textarea sits at the bottom, just before the footer.

```html
<form class="elicit">
  <div class="elicit-header">
    <svg viewBox="0 0 20 20" fill="currentColor"><path d="M11.586 2a1.5 1.5 0 0 1 1.06.44l2.914 2.914a1.5 1.5 0 0 1 .44 1.06V16.5a1.5 1.5 0 0 1-1.5 1.5h-9a1.5 1.5 0 0 1-1.492-1.347L4 16.5v-13A1.5 1.5 0 0 1 5.5 2zM5.5 3a.5.5 0 0 0-.5.5v13a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h-2.5A1.5 1.5 0 0 1 11 5.5V3zm7.04 10.304a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696m0-4a.5.5 0 0 1 .92.392c-.295.69-.871 1.304-1.66 1.304-.487 0-.892-.234-1.2-.574-.309.34-.713.574-1.2.574-.486 0-.892-.233-1.2-.574-.31.34-.714.574-1.2.574a.5.5 0 0 1 0-1c.212 0 .52-.18.74-.696l.034-.067a.5.5 0 0 1 .886.067c.221.516.528.696.74.696.213 0 .52-.18.74-.696l.035-.067a.5.5 0 0 1 .885.067c.22.516.527.696.74.696s.519-.18.74-.696M12 5.5a.5.5 0 0 0 .5.5h2.293L12 3.207z"/></svg>
    <span>Plan details</span>
  </div>
  <div class="elicit-body">
    <!-- Existing elicit-groups for cycle length, intensity, dietary restrictions go here -->

    <div class="elicit-group">
      <label class="elicit-question">Ask me something first?</label>
      <p style="font-size: 12px; color: var(--color-text-tertiary); margin: 4px 0 12px 0;">Optional. If anything in the form is unclear, ask here and I will answer before you commit to choices.</p>
      <textarea class="elicit-textarea" data-name="ask_claude" placeholder="For example: What does Other mean for cycle length? Why is intensity affecting recovery days?"></textarea>
    </div>
  </div>
  <div class="elicit-footer">
    <button type="button" class="elicit-skip">Skip</button>
    <button type="button" class="elicit-submit">Continue</button>
  </div>
</form>
```

When the answer payload comes back, check `Ask me something first` first. If non-empty:

1. Answer the user's question in chat first, in plain prose. Keep it tight; the user wants to get back to the form.
2. State the user's previous picks in the prose lead-in so they do not have to scroll up. The form is stateless, and pill prefilling does not work; the prose summary is the only way to remind them what they had.
3. Re-render the form with the same questions. Update the rationale text on any question whose answer is now clearer in light of the clarification. For any textarea where the user wrote content in the previous round, set the placeholder to that previous content so they can see what they typed without auto-filling.
4. Skip the probe on this re-render. The platform cannot have switched between the user's submit and your response within the same conversational turn.

Example response when the user filled in cycle length=28 days, intensity=moderate, dietary=vegetarian, and asked "What does Other mean for cycle length?":

> "Other" lets you type a number that is not 24, 28, or 30 days. If your typical cycle is something like 26 or 32 days, pick Other and type the number. Re-rendering the form below. Your earlier picks were Cycle length=28 days, Intensity=moderate, Dietary=vegetarian. Keep them or change based on this clarification.
>
> [render the form again, with `placeholder="vegetarian"` on the dietary textarea if it is rendered as free-text]

Do not over-explain or add unrelated context. The clarification should be the minimum needed to answer the specific question. The previous-picks summary should be one line, not a re-explanation.

## Receiving answers across all examples

The native answer-return contract: pills return their `data-value`, multi-select pills comma-join, textareas return their full content (folded under `--- Full content ---` if long), file uploads return `(attached)` markers and the file is added to the conversation. The Skip button at the form footer returns `(Skipped the form — proceed with defaults or ask me in plain text)`.

The `data-name` field becomes the human-readable label in the payload (`cycle_length` becomes `Cycle length`, `ask_claude` becomes `Ask claude` or similar). Path the answers by name, not by position.
