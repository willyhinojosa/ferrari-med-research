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
        {"title": "Cardiometabolic risk in hypertension", "year": 2023},
        {"title": "Renal outcomes under guideline therapy", "year": 2022},
    ]

    result = inject_citations(_base_text(), references)

    assert "(Cardiometabolic, 2023)" in result
    assert "(Renal, 2022)" in result

    intro_block = result.split("## Discussion")[0]
    discussion_block = result.split("## Discussion")[1]
    assert "(Cardiometabolic, 2023)" in intro_block
    assert "(Renal, 2022)" in discussion_block


def test_inject_citations_is_idempotent_no_duplication() -> None:
    references = [{"title": "Clinical pathway synthesis", "year": 2024}]

    once = inject_citations(_base_text(), references)
    twice = inject_citations(once, references)

    assert once.count("(Clinical, 2024)") == 2
    assert twice.count("(Clinical, 2024)") == 2


def test_inject_citations_with_empty_references_returns_original_text() -> None:
    text = _base_text()

    assert inject_citations(text, []) == text
