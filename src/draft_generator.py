"""Markdown manuscript draft generator for Ferrari Med Research."""

from __future__ import annotations

from typing import Any


def generate_title_page(intake: dict[str, Any]) -> str:
    """Build a simple academic title page section in markdown."""

    title = str(intake.get("title") or intake.get("topic") or "Untitled Manuscript").strip()
    document_type = str(intake.get("document_type") or "Unspecified").strip()
    topic = str(intake.get("topic") or "Unspecified").strip()
    language = str(intake.get("language") or "Unspecified").strip()
    academic_level = str(intake.get("academic_level") or "Unspecified").strip()

    return (
        "## Title Page\n\n"
        f"# {title}\n\n"
        f"- **Document Type:** {document_type}\n"
        f"- **Topic:** {topic}\n"
        f"- **Language:** {language}\n"
        f"- **Academic Level:** {academic_level}"
    )


def generate_abstract_section(text: str) -> str:
    """Build the abstract section using available manuscript text."""

    clean_text = (text or "").strip()
    abstract_text = clean_text if clean_text else "Abstract content not provided."
    return f"## Abstract\n\n{abstract_text}"


def generate_keywords_section(intake: dict[str, Any]) -> str:
    """Build the keywords section from intake metadata."""

    keywords: list[str] = []
    for key in ("topic", "document_type", "academic_level"):
        value = intake.get(key)
        if isinstance(value, str):
            cleaned = value.strip()
            if cleaned:
                keywords.append(cleaned)

    if not keywords:
        keywords = ["medical research", "manuscript draft"]

    return f"## Keywords\n\n{', '.join(keywords)}"


def generate_main_body(text: str) -> str:
    """Build required Introduction and Discussion sections."""

    clean_text = (text or "").strip()
    if not clean_text:
        clean_text = "Content pending from validated manuscript text."

    return (
        "## Introduction\n\n"
        f"{clean_text}\n\n"
        "## Discussion\n\n"
        f"{clean_text}"
    )


def generate_references_section(references_checked: list[dict[str, Any]]) -> str:
    """Build references from DOI-validated references only."""

    valid_items = [item for item in references_checked if item.get("is_valid_doi")]

    if not valid_items:
        return "## References\n\nReferences require validation before final inclusion."

    lines: list[str] = []
    for item in valid_items:
        original_entry = item.get("original_entry", {})
        if isinstance(original_entry, dict):
            title = str(original_entry.get("title") or "Untitled reference").strip()
        else:
            title = "Untitled reference"
        doi = str(item.get("normalized_doi") or "").strip()
        lines.append(f"- {title}. https://doi.org/{doi}")

    return "## References\n\n" + "\n".join(lines)


def generate_manuscript(intake: dict[str, Any], text: str, references_checked: list[dict[str, Any]]) -> str:
    """Generate the full markdown manuscript draft in required section order."""

    sections = [
        generate_title_page(intake),
        generate_abstract_section(text),
        generate_keywords_section(intake),
        generate_main_body(text),
        generate_references_section(references_checked),
    ]
    return "\n\n".join(sections) + "\n"
