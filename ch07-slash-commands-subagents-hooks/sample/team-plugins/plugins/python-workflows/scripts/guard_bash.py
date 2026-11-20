"""PreToolUse hook: deny or confirm dangerous shell commands.

A seatbelt, not a sandbox: it catches common mistakes in the commands
Claude writes, not every possible way to do damage.
"""

import json
import os
import shlex
import sys
from pathlib import Path

SHELLS = {"sh", "bash", "zsh"}
Verdict = tuple[str, str]  # (permission decision, reason)


def split_commands(line: str) -> list[tuple[list[str], str]]:
    """Split a command line into (words, operator that follows) pairs."""
    line = line.replace("\n", ";")
    lexer = shlex.shlex(line, posix=True, punctuation_chars=";&|")
    lexer.whitespace_split = True
    commands: list[tuple[list[str], str]] = []
    words: list[str] = []
    for token in lexer:
        if token in {";", "&", "&&", "|", "||"}:
            commands.append((words, token))
            words = []
        else:
            words.append(token)
    commands.append((words, ""))
    # Drop "sudo" and leading VAR=value assignments.
    for words, _ in commands:
        while words and (words[0] == "sudo" or "=" in words[0]):
            del words[0]
    return [(words, op) for words, op in commands if words]


def short_flags(args: list[str]) -> str:
    return "".join(a[1:] for a in args if a.startswith("-") and a[1:2] != "-")


def check_rm(args: list[str], project: Path, cwd: Path) -> Verdict | None:
    flags = short_flags(args)
    recursive = "r" in flags.lower() or "--recursive" in args
    if not (recursive and ("f" in flags or "--force" in args)):
        return None
    for target in (a for a in args if not a.startswith("-")):
        path = (cwd / os.path.expandvars(os.path.expanduser(target))).resolve()
        if path == project or not path.is_relative_to(project):
            return "deny", f"rm -rf '{target}' reaches outside the project folder."
        if any(ch in target for ch in "*?[") and path.parent == project:
            return "deny", f"rm -rf '{target}' would empty the project root."
    return None


def check(words: list[str], project: Path, cwd: Path) -> Verdict | None:
    """Return a verdict for one simple command, or None for no opinion."""
    prog, args = Path(words[0]).name, words[1:]
    if prog in SHELLS and "-c" in args[:-1]:
        return check_line(args[args.index("-c") + 1], project, cwd)
    if prog == "rm":
        return check_rm(args, project, cwd)
    if prog == "git" and args[:1] == ["push"]:
        if "--force" in args or "f" in short_flags(args):
            return "deny", "Force-pushing rewrites shared history."
    if prog == "git" and args[:2] == ["reset", "--hard"]:
        return "ask", "git reset --hard throws away uncommitted work."
    if prog == "git" and args[:1] == ["clean"]:
        if "--force" in args or "f" in short_flags(args):
            return "ask", "git clean deletes untracked files for good."
    if (prog in {"pip", "pip3"} and args[:1] == ["install"]) or (
        prog.startswith("python") and args[:3] == ["-m", "pip", "install"]
    ):
        return "deny", "This project uses uv: ask the user, then `uv add <pkg>`."
    return None


def check_line(line: str, project: Path, cwd: Path) -> Verdict | None:
    try:
        commands = split_commands(line)
    except ValueError:  # unbalanced quotes: let a human decide
        return "ask", "The guard hook could not parse this command."
    verdicts: list[Verdict] = []
    for i, (words, op) in enumerate(commands):
        prog = Path(words[0]).name
        if prog in {"curl", "wget"} and op == "|" and i + 1 < len(commands):
            if Path(commands[i + 1][0][0]).name in SHELLS | {"python", "python3"}:
                verdicts.append(("deny", "Don't pipe a download into a shell."))
        if prog == "cd" and len(words) > 1:  # later commands run there
            cwd = (cwd / os.path.expanduser(words[1])).resolve()
        elif verdict := check(words, project, cwd):
            verdicts.append(verdict)
    # The most restrictive verdict wins, as it does between hooks.
    for decision in ("deny", "ask"):
        for verdict in verdicts:
            if verdict[0] == decision:
                return verdict
    return None


def main() -> int:
    event = json.load(sys.stdin)
    command = event.get("tool_input", {}).get("command", "")
    cwd = Path(event["cwd"]).resolve()
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", cwd)).resolve()

    verdict = check_line(command, project, cwd)
    if verdict is None:
        return 0  # no output: the normal permission rules decide
    decision, reason = verdict
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
