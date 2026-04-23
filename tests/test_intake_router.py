import pytest

from src.intake_router import IntakeSpec, normalize_intake, validate_intake


def test_validate_intake_requires_expected_fields() -> None:
    ok, errors = validate_intake({"topic": "X"})

    assert ok is False
    assert "Missing required field: document_type" in errors
    assert "Missing required field: language" in errors
    assert "Missing required field: academic_level" in errors
    assert "Missing required field: source_mode" in errors


def test_validate_intake_rejects_empty_required_fields() -> None:
    payload = {
        "topic": "   ",
        "document_type": "",
        "language": "   ",
        "academic_level": "",
        "source_mode": "",
    }

    ok, errors = validate_intake(payload)

    assert ok is False
    assert "Field 'topic' cannot be empty." in errors
    assert "Field 'source_mode' cannot be empty." in errors


def test_normalize_intake_normalizes_whitespace_and_case() -> None:
    payload = {
        "topic": "  Cardio   risk   ",
        "document_type": "  REVIEW PAPER ",
        "language": "  English ",
        "academic_level": "  Postgraduate  ",
        "source_mode": "  MIXED ",
        "title": "  A   Study ",
        "body_text": "  line  one   ",
        "references": [{"doi": "10.1000/xyz"}],
    }

    result = normalize_intake(payload)

    assert isinstance(result, IntakeSpec)
    assert result.topic == "Cardio risk"
    assert result.document_type == "review paper"
    assert result.source_mode == "mixed"
    assert result.title == "A Study"


def test_normalize_intake_raises_for_invalid_payload() -> None:
    with pytest.raises(ValueError, match="Invalid intake payload"):
        normalize_intake({"topic": "only topic"})
