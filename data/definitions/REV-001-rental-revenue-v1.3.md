---
doc_id: REV-001
title: Rental revenue
version: "1.3"
effective_date: 2025-04-01
owner: Finance
language: en
synthetic: true
---

# Rental revenue

## 1. Purpose

1.1 This document defines **rental revenue**, the figure Tarrowby Hire uses to say how much it earned from renting out equipment. Every report, dashboard and answer that uses the words "rental revenue" or "revenue" without another qualifier means the figure defined here.

1.2 Rental revenue is reported per week, per depot, per equipment category and per channel. It is stated in euros, before tax.

## 2. What is included

2.1 The table lists every kind of amount that can appear on a rental invoice and says whether it is part of rental revenue.

| Code | Component | In rental revenue? | Remark |
|---|---|---|---|
| RC-01 | Hire charges | yes | the charge for the days the equipment is out |
| RC-02 | Damage waiver | yes | the optional charge that limits what a customer pays for accidental damage |
| RC-03 | Delivery and collection fees | yes | charged when we bring the equipment to the customer or fetch it |
| RC-04 | Credit notes | deducted | see section 3 |
| RC-05 | Fuel and consumables sold | no | reported as sales of goods |
| RC-06 | Damage recharges | no | reported as other income |
| RC-07 | Tax | no | every figure is before tax |

2.2 In words: rental revenue is hire charges, plus damage waiver, plus delivery and collection fees, less credit notes.

2.3 The reporting database stores hire charges, damage waiver and credit notes together in one amount, and delivery and collection fees in a second amount. Under this version, rental revenue is the **sum of the two amounts**.

## 3. Credit notes

3.1 A credit note is an amount given back to a customer, for example when equipment broke down during the hire.

3.2 A credit note reduces rental revenue in the week in which it is issued, not in the week of the original invoice.

## 4. Timing

4.1 Revenue belongs to the week in which the equipment was on rent, not to the week in which the invoice was sent or paid.

4.2 A hire that runs over two weeks is split between them in proportion to the days in each week.

4.3 Weeks, months and fiscal years are defined in CAL-001.

## 5. What this document does not define

5.1 Revenue per day is defined in REV-002. Utilisation is not a revenue figure and is defined elsewhere.

5.2 Amounts not yet invoiced at the time of reporting are covered by DAT-001.
