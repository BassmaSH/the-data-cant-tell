*The lab notebook, written during the runs (Oct 13 to 20, 2026), in the third person: "her" is Bassma, who
designed the cases, made every prediction and decided the grading rules; Claude (Claude Code) wrote the data, the
scripts and this record. The README is the write-up.*

# Results — does a Mistral model invent causes when the data cannot tell?

One row per run of the case set. Cases in `cases/`, data shown in `cases/data/`, raw answers in `results/<date>/`,
script `run_cases.py`. Graded by hand by Bassma on four measures (the first two from Oct 13, the third from the
C09 runs, the fourth added Oct 15 for cases whose cause is in the data):

1. **Invented cause:** an unsupported cause presented as a finding (a labelled hypothesis is not one).
2. **Said what the data shows:** the size, place and timing of the change, not only "the data cannot tell".
3. **Figures right:** every quoted figure is the one in the data, and what is said about it is true.
4. **Found the cause in the data:** C04 the walkout note, C06 the missing file; for C07, C08, C09 the right
   answer is "none in the data".

## Run 1 — Oct 15, 2026

Five cases (C04, C06, C07, C08, C09), each once per model, temperature 0, the same system message:
"Don't say anything that isn't clearly supported by the data. If you are unable to answer something with the
data, say so." C06 counted from its rerun with the region named in the table (see below).

| model | invented cause | said what data shows | figures right | found the cause / rightly "none" | prompt + answer tokens (avg) | seconds (median, max) | cost per 1,000 answers |
|---|---|---|---|---|---|---|---|
| `mistral-small-2603` | 0 / 5 | 4 / 5 (C07) | 4 / 5 (C07) | 5 / 5 | 883 + 134 | 1.7, 2.1 | about $0.21 |
| `mistral-large-2512` | 0 / 5 | 5 / 5 | 4 / 5 (C07) | 5 / 5 | 871 + 326 | 4.6, 16.4 | about $0.92 |

