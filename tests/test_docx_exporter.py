from __future__ import annotations

from pathlib import Path

from src.docx_exporter import export_manuscript_to_docx


def test_export_creates_docx_file(tmp_path: Path) -> None:
    markdown = "# Sample Title\n\n## Introduction\n\nThis is a test paragraph."
    output_path = tmp_path / "manuscript.docx"

    result = export_manuscript_to_docx(markdown, str(output_path))

    assert output_path.exists()
    assert output_path.suffix == ".docx"
    assert result == str(output_path)


def test_export_handles_empty_manuscript(tmp_path: Path) -> None:
    output_path = tmp_path / "empty.docx"

    export_manuscript_to_docx("", str(output_path))

    assert output_path.exists()


def test_export_returns_output_path(tmp_path: Path) -> None:
    markdown = "## References\n\n- Example, A. (2024). Example title."
    output_path = tmp_path / "return-path.docx"

    result = export_manuscript_to_docx(markdown, str(output_path))

    assert result == str(output_path)
