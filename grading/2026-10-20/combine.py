"""Combine the five grading files into one table: per model and set-up, the four verdict counts, fully right
answers (not invented, shows, figures, found), cost per 1,000 answers and cost per fully right answer."""
import json, re, glob
from pathlib import Path
G = Path(__file__).parent; R = Path(__file__).parent.parent.parent / "results"
FILES = {"large4-none.md": "mistral-large-4-0 (reasoning off)", "large4-high.md": "mistral-large-4-0 (reasoning high)",
         "haiku.md": "claude-haiku-5-5", "sonnet.md": "claude-sonnet-5-5", "opus.md": "claude-opus-5-5"}
PRICE = {"mistral-small-2603": (0.15, 0.60), "mistral-large-2512": (0.50, 1.50), "mistral-large-4-0": (1.36, 4.18),
         "claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2, 10), "claude-opus-5-5": (4, 20)}
# Rule C read both ways (her convention or the plain calendar): two verdicts flipped by Claude, Oct 20.
FLIP = {("mistral-large-4-0 (reasoning high)", "C02", "system + sentence"): "figures",
        ("mistral-small-2603", "C08", "steps"): "figures"}
rows = []
def parse(path, model):
    for line in path.read_text().splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        case = c[0].replace("*", "").strip() if c else ""
        if len(c) >= 6 and re.fullmatch(r"C0\d.*", case) and all(x in ("y", "n") for x in c[2:6]):
            setup = {"system": "system message"}.get(c[1], c[1])
            rows.append([model, case, setup] + [x == "y" for x in c[2:6]])
for f, m in FILES.items(): parse(G / f, m)
txt = (G / "mistral-2512-small.md").read_text().split("## mistral-large-2512")
for part, m in zip(txt, ["mistral-small-2603", "mistral-large-2512"]):
    p = G / "_tmp.md"; p.write_text(part); parse(p, m); p.unlink()
for r in rows:
    k = (r[0], r[1].split()[0], r[2])
    if k in FLIP: r[5] = True
def files_for(model, setup):
    base = model.split(" ")[0]
    tag = {"system message": "", "none": "-nosys", "system + sentence": "-premise", "sentence alone": "-premiseonly", "steps": "-steps"}[setup]
    if "reasoning off" in model: tag += "-rnone"
    if "reasoning high" in model: tag += "-rhigh"
    out = []
    for case in ["C01","C02","C03","C04","C06","C07","C08","C09","C05"]:
        names = [f"{case}-{base}{tag}.json"] + ([f"{case}-{base}{tag}-categories.json"] if case == "C05" else [])
        if case == "C06" and setup == "system message" and base in ("mistral-small-2603","mistral-large-2512"):
            names = [f"C06-{base}-v2.json"]
        for n in names:
            for d in ["2026-10-20", "2026-10-15"]:
                if (R / d / n).exists() and not (d == "2026-10-20" and setup == "system message" and case in ("C04","C06","C07","C08","C09") and base in ("mistral-small-2603","mistral-large-2512")):
                    out.append(R / d / n); break
    return out
models = list(dict.fromkeys(r[0] for r in rows))
print("| model | set-up | n | invented | shows | figures | found | fully right | cost per 1,000 answers | cost per fully right answer | seconds (median, max) |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
summary = []
for m in models:
    for s in ["none", "system message", "system + sentence", "sentence alone", "steps"]:
        rs = [r for r in rows if r[0] == m and r[2] == s]
        if not rs: continue
        inv, sh, fi, fo = (sum(r[i] for r in rs) for i in (3, 4, 5, 6))
        full = sum((not r[3]) and r[4] and r[5] and r[6] for r in rs)
        fs = files_for(m, s); pi, po = PRICE[m.split(" ")[0]]
        recs = [json.loads(f.read_text()) for f in fs]
        cost = sum(x["prompt_tokens"] * pi + x["completion_tokens"] * po for x in recs) / 1e6
        per1000 = cost / len(recs) * 1000 if recs else 0
        perright = (cost / full) if full else float("nan")
        secs = sorted(x["seconds"] for x in recs); med = secs[len(secs) // 2] if len(secs) % 2 else sum(secs[len(secs)//2 - 1:len(secs)//2 + 1]) / 2
        print(f"| {m} | {s} | {len(rs)} ({len(recs)} files) | {inv} | {sh} | {fi} | {fo} | {full} | ${per1000:.2f} | ${perright*1000:.2f} per 1,000 right | {med:.1f}, {secs[-1]:.1f} |")
