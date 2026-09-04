#!/usr/bin/env python3
"""Dry-run or send one approved template to one explicitly owned test number."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from whatsapp_api import WhatsAppAPIError, asset_id, graph_request, required_env, write_json

APPROVAL = "TEST_RECIPIENT_ONLY"


def normalize_phone(value: str) -> str:
    phone = re.sub(r"\D", "", value)
    if len(phone) < 8 or len(phone) > 15:
        raise WhatsAppAPIError("Recipient must be a valid international phone number")
    return phone


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", default="META-WHATSAPP-TEST-RECEIPT.json")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm", default="")
    args = parser.parse_args()
    try:
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))
        phone_number_id = asset_id(str(config.get("phone_number_id", "")))
        recipient = normalize_phone(str(config.get("recipient", "")))
        template = config.get("template") or {}
        if not config.get("operation_id") or not template.get("name") or not template.get("language"):
            raise WhatsAppAPIError("operation_id, template name and template language are required")
        receipt = {
            "kind": "meta_whatsapp_test",
            "operation_id": config["operation_id"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "phone_number_id": phone_number_id,
            "recipient_ending": recipient[-4:],
            "template": {"name": template["name"], "language": template["language"]},
            "applied": False,
            "delivery_state": "not_sent",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "template",
            "template": {
                "name": template["name"],
                "language": {"code": template["language"]},
                "components": template.get("components", []),
            },
        }
        if not args.apply:
            receipt["dry_run"] = True
            receipt["payload_redacted"] = {**payload, "to": "***" + recipient[-4:]}
            write_json(args.out, receipt)
            print(f"Dry run only. Wrote test plan: {args.out}")
            return 0
        if args.confirm != APPROVAL or config.get("recipient_is_owned_test_number") is not True:
            raise WhatsAppAPIError(f"Send blocked. Mark the owned test number true and pass --confirm {APPROVAL} after explicit approval")
        token = required_env("META_ACCESS_TOKEN")
        version = required_env("META_GRAPH_VERSION")
        result = graph_request("POST", f"{phone_number_id}/messages", payload, token, version)
        messages = result.get("messages") or []
        message_id = messages[0].get("id") if messages else ""
        if not message_id:
            raise WhatsAppAPIError("Meta returned no WhatsApp message ID; the send is not accepted")
        receipt.update({"applied": True, "dry_run": False, "accepted_message_id": message_id, "delivery_state": "accepted"})
        write_json(args.out, receipt)
        print(f"Accepted by Meta; delivery is not yet proven. Receipt: {args.out}")
        return 0
    except (OSError, json.JSONDecodeError, WhatsAppAPIError) as exc:
        print(f"Test send failed: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
