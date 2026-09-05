from __future__ import annotations

from docs.model_specs.codex.e18.tools.e18_24_deferred_plant_on_water_controller import (
    DeferredPlantOnWaterController,
)


def test_deferred_targets_are_derived_only_from_d11_sw_plants() -> None:
    plan = {
        "trajectory": [
            {
                "day": 11,
                "opcode": "PLANT",
                "position": [3, 6],
                "arguments": {"crop": "STRAWBERRY"},
            },
            {
                "day": 11,
                "opcode": "PLANT",
                "position": [6, 3],
                "arguments": {"crop": "WHEAT"},
            },
            {
                "day": 12,
                "opcode": "PLANT",
                "position": [2, 7],
                "arguments": {"crop": "WHEAT"},
            },
        ]
    }
    controller = object.__new__(DeferredPlantOnWaterController)
    controller.deferred_source_day = 11
    targets = {
        tuple(row["position"]): row["arguments"]["crop"]
        for row in plan["trajectory"]
        if row["day"] == controller.deferred_source_day
        and row["opcode"] == "PLANT"
        and row["position"][0] < 5
        and row["position"][1] >= 5
    }

    assert targets == {(3, 6): "STRAWBERRY"}
