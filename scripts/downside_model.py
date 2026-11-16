#!/usr/bin/env python3
"""2027 downside case by payer: base, downside and severe scenarios, a revenue bridge,
cash runway, a sensitivity ranking and the early-warning triggers that say which scenario
the organization is actually living in.

Inputs (workspace):
  inputs/payer_mix.csv    financial_class, visits, net_revenue   (D01; falls back to the archetype default mix)
  assumptions.json        the assumption register (falls back to reference/assumptions-defaults.json)
  profile.json            financials.net_revenue_2026, operating_expense_2026, cash_on_hand

Outputs: outputs/model/downside-case.{html,md,json}
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import confidence_for, load_profile, workspace_arg  # noqa: E402
from lib.report import (REFERENCE, Raw, badge, callout, grade_badge, hbars, load_json, money, page, pct,  # noqa: E402
                        read_csv, save_json, section, table, tiles, today, waterfall, write_text)

CLASSES = ["medicare_ffs", "medicare_advantage", "medicaid", "exchange", "commercial", "self_pay", "other"]
DEFAULT_MIX = {  # tier D placeholders from segment-archetypes.md
    "physician-group": {"medicare_ffs": .30, "medicare_advantage": .15, "medicaid": .10, "exchange": .05, "commercial": .37, "self_pay": .03},
    "platform-mso": {"medicare_ffs": .28, "medicare_advantage": .15, "medicaid": .12, "exchange": .05, "commercial": .37, "self_pay": .03},
    "community-hospital": {"medicare_ffs": .30, "medicare_advantage": .15, "medicaid": .18, "exchange": .04, "commercial": .28, "self_pay": .05},
    "asc-imaging-infusion": {"medicare_ffs": .30, "medicare_advantage": .12, "medicaid": .06, "exchange": .05, "commercial": .45, "self_pay": .02},
    "outpatient-services": {"medicare_ffs": .25, "medicare_advantage": .12, "medicaid": .20, "exchange": .05, "commercial": .33, "self_pay": .05},
}


def load_mix(ws, prof):
    path = Path(ws) / "inputs" / "payer_mix.csv"
    if path.exists():
        rows = read_csv(path)
        mix = {c: 0.0 for c in CLASSES}
        for r in rows:
            mix[r["financial_class"].strip().lower()] = mix.get(r["financial_class"].strip().lower(), 0.0) + float(r["net_revenue"])
        return mix, "inputs/payer_mix.csv"
    total = prof.get("financials", {}).get("net_revenue_2026", 0)
    shares = DEFAULT_MIX.get(prof.get("archetype"), DEFAULT_MIX["physician-group"])
    return {c: total * shares.get(c, 0) for c in CLASSES}, "archetype default mix (tier D, directional)"


def load_assumptions(ws):
    path = Path(ws) / "assumptions.json"
    base = load_json(REFERENCE / "assumptions-defaults.json")
    if path.exists():
        user = load_json(path)
        for k, v in user.get("assumptions", {}).items():
            base["assumptions"].setdefault(k, {}).update(v)
    return base["assumptions"]


def run(mix, A, s, opex, apm=False):
    v = {k: A[k]["values"][s] for k in A}
    cf = v["pfs_cf_change"] if not apm else -0.0183
    steps = []
    # 1. Medicaid work requirements
    months = 6 if v["hold_harmless_elected"] else 12
    lost = mix["medicaid"] * v["medicaid_subject_share"] * v["medicaid_disenroll_rate"] * months / 12
    recovered = lost * (1 - v["uninsured_utilization_drop"]) * v["self_pay_collection_rate"]
    steps.append(("Medicaid churn", -lost + recovered))
    # 2. Exchange coverage loss
    ex_lost = mix["exchange"] * v["exchange_volume_loss"] * v["exchange_losers_uninsured"]
    ex_rec = ex_lost * (1 - v["uninsured_utilization_drop"]) * v["self_pay_collection_rate"]
    steps.append(("Exchange to self-pay", -ex_lost + ex_rec))
    # 3. Medicare fee schedule (FFS fully, MA partly)
    steps.append(("Medicare fee schedule", (mix["medicare_ffs"] + mix["medicare_advantage"] * v["ma_share_tied_to_pfs"]) * cf))
    # 4. Commercial renewals, half a year on average
    steps.append(("Commercial renewals", mix["commercial"] * v["commercial_share_renewing"] * v["commercial_renewal_change"] * 0.5))
    revenue0 = sum(mix.values())
    revenue1 = revenue0 + sum(d for _, d in steps)
    opex1 = opex * (1 + v["opex_growth"])
    return {"scenario": s, "steps": steps, "revenue_2026": revenue0, "revenue_2027": revenue1,
            "opex_2027": opex1, "ebitda_2026": revenue0 - opex, "ebitda_2027": revenue1 - opex1}


def sensitivity(mix, A, opex, apm):
    base = run(mix, A, "downside", opex, apm)["ebitda_2027"]
    out = []
    for k, a in A.items():
        if isinstance(a["values"]["downside"], bool) or a["kind"] == "sourced" and k == "pfs_cf_change":
            continue
        for mult in (0.5, 1.5):
            B = copy.deepcopy(A)
            B[k]["values"]["downside"] = a["values"]["downside"] * mult
            out.append((k, mult, run(mix, B, "downside", opex, apm)["ebitda_2027"] - base))
    rank = {}
    for k, _, d in out:
        rank[k] = max(rank.get(k, 0), abs(d))
    return sorted(rank.items(), key=lambda kv: -kv[1])


def main():
    args = workspace_arg(__doc__).parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    run_date = today(args.today)
    fin = prof.get("financials", {})
    mix, mix_src = load_mix(ws, prof)
    A = load_assumptions(ws)
    if not prof.get("medicaid_expansion_state", True):
        A["medicaid_subject_share"]["values"] = {k: 0.0 for k in ("base", "downside", "severe")}
        A["medicaid_subject_share"]["note"] = "Zeroed: every state in the footprint is outside the 2027 work requirements."
    opex = fin.get("operating_expense_2026", sum(mix.values()) * 0.92)
    cash = fin.get("cash_on_hand", 0)
    apm = prof.get("apm_qualifying", False)
    grade = confidence_for(["D01", "D02", "D03", "D04", "D07"], prof) if mix_src.startswith("inputs") else "D"
    results = {s: run(mix, A, s, opex, apm) for s in ("base", "downside", "severe")}
    sens = sensitivity(mix, A, opex, apm)

    rows = []
    for s, r in results.items():
        delta = r["revenue_2027"] - r["revenue_2026"]
        margin = r["ebitda_2027"] / r["revenue_2027"] if r["revenue_2027"] else 0
        burn = -r["ebitda_2027"] / 12 if r["ebitda_2027"] < 0 else 0
        runway = f"{cash / burn:.0f} months" if burn else "cash positive"
        rows.append([s.title(), money(r["revenue_2027"], 1), money(delta), money(r["ebitda_2027"]), pct(margin), runway])

    d = results["downside"]
    tile_items = [
        {"label": "2027 revenue at risk (downside)", "value": money(d["revenue_2027"] - d["revenue_2026"]), "note": "vs. 2026 run rate", "tone": "bad"},
        {"label": "2027 EBITDA margin (downside)", "value": pct(d["ebitda_2027"] / d["revenue_2027"]), "note": f"2026: {pct(d['ebitda_2026'] / d['revenue_2026'])}", "tone": "warn"},
        {"label": "Severe-case EBITDA", "value": money(results['severe']['ebitda_2027']), "note": "the number to plan liquidity against", "tone": "bad"},
        {"label": "Model confidence", "value": grade, "note": "weakest critical input tier", "tone": {"A": "ok", "B": "info", "C": "warn", "D": "bad"}[grade]},
    ]
    assume_rows = []
    for k, a in A.items():
        vals = a["values"]
        fmt = (lambda x: str(x)) if isinstance(vals["base"], bool) else (lambda x: pct(x))
        src = a.get("source", {}).get("name", "") if a["kind"] == "sourced" else (a.get("set_by") or "leader to confirm")
        assume_rows.append([a["label"], fmt(vals["base"]), fmt(vals["downside"]), fmt(vals["severe"]),
                            badge(a["kind"], "ok" if a["kind"] == "sourced" else "warn"), src])
    triggers = [
        ["Self-pay share of visits", "+1.5 points vs. baseline by March 2027", "Medicaid churn is running at downside rates"],
        ["Coverage denials (CARC 26, 27, 31)", "above 2% of claims for two months", "Eligibility checks are not keeping up with six-month renewals"],
        ["State hold-harmless election", "state declines the option", "Coverage losses hit cash in Q1 instead of Q3"],
        ["First 2027 commercial renewal", "flat or below", "Commercial assumption moves from base to downside"],
        ["Congressional fee schedule fix", "enacted", "Medicare line improves; rerun all scenarios"],
    ]
    body = [
        tiles(tile_items),
        section("Revenue bridge, downside scenario", waterfall("2026 revenue", d["revenue_2026"], d["steps"], "2027 revenue"),
                lead=f"Payer mix from {mix_src}. Every bar is computed from the assumption register below."),
        section("Three scenarios", table(["Scenario", "2027 revenue", "Change", "2027 EBITDA", "Margin", "Cash runway"], rows)),
        section("What moves the answer most", hbars([(k.replace("_", " "), v) for k, v in sens[:6]], fmt=money,
                                                     accent_labels=(sens[0][0].replace("_", " "),) if sens else ()),
                lead="Swing in downside EBITDA when each assumption moves 50% either way. Spend data-gathering effort on the top two."),
        section("Early-warning triggers", table(["Signal", "Threshold", "What it means"], triggers),
                lead="kpi-pulse checks these monthly. Two triggers firing moves planning from base to downside."),
        section("Assumption register", table(["Assumption", "Base", "Downside", "Severe", "Kind", "Source or owner"], assume_rows),
                callout("Sourced figures are published numbers. Assumptions are placeholders until the CFO confirms them; policy-radar proposes updates as facts change.", "warn")),
    ]
    html_out = page("2027 downside case by payer", prof.get("org_name", ""), body,
                    meta=[f"Run {run_date.isoformat()}", f"Confidence {grade}", "Revenue-side model; expenses grow at the register rate"],
                    footer="Directional planning model, not a forecast or financial advice. Replace every assumption marked 'assumption' with the organization's own figure.")
    out = ws / "outputs" / "model"
    write_text(out / "downside-case.html", html_out)
    save_json(out / "downside-case.json", {"run": run_date.isoformat(), "confidence": grade, "mix_source": mix_src,
                                           "results": results, "sensitivity": sens})
    md = [f"# 2027 downside case: {prof.get('org_name')}", "", f"Run {run_date.isoformat()}, confidence {grade}, payer mix from {mix_src}.", "",
          "| Scenario | 2027 revenue | Change | 2027 EBITDA | Margin | Cash runway |", "| --- | --- | --- | --- | --- | --- |"]
    md += ["| " + " | ".join(r) + " |" for r in rows]
    md += ["", "Biggest swing factors: " + ", ".join(k.replace("_", " ") for k, _ in sens[:3]) + "."]
    write_text(out / "downside-case.md", "\n".join(md) + "\n")
    print(f"Downside 2027 revenue change {money(d['revenue_2027'] - d['revenue_2026'])}; confidence {grade}; wrote {out}")


if __name__ == "__main__":
    main()
