# Skill reference

Generated from each `skills/*/SKILL.md` and the action register. Ask for any skill by name or with the phrases in the second column.

## `action-tracker`

Maintains the readiness action plan as the single source of truth (owners, due dates, dependencies, evidence, derived status and the critical path) and runs the Friday close-out that chases owners and flags slips.

- **Ask for it when** the leader asks "where are we on the plan", "what's late", "update the tracker", "mark A02 done", "who owns this", "what's the critical path", or on the scheduled Friday close-out and action checkpoints.
- **Actions:** recurring
- **Scheduled as:** Friday action tracker close-out
- **Engine scripts:** `tracker.py`

## `board-update`

Drafts the quarterly board, owner or investor update on 2027 readiness (exposure range, plan status and critical path, KPI trends and triggers, assumption changes with sources, decisions requested and risks) from the workspace's latest outputs.

- **Ask for it when** the leader asks "draft the board update", "investor update on 2027", "summarize readiness for the owners", "quarterly update", or on the scheduled quarterly run.
- **Actions:** recurring
- **Scheduled as:** Quarterly board or investor update
- **Engine scripts:** none

## `cadence-scheduler`

Builds and creates the leader's schedule of recurring and one-time agent jobs (weekly brief, policy radar, KPI pulse, contract reminders, milestone checks) with fallbacks from Claude scheduled tasks to cron, GitHub Actions and calendar reminders.

- **Ask for it when** the leader says "schedule the readiness jobs", "set up my cron jobs", "keep me on track automatically", "change when my brief arrives", "pause the autopilot", or after readiness-setup finishes.
- **Actions:** recurring
- **Scheduled as:** on demand or milestone jobs
- **Engine scripts:** `build_schedule.py`, `contract_radar.py`

## `coding-integrity-audit`

Audits coding patterns before payers do, especially after AI documentation or ambient scribe rollouts: E/M level distribution by provider against a pre-AI baseline and a specialty benchmark, a reproducible probe sample, coder review against 2021 E/M guidelines, AI tool settings review and a documented corrective plan.

- **Ask for it when** the leader or compliance officer asks "are we upcoding", "audit our AI scribe coding", "payers are asking about our E/M levels", "run the coding audit", or on the scheduled quarterly audit.
- **Actions:** A06 (due 2027-03-31)
- **Scheduled as:** Quarterly coding integrity audit
- **Engine scripts:** `coding_audit.py`

## `contract-renewal-radar`

Inventories every payer contract, computes the real decision date (the notice deadline, not the renewal date), schedules reminders at 180, 120, 90, 60 and 30 days, flags windows already missed and contracts tied to the Medicare fee schedule, and builds a negotiation prep pack for 2027 renewals.

- **Ask for it when** the leader asks "which contracts renew in 2027", "when do we have to give notice", "prep me for the payer negotiation", "are we tied to the Medicare fee schedule", or on the scheduled Tuesday contract watch.
- **Actions:** A02 (due 2026-12-31)
- **Scheduled as:** Contract notice-window watch
- **Engine scripts:** `contract_radar.py`

## `data-readiness`

Grades every data input the readiness program depends on (payer mix, Medicaid roster, contracts, A/R, coding, vendors and more) on a four-tier fallback ladder, shows how data gaps lower the confidence of each action, and ranks the cheapest upgrades.

- **Ask for it when** the leader asks "what data do we need", "how good is our data", "why is this number directional", "what should we export", during setup, or on the monthly re-check.
- **Actions:** recurring
- **Scheduled as:** Monthly data readiness re-check
- **Engine scripts:** `data_readiness.py`

## `deal-readiness`

Keeps 2027 healthcare acquisitions, affiliations and recapitalizations on schedule under new state transaction and corporate-practice laws: works back from each target close through every state's notice period, flags filings due now, and checks MSO and professional corporation governance and deal documents for regulator review.

- **Ask for it when** the leader asks "when do we have to file for this deal", "which states need notice", "will Oregon's law affect our MSO", "is our MSO structure compliant", "add the deal to the plan", or when a deal enters the pipeline.
- **Actions:** A09 (due before any deal)
- **Scheduled as:** on demand or milestone jobs
- **Engine scripts:** `deal_timeline.py`

## `downside-case-model`

Builds and maintains the 2027 downside case by payer (base, downside and severe scenarios for Medicaid work-requirement churn, exchange coverage loss, the Medicare fee schedule cut and commercial renewals) with a revenue bridge, cash runway, sensitivity ranking, early-warning triggers and an assumption register tied to sources.

- **Ask for it when** the leader or CFO asks "run the downside case", "how much revenue is at risk in 2027", "what if our state doesn't take the hold-harmless option", "stress test the budget", "update the model", or when policy-radar or kpi-pulse calls for a rerun.
- **Actions:** A01 (due 2026-12-31)
- **Scheduled as:** on demand or milestone jobs
- **Engine scripts:** `downside_model.py`

## `financing-cliff-2028`

Models a hospital's exposure to the Medicaid financing changes that start right after 2027 (provider tax safe harbor phase-down from October 1, 2027 and state-directed payment cuts from January 1, 2028), year by year through 2033, with state response scenarios and budget integration.

