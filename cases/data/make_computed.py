"""Add to each data block the figures its question needs, computed by code (run 9, Oct 20, 2026).

    python cases/data/make_computed.py   # writes <case>-data-computed.txt for every case, and
                                         # C05-data-categories-computed.txt, next to this file

The tools test, small version: the figures are computed from the tables in the block itself, so
the model only explains (the author's rule: code computes, the model writes).

Numbers only: before and after, changes, per depot or channel. No interpretation and no cause. C05
totals gets no category breakdown (the case still tests "can't tell"); C05 categories gets shares
and changes, not the mix calculation.

Code written by Claude Code on Oct 20, 2026, for the author; type hints, docstrings and a main()
function added on Nov 15, 2026.
"""

from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).parent
HEAD = "Computed from the tables above (by code, not by the assistant):"

# A table of a block: its column names, and its rows by first cell (a week, a period, a category).
# A cell is a number, None for a dash (no rows loaded), or text.
Rows = dict[str, list]
Table = tuple[list[str], Rows]
# A named span of weeks: (label, first week, last week).
Span = tuple[str, str, str]


def cell(text: str) -> float | str | None:
    """Read one cell: a number, None for a dash, or the text as it is."""
    if text == "-":
        return None
    digits = text.replace(",", "")
    return float(digits) if digits.replace(".", "").isdigit() else text


def tables(text: str) -> dict[str, Table]:
    """Read every table of a block.

    Returns:
        The line above each table -> (its columns, its rows).
    """
    out, lines = {}, text.splitlines()
    for i, line in enumerate(lines):
        if " | " in line and (i == 0 or " | " not in lines[i - 1]):
            cols = [c.strip() for c in line.split("|")]
            rows = {}
            for row in lines[i + 1 :]:
                if " | " not in row:
                    break
                cells = [c.strip() for c in row.split("|")]
                rows[cells[0]] = [cell(c) for c in cells[1:]]
            out[lines[i - 1] if i else ""] = (cols, rows)
    return out


def mean(values: list[float | None]) -> float | None:
    """Return the mean of the values that are not None, or None when there is none."""
    known = [x for x in values if x is not None]
    return sum(known) / len(known) if known else None


def pct(before: float, after: float) -> str:
    """Return a change as a signed percentage, for example "-12.4 %"."""
    return f"{(after - before) / before * 100:+.1f} %"


def number(x: float) -> str:
    """Return a figure rounded to the unit, with thousands separators."""
    return f"{x:,.0f}"


def windows(rows: Rows, col: int, spans: list[Span]) -> list[tuple[str, float | None, int]]:
    """Average one column over named spans of weeks.

    Returns:
        For each span: (its label, the mean, the number of weeks that have a figure).
    """
    result = []
    for label, first, last in spans:
        values = [v[col] for week, v in rows.items() if first <= week <= last]
        result.append((label, mean(values), len([x for x in values if x is not None])))
    return result


def block(title: str, lines: list[str]) -> str:
    """Return a titled list, as it is added after a data block."""
    return "\n\n" + title + "\n" + "\n".join("- " + line for line in lines)


def per_column(rows: Rows, cols: list[str], spans: list[Span], unit: str) -> list[str]:
    """Return one line per column: its weekly average per span, and the change from the first."""
    lines = []
    for j, col in enumerate(cols[1:]):
        averages = windows(rows, j, spans)
        first_label, first_mean, _ = averages[0]
        parts = [
            f"{label} {number(m)} ({weeks} weeks)" if m is not None else f"{label} no rows"
            for label, m, weeks in averages
        ]
        changes = [
            f"{first_label} → {label}: {pct(first_mean, m)}"
            for label, m, _ in averages[1:]
            if m is not None and first_mean
        ]
        lines.append(
            f"{col}, weekly average {unit}: "
            + "; ".join(parts)
            + (". Change " + "; ".join(changes) if changes else "")
        )
    return lines


