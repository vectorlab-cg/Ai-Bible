"""Export candidate source spans into a compact citation review queue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index_file", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()

    index = json.loads(args.index_file.read_text(encoding="utf-8"))
    queue = []
    for block in index["documents"]:
        for span in block.get("source_spans", []):
            queue.append(
                {
                    "block_id": block["id"],
                    "chapter_id": block["chapter_id"],
                    "section_title": block["section_title"],
                    "block_text": block["text"],
                    "source_id": span["source_id"],
                    "segment_id": span["segment_id"],
                    "start_time": span["start_time"],
                    "end_time": span["end_time"],
                    "score": span["score"],
                    "review_status": "candidate",
                    "review_note": "Confirm that the source span supports the complete block claim.",
                }
            )
    result = {
        "schema_version": 1,
        "status": "candidate",
        "count": len(queue),
        "items": queue,
    }
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(result, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(queue)} citation candidates")


if __name__ == "__main__":
    main()
