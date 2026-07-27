#!/usr/bin/env python3
"""Run the pinned veraPDF PDF/UA-1 machine-validation gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from edition_contract import load_edition_contract
from release_common import ReleaseVerificationError
from verapdf_validation import run_verapdf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verapdf", required=True, type=Path)
    parser.add_argument(
        "--report-output",
        type=Path,
        default=Path("build/verapdf-report.json"),
    )
    arguments = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    edition = load_edition_contract(root / "book" / "edition.json")
    pdf_path = root / edition.pdf_relative_path
    executable = arguments.verapdf
    if not executable.is_absolute():
        executable = root / executable
    report_output = arguments.report_output
    if not report_output.is_absolute():
        report_output = root / report_output
    try:
        facts = run_verapdf(executable, pdf_path, root, report_output)
    except (OSError, ReleaseVerificationError, ValueError) as error:
        print(f"veraPDF verification failed: {error}", file=sys.stderr)
        raise SystemExit(2) from error
    print(
        f"Verified {facts.profile} with veraPDF {facts.version}: "
        f"{facts.passed_rules} rules and {facts.passed_checks} checks passed."
    )


if __name__ == "__main__":
    main()
