"""Prevent source-code collisions across parallel editorial changes.

These checks verify traceability structure, not the truth of a doctrinal claim.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAP = ROOT / "book/chapters/99-nguon.typ"
LEDGER = ROOT / "book/references/claim-ledger.md"


class SourceRegistryIntegrityTests(unittest.TestCase):
    def test_canonical_source_codes_are_unique_complete_and_ordered(self) -> None:
        text = SOURCE_MAP.read_text(encoding="utf-8")
        codes = re.findall(r"#reference-item\(\s*\[(K\d{2})\]", text)
        self.assertEqual(codes, [f"K{i:02d}" for i in range(1, 54)])
        self.assertIn("*K01–K53*", text)

    def test_checklist_and_aggregate_sources_keep_distinct_bindings(self) -> None:
        text = SOURCE_MAP.read_text(encoding="utf-8")
        blocks = re.split(r"(?=#reference-item\()", text)
        entries = {}
        for block in blocks:
            match = re.match(r"#reference-item\(\s*\[(K\d{2})\]", block)
            if match:
                entries[match.group(1)] = block
        self.assertIn("/SN22_82.html", entries["K45"])
        self.assertNotIn("/SN22_48.html", entries["K45"])
        self.assertIn("/SN22_48.html", entries["K53"])
        self.assertNotIn("/SN22_82.html", entries["K53"])
        for code in (f"K{i:02d}" for i in range(46, 53)):
            self.assertIn(code, entries)

    def test_claim_identifiers_are_unique_and_preserve_both_audits(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        codes = re.findall(r"^\| (C\d{2}) \|", text, re.MULTILINE)
        self.assertEqual(codes, [f"C{i:02d}" for i in range(1, 94)])
        rows = {line.split("|")[1].strip(): line for line in text.splitlines()
                if re.match(r"^\| C\d{2} \|", line)}
        self.assertIn("SN 22.82", rows["C81"])
        self.assertIn("SN 22.48", rows["C91"])
        self.assertIn("K53", rows["C91"])

    def test_every_reader_facing_canonical_code_resolves(self) -> None:
        text = SOURCE_MAP.read_text(encoding="utf-8")
        declared = set(re.findall(r"#reference-item\(\s*\[(K\d{2})\]", text))
        for directory in (ROOT / "book/chapters", ROOT / "book/appendices"):
            for path in sorted(directory.glob("*.typ")):
                used = set(re.findall(r"\bK\d{2}\b", path.read_text(encoding="utf-8")))
                with self.subTest(path=path.relative_to(ROOT).as_posix()):
                    self.assertFalse(used - declared, sorted(used - declared))


if __name__ == "__main__":
    unittest.main()
