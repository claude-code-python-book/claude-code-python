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
