"""Run the book's code offline: install the fake `anthropic` before any import."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))          # fake_anthropic
sys.path.insert(1, str(HERE.parent))   # the chapter's modules

import fake_anthropic  # noqa: E402

sys.modules["anthropic"] = fake_anthropic
