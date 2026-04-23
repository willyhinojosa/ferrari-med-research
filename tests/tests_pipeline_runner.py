from src.pipeline_runner import run_pipeline


def _valid_intake() -> dict:
    return {
        "topic": "Hypertension outcomes",
        "document_type": "Review",
        "language": "English",
        "academic_level": "Graduate",
        "source_mode": "Mixed",
        "title": "Sample",
        "body_text": "Sample body",
    }


def _sample_text() -> str:
    return """
    Abstract
    Brief abstract text.
    Introduction
    Intro text.
    Discussion
    Discussion text.
    References
    Doe, J. (2023). Sample study title.
    """


def test_run_pipeline_valid_intake_flow() -> None:
    refs = [{"doi": "10.1000/xyz123"}, {"doi": "https://doi.org/10.5555/abc"}]

    result = run_pipeline(_valid_intake(), _sample_text(), refs)

    assert result["intake_valid"] is True
    assert result["intake_errors"] == []
    assert result["pipeline_status"] == "ok"
    assert "total_score" in result["score"]
    assert "manuscript_draft" in result
    assert "research_packet" in result
    assert "## Title Page" in result["manuscript_draft"]
    assert result["research_packet"]["reference_count"] == 2


def test_run_pipeline_invalid_intake_flow() -> None:
    invalid = {"topic": "Only topic"}

    result = run_pipeline(invalid, _sample_text(), [{"doi": "10.1000/ok"}])

    assert result["intake_valid"] is False
    assert result["pipeline_status"] == "invalid_intake"
    assert len(result["intake_errors"]) >= 1


def test_run_pipeline_reference_counting() -> None:
    refs = [
        {"doi": "10.1000/valid-one"},
        {"doi": "bad-doi"},
        {"title": "Missing DOI"},
    ]

    result = run_pipeline(_valid_intake(), _sample_text(), refs)

    assert len(result["references_checked"]) == 3
    assert result["invalid_reference_count"] == 2


def test_run_pipeline_status_values_are_expected() -> None:
    ok_result = run_pipeline(_valid_intake(), _sample_text(), [])
    bad_result = run_pipeline({"topic": "missing required fields"}, _sample_text(), [])

    assert ok_result["pipeline_status"] == "ok"
    assert bad_result["pipeline_status"] == "invalid_intake"
