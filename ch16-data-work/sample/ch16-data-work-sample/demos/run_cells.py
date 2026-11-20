"""Run a notebook's code cells top to bottom in a fresh namespace.

Jupyter could not be installed where this book was written, so this small
runner stands in for "Restart Kernel and Run All" when producing the outputs
quoted in the chapter. It prints what IPython would show for each cell: any
printed text, then the repr of a final bare expression.
"""

import ast
import contextlib
import io
import json
import os
import sys
from pathlib import Path

import pandas as pd

pd.set_option("display.width", 72)


def run(path: Path, only: set[str] | None = None) -> None:
    cells = json.loads(path.read_text())["cells"]
    namespace: dict[str, object] = {"__name__": "__main__"}
    os.chdir(path.parent)
    for number, cell in enumerate(cells, start=1):
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        tree = ast.parse(source)
        last = (
            tree.body.pop()
            if tree.body and isinstance(tree.body[-1], ast.Expr)
            else None
        )
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exec(compile(tree, f"cell {number}", "exec"), namespace)
            value = (
                eval(
                    compile(ast.Expression(last.value), f"cell {number}", "eval"),
                    namespace,
                )
                if last
                else None
            )
        if only is None or cell["id"] in only:
            print(f"--- cell {number} ({cell['id']})")
            text = buffer.getvalue()
            if text:
                print(text, end="")
            if value is not None:
                print(repr(value))


if __name__ == "__main__":
    run(Path(sys.argv[1]).resolve(), set(sys.argv[2:]) or None)
