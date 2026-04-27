"""Local Streamlit interface for the Ferrari Med Research pipeline."""

from __future__ import annotations

from pathlib import Path
import tempfile

import streamlit as st

from src.docx_exporter import export_manuscript_to_docx
from src.pipeline_runner import run_pipeline
from src.pubmed_client import build_pubmed_references


SECTION_ORDER = ("Abstract", "Introduction", "Discussion", "References")


def _build_sample_text(topic: str, references: list[dict]) -> str:
    """Create deterministic sectioned text for APA audit/scoring input."""

    abstract_bits: list[str] = []
    intro_bits: list[str] = []
    discussion_bits: list[str] = []

    for item in references:
        title = str(item.get("title") or "Untitled study").strip()
        abstract = str(item.get("abstract") or "").strip()
        if abstract:
            abstract_bits.append(abstract)
        intro_bits.append(f"This manuscript reviews evidence from {title}.")
        discussion_bits.append(f"The findings from {title} support ongoing investigation in {topic}.")

    abstract_text = " ".join(abstract_bits) or f"This manuscript evaluates current PubMed evidence on {topic}."
    introduction_text = " ".join(intro_bits) or f"This introduction frames the research context for {topic}."
    discussion_text = " ".join(discussion_bits) or f"Discussion highlights implications and research gaps for {topic}."

    return (
        "Abstract\n"
        f"{abstract_text}\n"
        "Introduction\n"
        f"{introduction_text}\n"
        "Discussion\n"
        f"{discussion_text}\n"
        "References\n"
        "Reference list generated from DOI-validated PubMed evidence."
    )


def _extract_section_text(manuscript: str, section_name: str) -> str:
    heading = f"## {section_name}"
    lines = manuscript.splitlines()

    try:
        start_index = lines.index(heading)
    except ValueError:
        return "Section not available in manuscript output."

    collected: list[str] = []
    for line in lines[start_index + 1 :]:
        if line.startswith("## "):
            break
        stripped = line.strip()
        if stripped:
            collected.append(stripped)

    return "\n".join(collected) if collected else "Section not available in manuscript output."


def _render_sections(manuscript: str) -> None:
    for section_name in SECTION_ORDER:
        with st.expander(section_name, expanded=(section_name == "Abstract")):
            st.markdown(_extract_section_text(manuscript, section_name))


def _run_pipeline(topic: str, document_type: str, academic_level: str, max_results: int) -> None:
    references = build_pubmed_references(query=topic, max_results=max_results)

    if not references:
        st.error("PubMed lookup failed or returned no results. Please adjust the topic and try again.")
        st.session_state.pipeline_result = None
        st.session_state.docx_path = None
        return

    intake_data = {
        "topic": topic,
        "document_type": document_type,
        "language": "English",
        "academic_level": academic_level,
        "source_mode": "pubmed",
        "title": f"{topic} - {document_type.title()} Manuscript",
        "body_text": "Generated from PubMed evidence.",
    }

    sample_text = _build_sample_text(topic=topic, references=references)
    result = run_pipeline(intake_data=intake_data, sample_text=sample_text, references=references)

    checked_references = result.get("references_checked", [])
    valid_reference_count = sum(1 for item in checked_references if item.get("is_valid_doi"))
    if valid_reference_count == 0:
        st.error("No DOI-validated references were found. Unable to build a full references section.")

    st.session_state.pipeline_result = result
    st.session_state.docx_path = None


def _prepare_docx_download() -> None:
    result = st.session_state.get("pipeline_result")
    if not result:
        st.warning("Run the research pipeline before exporting a DOCX file.")
        return

    manuscript = str(result.get("manuscript_draft") or "").strip()
    if not manuscript:
        st.warning("No manuscript output found to export.")
        return

    temp_dir = Path(tempfile.gettempdir())
    output_path = temp_dir / "ferrari_med_research_manuscript.docx"
    metadata = {
        "title": result.get("intake", {}).get("title", "Ferrari Med Research Manuscript"),
        "author": "Ferrari Med Research",
        "institution": "Local Streamlit App",
        "course": "N/A",
        "instructor": "N/A",
        "date": "Generated locally",
    }
    export_path = export_manuscript_to_docx(manuscript, str(output_path), metadata=metadata)
    st.session_state.docx_path = export_path


def main() -> None:
    st.set_page_config(page_title="Ferrari Med Research", layout="wide")
    st.title("Ferrari Med Research - Local Pipeline App")
    st.caption("Run a deterministic local research flow using PubMed evidence and export a DOCX draft.")

    with st.form("pipeline_form"):
        topic = st.text_input("Topic", value="SGLT2 inhibitors heart failure type 2 diabetes")
        document_type = st.selectbox("Document type", options=["review", "research", "essay"], index=0)
        academic_level = st.selectbox("Academic level", options=["undergraduate", "postgraduate"], index=0)
        max_results = st.slider("Number of PubMed results", min_value=1, max_value=10, value=5, step=1)
        run_clicked = st.form_submit_button("Run Research Pipeline")

    if run_clicked:
        if not topic.strip():
            st.error("Topic is required.")
        else:
            _run_pipeline(
                topic=topic.strip(),
                document_type=document_type,
                academic_level=academic_level,
                max_results=max_results,
            )

    if st.button("Download DOCX"):
        _prepare_docx_download()

    result = st.session_state.get("pipeline_result")
    if result:
        score_payload = result.get("score", {})
        total_score = score_payload.get("total_score", "N/A")
        classification = score_payload.get("classification", "N/A")

        st.subheader("Pipeline Results")
        col_a, col_b = st.columns(2)
        col_a.metric("Score", total_score)
        col_b.metric("Classification", classification)

        manuscript = str(result.get("manuscript_draft") or "")
        st.subheader("Manuscript Preview")
        _render_sections(manuscript)

    docx_path = st.session_state.get("docx_path")
    if docx_path:
        docx_file = Path(docx_path)
        if docx_file.exists():
            st.download_button(
                label="Download Generated DOCX",
                data=docx_file.read_bytes(),
                file_name="ferrari_med_research_manuscript.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )


if __name__ == "__main__":
    main()
