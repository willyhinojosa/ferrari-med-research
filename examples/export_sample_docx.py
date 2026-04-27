"""Run sample pipeline and export markdown manuscript to DOCX."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.docx_exporter import export_manuscript_to_docx
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

    output_path = ROOT / "data" / "exports" / "sample_manuscript.docx"
    generated_path = export_manuscript_to_docx(
        manuscript_markdown=result["manuscript_draft"],
        output_path=str(output_path),
        metadata={
            "title": intake_payload["title"],
            "author": "Ferrari Med Research",
            "institution": "Ferrari Med Research Lab",
            "course": "Internal Validation",
            "instructor": "Automated Pipeline",
            "date": "2026-04-27",
        },
    )

    print(generated_path)
