"""Tests for the data blocks in cases/data/: each one follows from data/company.sqlite. No API call.

    pytest tests/test_case_data.py

Three checks on the files of the repo. The blocks of C01, C02, C03 and C05 are the ones
make_case_data.py builds. Every "-computed" block is the one make_computed.py builds. The blocks of
C04 and C06 to C09 have no script: every figure of their tables is compared with the database.

Code written by Claude Code on Nov 15, 2026, for the author.
"""

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
BLOCKS = ROOT / "cases" / "data"
sys.path.insert(0, str(BLOCKS))

import make_case_data  # noqa: E402
import make_computed  # noqa: E402

DATABASE = sqlite3.connect(f"file:{ROOT / 'data' / 'company.sqlite'}?mode=ro", uri=True)

# Every table of the blocks that no script builds, in the order of the block: what one cell is, as
# a query that takes the week and the column's name. Depot columns start with the depot id; channel
# columns are the channel.
BY_DEPOT = "SELECT SUM({measure}) FROM weekly_rentals WHERE week_start = ? AND depot_id = ?"
HAND_MADE = {
    "C04": [(BY_DEPOT.format(measure="on_rent_days"), "depot", "days")],
    "C06": [(BY_DEPOT.format(measure="rental_revenue_cents"), "depot", "euros")],
    "C08": [(BY_DEPOT.format(measure="on_rent_days"), "depot", "days")],
    "C07": [
        (
            "SELECT SUM(on_rent_days) FROM weekly_rentals WHERE week_start = ? AND channel = ? "
            "AND depot_id = 'D11' AND category_id = 'PWL'",
            "channel",
            "days",
        ),
        (BY_DEPOT.format(measure="on_rent_days") + " AND category_id = 'PWL'", "depot", "days"),
    ],
    "C09": [
        (
            "SELECT SUM(on_rent_days) FROM weekly_rentals JOIN depots USING (depot_id) "
            "WHERE week_start = ? AND channel = ? AND region_id = 'R3'",
            "channel",
            "days",
        )
    ],
}


def tables_of(case: str) -> list[tuple[list[str], dict[str, list]]]:
    """Return the columns and the rows of every table of a case's block."""
    text = (BLOCKS / f"{case}-data.txt").read_text()
    return list(make_computed.tables(text).values())


# --- the rules, on small examples ---


def test_a_cell_is_a_number_a_dash_or_text():
    assert make_computed.cell("1,234") == 1234.0
    assert make_computed.cell("34.05") == 34.05
    assert make_computed.cell("-") is None
    assert make_computed.cell("2026-07-13") == "2026-07-13"


def test_a_table_is_read_with_the_line_above_it_as_its_name():
    text = "Title of the table\nweek_start | D01 | D02\n2026-01-05 | 1,000 | -\n\nNotes:\n- none"
    assert make_computed.tables(text) == {
        "Title of the table": (["week_start", "D01", "D02"], {"2026-01-05": [1000.0, None]})
    }


def test_the_mean_leaves_out_weeks_without_rows():
    assert make_computed.mean([10, None, 20]) == 15
    assert make_computed.mean([None]) is None


def test_a_change_is_signed_and_relative_to_the_first_figure():
    assert make_computed.pct(200, 150) == "-25.0 %"
    assert make_computed.pct(34.05, 29.82) == "-12.4 %"
    assert make_computed.pct(100, 110) == "+10.0 %"


def test_a_span_of_weeks_includes_both_ends_and_counts_the_weeks_with_a_figure():
    rows = {"2026-01-05": [10], "2026-01-12": [None], "2026-01-19": [30], "2026-01-26": [50]}
    spans = [("first three", "2026-01-05", "2026-01-19")]
    assert make_computed.windows(rows, 0, spans) == [("first three", 20, 2)]


def test_amounts_are_printed_in_whole_euros():
    assert make_case_data.eur(4_117_349) == "41,173"
    assert make_case_data.number(2008) == "2,008"


# --- the files of the repo ---


def test_the_blocks_of_c01_c02_c03_and_c05_are_the_ones_the_script_builds():
    company = make_case_data.open_company(make_case_data.DATABASE)
    built = make_case_data.blocks(company)
    assert sorted(built) == [
        "C01-data.txt",
        "C02-data.txt",
        "C03-data.txt",
        "C05-data-categories.txt",
        "C05-data.txt",
    ]
    for name, text in built.items():
        assert (BLOCKS / name).read_text() == text, name


def test_every_computed_block_is_the_one_the_script_builds():
    assert len(make_computed.MAKERS) == 10
    for name in make_computed.MAKERS:
        block = (BLOCKS / f"{name}.txt").read_text()
        on_disk = (BLOCKS / f"{name}-computed.txt").read_text()
        assert on_disk == make_computed.with_computed(name, block), name
        assert on_disk.startswith(block.rstrip("\n")) and make_computed.HEAD in on_disk, name


def test_no_block_is_left_without_a_check():
    scripted = {name.split("-")[0] for name in make_computed.MAKERS if name != "C05-data"}
    built = {"C01", "C02", "C03", "C05"}
    assert built | set(HAND_MADE) == scripted == {f"C0{i}" for i in range(1, 10)}


def test_the_tables_of_the_blocks_without_a_script_hold_the_figures_of_the_database():
    compared = 0
    for case, queries in HAND_MADE.items():
        for (columns, rows), (query, column_is, unit) in zip(tables_of(case), queries, strict=True):
            for week, cells in rows.items():
                for column, printed in zip(columns[1:], cells, strict=True):
                    key = column.split()[0] if column_is == "depot" else column
                    (value,) = DATABASE.execute(query, (week, key)).fetchone()
                    if value is not None and unit == "euros":
                        value = round(value / 100)
                    assert printed == value, (case, week, column)
                    compared += 1
    assert compared == 204  # every cell of the six tables
