# Ferrari Med Research

Ferrari Med Research is a Python-first MVP for a **medical academic operating system**.
The goal is to provide a lightweight foundation that helps academic users move from raw intake data to basic compliance and scoring outputs in a consistent, testable way.

## MVP Scope

This MVP focuses on four core capabilities:

1. intake normalization and validation,
2. DOI formatting and validation checks,
3. APA 7 heuristic auditing,
4. simple academic scoring.

It is intentionally minimal and designed to be easy to extend.

## Initial Modules

### `intake_router`
Validates incoming intake payloads and normalizes them into a typed structure used by downstream modules.

### `doi_validator`
Normalizes DOI values and runs format checks for reference entries.

### `apa7_auditor`
Runs lightweight APA 7 heuristics for section presence and reference quality indicators.

### `academic_score_engine`
Computes a starter score out of 100 with a simple category breakdown.

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
    ├── test_doi_validator.py
    ├── test_apa7_auditor.py
    └── test_score_engine.py
```

## Roadmap (Next Modules)

Short-term extensions after this MVP:

- `source_ranker`: evidence source ranking by publication signals.
- `bias_scanner`: basic risk flags for overclaiming or unsupported causality.
- `outline_builder`: scaffold for paper structure and section planning.
- `export_layer`: structured output adapters for LMS and manuscript workflows.
