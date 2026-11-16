# Scheduled tasks for Lakeshore Community Hospital (fictional sample)

Timezone: America/New_York. Create each as a scheduled task in Claude (recurring tasks use the cron line; one-time tasks use the date and time).
Each prompt is self-contained because every run starts a fresh session.

## Quarterly board or investor update

- Job id: `board-update`
- Skill: `board-update`
- When: cron `CRON_TZ=America/New_York 52 9 8 1,4,7,10 *` (Day 8 of Jan, Apr, Jul, Oct at 09:52)

```text
Run the `board-update` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Eighth of the month after quarter end: draft the update while numbers are fresh.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Quarterly coding integrity audit

- Job id: `coding-audit`
- Skill: `coding-integrity-audit`
- When: cron `CRON_TZ=America/New_York 26 10 15 1,4,7,10 *` (Day 15 of Jan, Apr, Jul, Oct at 10:26)

```text
Run the `coding-integrity-audit` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Mid-month after each quarter closes: compare coding patterns before payers do.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Contract notice-window watch

- Job id: `contract-watch`
- Skill: `contract-renewal-radar`
- When: cron `CRON_TZ=America/New_York 17 8 * * 2` (Every Tue at 08:17)

```text
Run the `contract-renewal-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Tuesday morning: no notice deadline passes unprepared.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Monthly data readiness re-check

- Job id: `data-readiness`
- Skill: `data-readiness`
- When: cron `CRON_TZ=America/New_York 41 16 2 * *` (Monthly on day 2 at 16:41)

```text
Run the `data-readiness` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Second of the month: try to upgrade every dependency one tier.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Monthly KPI pulse

- Job id: `kpi-pulse`
- Skill: `kpi-pulse`
- When: cron `CRON_TZ=America/New_York 13 7 5 * *` (Monthly on day 5 at 07:13)

```text
Run the `kpi-pulse` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Fifth of the month: month-end data has usually landed; triggers fire the right playbook.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Policy radar

- Job id: `policy-radar`
- Skill: `policy-radar`
- When: cron `CRON_TZ=America/New_York 23 13 * * 4` (Every Thu at 13:23)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Thursday afternoon: catch the week's CMS, state and congressional moves before Monday's brief.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Friday action tracker close-out

- Job id: `tracker-closeout`
- Skill: `action-tracker`
- When: cron `CRON_TZ=America/New_York 37 15 * * 5` (Every Fri at 15:37)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Friday afternoon: update status, chase owners, flag slips while there is still a week to recover.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Monthly vendor resilience check

- Job id: `vendor-check`
- Skill: `vendor-resilience`
- When: cron `CRON_TZ=America/New_York 9 11 20 * *` (Monthly on day 20 at 11:09)

```text
Run the `vendor-resilience` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Twentieth of the month: BAAs, backups and downtime tests stay current.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Weekly leader brief

- Job id: `weekly-brief`
- Skill: `weekly-leader-brief`
- When: cron `CRON_TZ=America/New_York 47 6 * * 1` (Every Mon at 06:47)

```text
Run the `weekly-leader-brief` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Monday morning: what needs the leader this week, before the first meeting.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A00 checkpoint: Set up the readiness program: profile, data tiers, schedule

- Job id: `A00-checkpoint`
- Skill: `action-tracker`
- When: once at 2026-11-16 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: Set up the readiness program: profile, data tiers, schedule.
Action in scope: A00 (Set up the readiness program: profile, data tiers, schedule). Done when: profile.json saved, data readiness map produced, recurring jobs scheduled and the first weekly brief delivered.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Prep: Medicaid work requirements begin in 44 states

- Job id: `medicaid-work-requirements-prep`
- Skill: `medicaid-coverage-guard`
- When: once at 2026-11-17 07:31 (America/New_York)

