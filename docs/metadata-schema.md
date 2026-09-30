# Structured case records: next implementation step

PDF download, page-preserving text extraction, and initial case segmentation are complete for ten cases. Metadata classification is pending. `data/case-catalogue.json` contains routing hints, not verified factual tags.

## Storage

Use one validated JSON file per case under `data/processed/cases/`. Generate a compact `data/processed/catalogue.json` from those records. JSON is the canonical store at this scale; SQLite can be a derived index later if needed.

## Record structure

| Field | Purpose | Evidence requirement |
|---|---|---|
| case_id, title | Stable identity | Preserve document identity |
| source_id, pages | Link to manifest and physical PDF pages | Valid source ID and page range |
| organization, year | Client and engagement timing, when stated | Quote and page; null when absent |
| observed_tags | Industry, function, capability, technology, AI use case, lifecycle stage, challenge, solution, outcome, brand context, geography | Each tag carries quote and page |
| inferred_retrieval_concepts | Related concepts a search request might use | Explicitly marked inference |
| summaries | Short challenge, solution, and outcome summaries | Evidence references for factual claims |
| proof_points | Metric, description, scope, baseline, period, limitations | Exact source quote and page |
| classification_metadata | Provider/model when applicable, schema version, date, review state | Distinguish model output from human review |

The initial Pydantic schema in `src/case_studies/models.py` covers identity, tags, concepts, proof points, and review state. Extend it for the fields above before producing final records; it is not yet the final classification contract.

## Controlled labels

Begin with a small vocabulary derived from the ten cases. Allow null/unknown and flag proposed new labels rather than forcing a match. Do not equate premium appliances with ultra-luxury fashion, workplace Copilot adoption with software engineering, customer-care assistants with marketing agents, or content generation with persona simulation.

## Classification process

1. Review three contrasting cases: Jura, an AI SDLC case, and pharma marketing.
2. Agree on dimension definitions and normalize labels based on the examples.
3. Extend schema and write a provider-independent classification prompt.
4. Classify all ten selected case ranges, preserving evidence per tag and metric.
5. Validate records; check quote presence and source/page correctness programmatically.
6. Review claim meaning, metric scope, and ambiguous classifications manually.
7. Generate a short catalogue for model context.

Quote presence alone does not establish semantic entailment. Publisher-reported metrics are not independently verified outcomes. Objectives and projected benefits must not be mislabeled as achieved results.

## Publication

Code, schema, source URLs, and minimal source-grounded metadata can be reviewed for public commit. Do not publish full extracted source text or original documents without permission. Review any evidence excerpts for appropriate length and rights before publication.
