#!/usr/bin/env python3
"""Action tracker: the single source of truth for the readiness plan.

  python3 tracker.py init   --workspace W            create state/tracker.json from the action register and profile
  python3 tracker.py update --workspace W --id A02 --status at_risk --note "..." [--owner NAME] [--decision "..."] [--evidence PATH]
  python3 tracker.py report --workspace W            derive late/at-risk/blocked, find the critical path, write outputs/tracker/

Statuses: not_started, on_track, at_risk, blocked, late, done, n/a.
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import applicable_actions, confidence_for, load_profile, workspace_arg  # noqa: E402
from lib.report import (STATUS_COLOR, Raw, badge, gantt, grade_badge, load_json, page, save_json, section,  # noqa: E402
                        table, tiles, today, write_text)

TONE = {"done": "ok", "on_track": "info", "at_risk": "warn", "blocked": "bad", "late": "bad", "not_started": "neutral", "n/a": "neutral"}


def resolve_due(action, prof, start):
    if action["due"][:4].isdigit():
        return action["due"]
    deals = [d for d in prof.get("deal_pipeline", []) if d.get("target_close")]
    if deals:
        first = min(dt.date.fromisoformat(d["target_close"]) for d in deals)
        return (first - dt.timedelta(days=120)).isoformat()
    return (start + dt.timedelta(days=180)).isoformat()


def cmd_init(ws, prof, now):
    path = ws / "state" / "tracker.json"
    if path.exists():
        raise SystemExit(f"{path} exists. Use update, or delete it to start over.")
    items = []
    for a in applicable_actions(prof):
        items.append({"id": a["id"], "title": a["title"], "skill": a["skill"], "owner_role": a["owner_role"], "owner": "",
                      "due": resolve_due(a, prof, now), "depends_on": a["depends_on"], "data": a["data"],
                      "done_when": a["done_when"], "protects_against": a["protects_against"],
                      "status": "not_started", "decision_needed": "", "evidence": [], "history": []})
    save_json(path, {"created": now.isoformat(), "items": items})
    print(f"Created {path} with {len(items)} actions")


def cmd_update(ws, args, now):
    path = ws / "state" / "tracker.json"
    t = load_json(path)
    for it in t["items"]:
        if it["id"] == args.id:
            if args.status:
                it["status"] = args.status
            if args.owner:
                it["owner"] = args.owner
            if args.decision is not None:
                it["decision_needed"] = args.decision
            if args.evidence:
                it["evidence"].append(args.evidence)
            it["history"].append({"date": now.isoformat(), "status": it["status"], "note": args.note or ""})
            save_json(path, t)
            print(f"{args.id} -> {it['status']}")
            return
    raise SystemExit(f"No action {args.id}")


def derive(items, now):
    by_id = {i["id"]: i for i in items}
    for i in items:
        due = dt.date.fromisoformat(i["due"])
        s = i["status"]
        if s in ("done", "n/a"):
            i["derived"] = s
            continue
        blockers = [d for d in i["depends_on"] if d in by_id and by_id[d]["status"] != "done"
                    and dt.date.fromisoformat(by_id[d]["due"]) < now]
        if due < now:
            i["derived"] = "late"
        elif blockers or s == "blocked":
            i["derived"] = "blocked"
        elif s == "at_risk" or (s == "not_started" and (due - now).days <= 21):
            i["derived"] = "at_risk"
        else:
            i["derived"] = s
        i["blockers"] = blockers
    return items


def critical_path(items):
    by_id = {i["id"]: i for i in items}
    memo = {}

    def chain(i):
        if i["id"] in memo:
            return memo[i["id"]]
        deps = [by_id[d] for d in i["depends_on"] if d in by_id and by_id[d]["derived"] != "done"]
        best = max((chain(d) for d in deps), key=len, default=[])
        memo[i["id"]] = best + [i["id"]]
        return memo[i["id"]]

    open_items = [i for i in items if i["derived"] not in ("done", "n/a")]
    return max((chain(i) for i in open_items), key=lambda c: (len(c), c[-1]), default=[])


def cmd_report(ws, prof, now):
    t = load_json(ws / "state" / "tracker.json")
    items = derive(t["items"], now)
    path_ids = critical_path(items)
    counts = {k: sum(1 for i in items if i["derived"] == k) for k in TONE}
    by_id = {i["id"]: i for i in items}
    g_items = []
    for i in sorted(items, key=lambda x: x["due"]):
        due = dt.date.fromisoformat(i["due"])
        starts = [dt.date.fromisoformat(by_id[d]["due"]) for d in i["depends_on"] if d in by_id]
        start = max(starts + [dt.date.fromisoformat(t["created"])])
        if start >= due:
            start = due - dt.timedelta(days=14)
        g_items.append({"label": f"{i['id']} {i['title']}", "start": start, "end": due, "status": i["derived"]})
    end = max(dt.date.fromisoformat(i["due"]) for i in items) + dt.timedelta(days=20)
    rows = []
    for i in sorted(items, key=lambda x: x["due"]):
        last = i["history"][-1]["note"] if i["history"] else ""
        rows.append([i["id"], i["title"], i["owner"] or i["owner_role"], i["due"], badge(i["derived"].replace("_", " "), TONE[i["derived"]]),
                     grade_badge(confidence_for(i["data"], prof)), last])
    decisions = [[i["id"], i["decision_needed"], i["owner"] or i["owner_role"]] for i in items if i.get("decision_needed")]
    body = [
        tiles([
            {"label": "Done", "value": str(counts["done"]), "tone": "ok"},
            {"label": "On track", "value": str(counts["on_track"]), "tone": "info"},
            {"label": "At risk", "value": str(counts["at_risk"]), "tone": "warn"},
            {"label": "Late or blocked", "value": str(counts["late"] + counts["blocked"]), "tone": "bad"},
        ]),
        section("Plan on a page", gantt(g_items, dt.date.fromisoformat(t["created"]) - dt.timedelta(days=7), end, now, width=1000, left=360),
                lead="Bars run from when an action can start (its dependencies' due dates) to its own due date. Color is derived status."),
        section("Critical path", Raw("<p><b>" + " &rarr; ".join(path_ids) + "</b></p>"),
                lead="The longest chain of unfinished, dependent actions. A slip anywhere on it moves the end date."),
        section("Decisions the leader owes", table(["Action", "Decision", "Who is waiting"], decisions) if decisions else Raw("<p>None this week.</p>")),
        section("Every action", table(["ID", "Action", "Owner", "Due", "Status", "Data", "Latest note"], rows)),
    ]
    out = ws / "outputs" / "tracker"
    write_text(out / f"{now.isoformat()}-tracker.html", page("Action tracker", prof.get("org_name", ""), body,
               meta=[f"As of {now.isoformat()}", f"{len(items)} actions", "Data column = confidence grade of the action's inputs"]))
    save_json(ws / "state" / "tracker.json", {**t, "items": items, "critical_path": path_ids, "reported": now.isoformat()})
    md = [f"# Action tracker, {now.isoformat()}", "", f"Critical path: {' -> '.join(path_ids)}", "", "| ID | Action | Due | Status |", "| --- | --- | --- | --- |"]
    md += [f"| {i['id']} | {i['title']} | {i['due']} | {i['derived']} |" for i in sorted(items, key=lambda x: x["due"])]
    write_text(out / f"{now.isoformat()}-tracker.md", "\n".join(md) + "\n")
    print(f"Tracker: {counts}; critical path {' -> '.join(path_ids)}")


def main():
    ap = workspace_arg(__doc__)
    ap.add_argument("command", choices=["init", "update", "report"])
    ap.add_argument("--id")
    ap.add_argument("--status", choices=list(TONE))
    ap.add_argument("--note")
    ap.add_argument("--owner")
    ap.add_argument("--decision")
    ap.add_argument("--evidence")
    args = ap.parse_args()
    ws = Path(args.workspace)
    now = today(args.today)
    prof = load_profile(ws)
    if args.command == "init":
        cmd_init(ws, prof, now)
    elif args.command == "update":
        cmd_update(ws, args, now)
    else:
        cmd_report(ws, prof, now)


if __name__ == "__main__":
    main()
