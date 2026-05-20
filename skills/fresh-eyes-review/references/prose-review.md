# Prose Review Reference

Per-pass categories for reviewing prose: notes, documents, articles, emails, reports.

## Pass 1: Surface

- Typos and misspellings
- Grammar and subject-verb agreement
- Punctuation: missing periods, doubled punctuation, mismatched quotes
- Em-dashes (check user preferences; many users prefer regular dashes or rephrasing)
- Contractions (check user preferences)
- Emoji in formal documents (check user preferences)
- Inconsistent capitalization of proper nouns, product names, technical terms
- Inconsistent terminology: pick one term per concept and use it throughout
- Markdown rendering: broken headers, malformed lists, broken links, incorrect heading levels
- Heading hierarchy: jumps from H1 to H3 with no H2
- Acronyms used before being defined

## Pass 2: Logic and internal consistency

- Factual claims: do dates, numbers, names appear consistent throughout?
- Internal contradictions: does section 3 contradict section 1?
- Narrative flow: are sections in an order that makes sense to a reader who has not read this before?
- Argument structure: do conclusions follow from the evidence presented?
- Definitions: is every introduced term defined before it is used?
- Quantifiers and qualifiers: "all", "some", "always", "never" used precisely?
- Pronouns and references: does every "it", "this", "that" have a clear antecedent?
- Lists and parallel structure: are list items parallel in form and grammatical structure?
- Tables: are headers consistent with cell content, do all cells make sense?
- Examples match the surrounding claims they are intended to illustrate

## Pass 3: Cross-reference

- Original user request: did the document address every part of what the user asked for?
- User-stated preferences from the conversation (formatting, tone, audience)
- Source material: if the document is derived from a transcript, source files, or past chats, does it accurately represent the source?
- Domain conventions: does the document follow conventions appropriate to its audience (legal, technical, executive)?
- Cited sources or referenced documents: do they exist and say what is claimed?
- Date and version sensitivity: is the document still consistent with the present-day state of the world?

For meeting notes specifically: cross-reference any names, dates, organization references against the conversation history. Flag transcription-style errors before assuming them as facts.

## Pass 4: Regression

- Did a fix introduce a new typo?
- Did a paragraph rewrite leave behind a now-stale sentence in an adjacent paragraph?
- Did renaming a section break references to that section elsewhere in the document?
- Did the fix introduce an em-dash, contraction, or other format violation?
- Did the fix accidentally remove content that was intentionally there?
- Did the fix change the meaning of a sentence in a way the user did not approve?
- Are list numberings still correct after items were added or removed?

## Reporting tone

For prose, fixes are often subjective. Distinguish:

- **Error**: clearly wrong (typo, broken grammar, factual mistake)
- **Inconsistency**: the document contradicts itself or its source
- **Style**: matches some convention but might be improved
- **Question**: Claude is unsure of intent

Fix errors and inconsistencies. Surface style and questions for the user rather than rewriting silently.
