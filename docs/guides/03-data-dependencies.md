# Data dependencies and fallback chains

Generated from `reference/dependencies.json`. Every input the program uses has four tiers. Skills use the best tier available, never stop because tier A is missing, and label every number with the grade of its weakest input.

| Tier | Name | Confidence | Meaning |
| --- | --- | --- | --- |
| A | Live system | High | Read directly from a connected system (EHR/PM, clearinghouse, ERP, CLM, BI warehouse) through a connector, API or saved query. |
| B | Export file | High once mapped | A report someone exports on a schedule (CSV/XLSX) and drops in the readiness inputs folder. Validate the column mapping once. |
| C | Leader estimate | Medium | A structured estimate from the CFO, practice administrator or department lead, captured in a template with a named owner and date. |
| D | Public default | Directional | A public benchmark or national figure used until better data exists. Always labeled 'directional' in outputs. |

## D01 Payer mix by financial class (trailing 12 months) (critical)

Used by: `downside-case-model`, `kpi-pulse`, `board-update`. Fields: financial_class, visits, gross_charges, net_revenue.

| Tier | How to get it |
| --- | --- |
| A | EHR/PM or BI connector query: net revenue and visits by financial class, trailing 12 months, by month. |
| B | Practice management 'financial class summary' or 'payer mix' report exported monthly (names vary by system). Template: templates/payer_mix.csv. |
| C | CFO estimate of net revenue and percentage by payer class (Medicare FFS, Medicare Advantage, Medicaid FFS, Medicaid managed care, exchange, commercial, self-pay, other). |
| D | Segment default mix from segment-archetypes.md, adjusted with the state's coverage distribution from KFF State Health Facts. Directional only. |

Validation: Net revenue by class should tie to the income statement within 3%. Visits should tie to the scheduling system within 2%.

## D02 Medicaid patient roster with age and aid category (critical)

Used by: `medicaid-coverage-guard`, `downside-case-model`. Fields: patient_id, age, plan, aid_category, last_visit, next_visit.

| Tier | How to get it |
| --- | --- |
| A | Eligibility responses (271) or PM coverage table with aid category, so expansion adults are identified exactly. |
| B | PM export of active Medicaid patients with date of birth and plan name. Proxy for expansion adults: ages 19 to 64, excluding plans or aid codes for pregnancy, disability (SSI) and children. |
| C | Count of active Medicaid patients ages 19 to 64 from the practice administrator. |
| D | National default: roughly 30% of Medicaid beneficiaries are subject to work requirements (Morgan Lewis, Nov 2026). Apply to the Medicaid share from D01. |

Validation: Expansion-adult proxy count should be within 15% of a 50-chart manual spot check.

## D03 Exchange (marketplace) plan patients

Used by: `downside-case-model`, `point-of-service-collections`. Fields: patient_id, plan, metal_tier, visits, net_revenue.

| Tier | How to get it |
| --- | --- |
| A | Product type field (individual/marketplace) in the PM coverage table. |
| B | PM export filtered on plan names that carry marketplace or metal-tier wording; confirm the list once with the billing lead. |
| C | Billing lead estimate of the share of commercial revenue from individual-market plans. |
| D | State marketplace enrollment as a share of state population (KFF) applied to the commercial share. Directional. |

Validation: Plan-name list reviewed once by billing; re-review when new plans appear.

## D04 Medicare Part B professional revenue by CPT (critical)

Used by: `downside-case-model`, `site-of-care-shift`. Fields: cpt, units, allowed, place_of_service.

| Tier | How to get it |
| --- | --- |
| A | Claims or remittance (835) data by CPT and place of service. |
| B | PM 'CPT frequency by payer' export for Medicare, trailing 12 months. |
| C | Total Medicare Part B professional revenue from the income statement. |
| D | CMS public data: 'Medicare Physician & Other Practitioners - by Provider and Service' for the group's NPIs (lags about two years). Directional for trend, solid for mix. |

Validation: Units times 2026 rates should land within 5% of reported Medicare professional revenue.

## D05 Hospital outpatient services by site and APC

Used by: `site-of-care-shift`, `downside-case-model`. Fields: service_line, apc_or_hcpcs, site_type, volume, medicare_payment. Applies only when `hospital_outpatient` is true.

