#!/usr/bin/env python3
"""End-to-end tests for the persistent mistake-review API.

    python3 scripts/test_review_api.py

Starts the real server as a subprocess against a temporary store, exercises
every endpoint, restarts the process and checks the notebook is still there.
"""
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER = os.path.join(ROOT, "server.py")
PASSED = []


def check(name, condition, detail=""):
    if condition:
        PASSED.append(name)
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name} {detail}")
        raise SystemExit(1)


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def call(port, method, path, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}", data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8")


def start(port, state):
    process = subprocess.Popen(
        [sys.executable, SERVER, "--bind", "127.0.0.1", "--port", str(port), "--state", state],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    for _ in range(60):
        try:
            status, _ = call(port, "GET", "/health.json")
            if status == 200:
                return process
        except OSError:
            pass
        if process.poll() is not None:
            raise SystemExit(f"server exited early:\n{process.stdout.read()}")
        time.sleep(0.1)
    raise SystemExit("server did not become healthy")


def stop(process):
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        state = os.path.join(tmp, "mistakes.json")
        port = free_port()
        process = start(port, state)
        try:
            status, body = call(port, "GET", "/")
            check("static index served", status == 200 and "漢字の庭" in body)

            status, body = call(port, "GET", "/api/mistakes")
            check("empty store returns []", status == 200 and json.loads(body) == [])

            first = {"id": "word:一つ:ひとつ", "type": "word", "text": "一つ",
                     "reading": "ひとつ", "accepted": ["ひとつ"], "wrongCount": 1,
                     "lastWrongAt": "2026-09-10T10:00:00+08:00", "reason": "wrong"}
            second = {"id": "kanji:山:やま", "type": "kanji", "text": "山",
                      "reading": "やま", "accepted": ["やま", "さん"], "wrongCount": 2,
                      "lastWrongAt": "2026-09-10T11:00:00+08:00", "reason": "timeout"}
            status, body = call(port, "PUT", "/api/mistakes", {"items": [first, second]})
            check("PUT replaces list", status == 200 and len(json.loads(body)) == 2)

            status, body = call(port, "POST", "/api/mistakes", {"item": first})
            stored = json.loads(body)
            check("POST upserts and bumps wrongCount",
                  status == 200 and len(stored) == 2 and stored[0]["wrongCount"] == 2,
                  detail=body)

            status, body = call(port, "POST", "/api/mistakes",
                                {"id": "kanji:川:かわ", "type": "kanji", "text": "川",
                                 "reading": "かわ", "accepted": ["かわ"]})
            check("POST adds a new item", status == 200 and len(json.loads(body)) == 3)

            status, body = call(port, "PUT", "/api/mistakes", {"items": "nope"})
            check("invalid payload rejected", status == 400)

            status, body = call(port, "DELETE", "/api/mistakes/word%3A%E4%B8%80%E3%81%A4%3A%E3%81%B2%E3%81%A8%E3%81%A4")
            check("DELETE one item by id",
                  status == 200 and len(json.loads(body)) == 2
                  and all(x["id"] != first["id"] for x in json.loads(body)))

            with open(state, encoding="utf-8") as handle:
                on_disk = json.load(handle)
            check("state flushed to disk", len(on_disk["items"]) == 2)
        finally:
            stop(process)

        # Restart: persistence is the whole point.
        process = start(port, state)
        try:
            status, body = call(port, "GET", "/api/mistakes")
            check("store survives restart", status == 200 and len(json.loads(body)) == 2, detail=body)

            status, body = call(port, "DELETE", "/api/mistakes")
            check("DELETE all clears", status == 200 and json.loads(body) == [])
            status, body = call(port, "GET", "/api/mistakes")
            check("clear persisted", status == 200 and json.loads(body) == [])
            status, body = call(port, "GET", "/api/nope")
            check("unknown api path is 404", status == 404)
        finally:
            stop(process)

    print(f"\n{len(PASSED)} checks passed")


if __name__ == "__main__":
    main()
