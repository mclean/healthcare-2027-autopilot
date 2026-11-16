#!/usr/bin/env python3
"""Weekly leader brief: the facts layer. Pulls every deterministic signal into one page so the agent
spends its effort on judgment, not assembly.

Reads (all optional except the tracker): state/tracker.json, state/triggers.json, state/policy_log.json,
inputs/contracts.csv, the regulatory calendar and profile.json.
Writes: outputs/briefs/<date>-weekly-brief.{md,html}
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contract_radar import analyze  # noqa: E402
from lib.common import applicable_events, load_profile, workspace_arg  # noqa: E402
from lib.report import Raw, badge, esc, load_json, page, read_csv, section, table, tiles, today, write_text  # noqa: E402
from tracker import derive  # noqa: E402


def main():
    ap = workspace_arg(__doc__)
    ap.add_argument("--horizon-days", type=int, default=60)
    args = ap.parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    now = today(args.today)
    horizon = now + dt.timedelta(days=args.horizon_days)

    t = load_json(ws / "state" / "tracker.json")
    items = derive(t["items"], now)
    trig_path, pol_path, con_path = ws / "state" / "triggers.json", ws / "state" / "policy_log.json", ws / "inputs" / "contracts.csv"
    fired = load_json(trig_path)["fired"] if trig_path.exists() else []
    policy = load_json(pol_path)["entries"] if pol_path.exists() else []
    contracts = analyze(read_csv(con_path), now) if con_path.exists() else []

    needs = []
    for i in items:
        if i.get("decision_needed"):
            needs.append(("Decision", f"{i['id']}: {i['decision_needed']}", i["owner"] or i["owner_role"]))
    for i in items:
        if i["derived"] in ("late", "blocked"):
            needs.append(("Unblock", f"{i['id']} {i['title']} is {i['derived']}" + (f" (waiting on {', '.join(i.get('blockers', []))})" if i.get("blockers") else ""), i["owner"] or i["owner_role"]))
    for c in contracts:
        if 0 <= c["days_left"] <= 30:
            needs.append(("Contract", f"{c['payer']}: notice deadline {c['deadline']} ({c['days_left']} days). Renegotiate, renew or give notice?", c.get("owner", "")))
    for f in fired:
        needs.append(("Signal", f"{f['name']}: {f['why']}. {f['meaning']}", ", ".join(f["fires"])))

    coming = []
    for e in applicable_events(prof):
        if now <= e["_date"] <= horizon:
            coming.append([e["_date"].isoformat(), e["title"], e.get("status", ""), "calendar"])
    for i in items:
        d = dt.date.fromisoformat(i["due"])
        if now <= d <= horizon and i["derived"] != "done":
            coming.append([i["due"], f"{i['id']} due: {i['title']}", i["derived"].replace("_", " "), i["owner"] or i["owner_role"]])
    for c in contracts:
        if now <= c["deadline"] <= horizon:
            coming.append([c["deadline"].isoformat(), f"Notice deadline: {c['payer']}", c["state"], "contract"])
    coming.sort()

    week_ago = now - dt.timedelta(days=14)
    changes = [p for p in policy if dt.date.fromisoformat(p["date"]) >= week_ago]
    counts = {k: sum(1 for i in items if i["derived"] == k) for k in ("done", "on_track", "at_risk", "blocked", "late", "not_started")}

    top = needs[:3]
    md = [f"# Weekly brief, week of {now.isoformat()}", "", f"_{prof.get('org_name')}_", "", "## Needs you this week", ""]
    md += [f"{n + 1}. **{k}.** {txt} _(owner: {who})_" for n, (k, txt, who) in enumerate(needs)] or ["Nothing needs you this week."]
    md += ["", f"## Coming up in the next {args.horizon_days} days", "", "| Date | What | Status | Owner |", "| --- | --- | --- | --- |"]
    md += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in coming]
    md += ["", "## What changed in policy", ""]
    md += [f"- **{p['date']}** {p['headline']} ({p['source']['name']}, credibility {p['source']['credibility']}). {p['so_what']}" for p in changes] or ["- No material changes."]
    md += ["", "## Plan status", "", ", ".join(f"{v} {k.replace('_', ' ')}" for k, v in counts.items() if v), ""]
    write_text(ws / "outputs" / "briefs" / f"{now.isoformat()}-weekly-brief.md", "\n".join(md) + "\n")

    kind_tone = {"Decision": "info", "Unblock": "bad", "Contract": "warn", "Signal": "warn"}
    body = [
        tiles([
            {"label": "Needs you this week", "value": str(len(needs)), "note": "decisions, blocks, deadlines, signals", "tone": "warn" if needs else "ok"},
            {"label": "Top item", "value": top[0][0] if top else "none", "note": (top[0][1][:70] + "...") if top else "", "tone": "info"},
            {"label": "Plan", "value": f"{counts['done']} done / {len(items)}", "note": f"{counts['at_risk']} at risk, {counts['blocked'] + counts['late']} blocked or late", "tone": "info"},
            {"label": "Policy changes (14 days)", "value": str(len(changes)), "note": "scored sources only", "tone": "neutral"},
        ]),
        section("Needs you this week", table(["Type", "Item", "Owner"], [[badge(k, kind_tone[k]), txt, who] for k, txt, who in needs]),
                lead="Ordered: decisions first, then blocks, contract deadlines and KPI signals."),
        section(f"Coming up in the next {args.horizon_days} days", table(["Date", "What", "Status", "Owner"], coming)),
        section("What changed in policy", Raw("<ul>" + "".join(
            f"<li><b>{esc(p['date'])}</b> {esc(p['headline'])} <i>({esc(p['source']['name'])}, credibility {p['source']['credibility']})</i>. {esc(p['so_what'])}</li>"
            for p in changes) + "</ul>") if changes else Raw("<p>No material changes.</p>")),
    ]
    write_text(ws / "outputs" / "briefs" / f"{now.isoformat()}-weekly-brief.html",
               page(f"Weekly brief: week of {now:%B %-d, %Y}", prof.get("org_name", ""), body,
                    meta=[f"{len(items)} actions tracked", f"Horizon {args.horizon_days} days"],
                    footer="Facts layer generated by weekly_brief.py. The agent adds the read: what matters most, what to ask, what to drop."))
    print(f"Brief: {len(needs)} items need the leader; {len(coming)} dated items ahead; {len(changes)} policy changes")


if __name__ == "__main__":
    main()
