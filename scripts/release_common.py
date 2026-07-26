"""Shared failure type and assertion helper for release verification."""

from __future__ import annotations


class ReleaseVerificationError(ValueError):
    """Raised when a release fact is absent, malformed, or contradicted."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseVerificationError(message)
