#!/usr/bin/env python3
"""2028 financing cliff: provider tax and state-directed payment exposure, 2027 to 2033.

Input: inputs/supplemental.json
  {"state": "OH", "expansion_state": true,
   "programs": [
     {"name": "...", "type": "sdp", "fy2026_amount": 0, "total_payment_pct_of_medicare": 160, "base_medicaid_pct_of_medicare": 80},
     {"name": "...", "type": "provider_tax", "fy2026_amount": 0, "tax_paid": 0, "state_tax_rate_pct": 6.0},
     {"name": "...", "type": "other", "fy2026_amount": 0}]}
Rules (statute as summarized by CLA and HFMA):
  SDP: total payment capped at 100% of Medicare (expansion) or 110% (non-expansion); above-cap amounts fall
       10 percentage points a year from January 1, 2028.
  Provider tax: expansion-state safe harbor steps from 6.0% down 0.5 points a year from FFY 2028 (Oct 1, 2027)
       to 3.5%. A state taxing above the new limit must lower the tax, which shrinks what it funds.
Output: outputs/financing/<date>-financing-cliff.{html,md}
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import confidence_for, load_profile, workspace_arg  # noqa: E402
from lib.report import callout, load_json, money, page, section, table, tiles, today, waterfall, write_text  # noqa: E402

YEARS = list(range(2027, 2034))
TAX_LIMIT = {2027: 6.0, 2028: 5.5, 2029: 5.0, 2030: 4.5, 2031: 4.0, 2032: 3.5, 2033: 3.5}  # by federal fiscal year


def sdp_amount(p, year, expansion):
    cap = 100 if expansion else 110
    L, base = p["total_payment_pct_of_medicare"], p["base_medicaid_pct_of_medicare"]
    if year <= 2027 or L <= cap:
        return p["fy2026_amount"]
    level = max(cap, L - 10 * (year - 2027))
    return p["fy2026_amount"] * (level - base) / (L - base) if L > base else 0


def tax_net(p, year, expansion):
    net = p["fy2026_amount"] - p.get("tax_paid", 0)
    if not expansion:
        return net
    rate = p.get("state_tax_rate_pct", 6.0)
    scale = min(rate, TAX_LIMIT[year]) / rate if rate else 1
    return net * scale


def main():
    args = workspace_arg(__doc__).parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    now = today(args.today)
    sup = load_json(ws / "inputs" / "supplemental.json")
    exp = sup.get("expansion_state", prof.get("medicaid_expansion_state", True))
    table_rows, totals = [], {y: 0.0 for y in YEARS}
    for p in sup["programs"]:
        vals = []
        for y in YEARS:
            if p["type"] == "sdp":
                v = sdp_amount(p, y, exp)
            elif p["type"] == "provider_tax":
                v = tax_net(p, y, exp)
            else:
                v = p["fy2026_amount"]
            totals[y] += v
            vals.append(v)
        table_rows.append([p["name"]] + [money(v) for v in vals])
    table_rows.append(["Total"] + [money(totals[y]) for y in YEARS])
    base = totals[2027]
    cum = sum(base - totals[y] for y in YEARS if y >= 2028)
    steps = []
    prev = base
    for y in YEARS[1:]:
        steps.append((f"{y} change", totals[y] - prev))
        prev = totals[y]
    grade = confidence_for(["D13"], prof)
    body = [
        tiles([
            {"label": "Supplemental funding, 2027", "value": money(base), "note": "net of provider tax paid", "tone": "info"},
            {"label": "2028 change", "value": money(totals[2028] - base), "note": "first year of both phase-downs", "tone": "bad"},
            {"label": "Run-rate loss by 2033", "value": money(totals[2033] - base), "note": "per year, at constant volume", "tone": "bad"},
            {"label": "Cumulative 2028 to 2033", "value": money(-cum), "note": "the number for the long-range plan", "tone": "bad"},
        ]),
        section("How supplemental funding steps down", waterfall("2027 level", base, steps, "2033 level"),
                lead="Each red step is a year of the phase-down at constant volume and constant state policy."),
        section("By program and year", table(["Program"] + [str(y) for y in YEARS], table_rows)),
        callout("States will respond: some will restructure taxes, cut base rates or reprioritize. Treat this as the exposure if the state passes the cuts straight through, "
                "then ask the state hospital association which response the state is planning. Nursing home and ICF provider taxes are exempt from the phase-down.", "warn"),
    ]
    out = ws / "outputs" / "financing"
    write_text(out / f"{now.isoformat()}-financing-cliff.html", page("2028 financing cliff", prof.get("org_name", ""), body,
               meta=[f"As of {now.isoformat()}", f"State {sup.get('state')}, {'expansion' if exp else 'non-expansion'}", f"Data confidence {grade}"],
               footer="Rules from the 2025 reconciliation law as summarized by CLA and HFMA. Confirm program terms with the state Medicaid agency."))
    md = [f"# Financing cliff, {now.isoformat()}", "", "| Year | Total |", "| --- | --- |"] + [f"| {y} | {money(totals[y])} |" for y in YEARS]
    write_text(out / f"{now.isoformat()}-financing-cliff.md", "\n".join(md) + "\n")
    print(f"2027 {money(base)} -> 2033 {money(totals[2033])}; cumulative {money(-cum)}")


if __name__ == "__main__":
    main()
