"""Simple scoring engine for the Ferrari Med Research MVP."""

from __future__ import annotations

from typing import Any


def _clamp_score(value: float) -> int:
    return max(0, min(100, int(round(value))))


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def score_evidence_quality(data: dict[str, Any]) -> int:
    """Score evidence quality from source count and peer-reviewed ratio."""

    source_count = max(0, _to_int(data.get("source_count"), default=0))
    peer_reviewed_ratio = _to_float(data.get("peer_reviewed_ratio"), default=0.0)
    peer_reviewed_ratio = max(0.0, min(1.0, peer_reviewed_ratio))

    score = min(source_count * 8, 60) + (peer_reviewed_ratio * 40)
    return _clamp_score(score)


def score_apa_compliance(data: dict[str, Any]) -> int:
    """Score APA compliance using an audit score when available."""

    apa_audit_score = _to_int(data.get("apa_audit_score"), default=0)
    return _clamp_score(apa_audit_score)


def score_clarity(data: dict[str, Any]) -> int:
    """Score clarity using readability and structure hints."""

    readability = _to_int(data.get("readability"), default=50)
    has_clear_sections = bool(data.get("has_clear_sections", False))

    bonus = 10 if has_clear_sections else 0
    return _clamp_score(readability + bonus)


def _classify(total_score: int) -> str:
    if 90 <= total_score <= 100:
        return "Publicable"
    if 80 <= total_score <= 89:
        return "Sólido"
    if 70 <= total_score <= 79:
        return "Aceptable con mejoras"
    return "Requiere revisión mayor"


def score_document(data: dict[str, Any]) -> dict[str, Any]:
    """Return a weighted final score out of 100 with category breakdown."""

    evidence = score_evidence_quality(data)
    apa = score_apa_compliance(data)
    clarity = score_clarity(data)

    total_score = _clamp_score((evidence * 0.4) + (apa * 0.35) + (clarity * 0.25))
    classification = _classify(total_score)

    summary = (
        f"Puntaje total {total_score}/100. "
        f"Clasificación: {classification}. "
        f"Evidencia {evidence}, APA {apa}, Claridad {clarity}."
    )

    return {
        "total_score": total_score,
        "classification": classification,
        "breakdown": {
            "evidence_quality": evidence,
            "apa_compliance": apa,
            "clarity": clarity,
        },
        "summary": summary,
    }
