---
name: weekly-leader-brief
description: Produces the Monday leader brief for the 2027 readiness program: the decisions owed, what is blocked, contract and regulatory deadlines in the next 60 days, KPI triggers and policy changes, with a short read on what matters most and what to ignore. Use when the leader asks "what do I need to know this week", "send me my brief", "weekly readiness update", "what's coming up", or on the scheduled Monday run.
---

# Weekly leader brief

One page, read in three minutes, that tells the leader what needs them this week. The script assembles the facts; the agent supplies judgment. Read `../../reference/conventions.md` first.

## Steps

1. **Refresh the facts layer.**
   - If the tracker has not been reported since Friday, run `python3 ../../scripts/tracker.py report --workspace <ws>`.
   - Run `python3 ../../scripts/weekly_brief.py --workspace <ws>`. It writes `outputs/briefs/<date>-weekly-brief.md` and `.html` with: needs-you items (decisions, blocks, contract notice deadlines within 30 days, fired KPI triggers), dated items in the next 60 days, policy changes from the last 14 days, and plan status.
2. **Read it as the leader's chief of staff would.** Then write the brief the leader actually receives, on top of the facts:
   - **Line 1:** the single most important thing this week, with its date and consequence.
   - **Needs you (at most five):** decisions first. For each decision, give a recommendation and the reason in one sentence, plus what happens if it waits a week.
   - **Coming up:** only items that need preparation this week, not everything on the calendar.
   - **Signals:** group related triggers into one story (self-pay up, coverage denials up and point-of-service collections down are one story: coverage churn reaching the front desk).
   - **Safe to ignore this week:** one or two items that look alarming but are handled, so the leader does not spend time on them.
   - **Confidence:** one line naming any number in the brief that rests on tier C or D data.
3. **Deliver** through the profile's channel. Attach or link the HTML for the full facts. Keep the message body under 250 words.

## Judgment rules

- Rank by consequence and reversibility, not by order of discovery. A notice deadline in 15 days outranks a KPI drifting for the third month.
- Name owners. "VP managed care needs a yes or no on Payer D by Friday" beats "contract decision pending".
- Say when the plan is working. A brief that only lists problems trains the leader to stop reading.
- If nothing needs the leader, the brief is three lines long. That is a good week, and the brief should say so.
- Never introduce a number that is not in the workspace or a scored source.

## Example opening (from the fictional sample)

> Two filings decide whether both 2027 acquisitions close on time: Indiana needs 90 days' notice for Project Birch, so the filing is due by December 31, and Oregon's review for Project Cedar should start now. General counsel needs your call on Birch's close date this week.

## What most briefs get wrong

- **They report activity instead of exposure.** "Eligibility tool live at 6 sites" matters less than "coverage denials hit 2.6% of claims, above the 2% trigger".
- **They bury the date.** Every item carries a date or it does not belong in the brief.
- **They repeat last week.** Unchanged items move to a single line: "Unchanged: A04, A05, A06 on track."