```text
Run the `medicaid-coverage-guard` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Prepare for: Medicaid work requirements begin in 44 states. Expansion adults ages 19 to 64 must report 80 hours a month of qualifying activity. About 30% of Medicaid beneficiaries are subject. Excluded states: WY, TX, KS, MS, AL, FL, SC.
Calendar event in scope: medicaid-work-requirements on 2027-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Prep: Six-month eligibility renewals for expansion adults

- Job id: `six-month-redeterminations-prep`
- Skill: `medicaid-coverage-guard`
- When: once at 2026-11-17 07:31 (America/New_York)

```text
Run the `medicaid-coverage-guard` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Prepare for: Six-month eligibility renewals for expansion adults. Expansion adults are redetermined every six months instead of annually, doubling the number of points where coverage can lapse.
Calendar event in scope: six-month-redeterminations on 2027-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A00 due: Set up the readiness program: profile, data tiers, schedule

- Job id: `A00-due`
- Skill: `readiness-setup`
- When: once at 2026-11-30 08:03 (America/New_York)

```text
Run the `readiness-setup` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: Set up the readiness program: profile, data tiers, schedule.
Action in scope: A00 (Set up the readiness program: profile, data tiers, schedule). Done when: profile.json saved, data readiness map produced, recurring jobs scheduled and the first weekly brief delivered.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Prep: Optional CMS hold-harmless period on work-requirement disenrollments

- Job id: `hold-harmless-window-prep`
- Skill: `downside-case-model`
- When: once at 2026-12-02 07:31 (America/New_York)

```text
Run the `downside-case-model` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Prepare for: Optional CMS hold-harmless period on work-requirement disenrollments. States that elect it must still assess compliance from January 1 but cannot deny or disenroll solely for failing the requirement until June 30, 2027. Which states elect it changes when coverage losses hit cash.
Calendar event in scope: hold-harmless-window on 2027-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A01 checkpoint: Run a 2027 downside case by payer

- Job id: `A01-checkpoint`
- Skill: `action-tracker`
- When: once at 2026-12-17 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: Run a 2027 downside case by payer.
Action in scope: A01 (Run a 2027 downside case by payer). Done when: Base, downside and severe scenarios reviewed by the CFO, with cash runway and the trigger points that move the organization from base to downside.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A02 checkpoint: List every commercial contract renewing in 2027 with escalator and notice dates

- Job id: `A02-checkpoint`
- Skill: `action-tracker`
- When: once at 2026-12-17 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: List every commercial contract renewing in 2027 with escalator and notice dates.
Action in scope: A02 (List every commercial contract renewing in 2027 with escalator and notice dates). Done when: Every commercial contract has a notice deadline, an escalator and a negotiation-prep start date on the schedule.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A03 checkpoint: Re-verify eligibility at every visit and flag expansion adults due for six-month renewal

- Job id: `A03-checkpoint`
- Skill: `action-tracker`
- When: once at 2026-12-18 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: Re-verify eligibility at every visit and flag expansion adults due for six-month renewal.
Action in scope: A03 (Re-verify eligibility at every visit and flag expansion adults due for six-month renewal). Done when: Eligibility runs before every visit, expansion adults are flagged, and a weekly coverage-churn worklist exists.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A01 due: Run a 2027 downside case by payer

- Job id: `A01-due`
- Skill: `downside-case-model`
- When: once at 2026-12-31 08:03 (America/New_York)

```text
Run the `downside-case-model` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: Run a 2027 downside case by payer.
Action in scope: A01 (Run a 2027 downside case by payer). Done when: Base, downside and severe scenarios reviewed by the CFO, with cash runway and the trigger points that move the organization from base to downside.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A02 due: List every commercial contract renewing in 2027 with escalator and notice dates

- Job id: `A02-due`
- Skill: `contract-renewal-radar`
- When: once at 2026-12-31 08:03 (America/New_York)

```text
Run the `contract-renewal-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: List every commercial contract renewing in 2027 with escalator and notice dates.
Action in scope: A02 (List every commercial contract renewing in 2027 with escalator and notice dates). Done when: Every commercial contract has a notice deadline, an escalator and a negotiation-prep start date on the schedule.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A03 due: Re-verify eligibility at every visit and flag expansion adults due for six-month renewal

- Job id: `A03-due`
- Skill: `medicaid-coverage-guard`
- When: once at 2027-01-01 08:03 (America/New_York)

```text
Run the `medicaid-coverage-guard` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: Re-verify eligibility at every visit and flag expansion adults due for six-month renewal.
Action in scope: A03 (Re-verify eligibility at every visit and flag expansion adults due for six-month renewal). Done when: Eligibility runs before every visit, expansion adults are flagged, and a weekly coverage-churn worklist exists.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: Optional CMS hold-harmless period on work-requirement disenrollments

