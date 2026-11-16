# Who this is for: designing for most of the market

The design target is that about four out of five provider-side leaders in the United States recognize their organization in one of five archetypes and get useful defaults on day one, and that the program runs whatever their data looks like. That is a design target, not a measured market share.

Two things make that possible: archetypes that decide which playbooks apply, and a data ladder that lets every playbook run at whatever tier the organization has.

## Archetypes and what applies

| Action | Physician group | Platform / MSO | Community hospital | ASC, imaging, infusion | Outpatient services |
| --- | :---: | :---: | :---: | :---: | :---: |
| A01 Downside case | yes | yes | yes | yes | yes |
| A02 Contract renewals | yes | yes | yes | yes | yes |
| A03 Eligibility re-verification | yes | yes | yes | yes | yes |
| A04 Point-of-service collections | yes | yes | yes | yes | yes |
| A05 Medicaid documentation help | yes | yes | yes | yes | yes |
| A06 Coding integrity audit | yes | yes | yes | yes | optional, on demand |
| A07 Site-of-care shift | yes | yes | yes | yes | no |
| A08 Vendor resilience | yes | yes | yes | yes | yes |
| A09 Deal readiness | when a deal is possible | yes | yes | yes | yes |
| A10 2028 financing cliff | no | no | yes | no | no |

Details and default payer mixes: [`reference/segment-archetypes.md`](../../reference/segment-archetypes.md).

## Data situations covered

| Situation | How the program runs |
| --- | --- |
| Data warehouse or BI connector (larger systems, platforms) | Tier A inputs, high-confidence outputs from the first run |
| One PM/EHR with standard exports (most physician groups, ASCs) | Tier B monthly exports; the data map drafts each request |
| Spreadsheets and leader knowledge (smaller practices, services businesses) | Tier C estimates with owners and dates; outputs labeled medium |
| Nothing yet | Tier D public defaults; outputs labeled directional; the first upgrades are ranked |

## State footprint

- Medicaid work requirements apply in 44 states; WY, TX, KS, MS, AL, FL and SC are outside them. Organizations only in those states skip most of the coverage work.
- State transaction and corporate practice laws matter for anyone buying, selling or affiliating in CA, OR, WA, IN, MN, MA, RI, CT, IL, ME, VT and DE, with NY, PA and NJ pending. See [`reference/state-rules.md`](../../reference/state-rules.md).

## Out of scope by design

Payers, manufacturers and distributors, federal and VA facilities, dental-only organizations, and large academic medical centers with their own enterprise planning teams. The scheduling, tracking and brief skills still work for them; the defaults will not fit.
