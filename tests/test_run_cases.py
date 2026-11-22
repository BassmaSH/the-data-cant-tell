"""Tests for run_cases.py: what each command would run, and under which file names. No API call.

    pytest tests/test_run_cases.py

No test calls a model. The commands are only read, and what they would run is compared with the
answers already saved in results/: the same file names, the same system message, the same question.

Code written by Claude Code on Nov 15, 2026, for the author.
"""

import json
import re
import shlex
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import run_cases  # noqa: E402
from run_cases import PREMISE, SMALL, STEPS, SYSTEM  # noqa: E402

RESULTS = ROOT / "results"
README = (ROOT / "README.md").read_text()

# Commands in the form used for the runs, with what each must mean: the models, the system message,
# and one answer file that the run of that day saved. The first eight and the two that start with
# "x" are written in NOTEBOOK.md, the README or the earlier usage text of run_cases.py. The other
# three combine the same options to reach an answer that no recorded command names.
RECORDED = [
    (
        "mistral-large-2512",
        [SMALL, "mistral-large-2512"],
        SYSTEM,
        "2026-10-20/C01-mistral-large-2512.json",
    ),
    (
        "mistral-large-2512 --no-system",
        [SMALL, "mistral-large-2512"],
        None,
        "2026-10-20/C04-mistral-small-2603-nosys.json",
    ),
    (
        "mistral-large-2512 --premise",
        [SMALL, "mistral-large-2512"],
        SYSTEM + " " + PREMISE,
        "2026-10-20/C09-mistral-large-2512-premise.json",
    ),
    (
        "mistral-large-2512 --premise-only",
        [SMALL, "mistral-large-2512"],
        PREMISE,
        "2026-10-20/C06-mistral-small-2603-premiseonly.json",
    ),
    (
        "mistral-large-2512 --steps",
        [SMALL, "mistral-large-2512"],
        STEPS,
        "2026-10-20/C02-mistral-large-2512-steps.json",
    ),
    (
        "mistral-large-2512 C06 --tag v2",
        [SMALL, "mistral-large-2512"],
        SYSTEM,
        "2026-10-15/C06-mistral-large-2512-v2.json",
    ),
    (
        "mistral-large-2512 C05 --data categories",
        [SMALL, "mistral-large-2512"],
        SYSTEM,
        "2026-10-20/C05-mistral-small-2603-categories.json",
    ),
    (
        "mistral-large-4-0 --models mistral-large-4-0 --reasoning high",
        ["mistral-large-4-0"],
        SYSTEM,
        "2026-10-20/C03-mistral-large-4-0-rhigh.json",
    ),
    (
        "mistral-large-4-0 --models mistral-large-4-0 --reasoning none --no-system",
        ["mistral-large-4-0"],
        None,
        "2026-10-20/C03-mistral-large-4-0-nosys-rnone.json",
    ),
    (
        "mistral-large-4-0 C05 --models mistral-large-4-0 --reasoning high --steps "
        "--data categories",
        ["mistral-large-4-0"],
        STEPS,
        "2026-10-20/C05-mistral-large-4-0-steps-rhigh-categories.json",
    ),
    (
        "x C04 --models claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5",
        ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"],
        SYSTEM,
        "2026-10-20/C04-claude-opus-5-5.json",
    ),
    (
        "x --data computed --models mistral-large-4-0 --reasoning none",
        ["mistral-large-4-0"],
        SYSTEM,
        "2026-10-20/C07-mistral-large-4-0-rnone-computed.json",
    ),
    (
        "C05 --data categories-computed --models mistral-small-2603",
        [SMALL],
        SYSTEM,
        "2026-10-20/C05-mistral-small-2603-categories-computed.json",
    ),
]


def readme_commands() -> list[str]:
    """Return the arguments of each run_cases.py command in the README's "Run it" block."""
    return re.findall(r"python run_cases\.py ([^#\n]+)", README)


def saved_by(plan: run_cases.Plan, folder: str) -> list[Path]:
    """Return the answer files a plan would write, placed in a folder of results/."""
    return [RESULTS / folder / plan.answer_name(c, m) for c in plan.cases for m in plan.models]


@pytest.mark.parametrize(("command", "models", "system", "saved"), RECORDED)
def test_a_recorded_command_still_means_what_it_ran(
    command: str, models: list[str], system: str | None, saved: str
):
    plan = run_cases.plan_from(shlex.split(command))
    assert plan.models == models
    assert plan.system == system
    folder, name = saved.split("/")
    assert RESULTS / saved in saved_by(plan, folder)
    record = json.loads((RESULTS / saved).read_text())
    assert record["system"] == plan.system
    assert record["question"] == run_cases.QUESTIONS[record["case"]]
    assert (ROOT / "cases" / "data" / plan.data_name(record["case"])).exists()


