from src.draft_generator import (
    generate_keywords_section,
    generate_manuscript,
    generate_references_section,
    generate_title_page,
)


def test_title_page_generation_contains_expected_fields() -> None:
    intake = {
        "title": "Clinical Trends in Hypertension",
        "topic": "Hypertension",
        "document_type": "Review",
        "language": "English",
        "academic_level": "Graduate",
    }

    result = generate_title_page(intake)

    assert "## Title Page" in result
    assert "# Clinical Trends in Hypertension" in result
    assert "**Document Type:** Review" in result


def test_keyword_section_presence_includes_intake_terms() -> None:
    intake = {
        "topic": "Cardiology",
        "document_type": "Meta-analysis",
        "academic_level": "Postgraduate",
    }

    result = generate_keywords_section(intake)

    assert result.startswith("## Keywords")
    assert "Cardiology" in result
    assert "Meta-analysis" in result


def test_references_section_filters_invalid_references() -> None:
    references_checked = [
        {
            "original_entry": {"title": "Valid Paper", "doi": "10.1000/xyz123"},
            "normalized_doi": "10.1000/xyz123",
            "is_valid_doi": True,
            "errors": [],
        },
        {
            "original_entry": {"title": "Invalid Paper", "doi": "bad-doi"},
            "normalized_doi": "bad-doi",
            "is_valid_doi": False,
            "errors": ["Invalid DOI format."],
        },
    ]

    result = generate_references_section(references_checked)

    assert "Valid Paper" in result
    assert "10.1000/xyz123" in result
    assert "Invalid Paper" not in result


def test_final_manuscript_structure() -> None:
    intake = {
        "title": "Sample Title",
        "topic": "Diabetes",
        "document_type": "Review",
        "language": "English",
        "academic_level": "Graduate",
    }
    text = "This is validated manuscript content."
    references_checked = []

    result = generate_manuscript(intake, text, references_checked)

    expected_order = [
        "## Title Page",
        "## Abstract",
        "## Keywords",
        "## Introduction",
        "## Discussion",
        "## References",
    ]

    positions = [result.index(section) for section in expected_order]
    assert positions == sorted(positions)
    assert "References require validation before final inclusion." in result


def test_generate_manuscript_injects_citations_without_changing_references() -> None:
    intake = {
        "title": "Citation Test",
        "topic": "Kidney Disease",
        "document_type": "Review",
        "language": "English",
        "academic_level": "Graduate",
    }

    references_checked = [
        {
            "original_entry": {"title": "Guideline adherence outcomes", "year": 2021, "doi": "10.1000/one"},
            "normalized_doi": "10.1000/one",
            "is_valid_doi": True,
            "errors": [],
        },
        {
            "original_entry": {"title": "Biomarker progression analysis", "year": 2020, "doi": "10.1000/two"},
            "normalized_doi": "10.1000/two",
            "is_valid_doi": True,
            "errors": [],
        },
    ]

    manuscript = generate_manuscript(intake, "", references_checked)

    intro_block = manuscript.split("## Discussion")[0]
    discussion_block = manuscript.split("## Discussion")[1]

    assert "(Guideline, 2021)" in intro_block
    assert "(Biomarker, 2020)" in discussion_block
    assert "- Guideline adherence outcomes. https://doi.org/10.1000/one" in manuscript
    assert "- Biomarker progression analysis. https://doi.org/10.1000/two" in manuscript
