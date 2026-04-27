from __future__ import annotations

from unittest.mock import patch

from src.pubmed_client import build_pubmed_references, fetch_pubmed_details, search_pubmed


def test_search_pubmed_parses_esearch_ids() -> None:
    esearch_xml = """
    <eSearchResult>
      <IdList>
        <Id>40101010</Id>
        <Id>40101011</Id>
      </IdList>
    </eSearchResult>
    """

    with patch("src.pubmed_client._http_get", return_value=esearch_xml):
        result = search_pubmed("heart failure", max_results=2)

    assert result == ["40101010", "40101011"]


def test_fetch_pubmed_details_parses_metadata() -> None:
    efetch_xml = """
    <PubmedArticleSet>
      <PubmedArticle>
        <MedlineCitation>
          <Article>
            <ArticleTitle>Clinical effects of SGLT2 inhibition</ArticleTitle>
            <Abstract>
              <AbstractText>First abstract sentence.</AbstractText>
              <AbstractText>Second abstract sentence.</AbstractText>
            </Abstract>
            <Journal>
              <Title>Journal of Cardio-Metabolic Medicine</Title>
              <JournalIssue>
                <PubDate>
                  <Year>2024</Year>
                </PubDate>
              </JournalIssue>
            </Journal>
            <AuthorList>
              <Author>
                <LastName>Smith</LastName>
                <ForeName>Jane</ForeName>
              </Author>
              <Author>
                <CollectiveName>Heart Study Group</CollectiveName>
              </Author>
            </AuthorList>
          </Article>
        </MedlineCitation>
        <PubmedData>
          <ArticleIdList>
            <ArticleId IdType="pubmed">40101010</ArticleId>
            <ArticleId IdType="doi">10.1000/example-doi</ArticleId>
          </ArticleIdList>
        </PubmedData>
      </PubmedArticle>
    </PubmedArticleSet>
    """

    with patch("src.pubmed_client._http_get", return_value=efetch_xml):
        details = fetch_pubmed_details(["40101010"])

    assert len(details) == 1
    assert details[0]["pmid"] == "40101010"
    assert details[0]["title"] == "Clinical effects of SGLT2 inhibition"
    assert details[0]["abstract"] == "First abstract sentence. Second abstract sentence."
    assert details[0]["journal"] == "Journal of Cardio-Metabolic Medicine"
    assert details[0]["year"] == "2024"
    assert details[0]["doi"] == "10.1000/example-doi"
    assert details[0]["authors"] == ["Smith, Jane", "Heart Study Group"]


def test_build_pubmed_references_graceful_failure() -> None:
    with patch("src.pubmed_client._http_get", side_effect=OSError("network down")):
        references = build_pubmed_references("heart failure", max_results=3)

    assert references == []
