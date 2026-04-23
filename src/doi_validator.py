"""DOI normalization and validation helpers for reference entries."""

from __future__ import annotations

import re
from typing import Any

# DOI Handbook-derived structure: directory indicator + suffix with no spaces.
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
DOI_URL_PREFIX = re.compile(r"^https?://(?:dx\.)?doi\.org/", re.IGNORECASE)


def normalize_doi(doi: str) -> str:
    """Normalize DOI strings by removing URL prefixes and extra whitespace."""

    cleaned = doi.strip()
    cleaned = DOI_URL_PREFIX.sub("", cleaned)
    cleaned = re.sub(r"^doi:\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.rstrip(".,;)")
    cleaned = cleaned.lstrip("(")
    return cleaned.lower()


def is_valid_doi_format(doi: str) -> bool:
    """Return ``True`` when DOI matches a standard DOI format pattern."""

    normalized = normalize_doi(doi)
    return bool(DOI_PATTERN.fullmatch(normalized))


def validate_reference_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """Validate a reference entry and return normalized DOI plus validation result."""

    errors: list[str] = []

    raw_doi = entry.get("doi") if isinstance(entry, dict) else None
    if raw_doi is None:
        errors.append("Missing DOI.")
        normalized = ""
    elif not isinstance(raw_doi, str):
        errors.append("DOI must be a string.")
        normalized = ""
    else:
        normalized = normalize_doi(raw_doi)
        if not normalized:
            errors.append("Missing DOI.")
        elif not is_valid_doi_format(normalized):
            errors.append("Invalid DOI format.")

    return {
        "original_entry": entry,
        "normalized_doi": normalized,
        "is_valid_doi": len(errors) == 0,
        "errors": errors,
    }
