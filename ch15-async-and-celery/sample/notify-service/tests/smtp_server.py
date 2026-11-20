"""A small SMTP server for tests: it speaks enough SMTP for smtplib.

`fail_at` makes it answer one command with an error, so tests can check
how the sender reacts to a busy server (4xx) or a bad address (5xx).
"""

import socketserver
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import cast


@dataclass
class Mailbox:
    """What the server received, and how it should misbehave."""

    messages: list[bytes] = field(default_factory=list)
    fail_at: str | None = None  # "MAIL", "RCPT" or "DATA"
    fail_reply: bytes = b"421 4.7.0 Try again later"


class _Handler(socketserver.StreamRequestHandler):
    def reply(self, line: bytes) -> None:
        self.wfile.write(line + b"\r\n")

    def handle(self) -> None:
        box = cast("_Server", self.server).mailbox
        self.reply(b"220 test.local ESMTP")
        while line := self.rfile.readline():
            command = line[:4].upper().decode(errors="replace")
            if command == box.fail_at:
                self.reply(box.fail_reply)
            elif command in ("EHLO", "HELO"):
                self.reply(b"250 test.local")
            elif command in ("MAIL", "RCPT", "RSET", "NOOP"):
                self.reply(b"250 OK")
            elif command == "DATA":
                self.reply(b"354 End data with <CR><LF>.<CR><LF>")
                body = b"".join(iter(self.rfile.readline, b".\r\n"))
                box.messages.append(body)
                self.reply(b"250 OK: queued")
            elif command == "QUIT":
                self.reply(b"221 Bye")
                return
            else:
                self.reply(b"502 Command not implemented")


class _Server(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True
    mailbox: Mailbox


@contextmanager
def smtp_server() -> Iterator[tuple[int, Mailbox]]:
    """Run a server on a free local port; yield (port, mailbox)."""
    server = _Server(("127.0.0.1", 0), _Handler)
    server.mailbox = Mailbox()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server.server_address[1], server.mailbox
    finally:
        server.shutdown()
        server.server_close()
