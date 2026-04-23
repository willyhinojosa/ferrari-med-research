from src.citation_injector import inject_citations


def _base_text() -> str:
    return (
        "## Introduction\n\n"
        "This section introduces the topic. It outlines core context.\n\n"
        "## Discussion\n\n"
        "This section interprets evidence. It states implications.\n\n"
        "## References\n\n"
        "- Placeholder reference."
    )


def test_inject_citations_adds_intro_and_discussion_citations() -> None:
    references = [
        {"title": "Cardiometabolic risk in hypertension", "year": 2023, "is_valid_doi": True},
        {"title": "Renal outcomes under guideline therapy", "year": 2022, "is_valid_doi": True},
    ]

    result = inject_citations(_base_text(), references)

    assert "(Cardiometabolic, 2023)" in result
    assert "(Renal, 2022)" in result

    intro_block = result.split("## Discussion")[0]
    discussion_block = result.split("## Discussion")[1]
    assert "(Cardiometabolic, 2023)" in intro_block
    assert "(Renal, 2022)" in discussion_block


def test_inject_citations_is_idempotent_no_duplication() -> None:
    references = [{"title": "Clinical pathway synthesis", "year": 2024, "is_valid_doi": True}]

    once = inject_citations(_base_text(), references)
    twice = inject_citations(once, references)

    assert once.count("(Clinical, 2024)") == 2
    assert twice.count("(Clinical, 2024)") == 2


def test_inject_citations_with_empty_references_returns_original_text() -> None:
    text = _base_text()

    assert inject_citations(text, []) == text


def test_inject_citations_ignores_invalid_references() -> None:
    text = _base_text()
    references = [
        {"title": "123 ## @@ title", "year": 2021, "is_valid_doi": False},
        {"title": "Valid biomarker trajectory analysis", "year": 2020, "is_valid_doi": True},
        {
            "invalid_references": [
                {"title": "Should not be used", "year": 2019, "is_valid_doi": False}
            ]
        },
    ]

    result = inject_citations(text, references)

    assert "(Valid, 2020)" in result
    assert "(Should, 2019)" not in result
    assert "(Study, 2021)" not in result


def test_inject_citations_with_no_valid_references_returns_original_text() -> None:
    text = _base_text()
    references = [
        {"title": "Clinical trend report", "year": 2024, "is_valid_doi": False},
        {"title": "Another source", "year": 2023},
    ]

    assert inject_citations(text, references) == text


def test_inject_citations_places_single_citation_per_target_section() -> None:
    references = [
        {"title": "The 2024/2025 pooled-analysis update", "year": 2025, "is_valid_doi": True},
        {"title": "Renal outcomes under guideline therapy", "year": 2022, "is_valid_doi": True},
    ]

    result = inject_citations(_base_text(), references)
    intro_block = result.split("## Discussion")[0]
    discussion_block = result.split("## Discussion")[1]

    assert intro_block.count("(Pooled, 2025)") == 1
    assert discussion_block.count("(Renal, 2022)") == 1
