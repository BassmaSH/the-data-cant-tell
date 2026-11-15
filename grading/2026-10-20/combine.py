"""Rebuild the published tables from the grading files and the saved answers. No API call, no key.

    python grading/2026-10-20/combine.py

It prints, in this order:

1. one line per model and set-up: the four verdict counts, the fully right answers, the cost and
   the time (the table of NOTEBOOK.md, "Runs 6 and 7 graded");
2. the same line for the computed-figures run (NOTEBOOK.md, run 9);
3. the README's table of fully right answers;
4. the README's table of cost and speed;
5. the counts the README quotes in its text.

The verdicts are read from the .md files of this folder, one row per answer. The cost and the time
are computed from the token counts and the seconds saved with each answer in results/. Standard
library only.

Code written by Claude Code on Oct 20, 2026, for the author; reorganised on Nov 15, 2026 (one
function per job, and the two verdicts changed after grading are read from the grading files).
"""

import json
import re
import statistics
from dataclasses import dataclass
from pathlib import Path

GRADING = Path(__file__).parent
RESULTS = GRADING.parent.parent / "results"

MEASURES = ("invented", "shows", "figures", "found")
COMPUTED = "computed figures"
SETUPS = ("none", "system message", "system + sentence", "sentence alone", "steps")

# Grading file -> the models it grades. A file with several models has one "## <model>" section
# for each. The order decides the order of the lines printed.
FILES = {
    "large4-none.md": ["mistral-large-4-0 (reasoning off)"],
    "large4-high.md": ["mistral-large-4-0 (reasoning high)"],
    "haiku.md": ["claude-haiku-5-5"],
    "sonnet.md": ["claude-sonnet-5-5"],
    "opus.md": ["claude-opus-5-5"],
    "mistral-2512-small.md": ["mistral-small-2603", "mistral-large-2512"],
    "computed.md": ["mistral-small-2603", "mistral-large-4-0 (reasoning off)"],
}

# List prices in USD per million tokens (input, output). Sources and dates: README, "Results".
PRICE = {
    "mistral-small-2603": (0.15, 0.60),
    "mistral-large-2512": (0.50, 1.50),
    "mistral-large-4-0": (1.36, 4.18),
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2, 10),
    "claude-opus-5-5": (4, 20),
}

# How run_cases.py names an answer file: <case>-<model><set-up><reasoning><data>.json
SETUP_TAG = {
    "none": "-nosys",
    "system message": "",
    "system + sentence": "-premise",
    "sentence alone": "-premiseonly",
    "steps": "-steps",
    COMPUTED: "",
}
REASONING_TAG = {"reasoning off": "-rnone", "reasoning high": "-rhigh"}
CASE_ORDER = ("C01", "C02", "C03", "C04", "C06", "C07", "C08", "C09", "C05")
CASE_WITH_TWO_VERSIONS = "C05"  # totals only, and with the category breakdown

# Run 1 (Oct 15): these cases, on these two models, with the system message. Their answers are
# in the folder of that day. C06 was run twice that day; the graded answers are the second run's,
# on the data that names the region (saved as -v2).
RUN_FOLDER = "2026-10-20"
RUN_1_FOLDER = "2026-10-15"
RUN_1_MODELS = ("mistral-small-2603", "mistral-large-2512")
RUN_1_CASES = ("C04", "C06", "C07", "C08", "C09")
RUN_1_SECOND_VERSION = {"C06": "-v2"}

# A verdict cell is "y" or "n". "n → y" is a verdict changed after grading: the grader's verdict,
# then the one counted in the published tables. The grading file says why, next to the row.
CELL = re.compile(r"([yn])(?: → ([yn]))?")
CASE = re.compile(r"C0\d.*")
SHORT_SETUP_NAMES = {"system": "system message"}

