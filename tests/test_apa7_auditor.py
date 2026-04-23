from src.apa7_auditor import audit_sections, run_apa7_audit


def test_audit_sections_detects_expected_sections() -> None:
    text = """
    Abstract
    Introduction
    Methods
    Results
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

    assert "sections" in report
    assert "references" in report
    assert "overall_score" in report
    assert isinstance(report["overall_score"], int)
