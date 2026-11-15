"""Tests for data/make_data.py and data/check_data.py: the database behind every figure.

    pytest tests/test_data.py    # no API call

The first half tests the rules on small examples. The second half rebuilds the database in memory
and checks that it is the one in the repo, by its content hash.

Code written by Claude Code on Nov 15, 2026, for the author.
"""

import datetime as dt
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "data"))

import check_data  # noqa: E402
import make_data  # noqa: E402

PUBLISHED_HASH = "a5447e8fda05733a"  # printed in data/README.md


def built_in_memory() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    make_data.fill(con, make_data.build_tables())
    return con


# --- the rules, on small examples ---


def test_a_fiscal_year_starts_on_the_first_monday_of_april_and_is_named_after_its_end():
    assert make_data.fiscal(dt.date(2025, 4, 7)) == (2026, 1, 1)
    assert make_data.fiscal(dt.date(2026, 3, 30)) == (2026, 52, 4)
    assert make_data.fiscal(dt.date(2026, 4, 6)) == (2027, 1, 1)


def test_the_weeks_c05_compares_are_fiscal_weeks_14_to_24_of_both_years():
    """The labels printed in the C05 block: 2025-07-07 to 2025-09-15, 2026-07-06 to 2026-09-14."""
    assert make_data.fiscal(dt.date(2025, 7, 7))[:2] == (2026, 14)
    assert make_data.fiscal(dt.date(2025, 9, 15))[:2] == (2026, 24)
    assert make_data.fiscal(dt.date(2026, 7, 6))[:2] == (2027, 14)
    assert make_data.fiscal(dt.date(2026, 9, 14))[:2] == (2027, 24)


def test_a_fall_must_be_at_least_as_large_as_stated():
    expect = {"direction": "down", "at_least_pct": 20}
    assert check_data.judge((100, 75), expect)[1]
    assert not check_data.judge((100, 85), expect)[1]
    assert not check_data.judge((100, 125), expect)[1]
    assert check_data.judge((100, 125), {"direction": "up", "at_least_pct": 20})[1]


def test_a_figure_stated_as_not_moving_may_move_by_the_margin_only():
    assert check_data.judge((100, 104), {"within_pct": 5})[1]
    assert check_data.judge((100, 96), {"within_pct": 5})[1]
    assert not check_data.judge((100, 106), {"within_pct": 5})[1]


def test_a_count_must_be_exact():
    assert check_data.judge(0, {"equals": 0})[1]
    assert not check_data.judge(1, {"equals": 0})[1]


# --- the files of the repo ---


def test_the_database_in_the_repo_is_the_one_the_script_builds():
    con = built_in_memory()
    make_data.self_check(con)
    assert make_data.content_hash(con) == PUBLISHED_HASH
    assert make_data.hash_on_disk(make_data.DB_PATH) == PUBLISHED_HASH
    assert f"`{PUBLISHED_HASH}`" in (ROOT / "data" / "README.md").read_text()


def test_a_rebuild_that_changes_nothing_leaves_the_file_untouched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    path = tmp_path / "company.sqlite"
    monkeypatch.setattr(make_data, "DB_PATH", path)
    make_data.main()
    assert capsys.readouterr().out.startswith("wrote ")
    first = path.read_bytes()
    # Stand-in for a file written by another SQLite version: same rows, other bytes in the header.
    marked = bytearray(first)
    marked[96:100] = b"\x00\x00\x00\x01"
    path.write_bytes(marked)
    make_data.main()
    assert capsys.readouterr().out.startswith("unchanged ")
    assert path.read_bytes() == bytes(marked)


def test_a_file_with_other_rows_is_replaced(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    path = tmp_path / "company.sqlite"
    monkeypatch.setattr(make_data, "DB_PATH", path)
    make_data.main()
    with sqlite3.connect(path) as con:
        con.execute("DELETE FROM depot_notes WHERE note_date = '2026-06-15'")
    assert make_data.hash_on_disk(path) != PUBLISHED_HASH
    capsys.readouterr()
    make_data.main()
    assert capsys.readouterr().out.startswith("wrote ")
    assert make_data.hash_on_disk(path) == PUBLISHED_HASH


def test_the_nine_planted_episodes_are_visible_at_the_stated_size(
    capsys: pytest.CaptureFixture[str],
):
    with pytest.raises(SystemExit) as stop:
        check_data.main()
    assert stop.value.code == 0
    assert "9 of 9 causes visible at the stated size" in capsys.readouterr().out
