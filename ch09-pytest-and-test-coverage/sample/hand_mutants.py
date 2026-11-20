"""Apply one hand-written mutation at a time and run the suite (what mutmut automates)."""
import os, shutil, subprocess, sys
from pathlib import Path

PROJ = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "invoicer"
PY = sys.argv[2] if len(sys.argv) > 2 else str(PROJ / ".venv/bin/python")
MUTANTS = [
    ("src/invoicer/billing.py", 'gross * Decimal("0.10")', 'gross * Decimal("0.11")'),
    ("src/invoicer/billing.py", "if days > 30:", "if days >= 30:"),
    ("src/invoicer/billing.py", "if days > 30:", "if days > 31:"),
    ("src/invoicer/billing.py", "periods = (days - 30) // 30 + 1", "periods = (days - 30) // 30"),
    ("src/invoicer/billing.py", 'row.qty >= 100', 'row.qty > 100'),
    ("src/invoicer/billing.py", 'Decimal("0.015")', 'Decimal("0.016")'),
    ("src/invoicer/billing.py", 'net * Decimal("0.05")', 'net * Decimal("0.06")'),
    ("src/invoicer/csv_rows.py", 'first.count(";") > first.count(",")', 'first.count(";") >= first.count(",")'),
    ("src/invoicer/csv_rows.py", "if not any(cleaned):", "if not all(cleaned):"),
    ("src/invoicer/money.py", "if isinstance(value, float):", "if isinstance(value, bool):"),
    ("src/invoicer/billing_models.py", "if self.paid is not None and self.paid < self.issued:", "if self.paid is not None and self.paid <= self.issued:"),
    ("src/invoicer/billing.py", 'if inv.customer != row.customer or inv.region != row.region:', 'if inv.customer != row.customer:'),
    ("src/invoicer/legacy_export.py", '{line.quantity},{line.unit_price}', '{line.quantity};{line.unit_price}'),
]
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(PROJ / "src")}
base = subprocess.run([PY, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", "-m", "not slow", "--ignore=tests/test_properties.py", "--ignore=tests/test_fx_async.py"], cwd=PROJ, env=env, capture_output=True, text=True)
assert base.returncode == 0, base.stdout[-2000:]
for path, old, new in MUTANTS:
    f = PROJ / path
    orig = f.read_text()
    assert orig.count(old) == 1, (path, old)
    f.write_text(orig.replace(old, new))
    for c in PROJ.rglob("__pycache__"):
        shutil.rmtree(c, ignore_errors=True)
    r = subprocess.run([PY, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", "-m", "not slow", "--ignore=tests/test_properties.py", "--ignore=tests/test_fx_async.py"], cwd=PROJ, env=env, capture_output=True, text=True)
    f.write_text(orig)
    subprocess.run(["git", "checkout", "--", "tests/golden"], cwd=PROJ, capture_output=True)
    status = "killed" if r.returncode else "SURVIVED"
    print(f"{status:9} {path}: {old!r} -> {new!r}")
for c in PROJ.rglob("__pycache__"):
    shutil.rmtree(c, ignore_errors=True)