**Cost:** average tokens × price per million, list prices in USD looked up Oct 15: large $0.50 in / $1.50 out
(mistral.ai/pricing, given for "Mistral Large" without a version); small $0.15 in / $0.60 out (third-party price
lists citing Mistral; Mistral's own page shows no Small price). Check both on the console before quoting them.
The large model costs about 4× the small one per answer, mostly because its answers are about 2.5× longer.

**Prediction (written before the run):** invented cause no, said what the data shows yes, found the cause yes,
in every case; figures right for the large model and wrong for the small one.
- Invented cause, said what the data shows, found the cause: held, except the small model on C07.
- Figures: the large model was wrong once (C07: "contract notably higher than 49–98 in October"; October was
  98, 143, 49, 142, 97). The small model was wrong once, and not in the way predicted: on C07 its figures are
  real but it compares the first and last week inside the period and calls 132 → 126 "increased".

**What five cases can support.** Zero invented causes in five answers does not mean the rate is zero: with five
cases, the most it rules out is a rate above about 60 % (the rule of three: 3 / n); nine cases would bring that
to about 33 %. The row says the models did not invent causes on these five cases with this system message,
not how often they do.

**C06, first version (no region in the table).** Both models failed it: neither knew that the three depots are
North, neither added them up, the small model placed Scarrow Bridge in the West, and the large model reversed
two weeks of Petherby (it gave 56,469 → 46,873; the data is 46,873 → 56,469) and so described a drop that was a
rise. With the region named (`C06-data.txt`, v2), both answered right: the drop is the missing D03 file. Concluded
Oct 15 (her question, whether to fix the data or the prompt): the case tested two things at once; the region belongs in the data, as a real assistant would have
it from the `depots` table. The other half, a question that uses a word the data does not contain, is a separate
behaviour (did it say how it read the word?) and becomes its own case.

**Not done in this run:** the other four cases (C01, C02, C03, C05) · the runs without the system message on
the large model.

**Next tests she proposed (Oct 17).** (1) The question's own premise: the same "why" case with no system
message, on the large model too (C09 run 3 on the small model invented a cause). (2) Irrelevant context: one case
with 0, 5 and 20 unrelated staff notes, counting how often a note is taken as the cause.

## Run 2 — Oct 20, 2026: no system message

The same five cases, data and questions as run 1, each once per model, temperature 0, **no system message**
(`run_cases.py mistral-large-2512 --no-system`; raw answers in `results/2026-10-20/*-nosys.json`). C06 on the
v2 data (region named). Graded by hand by Bassma on the same four measures (C07 to C09 from Claude's proposed
verdicts, which she checked and agreed; the figure checks against the data are Claude's).

| model | invented cause | said what data shows | figures right | found the cause / rightly "none" | prompt + answer tokens (avg) | seconds (median, max) | cost per 1,000 answers |
|---|---|---|---|---|---|---|---|
| `mistral-small-2603` | 3 / 5 (C06, C08, C09) | 3 / 5 (not C07, C09) | 1 / 5 (C04 only) | 1 / 5 (C04 only) | 854 + 462 | 3.3, 3.5 | about $0.41 |
| `mistral-large-2512` | 4 / 5 (C06, C07, C08, C09) | 5 / 5 | 0 / 5 | 2 / 5 (C04, C06) | 842 + 1,026 | 14.9, 22.0 | about $1.96 |

**Against run 1 (with the system message):** invented causes 0 / 10 → 7 / 10; figures right 8 / 10 → 1 / 10;
found the cause or rightly "none" 10 / 10 → 3 / 10. Only C04, the case where the cause is a plain note at the
right depot and week, came through on both models. Cost at the same list prices as run 1: answers about 3×
longer on both models, so about 2× the cost per answer (small $0.21 → $0.41, large $0.92 → $1.96).

**Her prediction (written and committed before the run, Oct 20):** C04 and C06 same as before; C07, C08, C09
will invent a cause, on both models.
- C04: held, except Large's figures (it put the South price change "6 weeks" before the drop; it was 10).
- C06: did not hold. Both models invented a cause (Small: the South walkout a month earlier, in another region;
  Large: "a real but unexplained decline in D02", which rose), both got figures wrong (Large reversed Petherby,
  56,469 → 46,873, the same error as run 1 on the v1 data), and Small treated the missing file as secondary.
- C07, C08, C09: held on 5 of 6 answers. The exception is C07 on Small: no named cause, only a hedged
  "possible reduction in demand", but it read the three-week rise as a decline.

**Her reason, and what the run adds to it.** Before the run: a "why did X drop?" question carries a hidden
assumption that the cause is in the data, and the system message is what corrects it. After the run (hers,
Oct 20): the models did not only look for a cause, they bent the data to fit the decline the question
described, reversing two weeks (C06 Large), calling rises drops (C06 Small) or quoting another column (C09
Small). Her proposal: add to the system message "if the user is making an observation, check it is true first
and correct it if not". Against it, honestly: C07 asks "what happened", with no decline in the question, and
Small still read the rise as a decline, so the premise is not the only source of misreadings; and run 1
(with the system message) reversed Petherby too, so "don't say what isn't supported" alone does not catch it.
Related terms: false-premise questions, sycophancy (a model agreeing with what the user seems to believe).

**Why the answers are longer.** Most of the extra length is speculation the system message forbids: on C09
Large, five of seven sections are possible causes not in the data, then recommendations. Without the
instruction the model falls back on its trained idea of a helpful answer (thorough, structured, every
possibility). So the one sentence of system message both prevents invented causes and cuts output tokens
about 3× on these cases.

**What five cases can support.** As in run 1: these are five cases, one call each, at temperature 0. The
difference 0 / 10 → 7 / 10 is large enough to matter on these cases, not a rate.

**Next, from this run:** row 3, the same cases with her sentence added to the system message (does it fix the
reversed and misread figures?) · the four unwritten cases (C01, C02, C03, C05) · the Anthropic models on the
same runs · her irrelevant-notes test (0, 5, 20 notes).

## Run 3 — Oct 20, 2026: her premise sentence (prediction written before the run)

Her sentence, from reading run 2: "If the user is making an observation, make sure that observation is true
first and correct it if not." Two variants, the same five cases, both models, temperature 0
(`run_cases.py mistral-large-2512 --premise` and `--premise-only`):
- **(a) `-premise`:** the run 1 system message plus her sentence. Compared with run 1.
- **(b) `-premiseonly`:** her sentence alone. Compared with run 2; this is the direct test of her claim that the
  question's hidden assumption is what the system message corrects.

**Her prediction (Oct 20, before the run):**
- (b): same as run 2 (causes still invented, the cause still missed where it was), **except figures right**.
  So: checking the premise stops the bending of the data, not the inventing of causes.
- (a): same as run 1, maybe better figures (run 1's misses were both on C07).

**Result (Oct 20).** Raw answers `results/2026-10-20/*-premiseonly.json` and `*-premise.json`. Verdicts proposed
by Claude from the figure checks against the data, confirmed by her.

| variant | model | invented cause | said what data shows | figures right | found the cause / rightly "none" | prompt + answer tokens (avg) | seconds (median, max) | cost per 1,000 answers |
|---|---|---|---|---|---|---|---|---|
| (b) sentence alone | `mistral-small-2603` | 1 / 5 (C09) | 2 / 5 (C06, C08) | 2 / 5 (C04, C08) | 3 / 5 (C04, C06, C08) | 877 + 360 | 2.6, 3.9 | about $0.35 |
| (b) sentence alone | `mistral-large-2512` | 2 / 5 (C06, C07) | 4 / 5 (not C06) | 3 / 5 (C04, C08, C09) | 3 / 5 (C04, C08, C09) | 865 + 626 | 10.1, 13.5 | about $1.37 |
| (a) run 1 message + sentence | `mistral-small-2603` | 1 / 5 (C09) | 2 / 5 (C06, C08) | 3 / 5 (C04, C06, C08) | 3 / 5 (C04, C06, C08) | 904 + 256 | 1.7, 3.1 | about $0.29 |
| (a) run 1 message + sentence | `mistral-large-2512` | 0 / 5 | 5 / 5 | 4 / 5 (not C07) | 5 / 5 | 892 + 363 | 6.5, 7.8 | about $0.99 |

Per answer, what decided the verdicts:
- **C06, (b) Small:** corrected the premise (North 186,376 → 136,429, "primarily due to missing data for D03");
  figures marked wrong for "D01 and D02 increased slightly" (D02 rose 20 %).
- **C06, (b) Large:** worse than run 2. "Petherby dropped from 59,593 to 46,873" mixes D03's figure into D02;
  it dismissed the missing file ("doesn't explain the drop") and blamed "a localized disruption" at D02.
- **C06, (a) Large:** the clearest premise correction: "this is actually an increase… so the premise of a
  revenue drop for this depot is incorrect"; "the only anomaly is the missing data for D03".
- **C07, Small, both variants:** the rise read as a decline again; in (a) "increased from 132 to 126 (a slight
  decrease)" and contract "stable at 135" (it went to 129).
- **C07, Large:** (b) a "Most likely explanation" with three generic causes; both variants repeat a wrong
  contract claim ("elevated", "higher than earlier weeks like 49 or 97", leaving out 142 and 143).
- **C08, both models, both variants:** "cannot be determined" with the right figures (in run 2: the season).
- **C09, Small, both variants:** the walkout as the cause, and the contract column quoted as counter (1,792 →
  1,507). **C09, Large, (b):** possible causes labelled "if…", ending "not directly explained by the data"
  (counted as not invented, borderline).

**Against her prediction.** (b) "same as run 2 except figures right": the sentence did more than predicted on
invented causes (run 2: 3 and 4 → 1 and 2; C08 now ends "cannot be determined" on both models) and less on
figures (Small still reads the wrong column or direction; Large broke C06 in a new way: checking the premise,
it looked for another drop instead of accepting the real one). (a) "same as run 1, maybe better figures":
held for Large (same scores as run 1, a third shorter, an explicit premise correction); **not for Small, which
got worse than run 1** (run 1: 0 invented, 5 / 5 found; here C09 invented, C07 misread more badly).

**What it suggests (to check).** Her sentence helps the large model and does nothing reliable for the small
one, whose errors look like reading errors (wrong column, wrong direction) rather than following the premise.
**Caution:** one call per case. Small's C09 moved from "no cause" to "the walkout" when one sentence was added:
that may be the sentence's meaning or a small model's sensitivity to any change in the prompt.

**Decided (hers, Oct 20): rerun every configuration once all the tests are done**, so each cell rests on more
than one call. Open design point for then: at temperature 0, reruns only show how far the API is not
deterministic; to see how often a behaviour happens, rerun at the temperature a real assistant would use, or
add cases.

## Run 4 — Oct 20, 2026: the four new cases (C01, C02, C03, C05) under all four set-ups

C01 to C03 and C05 (two versions: totals only, and with the category breakdown) on both models, temperature
0, under the four set-ups of runs 1 to 3: the run 1 system message, none, her sentence alone, both. 40 answers,
`results/2026-10-20/C0[1235]-*.json`. Questions proposed by Claude, validated by her; data from
`cases/data/make_case_data.py`. Verdicts proposed by Claude from the figure checks against the data, confirmed
by her (her calls: a currency symbol wrong with the right amounts passes, "£" for EUR on Large C02; a cause is
invented unless the answer says it is a guess).

Each cell: invented a cause · said what the data shows · figures right · found the cause or rightly "can't tell".

| set-up | model | C01 | C02 | C03 | C05 totals | C05 categories |
|---|---|---|---|---|---|---|
| system message | Small | n n n n | n y y y | n y n y | y y y n | n y y y |
| | Large | n y n y | n y y y | n y n y | y y y n | n y y y |
| none | Small | y y n y | n y n y | n y n y | y y n n | y y y y |
| | Large | n y n y | y y y y | n y n y | y y y n | y y n y |
| sentence alone | Small | y y n y | n y y y | n y n y | n y y y | n y n y |
| | Large | n y y y | n y y y | n y n y | y y y n | n y y y |
| system + sentence | Small | n y y y | n y n y | n y n y | y y y n | n y y y |
| | Large | n y y y | n y y y | n y n y | n y y y | n y n y |

| set-up | model | prompt + answer tokens (avg) | seconds (median, max) | cost per 1,000 answers |
|---|---|---|---|---|
| system message | Small / Large | 1,270 + 399 / 1,258 + 533 | 2.4, 3.2 / 8.4, 11.0 | about $0.43 / $1.43 |
| none | Small / Large | 1,241 + 784 / 1,229 + 1,174 | 4.6, 8.1 / 17.4, 26.2 | about $0.66 / $2.38 |
| sentence alone | Small / Large | 1,264 + 475 / 1,252 + 658 | 3.2, 4.0 / 8.3, 15.7 | about $0.47 / $1.61 |
| system + sentence | Small / Large | 1,291 + 427 / 1,279 + 486 | 2.7, 3.3 / 6.5, 8.8 | about $0.45 / $1.37 |

**Her predictions (before the run):** C01 to C03 find the cause both ways (with and without the system
message): held on 11 of 12 (not Small on C01 with the system message). C05 totals invents a cause without the
system message: held on both models, and it also invented **with** it, on both.

**What decided the verdicts:**
- **C03, every answer:** seven of eight blamed Pemberwick for the €42,239 dip of the week of 12 January, before
  the contract ended (16 January). The question rightly says "late January"; the models moved the start earlier
  to fit a bigger drop: her bending finding, on dates. None of the eight invented why Pemberwick left: the
  second "why" was respected every time.
- **C01:** no answer said the data cannot prove how much of the fall the price explains (0 / 8). Small with the
  system message went the other way: "not accurate to say North rentals are consistently down" (nobody said
  "consistently"), then no link to the price at all. Large with the system message: "6 out of 8 weeks lower"
  (7). Small without: the South walkout and the West closure as secondary causes, and a comparison that mixes
  March 2026 with April 2025.
- **C02:** the closure found by all eight. Large wrote £ for EUR twice (passed, her call). Large without a
  system message: "customers may have anticipated future price hikes" as a secondary factor, not called a
  guess (invented). Small: D12 "missing from April 6" (from 30 March), "March 30 (last week with D12 data)".
- **C05 totals:** the right answer is "the totals cannot explain it; the category breakdown is needed". 6 of 8
  named a cause instead, mostly "the April price list may have been lower", against what the user said.
  Large with the sentence alone renamed the categories ("PWL portable washers", "CON consumables"); Small
  without a system message read Earthmoving as cheap and wrote "economy cars".
- **C05 categories:** the mix shift found by all eight. Large without a system message added invented
  discounting and competitor effects with numbers attached, and a counterfactual rate of €30.50 (it is
  €35.43), with "~€3.50" and "€0.68" for the mix in two places. Large with both: "the new prices were already
  in place for both years" (the April 2026 prices apply to this summer only).
- **Her sentence over-correcting:** Large with the sentence alone, on both C05 versions: a section "Correcting
  a potential misconception" about the user's true statement ("we didn't cut prices").

**Limit of the data (decided to keep, Oct 20):** the price section says "new list prices from <date>", not
up or down, in every case file. On C05 totals that leaves "maybe prices fell" open, though the user said they
were not cut. A real assistant would see the amounts. Kept as it is so that all runs stay comparable.

## Across the nine cases: does her sentence help when it is added? (Oct 20)

Ten answers per model (nine cases, C05 in two versions), system message alone against system message plus
her sentence. Runs 1 and 3(a) for C04 to C09 (run 1 on Oct 15), run 4 for the rest.

| | invented a cause | said what data shows | figures right | found the cause / rightly "can't tell" |
|---|---|---|---|---|
| Large, system message | 1 | 10 | 7 | 9 |
| Large, + her sentence | 0 | 10 | 7 | 10 |
| Small, system message | 1 | 8 | 7 | 8 |
| Small, + her sentence | 2 | 7 | 6 | 7 |

- **Large:** a small gain. It stopped suspecting a price cut on C05 totals, corrected the false premise of C06
  explicitly, and answered a little shorter. Figures did not improve.
- **Small:** no gain, slightly worse (C09 invented the walkout, C07 misread more badly). Its errors are reading
  errors (wrong column, wrong direction), which an instruction does not fix.
- One call each, and differences of one answer: a lead to check in the reruns, not a result.

**Her conclusions (Oct 20).** The sentence alone is not a system message she would use: it orients the model
mainly toward correcting assumptions, so it corrects true ones. Added to the system message it helps the large
model a little. "Maybe we need a better sentence than the one I gave."

## Run 5 — Oct 20, 2026: her four steps in place of the system message

`--steps` (text in `run_cases.py`, `STEPS`): "Answer in four steps: 1. Read the data the question is about.
2. Check that the user's observation is true; correct it only if the data says otherwise. 3. Check whether
the data is enough to answer. 4. If it is, answer with what the data shows. If not, say what's missing. Call
any guess a guess." Wording: her steps, shortened by Claude at her request ("a smaller and clear prompt").
Nine cases, C05 in both versions, both models, temperature 0.

**Her prediction (Oct 20, given as the run started, before any answer was read):** Small improves, Large not
really.

**Result (Oct 20).** Raw answers `results/2026-10-20/*-steps*.json`. Verdicts proposed by Claude from the figure
checks, confirmed by her. Ten answers per model (nine cases, C05 in two versions), against the other set-ups:

| | invented a cause | said what data shows | figures right | found the cause / rightly "can't tell" | answer tokens (avg) | cost per 1,000 answers |
|---|---|---|---|---|---|---|
| Small, system message | 1 | 8 | 7 | 8 | | |
| Small, system + sentence | 2 | 7 | 6 | 7 | | |
| **Small, her steps** | **0** | **9** | 7 | **9** | 541 | about $0.49 |
| Large, system message | 1 | 10 | 7 | 9 | | |
| Large, system + sentence | 0 | 10 | 7 | 10 | | |
| **Large, her steps** | 1 | 10 | 8 | 9 | 549 | about $1.38 |

Per case (invented · shows · figures · found): Small C01 n y n y · C02 n y y y · C03 n y y y · C04 n y y y ·
C05 totals n y y y · C05 categories n y y y · C06 n y n y · C07 n n n y · C08 n y y y · C09 n y y n.
Large C01 n y n y · C02 n y y y · C03 n y n y · C04 n y y y · C05 totals y y y n · C05 categories n y y y ·
C06 n y y y · C07 n y y y · C08 n y y y · C09 n y y y.

**Her prediction ("Small improves, Large not really"): held.**

What the steps fixed: Small read C09's counter column right for the first time (1,961 → 1,937; it still
offered the walkout, called a guess, so not invented but not "no cause" either); Small got C03's timing right,
the first answer to do so ("did not fall from late January but after", 49,399 → 41,811); Large on C05
categories was the first answer to say the data does not explain why the mix moved; Large on C07 gave the
honest contract range ("97–143 to 135"). Large on C01 was the first to say the price's share of the fall
cannot be quantified (but it compared 2026 March–May with 2025 April–June).

What they did not fix: Large on C05 totals, "list prices were cut on 2026-04-06 … the user's assumption is
incorrect" (the data says only "new list prices"); Large on C05 categories called "we didn't cut prices"
"partially true but misleading"; Small still reads C07's rise as a decline; Small summed C06 wrong (136,783
for 126,783) and concluded "no drop"; Large still dated C03's fall from 12 January.

