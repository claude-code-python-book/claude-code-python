"""List the public functions and methods of a Python module as JSON.

Usage:  python3 scripts/list_functions.py <module.py>

For each public function and method this prints its signature, the first
line of its docstring and the exceptions it raises directly. It reads the
code with the ast module and never runs it. Standard library only.
Exit codes: 0 = success, 1 = the file is missing or is not valid Python.
"""
import ast
import json
import sys
from pathlib import Path

NESTED = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)


def raised_exceptions(func: ast.AST) -> list[str]:
    """Names of exceptions raised in this function, not in nested ones."""
    names: set[str] = set()
    stack = list(ast.iter_child_nodes(func))
    while stack:
        node = stack.pop()
        if isinstance(node, NESTED):
            continue                      # a nested def raises on its own
        if isinstance(node, ast.Raise) and node.exc is not None:
            exc = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
            names.add(ast.unparse(exc))
        stack.extend(ast.iter_child_nodes(node))
    return sorted(names)


def describe(func: ast.FunctionDef | ast.AsyncFunctionDef, owner: str = "") -> dict:
    prefix = "async def" if isinstance(func, ast.AsyncFunctionDef) else "def"
    returns = f" -> {ast.unparse(func.returns)}" if func.returns else ""
    doc = ast.get_docstring(func) or ""
    return {
        "name": f"{owner}.{func.name}" if owner else func.name,
        "signature": f"{prefix} {func.name}({ast.unparse(func.args)}){returns}",
        "line": func.lineno,
        "summary": doc.splitlines()[0] if doc else "",
        "raises": raised_exceptions(func),
    }


def public_functions(tree: ast.Module) -> list[dict]:
    """Top-level functions and the methods of top-level classes, in file order."""
    found = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                found.append(describe(node))
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            for item in node.body:
                if (isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                        and not item.name.startswith("_")):
                    found.append(describe(item, owner=node.name))
    return found


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python3 scripts/list_functions.py <module.py>", file=sys.stderr)
        return 1
    path = Path(argv[1])
    if not path.is_file():
        print(f"error: {path.as_posix()} does not exist; pass the path of a .py file",
              file=sys.stderr)
        return 1
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        print(f"error: {path.as_posix()} is not valid Python (line {exc.lineno}: "
              f"{exc.msg}); fix the syntax first", file=sys.stderr)
        return 1
    print(json.dumps(public_functions(tree), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
