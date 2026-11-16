#!/usr/bin/env python3
"""Regenerate the reference guides from the JSON source of truth, so docs never drift from data.

  python3 docs/tools/build_reference_docs.py
Writes docs/guides/03-data-dependencies.md, 05-skill-reference.md, 08-regulatory-calendar.md
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "reference"
GUIDES = ROOT / "docs" / "guides"


def load(name):
    return json.loads((REF / name).read_text())


def deps_doc():
    d = load("dependencies.json")
    out = ["# Data dependencies and fallback chains", "",
           "Generated from `reference/dependencies.json`. Every input the program uses has four tiers. Skills use the best tier available, never stop because tier A is missing, and label every number with the grade of its weakest input.", "",
           "| Tier | Name | Confidence | Meaning |", "| --- | --- | --- | --- |"]
    for k, v in d["tiers"].items():
        out.append(f"| {k} | {v['name']} | {v['confidence']} | {v['meaning']} |")
    out.append("")
    for dep in d["dependencies"]:
        crit = " (critical)" if dep["critical"] else ""
        cond = ""
        if dep.get("applies_if"):
            cond = " Applies only when " + ", ".join(f"`{k}` is {str(v).lower()}" for k, v in dep["applies_if"].items()) + "."
        out += [f"## {dep['id']} {dep['name']}{crit}", "",
                f"Used by: {', '.join('`' + u + '`' for u in dep['used_by'])}. Fields: {', '.join(dep['fields'])}.{cond}", "",
                "| Tier | How to get it |", "| --- | --- |"]
        for t in "ABCD":
            out.append(f"| {t} | {dep['tiers'][t]} |")
        out += ["", f"Validation: {dep['validation']}", ""]
    (GUIDES / "03-data-dependencies.md").write_text("\n".join(out) + "\n")


def skills_doc():
    reg = load("action-register.json")
    cat = load("schedule-catalog.json")
    by_skill_actions = {}
    for a in reg["actions"]:
        by_skill_actions.setdefault(a["skill"], []).append(f"{a['id']} (due {a['due'] if a['due'][:4].isdigit() else 'before any deal'})")
    by_skill_jobs = {}
    for j in cat["recurring"]:
        by_skill_jobs.setdefault(j["skill"], []).append(j["name"])
    rows = []
    for sk in sorted((ROOT / "skills").iterdir()):
        text = (sk / "SKILL.md").read_text()
        desc = re.search(r"^description: (.*)$", text, re.M).group(1)
        what = desc.split(" Use when")[0]
        when = desc.split(" Use when")[1] if " Use when" in desc else ""
        scripts = sorted(set(re.findall(r"scripts/([a-z_]+\.py)", text)))
        rows.append((sk.name, what, when.strip(), ", ".join(by_skill_actions.get(sk.name, [])) or "recurring",
                     ", ".join(by_skill_jobs.get(sk.name, [])) or "on demand or milestone jobs",
                     ", ".join(f"`{s}`" for s in scripts) or "none"))
    out = ["# Skill reference", "", "Generated from each `skills/*/SKILL.md` and the action register. Ask for any skill by name or with the phrases in the second column.", ""]
    for name, what, when, acts, jobs, scr in rows:
        out += [f"## `{name}`", "", what, "", f"- **Ask for it when** {when}" if when else "", f"- **Actions:** {acts}", f"- **Scheduled as:** {jobs}", f"- **Engine scripts:** {scr}", ""]
    (GUIDES / "05-skill-reference.md").write_text("\n".join(x for x in out if x is not None) + "\n")


def calendar_doc():
    cal = load("regulatory-calendar.json")
    out = ["# Regulatory calendar", "", f"Generated from `reference/regulatory-calendar.json` (as of {cal['as_of']}). {cal['note']}", "",
           "| Date | Event | Status | Applies when | Lead days | Source |", "| --- | --- | --- | --- | --- | --- |"]
    for e in cal["events"]:
        date = e["date"] + (f" to {e['end_date']}" if e.get("end_date") else "")
        cond = ", ".join(f"{k}={v}" for k, v in e.get("applies_if", {}).items()) or "everyone"
        out.append(f"| {date} | **{e['title']}**. {e['detail']} | {e['status']} | {cond} | {e['lead_days']} | [{e['source']['name']}]({e['source']['url']}) |")
    (GUIDES / "08-regulatory-calendar.md").write_text("\n".join(out) + "\n")


if __name__ == "__main__":
    GUIDES.mkdir(parents=True, exist_ok=True)
    deps_doc()
    skills_doc()
    calendar_doc()
    print("Reference guides regenerated")
