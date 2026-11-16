# Changelog

Notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Code of conduct (Contributor Covenant 2.0).

### Changed

- The smoke test now uses `actions/checkout` and `actions/setup-python` v7.

## [0.1.0] - 2026-11-16

First public release.

### Added

- 17 skills in four layers. Running the program: `readiness-setup`, `cadence-scheduler`, `data-readiness`, `action-tracker`. Keeping the leader informed: `weekly-leader-brief`, `policy-radar`, `kpi-pulse`, `board-update`. Executing the ten actions: `downside-case-model`, `contract-renewal-radar`, `medicaid-coverage-guard`, `point-of-service-collections`, `coding-integrity-audit`, `site-of-care-shift`, `vendor-resilience`, `deal-readiness`. Hospitals: `financing-cliff-2028`.
- 12 engine scripts that use only the Python standard library.
- 18 data dependencies, each with a four-tier fallback chain (A live system, B export, C leader estimate, D public default).
- Regulatory calendar, state notice periods, KPI definitions and assumption defaults, each sourced and dated as of November 16, 2026.
- Four ways to run the schedule: Claude scheduled tasks, cron with `claude -p`, GitHub Actions, or calendar reminders.
- Two fictional sample organizations, Prairie Ridge Specialty Partners and Lakeshore Community Hospital, with every output generated.
- Guides, screenshots, the installable `.plugin` file and the script that builds it.
- A smoke test that regenerates every example, checks the manifests and skill files, builds the plugin, and runs a fresh workspace on public defaults.
- Contributing guide, security policy, and issue and pull request templates.

[Unreleased]: https://github.com/mclean/healthcare-2027-autopilot/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/mclean/healthcare-2027-autopilot/releases/tag/v0.1.0