| Tier | How to get it |
| --- | --- |
| A | Hospital decision-support or claims warehouse by revenue code, HCPCS, APC and location (on-campus, off-campus excepted, off-campus non-excepted). |
| B | Chargemaster utilization report by department and location. |
| C | Service-line leader estimates of volume at off-campus departments for clinic visits, drug administration and imaging without contrast. |
| D | CMS OPPS and PFS rate files to price the site differential for any volume estimate. |

Validation: Off-campus department list matches the provider-based attestation list.

## D06 Commercial payer contracts (critical)

Used by: `contract-renewal-radar`, `downside-case-model`. Fields: payer, product, effective_date, term_months, auto_renew, notice_days, escalator, termination_without_cause_days, share_of_net_revenue.

| Tier | How to get it |
| --- | --- |
| A | Contract lifecycle system or a connected drive folder of executed contracts, read by the agent. |
| B | Contract summary spreadsheet (templates/contracts.csv) maintained by managed care. |
| C | Email search for amendments, renewal letters and fee schedule notices, then a confirmed list from the CFO. |
| D | No public fallback. Ask each payer's provider relations representative for a contract summary and assume a 90-day notice window until confirmed. |

Validation: Every contract with more than 2% of net revenue has a confirmed notice deadline.

## D07 A/R aging, bad debt and charity by financial class (critical)

Used by: `kpi-pulse`, `point-of-service-collections`, `downside-case-model`. Fields: month, financial_class, ar_0_30, ar_31_60, ar_61_90, ar_91_120, ar_120_plus, bad_debt, charity.

| Tier | How to get it |
| --- | --- |
| A | PM or ERP connector. |
| B | Month-end A/R aging by financial class export plus the bad debt and charity lines from the monthly close. |
| C | Monthly financial statement bad debt line and total A/R from the controller. |
| D | Kaufman Hall National Hospital Flash Report trend (bad debt and charity per calendar day) as an external comparison. Directional for non-hospitals. |

Validation: Total A/R ties to the balance sheet.

## D08 Point-of-service collections and estimates

Used by: `point-of-service-collections`, `kpi-pulse`. Fields: week, patient_responsibility_due_at_service, collected_at_service, estimates_given, payment_plans_opened.

| Tier | How to get it |
| --- | --- |
| A | PM daily close or payment platform connector. |
| B | Weekly front-desk close report export. |
| C | Front-desk manager weekly log in templates/pos_log.csv. |
| D | None. Start a log; two weeks of data beats any benchmark. |

Validation: Collected at service ties to deposits.

## D09 E/M and procedure code distribution by rendering provider (critical)

Used by: `coding-integrity-audit`. Fields: provider, period, code, count.

| Tier | How to get it |
| --- | --- |
| A | Claims warehouse query by rendering NPI, month and CPT. |
| B | PM 'CPT frequency by provider' export for a baseline period (before AI documentation tools) and the current period. Template: templates/em_codes.csv. |
| C | Coding manager's sample of recent encounters by level. |
| D | CMS public Medicare data by NPI and HCPCS for each provider (lagged) plus specialty-level distributions as the benchmark. |

Validation: Code counts per provider tie to visit counts within 2%.

## D10 Denials by reason code

Used by: `kpi-pulse`, `medicaid-coverage-guard`, `coding-integrity-audit`. Fields: month, payer, carc, rarc, claims, dollars.

| Tier | How to get it |
| --- | --- |
| A | Clearinghouse denial analytics (835 CARC/RARC) via connector. |
| B | Clearinghouse or PM denial report export. |
| C | Billing lead's monthly count of eligibility and coding denials. |
| D | None. Start tracking CARC 26, 27 and 31 (coverage) and coding-related denials now. |

Validation: Denied claims count ties to the remittance totals.

## D11 Vendors with PHI access, BAAs and cash-criticality (critical)

Used by: `vendor-resilience`. Fields: vendor, function, phi_access, baa_on_file, cash_critical, backup_option, last_tested.

| Tier | How to get it |
| --- | --- |
| A | Vendor risk platform or IT asset inventory connector. |
| B | Accounts payable vendor list joined to the BAA folder index. Template: templates/vendors.csv. |
| C | CIO and practice administrator workshop listing systems that touch PHI or cash. |
| D | The function checklist in vendor-resilience (clearinghouse, PM/EHR, eligibility, payment processing, patient statements, transcription, AI scribe, cloud backup). |

