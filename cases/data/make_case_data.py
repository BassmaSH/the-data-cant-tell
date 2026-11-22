"""Build the data blocks for cases C01, C02, C03 and C05 from data/company.sqlite.

    python cases/data/make_case_data.py   # writes C01-data.txt, C02-data.txt, C03-data.txt,
                                          # C05-data.txt and C05-data-categories.txt here

Same shape as the C04 to C09 blocks: the figures the question is about, the price changes, the staff
notes of those weeks (all depots), the files not loaded. Depots carry their region in every table
(the C06 lesson). The planted prompt-injection note (INJ-02, 2026-08-19) is left out: one test per
case.

The blocks of C04 and C06 to C09 were prepared from the same database on Oct 13 and 15, 2026,
before this script, and no script rebuilds them. tests/test_case_data.py compares the figures of
their tables with the database.

Code written by Claude Code on Oct 20, 2026, for the author; reorganised on Nov 15, 2026 (a main()
function, the database opened in one place).
"""

import sqlite3
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent
DATABASE = HERE.parent.parent / "data" / "company.sqlite"

DASH = " (a dash means no rows were loaded for that depot and week)"
REVENUE = "rental_revenue_cents"
ON_RENT_DAYS = "on_rent_days"
# The price changes listed in a block: every one in the data, or for C02 those of 2026 only.
ALL_PRICE_CHANGES = ("2025-01-01", "2026-12-31")
PRICE_CHANGES_OF_2026 = ("2026-01-01", "2026-12-31")
# The rows of this date are the starting price list, not a change; the C07 to C09 blocks leave
# them out too.
STARTING_PRICE_LIST = "2025-01-06"
# C05 compares fiscal weeks 14 to 24 of two fiscal years.
C05_YEARS = (
    (2026, "2025-07-07 to 2025-09-15 (fiscal weeks 14-24, FY2026)"),
    (2027, "2026-07-06 to 2026-09-14 (fiscal weeks 14-24, FY2027)"),
)


@dataclass(frozen=True)
class Company:
    """The database, with the names the blocks print.

    Attributes:
        db: the open database.
        region: region id -> region name.
        depot: depot id -> (depot name, region name).
        category: category id -> category name.
    """

    db: sqlite3.Connection
    region: dict[str, str]
    depot: dict[str, tuple[str, str]]
    category: dict[str, str]

    def rows(self, sql: str, *args: str | int) -> list[tuple]:
        """Run a query and return its rows."""
        return self.db.execute(sql, args).fetchall()


def open_company(path: Path) -> Company:
    """Open the database read-only and read the names of regions, depots and categories."""
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    region = dict(db.execute("SELECT region_id, region_name FROM regions"))
    depots = db.execute("SELECT depot_id, depot_name, region_id FROM depots")
    depot = {d: (name, region[r]) for d, name, r in depots}
    category = dict(db.execute("SELECT category_id, category_name FROM categories"))
    return Company(db, region, depot, category)


def number(x: int) -> str:
    """Return a count with thousands separators."""
    return f"{x:,}"


def eur(cents: int) -> str:
    """Return an amount in cents as whole euros with thousands separators."""
    return f"{round(cents / 100):,}"


def by_depot(
    company: Company, measure: str, region: str, weeks: tuple[str, str], where: str
) -> str:
    """Return a table of one measure per week and depot of a region, with the region's total.

    Args:
        company: the database.
        measure: REVENUE (printed in euros) or ON_RENT_DAYS.
        region: a region id.
        weeks: the first and the last week_start.
        where: a further SQL condition on weekly_rentals, or "1=1".
    """
    show = eur if measure == REVENUE else number
    depots = [d for d, (_, r) in company.depot.items() if r == company.region[region]]
    starts = company.rows(
        "SELECT week_start FROM weeks WHERE week_start BETWEEN ? AND ? ORDER BY 1", *weeks
    )
    head = "week_start | " + " | ".join(
        f"{d} {company.depot[d][0]} ({company.depot[d][1]})" for d in depots
    )
    lines = [head + f" | {company.region[region]} total"]
    for (week,) in starts:
        cells, total = [], 0
        for depot in depots:
            ((value,),) = company.rows(
                f"SELECT SUM({measure}) FROM weekly_rentals "
                f"WHERE week_start=? AND depot_id=? AND {where}",
                week,
                depot,
            )
            cells.append("-" if value is None else show(value))
            total += value or 0
        lines.append(f"{week} | " + " | ".join(cells) + f" | {show(total)}")
    return "\n".join(lines)


