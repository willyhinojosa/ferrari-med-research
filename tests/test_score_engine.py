from src.academic_score_engine import score_document


def test_score_document_returns_breakdown_and_final_score() -> None:
    data = {
        "source_count": 8,
        "peer_reviewed_ratio": 0.75,
        "apa_audit_score": 80,
        "readability": 70,
        "has_clear_sections": True,
    }

    result = score_document(data)

    assert "final_score" in result
    assert "breakdown" in result
    assert result["scale"] == "0-100"
    assert 0 <= result["final_score"] <= 100
