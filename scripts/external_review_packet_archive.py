"""Deterministic ZIP writer and validator for external-review packets."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from external_review_packet_content import (
    GATE_ORDER,
    PacketMember,
    PacketSnapshot,
    manifest_bytes,
)
from release_common import require


ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
RESERVED_PATHS = {"manifest.json", "SHA256SUMS.txt"}


def _zip_info(path: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(path, ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


def _safe_archive_path(path: str) -> bool:
    pure = PurePosixPath(path)
    return (
        bool(path)
        and not pure.is_absolute()
        and ".." not in pure.parts
        and path == pure.as_posix()
    )


def write_packet(
    output: Path,
    snapshot: PacketSnapshot,
    members: tuple[PacketMember, ...],
) -> None:
    require(output.suffix == ".zip", "review packet output must use .zip")
    require(
        len({member.archive_path for member in members}) == len(members),
        "review packet contains duplicate archive paths",
    )
    require(
        all(_safe_archive_path(member.archive_path) for member in members),
        "review packet contains an unsafe archive path",
    )
    require(
        not RESERVED_PATHS.intersection(member.archive_path for member in members),
        "review packet member uses a reserved archive path",
    )
    manifest = PacketMember(
        "manifest.json",
        manifest_bytes(snapshot, members),
        "manifest",
    )
    payloads = {member.archive_path: member.payload for member in (*members, manifest)}
    checksums = "\n".join(
        f"{hashlib.sha256(payloads[path]).hexdigest()}  {path}"
        for path in sorted(payloads)
    ) + "\n"
    payloads["SHA256SUMS.txt"] = checksums.encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=f".{output.name}.",
        suffix=".tmp",
        dir=output.parent,
        delete=False,
    ) as handle:
        temporary = Path(handle.name)
    try:
        with zipfile.ZipFile(temporary, "w") as archive:
            for path in sorted(payloads):
                archive.writestr(_zip_info(path), payloads[path], compresslevel=9)
        validate_packet(temporary, snapshot)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)


def validate_packet(path: Path, snapshot: PacketSnapshot) -> None:
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        require(names == sorted(names), "review packet entries are not sorted")
        require(len(names) == len(set(names)), "review packet has duplicate entries")
        require(
            all(info.date_time == ZIP_TIMESTAMP for info in infos),
            "review packet timestamps are not deterministic",
        )
        checksum_lines = archive.read("SHA256SUMS.txt").decode("utf-8").splitlines()
        require(
            all(re.fullmatch(r"[0-9a-f]{64}  [^\r\n]+", line) for line in checksum_lines),
            "review packet checksum index is malformed",
        )
        expected = {
            line.split("  ", 1)[1]: line.split("  ", 1)[0]
            for line in checksum_lines
        }
        require(
            set(expected) == set(names) - {"SHA256SUMS.txt"},
            "checksum index is incomplete",
        )
        for name, digest in expected.items():
            require(
                hashlib.sha256(archive.read(name)).hexdigest() == digest,
                f"review packet checksum mismatch: {name}",
            )
        manifest = json.loads(archive.read("manifest.json"))
        candidate = manifest.get("candidate", {})
        require(candidate.get("commit") == snapshot.commit, "packet commit drift")
        require(
            candidate.get("pdf_sha256") == snapshot.release.pdf_sha256,
            "packet PDF drift",
        )
        require(
            candidate.get("epub_sha256") == snapshot.release.epub_sha256,
            "packet EPUB drift",
        )
        require(
            candidate.get("pdf_pages") == snapshot.release.pdf_pages,
            "packet page-count drift",
        )
        require(
            manifest.get("gate_statuses") == dict(snapshot.gate_statuses),
            "packet gate drift",
        )
        require(
            manifest.get("permitted_claims") == list(snapshot.permitted_claims),
            "packet permitted-claim drift",
        )
        declared = {
            item["archive_path"]: item["sha256"]
            for item in manifest.get("members", [])
        }
        require(
            set(declared) == set(names) - {"SHA256SUMS.txt", "manifest.json"},
            "packet manifest member index is incomplete",
        )
        for name, digest in declared.items():
            require(
                hashlib.sha256(archive.read(name)).hexdigest() == digest,
                f"packet manifest hash mismatch: {name}",
            )
        for gate in GATE_ORDER:
            text = archive.read(f"generated/assignments/{gate}.md").decode("utf-8")
            require(f"Gate ID: `{gate}`" in text, f"assignment gate drift: {gate}")
            require(snapshot.commit in text, f"assignment commit drift: {gate}")
            require(
                snapshot.release.pdf_sha256 in text,
                f"assignment PDF drift: {gate}",
            )
            require(
                snapshot.release.epub_sha256 in text,
                f"assignment EPUB drift: {gate}",
            )
