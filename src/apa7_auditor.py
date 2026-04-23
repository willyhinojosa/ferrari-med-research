"""Lightweight APA 7 heuristic audit routines."""

from __future__ import annotations


def audit_sections(text: str) -> dict:
    """Check whether expected academic sections are present in the document text."""

    content = text.lower()
    expected = ["abstract", "introduction", "methods", "results", "discussion", "references"]

    found = {section: (section in content) for section in expected}
    missing = [section for section, present in found.items() if not present]

    return {
        "found": found,
        "missing": missing,
        "score": max(0, 100 - (len(missing) * 15)),
    }


def audit_references(text: str) -> dict:
    """Run simple reference checks using line-based heuristics."""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    reference_lines = [line for line in lines if "." in line and "(" in line and ")" in line]

    return {
        "reference_line_count": len(reference_lines),
        "has_reference_like_entries": len(reference_lines) > 0,
        "score": 100 if reference_lines else 40,
    }


def run_apa7_audit(text: str) -> dict:
    """Run section and reference audits and return a combined summary."""

    section_report = audit_sections(text)
    reference_report = audit_references(text)

    overall_score = int((section_report["score"] * 0.6) + (reference_report["score"] * 0.4))

    return {
        "sections": section_report,
        "references": reference_report,
        "overall_score": overall_score,
    }
