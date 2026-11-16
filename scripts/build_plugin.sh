#!/usr/bin/env bash
# Build the installable .plugin file (a zip of the plugin root) into dist/.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/healthcare-2027-autopilot.plugin
zip -qr dist/healthcare-2027-autopilot.plugin . -x ".git/*" -x "dist/*" -x "*.DS_Store" -x "*__pycache__*" -x ".github/*"
echo "Built dist/healthcare-2027-autopilot.plugin"