# The README's two tables: its labels, in its order.
README_MODELS = {
    "Mistral Small 2603": "mistral-small-2603",
    "Mistral Large 3": "mistral-large-2512",
    "Mistral Large 4, reasoning off": "mistral-large-4-0 (reasoning off)",
    "Mistral Large 4, reasoning high": "mistral-large-4-0 (reasoning high)",
    "Claude Haiku 5.5": "claude-haiku-5-5",
    "Claude Sonnet 5.5": "claude-sonnet-5-5",
    "Claude Opus 5.5": "claude-opus-5-5",
}
README_SETUPS = {
    "none": "none",
    "system message": "system message",
    "+ my sentence": "system + sentence",
    "steps": "steps",
    COMPUTED: COMPUTED,
}
README_BEST_SETUP = {
    "Mistral Small, steps": ("mistral-small-2603", "steps"),
    "Mistral Large 3, system message": ("mistral-large-2512", "system message"),
    "Mistral Large 4 reasoning off, computed figures": (
        "mistral-large-4-0 (reasoning off)",
        COMPUTED,
    ),
    "Mistral Large 4 reasoning high, + my sentence": (
        "mistral-large-4-0 (reasoning high)",
        "system + sentence",
    ),
    "Claude Haiku, system message": ("claude-haiku-5-5", "system message"),
    "Claude Sonnet, system message": ("claude-sonnet-5-5", "system message"),
    "Claude Opus, system message": ("claude-opus-5-5", "system message"),
}
CLAUDE_MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5")
SHARED_SETUPS = ("none", "system message", "system + sentence", "steps")

HEADER = (
    "| model | set-up | n | invented | shows | figures | found | fully right "
    "| cost per 1,000 answers | cost per fully right answer | seconds (median, max) |"
)
RULE = "|---|---|---|---|---|---|---|---|---|---|---|"


@dataclass(frozen=True)
class Verdict:
    """One graded answer. The four booleans follow MEASURES.

    Attributes:
        graded: what the grader wrote.
        counted: what the published tables count. It differs from graded only in a cell
            written "n → y" in the grading file.
    """

    model: str
    case: str
    setup: str
    graded: tuple[bool, ...]
    counted: tuple[bool, ...]

    @property
    def fully_right(self) -> bool:
        """Not invented, shows what the data shows, figures right, cause found."""
        invented, shows, figures, found = self.counted
        return not invented and shows and figures and found


@dataclass(frozen=True)
class Cell:
    """The answers of one model in one set-up, summed up. Costs are in USD."""

    model: str
    setup: str
    answers: int
    files: int
    counts: tuple[int, ...]
    fully_right: int
    cost_per_1000_answers: float
    cost_per_1000_fully_right: float
    median_seconds: float
    max_seconds: float


def parse_row(line: str, model: str) -> Verdict | None:
    """Read one line of a grading file.

    Returns:
        The verdict, or None when the line is not a verdict row (text, a header, a totals row).
    """
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) < 2 + len(MEASURES):
        return None
    case = cells[0].replace("*", "").strip()
    marks = [CELL.fullmatch(cell) for cell in cells[2 : 2 + len(MEASURES)]]
    if not CASE.fullmatch(case) or not all(marks):
        return None
    return Verdict(
        model=model,
        case=case,
        setup=SHORT_SETUP_NAMES.get(cells[1], cells[1]),
        graded=tuple(mark[1] == "y" for mark in marks),
        counted=tuple((mark[2] or mark[1]) == "y" for mark in marks),
    )


def section(text: str, heading: str) -> str:
    """Return the lines of a grading file under "## <heading>", up to the next "## " heading."""
    lines = text.splitlines()
    start = lines.index(f"## {heading}") + 1
    rest = lines[start:]
    end = next((i for i, line in enumerate(rest) if line.startswith("## ")), len(rest))
    return "\n".join(rest[:end])


