"""Canonical repository paths after the agent-material migration."""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path


MIGRATION_MANIFEST = (
    Path(__file__).resolve().parents[3]
    / "docs/model_specs/AGENT_MATERIAL_MIGRATION_2026_09_04.json"
)
_AGENTS = frozenset({"antigravity", "claude", "codex", "copilot"})
_DIRECT_CATEGORIES = frozenset(
    {"candidates", "configs", "design", "prompts", "reports", "reviews", "tools"}
)
_ARTIFACT_KINDS = frozenset({"derived", "discovery", "freeze", "runs"})


@lru_cache(maxsize=1)
def _migration() -> dict:
    return json.loads(MIGRATION_MANIFEST.read_text(encoding="utf-8"))


def canonical_relative_path(relative_path: str) -> str:
    """Map a live pre-migration agent path to its canonical relative path."""

    normalized = relative_path.replace("\\", "/")
    parts = normalized.split("/")
    if len(parts) < 5 or parts[0] != "experiments" or parts[1] not in {"e17", "e18"}:
        return normalized
    round_id = parts[1]
    if parts[2] in _DIRECT_CATEGORIES and parts[3] in _AGENTS:
        return "/".join(
            ["docs", "model_specs", parts[3], round_id, parts[2], *parts[4:]]
        )
    if (
        len(parts) >= 6
        and parts[2] == "artifacts"
        and parts[3] in _ARTIFACT_KINDS
        and parts[4] in _AGENTS
    ):
        return "/".join(
            [
                "docs",
                "model_specs",
                parts[4],
                round_id,
                "artifacts",
                parts[3],
                *parts[5:],
            ]
        )
    return normalized


def canonical_repository_path(repository_root: Path, relative_path: str) -> Path:
    return repository_root / canonical_relative_path(relative_path)


def expected_current_sha256(relative_path: str, historical_sha256: str) -> str:
    """Return the attested current hash while retaining the historical hash."""

    normalized = relative_path.replace("\\", "/")
    entry = _migration()["source_rewrites"].get(normalized)
    if entry is None:
        return historical_sha256
    if entry["sha256_before"] != historical_sha256:
        raise ValueError(f"historical SHA-256 mismatch for {normalized}")
    return str(entry["sha256_after"])


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def verify_migrated_source(
    repository_root: Path,
    relative_path: str,
    historical_sha256: str,
) -> bool:
    path = canonical_repository_path(repository_root, relative_path)
    return sha256_file(path) == expected_current_sha256(
        relative_path,
        historical_sha256,
    )
