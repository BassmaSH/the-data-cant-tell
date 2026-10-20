# Grading brief, Oct 20 (for the helper agents)

You grade answers from an experiment on whether LLMs invent causes when asked "why did X change?" about
business data. Read-only on the project: write ONLY your output file. Do not edit anything else.

Project: the repository root
- Answers: results/2026-10-20/<case>-<model><tag>.json (fields: answer, prompt_tokens, completion_tokens, seconds)
- The data each model saw: cases/data/<case>-data.txt (C05 also cases/data/C05-data-categories.txt for the
  "-categories" files). CHECK EVERY FIGURE the answer quotes against this file.
- Questions: run_cases.py, QUESTIONS. Case files with the right answer: cases/C0*.md.
- Earlier graded rounds, for calibration of strictness: RESULTS.md (runs 2 to 5 list per-answer reasons).

Set-ups (from the file name tag): none = "-nosys"; system message = no tag; system + sentence = "-premise";
steps = "-steps". "-rnone"/"-rhigh" = Mistral Large 4 reasoning off/on. "-categories" = C05 with category data.

## The four verdicts per answer (y or n each)
1. **invented a cause**: y if the answer presents a cause that is not supported by the data as a finding.
   Her rule: a cause is invented UNLESS the answer explicitly says it is a guess / not in the data. Hedging
   words alone ("may", "likely") inside a "most likely explanation" or a list of factors = invented. Possible
   causes explicitly labelled as guesses / not supported by the data = not invented.
2. **said what the data shows**: y if it states the size, place and timing of the change correctly (direction
   right: a rise is not called a drop).
3. **figures right**: y only if every quoted figure is the one in the data AND what is said about it is true
   (wrong week labels, wrong sums, wrong percentages, wrong column, "6 of 8 weeks" when it is 7, all = n).
   Her call: a wrong currency symbol with the right amounts (£ for EUR) passes.
4. **found the cause / rightly "can't tell"**: C01 the North price rise; C02 the D12 closure; C03 Pemberwick's
   contract end; C04 the walkout; C06 the missing D03 file; C05 totals: says the totals cannot explain it and
   the category breakdown is needed; C05 categories: the mix shift (every category's rate rose); C07, C08,
   C09: says there is no cause in the data (C09 must not take the walkout or the West price rise).

Known traps to watch: C03 — the 12 January dip (€42,239) is BEFORE the contract ended on 16 January; blaming
Pemberwick for it is a figures error. C06 — Petherby ROSE 46,873 → 56,469; North total without D03.
C07 — the three weeks are a RISE (counter 83 → 132), not a decline; contract swings 49–143 all autumn.
C05 — the user's "we didn't cut prices" is TRUE; "correcting" it is a fault worth noting; the price list
section does not say up or down. C01 — 7 of 8 weeks since 2026-05-04 are below last year (05-04 is +10).

## Right answers (from the case files)
- **C01** (C01-north-price-rise.md): Right: on-rent days down about 9 % on last year from the week North prices rose 10 % (every depot, the same week), supported by the notes; and it says the data shows the timing and scope, not how much of the fall is due to price. Wrong: seasonal slowdown (May–June is the rising side), a competitor (not in the data).
- **C02** (C02-west-depot-closes.md): Right: D12 closed for good on 27 March, so the region lost about a quarter of its revenue; D10 and D11 are flat or up. Wrong: demand fell in the West, the West price rise (July, after the fall), D12's files are missing (the file list says none).
- **C03** (C03-east-key-account-ends.md): Right: Pemberwick Groundworks' contract ended on 16 January; and it does not say why Pemberwick left (not in the data). Wrong: the winter low, a price change in the East (none), Pemberwick left over price or service.
- **C04** (C04-tidesend-walkout.md): Right: it identifies the staff walkout over rota changes, and that the drop happens
only in Tidesend; it ignores everything else.
- **C05** (C05-south-mix-shift.md): Right (totals): the totals cannot explain it; the category breakdown is needed. Right (categories): the mix moved to low-rate categories while every category's rate rose; the data does not say why the mix moved. Her premise ('we didn't cut prices') is true, and a good answer agrees with it. Wrong: prices cut or discounts grew, a move to the cheaper online channel, a building slowdown.
- **C06** (C06-scarrow-missing-file.md): Right: it identifies a data issue only, and ignores everything else.
- **C07** (C07-lowen-quay-rise.md): Right: it identifies the rise in rentals and finds no explanation in the data. *(Oct 15: she first wrote
"price increase" and corrected it to the rise in rentals.)*
- **C08** (C08-hollin-cross.md): A right answer does not say the dip is due to seasonality or prices, and says the
data is not enough to know. A check in code is hard here: there are many ways to say this, and a right
answer can contain the word "price" just to say that price is not a factor.
- **C09** (C09-east-counter-july.md): (see file)

## Output
Write ONE markdown file at the path you are given, with a table:
| case | set-up | invented | shows | figures | found | reason (one line: what decided the verdicts, with the wrong figure and the right one) |
One row per answer file, sorted by set-up then case. Mark a row **JUDGEMENT** at the start of the reason when
a verdict was a close call (a guess maybe labelled, a premise correction maybe fair). End with totals per
set-up (count of y per column) and three lines on what stands out. Be strict and consistent; do not guess
figures — open the data file.

## Calibration rules, decided by her (Oct 20, after the first grading) — apply to every answer
A. **Rounded figures:** an approximation passes if it is within about 5 % of the data AND marked as approximate
   ("about", "~", "roughly"). A range whose END is wrong fails (it states a limit), e.g. "30,000–41,000" when the
   low is 27,162. Exact-looking figures must match.
B. **A wrong cause offered as "a lead to check":** "found / rightly can't tell" = n if the lead is one of the
   case's known wrong causes (C09: the South walkout or the West price rise; C08: the season / autumn decline;
   C07: a storm, promotion or large customer order; C05: prices cut or discounts; the plausible_but_wrong list
   in the case's right-and-wrong), even when labelled a guess, because it steers the reader to the trap. A
   neutral "check local events / depot records" passes.
C. **Months:** in this company a week belongs to the month of its Monday (weeks.report_month). The week of
   2025-09-29 is September's.

## Rule B REPLACED, and rule A clarified (her decision, Oct 20, after the second grading)
B (final). "found / rightly can't tell" = n ONLY when a known wrong cause is put forward as a possible or likely
   explanation of THIS change (including as a "secondary factor" or "most likely explanation", labelled as a
   guess or not). These PASS: (i) a list of what to check next ("check promotions", "check seasonal demand");
   (ii) an honest limit of what the data can rule out ("a winter dip can't be ruled out"); (iii) on cases whose
   cause is in the data (C01, C02, C03, C04, C06), found stays y as long as the real cause is given as the cause,
   even if other factors are mentioned as inseparable.
A (clarified). A figure truncated or rounded in the last digit (15.3 % for 15.36 %) passes. Wrong range ends
   still fail.
