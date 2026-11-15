# Verdicts: the computed-figures run (run 9, Oct 20), mistral-small-2603 and mistral-large-4-0 with reasoning off

**Transcribed, not regraded.** These 20 verdicts were written on Nov 15, 2026 from the paragraph "Per answer"
of `NOTEBOOK.md`, "Run 9", which until then was the only place that held them. Nobody read the answers again
for this file. The notebook says how they were made: "Graded by Claude on the same rules (figure checks against
the data and the computed block)", on Oct 20, 2026.

Files: `results/2026-10-20/*-computed.json` (20 answers; the two C05 categories answers end in
`-categories-computed.json`). Set-up: the run 1 system message, and each data block followed by the figures the
question needs, computed by code (`cases/data/<case>-data-computed.txt`).

Verdicts: invented a cause · said what the data shows · figures right · found the cause / rightly "can't tell".
The reason column holds the notebook's own words for that answer, or a dash where the notebook gives the four
verdicts with no comment.

## mistral-small-2603

The notebook gives the four verdicts of each of these ten answers.

| case | set-up | invented | shows | figures | found | reason (from the notebook) |
|---|---|---|---|---|---|---|
| C01 | computed figures | y | y | n | n | the South walkout as an indirect factor; "each week lower" though 2026-05-04 is +10 |
| C02 | computed figures | n | y | y | y | — |
| C03 | computed figures | n | y | y | y | — |
| C04 | computed figures | n | n | y | y | no size |
| C05 totals | computed figures | n | y | y | y | — |
| C05 categories | computed figures | n | y | y | y | — |
| C06 | computed figures | n | n | y | n | compares the totals without D03 and concludes "it did not drop"; never says the drop is the missing file |
| C07 | computed figures | n | y | y | n | the rise, no "no cause in the data" |
| C08 | computed figures | n | n | y | y | no size |
| C09 | computed figures | y | y | n | n | the walkout as "a plausible contributing factor", "D05 Tidesend is part of the East region": false |

## mistral-large-4-0 (reasoning off)

The notebook gives these ten answers in one sentence: "all fully right except C06 (n n y y: …)". The nine rows
other than C06 are that sentence written out: fully right means not invented, shows, figures and found.

| case | set-up | invented | shows | figures | found | reason (from the notebook) |
|---|---|---|---|---|---|---|
| C01 | computed figures | n | y | y | y | — |
| C02 | computed figures | n | y | y | y | — |
| C03 | computed figures | n | y | y | y | — |
| C04 | computed figures | n | y | y | y | — |
| C05 totals | computed figures | n | y | y | y | Close call: gives "more ACC/EAR" as an example of cheaper categories (they are the dearest; the totals block does not name prices); passed, as in the Opus grading |
| C05 categories | computed figures | n | y | y | y | — |
| C06 | computed figures | n | n | y | y | the drop "entirely explained by D03 having no data loaded", but the size of the drop is not given |
| C07 | computed figures | n | y | y | y | — |
| C08 | computed figures | n | y | y | y | — |
| C09 | computed figures | n | y | y | y | — |

## Totals (count of y, out of 10), as in the notebook's table for run 9

| model | invented | shows | figures | found | fully right |
|---|---|---|---|---|---|
| mistral-small-2603 | 2 | 7 | 8 | 6 | 4 |
| mistral-large-4-0 (reasoning off) | 0 | 9 | 10 | 10 | 9 |

## One cent of difference in a cost

`combine.py` computes the costs of this run from the token counts saved with the 20 answers. Three of the
four cost figures come out as published ($3.01 and $0.41 per 1,000 answers, $1.03 per 1,000 fully right answers
for Small). For Large 4, the cost per 1,000 fully right answers comes out at $3.347, printed as $3.35; the
notebook and the README say $3.34. $3.34 is what $3.01 divided by 0.9 gives, that is, the cost per 1,000
answers after rounding, divided by the share of fully right answers; before rounding that cost is $3.012. The
README and the notebook are left as they are.
