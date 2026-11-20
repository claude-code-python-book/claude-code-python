RULES = [
    (r"\bgit\s+push\b.*(--force\b|-f\b|--force-with-lease\b)", "force-push"),
    (r"\bgit\s+push\b.*\b(main|master|release/\S+)\b", "push to a protected branch"),
    (r"(^|[\s;&|])(cat|less|head|tail|cp|scp)\s+\S*\.env\b", "reading a .env file"),
    (r"\b(curl|wget)\b[^|]*\|\s*(ba|z)?sh\b", "piping a download into a shell"),
]


def main() -> int:
    event = json.load(sys.stdin)
    command = event.get("tool_input", {}).get("command", "")
    for pattern, label in RULES:
        if re.search(pattern, command):
            print(f"Blocked by acme-dev policy ({label}). Ask a human to do this.",
                  file=sys.stderr)
            return 2
    return 0
