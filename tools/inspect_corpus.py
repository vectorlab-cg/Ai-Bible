"""Build a metadata inventory for SRT and TXT source material."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

SRT_TIMESTAMP = re.compile(
    r"^(?P<start>\d{2}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+(?P<end>\d{2}:\d{2}:\d{2}[,.]\d{3})"
)
TAG_PATTERN = re.compile(r"<[^>]+>")
SPACE_PATTERN = re.compile(r"\s+")

CATEGORY_KEYWORDS = {
    "foundations": ("concepts", "myths", "fine-tuning", "model collapse", "large database models"),
    "architecture": ("rag", "context engineering", "agentic harness", "business rules", "super agents", "chunkless"),
    "engineering": ("code", "developer", "skills", "mlflow", "gpu", "llama.cpp", "vllm", "productivity"),
    "governance-security": ("security", "risk", "sovereignty", "breach", "owasp", "manage your ai", "secure"),
    "news": ("anthropic", "openai", "ibm", "stripe", "reddit", "thinking machines", "pacing", "glimmer", "glm-5.2"),
}


def timestamp_to_seconds(value: str) -> float:
    hours, minutes, seconds = value.replace(",", ".").split(":")
    whole_seconds, milliseconds = seconds.split(".")
    return int(hours) * 3600 + int(minutes) * 60 + int(whole_seconds) + int(milliseconds) / 1000


def normalize_text(lines: list[str]) -> str:
    text = " ".join(lines)
    text = TAG_PATTERN.sub("", text)
    text = SPACE_PATTERN.sub(" ", text)
    return text.strip()


def parse_srt(path: Path) -> tuple[list[dict[str, Any]], str]:
    raw = path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\r?\n\s*\r?\n", raw.strip())
    cues: list[dict[str, Any]] = []

    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3:
            continue
        match = SRT_TIMESTAMP.match(lines[1].strip())
        if not match:
            continue
        text = normalize_text(lines[2:])
        if not text:
            continue
        cues.append(
            {
                "start_time": match.group("start").replace(".", ","),
                "end_time": match.group("end").replace(".", ","),
                "start_seconds": timestamp_to_seconds(match.group("start")),
                "end_seconds": timestamp_to_seconds(match.group("end")),
                "text": text,
            }
        )

    return cues, normalize_text([cue["text"] for cue in cues])


def parse_txt(path: Path) -> tuple[list[dict[str, Any]], str]:
    text = normalize_text(path.read_text(encoding="utf-8-sig").splitlines())
    return ([{"text": text}] if text else []), text


def display_title(path: Path) -> str:
    title = path.stem
    title = re.sub(r"^\[English(?: \(auto-generated\))?\]\s*", "", title)
    title = re.sub(r"\s*\[DownSub\.com\]", "", title)
    title = re.sub(r"\s*\(1\)$", "", title)
    return title.strip()


def classify(title: str) -> str:
    lowered = title.lower()
    scores = {
        category: sum(keyword in lowered for keyword in keywords)
        for category, keywords in CATEGORY_KEYWORDS.items()
    }
    category, score = max(scores.items(), key=lambda item: item[1])
    return category if score else "unclassified"


def build_record(path: Path) -> dict[str, Any]:
    file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if path.suffix.lower() == ".srt":
        cues, text = parse_srt(path)
    elif path.suffix.lower() == ".txt":
        cues, text = parse_txt(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    duration = None
    if cues and "end_seconds" in cues[-1]:
        duration = cues[-1]["end_seconds"]

    return {
        "source_id": file_hash[:16],
        "filename": path.name,
        "title": display_title(path),
        "format": path.suffix.lower().lstrip("."),
        "category": classify(display_title(path)),
        "sha256": file_hash,
        "duplicate_key": file_hash,
        "cue_count": len(cues),
        "word_count": len(text.split()),
        "duration_seconds": duration,
    }


def build_inventory(source_dir: Path) -> dict[str, Any]:
    paths = sorted(
        path for path in source_dir.iterdir() if path.is_file() and path.suffix.lower() in {".srt", ".txt"}
    )
    records = [build_record(path) for path in paths]
    duplicate_groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        duplicate_groups[record["duplicate_key"]].append(record["filename"])

    duplicates = [files for files in duplicate_groups.values() if len(files) > 1]
    return {
        "schema_version": 1,
        "source_directory": source_dir.name,
        "file_count": len(records),
        "format_counts": {
            extension: sum(record["format"] == extension for record in records)
            for extension in ("srt", "txt")
        },
        "duplicate_groups": duplicates,
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()

    inventory = build_inventory(args.source_dir)
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(
        json.dumps(inventory, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Indexed {inventory['file_count']} files; "
        f"duplicates: {len(inventory['duplicate_groups'])}; "
        f"output: {args.output_file}"
    )


if __name__ == "__main__":
    main()
