"""Load and strictly validate the canonical publication edition contract."""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from edition_contract_validation import (
    EditionContractError,
    exact_object,
    nonempty_text,
    nonempty_text_array,
    read_json_object,
    require_https_url,
    require_matching_utc_instant,
)


DEFAULT_EDITION_PATH = Path(__file__).resolve().parents[1] / "book" / "edition.json"


@dataclass(frozen=True)
class EditionContract:
    schema_version: int
    edition_id: str
    title: str
    author: str
    language: str
    description: str
    keywords: tuple[str, ...]
    subjects: tuple[str, ...]
    file_stem: str
    identifier_seed: str
    epub_modified: str
    pdf_creation_timestamp: str
    source_path: str
    source_sha256: str
    cover_title_lines: tuple[str, ...]
    cover_kicker: str
    cover_edition_label: str
    cover_epigraph_lines: tuple[str, ...]
    cover_epigraph_source: str
    cover_provenance_lines: tuple[str, ...]
    author_label: str
    chapter_label: str
    practice_label: str
    faq_label: str
    caution_label: str
    source_link_label: str
    toc_label: str
    introduction_label: str
    cover_label: str
    content_label: str
    landmarks_label: str
    cover_alt: str
    accessibility_summary: str
    semantic_required_text: tuple[str, ...]
    validation_locale: str
    target_audience: str

    @property
    def identifier(self) -> str:
        value = uuid.uuid5(uuid.NAMESPACE_URL, self.identifier_seed)
        return f"urn:uuid:{value}"
    @property
    def pdf_relative_path(self) -> Path:
        return Path("dist") / f"{self.file_stem}.pdf"
    @property
    def epub_relative_path(self) -> Path:
        return Path("dist") / f"{self.file_stem}.epub"


def load_edition_contract(path: Path = DEFAULT_EDITION_PATH) -> EditionContract:
    """Load one exact schema-v1 edition contract and reject silent drift."""
    root = exact_object(
        read_json_object(path),
        "edition",
        {
            "schema_version",
            "edition_id",
            "metadata",
            "publication",
            "source",
            "cover",
            "labels",
            "accessibility",
            "quality",
            "scope",
        },
    )
    if type(root["schema_version"]) is not int or root["schema_version"] != 1:
        raise EditionContractError("edition.schema_version must be integer 1")

    metadata = exact_object(
        root["metadata"],
        "edition.metadata",
        {"title", "author", "language", "description", "keywords", "subjects"},
    )
    publication = exact_object(
        root["publication"],
        "edition.publication",
        {
            "file_stem",
            "identifier_seed",
            "epub_modified",
            "pdf_creation_timestamp",
        },
    )
    source = exact_object(root["source"], "edition.source", {"path", "sha256"})
    cover = exact_object(
        root["cover"],
        "edition.cover",
        {
            "title_lines",
            "kicker",
            "edition_label",
            "epigraph_lines",
            "epigraph_source",
            "provenance_lines",
        },
    )
    labels = exact_object(
        root["labels"],
        "edition.labels",
        {
            "author",
            "chapter",
            "practice",
            "faq",
            "caution",
            "source_link",
            "toc",
            "introduction",
            "cover",
            "content",
            "landmarks",
        },
    )
    accessibility = exact_object(
        root["accessibility"],
        "edition.accessibility",
        {"cover_alt", "summary"},
    )
    quality = exact_object(
        root["quality"],
        "edition.quality",
        {"semantic_required_text"},
    )
    scope = exact_object(
        root["scope"],
        "edition.scope",
        {"validation_locale", "target_audience"},
    )

    contract = EditionContract(
        schema_version=root["schema_version"],
        edition_id=nonempty_text(root["edition_id"], "edition.edition_id"),
        title=nonempty_text(metadata["title"], "edition.metadata.title"),
        author=nonempty_text(metadata["author"], "edition.metadata.author"),
        language=nonempty_text(metadata["language"], "edition.metadata.language"),
        description=nonempty_text(
            metadata["description"],
            "edition.metadata.description",
        ),
        keywords=nonempty_text_array(
            metadata["keywords"],
            "edition.metadata.keywords",
        ),
        subjects=nonempty_text_array(
            metadata["subjects"],
            "edition.metadata.subjects",
        ),
        file_stem=nonempty_text(
            publication["file_stem"],
            "edition.publication.file_stem",
        ),
        identifier_seed=nonempty_text(
            publication["identifier_seed"],
            "edition.publication.identifier_seed",
        ),
        epub_modified=nonempty_text(
            publication["epub_modified"],
            "edition.publication.epub_modified",
        ),
        pdf_creation_timestamp=nonempty_text(
            publication["pdf_creation_timestamp"],
            "edition.publication.pdf_creation_timestamp",
        ),
        source_path=nonempty_text(source["path"], "edition.source.path"),
        source_sha256=nonempty_text(source["sha256"], "edition.source.sha256"),
        cover_title_lines=nonempty_text_array(
            cover["title_lines"],
            "edition.cover.title_lines",
        ),
        cover_kicker=nonempty_text(cover["kicker"], "edition.cover.kicker"),
        cover_edition_label=nonempty_text(
            cover["edition_label"],
            "edition.cover.edition_label",
        ),
        cover_epigraph_lines=nonempty_text_array(
            cover["epigraph_lines"],
            "edition.cover.epigraph_lines",
        ),
        cover_epigraph_source=nonempty_text(
            cover["epigraph_source"],
            "edition.cover.epigraph_source",
        ),
        cover_provenance_lines=nonempty_text_array(
            cover["provenance_lines"],
            "edition.cover.provenance_lines",
        ),
        author_label=nonempty_text(labels["author"], "edition.labels.author"),
        chapter_label=nonempty_text(labels["chapter"], "edition.labels.chapter"),
        practice_label=nonempty_text(labels["practice"], "edition.labels.practice"),
        faq_label=nonempty_text(labels["faq"], "edition.labels.faq"),
        caution_label=nonempty_text(labels["caution"], "edition.labels.caution"),
        source_link_label=nonempty_text(
            labels["source_link"],
            "edition.labels.source_link",
        ),
        toc_label=nonempty_text(labels["toc"], "edition.labels.toc"),
        introduction_label=nonempty_text(
            labels["introduction"],
            "edition.labels.introduction",
        ),
        cover_label=nonempty_text(labels["cover"], "edition.labels.cover"),
        content_label=nonempty_text(labels["content"], "edition.labels.content"),
        landmarks_label=nonempty_text(
            labels["landmarks"],
            "edition.labels.landmarks",
        ),
        cover_alt=nonempty_text(
            accessibility["cover_alt"],
            "edition.accessibility.cover_alt",
        ),
        accessibility_summary=nonempty_text(
            accessibility["summary"],
            "edition.accessibility.summary",
        ),
        semantic_required_text=nonempty_text_array(
            quality["semantic_required_text"],
            "edition.quality.semantic_required_text",
        ),
        validation_locale=nonempty_text(
            scope["validation_locale"],
            "edition.scope.validation_locale",
        ),
        target_audience=nonempty_text(
            scope["target_audience"],
            "edition.scope.target_audience",
        ),
    )
    _validate_contract(contract)
    return contract


