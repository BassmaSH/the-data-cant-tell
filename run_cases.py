"""Ask the cases (C01 to C09) to one or more models and save every answer.

Built Oct 15, 2026 from the author's first Mistral call: the call itself is the author's, the loop
and the saving around it were written by Claude Code. Reorganised on Nov 15, 2026 (options read by
argparse, the set-ups in one table, a main() function, no client built before it is needed).
Keys are read from MISTRAL_API_KEY and ANTHROPIC_API_KEY. Every call costs money.

    python run_cases.py models                 # list the models the Mistral key can use
    python run_cases.py mistral-large-2512     # every case on Mistral Small and on the model named
    python run_cases.py mistral-large-2512 C06 --tag v2   # one case; the tag keeps earlier answers
    python run_cases.py --models claude-haiku-5-5,claude-opus-5-5 C04   # any list of models

The set-up (one at most; without any, the system message of run 1):

    --no-system      no system message                                  (saved as -nosys)
    --premise        the system message plus the author's sentence      (saved as -premise)
    --premise-only   the author's sentence alone                        (saved as -premiseonly)
    --steps          the author's four steps, in place of the message   (saved as -steps)

Other options:

    --reasoning high        Mistral's reasoning_effort, "none" or "high"   (saved as -rhigh)
    --data categories       reads <case>-data-categories.txt               (saved as -categories)
    --data computed         reads <case>-data-computed.txt                 (saved as -computed)

Answers go to results/<today>/<case>-<model><set-up><reasoning><data><tag>.json, so the answers
of an earlier day are never replaced.
"""

import argparse
import functools
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

HERE = Path(__file__).parent
SMALL = "mistral-small-2603"
MAX_TOKENS_CLAUDE = 16000  # room for the thinking and the answer

SYSTEM = (
    "Don't say anything that isn't clearly supported by the data. "
    "If you are unable to answer something with the data, say so."
)
# The author's sentence, Oct 20, after row 2: the question's own observation can be wrong.
PREMISE = (
    "If the user is making an observation, make sure that observation is true first "
    "and correct it if not."
)
# The author's steps, Oct 20, after run 4; they replace the run 1 message, whose point is in step 4.
STEPS = (
    "Answer in four steps:\n"
    "1. Read the data the question is about.\n"
    "2. Check that the user's observation is true; correct it only if the data says otherwise.\n"
    "3. Check whether the data is enough to answer.\n"
    "4. If it is, answer with what the data shows. If not, say what's missing. "
    "Call any guess a guess."
)

# Set-up -> (the system message, the tag in the file name). "system" is the one used when no
# set-up option is given.
SETUPS: dict[str, tuple[str | None, str]] = {
    "system": (SYSTEM, ""),
    "no-system": (None, "-nosys"),
    "premise": (SYSTEM + " " + PREMISE, "-premise"),
    "premise-only": (PREMISE, "-premiseonly"),
    "steps": (STEPS, "-steps"),
}

# The questions as written in cases/C0*.md (Oct 13 and Oct 15); C01, C02, C03, C05 proposed by
# Claude and validated by the author on Oct 20.
QUESTIONS = {
    "C01": "Why are North rentals down on last year since May?",
    "C02": "Why did West revenue fall from April 2026?",
    "C03": "Why did East contract revenue fall from late January 2026?",
    "C04": "Why is there a drop in Tidesend on the week of 2026-06-15?",
    "C05": "Why is the South's average daily rate lower this summer than last summer? "
    "We didn't cut prices.",
    "C06": "Why did North revenue drop on the week of 2026-07-13?",
    "C07": "What happened between 2025-11-10 and 2025-11-24 at D11 Lowen Quay?",
    "C08": "Why did rentals drop at Hollin Cross in October 2025?",
    "C09": "Why did walk-in rentals drop at the counter, East region, July 2026?",
}


