#!/usr/bin/env python3
"""Coding integrity audit: find the coding shifts payers will find, before they do.

Inputs:  inputs/em_codes.csv       provider, period, code, count   (two periods: before and after AI documentation tools)
         inputs/em_benchmark.csv   code, share                     (optional; e.g. CMS public data for the specialty)
         inputs/encounters.csv     encounter_id, provider, date, code   (optional; enables the probe sample draw)
Outputs: outputs/coding/<date>-coding-audit.{html,md}, outputs/coding/<date>-probe-sample.csv when encounters exist

Flags a provider when the level 4 and 5 share of established visits rose 5 points or more, or sits
10 points above the benchmark. A flag means "be ready to explain it", not "something is wrong".
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import confidence_for, load_profile, workspace_arg  # noqa: E402
from lib.report import (Raw, badge, callout, hbars, page, pct, read_csv, section, table, tiles, today,  # noqa: E402
                        write_csv, write_text)

EST = ["99212", "99213", "99214", "99215"]
HIGH = {"99214", "99215"}
PROBE_SIZE = 30


def shares(rows):
    tot = sum(int(r["count"]) for r in rows if r["code"] in EST)
    hi = sum(int(r["count"]) for r in rows if r["code"] in HIGH)
    dist = {c: sum(int(r["count"]) for r in rows if r["code"] == c) / tot if tot else 0 for c in EST}
    return (hi / tot if tot else 0), dist, tot


def main():
    ap = workspace_arg(__doc__)
    ap.add_argument("--rise-pts", type=float, default=5.0)
    ap.add_argument("--above-benchmark-pts", type=float, default=10.0)
    ap.add_argument("--seed", type=int, default=2027)
    args = ap.parse_args()
    ws = Path(args.workspace)
    prof = load_profile(ws)
    now = today(args.today)
    rows = read_csv(ws / "inputs" / "em_codes.csv")
    periods = sorted({r["period"] for r in rows})
    if len(periods) < 2:
        raise SystemExit("Need two periods (baseline and current) in em_codes.csv")
    base_p, cur_p = periods[0], periods[-1]
    bench_path = ws / "inputs" / "em_benchmark.csv"
    bench = None
    if bench_path.exists():
        b = read_csv(bench_path)
        bench = sum(float(r["share"]) for r in b if r["code"] in HIGH)
    providers = sorted({r["provider"] for r in rows})
    results = []
    for p in providers:
        b_hi, _, b_n = shares([r for r in rows if r["provider"] == p and r["period"] == base_p])
        c_hi, c_dist, c_n = shares([r for r in rows if r["provider"] == p and r["period"] == cur_p])
        rise = (c_hi - b_hi) * 100
        reasons = []
        if rise >= args.rise_pts:
            reasons.append(f"+{rise:.1f} pts since {base_p}")
        if bench is not None and (c_hi - bench) * 100 >= args.above_benchmark_pts:
            reasons.append(f"{(c_hi - bench) * 100:.1f} pts above benchmark")
        results.append({"provider": p, "base": b_hi, "cur": c_hi, "rise": rise, "n": c_n, "flag": bool(reasons), "reasons": reasons, "dist": c_dist})
    org_b, _, _ = shares([r for r in rows if r["period"] == base_p])
    org_c, org_dist, org_n = shares([r for r in rows if r["period"] == cur_p])
    flagged = [r for r in results if r["flag"]]

    sample_note = "No inputs/encounters.csv: draw the probe sample in the PM system (30 random established visits per flagged provider from the current period)."
    enc_path = ws / "inputs" / "encounters.csv"
    if enc_path.exists():
        enc = read_csv(enc_path)
        rng = random.Random(args.seed)
        picks = []
        for r in flagged:
            pool = [e for e in enc if e["provider"] == r["provider"] and e["code"] in EST]
            picks += rng.sample(pool, min(PROBE_SIZE, len(pool)))
        write_csv(ws / "outputs" / "coding" / f"{now.isoformat()}-probe-sample.csv", picks)
        sample_note = f"Probe sample of {len(picks)} encounters written (seed {args.seed}, reproducible)."

    grade = confidence_for(["D09"], prof)
    bars = [(f"{r['provider']} ({r['base'] * 100:.0f}% before)", r["cur"] * 100) for r in sorted(results, key=lambda x: -x["cur"])]
    rows_html = [[r["provider"], pct(r["base"]), pct(r["cur"]), f"{r['rise']:+.1f}", f"{r['n']:,}",
                  badge("review" if r["flag"] else "ok", "warn" if r["flag"] else "ok"), "; ".join(r["reasons"])] for r in results]
    body = [
        tiles([
            {"label": f"Level 4 and 5 share, {cur_p}", "value": pct(org_c), "note": f"{base_p}: {pct(org_b)}", "tone": "warn" if (org_c - org_b) * 100 >= args.rise_pts else "info"},
            {"label": "Providers to review", "value": f"{len(flagged)} of {len(results)}", "note": "explainable is fine; unexplained is risk", "tone": "warn" if flagged else "ok"},
            {"label": "Benchmark (level 4 and 5)", "value": pct(bench) if bench is not None else "none", "note": "from inputs/em_benchmark.csv", "tone": "neutral"},
            {"label": "Established visits, current period", "value": f"{org_n:,}", "note": f"data confidence {grade}", "tone": "neutral"},
        ]),
        section("Level 4 and 5 share by provider, current period",
                hbars(bars, fmt=lambda v: f"{v:.0f}%", accent_labels=tuple(b[0] for b in bars if any(r["flag"] and b[0].startswith(r["provider"]) for r in results)),
                      ref=bench * 100 if bench is not None else None, ref_label="benchmark" if bench is not None else None),
                lead="Blue bars are flagged. Payers run the same comparison against their own data and the CMS public files."),
        section("Provider detail", table(["Provider", f"{base_p}", f"{cur_p}", "Change (pts)", "Visits", "Status", "Why"], rows_html)),
        section("Next steps", Raw(
            "<ol><li>Pull the probe sample: " + sample_note + "</li>"
            "<li>Have a certified coder audit each chart against the 2021 E/M guidelines (medical decision making or total time) without seeing the billed level.</li>"
            "<li>Compare audited to billed level. Many compliance teams treat 90% agreement as the bar; below it, expand the sample and involve compliance counsel.</li>"
            "<li>Check AI scribe settings: does the tool suggest a level, and do clinicians accept it unreviewed?</li>"
            "<li>Document the result. A written, dated self-audit is the best answer to a future payer inquiry.</li></ol>")),
        callout("A rise after an ambient documentation rollout can be legitimate: better capture of work that was always done. "
                "The risk is a rise nobody can explain. PwC reports 70% of health plans rank provider AI documentation tools among their top three cost drivers for 2027.", "warn"),
    ]
    out = ws / "outputs" / "coding"
    write_text(out / f"{now.isoformat()}-coding-audit.html", page("Coding integrity audit", prof.get("org_name", ""), body,
               meta=[f"As of {now.isoformat()}", f"Baseline {base_p}, current {cur_p}", f"Data confidence {grade}"],
               footer="Compliance support, not legal advice. Sampling for repayment estimates needs statistically valid methods; involve counsel."))
    md = [f"# Coding integrity audit, {now.isoformat()}", "", f"Level 4 and 5 share: {pct(org_b)} in {base_p}, {pct(org_c)} in {cur_p}.", "",
          "| Provider | Before | Now | Change | Flag |", "| --- | --- | --- | --- | --- |"]
    md += [f"| {r['provider']} | {pct(r['base'])} | {pct(r['cur'])} | {r['rise']:+.1f} | {'review' if r['flag'] else 'ok'} |" for r in results]
    write_text(out / f"{now.isoformat()}-coding-audit.md", "\n".join(md) + "\n")
    print(f"{len(flagged)} of {len(results)} providers flagged; org level 4/5 share {pct(org_b)} -> {pct(org_c)}")


if __name__ == "__main__":
    main()
