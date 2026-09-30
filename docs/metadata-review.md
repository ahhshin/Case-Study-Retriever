# Metadata v1 review

One JSON record per case is the canonical metadata database. `case-validate` checks the corpus and regenerates the catalogue. No classification API was called: these records were curated and reviewed against extracted source text by the assistant. They remain drafts pending independent human review.

## Three contrasting examples

| Case | Observed classification | Proof point and scope | Boundary |
|---|---|---|---|
| Jura | Premium appliances; AR/3D; immersive commerce | 15% conversion boost on AR-enabled products | Does not establish an AI deployment or ultra-luxury fashion engagement |
| Agentic SDLC | Software engineering; backlog/test generation; controlled PoC | Requirements cycle: 3 weeks to 1 week for one portal feature | Not enterprise-wide release acceleration |
| Pharma marketing | Generative AI; marketing content agent; brand guidelines | 50–75% production-time reduction; estimated 60% cost reduction | Does not establish persona simulation or independently verified compliance |

## Review findings

- Pharmacy content source describes 50–75% using both first-draft turnaround and draft-to-final-approval wording. The record retains the KPI scope and flags ambiguity.
- Modernization's 68% savings covers automation, modernization, and infrastructure consolidation; it is not attributed solely to AI.
- Eneco's wrap-up reduction is rounded to 50% in the overview and described as almost 50% in the narrative. Training time concerns Copilot-assisted functionality.
- Navantia's license activation and administrative time savings are workplace outcomes, not developer-productivity metrics.
- Burberry has a qualitative outcome summary but no quantified proof point; multicolumn extraction requires caution.
- Unknown client identities and engagement years remain null. URL dates and document copyright years are not engagement dates.
- Inferred search concepts are separate from observed tags. No case demonstrates persona simulation.

## Validation limits

Quote matching confirms presence, not semantic entailment or causal attribution. Metrics are publisher-reported. Source hashes detect changed documents and require reclassification. A reviewer should inspect selected PDF pages before setting `review_status` to `reviewed`.

The initial records contain a selected set of useful metrics, not an exhaustive extraction of every number in each document. Raw PDFs and full extracts remain excluded from Git.
