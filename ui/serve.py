#!/usr/bin/env python3
"""Serve the quick-try page and proxy /api/* to japanese-kanji."""
import os
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UI_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 19473
TARGET = "http://127.0.0.1:" + (sys.argv[2] if len(sys.argv) > 2 else "18473")
HERE = os.path.dirname(os.path.abspath(__file__))
HOP = {"host", "content-length", "connection", "accept-encoding"}


class Handler(BaseHTTPRequestHandler):
    def _proxy(self):
        path = self.path[len("/api"):] or "/"
        body = self.rfile.read(int(self.headers["Content-Length"])) if self.headers.get("Content-Length") else None
        req = urllib.request.Request(TARGET + path, data=body, method=self.command)
        for key, value in self.headers.items():
            if key.lower() not in HOP:
                req.add_header(key, value)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                self.send_response(response.status)
                self.send_header("Content-Type", response.headers.get("Content-Type", "application/octet-stream"))
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as error:
            self.send_response(error.code)
            self.end_headers()
            self.wfile.write(error.read())
        except Exception as error:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(("proxy error: %s" % error).encode())

    def _static(self):
        path = os.path.join(HERE, "index.html")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        with open(path, "rb") as source:
            self.wfile.write(source.read())

    def _route(self):
        self._proxy() if self.path == "/api" or self.path.startswith("/api/") else self._static()

    do_GET = _route
    do_POST = _route
    do_PUT = _route
    do_DELETE = _route

    def log_message(self, *_args):
        pass


if __name__ == "__main__":
    print(f"quick-try UI on http://127.0.0.1:{UI_PORT} -> {TARGET}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", UI_PORT), Handler).serve_forever()
