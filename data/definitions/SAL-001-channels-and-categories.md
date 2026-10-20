---
doc_id: SAL-001
title: Channels, categories and customer segments
version: "3.1"
effective_date: 2025-04-01
owner: Sales
language: en
synthetic: true
---

# Channels, categories and customer segments

## 1. Why three different groupings

1.1 Figures are broken down in three ways that are easy to confuse. A **channel** says how a rental was arranged. A **category** says what was rented. A **segment** says what kind of customer rented it.

## 2. Channels

| Code | Channel | What it means |
|---|---|---|
| `counter` | Counter | the customer came to a depot or phoned it, and paid per rental |
| `online` | Online booking | booked and paid on the website; called "web" in reports before 2025 |
| `contract` | Contract accounts | rented on an account with agreed terms and a monthly invoice |

2.1 Counter and online together are called the walk-in channels.

2.2 Every rental belongs to exactly one channel. The three channels add up to the total.

## 3. Equipment categories

| Code | Category | Examples | Typical price level |
|---|---|---|---|
| `ACC` | Access | scaffold towers, scissor lifts, podium steps | high |
| `EAR` | Earthmoving | mini excavators, dumpers, rollers; called "Plant" before 2024 | highest |
| `PWT` | Power tools | breakers, drills, saws, sanders | lowest |
| `PWL` | Power and lighting | generators, lighting towers, heaters | medium |
| `CON` | Concrete and compaction | mixers, plate compactors, floor saws | medium to low |

3.1 A day of Earthmoving costs several times a day of Power tools. Any average across categories therefore depends on how many days each category contributes (REV-002, section 2).

## 4. Customer segments

4.1 A segment is a property of a customer, not of a rental: `household`, `trade` (builders and other small firms) or `key_account` (large customers with a negotiated contract and a named manager).

4.2 Only customers with a contract account are identified in the reporting database. A key account always rents through the contract channel. Counter and online customers are not identified, so there is no breakdown of the counter or online channel by segment or by customer.

4.3 A key account may rent from depots in more than one region.

## 5. Share of a total

5.1 The **share** of a channel (or category, or region) is its figure divided by the total of the same figure for the same weeks and the same scope, as a percentage. Example for one region and one month:

| Channel | Rental revenue (EUR) | Share |
|---|---|---|
| Counter | 210,000 | 42.0 % |
| Online booking | 90,000 | 18.0 % |
| Contract accounts | 200,000 | 40.0 % |
| Total | 500,000 | 100.0 % |

5.2 Say which figure the share is of. The online share of revenue, of on-rent days and of contracts are three different numbers.

5.3 To get a share for several regions or several weeks, add up the amounts first, then divide. Do not average the shares.

5.4 A change in a share is given in **percentage points**: from 18.0 % to 21.0 % is a rise of 3.0 percentage points, not of 3 percent. A share can fall while the amount behind it grows, if the rest grows faster.
