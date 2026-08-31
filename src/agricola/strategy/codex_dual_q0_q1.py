"""Codex V7.2 isolated dual-quadrant candidate.

Q0 preserves the verified V7.1 module.  Q1 mirrors its geometry and receives
six additional persistent operating roles after a cash- and horizon-gated
land activation.  The canonical V7.1 entry point remains unchanged.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex_compact_q0 import (
    ANIMAL_RULES,
    CODEX_COHORT_OFFSET,
    CODEX_CROP_PLAN,
    CODEX_CROP_POSITIONS,
    CODEX_CROP_ZONES,
    CODEX_PASTURE_POSITIONS,
    MOVE_ACTIONS,
    CodexC2Agent,
)
from agricola.strategy.codex_lifecycle import CodexSnapshot

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DUAL_CONFIG_PATH = (
    REPO_ROOT / "configs" / "model_spec_c2" / "CODEX_C2_DUAL_Q0_Q1_CONFIG.json"
)
DUAL_MODEL_SPEC_VERSION = "CODEX-C2-V7.2-DUAL-Q0-Q1"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def _mirror_q1(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    return 9 - x, y


Q1_CROP_ZONES: tuple[tuple[tuple[int, int], ...], ...] = tuple(
    tuple(_mirror_q1(position) for position in zone)
    for zone in CODEX_CROP_ZONES
)
Q1_CROP_POSITIONS: tuple[tuple[int, int], ...] = tuple(
    position for zone in Q1_CROP_ZONES for position in zone
)
Q1_PASTURE_POSITIONS: tuple[tuple[int, int], ...] = tuple(
    _mirror_q1(position) for position in CODEX_PASTURE_POSITIONS
)

DUAL_ROLE_SEQUENCE = (
    "FLOAT_RESERVE",
    "CROP_ZONE_0",
    "CROP_ZONE_1",
    "CROP_ZONE_2",
    "LIVESTOCK_COW_Q0",
    "LIVESTOCK_SHEEP_Q0",
    "FERTILIZER_LOGISTICS_Q0",
    "CROP_ZONE_3",
    "CROP_ZONE_4",
    "CROP_ZONE_5",
    "LIVESTOCK_COW_Q1",
    "LIVESTOCK_SHEEP_Q1",
    "FERTILIZER_LOGISTICS_Q1",
)


def load_dual_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path) if path is not None else DEFAULT_DUAL_CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("candidate_id") != "CODEX_C2_DUAL_Q":
        raise ValueError("unexpected dual candidate_id")
    if config.get("model_spec_version") != DUAL_MODEL_SPEC_VERSION:
        raise ValueError("unexpected dual model_spec_version")
    if int(config.get("quadrants_owned", 0)) != 2:
        raise ValueError("dual candidate requires Q0+Q1")
    if int(config.get("workforce_total", 0)) != len(DUAL_ROLE_SEQUENCE):
        raise ValueError("dual candidate requires thirteen total workers")
    if int(config.get("crop_working_set_target", 0)) != 36:
        raise ValueError("dual candidate requires thirty-six crop tiles")
    if int(config.get("pasture_allocation_target", 0)) != 12:
        raise ValueError("dual candidate requires twelve pastures")
    if config.get("livestock_targets") != {"COW": 6, "SHEEP": 6}:
        raise ValueError("dual candidate requires six cows and six sheep")
    return deepcopy(config)


class CodexDualQAgent(CodexC2Agent):
    """Two mirrored V7.1 modules with one shared market/logistics farmer."""

    def __init__(
        self,
        candidate_config: dict[str, Any] | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        config = deepcopy(candidate_config or load_dual_config())
        super().__init__(config, run_context=run_context)
        self.candidate_id = "CODEX_C2_DUAL_Q"
        self.model_spec_version = DUAL_MODEL_SPEC_VERSION
        self.expected_max_quadrants = 2

        self.q0_crop_positions = CODEX_CROP_POSITIONS
        self.q1_crop_positions = Q1_CROP_POSITIONS
        self.crop_zones = (*CODEX_CROP_ZONES, *Q1_CROP_ZONES)
        self.crop_positions = (*self.q0_crop_positions, *self.q1_crop_positions)
        q1_plan = {
            _mirror_q1(position): crop for position, crop in CODEX_CROP_PLAN.items()
        }
        self.crop_plan = {**CODEX_CROP_PLAN, **q1_plan}
        self.zone_by_position = {
            position: zone_id
            for zone_id, zone in enumerate(self.crop_zones)
            for position in zone
        }
        self.route_index = {
            position: route_index
            for zone in self.crop_zones
            for route_index, position in enumerate(zone)
        }
        self.cohort_offset = dict(CODEX_COHORT_OFFSET)
        self._q1_relative_cohort = {
            _mirror_q1(position): int(offset)
            for position, offset in CODEX_COHORT_OFFSET.items()
        }
        self.cohort_offset.update(
            {position: 10_000 for position in self.q1_crop_positions}
        )

        self.q0_pasture_positions = CODEX_PASTURE_POSITIONS
        self.q1_pasture_positions = Q1_PASTURE_POSITIONS
        self.pasture_positions = (
            *self.q0_pasture_positions,
            *self.q1_pasture_positions,
        )
        self.pasture_positions_by_species = {
            "COW": (
                *self.q0_pasture_positions[:3],
                *self.q1_pasture_positions[:3],
            ),
            "SHEEP": (
                *self.q0_pasture_positions[3:],
                *self.q1_pasture_positions[3:],
            ),
        }

        self.q1_activation_day: int | None = None
        self.q1_full_module_day: int | None = None
        self.q1_first_output_day: int | None = None
        self.q1_first_output_product: str | None = None
        self.q1_activation_records: list[dict[str, Any]] = []
        self._q1_activation_decisions: set[int] = set()
        self.quadrant_production: Counter[str] = Counter()
        self.quadrant_livestock_service: Counter[str] = Counter()
        self.quadrant_state_trajectory: list[dict[str, Any]] = []

    def _role_for(self, worker_id: int) -> str:
        return DUAL_ROLE_SEQUENCE[min(worker_id, len(DUAL_ROLE_SEQUENCE) - 1)]

    def _target_workforce(self, snapshot: CodexSnapshot) -> int:
        if self._owned_quadrants(snapshot.farm) < 2:
            return int(self.config["q0_workforce_total"])
        return int(self.config["workforce_total"])

    def _crop_positions_for_role(
        self, role: str
    ) -> tuple[tuple[int, int], ...]:
        if role.endswith("_Q0"):
            return self.q0_crop_positions
        if role.endswith("_Q1"):
            return self.q1_crop_positions
        return self.crop_positions

    @staticmethod
    def _role_module(role: str) -> str | None:
        if role.endswith("_Q0"):
            return "Q0"
        if role.endswith("_Q1"):
            return "Q1"
        if role.startswith("CROP_ZONE_"):
            return "Q0" if int(role.rsplit("_", 1)[1]) < 3 else "Q1"
        return None

    def _module_animal_positions(
        self, module: str, species: str
    ) -> tuple[tuple[int, int], ...]:
        positions = (
            self.q0_pasture_positions if module == "Q0" else self.q1_pasture_positions
        )
        return positions[:3] if species == "COW" else positions[3:]

    def _module_animal_tasks(
        self, snapshot: CodexSnapshot, module: str, species: str
    ) -> list[dict[str, Any]]:
        allowed = set(self._module_animal_positions(module, species))
        return [
            task
            for task in self._animal_tasks(snapshot, species)
            if tuple(task["target"]) in allowed
        ]

    def _feed_assignments(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[tuple[str, str]]:
        if role == "LIVESTOCK_COW_Q0":
            return [("Q0", "COW")]
        if role == "LIVESTOCK_SHEEP_Q0":
            return [("Q0", "SHEEP")]
        if role == "LIVESTOCK_COW_Q1":
            return [("Q1", "COW")]
        if role == "LIVESTOCK_SHEEP_Q1":
            return [("Q1", "SHEEP")]

        worker_count = len(self._positions(snapshot.farm))
        assignments: list[tuple[str, str]] = []
        if worker_count <= 4 and worker_id == 0:
            assignments.append(("Q0", "COW"))
        if worker_count <= 5:
            q0_sheep_owner = 1 if worker_count >= 2 else 0
            if worker_id == q0_sheep_owner:
                assignments.append(("Q0", "SHEEP"))
        if self._owned_quadrants(snapshot.farm) >= 2:
            if worker_count <= 10 and worker_count >= 8 and worker_id == 7:
                assignments.append(("Q1", "COW"))
            if worker_count <= 11 and worker_count >= 9 and worker_id == 8:
                assignments.append(("Q1", "SHEEP"))
        return assignments

    def _feed_tasks_for_worker(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[dict[str, Any]]:
        tasks: list[dict[str, Any]] = []
        for module, species in self._feed_assignments(
            snapshot, worker_id, role
        ):
            tasks.extend(
                task
                for task in self._module_animal_tasks(snapshot, module, species)
                if task["kind"] == "FEED"
            )
        return tasks

    def _float_reserve_candidates(
        self,
        snapshot: CodexSnapshot,
        crop_tasks: list[dict[str, Any]],
        hard_crop_tasks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        growth = [
            task
            for task in crop_tasks
            if task["kind"]
            in {"PLANT", "WEED_RECOVERY", "RETIREMENT_CLEAR"}
        ]
        pasture_growth = [
            task
            for species in ("COW", "SHEEP")
            for task in self._animal_tasks(snapshot, species)
            if task["kind"] == "BUILD_PASTURE"
        ]
        high_value = [
            task
            for task in crop_tasks
            if task["kind"] in {"HARVEST", "WATER"}
        ]
        return hard_crop_tasks + pasture_growth + growth + high_value

    def _fertilizer_role_candidates(
        self,
        snapshot: CodexSnapshot,
        role: str,
        hard_crop_tasks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        module = self._role_module(role) or "Q0"
        local_hard = [
            task
            for task in hard_crop_tasks
            if task.get("zone") is not None
            and ("Q0" if int(task["zone"]) < 3 else "Q1") == module
        ]
        local_animals = [
            *self._module_animal_tasks(snapshot, module, "COW"),
            *self._module_animal_tasks(snapshot, module, "SHEEP"),
        ]
        fertilizer = [
            task
            for task in local_animals
            if task["kind"] in {"FERTILIZER_COLLECTION", "BUILD_PASTURE"}
        ]
        return local_hard + fertilizer

    def _maybe_replan_global(self, snapshot: CodexSnapshot) -> None:
        if (
            self._owned_quadrants(snapshot.farm) >= 2
            and self.q1_activation_day is None
        ):
            self.q1_activation_day = snapshot.clock.day
            for position, relative in self._q1_relative_cohort.items():
                self.cohort_offset[position] = self.q1_activation_day + relative
            self.q1_activation_records.append(
                {
                    "event": "Q1_OBSERVED_ACTIVE",
                    "day": snapshot.clock.day,
                    "step": snapshot.clock.step,
                    "money": float(snapshot.farm.get("money", 0.0)),
                }
            )
        super()._maybe_replan_global(snapshot)

    def _unit_actions(self, snapshot: CodexSnapshot) -> list[list[Any]]:
        positions = self._positions(snapshot.farm)
        crop_tasks = self._crop_tasks(snapshot)
        hard_crop_tasks = [task for task in crop_tasks if task.get("hard_reason")]
        reserved: set[tuple[int, int]] = set()
        actions: dict[int, list[Any]] = {}

        dispatch_order = [
            worker_id
            for worker_id in (*range(1, len(DUAL_ROLE_SEQUENCE)), 0)
            if worker_id < len(positions)
        ]
        for worker_id in dispatch_order:
            role = self._role_for(worker_id)
            inventory_tasks = self._inventory_task(snapshot, worker_id, role)
            candidates: list[dict[str, Any]]
            if inventory_tasks:
                candidates = inventory_tasks
            elif role.startswith("CROP_ZONE_"):
                zone_id = int(role.rsplit("_", 1)[1])
                module_id = zone_id // 3
                own = [task for task in crop_tasks if task.get("zone") == zone_id]
                cross_hard = [
                    task
                    for task in hard_crop_tasks
                    if task.get("zone") is not None
                    and int(task["zone"]) // 3 == module_id
                    and int(task["zone"]) != zone_id
                ]
                candidates = own if own else cross_hard
            elif role.startswith("LIVESTOCK_COW"):
                module = self._role_module(role) or "Q0"
                local = self._module_animal_tasks(snapshot, module, "COW")
                fertilizer_staffed = len(positions) >= (7 if module == "Q0" else 13)
                candidates = [
                    task
                    for task in local
                    if task["kind"] != "FEED"
                    and not (
                        task["kind"] == "FERTILIZER_COLLECTION"
                        and fertilizer_staffed
                    )
                ]
            elif role.startswith("LIVESTOCK_SHEEP"):
                module = self._role_module(role) or "Q0"
                local = self._module_animal_tasks(snapshot, module, "SHEEP")
                fertilizer_staffed = len(positions) >= (7 if module == "Q0" else 13)
                candidates = [
                    task
                    for task in local
                    if task["kind"] != "FEED"
                    and not (
                        task["kind"] == "FERTILIZER_COLLECTION"
                        and fertilizer_staffed
                    )
                ]
            elif self._is_fertilizer_role(role):
                candidates = self._fertilizer_role_candidates(
                    snapshot, role, hard_crop_tasks
                )
            else:
                candidates = self._float_reserve_candidates(
                    snapshot, crop_tasks, hard_crop_tasks
                )

            action = self._choose_committed_task(
                snapshot,
                worker_id,
                role,
                positions[worker_id],
                candidates,
                reserved,
            )
            if not self._eligible_unit_action(snapshot, worker_id, action):
                if action[0] not in MOVE_ACTIONS:
                    self._close_commitment(worker_id, snapshot.clock.step)
                action = ["PASS"]
            actions[worker_id] = action
        return [actions.get(worker_id, ["PASS"]) for worker_id in range(len(positions))]

    def _market_orders(self, snapshot: CodexSnapshot) -> list[list[Any]]:
        owned = self._owned_quadrants(snapshot.farm)
        original_targets = self.config["livestock_targets"]
        if owned < 2:
            self.config["livestock_targets"] = {"COW": 3, "SHEEP": 3}
        try:
            orders = super()._market_orders(snapshot)
        finally:
            self.config["livestock_targets"] = original_targets

        if owned >= 2 or self._shutdown(snapshot):
            return orders

        day = snapshot.clock.day
        if not int(self.config["q1_activation_min_day"]) <= day <= int(
            self.config["q1_activation_max_day"]
        ):
            return orders

        shed = snapshot.private.get("shed", {}) or {}
        prices = snapshot.market.get("prices", {}) or {}
        prospective_sales = sum(
            int(shed.get(item, 0)) * float(prices.get(item, 0.0))
            for item in ("MILK", "WOOL", "MELON", "STRAWBERRY", "FERTILIZER")
        )
        available = float(snapshot.farm.get("money", 0.0)) + prospective_sales
        threshold = float(self.config["q1_activation_cash"])
        if day not in self._q1_activation_decisions:
            self._q1_activation_decisions.add(day)
            self.q1_activation_records.append(
                {
                    "event": "Q1_ADMISSION_DECISION",
                    "day": day,
                    "step": snapshot.clock.step,
                    "money": float(snapshot.farm.get("money", 0.0)),
                    "prospective_sales": prospective_sales,
                    "available": available,
                    "threshold": threshold,
                    "admitted": available >= threshold,
                }
            )
        if available < threshold:
            return orders

        insert_at = 0
        while insert_at < len(orders) and orders[insert_at][0] == "SELL":
            insert_at += 1
        orders.insert(insert_at, ["BUY_LAND"])
        return orders[: self.max_market_orders]

    def _request_outcome(
        self, request: dict[str, Any], snapshot: CodexSnapshot
    ) -> str:
        if (
            request["actor_kind"] == "MARKET"
            and request["action"]
            and request["action"][0] == "BUY_LAND"
        ):
            return (
                "SUCCESS"
                if self._owned_quadrants(snapshot.farm) >= 2
                else "NO_OP"
            )
        return super()._request_outcome(request, snapshot)

    def _record_success(
        self, request: dict[str, Any], snapshot: CodexSnapshot
    ) -> None:
        if request.get("actor_kind") == "UNIT" and request.get("action"):
            action = request["action"]
            before_tile = request.get("before_tile")
            position = tuple(int(value) for value in request["actor_position"])
            module = "Q0" if position[0] < 5 else "Q1"
            if (
                isinstance(before_tile, dict)
                and before_tile.get("animal") in ANIMAL_RULES
                and action[0] in {"FEED", "CARE", "HARVEST"}
            ):
                species = str(before_tile["animal"])
                self.quadrant_livestock_service[
                    f"{module}_{species}_{action[0]}"
                ] += 1
            if action[0] == "HARVEST" and isinstance(before_tile, dict):
                units = int(before_tile.get("yield_units", 0))
                if before_tile.get("kind") == "PLANT":
                    crop = str(before_tile.get("crop", "UNKNOWN"))
                    self.quadrant_production[f"{module}_{crop}"] += units
                    product = crop
                elif before_tile.get("animal") in ANIMAL_RULES:
                    product = str(
                        ANIMAL_RULES[str(before_tile["animal"])]["product"]
                    )
                    self.quadrant_production[f"{module}_{product}"] += units
                else:
                    product = None
                if (
                    module == "Q1"
                    and units > 0
                    and product is not None
                    and self.q1_first_output_day is None
                ):
                    self.q1_first_output_day = snapshot.clock.day
                    self.q1_first_output_product = product
        super()._record_success(request, snapshot)

    def _record_state_telemetry(self, snapshot: CodexSnapshot) -> None:
        super()._record_state_telemetry(snapshot)
        q0_crop = sum(
            1
            for position in self.q0_crop_positions
            if isinstance(self._tile(snapshot.farm, position), dict)
            and self._tile(snapshot.farm, position).get("kind") == "PLANT"
        )
        q1_crop = sum(
            1
            for position in self.q1_crop_positions
            if isinstance(self._tile(snapshot.farm, position), dict)
            and self._tile(snapshot.farm, position).get("kind") == "PLANT"
        )
        q1_animals = sum(
            1
            for position in self.q1_pasture_positions
            if isinstance(self._tile(snapshot.farm, position), dict)
            and bool(self._tile(snapshot.farm, position).get("animal"))
        )
        self.quadrant_state_trajectory.append(
            {
                "step": snapshot.clock.step,
                "day": snapshot.clock.day,
                "q0_active_crops": q0_crop,
                "q1_active_crops": q1_crop,
                "q1_active_animals": q1_animals,
                "worker_count": len(self._positions(snapshot.farm)),
            }
        )
        if (
            self.q1_full_module_day is None
            and q1_crop >= 18
            and q1_animals >= 6
        ):
            self.q1_full_module_day = snapshot.clock.day

    def telemetry_snapshot(self) -> dict[str, Any]:
        payload = super().telemetry_snapshot()
        payload.update(
            {
                "agent_version": self.model_spec_version,
                "Q1_activation_day": self.q1_activation_day,
                "Q1_full_module_day": self.q1_full_module_day,
                "Q1_first_output_day": self.q1_first_output_day,
                "Q1_first_output_product": self.q1_first_output_product,
                "Q1_activation_records": deepcopy(self.q1_activation_records),
                "Q0_MELON_units": int(self.quadrant_production["Q0_MELON"]),
                "Q0_STRAWBERRY_units": int(
                    self.quadrant_production["Q0_STRAWBERRY"]
                ),
                "Q1_MELON_units": int(self.quadrant_production["Q1_MELON"]),
                "Q1_STRAWBERRY_units": int(
                    self.quadrant_production["Q1_STRAWBERRY"]
                ),
                "Q0_MILK_units": int(self.quadrant_production["Q0_MILK"]),
                "Q0_WOOL_units": int(self.quadrant_production["Q0_WOOL"]),
                "Q1_MILK_units": int(self.quadrant_production["Q1_MILK"]),
                "Q1_WOOL_units": int(self.quadrant_production["Q1_WOOL"]),
                "quadrant_livestock_service": dict(
                    self.quadrant_livestock_service
                ),
                "quadrant_state_trajectory": deepcopy(
                    self.quadrant_state_trajectory
                ),
            }
        )
        return payload


def create_dual_agent(
    candidate_config: dict[str, Any] | None = None,
    run_context: dict[str, Any] | None = None,
) -> Callable[[dict[str, Any], Any], dict[str, Any]]:
    instance = CodexDualQAgent(candidate_config, run_context=run_context)

    def candidate_agent(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            return instance(observation, configuration)
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            return deepcopy(_SAFE_PASS)

    candidate_agent.codex_dual_instance = instance  # type: ignore[attr-defined]
    candidate_agent.candidate_id = "CODEX_C2_DUAL_Q"  # type: ignore[attr-defined]
    return candidate_agent
