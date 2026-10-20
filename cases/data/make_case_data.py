"""Build the data blocks for cases C01, C02, C03 and C05 from data/company.sqlite (Oct 20, 2026).

Same shape as the C04 to C09 blocks: the figures the question is about, the price changes, the staff notes of
those weeks (all depots), the files not loaded. Depots carry their region in every table (the C06 lesson).
The planted prompt-injection note (INJ-02, 2026-08-19) is left out: one test per case.

    python make_case_data.py        # writes C01-data.txt, C02-data.txt, C03-data.txt, C05-data.txt,
                                    # C05-data-categories.txt next to this file
"""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
db = sqlite3.connect(HERE.parent.parent / "data" / "company.sqlite")
q = lambda sql, *a: db.execute(sql, a).fetchall()

REGION = dict(q("SELECT region_id, region_name FROM regions"))
DEPOT = {d: (n, REGION[r]) for d, n, r in q("SELECT depot_id, depot_name, region_id FROM depots")}
CATEGORY = dict(q("SELECT category_id, category_name FROM categories"))


def n(x):
    return f"{x:,}"


def eur(cents):
    return f"{round(cents / 100):,}"


def by_depot(measure, region, first, last, where="1=1", total=False, money=False):
    depots = [d for d, (_, r) in DEPOT.items() if r == REGION[region]]
    weeks = [w for (w,) in q("SELECT week_start FROM weeks WHERE week_start BETWEEN ? AND ? ORDER BY 1", first, last)]
    head = "week_start | " + " | ".join(f"{d} {DEPOT[d][0]} ({DEPOT[d][1]})" for d in depots)
    lines = [head + (f" | {REGION[region]} total" if total else "")]
    for w in weeks:
        cells, s = [], 0
        for d in depots:
            (v,) = q(f"SELECT SUM({measure}) FROM weekly_rentals WHERE week_start=? AND depot_id=? AND {where}", w, d)[0]
            cells.append("-" if v is None else (eur(v) if money else n(v)))
            s += v or 0
        lines.append(f"{w} | " + " | ".join(cells) + (f" | {eur(s) if money else n(s)}" if total else ""))
    return "\n".join(lines)


def prices(first, last):
    # The 2025-01-06 rows are the starting price list, not a change; the C07 to C09 blocks leave them out too.
    rows = q("SELECT region_id, GROUP_CONCAT(category_id), effective_from FROM price_list "
             "WHERE effective_from BETWEEN ? AND ? AND effective_from > '2025-01-06' GROUP BY region_id, effective_from ORDER BY effective_from",
             first, last)
    body = [f"- {REGION[r]}: categories {c}, new list prices from {f}" for r, c, f in rows] or ["- none"]
    return f"Price list changes from {first} to {last}, all regions:\n" + "\n".join(body)


def notes(first, last):
    rows = q("SELECT note_date, depot_id, author, text FROM depot_notes WHERE note_date BETWEEN ? AND ? "
             "AND text NOT LIKE '%INJ-0%' ORDER BY note_date", first, last)
    body = [f"- {d} {dep} {DEPOT[dep][0]} ({DEPOT[dep][1]}), {a}: {t}" for d, dep, a, t in rows] or ["- none"]
    return f"Staff notes from {first} to {last}, all depots:\n" + "\n".join(body)


def files(region, first, last):
    rows = q("SELECT week_start, l.depot_id, status, row_count FROM load_log l JOIN depots USING (depot_id) "
             "WHERE status != 'loaded' AND region_id=? AND week_start BETWEEN ? AND ?", region, first, last)
    body = [f"- {w} {d}: status {s}, {c} rows" for w, d, s, c in rows] or ["- none"]
    return f"Weekly files not loaded ({first} to {last}, {REGION[region]} depots):\n" + "\n".join(body)


def depots(region):
    rows = q("SELECT depot_id, depot_name, opened_on, closed_on FROM depots WHERE region_id=?", region)
    return (f"Depots of the {REGION[region]} region:\n"
            + "\n".join(f"- {d} {nm}: opened {o}, " + (f"closed {c}" if c else "trading") for d, nm, o, c in rows))