@dataclass(frozen=True)
class Plan:
    """What one command runs.

    Attributes:
        models: the models to ask, in order.
        cases: the cases to ask, in order.
        system: the system message, or None for no system message.
        reasoning: Mistral's reasoning_effort, or None to leave it unset.
        data: which data block is read: "" for <case>-data.txt, "computed" for
            <case>-data-computed.txt.
        tag: what follows the model in the name of the answer file.
    """

    models: list[str]
    cases: list[str]
    system: str | None
    reasoning: str | None
    data: str
    tag: str

    def data_name(self, case: str) -> str:
        """Return the name of the data block of a case, in cases/data/."""
        return f"{case}-data{'-' + self.data if self.data else ''}.txt"

    def answer_name(self, case: str, model: str) -> str:
        """Return the name of the file that holds one answer."""
        return f"{case}-{model}{self.tag}.json"


@dataclass(frozen=True)
class Answer:
    """What a model returned: the text, the tokens billed and why it stopped."""

    text: str
    prompt_tokens: int
    completion_tokens: int
    stop: str


def build_parser() -> argparse.ArgumentParser:
    """Return the parser of the command line. The docstring of this file is its help text."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "names",
        nargs="*",
        metavar="model-or-case",
        help='the large model to run next to Mistral Small, and any cases; or the word "models"',
    )
    parser.add_argument("--models", help="a list of models, with commas, in place of the pair")
    setup = parser.add_mutually_exclusive_group()
    for name in SETUPS:
        if name != "system":
            setup.add_argument(f"--{name}", dest="setup", action="store_const", const=name)
    parser.add_argument("--reasoning", choices=["none", "high"])
    parser.add_argument("--data", default="", help="the variant of the data block")
    parser.add_argument("--tag", default="", help="a word added to the names of the answer files")
    parser.set_defaults(setup="system")
    return parser


def choose_models(positional: list[str], listed: str | None) -> list[str]:
    """Decide which models to ask.

    Args:
        positional: the words of the command that are not cases.
        listed: the value of --models, or None.

    Returns:
        The list given with --models, or Mistral Small and the model named.

    Raises:
        ValueError: when the command names no model, or more than one outside --models.
    """
    if len(positional) > 1:
        raise ValueError(f"expected one model, got {positional} (cases are C01 to C09)")
    if listed:
        # Commands written before Nov 15 gave a first word even with --models; it was never used.
        if positional:
            print(f"note: {positional[0]!r} is not used, --models decides", file=sys.stderr)
        return listed.split(",")
    if not positional:
        raise ValueError("name the large model to run next to Mistral Small, or pass --models")
    return [SMALL, positional[0]]


def plan_from(argv: list[str]) -> Plan:
    """Turn the words of a command into what it runs.

    Raises:
        ValueError: when the command names no model, or more than one outside --models.
    """
    args = build_parser().parse_intermixed_args(argv)
    cases = [name for name in args.names if name in QUESTIONS]
    system, tag = SETUPS[args.setup]
    if args.reasoning:
        tag += f"-r{args.reasoning}"
    if args.data:
        tag += f"-{args.data}"
    if args.tag:
        tag += f"-{args.tag}"
    return Plan(
        models=choose_models([n for n in args.names if n not in QUESTIONS], args.models),
        cases=cases or list(QUESTIONS),
        system=system,
        reasoning=args.reasoning,
        data=args.data,
        tag=tag,
    )


def user_message(data: str, question: str) -> str:
    """Return the user message: the data block, then the question."""
    return f"data:{data}, question:{question}"


@functools.cache
def mistral_client() -> Any:  # noqa: ANN401 (the library is imported only when a call is made)
    """Return the Mistral client, built on first use from MISTRAL_API_KEY."""
    from mistralai.client import Mistral

    return Mistral(api_key=os.environ.get("MISTRAL_API_KEY", ""))


@functools.cache
def claude_client() -> Any:  # noqa: ANN401 (the library is imported only when a call is made)
    """Return the Anthropic client, built on first use from ANTHROPIC_API_KEY."""
    from anthropic import Anthropic

    return Anthropic()


def ask_mistral(model: str, system: str | None, user: str, reasoning: str | None) -> Answer:
    """Ask a Mistral model at temperature 0.

    Args:
        model: the model's name.
        system: the system message, or None.
        user: the user message.
        reasoning: reasoning_effort, or None to leave it unset (Oct 20: the docs give no default).
    """
    messages = [{"role": "user", "content": user}]
    if system:
        messages.insert(0, {"role": "system", "content": system})
    extra = {"reasoning_effort": reasoning} if reasoning else {}
    # top_p=1: Large 4 requires it with temperature 0 (no effect under greedy sampling).
    result = mistral_client().chat.complete(
        model=model, temperature=0, top_p=1, messages=messages, **extra
    )
    text = result.choices[0].message.content
    if not isinstance(text, str):
        # Reasoning answers come in chunks: keep the text, drop the thinking.
        chunks = [getattr(c, "text", "") for c in text if getattr(c, "type", "") == "text"]
        text = "".join(chunks)
    usage = result.usage
    return Answer(
        text, usage.prompt_tokens, usage.completion_tokens, str(result.choices[0].finish_reason)
    )


def ask_claude(model: str, system: str | None, user: str) -> Answer:
    """Ask a Claude model at its own defaults.

    Written by Claude Code at the author's request (Oct 20). Claude models take no temperature
    setting and think before answering (adaptive thinking, the model's default effort). No
    server-side fallback, so every answer comes from the model named; a refusal shows in stop.
    """
    request = {
        "model": model,
        "max_tokens": MAX_TOKENS_CLAUDE,
        "messages": [{"role": "user", "content": user}],
    }
    if system:
        request["system"] = system
    result = claude_client().messages.create(**request)
    text = "".join(block.text for block in result.content if block.type == "text")
    return Answer(
        text, result.usage.input_tokens, result.usage.output_tokens, str(result.stop_reason)
    )


def ask(model: str, plan: Plan, user: str) -> Answer:
    """Ask one model, by the library its name calls for."""
    if model.startswith("claude-"):
        return ask_claude(model, plan.system, user)
    return ask_mistral(model, plan.system, user, plan.reasoning)


def run(plan: Plan, folder: Path) -> None:
    """Ask every case to every model, save each answer in the folder and print it."""
    folder.mkdir(parents=True, exist_ok=True)
    for case in plan.cases:
        question = QUESTIONS[case]
        data = (HERE / "cases" / "data" / plan.data_name(case)).read_text()
        for model in plan.models:
            start = time.perf_counter()
            answer = ask(model, plan, user_message(data, question))
            seconds = time.perf_counter() - start
            record = {
                "case": case,
                "model": model,
                "question": question,
                "system": plan.system,
                "prompt_tokens": answer.prompt_tokens,
                "completion_tokens": answer.completion_tokens,
                "stop": answer.stop,
                "seconds": round(seconds, 2),
                "answer": answer.text,
            }
            path = folder / plan.answer_name(case, model)
            path.write_text(json.dumps(record, indent=1, ensure_ascii=False))
            print(
                f"\n=== {case} · {model} · {answer.prompt_tokens}+{answer.completion_tokens} "
                f"tokens · {seconds:.1f} s\n{answer.text}"
            )


def main(argv: list[str] | None = None) -> None:
    """Run the command. With no word at all, print how to use it."""
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        sys.exit(__doc__)
    if argv == ["models"]:
        for model in mistral_client().models.list().data:
            print(model.id)
        return
    try:
        plan = plan_from(argv)
    except ValueError as error:
        sys.exit(f"run_cases.py: {error}")
    run(plan, HERE / "results" / date.today().isoformat())


if __name__ == "__main__":
    main()
