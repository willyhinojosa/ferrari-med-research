from src.evidence_to_text_generator import generate_abstract, generate_discussion, generate_introduction


def test_generator_outputs_are_non_empty() -> None:
    packet = {
        "topic": "Hypertension management",
        "valid_references": [{"normalized_doi": "10.1000/a"}, {"normalized_doi": "10.1000/b"}],
        "evidence_notes": ["2 validated references available."],
    }

    assert generate_abstract(packet).strip()
    assert generate_introduction(packet).strip()
    assert generate_discussion(packet).strip()


def test_generator_reflects_reference_volume() -> None:
    low_packet = {
        "topic": "Hypertension",
        "valid_references": [],
        "evidence_notes": [],
    }
    high_packet = {
        "topic": "Hypertension",
        "valid_references": [{"normalized_doi": "10.1/a"}] * 5,
        "evidence_notes": [],
    }

    low_text = generate_abstract(low_packet)
    high_text = generate_abstract(high_packet)

    assert "No validated studies" in low_text
    assert "Multiple validated studies" in high_text


def test_generator_handles_empty_evidence_packet() -> None:
    packet = {"topic": "Rare disease", "valid_references": [], "evidence_notes": []}

    introduction = generate_introduction(packet)
    discussion = generate_discussion(packet)

    assert "conservatively" in introduction
    assert "limited number of validated references" in discussion