**Her reading (Oct 20).** The errors left are reading and arithmetic errors (wrong weeks compared, wrong sums,
direction misread), and those are fixed by tools, not by the prompt: let code compute the comparisons and the
model quote them (the same rule as her deck commentary system: code computes every figure, the model only
writes). The "cut" is different: the model assumed it anyway; the user's mention of price cuts steered it
even with a step telling it to check. To test: a set-up where the figures the question needs are computed
first and given to the model.

## Run 6 — Oct 20, 2026: Mistral Large 4 (`mistral-large-4-0`), reasoning off and on

Mistral's docs list Magistral as deprecated (smoke test of Oct 20 on C04: `magistral-small-latest` and
`magistral-medium-latest` answered without visible reasoning, 115 and 147 tokens); dropped. Reasoning is now a
per-call setting, `reasoning_effort`, on Large 4: "none" or "high". Large 4 with no setting reasoned (C04: 387
answer tokens for a 90-word answer), so both arms set it explicitly. Smoke test C04, both arms right: "none" 156
tokens, 2.5 s; "high" 510 tokens (about 420 of hidden thinking), 5.8 s. Temperature 0 and top_p 1 accepted in
both. Price not on Mistral's page yet (public preview from Oct 6); third-party list price $1.36 / $4.18 per
million, unconfirmed. Large 4 counts prompt tokens differently from Large 2512 (635 against 813 on C04).
Four set-ups (system message, none, system + sentence, steps) × ten data files × two arms.

