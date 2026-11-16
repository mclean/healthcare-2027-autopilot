#!/usr/bin/env python3
"""Data readiness map: which tier each data dependency is at, what that does to the confidence
of every action, and the cheapest upgrades that raise confidence the most.

Input:  profile.json data_tiers {D01: "B", ...}; files present in inputs/
Output: outputs/data/<date>-data-readiness.{html,md}
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import GRADE_ORDER, applicable_actions, dependency_tiers, load_profile, reference, weakest, workspace_arg  # noqa: E402
from lib.report import Raw, badge, callout, grade_badge, page, section, table, tiles, today, write_text  # noqa: E402

FILES = {"D01": "payer_mix.csv", "D02": "medicaid_roster.csv", "D03": "exchange_patients.csv", "D04": "cpt_medicare.csv",
         "D05": "hopd_services.csv", "D06": "contracts.csv", "D07": "ar_aging.csv", "D08": "pos_log.csv", "D09": "em_codes.csv",
         "D10": "denials.csv", "D11": "vendors.csv", "D13": "supplemental.json", "D14": "workforce.csv", "D16": "appointments.csv"}
NEXT = {"D": "C", "C": "B", "B": "A", "A": None}


def main():
    args = workspace_arg(__doc__).parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    now = today(args.today)
    deps = {d["id"]: d for d in reference("dependencies.json")["dependencies"]}
    tiers = dependency_tiers(prof, include_na=True)
    actions = applicable_actions(prof)
    used = {}
    for a in actions:
        for d in a["data"]:
            used.setdefault(d, []).append(a["id"])

    hints = []
    for dep, fname in FILES.items():
        if tiers.get(dep) and (ws / "inputs" / fname).exists() and GRADE_ORDER[tiers[dep]] > GRADE_ORDER["B"]:
            hints.append(f"{dep}: inputs/{fname} exists, so this can move to tier B once the column mapping is validated.")

    rows = []
    for did, d in deps.items():
        t = tiers[did]
        if t is None:
            rows.append([did, d["name"], badge("not applicable", "neutral"), "", "", "Does not apply to this organization's profile.", ""])
            continue
        nxt = NEXT[t]
        rows.append([did, d["name"], grade_badge(t), badge("critical", "bad") if d["critical"] else "",
                     ", ".join(used.get(did, [])) or "recurring jobs", d["tiers"][nxt] if nxt else "At the top tier. Keep validating.", d["validation"]])

    act_rows = []
    for a in actions:
        live = [x for x in a["data"] if tiers.get(x) is not None]
        g = weakest([tiers[x] for x in live])
        weakest_dep = max(live, key=lambda x: GRADE_ORDER[tiers[x]]) if live else ""
        act_rows.append([a["id"], a["title"], grade_badge(g), f"{weakest_dep} {deps[weakest_dep]['name']}" if weakest_dep else ""])

    scores = []
    for did, d in deps.items():
        t = tiers[did]
        if t in ("C", "D"):
            gain = len(used.get(did, [])) * (2 if d["critical"] else 1) * (2 if t == "D" else 1)
            scores.append((gain, did))
    upgrades = [[did, deps[did]["name"], f"{tiers[did]} to {NEXT[tiers[did]]}", deps[did]["tiers"][NEXT[tiers[did]]]]
                for _, did in sorted(scores, reverse=True)[:5]]

    crit = [d for d in deps.values() if d["critical"] and tiers[d["id"]] is not None]
    strong = sum(1 for d in crit if tiers[d["id"]] in ("A", "B"))
    dist = {g: sum(1 for t in tiers.values() if t == g) for g in "ABCD"}
    body = [
        tiles([
            {"label": "Critical inputs at tier A or B", "value": f"{strong} of {len(crit)}", "note": "the readiness score", "tone": "ok" if strong == len(crit) else "warn"},
            {"label": "Live (A) / Export (B)", "value": f"{dist['A']} / {dist['B']}", "note": "high confidence", "tone": "info"},
            {"label": "Estimate (C) / Public (D)", "value": f"{dist['C']} / {dist['D']}", "note": "medium and directional", "tone": "warn"},
            {"label": "Actions held back by data", "value": str(sum(1 for r in act_rows if 'C ' in str(r[2]) or 'D ' in str(r[2]))), "note": "confidence C or D", "tone": "warn"},
        ]),
        section("Upgrade these first", table(["Dependency", "Name", "Move", "How"], upgrades),
                lead="Ranked by how many actions each feeds, whether it is critical, and how far it has to climb."),
        section("Confidence by action", table(["Action", "Title", "Confidence", "Held back by"], act_rows),
                lead="An action's confidence is its weakest input. Outputs carry this grade so nobody mistakes a directional number for a measured one."),
        section("Every dependency and its fallback chain", table(["ID", "Dependency", "Tier now", "", "Feeds", "Next tier up", "Validation"], rows)),
    ]
    if hints:
        body.insert(1, callout(" ".join(hints), "ok"))
    out = ws / "outputs" / "data"
    write_text(out / f"{now.isoformat()}-data-readiness.html", page("Data readiness map", prof.get("org_name", ""), body,
               meta=[f"As of {now.isoformat()}", "Tiers: A live, B export, C estimate, D public default"]))
    md = [f"# Data readiness, {now.isoformat()}", "", f"Critical inputs at A or B: {strong} of {len(crit)}.", "", "Upgrade first:"]
    md += [f"- {u[0]} {u[1]} ({u[2]}): {u[3]}" for u in upgrades]
    write_text(out / f"{now.isoformat()}-data-readiness.md", "\n".join(md) + "\n")
    print(f"Critical at A/B: {strong}/{len(crit)}; upgrades: {[u[0] for u in upgrades]}")


if __name__ == "__main__":
    main()
