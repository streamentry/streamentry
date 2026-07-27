"""Validate registry files, fingerprints, and local Markdown links."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from release_common import ReleaseVerificationError, require


EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:\+?\d[\d .()-]{7,}\d)(?![A-Za-z0-9])"
)
PUBLIC_EVIDENCE_HASH_FIELDS = {
    "Candidate commit",
    "PDF SHA-256",
    "EPUB SHA-256",
    "Manifest SHA-256",
    "Counted record SHA-256",
}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ReleaseVerificationError(
                f"external release registry has duplicate key: {key}"
            )
        value[key] = item
    return value


def load_registry(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
    except json.JSONDecodeError as error:
        raise ReleaseVerificationError(
            f"external release registry is invalid JSON: {error.msg}"
        ) from error
    require(
        isinstance(value, dict),
        "external release registry must be one JSON object",
    )
    return value


def exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    require(
        actual == expected,
        f"{label} keys differ: missing={sorted(expected - actual)}, "
        f"unexpected={sorted(actual - expected)}",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_file(root: Path, relative: str, label: str) -> Path:
    path = Path(relative)
    require(
        not path.is_absolute() and ".." not in path.parts,
        f"{label} must be a safe repository-relative path",
    )
    candidate = root / path
    require(not candidate.is_symlink(), f"{label} must not be a symlink")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as error:
        raise ReleaseVerificationError(
            f"{label} must resolve to a file inside the repository"
        ) from error
    require(resolved.is_file(), f"{label} must resolve to a regular file")
    return resolved


def _validate_local_markdown_links(
    root: Path,
    path: Path,
    label: str,
) -> None:
    markdown = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", markdown):
        if (
            target.startswith(("http://", "https://", "mailto:", "#"))
            or "://" in target
        ):
            continue
        relative_target = unquote(target.split("#", 1)[0])
        require(relative_target, f"{label} contains an empty local link")
        try:
            resolved = (path.parent / relative_target).resolve(strict=True)
            resolved.relative_to(root.resolve(strict=True))
        except (OSError, ValueError) as error:
            raise ReleaseVerificationError(
                f"{label} contains a broken or escaping local link: {target}"
            ) from error
        require(
            resolved.is_file(),
            f"{label} local link is not a file: {target}",
        )


def validate_hashed_file(
    root: Path,
    record: dict[str, Any],
    expected_path: str,
    label: str,
) -> Path:
    require(isinstance(record, dict), f"{label} must be one object")
    exact_keys(record, {"path", "sha256"}, label)
    require(record["path"] == expected_path, f"{label} path is not canonical")
    require(
        isinstance(record["sha256"], str)
        and re.fullmatch(r"[0-9a-f]{64}", record["sha256"]) is not None,
        f"{label} SHA-256 is malformed",
    )
    path = safe_file(root, record["path"], label)
    require(
        sha256_file(path) == record["sha256"],
        f"{label} SHA-256 is stale",
    )
    if path.suffix.lower() == ".md":
        _validate_local_markdown_links(root, path, label)
    return path


def evidence_status(markdown: str) -> str:
    matches = re.findall(
        r"^Gate status:\s*(?:\*\*)?(PASSED|FAILED)(?:\*\*)?\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        len(matches) == 1,
        "external evidence must contain exactly one Gate status line",
    )
    return matches[0].lower()


def evidence_role(markdown: str) -> str:
    matches = re.findall(
        r"^Evidence role:\s*([a-z0-9_]+)\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        len(matches) == 1,
        "external evidence must contain exactly one Evidence role line",
    )
    return matches[0]


def evidence_artifact_sha256(markdown: str, artifact: str) -> str:
    require(
        artifact in {"PDF", "EPUB"},
        "external evidence artifact label is unsupported",
    )
    matches = re.findall(
        rf"^{artifact} SHA-256:\s*`?([0-9a-f]{{64}})`?\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        len(matches) == 1,
        f"external evidence must contain exactly one {artifact} SHA-256 line",
    )
    return matches[0]


def _evidence_text_field(markdown: str, field: str) -> str:
    matches = re.findall(
        rf"^{re.escape(field)}:\s*(\S(?:.*\S)?)\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        len(matches) == 1,
        f"external evidence must contain exactly one {field} line",
    )
    value = matches[0]
    require(
        len(value) <= 500,
        f"external evidence {field} is too long",
    )
    return value


def evidence_completed(markdown: str) -> str:
    value = _evidence_text_field(markdown, "Completed")
    require(
        re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is not None,
        "external evidence Completed must be one ISO calendar date",
    )
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise ReleaseVerificationError(
            "external evidence Completed is not a real calendar date"
        ) from error
    return value


def evidence_public_confirmation(markdown: str) -> str:
    return _evidence_text_field(
        markdown,
        "Signer or verifiable public confirmation",
    )


def evidence_limit(markdown: str) -> str:
    return _evidence_text_field(
        markdown,
        "What this evidence does not establish",
    )


def evidence_cohort_binding(markdown: str) -> tuple[str, str]:
    cohort_id = _evidence_text_field(markdown, "Cohort ID")
    require(
        re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,63}", cohort_id) is not None,
        "external evidence Cohort ID is malformed",
    )
    manifest_matches = re.findall(
        r"^Manifest SHA-256:\s*`?([0-9a-f]{64})`?\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        len(manifest_matches) == 1,
        "external evidence must contain exactly one Manifest SHA-256 line",
    )
    return cohort_id, manifest_matches[0]


def evidence_counted_record_sha256s(
    markdown: str,
    expected_count: int,
) -> frozenset[str]:
    matches = re.findall(
        r"^Counted record SHA-256:\s*`?([0-9a-f]{64})`?\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    require(
        len(matches) == expected_count,
        "external evidence has the wrong number of Counted record SHA-256 lines",
    )
    require(
        len(set(matches)) == len(matches),
        "external evidence repeats a Counted record SHA-256",
    )
    return frozenset(matches)


def reject_public_contact_data(markdown: str) -> None:
    searchable_lines = []
    for line in markdown.splitlines():
        field = line.split(":", 1)[0]
        if field in PUBLIC_EVIDENCE_HASH_FIELDS:
            continue
        searchable_lines.append(line)
    searchable = re.sub(
        r"\b\d{4}-\d{2}-\d{2}\b",
        "",
        "\n".join(searchable_lines),
    )
    require(
        EMAIL_PATTERN.search(searchable) is None
        and PHONE_PATTERN.search(searchable) is None,
        "external evidence contains possible private contact data",
    )
