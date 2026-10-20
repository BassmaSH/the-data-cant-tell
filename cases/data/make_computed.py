"""The tools test, small version (Oct 20, 2026): each data block plus the figures its question needs, computed by
code from the tables in the block itself, so the model only explains (her rule: code computes, the model writes).

Numbers only: before and after, changes, per depot or channel. No interpretation and no cause. C05 totals gets no
category breakdown (the case still tests "can't tell"); C05 categories gets shares and changes, not the mix
calculation.

    python make_computed.py     # writes <case>-data-computed.txt (and C05-data-categories-computed.txt)
"""
from pathlib import Path

HERE = Path(__file__).parent


def tables(text):
    """Every table in a block: {header line: (columns, {first cell: [numbers or None]})}."""
    out, lines = {}, text.splitlines()
    for i, line in enumerate(lines):
        if " | " in line and (i == 0 or " | " not in lines[i - 1]):
            cols = [c.strip() for c in line.split("|")]
            rows = {}
            for row in lines[i + 1:]:
                if " | " not in row:
                    break
                cells = [c.strip() for c in row.split("|")]
                rows[cells[0]] = [None if c == "-" else float(c.replace(",", "")) if c.replace(",", "").replace(".", "").isdigit() else c
                                  for c in cells[1:]]
            out[lines[i - 1] if i else ""] = (cols, rows)
    return out


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def pct(a, b):
    return f"{(b - a) / a * 100:+.1f} %"


def n(x):
    return f"{x:,.0f}"


def windows(rows, col, spans):
    """Mean of one column over named spans of weeks: [(label, first, last)]."""
    res = []
    for label, a, b in spans:
        vals = [v[col] for w, v in rows.items() if a <= w <= b]
        res.append((label, mean(vals), len([x for x in vals if x is not None])))
    return res


def block(title, lines):
    return "\n\n" + title + "\n" + "\n".join("- " + l for l in lines)


HEAD = "Computed from the tables above (by code, not by the assistant):"


def per_column(t, cols, spans, unit):
    lines = []
    for j, c in enumerate(cols[1:]):
        w = windows(t, j, spans)
        parts = [f"{lab} {n(m)} ({k} weeks)" if m is not None else f"{lab} no rows" for lab, m, k in w]
        changes = [f"{w[0][0]} → {lab}: {pct(w[0][1], m)}" for lab, m, k in w[1:] if m is not None and w[0][1]]
        lines.append(f"{c}, weekly average {unit}: " + "; ".join(parts) + (". Change " + "; ".join(changes) if changes else ""))
    return lines


def c01(text):
    tb = list(tables(text).values())
    (cols, now), (_, last) = tb[0], tb[1]
    weeks_now = [w for w in now if w >= "2026-05-04"]
    weeks_last = [w for w in last if w >= "2025-05-05"]
    lines = []
    for j, c in enumerate(cols[1:]):
        a = sum(last[w][j] for w in weeks_last)
        b = sum(now[w][j] for w in weeks_now)
        below = sum(now[x][j] < last[y][j] for x, y in zip(weeks_now, weeks_last))
        lines.append(f"{c}: on-rent days in the {len(weeks_now)} weeks from 2026-05-04 {n(b)}, the same {len(weeks_last)} fiscal "
                     f"weeks of 2025 {n(a)}, change {pct(a, b)}; weeks below last year: {below} of {len(weeks_now)}")
    pairs = [f"{x} {n(now[x][-1])} vs {y} {n(last[y][-1])} ({now[x][-1] - last[y][-1]:+,.0f})" for x, y in zip(weeks_now, weeks_last)]
    lines.append("North total, week by week (2026 vs the same fiscal week of 2025): " + "; ".join(pairs))
    return block(HEAD, lines)


def c02(text):
    cols, t = list(tables(text).values())[0]
    spans = [("2026-01-05 to 2026-03-23", "2026-01-05", "2026-03-23"), ("2026-03-30 to 2026-05-25", "2026-03-30", "2026-05-25")]
    lines = per_column(t, cols, spans, "revenue (EUR)")
    d12 = cols.index("D12 Carrick Stowe (West)") - 1
    last = max(w for w, v in t.items() if v[d12] is not None)
    lines.append(f"D12 Carrick Stowe: last week with rows {last}; weekly revenue before that: lowest {n(min(v[d12] for v in t.values() if v[d12] is not None))}, "
                 f"highest {n(max(v[d12] for v in t.values() if v[d12] is not None))}")
    return block(HEAD, lines)


def c03(text):
    cols, t = list(tables(text).values())[0]
    spans = [("2025-11-24 to 2026-01-12", "2025-11-24", "2026-01-12"), ("2026-01-19 to 2026-03-09", "2026-01-19", "2026-03-09")]
    return block(HEAD, per_column(t, cols, spans, "contract revenue (EUR)"))


