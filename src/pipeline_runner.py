"""End-to-end orchestration runner for the Ferrari Med Research MVP."""

from __future__ import annotations

from typing import Any

from src.academic_score_engine import score_document
from src.apa7_auditor import run_apa7_audit
from src.doi_validator import validate_reference_entry
from src.intake_router import normalize_intake, validate_intake
from src.draft_generator import generate_manuscript
from src.section_parser import split_sections


def _build_scoring_input(apa_audit: dict[str, Any], references_checked: list[dict[str, Any]], text: str) -> dict[str, Any]:
    source_count = len(references_checked)
    valid_reference_count = sum(1 for item in references_checked if item.get("is_valid_doi"))
    peer_reviewed_ratio = (valid_reference_count / source_count) if source_count else 0.0

    missing_count = len(apa_audit.get("missing_sections", []))
    warning_count = len(apa_audit.get("warnings", []))
    apa_audit_score = max(0, 100 - (missing_count * 20) - (warning_count * 10))

    word_count = len((text or "").split())
    readability = 70 if word_count >= 80 else 55

    return {
        "source_count": source_count,
        "peer_reviewed_ratio": peer_reviewed_ratio,
        "apa_audit_score": apa_audit_score,
        "readability": readability,
        "has_clear_sections": bool(apa_audit.get("has_required_sections", False)),
    }


def run_pipeline(intake_data: dict, sample_text: str, references: list[dict]) -> dict[str, Any]:
    """Run the MVP flow: intake -> DOI checks -> APA audit -> scoring."""

    intake_valid, intake_errors = validate_intake(intake_data)

    if intake_valid:
        normalized = normalize_intake(intake_data)
        intake_output: dict[str, Any] = {
            "topic": normalized.topic,
            "document_type": normalized.document_type,
            "language": normalized.language,
            "academic_level": normalized.academic_level,
            "source_mode": normalized.source_mode,
            "title": normalized.title,
            "body_text": normalized.body_text,
            "references": normalized.references,
        }
        pipeline_status = "ok"
    else:
        intake_output = dict(intake_data) if isinstance(intake_data, dict) else {"raw_input": intake_data}
        pipeline_status = "invalid_intake"

    safe_references = references if isinstance(references, list) else []
    references_checked = [validate_reference_entry(entry) for entry in safe_references]
    invalid_reference_count = sum(1 for result in references_checked if not result.get("is_valid_doi", False))

    apa_audit = run_apa7_audit(sample_text)
    scoring_input = _build_scoring_input(apa_audit, references_checked, sample_text)
    score = score_document(scoring_input)

    parsed_sections = split_sections(sample_text)
    manuscript_draft = generate_manuscript(intake_output, sample_text, references_checked, parsed_sections=parsed_sections)

    return {
        "intake": intake_output,
        "intake_valid": intake_valid,
        "intake_errors": intake_errors,
        "references_checked": references_checked,
        "invalid_reference_count": invalid_reference_count,
        "apa_audit": apa_audit,
        "score": score,
        "manuscript_draft": manuscript_draft,
        "pipeline_status": pipeline_status,
    }
