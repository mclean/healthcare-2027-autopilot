---
name: cadence-scheduler
description: Builds and creates the leader's schedule of recurring and one-time agent jobs (weekly brief, policy radar, KPI pulse, contract reminders, milestone checks) with fallbacks from Claude scheduled tasks to cron, GitHub Actions and calendar reminders. Use when the leader says "schedule the readiness jobs", "set up my cron jobs", "keep me on track automatically", "change when my brief arrives", "pause the autopilot", or after readiness-setup finishes.
---

# Cadence scheduler

Make the plan run itself. Every job is a self-contained prompt that a fresh agent session can execute with nothing but the workspace. Read `../../reference/conventions.md` first.

## Build the schedule

1. Confirm `profile.json` exists and has the leader's timezone and delivery channel. If contracts are loaded, run `python3 ../../scripts/contract_radar.py --workspace <ws>` first so contract reminders are included.
2. Run:

```
python3 ../../scripts/build_schedule.py --workspace <ws> --workspace-label "<how a fresh session finds the workspace, e.g. the connected folder 'Readiness 2027'>"
```

3. Review `schedule/schedule.html` with the leader: the recurring cadence (from `../../reference/schedule-catalog.json`), the one-time milestone jobs (prep and day-of for each applicable calendar event, a checkpoint 14 days before and a verification on each action's due date), and contract reminders at 180, 120, 90, 60 and 30 days before each notice deadline.
4. Move anything that collides with the leader's week by adding `schedule_overrides` to `profile.json` (`{"weekly-brief": "17 6 * * 1"}`) and rebuilding.

## Create the jobs: pick the highest tier that works here

**Tier A: scheduled tasks in the agent platform.** Look for the platform's scheduling tool (in Claude, the scheduled task tools, which may need loading through tool search). Before creating anything, list existing scheduled tasks and skip or update any job that already exists under the same name. Create one task per job in `schedule/scheduled-task-prompts.md`:
- Recurring jobs: the cron line as written, with the leader's timezone (`CRON_TZ=<tz> <cron>`).
- One-time jobs: the date and time in the leader's timezone.
- Name each task with the job name so the leader recognizes it in their task list.
- If the task needs files on the leader's computer, mark it as requiring that computer and attach the workspace folder.
- Tell the leader in one sentence which approval setting the tasks received, and that runs which stop for approval can be switched to automatic approval in the task's settings if their organization allows it.
- Do not promise a delivery time to the minute; shared schedulers can start a run a few minutes late. The catalog's off-the-hour times reduce that.

Creating 60 one-time tasks is noisy. Default to creating every recurring job plus the one-time jobs in the next 90 days; the Friday tracker close-out creates the next tranche each month (step "Roll forward").

**Tier B: headless agent.** When the platform has no scheduler, or the organization wants runs on its own infrastructure:
- `schedule/crontab.txt` for a machine that stays on, using `claude -p` with the prompt files in `schedule/prompts/headless/`. Requires the Claude CLI with this plugin installed and an API key in the environment.
- `schedule/github-actions/*.yml` for a private repository that holds the workspace under `readiness/`. Requires an `ANTHROPIC_API_KEY` repository secret. GitHub cron runs in UTC; the files are converted from local time and drift an hour across daylight saving changes.

**Tier C: calendar reminders.** Import `schedule/readiness-calendar.ics` into the leader's calendar. Each event says which skill to ask the agent to run. This keeps the cadence even with no automation at all.

**Tier D: the printed map.** `schedule/schedule.html` printed or pinned is the floor.

Record the tier actually used in `profile.json` `infrastructure.scheduler` and tell the leader what fires next and when.

## Roll forward (monthly, inside the Friday close-out nearest month end)

Rebuild the schedule, create one-time jobs entering the 90-day window, and delete jobs for actions marked done or not applicable. Re-run after any change to contracts, deals, owners or the calendar.

## Pause, resume, change

- Pause: disable (do not delete) every task whose name starts with the job names in `schedule/jobs.json`; note the pause in the tracker.
- Change delivery or timing: update `profile.json`, rebuild, update the existing tasks in place.
- Remove: only on the leader's explicit request; list what will be removed first.

## Design rules for prompts (already built into the generator; keep them if editing by hand)

- Self-contained: name the plugin, the skill, the workspace and the purpose of the run.
- State lives in files: read profile and state first, write outputs and tracker updates last.
- Tiered data: walk the fallback chain and grade every number.
- Quiet by default: jobs marked deliver-only-if-material send nothing when nothing changed.
- Safe: no messages to anyone but the leader, no changes to contracts, claims or records, stop before anything irreversible.

## What most schedules get wrong

- **Too many deliveries.** A leader who gets nine messages a week reads none. Only the Monday brief, the monthly pulse and true alerts should reach the leader; everything else lands in the workspace and surfaces through the brief.
- **Reminders on the renewal date.** The decision date is the notice deadline, often 90 to 180 days earlier. The contract reminders are keyed to notice deadlines for that reason.
- **No day-of confirmation.** Policy dates move (the 2027 physician rule landed deeper than proposed). Every calendar event gets a day-of job that confirms what actually happened before assumptions change.
