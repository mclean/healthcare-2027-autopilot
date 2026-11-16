---
name: readiness-setup
description: Sets up a healthcare organization's 2027 readiness program end to end: interviews the leader, classifies the organization into one of five archetypes, creates the readiness workspace, grades every data dependency, seeds the action tracker and hands off to cadence-scheduler. Use when a leader says "set up the 2027 readiness autopilot", "get me ready for 2027", "start the readiness program", "onboard my organization", or opens the plugin for the first time.
---

# Readiness setup

Turn a leader's description of their organization into a running program in one session: profile, workspace, data map, action plan, schedule, first brief. Read `../../reference/conventions.md` first.

## Outcome

- A readiness workspace with `profile.json`, `assumptions.json`, `inputs/` templates and `state/tracker.json`.
- A data readiness map with the grade of every input and the top upgrades.
- The schedule built and created (through cadence-scheduler).
- A first weekly brief delivered, so the leader sees the system working the same day.

## Steps

### 1. Interview (about 10 minutes)

Ask at most four questions at a time; skip anything already known from the conversation or connected tools. Offer choices where possible.

1. **Organization:** name, what it does, how many clinicians or beds, which states.
2. **Archetype:** confirm one of `physician-group`, `platform-mso`, `community-hospital`, `asc-imaging-infusion`, `outpatient-services` (definitions in `../../reference/segment-archetypes.md`). If it straddles two, pick the one whose biggest exposure matches theirs and note the other.
3. **Money:** 2026 net revenue, operating expense and cash on hand (round numbers are fine; they become tier C until finance confirms). Whether they bill Medicare Part B, run hospital outpatient departments, receive Medicaid supplemental payments, or are a qualifying APM participant.
4. **Systems:** EHR/PM, clearinghouse, where executed payer contracts live, BI or data warehouse if any. Each answer maps to a data tier (step 3).
5. **Deals:** any acquisition, affiliation, recapitalization or sale that could close in 2027, with states and rough dates.
6. **Rhythm:** timezone, the day the leader plans the week, where deliveries should land (email, chat, a folder), and who owns finance, revenue cycle, managed care, compliance and IT.

If the session is unattended, infer what is reasonable from connected tools and files, mark inferred answers as tier C, and list them at the top of the first brief for confirmation.

### 2. Create the workspace

Pick the state store with the leader, in this order of preference: a connected folder on their computer (works with scheduled tasks that run on that computer), a cloud drive folder reachable by connector, a private Git repository (for GitHub Actions), a local folder for cron. Then run:

```
python3 ../../scripts/init_workspace.py --workspace "<path>" --archetype <id> --org "<name>" --states IL,IN --tz America/Chicago
```

Fill `profile.json` from the interview: financials, flags (`bills_medicare_part_b`, `hospital_outpatient`, `receives_supplemental_payments`, `apm_qualifying`), `deal_pipeline`, `infrastructure` (scheduler, state store and a human label for it, delivery channel), and `kpi_baseline_period` (the most recent month before 2027 effects, usually September or October 2026).

### 3. Grade the data

For each dependency in `../../reference/dependencies.json`, set `data_tiers` from what the interview revealed:
- A connector or warehouse query exists and works now: **A**.
- Someone can export the report monthly: **B**.
- A leader can estimate it: **C**.
- Nothing yet: **D** (the plugin uses the public default and labels it directional).

Run `python3 ../../scripts/data_readiness.py --workspace <ws>` and walk the leader through the top three upgrades. Assign each upgrade an owner; add them to the tracker notes for A00.

### 4. Seed the plan

```
python3 ../../scripts/tracker.py init --workspace <ws>
python3 ../../scripts/tracker.py update --workspace <ws> --id A01 --owner "<CFO name>" --status not_started --note "Owner confirmed at setup"
```

Assign an owner to every applicable action (the register drops actions that do not apply to the archetype). Ask whether any default due date in `../../reference/action-register.json` is wrong for them and adjust with an update note.

### 5. First model pass

If any payer mix exists (export or estimate), put it in `inputs/payer_mix.csv` and run `python3 ../../scripts/downside_model.py --workspace <ws>`. A directional first number on day one changes how seriously the program is taken. Label it with its grade.

### 6. Schedule

Hand off to the `cadence-scheduler` skill with the profile in place. Do not create scheduled jobs here.

### 7. First brief

Run the `weekly-leader-brief` skill now, even mid-week. Close setup by telling the leader, in five lines or fewer: what was set up, the confidence grade of the plan today, the single most valuable data upgrade, the first decision they owe, and when the first scheduled run fires.

## What most setups miss

- **The deal calendar is a data dependency.** An Indiana acquisition closing March 31, 2027 needs its 90-day notice filed by December 31, 2026. Ask about deals on day one; deal-readiness turns them into filing dates.
- **The baseline month matters more than the threshold.** Pick a pre-2027 month as the KPI baseline so the pulse measures change caused by 2027, not seasonality from a random month.
- **Owners beat roles.** A tracker full of "CFO" with no names produces reminders nobody owns. Get names.
- **Seven states are outside the work requirements** (WY, TX, KS, MS, AL, FL, SC per Morgan Lewis). For organizations only in those states, the coverage work narrows to exchange coverage loss and ordinary Medicaid renewals; say so instead of running the full playbook.
