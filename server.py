#!/usr/bin/env python3
"""漢字の庭 static server with a persistent mistake-review API.

Python standard library only. Serves the site exactly like `http.server`
does, and adds a small JSON store so the review notebook survives
restarts and is shared by every browser that hits this origin.

API
---
GET    /api/mistakes                -> [item, ...]
PUT    /api/mistakes   {items:[...]} -> replaces the whole notebook
POST   /api/mistakes   {item:{...}}  -> upserts one item (wrongCount += 1)
DELETE /api/mistakes                 -> clears the notebook
DELETE /api/mistakes/<url-encoded id>-> removes one item
"""
import argparse
import datetime
import json
import os
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STATE = os.path.join(HERE, "data", "mistakes.json")
MAX_ITEMS = 5000
LOCK = threading.RLock()

_STATE_PATH = DEFAULT_STATE


# ---------------------------------------------------------------- storage

def read_items():
    with LOCK:
        try:
            with open(_STATE_PATH, encoding="utf-8") as handle:
                payload = json.load(handle)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return []
    if isinstance(payload, dict):
        payload = payload.get("items")
    return payload if isinstance(payload, list) else []


def write_items(items):
    """Atomic replace so a crash mid-write cannot corrupt the notebook."""
    with LOCK:
        os.makedirs(os.path.dirname(_STATE_PATH), exist_ok=True)
        tmp = _STATE_PATH + ".tmp"
        payload = {
            "version": 1,
            "updatedAt": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "items": items,
        }
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, _STATE_PATH)


def normalize(raw):
    """Keep only fields the notebook understands, so a bad client cannot
    stuff arbitrary data into the shared store."""
    if not isinstance(raw, dict):
        return None
    item_id = raw.get("id")
    text = raw.get("text")
    if not isinstance(item_id, str) or not item_id or not isinstance(text, str) or not text:
        return None
    accepted = raw.get("accepted")
    if not isinstance(accepted, list):
        accepted = []
    accepted = [str(x) for x in accepted if isinstance(x, (str, int, float))][:12]
    try:
        wrong_count = max(1, int(raw.get("wrongCount", 1)))
    except (TypeError, ValueError):
        wrong_count = 1
    return {
        "id": item_id[:200],
        "type": raw.get("type") if raw.get("type") in ("kanji", "word") else "word",
        "text": text[:64],
        "reading": str(raw.get("reading", ""))[:128],
        "accepted": accepted,
        "wrongCount": min(wrong_count, 100000),
        "lastWrongAt": str(raw.get("lastWrongAt", ""))[:40],
        "reason": str(raw.get("reason", ""))[:40],
    }


def normalize_list(raw):
    if isinstance(raw, dict):
        raw = raw.get("items")
    if not isinstance(raw, list):
        raise ValueError("expected a JSON array or {\"items\": [...]}")
    seen, cleaned = set(), []
    for entry in raw:
        item = normalize(entry)
        if item and item["id"] not in seen:
            seen.add(item["id"])
            cleaned.append(item)
    return cleaned[:MAX_ITEMS]


# ---------------------------------------------------------------- handler

class Handler(SimpleHTTPRequestHandler):
    server_version = "KanjiGarden/2.0"

    def _json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return None
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _api(self, method):
        path = self.path.split("?", 1)[0]
        if not path.startswith("/api/"):
            return False

        if path == "/api/mistakes":
            if method == "GET":
                self._json(read_items())
            elif method == "PUT":
                try:
                    items = normalize_list(self._read_body())
                except (ValueError, json.JSONDecodeError) as error:
                    self._json({"error": str(error)}, 400)
                    return True
                write_items(items)
                self._json(items)
            elif method == "POST":
                try:
                    payload = self._read_body()
                except (ValueError, json.JSONDecodeError) as error:
                    self._json({"error": str(error)}, 400)
                    return True
                raw = payload.get("item") if isinstance(payload, dict) and "item" in payload else payload
                incoming = normalize(raw)
                if not incoming:
                    self._json({"error": "invalid item"}, 400)
                    return True
                items = read_items()
                for existing in items:
                    if existing["id"] == incoming["id"]:
                        incoming["wrongCount"] = max(existing["wrongCount"], incoming["wrongCount"]) + 1
                        items.remove(existing)
                        break
                items.insert(0, incoming)
                items = items[:MAX_ITEMS]
                write_items(items)
                self._json(items)
            elif method == "DELETE":
                write_items([])
                self._json([])
            else:
                self._json({"error": "method not allowed"}, 405)
            return True

        if path.startswith("/api/mistakes/") and method == "DELETE":
            from urllib.parse import unquote
            target = unquote(path[len("/api/mistakes/"):])
            items = read_items()
            remaining = [item for item in items if item["id"] != target]
            write_items(remaining)
            self._json(remaining)
            return True

        self._json({"error": "not found"}, 404)
        return True

    def do_GET(self):
        if not self._api("GET"):
            super().do_GET()

    def do_HEAD(self):
        if not self._api("HEAD"):
            super().do_HEAD()

    def do_POST(self):
        if not self._api("POST"):
            self._json({"error": "method not allowed"}, 405)

    def do_PUT(self):
        if not self._api("PUT"):
            self._json({"error": "method not allowed"}, 405)

    def do_DELETE(self):
        if not self._api("DELETE"):
            self._json({"error": "method not allowed"}, 405)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)


def main():
    global _STATE_PATH
    parser = argparse.ArgumentParser(description="Serve 漢字の庭 with a persistent review API.")
    parser.add_argument("--bind", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=18473)
    parser.add_argument("--state", default=DEFAULT_STATE, help="path to the mistake store JSON")
    args = parser.parse_args()
    _STATE_PATH = os.path.abspath(args.state)

    handler = partial(Handler, directory=HERE)
    httpd = ThreadingHTTPServer((args.bind, args.port), handler)
    print(f"漢字の庭 on http://{args.bind}:{args.port}  (review store: {_STATE_PATH})", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
