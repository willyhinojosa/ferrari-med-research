"""Intake routing and normalization utilities for the MVP."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class IntakeSpec:
    """Normalized representation of intake input used across modules."""

    title: str
    document_type: str
    body_text: str
    references: list[dict]


def validate_intake(data: dict) -> tuple[bool, list[str]]:
    """Validate required intake fields and return a success flag with errors."""

    errors: list[str] = []

    if not isinstance(data, dict):
        return False, ["Input must be a dictionary."]

    required_fields = ("title", "document_type", "body_text", "references")
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "title" in data and not str(data["title"]).strip():
        errors.append("Field 'title' cannot be empty.")

    if "document_type" in data and not str(data["document_type"]).strip():
        errors.append("Field 'document_type' cannot be empty.")

    if "body_text" in data and not str(data["body_text"]).strip():
        errors.append("Field 'body_text' cannot be empty.")

    if "references" in data and not isinstance(data["references"], list):
        errors.append("Field 'references' must be a list.")

    return len(errors) == 0, errors


def normalize_intake(data: dict) -> IntakeSpec:
    """Normalize intake payload into an ``IntakeSpec`` instance."""

    return IntakeSpec(
        title=str(data.get("title", "")).strip(),
        document_type=str(data.get("document_type", "")).strip().lower(),
        body_text=str(data.get("body_text", "")).strip(),
        references=data.get("references", []) if isinstance(data.get("references", []), list) else [],
    )
