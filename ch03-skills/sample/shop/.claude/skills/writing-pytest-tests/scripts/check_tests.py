"""Find pytest tests that can never fail, and other common test mistakes.

Usage:  python3 scripts/check_tests.py <test_file.py>

A test needs an assert, a pytest.raises/warns call or a mock assertion such
as assert_called_once_with(). The script also reports 'assert True', bare
'except:', time.sleep and test functions defined twice under one name.
Standard library only. Exit codes: 0 = no problems, 1 = problems or bad input.
"""
import ast
import sys
from pathlib import Path

TestFunc = ast.FunctionDef | ast.AsyncFunctionDef
CHECK_CALLS = {"raises", "warns", "deprecated_call", "fail"}   # pytest.<name>


def call_name(node: ast.Call) -> str:
    """The called name: 'raises' for pytest.raises(...), 'f' for f(...)."""
    func = node.func
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


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


def test_functions(tree: ast.Module) -> list[TestFunc]:
    """Module-level test_ functions and test_ methods of Test classes."""
    found: list[TestFunc] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("test"):
                found.append(node)
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            found.extend(item for item in node.body
                         if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                         and item.name.startswith("test"))
    return found


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python3 scripts/check_tests.py <test_file.py>", file=sys.stderr)
        return 1
    path = Path(argv[1])
    shown = path.as_posix()
    if not path.is_file():
        print(f"error: {shown} does not exist; write the tests first", file=sys.stderr)
        return 1
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        print(f"error: {shown} is not valid Python (line {exc.lineno}: {exc.msg})",
              file=sys.stderr)
        return 1
    tests = test_functions(tree)
    if not tests:
        print(f"error: no test functions in {shown}; name them test_<function>_<behaviour>",
              file=sys.stderr)
        return 1
    problems: list[tuple[int, str, str]] = []
    first_seen: dict[str, int] = {}
    for func in tests:
        if func.name in first_seen:
            problems.append((func.lineno, func.name,
                             f"duplicate name; replaces the test on line "
                             f"{first_seen[func.name]}, which will never run"))
        else:
            first_seen[func.name] = func.lineno
        problems.extend((line, func.name, msg) for line, msg in problems_in(func))
    if not problems:
        print(f"OK: {len(tests)} tests in {shown}, no problems found")
        return 0
    print(f"{shown}: {len(problems)} problems in {len(tests)} tests")
    for line, name, msg in sorted(problems):
        print(f"  line {line}: {name}: {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
