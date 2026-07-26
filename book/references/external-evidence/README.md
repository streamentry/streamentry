# Public external evidence only

This directory is reserved for privacy-safe, signed or publicly verifiable evidence that closes or fails one gate in `external-release-gates.json`.

Allowed:

- signed rights decisions with private contact details removed;
- doctrinal and clinical-safety reports;
- scorer-produced beginner aggregate reports;
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
Candidate commit: <40 lowercase hex>
PDF SHA-256: <64 lowercase hex>
EPUB SHA-256: <64 lowercase hex>
Completed:
Signer or verifiable public confirmation:
What this evidence does not establish:
```

Use one descriptive filename such as `doctrinal-review-2026-08-15.md`. A passed or failed gate must list every public evidence file in the registry. The machine verifier checks paths, hashes and candidate binding. A human steward still verifies identity, qualifications, authority, signature, confidentiality and substantive findings.
