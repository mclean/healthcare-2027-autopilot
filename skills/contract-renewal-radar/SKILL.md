---
name: contract-renewal-radar
description: Inventories every payer contract, computes the real decision date (the notice deadline, not the renewal date), schedules reminders at 180, 120, 90, 60 and 30 days, flags windows already missed and contracts tied to the Medicare fee schedule, and builds a negotiation prep pack for 2027 renewals. Use when the leader asks "which contracts renew in 2027", "when do we have to give notice", "prep me for the payer negotiation", "are we tied to the Medicare fee schedule", or on the scheduled Tuesday contract watch.
---

# Contract renewal radar

Employers expect their health benefit costs to rise 8.2% in 2027, the most since 2003 (Marsh), and 59% plan cost-cutting changes. Payers will carry that pressure into every renewal. This skill makes sure no notice deadline passes unprepared. Read `../../reference/conventions.md` first.

## Build the inventory (D06)

Work down the tiers:
- **A:** read executed contracts from the connected drive or contract system. Extract payer, product, effective date, term, auto-renewal, notice period, escalator, termination without cause, and any rate floor or audit clause. Quote the clause page for each extracted field.
- **B:** use managed care's contract spreadsheet, mapped to `templates/contracts.csv`.
- **C:** search the leader's connected email for renewal letters, amendments and fee schedule notices; build a draft list and have the CFO confirm it.
- **D:** ask each payer's provider relations representative for a contract summary. Until confirmed, the script assumes a 90-day notice and marks the deadline "(assumed)".

Add `share_of_net_revenue` for each contract; the payer mix or remittance data gives it.

## Run

```
python3 ../../scripts/contract_radar.py --workspace <ws>
```

It writes the radar (`outputs/contracts/`), reminder jobs for the scheduler (`state/contract_alerts.json`) and the recommended `commercial_share_renewing` for the downside model. Copy that value into `assumptions.json` with `set_by: contract-renewal-radar` and rebuild the schedule through cadence-scheduler.

## Weekly watch (scheduled Tuesday)

Rerun the radar. Deliver only if a contract entered its prep window, came within 30 days of notice, or was found with a missed window.

## Prep pack (start 90 days before the notice deadline)

Produce `outputs/contracts/<payer>-prep.md` with:
1. **The number:** the contract's share of revenue, volume trend, and its 2027 exposure in the downside model.
2. **Your leverage:** market share for the services the payer's members use, access (appointment availability, sites, hours), quality and outcome measures, total cost of care or site-of-care savings you deliver (site-of-care-shift results are strong evidence), and patient experience.
3. **Their pressure:** employer cost trend (Marsh 8.2%, PwC 9% group medical trend), so the ask is framed around what you save them, not what you need.
4. **Terms beyond rate:** escalator design (a floor plus an index), protection if the contract is paid off the Medicare fee schedule (a floor so CMS cuts do not flow through automatically), payment for new codes, prompt-pay and denial terms, prior authorization relief for high-approval services, and the audit clause (payers are adding rights to audit AI-assisted documentation).
5. **Walk-away analysis:** what happens to volume and revenue if the contract terminates, and whether a termination-without-cause notice is a credible lever.
6. **The decision:** renegotiate, renew as is, or give notice, with the date it must be made.

Draft any letter to a payer for the leader's review. Never send it.

## What most teams miss

- **The deadline is the notice date.** A contract renewing January 1 with 90 days' notice was decided on October 3.
- **Missed windows still have a lever.** If notice passed, the contract auto-renews, but a termination-without-cause clause may still allow a reopening. It is a last resort and a relationship cost; quantify both.
- **Medicare Advantage contracts at a percent of Medicare inherit the 2027 cut** (−2.31% for most clinicians) unless they carry a floor.
- **CPI-capped escalators lag medical cost trend.** A 3% CPI cap against a 9% medical trend is a real cut each year.
