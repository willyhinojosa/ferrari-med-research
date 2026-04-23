# Ferrari Med Research

Ferrari Med Research is a Python-first MVP for a **medical academic operating system**.
This v2 hardening pass keeps the project lean while improving validation, error handling, and deterministic outputs for production-minded usage.

## MVP Scope (Hardened v2)

This MVP focuses on four core capabilities:

1. intake normalization and validation,
2. DOI normalization and validation checks,
3. APA 7 heuristic auditing,
4. deterministic academic scoring.

No external APIs, web requests, or databases are used.

## Current capabilities

- **`intake_router`**
  - Validates required intake fields (`topic`, `document_type`, `language`, `academic_level`, `source_mode`).
  - Normalizes whitespace consistently.
  - Normalizes `document_type` and `source_mode` to lowercase.
  - Raises clear `ValueError` when normalization is attempted with invalid payloads.

- **`doi_validator`**
  - Accepts raw DOI values and DOI URLs (`https://doi.org/...`, `http://dx.doi.org/...`).
  - Returns structured DOI validation reports with original entry, normalized DOI, validity flag, and errors.
  - Handles missing/non-string DOI values safely.

- **`apa7_auditor`**
  - Uses lightweight heuristics only (no NLP model dependencies).
  - Detects required section presence (`abstract`, `introduction`, `discussion`, `references`).
  - Reports missing sections, reference-like line count, and warnings.
  - Handles empty input safely.

- **`academic_score_engine`**
  - Produces bounded, deterministic scores out of 100.
  - Returns structured output: total score, classification, breakdown, and summary.
  - Classification scale:
    - `90-100`: `Publicable`
    - `80-89`: `Sólido`
    - `70-79`: `Aceptable con mejoras`
    - `<70`: `Requiere revisión mayor`

## Known limitations

- APA checks are heuristic and section-keyword based; they do not guarantee full APA 7 compliance.
- DOI validation focuses on format-level validity and normalization, not DOI resolvability.
- Scoring is rule-based and intentionally simple; it is not a substitute for expert peer review.

## Project Structure

```text
ferrari-med-research/
├── README.md
├── requirements.txt
├── src/
│   ├── intake_router.py
│   ├── doi_validator.py
│   ├── apa7_auditor.py
│   └── academic_score_engine.py
└── tests/
    ├── test_intake_router.py
    ├── test_doi_validator.py
    ├── test_apa7_auditor.py
    └── test_score_engine.py
```
