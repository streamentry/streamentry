#!/usr/bin/env python3
"""Build the deterministic coordinator packet for all external release gates."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from beginner_pilot_artifact import sha256_file
from edition_contract import load_edition_contract
from external_review_packet import build_packet, clean_head
from release_common import ReleaseVerificationError


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        edition = load_edition_contract(root / "book" / "edition.json")
        commit = clean_head(root)
        default = (
            root
            / "build"
            / "external-review-packet"
            / f"{edition.file_stem}-external-review-{commit[:12]}.zip"
        )
        requested = args.output or default
        output = requested if requested.is_absolute() else root / requested
        snapshot = build_packet(root, output)
    except (OSError, ValueError, zipfile.BadZipFile, ReleaseVerificationError) as error:
        print(f"External review packet failed: {error}", file=sys.stderr)
        raise SystemExit(2) from error
    print(f"Built {output.relative_to(root)}")
    print(f"Packet ID: {snapshot.packet_id}")
    print(f"SHA-256: {sha256_file(output)}")
    print(f"Size: {output.stat().st_size} bytes")


if __name__ == "__main__":
    main()
