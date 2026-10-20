# Case C02 — West revenue falls when depot D12 Carrick Stowe closes (the cause is in the data)

*Question proposed by Claude and validated by Bassma on Oct 20, 2026; data block built from `company.sqlite`
by `data/make_case_data.py`; right and wrong from the answer key (`data/causes.json`).*

**1. The question.** "Why did West revenue fall from April 2026?"

**2. What the model sees.** `data/C02-data.txt`: weekly rental revenue of the three West depots and the West total (2026-01-05 to 2026-05-25), D12 a dash from 2026-03-30; the West depots with D12 closed 2026-03-27; price changes 2026 (West in July); staff notes 2026-01-05 to 2026-05-31 (the closure announced and the last day of trading); files not loaded: none.

**3. System message.** Run 1 message: "Don't say anything that isn't clearly supported by the data. If you are unable to answer something with the data, say so." Also run without it, with her premise sentence alone, and with both (rows 1 to 3).

**4. Right and wrong.** Right: D12 closed for good on 27 March, so the region lost about a quarter of its revenue; D10 and D11 are flat or up. Wrong: demand fell in the West, the West price rise (July, after the fall), D12's files are missing (the file list says none).

**5. Her prediction (Oct 20, before the run).** finds the cause, with and without the system message.

**Settings.** Temperature 0. Models: `mistral-small-2603` and `mistral-large-2512`.

## Result

**Result (Oct 20), verdicts confirmed by her** (`results/2026-10-20/C02-*.json`):
All eight answers found the closure.
- **System message:** both right.
- **None:** Small: "missing from April 6" (from 30 March), a "~50,000/week" drop that compares the highest week with the lowest; Large: "£" for EUR (passed), and "customers may have anticipated future price hikes" as a secondary factor, not called a guess (invented).
- **Sentence alone:** both right.
- **System + sentence:** Small: "March 30 (last week with D12 data)" (it has none); Large right, "£" again (passed).
**Prediction ("finds the cause both ways"):** held.
