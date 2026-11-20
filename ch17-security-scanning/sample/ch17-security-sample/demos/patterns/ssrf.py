"""Fetching a user-supplied URL reaches services that should be private."""

import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import requests

PROJECT = next(p / "bookfinder" for p in Path(__file__).resolve().parents
               if (p / "bookfinder").is_dir())
sys.path.insert(0, str(PROJECT / "src"))
from bookfinder.covers import BlockedURLError, check_url  # noqa: E402


class Internal(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"internal admin: db_password=example")

    def log_message(self, *args):
        pass


server = HTTPServer(("127.0.0.1", 0), Internal)
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{server.server_port}/admin"

print("naive fetch ->", requests.get(url, timeout=5).text)
for target in (url, "https://169.254.169.254/latest/meta-data/"):
    try:
        check_url(target)
    except BlockedURLError as error:
        print("check_url   ->", error)
server.shutdown()