def c01(text: str) -> str:
    """C01: on-rent days since 2026-05-04 against the same fiscal weeks of 2025."""
    (cols, now), (_, last) = list(tables(text).values())[:2]
    weeks_now = [w for w in now if w >= "2026-05-04"]
    weeks_last = [w for w in last if w >= "2025-05-05"]
    pairs = list(zip(weeks_now, weeks_last, strict=True))
    lines = []
    for j, col in enumerate(cols[1:]):
        before = sum(last[w][j] for w in weeks_last)
        after = sum(now[w][j] for w in weeks_now)
        below = sum(now[x][j] < last[y][j] for x, y in pairs)
        lines.append(
            f"{col}: on-rent days in the {len(weeks_now)} weeks from 2026-05-04 {number(after)}, "
            f"the same {len(weeks_last)} fiscal weeks of 2025 {number(before)}, "
            f"change {pct(before, after)}; weeks below last year: {below} of {len(weeks_now)}"
        )
    week_by_week = [
        f"{x} {number(now[x][-1])} vs {y} {number(last[y][-1])} ({now[x][-1] - last[y][-1]:+,.0f})"
        for x, y in pairs
    ]
    lines.append(
        "North total, week by week (2026 vs the same fiscal week of 2025): "
        + "; ".join(week_by_week)
    )
    return block(HEAD, lines)


def c02(text: str) -> str:
    """C02: weekly revenue before and from 2026-03-30, and the range of D12 while it had rows."""
    cols, rows = list(tables(text).values())[0]
    spans = [
        ("2026-01-05 to 2026-03-23", "2026-01-05", "2026-03-23"),
        ("2026-03-30 to 2026-05-25", "2026-03-30", "2026-05-25"),
    ]
    lines = per_column(rows, cols, spans, "revenue (EUR)")
    d12 = cols.index("D12 Carrick Stowe (West)") - 1
    with_rows = {week: v[d12] for week, v in rows.items() if v[d12] is not None}
    lines.append(
        f"D12 Carrick Stowe: last week with rows {max(with_rows)}; weekly revenue before that: "
        f"lowest {number(min(with_rows.values()))}, highest {number(max(with_rows.values()))}"
    )
    return block(HEAD, lines)


def c03(text: str) -> str:
    """C03: weekly contract revenue in the eight weeks before and after the contract ended."""
    cols, rows = list(tables(text).values())[0]
    spans = [
        ("2025-11-24 to 2026-01-12", "2025-11-24", "2026-01-12"),
        ("2026-01-19 to 2026-03-09", "2026-01-19", "2026-03-09"),
    ]
    return block(HEAD, per_column(rows, cols, spans, "contract revenue (EUR)"))


def c04(text: str) -> str:
    """C04: the week of 2026-06-15 against the two weeks before and the two after."""
    cols, rows = list(tables(text).values())[0]
    around = ["2026-06-01", "2026-06-08", "2026-06-22", "2026-06-29"]
    lines = []
    for j, col in enumerate(cols[1:]):
        usual = mean([rows[w][j] for w in around])
        that_week = rows["2026-06-15"][j]
        lines.append(
            f"{col}: week of 2026-06-15 {number(that_week)}; average of the two weeks before "
            f"and the two after {number(usual)}; change {pct(usual, that_week)}"
        )
    return block(HEAD, lines)


def c05(text: str, categories: bool) -> str:
    """C05: the change in revenue, days and rate; with categories, the same for each one."""
    found = list(tables(text).values())
    _, totals = found[0]
    (revenue_26, days_26, rate_26), (revenue_27, days_27, rate_27) = list(totals.values())
    lines = [
        f"Rental revenue {pct(revenue_26, revenue_27)}; on-rent days {pct(days_26, days_27)}; "
        f"average daily rate {rate_26:.2f} → {rate_27:.2f} EUR ({pct(rate_26, rate_27)})"
    ]
    if categories:
        _, by_category = found[1]
        lines.append(
            "By category (on-rent days FY2026 → FY2027, share of all on-rent days, "
            "average daily rate change):"
        )
        for category, (d26, d27, r26, r27) in by_category.items():
            lines.append(
                f"{category}: {number(d26)} → {number(d27)} ({pct(d26, d27)}); "
                f"share {d26 / days_26 * 100:.1f} % → {d27 / days_27 * 100:.1f} %; "
                f"rate {r26:.2f} → {r27:.2f} ({pct(r26, r27)})"
            )
    return block(HEAD, lines)


