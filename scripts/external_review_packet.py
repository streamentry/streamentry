"""Collect one clean Git snapshot for a deterministic external-review packet."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path, PurePosixPath

from beginner_pilot_artifact import sha256_file
from edition_contract import load_edition_contract
from external_review_packet_archive import write_packet
from external_review_packet_content import (
    GATE_ASSIGNMENTS,
    GATE_ORDER,
    PILOT_RUNTIME_PATHS,
    STATIC_SOURCE_PATHS,
    PacketMember,
    PacketSnapshot,
    generated_members,
)
from release_common import ReleaseVerificationError, require
from verify_release import verify_release


def _git_bytes(root: Path, arguments: list[str], label: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ReleaseVerificationError(f"cannot read {label} from Git") from error
    return result.stdout


def clean_head(root: Path) -> str:
    commit = _git_bytes(root, ["rev-parse", "HEAD"], "candidate commit").decode().strip()
    require(
        re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
        "review packet candidate must be one full lowercase commit",
    )
    status = _git_bytes(
        root,
        ["status", "--porcelain", "--untracked-files=all"],
        "worktree status",
    )
    require(not status.strip(), "review packet requires a clean worktree")
    return commit


def _safe_relative(path: str) -> str:
    pure = PurePosixPath(path)
    require(
        not pure.is_absolute() and ".." not in pure.parts and path == pure.as_posix(),
        f"unsafe packet source path: {path}",
    )
    return path


def _committed_member(
    root: Path,
    commit: str,
    path: str,
    role: str,
) -> PacketMember:
    relative = _safe_relative(path)
    current = root / relative
    require(current.is_file(), f"packet source is missing: {relative}")
    payload = current.read_bytes()
    committed = _git_bytes(root, ["show", f"{commit}:{relative}"], relative)
    require(
        payload == committed,
        f"packet source differs from {commit[:12]}: {relative}",
    )
    return PacketMember(f"repository/{relative}", payload, role, relative)


def _typst_sources(root: Path, commit: str) -> tuple[str, ...]:
    output = _git_bytes(
        root,
        [
            "ls-tree",
            "-r",
            "--name-only",
            commit,
            "book/chapters",
            "book/appendices",
        ],
        "Typst reading sources",
    ).decode()
    return tuple(sorted(path for path in output.splitlines() if path.endswith(".typ")))


def load_snapshot(root: Path) -> PacketSnapshot:
    commit = clean_head(root)
    release = verify_release(root)
    edition = load_edition_contract(root / "book" / "edition.json")
    registry_path = root / "book" / "references" / "external-release-gates.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    gates = registry.get("gates")
    require(isinstance(gates, dict), "external gate registry has no gates object")
    require(
        set(gates) == set(GATE_ORDER),
        "external gate registry has unexpected gates",
    )
    statuses = tuple((gate, gates[gate]["status"]) for gate in GATE_ORDER)
    claims = registry.get("permitted_claims")
    require(
        isinstance(claims, list) and all(isinstance(item, str) for item in claims),
        "external gate registry permitted claims are malformed",
    )
    return PacketSnapshot(
        commit=commit,
        edition=edition,
        release=release,
        release_evidence_sha256=sha256_file(
            root / "book" / "references" / "release-evidence.md"
        ),
        gate_statuses=statuses,
        permitted_claims=tuple(claims),
    )


def source_members(
    root: Path,
    snapshot: PacketSnapshot,
) -> tuple[PacketMember, ...]:
    dynamic = (
        snapshot.edition.source_path,
        snapshot.edition.pdf_relative_path.as_posix(),
        snapshot.edition.epub_relative_path.as_posix(),
        *_typst_sources(root, snapshot.commit),
    )
    paths = tuple(dict.fromkeys((*STATIC_SOURCE_PATHS, *dynamic)))
    artifact_paths = {
        snapshot.edition.pdf_relative_path.as_posix(),
        snapshot.edition.epub_relative_path.as_posix(),
    }
    protocol_paths = {
        path
        for values in GATE_ASSIGNMENTS.values()
        for path in values[2]
    }
    runtime_paths = set(PILOT_RUNTIME_PATHS)
    return tuple(
        _committed_member(
            root,
            snapshot.commit,
            path,
            (
                "artifact"
                if path in artifact_paths
                else "protocol"
                if path in protocol_paths
                else "operator-runtime"
                if path in runtime_paths
                else "publication-source"
            ),
        )
        for path in paths
    )


def build_packet(root: Path, output: Path) -> PacketSnapshot:
    snapshot = load_snapshot(root)
    members = (*source_members(root, snapshot), *generated_members(snapshot))
    write_packet(output, snapshot, members)
    return snapshot
