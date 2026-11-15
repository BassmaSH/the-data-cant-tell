"""Tests for grading/2026-10-20/combine.py, which produces every published table. No API call.

    pytest tests/test_combine.py

The first half tests the rules on small examples. The second half checks the files of the repo:
that the grading files hold the number of rows they should, that their own totals add up, and that
the tables in README.md and NOTEBOOK.md are the ones the script prints.

Code written by Claude Code on Nov 15, 2026, for the author.
"""

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "grading" / "2026-10-20"))

import combine  # noqa: E402
from combine import COMPUTED, Verdict  # noqa: E402

README = (ROOT / "README.md").read_text()
NOTEBOOK = (ROOT / "NOTEBOOK.md").read_text()
VERDICTS = combine.load_verdicts()
CELLS = combine.build_cells(VERDICTS)

# The one published figure that the script does not reproduce to the cent. The README and the
# notebook say $3.34; the token counts give $3.347. grading/2026-10-20/computed.md explains it.
KNOWN_DIFFERENCE = ("$3.35", "$3.34")


def verdict(marks: str) -> Verdict:
    """Build a verdict from four letters, for example "nyyy"."""
    values = tuple(mark == "y" for mark in marks)
    return Verdict("a-model", "C01", "steps", values, values)


def plain(line: str) -> str:
    """Return a table line without bold marks and without spaces around the cell bars."""
    return re.sub(r"\s*\|\s*", "|", line.replace("*", "")).strip()


# --- the rules, on small examples ---


def test_a_row_gives_the_four_verdicts_in_order():
    row = combine.parse_row("| C04 | steps | n | y | y | n | the reason |", "a-model")
    assert row == Verdict(
        "a-model", "C04", "steps", (False, True, True, False), (False,) + (True, True, False)
    )


def test_a_changed_cell_keeps_the_graders_verdict_and_counts_the_new_one():
    row = combine.parse_row("| C02 | system + sentence | n | y | n → y | y | why |", "a-model")
    assert row.graded == (False, True, False, True)
    assert row.counted == (False, True, True, True)
    assert not verdict("nyny").fully_right and row.fully_right


def test_the_short_set_up_name_and_a_bold_case_are_read():
    row = combine.parse_row("| **C05 tot** | system | y | y | y | n | x | y | z |", "a-model")
    assert (row.case, row.setup) == ("C05 tot", "system message")


def test_lines_that_are_not_verdict_rows_are_skipped():
    for line in (
        "| case | set-up | invented | shows | figures | found | reason |",
        "|---|---|---|---|---|---|---|",
        "| system message | 0 | 10 | 8 | 9 |",
        "| steps | 0 | 8 | 6 as graded, 7 as counted | 7 |",
        "| C02 | system + sentence | figures | n | y | Rule C. The only fault |",
        "| C01 | steps | n | y | maybe | y | a cell that is not a verdict |",
        "Graded once, with the brief's final calibration.",
        "",
    ):
        assert combine.parse_row(line, "a-model") is None, line


def test_fully_right_needs_all_four():
    assert verdict("nyyy").fully_right
    for marks in ("yyyy", "nnyy", "nyny", "nyyn"):
        assert not verdict(marks).fully_right, marks


def test_a_file_with_two_models_is_read_section_by_section():
    text = "\n".join(
        [
            "intro",
            "## one",
            "| C01 | none | n | y | y | y | r |",
            "### totals of one",
            "| C02 | none | y | y | y | y | r |",
            "## two",
            "| C01 | none | n | n | n | n | r |",
            "## What stands out",
            "| C09 | none | y | y | y | y | not a row of model two |",
        ]
    )
    rows = combine.parse_file(text, ["one", "two"])
    assert [(r.model, r.case) for r in rows] == [("one", "C01"), ("one", "C02"), ("two", "C01")]


def test_cost_is_tokens_times_the_price_per_million():
    records = [
        {"prompt_tokens": 1_000_000, "completion_tokens": 0},
        {"prompt_tokens": 0, "completion_tokens": 500_000},
    ]
    assert combine.cost_usd(records, (2, 10)) == 2 + 5


