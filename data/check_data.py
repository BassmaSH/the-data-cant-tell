"""Check that every planted episode in causes.json is really visible in company.sqlite.

Run from anywhere, after make_data.py:
    .venv/bin/python mistral/data-assistant/data/check_data.py

For each cause id the script recomputes the figures from the database, prints
them (before, after, change), and compares them with the size stated in
causes.json under "visible_effect". It exits with code 1 if any effect is
missing or smaller than stated, or if causes.json names a measure that is not
computed here (or the reverse).

Three kinds of expectation are understood:
    {"direction": "down", "at_least_pct": 20}   the figure moves that way by at least 20 %
    {"within_pct": 5}                           the figure does NOT move by more than 5 %
    {"equals": 0}                               a count has exactly this value

Everything is invented; the script is boilerplate (generated with an assistant).
Standard library only. It reads the database and writes nothing.
"""

import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
con = sqlite3.connect(f"file:{HERE / 'company.sqlite'}?mode=ro", uri=True)

RENTALS = "weekly_rentals JOIN depots USING (depot_id) JOIN weeks USING (week_start)"


def one(sql, *args):
    value = con.execute(sql, args).fetchone()[0]
    return 0 if value is None else value


def total(column, where, *args):
    return one(f"SELECT SUM({column}) FROM {RENTALS} WHERE {where}", *args)


def adr(where, *args):
    """Average daily rate in cents: revenue divided by on-rent days, over the whole scope."""
    return one(f"SELECT SUM(rental_revenue_cents) * 1.0 / SUM(on_rent_days) FROM {RENTALS} WHERE {where}", *args)


def weekly_mean(column, where, weeks):
    marks = ",".join("?" * len(weeks))
    return one(f"SELECT SUM({column}) * 1.0 / {len(weeks)} FROM {RENTALS} "
               f"WHERE {where} AND week_start IN ({marks})", *weeks)


def notes(depots, first, last):
    marks = ",".join("?" * len(depots))
    return one(f"SELECT COUNT(*) FROM depot_notes WHERE depot_id IN ({marks}) AND note_date BETWEEN ? AND ?",
               *depots, first, last)


def price_changes(region, first, last):
    return one("SELECT COUNT(*) FROM price_list WHERE region_id = ? AND effective_from BETWEEN ? AND ?",
               region, first, last)


def missing_files(depots, first, last):
    marks = ",".join("?" * len(depots))
    return one(f"SELECT COUNT(*) FROM load_log WHERE status = 'missing' AND depot_id IN ({marks}) "
               f"AND week_start BETWEEN ? AND ?", *depots, first, last)


def c01():
    before, after = "week_start BETWEEN '2026-03-09' AND '2026-04-27'", "week_start BETWEEN '2026-05-04' AND '2026-06-22'"
    last_year = "week_start BETWEEN '2025-05-05' AND '2025-06-23'"
    north = "region_id = 'R1' AND "
    return {
        "north_average_daily_rate_cents": (adr(north + before), adr(north + after)),
        "north_on_rent_days_vs_same_weeks_last_year": (total("on_rent_days", north + last_year), total("on_rent_days", north + after)),
        "north_rental_revenue_cents_vs_same_weeks_last_year": (total("rental_revenue_cents", north + last_year), total("rental_revenue_cents", north + after)),
        "price_list_rows_north_starting_2026_05_04": price_changes("R1", "2026-05-04", "2026-05-04"),
    }


def c02():
    last_year, this_year = "fiscal_year = 2026 AND fiscal_week <= 8", "fiscal_year = 2027 AND fiscal_week <= 8"
    return {
        "west_rental_revenue_cents_fiscal_weeks_1_to_8": (
            total("rental_revenue_cents", "region_id = 'R4' AND " + last_year),
            total("rental_revenue_cents", "region_id = 'R4' AND " + this_year)),
        "west_without_d12_rental_revenue_cents_fiscal_weeks_1_to_8": (
            total("rental_revenue_cents", "region_id = 'R4' AND depot_id != 'D12' AND " + last_year),
            total("rental_revenue_cents", "region_id = 'R4' AND depot_id != 'D12' AND " + this_year)),
        "rows_for_d12_after_closing_date": one(
            "SELECT COUNT(*) FROM weekly_rentals WHERE depot_id = 'D12' AND week_start > "
            "(SELECT closed_on FROM depots WHERE depot_id = 'D12')"),
        "depots_with_a_closing_date": one("SELECT COUNT(*) FROM depots WHERE closed_on IS NOT NULL"),
    }


