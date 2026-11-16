---
name: point-of-service-collections
description: Reduces 2027 bad debt as more patients arrive uninsured or on high-deductible plans: price estimates, good faith estimates for self-pay patients, collection at time of service, payment plans, financial assistance policy updates and weekly tracking of the point-of-service collection rate. Use when the leader asks "how do we cut bad debt", "self-pay is rising", "set up price estimates", "front desk collections", "update our financial assistance policy", or when kpi-pulse fires a self-pay, collection or bad debt trigger.
---

# Point-of-service collections

Hospital bad debt and charity care per day rose 49% in three years (Kaufman Hall, August 2026), before the 2027 coverage changes start. Balances that leave the building unpaid are collected far less often. This skill moves the conversation to the front of the visit, respectfully. Read `../../reference/conventions.md` first.

## 1. Baseline (D07, D08)

- Point-of-service collection rate = collected at service ÷ patient responsibility due at service, weekly by site. Fallback: a front-desk log in `templates/pos_log.csv` for two weeks.
- Self-pay share, bad debt plus charity as a share of gross revenue, and self-pay recovery rate from A/R aging.
- Feed the self-pay recovery rate into `assumptions.json` `self_pay_collection_rate` (with `set_by`) so the downside model uses the real number.

## 2. Estimates before the visit

- Give a good faith estimate to uninsured and self-pay patients when they schedule, as the No Surprises Act requires, and an out-of-pocket estimate to insured patients with deductibles where the eligibility response allows it.
- Use the eligibility check from medicaid-coverage-guard (48 to 72 hours before the visit) to catch coverage changes before the patient arrives.

## 3. At the visit

Draft a short script for front-desk staff, for the leader to approve:
1. State the amount and what it covers.
2. Offer to collect now, with card, HSA or payment plan options.
3. If the patient cannot pay, screen for coverage (Medicaid, marketplace special enrollment, exemptions) and financial assistance before setting up a plan.
4. Never delay emergency or medically necessary care over payment; follow EMTALA and state law where they apply.

## 4. Payment plans and assistance

- Standard interest-free plans with simple terms (for example, a minimum monthly amount and a maximum term) approved by the CFO.
- Update the financial assistance policy for a larger uninsured population: eligibility thresholds, documentation, presumptive eligibility screening. Nonprofit hospitals must also meet Section 501(r) requirements (written policy, limits on charges, rules before extraordinary collection actions); have counsel review changes.
- Marketplace insurers proposed a median 15% premium increase for 2027 after 20% in 2026 (KFF), so more insured patients carry high deductibles. Plans and estimates matter for them too.

## 5. Track weekly, report monthly

POS collection rate by site with a target the CFO sets (the KPI trigger defaults to 70%), estimates given, plans opened, and the share of self-pay patients screened for coverage. Update A04 in the tracker.

## What most teams miss

- **Screening beats collecting.** Some self-pay patients qualify for coverage they do not have. Finding it is better for the patient and pays more than any collection call.
- **Tone is a revenue lever.** Staff who are trained and given a script collect more and generate fewer complaints than staff who are told to "ask for payment".
- **Measure by site.** One site with a 40% collection rate hides inside an organization average of 64%.
