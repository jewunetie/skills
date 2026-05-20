# Google Search Operators Reference

Complete syntax details and edge cases for all active operators.

## Site and Domain Operators

### site:

Restricts results to a specific domain or subdomain.

```
site:nytimes.com              # All pages on nytimes.com
site:cooking.nytimes.com      # Only the cooking subdomain
site:.gov                     # All .gov domains
site:.edu                     # All .edu domains
site:*.nasa.gov               # All NASA subdomains
```

Domain can be specified with or without leading period: `site:.gov` and `site:gov` are equivalent.

### inurl: / allinurl:

Restricts to pages with specified terms in the URL.

```
inurl:api                     # "api" appears in URL
allinurl:api docs             # Both "api" AND "docs" in URL
```

Note: `allinurl:` applies to ALL following terms. Do not combine with other operators.

### intitle: / allintitle:

Restricts to pages with terms in the title.

```
intitle:guide                 # "guide" in page title
allintitle:python guide       # Both words in title
intitle:guide python async    # "guide" in title, other terms anywhere
```

### intext: / allintext:

Restricts to pages with terms in body text (not title/URL).

```
intext:deprecated             # "deprecated" in page body
allintext:deprecated warning  # Both terms in body text
```

### inanchor: / allinanchor:

Restricts to pages where the specified terms appear in anchor text of links pointing TO the page.

```
inanchor:best restaurant      # Links to page use "best" in anchor text
allinanchor:best restaurant   # Links use both words
```

## Text Matching Operators

### Quotes ("...")

Exact phrase matching. Disables synonyms and spelling correction.

```
"machine learning"            # Exact phrase
"Alexander * Bell"            # Phrase with wildcard gap
```

Single word in quotes forces exact match without synonyms: `"ca" history` matches "ca" literally, not "California".

### Minus (-)

Excludes terms or sites. Must be immediately before the term (no space).

```
jaguar -cars                  # Exclude "cars"
jaguar -cars -football -os    # Multiple exclusions
security -site:wikipedia.org  # Exclude entire site
recipe -filetype:pdf          # Exclude file type
```

### OR

Boolean OR for alternative terms. Must be uppercase.

```
mesothelioma OR "lung disease"
cat OR dog OR hamster
site:reuters.com OR site:bloomberg.com
```

Note: OR inside quotes is treated literally, not as Boolean: `"cat OR dog"` searches for that exact phrase.

### Wildcard (*)

Matches one or more words (tokens). Works best inside quoted phrases where behavior is predictable.

```
"how to * a PDF"              # Matches "how to edit a PDF", "how to sign a PDF", etc.
"* is the capital of France"  # Matches "Paris is the capital of France"
```

Inside quotes, `*` matches 1-5 words. Outside quotes, behavior is less predictable.

### AROUND n

Proximity search. Finds documents where two terms appear within n words of each other.

```
CEO AROUND 3 resigned         # "CEO" within 3 words of "resigned"
"climate change" AROUND 10 legislation
```

Does not preserve order: matches both "CEO resigned" and "resigned CEO".

## Date and Number Operators

### before: / after:

Filter by publication date. Format: `YYYY-MM-DD` or `YYYY`.

```
after:2024-01-01              # Published after Jan 1, 2024
before:2023-06-15             # Published before June 15, 2023
after:2023-01-01 before:2024-01-01   # Published in 2023
```

**Gotcha**: `after:YYYY` defaults to after Jan 1 of the NEXT year. So `after:2024` means after Jan 1, 2025. Always use full dates like `after:2024-01-01` to avoid confusion.

### Number Range (..)

Searches for numbers within a range.

```
camera $200..$500             # Price range
"world war" 1914..1918        # Year range
laptop 13..15 inch            # Size range
```

## File Type Operator

### filetype:

Restricts to specific file extensions.

```
filetype:pdf                  # PDF files
filetype:pptx                 # PowerPoint files
filetype:docx                 # Word documents
filetype:xlsx                 # Excel files
```

For data files, use Google Dataset Search instead of `filetype:csv` (no longer indexed).

## Definition Operator

### define

Returns definitions from web pages.

```
define peruse                 # Definition of "peruse"
define Hobson's choice        # Definition of phrase
```

No colon needed. For rare words, searching the word alone often returns definitions.

## Deprecated Operators (Do Not Use)

These operators no longer function. Do not include them in queries.

| Operator | Status | Alternative |
|----------|--------|-------------|
| `link:` | Removed mid-2016 | None |
| `info:` | Removed mid-2017 | None |
| `+` (plus) | Removed | Use `"term"` for verbatim |
| `~` (tilde) | Removed | Synonyms now automatic |
| `related:` | Removed June 2023 | None |
| `filetype:csv` | No longer indexed | Google Dataset Search |
| `filetype:mp3` | No longer indexed | `inurl:mp3` as workaround |

## Special Characters

Most special characters are now searchable:

```
I ❤ NY                        # Emoji in search
C++                           # Plus signs in terms
size 7½                       # Fractions (synonymized with 7.5)
10:27                         # Colons (useful for Bible verses)
```

## Syntax Notes

**Parentheses do not work**: Google ignores parentheses for grouping. `(A B) OR (C D)` is interpreted as `A B OR C D` which means A, (B OR C), D. Run separate searches if you need true grouping.

**Word order matters**: `to be or not to be` returns different results than `be to not or be to`.

**Combining operators**: Most operators can be combined freely except `allin*` variants which apply to all following terms.