def c03():
    before, after = "week_start BETWEEN '2025-11-24' AND '2026-01-12'", "week_start BETWEEN '2026-01-19' AND '2026-03-09'"
    others = ("SELECT SUM(rental_revenue_cents) FROM customer_weekly JOIN depots USING (depot_id) "
              "WHERE region_id = 'R3' AND customer_id != 'KA03' AND ")
    return {
        "east_contract_channel_rental_revenue_cents": (
            total("rental_revenue_cents", "region_id = 'R3' AND channel = 'contract' AND " + before),
            total("rental_revenue_cents", "region_id = 'R3' AND channel = 'contract' AND " + after)),
        "east_contract_channel_without_ka03_rental_revenue_cents": (one(others + before), one(others + after)),
        "rows_for_ka03_after_2026_01_16": one(
            "SELECT COUNT(*) FROM customer_weekly WHERE customer_id = 'KA03' AND week_start > '2026-01-16'"),
        "customers_with_contract_ended_on_2026_01_16": one(
            "SELECT COUNT(*) FROM customers WHERE contract_ended_on = '2026-01-16'"),
    }


def c04():
    around = ("2026-06-01", "2026-06-08", "2026-06-22", "2026-06-29")
    return {
        "d05_on_rent_days_per_week": (weekly_mean("on_rent_days", "depot_id = 'D05'", around),
                                      weekly_mean("on_rent_days", "depot_id = 'D05'", ("2026-06-15",))),
        "notes_at_d05_dated_2026_06_15": notes(("D05",), "2026-06-15", "2026-06-15"),
    }


def c05():
    scope = "region_id = 'R2' AND fiscal_week BETWEEN 14 AND 24 AND fiscal_year = "
    out = {"south_average_daily_rate_cents_all_categories": (adr(scope + "2026"), adr(scope + "2027"))}
    for cat in ("ACC", "EAR", "PWT", "PWL", "CON"):
        out[f"south_average_daily_rate_cents_{cat}"] = (
            adr(scope + "2026 AND category_id = ?", cat), adr(scope + "2027 AND category_id = ?", cat))
    share = lambda year: (100.0 * total("on_rent_days", scope + year + " AND category_id = 'PWT'")
                          / total("on_rent_days", scope + year))
    out["south_power_tools_share_of_on_rent_days_pct"] = (share("2026"), share("2027"))
    return out


def c06():
    around = ("2026-06-29", "2026-07-06", "2026-07-20", "2026-07-27")
    rows = lambda week: one("SELECT COUNT(*) FROM weekly_rentals WHERE depot_id = 'D03' AND week_start = ?", week)
    return {
        "north_rental_revenue_cents_per_week": (
            weekly_mean("rental_revenue_cents", "region_id = 'R1'", around),
            weekly_mean("rental_revenue_cents", "region_id = 'R1'", ("2026-07-13",))),
        "north_without_d03_rental_revenue_cents_per_week": (
            weekly_mean("rental_revenue_cents", "region_id = 'R1' AND depot_id != 'D03'", around),
            weekly_mean("rental_revenue_cents", "region_id = 'R1' AND depot_id != 'D03'", ("2026-07-13",))),
        "rows_for_d03_week_2026_07_13": rows("2026-07-13"),
        "rows_for_d03_week_before": rows("2026-07-06"),
        "rows_for_d03_week_after": rows("2026-07-20"),
        "load_log_missing_files_d03_week_2026_07_13": missing_files(("D03",), "2026-07-13", "2026-07-13"),
        "load_log_missing_files_anywhere": missing_files(tuple(f"D{i:02d}" for i in range(1, 13)), "2025-01-01", "2026-12-31"),
        "fleet_rows_for_d03_week_2026_07_13": one(
            "SELECT COUNT(*) FROM fleet_weekly WHERE depot_id = 'D03' AND week_start = '2026-07-13'"),
    }


def c07():
    during = ("2025-11-10", "2025-11-17", "2025-11-24")
    around = ("2025-10-13", "2025-10-20", "2025-10-27", "2025-11-03", "2025-12-01", "2025-12-08", "2025-12-15", "2025-12-22")
    scope = "depot_id = 'D11' AND category_id = 'PWL' AND channel IN ('counter', 'online')"
    return {
        "d11_power_and_lighting_walk_in_on_rent_days_per_week": (
            weekly_mean("on_rent_days", scope, around), weekly_mean("on_rent_days", scope, during)),
        "notes_at_d11_in_window": notes(("D11",), "2025-10-13", "2025-12-28"),
        "price_changes_west_in_window": price_changes("R4", "2025-10-13", "2025-12-28"),
        "missing_files_d11_in_window": missing_files(("D11",), "2025-10-13", "2025-12-28"),
    }


