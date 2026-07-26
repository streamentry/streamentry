"""Verify committed pilot artifacts and a bounded EPUB container contract."""

from __future__ import annotations

import hashlib
import re
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


class ArtifactVerificationError(ValueError):
    """Raised when frozen artifact evidence is not reproduced."""


@dataclass(frozen=True)
class ArtifactEvidence:
    git_commit: str
    pdf_sha256: str
    epub_sha256: str
    pdf_pages: int


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_checked(command: list[str], cwd: Path, label: str) -> bytes:
    try:
        result = subprocess.run(
            command, cwd=cwd, capture_output=True, timeout=60, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ArtifactVerificationError(
            f"{label}: cannot run {command[0]}"
        ) from error
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ArtifactVerificationError(f"{label}: {detail or 'command failed'}")
    return result.stdout


def repo_file(path: Path, repo_root: Path, label: str) -> tuple[Path, str]:
    try:
        resolved = path.resolve(strict=True)
        relative = resolved.relative_to(repo_root.resolve(strict=True))
    except (OSError, ValueError) as error:
        raise ArtifactVerificationError(
            f"{label}: file must exist inside the repository"
        ) from error
    return resolved, relative.as_posix()


def committed_hash(repo_root: Path, commit: str, relative_path: str) -> str:
    blob = run_checked(
        ["git", "show", f"{commit}:{relative_path}"],
        repo_root,
        f"committed file {relative_path}",
    )
    return hashlib.sha256(blob).hexdigest()


def _pdf_pages(path: Path, repo_root: Path) -> int:
    output = run_checked(["pdfinfo", str(path)], repo_root, "PDF page verification")
    match = re.search(rb"^Pages:\s+(\d+)\s*$", output, flags=re.MULTILINE)
    if match is None:
        raise ArtifactVerificationError("PDF page verification: page count is missing")
    return int(match.group(1))


def verify_epub_structure(path: Path) -> None:
    if not zipfile.is_zipfile(path):
        raise ArtifactVerificationError("EPUB is not a ZIP container")
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            if not infos or infos[0].filename != "mimetype":
                raise ArtifactVerificationError("EPUB mimetype must be the first entry")
            if infos[0].compress_type != zipfile.ZIP_STORED:
                raise ArtifactVerificationError("EPUB mimetype must be uncompressed")
            if archive.read("mimetype") != b"application/epub+zip":
                raise ArtifactVerificationError("EPUB mimetype is invalid")
            container = ET.fromstring(archive.read("META-INF/container.xml"))
            rootfiles = container.findall(
                ".//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile"
            )
            if not rootfiles:
                raise ArtifactVerificationError("EPUB container has no rootfile")
            package_path = rootfiles[0].get("full-path", "")
            if not package_path or package_path not in archive.namelist():
                raise ArtifactVerificationError("EPUB package document is missing")
            package = ET.fromstring(archive.read(package_path))
            if not package.tag.endswith("package"):
                raise ArtifactVerificationError("EPUB package document is invalid")
    except (KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        raise ArtifactVerificationError(
            f"EPUB container is malformed: {error}"
        ) from error


def verify_artifacts(
    metadata: dict[str, Any],
    repo_root: Path,
    pdf_path: Path,
    epub_path: Path,
) -> ArtifactEvidence:
    root = repo_root.resolve(strict=True)
    pdf, pdf_relative = repo_file(pdf_path, root, "PDF")
    epub, epub_relative = repo_file(epub_path, root, "EPUB")
    full_commit = (
        run_checked(
            ["git", "rev-parse", "--verify", f"{metadata['git_commit']}^{{commit}}"],
            root,
            "Git commit verification",
        )
        .decode("ascii")
        .strip()
    )
    pdf_hash = sha256_file(pdf)
    epub_hash = sha256_file(epub)
    pages = _pdf_pages(pdf, root)
    verify_epub_structure(epub)
    checks = (
        (pdf_hash == metadata["pdf_sha256"], "recorded PDF hash mismatch"),
        (epub_hash == metadata["epub_sha256"], "recorded EPUB hash mismatch"),
        (pages == metadata["pdf_pages"], "recorded PDF page count mismatch"),
        (
            committed_hash(root, full_commit, pdf_relative) == pdf_hash,
            "PDF does not match its committed blob",
        ),
        (
            committed_hash(root, full_commit, epub_relative) == epub_hash,
            "EPUB does not match its committed blob",
        ),
    )
    for passed, message in checks:
        if not passed:
            raise ArtifactVerificationError(message)
    return ArtifactEvidence(full_commit, pdf_hash, epub_hash, pages)
