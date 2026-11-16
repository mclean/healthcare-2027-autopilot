---
name: downside-case-model
description: Builds and maintains the 2027 downside case by payer (base, downside and severe scenarios for Medicaid work-requirement churn, exchange coverage loss, the Medicare fee schedule cut and commercial renewals) with a revenue bridge, cash runway, sensitivity ranking, early-warning triggers and an assumption register tied to sources. Use when the leader or CFO asks "run the downside case", "how much revenue is at risk in 2027", "what if our state doesn't take the hold-harmless option", "stress test the budget", "update the model", or when policy-radar or kpi-pulse calls for a rerun.
---

# Downside case model

Give the CFO a defensible range for 2027 and the signals that say which part of the range is coming true. Read `../../reference/conventions.md` first.

## Inputs and fallbacks

| Input | File | Fallback |
| --- | --- | --- |
| Payer mix, net revenue by class (D01) | `inputs/payer_mix.csv` | Archetype default mix, labeled directional |
| Expansion-adult share of Medicaid (D02) | `assumptions.json` `medicaid_subject_share` | National 30% (Morgan Lewis) |
| Exchange revenue (D03) | the `exchange` row of the payer mix | Commercial share times the state marketplace share |
| Medicare exposure (D04) | Medicare FFS and MA rows | Same rows from the default mix |
| Commercial renewals (D06) | `commercial_share_renewing` from contract-renewal-radar | 40% placeholder |
| Financials | `profile.json` `financials` | Expense at 92% of revenue, labeled |

## Steps

1. Confirm the payer mix is current (the most recent 12 months). If not, refresh it at the best tier.
2. Review the assumption register with the CFO the first time: every row marked `assumption` needs a value they own. Write their values into `assumptions.json` with `set_by` and the date.
3. Run `python3 ../../scripts/downside_model.py --workspace <ws>`.
4. Read the outputs in `outputs/model/`: the revenue bridge, the three scenarios with EBITDA margin and cash runway, the sensitivity ranking and the trigger table.
5. Write the CFO memo (one page): the range, the scenario to plan against and why, the two assumptions that move the answer most and how to firm them up, the triggers to watch with their check dates, and the decisions the plan implies at each scenario (for example: base = proceed with 2027 hiring plan; downside = hold open requisitions in non-clinical roles from April; severe = draw the line of credit). Recommendations at each level are for the CFO to adopt or change.
6. Update A01 in the tracker with the memo path as evidence.

## Model logic (so the agent can explain any number)

- **Medicaid churn** = Medicaid revenue × share subject × share disenrolled × months in effect (6 if the state elects hold-harmless, else 12) ÷ 12, offset by self-pay recoveries: lost revenue × (1 − utilization drop) × self-pay collection rate.
- **Exchange** = exchange revenue × volume loss × share becoming uninsured, with the same self-pay offset.
- **Medicare fee schedule** = (Medicare FFS + MA revenue × share tied to the fee schedule) × conversion factor change (−2.31% for most clinicians, −1.83% for qualifying APM participants).
- **Commercial** = commercial revenue × share renewing in 2027 × average rate change × 0.5 (mid-year average).
- **EBITDA** = revenue − 2026 operating expense × (1 + expense growth).
Hospital-specific lines (340B, site-neutral, supplemental payments) are handled by site-of-care-shift and financing-cliff-2028; bring their results into the memo rather than double counting.

## Reruns

Rerun when: policy-radar applies a sourced change, a hold-harmless election is announced for a profile state, contract-renewal-radar updates the renewing share, the monthly pulse fires two or more early-warning triggers, or the CFO changes an assumption. Each rerun goes in the tracker history with what changed.

## What most models miss

- **Timing, not just size.** The hold-harmless option does not change how many people lose coverage; it moves the cash impact from Q1 to Q3. Liquidity planning cares about the quarter.
- **People who lose coverage still come in.** HCA expects most exchange enrollees who lose coverage to become uninsured and cut their use of care by about 30%. The rest show up as self-pay, which is why collection rate is in the model.
- **The biggest swing is often your own cost line.** In the sample, a 50% miss on expense growth moves EBITDA more than any policy assumption. Do not let policy work crowd out cost work.
- **Medicare Advantage contracts often inherit fee schedule cuts.** Check how much MA revenue is paid as a percent of Medicare.
