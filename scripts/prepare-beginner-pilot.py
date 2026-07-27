#!/usr/bin/env python3
"""Prepare and finalize a privacy-bounded beginner-pilot cohort."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from beginner_pilot_artifact import ArtifactVerificationError
from beginner_pilot_validation import InvalidRecord
from beginner_pilot_preparation import (
    WorkflowError,
    initialize_cohort,
    registration_sha256,
    utc_timestamp,
)
from beginner_pilot_workflow import (
    create_attempt_draft,
    finalize_cohort,
)
from edition_contract_validation import EditionContractError


ROOT = Path(__file__).resolve().parents[1]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare real pilot records without manufacturing participant evidence."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    init.add_argument("--cohort-id", required=True)
    init.add_argument("--primary-format", choices=("pdf", "epub"), required=True)
    init.add_argument("--registered-at", default=None)
    init.add_argument("--external-registry-reference")

    attempt = subparsers.add_parser("new-attempt")
    attempt.add_argument("--cohort-id", required=True)
    attempt.add_argument("--started-at", default=None)
    attempt.add_argument("--consent-confirmed", action="store_true")
    attempt.add_argument("--include-epub-smoke", action="store_true")

    finalize = subparsers.add_parser("finalize")
    finalize.add_argument("--cohort-id", required=True)
    finalize.add_argument("--closed-at", required=True)
    return parser


def _score(manifest_path: Path) -> int:
    cohort_dir = manifest_path.parent
    command = [
        sys.executable,
        str(ROOT / "scripts" / "score-beginner-pilot.py"),
        str(manifest_path),
        "--output",
        str(cohort_dir / "aggregate-report.md"),
        "--epub-evidence-output",
        str(cohort_dir / "reader-app-report.md"),
    ]
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "init":
            path = initialize_cohort(
                ROOT,
                cohort_id=args.cohort_id,
                primary_format=args.primary_format,
                registered_at=args.registered_at or utc_timestamp(),
                external_registry_reference=args.external_registry_reference,
            )
            print(f"Registration: {path}")
            print(f"Registration SHA-256: {registration_sha256(path)}")
            print(
                "Evidence boundary: this local registration is not participant "
                "evidence and does not independently prove preregistration."
            )
            return 0
        if args.command == "new-attempt":
            path = create_attempt_draft(
                ROOT,
                cohort_id=args.cohort_id,
                started_at=args.started_at or utc_timestamp(),
                consent_confirmed=args.consent_confirmed,
                include_epub_smoke=args.include_epub_smoke,
            )
            print(f"Draft record: {path}")
            print(
                "Evidence boundary: the draft is intentionally schema-invalid "
                "until every null is replaced with real session data."
            )
            return 0
        manifest_path = finalize_cohort(
            ROOT,
            cohort_id=args.cohort_id,
            closed_at=args.closed_at,
        )
        score_status = _score(manifest_path)
        print(f"Final manifest: {manifest_path}")
        if score_status == 0:
            print("Cohort result: PASS")
        elif score_status == 1:
            print("Cohort result: FAIL; do not claim beginner validation")
        else:
            print("Cohort evidence became invalid during scoring", file=sys.stderr)
        return score_status
    except (
        ArtifactVerificationError,
        EditionContractError,
        InvalidRecord,
        OSError,
        WorkflowError,
    ) as error:
        print(f"Beginner-pilot workflow refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
