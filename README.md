# Case Study Retriever

Canonical project: https://github.com/ahhshin/Case-Study-Retriever

Ten public PDF sources, page-preserving ingestion, and ten structured case records with source-backed tags and proof points. A provider-independent retrieval harness and simple GUI are now included. Real provider access is configured through an adapter.

## Try the demo — no installation required

1. Click **Code → Download ZIP** above, then extract the ZIP.
2. Open **web/demo.html** in Chrome or another modern browser.
3. Type **“find me a case study about luxury brands”**, or click an example.

The luxury query returns Burberry with supporting evidence from page 48. The demo includes all ten case records and works offline; source links need internet access. **This immediate demo uses metadata search, not a live AI model.** No Python, API key, or PDF download is required. GitHub displays HTML source; download the file or repository before opening the demo.

## Run the Python-backed GUI

Clone or download this repository. Python 3.10+ is required:

```bash
git clone https://github.com/ahhshin/Case-Study-Retriever.git
cd Case-Study-Retriever
python -m venv .venv
```

Activate the environment:

- **macOS/Linux:** `source .venv/bin/activate`
- **Windows PowerShell:** `.venv\Scripts\Activate.ps1`
- **Windows Command Prompt:** `.venv\Scripts\activate.bat`

Then:

```bash
python -m pip install -e .
case-serve
```

Open **http://127.0.0.1:8765**. The committed metadata is sufficient for default search; there is no ingestion step or model key required. Plug in any model through the adapter interface described in the [harness guide](docs/retrieval-harness.md).

## Optional: rebuild the source corpus

Python 3.10+, Poppler (`pdftotext` and `pdftoppm`). Only needed to download/parse the original PDFs, verify them against the records, or enable full-page model reads.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
case-ingest
case-validate
python -m unittest discover -s tests -v
```

Existing PDFs are reused; use `case-ingest --force` to redownload. Downloads have a 50 MiB limit and a timeout; failed sources appear in `data/ingestion-report.json` and make the command exit nonzero.

- `data/sources.json`: reproducible document manifest; selection themes are provisional.
- `data/raw/`: original PDFs, excluded from public git.
- `data/parsed/`: page-numbered JSON, TXT, and Markdown, excluded from public git.
- `data/case-catalogue.json`: selected case boundaries and compact routing notes.
- `src/case_studies/models.py`: strict Pydantic case, tag, metric, and evidence schema.
- `src/case_studies/tools.py`: bounded page reads and exact evidence checks.
- `data/taxonomy.json`: controlled labels and definitions.
- `data/processed/cases/`: canonical draft records.
- `data/processed/catalogue.json`: generated short catalogue for model context.
- `src/case_studies/metadata.py`: source/hash/evidence validation and catalogue generation.
- `docs/metadata-review.md`: example classifications and review caveats.
- `docs/architecture.md`: proposed small-corpus harness and limitations.

No API key is required for ingestion. No model calls have been made. Source reports are retained in full, but only selected case pages should enter classification. Parsed page numbers are physical PDF pages, not printed slide labels.

## Search and test UI

Open `web/demo.html` in Chrome to try the ten-case metadata search without installing anything. For the Python-backed GUI, run `case-serve` and open http://127.0.0.1:8765. Run `case-search "luxury brands"` for CLI search. Plug in a model with `--adapter module:factory`; see [harness guide](docs/retrieval-harness.md).

## Next milestone

Connect and evaluate a chosen model adapter on broader business requests. Metadata v1 contains 10 draft records, 78 observed tags, and 15 publisher-reported proof points. See [metadata schema](docs/metadata-schema.md) and [build status](docs/next-steps.md).
