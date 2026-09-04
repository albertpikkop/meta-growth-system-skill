#!/usr/bin/env python3
"""Dry-run or create one campaign, ad set and optional ad, all PAUSED."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from meta_api import MetaAPIError, graph_request, normalized_id, required_env, write_json

APPROVAL = "I_APPROVE_PAUSED_META_BUILD"


def load_config(path: str) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    required = ["operation_id", "ad_account_id", "campaign", "adset", "business_outcome"]
    missing = [key for key in required if not payload.get(key)]
    if missing:
        raise MetaAPIError("Missing configuration keys: " + ", ".join(missing))
    budget = payload["adset"].get("daily_budget_minor")
    if not isinstance(budget, int) or budget <= 0:
        raise MetaAPIError("daily_budget_minor must be a positive integer in the account's minor currency unit")
    return payload


def validate(config: dict) -> None:
    normalized_id(config["ad_account_id"], "act_")
    for section, key in [("campaign", "name"), ("campaign", "objective"), ("adset", "name"), ("adset", "optimization_goal")]:
        if not str(config[section].get(key, "")).strip():
            raise MetaAPIError(f"Missing {section}.{key}")
    if not config["business_outcome"].get("name") or not config["business_outcome"].get("system_of_record"):
        raise MetaAPIError("A verified business outcome and system of record are required")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", default="META-PAUSED-BUILD-RECEIPT.json")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm", default="")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        validate(config)
        account = normalized_id(config["ad_account_id"], "act_")
        receipt = {
            "kind": "meta_paused_build",
            "operation_id": config["operation_id"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "ad_account_id": account,
            "requested_daily_budget_minor": config["adset"]["daily_budget_minor"],
            "status_required": "PAUSED",
            "applied": False,
            "objects": [],
            "business_outcome": config["business_outcome"],
        }
        if not args.apply:
            receipt["dry_run"] = True
            receipt["plan"] = config
            write_json(args.out, receipt)
            print(f"Dry run only. Wrote plan receipt: {args.out}")
            return 0
        if args.confirm != APPROVAL:
            raise MetaAPIError(f"Apply blocked. Pass --confirm {APPROVAL} only after explicit user approval")

        token = required_env("META_ACCESS_TOKEN")
        version = required_env("META_GRAPH_VERSION")
        campaign = config["campaign"]
        created_campaign = graph_request(
            "POST",
            f"{account}/campaigns",
            {
                "name": campaign["name"],
                "objective": campaign["objective"],
                "special_ad_categories": campaign.get("special_ad_categories", []),
                "status": "PAUSED",
            },
            token,
            version,
        )
        campaign_id = normalized_id(created_campaign.get("id", ""))
        receipt["objects"].append({"type": "campaign", "id": campaign_id, "status": "PAUSED"})
        write_json(args.out, receipt)

        adset = config["adset"]
        params = {
            "campaign_id": campaign_id,
            "name": adset["name"],
            "daily_budget": adset["daily_budget_minor"],
            "billing_event": adset.get("billing_event", "IMPRESSIONS"),
            "optimization_goal": adset["optimization_goal"],
            "bid_strategy": adset.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
            "targeting": adset["targeting"],
            "status": "PAUSED",
        }
        if adset.get("promoted_object"):
            params["promoted_object"] = adset["promoted_object"]
        for optional in ("start_time", "end_time"):
            if adset.get(optional):
                params[optional] = adset[optional]
        created_adset = graph_request("POST", f"{account}/adsets", params, token, version)
        adset_id = normalized_id(created_adset.get("id", ""))
        receipt["objects"].append({"type": "adset", "id": adset_id, "status": "PAUSED"})
        write_json(args.out, receipt)

        ad = config.get("ad") or {}
        if ad.get("creative_id"):
            created_ad = graph_request(
                "POST",
                f"{account}/ads",
                {
                    "name": ad["name"],
                    "adset_id": adset_id,
                    "creative": {"creative_id": normalized_id(ad["creative_id"])},
                    "status": "PAUSED",
                },
                token,
                version,
            )
            receipt["objects"].append({"type": "ad", "id": normalized_id(created_ad.get("id", "")), "status": "PAUSED"})

        for item in receipt["objects"]:
            current = graph_request("GET", item["id"], {"fields": "id,name,status,effective_status"}, token, version)
            item["read_back"] = current
            if current.get("status") != "PAUSED":
                raise MetaAPIError(f"Fail closed: {item['type']} {item['id']} did not read back PAUSED")
        receipt["applied"] = True
        receipt["dry_run"] = False
        write_json(args.out, receipt)
        print(f"Created and verified paused objects. Receipt: {args.out}")
        return 0
    except (MetaAPIError, OSError, json.JSONDecodeError) as exc:
        print(f"Paused build failed: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

