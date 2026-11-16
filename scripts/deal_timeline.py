#!/usr/bin/env python3
"""Deal timeline: work back from each target close date through every state's notice period.

Input:  profile.json deal_pipeline [{name, type, states, target_close, target_assets}]
Output: outputs/deals/<date>-deal-timeline.{html,md}
For each deal and state: file-by date = target close - notice period - 21 days of preparation buffer.
States with no fixed period in the sources get a 180-day placeholder flagged for counsel.
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import load_profile, reference, workspace_arg  # noqa: E402
from lib.report import badge, callout, gantt, page, section, table, tiles, today, write_text  # noqa: E402

PREP_BUFFER = 21


def main():
    args = workspace_arg(__doc__).parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    now = today(args.today)
    ref = reference("state-notice-periods.json")
    rows, g, alerts = [], [], 0
    for deal in prof.get("deal_pipeline", []):
        close = dt.date.fromisoformat(deal["target_close"])
        for st in deal.get("states", []):
            info = ref["states"].get(st)
            if not info:
                rows.append([deal["name"], st, "no state notice law in reference", "", "", badge("confirm with counsel", "neutral"), ""])
                continue
            days = info["days"] or ref["placeholder_days"]
            placeholder = info["days"] is None
            file_by = close - dt.timedelta(days=days)
            prep_by = file_by - dt.timedelta(days=PREP_BUFFER)
            left = (file_by - now).days
            if left < 0:
                status, tone = "window missed: move the close", "bad"
            elif left <= 45:
                status, tone = "file now", "bad"
            elif left <= 90:
                status, tone = "prepare filing", "warn"
            else:
                status, tone = "on calendar", "info"
            alerts += 1
            rows.append([deal["name"], st, f"{days} days" + (" (placeholder)" if placeholder else ""), prep_by.isoformat(), file_by.isoformat(),
                         badge(status, tone), info["rule"].rstrip(".") + "." + (f" Threshold: {info['threshold']}." if info.get("threshold") else "")])
            g.append({"label": f"{deal['name'][:22]} {st} notice", "start": file_by, "end": close,
                      "status": {"bad": "late", "warn": "at_risk", "info": "on_track"}[tone]})
            g.append({"label": f"{deal['name'][:22]} {st} prep", "start": prep_by, "end": file_by, "status": "not_started"})
    if not rows:
        raise SystemExit("No deal_pipeline entries in profile.json")
    start = min(x["start"] for x in g) - dt.timedelta(days=14) if g else now
    end = max(x["end"] for x in g) + dt.timedelta(days=14) if g else now
    body = [
        tiles([
            {"label": "Deals in pipeline", "value": str(len(prof.get('deal_pipeline', []))), "tone": "info"},
            {"label": "State filings to plan", "value": str(alerts), "tone": "info"},
            {"label": "Filings due within 45 days", "value": str(sum(1 for r in rows if 'file now' in str(r[5]))), "tone": "bad"},
        ]),
        section("Filing windows", gantt(g, min(start, now), end, now, width=1000, left=320),
                lead="Prep bars end on the file-by date; notice bars run from filing to the target close."),
        section("By deal and state", table(["Deal", "State", "Notice period", "Start prep by", "File by", "Status", "Rule"], rows, cls="notes")),
        callout("Not legal advice. Periods come from the state rules reference (PESP and McDermott, 2026). Thresholds decide whether a filing is required at all; "
                "counsel confirms each one. Also plan for: HSR, payer change-of-ownership notices and Medicaid re-enrollment.", "warn"),
    ]
    out = ws / "outputs" / "deals"
    write_text(out / f"{now.isoformat()}-deal-timeline.html", page("Deal timeline: state notice windows", prof.get("org_name", ""), body,
               meta=[f"As of {now.isoformat()}", f"Prep buffer {PREP_BUFFER} days"]))
    md = [f"# Deal timeline, {now.isoformat()}", "", "| Deal | State | Notice | File by | Status |", "| --- | --- | --- | --- | --- |"]
    md += [f"| {r[0]} | {r[1]} | {r[2]} | {r[4]} | {str(r[5]).split('>')[1].split('<')[0] if '<' in str(r[5]) else r[5]} |" for r in rows]
    write_text(out / f"{now.isoformat()}-deal-timeline.md", "\n".join(md) + "\n")
    print("\n".join(md[4:]))


if __name__ == "__main__":
    main()
