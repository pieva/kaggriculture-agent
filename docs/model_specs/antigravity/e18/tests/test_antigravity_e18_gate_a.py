"""Pytest test suite for Antigravity E18 Gate A contract compliance."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
GATE_A_ARTIFACT = (
    ROOT
    / "docs"
    / "model_specs"
    / "antigravity"
    / "e18"
    / "artifacts"
    / "derived"
    / "E18_ANTIGRAVITY_REACTIVE_V1_GATE_A.json"
)


def test_gate_a_artifact_exists_and_passes() -> None:
    assert GATE_A_ARTIFACT.exists(), "Gate A artifact does not exist yet; run run_antigravity_e18_gate_a.py"
    data = json.loads(GATE_A_ARTIFACT.read_text(encoding="utf-8"))

    assert data["gate"] == "GATE_A_ENGINE_CONTRACT_AUDIT"
    assert data["passed"] is True, f"Gate A failed checks: {data.get('checks')}"
    checks = data["checks"]
    assert checks["all_runs_720_steps"] is True
    assert checks["zero_errors"] is True
    assert checks["zero_fallbacks"] is True
    assert checks["chain_observed_all_runs"] is True
    assert checks["productive_actions_positive"] is True
    assert checks["peak_crops_positive"] is True
    assert checks["money_gt_2840_at_least_once"] is True
    assert len(data["runs"]) == 6