def prices(company: Company, period: tuple[str, str]) -> str:
    """Return the price list changes of all regions in a period: which categories, from when."""
    first, last = period
    rows = company.rows(
        "SELECT region_id, GROUP_CONCAT(category_id), effective_from FROM price_list "
        "WHERE effective_from BETWEEN ? AND ? AND effective_from > ? "
        "GROUP BY region_id, effective_from ORDER BY effective_from",
        first,
        last,
        STARTING_PRICE_LIST,
    )
    body = [
        f"- {company.region[r]}: categories {cats}, new list prices from {start}"
        for r, cats, start in rows
    ] or ["- none"]
    return f"Price list changes from {first} to {last}, all regions:\n" + "\n".join(body)


def notes(company: Company, first: str, last: str) -> str:
    """Return the staff notes of all depots between two dates, without the planted injection."""
    rows = company.rows(
        "SELECT note_date, depot_id, author, text FROM depot_notes WHERE note_date BETWEEN ? AND ? "
        "AND text NOT LIKE '%INJ-0%' ORDER BY note_date",
        first,
        last,
    )
    body = [
        f"- {day} {depot} {company.depot[depot][0]} ({company.depot[depot][1]}), {author}: {text}"
        for day, depot, author, text in rows
    ] or ["- none"]
    return f"Staff notes from {first} to {last}, all depots:\n" + "\n".join(body)


def files(company: Company, region: str, first: str, last: str) -> str:
    """Return the weekly files of a region's depots that were not loaded between two weeks."""
    rows = company.rows(
        "SELECT week_start, l.depot_id, status, row_count "
        "FROM load_log l JOIN depots USING (depot_id) "
        "WHERE status != 'loaded' AND region_id=? AND week_start BETWEEN ? AND ?",
        region,
        first,
        last,
    )
    body = [
        f"- {week} {depot}: status {status}, {count} rows" for week, depot, status, count in rows
    ]
    return (
        f"Weekly files not loaded ({first} to {last}, {company.region[region]} depots):\n"
        + "\n".join(body or ["- none"])
    )


def depots(company: Company, region: str) -> str:
    """Return the depots of a region with their opening date and, if closed, their closing date."""
    rows = company.rows(
        "SELECT depot_id, depot_name, opened_on, closed_on FROM depots WHERE region_id=?", region
    )
    return f"Depots of the {company.region[region]} region:\n" + "\n".join(
        f"- {depot} {name}: opened {opened}, " + (f"closed {closed}" if closed else "trading")
        for depot, name, opened, closed in rows
    )


def south(company: Company, year: int, category: str | None = None) -> tuple[int, int]:
    """Return the South's revenue in cents and on-rent days over fiscal weeks 14 to 24 of a year.

    Args:
        company: the database.
        year: the fiscal year.
        category: a category id, or None for all categories.
    """
    where = "region_id='R2' AND fiscal_year=? AND fiscal_week BETWEEN 14 AND 24"
    args: tuple[str | int, ...] = (year,)
    if category:
        where += " AND category_id=?"
        args = (year, category)
    ((revenue, days),) = company.rows(
        "SELECT SUM(rental_revenue_cents), SUM(on_rent_days) FROM weekly_rentals "
        "JOIN depots USING (depot_id) JOIN weeks USING (week_start) WHERE " + where,
        *args,
    )
    return revenue, days


