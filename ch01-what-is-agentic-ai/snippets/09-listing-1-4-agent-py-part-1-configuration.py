"""A minimal agent that finds TODO comments in a Python project.

Run it with:  uv run python agent.py ./src
Needs:        uv add anthropic   and   ANTHROPIC_API_KEY set
"""
import sys
import textwrap
from collections.abc import Callable
from pathlib import Path
from typing import Any

import anthropic

MODEL = "claude-sonnet-5-5"   # check the Models page for current IDs
MAX_TOKENS = 16000            # a ceiling, not a cost: thinking counts too
MAX_STEPS = 10                # hard stop: never let the loop run forever
THINKING = {"type": "adaptive", "display": "summarized"}  # show reasoning

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the env
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SKIP_DIRS = {".venv", "venv", ".git", "__pycache__", "node_modules"}
