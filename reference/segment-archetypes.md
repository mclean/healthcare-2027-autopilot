# Segment archetypes

The plugin targets provider-side leaders in the United States. Five archetypes cover the organizations most of them run. The design goal is that about four out of five provider-side leaders recognize their organization in one archetype and get usable defaults on day one. That figure is a design target, not a measured market share.

Each archetype sets defaults for: which actions apply, which data dependencies matter most, the default schedule, the KPIs that lead the monthly pulse, and the fallback payer mix used when no data is available (tier D). Default mixes are placeholders for modeling only. They are deliberately round so nobody mistakes them for a benchmark.

## 1. `physician-group`: independent or single-specialty physician group

- **Who:** 3 to 150 clinicians, one or a few specialties (orthopedics, cardiology, GI, primary care, OB-GYN, pain, urology).
- **Biggest 2027 exposures:** Medicare fee schedule cut (-2.31% for most clinicians), coverage churn showing up as self-pay, commercial renewals, payer scrutiny of AI-assisted coding.
- **Actions that apply:** A01 to A08. A09 if an acquisition or recapitalization is possible. A10 does not apply.
- **Data reality:** usually a single PM/EHR with standard exports, no data warehouse. Expect tier B for most inputs and tier C for contracts.
- **Lead KPIs:** self-pay share, eligibility denials, POS collection rate, level 4 and 5 E/M share by provider, days in A/R.
- **Default mix (tier D placeholder):** Medicare FFS 30%, Medicare Advantage 15%, Medicaid 10%, exchange 5%, commercial 37%, self-pay 3%.

## 2. `platform-mso`: multi-site platform or MSO, often sponsor-backed

- **Who:** PE-backed or physician-owned platforms running an MSO for affiliated professional corporations across several states.
- **Biggest 2027 exposures:** state transaction notice and corporate-practice laws, deal timelines, same exposures as physician groups at larger scale, integration of acquired practices onto one revenue cycle.
- **Actions that apply:** A01 to A09.
- **Data reality:** a BI layer or data warehouse at the MSO, uneven quality from recently acquired practices. Expect tier A or B centrally, tier C at new sites.
- **Lead KPIs:** same as physician groups, rolled up by site, plus deal-calendar items.
- **Default mix (tier D placeholder):** Medicare FFS 28%, Medicare Advantage 15%, Medicaid 12%, exchange 5%, commercial 37%, self-pay 3%.

## 3. `community-hospital`: community hospital or small health system

- **Who:** 25 to 400 bed hospitals and small systems, including rural and safety-net facilities. Kaufman Hall data shows hospitals with 100 to 199 beds saw the steepest bad debt growth since 2023 (64.2%).
- **Biggest 2027 exposures:** coverage loss turning into bad debt, 340B cuts, site-neutral expansion at off-campus departments, provider tax and state-directed payment phase-downs from October 2027 and January 2028.
- **Actions that apply:** all, including A10.
- **Data reality:** decision-support system plus finance and reimbursement teams. Tier A or B for most, tier C for contracts in smaller hospitals.
- **Lead KPIs:** bad debt and charity per calendar day, payer mix shift, days in A/R, agency labor share, off-campus volumes.
- **Default mix (tier D placeholder):** Medicare FFS 30%, Medicare Advantage 15%, Medicaid 18%, exchange 4%, commercial 28%, self-pay 5%.

## 4. `asc-imaging-infusion`: ambulatory surgery, imaging and infusion centers

- **Who:** freestanding ASCs, imaging centers and infusion centers, often joint ventures with physicians or health systems.
- **Biggest 2027 exposures:** high-deductible plans and patient balances, commercial renewals, and the opportunity side of site-neutral pay (volume moving out of hospital outpatient departments).
- **Actions that apply:** A01 to A04, A06 to A09.
- **Data reality:** specialty PM systems with clean procedure-level data. Tier B is typical.
- **Lead KPIs:** POS collection rate, prior authorization and eligibility denials, case volume by payer, payer mix.
- **Default mix (tier D placeholder):** Medicare FFS 30%, Medicare Advantage 12%, Medicaid 6%, exchange 5%, commercial 45%, self-pay 2%.

## 5. `outpatient-services`: therapy, behavioral health, home-based and post-acute services

- **Who:** outpatient physical therapy and rehab, behavioral health groups, home health and hospice, and similar services businesses.
- **Biggest 2027 exposures:** Medicaid coverage churn (behavioral health especially), workforce, state transaction notice laws for acquisitive operators, and payer audits.
- **Actions that apply:** A01 to A05, A08, A09. A06 when billing E/M or time-based codes at volume.
- **Data reality:** lighter systems and more spreadsheets. Expect tier B to C.
- **Lead KPIs:** Medicaid share and churn, eligibility denials, visits per authorization, clinician vacancies.
- **Default mix (tier D placeholder):** Medicare FFS 25%, Medicare Advantage 12%, Medicaid 20%, exchange 5%, commercial 33%, self-pay 5%.

## Out of scope by design

Payers, drug and device manufacturers, distributors, federal and VA facilities, dental-only organizations and large academic medical centers with their own enterprise planning teams. Academic centers can still use the scheduling and tracking skills, but the defaults will not fit.