def test_every_command_in_the_readme_names_answers_that_were_saved():
    commands = readme_commands()
    assert len(commands) == 3
    for command in commands:
        plan = run_cases.plan_from(shlex.split(command))
        assert plan.cases == list(run_cases.QUESTIONS), command
        for path in saved_by(plan, "2026-10-20"):
            # Run 1 (Oct 15) holds five of the system-message answers of the first two models.
            assert path.exists() or (RESULTS / "2026-10-15" / path.name).exists(), path


def test_the_system_message_of_every_saved_answer_is_one_of_the_set_ups():
    messages = {system for system, _ in run_cases.SETUPS.values()}
    records = [json.loads(p.read_text()) for p in RESULTS.glob("*/*.json")]
    assert len(records) > 320
    assert {r["system"] for r in records} == messages


def test_the_set_ups_in_the_readme_are_the_ones_sent():
    one_line = " ".join(README.split())
    assert f'"{SYSTEM}"' in one_line
    assert f'"{PREMISE}"' in one_line
    assert f'"{" ".join(STEPS.split())}"' in one_line
    for case, question in run_cases.QUESTIONS.items():
        assert f"| {case} | {question} |" in one_line


def test_without_models_the_pair_is_small_and_the_model_named():
    plan = run_cases.plan_from(["some-large-model", "C04", "C09"])
    assert plan.models == [SMALL, "some-large-model"]
    assert plan.cases == ["C04", "C09"]
    assert plan.tag == ""


def test_models_alone_is_enough():
    plan = run_cases.plan_from(["--models", "claude-haiku-5-5", "--steps"])
    assert plan.models == ["claude-haiku-5-5"]
    assert plan.answer_name("C01", "claude-haiku-5-5") == "C01-claude-haiku-5-5-steps.json"


def test_a_command_that_names_no_model_is_refused():
    for command in ([], ["C04"], ["--steps"], ["one-model", "another-model"]):
        with pytest.raises(ValueError):
            run_cases.plan_from(command)


def test_a_word_shaped_like_a_case_that_does_not_exist_is_refused():
    for command in (["--models", "a-model", "C10"], ["a-model", "c04"], ["a-model", "C4"]):
        with pytest.raises(ValueError, match="no such case"):
            run_cases.plan_from(command)


def test_every_command_in_the_readme_stops_before_any_call_when_no_key_is_set(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    today = ROOT / "results" / run_cases.date.today().isoformat()
    existed = today.exists()
    for command in [*readme_commands(), "models"]:
        with pytest.raises(SystemExit) as stop:
            run_cases.main(shlex.split(command))
        assert "API_KEY not set: nothing was called" in str(stop.value), command
    assert today.exists() == existed
    assert run_cases.mistral_client.cache_info().currsize == 0
    assert run_cases.claude_client.cache_info().currsize == 0


def test_the_key_asked_for_is_the_one_of_the_models_named():
    plan = run_cases.plan_from(["--models", "claude-haiku-5-5,mistral-large-4-0"])
    folder = ROOT / "results" / "no-such-day"
    assert run_cases.reason_not_to_run(plan, folder, {"MISTRAL_API_KEY": "k"}).startswith(
        "ANTHROPIC_API_KEY not set"
    )
    assert run_cases.reason_not_to_run(plan, folder, {}).startswith(
        "ANTHROPIC_API_KEY and MISTRAL_API_KEY not set"
    )
    both = {"MISTRAL_API_KEY": "k", "ANTHROPIC_API_KEY": "k"}
    assert run_cases.reason_not_to_run(plan, folder, both) is None


def test_a_saved_answer_is_never_replaced():
    keys = {"MISTRAL_API_KEY": "k"}
    plan = run_cases.plan_from(["mistral-large-2512", "--steps"])
    reason = run_cases.reason_not_to_run(plan, RESULTS / "2026-10-20", keys)
    assert reason.startswith("18 of these answers are already saved") and "--tag" in reason
    again = run_cases.plan_from(["mistral-large-2512", "--steps", "--tag", "repeat2"])
    assert run_cases.reason_not_to_run(again, RESULTS / "2026-10-20", keys) is None


def test_two_set_ups_at_once_are_refused():
    with pytest.raises(SystemExit):
        run_cases.plan_from(["a-model", "--steps", "--premise"])


def test_the_data_block_follows_the_data_option():
    assert run_cases.plan_from(["m"]).data_name("C05") == "C05-data.txt"
    assert (
        run_cases.plan_from(["m", "--data", "computed"]).data_name("C05") == "C05-data-computed.txt"
    )


def test_the_user_message_is_the_data_then_the_question():
    assert run_cases.user_message("D", "Q?") == "data:D, question:Q?"


def test_reading_a_command_builds_no_client():
    run_cases.plan_from(["a-model"])
    assert run_cases.mistral_client.cache_info().currsize == 0
    assert run_cases.claude_client.cache_info().currsize == 0
    assert "mistralai" not in sys.modules and "anthropic" not in sys.modules
