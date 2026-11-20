"""A multi-agent content pipeline: plan -> write in parallel -> review -> fix.

Run it with:  uv run python pipeline.py "How Python's GIL affects threads"
Needs:        uv add anthropic   and   ANTHROPIC_API_KEY set
"""
import asyncio
import json
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import anthropic

MODEL = "claude-sonnet-5-5"   # check the Models page for current IDs
MAX_TOKENS = 16000            # a ceiling per reply; thinking counts toward it
MAX_REVISIONS = 1             # how many times the writers may fix their work
client = anthropic.AsyncAnthropic()

# --- Shared state: one place that every step reads and writes ----------
@dataclass
class PipelineState:
    topic: str
    outline: list[dict[str, str]] = field(default_factory=list)
    sections: dict[str, str] = field(default_factory=dict)
    review: dict[str, Any] = field(default_factory=dict)
    log: list[str] = field(default_factory=list)
    tokens: int = 0
