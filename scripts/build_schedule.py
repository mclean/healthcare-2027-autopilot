#!/usr/bin/env python3
"""Build the leader's schedule: recurring agent jobs plus one-shot milestone jobs.

Writes, under <workspace>/schedule/:
  jobs.json                     canonical list of jobs (recurring and one-shot)
  scheduled-task-prompts.md     ready to create as Claude scheduled tasks (tier A)
  prompts/<job>.txt             self-contained prompt per job
  crontab.txt                   headless agent via cron and `claude -p` (tier B)
  github-actions/<job>.yml      scheduled GitHub Actions workflows (tier B)
  readiness-calendar.ics        calendar reminders for when no agent scheduler exists (tier C)
  schedule.html                 visual map of the next 14 months

Usage: python3 build_schedule.py --workspace readiness [--today 2026-11-16]
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import applicable_actions, applicable_events, load_profile, reference, workspace_arg  # noqa: E402
from lib.report import Raw, badge, gantt, page, save_json, section, table, tiles, today, write_text  # noqa: E402

PLUGIN = "healthcare-2027-autopilot"
DOW = {"0": "Sun", "1": "Mon", "2": "Tue", "3": "Wed", "4": "Thu", "5": "Fri", "6": "Sat", "7": "Sun"}


def business_day_on_or_after(d):
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def business_day_on_or_before(d):
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d


def human_cron(expr):
    m, h, dom, mon, dow = expr.split()
    t = f"{int(h):02d}:{int(m):02d}"
    if dom == "*" and dow != "*":
        return f"Every {', '.join(DOW[d] for d in dow.split(','))} at {t}"
    if dom != "*" and mon == "*":
        return f"Monthly on day {dom} at {t}"
    if dom != "*" and mon != "*":
        months = ", ".join(dt.date(2000, int(x), 1).strftime("%b") for x in mon.split(","))
        return f"Day {dom} of {months} at {t}"
    return expr


def prompt_for(job, prof, ws_label):
    org = prof.get("org_name", "the organization")
    deliver = prof.get("infrastructure", {}).get("delivery", "a markdown file in outputs/")
    lines = [
        f"Run the `{job['skill']}` skill from the {PLUGIN} plugin for {org}.",
        f"Readiness workspace: {ws_label} (profile.json, assumptions.json, inputs/, state/, outputs/).",
        f"Purpose of this run: {job['why']}",
    ]
    if job.get("action"):
        lines.append(f"Action in scope: {job['action']} ({job['action_title']}). Done when: {job['done_when']}.")
    if job.get("event"):
        lines.append(f"Calendar event in scope: {job['event']} on {job['event_date']}. Confirm the date still holds with a source scored 4 or higher before acting on it.")
    lines += [
        "Before using any data input, check its tier in profile.json data_tiers. If the tier-A or tier-B source is missing or stale, walk the fallback chain in reference/dependencies.json, use the best available tier, and label every number with its confidence grade.",
        "Write outputs to the workspace paths listed in the skill. Update state/tracker.json for any action whose status changed.",
        f"Deliver a short summary through: {deliver}. If nothing material changed, deliver one line saying so, or nothing if the job is marked deliver-only-if-material.",
        "Never send messages to anyone other than the leader, never change payer contracts, claims or patient records, and stop to ask before any irreversible step.",
    ]
    return "\n".join(lines)


def build_jobs(prof, start):
    catalog = reference("schedule-catalog.json")
    actions = applicable_actions(prof)
    action_skills = {a["skill"] for a in actions}
    always = {"weekly-leader-brief", "policy-radar", "action-tracker", "kpi-pulse", "data-readiness", "board-update"}
    jobs = []
    prefs = prof.get("schedule_overrides", {})
    for r in catalog["recurring"]:
        if r["skill"] not in always and r["skill"] not in action_skills:
            continue
        cron = prefs.get(r["id"], r["cron"])
        jobs.append({**r, "type": "recurring", "cron": cron, "when": human_cron(cron)})

    horizon = start + dt.timedelta(days=420)
    for e in applicable_events(prof):
        prep = business_day_on_or_before(e["_date"] - dt.timedelta(days=e.get("lead_days", 30)))
        day_of = business_day_on_or_after(e["_date"])
        for kind, d, why in (("prep", prep, f"Prepare for: {e['title']}. {e['detail']}"),
                             ("day-of", day_of, f"Confirm what happened: {e['title']}, and update assumptions and the tracker.")):
            if start <= d <= horizon:
                skill = "policy-radar" if kind == "day-of" else _skill_for_event(e, actions)
                jobs.append({"id": f"{e['id']}-{kind}", "type": "once", "at": d.isoformat(), "time": "07:31",
                             "skill": skill, "name": f"{'Prep' if kind == 'prep' else 'Day of'}: {e['title']}",
                             "why": why, "event": e["id"], "event_date": e["date"], "deliver": True,
                             "needs": [], "outputs": []})
    for a in actions:
        if not a["due"][:4].isdigit():
            continue
        due = business_day_on_or_before(dt.date.fromisoformat(a["due"]))
        for kind, d in (("checkpoint", due - dt.timedelta(days=14)), ("due", due)):
            if start <= d <= horizon:
                jobs.append({"id": f"{a['id']}-{kind}", "type": "once", "at": d.isoformat(), "time": "08:03",
                             "skill": "action-tracker" if kind == "checkpoint" else a["skill"],
                             "name": f"{a['id']} {'checkpoint' if kind == 'checkpoint' else 'due'}: {a['title']}",
                             "why": f"{'Two weeks out' if kind == 'checkpoint' else 'Due today'}: {a['title']}.",
                             "action": a["id"], "action_title": a["title"], "done_when": a["done_when"],
                             "deliver": True, "needs": a["data"], "outputs": []})
    for c in prof.get("_contract_alerts", []):
        jobs.append(c)
    return jobs


def _skill_for_event(e, actions):
    ids = e.get("actions", [])
    for a in actions:
        if a["id"] in ids:
            return a["skill"]
    return "policy-radar"


def to_utc_cron(expr, tz, ref):
    m, h, dom, mon, dow = expr.split()
    local = dt.datetime(ref.year, ref.month, ref.day, int(h), int(m), tzinfo=ZoneInfo(tz))
    u = local.astimezone(dt.timezone.utc)
    shift = (u.date() - local.date()).days
    if shift and dow != "*":
        dow = ",".join(str((int(d) + shift) % 7) for d in dow.split(","))
    if shift and dom != "*":
        dom = ",".join(str(int(d) + shift) for d in dom.split(","))
    return f"{u.minute} {u.hour} {dom} {mon} {dow}"


def ics_escape(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


RRULE_DAY = {"0": "SU", "1": "MO", "2": "TU", "3": "WE", "4": "TH", "5": "FR", "6": "SA"}


def ics_for(jobs, tz, start):
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", f"PRODID:-//{PLUGIN}//schedule//EN", "CALSCALE:GREGORIAN",
           "X-WR-CALNAME:2027 Readiness Autopilot"]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for j in jobs:
        desc = f"Ask your agent: run the {j['skill']} skill ({PLUGIN}). {j['why']}"
        if j["type"] == "once":
            hh, mm = j["time"].split(":")
            d = dt.date.fromisoformat(j["at"])
            dtstart = f"DTSTART;TZID={tz}:{d:%Y%m%d}T{hh}{mm}00"
            rrule = None
        else:
            m, h, dom, mon, dow = j["cron"].split()
            first = start
            if dow != "*":
                days = [int(x) % 7 for x in dow.split(",")]
                while (first.isoweekday() % 7) not in days:
                    first += dt.timedelta(days=1)
                rrule = "RRULE:FREQ=WEEKLY;BYDAY=" + ",".join(RRULE_DAY[str(d)] for d in days)
            else:
                first = dt.date(start.year, start.month, int(dom.split(",")[0]))
                if first < start:
                    first = dt.date(start.year + (start.month // 12), start.month % 12 + 1, first.day)
                rrule = f"RRULE:FREQ=MONTHLY;BYMONTHDAY={dom}" + ("" if mon == "*" else f";BYMONTH={mon}")
            dtstart = f"DTSTART;TZID={tz}:{first:%Y%m%d}T{int(h):02d}{int(m):02d}00"
        out += ["BEGIN:VEVENT", f"UID:{j['id']}@{PLUGIN}", f"DTSTAMP:{stamp}", dtstart, "DURATION:PT15M",
                f"SUMMARY:{ics_escape(j['name'])}", f"DESCRIPTION:{ics_escape(desc)}"]
        if rrule:
            out.append(rrule)
        out += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{ics_escape(j['name'])}", "TRIGGER:-PT10M", "END:VALARM", "END:VEVENT"]
    out.append("END:VCALENDAR")
    return "\r\n".join(out) + "\r\n"


def gha_for(job, prompt, tz, ref):
    utc = to_utc_cron(job["cron"], tz, ref)
    body = prompt.replace("\n", "\n            ")
    return f"""# {job['name']} ({job['when']}, {tz})
