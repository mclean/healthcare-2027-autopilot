#!/usr/bin/env python3
"""Contract renewal radar: the real deadline is the notice date, not the renewal date.

Input:  inputs/contracts.csv  (template: templates/contracts.csv)
        payer, product, effective_date, term_months, auto_renew, notice_days, escalator,
        share_of_net_revenue, termination_without_cause_days, prep_status, owner
Output: outputs/contracts/<date>-contract-radar.{html,md}
        state/contract_alerts.json  one-time jobs that build_schedule.py adds to the schedule
        a recommended value for commercial_share_renewing in the assumption register
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import confidence_for, load_profile, workspace_arg  # noqa: E402
from lib.report import (Raw, badge, callout, gantt, grade_badge, page, pct, read_csv, save_json, section,  # noqa: E402
                        table, tiles, today, write_text)

ALERT_OFFSETS = (180, 120, 90, 60, 30)
DEFAULT_NOTICE = 90


def add_months(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    return dt.date(d.year + y, m + 1, min(d.day, 28))


def next_renewal(eff, term, now):
    r = add_months(eff, term)
    while r < now:
        r = add_months(r, term)
    return r


def analyze(rows, now):
    out = []
    for r in rows:
        eff = dt.date.fromisoformat(r["effective_date"])
        term = int(r.get("term_months") or 12)
        renewal = add_months(eff, term)
        auto = r.get("auto_renew", "").lower() in ("yes", "y", "true", "1")
        confirmed = bool(r.get("notice_days"))
        notice = int(r["notice_days"]) if confirmed else DEFAULT_NOTICE
        deadline = renewal - dt.timedelta(days=notice)
        missed = deadline < now <= renewal
        if renewal < now:
            renewal = next_renewal(eff, term, now)
            deadline = renewal - dt.timedelta(days=notice)
            missed = deadline < now
        prep_start = deadline - dt.timedelta(days=90)
        days_left = (deadline - now).days
        if missed and auto:
            state, tone = "auto-renewed: notice window missed", "bad"
        elif missed:
            state, tone = "notice window missed", "bad"
        elif days_left <= 30:
            state, tone = "act now", "bad"
        elif now >= prep_start and r.get("prep_status", "") != "done":
            state, tone = "in prep window", "warn"
        else:
            state, tone = "scheduled", "info"
        insights = []
        esc_txt = (r.get("escalator") or "").lower()
        if "medicare" in esc_txt:
            insights.append("Paid off the Medicare fee schedule: inherits the 2027 conversion factor cut (-2.31% for most clinicians) unless the contract has a floor.")
        if not esc_txt:
            insights.append("No escalator on file: rates are flat until renegotiated.")
        if "cpi" in esc_txt:
            insights.append("CPI-linked: check the cap against medical cost trend (PwC projects 9% group trend for 2027).")
        if missed and r.get("termination_without_cause_days"):
            insights.append(f"Notice window passed; remaining lever is termination without cause ({r['termination_without_cause_days']} days), used only as a last resort.")
        if not confirmed:
            insights.append(f"Notice period not confirmed; assumed {DEFAULT_NOTICE} days. Confirm with the payer.")
        out.append({**r, "renewal": renewal, "deadline": deadline, "prep_start": prep_start, "days_left": days_left,
                    "state": state, "tone": tone, "confirmed": confirmed, "insights": insights,
                    "share": float(r.get("share_of_net_revenue") or 0)})
    return sorted(out, key=lambda c: c["deadline"])


def main():
    args = workspace_arg(__doc__).parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    now = today(args.today)
    rows = read_csv(ws / "inputs" / "contracts.csv")
    if not rows:
        raise SystemExit("inputs/contracts.csv has no rows yet. Fill it from the contract folder (tier A/B) or the CFO's list (tier C); see dependencies.json D06.")
    cs = analyze(rows, now)
    grade = confidence_for(["D06"], prof)

    alerts = []
    for c in cs:
        if c["state"].startswith("auto-renewed") or c["state"] == "notice window missed":
            continue
        for off in ALERT_OFFSETS:
            d = c["deadline"] - dt.timedelta(days=off)
            if d > now:
                slug = c["payer"].lower().replace(" ", "-").replace("(", "").replace(")", "")
                alerts.append({"id": f"contract-{slug}-{off}d", "type": "once", "at": d.isoformat(), "time": "08:21",
                               "skill": "contract-renewal-radar", "name": f"{c['payer']}: notice deadline in {off} days",
                               "why": f"{c['payer']} ({c['product']}) notice deadline {c['deadline']} for renewal {c['renewal']}. "
                                      f"{'Start the negotiation prep pack.' if off >= 90 else 'Confirm the decision: renegotiate, renew or give notice.'}",
                               "deliver": True, "needs": ["D06"], "outputs": []})
    save_json(ws / "state" / "contract_alerts.json", alerts)

    commercial = [c for c in cs if c.get("product", "").lower() == "commercial"]
    renew27 = sum(c["share"] for c in commercial if c["renewal"].year == 2027)
    com_total = None
    mix_path = ws / "inputs" / "payer_mix.csv"
    if mix_path.exists():
        mix = read_csv(mix_path)
        tot = sum(float(m["net_revenue"]) for m in mix)
        com_total = sum(float(m["net_revenue"]) for m in mix if m["financial_class"] == "commercial") / tot
    com_total = com_total or sum(c["share"] for c in commercial) or 1
    recommended = renew27 / com_total

    soon = [c for c in cs if 0 <= c["days_left"] <= 90]
    missed = [c for c in cs if "missed" in c["state"]]
    unconf = [c for c in cs if not c["confirmed"]]
    start = now - dt.timedelta(days=30)
    end = max(c["renewal"] for c in cs) + dt.timedelta(days=30)
    g = []
    for c in cs:
        g.append({"label": f"{c['payer']}: prep to notice", "start": c["prep_start"], "end": c["deadline"],
                  "status": {"bad": "late", "warn": "at_risk", "info": "on_track"}[c["tone"]]})
    rows_html = []
    for c in cs:
        rows_html.append([Raw(f"{c['payer']}<br><span style='color:#6b7685'>{c['product'].replace('_', ' ')}</span>"), pct(c["share"]), c["renewal"].isoformat(),
                          c["deadline"].isoformat() + ("" if c["confirmed"] else " (assumed)"),
                          c.get("escalator") or "none on file", badge(c["state"], c["tone"]),
                          Raw("<br>".join(f"&bull; {i}" for i in c["insights"]))])
    body = [
        tiles([
            {"label": "Contracts tracked", "value": str(len(cs)), "note": f"{pct(sum(c['share'] for c in cs), 0)} of net revenue", "tone": "info"},
            {"label": "Notice deadlines in 90 days", "value": str(len(soon)), "note": "need a decision", "tone": "warn" if soon else "ok"},
            {"label": "Windows already missed", "value": str(len(missed)), "note": "auto-renewed or exposed", "tone": "bad" if missed else "ok"},
            {"label": "Commercial revenue renewing in 2027", "value": pct(recommended, 0), "note": "feeds the downside model", "tone": "info"},
        ]),
        section("Notice windows", gantt(g, start, end, now, width=1000, left=320),
                lead="Each bar runs from the start of negotiation prep (90 days before notice) to the notice deadline, the last day to act."),
        section("Every contract", table(["Payer and product", "Share", "Renews", "Notice deadline", "Escalator", "Status", "What to know"], rows_html, cls="notes")),
        callout(f"{len(alerts)} reminder jobs written to state/contract_alerts.json. Rebuild the schedule to add them. "
                f"Recommended assumption: commercial_share_renewing = {recommended:.2f}.", "info"),
    ]
    out = ws / "outputs" / "contracts"
    write_text(out / f"{now.isoformat()}-contract-radar.html", page("Contract renewal radar", prof.get("org_name", ""), body,
               meta=[f"As of {now.isoformat()}", f"Data confidence {grade}", "Payer names in the sample are anonymized"]))
    md = [f"# Contract renewal radar, {now.isoformat()}", "", "| Payer | Renews | Notice deadline | Status |", "| --- | --- | --- | --- |"]
    md += [f"| {c['payer']} | {c['renewal']} | {c['deadline']} | {c['state']} |" for c in cs]
    md += ["", f"Recommended commercial_share_renewing: {recommended:.2f}"]
    write_text(out / f"{now.isoformat()}-contract-radar.md", "\n".join(md) + "\n")
    print(f"{len(cs)} contracts; {len(soon)} deadlines within 90 days; {len(missed)} missed; {len(alerts)} alerts; commercial renewing 2027 = {recommended:.2f}")


if __name__ == "__main__":
    main()
