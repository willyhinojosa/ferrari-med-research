"""Intake routing and normalization utilities for the MVP."""

from __future__ import annotations

from dataclasses import dataclass

REQUIRED_VALIDATED_FIELDS = (
    "topic",
    "document_type",
    "language",
    "academic_level",
    "source_mode",
)


@dataclass(slots=True)
class IntakeSpec:
    """Normalized representation of intake input used across modules."""

    topic: str
    document_type: str
    language: str
    academic_level: str
    source_mode: str
    title: str
    body_text: str
    references: list[dict]


def _clean_text(value: object) -> str:
    """Normalize text by trimming and collapsing internal whitespace."""

    if value is None:
        return ""
    return " ".join(str(value).split())


def validate_intake(data: dict) -> tuple[bool, list[str]]:
    """Validate required intake fields and return a success flag with errors."""

    errors: list[str] = []

    if not isinstance(data, dict):
        return False, ["Input must be a dictionary."]

    for field in REQUIRED_VALIDATED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not _clean_text(data.get(field)):
            errors.append(f"Field '{field}' cannot be empty.")

    if "references" in data and not isinstance(data["references"], list):
        errors.append("Field 'references' must be a list.")

    return len(errors) == 0, errors


def normalize_intake(data: dict) -> IntakeSpec:
    """Normalize intake payload into an ``IntakeSpec`` instance.

    Raises:
        ValueError: If required validated fields are missing or empty.
    """

    is_valid, errors = validate_intake(data)
    if not is_valid:
        raise ValueError(f"Invalid intake payload: {'; '.join(errors)}")

    refs = data.get("references", [])
    normalized_refs = refs if isinstance(refs, list) else []

    return IntakeSpec(
        topic=_clean_text(data.get("topic", "")),
        document_type=_clean_text(data.get("document_type", "")).lower(),
        language=_clean_text(data.get("language", "")),
        academic_level=_clean_text(data.get("academic_level", "")),
        source_mode=_clean_text(data.get("source_mode", "")).lower(),
        title=_clean_text(data.get("title", "")),
        body_text=_clean_text(data.get("body_text", "")),
        references=normalized_refs,
    )
