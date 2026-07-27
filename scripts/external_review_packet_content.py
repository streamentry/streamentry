"""Canonical content and data structures for an external-review packet."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from edition_contract import EditionContract
from release_evidence import ReleaseEvidence


GATE_ORDER = (
    "redistribution_rights",
    "doctrinal_review",
    "clinical_safety_review",
    "beginner_cohort",
    "epub_reader_app",
    "comparative_evidence",
)
GATE_ASSIGNMENTS = {
    "redistribution_rights": (
        "Quyết định quyền phát hành",
        "Xác định thẩm quyền và phạm vi cho phép đối với đúng PDF và EPUB.",
        (
            "book/references/rights-decision-template.md",
            "book/references/rights-materials-inventory.md",
        ),
    ),
    "doctrinal_review": (
        "Phản biện giáo lý độc lập",
        "Kiểm nguồn, tầng văn bản, giới hạn và các mệnh đề Theravāda chịu tải.",
        (
            "book/references/doctrinal-review-protocol.md",
            "book/references/attainment-source-audit.md",
        ),
    ),
    "clinical_safety_review": (
        "Phản biện an toàn lâm sàng độc lập",
        "Kiểm toàn bộ cơ chế nguy hại, giới hạn y khoa và phương pháp nghiên cứu.",
        ("book/references/clinical-safety-review-protocol.md",),
    ),
    "beginner_cohort": (
        "Cohort năm người mới",
        "Điều phối năm bản ghi được tính theo giao thức và scorer đã khóa.",
        (
            "book/references/beginner-validation-protocol.md",
            "book/references/beginner-reader-kit.md",
        ),
    ),
    "epub_reader_app": (
        "Thử EPUB trong ứng dụng đọc thật",
        "Ghi hai tác vụ lặp lại và tám kiểm tra hiển thị của người đọc được tính.",
        ("book/references/beginner-reader-kit.md",),
    ),
    "comparative_evidence": (
        "So sánh lần sử dụng đầu tiên",
        "Đăng ký trước và chạy đúng panel, dân số, phân nhóm và outcome đã khóa.",
        ("book/references/comparative-beginner-protocol.md",),
    ),
}
STATIC_SOURCE_PATHS = (
    "README.md",
    "book/main.typ",
    "book/theme.typ",
    "book/components.typ",
    "book/edition.typ",
    "book/edition.json",
    "book/references/release-evidence.md",
    "book/references/edition-contract.md",
    "book/references/publish-readiness-audit.md",
    "book/references/claim-ledger.md",
    "book/references/attainment-source-audit.md",
    "book/references/external-release-packet.md",
    "book/references/external-release-gates.json",
    "book/references/external-evidence/README.md",
    "book/references/rights-decision-template.md",
    "book/references/rights-materials-inventory.md",
    "book/references/doctrinal-review-protocol.md",
    "book/references/clinical-safety-review-protocol.md",
    "book/references/beginner-validation-protocol.md",
    "book/references/beginner-reader-kit.md",
    "book/references/comparative-beginner-protocol.md",
    "book/references/beginner-pilot-record.schema.json",
    "book/references/beginner-pilot-cohort-manifest.schema.json",
)


@dataclass(frozen=True)
class PacketSnapshot:
    commit: str
    edition: EditionContract
    release: ReleaseEvidence
    release_evidence_sha256: str
    gate_statuses: tuple[tuple[str, str], ...]
    permitted_claims: tuple[str, ...]

    @property
    def packet_id(self) -> str:
        return f"{self.edition.edition_id}-{self.commit[:12]}"


@dataclass(frozen=True)
class PacketMember:
    archive_path: str
    payload: bytes
    role: str
    source_path: str | None = None

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.payload).hexdigest()


def assignment_text(gate_id: str, snapshot: PacketSnapshot) -> str:
    title, decision, protocols = GATE_ASSIGNMENTS[gate_id]
    status = dict(snapshot.gate_statuses)[gate_id]
    protocol_lines = "\n".join(f"- `repository/{path}`" for path in protocols)
    return f"""# Phiếu phân công: {title}

