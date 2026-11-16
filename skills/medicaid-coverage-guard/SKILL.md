---
name: medicaid-coverage-guard
description: Protects patients' Medicaid coverage and the organization's revenue through the 2027 work requirements and six-month renewals: eligibility re-verification timing, expansion-adult flags, renewal-date tracking, medical frailty and exemption screening, documentation accuracy, patient outreach, coverage-denial monitoring and state hold-harmless tracking. Use when the leader asks "how do we get ready for Medicaid work requirements", "are we losing Medicaid patients", "eligibility denials are up", "help patients keep coverage", "build the coverage worklist", or when kpi-pulse fires a coverage trigger.
---

# Medicaid coverage guard

Work requirements start January 1, 2027 in 44 states and reach about 30% of Medicaid beneficiaries. Expansion adults are renewed every six months. Every lapse is a patient at risk and a claim that may not pay. Read `../../reference/conventions.md` and `../../reference/state-rules.md` first.

## Applies when

At least one profile state is subject (all states except WY, TX, KS, MS, AL, FL, SC). In the others, run only steps 1 and 5 for ordinary renewals and exchange coverage.

## 1. Eligibility timing (A03, due January 1, 2027)

- Run eligibility in a batch 48 to 72 hours before every visit (270/271 through the clearinghouse) and again at check-in for Medicaid and exchange patients. A single check at scheduling misses lapses.
- Capture the aid category from the 271 response where the state returns it; it identifies expansion adults exactly.
- Store the next renewal date for every expansion adult. Six-month renewals double the number of points where coverage can lapse.
- Fallbacks (D17): real-time check at check-in, then the state provider portal, then card plus attestation with a same-day follow-up check. Card-only is the highest risk; flag those sites in the brief.

## 2. Find the patients (D02)

From the Medicaid roster, flag expansion adults (aid category, or the proxy: ages 19 to 64, excluding pregnancy, disability (SSI) and children's plans). Produce counts by site, and a worklist that stays inside the revenue cycle team's own systems or workspace: patients with a visit in the next 30 days, a renewal in the next 60, or no recent eligibility check. Never put patient-level data in an email or chat delivery.

## 3. Screen for exemptions at intake (A05)

The statute's medical frailty categories: blind or disabled; substance use disorders; disabling mental disorders; physical, intellectual or developmental disabilities that significantly impair activities of daily living; serious or complex medical conditions. A federal court vacated CMS's extra functional-impairment test for these categories on October 29, 2026. The law lists other exemption groups as well; pull the state's current list from its Medicaid agency and keep it in the workspace.

Because self-attestation of frailty is restricted and states verify using the prior 12 months of claims and encounter data, **accurate and complete diagnosis coding on claims can be the evidence that keeps an exempt patient covered.** This is a documentation-accuracy point: code what the record supports, nothing more. Brief clinicians and coders on it.

## 4. Help patients document (A05, due March 31, 2027)

Draft plain-language outreach (text, letter, front-desk script) that tells patients what the requirement is, how many hours, how to report, where to get help, and how exemptions work. Offer a staff member or community partner who can help with reporting. Drafts go to the leader or patient access lead for approval; nothing goes to patients without it.

## 5. Watch the signals

- Coverage denials (CARC 26 expenses before coverage, 27 after coverage terminated, 31 patient not identified as insured), by payer and site, monthly. Trigger: above 2% of claims.
- Self-pay share and Medicaid share by site, monthly.
- State elections of the CMS hold-harmless period (disenrollments paused until June 30, 2027) and litigation, through policy-radar. If a state elects it, coverage losses arrive in July: plan staffing for a July spike in renewals and self-pay conversions.

## Deliverables

`outputs/coverage/<date>-coverage-guard.md`: protocol status by site, counts (flagged, screened, exempt, outreach completed), denial trend, and the next three actions. Update A03 and A05 in the tracker.

## What most organizations miss

- **January is not the cliff if the state takes the hold-harmless option.** Assessments start January 1, disenrollments can wait until July. The work is identical; the timing of the revenue hit is not.
- **Front desk scripts matter as much as software.** A patient told "your coverage didn't go through" leaves; a patient told "your coverage needs a work report, here is how we can help" stays covered.
- **Renewal dates are data you can own.** States know them; most practices do not track them. Track them.
