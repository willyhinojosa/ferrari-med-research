from src.doi_validator import is_valid_doi_format, normalize_doi, validate_reference_entry


def test_normalize_doi_supports_url_and_dx_url() -> None:
    assert normalize_doi("https://doi.org/10.1000/ABC123") == "10.1000/abc123"
    assert normalize_doi("http://dx.doi.org/10.5555/xyz-123") == "10.5555/xyz-123"


def test_normalize_doi_handles_raw_doi_and_markers() -> None:
    raw = " doi:10.1016/J.JMB.2010.12.004. "
    assert normalize_doi(raw) == "10.1016/j.jmb.2010.12.004"


def test_valid_doi_format_returns_true_for_standard_doi() -> None:
    assert is_valid_doi_format("10.1016/j.jmb.2010.12.004") is True


def test_valid_doi_format_returns_false_for_invalid_values() -> None:
    assert is_valid_doi_format("doi:abc") is False
    assert is_valid_doi_format("10.1000") is False


def test_validate_reference_entry_returns_structured_result_valid() -> None:
    entry = {"title": "Paper", "doi": "https://doi.org/10.1000/xyz"}
    result = validate_reference_entry(entry)

    assert result["original_entry"] == entry
    assert result["normalized_doi"] == "10.1000/xyz"
    assert result["is_valid_doi"] is True
    assert result["errors"] == []


def test_validate_reference_entry_handles_missing_and_non_string_doi() -> None:
    missing = validate_reference_entry({"title": "No DOI"})
    non_string = validate_reference_entry({"doi": 12345})

    assert missing["is_valid_doi"] is False
    assert "Missing DOI." in missing["errors"]

    assert non_string["is_valid_doi"] is False
    assert "DOI must be a string." in non_string["errors"]
