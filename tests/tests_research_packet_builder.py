from src.research_packet_builder import build_research_packet


def _intake() -> dict:
    return {
        "topic": "Heart failure outcomes",
        "document_type": "Review",
        "academic_level": "Postgraduate",
    }


def test_valid_reference_filtering() -> None:
    references_checked = [
        {"normalized_doi": "10.1000/ok1", "is_valid_doi": True, "errors": []},
        {"normalized_doi": "10.1000/bad", "is_valid_doi": False, "errors": ["Invalid DOI format."]},
        {"normalized_doi": "10.1000/ok2", "is_valid_doi": True, "errors": []},
    ]

    packet = build_research_packet(_intake(), references_checked)

    assert len(packet["valid_references"]) == 2
    assert all(item["is_valid_doi"] is True for item in packet["valid_references"])


def test_invalid_reference_counting() -> None:
    references_checked = [
        {"is_valid_doi": True},
        {"is_valid_doi": False},
        {"errors": ["Missing DOI."]},
    ]

    packet = build_research_packet(_intake(), references_checked)

    assert packet["reference_count"] == 1
    assert packet["invalid_reference_count"] == 2
    assert len(packet["invalid_references"]) == 2


def test_evidence_notes_generation() -> None:
    references_checked = [
        {"is_valid_doi": True},
        {"is_valid_doi": True},
        {"is_valid_doi": False},
    ]

    packet = build_research_packet(_intake(), references_checked)

    assert packet["evidence_notes"] == [
        "2 validated references available.",
        "1 reference requires correction before final inclusion.",
    ]


def test_expected_output_structure() -> None:
    packet = build_research_packet(_intake(), [{"is_valid_doi": True}, {"is_valid_doi": False}])

    expected_keys = {
        "topic",
        "document_type",
        "academic_level",
        "valid_references",
        "invalid_references",
        "reference_count",
        "invalid_reference_count",
        "evidence_notes",
    }

    assert set(packet.keys()) == expected_keys
    assert packet["topic"] == "Heart failure outcomes"
    assert packet["document_type"] == "Review"
    assert packet["academic_level"] == "Postgraduate"
