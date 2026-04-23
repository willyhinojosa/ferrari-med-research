"""Small runnable example for the end-to-end MVP pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline_runner import run_pipeline


if __name__ == "__main__":
    intake_payload = {
        "topic": "Cardiovascular outcomes in Type 2 Diabetes",
        "document_type": "Review",
        "language": "English",
        "academic_level": "Postgraduate",
        "source_mode": "Mixed",
        "title": "SGLT2 Inhibitors and Heart Failure Outcomes",
        "body_text": "A concise review-style manuscript for internal validation.",
    }

    manuscript_text = """
    Abstract
    This manuscript summarizes recent cardiovascular evidence in type 2 diabetes.

    Introduction
    Cardiovascular risk reduction remains a central treatment objective.

    Discussion
    SGLT2 inhibitor evidence suggests improved heart-failure related outcomes in selected populations.

    References
    Doe, J. (2022). Cardio-metabolic outcomes and guideline adoption.
    Smith, R. (2021). Modern evidence synthesis in diabetes care.
    """

    reference_entries = [
        {"title": "Empagliflozin Outcome Trial", "doi": "10.1056/NEJMoa1504720"},
        {"title": "Malformed DOI Example", "doi": "10.abc/not-a-doi"},
        {"title": "URL DOI Example", "doi": "https://doi.org/10.1016/j.cell.2020.04.001"},
    ]

    result = run_pipeline(intake_payload, manuscript_text, reference_entries)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n--- Manuscript Draft ---\n")
    print(result["manuscript_draft"])
