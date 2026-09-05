from __future__ import annotations

from typing import Any

from docs.model_specs.codex.e18.tools.e18_19_retrying_trajectory_controller import (
    RetryingTrajectoryController,
)


def _plan(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "trajectory": [row],
        "daily": [{"day": 1, "planned_hands": 0}],
    }


def _row(opcode: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "step": 1,
        "day": 1,
        "turn": 1,
        "worker": 0,
        "opcode": opcode,
        "arguments": arguments or {},
        "position": [1, 1],
    }


def _farm(tile: Any) -> dict[str, Any]:
    tiles = [[None for _ in range(10)] for _ in range(10)]
    tiles[1][1] = tile
    return {"farmer": [1, 1], "hands": [], "tiles": tiles}


def test_weed_is_dug_then_plant_is_retried() -> None:
    controller = RetryingTrajectoryController(
        _plan(_row("PLANT", {"crop": "WHEAT"}))
    )
    private = {"seeds": {"WHEAT": 1}, "inventories": [{}], "shed": {}}

    command, planned = controller._worker_command(
        1, 1, 0, _farm({"kind": "WEED"}), private
    )
    assert command == ["DIG"]
    assert planned is None
    assert controller.cursors[(1, 0)] == 0

    command, planned = controller._worker_command(1, 2, 0, _farm(None), private)
    assert command == ["PLANT", "WHEAT"]
    assert planned is not None
    assert controller.cursors[(1, 0)] == 1


def test_partial_pickup_has_one_bounded_residual_retry() -> None:
    controller = RetryingTrajectoryController(
        _plan(_row("PICKUP", {"item": "WHEAT", "units": 4}))
    )
    farm = _farm(None)

    command, _ = controller._worker_command(
        1,
        1,
        0,
        farm,
        {"seeds": {}, "inventories": [{}], "shed": {"WHEAT": 2}},
    )
    assert command == ["PICKUP", "WHEAT", 2]
    assert controller.cursors[(1, 0)] == 0

    command, _ = controller._worker_command(
        1,
        2,
        0,
        farm,
        {"seeds": {}, "inventories": [{"WHEAT": 2}], "shed": {}},
    )
    assert command == ["PASS"]
    assert controller.cursors[(1, 0)] == 0

    command, _ = controller._worker_command(
        1,
        3,
        0,
        farm,
        {"seeds": {}, "inventories": [{"WHEAT": 2}], "shed": {}},
    )
    assert command == ["PASS"]
    assert controller.cursors[(1, 0)] == 1
    assert controller.skipped_stale["PICKUP"] == 1
