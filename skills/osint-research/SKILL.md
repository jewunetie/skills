---
name: osint-research
description: Deep research methodology for investigating people, companies/organizations, and topics/events using publicly accessible sources. Use when research requires going beyond simple web search - finding connected information across multiple sources, verifying claims, building comprehensive profiles, or investigating entities systematically. Triggers on "investigate", "research [person/company]", "find information about", "background check", "verify", "deep dive", "OSINT", "find out everything about", or when a single search would be insufficient to answer the query.
---

# OSINT Research Skill

Systematic methodology for open source intelligence gathering across three domains: people, organizations, and topics/events.

## Investigation Type Router

Determine investigation type and load appropriate reference:

| Query Pattern | Type | Load Reference |
|---------------|------|----------------|
| Research a specific person, find someone, background on individual | People | `references/people-techniques.md` |
| Research company, organization, business intelligence, corporate due diligence | Organization | `references/organization-techniques.md` |
| Verify claim, fact-check, confirm event happened, geolocation | Verification | `references/verification-techniques.md` |
| Complex investigation spanning multiple types | Multi-domain | Load relevant references as needed |

For all investigations, `references/source-evaluation.md` provides source quality assessment frameworks.

## Search Query Construction

For precise web searches, load the `google-search-operators` skill. Key patterns for OSINT:

```
site:linkedin.com/in/ "target name" "company"    # LinkedIn profiles
site:twitter.com "username"                       # Twitter/X accounts
"target name" filetype:pdf                        # Documents mentioning target
site:.gov "company name"                          # Government records
"email@domain.com"                                # Email footprint
```

## Intelligence Cycle

Every investigation follows five phases:

### 1. Planning
- Define specific question to answer
- Identify starting data points (name, email, company, URL, image, etc.)
- Set scope boundaries and stopping criteria
- List source categories to search

### 2. Collection
- Execute searches systematically across planned sources
- Document every query and source checked
- Capture content immediately (pages change/disappear)
- Note negative findings (absence of expected information is informative)

### 3. Processing
- Organize raw findings by source type
- Extract key identifiers for pivoting
- Flag items requiring verification
- Remove duplicates

### 4. Analysis
- Cross-reference across sources
- Build timeline if temporal
- Map relationships if network
- Assess source reliability (see `references/source-evaluation.md`)
- Identify gaps and contradictions

### 5. Reporting
- Structure findings per output template below
- State confidence levels explicitly
- Document methodology for reproducibility
- List limitations and what could not be found

## Pivoting Patterns

Pivoting expands from one data point to discover connected information:

| Starting Point | Pivot To |
|----------------|----------|
| Email address | Username (before @), domain owner, breach databases, account recovery flows |
| Username | Same username on other platforms, variations (appending numbers, underscores) |
| Phone number | Reverse lookup, carrier, linked social accounts |
| Real name | Social profiles, public records, news mentions, academic papers |
| Domain | WHOIS history, DNS records, other domains on same IP, SSL certificates |
| Image | Reverse image search, EXIF metadata, geolocation from visual clues |
| Company | Officers/directors, corporate filings, SEC records, job postings |
| Address | Property records, satellite imagery, street view, associated entities |

Chain pivots: Email → Username → Other platforms → Images → Geolocation → Address

## Stopping Criteria

Stop collecting when:
- Original question is answered with sufficient confidence
- New searches return only previously-found information
- Remaining gaps require non-public sources
- Time/effort exceeds value of additional findings

Warning signs of over-collection:
- Continuing without clear connection to original question
- Justifying "one more search" repeatedly
- Accumulating data without analyzing it

## Output Template

Structure findings flexibly based on investigation complexity:

```markdown
## Summary
[One paragraph answering the original question]

## Key Findings
[Organized by theme or chronologically, with confidence levels]

### [Theme/Category 1]
- Finding with source attribution
- Finding with source attribution

### [Theme/Category 2]
- Finding with source attribution

## Source Assessment
[Note any conflicting information, source reliability concerns]

## Gaps and Limitations
[What could not be determined, what would require additional access]

## Methodology
[Brief description of sources searched, for reproducibility]
```

Confidence levels:
- **Confirmed**: 3+ independent, reliable sources agree
- **High**: 2 reliable sources, consistent details
- **Medium**: Single reliable source
- **Low**: Unverified single source
- **Conflicting**: Sources disagree, note the conflict

## Handling Conflicting Information

When sources conflict:
1. Prefer primary over secondary sources
2. Prefer official over unofficial sources
3. Prefer recent over older (for current-state questions)
4. Consider source motivation and potential bias
5. Note the conflict explicitly rather than choosing arbitrarily
6. Search for additional sources to break the tie

## Tool Usage Notes

- **web_search**: Primary collection tool. Use google-search-operators skill for precision.
- **web_fetch**: Retrieve full page content after search identifies relevant URLs.
- Most OSINT tools are web-based and can be accessed via web_fetch.
- Some tools require accounts or have rate limits - note when a tool cannot be used.
- Archive.org (Wayback Machine) for historical/deleted content: `web.archive.org/web/*/[URL]`

## Scripts

This skill includes automation scripts in `scripts/` for common OSINT tasks:

### domain_recon.py
Full domain reconnaissance combining DNS, WHOIS, and subdomain discovery.
```bash
python scripts/domain_recon.py <domain> [--json]
python scripts/domain_recon.py anthropic.com
python scripts/domain_recon.py example.com --json
```
Returns: DNS records (A, AAAA, MX, NS, TXT), WHOIS data (registrar, dates, nameservers), subdomains from Certificate Transparency logs.

### wayback_check.py
Check Wayback Machine archive availability for URLs.
```bash
python scripts/wayback_check.py <url> [--json]
python scripts/wayback_check.py example.com
python scripts/wayback_check.py https://example.com/page --json
```
Returns: Archive status, most recent snapshot URL and date.

### image_metadata.py
Extract EXIF metadata from images including GPS coordinates.
```bash
python scripts/image_metadata.py <image_path_or_url> [--json]
python scripts/image_metadata.py photo.jpg
python scripts/image_metadata.py https://example.com/image.jpg --json
```
Returns: Camera info, capture settings, GPS coordinates with Google Maps link.
Requires: `pip install exifread --break-system-packages`

### When to Use Scripts vs. Manual Tools

| Task | Use Script | Use Manual/Web |
|------|------------|----------------|
| Domain reconnaissance | `domain_recon.py` | When script fails or need more detail |
| Check if URL archived | `wayback_check.py` | When need to browse snapshots |
| Extract image GPS/EXIF | `image_metadata.py` | For advanced analysis or formats script does not support |
| Username enumeration | - | Web tools (rate limits, anti-bot) |
| Reverse image search | - | Web tools (requires upload) |
| Social media research | - | Platform-specific tools |
