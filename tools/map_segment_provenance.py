"""Attach candidate timestamp spans to Bible blocks using source-scoped lexical overlap."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

WORD = re.compile(r"[\w'-]+", re.UNICODE)
STOPWORDS = {
    "about", "after", "also", "been", "being", "from", "have", "into", "more", "only",
    "that", "their", "there", "these", "they", "this", "with", "your", "are", "and", "the",
    "per", "con", "che", "dei", "del", "della", "delle", "gli", "una", "uno", "sono", "come",
    "quando", "dopo", "prima", "ogni", "deve", "essere", "sua", "suo", "non", "una", "un",
}


def terms(text: str) -> set[str]:
    return {
        match.group(0).lower()
        for match in WORD.finditer(text)
        if len(match.group(0)) > 2 and match.group(0).lower() not in STOPWORDS
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def map_blocks(index: dict[str, Any], segments: list[dict[str, Any]], limit: int) -> dict[str, Any]:
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for segment in segments:
        by_source[segment["source_id"]].append(segment)

    mapped = 0
    candidate_count = 0
    for block in index["documents"]:
        block_terms = terms(block["text"])
        source_ids = {reference["source_id"] for reference in block.get("source_references", [])}
        candidates: list[tuple[float, dict[str, Any]]] = []
        for source_id in source_ids:
            for segment in by_source.get(source_id, []):
                segment_terms = terms(segment["text"])
                if not block_terms or not segment_terms:
                    continue
                overlap = len(block_terms & segment_terms)
                score = overlap / max(1, len(block_terms))
                if overlap:
                    candidates.append((score, segment))
        candidates.sort(key=lambda item: (-item[0], item[1]["segment_id"]))
        selected = []
        for score, segment in candidates[:limit]:
            selected.append(
                {
                    "segment_id": segment["segment_id"],
                    "source_id": segment["source_id"],
                    "start_time": segment.get("start_time"),
                    "end_time": segment.get("end_time"),
                    "score": round(score, 4),
                    "status": "candidate",
                }
            )
        block["source_spans"] = selected
        block["provenance_status"] = "candidate-timestamps" if selected else block.get("provenance_status", "unmatched")
        if selected:
            mapped += 1
            candidate_count += len(selected)

    index["provenance"] = {
        "method": "source-scoped lexical overlap",
        "status": "candidate",
        "note": "Candidate spans require manual review before publication as precise citations.",
        "mapped_block_count": mapped,
        "candidate_span_count": candidate_count,
    }
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index_file", type=Path)
    parser.add_argument("segments_file", type=Path)
    parser.add_argument("output_file", type=Path)
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    index = json.loads(args.index_file.read_text(encoding="utf-8"))
    result = map_blocks(index, load_jsonl(args.segments_file), args.limit)
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(result, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(
        f"Mapped {result['provenance']['mapped_block_count']} blocks to "
        f"{result['provenance']['candidate_span_count']} candidate spans"
    )


if __name__ == "__main__":
    main()
