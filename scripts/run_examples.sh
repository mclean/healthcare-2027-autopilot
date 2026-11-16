#!/usr/bin/env bash
# Regenerate every example output from the fictional sample data. Also serves as a smoke test.
set -euo pipefail
cd "$(dirname "$0")/.."
D=2026-11-16
O="--workspace examples/sample-org --today $D"
H="--workspace examples/sample-hospital --today $D"

python3 scripts/data_readiness.py $O
python3 scripts/downside_model.py $O
python3 scripts/contract_radar.py $O
python3 scripts/build_schedule.py $O --workspace-label "the connected folder 'Readiness 2027'"
python3 scripts/tracker.py report $O
python3 scripts/kpi_pulse.py $O
python3 scripts/coding_audit.py $O
python3 scripts/site_of_care.py $O
python3 scripts/deal_timeline.py $O
python3 scripts/weekly_brief.py $O

python3 scripts/data_readiness.py $H
python3 scripts/downside_model.py $H
python3 scripts/financing_cliff.py $H
python3 scripts/build_schedule.py $H
echo "All examples regenerated."
