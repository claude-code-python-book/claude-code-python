"""Check Agent Skill folders against the rules in Chapter 3.

Usage:  python validate_skill.py <skill-folder> [<skill-folder> ...]
Needs:  PyYAML (uv add pyyaml)

Errors break a rule of the open specification or Anthropic's platform;
warnings are best practice. Exit code 1 if any skill has an error.
"""
import re
import sys
from pathlib import Path

import yaml

NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PORTABLE = {"name", "description", "license", "compatibility", "metadata",
            "allowed-tools"}
FILE_REF = re.compile(r"\b((?:scripts|references|assets)/[\w./-]+)")


def check(folder: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill = folder / "SKILL.md"
    if not skill.is_file():
        return [f"{skill.as_posix()} does not exist"], []
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ["SKILL.md must start with '---' on line 1 (YAML front matter)"], []
    try:
        _, front, body = text.split("---", 2)
        meta = yaml.safe_load(front) or {}
    except (ValueError, yaml.YAMLError) as exc:
        return [f"front matter is not valid YAML: {exc}"], []

    name = str(meta.get("name", ""))
    if not name:
        errors.append("'name' is required")
    else:
        if len(name) > 64:
            errors.append("'name' must be at most 64 characters")
        if not NAME.match(name):
            errors.append("'name' may use only lowercase letters, numbers and single "
                          "hyphens, and cannot start or end with a hyphen")
        if name != folder.name:
            errors.append(f"'name' ({name}) must match the folder name ({folder.name})")
        if "anthropic" in name or "claude" in name:
            errors.append("'name' cannot contain 'anthropic' or 'claude'")

    description = str(meta.get("description", ""))
    if not description:
        errors.append("'description' is required")
    elif len(description) > 1024:
        errors.append("'description' must be at most 1,024 characters")
    if re.search(r"<[^>]+>", description):
        errors.append("'description' cannot contain XML tags")

    for ref in sorted(set(FILE_REF.findall(body))):
        ref = ref.rstrip(".")
        if not (folder / ref).exists():
            errors.append(f"SKILL.md mentions {ref}, which does not exist")

    if description and "use when" not in description.lower():
        warnings.append("'description' should say when to use the skill ('Use when ...')")
    if re.search(r"\b(I|me|my|you|your)\b", description):
        warnings.append("write 'description' in the third person")
    extra = sorted(set(meta) - PORTABLE)
    if extra:
        warnings.append(f"Claude Code-only fields {extra}: claude.ai and the Skills API "
                        "reject them")
    if re.search(r"\w\\\w", body):
        warnings.append("use forward slashes in file paths")
    return errors, warnings


def main(folders: list[str]) -> int:
    if not folders:
        print("usage: python validate_skill.py <skill-folder> ...", file=sys.stderr)
        return 1
    failed = False
    for arg in folders:
        folder = Path(arg)
        errors, warnings = check(folder)
        failed |= bool(errors)
        print(f"{'FAIL' if errors else 'OK'}: {folder.name}")
        for msg in errors:
            print(f"  error:   {msg}")
        for msg in warnings:
            print(f"  warning: {msg}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
