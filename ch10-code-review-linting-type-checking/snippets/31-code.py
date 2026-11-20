from typing import Any


def parse_amount(raw: Any) -> Any:
    try:
        return float(raw)
    except Exception:
        return None


def total(values: list[str]) -> int:
    return sum(int(v) for v in values)  # type: ignore[return-value]
