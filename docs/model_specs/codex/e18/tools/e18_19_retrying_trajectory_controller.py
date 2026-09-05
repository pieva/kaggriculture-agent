#!/usr/bin/env python3
"""State-recovering executor for the fixed E18.18 7-7-0 trajectory.

E18.18 proved the plan in the weed-free oracle but discarded a planned task
whenever its state guard rejected it.  This controller keeps one ordered daily
queue per worker.  A rejected critical task remains at the head of the queue;
the worker first repairs position or tile state and then retries it.  Planned
PASS slots that are already due are consumed as slack, so a short recovery does
not necessarily move the remainder of the mission past turn 24.

This module is a development controller.  It deliberately reuses the frozen
E18.18 planner and market policy so that Gate-1 measures only execution
recovery, not a simultaneous change to composition or economics.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from typing import Any

from docs.model_specs.codex.e18.tools.run_e18_18_770_capacity_trajectory_gate_0b import (
    SAFE_PASS,
    Gate0BController,
    _farm,
)

MOVES: dict[str, tuple[int, int]] = {
    "NORTH": (0, -1),
    "SOUTH": (0, 1),
    "EAST": (1, 0),
    "WEST": (-1, 0),
}
class RetryingTrajectoryController(Gate0BController):
    """Execute the E18.18 plan as recoverable, state-aware worker queues."""

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.routes: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
        for row in plan["trajectory"]:
            self.routes[(int(row["day"]), int(row["worker"]))].append(row)
        for rows in self.routes.values():
            rows.sort(key=lambda row: (int(row["turn"]), int(row["step"])))
        self.cursors: dict[tuple[int, int], int] = defaultdict(int)
        self.pickup_remaining: dict[tuple[int, int, int], int] = {}
        self.wait_counts: Counter[tuple[int, int, int, str]] = Counter()
        self.recovery_actions: Counter[str] = Counter()
        self.deferred_critical: Counter[str] = Counter()
        self.skipped_stale: Counter[str] = Counter()
        self.unfinished_by_day: dict[int, int] = {}
        self._last_day = 0

    @staticmethod
    def _inventory(private: dict[str, Any], worker: int) -> Counter[str]:
        inventories = private.get("inventories", []) or []
        if worker >= len(inventories):
            return Counter()
        return Counter(inventories[worker] or {})

    @staticmethod
    def _position(farm: dict[str, Any], worker: int) -> tuple[int, int] | None:
        positions = [farm.get("farmer", [4, 4]), *(farm.get("hands", []) or [])]
        if worker >= len(positions):
            return None
        return tuple(int(value) for value in positions[worker])

    @staticmethod
    def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
        x, y = position
        rows = farm.get("tiles", []) or []
        if not 0 <= y < len(rows) or not 0 <= x < len(rows[y]):
            return "LOCKED"
        return rows[y][x]

    @staticmethod
    def _move_toward(
        position: tuple[int, int], target: tuple[int, int]
    ) -> tuple[list[str], bool]:
        x, y = position
        tx, ty = target
        if x < tx:
            return ["EAST"], x + 1 == tx and y == ty
        if x > tx:
            return ["WEST"], x - 1 == tx and y == ty
        if y < ty:
            return ["SOUTH"], x == tx and y + 1 == ty
        if y > ty:
            return ["NORTH"], x == tx and y - 1 == ty
        return ["PASS"], True

    def _advance(self, key: tuple[int, int]) -> None:
        self.cursors[key] += 1

    def _bounded_defer(
        self,
        key: tuple[int, int],
        opcode: str,
        *,
        max_waits: int = 1,
    ) -> None:
        wait_key = (*key, self.cursors[key], opcode)
        if self.wait_counts[wait_key] < max_waits:
            self.wait_counts[wait_key] += 1
            self.deferred_critical[opcode] += 1
            return
        self.skipped_stale[opcode] += 1
        self._advance(key)

    def _remaining(
        self,
        day: int,
        turn: int,
        requirement_kind: str,
        *,
        include_tomorrow: bool,
    ) -> Counter[str]:
        del turn
        needed = self._pending_requirements(day, requirement_kind)
        if include_tomorrow:
            needed.update(
                self.requirements.get(day + 1, {}).get(requirement_kind, {})
            )
        return needed

    def _remaining_horizon(
        self,
        day: int,
        turn: int,
        requirement_kind: str,
        *,
        horizon_days: int,
    ) -> Counter[str]:
        del turn
        needed = self._pending_requirements(day, requirement_kind)
        for horizon_day in range(day + 1, min(30, day + horizon_days) + 1):
            needed.update(
                self.requirements.get(horizon_day, {}).get(requirement_kind, {})
            )
        return needed

    def _pending_requirements(
        self, day: int, requirement_kind: str
    ) -> Counter[str]:
        opcode = "PICKUP" if requirement_kind == "pickup" else "PLANT"
        argument = "item" if opcode == "PICKUP" else "crop"
        needed: Counter[str] = Counter()
        for key, rows in self.routes.items():
            if key[0] != day:
                continue
            for index, row in enumerate(
                rows[self.cursors[key] :], start=self.cursors[key]
            ):
                if row["opcode"] != opcode:
                    continue
                args = row.get("arguments", {}) or {}
                units = int(args.get("units", 1))
                if opcode == "PICKUP":
                    units = self.pickup_remaining.get((*key, index), units)
                needed[str(args[argument])] += units
        return needed

    def _planned_or_recovery(
        self,
        row: dict[str, Any],
        farm: dict[str, Any],
        private: dict[str, Any],
        worker: int,
        key: tuple[int, int],
    ) -> tuple[list[Any], dict[str, Any] | None]:
        opcode = str(row["opcode"])
        position = self._position(farm, worker)
        if position is None:
            return ["PASS"], None
        target = tuple(int(value) for value in row.get("position", position))

        if opcode in MOVES:
            if position == target:
                self._advance(key)
                return ["PASS"], None
            command, reaches_target = self._move_toward(position, target)
            if reaches_target:
                self._advance(key)
            index = self.cursors[key] - int(reaches_target)
            expected_origin = (
                tuple(self.routes[key][index - 1]["position"])
                if index > 0
                else (4, 4)
            )
            metric = (
                "PLANNED_MOVE"
                if position == expected_origin
                else "POSITION_CORRECTION"
            )
            self.recovery_actions[metric] += 1
            return command, None

        if position != target:
            command, _ = self._move_toward(position, target)
            self.recovery_actions["POSITION_CORRECTION"] += 1
            return command, None

        command = self._unit_command(row)
        args = row.get("arguments", {}) or {}
        inventory = self._inventory(private, worker)
        shed = Counter(private.get("shed", {}) or {})
        tile = self._tile(farm, position)

        if opcode == "PICKUP":
            item = str(args["item"])
            pickup_key = (*key, self.cursors[key])
            units = self.pickup_remaining.get(
                pickup_key, int(args.get("units", 1))
            )
            available = int(shed.get(item, 0))
            if available <= 0 and item == "FERTILIZER":
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
            if available <= 0:
                self._bounded_defer(key, opcode)
                return ["PASS"], None
            picked = min(units, available)
            command = ["PICKUP", item, picked]
            if picked < units and item != "FERTILIZER":
                self.pickup_remaining[pickup_key] = units - picked
                self.recovery_actions["PARTIAL_PICKUP"] += 1
                return command, row
            self.pickup_remaining.pop(pickup_key, None)
        elif opcode == "PLANT":
            crop = str(args["crop"])
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                self.recovery_actions["DIG_BEFORE_PLANT"] += 1
                return ["DIG"], None
            if tile is not None or int(
                (private.get("seeds", {}) or {}).get(crop, 0)
            ) <= 0:
                self._bounded_defer(key, opcode)
                return ["PASS"], None
        elif opcode == "BUILD_PASTURE":
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                self.recovery_actions["DIG_BEFORE_BUILD"] += 1
                return ["DIG"], None
            if tile is not None:
                self._bounded_defer(key, opcode)
                return ["PASS"], None
        elif opcode == "PLACE":
            animal = str(args["animal"])
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                self.recovery_actions["DIG_BEFORE_PLACE"] += 1
                return ["DIG"], None
            if tile is None:
                self.recovery_actions["BUILD_BEFORE_PLACE"] += 1
                return ["BUILD_PASTURE"], None
            valid_pasture = (
                isinstance(tile, dict)
                and tile.get("kind") == "PASTURE"
                and "animal" not in tile
            )
            if not valid_pasture or int(inventory.get(animal, 0)) <= 0:
                self._bounded_defer(key, opcode)
                return ["PASS"], None
        elif opcode == "FEED":
            if not isinstance(tile, dict) or "animal" not in tile:
                self._bounded_defer(key, opcode, max_waits=0)
                return ["PASS"], None
            if bool(tile.get("fed_today")):
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
            if int(inventory.get("WHEAT", 0)) <= 0:
                # Wheat in the shed cannot reach a worker already at pasture
                # without abandoning the route.  Skip this feed instead of
                # deadlocking all later animals in the same daily mission.
                self._bounded_defer(key, opcode, max_waits=0)
                return ["PASS"], None
        elif opcode == "WATER":
            valid = (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and not bool(tile.get("watered_today"))
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "HARVEST":
            if not isinstance(tile, dict) or int(tile.get("yield_units", 0)) <= 0:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "FERTILIZE":
            valid = (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and int(inventory.get("FERTILIZER", 0)) > 0
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "DIG":
            valid = tile is not None and not (
                isinstance(tile, dict) and "animal" in tile
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "CARE":
            valid = (
                isinstance(tile, dict)
                and "animal" in tile
                and not bool(tile.get("cared_today"))
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "COLLECT_FERTILIZER":
            valid = (
                isinstance(tile, dict)
                and "animal" in tile
                and bool(tile.get("fertilizer_available"))
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "DROP" and not any(inventory.values()):
            self.skipped_stale[opcode] += 1
            self._advance(key)
            return ["PASS"], None

        self._advance(key)
        return command, row

    def _worker_command(
        self,
        day: int,
        turn: int,
        worker: int,
        farm: dict[str, Any],
        private: dict[str, Any],
    ) -> tuple[list[Any], dict[str, Any] | None]:
        key = (day, worker)
        rows = self.routes.get(key, [])
        while self.cursors[key] < len(rows):
            row = rows[self.cursors[key]]
            if int(row["turn"]) > turn:
                return ["PASS"], None
            if row["opcode"] == "PASS":
                self._advance(key)
                continue
            command, emitted_row = self._planned_or_recovery(
                row, farm, private, worker, key
            )
            if (
                command[0] == "PASS"
                and self.cursors[key] < len(rows)
                and rows[self.cursors[key]] is not row
            ):
                # A stale optional action advances the cursor and can expose a
                # second already-due task in the same engine turn.  A critical
                # deferred task leaves the cursor unchanged and must wait.
                continue
            return command, emitted_row
        return ["PASS"], None

    def _record_finished_day(self, day: int) -> None:
        if day <= 0 or day in self.unfinished_by_day:
            return
        unfinished = 0
        for key, rows in self.routes.items():
            if key[0] == day:
                unfinished += len(rows) - self.cursors[key]
        self.unfinished_by_day[day] = unfinished

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        del configuration
        try:
            day = int(observation.get("day", 0)) + 1
            turn = int(observation.get("hour", 0)) + 1
            if day != self._last_day:
                self._record_finished_day(self._last_day)
                self._last_day = day
            farm = _farm(observation, self.seat)
            private = observation.get("private", {}) or {}
            actual_hands = len(farm.get("hands", []) or [])
            selected = [
                self._worker_command(day, turn, worker, farm, private)
                for worker in range(actual_hands + 1)
            ]
            commands = [command for command, _ in selected]
            self.requested_actions.update(command[0] for command in commands)

            # Gate0B's market bridge counts same-batch planned drops.  Expose
            # only drops that this retrying executor actually emits now, then
            # restore the immutable static lookup immediately afterwards.
            marker = object()
            prior: dict[tuple[int, int, int], object] = {}
            for worker, (command, row) in enumerate(selected):
                lookup = (day, turn, worker)
                prior[lookup] = self.actions.get(lookup, marker)
                if command[0] == "DROP" and row is not None:
                    self.actions[lookup] = row
                else:
                    self.actions.pop(lookup, None)
            try:
                market = self._market_orders(observation, day, turn)
            finally:
                for lookup, value in prior.items():
                    if value is marker:
                        self.actions.pop(lookup, None)
                    else:
                        self.actions[lookup] = value  # type: ignore[assignment]

            return {
                "farmer": commands[0] if commands else ["PASS"],
                "hands": commands[1:],
                "market": market,
            }
        except Exception as exc:  # noqa: BLE001 - fail closed and report at Gate-1
            self.error_count += 1
            self.last_error = f"{type(exc).__name__}: {exc}"
            return deepcopy(SAFE_PASS)

    def finalize_metrics(self) -> None:
        self._record_finished_day(self._last_day)
