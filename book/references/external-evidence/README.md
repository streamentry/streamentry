# Public external evidence only

This directory is reserved for privacy-safe, signed or publicly verifiable evidence that closes or fails one gate in `external-release-gates.json`.

Allowed:

- signed rights decisions with private contact details removed;
- doctrinal and clinical-safety reports;
- scorer-produced beginner aggregate and reader-app reports;
- external preregistration or timestamp receipts;
- privacy-safe EPUB environment and defect summaries;
- comparative preregistration and aggregate results.

Never place here:

- raw beginner manifests or attempt records;
- first answers, free-text participant notes or direct identifiers;
- personalized device names, account names, hostnames or private contact routes;
- unredacted contracts, identity documents, medical records or signatures that the signer did not authorize for publication;
- copyrighted comparator text, scans or screenshots.

Each gate report must include:

```text
Gate status: PASSED | FAILED
Evidence role: <canonical_role>
Candidate commit: <40 lowercase hex>
PDF SHA-256: <64 lowercase hex>
EPUB SHA-256: <64 lowercase hex>
Completed:
Signer or verifiable public confirmation:
What this evidence does not establish:
```

`Completed:` must contain one real ISO date. `Signer or verifiable public confirmation:` must identify the public confirmation mechanism without exposing a private contact route. `What this evidence does not establish:` must state the scope limit. The `Evidence role:`, `PDF SHA-256:`, and `EPUB SHA-256:` lines must each appear exactly once. The role and both digests must match the registry and current candidate record. Public evidence containing a likely private email address or phone number is rejected.

The frozen `Candidate commit` need not be the commit that later adds this evidence or updates `release-evidence.md`. It must be a 40-character ancestor of the evidence commit and must itself contain the exact PDF and EPUB bytes named by the current release record.

For `aggregate_report`, also require exactly one `Cohort ID:`, one `Manifest SHA-256:`, and exactly five distinct `Counted record SHA-256:` lines. For `reader_app_report`, require the same cohort ID and manifest hash plus exactly one counted-record hash drawn from those five. Generate these two role-specific files with the scorer's `--output` and `--epub-evidence-output` options. Their deterministic bindings do not authenticate the reader or moderator and do not independently prove preregistration time, public-history freshness, or that no attempt was omitted.

For `rights_decision`, include every exact field in the machine-readable summary
of [`../rights-decision-template.md`](../rights-decision-template.md). A passed
record must authorize both PDF and EPUB, bind the current rights-inventory and
immutable-manuscript hashes, resolve the contributor chain and third-party
materials, and record no unresolved rights item. The verifier checks this
structure and its internal consistency. It does not authenticate the signer or
establish that the asserted ownership, assignment, licence, jurisdictional
analysis, or third-party resolution is legally valid.

Canonical roles are gate-specific: `rights_decision`; `doctrinal_review_report`; `clinical_safety_review_report`; `aggregate_report`; `preregistration_receipt`; `public_history_confirmation`; `privacy_review_confirmation`; `reader_app_report`; `comparative_results`.

Use one descriptive filename per evidence role such as `doctrinal-review-2026-07-15.md`. A passed or failed gate must list every public evidence file in the registry with its `path`, `sha256`, and `role`. Unsupported roles, duplicate singleton roles, reused file paths, stale hashes, or one generic file pretending to close multiple roles are rejected. The machine verifier checks paths, hashes, candidate binding, role lines, and required-role coverage. A human steward still verifies identity, qualifications, authority, signature, confidentiality and substantive findings.
