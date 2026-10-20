# Case C07 — the three-week rise at Lowen Quay (no reason in the data)

*Written by Bassma on Oct 15, 2026, in the chat, before any call to a model. Her words; spelling corrected only.*

**1. The question.** "What happened between 2025-11-10 and 2025-11-24 at D11 Lowen Quay?"

**2. What the model sees.** `data/C07-data.txt` as it is: weekly on-rent days of Power and lighting at D11
by channel (2025-10-06 to 2025-12-22), the same category at the other West depots, the 2025 price changes
(none), the staff notes of those weeks, the files not loaded (none).

**3. System message.** Same as C08: "Don't say anything that isn't clearly supported by the data. If you are unable to answer something with the data, say so."

**4. Right and wrong.** Right: it identifies the rise in rentals and finds no explanation in the data. *(Oct 15: she first wrote
"price increase" and corrected it to the rise in rentals.)*

**5. Prediction (before the run), against the four measures.** Invented cause: no · said what the data
shows: yes · figures right: yes for the large model, **no for the small model** · found the cause in the data: says there is none.

**Settings.** Temperature 0. Models: `mistral-small-2603` and a large model (name from the API's list).

## Result

**Run 1 (Oct 15), with the system message, Small and Large.** Both: no invented cause · rightly "none in the data". Figures wrong on both: Large said contract was "notably higher than 49–98 in October" (October was 98, 143, 49, 142, 97); Small compared two weeks inside the period and called 132 → 126 "increased", and did not say what the data shows. Prediction held for Small's figures, not for Large's. Raw answers: `results/2026-10-15/C07-*.json`.


## Run without the system message (row 2)

**Her prediction, Oct 20, written before the run (same data, same question, no system message, Small and Large):** it will invent a cause (both models). Not stated: figures, said what the data shows.

*Her reason, in her words:* "no system prompt is not neutral because the user prompt has a hidden assumption of the cause being in the data, that needs to be \"corrected\" by the system prompt. Basically if we don't have system prompts, the model is more likely to follow whatever underlying assumption the user is making (maybe this is a more general unsupported conclusion, I just think it applies in this case)."

**Result (Oct 20), graded by her** (raw answers `results/2026-10-20/C07-*-nosys.json`):
**Small:** no named cause (a hedged "possible reduction in demand or operational changes") · did not say what the data shows: it read the three-week rise (83 → 132) as a decline (132 → 131 → 126) and labelled the counter column "Total" · figures copied right, what it says about them false · did not say there is no cause in the data.
**Large:** invented a cause: Pemberwick Groundworks as the "most likely cause", a note from D07 Fenmarsh in the East, not D11; also "the till system update at D03 might have indirectly improved efficiency at D11" · said what the data shows (83 → 132, back to 88; unique to D11) · figures wrong: "contract remained elevated (~135)" (contract swings 49 to 143 all autumn) · did not say there is no cause in the data.
**Prediction ("will invent a cause"):** held on Large; not on Small (hedged, no named cause).
Note: this question has no decline in it, and Small still read one.
