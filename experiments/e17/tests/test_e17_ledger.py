from __future__ import annotations

from copy import deepcopy

from agricola.core.e17_ledger import (
    E17CommandLedger,
    canonical_sha256,
    instrument_policy,
)


def _observation(*, step: int, farmer: list[int], money: float = 3000.0):
    tiles = [[None for _ in range(10)] for _ in range(10)]
    return {
        "step": step,
        "day": step // 24,
        "hour": step % 24,
        "player": 0,
        "farms": [
            {
                "money": money,
                "farmer": farmer,
                "hands": [],
                "tiles": tiles,
                "unlocked_quadrants": ["NW"],
            }
        ],
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
        "market": {},
    }


def _metadata():
    return {
        "episode_id": "E17-TEST",
        "seed": 1,
        "seat": 0,
        "policy_version": "TEST",
        "source_hash": "SOURCE",
        "config_hash": "CONFIG",
        "routine_hash": "ROUTINE",
    }


def test_canonical_hash_is_order_independent_for_mapping_keys() -> None:
    assert canonical_sha256({"b": 2, "a": 1}) == canonical_sha256({"a": 1, "b": 2})


def test_ledger_records_every_emitted_command_and_keeps_market_ambiguity() -> None:
    ledger = E17CommandLedger(_metadata())
    ledger.record(
        _observation(step=0, farmer=[4, 4]),
        {
            "farmer": ["EAST"],
            "hands": [],
            "market": [["BUY_SEED", "WHEAT", 2], ["BUY_PRODUCT", "WHEAT", 1]],
        },
    )
    ledger.record(
        _observation(step=1, farmer=[5, 4], money=2975.0),
        {"farmer": ["PASS"], "hands": [], "market": []},
    )
    ledger.finalize(_observation(step=2, farmer=[5, 4], money=2975.0))

    metrics = ledger.metrics()
    assert metrics["ledger_records"] == 4
    assert metrics["emitted_commands"] == 4
    assert metrics["ledger_record_coverage"] == 1.0
    assert len({record["command_id"] for record in ledger.records}) == 4
    assert ledger.records[0]["outcome"] == "EXECUTED"
    assert [record["outcome"] for record in ledger.records[1:3]] == [
        "UNKNOWN",
        "UNKNOWN",
    ]
    assert ledger.records[-1]["outcome"] == "EXECUTED"


def test_instrumentation_returns_the_exact_policy_action() -> None:
    emitted = {"farmer": ["PASS"], "hands": [], "market": []}

    def policy(observation, configuration=None):
        del observation, configuration
        return deepcopy(emitted)

    ledger = E17CommandLedger(_metadata())
    wrapped = instrument_policy(policy, ledger)
    returned = wrapped(_observation(step=0, farmer=[4, 4]))

    assert returned == emitted
    assert returned is not emitted
    assert ledger.action_batches[0]["action"] == emitted
    assert ledger.errors == []
