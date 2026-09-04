#!/usr/bin/env python3
"""Small dependency-free WhatsApp Cloud API helper. Never logs tokens."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


class WhatsAppAPIError(RuntimeError):
    pass


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise WhatsAppAPIError(f"Missing required environment variable: {name}")
    return value


def asset_id(value: str) -> str:
    value = value.strip()
    if not value or not value.isdigit():
        raise WhatsAppAPIError("A WhatsApp asset ID is missing or invalid")
    return value


def graph_request(method: str, path: str, params: dict[str, Any], token: str, version: str) -> dict[str, Any]:
    clean_version = version.strip().lstrip("/")
    if not clean_version.startswith("v"):
        raise WhatsAppAPIError("META_GRAPH_VERSION must look like v23.0")
    url = f"https://graph.facebook.com/{clean_version}/{path.lstrip('/')}"
    headers = {"Authorization": f"Bearer {token}"}
    if method.upper() == "GET":
        query = urllib.parse.urlencode(params)
        request = urllib.request.Request(url + ("?" + query if query else ""), headers=headers, method="GET")
    else:
        headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=json.dumps(params).encode("utf-8"), headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(raw).get("error", {})
            message = detail.get("message", "WhatsApp API request failed")
            code = detail.get("code", exc.code)
        except json.JSONDecodeError:
            message, code = "WhatsApp API request failed", exc.code
        raise WhatsAppAPIError(f"Meta API error {code}: {message}") from exc


def write_json(path: str, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

