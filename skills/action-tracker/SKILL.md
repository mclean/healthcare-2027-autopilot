---
name: action-tracker
description: Maintains the readiness action plan as the single source of truth (owners, due dates, dependencies, evidence, derived status and the critical path) and runs the Friday close-out that chases owners and flags slips. Use when the leader asks "where are we on the plan", "what's late", "update the tracker", "mark A02 done", "who owns this", "what's the critical path", or on the scheduled Friday close-out and action checkpoints.
---

# Action tracker

Keep `state/tracker.json` true. Everything else (the brief, the board update, the schedule) reads from it. Read `../../reference/conventions.md` first.

## Commands

```
python3 ../../scripts/tracker.py report --workspace <ws>
python3 ../../scripts/tracker.py update --workspace <ws> --id A04 --status on_track --note "Estimate script live at 4 of 9 sites" [--owner "Name"] [--decision "..."] [--evidence outputs/...]
```

Statuses a person sets: `not_started`, `on_track`, `at_risk`, `blocked`, `done`, `n/a`. The script derives the rest: an item past due is `late`; an item whose dependency is unfinished past its own due date is `blocked`; a not-started item due within 21 days is `at_risk`.

## Friday close-out (scheduled)

1. **Gather status without bothering people.** Look for evidence in the workspace first: new outputs, updated inputs, notes. Then check connected tools the leader has authorized (task tracker, email threads the leader is on) for progress on each open action. Record what you find with `update`, citing where it came from.
2. **Done means evidence.** Mark an action `done` only when its `done_when` condition is met and there is evidence (a file, a decision record, an email from the owner). Attach the path with `--evidence`.
3. **Run the report.** Read the derived statuses and the critical path.
4. **Draft nudges, do not send them.** For each at-risk, blocked or late item, draft a two-sentence note to the owner (what is due, what is missing, the date). Put the drafts in `outputs/tracker/<date>-nudges.md` and list them in the delivery so the leader can forward them in one step.
5. **Decisions.** If an item cannot move without the leader, set `--decision` with the exact decision and the date it is needed by. The Monday brief leads with these.
6. **Roll the schedule forward** at month end by running the cadence-scheduler skill.
7. **Deliver only if material:** a status changed, a new decision is needed, or the critical path moved.

## Checkpoint jobs (14 days before a due date)

Answer three questions in the tracker note: will it be done by the due date, what is blocking it, what does the leader need to do. If the answer to the first is no, set `at_risk` and propose a new date with the consequence of slipping (what downstream action moves).

## Due-date jobs

Verify the `done_when` condition. If met, mark done with evidence. If not, set the honest status and a decision for the leader: extend (with new date), descope (what is dropped), or escalate (who needs to act).

## Re-planning rules

- Never silently move a due date. Every change gets a history note with the reason.
- When an upstream date moves (a calendar event, a deal close, a payer notice deadline), recompute the downstream actions and say which ones moved.
- When a KPI trigger fires (`state/triggers.json`), add a note to the action its skill belongs to, and set it to at least `at_risk` if the trigger means the current plan is not working.

## What most trackers miss

- **The critical path is the only schedule that matters.** Ten green items do not offset one late item on the critical path. Lead with it.
- **"Blocked" is a request, not a status.** Every blocked item names who can unblock it and by when.
- **Evidence beats updates.** A tracker that says "on track" for six weeks with no evidence is the most dangerous kind.
