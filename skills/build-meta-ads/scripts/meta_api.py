#!/usr/bin/env python3
"""Small dependency-free Meta Graph API helper. Never logs tokens."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


class MetaAPIError(RuntimeError):
    pass


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise MetaAPIError(f"Missing required environment variable: {name}")
    return value


def normalized_id(value: str, prefix: str = "") -> str:
    result = value.strip()
    if prefix and result and not result.startswith(prefix):
        result = prefix + result
    if not result or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for ch in result):
        raise MetaAPIError("An asset ID is missing or contains unexpected characters")
    return result


def graph_request(method: str, path: str, params: dict[str, Any], token: str, version: str) -> dict[str, Any]:
    clean_version = version.strip().lstrip("/")
    if not clean_version.startswith("v"):
        raise MetaAPIError("META_GRAPH_VERSION must look like v23.0")
    url = f"https://graph.facebook.com/{clean_version}/{path.lstrip('/')}"
    body_params = dict(params)
    body_params["access_token"] = token
    encoded = urllib.parse.urlencode(
        {key: json.dumps(value, separators=(",", ":")) if isinstance(value, (dict, list)) else value for key, value in body_params.items()}
    ).encode("utf-8")
    if method.upper() == "GET":
        request = urllib.request.Request(url + "?" + encoded.decode("utf-8"), method="GET")
    else:
        request = urllib.request.Request(url, data=encoded, method=method.upper())
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(raw).get("error", {})
            message = detail.get("message", "Meta API request failed")
            code = detail.get("code", exc.code)
        except json.JSONDecodeError:
            message, code = "Meta API request failed", exc.code
        raise MetaAPIError(f"Meta API error {code}: {message}") from exc


def write_json(path: str, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

