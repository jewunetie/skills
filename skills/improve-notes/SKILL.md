---
name: improve-notes
description: Improve, clean up, or organize meeting notes, with or without an accompanying transcript. Triggers on requests like "improve my notes", "clean up my notes", "help me organize these meeting notes", "improve notes from transcript", or when a user provides raw meeting notes and/or a transcript and asks for cleanup. Also triggers when user provides notes and asks to merge them with a transcript or recording output.
---

# Improve Notes

Transform raw meeting notes (with or without a transcript) into structured, improved notes.

## Input Combinations

1. **Raw notes + transcript** (most common) - merge both sources
2. **Raw notes only** - organize and enrich what exists
3. **Transcript only** - create notes from scratch; warn user output may miss unrecorded context

## General Principle

When unsure about any aspect of the notes - meaning of a term, intent behind a bullet point, whether something is a feature request or an observation, whether a detail is accurate - ask the user rather than guessing. It is better to ask one extra question than to produce notes with incorrect assumptions baked in.

## Step 1: Identify Missing Metadata

Before processing, ensure the following metadata is available. Ask for ALL missing items in a single message rather than one at a time:

- **Participants and roles**: Who was interviewing vs. being interviewed (names and roles)
- **Speaker attribution rules**: Any names to correct, omit, or depersonalize (common with shared laptops or transcription software errors). Depersonalization applies only to speakers and interviewers, not third parties mentioned in discussion.
- **Pre-recording content** (only when transcript is provided): Whether the raw notes contain information not present in the transcript

Do NOT ask about structure, detail level, acronym handling, or whether to extract action items. These are fixed defaults.

## Step 2: Flag Transcription Issues

When a transcript is provided, scan for issues and present them to the user BEFORE producing the improved notes. Wait for corrections. Common issues:

- Incorrect or swapped speaker names
- Garbled words, sentence fragments, crosstalk
- Misspelled proper nouns (people, organizations, software)
- Incorrectly transcribed technical terms, identifiers, reference numbers, or domain-specific terminology
- Phrases that appear to be transcription artifacts rather than meaningful content

Present as a numbered list with the problematic text, location (timestamp or line), and a suggested correction or question. Example:

```
Transcription issues found:
1. [00:12:40] "rest full" - likely "RESTful" (garbled technical term). Confirm?
2. [00:37:40] "Hello there" / "I miss" from Speaker B - appears to be crosstalk, not content. Remove?
3. [throughout] Transcript labels Speaker A as "Dan" but user notes indicate this is Grace (shared laptop). Correct all to Grace?
```

Skip this step when no transcript is provided.

## Step 3: Produce Improved Notes

Processing depends on the input combination:

- **Raw notes + transcript**: Use raw notes as the structural backbone and fill in detail from the transcript. Preserve anything in raw notes absent from the transcript (pre-recording content, sidebar observations, visual context).
- **Raw notes only**: Organize and structure the raw notes using the output defaults and template below. Enrich with clearer phrasing where the intent is obvious; ask when it is not.
- **Transcript only**: Create notes from scratch by identifying topics and organizing chronologically. Warn the user that the output may miss context not captured in the recording.

### Conflict Resolution (raw notes + transcript only)

When raw notes and transcript contradict each other (e.g., different names, different facts, different descriptions of a feature or process), flag the discrepancy and ask the user which source is correct. Neither source is reliably authoritative - raw notes may contain misunderstandings while transcripts may contain speech errors or misattributions.

### Fixed Output Defaults

Apply all of the following unless the user explicitly overrides:

- **Structure**: Chronological flow with Q&A elements. Use section headers by topic as they arose in the meeting.
- **Acronyms**: Define all abbreviations in a dedicated section at the top. Assume the reader knows them but include definitions for reference.
- **Detail level**: Keep all detailed examples, specific anecdotes, and concrete scenarios.
- **Feature requests**: Call out inline where they arise AND extract to a dedicated section at the end.
- **Action items**: Call out inline where they arise AND extract to a dedicated section at the end.

### Output Template

```markdown
## [Meeting Title] - [Date]

**Participants:** [interviewee(s)] (interviewed by [interviewer(s)])

**Acronyms**
- [abbreviation]: [definition]
- ...

---

### [Topic Section Header]

[Chronological Q&A content]

### [Next Topic Section Header]

[Chronological Q&A content]

---

## Feature Requests
- [item] (from [section reference])
- ...

## Action Items
- [item] (owner if known, deadline if known)
- ...
```

### Structure Override

If the raw notes use a non-chronological structure, ask the user whether to keep the raw notes structure or apply the default chronological Q&A structure. If the user requests thematic grouping, group content by theme but preserve Q&A elements within each theme. If the user requests extraction of only one speaker's content, filter accordingly before processing.

## Step 4: Fresh Eyes Review

After producing the improved notes, perform a review checking for:

- Errors, typos, or inconsistencies between sections
- Acronyms used but not defined at the top
- Duplicated content across sections
- Feature requests or action items mentioned inline but missing from the extracted sections (or vice versa)
- Formatting issues
- Information from the raw notes that was lost during merging
- Speaker attribution errors
- Unverified statistics or estimates presented as fact (flag with a note that the number is unverified)
- People referenced in content but not listed in participants
- Contradictory information within the notes (e.g., two sections describing the same process differently)
- Role or title inaccuracies where the transcript clarifies differently than the raw notes

Present findings to the user before considering the task complete.
