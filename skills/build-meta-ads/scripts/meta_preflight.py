#!/usr/bin/env python3
"""Read-only Meta Ads asset and permission preflight."""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone

from meta_api import MetaAPIError, graph_request, normalized_id, required_env, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ad-account", default=os.environ.get("META_AD_ACCOUNT_ID", ""))
    parser.add_argument("--page", default=os.environ.get("META_PAGE_ID", ""))
    parser.add_argument("--pixel", default=os.environ.get("META_PIXEL_ID", ""))
    parser.add_argument("--out", default="META-ADS-PREFLIGHT.json")
    args = parser.parse_args()

    try:
        token = required_env("META_ACCESS_TOKEN")
        version = required_env("META_GRAPH_VERSION")
        account = normalized_id(args.ad_account, "act_")
        report = {
            "kind": "meta_ads_preflight",
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "graph_version": version,
            "writes_performed": False,
            "checks": {},
            "errors": [],
        }
        report["checks"]["identity"] = graph_request("GET", "me", {"fields": "id,name"}, token, version)
        report["checks"]["ad_account"] = graph_request(
            "GET",
            account,
            {"fields": "id,name,account_status,disable_reason,currency,timezone_name,amount_spent,balance"},
            token,
            version,
        )
        report["checks"]["recent_campaigns"] = graph_request(
            "GET",
            f"{account}/campaigns",
            {"fields": "id,name,status,effective_status,objective", "limit": 5},
            token,
            version,
        )
        if args.page:
            page = normalized_id(args.page)
            report["checks"]["page"] = graph_request("GET", page, {"fields": "id,name"}, token, version)
        if args.pixel:
            pixel = normalized_id(args.pixel)
            report["checks"]["pixel"] = graph_request("GET", pixel, {"fields": "id,name,last_fired_time"}, token, version)
        report["ready"] = report["checks"]["ad_account"].get("account_status") == 1
        write_json(args.out, report)
        print(f"Wrote redacted read-only preflight: {args.out}")
        return 0 if report["ready"] else 2
    except MetaAPIError as exc:
        print(f"Preflight failed: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