def parse_file(text: str, models: list[str]) -> list[Verdict]:
    """Read every verdict row of one grading file, in the order of its models."""
    parts = [text] if len(models) == 1 else [section(text, model) for model in models]
    verdicts = []
    for part, model in zip(parts, models, strict=True):
        rows = (parse_row(line, model) for line in part.splitlines())
        verdicts += [row for row in rows if row]
    return verdicts


def load_verdicts() -> list[Verdict]:
    """Read every grading file of this folder."""
    verdicts = []
    for name, models in FILES.items():
        verdicts += parse_file((GRADING / name).read_text(), models)
    return verdicts


def answer_files(model: str, setup: str) -> list[Path]:
    """List the saved answers of one model in one set-up: ten files, C05 in two versions.

    Args:
        model: as in FILES, for example "mistral-large-4-0 (reasoning off)".
        setup: one of SETUPS, or COMPUTED.
    """
    name = model.split(" ")[0]
    reasoning = "".join(tag for label, tag in REASONING_TAG.items() if label in model)
    tag = SETUP_TAG[setup] + reasoning
    end = "-computed" if setup == COMPUTED else ""
    from_run_1 = setup == "system message" and name in RUN_1_MODELS
    paths = []
    for case in CASE_ORDER:
        if from_run_1 and case in RUN_1_CASES:
            version = RUN_1_SECOND_VERSION.get(case, "")
            paths.append(RESULTS / RUN_1_FOLDER / f"{case}-{name}{version}.json")
            continue
        paths.append(RESULTS / RUN_FOLDER / f"{case}-{name}{tag}{end}.json")
        if case == CASE_WITH_TWO_VERSIONS:
            paths.append(RESULTS / RUN_FOLDER / f"{case}-{name}{tag}-categories{end}.json")
    return paths


def cost_usd(records: list[dict], price: tuple[float, float]) -> float:
    """Return the cost of some answers at a list price per million tokens (input, output)."""
    price_in, price_out = price
    tokens = sum(
        r["prompt_tokens"] * price_in + r["completion_tokens"] * price_out for r in records
    )
    return tokens / 1e6


def summarise(verdicts: list[Verdict], records: list[dict], price: tuple[float, float]) -> Cell:
    """Sum up the answers of one model in one set-up.

    Args:
        verdicts: the graded answers of the cell.
        records: the saved answers of the cell, with their token counts and seconds.
        price: list price in USD per million tokens (input, output).
    """
    fully_right = sum(v.fully_right for v in verdicts)
    cost = cost_usd(records, price)
    seconds = [r["seconds"] for r in records]
    return Cell(
        model=verdicts[0].model,
        setup=verdicts[0].setup,
        answers=len(verdicts),
        files=len(records),
        counts=tuple(sum(v.counted[i] for v in verdicts) for i in range(len(MEASURES))),
        fully_right=fully_right,
        cost_per_1000_answers=cost / len(records) * 1000,
        # With no fully right answer there is no such cost: printed as "nan".
        cost_per_1000_fully_right=cost / fully_right * 1000 if fully_right else float("nan"),
        median_seconds=statistics.median(seconds),
        max_seconds=max(seconds),
    )


def build_cells(verdicts: list[Verdict]) -> dict[tuple[str, str], Cell]:
    """Sum up every (model, set-up) that has verdicts, reading its answer files."""
    groups: dict[tuple[str, str], list[Verdict]] = {}
    for verdict in verdicts:
        groups.setdefault((verdict.model, verdict.setup), []).append(verdict)
    cells = {}
    for (model, setup), group in groups.items():
        records = [json.loads(path.read_text()) for path in answer_files(model, setup)]
        cells[model, setup] = summarise(group, records, PRICE[model.split(" ")[0]])
    return cells


def cell_line(cell: Cell) -> str:
    """Return one line of the main table."""
    counts = " | ".join(str(count) for count in cell.counts)
    return (
        f"| {cell.model} | {cell.setup} | {cell.answers} ({cell.files} files) | {counts} "
        f"| {cell.fully_right} | ${cell.cost_per_1000_answers:.2f} "
        f"| ${cell.cost_per_1000_fully_right:.2f} per 1,000 right "
        f"| {cell.median_seconds:.1f}, {cell.max_seconds:.1f} |"
    )