def test_a_cell_is_summed_up_from_its_verdicts_and_records():
    verdicts = [verdict("nyyy"), verdict("nyyy"), verdict("yyny"), verdict("nnyy")]
    records = [
        {"prompt_tokens": 1000, "completion_tokens": 100, "seconds": seconds}
        for seconds in (4.0, 1.0, 3.0, 10.0)
    ]
    cell = combine.summarise(verdicts, records, (1, 10))
    assert cell.counts == (1, 3, 3, 4)
    assert cell.fully_right == 2
    assert (cell.answers, cell.files) == (4, 4)
    # Four answers cost 4 x (1000 x 1 + 100 x 10) / 1e6 = 0.008 dollars.
    assert math.isclose(cell.cost_per_1000_answers, 2.0)
    assert math.isclose(cell.cost_per_1000_fully_right, 4.0)
    # An even number of answers: the median is halfway between the two middle ones.
    assert (cell.median_seconds, cell.max_seconds) == (3.5, 10.0)


def test_no_fully_right_answer_gives_no_cost_per_right_answer():
    records = [{"prompt_tokens": 1, "completion_tokens": 1, "seconds": 1.0}]
    cell = combine.summarise([verdict("yyyy")], records, (1, 1))
    assert math.isnan(cell.cost_per_1000_fully_right)
    assert "$nan per 1,000 right" in combine.cell_line(cell)


def test_answer_files_follow_the_names_run_cases_gives():
    names = [p.name for p in combine.answer_files("mistral-large-4-0 (reasoning high)", "steps")]
    assert names[0] == "C01-mistral-large-4-0-steps-rhigh.json"
    assert names[-2:] == [
        "C05-mistral-large-4-0-steps-rhigh.json",
        "C05-mistral-large-4-0-steps-rhigh-categories.json",
    ]
    names = [p.name for p in combine.answer_files("mistral-large-4-0 (reasoning off)", COMPUTED)]
    assert names[0] == "C01-mistral-large-4-0-rnone-computed.json"
    assert names[-1] == "C05-mistral-large-4-0-rnone-categories-computed.json"


def test_run_1_answers_come_from_the_folder_of_oct_15():
    paths = combine.answer_files("mistral-small-2603", "system message")
    by_case = {p.name[:3]: p for p in paths if "categories" not in p.name}
    assert by_case["C06"].name == "C06-mistral-small-2603-v2.json"
    assert {c: by_case[c].parent.name for c in ("C01", "C04", "C06", "C09")} == {
        "C01": "2026-10-20",
        "C04": "2026-10-15",
        "C06": "2026-10-15",
        "C09": "2026-10-15",
    }
    # Only the system message: the other set-ups were all run on Oct 20.
    assert {p.parent.name for p in combine.answer_files("mistral-small-2603", "steps")} == {
        "2026-10-20"
    }


# --- the files of the repo ---


def test_every_grading_file_holds_the_rows_it_should():
    counts = {}
    for name, models in combine.FILES.items():
        rows = combine.parse_file((combine.GRADING / name).read_text(), models)
        counts[name] = [sum(r.model == m for r in rows) for m in models]
    assert counts == {
        "large4-none.md": [40],
        "large4-high.md": [40],
        "haiku.md": [40],
        "sonnet.md": [40],
        "opus.md": [40],
        "mistral-2512-small.md": [50, 50],
        "computed.md": [10, 10],
    }


def test_every_cell_has_ten_verdicts_and_ten_answer_files_that_exist():
    assert len(CELLS) == 5 * 4 + 2 * 5 + 2
    for (model, setup), cell in CELLS.items():
        assert (cell.answers, cell.files) == (10, 10), (model, setup)
        files = combine.answer_files(model, setup)
        assert len(set(files)) == 10 and all(f.exists() for f in files), (model, setup)


def test_no_answer_file_is_counted_in_two_cells():
    files = [f for model, setup in CELLS for f in combine.answer_files(model, setup)]
    assert len(files) == len(set(files)) == 320


def test_exactly_two_verdicts_were_changed_after_grading_and_each_file_says_why():
    changed = [(v.model, v.case, v.setup) for v in VERDICTS if v.graded != v.counted]
    assert changed == [
        ("mistral-large-4-0 (reasoning high)", "C02", "system + sentence"),
        ("mistral-small-2603", "C08", "steps"),
    ]
    for v in VERDICTS:
        if v.graded != v.counted:
            differs = [
                m for m, g, c in zip(combine.MEASURES, v.graded, v.counted, strict=True) if g != c
            ]
            assert differs == ["figures"]
    for name in ("large4-high.md", "mistral-2512-small.md"):
        text = (combine.GRADING / name).read_text()
        assert "Verdicts changed after grading" in text and "Rule C" in text, name


