# Slides and Decks Review Reference

Per-pass categories for reviewing slide decks and presentations.

## Pass 1: Surface

- Typos in titles, body text, speaker notes
- Inconsistent capitalization across slide titles (title case vs sentence case mixed)
- Inconsistent terminology and product names across slides
- Formatting: font size variation that is not intentional, misaligned text boxes, inconsistent bullet styles
- Em-dashes, contractions, emojis (check user preferences)
- Slide numbers, footer text, header text consistent across slides where applicable
- Image and chart labels: are axes labeled, are units present, is the legend correct
- Acronyms used before being defined on the slide where they first appear
- Speaker notes: are they present where the slide needs explanation, are they free of typos

## Pass 2: Logic and internal consistency

- Narrative arc: do the slides build to a clear takeaway, or are they a list of disconnected facts?
- Does each slide have one clear message? Slides with multiple competing messages dilute impact.
- Are claims on slide N supported by evidence on slide N or earlier slides? Do later slides contradict earlier ones?
- Numbers, percentages, and dates consistent across slides where they refer to the same thing
- Does the title of each slide accurately summarize what the slide says?
- Does the section structure make sense as a sequence? Is there a logical reason for the order?
- Are charts the right type for the data (e.g., not using a pie chart for time-series)?
- Are comparisons fair? Same scales, same time periods, like-for-like
- Animations and builds: do they reveal information in an order that supports the narrative?

## Pass 3: Cross-reference

- Original request: does the deck address every part of what the user asked for?
- Audience: is the language and depth appropriate for the stated audience? Technical depth for technical audiences, plain language for non-technical
- Source material: if the deck is derived from notes, transcripts, or a working document, do the slide claims accurately represent the source?
- Brand or template guidelines: does the deck follow conventions for this audience or organization?
- Time budget: is the slide count appropriate for the meeting length, given a reasonable pace?
- For pilot, sales, or stakeholder decks: are the messages framed for the recipient's concerns, not the producer's?
- Plain-language messaging: if the audience is non-technical, are technical terms explained or replaced?

## Pass 4: Regression

- Did a fix to slide N introduce a contradiction with slide N+1?
- Did renaming a section break the table of contents or section dividers?
- Did changing a number on one slide leave a now-inconsistent number on another slide?
- Did rewriting a title leave the body still keyed to the old title?
- Did adding speaker notes accidentally introduce content that conflicts with the on-slide text?
- Did a chart edit break the labels, legend, or axes?
- Did the fix introduce format violations (em-dashes, contractions, etc.) that the original did not have?

## Slide-specific gotchas

- **Wall of text.** A slide with more than approximately 30-40 words is often unreadable in a meeting. Flag for tightening.
- **Title that is not a takeaway.** "Q3 Results" is a label; "Q3 Revenue Beat Plan by 12%" is a takeaway. Takeaway titles are usually better for executive audiences.
- **Builds out of order.** Animation that reveals the conclusion before the supporting evidence undermines the slide.
- **Inconsistent visual weight.** Important slides should look important; throwaway slides should not look the same as the main message.
- **Source unclear.** When a chart, claim, or quote is on a slide, can a reader tell where it came from?

## Reporting tone

For slides:

- **Error**: clearly wrong (typo, factual mistake, misleading chart)
- **Inconsistency**: deck contradicts itself or its source
- **Audience mismatch**: language or depth wrong for the stated audience
- **Style**: works but could be sharper
- **Question**: Claude is unsure of intent

Fix errors and audience mismatches when the user has stated the audience. Surface style and questions for the user.
