"""Search the local lexical Bible index."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

WORD = re.compile(r"[\w'-]+", re.UNICODE)


def tokenize(text: str) -> set[str]:
    return {match.group(0).lower() for match in WORD.finditer(text)}


def search(index: dict[str, Any], query: str, limit: int) -> list[dict[str, Any]]:
    query_terms = tokenize(query)
    scored: list[tuple[int, dict[str, Any]]] = []
    for document in index["documents"]:
        title_terms = tokenize(f"{document['chapter_title']} {document['section_title']}")
        text_terms = set(document["terms"])
        score = len(query_terms & text_terms) + 2 * len(query_terms & title_terms)
        if score:
            scored.append((score, document))
    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [{"score": score, **document} for score, document in scored[:limit]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index_file", type=Path)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    index = json.loads(args.index_file.read_text(encoding="utf-8"))
    results = search(index, args.query, args.limit)
    for result in results:
        print(f"[{result['score']}] {result['chapter_title']} / {result['section_title']}")
        print(result["text"])
        print(f"Fonte: {result['source_file']}\n")
    if not results:
        print("Nessun risultato nella Bibbia locale.")


if __name__ == "__main__":
    main()
