"""Read and enforce the fixed PDF release contract."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from release_common import ReleaseVerificationError, require


A5_WIDTH_POINTS = 419.528
A5_HEIGHT_POINTS = 595.276
A5_TOLERANCE_POINTS = 0.6


@dataclass(frozen=True)
class PdfPageFacts:
    number: int
    width_points: float
    height_points: float
    rotation: int


@dataclass(frozen=True)
class PdfFacts:
    title: str
    author: str
    tagged: bool
    suspects: bool
    javascript: bool
    encrypted: bool
    pages: int
    file_size: int
    page_facts: tuple[PdfPageFacts, ...]


def _parse_pdf_page_facts(output: str, expected_pages: int) -> tuple[PdfPageFacts, ...]:
    sizes: dict[int, tuple[float, float]] = {}
    rotations: dict[int, int] = {}
    for line in output.splitlines():
        size = re.fullmatch(
            r"Page\s+(\d+)\s+size:\s+([0-9.]+)\s+x\s+([0-9.]+)\s+pts(?:\s.*)?",
            line.strip(),
        )
        if size is not None:
            page = int(size.group(1))
            if page in sizes:
                raise ReleaseVerificationError(f"pdfinfo repeated page {page} size")
            sizes[page] = (float(size.group(2)), float(size.group(3)))
            continue
        rotation = re.fullmatch(
            r"Page\s+(\d+)\s+rot:\s+(-?\d+)",
            line.strip(),
        )
        if rotation is not None:
            page = int(rotation.group(1))
            if page in rotations:
                raise ReleaseVerificationError(f"pdfinfo repeated page {page} rotation")
            rotations[page] = int(rotation.group(2))

    expected = set(range(1, expected_pages + 1))
    if sizes.keys() != expected or rotations.keys() != expected:
        raise ReleaseVerificationError(
            "pdfinfo did not report size and rotation for every PDF page"
        )
    return tuple(
        PdfPageFacts(
            number=page,
            width_points=sizes[page][0],
            height_points=sizes[page][1],
            rotation=rotations[page],
        )
        for page in range(1, expected_pages + 1)
    )


def parse_pdfinfo(output: str, pages_output: str | None = None) -> PdfFacts:
    fields: dict[str, str] = {}
    for line in output.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    required = {
        "Title",
        "Author",
        "Tagged",
        "Suspects",
        "JavaScript",
        "Encrypted",
        "Pages",
        "File size",
        "Page size",
        "Page rot",
    }
    missing = sorted(required - fields.keys())
    if missing:
        raise ReleaseVerificationError(f"pdfinfo is missing fields: {missing}")
    file_size = re.fullmatch(r"([\d,]+) bytes", fields["File size"])
    page_size = re.match(
        r"([0-9.]+)\s+x\s+([0-9.]+)\s+pts(?:\s|$)", fields["Page size"]
    )
    rotation = re.fullmatch(r"-?\d+", fields["Page rot"])
    if (
        file_size is None
        or page_size is None
        or rotation is None
        or not fields["Pages"].isdigit()
    ):
        raise ReleaseVerificationError("pdfinfo contains malformed numeric fields")
    boolean_values = {
        label: fields[label].lower()
        for label in ("Tagged", "Suspects", "JavaScript", "Encrypted")
    }
    if any(value not in {"yes", "no"} for value in boolean_values.values()):
        raise ReleaseVerificationError("pdfinfo contains malformed yes/no fields")
    pages = int(fields["Pages"])
    page_facts = (
        _parse_pdf_page_facts(pages_output, pages)
        if pages_output is not None
        else (
            PdfPageFacts(
                number=1,
                width_points=float(page_size.group(1)),
                height_points=float(page_size.group(2)),
                rotation=int(rotation.group()),
            ),
        )
    )
    return PdfFacts(
        title=fields["Title"],
        author=fields["Author"],
        tagged=boolean_values["Tagged"] == "yes",
        suspects=boolean_values["Suspects"] == "yes",
        javascript=boolean_values["JavaScript"] == "yes",
        encrypted=boolean_values["Encrypted"] == "yes",
        pages=pages,
        file_size=int(file_size.group(1).replace(",", "")),
        page_facts=page_facts,
    )


def _run_pdfinfo(command: list[str], root: Path, environment: dict[str, str]) -> str:
    try:
        result = subprocess.run(
            command,
            cwd=root,
            env=environment,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ReleaseVerificationError("cannot run pdfinfo") from error
    if result.returncode:
        raise ReleaseVerificationError(
            f"pdfinfo failed: {result.stderr.strip() or 'unknown error'}"
        )
    return result.stdout


def read_pdf_facts(path: Path, root: Path) -> PdfFacts:
    environment = os.environ.copy()
    environment["LC_ALL"] = "C"
    summary = _run_pdfinfo(["pdfinfo", str(path)], root, environment)
    summary_facts = parse_pdfinfo(summary)
    pages = _run_pdfinfo(
        [
            "pdfinfo",
            "-f",
            "1",
            "-l",
            str(summary_facts.pages),
            str(path),
        ],
        root,
        environment,
    )
    return parse_pdfinfo(summary, pages)


def validate_pdf_contract(pdf: PdfFacts) -> None:
    require(pdf.tagged, "PDF must be tagged")
    require(not pdf.suspects, "pdfinfo marked the PDF as suspect")
    require(not pdf.javascript, "PDF must not contain JavaScript")
    require(not pdf.encrypted, "PDF must not be encrypted")
    require(
        len(pdf.page_facts) == pdf.pages,
        "pdfinfo did not return geometry for every PDF page",
    )
    for page in pdf.page_facts:
        require(page.rotation == 0, f"PDF page {page.number} must not be rotated")
        require(
            abs(page.width_points - A5_WIDTH_POINTS) <= A5_TOLERANCE_POINTS
            and abs(page.height_points - A5_HEIGHT_POINTS) <= A5_TOLERANCE_POINTS,
            f"PDF page {page.number} is not A5 portrait",
        )
