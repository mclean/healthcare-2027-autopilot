---
name: financing-cliff-2028
description: Models a hospital's exposure to the Medicaid financing changes that start right after 2027 (provider tax safe harbor phase-down from October 1, 2027 and state-directed payment cuts from January 1, 2028), year by year through 2033, with state response scenarios and budget integration. Use when a hospital leader asks "what happens to our supplemental payments", "model the provider tax phase-down", "how big is the 2028 cliff", "state-directed payment exposure", or on the A10 checkpoint.
---

# 2028 financing cliff

For hospitals, 2027 is the last year before Medicaid financing shrinks. In expansion states the provider tax safe harbor steps down from 6% toward 3.5% starting October 1, 2027 (nursing homes and ICFs exempt), and state-directed payments above 100% of Medicare (110% in non-expansion states) fall 10 percentage points a year from January 1, 2028; the first-year federal cut is estimated at $8.7 billion (CLA, HFMA). Read `../../reference/conventions.md` first.

## Applies when

`receives_supplemental_payments` is true in the profile (usually the community-hospital archetype).

## 1. Inputs (D13)

Fill `inputs/supplemental.json` from finance's supplemental payment schedule (B) or the CFO's estimate (C):
- Each state-directed payment program: FY2026 amount, total payment level as a percent of Medicare, and the base Medicaid rate as a percent of Medicare.
- Each provider-tax-funded program: FY2026 payments, tax paid, and the state's tax rate.
- DSH and other supplemental programs (held flat in the model; watch separately).
Fallback (D): the state hospital association's briefing and KFF or MACPAC state tables, labeled directional.

## 2. Run

```
python3 ../../scripts/financing_cliff.py --workspace <ws>
```

The model assumes constant volume and that the state passes cuts straight through. It shows the step-down by year, the run-rate loss by 2033 and the cumulative loss from 2028.

## 3. State response scenarios

States will respond. Model at least: pass-through (the script's default), partial backfill from the state budget, and base-rate restructuring. Ask the state hospital association which response the state is planning; policy-radar watches for state budget proposals.

## 4. Into the plan (A10, due September 30, 2027)

Bring the 2028 figure into the 2028 budget and the long-range plan, the downside model memo, and the board update. Identify offsets: service line changes, site-of-care moves, cost programs and partnerships. Mark A10 done when the 2028 budget carries the number.

## What most hospitals miss

- **The tax phase-down hits the state's ability to pay, not just the hospital's tax bill.** Lower taxes mean less non-federal share, which means less federal match and smaller add-ons.
- **Above-cap programs shrink slowly but surely.** A program at 160% of Medicare in an expansion state takes six years to reach the cap; the loss compounds.
- **Timing differs by calendar.** The tax change follows the federal fiscal year (October); state-directed payments follow the calendar year (January).
