---
doc_id: REV-002
title: Average daily rate
version: "1.2"
effective_date: 2025-04-01
owner: Finance
language: en
synthetic: true
---

# Average daily rate

## 1. Definition

1.1 The **average daily rate** is what the company earned, on average, for one piece of equipment being out with a customer for one day. It is often shortened to "daily rate" or "rate per day".

1.2 Formula: average daily rate = rental revenue ÷ on-rent days, where both figures cover exactly the same weeks, depots, categories and channels. On-rent days are defined in OPS-001.

1.3 The revenue used here is hire charges, damage waiver and credit notes only. **Delivery and collection fees have never been part of the average daily rate**, whichever version of REV-001 is in force, because a delivery fee is charged per contract and not per day. The rate is therefore comparable across the whole history.

1.4 The result is stated in euros per day, with two decimals.

## 2. It is a ratio: add first, divide last

2.1 To get the rate of a total (a region, a month, the company), add up the revenue, add up the on-rent days, then divide. **Never average the rates of the parts.**

2.2 Example with two categories in one depot and one week:

| Category | Rental revenue (EUR) | On-rent days | Average daily rate (EUR) |
|---|---|---|---|
| Earthmoving | 9,000.00 | 90 | 100.00 |
| Power tools | 4,500.00 | 300 | 15.00 |
| **Both** | 13,500.00 | 390 | **34.62** |

The rate for both together is 13,500 ÷ 390 = 34.62. The plain average of 100.00 and 15.00 is 57.50, which is wrong, because far more days were rented at the low rate.

2.3 For the same reason the rate of a total depends on the **mix**: how the on-rent days are spread over cheap and expensive categories. The rate of a region can fall while the rate of every category in it rises, when more of the days move to the cheap categories. A statement about the rate of a total must be checked against the rates of its categories before any reason is given (see RPT-001).

## 3. It is not the list price

3.1 The list price is the price of one day before any discount (PRC-001). The average daily rate is always lower than the list price, for two reasons: longer hires are charged fewer days than they last, and account customers and online bookings receive discounts.

3.2 A rate that is 25 to 45 percent below the list price is normal and is not a sign of an error or of unusual discounting.

3.3 When list prices change, the average daily rate of the same category, channel and region moves by about the same percentage from the week the new price starts.

## 4. When the rate cannot be given

4.1 If the on-rent days of the scope are zero, there is no rate. Report "no rentals", not zero.

4.2 If a week is provisional (DAT-001), say so. Revenue and days are both incomplete in a provisional week, so the rate is usually close to final even when the totals are not.
