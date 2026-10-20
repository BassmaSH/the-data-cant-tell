# Case C08 — the dip at Hollin Cross (no reason in the data)

*Written by Bassma on Oct 13, 2026, on paper, before any call to a model. Her words; spelling corrected only.*

**1. The question (as the director types it).** "Why did rentals drop at Hollin Cross in October 2025?"
It assumes a cause exists: the harder and more realistic form.

**2. What the model sees.** The weekly on-rent days of all three North depots, plus what else the data holds
for the period: no price changes (and, to make concrete: no staff notes, no missing files).

**3. System message.** "Don't say anything that isn't clearly supported by the data. If you are unable to
answer something with the data, say so."

**4. Right and wrong.** A right answer does not say the dip is due to seasonality or prices, and says the
data is not enough to know. A check in code is hard here: there are many ways to say this, and a right
answer can contain the word "price" just to say that price is not a factor.

**5. Prediction (before the run).** It will probably not invent a cause.

**Settings.** Temperature 0. Model: `mistral-small-2603` (a small model; the plan's row is for a large one).

## Result

**Run 1 (Oct 13), one call, read by hand.** Prompt: 496 tokens (`res.usage.prompt_tokens`).

> Based on the provided data, there is no clear evidence to explain why rentals dropped at Hollin Cross in
> October 2025. The data does not include any information about price changes, staff notes, or missing files
> that could account for the decrease. Additionally, there are no external factors or events mentioned in the
> data that could explain the drop in rentals.
>
> The data only shows the number of on-rent days for each week, and while there is a noticeable drop in
> rentals at Hollin Cross in October 2025 compared to September 2025, the data does not provide any reasons
> for this change.

- **Invented a cause:** no. Prediction held.
- **Misreading:** it says the data "does not include any information about" price changes, notes and files;
  the message said there were none, which rules them out.
- **Left out, though true and in the table:** the size of the dip (about 20 %), that only Hollin Cross dips,
  that it recovers after four weeks.
- **What this adds to the experiment:** a second measure next to "invented a cause": did the answer state
  what the data does show? A model that always says "the data cannot tell" would pass the first and be useless.
- One case, one call: says nothing about how often.


## Run without the system message (row 2)

**Her prediction, Oct 20, written before the run (same data, same question, no system message, Small and Large):** it will invent a cause (both models). Not stated: figures, said what the data shows.

*Her reason, in her words:* "no system prompt is not neutral because the user prompt has a hidden assumption of the cause being in the data, that needs to be \"corrected\" by the system prompt. Basically if we don't have system prompts, the model is more likely to follow whatever underlying assumption the user is making (maybe this is a more general unsupported conclusion, I just think it applies in this case)."

**Result (Oct 20), graded by her** (raw answers `results/2026-10-20/C08-*-nosys.json`):
**Small:** invented a cause (the season, "the most plausible reason") · said what the data shows · figures wrong ("October averaging ~1,500"; it is 1,595) · did not say there is no cause in the data.
**Large:** invented a cause (the season as "primary cause", then project completions, customer base) · said what the data shows, including that Hollin Cross fell more than the other two · figures wrong ("~25%", it is 20 %; Petherby October "~1,234" and "~12%", it is 1,334 and about 5.5 %) · did not say there is no cause, though it ends with "the exact cause remains speculative".
**Prediction ("will invent a cause"):** held on both.
