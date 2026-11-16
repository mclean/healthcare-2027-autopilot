---
name: kpi-pulse
description: Runs the monthly KPI pulse for the 2027 readiness program (payer mix shift, self-pay share, coverage denials, point-of-service collections, bad debt, days in A/R, high-level E/M share, contract and vendor gaps), compares each to a pre-2027 baseline, fires triggers and routes each one to the skill that handles it. Use when the leader asks "how are the numbers", "is coverage churn showing up", "run the KPI pulse", "are we in the downside case", or on the scheduled monthly run.
---

# KPI pulse

Turn month-end numbers into a decision: which playbook to run harder this month. Read `../../reference/conventions.md` first.

## Steps

1. **Collect the month.** For each KPI in `../../reference/kpi-definitions.json`, get the latest month's value at the best available tier (connector, export, then estimate) and append rows to `inputs/kpis.csv` as `month,kpi,value`. Percentages are written as numbers (3.8 means 3.8%). Do not overwrite earlier months; the history is the trend.
2. **Run** `python3 ../../scripts/kpi_pulse.py --workspace <ws>`. It compares the latest month to `kpi_baseline_period`, applies each trigger (or the leader's `kpi_overrides`), writes `outputs/kpi/<date>-kpi-pulse.html` and `state/triggers.json`.
3. **Read the pattern, not the list.** Combine fired triggers into the story they tell (see below) and name the one action that addresses it.
4. **Route.** For each skill named in `state/triggers.json`, add a tracker note on that skill's action and, where the trigger means the plan is not working, set the action to `at_risk`. If two or more of the downside model's early-warning triggers fired, schedule a downside-case-model rerun and say that planning should move from base to downside.
5. **Deliver** a five-line summary: the story, the numbers behind it with grades, the action, the owner, the date.

## Patterns worth naming

| Triggers together | Story | First move |
| --- | --- | --- |
| Self-pay share up, Medicaid share down, coverage denials up | Coverage churn reaching the front desk | medicaid-coverage-guard: tighten eligibility timing, start exemption screening |
| Self-pay up, POS collection rate down, bad debt up | Churn turning into bad debt | point-of-service-collections: estimates and collection at every visit |
| Days in A/R up with stable volume and denials | Cash slowing in the pipe, often a vendor or payer process problem | vendor-resilience and a payer-by-payer A/R review |
| High-level E/M share up after an AI scribe rollout | Coding pattern payers will notice | coding-integrity-audit |
| Contracts in notice window without prep | Leverage expiring | contract-renewal-radar prep pack this week |

## Tuning

Default thresholds are starting points. After two or three months, tune them in `profile.json` `kpi_overrides` so a trigger fires roughly when the leader would want to act, and log every change with the reason. Never tune a threshold to make a bad month disappear.

## What most dashboards miss

- **Per-day and per-visit rates beat totals.** Kaufman Hall tracks bad debt and charity per calendar day for a reason: month length and volume swings hide trends in totals.
- **Mix shift is the early signal, bad debt the late one.** Self-pay share moves in weeks; bad debt confirms it months later. Act on the early signal.
- **A missing KPI is information.** If the organization cannot produce coverage denial counts, it cannot see churn coming. The pulse lists missing KPIs with their data fallback instead of hiding them.
