---
name: site-of-care-shift
description: Finds and sizes services to move between hospital outpatient departments, ambulatory surgery centers and offices as Medicare site-neutral pay expands (clinic visits, drug administration and, from 2027, off-campus imaging without contrast) and the inpatient-only list phases out: margin change, payback, patient savings and gating checks for each candidate. Use when the leader asks "what should we move to the ASC", "how does site-neutral affect us", "is the imaging center worth it", "where should infusion live", or on the A07 checkpoint.
---

# Site-of-care shift

The hospital outpatient premium is shrinking: site-neutral pay now covers clinic visits and drug administration at off-campus departments, and from January 1, 2027 imaging without contrast at excepted off-campus departments (about $260 million less in 2027, rural sole community hospitals exempt, per BakerHostetler). CMS is also in a three-year elimination of the inpatient-only list. That reshapes where services make sense. Read `../../reference/conventions.md` first.

## Point of view first

- **Physician groups, platforms, ASCs, imaging and infusion centers:** the question is what to pull into owned sites, and what that does to margin and patient cost.
- **Hospitals:** the question is which off-campus services lose their premium, whether to relocate them on campus, convert them, partner with physicians on an ASC, or accept the lower rate. Run the analysis from the hospital's side.

## 1. Candidate list

Start from: off-campus clinic visits, drug administration and infusion, MRI and CT without contrast, procedures on the ASC covered procedures list now done in hospital outpatient departments, and procedures recently removed from the inpatient-only list. Use claims or CPT frequency (D04, D05) to rank by volume.

## 2. Price each site honestly

For each candidate, from the organization's own point of view: net per case now and at the alternative site (payment minus direct cost), one-time cost (equipment, build-out, staffing), and patient out-of-pocket at each site. Price Medicare from the CMS OPPS Addendum B, ASC Addendum AA and Physician Fee Schedule files; price commercial from contracts. Record per-case figures in `inputs/site_of_care.csv`. Never invent rates; leave a row out until it is priced.

## 3. Run

```
python3 ../../scripts/site_of_care.py --workspace <ws>
```

## 4. Gate every move

Before recommending any move, check: the code is payable at the new site (ASC covered list, payer contracts and carve-outs), clinical selection criteria and transfer agreements, state certificate-of-need rules, staffing and equipment lead times, and ownership and referral rules (Stark, Anti-Kickback safe harbors such as the ASC safe harbor) with counsel.

## 5. Decide

Each candidate gets a go, no-go or later decision, an owner and a date in the tracker under A07. Bring the margin total and patient savings into the downside model memo and, for commercial payers, into the contract prep pack: lower total cost of care is leverage.

## What most analyses miss

- **Patient savings are strategy.** Lower coinsurance at an ASC or office is a referral and loyalty story, and a negotiating point with payers trying to hold down employer costs.
- **Volume does not move itself.** Scheduling templates, referral patterns and surgeon preference move it. Put a ramp in the plan.
- **Hospitals have a play too.** Joint ventures with physicians on ASCs or imaging can keep volume in the system while the hospital outpatient premium shrinks.
