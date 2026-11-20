# --- A tool for the reviewer: check Python syntax without running it ---
def check_python(code: str) -> str:
    """Compile a snippet to find syntax errors. The code is never run."""
    try:
        compile(code, "<snippet>", "exec")
        return "OK: no syntax errors"
    except SyntaxError as exc:
        return f"SyntaxError on line {exc.lineno}: {exc.msg}"

CHECK_PYTHON_SCHEMA = {
    "name": "check_python",
    "description": "Check one Python code block for syntax errors. "
                   "Pass only the code, without the ``` fences.",
    "input_schema": {
        "type": "object",
        "properties": {"code": {"type": "string"}},
        "required": ["code"],
    },
}
Tools = dict[str, tuple[Callable[..., str], dict[str, Any]]]