- Job id: `hold-harmless-window-day-of`
- Skill: `policy-radar`
- When: once at 2027-01-01 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: Optional CMS hold-harmless period on work-requirement disenrollments, and update assumptions and the tracker.
Calendar event in scope: hold-harmless-window on 2027-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: Medicaid work requirements begin in 44 states

- Job id: `medicaid-work-requirements-day-of`
- Skill: `policy-radar`
- When: once at 2027-01-01 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: Medicaid work requirements begin in 44 states, and update assumptions and the tracker.
Calendar event in scope: medicaid-work-requirements on 2027-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: 2027 outpatient (OPPS/ASC) rule takes effect

- Job id: `opps-2027-day-of`
- Skill: `policy-radar`
- When: once at 2027-01-01 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: 2027 outpatient (OPPS/ASC) rule takes effect, and update assumptions and the tracker.
Calendar event in scope: opps-2027 on 2027-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: 2027 Medicare physician fee schedule takes effect

- Job id: `pfs-2027-day-of`
- Skill: `policy-radar`
- When: once at 2027-01-01 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: 2027 Medicare physician fee schedule takes effect, and update assumptions and the tracker.
Calendar event in scope: pfs-2027 on 2027-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: Six-month eligibility renewals for expansion adults

- Job id: `six-month-redeterminations-day-of`
- Skill: `policy-radar`
- When: once at 2027-01-01 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: Six-month eligibility renewals for expansion adults, and update assumptions and the tracker.
Calendar event in scope: six-month-redeterminations on 2027-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A04 checkpoint: Give price estimates, collect at time of service, offer payment plans

- Job id: `A04-checkpoint`
- Skill: `action-tracker`
- When: once at 2027-01-15 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: Give price estimates, collect at time of service, offer payment plans.
Action in scope: A04 (Give price estimates, collect at time of service, offer payment plans). Done when: Estimate, collection and payment-plan scripts are live, the financial assistance policy is updated, and the POS collection rate is tracked weekly.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A04 due: Give price estimates, collect at time of service, offer payment plans

- Job id: `A04-due`
- Skill: `point-of-service-collections`
- When: once at 2027-01-29 08:03 (America/New_York)

```text
Run the `point-of-service-collections` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: Give price estimates, collect at time of service, offer payment plans.
Action in scope: A04 (Give price estimates, collect at time of service, offer payment plans). Done when: Estimate, collection and payment-plan scripts are live, the financial assistance policy is updated, and the POS collection rate is tracked weekly.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A05 checkpoint: Help Medicaid patients document work hours and exemptions

- Job id: `A05-checkpoint`
- Skill: `action-tracker`
- When: once at 2027-03-17 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: Help Medicaid patients document work hours and exemptions.
Action in scope: A05 (Help Medicaid patients document work hours and exemptions). Done when: At-risk patients receive outreach, exemption screening is part of intake, and diagnosis documentation supports frailty exemptions where accurate.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A06 checkpoint: Audit AI-assisted coding before payers do

- Job id: `A06-checkpoint`
- Skill: `action-tracker`
- When: once at 2027-03-17 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: Audit AI-assisted coding before payers do.
Action in scope: A06 (Audit AI-assisted coding before payers do). Done when: E/M distribution by provider compared to baseline and benchmark, probe sample reviewed, findings and corrective actions documented.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A05 due: Help Medicaid patients document work hours and exemptions

- Job id: `A05-due`
- Skill: `medicaid-coverage-guard`
- When: once at 2027-03-31 08:03 (America/New_York)

```text
Run the `medicaid-coverage-guard` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: Help Medicaid patients document work hours and exemptions.
Action in scope: A05 (Help Medicaid patients document work hours and exemptions). Done when: At-risk patients receive outreach, exemption screening is part of intake, and diagnosis documentation supports frailty exemptions where accurate.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A06 due: Audit AI-assisted coding before payers do

