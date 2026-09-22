"""Build a small lexical index from approved or draft Bible Markdown chapters."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

HEADING = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
WORD = re.compile(r"[\w'-]+", re.UNICODE)
SOURCE_ITEM = re.compile(r"^\s*[-*]\s+`(.+?)`\s*$")


def words(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD.finditer(text)]


def normalize_title(text: str) -> set[str]:
    return set(words(text))


def source_references(path: Path, inventory: dict[str, Any] | None) -> list[dict[str, str]]:
    if inventory is None:
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    source_titles: list[str] = []
    in_sources = False
    for line in lines:
        if line.startswith("## Fonti"):
            in_sources = True
            continue
        if in_sources:
            match = SOURCE_ITEM.match(line)
            if match:
                source_titles.append(match.group(1))
    references: list[dict[str, str]] = []
    records = inventory.get("records", [])
    for title in source_titles:
        title_words = normalize_title(title)
        matches = [
            record for record in records
            if title_words and title_words <= normalize_title(record["title"])
        ]
        if len(matches) == 1:
            record = matches[0]
            references.append({"source_id": record["source_id"], "title": record["title"]})
    return references


def parse_chapter(path: Path, inventory: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    chapter_title = path.stem
    section_title = chapter_title
    body: list[str] = []
    blocks: list[dict[str, Any]] = []
    pending_blank = False
    references = source_references(path, inventory)

    def flush() -> None:
        nonlocal body
        text = " ".join(line.strip() for line in body if line.strip())
        body = []
        if not text:
            return
        tokens = words(text)
        block_id = hashlib.sha1(f"{path.name}:{len(blocks)}:{text}".encode("utf-8")).hexdigest()[:12]
        blocks.append(
            {
                "id": f"kb-{block_id}",
                "chapter_id": path.stem,
                "chapter_title": chapter_title,
                "section_title": section_title,
                "source_file": path.name,
                "source_references": references,
                "provenance_status": "title-level",
                "status": "draft",
                "word_count": len(tokens),
                "text": text,
                "terms": sorted(set(tokens)),
            }
        )

    for line in lines:
        if line.startswith("## Fonti"):
            flush()
            break
        match = HEADING.match(line)
        if match:
            flush()
            pending_blank = False
            title = match.group(2)
            if len(match.group(1)) <= 2:
                section_title = title
            if len(match.group(1)) == 1:
                chapter_title = title
            continue
        if not line.strip():
            pending_blank = True
        else:
            is_list_item = bool(re.match(r"^\s*(?:[-*]|\d+\.)\s+", line))
            previous_is_list_item = bool(body and re.match(r"^\s*(?:[-*]|\d+\.)\s+", body[-1]))
            if pending_blank and body and not (is_list_item and previous_is_list_item):
                flush()
            body.append(line)
            pending_blank = False
    flush()
    return blocks


def build_index(bible_dir: Path, inventory_file: Path | None = None) -> dict[str, Any]:
    inventory = json.loads(inventory_file.read_text(encoding="utf-8")) if inventory_file else None
    blocks: list[dict[str, Any]] = []
    for path in sorted(bible_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        blocks.extend(parse_chapter(path, inventory))
    return {
        "schema_version": 1,
        "index_type": "lexical",
        "source": str(bible_dir.name),
        "documents": blocks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bible_dir", type=Path)
    parser.add_argument("output_file", type=Path)
    parser.add_argument("--inventory", type=Path)
    args = parser.parse_args()
    index = build_index(args.bible_dir, args.inventory)
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(index, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {len(index['documents'])} knowledge blocks")


if __name__ == "__main__":
    main()
