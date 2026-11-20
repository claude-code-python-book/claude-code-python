from pathlib import Path

import pytest
import yaml

from bookfinder.importer import count_lines, load_cache, load_catalogue, save_cache

CATALOGUE = """
- title: Fluent Python
  year: 2022
"""


def test_loads_plain_yaml() -> None:
    assert load_catalogue(CATALOGUE) == [{"title": "Fluent Python", "year": 2022}]


def test_python_object_tags_are_refused() -> None:
    with pytest.raises(yaml.constructor.ConstructorError):
        load_catalogue("- !!python/object/apply:os.getcwd []")


def test_cache_round_trips_as_json(tmp_path: Path) -> None:
    path = tmp_path / "cache.json"
    save_cache([{"title": "Robust Python"}], path)
    assert path.read_text() == '[{"title": "Robust Python"}]'
    assert load_cache(path) == [{"title": "Robust Python"}]


def test_file_names_cannot_inject_commands(tmp_path: Path) -> None:
    sneaky = tmp_path / "books.txt; echo INJECTED"
    sneaky.write_text("a\nb\n")
    assert count_lines(sneaky) == 2
