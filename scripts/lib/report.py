"""Shared helpers for the autopilot scripts: JSON/CSV IO and self-contained HTML reports.

Standard library only, so every script runs anywhere Python 3.9+ runs:
a laptop, a cron host, a GitHub Actions runner or an agent sandbox.
"""
from __future__ import annotations

import csv
import datetime as dt
import html
import json
import os
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
REFERENCE = PLUGIN_ROOT / "reference"

# ---------------------------------------------------------------- IO helpers

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
        f.write("\n")


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [{k.strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


def write_csv(path, rows, headers=None):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    headers = headers or (list(rows[0].keys()) if rows else [])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in headers})


def write_text(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def parse_date(s):
    return dt.date.fromisoformat(str(s)[:10])


def today(override=None):
    """Honor AUTOPILOT_TODAY so examples and tests render the same every time."""
    value = override or os.environ.get("AUTOPILOT_TODAY")
    return parse_date(value) if value else dt.date.today()


def money(x, digits=0):
    sign = "-" if x < 0 else ""
    x = abs(x)
    if x >= 1_000_000:
        return f"{sign}${x / 1_000_000:,.{max(digits, 1)}f}M"
    if x >= 10_000:
        return f"{sign}${x / 1_000:,.0f}K"
    return f"{sign}${x:,.{digits}f}"


def pct(x, digits=1):
    return f"{x * 100:.{digits}f}%"


# ---------------------------------------------------------------- HTML building blocks

class Raw(str):
    """Marks a string as trusted HTML so table() will not escape it."""


def esc(x):
    return x if isinstance(x, Raw) else html.escape(str(x))


TONES = {
    "ok": ("#e6f4ea", "#1e6b3a"),
    "warn": ("#fff4dc", "#8a5a00"),
    "bad": ("#fde8e6", "#a3241a"),
    "info": ("#e8f0fb", "#1f4e8c"),
    "neutral": ("#eef0f3", "#3b4350"),
}

GRADE_TONE = {"A": "ok", "B": "info", "C": "warn", "D": "bad"}
GRADE_LABEL = {"A": "A live", "B": "B export", "C": "C estimate", "D": "D public default"}


def badge(text, tone="neutral"):
    bg, fg = TONES.get(tone, TONES["neutral"])
    return Raw(f'<span class="badge" style="background:{bg};color:{fg}">{esc(text)}</span>')


def grade_badge(grade):
    return badge(GRADE_LABEL.get(grade, grade), GRADE_TONE.get(grade, "neutral"))


def tiles(items):
    out = ['<div class="tiles">']
    for it in items:
        bg, fg = TONES.get(it.get("tone", "neutral"), TONES["neutral"])
        out.append(
            f'<div class="tile" style="border-top:4px solid {fg}">'
            f'<div class="tile-label">{esc(it["label"])}</div>'
            f'<div class="tile-value" style="color:{fg}">{esc(it["value"])}</div>'
            f'<div class="tile-note">{esc(it.get("note", ""))}</div></div>'
        )
    out.append("</div>")
    return Raw("".join(out))


def _cell(c):
    if not isinstance(c, Raw) and isinstance(c, str) and len(c) <= 30 and c[:4].isdigit() and c[4:5] == "-":
        return f'<span style="white-space:nowrap">{esc(c)}</span>'
    return esc(c)


def table(headers, rows, cls=""):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{_cell(c)}</td>" for c in r) + "</tr>" for r in rows)
    return Raw(f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>')


def section(title, *parts, lead=None):
    inner = "".join(str(p) for p in parts)
    lead_html = f'<p class="lead">{esc(lead)}</p>' if lead else ""
    return Raw(f'<section><h2>{esc(title)}</h2>{lead_html}{inner}</section>')


def callout(text, tone="info"):
    bg, fg = TONES.get(tone, TONES["info"])
    return Raw(f'<div class="callout" style="background:{bg};border-left:4px solid {fg}">{esc(text)}</div>')


# ---------------------------------------------------------------- SVG charts

INK = "#1b2430"
QUIET = "#6b7685"
GRID = "#e3e7ed"
ACCENT = "#1f6feb"
GOOD = "#2f9e5b"
BAD = "#d9483b"
WARN = "#e0a020"


def hbars(rows, fmt=lambda v: f"{v:,.0f}", width=720, accent_labels=(), ref=None, ref_label=None):
    """rows: list of (label, value). Bars from zero; accent on labels in accent_labels."""
    if not rows:
        return Raw("")
    left, right, bar_h, gap = 230, 90, 22, 10
    h = len(rows) * (bar_h + gap) + 30
    vmax = max([abs(v) for _, v in rows] + ([abs(ref)] if ref else [])) or 1
    scale = (width - left - right) / vmax
    out = [f'<svg viewBox="0 0 {width} {h}" class="chart" role="img">']
    if ref is not None:
        x = left + ref * scale
        out.append(f'<line x1="{x}" x2="{x}" y1="4" y2="{h - 20}" stroke="{QUIET}" stroke-dasharray="4 4"/>')
        if ref_label:
            out.append(f'<text x="{x + 4}" y="{h - 6}" font-size="11" fill="{QUIET}">{esc(ref_label)}</text>')
    for i, (label, v) in enumerate(rows):
        y = 8 + i * (bar_h + gap)
        color = ACCENT if label in accent_labels else "#9aa6b5"
        w = max(abs(v) * scale, 1)
        out.append(f'<text x="{left - 10}" y="{y + bar_h * 0.7}" text-anchor="end" font-size="13" fill="{INK}">{esc(label)}</text>')
        out.append(f'<rect x="{left}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="4" fill="{color}"/>')
        out.append(f'<text x="{left + w + 8}" y="{y + bar_h * 0.7}" font-size="12" fill="{INK}">{esc(fmt(v))}</text>')
    out.append("</svg>")
    return Raw("".join(out))


def waterfall(start_label, start, steps, end_label, width=760, height=340, fmt=money):
    """steps: list of (label, delta). Green increases, red decreases, grey totals."""
    labels = [start_label] + [s[0] for s in steps] + [end_label]
    n = len(labels)
    left, right, top_pad, bottom = 20, 20, 30, 70
    plot_h = height - top_pad - bottom
    running = start
    levels = [start]
    for _, d in steps:
        running += d
        levels.append(running)
    truncated = min(levels) > 0.6 * max(levels)
    lo = min(levels) * 0.96 if truncated else 0
    hi = max(levels) * 1.01
    span = (hi - lo) or 1
    y = lambda v: top_pad + (hi - v) / span * plot_h
    colw = (width - left - right) / n
    bw = colw * 0.62
    out = [f'<svg viewBox="0 0 {width} {height}" class="chart" role="img">']
    out.append(f'<line x1="{left}" x2="{width - right}" y1="{top_pad + plot_h}" y2="{top_pad + plot_h}" stroke="{GRID}"/>')
    prev = start
    for i, label in enumerate(labels):
        x = left + i * colw + (colw - bw) / 2
        if i == 0 or i == n - 1:
            v = start if i == 0 else running
            y0, y1 = y(v), y(lo)
            color, txt = "#8d99a8", fmt(v)
        else:
            d = steps[i - 1][1]
            a, b = prev, prev + d
            y0, y1 = y(max(a, b)), y(min(a, b))
            color = GOOD if d >= 0 else BAD
            txt = ("+" if d >= 0 else "") + fmt(d)
            prev = b
        out.append(f'<rect x="{x:.1f}" y="{y0:.1f}" width="{bw:.1f}" height="{max(y1 - y0, 1.5):.1f}" rx="3" fill="{color}" opacity="0.9"/>')
        if truncated and (i == 0 or i == n - 1):
            yb = y(lo) - 14
            out.append(f'<path d="M{x - 2:.1f} {yb + 4:.1f} L{x + bw + 2:.1f} {yb - 4:.1f} M{x - 2:.1f} {yb + 10:.1f} L{x + bw + 2:.1f} {yb + 2:.1f}" stroke="#ffffff" stroke-width="3"/>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{y0 - 6:.1f}" text-anchor="middle" font-size="12" fill="{INK}">{esc(txt)}</text>')
        words = label.split(" ")
        lines, cur = [], ""
        for w in words:
            if len(cur + " " + w) > 14 and cur:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for j, ln in enumerate(lines[:3]):
            out.append(f'<text x="{x + bw / 2:.1f}" y="{top_pad + plot_h + 18 + j * 14}" text-anchor="middle" font-size="11.5" fill="{QUIET}">{esc(ln)}</text>')
    note = "green raises, red lowers; axis broken on the totals to show the steps" if truncated else "green raises, red lowers; axis starts at zero"
    out.append(f'<text x="{width - right}" y="16" text-anchor="end" font-size="11" fill="{QUIET}">{note}</text>')
    out.append("</svg>")
    return Raw("".join(out))


STATUS_COLOR = {"done": GOOD, "on_track": ACCENT, "at_risk": WARN, "late": BAD, "blocked": BAD, "not_started": "#9aa6b5", "n/a": "#c8ced6"}


def gantt(items, start, end, today_date, width=900, left=300):
    """items: dicts with label, start, end, status, milestone(bool). Labels are trimmed to fit the left column."""
    right, row_h = 30, 30
    max_chars = int((left - 16) / 6.9)
    top_pad = 40
    h = top_pad + len(items) * row_h + 20
    span = (end - start).days or 1
    X = lambda d: left + (d - start).days / span * (width - left - right)
    out = [f'<svg viewBox="0 0 {width} {h}" class="chart" role="img">']
    months = (end.year - start.year) * 12 + end.month - start.month + 1
    step = 1 if months <= 12 else (2 if months <= 24 else 3)
    m = dt.date(start.year, start.month, 1)
    i = 0
    while m <= end:
        x = X(m)
        if x >= left:
            out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{top_pad - 8}" y2="{h - 10}" stroke="{GRID}"/>')
            if i % step == 0:
                out.append(f'<text x="{x + 3:.1f}" y="{top_pad - 14}" font-size="11" fill="{QUIET}">{m.strftime("%b %Y")}</text>')
            i += 1
        m = dt.date(m.year + (m.month // 12), m.month % 12 + 1, 1)
    tx = X(today_date)
    out.append(f'<line x1="{tx:.1f}" x2="{tx:.1f}" y1="{top_pad - 8}" y2="{h - 10}" stroke="{ACCENT}" stroke-dasharray="4 4"/>')
    out.append(f'<text x="{tx + 4:.1f}" y="{h - 2}" font-size="11" fill="{ACCENT}">today</text>')
    for i, it in enumerate(items):
        y = top_pad + i * row_h
        color = STATUS_COLOR.get(it.get("status", "not_started"), "#9aa6b5")
        label = it["label"] if len(it["label"]) <= max_chars else it["label"][: max_chars - 3].rstrip() + "..."
        out.append(f'<text x="{left - 10}" y="{y + 18}" text-anchor="end" font-size="12.5" fill="{INK}">{esc(label)}</text>')
        s, e = max(it["start"], start), min(it["end"], end)
        if it.get("milestone"):
            cx = X(e)
            out.append(f'<path d="M{cx:.1f} {y + 6}l8 8l-8 8l-8 -8z" fill="{color}"/>')
        else:
            out.append(f'<rect x="{X(s):.1f}" y="{y + 7}" width="{max(X(e) - X(s), 4):.1f}" height="16" rx="8" fill="{color}" opacity="0.85"/>')
    out.append("</svg>")
    return Raw("".join(out))


def timeline(events, start, end, today_date, width=900):
    """events: dicts with date, label, tone. One row per event, sorted by date."""
    items = [{"label": e["label"], "start": e["date"], "end": e["date"], "status": e.get("status", "on_track"), "milestone": True} for e in events]
    return gantt(items, start, end, today_date, width)


# ---------------------------------------------------------------- page shell

CSS = """
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;color:#1b2430;background:#f6f7f9;line-height:1.45}
.wrap{max-width:1040px;margin:0 auto;padding:28px 32px 48px}
header{background:#0f2238;color:#fff;padding:22px 32px}
header .kicker{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#9fb6d3}
header h1{margin:4px 0 2px;font-size:24px;font-weight:650}
header .sub{color:#c9d6e6;font-size:14px}
.meta{display:flex;gap:18px;flex-wrap:wrap;font-size:12px;color:#c9d6e6;margin-top:10px}
section{background:#fff;border:1px solid #e3e7ed;border-radius:10px;padding:18px 22px;margin:18px 0}
h2{font-size:17px;margin:0 0 8px}
.lead{margin:0 0 12px;color:#3b4350}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:6px 0}
.tile{background:#fff;border:1px solid #e3e7ed;border-radius:8px;padding:12px 14px}
.tile-label{font-size:12px;color:#6b7685}.tile-value{font-size:24px;font-weight:650;margin:2px 0}.tile-note{font-size:12px;color:#6b7685}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;font-weight:600;color:#3b4350;border-bottom:2px solid #e3e7ed;padding:7px 8px;background:#fafbfc}
td{border-bottom:1px solid #eef0f3;padding:7px 8px;vertical-align:top}
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11.5px;font-weight:600;line-height:1.35}
section{overflow-x:auto}
.notes td:last-child{min-width:280px}
.notes td:first-child{min-width:130px}
.callout{padding:10px 14px;border-radius:6px;margin:10px 0;font-size:13.5px}
.chart{width:100%;height:auto;display:block;margin:6px 0}
footer{font-size:11.5px;color:#6b7685;margin-top:18px}
ul{margin:6px 0 6px 18px;padding:0}li{margin:3px 0}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
"""


def page(title, subtitle, body_parts, kicker="Healthcare 2027 Autopilot", meta=None, footer=None):
    meta_html = "".join(f"<span>{esc(m)}</span>" for m in (meta or []))
    body = "".join(str(p) for p in body_parts)
    foot = f"<footer>{esc(footer)}</footer>" if footer else ""
    return (
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{esc(title)}</title><style>{CSS}</style></head><body>"
        f"<header><div class='kicker'>{esc(kicker)}</div><h1>{esc(title)}</h1>"
        f"<div class='sub'>{esc(subtitle)}</div><div class='meta'>{meta_html}</div></header>"
        f"<div class='wrap'>{body}{foot}</div></body></html>"
    )
