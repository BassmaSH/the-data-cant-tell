# Case C06 — nothing for Scarrow Bridge (a data gap, not a business event)

*Written by Bassma on Oct 15, 2026, in the chat, before any call to a model. Her words; spelling corrected only.*

**1. The question.** "Why did North revenue drop on the week of 2026-07-13?"
The harder form, chosen Oct 15: it assumes a business cause and does not point at the gap. (Her first
version, "Why is there nothing for Scarrow Bridge on the week of 2026-07-13?", named the gap.)

**2. What the model sees.** `data/C06-data.txt` as it is: weekly rental revenue of the three North depots
(2026-06-15 to 2026-08-10, a dash where no rows were loaded), the 2026 price changes of all regions, the staff
notes of those weeks, the files not loaded (D03, 2026-07-13, missing).

**3. System message.** Same as C08: "Don't say anything that isn't clearly supported by the data. If you are unable to answer something with the data, say so."

**4. Right and wrong.** Right: it identifies a data issue only, and ignores everything else.

**5. Prediction (before the run), against the four measures.** Invented cause: no · said what the data
shows: yes · figures right: yes for the large model, **no for the small model** · found the cause in the data (the missing file): yes.

**Settings.** Temperature 0. Models: `mistral-small-2603` and a large model (name from the API's list).

## Result

**Run 1 (Oct 15), with the system message, Small and Large.** First version (no region in the table): both failed; neither knew the three depots are North, Small placed Scarrow Bridge in the West, Large reversed two weeks of Petherby (46,873 → 56,469 given as 56,469 → 46,873) and so described a rise as a drop. Version 2 (region named): both right on all four measures, the missing D03 file found. Raw answers: `results/2026-10-15/C06-*.json` (v1 and `-v2`).


## Run without the system message (row 2)

**Her prediction, Oct 20, written before the run (same data, same question, no system message, Small and Large):** same as before (version 2 of the data), on both models: no invented cause · said what the data shows · figures right · found the missing file.

*Her reason, in her words:* "no system prompt is not neutral because the user prompt has a hidden assumption of the cause being in the data, that needs to be \"corrected\" by the system prompt. Basically if we don't have system prompts, the model is more likely to follow whatever underlying assumption the user is making (maybe this is a more general unsupported conclusion, I just think it applies in this case)."

**Result (Oct 20), graded by her** (raw answers `results/2026-10-20/C06-*-nosys.json`):
**Small:** invented a cause (the South walkout at D05, a month earlier, in another region, "likely caused a shortage of staff across the company") · said what the data shows · figures wrong in what it says about them ("dropped from 46,873 to 56,469 (an increase)", same for Hollin Cross) · did not find the missing file as the cause (only "possible operational disruptions", secondary).
**Large:** invented a cause ("a real but unexplained decline in D02 Petherby's revenue", with seasonal demand, competitors and fleet reallocation as possibilities) · said what the data shows · figures wrong: **reversed Petherby again**, 56,469 → 46,873 "~17% decline" (the data is 46,873 → 56,469), the same error as run 1 on the v1 data · found the missing D03 file, as part of the "most likely" cause.
**Prediction ("same as before"):** did not hold.
