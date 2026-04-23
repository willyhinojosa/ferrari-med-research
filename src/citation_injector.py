"""Deterministic inline citation injector for manuscript sections."""

from __future__ import annotations

import re
from typing import Any

_STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
    "without",
}


def _extract_title(reference: dict[str, Any]) -> str:
    if not isinstance(reference, dict):
        return ""

    direct_title = reference.get("title")
    if isinstance(direct_title, str) and direct_title.strip():
        return direct_title.strip()

    original_entry = reference.get("original_entry")
    if isinstance(original_entry, dict):
        nested_title = original_entry.get("title")
        if isinstance(nested_title, str) and nested_title.strip():
            return nested_title.strip()

    return ""


def _extract_year(reference: dict[str, Any]) -> str:
    if not isinstance(reference, dict):
        return "n.d."

    for key in ("year", "publication_year", "published_year"):
        value = reference.get(key)
        if isinstance(value, int):
            return str(value)
        if isinstance(value, str):
            match = re.search(r"\b(19|20)\d{2}\b", value)
            if match:
                return match.group(0)

    original_entry = reference.get("original_entry")
    if isinstance(original_entry, dict):
        for key in ("year", "publication_year", "published_year"):
            value = original_entry.get(key)
            if isinstance(value, int):
                return str(value)
            if isinstance(value, str):
                match = re.search(r"\b(19|20)\d{2}\b", value)
                if match:
                    return match.group(0)

    return "n.d."


def _extract_label(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9']+", title)
    if not words:
        return "Study"

    for word in words:
        normalized = word.strip("'").lower()
        if normalized in _STOPWORDS:
            continue
        if len(normalized) < 3:
            continue
        if not re.search(r"[a-z]", normalized):
            continue
        if not re.fullmatch(r"[a-z0-9']+", normalized):
            continue
        return normalized.capitalize()

    fallback = re.sub(r"[^A-Za-z]", "", words[0])
    return fallback.capitalize() if len(fallback) >= 3 else "Study"


def _build_citations(references: list[dict[str, Any]]) -> list[str]:
    seen: set[tuple[str, str]] = set()
    citations: list[str] = []

    for reference in references:
        title = _extract_title(reference)
        label = _extract_label(title)
        year = _extract_year(reference)
        key = (label, year)
        if key in seen:
            continue
        seen.add(key)
        citations.append(f"({label}, {year})")

    return citations


def _insert_citation_in_section(text: str, section_name: str, citation: str) -> str:
    section_pattern = re.compile(rf"(?ms)^(##\s+{re.escape(section_name)}\s*\n\n)(.*?)(?=^##\s+|\Z)")

    def _replace(match: re.Match[str]) -> str:
        header = match.group(1)
        body = match.group(2)
        if citation in body:
            return match.group(0)

        sentences = re.split(r"(?<=[.!?])\s+", body.strip())
        if not sentences:
            return match.group(0)

        updated = False
        for index, sentence in enumerate(sentences):
            if citation in sentence:
                updated = True
                break
            if not re.search(r"[A-Za-z0-9]", sentence):
                continue
            punct_match = re.search(r"([.!?])$", sentence)
            if punct_match:
                sentences[index] = sentence[:-1] + f" {citation}" + punct_match.group(1)
            else:
                sentences[index] = sentence + f" {citation}"
            updated = True
            break

        if not updated:
            return match.group(0)

        trailing = "\n\n" if body.endswith("\n\n") else ("\n" if body.endswith("\n") else "")
        return header + " ".join(sentences) + trailing

    return section_pattern.sub(_replace, text, count=1)


def inject_citations(text: str, references: list[dict]) -> str:
    """Inject deterministic APA-style inline citations into Introduction and Discussion."""

    if not isinstance(text, str) or not text.strip():
        return text

    if not isinstance(references, list) or not references:
        return text

    valid_references = [
        ref
        for ref in references
        if isinstance(ref, dict) and ref.get("is_valid_doi") is True
    ]
    if not valid_references:
        return text

    citations = _build_citations(valid_references)
    if not citations:
        return text

    intro_citation = citations[0]
    discussion_citation = citations[1] if len(citations) > 1 else citations[0]

    updated = _insert_citation_in_section(text, "Introduction", intro_citation)
    updated = _insert_citation_in_section(updated, "Discussion", discussion_citation)
    return updated