def c04(text):
    cols, t = list(tables(text).values())[0]
    spans = [("the four weeks around it (2026-06-01, 06-08, 06-22, 06-29)", None, None)]
    lines = []
    around = ["2026-06-01", "2026-06-08", "2026-06-22", "2026-06-29"]
    for j, c in enumerate(cols[1:]):
        m = mean([t[w][j] for w in around])
        v = t["2026-06-15"][j]
        lines.append(f"{c}: week of 2026-06-15 {n(v)}; average of the two weeks before and the two after {n(m)}; change {pct(m, v)}")
    return block(HEAD, lines)


def c05(text, categories):
    tb = list(tables(text).values())
    cols, t = tb[0]
    (r6, d6, a6), (r7, d7, a7) = [v for v in t.values()]
    lines = [f"Rental revenue {pct(r6, r7)}; on-rent days {pct(d6, d7)}; average daily rate {a6:.2f} → {a7:.2f} EUR ({pct(a6, a7)})"]
    if categories:
        ccols, ct = tb[1]
        lines.append("By category (on-rent days FY2026 → FY2027, share of all on-rent days, average daily rate change):")
        for cat, (x6, x7, y6, y7) in ct.items():
            lines.append(f"{cat}: {n(x6)} → {n(x7)} ({pct(x6, x7)}); share {x6 / d6 * 100:.1f} % → {x7 / d7 * 100:.1f} %; rate {y6:.2f} → {y7:.2f} ({pct(y6, y7)})")
    return block(HEAD, lines)


def c06(text):
    cols, t = list(tables(text).values())[0]
    lines = []
    for w, v in t.items():
        known = [x for x in v if x is not None]
        lines.append(f"{w}: total of the depots with rows {n(sum(known))}" + ("" if len(known) == len(v) else f" ({len(v) - len(known)} depot without rows)")
                     + f"; total without D03 {n(v[0] + v[1])}")
    weeks = list(t)
    i = weeks.index("2026-07-13")
    a, b = t[weeks[i - 1]], t[weeks[i]]
    lines.append(f"Week of 2026-07-13 against the week before, by depot: " + "; ".join(
        f"{c} {'no rows' if y is None else pct(x, y)}" for c, x, y in zip(cols[1:], a, b)))
    return block(HEAD, lines)


def c07(text):
    tb = list(tables(text).values())
    spans = [("2025-10-06 to 2025-11-03", "2025-10-06", "2025-11-03"), ("2025-11-10 to 2025-11-24", "2025-11-10", "2025-11-24"),
             ("2025-12-01 to 2025-12-22", "2025-12-01", "2025-12-22")]
    lines = []
    for cols, t in tb:
        lines += per_column(t, cols, spans, "on-rent days")
    return block(HEAD, lines)


def c08(text):
    cols, t = list(tables(text).values())[0]
    spans = [("2025-09-01 to 2025-09-22", "2025-09-01", "2025-09-22"), ("2025-09-29 to 2025-10-20", "2025-09-29", "2025-10-20"),
             ("2025-10-27 to 2025-11-17", "2025-10-27", "2025-11-17")]
    return block(HEAD, per_column(t, cols, spans, "on-rent days"))


def c09(text):
    cols, t = list(tables(text).values())[0]
    spans = [("July 2025 (2025-07-07 to 07-28)", "2025-07-07", "2025-07-28"), ("June 2026 (2026-06-01 to 06-29)", "2026-06-01", "2026-06-29"),
             ("July 2026 (2026-07-06 to 07-27)", "2026-07-06", "2026-07-27"), ("August 2026 (2026-08-03 to 08-31)", "2026-08-03", "2026-08-31")]
    lines = []
    for j, c in enumerate(cols[1:]):
        (l25, m25, k25), (l6, m6, k6), (l7, m7, k7), (l8, m8, k8) = windows(t, j, spans)
        lines.append(f"{c}, weekly average on-rent days: {l25} {n(m25)}; {l6} {n(m6)}; {l7} {n(m7)}; {l8} {n(m8)}. "
                     f"July 2026 against July 2025 {pct(m25, m7)}; against June 2026 {pct(m6, m7)}; August 2026 against July 2026 {pct(m7, m8)}")
    return block(HEAD, lines)


MAKERS = {"C01": c01, "C02": c02, "C03": c03, "C04": c04, "C06": c06, "C07": c07, "C08": c08, "C09": c09}
for case, make in MAKERS.items():
    text = (HERE / f"{case}-data.txt").read_text().rstrip("\n")
    (HERE / f"{case}-data-computed.txt").write_text(text + make(text) + "\n")
for name, cats in (("C05-data", False), ("C05-data-categories", True)):
    text = (HERE / f"{name}.txt").read_text().rstrip("\n")
    (HERE / f"{name}-computed.txt").write_text(text + c05(text, cats) + "\n")
print("written: computed blocks for C01 to C09, C05 in both versions")
