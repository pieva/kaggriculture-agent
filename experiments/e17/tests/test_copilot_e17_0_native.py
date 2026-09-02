from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

from agricola.core.e17_ledger import E17CommandLedger, instrument_policy
from agricola.strategy.copilot.e17_native_3q import (
    DEFAULT_CONFIG_PATH,
    POLICY_VERSION,
    create_native_agent,
    native_policy_fingerprint,
)

CODEX_ROUTINE_SHA256 = (
    "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"
)
SOURCE_PATH = Path(__file__).resolve().parents[3] / "src" / "agricola" / "strategy" / "copilot" / "e17_native_3q.py"


def _observation(*, step: int = 0, unlocked: tuple[str, ...] = ("NW",)):
    tiles = []
    for y in range(10):
        row = []
        for x in range(10):
            quadrant = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
            row.append(None if quadrant in unlocked else "LOCKED")
        tiles.append(row)
    farm = {
        "money": 3000.0,
        "farmer": [4, 4],
        "hands": [],
        "tiles": tiles,
        "unlocked_quadrants": list(unlocked),
        "hires_today": 0,
    }
    return {
        "step": step,
        "day": step // 24,
        "hour": step % 24,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {
            "shed": {"WHEAT": 0},
            "seeds": {"WHEAT": 0},
            "inventories": [{}],
        },
        "market": {"inventory": {}, "prices": {}},
    }


def test_native_source_has_no_other_agent_strategy_dependency() -> None:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    assert not any(
        name.startswith("agricola.strategy.codex")
        or name.startswith("agricola.strategy.antigravity")
        for name in imported
    )
    assert "ROUTINE_ACTIONS" not in source
    assert "codex_v9_routine_data" not in source


def test_config_is_native_three_quadrant_and_holdout_remains_unconsumed() -> None:
    policy = create_native_agent(DEFAULT_CONFIG_PATH)
    assert policy.config.policy_id == POLICY_VERSION
    assert policy.config.target_quadrants == 3
    config_text = DEFAULT_CONFIG_PATH.read_text(encoding="utf-8")
    assert '"holdout_consumed": false' in config_text
    assert '"final_confirmation_consumed": false' in config_text


def test_native_fingerprint_is_distinct_from_codex_routine() -> None:
    fingerprint = native_policy_fingerprint()
    assert len(fingerprint) == 64
    assert fingerprint != CODEX_ROUTINE_SHA256


def test_policy_is_deterministic_and_requests_native_opening() -> None:
    observation = _observation()
    first = create_native_agent()(deepcopy(observation), {"episodeSteps": 720})
    second = create_native_agent()(deepcopy(observation), {"episodeSteps": 720})
    assert first == second
    assert first["farmer"] == ["PASS"]
    assert ["BUY_LAND"] in first["market"]
    assert ["BUY_SEED", "WHEAT", 18] in first["market"]
    assert first["market"].count(["HIRE"]) == 5


def test_ledger_covers_every_native_command_without_affecting_action() -> None:
    observation = _observation()
    policy = create_native_agent()
    ledger = E17CommandLedger(
        {
            "episode_id": "E17-0-COPILOT-UNIT",
            "seed": 26090101,
            "seat": 0,
            "policy_version": POLICY_VERSION,
            "source_hash": "SOURCE",
            "config_hash": "CONFIG",
            "routine_hash": native_policy_fingerprint(),
        }
    )
    wrapped = instrument_policy(policy, ledger)
    action = wrapped(observation, {"episodeSteps": 720})
    expected_commands = 1 + len(action["hands"]) + len(action["market"])
    assert len(ledger.records) == expected_commands
    assert ledger.metrics()["ledger_record_coverage"] == 1.0
    assert wrapped.e17_inner_policy is policy
    assert policy.technical_errors == 0
