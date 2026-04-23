from src.doi_validator import is_valid_doi_format, normalize_doi


def test_normalize_doi_removes_url_prefix() -> None:
    raw = "https://doi.org/10.1000/ABC123"
    assert normalize_doi(raw) == "10.1000/abc123"


def test_normalize_doi_trims_whitespace() -> None:
    raw = "  10.5555/xyz-123  "
    assert normalize_doi(raw) == "10.5555/xyz-123"


def test_valid_doi_format_returns_true_for_standard_doi() -> None:
    assert is_valid_doi_format("10.1016/j.jmb.2010.12.004") is True


def test_valid_doi_format_returns_false_for_invalid_value() -> None:
    assert is_valid_doi_format("doi:abc") is False
