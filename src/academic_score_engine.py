"""Simple scoring engine for the Ferrari Med Research MVP."""

from __future__ import annotations


def _clamp_score(value: int) -> int:
    return max(0, min(100, value))


def score_evidence_quality(data: dict) -> int:
    """Score evidence quality from source count and peer-reviewed ratio."""

    source_count = int(data.get("source_count", 0) or 0)
    peer_reviewed_ratio = float(data.get("peer_reviewed_ratio", 0.0) or 0.0)

    score = min(source_count * 8, 60) + int(peer_reviewed_ratio * 40)
    return _clamp_score(score)


def score_apa_compliance(data: dict) -> int:
    """Score APA compliance using an audit score when available."""

    apa_audit_score = int(data.get("apa_audit_score", 0) or 0)
    return _clamp_score(apa_audit_score)


def score_clarity(data: dict) -> int:
    """Score clarity using readability and structure hints."""

    readability = int(data.get("readability", 50) or 50)
    has_clear_sections = bool(data.get("has_clear_sections", False))

    bonus = 10 if has_clear_sections else 0
    return _clamp_score(readability + bonus)


def score_document(data: dict) -> dict:
    """Return a weighted final score out of 100 with category breakdown."""

    evidence = score_evidence_quality(data)
    apa = score_apa_compliance(data)
    clarity = score_clarity(data)

    final_score = int((evidence * 0.4) + (apa * 0.35) + (clarity * 0.25))

    return {
        "final_score": _clamp_score(final_score),
        "breakdown": {
            "evidence_quality": evidence,
            "apa_compliance": apa,
            "clarity": clarity,
        },
        "scale": "0-100",
    }
