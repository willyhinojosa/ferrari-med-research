"""DOI normalization and validation helpers for reference entries."""

from __future__ import annotations

import re

DOI_PATTERN = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)


def normalize_doi(doi: str) -> str:
    """Normalize DOI strings by removing URL prefixes and extra whitespace."""

    cleaned = doi.strip()
    cleaned = re.sub(r"^https?://(dx\.)?doi\.org/", "", cleaned, flags=re.IGNORECASE)
    return cleaned.lower()


def is_valid_doi_format(doi: str) -> bool:
    """Return ``True`` when DOI matches a standard DOI format pattern."""

    normalized = normalize_doi(doi)
    return bool(DOI_PATTERN.match(normalized))


def validate_reference_entry(entry: dict) -> dict:
    """Validate a reference entry and return normalized DOI plus validation result."""

    doi_value = str(entry.get("doi", "")).strip()
    normalized = normalize_doi(doi_value) if doi_value else ""

    result = {
        "is_valid": bool(normalized) and is_valid_doi_format(normalized),
        "normalized_doi": normalized,
        "errors": [],
    }

    if not normalized:
        result["errors"].append("Missing DOI.")
    elif not result["is_valid"]:
        result["errors"].append("Invalid DOI format.")

    return result