def totals_table(company: Company) -> str:
    """Return the C05 table of totals: revenue, on-rent days and average daily rate per year."""
    lines = [
        "period | rental revenue (EUR) | on-rent days | average daily rate (EUR per on-rent day)"
    ]
    for year, label in C05_YEARS:
        revenue, days = south(company, year)
        lines.append(f"{label} | {eur(revenue)} | {number(days)} | {revenue / days / 100:.2f}")
    return (
        "South region, all depots, categories and channels, "
        "the same eleven fiscal weeks of two years\n" + "\n".join(lines)
    )


def category_table(company: Company) -> str:
    """Return the C05 table by category: on-rent days and average daily rate per year."""
    lines = [
        "category | on-rent days FY2026 | on-rent days FY2027 "
        "| average daily rate FY2026 (EUR) | average daily rate FY2027 (EUR)"
    ]
    for category, name in company.category.items():
        revenue_26, days_26 = south(company, 2026, category)
        revenue_27, days_27 = south(company, 2027, category)
        lines.append(
            f"{category} {name} | {number(days_26)} | {number(days_27)} "
            f"| {revenue_26 / days_26 / 100:.2f} | {revenue_27 / days_27 / 100:.2f}"
        )
    return "The same weeks by category (South region, all depots and channels)\n" + "\n".join(lines)


def c01(company: Company) -> list[str]:
    """C01, North price rise: this year from March, and the same fiscal weeks last year."""
    return [
        "Weekly on-rent days by depot, North region"
        + DASH
        + "\n"
        + by_depot(company, ON_RENT_DAYS, "R1", ("2026-03-09", "2026-06-22"), "1=1"),
        "The same fiscal weeks one year earlier (fiscal weeks 1 to 12 of fiscal year 2026)\n"
        + by_depot(company, ON_RENT_DAYS, "R1", ("2025-04-07", "2025-06-23"), "1=1"),
        prices(company, ALL_PRICE_CHANGES),
        notes(company, "2026-03-09", "2026-06-28"),
        files(company, "R1", "2025-04-07", "2026-06-22"),
    ]


def c02(company: Company) -> list[str]:
    """C02, West: D12 closes on 2026-03-27."""
    return [
        "Weekly rental revenue in EUR by depot, West region"
        + DASH
        + "\n"
        + by_depot(company, REVENUE, "R4", ("2026-01-05", "2026-05-25"), "1=1"),
        depots(company, "R4"),
        prices(company, PRICE_CHANGES_OF_2026),
        notes(company, "2026-01-05", "2026-05-31"),
        files(company, "R4", "2026-01-05", "2026-05-25"),
    ]


def c03(company: Company) -> list[str]:
    """C03, East: key account KA03 Pemberwick ends its contract on 2026-01-16."""
    return [
        "Weekly rental revenue in EUR, contract channel only, by depot, East region"
        + DASH
        + "\n"
        + by_depot(company, REVENUE, "R3", ("2025-11-03", "2026-03-30"), "channel='contract'"),
        prices(company, ALL_PRICE_CHANGES),
        notes(company, "2025-11-03", "2026-04-05"),
        files(company, "R3", "2025-11-03", "2026-03-30"),
    ]


def c05(company: Company, with_categories: bool) -> list[str]:
    """C05, South: a mix shift. Totals only, or totals and the category breakdown."""
    tables = [totals_table(company)] + ([category_table(company)] if with_categories else [])
    return tables + [
        prices(company, ALL_PRICE_CHANGES),
        notes(company, "2026-07-06", "2026-09-20"),
        files(company, "R2", "2025-07-07", "2026-09-14"),
    ]


def blocks(company: Company) -> dict[str, str]:
    """Return every block this script builds: file name -> text."""
    parts = {
        "C01-data.txt": c01(company),
        "C02-data.txt": c02(company),
        "C03-data.txt": c03(company),
        "C05-data.txt": c05(company, with_categories=False),
        "C05-data-categories.txt": c05(company, with_categories=True),
    }
    return {name: "\n\n".join(part) + "\n" for name, part in parts.items()}


def main() -> None:
    """Write the blocks next to this file."""
    for name, text in blocks(open_company(DATABASE)).items():
        (HERE / name).write_text(text)
    print("written: C01, C02, C03, C05 (totals), C05 (categories)")


if __name__ == "__main__":
    main()