def main_table(cells: dict[tuple[str, str], Cell], setups: tuple[str, ...]) -> list[str]:
    """Return the lines of the main table for these set-ups, model by model."""
    models = list(dict.fromkeys(model for model, _ in cells))
    keys = [(model, setup) for model in models for setup in setups]
    return [HEADER, RULE] + [cell_line(cells[key]) for key in keys if key in cells]


def fully_right_table(cells: dict[tuple[str, str], Cell]) -> list[str]:
    """Return the README's table: fully right answers out of 10, by model and set-up."""
    lines = [
        "| model | " + " | ".join(README_SETUPS) + " |",
        "|---" * (len(README_SETUPS) + 1) + "|",
    ]
    for label, model in README_MODELS.items():
        scores = [cells.get((model, setup)) for setup in README_SETUPS.values()]
        lines.append(
            f"| {label} | " + " | ".join(str(c.fully_right) if c else "—" for c in scores) + " |"
        )
    return lines


def best_setup_table(cells: dict[tuple[str, str], Cell]) -> list[str]:
    """Return the README's table: cost and speed of each model's best set-up."""
    lines = [
        "| model, best set-up | fully right | cost per 1,000 answers "
        "| cost per 1,000 fully right answers | seconds per answer (median) |",
        "|---|---|---|---|---|",
    ]
    for label, key in README_BEST_SETUP.items():
        cell = cells[key]
        lines.append(
            f"| {label} | {cell.fully_right} | ${cell.cost_per_1000_answers:.2f} "
            f"| ${cell.cost_per_1000_fully_right:.2f} | {cell.median_seconds:.1f} |"
        )
    return lines


def quoted_counts(cells: dict[tuple[str, str], Cell]) -> list[str]:
    """Return the counts the README quotes in its text, one per line."""
    invented = MEASURES.index("invented")
    no_message = {m: cells[m, "none"].counts[invented] for m in RUN_1_MODELS}
    message = {m: cells[m, "system message"].counts[invented] for m in RUN_1_MODELS}
    claude = [cells[m, s] for m in CLAUDE_MODELS for s in SHARED_SETUPS]
    lines = [
        f"- answers graded: {sum(cell.answers for cell in cells.values())}",
        "- answers with an invented cause, no system message: "
        + ", ".join(f"{m} {n} of 10" for m, n in no_message.items()),
        "- the same with the system message: "
        + ", ".join(f"{m} {n} of 10" for m, n in message.items()),
        f"- Claude answers with an invented cause: {sum(c.counts[invented] for c in claude)} "
        f"of {sum(c.answers for c in claude)}",
    ]
    for model in ("mistral-large-4-0 (reasoning high)", "claude-opus-5-5"):
        shared = [cells[model, setup] for setup in SHARED_SETUPS]
        lines.append(
            f"- fully right over the four set-ups every model ran, {model}: "
            f"{sum(c.fully_right for c in shared)} of {sum(c.answers for c in shared)}"
        )
    return lines


def main() -> None:
    """Print every table."""
    cells = build_cells(load_verdicts())
    print("\n".join(main_table(cells, SETUPS)))
    print(
        "\nThe computed-figures run (verdicts transcribed from NOTEBOOK.md, run 9: "
        "see computed.md):\n"
    )
    print("\n".join(main_table(cells, (COMPUTED,))))
    print("\nFully right answers out of 10, as in the README's results table:\n")
    print("\n".join(fully_right_table(cells)))
    print("\nCost and speed of each model's best set-up, as in the README:\n")
    print("\n".join(best_setup_table(cells)))
    print("\nCounts quoted in the README's text:\n")
    print("\n".join(quoted_counts(cells)))


if __name__ == "__main__":
    main()
