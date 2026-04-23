from src.apa7_auditor import audit_sections, run_apa7_audit


def test_audit_sections_detects_required_sections() -> None:
    text = """
    Abstract
    Introduction
    Discussion
    References
    """
    report = audit_sections(text)

    assert report["missing"] == []
    assert report["found"]["abstract"] is True


def test_run_apa7_audit_returns_expected_structure() -> None:
    text = """
    Introduction
    Discussion
    References
    Doe, J. (2020). Sample title.
    """
    report = run_apa7_audit(text)

    assert "has_required_sections" in report
    assert "missing_sections" in report
    assert "reference_line_count" in report
    assert "warnings" in report
    assert isinstance(report["reference_line_count"], int)


def test_run_apa7_audit_reports_missing_sections_and_warning() -> None:
    text = "Introduction\nSome body text"
    report = run_apa7_audit(text)

    assert report["has_required_sections"] is False
    assert "abstract" in report["missing_sections"]
    assert "references" in report["missing_sections"]
    assert len(report["warnings"]) >= 1


def test_run_apa7_audit_handles_empty_input_safely() -> None:
    report = run_apa7_audit("")

    assert report["has_required_sections"] is False
    assert report["reference_line_count"] == 0
    assert report["missing_sections"]
    assert "Input text is empty." in report["warnings"]
