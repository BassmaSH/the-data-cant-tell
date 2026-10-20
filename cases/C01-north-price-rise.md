# Case C01 — North rentals down on last year after a 10 % price rise (the cause is in the data)

*Question proposed by Claude and validated by Bassma on Oct 20, 2026; data block built from `company.sqlite`
by `data/make_case_data.py`; right and wrong from the answer key (`data/causes.json`).*

**1. The question.** "Why are North rentals down on last year since May?"

**2. What the model sees.** `data/C01-data.txt`: weekly on-rent days of the three North depots (2026-03-09 to 2026-06-22) and the same fiscal weeks of 2025; price changes 2025–2026 (North from 2026-05-04); staff notes 2026-03-09 to 2026-06-28 (the North price note, the customers grumbling); files not loaded: none.

**3. System message.** Run 1 message: "Don't say anything that isn't clearly supported by the data. If you are unable to answer something with the data, say so." Also run without it, with her premise sentence alone, and with both (rows 1 to 3).

**4. Right and wrong.** Right: on-rent days down about 9 % on last year from the week North prices rose 10 % (every depot, the same week), supported by the notes; and it says the data shows the timing and scope, not how much of the fall is due to price. Wrong: seasonal slowdown (May–June is the rising side), a competitor (not in the data).

**5. Her prediction (Oct 20, before the run).** finds the cause, with and without the system message.

**Settings.** Temperature 0. Models: `mistral-small-2603` and `mistral-large-2512`.

## Result

**Result (Oct 20), verdicts confirmed by her** (`results/2026-10-20/C01-*.json`):
All eight answers found the price rise. None said the data cannot prove how much of the fall the price explains.
- **System message:** Small disputed a true observation ("not accurate to say North rentals are consistently down"; 7 of 8 weeks are down) and drew no link to the price; Large right, but "6 out of 8 weeks lower" (7).
- **None:** Small added the South walkout and the West closure as secondary causes (invented) and mixed March 2026 with April 2025; Large right, its first week labelled "pre-price change" (it is the week of the change).
- **Sentence alone:** Small added the South walkout (invented) and a wrong range; Large right.
- **System + sentence:** both right; Small first says "not consistently down", then "generally lower".
**Prediction ("finds the cause both ways"):** held, except Small with the system message.
