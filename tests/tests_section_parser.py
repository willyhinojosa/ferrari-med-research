from src.section_parser import split_sections


def test_split_sections_correctly_assigns_content() -> None:
    text = """
    Abstract
    Abstract summary.
    Introduction
    Intro paragraph.
    Discussion
    Discussion paragraph.
    References
    Ref A
    """

    result = split_sections(text)

    assert result["abstract"] == "Abstract summary."
    assert result["introduction"] == "Intro paragraph."
    assert result["discussion"] == "Discussion paragraph."
    assert result["references"] == "Ref A"


def test_split_sections_handles_missing_sections() -> None:
    text = """
    Introduction
    Intro only.
    """

    result = split_sections(text)

    assert result["abstract"] == ""
    assert result["introduction"] == "Intro only."
    assert result["discussion"] == ""
    assert result["references"] == ""


def test_split_sections_supports_mixed_case_headers() -> None:
    text = """
    aBsTrAcT
    Mixed case abstract.
    INTRODUCTION
    Mixed case intro.
    dIsCuSsIoN
    Mixed case discussion.
    ReFeReNcEs
    Mixed case refs.
    """

    result = split_sections(text)

    assert result["abstract"] == "Mixed case abstract."
    assert result["introduction"] == "Mixed case intro."
    assert result["discussion"] == "Mixed case discussion."
    assert result["references"] == "Mixed case refs."


def test_split_sections_removes_duplicated_markers_inside_content() -> None:
    text = """
    Abstract
    Abstract
    Primary abstract.
    Introduction
    Introduction
    Primary introduction.
    Discussion
    discussion
    Primary discussion.
    References
    References
    Primary refs.
    """

    result = split_sections(text)

    assert result["abstract"] == "Primary abstract."
    assert result["introduction"] == "Primary introduction."
    assert result["discussion"] == "Primary discussion."
    assert result["references"] == "Primary refs."
