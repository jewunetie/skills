# Skill, Spec, and Prompt Review Reference

Per-pass categories for reviewing artifacts that instruct an AI agent or another person: skills, specs, prompts, agent configurations, instruction documents.

## Pass 1: Surface

- YAML frontmatter syntax (required for skills): is it valid, are required fields present (name, description)
- Skill name matches the folder name and is consistent across all references
- Code blocks in examples: do they actually parse, are language hints correct
- Broken inline references: links to files that do not exist, references to sections that were renamed
- Formatting violations against user preferences (em-dashes, contractions, emojis)
- Inconsistent terminology for the same concept ("pass" vs "iteration" vs "round")
- All-caps imperatives (MUST, ALWAYS, NEVER) without explanatory context: per Anthropic's skill guidance, prefer explaining why over commanding
- Typos in trigger phrases (these matter; a typo in a trigger means the skill never fires)

## Pass 2: Logic and internal consistency

- Are instructions internally consistent? Section A saying "always X" while section B saying "X only when Y" is a contradiction
- Are all referenced files, scripts, or sections actually present in the skill?
- Do examples match the rules stated in the skill body?
- Is every step in a workflow actually reachable? Do the conditions for each step match the conditions for getting there?
- Are the trigger phrases in the description actually findable in the skill body, and do they match user phrasing in the wild?
- Does the skill describe edge cases and what to do when the happy path fails?
- Are completion criteria unambiguous? "Done when no issues remain" is ambiguous; "done when a full pass over Pass 1-4 finds zero new fixes" is unambiguous
- Are gotchas backed by real failure modes, or invented?
- Does the skill explain why rules exist, not just what the rules are? Generalizable wisdom requires the why

## Pass 3: Cross-reference

- Skill description: does it match Anthropic's skill design guidance? Is it pushy enough to trigger reliably? Are the triggers specific?
- Skill body: does it stay under approximately 500 lines, with detail pushed to references/?
- User's actual past usage: does the skill cover the situations the user has actually encountered? (Search past chats if relevant.)
- Conflict with other skills the user has installed: if this skill overlaps with another, is the relationship explicit?
- Does the skill respect user preferences globally (no em-dashes, no contractions in file outputs, etc.)?
- If the skill includes scripts or example code, do those scripts work? Run them if possible.
- Anthropic skill design principles: progressive disclosure, gotchas, explain-the-why, autonomy calibration

## Pass 4: Regression

- Did a fix to one section create a contradiction with another section?
- Did renaming a step break references to it in examples or in other reference files?
- Did the fix remove a trigger phrase that was load-bearing?
- Did the fix introduce content that violates user preferences (em-dashes, all-caps musts, sycophancy)?
- Are example outputs in the skill still consistent with the current rules after edits?
- Did the description and body drift apart? After edits, the description should still accurately summarize what the skill does and when it triggers.
- For multi-file skills: did the SKILL.md change require corresponding updates in references/ files that did not happen?

## Skill-specific gotchas to watch for

- **Underspecified description.** Vague descriptions like "helps with X" undertrigger. Real triggers are user phrases.
- **Buried critical info.** Important rules hidden several headers deep often get missed. Promote to top-level if load-bearing.
- **No examples.** Rules without examples are interpreted variably. Each major rule benefits from a concrete example.
- **Conflicting skills.** If two skills could both apply, neither will trigger reliably. Make scope boundaries explicit.
- **Stale references.** A skill that references "the latest model" or "current API" rots quickly. Prefer evergreen language.

## Reporting tone

For skills and specs:

- **Bug**: an instruction is wrong, contradicts itself, or breaks if followed literally
- **Gap**: a real situation the user encountered is not covered
- **Ambiguity**: an instruction can be reasonably interpreted multiple ways
- **Style**: works but could be sharper

Fix bugs and ambiguities. Surface gaps for the user to decide whether to add coverage.
