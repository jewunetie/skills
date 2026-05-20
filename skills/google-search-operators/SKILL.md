---
name: google-search-operators
description: Advanced Google search operator syntax for precise web searches. Read this skill BEFORE calling web_search when you need to restrict results to specific sites/domains, exclude terms or sites, find specific file types, filter by date range, find terms in proximity, or when basic keywords would return too many irrelevant results. Proactively use operators to improve search precision.
---

# Google Search Operators

Use these operators to construct precise web_search queries. Default to using operators when a naive keyword search would be too broad.

## Quick Reference: Goal to Operator

| Goal | Operator | Example |
|------|----------|---------|
| Restrict to specific site/domain | `site:` | `site:nytimes.com climate policy` |
| Exclude a term | `-term` | `jaguar -cars -football` |
| Exclude a site | `-site:` | `python tutorial -site:w3schools.com` |
| Find specific file type | `filetype:` | `annual report filetype:pdf` |
| Exact phrase match | `"..."` | `"machine learning"` |
| Either term (synonyms) | `OR` | `mesothelioma OR "lung disease"` |
| Terms in proximity | `AROUND n` | `CEO AROUND 3 resigned` |
| Date range | `before:` / `after:` | `election results after:2024-01-01` |
| Number range | `..` | `laptop $500..$1000` |
| Term in URL | `inurl:` | `inurl:api documentation` |
| Term in title | `intitle:` | `intitle:guide python asyncio` |
| Wildcard (any word) | `*` | `"how to * a PDF"` |

## High-Value Idioms

### Site Minus Site (discover subdomains)

Find subdomains within a domain:
```
site:nasa.gov -site:www.nasa.gov
```
Returns pages on nasa.gov subdomains (science.nasa.gov, mars.nasa.gov, etc.) excluding the main www site.

### Stars in Quoted Phrases

Wildcards inside quotes enforce word order while allowing gaps:
```
"CEO * resigned * misconduct"
```
Finds variations like "CEO John Smith resigned following misconduct" in that sequence.

### Stars in Site Search

Match patterns in domain names:
```
site:*.law.*.edu
```
Finds all .edu law school sites. In domain patterns, each `*` matches one subdomain segment.

## Operator Combination Patterns

Combine operators for precision:

```
site:.gov filetype:pdf "climate change" after:2023-01-01
```

```
intitle:tutorial python asyncio -site:youtube.com -site:medium.com
```

```
"quarterly earnings" AROUND 5 "beat expectations"
```

```
site:reuters.com OR site:bloomberg.com "fed rate decision"
```

## Key Syntax Rules

1. No space between operator and value: `site:example.com` not `site: example.com`
2. `-` must touch the excluded term: `-cats` not `- cats`
3. `OR` must be uppercase
4. Date format: `YYYY-MM-DD` or just `YYYY`
5. **Gotcha**: `after:2024` means after Jan 1, 2025 (the year AFTER 2024). Use `after:2024-01-01` for precision.
6. Quotes disable synonyms and enforce exact matching
7. Word order matters even without quotes
8. Parentheses do NOT work for grouping: `(A B) OR (C D)` is interpreted as `A (B OR C) D`

## Do Not Use (Deprecated)

These operators no longer function and will not improve results:
- `link:` - Removed
- `info:` - Removed
- `+` (plus operator) - Use quotes for verbatim
- `~` (tilde/synonym) - Synonyms now automatic
- `filetype:csv` - No longer indexed
- `filetype:mp3` - No longer indexed
- `related:` - Removed

## When to Use Operators Proactively

- **Searching official sources**: Use `site:` to restrict to .gov, .edu, or specific authoritative domains
- **Avoiding content farms**: Use `-site:` to exclude low-quality aggregators
- **Finding documents**: Use `filetype:pdf` or `filetype:pptx` for reports, presentations
- **Recent information**: Use `after:` to filter to recent content
- **Specific phrases**: Use quotes for technical terms, proper nouns, error messages
- **Disambiguation**: Use `-term` to exclude irrelevant meanings (apple -fruit, python -snake)

For full operator details and edge cases, see [references/operators.md](references/operators.md).
