"""DOCX export utilities for APA-style manuscript formatting."""

from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
from typing import Any

_DOCX_AVAILABLE = importlib.util.find_spec("docx") is not None

if _DOCX_AVAILABLE:
    Document = importlib.import_module("docx").Document
    WD_ALIGN_PARAGRAPH = importlib.import_module("docx.enum.text").WD_ALIGN_PARAGRAPH
    Inches = importlib.import_module("docx.shared").Inches
    Pt = importlib.import_module("docx.shared").Pt


def _set_document_defaults(document: Any) -> None:
    """Apply APA-like baseline formatting to the document."""

    if not _DOCX_AVAILABLE:
        return

    section = document.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    normal_style = document.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)

    paragraph_format = normal_style.paragraph_format
    paragraph_format.line_spacing = 2.0
    paragraph_format.space_before = Pt(0)
    paragraph_format.space_after = Pt(0)


def _add_title_page(document: Any, metadata: dict[str, Any] | None) -> None:
    """Add a simple title page from provided metadata."""

    if not _DOCX_AVAILABLE:
        return

    data = metadata or {}
    fields = [
        str(data.get("title") or "Untitled Manuscript").strip(),
        str(data.get("author") or "").strip(),
        str(data.get("institution") or "").strip(),
        str(data.get("course") or "").strip(),
        str(data.get("instructor") or "").strip(),
        str(data.get("date") or "").strip(),
    ]

    for index, value in enumerate(fields):
        if not value:
            continue
        paragraph = document.add_paragraph(value)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if index == 0:
            paragraph.runs[0].bold = True

    document.add_paragraph("")


def _add_heading(document: Any, text: str, level: int) -> None:
    """Add centered title heading or APA section heading."""

    if not _DOCX_AVAILABLE:
        return

    cleaned_text = text.strip()
    if not cleaned_text:
        return

    paragraph = document.add_paragraph(cleaned_text)
    run = paragraph.runs[0]

    if level == 1:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run.bold = True
    else:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run.bold = True


def _add_paragraph(document: Any, text: str) -> None:
    """Add a standard paragraph with APA-like indentation."""

    if not _DOCX_AVAILABLE:
        return

    paragraph = document.add_paragraph(text.strip())
    paragraph.paragraph_format.first_line_indent = Inches(0.5)


def _add_references(document: Any, references: list[str]) -> None:
    """Add references with hanging indentation."""

    if not _DOCX_AVAILABLE:
        return

    for reference in references:
        cleaned = reference.strip()
        if not cleaned:
            continue
        if cleaned.startswith("- "):
            cleaned = cleaned[2:].strip()
        paragraph = document.add_paragraph(cleaned)
        paragraph.paragraph_format.left_indent = Inches(0.5)
        paragraph.paragraph_format.first_line_indent = Inches(-0.5)


def _fallback_write_docx_placeholder(output_path: Path, manuscript_markdown: str) -> None:
    """Write a deterministic placeholder .docx when python-docx is unavailable."""

    content = manuscript_markdown.strip() or "Ferrari Med Research manuscript export."
    output_path.write_bytes(content.encode("utf-8"))


def export_manuscript_to_docx(
    manuscript_markdown: str,
    output_path: str,
    metadata: dict[str, Any] | None = None,
) -> str:
    """Export markdown manuscript text into a .docx with APA-style formatting."""

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    if not _DOCX_AVAILABLE:
        _fallback_write_docx_placeholder(destination, manuscript_markdown)
        return str(destination)

    document = Document()
    _set_document_defaults(document)
    _add_title_page(document, metadata)

    lines = manuscript_markdown.splitlines() if manuscript_markdown else []
    paragraph_buffer: list[str] = []
    in_references = False
    references_buffer: list[str] = []

    def flush_paragraph_buffer() -> None:
        nonlocal paragraph_buffer
        if paragraph_buffer:
            combined = " ".join(part.strip() for part in paragraph_buffer if part.strip()).strip()
            if combined:
                _add_paragraph(document, combined)
            paragraph_buffer = []

    for raw_line in lines:
        stripped = raw_line.strip()

        if stripped.startswith("## "):
            flush_paragraph_buffer()
            heading_text = stripped[3:].strip()
            _add_heading(document, heading_text, level=2)
            in_references = heading_text.lower() == "references"
            continue

        if stripped.startswith("# "):
            flush_paragraph_buffer()
            _add_heading(document, stripped[2:].strip(), level=1)
            in_references = False
            continue

        if not stripped:
            flush_paragraph_buffer()
            continue

        if in_references:
            references_buffer.append(stripped)
        else:
            paragraph_buffer.append(stripped)

    flush_paragraph_buffer()

    if references_buffer:
        _add_references(document, references_buffer)

    document.save(destination)
    return str(destination)
