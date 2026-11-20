"""A file name that is also a shell command."""

import subprocess
from pathlib import Path

name = "notes.txt; echo INJECTED"
Path("notes.txt").write_text("one\ntwo\n")

print("shell=True:")
subprocess.run(f"wc -l {name}", shell=True)
print("argument list:")
subprocess.run(["wc", "-l", "--", name])