- Job id: `A06-due`
- Skill: `coding-integrity-audit`
- When: once at 2027-03-31 08:03 (America/New_York)

```text
Run the `coding-integrity-audit` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: Audit AI-assisted coding before payers do.
Action in scope: A06 (Audit AI-assisted coding before payers do). Done when: E/M distribution by provider compared to baseline and benchmark, probe sample reviewed, findings and corrective actions documented.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Prep: HIPAA Security Rule overhaul: final action targeted

- Job id: `hipaa-security-rule-prep`
- Skill: `vendor-resilience`
- When: once at 2027-04-02 07:31 (America/New_York)

```text
Run the `vendor-resilience` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Prepare for: HIPAA Security Rule overhaul: final action targeted. HHS pushed the final rule to July 2027. Proposed provisions (not final) include mandatory encryption, MFA and asset inventories.
Calendar event in scope: hipaa-security-rule on 2027-07-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Prep: Medicaid provider tax safe harbor begins phasing down (FFY 2028)

- Job id: `provider-tax-phase-down-prep`
- Skill: `financing-cliff-2028`
- When: once at 2027-06-03 07:31 (America/New_York)

```text
Run the `financing-cliff-2028` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Prepare for: Medicaid provider tax safe harbor begins phasing down (FFY 2028). Expansion states step down from 6% toward 3.5%. Nursing homes and ICFs are exempt from the phase-down.
Calendar event in scope: provider-tax-phase-down on 2027-10-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A07 checkpoint: Move eligible imaging, infusion and procedures to office or ASC settings

- Job id: `A07-checkpoint`
- Skill: `action-tracker`
- When: once at 2027-06-16 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: Move eligible imaging, infusion and procedures to office or ASC settings.
Action in scope: A07 (Move eligible imaging, infusion and procedures to office or ASC settings). Done when: Each candidate service has a margin comparison by site and a go or no-go decision with an owner.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A08 checkpoint: Inventory vendors holding PHI and test downtime and claims backup

- Job id: `A08-checkpoint`
- Skill: `action-tracker`
- When: once at 2027-06-16 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: Inventory vendors holding PHI and test downtime and claims backup.
Action in scope: A08 (Inventory vendors holding PHI and test downtime and claims backup). Done when: Cash-critical vendors identified, BAAs confirmed, a backup clearinghouse path exists and a downtime tabletop has been run.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A07 due: Move eligible imaging, infusion and procedures to office or ASC settings

- Job id: `A07-due`
- Skill: `site-of-care-shift`
- When: once at 2027-06-30 08:03 (America/New_York)

```text
Run the `site-of-care-shift` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: Move eligible imaging, infusion and procedures to office or ASC settings.
Action in scope: A07 (Move eligible imaging, infusion and procedures to office or ASC settings). Done when: Each candidate service has a margin comparison by site and a go or no-go decision with an owner.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A08 due: Inventory vendors holding PHI and test downtime and claims backup

- Job id: `A08-due`
- Skill: `vendor-resilience`
- When: once at 2027-06-30 08:03 (America/New_York)

```text
Run the `vendor-resilience` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: Inventory vendors holding PHI and test downtime and claims backup.
Action in scope: A08 (Inventory vendors holding PHI and test downtime and claims backup). Done when: Cash-critical vendors identified, BAAs confirmed, a backup clearinghouse path exists and a downtime tabletop has been run.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Prep: CY 2028 proposed physician and outpatient rules (expected)

- Job id: `cy2028-proposed-rules-prep`
- Skill: `downside-case-model`
- When: once at 2027-07-01 07:31 (America/New_York)

```text
Run the `downside-case-model` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Prepare for: CY 2028 proposed physician and outpatient rules (expected). In 2026 CMS released the proposed outpatient rule on July 2 and the physician rule on July 14. Expect the 2028 versions in early to mid July 2027.
Calendar event in scope: cy2028-proposed-rules on 2027-07-15. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: HIPAA Security Rule overhaul: final action targeted

