# Case Study Retriever

Canonical project: https://github.com/ahhshin/Case-Study-Retriever

Ten public PDF sources, page-preserving ingestion, and typed metadata/evidence structures. Retrieval engine and model integration are intentionally deferred pending corpus and taxonomy review.

## Setup

Python 3.10+, Poppler (`pdftotext` and `pdftoppm`).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
case-ingest
```

Existing PDFs are reused; use `case-ingest --force` to redownload. Downloads have a 50 MiB limit and a timeout; failed sources appear in `data/ingestion-report.json` and make the command exit nonzero.

- `data/sources.json`: reproducible document manifest; selection themes are provisional.
- `data/raw/`: original PDFs, excluded from public git.
- `data/parsed/`: page-numbered JSON, TXT, and Markdown, excluded from public git.
- `data/case-catalogue.json`: selected case boundaries and compact routing notes.
- `src/case_studies/models.py`: draft Pydantic case, tag, metric, and evidence schema.
- `src/case_studies/tools.py`: bounded page reads and exact evidence checks.
- `docs/architecture.md`: proposed small-corpus harness and limitations.

No API key is required for ingestion. No model calls have been made. Source reports are retained in full, but only selected case pages should enter classification. Parsed page numbers are physical PDF pages, not printed slide labels.

## Next milestone

Finalize the metadata taxonomy, classify ten cases into evidence-backed JSON records, and produce a compact catalogue. See [metadata schema](docs/metadata-schema.md) and [build status](docs/next-steps.md).
