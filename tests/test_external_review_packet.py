from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from edition_contract import EDITION  # noqa: E402
from external_review_packet import _safe_relative, clean_head  # noqa: E402
from external_review_packet_archive import (  # noqa: E402
    ZIP_TIMESTAMP,
    validate_packet,
    write_packet,
)
from external_review_packet_content import (  # noqa: E402
    GATE_ORDER,
    PacketMember,
    PacketSnapshot,
    generated_members,
)
from release_common import ReleaseVerificationError  # noqa: E402
from release_evidence import ReleaseEvidence  # noqa: E402


def _snapshot() -> PacketSnapshot:
    return PacketSnapshot(
        commit="1" * 40,
        edition=replace(EDITION, edition_id="packet-test"),
        release=ReleaseEvidence(
            edition_contract_sha256="2" * 64,
            source_sha256="3" * 64,
            pdf_sha256="4" * 64,
            epub_sha256="5" * 64,
            pdf_pages=149,
            pdf_size=1_200_000,
            epub_content_entries=155,
            epub_cover_entries=1,
            epub_size=160_000,
            publication_credit=EDITION.author,
        ),
        release_evidence_sha256="6" * 64,
        gate_statuses=tuple((gate, "open") for gate in GATE_ORDER),
        permitted_claims=("machine-verified candidate",),
    )


def _members(snapshot: PacketSnapshot) -> tuple[PacketMember, ...]:
    return (
        PacketMember(
            "repository/dist/book.pdf",
            b"pdf",
            "artifact",
            "dist/book.pdf",
        ),
        PacketMember(
            "repository/dist/book.epub",
            b"epub",
            "artifact",
            "dist/book.epub",
        ),
        *generated_members(snapshot),
    )


def _rewrite_member(source: Path, target: Path, name: str, payload: bytes) -> None:
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(target, "w") as changed:
        for member_name in sorted(original.namelist()):
            info = zipfile.ZipInfo(member_name, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            data = payload if member_name == name else original.read(member_name)
            changed.writestr(info, data, compresslevel=9)


class ExternalReviewPacketTests(unittest.TestCase):
    def test_build_is_byte_reproducible_and_self_validating(self) -> None:
        snapshot = _snapshot()
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.zip"
            second = Path(directory) / "second.zip"
            write_packet(first, snapshot, _members(snapshot))
            write_packet(second, snapshot, _members(snapshot))
            self.assertEqual(first.read_bytes(), second.read_bytes())
            validate_packet(first, snapshot)

    def test_manifest_and_assignments_bind_the_exact_candidate(self) -> None:
        snapshot = _snapshot()
        with tempfile.TemporaryDirectory() as directory:
            packet = Path(directory) / "packet.zip"
            write_packet(packet, snapshot, _members(snapshot))
            with zipfile.ZipFile(packet) as archive:
                manifest = json.loads(archive.read("manifest.json"))
                self.assertEqual(
                    manifest["packet_type"],
                    "external_review_coordinator",
                )
                self.assertEqual(manifest["candidate"]["commit"], snapshot.commit)
                self.assertEqual(
                    manifest["gate_statuses"],
                    dict(snapshot.gate_statuses),
                )
                for gate in GATE_ORDER:
                    assignment = archive.read(
                        f"generated/assignments/{gate}.md"
                    ).decode("utf-8")
                    self.assertIn(snapshot.commit, assignment)
                    self.assertIn(snapshot.release.pdf_sha256, assignment)
                    self.assertIn(snapshot.release.epub_sha256, assignment)
                    self.assertIn(f"Gate ID: `{gate}`", assignment)

    def test_guide_denies_that_packet_construction_passes_a_gate(self) -> None:
        snapshot = _snapshot()
        guide = generated_members(snapshot)[0].payload.decode("utf-8")
        self.assertIn("does not establish rights", guide)
        self.assertIn("clinical safety", guide)
        self.assertIn("comparative superiority", guide)

    def test_validator_rejects_tampered_payload(self) -> None:
        snapshot = _snapshot()
        with tempfile.TemporaryDirectory() as directory:
            packet = Path(directory) / "packet.zip"
            tampered = Path(directory) / "tampered.zip"
            write_packet(packet, snapshot, _members(snapshot))
            _rewrite_member(packet, tampered, "README.md", b"tampered")
            with self.assertRaisesRegex(
                ReleaseVerificationError,
                "checksum mismatch",
            ):
                validate_packet(tampered, snapshot)

    def test_writer_rejects_duplicate_archive_paths(self) -> None:
        snapshot = _snapshot()
        duplicate = PacketMember("README.md", b"duplicate", "duplicate")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(
                ReleaseVerificationError,
                "duplicate archive paths",
            ):
                write_packet(
                    Path(directory) / "packet.zip",
                    snapshot,
                    (*generated_members(snapshot), duplicate),
                )

    def test_writer_rejects_unsafe_and_reserved_archive_paths(self) -> None:
        snapshot = _snapshot()
        invalid = ("../escape", "/absolute", "manifest.json", "SHA256SUMS.txt")
        with tempfile.TemporaryDirectory() as directory:
            for index, path in enumerate(invalid):
                with self.subTest(path=path):
                    with self.assertRaises(ReleaseVerificationError):
                        write_packet(
                            Path(directory) / f"packet-{index}.zip",
                            snapshot,
                            (PacketMember(path, b"invalid", "invalid"),),
                        )

    def test_clean_head_rejects_dirty_worktree(self) -> None:
        with patch(
            "external_review_packet._git_bytes",
            side_effect=[b"1" * 40 + b"\n", b"?? untracked\n"],
        ):
            with self.assertRaisesRegex(
                ReleaseVerificationError,
                "clean worktree",
            ):
                clean_head(ROOT)

    def test_packet_source_paths_cannot_escape_repository(self) -> None:
        for path in ("/absolute", "../outside", "book/../outside"):
            with self.subTest(path=path):
                with self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "unsafe packet source path",
                ):
                    _safe_relative(path)


if __name__ == "__main__":
    unittest.main()
