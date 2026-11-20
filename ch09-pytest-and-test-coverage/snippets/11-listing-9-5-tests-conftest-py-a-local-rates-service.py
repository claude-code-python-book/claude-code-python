RATES = {
    "GBP": {"EUR": 1.15, "USD": 1.27},
    "EUR": {"GBP": 0.87, "USD": 1.10},
}


class RatesHandler(BaseHTTPRequestHandler):
    """Serves RATES the way the real rates service does: /latest?base=GBP."""

    def do_GET(self) -> None:
        base = parse_qs(urlsplit(self.path).query).get("base", [""])[0]
        if base not in RATES:
            self.send_error(404)
            return
        body = json.dumps({"base": base, "rates": RATES[base]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        pass  # keep pytest's output clean


@pytest.fixture(scope="session")
def rates_server() -> Iterator[str]:
    """A local rates service on a free port, started once per test session."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), RatesHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/latest"
    server.shutdown()
    server.server_close()
