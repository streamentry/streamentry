from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
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
    verify_external_release_gates,
)
from release_common import ReleaseVerificationError  # noqa: E402
from release_evidence import parse_release_evidence  # noqa: E402


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ExternalReleaseGateTests(unittest.TestCase):
    def _fixture(self, directory: str) -> tuple[Path, object]:
        root = Path(directory)
        shutil.copytree(
            ROOT / "book" / "references",
            root / "book" / "references",
        )
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
        for index, role in enumerate(roles, start=1):
            filename = path_by_role.get(role, f"{gate_id}-{index}.md")
            evidence_path = (
                root / "book" / "references" / "external-evidence" / filename
            )
            evidence_path.write_text(
                "\n".join(
                    [
                        f"Gate status: {status.upper()}",
                        role_line_by_role.get(role, f"Evidence role: {role}"),
                        extra_status_line,
                        f"Candidate commit: {candidate_commit}",
                        f"PDF SHA-256: {release.pdf_sha256}",
                        f"EPUB SHA-256: {release.epub_sha256}",
                        "",
                    ]
                ),
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
                    '"schema_version": 2,',
                    '"schema_version": 2, "schema_version": 2,',
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ReleaseVerificationError, "duplicate key"):
                verify_external_release_gates(root, release)

    def test_rejects_evidence_bound_to_another_candidate(self) -> None:
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
            with (
                patch(
                    "external_release_gates._current_git_candidate",
                    return_value=current_commit,
                ),
                self.assertRaisesRegex(
                    ReleaseVerificationError,
                    "current clean Git candidate",
                ),
            ):
                verify_external_release_gates(root, release)

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
                patch(
                    "external_release_gates._current_git_candidate",
                    return_value=current_commit,
                ),
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
                patch(
                    "external_release_gates._current_git_candidate",
                    return_value=current_commit,
                ),
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
                patch(
                    "external_release_gates._current_git_candidate",
                    return_value=current_commit,
                ),
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
                patch(
                    "external_release_gates._current_git_candidate",
                    return_value=current_commit,
                ),
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
                patch(
                    "external_release_gates._current_git_candidate",
                    return_value=current_commit,
                ),
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
                patch(
                    "external_release_gates._current_git_candidate",
                    return_value=current_commit,
                ),
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
                patch(
                    "external_release_gates._current_git_candidate",
                    return_value=current_commit,
                ),
                self.assertRaisesRegex(
                    ReleaseVerificationError, "Evidence role contradicts"
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
            with patch(
                "external_release_gates._current_git_candidate",
                return_value=current_commit,
            ):
                verified = verify_external_release_gates(root, release)
            self.assertEqual(
                verified["gates"]["clinical_safety_review"]["status"],
                "passed",
            )

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
