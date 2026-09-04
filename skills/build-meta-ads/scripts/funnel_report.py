#!/usr/bin/env python3
"""Create a plain Markdown full-funnel report from normalized JSON counts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

STAGES = [
    "impressions",
    "three_second_views",
    "link_clicks",
    "landing_page_views",
    "leads",
    "qualified_or_booked",
    "attended_or_sales_call",
    "purchases_or_won",
]


def number(value):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise ValueError("Funnel counts and money values must be non-negative numbers")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--out", default="META-FUNNEL-REPORT.md")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    counts = {stage: number(data.get("counts", {}).get(stage)) for stage in STAGES}
    spend = number(data.get("spend")) or 0
    revenue = number(data.get("revenue"))
    currency = str(data.get("currency") or "[UNKNOWN]")

    lines = [
        "# Meta funnel report",
        "",
        f"- Window: {data.get('window', '[UNKNOWN]')}",
        f"- Account timezone: {data.get('account_timezone', '[UNKNOWN]')}",
        f"- Spend: {spend:,.2f} {currency}",
        f"- Verified outcome: {data.get('verified_outcome', '[UNKNOWN]')}",
        "",
        "| Stage | Count | Kept from previous available stage |",
        "|---|---:|---:|",
    ]
    previous = None
    drops = []
    for stage in STAGES:
        current = counts[stage]
        if current is None:
            continue
        kept = "-" if previous in (None, 0) else f"{current / previous:.1%}"
        lines.append(f"| {stage.replace('_', ' ').title()} | {current:,.0f} | {kept} |")
        if previous and current <= previous:
            drops.append((1 - current / previous, stage))
        previous = current

    leads = counts["leads"]
    outcomes = counts["purchases_or_won"]
    lines.extend(["", "## Economics", ""])
    lines.append(f"- Cost per lead: {spend / leads:,.2f} {currency}" if leads else "- Cost per lead: [UNKNOWN]")
    lines.append(f"- Cost per verified outcome: {spend / outcomes:,.2f} {currency}" if outcomes else "- Cost per verified outcome: [UNKNOWN]")
    if revenue is not None:
        lines.append(f"- Verified revenue: {revenue:,.2f} {currency}")
        lines.append(f"- Gross return on spend: {revenue / spend:.2f}x" if spend else "- Gross return on spend: [UNKNOWN]")
    lines.extend(["", "## Diagnosis", ""])
    if drops:
        loss, stage = max(drops)
        lines.append(f"- Largest measured adjacent-stage loss ends at **{stage.replace('_', ' ')}**: {loss:.1%} lost.")
    else:
        lines.append("- Largest measured leak: [UNKNOWN]")
    unknown = data.get("unknown_or_untrusted") or []
    lines.append("- Unknown or untrusted: " + ("; ".join(map(str, unknown)) if unknown else "none declared"))
    lines.append("- Next action: investigate the largest verified leak before changing creative, targeting or budget.")
    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote funnel report: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