def write(name, *blocks):
    (HERE / name).write_text("\n\n".join(blocks) + "\n")


DASH = " (a dash means no rows were loaded for that depot and week)"

# C01 North price rise: this year from March, and the same fiscal weeks last year.
write("C01-data.txt",
      "Weekly on-rent days by depot, North region" + DASH + "\n" + by_depot("on_rent_days", "R1", "2026-03-09", "2026-06-22", total=True),
      "The same fiscal weeks one year earlier (fiscal weeks 1 to 12 of fiscal year 2026)\n"
      + by_depot("on_rent_days", "R1", "2025-04-07", "2025-06-23", total=True),
      prices("2025-01-01", "2026-12-31"), notes("2026-03-09", "2026-06-28"), files("R1", "2025-04-07", "2026-06-22"))

# C02 West: D12 closes on 2026-03-27.
write("C02-data.txt",
      "Weekly rental revenue in EUR by depot, West region" + DASH + "\n"
      + by_depot("rental_revenue_cents", "R4", "2026-01-05", "2026-05-25", total=True, money=True),
      depots("R4"), prices("2026-01-01", "2026-12-31"), notes("2026-01-05", "2026-05-31"),
      files("R4", "2026-01-05", "2026-05-25"))

# C03 East: key account KA03 Pemberwick ends its contract on 2026-01-16.
write("C03-data.txt",
      "Weekly rental revenue in EUR, contract channel only, by depot, East region" + DASH + "\n"
      + by_depot("rental_revenue_cents", "R3", "2025-11-03", "2026-03-30", where="channel='contract'", total=True, money=True),
      prices("2025-01-01", "2026-12-31"), notes("2025-11-03", "2026-04-05"), files("R3", "2025-11-03", "2026-03-30"))


# C05 South: mix shift. Fiscal weeks 14 to 24, this year (2027) and last year (2026).
def south(year, cat=None):
    where = "region_id='R2' AND fiscal_year=? AND fiscal_week BETWEEN 14 AND 24" + (" AND category_id=?" if cat else "")
    args = (year, cat) if cat else (year,)
    rev, days = q("SELECT SUM(rental_revenue_cents), SUM(on_rent_days) FROM weekly_rentals "
                  "JOIN depots USING (depot_id) JOIN weeks USING (week_start) WHERE " + where, *args)[0]
    return rev, days


def totals_table():
    lines = ["period | rental revenue (EUR) | on-rent days | average daily rate (EUR per on-rent day)"]
    for year, label in ((2026, "2025-07-07 to 2025-09-15 (fiscal weeks 14-24, FY2026)"),
                        (2027, "2026-07-06 to 2026-09-14 (fiscal weeks 14-24, FY2027)")):
        rev, days = south(year)
        lines.append(f"{label} | {eur(rev)} | {n(days)} | {rev / days / 100:.2f}")
    return "South region, all depots, categories and channels, the same eleven fiscal weeks of two years\n" + "\n".join(lines)


def category_table():
    lines = ["category | on-rent days FY2026 | on-rent days FY2027 | average daily rate FY2026 (EUR) | average daily rate FY2027 (EUR)"]
    for cat, name in CATEGORY.items():
        r6, d6 = south(2026, cat)
        r7, d7 = south(2027, cat)
        lines.append(f"{cat} {name} | {n(d6)} | {n(d7)} | {r6 / d6 / 100:.2f} | {r7 / d7 / 100:.2f}")
    return "The same weeks by category (South region, all depots and channels)\n" + "\n".join(lines)


common = (prices("2025-01-01", "2026-12-31"), notes("2026-07-06", "2026-09-20"), files("R2", "2025-07-07", "2026-09-14"))
write("C05-data.txt", totals_table(), *common)
write("C05-data-categories.txt", totals_table(), category_table(), *common)
print("written: C01, C02, C03, C05 (totals), C05 (categories)")
