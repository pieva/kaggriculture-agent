from __future__ import annotations

from pathlib import Path

from agricola.core.e17_ledger import E17CommandLedger, instrument_policy
from agricola.strategy.antigravity.antigravity_e17_native_3q import (
    E17_NATIVE_MODEL_SPEC_VERSION,
    create_e17_native_agent,
)


REPO_ROOT = Path(__file__).resolve().parents[5]
SOURCE_PATH = (
    REPO_ROOT
    / "src"
    / "agricola"
    / "strategy"
    / "antigravity"
    / "antigravity_e17_native_3q.py"
)


def _observation(*, step: int, day: int, hour: int, farmer: list[int], money: float, unlocked: list[str], seeds: dict[str, int], tiles=None):
    if tiles is None:
        tiles = [[None for _ in range(10)] for _ in range(10)]
    return {
        "step": step,
        "day": day,
        "hour": hour,
        "player": 0,
        "farms": [
            {
                "money": money,
                "farmer": farmer,
                "hands": [],
                "tiles": tiles,
                "unlocked_quadrants": unlocked,
            }
        ],
        "private": {"shed": {}, "seeds": seeds, "inventories": [{}]},
        "market": {"prices": {"CARROT": 35, "WHEAT": 15}},
    }


def test_native_policy_has_no_foreign_strategy_imports() -> None:
    text = SOURCE_PATH.read_text(encoding="utf-8")
    assert "agricola.strategy.codex" not in text
    assert "agricola.strategy.copilot" not in text
    assert "ROUTINE_ACTIONS" not in text


def test_native_policy_uses_distinct_routine_fingerprint() -> None:
    policy = create_e17_native_agent(
        run_context={"run_id": "test", "episode_id": "test", "seed": 26090101, "player_position": 0}
    )
    instance = policy.antigravity_e17_native_instance
    assert instance.model_spec_version == E17_NATIVE_MODEL_SPEC_VERSION
    assert instance.routine_hash != "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"


def test_native_policy_unlocks_q1_immediately_with_single_market_order() -> None:
    policy = create_e17_native_agent(
        run_context={"run_id": "test", "episode_id": "test", "seed": 26090101, "player_position": 0}
    )
    action = policy(
        _observation(
            step=0,
            day=0,
            hour=0,
            farmer=[4, 4],
            money=3000.0,
            unlocked=["NW"],
            seeds={"CARROT": 0, "WHEAT": 0},
        )
    )
    assert action["market"] == [["BUY_LAND"]]
    assert action["hands"] == []


def test_native_policy_unlocks_q2_immediately_after_q1_when_cash_allows() -> None:
    policy = create_e17_native_agent(
        run_context={"run_id": "test", "episode_id": "test", "seed": 26090101, "player_position": 0}
    )
    action = policy(
        _observation(
            step=1,
            day=0,
            hour=1,
            farmer=[4, 4],
            money=2000.0,
            unlocked=["NW", "NE"],
            seeds={"CARROT": 0, "WHEAT": 0},
        )
    )
    assert action["market"] == [["BUY_LAND"]]
    assert action["hands"] == []


def test_native_policy_is_ledger_compatible() -> None:
    policy = create_e17_native_agent(
        run_context={"run_id": "test", "episode_id": "test", "seed": 26090101, "player_position": 0}
    )
    ledger = E17CommandLedger(
        {
            "episode_id": "E17-ANTIGRAVITY-TEST",
            "seed": 26090101,
            "seat": 0,
            "player_id": 0,
            "policy_version": E17_NATIVE_MODEL_SPEC_VERSION,
            "source_hash": "SOURCE",
            "config_hash": "CONFIG",
            "routine_hash": policy.antigravity_e17_native_instance.routine_hash,
        }
    )
    wrapped = instrument_policy(policy, ledger)
    obs0 = _observation(
        step=0,
        day=0,
        hour=0,
        farmer=[4, 4],
        money=3000.0,
        unlocked=["NW"],
        seeds={"CARROT": 1},
    )
    action0 = wrapped(obs0)
    obs1 = _observation(
        step=1,
        day=0,
        hour=1,
        farmer=[4, 4],
        money=3000.0,
        unlocked=["NW"],
        seeds={"CARROT": 0},
        tiles=[[None for _ in range(10)] for _ in range(10)],
    )
    ledger.record(obs1, {"farmer": ["PASS"], "hands": [], "market": []})
    ledger.finalize(obs1)
    assert action0["hands"] == []
    assert ledger.metrics()["ledger_record_coverage"] == 1.0
