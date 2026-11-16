# Operating conventions (read once per session)

Every skill in this plugin follows these rules. They exist because most runs are scheduled: a fresh session, no memory of the last one, often nobody watching.

## Paths

- **Plugin root:** two levels above any skill's directory (`<skill dir>/../../`). Shared material lives in `reference/`, engine scripts in `scripts/`, blank inputs in `templates/`.
- **Readiness workspace:** the leader's folder for this program (default name `readiness`, often a connected folder such as "Readiness 2027", a cloud drive folder, or `readiness/` in a private repo). Its layout:

```
profile.json        who the organization is, data tiers, infrastructure, overrides
assumptions.json    the assumption register (overrides reference/assumptions-defaults.json)
inputs/             exports and templates: payer_mix.csv, contracts.csv, em_codes.csv, kpis.csv ...
state/              tracker.json, triggers.json, policy_log.json, contract_alerts.json
outputs/            dated reports by area: briefs/, model/, contracts/, kpi/, coding/, data/ ...
schedule/           jobs.json, prompts, crontab.txt, github-actions/, readiness-calendar.ics
logs/               headless run logs
```

- Run any engine script as `python3 <plugin root>/scripts/<script>.py --workspace <workspace>`. Scripts use only the Python standard library. Add `--today YYYY-MM-DD` only to reproduce a past run.

## State lives in files, never in memory

1. Start every run by reading `profile.json`, the relevant `state/` files and the newest output in the skill's area.
2. End every run by writing outputs and updating `state/tracker.json` (through `scripts/tracker.py update`) for any action whose status changed.
3. If the workspace cannot be reached, do not improvise one. Deliver a one-line failure notice through the delivery channel naming what was unreachable, and stop.

## Data tiers and confidence grades

Every input is a dependency (`reference/dependencies.json`, D01 to D18) with four tiers: **A** live system, **B** export file, **C** leader estimate, **D** public default. Before using an input:

1. Check its tier in `profile.json` `data_tiers` and whether the file or connector is actually present and fresh (exports older than 35 days are stale).
2. If it is missing or stale, walk down the fallback chain to the best available tier. Never stop just because tier A is missing.
3. Label every number in a leader-facing output with the grade of its weakest input. Grades C and D must be visible in the text, not buried in a footnote ("directional, based on the archetype default mix").
4. Record the tier actually used in the output's header, and suggest the upgrade that would raise it (data-readiness tracks these).

## Sources

Score every new external fact with `reference/source-scoring.md`. Assumptions change only on a source scored 4 or 5, or two independent sources scored 3. Name the source inside the sentence. Keep "proposed rule" and "final rule" distinct.

## Delivery

Deliver through the channel in `profile.json` `infrastructure.delivery`, falling back in this order: chat or email connector, a push notification with the file path, a dated markdown file in `outputs/`. Jobs marked deliver-only-if-material stay silent when nothing changed. Keep deliveries short: the first line is the point, then at most five items, then a link or path to the full output.

## Hard limits

- Send nothing to anyone except the leader unless the leader approved that specific message in this session. Draft emails to owners, payers or counsel; do not send them.
- Never change payer contracts, claims, patient records, prices or system settings. This plugin reads, analyzes, drafts and reminds.
- Keep protected health information out of outputs. Use counts, rates and de-identified worklists stored only in the workspace. A patient-level worklist is for the revenue cycle team's own systems, never for email.
- Not legal, financial or coding advice. Flag where counsel, the CFO or a certified coder must decide.
- Stop and ask before anything irreversible. In an unattended run, prepare the decision, put it in the tracker as `decision_needed`, and let the weekly brief raise it.

## Voice for leader-facing text

Plain and specific: numbers with units, names, dates, the source in the sentence. No em dashes, no exclamation marks, no emojis, no filler such as "navigate", "landscape", "headwinds" or "unprecedented". Lead with the point. Close without asking for anything unless a decision is genuinely needed, and then say exactly which decision and by when.
