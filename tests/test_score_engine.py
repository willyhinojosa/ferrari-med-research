from src.academic_score_engine import score_document


def test_score_document_returns_v2_structure() -> None:
    data = {
        "source_count": 8,
        "peer_reviewed_ratio": 0.75,
        "apa_audit_score": 80,
        "readability": 70,
        "has_clear_sections": True,
    }

    result = score_document(data)

    assert "total_score" in result
    assert "classification" in result
    assert "breakdown" in result
    assert "summary" in result
    assert 0 <= result["total_score"] <= 100


def test_score_document_clamps_and_handles_invalid_inputs() -> None:
    data = {
        "source_count": -10,
        "peer_reviewed_ratio": "not-number",
        "apa_audit_score": 999,
        "readability": -50,
        "has_clear_sections": True,
    }

    result = score_document(data)

    assert result["breakdown"]["evidence_quality"] == 0
    assert result["breakdown"]["apa_compliance"] == 100
    assert result["breakdown"]["clarity"] == 0
    assert result["classification"] in {
        "Publicable",
        "Sólido",
        "Aceptable con mejoras",
        "Requiere revisión mayor",
    }


def test_score_document_classification_boundaries() -> None:
    pub = score_document({
        "source_count": 20,
        "peer_reviewed_ratio": 1.0,
        "apa_audit_score": 100,
        "readability": 100,
        "has_clear_sections": True,
    })
    mayor = score_document({
        "source_count": 0,
        "peer_reviewed_ratio": 0,
        "apa_audit_score": 0,
        "readability": 0,
        "has_clear_sections": False,
    })

    assert pub["classification"] == "Publicable"
    assert mayor["classification"] == "Requiere revisión mayor"
