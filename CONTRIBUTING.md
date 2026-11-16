# Contributing

This plugin is only as useful as its facts are current and its outputs are believable in a real leadership meeting. Most of the best contributions are small: a corrected date, a state rule that changed, a skill instruction that confused someone.

## Ways to help

**Report a policy change.** If a date, rate or state rule in `reference/` has moved, open a [policy or source update](https://github.com/mclean/healthcare-2027-autopilot/issues/new?template=policy_update.yml) with a link and the source's publication date. An assumption only moves when its source scores 4 or higher on the rubric in [`reference/source-scoring.md`](reference/source-scoring.md).

**Report a bug.** A script crashed, a number looks off, or a skill did something it should not have. Use the [bug report form](https://github.com/mclean/healthcare-2027-autopilot/issues/new?template=bug_report.yml).

**Suggest a skill or coverage gap.** A state notice period we are missing, a KPI, a data source, an organization type the archetypes do not fit. Use the [idea form](https://github.com/mclean/healthcare-2027-autopilot/issues/new?template=feature_request.yml), and say what the fallback should be when the data is not there.

**Send a fix.** Pull requests are welcome. For anything larger than a few files, open an issue first so we can agree on the approach before you put in the time.

## Ground rules

Everyone taking part in this project follows the [code of conduct](CODE_OF_CONDUCT.md).

1. **No real data, ever.** No patient information, no real organization's financials or contract terms, no names of real people at real providers. Both sample organizations are invented, and anything added to `examples/` or `templates/` has to be invented too.
2. **Standard library only.** The scripts have to run on locked-down machines where nobody can install packages.
3. **Every fact has a source and a date.** Figures in `reference/` carry both. New ones need the same.
4. **The agent stays in its lane.** Skills read, analyze, draft and remind. They do not message anyone but the leader and do not touch contracts, claims or records. Changes that loosen this will not be merged.
5. **Planning support, not advice.** Text that reads like legal, financial or coding advice gets reworded or routed to counsel, the CFO or a certified coder.

## Making a change

1. Fork the repository and create a branch.
2. Make your change.
3. If you edited anything in `reference/` that feeds the guides, rebuild them:
   ```
   python3 docs/tools/build_reference_docs.py
   ```
4. Regenerate the examples and make sure nothing breaks:
   ```
   bash scripts/run_examples.sh
   ```
5. Add a line under `[Unreleased]` in [`CHANGELOG.md`](CHANGELOG.md).
6. Open a pull request. The smoke test runs on its own and has to pass.

Leave `dist/` alone. The plugin file is rebuilt when a release is cut.

## Writing style

Write for a CFO or practice president with ten minutes, not for a developer. Short sentences, plain words, numbers with their units and dates, and no hype. The conventions every skill follows are in [`reference/conventions.md`](reference/conventions.md).

## Security

Do not report security problems in a public issue. See [SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
