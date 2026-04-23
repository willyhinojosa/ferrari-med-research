"""Utilities for splitting raw manuscript text into canonical sections."""

from __future__ import annotations

import re

_SECTION_KEYS = ("abstract", "introduction", "discussion", "references")
_HEADING_PATTERN = re.compile(r"(?im)^\s*(abstract|introduction|discussion|references)\s*[:\-]?\s*$")


def _clean_content(section_name: str, content: str) -> str:
    """Normalize whitespace and remove repeated section labels from content."""

    text = (content or "").strip()
    if not text:
        return ""

    label_pattern = re.compile(rf"(?im)^\s*{re.escape(section_name)}\s*[:\-]?\s*$")
    lines = [line for line in text.splitlines() if not label_pattern.match(line)]

    return "\n".join(lines).strip()


def split_sections(text: str) -> dict[str, str]:
    """Split manuscript text into abstract/introduction/discussion/references sections."""

    source = text or ""
    sections: dict[str, str] = {key: "" for key in _SECTION_KEYS}

    matches = list(_HEADING_PATTERN.finditer(source))
    if not matches:
        return sections

    for index, match in enumerate(matches):
        section_name = match.group(1).lower()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        extracted = _clean_content(section_name, source[start:end])

        if extracted and not sections[section_name]:
            sections[section_name] = extracted

    return sections
