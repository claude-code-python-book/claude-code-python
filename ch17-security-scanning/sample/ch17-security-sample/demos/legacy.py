"""A module written years ago, run unchanged on newer interpreters."""

import sys
import warnings
from datetime import datetime

warnings.simplefilter("default")  # show DeprecationWarnings, as pytest does

print(f"Python {sys.version.split()[0]}")
stamp = datetime.utcnow()  # naive UTC timestamp
print("utcnow() ok:", stamp.year >= 2026)
try:
    import cgi  # used for cgi.parse_header()

    print("cgi ok:", cgi.parse_header("text/html; charset=utf-8"))
except ModuleNotFoundError as error:
    print("ModuleNotFoundError:", error)
