---
name: vendor-resilience
description: Protects cash and patient data from vendor failure: inventories every vendor with PHI access, classifies which ones stop cash if they go down, confirms BAAs, sets up a backup clearinghouse path, runs downtime tabletop exercises and tracks the HIPAA Security Rule overhaul. Use when the leader or CIO asks "what happens if our clearinghouse goes down", "vendor risk", "are our BAAs in place", "prepare for the HIPAA security rule", "run a downtime drill", or on the scheduled monthly vendor check.
---

# Vendor resilience

Business associates were involved in 43% of large healthcare breaches in the first half of 2026, up from about 20% in 2009 to 2017 (HIPAA Journal analysis of HHS data), and ransomware attacks on healthcare businesses rose 36% in that half (Comparitech). The 2024 Change Healthcare attack showed that one vendor can stop an industry's cash. Read `../../reference/conventions.md` first.

## 1. Inventory (D11)

Fill `inputs/vendors.csv` at the best tier: the vendor risk system or IT asset inventory (A); accounts payable vendors joined to the BAA folder (B); a CIO and practice administrator workshop (C); or the function checklist below (D). Every system that shows patient data at login belongs on the list.

Function checklist: practice management and EHR, clearinghouse, eligibility verification, payment processing and patient portal, patient statements and collections, prior authorization tools, transcription and AI scribe, coding and CDI tools, cloud backup, email and messaging, analytics and BI, IT managed services.

## 2. Classify

For each vendor: PHI access (yes or no), BAA on file and current, **cash-critical** (would claims, eligibility or payments stop within a week without it?), backup option, last tested date.

## 3. Close the gaps (A08, due June 30, 2027)

- **BAAs:** list missing or outdated agreements and draft requests for the leader to approve.
- **Backup clearinghouse:** a second clearinghouse enrollment can take weeks. Price it and set it up before it is needed; the sample organization's CIO estimated six weeks.
- **Downtime procedures:** for each cash-critical vendor, a written plan covering manual eligibility, claim holds and later batch submission, and patient communication.
- **Tabletop:** draft a 60-minute exercise (scenario: the clearinghouse is down for ten business days) with roles, decision points and a cash projection. Schedule it and record the date in `last_tested`.

## 4. Monthly check (scheduled)

Recount cash-critical vendors without a tested backup, BAAs expiring in 90 days, and new vendors since last month. Feed `cash_critical_vendors_untested` into `inputs/kpis.csv`. Deliver only if a count rose or a BAA is about to lapse.

## 5. HIPAA Security Rule watch

HHS pushed final action on the Security Rule overhaul to July 2027. Proposed provisions include mandatory encryption, multi-factor authentication and asset inventories; they are proposed, not final. Building the inventory and MFA coverage now is useful under any version of the rule. policy-radar confirms the final text when it lands.

## What most programs miss

- **Cash-critical is a different list from data-sensitive.** The payment processor may hold little PHI and still stop cash.
- **The backup must be live before the outage.** Enrollment, testing and payer connectivity take weeks.
- **AI tools are vendors too.** Ambient scribes and coding assistants see full encounters. They belong on the inventory with BAAs and access reviews.