def _validate_contract(contract: EditionContract) -> None:
    bcp47 = re.compile(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*")
    if bcp47.fullmatch(contract.language) is None:
        raise EditionContractError("edition.metadata.language must be a BCP 47 tag")
    if bcp47.fullmatch(contract.validation_locale) is None:
        raise EditionContractError("edition.scope.validation_locale must be a BCP 47 tag")
    if contract.validation_locale.split("-", 1)[0].casefold() != contract.language.split(
        "-", 1
    )[0].casefold():
        raise EditionContractError(
            "validation locale must share the publication language"
        )
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", contract.edition_id) is None:
        raise EditionContractError("edition.edition_id must be a lowercase slug")
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", contract.file_stem) is None:
        raise EditionContractError(
            "edition.publication.file_stem must be a lowercase slug"
        )
    require_https_url(
        contract.identifier_seed,
        "edition.publication.identifier_seed",
    )
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", contract.epub_modified) is None:
        raise EditionContractError(
            "edition.publication.epub_modified must be UTC RFC 3339"
        )
    if re.fullmatch(r"[1-9]\d*", contract.pdf_creation_timestamp) is None:
        raise EditionContractError(
            "edition.publication.pdf_creation_timestamp must be a positive epoch"
        )
    require_matching_utc_instant(
        contract.pdf_creation_timestamp,
        contract.epub_modified,
    )
    source_path = PurePosixPath(contract.source_path)
    if (
        source_path.is_absolute()
        or ".." in source_path.parts
        or source_path.suffix != ".md"
    ):
        raise EditionContractError("edition.source.path must be a safe relative path")
    if re.fullmatch(r"[0-9a-f]{64}", contract.source_sha256) is None:
        raise EditionContractError(
            "edition.source.sha256 must be one lowercase SHA-256"
        )
    if " ".join(contract.cover_title_lines) != contract.title:
        raise EditionContractError(
            "edition.cover.title_lines must reconstruct the metadata title"
        )
    if contract.title not in contract.cover_alt:
        raise EditionContractError(
            "edition.accessibility.cover_alt must identify the edition title"
        )
    for line in contract.cover_epigraph_lines:
        if line not in contract.cover_alt:
            raise EditionContractError(
                "edition.accessibility.cover_alt must preserve every cover epigraph line"
            )
    if contract.cover_epigraph_source not in contract.cover_alt:
        raise EditionContractError(
            "edition.accessibility.cover_alt must preserve the cover epigraph source"
        )


EDITION = load_edition_contract()
