#!/usr/bin/env python3
"""Create a readiness workspace: folders, a profile to fill in, the assumption register and blank input templates.

  python3 init_workspace.py --workspace "Readiness 2027" [--archetype physician-group] [--org "Name"] [--states IL,IN] [--tz America/Chicago]

Never overwrites existing files.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ARCHETYPES, workspace_arg  # noqa: E402
from lib.report import PLUGIN_ROOT, REFERENCE, load_json, save_json, today  # noqa: E402


def main():
    ap = workspace_arg(__doc__)
    ap.add_argument("--archetype", choices=ARCHETYPES, default=None)
    ap.add_argument("--org", default=None)
    ap.add_argument("--states", default=None, help="Comma-separated postal codes")
    ap.add_argument("--tz", default=None)
    args = ap.parse_args()
    ws = Path(args.workspace)
    for sub in ("inputs", "state", "outputs", "schedule", "logs"):
        (ws / sub).mkdir(parents=True, exist_ok=True)
    tpl = PLUGIN_ROOT / "templates"
    created = []
    prof_path = ws / "profile.json"
    if not prof_path.exists():
        prof = load_json(tpl / "profile.json")
        if args.org:
            prof["org_name"] = args.org
        if args.archetype:
            prof["archetype"] = args.archetype
        if args.states:
            prof["states"] = [s.strip().upper() for s in args.states.split(",") if s.strip()]
        if args.tz:
            prof["leader"]["timezone"] = args.tz
        save_json(prof_path, prof)
        created.append("profile.json")
    reg = ws / "assumptions.json"
    if not reg.exists():
        d = load_json(REFERENCE / "assumptions-defaults.json")
        d["note"] = f"Assumption register created {today(args.today).isoformat()}. Overrides here win over the plugin defaults. Record set_by and a source for every change."
        save_json(reg, d)
        created.append("assumptions.json")
    for f in tpl.iterdir():
        if f.name in ("profile.json",):
            continue
        dest = ws / "inputs" / f.name
        if not dest.exists():
            shutil.copy(f, dest)
            created.append(f"inputs/{f.name}")
    print(f"Workspace {ws}: created {len(created)} files")
    for c in created:
        print("  " + c)


if __name__ == "__main__":
    main()
