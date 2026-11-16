# Data readiness, 2026-11-16

Critical inputs at A or B: 9 of 11.

Upgrade first:
- D11 Vendors with PHI access, BAAs and cash-criticality (C to B): Accounts payable vendor list joined to the BAA folder index. Template: templates/vendors.csv.
- D06 Commercial payer contracts (C to B): Contract summary spreadsheet (templates/contracts.csv) maintained by managed care.
- D08 Point-of-service collections and estimates (C to B): Weekly front-desk close report export.
- D03 Exchange (marketplace) plan patients (C to B): PM export filtered on plan names that carry marketplace or metal-tier wording; confirm the list once with the billing lead.
- D14 Workforce: vacancies, agency and locum spend (C to B): Monthly HR vacancy report and AP agency invoices.
