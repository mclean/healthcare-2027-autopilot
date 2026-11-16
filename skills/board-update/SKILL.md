---
name: board-update
description: Drafts the quarterly board, owner or investor update on 2027 readiness (exposure range, plan status and critical path, KPI trends and triggers, assumption changes with sources, decisions requested and risks) from the workspace's latest outputs. Use when the leader asks "draft the board update", "investor update on 2027", "summarize readiness for the owners", "quarterly update", or on the scheduled quarterly run.
---

# Board update

A board or sponsor wants three things: how big the exposure is, whether management has it in hand, and what it needs from them. Read `../../reference/conventions.md` first.

## Gather (do not recompute what exists)

- Latest downside case (`outputs/model/`), rerun first if older than the quarter.
- Tracker report and critical path (`state/tracker.json`).
- Last three KPI pulses and fired triggers.
- Policy log entries for the quarter and assumption changes in `assumptions.json`.
- Contract radar, deal timeline, financing cliff and site-of-care outputs where they exist.
- The data readiness map, for the confidence line.

## Draft `outputs/board/<date>-board-update.md` (two pages at most)

1. **Summary (three sentences):** the exposure range for the year, the scenario management is planning against and why, the one thing the board should know.
2. **Exposure:** the scenario table and the revenue bridge, with each driver's source. Note what changed since last quarter and why.
3. **Plan status:** actions done, on track, at risk; the critical path; any slipped dates with consequences.
4. **Signals:** KPI trends against baseline, triggers that fired and what was done about them.
5. **Policy and market changes:** only those that moved an assumption, each with its source.
6. **Decisions requested:** each with a recommendation, the alternative, and the date needed (for example, approval of a secondary clearinghouse contract, a capital request for a site-of-care move, a change to a deal's close date).
7. **Risks and confidence:** the two assumptions that move the answer most, and the data grade of the key numbers.

Attach the downside case HTML and the tracker HTML. Deliver the draft to the leader only; the leader edits and sends it.

## What most board updates get wrong

- **Too much activity, too little exposure.** Lead with the range and the plan's effect on it.
- **Assumptions without provenance.** Boards trust a number more when they can see where it came from and how it moved.
- **Decisions buried at the end.** Put the ask in the summary too.
