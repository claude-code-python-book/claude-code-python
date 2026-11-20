def has_check(func: TestFunc) -> bool:
    for node in ast.walk(func):
        if isinstance(node, ast.Assert):
            return True
        if isinstance(node, ast.Call):
            name = call_name(node)
            if name in CHECK_CALLS or name.startswith("assert_"):
                return True
    return False

def problems_in(func: TestFunc) -> list[tuple[int, str]]:
    found = []
    if not has_check(func):
        found.append((func.lineno, "no assert or pytest.raises, so it can never fail"))
    for node in ast.walk(func):
        if (isinstance(node, ast.Assert) and isinstance(node.test, ast.Constant)
                and node.test.value):
            found.append((node.lineno, f"'assert {node.test.value!r}' always passes"))
        elif isinstance(node, ast.ExceptHandler) and node.type is None:
            found.append((node.lineno, "bare 'except:' hides real failures"))
        elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
              and node.func.attr == "sleep"
              and isinstance(node.func.value, ast.Name)
              and node.func.value.id == "time"):
            found.append((node.lineno, "time.sleep slows the suite; mock time instead"))
    return found
