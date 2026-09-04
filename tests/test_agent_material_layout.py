"""Repository contract for agent-owned model material."""

from __future__ import annotations

import json
from pathlib import Path

from agricola.core.repository_paths import (
    MIGRATION_MANIFEST,
    canonical_relative_path,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]
AGENTS = {"antigravity", "claude", "codex", "copilot"}


def test_experiments_has_no_agent_owned_directories() -> None:
    offenders = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "experiments").rglob("*")
        if path.is_dir() and path.name.casefold() in AGENTS
    )
    assert offenders == []


def test_legacy_live_paths_resolve_to_model_spec_namespaces() -> None:
    assert canonical_relative_path(
        "experiments/e18/configs/codex/CODEX_E18.json"
    ) == "docs/model_specs/codex/e18/configs/CODEX_E18.json"
    assert canonical_relative_path(
        "experiments/e17/artifacts/freeze/claude/FREEZE.json"
    ) == "docs/model_specs/claude/e17/artifacts/freeze/FREEZE.json"
    assert canonical_relative_path(
        "experiments/e18/reports/common/SHARED.md"
    ) == "experiments/e18/reports/common/SHARED.md"


def test_migration_attestation_matches_current_sources() -> None:
    migration = json.loads(MIGRATION_MANIFEST.read_text(encoding="utf-8"))
    assert migration["historical_hash_policy"] == (
        "PRESERVE_PRE_MIGRATION_HASH_AND_ATTEST_PATH_ONLY_REWRITE"
    )
    for relative_path, hashes in migration["source_rewrites"].items():
        assert hashes["sha256_before"] != hashes["sha256_after"]
        assert sha256_file(ROOT / relative_path) == hashes["sha256_after"]
