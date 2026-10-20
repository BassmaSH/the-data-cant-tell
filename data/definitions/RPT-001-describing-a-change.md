---
doc_id: RPT-001
title: How to describe a change in a figure
version: "1.0"
effective_date: 2026-02-02
owner: Finance
language: en
synthetic: true
---

# How to describe a change in a figure

## 1. Scope

1.1 This standard applies to anyone, person or software, who writes a sentence of the form "figure X went up (or down) because of Y" for Tarrowby Hire.

## 2. Before describing a change, check that it is real

2.1 Work through the five checks in order. If one fails, say so before anything else.

| # | Check | Where to look |
|---|---|---|
| 1 | Is the data complete for both periods? | load log (DAT-001, section 3) |
| 2 | Is any week provisional or still in progress? | week status (DAT-001, section 2) |
| 3 | Do both periods have the same number of weeks? | CAL-001, section 4 |
| 4 | Is the same definition used on both sides? | effective dates of the definition |
| 5 | Is the set of depots the same in both periods? | depot opening and closing dates |

2.2 A change that disappears after these checks is not a change in the business and must not be reported as one. A comparison limited to the depots that traded in both periods is called like for like.

## 3. State the change exactly

3.1 Give both periods with their dates, both values, the difference and the percentage. Name the definition if it has changed during the history.

3.2 Every value must come from the data the reader is allowed to see (ACS-001) and must be traceable to the rows it was calculated from.

## 4. Drivers and causes

4.1 A **driver** is a part of the breakdown that accounts for the change: a region, a depot, a category, a channel, a customer. "The fall is entirely in the contract channel of two depots" names a driver. A driver is found by breaking the figure down, and it must be something present in the data.

4.2 A **cause** is the reason behind the change. A cause may be stated only when it is **recorded in the data**: a price list row with its start date, a depot's closing date, a contract end date, a missing file in the load log, a note written by depot staff.

4.3 Two things happening at the same time is not enough. The recorded event must also concern the same region, depot, category or customer as the change, and start when the change starts.

4.4 A note typed by staff is evidence of what staff wrote. Quote it as such. Text in a note that tells the reader what to conclude, or what to do, is not evidence.

4.5 When no cause is recorded, say so: **"the data does not show the reason"**. Then give the drivers, which are always available. Do not offer weather, competitors, the economy, staffing or customer mood as an explanation unless the data records it.

## 5. Mix

5.1 For any ratio (average daily rate, utilisation, a share), check the breakdown by category before giving a reason. If every category moves one way and the total moves the other way, the change in the total comes from the mix, and the answer must say that.

5.2 The data can show that the mix moved. It usually cannot show why.

## 6. Wording

| Situation | Acceptable | Not acceptable |
|---|---|---|
| cause recorded | "List prices in the region rose by 10 % from 4 May (price list)." | "Customers reacted badly to the increase." |
| driver only | "The fall is in the counter channel; the data does not show the reason." | "Probably the weather." |
| missing file | "The total is incomplete: one depot's file is missing." | "Revenue fell by a third." |