# GitHub cron runs in UTC. Converted from local time on {ref.isoformat()}; daylight saving shifts it by an hour
# for part of the year. Re-run build_schedule.py after each DST change if the exact hour matters.
name: "autopilot: {job['name']}"
on:
  schedule:
    - cron: "{utc}"
  workflow_dispatch: {{}}
permissions:
  contents: write
jobs:
  run:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{{{ secrets.ANTHROPIC_API_KEY }}}}
          prompt: |
            {body}
      - name: Save outputs back to the private repo
        run: |
          git config user.name "readiness-autopilot"
          git config user.email "readiness-autopilot@users.noreply.github.com"
          git add -A readiness || true
          git diff --cached --quiet || git commit -m "autopilot: {job['id']} run"
          git push
"""


def main():
    ap = workspace_arg(__doc__)
    ap.add_argument("--workspace-label", default=None, help="How prompts should refer to the workspace (path, drive folder or repo)")
    args = ap.parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    start = today(args.today)
    tz = prof.get("leader", {}).get("timezone", "America/Chicago")
    ws_label = args.workspace_label or prof.get("infrastructure", {}).get("state_store_label", str(ws))
    contracts = ws / "state" / "contract_alerts.json"
    if contracts.exists():
        from lib.report import load_json
        prof["_contract_alerts"] = load_json(contracts)
    jobs = build_jobs(prof, start)
    for j in jobs:
        j["timezone"] = tz
        j["prompt"] = prompt_for(j, prof, ws_label)
    jobs.sort(key=lambda j: (j["type"] != "recurring", j.get("at", ""), j["id"]))

    out = ws / "schedule"
    save_json(out / "jobs.json", {"generated": start.isoformat(), "timezone": tz, "jobs": jobs})
    for j in jobs:
        write_text(out / "prompts" / f"{j['id']}.txt", j["prompt"] + "\n")

    md = [f"# Scheduled tasks for {prof.get('org_name')}", "",
          f"Timezone: {tz}. Create each as a scheduled task in Claude (recurring tasks use the cron line; one-time tasks use the date and time).",
          "Each prompt is self-contained because every run starts a fresh session.", ""]
    for j in jobs:
        when = f"cron `CRON_TZ={tz} {j['cron']}` ({j['when']})" if j["type"] == "recurring" else f"once at {j['at']} {j['time']} ({tz})"
        md += [f"## {j['name']}", "", f"- Job id: `{j['id']}`", f"- Skill: `{j['skill']}`", f"- When: {when}", "", "```text", j["prompt"], "```", ""]
    write_text(out / "scheduled-task-prompts.md", "\n".join(md))

    cron_lines = ["# Tier B fallback: headless agent on a machine that stays on.", f"# Requires the Claude CLI with the {PLUGIN} plugin installed and ANTHROPIC_API_KEY set.",
                  "# cronie and most modern cron daemons honor CRON_TZ; otherwise convert times to the host timezone.", f"CRON_TZ={tz}"]
    for j in jobs:
        if j["type"] == "recurring":
            write_text(out / "prompts" / "headless" / f"{j['id']}.txt", prompt_for(j, prof, "the current working directory") + "\n")
            cron_lines.append(f"{j['cron']} cd \"$HOME/{ws.name}\" && claude -p \"$(cat schedule/prompts/headless/{j['id']}.txt)\" --allowedTools \"Read,Write,Edit,Bash(python3:*),WebSearch,WebFetch\" >> logs/{j['id']}.log 2>&1")
    cron_lines.append("# One-time jobs: use `at`, or let the weekly brief pick them up from schedule/jobs.json.")
    write_text(out / "crontab.txt", "\n".join(cron_lines) + "\n")

    for j in jobs:
        if j["type"] == "recurring":
            write_text(out / "github-actions" / f"autopilot-{j['id']}.yml", gha_for(j, prompt_for(j, prof, "the readiness/ folder in this repository"), tz, start))

    write_text(out / "readiness-calendar.ics", ics_for(jobs, tz, start))

    rec = [j for j in jobs if j["type"] == "recurring"]
    once = [j for j in jobs if j["type"] == "once"]
    end = start + dt.timedelta(days=420)
    contract_jobs = [j for j in once if j["id"].startswith("contract-")]
    items = [{"label": j["name"], "start": dt.date.fromisoformat(j["at"]), "end": dt.date.fromisoformat(j["at"]),
              "milestone": True, "status": "on_track" if "Day of" in j["name"] else ("at_risk" if j["id"].endswith("-due") else "not_started")}
             for j in once if not j["id"].startswith("contract-")]
    body = [
        tiles([
            {"label": "Recurring jobs", "value": str(len(rec)), "note": "weekly, monthly and quarterly", "tone": "info"},
            {"label": "One-time milestone jobs", "value": str(len(once)), "note": f"through {end:%b %Y}", "tone": "info"},
            {"label": "Contract reminders", "value": str(len(contract_jobs)), "note": "180/120/90/60/30 days before each notice deadline", "tone": "warn" if contract_jobs else "neutral"},
            {"label": "Fallback paths generated", "value": "4", "note": "scheduled tasks, cron, GitHub Actions, calendar", "tone": "ok"},
        ]),
        section("Recurring cadence", table(["Job", "When (" + tz + ")", "Skill", "Why"],
                                           [[j["name"], j["when"], j["skill"], j["why"]] for j in rec]),
                lead="The rhythm that keeps the plan alive between milestones."),
        section("Milestones on the calendar", gantt(items, start, end, start, width=1000, left=380),
                lead="Diamonds are one-time jobs. Grey prepares, blue confirms on the day, amber verifies an action is done. Contract reminders are listed in the contract radar."),
        section("How each job runs", table(["Tier", "Scheduler", "File"], [
            [badge("A", "ok"), "Claude scheduled tasks", "scheduled-task-prompts.md"],
            [badge("B", "info"), "cron + claude -p, or GitHub Actions", "crontab.txt, github-actions/*.yml"],
            [badge("C", "warn"), "Calendar reminders that tell the leader what to ask the agent", "readiness-calendar.ics"],
            [badge("D", "bad"), "Printed action calendar", "this page"],
        ])),
    ]
    write_text(out / "schedule.html", page(f"Schedule map: {prof.get('org_name')}", "Every job the agent will run, and when",
                                           body, meta=[f"Generated {start.isoformat()}", f"Timezone {tz}", f"Archetype {prof.get('archetype')}"]))
    print(f"Wrote {len(rec)} recurring and {len(once)} one-time jobs to {out}")


if __name__ == "__main__":
    main()
