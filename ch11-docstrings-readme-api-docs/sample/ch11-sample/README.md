# Chapter 11 sample — Docstrings, README, and API Docs

- `invoicer/` — the running project with full git history. The chapter's commits:
  - `d368581` Document the public API; enforce docstrings with Ruff
  - `7204fa0` Add a README with tested examples
  - `3fb5eae` Add decision records, an API reference config and a tests README
  - `25d7528` Document fx.convert in full
- `examples/billing_api/` — the FastAPI metadata example (Listings 11-10 and 11-11).

Setup:

    cd invoicer
    uv sync --group docs
    uv run pytest              # tests + module doctests + README doctest
    uv run ruff check .
    uv run mkdocs build --strict

`docs` pins `mkdocs<2`: MkDocs 2.0 is not compatible with Material for MkDocs
or the current plugin ecosystem (see the Note in Section 6).
