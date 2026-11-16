#!/usr/bin/env python3
"""Monthly KPI pulse: compare the latest month to the baseline, fire triggers, route each to a skill.

Input:  inputs/kpis.csv   month (YYYY-MM), kpi (id from reference/kpi-definitions.json), value
        profile.json      kpi_baseline_period (YYYY-MM), optional kpi_overrides {kpi_id: {trigger...}}
Output: outputs/kpi/<date>-kpi-pulse.{html,md}
        state/triggers.json   fired triggers with the skill each one calls, read by the weekly brief and tracker
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import confidence_for, load_profile, reference, workspace_arg  # noqa: E402
from lib.report import (ACCENT, BAD, Raw, badge, esc, grade_badge, page, read_csv, save_json, section, table,  # noqa: E402
                        tiles, today, write_text)


def spark(values, color=ACCENT, w=140, h=34):
    if len(values) < 2:
        return Raw("")
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
    pts = " ".join(f"{i * (w - 6) / (len(values) - 1) + 3:.1f},{h - 4 - (v - lo) / span * (h - 8):.1f}" for i, v in enumerate(values))
    last = pts.split(" ")[-1].split(",")
    return Raw(f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}"><polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/>'
               f'<circle cx="{last[0]}" cy="{last[1]}" r="3" fill="{color}"/></svg>')


def check(trig, cur, base):
    t, v = trig["type"], trig["value"]
    if cur is None:
        return False, "no data"
    if t == "above":
        return cur > v, f"{cur:g} vs limit {v:g}"
    if t == "below":
        return cur < v, f"{cur:g} vs floor {v:g}"
    if base is None:
        return False, "no baseline"
    if t == "delta_vs_baseline_pts":
        d = cur - base
        return (d <= v if v < 0 else d >= v), f"{d:+.1f} pts vs baseline"
    if t == "delta_vs_baseline_pct":
        d = (cur - base) / base * 100 if base else 0
        return d >= v, f"{d:+.0f}% vs baseline"
    if t == "delta_vs_baseline_abs":
        d = cur - base
        return d >= v, f"{d:+.1f} vs baseline"
    return False, "unknown trigger"


def main():
    args = workspace_arg(__doc__).parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    now = today(args.today)
    defs = reference("kpi-definitions.json")["kpis"]
    overrides = prof.get("kpi_overrides", {})
    rows = read_csv(ws / "inputs" / "kpis.csv")
    if not rows:
        raise SystemExit("inputs/kpis.csv has no rows yet. kpi-pulse fills it from the month-end exports; see dependencies.json for each KPI's source.")
    months = sorted({r["month"] for r in rows})
    latest = months[-1]
    base_m = prof.get("kpi_baseline_period", months[0])
    series = {}
    for r in rows:
        series.setdefault(r["kpi"], {})[r["month"]] = float(r["value"])

    fired, table_rows, tile_items = [], [], []
    for d in defs:
        s = series.get(d["id"])
        if not s:
            table_rows.append([d["name"], "no data", "", "", badge("missing", "neutral"), f"Data {d['data']}: see dependencies.json"])
            continue
        trig = {**d["trigger"], **overrides.get(d["id"], {})}
        cur, base = s.get(latest), s.get(base_m)
        hit, why = check(trig, cur, base)
        if hit and "and" in trig:
            other = series.get(trig["and"]["kpi"], {})
            hit2, why2 = check(trig["and"], other.get(latest), other.get(base_m))
            hit, why = hit and hit2, f"{why} and {trig['and']['kpi']} {why2}"
        unit = "%" if d["unit"] == "pct" else (" days" if d["unit"] == "days" else "")
        vals = [s[m] for m in months if m in s]
        table_rows.append([d["name"], f"{cur:g}{unit}", f"{base:g}{unit}" if base is not None else "n/a", spark(vals, BAD if hit else ACCENT),
                           badge("trigger" if hit else "ok", "bad" if hit else "ok"), why])
        if hit:
            fired.append({"kpi": d["id"], "name": d["name"], "value": cur, "baseline": base, "why": why, "meaning": d["meaning"],
                          "fires": d["fires"], "month": latest, "confidence": confidence_for([d["data"]], prof)})
    save_json(ws / "state" / "triggers.json", {"run": now.isoformat(), "month": latest, "baseline": base_m, "fired": fired})

    route = {}
    for f in fired:
        for sk in f["fires"]:
            route.setdefault(sk, []).append(f["name"])
    tile_items = [
        {"label": "Triggers fired", "value": str(len(fired)), "note": f"{latest} vs baseline {base_m}", "tone": "bad" if fired else "ok"},
        {"label": "Playbooks called", "value": str(len(route)), "note": ", ".join(route) or "none", "tone": "warn" if route else "ok"},
        {"label": "KPIs with data", "value": f"{sum(1 for d in defs if d['id'] in series)} of {len(defs)}", "note": "missing ones list their fallback", "tone": "info"},
    ]
    route_rows = [[sk, "; ".join(names)] for sk, names in route.items()]
    body = [
        tiles(tile_items),
        section("Pulse", table(["KPI", latest, f"Baseline {base_m}", "Trend", "Status", "Why"], table_rows),
                lead="Thresholds are starting defaults from reference/kpi-definitions.json; tune them in profile.json kpi_overrides."),
        section("What the triggers set in motion", table(["Skill called", "Because of"], route_rows) if route_rows else Raw("<p>Nothing fired. No action needed this month.</p>"),
                lead="Each fired trigger becomes a task for the named skill and a line in Monday's brief."),
    ]
    if fired:
        body.append(section("Reading the pattern", Raw("<ul>" + "".join(f"<li><b>{esc(f['name'])}:</b> {esc(f['meaning'])}</li>" for f in fired) + "</ul>")))
    out = ws / "outputs" / "kpi"
    write_text(out / f"{now.isoformat()}-kpi-pulse.html", page("Monthly KPI pulse", prof.get("org_name", ""), body,
               meta=[f"Month {latest}", f"Baseline {base_m}", f"Run {now.isoformat()}"]))
    md = [f"# KPI pulse, {latest} (baseline {base_m})", "", f"{len(fired)} triggers fired.", ""]
    md += [f"- {f['name']}: {f['why']}. Calls: {', '.join(f['fires'])}." for f in fired]
    write_text(out / f"{now.isoformat()}-kpi-pulse.md", "\n".join(md) + "\n")
    print(f"{len(fired)} triggers fired; routes: {route}")


if __name__ == "__main__":
    main()
