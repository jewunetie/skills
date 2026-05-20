---
name: alphaxiv-paper-lookup
description: Look up any arxiv paper on alphaxiv.org to get a structured AI-generated overview. Use this skill whenever the user shares an arxiv URL (arxiv.org/abs/...), an arxiv paper ID (e.g. 2401.12345), an alphaxiv URL, or asks you to explain, summarize, or analyze a research paper by ID or link. This is faster and more reliable than reading a raw PDF. Trigger proactively even when the user says things like "can you read this paper", "summarize this arxiv link", or "what does this paper say".
---

# AlphaXiv Paper Lookup

## Workflow

### Step 1: Extract the Paper ID

Parse the paper ID from whatever the user provides:

| Input | Paper ID |
|---|---|
| `https://arxiv.org/abs/2401.12345` | `2401.12345` |
| `https://arxiv.org/pdf/2401.12345` | `2401.12345` |
| `https://alphaxiv.org/overview/2401.12345` | `2401.12345` |
| `2401.12345v2` | `2401.12345v2` |
| `2401.12345` | `2401.12345` |

### Step 2: Resolve the Paper

```bash
curl -s "https://api.alphaxiv.org/papers/v3/{PAPER_ID}"
```

From the JSON response, extract:

- **`versionId`** — UUID needed for Step 3
- **`title`** — paper title
- **`authors`** — author list

If this returns 404, the paper has not been indexed on alphaxiv yet — tell the user.

### Step 3: Fetch the AI Overview

```bash
curl -s "https://api.alphaxiv.org/papers/v3/{VERSION_ID}/overview/en"
```

The response contains:

- **`intermediateReport`** — machine-readable structured text; best for LLM consumption
- **`overview`** — full markdown blog post; human-readable
- **`summary`** — structured fields: `summary`, `originalProblem`, `solution`, `keyInsights`, `results`
- **`citations`** — cited papers with titles and justifications

**Prefer `intermediateReport`** when available. Fall back to `summary` fields if `intermediateReport` is null.

### Step 4: Present the Overview

Synthesize the fetched content into a clear, readable response. Do not dump raw JSON. Structure the output with:

- Title and authors (from Step 2 metadata if available)
- Problem being solved
- Approach / solution
- Key findings and results
- Notable citations (if relevant to the user's question)

## Error Handling

- **404 on Step 2**: Paper not indexed on alphaxiv. Tell the user it is not available yet.
- **404 on Step 3**: Overview not yet generated for this version.
- **`intermediateReport` is null**: Use `summary` and `overview` fields instead.

## Notes

- No authentication required. These are public endpoints.
- If `bash_tool` is unavailable, use `web_fetch` on the same URLs — the responses are identical.
- Replace `en` with a language code for translated overviews: `fr`, `de`, `es`, `zh`, `ja`, `ar`, `hi`, `pt`.
- Version suffixes (e.g. `v2`) are preserved and passed through as-is.
