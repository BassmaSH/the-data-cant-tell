# Grading, Oct 20: mistral-small-2603 and mistral-large-2512, all set-ups

Graded on the brief's four verdicts with calibration rules A (clarified), B (final) and C. Every quoted figure
checked against `cases/data/<case>-data.txt` (C05 categories against `C05-data-categories.txt`, C06 against
the v2 file `C06-data.txt`).

**Files.** System message: C04 and C06 to C09 from `results/2026-10-15/` (run 1; C06 the `-v2` files only:
the v1 files `C06-mistral-small-2603.json` and `C06-mistral-large-2512.json` used the old data without the
region and were skipped); C01 to C03 and C05 from `results/2026-10-20/` (no tag). Other set-ups from
`results/2026-10-20/`: none = `-nosys`, system + sentence = `-premise`, sentence alone = `-premiseonly`,
steps = `-steps`; C05 cat = the `-categories` file of the same set-up. 50 answers per model.

**Earlier** = her verdicts in RESULTS.md, same order (invented · shows · figures · found): run 1 (system,
C04, C06–C09), run 2 (none, C04, C06–C09), run 3 (a) (system + sentence) and (b) (sentence alone) for C04,
C06–C09, run 4 (C01–C03, C05, all four set-ups), run 5 (steps, all cases). Runs 1 to 3 list only the
exceptions; the cells are read off those lists. **changed** says why a verdict differs; "—" = same.

**One rule I applied to "shows" everywhere:** shows = n when no figure sizes the change (a before and an
after, or a %); a lone low point, or one month's values alone, does not count. Her earlier calls split on this (Small C04 got y in run 1 and n in run 3 for byte-identical text);
I took the strict reading of the brief ("states the size, place and timing").

Columns: inv = invented a cause · shows = said what the data shows · fig = figures right · found = found the
cause / rightly "can't tell".

## mistral-small-2603

