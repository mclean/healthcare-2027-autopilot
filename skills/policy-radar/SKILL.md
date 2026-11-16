---
name: policy-radar
description: Watches CMS, Congress, state Medicaid agencies, courts and industry data for changes that move the 2027 readiness plan (work requirement elections and lawsuits, physician and outpatient payment rules, fee schedule fixes, state transaction laws, HIPAA security rules), scores each source, logs material changes and proposes assumption updates. Use when the leader asks "what changed in healthcare policy this week", "did Congress fix the physician cut", "which states took the hold-harmless option", "is the date still January 1", or on the scheduled Thursday run and calendar day-of jobs.
---

# Policy radar

Find the few changes that move the plan, prove them with good sources, and update the plan's assumptions on the record. Read `../../reference/conventions.md` and `../../reference/source-scoring.md` first.

## Weekly scan (scheduled Thursday)

1. **Build this week's watch list** from three places:
   - The standing watchlist in `../../reference/source-scoring.md`.
   - Open questions in `state/policy_log.json` (anything marked "watching").
   - Calendar events in `../../reference/regulatory-calendar.json` within the next 60 days that apply to this organization, plus anything with status "expected" or "optional per state".
2. **Search.** Use web search for each item with the current month and year in the query, then open the primary page before trusting a snippet. Prefer, in order: CMS and Federal Register, state Medicaid agency pages, Congress.gov, CBO, KFF, then law firm alerts and trade press.
3. **Score** each candidate change for credibility and depth. Material changes need a source scored 4 or 5, or two independent sources scored 3.
4. **Decide materiality.** A change is material if it moves a date in the calendar, an assumption in `assumptions.json`, the applicability of an action, or a threshold. Everything else is noise for this program, however newsworthy.
5. **Log** material changes in `state/policy_log.json` with: date, headline, source (name, url, credibility), the assumption or date it affects (from and to), and a one-line "so what" for this organization.
6. **Propose, do not impose.** For an assumption change, write the proposed new value into the log entry with status "proposed". Apply it to `assumptions.json` (with `set_by` and source) only when it is sourced at the required level and is a matter of fact (a final rule's conversion factor). For judgment calls (a disenrollment rate), leave it proposed for the CFO and raise it in the brief.
7. **Re-run what changed.** If an applied change affects the model, run `downside_model.py`; if it moves a date, rebuild the schedule through cadence-scheduler.
8. **Deliver only if material.** Otherwise the Monday brief picks it up.

## Day-of jobs (on a calendar event's date)

Confirm what actually happened. Did the rule take effect as written? Did the state start enforcement or elect the hold-harmless period? Update the event's status in the policy log and the assumption register. Then tell the leader in two lines what changed for them.

## Standing watch items for this cycle (as of November 2026)

- **Work requirement hold-harmless elections** for each state in the profile. CMS offered the option on November 13, 2026; disenrollments can wait until June 30, 2027. The election decides whether coverage losses hit cash in Q1 or Q3 (assumption `hold_harmless_elected`).
- **Litigation:** *Massachusetts v. Oz* (partial vacatur, October 29, 2026) and the four-state suit filed November 5, 2026.
- **A year-end physician payment fix.** The 2027 conversion factor fell 2.31% for most clinicians; physician groups are lobbying Congress (assumption `pfs_cf_change`).
- **CY 2028 proposed rules** expected in early to mid July 2027; finals expected in early November 2027.
- **HIPAA Security Rule** final action targeted for July 2027.
- **State transaction laws** in profile states, especially pending bills in New York, Pennsylvania and New Jersey.
- **Data releases:** Kaufman Hall's monthly Flash Report, Marsh's final employer survey results, KFF marketplace enrollment and premium analyses.

## What most radars get wrong

- **They report news instead of deltas.** The output is "assumption X moved from A to B because of source Y", not a headline digest.
- **They trust the first summary.** Secondary sources get counts wrong. The source this plugin was built from had to correct a trade summary's "eight states" to the primary report's nine laws in six states.
- **They confuse proposed with final.** A proposed rule changes the watch list; only a final rule changes the model.
