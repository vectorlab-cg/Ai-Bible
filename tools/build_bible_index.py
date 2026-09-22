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


def words(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD.finditer(text)]


def parse_chapter(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    chapter_title = path.stem
    section_title = chapter_title
    body: list[str] = []
    blocks: list[dict[str, Any]] = []
    pending_blank = False

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
                "status": "draft",
                "word_count": len(tokens),
                "text": text,
                "terms": sorted(set(tokens)),
            }
        )

    for line in lines:
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
        if line.startswith("## Fonti"):
            flush()
            break
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


def build_index(bible_dir: Path) -> dict[str, Any]:
    blocks: list[dict[str, Any]] = []
    for path in sorted(bible_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        blocks.extend(parse_chapter(path))
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
    args = parser.parse_args()
    index = build_index(args.bible_dir)
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(index, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {len(index['documents'])} knowledge blocks")


if __name__ == "__main__":
    main()
