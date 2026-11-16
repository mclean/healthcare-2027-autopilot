#!/usr/bin/env python3
"""Site-of-care shift: margin, payback and patient savings for moving services between sites.

Input: inputs/site_of_care.csv
  service, code, annual_volume, from_site, to_site,
  entity_net_per_case_now, entity_net_per_case_alt, one_time_cost,
  patient_cost_now, patient_cost_alt, gating_items
  ("entity net" = what the organization keeps per case after direct costs, from its own point of view.
   Price each site from the CMS OPPS Addendum B, ASC Addendum AA and PFS RVU files, then your contracts.)
Output: outputs/site/<date>-site-of-care.{html,md}
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import confidence_for, load_profile, workspace_arg  # noqa: E402
from lib.report import callout, hbars, money, page, read_csv, section, table, tiles, today, write_text  # noqa: E402


def main():
    args = workspace_arg(__doc__).parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    now = today(args.today)
    rows = read_csv(ws / "inputs" / "site_of_care.csv")
    if not rows:
        raise SystemExit("inputs/site_of_care.csv has no rows yet. List candidate services first; see the site-of-care-shift skill.")
    res = []
    for r in rows:
        vol = float(r["annual_volume"])
        delta = vol * (float(r["entity_net_per_case_alt"]) - float(r["entity_net_per_case_now"]))
        one = float(r.get("one_time_cost") or 0)
        pay = (one / delta * 12) if delta > 0 and one else 0
        pat = vol * (float(r["patient_cost_now"]) - float(r["patient_cost_alt"]))
        res.append({**r, "delta": delta, "one": one, "payback": pay, "patient": pat})
    res.sort(key=lambda x: -x["delta"])
    grade = confidence_for(["D04", "D05"], prof)
    tot = sum(x["delta"] for x in res)
    capex = sum(x["one"] for x in res)
    body = [
        tiles([
            {"label": "Annual margin from all moves", "value": money(tot), "note": "entity point of view", "tone": "ok" if tot > 0 else "bad"},
            {"label": "One-time investment", "value": money(capex), "note": "equipment, build-out, staffing", "tone": "neutral"},
            {"label": "Blended payback", "value": f"{capex / tot * 12:.0f} months" if tot > 0 and capex else "n/a", "tone": "info"},
            {"label": "Patient out-of-pocket saved", "value": money(sum(x['patient'] for x in res)), "note": "per year; a referral and access story", "tone": "ok"},
        ]),
        section("Annual margin change by service", hbars([(f"{x['service']} ({x['code']})", x["delta"]) for x in res], fmt=money,
                                                          accent_labels=(f"{res[0]['service']} ({res[0]['code']})",) if res else ())),
        section("Detail", table(["Service", "Move", "Volume", "Margin change", "One-time", "Payback", "Patient saves", "Gating items"],
                                [[x["service"], f"{x['from_site']} to {x['to_site']}", f"{float(x['annual_volume']):,.0f}", money(x["delta"]),
                                  money(x["one"]), f"{x['payback']:.0f} mo" if x["payback"] else "immediate", money(x["patient"]), x.get("gating_items", "")] for x in res])),
        callout("Site-neutral pay now covers clinic visits, drug administration and (from 2027) off-campus imaging without contrast, so the hospital outpatient premium is shrinking. "
                "Before any move: confirm the code is payable at the new site (ASC covered procedures list, payer contracts), patient selection criteria, state certificate-of-need rules, "
                "and ownership and referral rules (Stark, Anti-Kickback safe harbors) with counsel.", "warn"),
    ]
    out = ws / "outputs" / "site"
    write_text(out / f"{now.isoformat()}-site-of-care.html", page("Site-of-care shift", prof.get("org_name", ""), body,
               meta=[f"As of {now.isoformat()}", f"Data confidence {grade}", "Per-case figures in the sample are illustrative"]))
    md = [f"# Site-of-care shift, {now.isoformat()}", "", f"Total annual margin change {money(tot)}; one-time {money(capex)}.", ""]
    md += [f"- {x['service']}: {money(x['delta'])} a year, payback {x['payback']:.0f} months" for x in res]
    write_text(out / f"{now.isoformat()}-site-of-care.md", "\n".join(md) + "\n")
    print(f"Site-of-care: {money(tot)} a year across {len(res)} services")


if __name__ == "__main__":
    main()
