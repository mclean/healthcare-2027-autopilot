---
name: coding-integrity-audit
description: Audits coding patterns before payers do, especially after AI documentation or ambient scribe rollouts: E/M level distribution by provider against a pre-AI baseline and a specialty benchmark, a reproducible probe sample, coder review against 2021 E/M guidelines, AI tool settings review and a documented corrective plan. Use when the leader or compliance officer asks "are we upcoding", "audit our AI scribe coding", "payers are asking about our E/M levels", "run the coding audit", or on the scheduled quarterly audit.
---

# Coding integrity audit

PwC reports that 70% of health plans rank provider AI documentation and coding tools among their top three cost drivers for 2027, and payers are adding audit rights to contracts. A rise in coding levels can be legitimate; the risk is a rise nobody can explain. This skill makes it explainable, on the record, first. Read `../../reference/conventions.md` first.

## Inputs (D09, D10)

- `inputs/em_codes.csv`: provider, period, code, count for established visits (99212 to 99215), for a baseline period before AI tools and the current period. Fallback: the coding manager's recent sample; then CMS public Medicare data by NPI and HCPCS (lagged about two years, still useful for the baseline).
- `inputs/em_benchmark.csv`: the specialty's distribution from CMS public data. Without it, the audit compares each provider to their own baseline only.
- Optional `inputs/encounters.csv` (encounter_id, provider, date, code) to draw the probe sample reproducibly.

## Steps

1. Run `python3 ../../scripts/coding_audit.py --workspace <ws>`. Defaults flag a provider whose level 4 and 5 share rose 5 points or more, or sits 10 points above the benchmark; adjust with `--rise-pts` and `--above-benchmark-pts`.
2. For each flagged provider, pull a probe sample (the script draws 30 per provider when encounters exist, seeded so it can be reproduced).
3. Have a certified coder audit each chart blind to the billed level, against the 2021 E/M guidelines (medical decision making or total time). Record agreement by provider.
4. Review the AI tool configuration with IT and the vendor: does it suggest a level, does the clinician confirm it, can the suggestion be turned off, what does the audit trail show?
5. Write `outputs/coding/<date>-coding-findings.md`: the pattern, the sample results, the explanation (better capture of work that was always done, a change in patient mix, or over-coding), and corrective actions (education, tool settings, prospective review for a period). Any overpayment question goes to compliance counsel; repayment estimates need statistically valid sampling under counsel's direction.
6. Update A06 in the tracker with the findings file as evidence.

## Quarterly run (scheduled)

Repeat with the latest quarter. Report only flagged providers and changes since the last quarter. Feed the organization-wide level 4 and 5 share into `inputs/kpis.csv` as `high_level_em_share` for the pulse.

## What most audits miss

- **Payers see the same CMS public data you can.** Benchmark yourself with it before an outlier report does.
- **The baseline must predate the tool.** Comparing this quarter to last quarter after a rollout hides the shift.
- **Documentation and coding are different fixes.** If the chart supports level 5 work, the issue may be that it was under-coded before. If it does not, the fix is education and tool settings, not a new note template.
- **Write it down.** A dated self-audit with findings and corrective action is the best answer to a future payer inquiry.
