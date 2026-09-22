"""Report working segments that have no candidate concept."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("segments_file", type=Path)
    parser.add_argument("candidates_file", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()

    segment_rows = [
        json.loads(line)
        for line in args.segments_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    candidate_rows = [
        json.loads(line)
        for line in args.candidates_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    segments = {row["segment_id"]: row for row in segment_rows}
    candidates = {row["segment_id"]: row for row in candidate_rows}
    unmapped = []
    for segment_id, segment in segments.items():
        is_outro = segment["text"].strip().lower() in {"thank you for watching the video.", "thank you for watching."}
        if candidates.get(segment_id, {}).get("concept_candidates") and not is_outro:
            continue
        unmapped.append(
            {
                "segment_id": segment_id,
                "source_id": segment["source_id"],
                "title": segment["title"],
                "category": segment["category"],
                "start_time": segment.get("start_time"),
                "end_time": segment.get("end_time"),
                "text": segment["text"],
                "review_status": "editorial-exclusion" if is_outro else "needs-manual-classification",
            }
        )

    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(unmapped, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Reported {len(unmapped)} unmapped segments")


if __name__ == "__main__":
    main()
