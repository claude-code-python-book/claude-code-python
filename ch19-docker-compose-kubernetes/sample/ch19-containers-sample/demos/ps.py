"""List processes in the container with their resident memory (no ps in slim images)."""

from pathlib import Path

for proc in sorted(Path("/proc").glob("[0-9]*"), key=lambda p: int(p.name)):
    try:
        cmd = (proc / "cmdline").read_bytes().replace(b"\0", b" ").decode().strip()
        rss = next(ln.split()[1] for ln in (proc / "status").read_text().splitlines()
                   if ln.startswith("VmRSS:"))
    except (OSError, StopIteration):
        continue
    if cmd and "ps.py" not in cmd:
        print(f"{proc.name:>4}  {int(rss) // 1024:>3} MiB  {cmd[:66]}")
