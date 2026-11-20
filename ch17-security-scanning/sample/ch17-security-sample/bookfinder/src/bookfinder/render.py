"""HTML rendering with autoescaping switched on."""

from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("bookfinder"),
    autoescape=select_autoescape(),  # escapes .html/.htm/.xml templates
)


def render_results(query: str, books: list[dict[str, Any]]) -> str:
    """Render the results page; ``query`` is user input and gets escaped."""
    return env.get_template("results.html").render(query=query, books=books)
