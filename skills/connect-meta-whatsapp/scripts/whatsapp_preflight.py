#!/usr/bin/env python3
"""Read-only WABA, phone-number and template preflight."""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone

from whatsapp_api import WhatsAppAPIError, asset_id, graph_request, required_env, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--waba", default=os.environ.get("META_WABA_ID", ""))
    parser.add_argument("--phone-number-id", default=os.environ.get("META_PHONE_NUMBER_ID", ""))
    parser.add_argument("--out", default="META-WHATSAPP-PREFLIGHT.json")
    args = parser.parse_args()
    try:
        token = required_env("META_ACCESS_TOKEN")
        version = required_env("META_GRAPH_VERSION")
        waba = asset_id(args.waba)
        phone = asset_id(args.phone_number_id)
        report = {
            "kind": "meta_whatsapp_preflight",
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "graph_version": version,
            "writes_performed": False,
            "waba_id": waba,
            "phone_number_id": phone,
            "checks": {},
        }
        report["checks"]["phone"] = graph_request(
            "GET",
            phone,
            {"fields": "id,display_phone_number,verified_name,quality_rating,name_status,code_verification_status"},
            token,
            version,
        )
        report["checks"]["templates"] = graph_request(
            "GET",
            f"{waba}/message_templates",
            {"fields": "id,name,language,status,category,quality_score", "limit": 100},
            token,
            version,
        )
        report["ready_for_controlled_test"] = bool(report["checks"]["phone"].get("display_phone_number"))
        write_json(args.out, report)
        print(f"Wrote redacted read-only preflight: {args.out}")
        return 0 if report["ready_for_controlled_test"] else 2
    except WhatsAppAPIError as exc:
        print(f"Preflight failed: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