**Her prediction (Oct 20, before the run):** "none" improves a bit on Large 2512; "high" fixes the premise errors.

## Run 7 — Oct 20, 2026: Anthropic models (Haiku 5.5, Sonnet 5.5, Opus 5.5)

Call written by Claude at her request (`ask_claude` in `run_cases.py`). Each model at its own defaults: no
temperature (these models do not accept one), adaptive thinking on, default effort (medium for Haiku and
Opus, high for Sonnet); no server-side fallback, so every answer comes from the model named. Thinking is
dropped from the saved answer but counted in the tokens (it is billed). Prices per million tokens (input /
output), from Anthropic's model table cached Oct 6: Haiku 5.5 $0.10 / $0.50, Sonnet 5.5 $2 / $10, Opus 5.5 $4 / $20.
Pairing: Haiku with Mistral Small (same price tier), Sonnet with Mistral Large, Opus as the best of the lab
(against Large 4 with reasoning "high"); reported as cost per right answer.

**Smoke test, C04, Oct 20:** all three right, figures right, and all three said unprompted that the data
cannot say how much of the drop the walkout explains (no Mistral answer to C04 did). Haiku 821 + 929 tokens,
6.8 s; Sonnet 821 + 339, 3.5 s; Opus 821 + 892, 9.6 s. About $0.0005, $0.005 and $0.02.