- Job id: `hipaa-security-rule-day-of`
- Skill: `policy-radar`
- When: once at 2027-07-01 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: HIPAA Security Rule overhaul: final action targeted, and update assumptions and the tracker.
Calendar event in scope: hipaa-security-rule on 2027-07-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Prep: State-directed payment phase-down begins

- Job id: `sdp-phase-down-prep`
- Skill: `financing-cliff-2028`
- When: once at 2027-07-05 07:31 (America/New_York)

```text
Run the `financing-cliff-2028` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Prepare for: State-directed payment phase-down begins. Payments above 100% of Medicare (expansion states) or 110% (non-expansion) fall 10 percentage points a year. First-year federal cut estimated at $8.7 billion.
Calendar event in scope: sdp-phase-down on 2028-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: CY 2028 proposed physician and outpatient rules (expected)

- Job id: `cy2028-proposed-rules-day-of`
- Skill: `policy-radar`
- When: once at 2027-07-15 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: CY 2028 proposed physician and outpatient rules (expected), and update assumptions and the tracker.
Calendar event in scope: cy2028-proposed-rules on 2027-07-15. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A10 checkpoint: Model provider tax and state-directed payment exposure for 2028

- Job id: `A10-checkpoint`
- Skill: `action-tracker`
- When: once at 2027-09-16 08:03 (America/New_York)

```text
Run the `action-tracker` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Two weeks out: Model provider tax and state-directed payment exposure for 2028.
Action in scope: A10 (Model provider tax and state-directed payment exposure for 2028). Done when: 2028 to 2032 exposure by program is modeled and built into the 2028 budget.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## A10 due: Model provider tax and state-directed payment exposure for 2028

- Job id: `A10-due`
- Skill: `financing-cliff-2028`
- When: once at 2027-09-30 08:03 (America/New_York)

```text
Run the `financing-cliff-2028` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Due today: Model provider tax and state-directed payment exposure for 2028.
Action in scope: A10 (Model provider tax and state-directed payment exposure for 2028). Done when: 2028 to 2032 exposure by program is modeled and built into the 2028 budget.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: Medicaid provider tax safe harbor begins phasing down (FFY 2028)

- Job id: `provider-tax-phase-down-day-of`
- Skill: `policy-radar`
- When: once at 2027-10-01 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: Medicaid provider tax safe harbor begins phasing down (FFY 2028), and update assumptions and the tracker.
Calendar event in scope: provider-tax-phase-down on 2027-10-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Prep: CY 2028 final physician and outpatient rules (expected)

- Job id: `cy2028-final-rules-prep`
- Skill: `downside-case-model`
- When: once at 2027-10-29 07:31 (America/New_York)

```text
Run the `downside-case-model` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Prepare for: CY 2028 final physician and outpatient rules (expected). The 2027 final rules were released November 4, 2026. Expect 2028 finals in early November 2027.
Calendar event in scope: cy2028-final-rules on 2027-11-05. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: CY 2028 final physician and outpatient rules (expected)

- Job id: `cy2028-final-rules-day-of`
- Skill: `policy-radar`
- When: once at 2027-11-05 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: CY 2028 final physician and outpatient rules (expected), and update assumptions and the tracker.
Calendar event in scope: cy2028-final-rules on 2027-11-05. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```

## Day of: State-directed payment phase-down begins

- Job id: `sdp-phase-down-day-of`
- Skill: `policy-radar`
- When: once at 2028-01-03 07:31 (America/New_York)

```text
Run the `policy-radar` skill from the healthcare-2027-autopilot plugin for Lakeshore Community Hospital (fictional sample).
Readiness workspace: examples/sample-hospital (profile.json, assumptions.json, inputs/, state/, outputs/).
Purpose of this run: Confirm what happened: State-directed payment phase-down begins, and update assumptions and the tracker.
Calendar event in scope: sdp-phase-down on 2028-01-01. Confirm the date still holds with a source scored 4 or higher before acting on it.
Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.
Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.
Deliver a short summary through: email. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.
Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.
```
