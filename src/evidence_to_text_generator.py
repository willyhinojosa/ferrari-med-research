"""Deterministic evidence-to-text helpers for manuscript drafting."""

from __future__ import annotations


def _normalize_topic(packet: dict) -> str:
    topic = packet.get("topic") if isinstance(packet, dict) else ""
    if isinstance(topic, str) and topic.strip():
        return topic.strip()
    return "the selected medical topic"


def _valid_reference_count(packet: dict) -> int:
    valid_refs = packet.get("valid_references") if isinstance(packet, dict) else []
    if isinstance(valid_refs, list):
        return len(valid_refs)
    return 0


def _notes_text(packet: dict) -> str:
    evidence_notes = packet.get("evidence_notes") if isinstance(packet, dict) else []
    if not isinstance(evidence_notes, list):
        return ""

    normalized_notes = [str(note).strip() for note in evidence_notes if str(note).strip()]
    return " ".join(normalized_notes)


def _evidence_level_statement(valid_count: int) -> str:
    if valid_count >= 5:
        return "Multiple validated studies suggest a consistent evidence base."
    if valid_count >= 2:
        return "Several validated studies suggest an emerging but coherent evidence base."
    if valid_count == 1:
        return "A single validated study is available, so conclusions remain preliminary."
    return "No validated studies are currently available, so claims should be interpreted cautiously."


def generate_abstract(packet: dict) -> str:
    """Generate a concise abstract grounded in validated evidence metadata."""

    topic = _normalize_topic(packet)
    valid_count = _valid_reference_count(packet)
    notes = _notes_text(packet)

    components = [
        f"This manuscript reviews current evidence on {topic}.",
        _evidence_level_statement(valid_count),
        "The synthesis prioritizes validated references and avoids unverified numeric claims.",
    ]

    if notes:
        components.append(f"Evidence context: {notes}")

    return " ".join(components)


def generate_introduction(packet: dict) -> str:
    """Generate an introduction section using deterministic evidence cues."""

    topic = _normalize_topic(packet)
    valid_count = _valid_reference_count(packet)

    limitation = (
        "Because the validated reference pool is limited, this introduction frames the topic conservatively."
        if valid_count < 2
        else "The available validated references allow a focused overview of current conceptual understanding."
    )

    return (
        f"{topic} remains an important area for clinical and translational inquiry. "
        f"{_evidence_level_statement(valid_count)} "
        f"{limitation} "
        "Accordingly, the manuscript emphasizes reproducible interpretation of validated literature."
    )


def generate_discussion(packet: dict) -> str:
    """Generate a discussion section from evidence structure without overclaiming."""

    topic = _normalize_topic(packet)
    valid_count = _valid_reference_count(packet)
    notes = _notes_text(packet)

    limitation_sentence = (
        "The limited number of validated references constrains generalizability and supports cautious interpretation."
        if valid_count < 3
        else "The validated reference set provides moderate support, though heterogeneity should still be considered."
    )

    discussion = (
        f"The discussion of {topic} indicates directionally consistent themes across validated sources. "
        f"{_evidence_level_statement(valid_count)} "
        f"{limitation_sentence} "
        "Future work should expand high-quality validation and refine methodology-specific comparisons."
    )

    if notes:
        return f"{discussion} Evidence notes: {notes}"

    return discussion
