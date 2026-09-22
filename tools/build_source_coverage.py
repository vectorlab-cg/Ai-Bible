"""Build a source-to-concept coverage matrix from corpus metadata and working candidates."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_coverage(inventory: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidates:
        by_source[row["source_id"]].append(row)

    records: list[dict[str, Any]] = []
    for source in inventory["records"]:
        source_segments = by_source.get(source["source_id"], [])
        concept_counts = Counter(
            match["concept_id"]
            for segment in source_segments
            for match in segment.get("concept_candidates", [])
        )
        records.append(
            {
                "source_id": source["source_id"],
                "filename": source["filename"],
                "title": source["title"],
                "category": source["category"],
                "format": source["format"],
                "sha256": source["sha256"],
                "segment_count": len(source_segments),
                "mapped_segment_count": sum(bool(row.get("concept_candidates")) for row in source_segments),
                "concepts": [
                    {"concept_id": concept_id, "segment_count": count}
                    for concept_id, count in sorted(concept_counts.items(), key=lambda item: (-item[1], item[0]))
                ],
                "coverage_status": "mapped" if source_segments else "unmapped",
            }
        )

    return {
        "schema_version": 1,
        "source_count": len(records),
        "mapped_source_count": sum(record["coverage_status"] == "mapped" for record in records),
        "unmapped_source_count": sum(record["coverage_status"] == "unmapped" for record in records),
        "segment_count": len(candidates),
        "mapped_segment_count": sum(bool(row.get("concept_candidates")) for row in candidates),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory_file", type=Path)
    parser.add_argument("candidates_file", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()

    coverage = build_coverage(load_json(args.inventory_file), load_jsonl(args.candidates_file))
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(coverage, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(
        f"Covered {coverage['mapped_source_count']}/{coverage['source_count']} sources; "
        f"mapped segments: {coverage['mapped_segment_count']}/{coverage['segment_count']}"
    )


if __name__ == "__main__":
    main()