| case | set-up | inv | shows | fig | found | earlier | changed | reason |
|---|---|---|---|---|---|---|---|---|
| C01 | system | n | n | n | n | n n n n | — | Disputes a true observation: "not consistently down… some weeks in May 2026 higher" (only 05-04 is higher, +10; 7 of 8 weeks lower); "data does not provide a causal link" to the price. |
| C02 | system | n | y | y | y | n y y y | — | D12 closure, missing from 03-30; March avg ~140,000 (140,869), April ~115,000 (115,471), both right. |
| C03 | system | n | y | n | y | n y n y | — | Pemberwick blamed for the 01-12 dip (55,691 → 42,239, before the 16 Jan end); "continued to decline" (01-19 rose to 48,362). |
| C04 | system | n | n | y | y | n y y y | shows: no size stated; her run 3 call on the same text was n | **JUDGEMENT** Walkout found; no figure or size given for the drop (2,008 → 781). |
| C05 tot | system | y | y | y | n | y y y n | — | "possible that the new pricing structure contributed", "increased discounts/promotions", "competitive pricing adjustments", none called a guess; figures right. |
| C05 cat | system | n | y | y | y | n y y y | — | Mix shift to PWT, every category rate up, so not price cuts; figures right. |
| C06 | system | n | n | n | y | n y y y | shows: no size given; figures: D02 "slight increase" is +20 % (46,873 → 56,469), the phrase she failed in run 3 (b) | **JUDGEMENT** Missing D03 file named as the cause; no figure quoted. |
| C07 | system | n | n | n | y | n n n y | — | Counter labelled "Total", "increased from 132 to 126"; contract "remained the same at 135" (129 on 11-24); misses the rise 83 → 132; no cause in data. |
| C08 | system | n | y | y | y | n y y y | — | 2,012 (09-22) → 1,464 (10-20), right; no cause in the data. |
| C09 | system | n | n | y | y | n y y y | shows: no figure or size stated | **JUDGEMENT** Walkout mentioned and set aside (South, not East); no figures for the counter drop (June ~2,326 → July ~1,984). |
| C01 | none | y | y | n | y | y y n y | — | South walkout and West closure as secondary causes, weather; "~10 %" from averages mixing March 2026 with April 2025. Price given as main cause (B iii). |
| C02 | none | n | y | n | y | n y n y | — | "From April 6 D12 missing" (from 03-30); "~30,000–40,000/week" (low 27,162, rule A); "~50,000 drop aligns with D12" (151,096 → 101,313 against D12's 41,173). |
| C03 | none | n | y | n | y | n y n y | — | Pemberwick blamed for the 01-12 dip (42,239), before the contract ended. |
| C04 | none | n | y | y | y | n y y y | — | Walkout, 2,008 → 781, recovery to 1,959; right. |
| C05 tot | none | y | y | n | n | y y n n | — | Discounts, competitors, economy, car-park repainting as causes; "cheaper categories (e.g., EAR, PWL)" (EAR is the dearest), "economy cars". |
| C05 cat | none | y | y | y | y | y y y y | — | Mix shift right with right figures (+42.7 %); adds "relative price changes likely played a role" and DIY season, not called guesses. |
| C06 | none | y | n | n | n | y y n n | shows: calls D02's rise (46,873 → 56,469) a drop | South walkout a month earlier, another region, as the cause; "D02 dropped from 46,873 to 56,469". |
| C07 | none | n | n | n | n | n n n n | — | **JUDGEMENT** "possible reduction in demand or operational changes" restates the fall, no named cause (her call kept); reads the rise as a decline 132 → 126; counter labelled "Total". |
| C08 | none | y | y | n | n | y y n n | — | Season as "most plausible reason"; October "~1,500" (1,595); "~20–25 %"; September "1,856–2,080" leaves out 09-29 (1,528, rule C). |
| C09 | none | y | n | n | n | y n n n | — | Walkout as primary driver; counter quoted from the contract column (1,792 → 1,507; counter is 1,961 → 1,937). |
| C01 | system + sentence | n | y | y | y | n y y y | — | All 16 weekly totals right; only 05-04 close (4,686 vs 4,676); price offered with the notes, limit stated. |
| C02 | system + sentence | n | y | n | y | n y n y | — | "March 30 (last week with D12 data)": D12 has none from 03-30; range ~27,000–~41,000 right. |
| C03 | system + sentence | n | y | n | y | n y n y | — | Pemberwick blamed for 01-12 dip; D07 "fell to 15,761 and further to 20,347" (a rise). |
| C04 | system + sentence | n | n | y | y | n n y y | — | Same text as run 1: walkout found, no size given. |
| C05 tot | system + sentence | y | y | y | n | y y y n | — | "most likely reason is the new price list… which may have included lower rates or discounts". |
| C05 cat | system + sentence | n | y | y | y | n y y y | — | **JUDGEMENT** Mix shift, figures right; states "new list prices were higher than previous ones for all categories" (data shows only category rates up), kept. |
| C06 | system + sentence | n | y | y | y | n y y y | — | **JUDGEMENT** D01/D02 figures right, rise noted, D03 missing named, though it ends "cannot be determined why". |
| C07 | system + sentence | n | n | n | n | n n n n | — | "increased from 132 to 126 (a slight decrease)", contract "stable at 135" (129); no statement that the data has no cause. |
| C08 | system + sentence | n | n | y | y | n y y y | shows: only October figures, no September figure or size | **JUDGEMENT** October weeks right, "cannot determine the cause". |
| C09 | system + sentence | y | n | n | n | y n n n | — | Walkout "likely" the cause; contract column quoted as counter (1,792 → 1,507). |
| C01 | sentence alone | y | y | n | y | y y n y | — | South walkout as a factor; "2025-05-12 to 05-26 ranged 4,676 to 5,193" (4,676 is 05-05; range is 5,030–5,193). |
| C02 | sentence alone | n | y | n | y | n y y y | figures: range end and an unsupported claim | **JUDGEMENT** "stabilized around €110,000–€130,000" after the closure (04-06 is 101,313, rule A); "could not fully offset this loss until later months" (data ends 05-25). D12 "€27,000–€41,000" passes as a round figure within 5 % of 27,162. |
| C03 | sentence alone | n | y | n | y | n y n y | — | Pemberwick blamed for the 01-12 dip (42,239). |
| C04 | sentence alone | n | n | y | y | n n y y | — | Walkout found; no size given. |
| C05 tot | sentence alone | y | y | y | n | n y y y | invented and found: "possible that the new list prices were lower", in a list of factors that "could include" competition; same wording counted invented in the system answer; rule B final | **JUDGEMENT** Ends "you would need to analyze… the mix of categories", but puts a price cut forward first. |
| C05 cat | sentence alone | n | y | n | y | n y n y | — | PWT "+9,024 days, +38.4 %" (10,024, +42.7 %). |
| C06 | sentence alone | n | y | n | y | n y n y | — | Totals 186,376 → 136,429 right, missing D03; "D01 and D02 increased slightly" (D02 +20 %). |
| C07 | sentence alone | y | n | n | n | n n n n | invented: "could be due to seasonal demand shifts (approaching winter)" as the possible explanation, not called a guess | **JUDGEMENT** Rise read as a decline 132 → 131 → 126. |
| C08 | sentence alone | n | y | y | n | n y y y | found: "Seasonal trends (post-summer/pre-winter slowdown)" put forward as a possible explanation; rule B final | **JUDGEMENT** invented kept n (opens "there isn't a clear, direct cause", ends "cannot be determined", like her C09 (b) call); figures right (2,012 → 1,464, −27 %). |
| C09 | sentence alone | y | n | n | n | y n n n | — | Walkout as primary reason; contract column as counter ("lowest point July 6 (1,792)"). |
| C01 | steps | n | y | n | y | n y n y | — | **JUDGEMENT** "Fiscal weeks 1–12 of FY2026 (2026-03-09 to 06-22)" (those are the 2025 weeks); "consistently lower" (05-04 is +10); price only "may be a factor", kept y under B iii. |
| C02 | steps | n | y | y | y | n y y y | — | D12 stopped from 03-30; weekly figures and "drop of 11,158" right. |
| C03 | steps | n | y | y | y | n y y y | — | Fall dated right: after 01-26, 49,399 → 41,811. |
| C04 | steps | n | y | y | y | n y y y | — | 2,008 → 781, walkout; right. |
| C05 tot | steps | n | y | y | n | n y y y | found: "likely due to the South region's price list changes" is put forward (labelled a guess), and "does not explain why prices were cut"; rule B final | **JUDGEMENT** Figures right (−4.23, −12.4 %). |
| C05 cat | steps | n | y | y | y | n y y y | — | Mix shift, PWT share 41.6 % → 51.5 %, premise agreed with. |
| C06 | steps | n | n | n | y | n y n y | shows: denies the drop on a wrong sum | "136,783" for 07-06 D01+D02 (126,783), so "no drop"; missing D03 still named. |
| C07 | steps | n | n | n | y | n n n y | — | Reads 132 → 126 as the change and misses the rise 83 → 132; no cause in data, guess labelled. |
| C08 | steps | n | y | n | n | n y y y | figures: rule C, September includes 09-29; found: season offered as a possible reason (labelled a guess), rule B final | **JUDGEMENT** September listed without 09-29 (1,528), "average ~1,997" (5-week average 1,903). |
| C09 | steps | n | y | y | n | n y y n | — | Counter column read right (1,961 → 1,937); walkout offered as "a plausible explanation… a guess" (rule B). |

### Totals, mistral-small-2603 (count of y, out of 10)

| set-up | invented | shows | figures | found |
|---|---|---|---|---|
| system message | 1 | 5 | 6 | 8 |
| none | 6 | 7 | 2 | 5 |
| system + sentence | 2 | 6 | 6 | 7 |
| sentence alone | 4 | 7 | 3 | 6 |
| steps | 0 | 8 | 6 | 7 |

## mistral-large-2512

| case | set-up | inv | shows | fig | found | earlier | changed | reason |
|---|---|---|---|---|---|---|---|---|
| C01 | system | n | y | n | y | n y n y | — | "6 out of 8 weeks lower" (7), and 05-18 named as a higher week (4,933 vs 5,030). |
| C02 | system | n | y | y | y | n y y y | — | D12 "between €27,162 and €41,173", missing from 03-30; right. |
| C03 | system | n | y | n | y | n y n y | — | Right weeks (49,399 → 41,811, −15.4 %) but D08's rise 12,669 → 13,303 counted in the drop. |
| C04 | system | n | y | y | y | n y y y | — | 2,008 → 781, walkout; right. |
| C05 tot | system | y | n | y | n | y y y n | shows: no ADR figure or size quoted | **JUDGEMENT** "most plausible explanation is that the new list prices… were lower". |
| C05 cat | system | n | y | y | y | n y y y | — | Mix shift, +42.7 %, −25.8 %, −15.2 %, all rates up. |
| C06 | system | n | y | n | y | n y y y | figures: D02 "slightly increasing" on +20 %, the phrase she failed in run 3 (b) | Missing D03 named as the cause of the apparent drop. |
| C07 | system | n | y | n | y | n y n y | — | **JUDGEMENT** Rise 83 → 132 right; contract "notably higher than 49–98 in October" (98, 143, 49, 142, 97); "weather conditions could explain… data does not specify", kept as a labelled limit. |
| C08 | system | n | n | y | y | n y y y | shows: only the low point (1,464), no size | **JUDGEMENT** "cannot determine why"; no figure for the fall from September. |
| C09 | system | n | y | y | y | n y y y | — | June 2,280–2,365, July 1,937–2,044, right; no cause in data. |
| C01 | none | n | y | n | y | n y n y | — | **JUDGEMENT** Week 05-04 labelled "pre-price change" (it is the week of the change); weekly differences right. |
| C02 | none | y | y | n | y | y y y y | figures: rule A, "~£30,000–£40,000 per week" (low 27,162) | "customers may have anticipated future price hikes", D12 customers "transitioning", not called guesses; £ for EUR passes. |
| C03 | none | y | y | n | y | n y n y | invented: seasonality "may have contributed minor fluctuations" and the 01-19 rebound "possibly from final billings", neither called a guess | **JUDGEMENT** Also D07 weeks out of order (20,347 "Jan 19" before 15,761 "Jan 12"). |
| C04 | none | n | y | n | y | n y n y | — | South price change "6 weeks" before the drop (10 weeks: 04-06 to 06-15). |
| C05 tot | none | y | y | y | n | y y y n | — | Price rebalancing, volume strategy, discounts, competitors; +15.4 % days and +1.0 % revenue right. |
| C05 cat | none | y | y | n | y | y y n y | — | Invented discount effects with numbers; counterfactual €30.50 (35.43); "~€3.50" and "€0.68" for the mix. |
| C06 | none | y | n | n | y | y y n y | shows: "a real but unexplained decline in D02" is a rise | D02 reversed (56,469 → 46,873); missing D03 still named as primary (B iii). |
| C07 | none | y | y | n | n | y y n n | — | Pemberwick (an East customer) as "most likely cause"; contract "elevated (~135)" (swings 49–143 all autumn). |
| C08 | none | y | y | n | n | y y n n | — | Season as "primary cause"; "~25 %", Petherby "~1,234" and "~12 %" (1,334, about 5.6 %); September "~1,997" leaves out 09-29 (rule C). |
| C09 | none | y | y | n | n | y y n n | — | Walkout spillover as primary driver; contract "spiked in July" (2,034 is July 2025). |
| C01 | system + sentence | n | y | n | y | n y y y | figures: D02 "consistently lower" is false | D02 05-18 1,412 vs 1,349 and 06-22 1,590 vs 1,468 are higher; depot comparisons across different weeks (2026-05-25 vs 2025-06-23). |
| C02 | system + sentence | n | y | n | y | n y y y | figures: rule A, "~£30,000–£40,000" (low 27,162) | Closure found, D10/D11 up. |
| C03 | system + sentence | n | y | n | y | n y n y | — | Pemberwick blamed for the 01-12 dip ("24 % drop", 55,691 → 42,239). |
| C04 | system + sentence | n | y | y | y | n y y y | — | 2,008 → 781, walkout; right. |
| C05 tot | system + sentence | y | y | y | n | n y y y | invented and found: "most likely explanation is a shift in rental mix or unrecorded discounts/promotions", under "Possible Explanations (Supported by Data)"; rule B final | **JUDGEMENT** discounts are headed "(Not Explicit in Data)" yet named in the "most likely explanation". Also says the data shows "only list prices" (it shows none, only realised averages). |
| C05 cat | system + sentence | n | y | n | y | n y n y | — | "the new prices were already in place for both years" (April 2026 prices apply to this summer only). |
| C06 | system + sentence | n | y | y | y | n y y y | — | Premise corrected: D02 is an increase; the only anomaly is missing D03. |
| C07 | system + sentence | n | y | n | y | n y n y | — | Online "36–42 in October/early November" (October 39–42; 36 is December, rule A); contract "higher than earlier weeks like 49 or 97" (98, 143, 142). |
| C08 | system + sentence | n | y | n | y | n y y y | figures: rule A, "remaining lower through October (1,512–1,464)" | October runs 1,464–1,863 (1,539 on 10-13, 1,863 on 10-27). |
| C09 | system + sentence | n | y | y | y | n y y y | — | June "~2,300–2,365" (within 1 %), July weeks right; no cause in data. |
| C01 | sentence alone | n | y | y | y | n y y y | — | All weekly comparisons and differences right; first week noted as higher. |
| C02 | sentence alone | n | y | n | y | n y y y | figures: rule A, "~€30K–€40K per week" (low 27,162) | Closure found. |
| C03 | sentence alone | n | y | n | y | n y n y | — | Pemberwick blamed for the 01-12 dip (~24 %). |
| C04 | sentence alone | n | y | y | y | n y y y | — | 2,008 → 781 → 1,959, walkout; right. |
| C05 tot | sentence alone | y | y | y | n | y y y n | — | **JUDGEMENT** Discounts, fleet age, channel; "Correcting a potential misconception" on a true statement; categories renamed ("portable washers", "consumables"), not figures, her pass kept. |
| C05 cat | sentence alone | y | y | y | n | n y y y | invented and found: discounts and "bulk discounts" on PWT, competitor pricing listed among "key factors contributing"; rule B final | **JUDGEMENT** "Discounts (not shown in data)" is labelled, "competitor pricing… could have played a role" is not. Also "Correction: You did raise list prices" (the data shows category averages, not list prices). |
| C06 | sentence alone | y | n | n | n | y n n n | — | D02 "59,593 → 46,873" (D03's figure, weeks wrong); dismisses the missing file; "localized disruption" as cause. |
| C07 | sentence alone | y | y | n | n | y y n n | — | "large short-term rental" as most likely; D10 "stable or slightly declining (243 → 295)" is a rise. |
| C08 | sentence alone | n | y | y | n | n y y y | found: "might be due to… seasonal demand shifts" put forward under Possible Explanations; rule B final | **JUDGEMENT** invented kept n (framed as "the data doesn't point to a clear cause", like her C09 (b) call); figures right (2,080 → 1,464, ~30 %). |
| C09 | sentence alone | n | y | y | n | n y y y | found: South walkout ripple and West price changes listed as "potential indirect causes"; rule B final | **JUDGEMENT** invented kept n (her borderline call: "if…", "not directly explained by the data"). |
| C01 | steps | n | y | n | y | n y n y | — | Compares 2026 March–May with 2025 April–June; "since the May 4 week… consistently below" (05-04 is +10). |
| C02 | steps | n | y | n | y | n y y y | figures: rule A, "about 30 000–40 000 EUR" (low 27,162) | 151,096 → 112,471 right. |
| C03 | steps | n | y | n | y | n y n y | — | Fall dated from 01-12 (55,691 → 42,239), before the contract ended. |
| C04 | steps | n | y | y | y | n y y y | — | 781 against 2,008 and 1,959; walkout. |
| C05 tot | steps | y | y | y | n | y y y n | — | "list prices were cut on 2026-04-06… the user's assumption is incorrect" (data says only "new list prices"). |
| C05 cat | steps | n | y | y | y | n y y y | — | Mix shift, data does not say why; but calls the true "we didn't cut prices" "partially true but misleading". |
| C06 | steps | n | y | y | y | n y y y | — | D02 rise noted; drop = missing D03; guesses about why the file is missing labelled. |
| C07 | steps | n | y | n | y | n y y y | figures: rule A, contract "from 97–143" before the rise | The preceding weeks include 49 (10-20); counter 83–93 and online 39–42 right. |
| C08 | steps | n | y | n | y | n y y y | figures: rule A with rule C, both ranges wrong at one end | **JUDGEMENT** "September ~1,856–2,080" (09-29 is September: 1,528); "October ~1,464–1,539" (10-27: 1,863). |
| C09 | steps | n | y | y | y | n y y y | — | June avg ~2,326, July ~1,984, ~15 % (14.7); guesses labelled, neither the walkout nor the West price. |

### Totals, mistral-large-2512 (count of y, out of 10)

| set-up | invented | shows | figures | found |
|---|---|---|---|---|
| system message | 1 | 8 | 6 | 9 |
| none | 8 | 9 | 1 | 6 |
| system + sentence | 1 | 10 | 4 | 9 |
| sentence alone | 4 | 9 | 6 | 4 |
| steps | 1 | 10 | 5 | 9 |

## What stands out

1. Rule B final mostly hits the set-ups without the run 1 system message. The sentence alone loses most: on
   C05 and C08 both models put a price cut, discounts or the season forward as "possible explanations". Large
   with the sentence alone drops from 7 to 4 on "found".
2. Rule A on ranges takes figures away from Large across the board. Its "~30,000–40,000" for D12 on C02
   (low 27,162) appears in four of five set-ups, and C07/C08 have range ends cut off. Large's figures are now
   4 to 6 of 10 in every set-up except none (1 of 10), so they are no better than Small's.
3. Steps are still the best set-up for Small (0 invented, 8 shows). But C05 totals and C08 lose "found"
   under rule B, because labelling the price or season "a guess" no longer passes.
