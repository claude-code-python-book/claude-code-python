# --- Tools: ordinary Python functions --------------------------------
def _safe_path(relative: str) -> Path:
    """Resolve a path and refuse anything outside the project root."""
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"{relative} is outside the project")
    return path

def list_python_files(directory: str = ".") -> str:
    """List .py files under a directory, relative to the project root."""
    base = _safe_path(directory)
    files = sorted(
        p.relative_to(ROOT).as_posix()
        for p in base.rglob("*.py")
        if not SKIP_DIRS.intersection(p.relative_to(ROOT).parts)
    )
    return "\n".join(files) or "(no Python files found)"

def read_file(path: str) -> str:
    """Return a file's contents with line numbers."""
    lines = _safe_path(path).read_text(encoding="utf-8").splitlines()
    numbered = "\n".join(f"{n:>4}: {line}" for n, line in enumerate(lines, 1))
    return numbered or "(empty file)"

TOOLS: dict[str, Callable[..., str]] = {
    "list_python_files": list_python_files,
    "read_file": read_file,
}
