"""Run a sample PubMed query and print structured JSON results."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pubmed_client import build_pubmed_references


PUBMED_QUERY = "SGLT2 inhibitors heart failure type 2 diabetes"


def main() -> None:
    try:
        references = build_pubmed_references(PUBMED_QUERY, max_results=5)
    except Exception as exc:  # Defensive fallback for unexpected runtime errors.
        print(f"PubMed lookup error: {exc}")
        return

    if not references:
        print("PubMed lookup failed or returned no records. Please try again later.")
        return

    print(json.dumps(references, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