Validation: Every system with a login that shows patient data appears on the list.

## D12 State footprint, entity structure and deal pipeline (critical)

Used by: `deal-readiness`, `readiness-setup`. Fields: state, entities, ownership, mso_relationship, pipeline_deals.

| Tier | How to get it |
| --- | --- |
| A | Entity management system or legal team tracker. |
| B | Org chart and entity list from counsel or the controller. |
| C | Leader's description during setup. |
| D | State lists in reference/state-rules.md. Always confirm with counsel. |

Validation: Counsel confirms the entity list once a year.

## D13 Medicaid supplemental payments: provider tax, state-directed payments, DSH (critical)

Used by: `financing-cliff-2028`. Fields: program, fy2026_amount, payment_level_vs_medicare, state, expansion_state. Applies only when `receives_supplemental_payments` is true.

| Tier | How to get it |
| --- | --- |
| A | Hospital reimbursement or cost report system. |
| B | Finance's supplemental payment schedule by program. |
| C | CFO estimate of annual supplemental payments by program. |
| D | State hospital association briefings and KFF/MACPAC state tables. Directional. |

Validation: Ties to the Medicaid supplemental lines in the audited financials.

## D14 Workforce: vacancies, agency and locum spend

Used by: `kpi-pulse`, `board-update`. Fields: month, role, vacancies, agency_spend, total_labor_cost.

| Tier | How to get it |
| --- | --- |
| A | HRIS and payroll connector. |
| B | Monthly HR vacancy report and AP agency invoices. |
| C | HR lead estimate. |
| D | HRSA workforce projections (10% RN shortage in 2027, 24% non-metro) as context only. |

Validation: Agency spend ties to AP.

## D15 Policy and market intelligence

Used by: `policy-radar`, `weekly-leader-brief`. Fields: date, source, headline, change, credibility.

| Tier | How to get it |
| --- | --- |
| A | Web search plus CMS, Federal Register, KFF and state Medicaid agency pages, scored with source-scoring.md. |
| B | Newsletters forwarded to a connected inbox and read by the agent. |
| C | Leader notes from association meetings. |
| D | The regulatory calendar in this plugin, which is static until refreshed. |

Validation: Every change that moves an assumption cites a source scored 4 or higher, or two sources scored 3.

## D16 Upcoming appointment schedule with coverage on file (critical)

Used by: `medicaid-coverage-guard`, `point-of-service-collections`. Fields: appointment_date, patient_id, plan, last_eligibility_check.

| Tier | How to get it |
| --- | --- |
| A | Scheduling connector or nightly appointment extract. |
| B | Daily or weekly appointment export with insurance columns. |
| C | Front-desk lead pulls the next week's Medicaid appointments manually. |
| D | None. |

Validation: Appointment count matches the schedule.

## D17 Real-time eligibility verification capability (critical)

Used by: `medicaid-coverage-guard`. Fields: tool, batch_supported, aid_category_returned.

| Tier | How to get it |
| --- | --- |
| A | Batch 270/271 eligibility through the clearinghouse 48 to 72 hours before visits, returning aid category. |
| B | Real-time eligibility at check-in through the PM or payer portal. |
| C | State Medicaid provider portal lookups by staff. |
| D | Patient-presented card plus attestation at check-in. Highest risk; escalate. |

Validation: Spot-check 20 verifications a month against the state portal.

## D18 Agent infrastructure: state store, delivery channel, scheduler (critical)

Used by: `cadence-scheduler`, `readiness-setup`, `weekly-leader-brief`. Fields: state_store, delivery_channel, scheduler.

| Tier | How to get it |
| --- | --- |
| A | Scheduled tasks in Claude with a connected folder or cloud drive as the state store, and email or chat as the delivery channel. |
| B | Headless agent on a schedule (cron with claude -p, or a GitHub Actions workflow) writing to a private repo or shared drive. |
| C | Calendar reminders (.ics) that tell the leader to open the agent and run the skill by name. |
| D | A printed or shared action calendar with the same dates. |

Validation: First scheduled run produces its output in the state store and reaches the delivery channel.

