---
name: deal-readiness
description: Keeps 2027 healthcare acquisitions, affiliations and recapitalizations on schedule under new state transaction and corporate-practice laws: works back from each target close through every state's notice period, flags filings due now, and checks MSO and professional corporation governance and deal documents for regulator review. Use when the leader asks "when do we have to file for this deal", "which states need notice", "will Oregon's law affect our MSO", "is our MSO structure compliant", "add the deal to the plan", or when a deal enters the pipeline.
---

# Deal readiness

States have moved from debating private equity in healthcare to building review gates. In 2026, six states enacted nine laws and Rhode Island added a notice rule (PESP, an advocacy group; facts only). Notice periods now sit on the critical path of a closing. Read `../../reference/conventions.md` and `../../reference/state-rules.md` first. Not legal advice: counsel confirms every filing.

## 1. Pipeline into the profile

For each live deal, add to `profile.json` `deal_pipeline`: name, type, states of every entity involved, target close date, and asset or revenue size (thresholds decide whether a filing is required).

## 2. Work back from the close

```
python3 ../../scripts/deal_timeline.py --workspace <ws>
```

For each deal and state it computes the file-by date (close minus notice period) and a prep-start date three weeks earlier, using `../../reference/state-notice-periods.json`. States without a fixed period in the sources get a 180-day placeholder marked for counsel. Statuses: file now (45 days or less), prepare filing (90 days or less), on calendar, or window missed (move the close).

Add each file-by date to the tracker under A09 and rebuild the schedule so reminders fire.

## 3. The filing plan

For each required filing, list: the agency, the trigger and threshold, what must be submitted (some states want the HSR filing, organizational charts, MSO agreements, financial projections and a post-closing plan), whether materials become public (Oregon's generally do), and who prepares it. Plan in parallel for HSR, payer change-of-ownership notices, Medicare and Medicaid enrollment updates, and licensure.

## 4. Governance check for MSO and PC structures

Review, with counsel, against the states involved:
- Clinical decisions, clinical policies and hiring of clinicians sit with licensed professionals; the MSO has no veto over clinical judgment. California's SB 351 and Vermont's new law say this explicitly.
- Management fees reflect fair market value for services actually provided.
- Restrictive covenants and non-competes comply with each state (California's SB 351 restricts certain non-compete clauses).
- Oregon SB 951 limits MSO ownership and control of medical groups; most existing arrangements must comply by January 1, 2029. Map which Oregon arrangements need restructuring and when.
- Sale-leasebacks of hospital real estate draw specific scrutiny (Connecticut bars them for a hospital's main campus; Washington and Massachusetts review them).

## 5. Document hygiene

Assume regulators will read every deal document (McDermott's advice). Make sure strategy memos, synergy models and board materials describe the same deal: access, quality and competition effects that match the numbers. Draft a one-page access and quality narrative for each market before filing.

## What most deal teams miss

- **The notice clock beats the diligence clock.** An Indiana deal closing March 31, 2027 needs its filing by December 31, 2026, before diligence usually wraps.
- **Thresholds are not just size.** Maine's review covers transactions over $100 million in assets "among other triggers", and some states reach MSO-to-MSO deals. Check triggers per state, not just dollars.
- **Conditions last.** Oregon approvals can carry up to five years of conditions. Price them into the model.
