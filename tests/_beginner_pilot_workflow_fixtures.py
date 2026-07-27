from __future__ import annotations

import shutil
import subprocess
from contextlib import contextmanager
from typing import Any

from _beginner_pilot_v2_fixtures import (
    CANONICAL_REMOTE_REF,
    ROOT,
    temp_artifact_repo,
)


WORKFLOW_SUPPORT_PATHS = (
    "book/edition.json",
    "scripts/beginner_pilot_preparation.py",
    "scripts/beginner_pilot_workflow.py",
    "scripts/edition_contract.py",
    "scripts/edition_contract_validation.py",
    "scripts/prepare-beginner-pilot.py",
)


@contextmanager
def workflow_artifact_repo() -> Any:
    with temp_artifact_repo() as ctx:
        repo_root = ctx["repo_root"]
        for relative_path in WORKFLOW_SUPPORT_PATHS:
            source = ROOT / relative_path
            target = repo_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        subprocess.run(
            ["git", "add", *WORKFLOW_SUPPORT_PATHS],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "add pilot workflow fixture"],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        subprocess.run(
            ["git", "update-ref", CANONICAL_REMOTE_REF, head],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
        ctx["artifact"]["git_commit"] = head
        yield ctx
