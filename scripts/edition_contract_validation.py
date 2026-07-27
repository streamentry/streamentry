"""Strict JSON primitives used by the publication edition contract."""

from __future__ import annotations

import json
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


class EditionContractError(ValueError):
    """Raised when the canonical edition contract is incomplete or ambiguous."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise EditionContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
    except (OSError, json.JSONDecodeError) as error:
        raise EditionContractError(
            f"cannot load edition contract {path}: {error}"
        ) from error
    if not isinstance(value, dict):
        raise EditionContractError("edition must be an object")
    return value


def exact_object(
    value: Any,
    path: str,
    expected_keys: set[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EditionContractError(f"{path} must be an object")
    actual_keys = set(value)
    missing = sorted(expected_keys - actual_keys)
    unknown = sorted(actual_keys - expected_keys)
    if missing:
        raise EditionContractError(f"{path} is missing keys: {missing}")
    if unknown:
        raise EditionContractError(f"{path} has unknown keys: {unknown}")
    return value


def nonempty_text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value:
        raise EditionContractError(f"{path} must be a non-empty string")
    if value != value.strip():
        raise EditionContractError(f"{path} must not have surrounding whitespace")
    if any(character in value for character in "\r\n\t"):
        raise EditionContractError(f"{path} must be a single-line string")
    if unicodedata.normalize("NFC", value) != value:
        raise EditionContractError(f"{path} must use NFC Unicode normalization")
    return value


def nonempty_text_array(value: Any, path: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise EditionContractError(f"{path} must be a non-empty array")
    items = tuple(
        nonempty_text(item, f"{path}[{index}]")
        for index, item in enumerate(value)
    )
    if len(items) != len(set(items)):
        raise EditionContractError(f"{path} must not contain duplicate values")
    return items


def require_https_url(value: str, path: str) -> None:
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        parsed.port
    except ValueError as error:
        raise EditionContractError(f"{path} must be an absolute HTTPS URL") from error
    if (
        parsed.scheme != "https"
        or not hostname
        or parsed.username is not None
        or parsed.password is not None
        or any(character.isspace() for character in parsed.netloc)
    ):
        raise EditionContractError(f"{path} must be an absolute HTTPS URL")


def require_matching_utc_instant(epoch: str, modified: str) -> None:
    try:
        timestamp_as_utc = datetime.fromtimestamp(
            int(epoch),
            timezone.utc,
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (OverflowError, OSError, ValueError) as error:
        raise EditionContractError(
            "edition.publication.pdf_creation_timestamp is outside the supported range"
        ) from error
    if timestamp_as_utc != modified:
        raise EditionContractError(
            "PDF creation timestamp and EPUB modified time must identify one instant"
        )
