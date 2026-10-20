---
doc_id: REV-001
title: Rental revenue
version: "2.0"
effective_date: 2026-04-06
owner: Finance
language: en
synthetic: true
supersedes: "REV-001 version 1.3"
---

# Rental revenue

## 1. Purpose and change from the previous version

1.1 This document defines **rental revenue**, the figure Tarrowby Hire uses to say how much it earned from renting out equipment. Every report, dashboard and answer that uses the words "rental revenue" or "revenue" without another qualifier means the figure defined here.

1.2 This version applies to every week that starts on or after **6 April 2026**, the first week of fiscal year 2027. It replaces version 1.3. The one change is that **delivery and collection fees are no longer part of rental revenue**. They are now reported on their own line, called ancillary revenue.

1.3 A figure about a period that lies entirely before 6 April 2026, quoted on its own, follows version 1.3, because that is how it was published at the time.

1.4 A **comparison** between a period before 6 April 2026 and a period after it must use one definition for both sides. Restate the earlier period under this version, that is, without delivery and collection fees, and say that you have done so. Comparing a figure with fees against a figure without fees shows a fall of about a tenth that never happened.

## 2. What is included

2.1 The table lists every kind of amount that can appear on a rental invoice and says where it is reported.

| Code | Component | In rental revenue? | Remark |
|---|---|---|---|
| RC-01 | Hire charges | yes | the charge for the days the equipment is out |
| RC-02 | Damage waiver | yes | the optional charge that limits what a customer pays for accidental damage |
| RC-03 | Delivery and collection fees | **no** | reported as ancillary revenue |
| RC-04 | Credit notes | deducted | see section 3 |
| RC-05 | Fuel and consumables sold | no | reported as sales of goods |
| RC-06 | Damage recharges | no | reported as other income |
| RC-07 | Tax | no | every figure is before tax |

2.2 In words: rental revenue is hire charges, plus damage waiver, less credit notes.

2.3 The reporting database stores hire charges, damage waiver and credit notes together in one amount, and delivery and collection fees in a second amount. Under this version, rental revenue is the **first amount only**. The three parts of the first amount are not stored separately, so the reporting database cannot say how much of rental revenue is damage waiver or how much was given back in credit notes.

## 3. Credit notes

3.1 A credit note is an amount given back to a customer, for example when equipment broke down during the hire.

3.2 A credit note reduces rental revenue in the week in which it is issued, not in the week of the original invoice.

## 4. Timing

4.1 Revenue belongs to the week in which the equipment was on rent, not to the week in which the invoice was sent or paid.

4.2 A hire that runs over two weeks is split between them in proportion to the days in each week.

4.3 The two most recent weeks are provisional and usually understate the final figure (see DAT-001). Weeks, months and fiscal years are defined in CAL-001.

## 5. What this document does not define

5.1 Revenue per day is defined in REV-002. Utilisation is not a revenue figure and is defined elsewhere.
