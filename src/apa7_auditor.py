"""Lightweight APA 7 heuristic audit routines."""

from __future__ import annotations

from typing import Final

REQUIRED_SECTIONS: Final[tuple[str, ...]] = (
    "abstract",
    "introduction",
    "discussion",
    "references",
)


def _normalize_text(text: str) -> str:
    return "\n".join(line.strip().lower() for line in text.splitlines())


def _detect_sections(content: str) -> dict[str, bool]:
    return {section: (section in content) for section in REQUIRED_SECTIONS}


def _count_reference_lines(text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return sum(1 for line in lines if "." in line and "(" in line and ")" in line)


def audit_sections(text: str) -> dict:
    """Backward-compatible section report for heuristic section detection."""

    normalized_text = _normalize_text(text if isinstance(text, str) else "")
    found = _detect_sections(normalized_text)
    missing = [name for name, is_found in found.items() if not is_found]
    return {"found": found, "missing": missing}


def audit_references(text: str) -> dict:
    """Backward-compatible reference report for heuristic detection."""

    count = _count_reference_lines(text if isinstance(text, str) else "")
    return {"reference_line_count": count, "has_reference_like_entries": count > 0}


def run_apa7_audit(text: str) -> dict:
    """Run section and reference heuristics and return a compact audit summary."""

    if not isinstance(text, str) or not text.strip():
        return {
            "has_required_sections": False,
            "missing_sections": list(REQUIRED_SECTIONS),
            "reference_line_count": 0,
            "warnings": ["Input text is empty."],
        }

    normalized_text = _normalize_text(text)
    found_sections = _detect_sections(normalized_text)
    missing_sections = [name for name, found in found_sections.items() if not found]
    reference_line_count = _count_reference_lines(text)

    warnings: list[str] = []
    if missing_sections:
        warnings.append("Missing one or more required APA-like sections.")
    if reference_line_count == 0:
        warnings.append("No reference-like lines detected.")

    return {
        "has_required_sections": len(missing_sections) == 0,
        "missing_sections": missing_sections,
        "reference_line_count": reference_line_count,
        "warnings": warnings,
    }