Packet ID: `{snapshot.packet_id}`
Gate ID: `{gate_id}`
Gate status khi tạo packet: `{status}`
Candidate commit: `{snapshot.commit}`
PDF SHA-256: `{snapshot.release.pdf_sha256}`
EPUB SHA-256: `{snapshot.release.epub_sha256}`
PDF pages: `{snapshot.release.pdf_pages}`

## Quyết định được yêu cầu

{decision}

## Tài liệu điều khiển

{protocol_lines}

## Phần người điều phối phải điền ngoài kho công khai

Reviewer or decision-maker:
Public qualifications or authority evidence:
Declared competence scope:
Conflicts:
Compensation and payer:
Start date:
Deadline:
Private return route:
Urgent escalation route:
May publish name and qualifications: yes | no | conditional
May publish findings or report: yes | no | conditional
Out-of-scope topics:

Không ghi email, số điện thoại, địa chỉ hoặc dữ liệu người tham gia vào hồ sơ công
khai. Packet này chỉ khóa ứng viên và yêu cầu công việc; nó không làm cổng được
thông qua, không xác thực danh tính và không thay chữ ký hoặc bằng chứng bên ngoài.
"""


def guide_text(snapshot: PacketSnapshot) -> str:
    statuses = "\n".join(
        f"- `{gate}`: **{status.upper()}**"
        for gate, status in snapshot.gate_statuses
    )
    return f"""# External review coordinator packet

Packet `{snapshot.packet_id}` binds all enclosed instructions and artifacts to
commit `{snapshot.commit}`.

- PDF: `{snapshot.release.pdf_sha256}` ({snapshot.release.pdf_pages} pages)
- EPUB: `{snapshot.release.epub_sha256}`
- Edition contract: `{snapshot.release.edition_contract_sha256}`
- Release evidence: `{snapshot.release_evidence_sha256}`

## Gate status at build time

{statuses}

## How to use

1. Verify every enclosed file with `shasum -a 256 -c SHA256SUMS.txt`.
2. Open the assignment matching the requested gate.
3. Keep private contacts, signatures and participant records outside public Git.
4. Return only the bounded, sanitized evidence required by the named protocol.
5. Rebuild this packet if the candidate commit, PDF or EPUB changes.

This packet reduces copy and handoff errors. It does not establish rights,
reviewer competence, independence, clinical safety, beginner comprehension,
reader-app compatibility or comparative superiority.
"""


def generated_members(snapshot: PacketSnapshot) -> tuple[PacketMember, ...]:
    assignments = tuple(
        PacketMember(
            f"generated/assignments/{gate}.md",
            assignment_text(gate, snapshot).encode("utf-8"),
            "assignment",
        )
        for gate in GATE_ORDER
    )
    guide = PacketMember(
        "README.md",
        guide_text(snapshot).encode("utf-8"),
        "packet-guide",
    )
    return (guide, *assignments)


def manifest_bytes(
    snapshot: PacketSnapshot,
    members: tuple[PacketMember, ...],
) -> bytes:
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "packet_type": "external_review_coordinator",
        "packet_id": snapshot.packet_id,
        "candidate": {
            "commit": snapshot.commit,
            "edition_id": snapshot.edition.edition_id,
            "title": snapshot.edition.title,
            "language": snapshot.edition.language,
            "pdf_sha256": snapshot.release.pdf_sha256,
            "epub_sha256": snapshot.release.epub_sha256,
            "pdf_pages": snapshot.release.pdf_pages,
            "edition_contract_sha256": snapshot.release.edition_contract_sha256,
            "release_evidence_sha256": snapshot.release_evidence_sha256,
        },
        "gate_statuses": dict(snapshot.gate_statuses),
        "permitted_claims": list(snapshot.permitted_claims),
        "members": [
            {
                "archive_path": member.archive_path,
                "source_path": member.source_path,
                "role": member.role,
                "sha256": member.sha256,
            }
            for member in sorted(members, key=lambda item: item.archive_path)
        ],
        "limitations": [
            "Packet construction does not pass any external gate.",
            (
                "Machine binding does not authenticate people, authority, "
                "competence, custody, signatures, or study completeness."
            ),
            "A changed candidate commit, PDF, or EPUB requires a new packet.",
        ],
    }
    return (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
