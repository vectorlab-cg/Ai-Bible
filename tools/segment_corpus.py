"""Create timestamped working segments from SRT and TXT source material."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).parent))

from inspect_corpus import build_record, parse_srt, parse_txt

SENTENCE_END = re.compile(r"[.!?][\"')\]]*$")
TARGET_WORDS = 550
MAX_WORDS = 750


def iter_source_records(source_dir: Path) -> Iterable[tuple[Path, dict[str, Any], list[dict[str, Any]]]]:
    for path in sorted(source_dir.iterdir()):
        if not path.is_file() or path.suffix.lower() not in {".srt", ".txt"}:
            continue
        record = build_record(path)
        if path.suffix.lower() == ".srt":
            cues, _ = parse_srt(path)
        else:
            cues, _ = parse_txt(path)
        yield path, record, cues


def split_large_cues(cues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expanded: list[dict[str, Any]] = []
    for cue in cues:
        words = cue["text"].split()
        if len(words) <= MAX_WORDS:
            expanded.append(cue)
            continue
        for start in range(0, len(words), MAX_WORDS):
            part = dict(cue)
            part["text"] = " ".join(words[start : start + MAX_WORDS])
            if start:
                part["start_time"] = None
                part["start_seconds"] = None
            if start + MAX_WORDS < len(words):
                part["end_time"] = None
                part["end_seconds"] = None
            expanded.append(part)
    return expanded


def make_segments(record: dict[str, Any], cues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_words = 0

    def flush() -> None:
        nonlocal current, current_words
        if not current:
            return
        first = current[0]
        last = current[-1]
        segments.append(
            {
                "segment_id": f"{record['source_id']}-{len(segments) + 1:04d}",
                "source_id": record["source_id"],
                "title": record["title"],
                "category": record["category"],
                "start_time": first.get("start_time"),
                "end_time": last.get("end_time"),
                "start_seconds": first.get("start_seconds"),
                "end_seconds": last.get("end_seconds"),
                "word_count": current_words,
                "text": " ".join(cue["text"] for cue in current),
            }
        )
        current = []
        current_words = 0

    for cue in split_large_cues(cues):
        word_count = len(cue["text"].split())
        if current and current_words + word_count > MAX_WORDS:
            flush()
        current.append(cue)
        current_words += word_count
        should_flush = current_words >= TARGET_WORDS and SENTENCE_END.search(cue["text"])
        if current_words >= MAX_WORDS or should_flush:
            flush()
    flush()
    return segments


def write_segments(source_dir: Path, output_file: Path) -> int:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    segment_count = 0
    with output_file.open("w", encoding="utf-8") as handle:
        for _, record, cues in iter_source_records(source_dir):
            for segment in make_segments(record, cues):
                handle.write(json.dumps(segment, ensure_ascii=True) + "\n")
                segment_count += 1
    return segment_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()
    count = write_segments(args.source_dir, args.output_file)
    print(f"Created {count} working segments: {args.output_file}")


if __name__ == "__main__":
    main()
