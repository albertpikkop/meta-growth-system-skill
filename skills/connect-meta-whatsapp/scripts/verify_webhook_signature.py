#!/usr/bin/env python3
"""Verify a Meta X-Hub-Signature-256 against an exact raw body file."""

from __future__ import annotations

import argparse
import hashlib
import hmac

from whatsapp_api import WhatsAppAPIError, required_env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("body_file")
    parser.add_argument("signature", help="Full sha256=... header value")
    args = parser.parse_args()
    try:
        secret = required_env("META_APP_SECRET").encode("utf-8")
        body = open(args.body_file, "rb").read()
        expected = "sha256=" + hmac.new(secret, body, hashlib.sha256).hexdigest()
        valid = hmac.compare_digest(expected, args.signature.strip())
        print("VALID" if valid else "INVALID")
        return 0 if valid else 2
    except (OSError, WhatsAppAPIError) as exc:
        print(f"Verification failed: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