def c06(text: str) -> str:
    """C06: each week's total with and without D03, and the week of 2026-07-13 by depot."""
    cols, rows = list(tables(text).values())[0]
    lines = []
    for week, values in rows.items():
        known = [x for x in values if x is not None]
        missing = len(values) - len(known)
        lines.append(
            f"{week}: total of the depots with rows {number(sum(known))}"
            + (f" ({missing} depot without rows)" if missing else "")
            + f"; total without D03 {number(values[0] + values[1])}"
        )
    weeks = list(rows)
    i = weeks.index("2026-07-13")
    before, that_week = rows[weeks[i - 1]], rows[weeks[i]]
    lines.append(
        "Week of 2026-07-13 against the week before, by depot: "
        + "; ".join(
            f"{col} {'no rows' if y is None else pct(x, y)}"
            for col, x, y in zip(cols[1:], before, that_week, strict=False)
        )
    )
    return block(HEAD, lines)


def c07(text: str) -> str:
    """C07: weekly on-rent days before, during and after the three weeks of the question."""
    spans = [
        ("2025-10-06 to 2025-11-03", "2025-10-06", "2025-11-03"),
        ("2025-11-10 to 2025-11-24", "2025-11-10", "2025-11-24"),
        ("2025-12-01 to 2025-12-22", "2025-12-01", "2025-12-22"),
    ]
    lines = []
    for cols, rows in tables(text).values():
        lines += per_column(rows, cols, spans, "on-rent days")
    return block(HEAD, lines)


def c08(text: str) -> str:
    """C08: weekly on-rent days in the four weeks before, during and after the dip."""
    cols, rows = list(tables(text).values())[0]
    spans = [
        ("2025-09-01 to 2025-09-22", "2025-09-01", "2025-09-22"),
        ("2025-09-29 to 2025-10-20", "2025-09-29", "2025-10-20"),
        ("2025-10-27 to 2025-11-17", "2025-10-27", "2025-11-17"),
    ]
    return block(HEAD, per_column(rows, cols, spans, "on-rent days"))


def c09(text: str) -> str:
    """C09: July 2026 against July 2025, June 2026 and August 2026, by channel."""
    cols, rows = list(tables(text).values())[0]
    spans = [
        ("July 2025 (2025-07-07 to 07-28)", "2025-07-07", "2025-07-28"),
        ("June 2026 (2026-06-01 to 06-29)", "2026-06-01", "2026-06-29"),
        ("July 2026 (2026-07-06 to 07-27)", "2026-07-06", "2026-07-27"),
        ("August 2026 (2026-08-03 to 08-31)", "2026-08-03", "2026-08-31"),
    ]
    lines = []
    for j, col in enumerate(cols[1:]):
        (l25, m25, _), (l6, m6, _), (l7, m7, _), (l8, m8, _) = windows(rows, j, spans)
        lines.append(
            f"{col}, weekly average on-rent days: {l25} {number(m25)}; {l6} {number(m6)}; "
            f"{l7} {number(m7)}; {l8} {number(m8)}. "
            f"July 2026 against July 2025 {pct(m25, m7)}; against June 2026 {pct(m6, m7)}; "
            f"August 2026 against July 2026 {pct(m7, m8)}"
        )
    return block(HEAD, lines)


# Data block (without ".txt") -> the function that computes its figures.
MAKERS: dict[str, Callable[[str], str]] = {
    "C01-data": c01,
    "C02-data": c02,
    "C03-data": c03,
    "C04-data": c04,
    "C06-data": c06,
    "C07-data": c07,
    "C08-data": c08,
    "C09-data": c09,
    "C05-data": lambda text: c05(text, categories=False),
    "C05-data-categories": lambda text: c05(text, categories=True),
}


def with_computed(name: str, text: str) -> str:
    """Return a data block followed by its computed figures.

    Args:
        name: the block's file name without ".txt", a key of MAKERS.
        text: the block.
    """
    text = text.rstrip("\n")
    return text + MAKERS[name](text) + "\n"


def main() -> None:
    """Write the computed version of every block next to this file."""
    for name in MAKERS:
        block_text = (HERE / f"{name}.txt").read_text()
        (HERE / f"{name}-computed.txt").write_text(with_computed(name, block_text))
    print("written: computed blocks for C01 to C09, C05 in both versions")


if __name__ == "__main__":
    main()
