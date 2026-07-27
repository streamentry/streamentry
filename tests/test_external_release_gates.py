from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from external_release_gates import (  # noqa: E402
    EXPECTED_PROTOCOLS,
    GATE_EVIDENCE_RULES,
    REGISTRY_PATH,
    RELEASE_EVIDENCE_PATH,
    _derived_claims,
    _validate_frozen_candidate,
    verify_external_release_gates,
)
from edition_contract import EDITION  # noqa: E402
from release_common import ReleaseVerificationError  # noqa: E402
from release_evidence import parse_release_evidence  # noqa: E402


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@contextmanager
def _verified_frozen_candidate(head_commit: str):
    with (
        patch(
            "external_release_gates._current_clean_git_head",
            return_value=head_commit,
        ),
        patch("external_release_gates._validate_frozen_candidate"),
    ):
        yield


class ExternalReleaseGateTests(unittest.TestCase):
    def _fixture(self, directory: str) -> tuple[Path, object]:
        root = Path(directory)
        shutil.copytree(
            ROOT / "book" / "references",
            root / "book" / "references",
        )
        shutil.copy2(ROOT / "book" / "edition.json", root / "book" / "edition.json")
        shutil.copytree(ROOT / "scripts", root / "scripts")
        release = parse_release_evidence(
            (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
        )
        return root, release

    def _registry(self, root: Path) -> dict:
        return json.loads((root / REGISTRY_PATH).read_text(encoding="utf-8"))

    def _write_registry(self, root: Path, registry: dict) -> None:
        (root / REGISTRY_PATH).write_text(
            json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _terminal_gate(
        self,
        root: Path,
        registry: dict,
        *,
        gate_id: str,
        status: str,
        candidate_commit: str,
        extra_status_line: str = "",
        evidence_roles: list[str] | None = None,
        evidence_role_line_by_role: dict[str, str] | None = None,
        evidence_path_by_role: dict[str, str] | None = None,
        cohort_binding_by_role: dict[str, tuple[str, str]] | None = None,
        counted_records_by_role: dict[str, list[str]] | None = None,
    ) -> None:
        release_path = root / RELEASE_EVIDENCE_PATH
        release_text = release_path.read_text(encoding="utf-8")
        label_by_gate = {
            "redistribution_rights": "Public redistribution rights",
            "doctrinal_review": "Independent Theravāda review",
            "clinical_safety_review": "Independent clinical-safety review",
            "beginner_cohort": "Five-reader beginner cohort",
            "epub_reader_app": "Human EPUB reader-app smoke test",
            "comparative_evidence": "Comparative evidence",
        }
        label = label_by_gate[gate_id]
        release_text = release_text.replace(
            f"{label}: **OPEN**",
            f"{label}: **{status.upper()}**",
            1,
        )
        release_path.write_text(release_text, encoding="utf-8")
        registry["release_evidence"]["sha256"] = _sha256(release_path)

        release = parse_release_evidence(release_text)
        roles = evidence_roles or sorted(
            GATE_EVIDENCE_RULES[gate_id]["required_singletons"]
            | GATE_EVIDENCE_RULES[gate_id]["required_at_least_one"]
        )
        registry["gates"][gate_id]["status"] = status
        registry["gates"][gate_id]["evidence"] = []
        role_line_by_role = evidence_role_line_by_role or {}
        path_by_role = evidence_path_by_role or {}
        binding_by_role = cohort_binding_by_role or {}
        records_by_role = counted_records_by_role or {}
        for index, role in enumerate(roles, start=1):
            filename = path_by_role.get(role, f"{gate_id}-{index}.md")
            evidence_path = (
                root / "book" / "references" / "external-evidence" / filename
            )
            lines = [
                f"Gate status: {status.upper()}",
                role_line_by_role.get(role, f"Evidence role: {role}"),
                extra_status_line,
                f"Candidate commit: {candidate_commit}",
                f"PDF SHA-256: {release.pdf_sha256}",
                f"EPUB SHA-256: {release.epub_sha256}",
                "Completed: 2026-07-27",
                "Signer or verifiable public confirmation: "
                "Public evidence steward confirmation",
                "What this evidence does not establish: "
                "No claim beyond this gate and frozen candidate.",
            ]
            if role in {"aggregate_report", "reader_app_report"}:
                cohort_id, manifest_sha256 = binding_by_role.get(
                    role,
                    ("cohort-v2-001", "3" * 64),
                )
                lines.extend(
                    [
                        f"Cohort ID: {cohort_id}",
                        f"Manifest SHA-256: {manifest_sha256}",
                    ]
                )
                default_records = (
                    [character * 64 for character in "abcde"]
                    if role == "aggregate_report"
                    else ["a" * 64]
                )
                lines.extend(
                    f"Counted record SHA-256: {digest}"
                    for digest in records_by_role.get(role, default_records)
                )
                if role == "aggregate_report":
                    lines.extend(
                        [
                            "",
                            "# Beginner validation cohort result",
                            "",
                            f"- Verdict: **{'PASS' if status == 'passed' else 'FAIL'}**",
                        ]
                    )
                else:
                    report_status = "PASSED" if status == "passed" else "FAILED"
                    lines.extend(
                        [
                            "",
                            "# Public EPUB reader-app report",
                            "",
                            f"- Repeated start-route status: `{report_status}`",
                            f"- Repeated section-finding status: `{report_status}`",
                            f"- Display criteria status: `{report_status}`",
                        ]
                    )
            lines.append("")
            evidence_path.write_text(
                "\n".join(lines),
                encoding="utf-8",
            )
            registry["gates"][gate_id]["evidence"].append(
                {
                    "path": evidence_path.relative_to(root).as_posix(),
                    "sha256": _sha256(evidence_path),
                    "role": role,
                }
            )
        registry["permitted_claims"] = _derived_claims(registry["gates"])

    def test_current_registry_matches_protocols_and_release_status(self) -> None:
        release = parse_release_evidence(
            (ROOT / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
        )
        registry = verify_external_release_gates(ROOT, release)
        self.assertEqual(
            registry["permitted_claims"],
            ["internally_verified_dual_format_candidate"],
        )
        self.assertTrue(
            all(gate["status"] == "open" for gate in registry["gates"].values())
        )

    def test_rejects_a_stale_protocol_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)
            packet = root / EXPECTED_PROTOCOLS["external_release_packet"]
            packet.write_text(
                packet.read_text(encoding="utf-8") + "\nchanged\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ReleaseVerificationError, "stale"):
                verify_external_release_gates(root, release)

    def test_rejects_a_broken_local_protocol_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)
            packet = root / EXPECTED_PROTOCOLS["external_release_packet"]
            packet.write_text(
                packet.read_text(encoding="utf-8")
                + "\n[missing](does-not-exist.md)\n",
                encoding="utf-8",
            )
            registry = self._registry(root)
            registry["protocols"]["external_release_packet"]["sha256"] = _sha256(
                packet
            )
            self._write_registry(root, registry)
            with self.assertRaisesRegex(ReleaseVerificationError, "broken"):
                verify_external_release_gates(root, release)

    def test_rejects_a_passed_gate_without_public_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)
            registry = self._registry(root)
            registry["gates"]["doctrinal_review"]["status"] = "passed"
            self._write_registry(root, registry)
            with self.assertRaisesRegex(ReleaseVerificationError, "public evidence"):
                verify_external_release_gates(root, release)

    def test_rejects_a_claim_not_derived_from_gate_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)
            registry = self._registry(root)
            registry["permitted_claims"].append(
                "independently_doctrinally_reviewed"
            )
            self._write_registry(root, registry)
            with self.assertRaisesRegex(ReleaseVerificationError, "do not follow"):
                verify_external_release_gates(root, release)

    def test_rejects_human_status_that_contradicts_registry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)
            evidence_path = root / RELEASE_EVIDENCE_PATH
            evidence_path.write_text(
                evidence_path.read_text(encoding="utf-8").replace(
                    "Independent Theravāda review: **OPEN**",
                    "Independent Theravāda review: **PASSED**",
                    1,
                ),
                encoding="utf-8",
            )
            registry = self._registry(root)
            registry["release_evidence"]["sha256"] = _sha256(evidence_path)
            self._write_registry(root, registry)
            with self.assertRaisesRegex(ReleaseVerificationError, "contradicts"):
                verify_external_release_gates(root, release)

    def test_rejects_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)
            registry_path = root / REGISTRY_PATH
            registry_path.write_text(
                registry_path.read_text(encoding="utf-8").replace(
                    '"schema_version": 3,',
                    '"schema_version": 3, "schema_version": 3,',
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ReleaseVerificationError, "duplicate key"):
                verify_external_release_gates(root, release)

    def test_allows_evidence_bound_to_a_frozen_ancestor_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit="2" * 40,
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with _verified_frozen_candidate(current_commit):
                verified = verify_external_release_gates(root, release)
            self.assertEqual(
                verified["gates"]["doctrinal_review"]["status"],
                "passed",
            )

    def test_rejects_frozen_candidate_outside_evidence_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)
            with (
                patch(
                    "external_release_gates._is_git_ancestor",
                    return_value=False,
                ),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "not an ancestor",
                ),
            ):
                _validate_frozen_candidate(
                    root,
                    "2" * 40,
                    "1" * 40,
                    release,
                    EDITION,
                )

    def test_rejects_frozen_candidate_with_other_artifact_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)
            with (
                patch(
                    "external_release_gates._is_git_ancestor",
                    return_value=True,
                ),
                patch(
                    "external_release_gates._git_blob_sha256",
                    return_value="0" * 64,
                ),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "recorded PDF",
                ),
            ):
                _validate_frozen_candidate(
                    root,
                    "2" * 40,
                    "1" * 40,
                    release,
                    EDITION,
                )

    def test_accepts_frozen_ancestor_with_recorded_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)

            def artifact_digest(
                _root: Path,
                _commit: str,
                relative: str,
            ) -> str:
                return (
                    release.pdf_sha256
                    if relative.endswith(".pdf")
                    else release.epub_sha256
                )

            with (
                patch(
                    "external_release_gates._is_git_ancestor",
                    return_value=True,
                ),
                patch(
                    "external_release_gates._git_blob_sha256",
                    side_effect=artifact_digest,
                ),
            ):
                _validate_frozen_candidate(
                    root,
                    "2" * 40,
                    "1" * 40,
                    release,
                    EDITION,
                )

    def test_frozen_candidate_uses_paths_from_the_supplied_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, release = self._fixture(directory)
            edition = replace(EDITION, file_stem="sentinel-edition")
            seen: list[str] = []

            def artifact_digest(
                _root: Path,
                _commit: str,
                relative: str,
            ) -> str:
                seen.append(relative)
                return (
                    release.pdf_sha256
                    if relative.endswith(".pdf")
                    else release.epub_sha256
                )

            with (
                patch(
                    "external_release_gates._is_git_ancestor",
                    return_value=True,
                ),
                patch(
                    "external_release_gates._git_blob_sha256",
                    side_effect=artifact_digest,
                ),
            ):
                _validate_frozen_candidate(
                    root,
                    "2" * 40,
                    "1" * 40,
                    release,
                    edition,
                )

            self.assertEqual(
                seen,
                [
                    "dist/sentinel-edition.pdf",
                    "dist/sentinel-edition.epub",
                ],
            )

    def test_rejects_conflicting_evidence_status_lines(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit=current_commit,
                extra_status_line="Gate status: FAILED",
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(ReleaseVerificationError, "exactly one"),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_unsupported_evidence_role_for_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit=current_commit,
                evidence_roles=["rights_decision"],
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError, "unsupported for gate"
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_missing_required_roles_for_beginner_cohort(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="beginner_cohort",
                status="passed",
                candidate_commit=current_commit,
                evidence_roles=["aggregate_report"],
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(ReleaseVerificationError, "missing required"),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_duplicate_singleton_roles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="beginner_cohort",
                status="passed",
                candidate_commit=current_commit,
                evidence_roles=[
                    "aggregate_report",
                    "aggregate_report",
                    "preregistration_receipt",
                    "public_history_confirmation",
                    "privacy_review_confirmation",
                ],
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError, "duplicate singleton roles"
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_reused_evidence_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="clinical_safety_review",
                status="passed",
                candidate_commit=current_commit,
                evidence_roles=[
                    "clinical_safety_review_report",
                    "clinical_safety_review_report",
                ],
                evidence_path_by_role={
                    "clinical_safety_review_report": "clinical-shared.md",
                },
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError, "may appear only once"
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_stale_hash_field_even_if_current_hash_appears_elsewhere(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit=current_commit,
            )
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            evidence_item = registry["gates"]["doctrinal_review"]["evidence"][0]
            evidence_path = root / evidence_item["path"]
            evidence_text = evidence_path.read_text(encoding="utf-8").replace(
                f"PDF SHA-256: {release.pdf_sha256}",
                "\n".join(
                    [
                        f"PDF SHA-256: {'0' * 64}",
                        f"Incidental current digest: {release.pdf_sha256}",
                    ]
                ),
                1,
            )
            evidence_path.write_text(evidence_text, encoding="utf-8")
            evidence_item["sha256"] = _sha256(evidence_path)
            self._write_registry(root, registry)
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "does not bind the current PDF SHA-256",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_mismatched_evidence_role_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit=current_commit,
                evidence_role_line_by_role={
                    "doctrinal_review_report": "Evidence role: rights_decision"
                },
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError, "Evidence role contradicts"
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_missing_public_evidence_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit=current_commit,
            )
            item = registry["gates"]["doctrinal_review"]["evidence"][0]
            path = root / item["path"]
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "Completed: 2026-07-27\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )
            item["sha256"] = _sha256(path)
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(ReleaseVerificationError, "Completed"),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_missing_public_evidence_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit=current_commit,
            )
            item = registry["gates"]["doctrinal_review"]["evidence"][0]
            path = root / item["path"]
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "Signer or verifiable public confirmation: "
                    "Public evidence steward confirmation\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )
            item["sha256"] = _sha256(path)
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "Signer or verifiable public confirmation",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_missing_public_evidence_limit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit=current_commit,
            )
            item = registry["gates"]["doctrinal_review"]["evidence"][0]
            path = root / item["path"]
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "What this evidence does not establish: "
                    "No claim beyond this gate and frozen candidate.\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )
            item["sha256"] = _sha256(path)
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "What this evidence does not establish",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_impossible_public_evidence_date(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit=current_commit,
            )
            item = registry["gates"]["doctrinal_review"]["evidence"][0]
            path = root / item["path"]
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "Completed: 2026-07-27",
                    "Completed: 2026-02-30",
                    1,
                ),
                encoding="utf-8",
            )
            item["sha256"] = _sha256(path)
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(ReleaseVerificationError, "real calendar"),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_public_evidence_with_contact_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="doctrinal_review",
                status="passed",
                candidate_commit=current_commit,
                extra_status_line="Private return: person@example.org",
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "private contact data",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_terminal_evidence_bound_to_two_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="clinical_safety_review",
                status="passed",
                candidate_commit=current_commit,
                evidence_roles=[
                    "clinical_safety_review_report",
                    "clinical_safety_review_report",
                ],
            )
            second = registry["gates"]["clinical_safety_review"]["evidence"][1]
            path = root / second["path"]
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    f"Candidate commit: {current_commit}",
                    f"Candidate commit: {'2' * 40}",
                    1,
                ),
                encoding="utf-8",
            )
            second["sha256"] = _sha256(path)
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "same frozen Candidate commit",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_allows_multiple_clinical_reports_with_the_same_role(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="clinical_safety_review",
                status="passed",
                candidate_commit=current_commit,
                evidence_roles=[
                    "clinical_safety_review_report",
                    "clinical_safety_review_report",
                ],
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with _verified_frozen_candidate(current_commit):
                verified = verify_external_release_gates(root, release)
            self.assertEqual(
                verified["gates"]["clinical_safety_review"]["status"],
                "passed",
            )

    def test_counted_beginner_and_epub_reports_share_manifest_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="beginner_cohort",
                status="passed",
                candidate_commit=current_commit,
            )
            self._terminal_gate(
                root,
                registry,
                gate_id="epub_reader_app",
                status="passed",
                candidate_commit=current_commit,
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with _verified_frozen_candidate(current_commit):
                verified = verify_external_release_gates(root, release)
            self.assertEqual(
                verified["gates"]["epub_reader_app"]["status"],
                "passed",
            )

    def test_rejects_passed_beginner_report_with_failed_body_verdict(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="beginner_cohort",
                status="passed",
                candidate_commit=current_commit,
            )
            aggregate = registry["gates"]["beginner_cohort"]["evidence"][0]
            path = root / aggregate["path"]
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "- Verdict: **PASS**",
                    "- Verdict: **FAIL**",
                    1,
                ),
                encoding="utf-8",
            )
            aggregate["sha256"] = _sha256(path)
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "report verdict contradicts",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_passed_epub_report_with_failed_body_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="beginner_cohort",
                status="passed",
                candidate_commit=current_commit,
            )
            self._terminal_gate(
                root,
                registry,
                gate_id="epub_reader_app",
                status="passed",
                candidate_commit=current_commit,
            )
            reader_app = registry["gates"]["epub_reader_app"]["evidence"][0]
            path = root / reader_app["path"]
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "- Display criteria status: `PASSED`",
                    "- Display criteria status: `FAILED`",
                    1,
                ),
                encoding="utf-8",
            )
            reader_app["sha256"] = _sha256(path)
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "report verdict contradicts",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_epub_report_from_another_beginner_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="beginner_cohort",
                status="passed",
                candidate_commit=current_commit,
            )
            self._terminal_gate(
                root,
                registry,
                gate_id="epub_reader_app",
                status="passed",
                candidate_commit=current_commit,
                cohort_binding_by_role={
                    "reader_app_report": ("cohort-v2-999", "4" * 64),
                },
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "does not bind the counted beginner manifest",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_epub_report_from_an_uncounted_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="beginner_cohort",
                status="passed",
                candidate_commit=current_commit,
            )
            self._terminal_gate(
                root,
                registry,
                gate_id="epub_reader_app",
                status="passed",
                candidate_commit=current_commit,
                counted_records_by_role={
                    "reader_app_report": ["f" * 64],
                },
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "not committed as one of the five counted records",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_rejects_terminal_epub_gate_without_terminal_cohort(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _release = self._fixture(directory)
            registry = self._registry(root)
            current_commit = "1" * 40
            self._terminal_gate(
                root,
                registry,
                gate_id="epub_reader_app",
                status="passed",
                candidate_commit=current_commit,
            )
            self._write_registry(root, registry)
            release = parse_release_evidence(
                (root / RELEASE_EVIDENCE_PATH).read_text(encoding="utf-8")
            )
            with (
                _verified_frozen_candidate(current_commit),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "terminal counted beginner cohort",
                ),
            ):
                verify_external_release_gates(root, release)

    def test_comparative_claim_requires_the_defined_beginner_gate(self) -> None:
        gates = {
            gate_id: {"status": "open"}
            for gate_id in (
                "redistribution_rights",
                "doctrinal_review",
                "clinical_safety_review",
                "beginner_cohort",
                "epub_reader_app",
                "comparative_evidence",
            )
        }
        gates["comparative_evidence"]["status"] = "passed"
        self.assertNotIn(
            "named_panel_first_use_outperformance",
            _derived_claims(gates),
        )
        gates["beginner_cohort"]["status"] = "passed"
        gates["epub_reader_app"]["status"] = "passed"
        self.assertIn(
            "named_panel_first_use_outperformance",
            _derived_claims(gates),
        )


if __name__ == "__main__":
    unittest.main()
