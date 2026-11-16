# Security policy

## Reporting a vulnerability

Report security problems privately through GitHub. Go to the [Security tab](https://github.com/mclean/healthcare-2027-autopilot/security), choose **Report a vulnerability**, and describe what you found. Only the maintainer can see the report.

Please do not open a public issue for a security problem. Leave out real patient data, credentials and any organization's financial or contract data. Steps to reproduce with the fictional sample workspaces in `examples/` are enough.

The maintainer aims to acknowledge a report within five business days and to share a fix or a plan within 30 days. You will be credited in the release notes unless you would rather not be.

## What to report

This plugin runs unattended on a schedule and works with sensitive financial and operational data, so the bar is broad. Report anything that could:

- send workspace contents (financials, contracts, patient-level worklists) anywhere other than the leader's own delivery channel
- lead a scheduled run to message someone other than the leader, change a contract, claim or record, or take any other irreversible step
- let text inside an input file, web page or policy source steer the agent into actions the skills do not allow
- give the generated GitHub Actions workflows or crontab entries more access than they need, or expose the `ANTHROPIC_API_KEY` secret
- execute code or write outside the workspace when an engine script reads an input file

## Not in scope

- Wrong dates, rates or rules in `reference/`. Those matter, but use the [policy or source update form](https://github.com/mclean/healthcare-2027-autopilot/issues/new?template=policy_update.yml) instead.
- The security of your own workspace location, Claude account, CI provider or calendar.

## Supported versions

| Version | Supported |
| --- | --- |
| 0.1.x | Yes |