- **Ask for it when** a hospital leader asks "what happens to our supplemental payments", "model the provider tax phase-down", "how big is the 2028 cliff", "state-directed payment exposure", or on the A10 checkpoint.
- **Actions:** A10 (due 2027-09-30)
- **Scheduled as:** on demand or milestone jobs
- **Engine scripts:** `financing_cliff.py`

## `kpi-pulse`

Runs the monthly KPI pulse for the 2027 readiness program (payer mix shift, self-pay share, coverage denials, point-of-service collections, bad debt, days in A/R, high-level E/M share, contract and vendor gaps), compares each to a pre-2027 baseline, fires triggers and routes each one to the skill that handles it.

- **Ask for it when** the leader asks "how are the numbers", "is coverage churn showing up", "run the KPI pulse", "are we in the downside case", or on the scheduled monthly run.
- **Actions:** recurring
- **Scheduled as:** Monthly KPI pulse
- **Engine scripts:** `kpi_pulse.py`

## `medicaid-coverage-guard`

Protects patients' Medicaid coverage and the organization's revenue through the 2027 work requirements and six-month renewals: eligibility re-verification timing, expansion-adult flags, renewal-date tracking, medical frailty and exemption screening, documentation accuracy, patient outreach, coverage-denial monitoring and state hold-harmless tracking.

- **Ask for it when** the leader asks "how do we get ready for Medicaid work requirements", "are we losing Medicaid patients", "eligibility denials are up", "help patients keep coverage", "build the coverage worklist", or when kpi-pulse fires a coverage trigger.
- **Actions:** A03 (due 2027-01-01), A05 (due 2027-03-31)
- **Scheduled as:** on demand or milestone jobs
- **Engine scripts:** none

## `point-of-service-collections`

Reduces 2027 bad debt as more patients arrive uninsured or on high-deductible plans: price estimates, good faith estimates for self-pay patients, collection at time of service, payment plans, financial assistance policy updates and weekly tracking of the point-of-service collection rate.

- **Ask for it when** the leader asks "how do we cut bad debt", "self-pay is rising", "set up price estimates", "front desk collections", "update our financial assistance policy", or when kpi-pulse fires a self-pay, collection or bad debt trigger.
- **Actions:** A04 (due 2027-01-31)
- **Scheduled as:** on demand or milestone jobs
- **Engine scripts:** none

## `policy-radar`

Watches CMS, Congress, state Medicaid agencies, courts and industry data for changes that move the 2027 readiness plan (work requirement elections and lawsuits, physician and outpatient payment rules, fee schedule fixes, state transaction laws, HIPAA security rules), scores each source, logs material changes and proposes assumption updates.

- **Ask for it when** the leader asks "what changed in healthcare policy this week", "did Congress fix the physician cut", "which states took the hold-harmless option", "is the date still January 1", or on the scheduled Thursday run and calendar day-of jobs.
- **Actions:** recurring
- **Scheduled as:** Policy radar
- **Engine scripts:** none

## `readiness-setup`

Sets up a healthcare organization's 2027 readiness program end to end: interviews the leader, classifies the organization into one of five archetypes, creates the readiness workspace, grades every data dependency, seeds the action tracker and hands off to cadence-scheduler.

- **Ask for it when** a leader says "set up the 2027 readiness autopilot", "get me ready for 2027", "start the readiness program", "onboard my organization", or opens the plugin for the first time.
- **Actions:** A00 (due 2026-11-30)
- **Scheduled as:** on demand or milestone jobs
- **Engine scripts:** `data_readiness.py`, `downside_model.py`, `init_workspace.py`, `tracker.py`

## `site-of-care-shift`

Finds and sizes services to move between hospital outpatient departments, ambulatory surgery centers and offices as Medicare site-neutral pay expands (clinic visits, drug administration and, from 2027, off-campus imaging without contrast) and the inpatient-only list phases out: margin change, payback, patient savings and gating checks for each candidate.

- **Ask for it when** the leader asks "what should we move to the ASC", "how does site-neutral affect us", "is the imaging center worth it", "where should infusion live", or on the A07 checkpoint.
- **Actions:** A07 (due 2027-06-30)
- **Scheduled as:** on demand or milestone jobs
- **Engine scripts:** `site_of_care.py`

## `vendor-resilience`

Protects cash and patient data from vendor failure: inventories every vendor with PHI access, classifies which ones stop cash if they go down, confirms BAAs, sets up a backup clearinghouse path, runs downtime tabletop exercises and tracks the HIPAA Security Rule overhaul.

- **Ask for it when** the leader or CIO asks "what happens if our clearinghouse goes down", "vendor risk", "are our BAAs in place", "prepare for the HIPAA security rule", "run a downtime drill", or on the scheduled monthly vendor check.
- **Actions:** A08 (due 2027-06-30)
- **Scheduled as:** Monthly vendor resilience check
- **Engine scripts:** none

## `weekly-leader-brief`

Produces the Monday leader brief for the 2027 readiness program: the decisions owed, what is blocked, contract and regulatory deadlines in the next 60 days, KPI triggers and policy changes, with a short read on what matters most and what to ignore.

- **Ask for it when** the leader asks "what do I need to know this week", "send me my brief", "weekly readiness update", "what's coming up", or on the scheduled Monday run.
- **Actions:** recurring
- **Scheduled as:** Weekly leader brief
- **Engine scripts:** `tracker.py`, `weekly_brief.py`

