"""Integrity checks for the frozen E18.4 V1 development result."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ARTIFACT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_4_STATE_DRIVEN_772_DEV_GATE_V1.json"
)


def test_e18_4_gate_is_complete_and_rejected_without_reserved_seeds() -> None:
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["match_count"] == 14
    assert payload["holdout_consumed"] is False
    assert payload["final_confirmation_consumed"] is False
    assert payload["candidate_gate"]["passed"] is False
    assert payload["candidate_gate"]["exact_topology_matches"] == 14
    assert payload["candidate_gate"]["fully_filled_matches"] == 14
    assert payload["standings"]["CODEX_E18_4_STATE_DRIVEN_772"][
        "verified_livestock_losses"
    ] == 0

