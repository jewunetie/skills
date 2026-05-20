# Source Evaluation

Frameworks for assessing source reliability, information credibility, and mitigating cognitive biases in analysis.

## CRAAP Test

Quick source quality assessment:

| Criterion | Questions |
|-----------|-----------|
| **Currency** | When published? Updated? Links functional? |
| **Relevance** | Does it address your specific question? Intended audience? |
| **Authority** | Who created it? Credentials? Organization reputation? |
| **Accuracy** | Evidence provided? Can claims be verified elsewhere? Citations? |
| **Purpose** | Why does this exist? Inform, sell, persuade, entertain? Who benefits? |

Score each 1-5. Total 20-25 = excellent source. Below 15 = use with caution or discard.

## Admiralty Code (NATO System)

Two-axis rating for intelligence assessment:

### Source Reliability

| Code | Rating | Definition |
|------|--------|------------|
| A | Completely reliable | No doubt about source's authenticity, trustworthiness, competency; history of complete reliability |
| B | Usually reliable | Minor doubt; has been reliable in past |
| C | Fairly reliable | Doubt exists but has provided valid information in past |
| D | Not usually reliable | Significant doubt; has been unreliable before |
| E | Unreliable | Lacking authenticity, trustworthiness, competency; history of invalid information |
| F | Cannot be judged | No basis for evaluating reliability |

### Information Credibility

| Code | Rating | Definition |
|------|--------|------------|
| 1 | Confirmed | Confirmed by other independent sources |
| 2 | Probably true | Likely based on logical reasoning consistent with other information |
| 3 | Possibly true | Reasonably consistent but not confirmed or logically derived |
| 4 | Doubtfully true | Not confirmed; possible but not logical; no other information |
| 5 | Improbable | Not confirmed; illogical; contradicted by other information |
| 6 | Cannot be judged | No basis for evaluating validity |

**Combined rating examples:**
- A1: Completely reliable source, confirmed information (highest quality)
- B2: Usually reliable source, probably true information
- C4: Fairly reliable source, doubtfully true information
- F6: Cannot evaluate source or information

## SIFT Method

Rapid verification for online content:

1. **Stop** - Pause before reacting or sharing
2. **Investigate the source** - What do you know about this source? Quick search.
3. **Find better coverage** - Can you find this claim from more authoritative sources?
4. **Trace claims** - Follow the chain back to the original source

## Cognitive Biases in OSINT

### Common Biases and Mitigations

| Bias | Description | Mitigation |
|------|-------------|------------|
| **Confirmation** | Favoring information that supports existing beliefs | Actively seek disconfirming evidence; use ACH |
| **Anchoring** | Over-relying on first information received | Evaluate all findings equally; revisit early conclusions |
| **Availability** | Overweighting easily accessible or recent information | Systematic source coverage; check for gaps |
| **Clustering illusion** | Seeing patterns in random data | Require statistical significance; seek alternative explanations |
| **Attribution error** | Attributing behavior to character vs. situation | Consider situational factors |
| **Hindsight** | Believing past events were predictable | Document predictions before outcomes |

### Structured Analytic Techniques

**Analysis of Competing Hypotheses (ACH)**
1. List all possible hypotheses (not just likely ones)
2. List significant evidence and arguments
3. Create matrix: hypotheses vs. evidence
4. Rate each evidence item's consistency with each hypothesis
5. Focus on disproving hypotheses rather than proving them
6. Most supported hypothesis = least inconsistent with evidence

**Key Assumptions Check**
1. List all assumptions underlying the analysis
2. Challenge each: What if this assumption is wrong?
3. Identify which assumptions are most critical
4. Test critical assumptions against evidence

**Devil's Advocacy**
- Assign someone to argue against the prevailing conclusion
- Systematically challenge evidence and logic
- Document counter-arguments

## Source Type Hierarchy

General reliability ranking (always consider specific context):

| Rank | Source Type | Examples |
|------|-------------|----------|
| 1 | Primary/Official | Government records, SEC filings, court documents, company filings |
| 2 | Authoritative | Academic journals, established news organizations, domain experts |
| 3 | Secondary | News aggregators, reference works, professional publications |
| 4 | Tertiary | Wikipedia, general encyclopedias (good for starting points) |
| 5 | Social/User-generated | Social media posts, forums, blogs, comments |
| 6 | Anonymous/Unverified | Anonymous tips, unattributed claims, rumors |

Note: Lower-ranked sources can still provide valuable leads - verify through higher-ranked sources.

## Evaluating Online Sources

### Credibility Indicators

**Positive signals:**
- Named author with verifiable credentials
- Publication with editorial standards
- Citations and references provided
- Contact information available
- Clear correction policy
- Domain matches claimed organization

**Warning signals:**
- Anonymous authorship
- No citations or "sources say"
- Emotional/sensational language
- Recent domain registration
- No physical address/contact
- Asks for sharing before reading

### Domain Trust Signals

| Domain Type | General Trust Level | Notes |
|-------------|---------------------|-------|
| .gov | High | Official government |
| .edu | High | Educational institutions |
| .org | Medium | Nonprofits (anyone can register) |
| .com | Varies | Commercial, evaluate individually |
| Country codes | Varies | Some (.io, .co) used commercially |

## Handling Uncertainty

### Expressing Confidence

Use consistent language:

| Term | Probability | Usage |
|------|-------------|-------|
| Almost certain | >95% | Strong evidence, multiple reliable sources |
| Highly likely | 80-95% | Good evidence, confident but some uncertainty |
| Likely | 60-80% | Preponderance of evidence |
| Possible | 40-60% | Roughly equal evidence both ways |
| Unlikely | 20-40% | Evidence leans against |
| Highly unlikely | 5-20% | Strong evidence against |
| Almost certainly not | <5% | Overwhelming evidence against |

### Documenting Gaps

Always note:
- Sources that could not be accessed
- Information that should exist but was not found
- Time constraints affecting coverage
- Potential sources not yet checked
- Conflicts that could not be resolved

Absence of expected information is itself informative.
