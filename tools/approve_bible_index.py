"""Promote Bible blocks after editorial approval."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index_file", type=Path)
    parser.add_argument("output_file", type=Path)
    parser.add_argument("--approver", required=True)
    args = parser.parse_args()

    index = json.loads(args.index_file.read_text(encoding="utf-8"))
    for block in index["documents"]:
        block["status"] = "approved"
        block["approved_by"] = args.approver
        block["approved_on"] = date.today().isoformat()
    index["approval"] = {
        "status": "approved",
        "approver": args.approver,
        "approved_on": date.today().isoformat(),
        "note": "Editorial content approved; candidate timestamp spans still require source-level verification.",
    }
    args.output_file.write_text(json.dumps(index, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Approved {len(index['documents'])} knowledge blocks by {args.approver}")


if __name__ == "__main__":
    main()
