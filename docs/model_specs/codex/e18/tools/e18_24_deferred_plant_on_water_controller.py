#!/usr/bin/env python3
"""E18.24 recovers D11 locked plants on later planned WATER visits."""

from __future__ import annotations

from collections import Counter
from typing import Any

from docs.model_specs.codex.e18.tools.e18_22_wheat_jit_d1_controller import (
    WheatJitD1Controller,
)


class DeferredPlantOnWaterController(WheatJitD1Controller):
    """Turn an invalid WATER slot into its deferred D11 PLANT obligation."""

    deferred_source_day = 11

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.deferred_plant_targets: dict[tuple[int, int], str] = {
            tuple(int(value) for value in row["position"]): str(
                (row.get("arguments", {}) or {})["crop"]
            )
            for row in plan["trajectory"]
            if int(row["day"]) == self.deferred_source_day
            and row["opcode"] == "PLANT"
            and int(row["position"][0]) < 5
            and int(row["position"][1]) >= 5
        }
        self.resolved_plant_targets: set[tuple[int, int]] = set()
        self.recovered_plant_targets: set[tuple[int, int]] = set()
        self.deferred_plant_metrics: Counter[str] = Counter()
        self.recovered_by_day: Counter[int] = Counter()

    def _planned_or_recovery(
        self,
        row: dict[str, Any],
        farm: dict[str, Any],
        private: dict[str, Any],
        worker: int,
        key: tuple[int, int],
    ) -> tuple[list[Any], dict[str, Any] | None]:
        position = self._position(farm, worker)
        target = tuple(int(value) for value in row.get("position", position))
        crop = self.deferred_plant_targets.get(target)
        if (
            row["opcode"] == "WATER"
            and position == target
            and crop is not None
            and target not in self.resolved_plant_targets
        ):
            tile = self._tile(farm, target)
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                self.deferred_plant_metrics["dig_before_recovered_plant"] += 1
                return ["DIG"], None
            seeds = int((private.get("seeds", {}) or {}).get(crop, 0))
            if tile is None and seeds > 0:
                self._advance(key)
                self.resolved_plant_targets.add(target)
                self.recovered_plant_targets.add(target)
                self.deferred_plant_metrics["recovered_plants"] += 1
                self.recovered_by_day[key[0]] += 1
                return ["PLANT", crop], row
            if tile is not None:
                self.deferred_plant_metrics["target_already_occupied"] += 1
                self.resolved_plant_targets.add(target)
            elif seeds <= 0:
                self.deferred_plant_metrics["recovery_seed_missing"] += 1
        return super()._planned_or_recovery(row, farm, private, worker, key)
