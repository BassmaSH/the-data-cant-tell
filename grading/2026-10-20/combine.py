"""Combine the five grading files into one table: per model and set-up, the four verdict counts, fully right
answers (not invented, shows, figures, found), cost per 1,000 answers and cost per fully right answer."""
import json, re, glob
from pathlib import Path
G = Path(__file__).parent; R = Path(__file__).parent.parent.parent / "results"
FILES = {"large4-none.md": "mistral-large-4-0 (reasoning off)", "large4-high.md": "mistral-large-4-0 (reasoning high)",
         "haiku.md": "claude-haiku-5-5", "sonnet.md": "claude-sonnet-5-5", "opus.md": "claude-opus-5-5"}
PRICE = {"mistral-small-2603": (0.15, 0.60), "mistral-large-2512": (0.50, 1.50), "mistral-large-4-0": (1.36, 4.18),
         "claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2, 10), "claude-opus-5-5": (4, 20)}
# A verdict cell is "y" or "n"; "n → y" is a verdict changed after grading (the file says why): the last one counts.
CELL = re.compile(r"[yn](?: → [yn])?")
rows = []
def parse(path, model):
    for line in path.read_text().splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        case = c[0].replace("*", "").strip() if c else ""
        if len(c) >= 6 and re.fullmatch(r"C0\d.*", case) and all(CELL.fullmatch(x) for x in c[2:6]):
            setup = {"system": "system message"}.get(c[1], c[1])
            rows.append([model, case, setup] + [x[-1] == "y" for x in c[2:6]])
for f, m in FILES.items(): parse(G / f, m)
txt = (G / "mistral-2512-small.md").read_text().split("## mistral-large-2512")
for part, m in zip(txt, ["mistral-small-2603", "mistral-large-2512"]):
    p = G / "_tmp.md"; p.write_text(part); parse(p, m); p.unlink()
# The computed-figures run: verdicts transcribed from NOTEBOOK.md, run 9 (computed.md says how).
COMPUTED = "computed figures"
txt = (G / "computed.md").read_text().split("## mistral-large-4-0 (reasoning off)")
for part, m in zip(txt, ["mistral-small-2603", "mistral-large-4-0 (reasoning off)"]):
    p = G / "_tmp.md"; p.write_text(part); parse(p, m); p.unlink()
def files_for(model, setup):
    base = model.split(" ")[0]
    tag = {"system message": "", "none": "-nosys", "system + sentence": "-premise", "sentence alone": "-premiseonly", "steps": "-steps", COMPUTED: ""}[setup]
    if "reasoning off" in model: tag += "-rnone"
    if "reasoning high" in model: tag += "-rhigh"
    end = "-computed" if setup == COMPUTED else ""
    out = []
    for case in ["C01","C02","C03","C04","C06","C07","C08","C09","C05"]:
        names = [f"{case}-{base}{tag}{end}.json"] + ([f"{case}-{base}{tag}-categories{end}.json"] if case == "C05" else [])
        if case == "C06" and setup == "system message" and base in ("mistral-small-2603","mistral-large-2512"):
            names = [f"C06-{base}-v2.json"]
        for n in names:
            for d in ["2026-10-20", "2026-10-15"]:
                if (R / d / n).exists() and not (d == "2026-10-20" and setup == "system message" and case in ("C04","C06","C07","C08","C09") and base in ("mistral-small-2603","mistral-large-2512")):
                    out.append(R / d / n); break
    return out
models = list(dict.fromkeys(r[0] for r in rows))
HEAD = "| model | set-up | n | invented | shows | figures | found | fully right | cost per 1,000 answers | cost per fully right answer | seconds (median, max) |"
RULE = "|---|---|---|---|---|---|---|---|---|---|---|"
full_right = {}
def line(m, s):
    rs = [r for r in rows if r[0] == m and r[2] == s]
    if not rs: return
    inv, sh, fi, fo = (sum(r[i] for r in rs) for i in (3, 4, 5, 6))
    full = sum((not r[3]) and r[4] and r[5] and r[6] for r in rs)
    full_right[m, s] = full
    fs = files_for(m, s); pi, po = PRICE[m.split(" ")[0]]
    recs = [json.loads(f.read_text()) for f in fs]
    cost = sum(x["prompt_tokens"] * pi + x["completion_tokens"] * po for x in recs) / 1e6
    per1000 = cost / len(recs) * 1000 if recs else 0
    perright = (cost / full) if full else float("nan")
    secs = sorted(x["seconds"] for x in recs); med = secs[len(secs) // 2] if len(secs) % 2 else sum(secs[len(secs)//2 - 1:len(secs)//2 + 1]) / 2
    print(f"| {m} | {s} | {len(rs)} ({len(recs)} files) | {inv} | {sh} | {fi} | {fo} | {full} | ${per1000:.2f} | ${perright*1000:.2f} per 1,000 right | {med:.1f}, {secs[-1]:.1f} |")
SETUPS = ["none", "system message", "system + sentence", "sentence alone", "steps"]
print(HEAD); print(RULE)
for m in models:
    for s in SETUPS: line(m, s)
print("\nThe computed-figures run (verdicts transcribed from NOTEBOOK.md, run 9: see computed.md):\n")
print(HEAD); print(RULE)
for m in models: line(m, COMPUTED)
# The README's results table, in its order of models and set-ups.
README_MODELS = {"Mistral Small 2603": "mistral-small-2603", "Mistral Large 3": "mistral-large-2512",
                 "Mistral Large 4, reasoning off": "mistral-large-4-0 (reasoning off)",
                 "Mistral Large 4, reasoning high": "mistral-large-4-0 (reasoning high)",
                 "Claude Haiku 5.5": "claude-haiku-5-5", "Claude Sonnet 5.5": "claude-sonnet-5-5", "Claude Opus 5.5": "claude-opus-5-5"}
README_SETUPS = {"none": "none", "system message": "system message", "+ my sentence": "system + sentence", "steps": "steps", COMPUTED: COMPUTED}
print("\nFully right answers out of 10, as in the README's results table:\n")
print("| model | " + " | ".join(README_SETUPS) + " |"); print("|---" * (len(README_SETUPS) + 1) + "|")
for label, m in README_MODELS.items():
    print(f"| {label} | " + " | ".join(str(full_right.get((m, s), "—")) for s in README_SETUPS.values()) + " |")
