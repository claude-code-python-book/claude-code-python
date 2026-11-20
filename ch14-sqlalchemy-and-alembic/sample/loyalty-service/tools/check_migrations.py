"""Flag Alembic operations that lock or break a busy PostgreSQL table.

Usage: python tools/check_migrations.py migrations/versions/*.py

Only upgrade() is checked. Silence a finding on its line with a comment such
as `# migration-ok: MIG007 nothing has read this column since v2.3`.
Exit status: 0 when clean, 1 when there are findings.
"""

import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path

MESSAGES = {
    "MIG001": "CREATE INDEX blocks writes until it ends; "
    "use postgresql_concurrently=True",
    "MIG002": "CONCURRENTLY can't run in a transaction block; "
    "wrap it in op.get_context().autocommit_block()",
    "MIG003": "NOT NULL with no server_default fails on a table that has rows",
    "MIG004": "a volatile default rewrites the whole table",
    "MIG005": "a type change can rewrite the table under ACCESS EXCLUSIVE",
    "MIG006": "SET NOT NULL scans the table under ACCESS EXCLUSIVE; "
    "VALIDATE a CHECK (col IS NOT NULL) NOT VALID first",
    "MIG007": "a contract step: ship it after no running code uses it",
    "MIG008": "imports app code, which will change after this migration",
}
# Functions PostgreSQL marks volatile; now() is stable, so it is not here.
VOLATILE = ("clock_timestamp", "random", "gen_random_uuid", "uuid_generate_v4")
OK_COMMENT = re.compile(r"#\s*migration-ok:\s*(MIG\d{3})")


@dataclass(frozen=True)
class Finding:
    """One problem at one line of one file."""

    path: str
    line: int
    code: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.code} {MESSAGES[self.code]}"


def _kw(call: ast.Call, name: str) -> ast.expr | None:
    return next((k.value for k in call.keywords if k.arg == name), None)


def _const(node: ast.expr | None) -> object:
    return node.value if isinstance(node, ast.Constant) else None


def _op(call: ast.Call) -> str | None:
    """Return "add_column" for op.add_column(...), else None."""
    f = call.func
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
        return f.attr if f.value.id == "op" else None
    return None


def _arg(call: ast.Call, index: int, name: str) -> ast.expr | None:
    return call.args[index] if len(call.args) > index else _kw(call, name)


def _volatile(node: ast.expr | None) -> bool:
    """Return True if a server_default calls a volatile function."""
    text = ast.unparse(node) if node is not None else ""
    return any(re.search(rf"\b{name}\b", text) for name in VOLATILE)


def _strings(tree: ast.AST) -> str:
    return " ".join(
        n.value.upper()
        for n in ast.walk(tree)
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    )


class _Checker(ast.NodeVisitor):
    def __init__(self, upgrade: ast.FunctionDef) -> None:
        self.found: list[tuple[int, str]] = []
        self.autocommit = 0
        self.new_tables = {
            _const(_arg(c, 0, "table_name"))
            for c in ast.walk(upgrade)
            if isinstance(c, ast.Call) and _op(c) == "create_table"
        }
        self.validates = "VALIDATE CONSTRAINT" in _strings(upgrade)

    def visit_With(self, node: ast.With) -> None:
        block = any(
            isinstance(i.context_expr, ast.Call)
            and isinstance(i.context_expr.func, ast.Attribute)
            and i.context_expr.func.attr == "autocommit_block"
            for i in node.items
        )
        self.autocommit += block
        self.generic_visit(node)
        self.autocommit -= block

    def visit_Call(self, node: ast.Call) -> None:
        name, line = _op(node), node.lineno
        concurrently = _const(_kw(node, "postgresql_concurrently")) is True
        if name in ("create_index", "drop_index") and concurrently:
            if not self.autocommit:
                self.found.append((line, "MIG002"))
        elif name == "create_index":
            if _const(_arg(node, 1, "table_name")) not in self.new_tables:
                self.found.append((line, "MIG001"))
        elif name == "add_column":
            col = _arg(node, 1, "column")
            if isinstance(col, ast.Call):
                default = _kw(col, "server_default")
                if _const(_kw(col, "nullable")) is False and default is None:
                    self.found.append((line, "MIG003"))
                if _volatile(default):
                    self.found.append((line, "MIG004"))
        elif name == "alter_column":
            if _kw(node, "type_") is not None:
                self.found.append((line, "MIG005"))
            if _const(_kw(node, "nullable")) is False and not self.validates:
                self.found.append((line, "MIG006"))
        elif name in ("drop_column", "drop_table"):
            self.found.append((line, "MIG007"))
        self.generic_visit(node)


def _imports_app(node: ast.Import | ast.ImportFrom) -> bool:
    if isinstance(node, ast.ImportFrom):
        return (node.module or "").split(".")[0] == "loyalty"
    return any(a.name.split(".")[0] == "loyalty" for a in node.names)


def check_source(source: str, path: str = "<migration>") -> list[Finding]:
    """Return the findings for one migration file."""
    tree = ast.parse(source)
    found = [
        (n.lineno, "MIG008")
        for n in ast.walk(tree)
        if isinstance(n, ast.Import | ast.ImportFrom) and _imports_app(n)
    ]
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "upgrade":
            checker = _Checker(node)
            checker.visit(node)
            found += checker.found
    lines = source.splitlines()
    return [
        Finding(path, line, code)
        for line, code in sorted(found)
        if code not in OK_COMMENT.findall(lines[line - 1])
    ]


def main(paths: list[str]) -> int:
    """Check each file named on the command line."""
    findings = [f for p in paths for f in check_source(Path(p).read_text(), p)]
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
