# Case C03 — East contract revenue falls when key account Pemberwick ends its contract (cause in the data; why it left is not)

*Question proposed by Claude and validated by Bassma on Oct 20, 2026; data block built from `company.sqlite`
by `data/make_case_data.py`; right and wrong from the answer key (`data/causes.json`).*

**1. The question.** "Why did East contract revenue fall from late January 2026?"

**2. What the model sees.** `data/C03-data.txt`: weekly contract-channel revenue of the three East depots and the East total (2025-11-03 to 2026-03-30); price changes 2025–2026 (none in the East); staff notes 2025-11-03 to 2026-04-05 (Pemberwick will not renew, contract ends 16 January; final collections 20 and 21 January); files not loaded: none.

**3. System message.** Run 1 message: "Don't say anything that isn't clearly supported by the data. If you are unable to answer something with the data, say so." Also run without it, with her premise sentence alone, and with both (rows 1 to 3).

**4. Right and wrong.** Right: Pemberwick Groundworks' contract ended on 16 January; and it does not say why Pemberwick left (not in the data). Wrong: the winter low, a price change in the East (none), Pemberwick left over price or service.

**5. Her prediction (Oct 20, before the run).** finds the cause, with and without the system message.

**Settings.** Temperature 0. Models: `mistral-small-2603` and `mistral-large-2512`.

## Result

**Result (Oct 20), verdicts confirmed by her** (`results/2026-10-20/C03-*.json`):
All eight answers found Pemberwick; none invented why Pemberwick left.
- **The shared error:** seven of eight blamed Pemberwick for the dip of the week of 12 January (€42,239), before the contract ended on 16 January; the question says "late January". Large with the system message used the right weeks (26 January to 2 February) but called D08's rise (12,669 → 13,303) part of the drop. Large without a system message listed D07's weeks out of order.
**Prediction ("finds the cause both ways"):** held; figures wrong in every answer.