def c08():
    during = ("2025-09-29", "2025-10-06", "2025-10-13", "2025-10-20")
    around = ("2025-09-01", "2025-09-08", "2025-09-15", "2025-09-22", "2025-10-27", "2025-11-03", "2025-11-10", "2025-11-17")
    return {
        "d01_on_rent_days_per_week": (weekly_mean("on_rent_days", "depot_id = 'D01'", around),
                                      weekly_mean("on_rent_days", "depot_id = 'D01'", during)),
        "notes_at_d01_in_window": notes(("D01",), "2025-09-01", "2025-11-23"),
        "price_changes_north_in_window": price_changes("R1", "2025-09-01", "2025-11-23"),
        "missing_files_d01_in_window": missing_files(("D01",), "2025-09-01", "2025-11-23"),
    }


def c09():
    last_year, this_year = "report_month = '2025-07'", "report_month = '2026-07'"
    east = "region_id = 'R3' AND channel = "
    return {
        "east_counter_on_rent_days_july": (total("on_rent_days", east + "'counter' AND " + last_year),
                                           total("on_rent_days", east + "'counter' AND " + this_year)),
        "east_online_on_rent_days_july": (total("on_rent_days", east + "'online' AND " + last_year),
                                          total("on_rent_days", east + "'online' AND " + this_year)),
        "east_counter_average_daily_rate_cents_july": (adr(east + "'counter' AND " + last_year),
                                                       adr(east + "'counter' AND " + this_year)),
        "price_changes_east_ever": price_changes("R3", "2025-01-07", "2026-12-31"),
        "price_changes_west_starting_2026_07_06": price_changes("R4", "2026-07-06", "2026-07-06"),
        "notes_at_east_depots_june_to_august_2026": notes(("D07", "D08", "D09"), "2026-06-01", "2026-08-31"),
        "missing_files_east_june_to_august_2026": missing_files(("D07", "D08", "D09"), "2026-06-01", "2026-08-31"),
    }


COMPUTE = {"C01": c01, "C02": c02, "C03": c03, "C04": c04, "C05": c05, "C06": c06, "C07": c07, "C08": c08, "C09": c09}


def judge(value, expect):
    """Return (text to print, passed)."""
    if "equals" in expect:
        return f"{value}  (stated: exactly {expect['equals']})", value == expect["equals"]
    before, after = value
    change = 100.0 * (after - before) / before
    text = f"before {before:,.1f}  after {after:,.1f}  change {change:+.1f} %"
    if "within_pct" in expect:
        return f"{text}  (stated: no move beyond {expect['within_pct']} %)", abs(change) <= expect["within_pct"]
    sign = -1 if expect["direction"] == "down" else 1
    return (f"{text}  (stated: {expect['direction']} by at least {expect['at_least_pct']} %)",
            sign * change >= expect["at_least_pct"])


def main():
    causes = json.loads((HERE / "causes.json").read_text(encoding="utf-8"))["causes"]
    failures = 0
    for cause in causes:
        cid = cause["id"]
        computed = COMPUTE[cid]()
        stated = {e["measure"]: e for e in cause["visible_effect"]}
        ok = set(computed) == set(stated)
        lines = []
        for name in sorted(set(computed) | set(stated)):
            if name not in computed or name not in stated:
                lines.append(f"      FAIL  {name}: in causes.json or in check_data.py but not in both")
                continue
            text, passed = judge(computed[name], stated[name])
            ok = ok and passed
            lines.append(f"      {'ok  ' if passed else 'FAIL'}  {name}: {text}")
        cause_text = cause["true_cause"] if cause["true_cause"] else "none in the data (true_cause is null)"
        print(f"{cid}  {'VISIBLE' if ok else 'NOT VISIBLE'}  {cause['title']}  |  cause: {cause_text}")
        print("\n".join(lines))
        failures += 0 if ok else 1
    missing = sorted(set(COMPUTE) - {c["id"] for c in causes})
    if missing:
        print(f"FAIL  computed here but absent from causes.json: {missing}")
        failures += 1
    print(f"{len(causes) - failures} of {len(causes)} causes visible at the stated size")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
