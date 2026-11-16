"""Workspace, profile and applicability logic shared by every script."""
from __future__ import annotations

import argparse
from pathlib import Path

from .report import REFERENCE, load_json, parse_date

# States not subject to the 2027 Medicaid work requirements (Morgan Lewis, Nov 2026).
NOT_SUBJECT_STATES = {"WY", "TX", "KS", "MS", "AL", "FL", "SC"}

ARCHETYPES = ["physician-group", "platform-mso", "community-hospital", "asc-imaging-infusion", "outpatient-services"]


def workspace_arg(description):
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--workspace", default="readiness", help="Readiness workspace folder (holds profile.json, inputs/, state/, outputs/)")
    p.add_argument("--today", default=None, help="Override today's date (YYYY-MM-DD) for reproducible runs")
    return p


def load_profile(ws):
    path = Path(ws) / "profile.json"
    if not path.exists():
        raise SystemExit(f"No profile.json in {ws}. Run the readiness-setup skill first (or copy templates/profile.json).")
    prof = load_json(path)
    states = set(prof.get("states", []))
    prof.setdefault("medicaid_expansion_state", bool(states - NOT_SUBJECT_STATES))
    return prof


def reference(name):
    return load_json(REFERENCE / name)


def event_applies(event, prof):
    cond = event.get("applies_if", {}) or {}
    for key, want in cond.items():
        if key == "states_any":
            if not set(want) & set(prof.get("states", [])):
                return False
        elif key == "segments_any":
            if prof.get("archetype") not in want:
                return False
        else:
            if bool(prof.get(key, False)) != bool(want):
                return False
    return True


def action_applies(action, prof):
    allowed = action.get("applies_to") or []
    return not allowed or prof.get("archetype") in allowed


def applicable_actions(prof):
    reg = reference("action-register.json")
    return [a for a in reg["actions"] if action_applies(a, prof)]


def applicable_events(prof):
    cal = reference("regulatory-calendar.json")
    evs = [e for e in cal["events"] if event_applies(e, prof)]
    for e in evs:
        e["_date"] = parse_date(e["date"])
    return sorted(evs, key=lambda e: e["_date"])


def dependency_applies(dep, prof):
    return all(bool(prof.get(k, False)) == bool(v) for k, v in (dep.get("applies_if") or {}).items())


def dependency_tiers(prof, include_na=False):
    """Current tier per dependency from the profile, defaulting to D (public default).
    Dependencies that do not apply to this organization (for example hospital outpatient data
    for a physician group) are left out, or returned as None when include_na is set."""
    deps = reference("dependencies.json")["dependencies"]
    tiers = prof.get("data_tiers", {})
    out = {}
    for d in deps:
        if dependency_applies(d, prof):
            out[d["id"]] = tiers.get(d["id"], "D")
        elif include_na:
            out[d["id"]] = None
    return out


GRADE_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}


def weakest(grades):
    grades = [g for g in grades if g]
    return max(grades, key=lambda g: GRADE_ORDER[g]) if grades else "D"


def confidence_for(dep_ids, prof):
    tiers = dependency_tiers(prof, include_na=True)
    return weakest([tiers.get(d, "D") for d in dep_ids if tiers.get(d, "D") is not None])
