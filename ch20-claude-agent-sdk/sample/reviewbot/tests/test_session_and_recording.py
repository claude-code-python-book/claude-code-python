"""Multi-turn sessions, interrupts, and record/replay round trips."""

from pathlib import Path

import pytest

from reviewbot.oneshot import ask_repo
from reviewbot.recording import RecordingTransport, load_turns
from reviewbot.session import review_chat

from fakecli import FakeCLI
from script import assistant, init_frame, result, text_block


def answer_turn(text: str, msg_id: str) -> list[dict]:
    return [assistant([text_block(text)], msg_id), result(text)]


@pytest.mark.anyio
async def test_two_turns_share_one_session(repo: Path) -> None:
    cli = FakeCLI([
        [init_frame(["Read"]), *answer_turn("One finding in stats.py.", "m1")],
        answer_turn("Restore the `if not xs` guard.", "m2"),
    ])
    answers = await review_chat(repo, ["Review the branch.", "How do I fix it?"],
                                transport=cli)
    assert answers == ["One finding in stats.py.", "Restore the `if not xs` guard."]
    prompts = [m["message"]["content"] for m in cli.sent if m["type"] == "user"]
    assert prompts == ["Review the branch.", "How do I fix it?"]


@pytest.mark.anyio
async def test_slow_turn_is_interrupted(repo: Path) -> None:
    slow = [{"type": "_pause", "seconds": 0.3},
            result("", subtype="error_during_execution", is_error=True)]
    cli = FakeCLI([slow])
    answers = await review_chat(repo, ["Review everything."], deadline_s=0.05,
                                transport=cli)
    subtypes = [m["request"]["subtype"] for m in cli.sent
                if m["type"] == "control_request"]
    assert "interrupt" in subtypes
    assert answers == ["[error_during_execution]"]


@pytest.mark.anyio
async def test_ask_repo_one_shot(repo: Path) -> None:
    cli = FakeCLI([[init_frame(["Read", "Grep", "Glob"]),
                    *answer_turn("average() is in stats.py.", "m1")]])
    assert await ask_repo(repo, "Where is average?", transport=cli) == (
        "average() is in stats.py.")


@pytest.mark.anyio
async def test_record_then_replay_gives_same_stream(repo: Path,
                                                   tmp_path: Path) -> None:
    script = [[init_frame(["Read"]), *answer_turn("first", "m1")],
              answer_turn("second", "m2")]
    path = tmp_path / "session.json"
    live = RecordingTransport(FakeCLI(script), path)
    first = await review_chat(repo, ["a", "b"], transport=live)

    turns = load_turns(path)
    assert [len(t) for t in turns] == [3, 2]    # no control_response frames
    replayed = await review_chat(repo, ["a", "b"], transport=FakeCLI(turns))
    assert replayed == first == ["first", "second"]
