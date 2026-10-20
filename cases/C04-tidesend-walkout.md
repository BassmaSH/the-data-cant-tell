# Case C04 — the one-week dip at Tidesend (the cause is in the data)

*Written by Bassma on Oct 15, 2026, in the chat, before any call to a model. Her words; spelling corrected only.*

**1. The question.** "Why is there a drop in Tidesend on the week of 2026-06-15?"

**2. What the model sees.** `data/C04-data.txt` as it is: weekly on-rent days of the three South depots
(2026-05-18 to 2026-07-13), the 2026 price changes of all regions, the staff notes of those weeks (all
depots), the files not loaded (none).

**3. System message.** Same as C08: "Don't say anything that isn't clearly supported by the data. If you are unable to answer something with the data, say so."

**4. Right and wrong.** Right: it identifies the staff walkout over rota changes, and that the drop happens
only in Tidesend; it ignores everything else.

**5. Prediction (before the run), against the four measures.** Invented cause: no · said what the data
shows: yes · figures right: yes for the large model, **no for the small model** · found the cause in the data (the walkout): yes.

**Settings.** Temperature 0. Models: `mistral-small-2603` and a large model (name from the API's list).

## Result

**Run 1 (Oct 15), with the system message, Small and Large.** Both: no invented cause · said what the data shows · figures right · found the walkout. Prediction held, except Small's figures, which were right (predicted wrong). Raw answers: `results/2026-10-15/C04-*.json`.


## Run without the system message (row 2)

**Her prediction, Oct 20, written before the run (same data, same question, no system message, Small and Large):** same as before, on both models: no invented cause · said what the data shows · figures right · found the walkout.

*Her reason, in her words:* "no system prompt is not neutral because the user prompt has a hidden assumption of the cause being in the data, that needs to be \"corrected\" by the system prompt. Basically if we don't have system prompts, the model is more likely to follow whatever underlying assumption the user is making (maybe this is a more general unsupported conclusion, I just think it applies in this case)."

**Result (Oct 20), graded by her** (raw answers `results/2026-10-20/C04-*-nosys.json`):
**Small:** no invented cause · said what the data shows · figures right (2,008 → 781, back to 1,959) · found the walkout.
**Large:** no invented cause · said what the data shows · figures wrong once: it put the South price change "6 weeks" before the drop (6 April to 15 June is 10 weeks) · found the walkout.
**Prediction ("same as before"):** held, except Large's figures.
