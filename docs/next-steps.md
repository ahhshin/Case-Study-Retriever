# Build status and next steps

Canonical repository: https://github.com/ahhshin/Case-Study-Retriever

Completed: ten public PDFs collected, parsed into page JSON/TXT/MD, selected case boundaries recorded, strict typed schema, taxonomy v1, ten draft records, 78 tags, 15 proof points, compact catalogue, and bounded evidence tools implemented. Parsing checks and initial-page visual review completed in the working session.

Metadata checks pass for all ten records. Assistant source-text review completed; independent human review remains pending. Run `case-validate` after ingestion to rebuild and verify the catalogue.

Next: implement model-driven search over the catalogue using bounded page tools and a small benchmark of business requests. Select and verify the API model at integration time. No vector database is currently required.

GitHub tracks source code, document URLs, case boundaries, schema, documentation, and later reviewed metadata. It is the source of truth for versions. Execution occurs in a checked-out workspace; GitHub does not itself run the interactive harness. Raw third-party documents and full extracts are reproducible working data, excluded from git.
