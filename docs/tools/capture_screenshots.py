#!/usr/bin/env python3
"""Capture the documentation screenshots from the example outputs (requires: pip install playwright; playwright install chromium).

  python3 docs/tools/capture_screenshots.py
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
SHOTS = [
    ("examples/sample-org/outputs/briefs/2026-11-16-weekly-brief.html", "01-weekly-brief.png"),
    ("examples/sample-org/schedule/schedule.html", "02-schedule-map.png"),
    ("examples/sample-org/outputs/data/2026-11-16-data-readiness.html", "03-data-readiness.png"),
    ("examples/sample-org/outputs/model/downside-case.html", "04-downside-case.png"),
    ("examples/sample-org/outputs/tracker/2026-11-16-tracker.html", "05-action-tracker.png"),
    ("examples/sample-org/outputs/kpi/2026-11-16-kpi-pulse.html", "06-kpi-pulse.png"),
    ("examples/sample-org/outputs/contracts/2026-11-16-contract-radar.html", "07-contract-radar.png"),
    ("examples/sample-org/outputs/coding/2026-11-16-coding-audit.html", "08-coding-audit.png"),
    ("examples/sample-org/outputs/deals/2026-11-16-deal-timeline.html", "09-deal-timeline.png"),
    ("examples/sample-org/outputs/site/2026-11-16-site-of-care.html", "10-site-of-care.png"),
    ("examples/sample-hospital/outputs/financing/2026-11-16-financing-cliff.html", "11-financing-cliff.png"),
]


def main():
    out = ROOT / "docs" / "screenshots"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome")
        except Exception:
            browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1180, "height": 900}, device_scale_factor=2)
        for src, name in SHOTS:
            page.goto((ROOT / src).as_uri())
            page.wait_for_timeout(150)
            page.screenshot(path=str(out / name), full_page=True)
            print("captured", name)
        browser.close()


if __name__ == "__main__":
    main()
