"""Build structured research packets from intake context and DOI validation results."""

from __future__ import annotations

from typing import Any


def _build_evidence_notes(valid_count: int, invalid_count: int) -> list[str]:
    notes = [
        f"{valid_count} validated reference{'s' if valid_count != 1 else ''} available.",
    ]

    if invalid_count == 0:
        notes.append("0 references require correction before final inclusion.")
    elif invalid_count == 1:
        notes.append("1 reference requires correction before final inclusion.")
    else:
        notes.append(f"{invalid_count} references require correction before final inclusion.")

    return notes


def build_research_packet(intake: dict, references_checked: list[dict]) -> dict[str, Any]:
    """Assemble a deterministic research packet for downstream drafting stages."""

    safe_intake = intake if isinstance(intake, dict) else {}
    safe_references = references_checked if isinstance(references_checked, list) else []

    valid_references = [item for item in safe_references if item.get("is_valid_doi") is True]
    invalid_references = [item for item in safe_references if item.get("is_valid_doi") is not True]

    valid_count = len(valid_references)
    invalid_count = len(invalid_references)

    return {
        "topic": safe_intake.get("topic", ""),
        "document_type": safe_intake.get("document_type", ""),
        "academic_level": safe_intake.get("academic_level", ""),
        "valid_references": valid_references,
        "invalid_references": invalid_references,
        "reference_count": valid_count,
        "invalid_reference_count": invalid_count,
        "evidence_notes": _build_evidence_notes(valid_count, invalid_count),
    }
