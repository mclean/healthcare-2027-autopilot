---
name: data-readiness
description: Grades every data input the readiness program depends on (payer mix, Medicaid roster, contracts, A/R, coding, vendors and more) on a four-tier fallback ladder, shows how data gaps lower the confidence of each action, and ranks the cheapest upgrades. Use when the leader asks "what data do we need", "how good is our data", "why is this number directional", "what should we export", during setup, or on the monthly re-check.
---

# Data readiness

The program never waits for perfect data. It runs on the best tier available and says so. This skill keeps that honest and pushes every input up the ladder. Read `../../reference/conventions.md` first.

## The ladder

| Tier | Meaning | Confidence label |
| --- | --- | --- |
| A | Live system through a connector, API or saved query | High |
| B | Export file dropped in `inputs/` on a schedule | High once the mapping is validated |
| C | Structured estimate from a named leader, dated | Medium |
| D | Public default or national figure | Directional |

The full chain for each of the 18 dependencies is in `../../reference/dependencies.json`, including which report to ask for and how to validate it.

## Monthly re-check (scheduled)

1. **Freshness.** For each tier-B input, check the file's modified date. Older than 35 days: mark stale, use it anyway with a "stale" label, and add an owner nudge to the brief.
2. **Discovery.** Look for new files in `inputs/` and for newly connected tools (search the available connectors). A new export or connector can move a dependency up a tier.
3. **Validation.** Run the dependency's validation rule before promoting it (for example, payer mix net revenue ties to the income statement within 3%). Promote only after it passes; record the date in a note.
4. **Run the map:** `python3 ../../scripts/data_readiness.py --workspace <ws>`.
5. **Report** only if a tier changed or a critical input went stale: one line per change and the next best upgrade.

## Setup or on-demand review

Walk the leader through the "Upgrade these first" table. For each upgrade, produce the exact ask for the person who owns it, ready to forward, for example:

> Please export the "financial class summary" (or payer mix by financial class) report for the trailing 12 months, by month, with visits, gross charges and net revenue, as CSV, into the Readiness 2027 folder under inputs/payer_mix.csv. Same report on the 3rd of each month.

Report names vary by system. Describe the content and columns precisely rather than guessing a menu path, and ask the owner to reply with the report name they used so the next request can name it.

## Fallback behavior other skills rely on

- When a skill needs an input at tier D, it uses the public default from `../../reference/assumptions-defaults.json` or the archetype default mix in `../../reference/segment-archetypes.md`, and writes "directional" next to every number derived from it.
- An action's confidence is the weakest of its inputs. A downside case built on an estimated Medicaid share is a C, however good the rest is.
- Dependencies that do not apply to the organization (hospital outpatient data for a physician group, supplemental payments for an ASC) are marked not applicable and never drag a grade down.

## What most teams miss

- **The Medicaid expansion-adult proxy is good enough.** Without aid-category data, Medicaid patients aged 19 to 64, excluding pregnancy, disability (SSI) and children's plans, gets within striking distance. Validate it once against 50 charts.
- **Public data covers more than people think.** CMS publishes Medicare utilization by provider NPI and HCPCS. It lags about two years, but it is enough to benchmark a group's E/M distribution and to see what payers can see.
- **Estimates are data.** A CFO's dated estimate with a name on it is tier C and far better than nothing. The failure mode is an undated number with no owner.
- **The agent's own plumbing is a dependency (D18).** If the state store or delivery channel breaks, everything downstream fails silently. Treat it like any other critical input.
