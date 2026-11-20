def matches(finding: Finding, path: str, expected: dict[str, Any]) -> bool:
    text = finding.message.lower()
    return (
        finding.path == path
        and abs(finding.line - expected["line"]) <= 3
        and RANK[finding.severity] >= RANK[expected["min_severity"]]
        and any(word in text for word in expected["keywords"])
    )