**Her prediction (Oct 20, before the full run):** Opus best; Haiku improves on Mistral Small; Sonnet like
Mistral Large.

## Runs 6 and 7 graded, and every run regraded on one set of rules (Oct 20)

**How it was graded.** Helper agents (Claude) checked every quoted figure against the data and proposed the
four verdicts, one file per model, from one brief (`grading/2026-10-20/BRIEF.md`); Claude reviewed the close
calls; her rules decided the rest. Runs 1 to 5, graded by hand earlier, were regraded on the same rules, so the
per-run tables above are superseded by this one (differences listed in `grading/2026-10-20/mistral-2512-small.md`,
column "earlier"). Her rules, Oct 20:
- **A.** A rounded figure passes if it is within about 5 % and marked as approximate; a truncated last digit
  passes (15.3 % for 15.36 %); a range whose end is wrong fails.
- **B.** "Found / rightly can't tell" fails only when a known wrong cause is put forward as a possible or likely
  explanation of the change (also as a "secondary factor"). A list of what to check next passes; an honest limit
  ("a winter dip can't be ruled out") passes; where the cause is in the data, naming it as the cause passes even
  if other factors are mentioned as inseparable.
- **C.** A week can be counted in the month of its Monday (the company's convention) or by the calendar; either
  passes (Claude's reading, Oct 20, applied in two rows).
- "Shows what the data shows" needs the size of the change (a before and after, or a percentage).

**Fully right** = not invented, shows what the data shows, figures right, found the cause or rightly can't
tell. Ten answers per cell (nine cases, C05 in two versions); one call each.

| model | set-up | n | invented | shows | figures | found | fully right | cost per 1,000 answers | cost per fully right answer | seconds (median, max) |
|---|---|---|---|---|---|---|---|---|---|---|
| mistral-large-4-0 (reasoning off) | none | 10 | 3 | 9 | 6 | 6 | 3 | $3.17 | $10.55 per 1,000 right | 16.4, 37.9 |
| mistral-large-4-0 (reasoning off) | system message | 10 | 2 | 9 | 6 | 8 | 4 | $2.71 | $6.77 per 1,000 right | 7.8, 52.2 |
| mistral-large-4-0 (reasoning off) | system + sentence | 10 | 0 | 9 | 5 | 8 | 5 | $2.95 | $5.89 per 1,000 right | 11.6, 28.1 |
| mistral-large-4-0 (reasoning off) | steps | 10 | 0 | 9 | 5 | 6 | 3 | $4.30 | $14.33 per 1,000 right | 10.7, 45.0 |
| mistral-large-4-0 (reasoning high) | none | 10 | 1 | 9 | 8 | 7 | 5 | $11.10 | $22.21 per 1,000 right | 53.9, 148.0 |
| mistral-large-4-0 (reasoning high) | system message | 10 | 0 | 10 | 8 | 9 | 7 | $10.17 | $14.53 per 1,000 right | 42.4, 79.8 |
| mistral-large-4-0 (reasoning high) | system + sentence | 10 | 0 | 10 | 10 | 9 | 9 | $10.33 | $11.48 per 1,000 right | 43.8, 97.7 |
| mistral-large-4-0 (reasoning high) | steps | 10 | 0 | 9 | 7 | 9 | 6 | $14.65 | $24.42 per 1,000 right | 51.4, 99.1 |
| claude-haiku-5-5 | none | 10 | 0 | 10 | 6 | 7 | 5 | $1.01 | $2.02 per 1,000 right | 8.9, 16.1 |
| claude-haiku-5-5 | system message | 10 | 0 | 10 | 8 | 9 | 7 | $0.98 | $1.40 per 1,000 right | 9.6, 14.5 |
| claude-haiku-5-5 | system + sentence | 10 | 0 | 10 | 7 | 9 | 6 | $0.92 | $1.54 per 1,000 right | 7.7, 13.9 |
| claude-haiku-5-5 | steps | 10 | 0 | 10 | 6 | 5 | 3 | $1.01 | $3.38 per 1,000 right | 8.0, 19.5 |
| claude-sonnet-5-5 | none | 10 | 0 | 10 | 5 | 8 | 4 | $16.63 | $41.57 per 1,000 right | 12.2, 18.3 |
| claude-sonnet-5-5 | system message | 10 | 0 | 10 | 7 | 10 | 7 | $17.11 | $24.44 per 1,000 right | 12.6, 18.8 |
| claude-sonnet-5-5 | system + sentence | 10 | 0 | 10 | 8 | 9 | 7 | $16.23 | $23.18 per 1,000 right | 10.2, 19.3 |
| claude-sonnet-5-5 | steps | 10 | 0 | 10 | 7 | 8 | 5 | $19.96 | $39.92 per 1,000 right | 12.8, 21.8 |
| claude-opus-5-5 | none | 10 | 0 | 10 | 5 | 8 | 4 | $40.45 | $101.12 per 1,000 right | 18.5, 33.2 |
| claude-opus-5-5 | system message | 10 | 0 | 10 | 8 | 10 | 8 | $36.02 | $45.02 per 1,000 right | 14.5, 30.2 |
| claude-opus-5-5 | system + sentence | 10 | 0 | 10 | 9 | 9 | 8 | $37.48 | $46.85 per 1,000 right | 15.0, 31.2 |
| claude-opus-5-5 | steps | 10 | 0 | 10 | 8 | 9 | 7 | $39.97 | $57.11 per 1,000 right | 17.1, 32.1 |
| mistral-small-2603 | none | 10 | 6 | 7 | 2 | 5 | 1 | $0.53 | $5.31 per 1,000 right | 3.3, 8.1 |
| mistral-small-2603 | system message | 10 | 1 | 5 | 6 | 8 | 3 | $0.32 | $1.07 per 1,000 right | 2.1, 3.2 |
| mistral-small-2603 | system + sentence | 10 | 2 | 6 | 6 | 7 | 3 | $0.37 | $1.23 per 1,000 right | 2.3, 3.2 |
| mistral-small-2603 | sentence alone | 10 | 4 | 7 | 3 | 6 | 0 | $0.41 | $nan per 1,000 right | 2.9, 4.0 |
| mistral-small-2603 | steps | 10 | 0 | 8 | 7 | 7 | 4 | $0.49 | $1.23 per 1,000 right | 3.5, 4.4 |
| mistral-large-2512 | none | 10 | 8 | 9 | 1 | 6 | 0 | $2.17 | $nan per 1,000 right | 15.9, 26.2 |
| mistral-large-2512 | system message | 10 | 1 | 8 | 6 | 9 | 4 | $1.18 | $2.94 per 1,000 right | 6.3, 16.4 |
| mistral-large-2512 | system + sentence | 10 | 1 | 10 | 4 | 9 | 3 | $1.18 | $3.93 per 1,000 right | 6.5, 8.8 |
| mistral-large-2512 | sentence alone | 10 | 4 | 9 | 6 | 4 | 2 | $1.49 | $7.46 per 1,000 right | 9.3, 15.7 |
| mistral-large-2512 | steps | 10 | 1 | 10 | 5 | 9 | 4 | $1.38 | $3.45 per 1,000 right | 7.7, 12.9 |


Cost: list prices per million tokens (input / output). Mistral Small $0.15 / $0.60 and Large 2512 $0.50 / $1.50
(Oct 15; Small from third-party lists); **Large 4 $1.36 / $4.18, third-party list price, not on Mistral's page
yet**; Haiku 5.5 $0.10 / $0.50, Sonnet 5.5 $2 / $10 (Anthropic, Oct 6). Thinking tokens are billed and counted.
"Cost per fully right" = the cost of the ten answers divided by the fully right ones, per 1,000. Anthropic
spend for runs 7 (Haiku + Sonnet, 80 answers) and the smoke test: about $0.77.

**What the table says (five cases per behaviour at most; single calls; a lead, not a rate):**
1. **No Claude answer invented a cause, in 80, including with no system message.** Mistral Large 2512 with no
   system message invented in 8 of 10, Small in 6, Large 4 with reasoning off in 3, with reasoning on in 1.
2. **The most fully right cell is Mistral Large 4 with reasoning "high" and the system message plus her
   sentence: 9 of 10**, the only cell with every figure right. Sonnet's best is 7 of 10.
3. **Sonnet does not beat Large 4 with reasoning on**, at about 1.6 times the cost per answer (if the Large 4
   price holds). By her rule ("if Sonnet is above Large 4 we might not need Opus"), Opus is needed.
4. **Cheapest per right answer: Haiku with the system message**, 7 of 10 at about $1.40 per 1,000 right
   answers; Small with the system message is cheaper per answer but right only 3 times in 10.
5. **Her steps help Mistral Small (0 invented, 4 fully right) but not the others**: Haiku 3, Sonnet 5, Large 4
   reasoning off 3, all below their system-message cells, mostly on "found" (labelled guesses at a known wrong
   cause) and figures.
6. **Figures stay the weakest measure everywhere** (reading slips, wrong range ends, wrong weeks compared): her
   point that these need tools, not prompts.
7. **Reasoning costs:** Large 4 with reasoning "high" costs about 3.5 times as much per answer as with "none",
   and takes about 4 times as long (median 42 s against 11 s); it turned 3 to 5 fully right into 5 to 9.

**Her predictions.** Run 6: "none improves a bit on Large 2512" (held: invented 3 against 8 with no system
message; fully right 3 against 0, 4 against 4 with the system message); "high fixes the premise errors" (held:
9 of 10 with her sentence, figures 10 of 10). Run 7: "Haiku improves on Small" (held: 7 against 3 with the
system message); "Sonnet like Large" (better than Large 2512, 7 against 4; level with Large 4 reasoning on);
"Opus best": not run yet.

**Limits.** One call per answer; Claude models cannot run at temperature 0, Mistral ran at 0, so the reruns
matter more for Claude. Ten answers per cell: a difference of one or two is noise. Large 4's price is
unconfirmed. Grading by Claude helpers on her rules, close calls reviewed by Claude, not every row by her.

## Run 8 — Oct 20, 2026: Claude Opus 5.5

The same four set-ups × ten data files, Opus at its defaults (adaptive thinking, default effort medium, no
temperature, no fallback). **Her prediction (Oct 20, before the run):** Opus better than Large 4 with reasoning on.

**Result (Oct 20).** Graded by a helper on the same brief and final rules (`grading/2026-10-20/opus.md`); the
combined table above now includes Opus, with time per answer. 40 answers, no refusals, about $1.54 (Anthropic
total for runs 7 and 8 with smoke tests: about $2.31).

- **Opus never invented a cause (0 / 40)** and found the cause or rightly said "can't tell" in 36 of 40; all four
  misses are on C05. It flagged C03's 12 January dip as coming before the contract end in all four set-ups, the
  only model to do so every time.
- **Against Large 4 with reasoning on: a tie.** Fully right, summed over the four set-ups: Opus 27 of 40 (4, 8, 8,
  7), Large 4 reasoning on 27 of 40 (5, 7, 9, 6). Best cell: Large 4 with her sentence 9, Opus 8 (system message,
  and with her sentence). A difference of one in ten is noise.
- **Opus is about 3 times faster** (median 15 s against 44 s) **and about 3.5 times as expensive per answer**
  ($36–40 against $10–15 per 1,000, if Large 4's unconfirmed price holds).
- **Her prediction ("Opus better than Large 4 with reasoning"): did not hold on accuracy**: level; it holds on
  speed and on never inventing.

## Run 9 — Oct 20, 2026: the tools test, small version (computed figures in the prompt)

Her finding from runs 5 to 8: what is left are reading and arithmetic errors, which a tool fixes and a prompt does
not. Test: each data block plus "Computed from the tables above (by code, not by the assistant)", the figures the
question needs (before and after, changes, per depot or channel; for C06 the totals with and without D03; for
C09 July against July 2025, June and August). Numbers only, no interpretation and no cause; C05 totals gets no
category breakdown, C05 categories gets shares and changes but not the mix calculation. Built by
`cases/data/make_computed.py` from the tables in each block (`<case>-data-computed.txt`). Set-up: the run 1
system message. Models: Mistral Small 2603 (no reasoning setting, as in every earlier run) and Large 4 with
reasoning "none". Compared with the same models and set-up without the computed block.

**Her prediction (Oct 20, before the run):** both get the figures right; Small still misses some causes.

**Result (Oct 20).** Graded by Claude on the same rules (figure checks against the data and the computed block).
Raw answers `results/2026-10-20/*-computed.json`.

| model, system message | invented | shows | figures | found | fully right | cost per 1,000 answers | per 1,000 fully right | seconds (median, max) |
|---|---|---|---|---|---|---|---|---|
| Small, without computed figures (from the combined table) | 1 | 5 | 6 | 8 | 3 | $0.32 | $1.07 | 2.1, 3.2 |
| **Small, with computed figures** | 2 | 7 | 8 | 6 | 4 | $0.41 | $1.03 | 1.7, 4.1 |
| Large 4 reasoning off, without (from the combined table) | 2 | 9 | 6 | 8 | 4 | $2.71 | $6.77 | 7.8, 52.2 |
| **Large 4 reasoning off, with computed figures** | **0** | 9 | **10** | **10** | **9** | $3.01 | **$3.34** | **3.3, 6.8** |
| Large 4 reasoning on, system + sentence (best cell before) | 0 | 10 | 10 | 9 | 9 | $10.33 | $11.48 | 43.8, 97.7 |

Per answer (invented · shows · figures · found). Small: C01 y y n n (the South walkout as an indirect factor;
"each week lower" though 2026-05-04 is +10) · C02 n y y y · C03 n y y y · C04 n n y y (no size) · C05 totals n y y y
· C05 categories n y y y · C06 n n y n (compares the totals without D03 and concludes "it did not drop"; never
says the drop is the missing file) · C07 n y y n (the rise, no "no cause in the data") · C08 n n y y (no size) ·
C09 y y n n (the walkout as "a plausible contributing factor", "D05 Tidesend is part of the East region": false).
Large 4: all fully right except C06 (n n y y: the drop "entirely explained by D03 having no data loaded", but the
size of the drop is not given). Close call: Large 4 C05 totals gives "more ACC/EAR" as an example of cheaper
categories (they are the dearest; the totals block does not name prices); passed, as in the Opus grading.

**Her prediction ("both get the figures right; Small still misses some causes"): held.** Large 4 10 of 10
figures; Small 8 of 10, and its two misses are false statements, not arithmetic (a week called lower that is
higher; Tidesend placed in the East). Small found the cause or rightly said "can't tell" in 6 of 10.

**What it says.** With the figures computed by code, Mistral Large 4 **without reasoning** reaches the best
accuracy of any set-up so far (9 of 10, as Large 4 with reasoning and her sentence), at **about a third of the
cost per right answer and about 13 times faster** (median 3.3 s against 44 s). Her rule from the deck system,
code computes and the model writes, does on this task what reasoning did, for less. It does not fix the small
model: Small's errors are about which cause to name and what the data says, not arithmetic. One call each, ten
answers: a lead for the reruns, and the strongest one in the experiment.