def totals_in_file(text: str) -> list[tuple[str, list[int], list[int]]]:
    """Read a grading file's own totals rows: (set-up, counts as graded, counts as counted)."""
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0] not in combine.SETUPS:
            continue
        # A cell is "9", "9 / 10" or "9 as graded, 10 as counted".
        graded = [int(re.match(r"\d+", cell)[0]) for cell in cells[1:]]
        changed = [re.search(r"(\d+) as counted", cell) for cell in cells[1:]]
        counted = [int(c[1]) if c else g for c, g in zip(changed, graded, strict=True)]
        rows.append((cells[0], graded, counted))
    return rows


def test_the_totals_written_in_each_grading_file_are_the_sums_of_its_rows():
    for name, models in combine.FILES.items():
        if name == "computed.md":
            continue
        text = (combine.GRADING / name).read_text()
        rows = combine.parse_file(text, models)
        written = totals_in_file(text)
        setups_per_model = len(written) // len(models)
        assert setups_per_model in (4, 5), name
        for i, (setup, graded, counted) in enumerate(written):
            model = models[i // setups_per_model]
            mine = [r for r in rows if r.model == model and r.setup == setup]
            assert graded == [sum(r.graded[k] for r in mine) for k in range(4)], (name, setup)
            assert counted == [sum(r.counted[k] for r in mine) for k in range(4)], (name, setup)


def test_the_computed_figures_totals_are_the_notebooks():
    """NOTEBOOK.md, run 9: Small 2, 7, 8, 6 and 4 fully right; Large 4 0, 9, 10, 10 and 9."""
    small = CELLS["mistral-small-2603", COMPUTED]
    large = CELLS["mistral-large-4-0 (reasoning off)", COMPUTED]
    assert (small.counts, small.fully_right) == ((2, 7, 8, 6), 4)
    assert (large.counts, large.fully_right) == ((0, 9, 10, 10), 9)
    assert "| **Small, with computed figures** | 2 | 7 | 8 | 6 | 4 |" in NOTEBOOK
    assert (
        "| **Large 4 reasoning off, with computed figures** | **0** | 9 | **10** | **10** | **9** |"
        in NOTEBOOK
    )


def test_the_notebooks_combined_table_is_the_one_printed():
    notebook_lines = {plain(line) for line in NOTEBOOK.splitlines()}
    printed = combine.main_table(CELLS, combine.SETUPS)[2:]
    assert len(printed) == 30
    for line in printed:
        assert plain(line.replace(" (10 files)", "")) in notebook_lines, line


def test_the_readmes_table_of_fully_right_answers_is_the_one_printed():
    readme_lines = {plain(line) for line in README.splitlines()}
    for line in combine.fully_right_table(CELLS):
        assert plain(line) in readme_lines, line


def test_the_readmes_table_of_cost_and_speed_is_the_one_printed():
    readme_lines = {plain(line) for line in README.splitlines()}
    different = []
    for line in combine.best_setup_table(CELLS)[2:]:
        if plain(line) not in readme_lines:
            different.append(line)
    assert len(different) == 1, different
    printed, published = KNOWN_DIFFERENCE
    assert plain(different[0].replace(printed, published)) in readme_lines


def test_the_counts_quoted_in_the_readme_are_the_ones_printed():
    counts = "\n".join(combine.quoted_counts(CELLS))
    assert "answers graded: 320" in counts and "about 320 answers" in README
    assert "mistral-small-2603 6 of 10, mistral-large-2512 8 of 10" in counts
    assert "invented a cause in 8 answers out of 10, Mistral Small in 6" in README
    assert "mistral-small-2603 1 of 10, mistral-large-2512 1 of 10" in counts
    assert "Claude answers with an invented cause: 0 of 120" in counts
    assert "never invented a cause, in 120 answers" in README
    assert counts.count("27 of 40") == 2 and "both got 27 of 40 fully right" in README
