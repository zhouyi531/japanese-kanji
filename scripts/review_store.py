#!/usr/bin/env python3
"""Inspect and edit the persisted mistake notebook without a browser.

    python3 scripts/review_store.py list
    python3 scripts/review_store.py remove <id>
    python3 scripts/review_store.py clear

The store path defaults to data/mistakes.json and can be overridden with
--state. The running server reads the file per request, so edits made
here show up in the UI on the next load.
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import server  # noqa: E402  (path set above)


def render(items):
    if not items:
        print("(復習ノートは空です)")
        return
    print(f"{len(items)} item(s):")
    for item in items:
        kind = "漢字" if item["type"] == "kanji" else "単語"
        print(f"  {item['id']}")
        print(f"    {item['text']}【{item['reading']}】 {kind} · {item['wrongCount']}回 · {item['lastWrongAt']}")


def main():
    parser = argparse.ArgumentParser(description="Edit the persisted mistake notebook.")
    parser.add_argument("--state", default=server.DEFAULT_STATE)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="show every stored item")
    remove = sub.add_parser("remove", help="delete one item by id")
    remove.add_argument("id")
    sub.add_parser("clear", help="delete every item")
    args = parser.parse_args()

    server._STATE_PATH = os.path.abspath(args.state)

    if args.command == "list":
        render(server.read_items())
        return 0

    if args.command == "clear":
        server.write_items([])
        print("cleared")
        return 0

    items = server.read_items()
    remaining = [item for item in items if item["id"] != args.id]
    if len(remaining) == len(items):
        print(f"no item with id: {args.id}", file=sys.stderr)
        return 1
    server.write_items(remaining)
    print(f"removed: {args.id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
