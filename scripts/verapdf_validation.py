"""Run and verify the pinned machine-checkable PDF/UA-1 validation contract."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from release_common import ReleaseVerificationError, require


VERAPDF_VERSION = "1.30.2"
VERAPDF_INSTALLER_URL = (
    "https://software.verapdf.org/releases/1.30/"
    "verapdf-greenfield-1.30.2-installer.zip"
)
VERAPDF_INSTALLER_SHA256 = (
    "6cc6341cb1af644044054b81f00a6590a7918abb18f762243de115258bcad838"
)
VERAPDF_PROFILE = "PDF/UA-1 validation profile"


@dataclass(frozen=True)
class VeraPdfFacts:
    version: str
    profile: str
    passed_rules: int
    passed_checks: int


def _mapping(value: Any, name: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"veraPDF report {name} must be an object")
    return value


def _single(value: Any, name: str) -> dict[str, Any]:
    require(
        isinstance(value, list) and len(value) == 1,
        f"veraPDF report {name} must contain exactly one item",
    )
    return _mapping(value[0], f"{name}[0]")


def _integer(value: Any, name: str) -> int:
    require(
        isinstance(value, int) and not isinstance(value, bool),
        f"veraPDF report {name} must be an integer",
    )
    return value


def parse_verapdf_report(
    payload: Any,
    expected_pdf: Path,
    expected_version: str = VERAPDF_VERSION,
) -> VeraPdfFacts:
    root = _mapping(payload, "root")
    report = _mapping(root.get("report"), "report")
    build = _mapping(report.get("buildInformation"), "buildInformation")
    release_details = build.get("releaseDetails")
    require(
        isinstance(release_details, list) and release_details,
        "veraPDF report must identify its release components",
    )
    components: dict[str, str] = {}
    for index, raw_component in enumerate(release_details):
        component = _mapping(raw_component, f"releaseDetails[{index}]")
        identifier = component.get("id")
        version = component.get("version")
        require(
            isinstance(identifier, str)
            and identifier
            and isinstance(version, str)
            and version,
            "veraPDF release components require non-empty id and version",
        )
        require(
            identifier not in components,
            f"veraPDF report repeats release component {identifier}",
        )
        components[identifier] = version
    require(
        set(components) == {"core", "validation-model", "apps"},
        "veraPDF report has an unexpected release-component set",
    )
    require(
        set(components.values()) == {expected_version},
        f"veraPDF report must come entirely from version {expected_version}",
    )

    job = _single(report.get("jobs"), "jobs")
    item = _mapping(job.get("itemDetails"), "itemDetails")
    reported_name = item.get("name")
    require(
        isinstance(reported_name, str) and reported_name,
        "veraPDF report requires the validated PDF path",
    )
    require(
        Path(reported_name).resolve() == expected_pdf.resolve(),
        "veraPDF report is bound to a different PDF",
    )
    require(
        item.get("size") == expected_pdf.stat().st_size,
        "veraPDF report PDF size does not match the validated artifact",
    )

    result = _single(job.get("validationResult"), "validationResult")
    require(
        result.get("jobEndStatus") == "normal",
        "veraPDF validation job did not end normally",
    )
    require(
        result.get("profileName") == VERAPDF_PROFILE,
        "veraPDF did not use the PDF/UA-1 validation profile",
    )
    require(
        result.get("compliant") is True,
        "veraPDF reports that the PDF is not PDF/UA-1 compliant",
    )
    details = _mapping(result.get("details"), "validation details")
    passed_rules = _integer(details.get("passedRules"), "passedRules")
    failed_rules = _integer(details.get("failedRules"), "failedRules")
    passed_checks = _integer(details.get("passedChecks"), "passedChecks")
    failed_checks = _integer(details.get("failedChecks"), "failedChecks")
    require(failed_rules == 0, "veraPDF reports failed PDF/UA-1 rules")
    require(failed_checks == 0, "veraPDF reports failed PDF/UA-1 checks")
    require(passed_rules > 0, "veraPDF report contains no passed PDF/UA-1 rules")
    require(passed_checks > 0, "veraPDF report contains no passed PDF/UA-1 checks")
    require(
        details.get("ruleSummaries") == [],
        "veraPDF compliant report must not contain failed-rule summaries",
    )

    batch = _mapping(report.get("batchSummary"), "batchSummary")
    expected_batch_values = {
        "totalJobs": 1,
        "outOfMemory": 0,
        "veraExceptions": 0,
        "failedEncryptedJobs": 0,
        "failedParsingJobs": 0,
    }
    for field, expected in expected_batch_values.items():
        require(
            batch.get(field) == expected,
            f"veraPDF batch summary {field} must equal {expected}",
        )
    validation = _mapping(batch.get("validationSummary"), "validationSummary")
    expected_validation_values = {
        "failedJobCount": 0,
        "totalJobCount": 1,
        "compliantPdfaCount": 1,
        "nonCompliantPdfaCount": 0,
        "successfulJobCount": 1,
    }
    for field, expected in expected_validation_values.items():
        require(
            validation.get(field) == expected,
            f"veraPDF validation summary {field} must equal {expected}",
        )
    return VeraPdfFacts(
        version=expected_version,
        profile=VERAPDF_PROFILE,
        passed_rules=passed_rules,
        passed_checks=passed_checks,
    )


def _run(command: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ReleaseVerificationError("cannot run veraPDF") from error
    require(
        completed.returncode == 0,
        f"veraPDF failed: {completed.stderr.strip() or 'unknown error'}",
    )
    require(
        not completed.stderr.strip(),
        f"veraPDF wrote unexpected stderr: {completed.stderr.strip()}",
    )
    return completed


def run_verapdf(
    executable: Path,
    pdf_path: Path,
    root: Path,
    report_output: Path | None = None,
) -> VeraPdfFacts:
    version_result = _run([str(executable), "--version"], root, timeout=30)
    first_line = version_result.stdout.splitlines()[0] if version_result.stdout else ""
    match = re.fullmatch(r"veraPDF ([0-9]+\.[0-9]+\.[0-9]+)", first_line)
    require(match is not None, "veraPDF returned a malformed version string")
    require(
        match.group(1) == VERAPDF_VERSION,
        f"veraPDF version must be {VERAPDF_VERSION}",
    )
    validation_result = _run(
        [
            str(executable),
            "--flavour",
            "ua1",
            "--format",
            "json",
            "--maxfailuresdisplayed",
            "20",
            str(pdf_path),
        ],
        root,
        timeout=180,
    )
    try:
        payload = json.loads(validation_result.stdout)
    except json.JSONDecodeError as error:
        raise ReleaseVerificationError("veraPDF returned malformed JSON") from error
    facts = parse_verapdf_report(payload, pdf_path)
    if report_output is not None:
        report_output.parent.mkdir(parents=True, exist_ok=True)
        report_output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return facts
