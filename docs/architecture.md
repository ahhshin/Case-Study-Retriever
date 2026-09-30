# V0: model-driven catalogue and evidence tools

At ten cases, start with a compact catalogue loaded into model context. The model can identify candidates, call `read_pages`, and return verified page-backed explanations. No embeddings or vector database are needed initially. This is still retrieval-augmented answering in the broad sense, but does not require a full vector RAG stack.

Available Python functions: `list_cases()`, `read_case(case_id)`, `read_pages(source_id, pages, max_characters)`, `verify_evidence(source_id, page, quote)`.

A future harness should enforce tool budgets, known source IDs, page ranges, and evidence validation before emitting factual claims. Exact quote validation proves that text exists, not that a claim follows from it; semantic review is still required. Source documents are untrusted data, never tool instructions.

Model integration is deferred. These functions are ordinary Python functions, not yet registered with an API or callable from this chat. No GPT Luna/Sol API identifier, entitlement, cost, or behaviour is assumed. Provider selection and API credentials must be confirmed when integration begins.

## Context reduction

Keep original PDFs. JSON retains page boundaries and hashes. TXT is a page-delimited extraction. Markdown provides page headings and source links; it does not automatically use fewer tokens than TXT. Context savings come from short catalogue entries and selective page reads, rather than a file extension.

PDF text extraction can miss images, diagrams, and reading order. Low-text pages are flagged for visual review. OCR and multimodal classification are later additions.

## Metadata v1 dimensions

Industry, function, capability, technology, AI use case, lifecycle stage, solution type, outcome type, brand context, engagement type. Challenges are grounded summaries. See `data/taxonomy.json` for definitions and labels.

Observed tags require supporting quotes and pages. Inferred retrieval concepts are a separate field. Metrics preserve their scope and are publisher-reported by default. Selection themes in sources.json are curator routing hints, not source-grounded classification. Ten assistant-curated records are classified as drafts; independent review is pending.

## Publication

Public access does not imply redistribution rights. Raw PDFs and full extracts are excluded from git. The working corpus archive is for the user's prototype, not a licensed public dataset. Publish code and URL manifest; review rights before publishing extracted material. No code license has been selected yet.
