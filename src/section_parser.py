"""Utilities for splitting raw manuscript text into canonical sections."""

from __future__ import annotations

import re

_SECTION_KEYS = ("abstract", "introduction", "discussion", "references")
_SECTION_SET = set(_SECTION_KEYS)
_SECTION_LABEL_PATTERN = re.compile(r"^\s*(abstract|introduction|discussion|references)\s*[:\-]?\s*$", re.IGNORECASE)


def _clean_content(section_name: str, lines: list[str]) -> str:
    """Normalize whitespace and remove repeated section labels from content."""

    cleaned_lines: list[str] = []
    own_label = re.compile(rf"^\s*{re.escape(section_name)}\s*[:\-]?\s*$", re.IGNORECASE)

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            # Preserve paragraph boundaries while trimming leading/trailing empties later.
            cleaned_lines.append("")
            continue
        if own_label.match(line):
            continue
        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines).strip()
    # Collapse excessive blank lines to avoid noisy output.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def split_sections(text: str) -> dict[str, str]:
    """Split manuscript text into abstract/introduction/discussion/references sections."""

    sections: dict[str, list[str]] = {key: [] for key in _SECTION_KEYS}
    current_section: str | None = None

    for line in (text or "").splitlines():
        heading_match = _SECTION_LABEL_PATTERN.match(line)
        if heading_match:
            current_section = heading_match.group(1).lower()
            continue

        if current_section in _SECTION_SET:
            sections[current_section].append(line)

    return {name: _clean_content(name, content_lines) for name, content_lines in sections.items()}
