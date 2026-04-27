"""Lightweight PubMed client using NCBI E-utilities."""

from __future__ import annotations

from typing import Any
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
REQUEST_TIMEOUT_SECONDS = 15


def _http_get(url: str, params: dict[str, Any]) -> str:
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    with urllib.request.urlopen(full_url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return response.read().decode("utf-8")


def search_pubmed(query: str, max_results: int = 5) -> list[str]:
    """Search PubMed via ESearch and return PubMed IDs."""

    if not isinstance(query, str) or not query.strip():
        return []

    result_count = max(1, int(max_results))

    try:
        xml_text = _http_get(
            ESEARCH_URL,
            {
                "db": "pubmed",
                "term": query.strip(),
                "retmax": result_count,
                "retmode": "xml",
            },
        )
        root = ET.fromstring(xml_text)
    except (OSError, ET.ParseError, ValueError, TypeError):
        return []

    return [
        (element.text or "").strip()
        for element in root.findall("./IdList/Id")
        if (element.text or "").strip()
    ]


def _extract_abstract(article_node: ET.Element) -> str:
    abstract_text_nodes = article_node.findall(".//Abstract/AbstractText")
    parts = [" ".join(node.itertext()).strip() for node in abstract_text_nodes]
    return " ".join(part for part in parts if part)


def _extract_authors(article_node: ET.Element) -> list[str]:
    authors: list[str] = []

    for author_node in article_node.findall(".//AuthorList/Author"):
        collective_name = author_node.findtext("CollectiveName", default="").strip()
        if collective_name:
            authors.append(collective_name)
            continue

        last_name = author_node.findtext("LastName", default="").strip()
        fore_name = author_node.findtext("ForeName", default="").strip()

        if last_name and fore_name:
            authors.append(f"{last_name}, {fore_name}")
        elif last_name:
            authors.append(last_name)
        elif fore_name:
            authors.append(fore_name)

    return authors


def _extract_doi(article_node: ET.Element) -> str:
    for article_id in article_node.findall(".//PubmedData/ArticleIdList/ArticleId"):
        if article_id.attrib.get("IdType") == "doi":
            return (article_id.text or "").strip()
    return ""


def fetch_pubmed_details(pmids: list[str]) -> list[dict[str, Any]]:
    """Fetch article metadata from PubMed via EFetch for a PMID list."""

    if not pmids:
        return []

    clean_pmids = [pmid.strip() for pmid in pmids if isinstance(pmid, str) and pmid.strip()]
    if not clean_pmids:
        return []

    try:
        xml_text = _http_get(
            EFETCH_URL,
            {
                "db": "pubmed",
                "id": ",".join(clean_pmids),
                "retmode": "xml",
            },
        )
        root = ET.fromstring(xml_text)
    except (OSError, ET.ParseError):
        return []

    articles: list[dict[str, Any]] = []

    for article_node in root.findall("./PubmedArticle"):
        citation_node = article_node.find("PubmedData/ArticleIdList/ArticleId[@IdType='pubmed']")
        pmid = (citation_node.text or "").strip() if citation_node is not None else ""

        title = " ".join(
            article_node.findtext(".//ArticleTitle", default="").split()
        )
        journal = article_node.findtext(".//Journal/Title", default="").strip()
        year = article_node.findtext(".//PubDate/Year", default="").strip()
        if not year:
            year = article_node.findtext(".//PubDate/MedlineDate", default="").strip()

        article_data: dict[str, Any] = {
            "pmid": pmid,
            "title": title,
            "abstract": _extract_abstract(article_node),
            "journal": journal,
            "year": year,
        }

        doi = _extract_doi(article_node)
        if doi:
            article_data["doi"] = doi

        authors = _extract_authors(article_node)
        if authors:
            article_data["authors"] = authors

        articles.append(article_data)

    return articles


def build_pubmed_references(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Search and fetch PubMed references in one step."""

    pmids = search_pubmed(query=query, max_results=max_results)
    if not pmids:
        return []

    return fetch_pubmed_details(pmids)
