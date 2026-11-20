import inspect
from collections.abc import Callable
from typing import Any, get_type_hints

PY_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean"}

def tool_schema(fn: Callable[..., Any]) -> dict[str, Any]:
    """Build a tool definition from a function's signature and docstring."""
    hints = get_type_hints(fn)
    params = inspect.signature(fn).parameters
    properties = {name: {"type": PY_TO_JSON[hints[name]]} for name in params}
    required = [name for name, p in params.items()
                if p.default is inspect.Parameter.empty]
    return {
        "name": fn.__name__,
        "description": inspect.getdoc(fn) or "",
        "input_schema": {"type": "object",
                         "properties": properties,
                         "required": required},
    }

def get_order_status(order_id: str, include_items: bool = False) -> str:
    """Look up the current status of an order by its ID."""
    return f"Order {order_id}: shipped"

print(tool_schema(get_order_status))
