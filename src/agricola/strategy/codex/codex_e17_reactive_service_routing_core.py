"""State-driven E17.2 unit execution for the Codex 3Q target topology.

Market, acquisitions, hires and land unlocks remain owned by the E17.1 V2
provider.  Unit commands are rebuilt from the current observation on every
turn, so routing does not inherit coordinates from an open-loop schedule.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import (
    CodexObservationAdapter,
    stable_payload_hash,
)
from agricola.core.state import CROPS
from agricola.strategy.codex.codex_e17_true_reactive import (
    create_codex_e17_true_reactive_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CORE_CONFIG_PATH = (
    REPO_ROOT
    / "experiments/e17/configs/codex/"
    / "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V2.json"
)
CORE_MODEL_SPEC_VERSION = "CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V2"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
_MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
_ANIMALS = ("COW", "SHEEP", "GOOSE")


@dataclass(frozen=True)
class CoreTask:
    kind: str
    target: tuple[int, int]
    action: tuple[Any, ...]
    priority: int
    allowed_workers: tuple[int, ...] | None = None
    resource: str | None = None

    @property
    def identity(self) -> tuple[str, tuple[int, int], tuple[Any, ...]]:
        return self.kind, self.target, self.action


def load_core_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path) if path is not None else DEFAULT_CORE_CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V2",
        "model_spec_version": CORE_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E17.1-TRUE-REACTIVE-V2",
        "causal_family": "REACTIVE_SERVICE_AND_ROUTING_CORE",
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    if int(config.get("turns_per_day", 0)) <= 0:
        raise ValueError("turns_per_day must be positive")
    if int(config.get("episode_steps", 0)) <= 0:
        raise ValueError("episode_steps must be positive")
    if int(config.get("activation_day", -1)) < 0:
        raise ValueError("activation_day must be non-negative")
    if not config.get("pasture_targets") or not config.get("task_priority"):
        raise ValueError("topology and task priorities are required")
    return deepcopy(config)


def _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:
    return [
        tuple(farm.get("farmer", [4, 4])),
        *(tuple(pos) for pos in farm.get("hands", []) or []),
    ]


def _inventories(private: dict[str, Any], count: int) -> list[dict[str, Any]]:
    inventories = [
        inv if isinstance(inv, dict) else {}
        for inv in (private.get("inventories", []) or [])
    ]
    inventories.extend({} for _ in range(max(0, count - len(inventories))))
    return inventories[:count]


def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
    x, y = position
    rows = farm.get("tiles", []) or []
    if not 0 <= y < len(rows) or not 0 <= x < len(rows[y]):
        return "OUT_OF_BOUNDS"
    return rows[y][x]


def _distance(source: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(source[0] - target[0]) + abs(source[1] - target[1])


def _move(source: tuple[int, int], target: tuple[int, int]) -> list[str]:
    sx, sy = source
    tx, ty = target
    if sx < tx:
        return ["EAST"]
    if sx > tx:
        return ["WEST"]
    if sy < ty:
        return ["SOUTH"]
    if sy > ty:
        return ["NORTH"]
    return ["PASS"]


def _shed_access(board_size: int) -> tuple[tuple[int, int], ...]:
    half = board_size // 2
    return (
        (half - 1, half - 1),
        (half, half - 1),
        (half - 1, half),
        (half, half),
    )


def _owned(position: tuple[int, int], farm: dict[str, Any]) -> bool:
    return _tile(farm, position) != "LOCKED"


def _animal_tiles(farm: dict[str, Any]) -> list[tuple[tuple[int, int], dict[str, Any]]]:
    return [
        ((x, y), tile)
        for y, row in enumerate(farm.get("tiles", []) or [])
        for x, tile in enumerate(row)
        if isinstance(tile, dict) and tile.get("animal")
    ]


def _crop_tiles(farm: dict[str, Any]) -> list[tuple[tuple[int, int], dict[str, Any]]]:
    return [
        ((x, y), tile)
        for y, row in enumerate(farm.get("tiles", []) or [])
        for x, tile in enumerate(row)
        if isinstance(tile, dict) and tile.get("kind") == "PLANT"
    ]


class CodexE17ReactiveServiceRoutingCore:
    """Replan all unit work from the immutable Foundation snapshot."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
    ) -> None:
        self.config = load_core_config(config_path)
        self.run_context = deepcopy(run_context or {})
        self.base_policy = create_codex_e17_true_reactive_agent(
            run_context=self.run_context
        )
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = CORE_MODEL_SPEC_VERSION
        self.last_assignments: dict[int, tuple[str, tuple[int, int], tuple[Any, ...]]] = {}
        self.observations = 0
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.action_counts: Counter[str] = Counter()
        self.task_counts: Counter[str] = Counter()
        self.routing_commands = 0
        self.service_commands = 0
        self.market_mutations = 0
        self.records: list[dict[str, Any]] = []
        self.execution_outcomes: Counter[str] = Counter()
        self.ledger_records: list[dict[str, Any]] = []
        self._pending_ledger: list[int] = []

    def _priority(self, kind: str) -> int:
        return int(self.config["task_priority"][kind])

    def _settle_pending(self, snapshot: Any) -> None:
        positions = _positions(snapshot.farm)
        inventories = _inventories(snapshot.private, len(positions))
        for index in self._pending_ledger:
            record = self.ledger_records[index]
            worker_id = int(record["worker_id"])
            if worker_id >= len(positions):
                outcome = "UNKNOWN"
            else:
                action = record["requested"]
                op = str(action[0]) if action else "PASS"
                source = tuple(record["source"])
                target = tuple(record["target"])
                tile = _tile(snapshot.farm, target)
                inventory = inventories[worker_id]
                if op in _MOVES:
                    outcome = (
                        "EXECUTED"
                        if positions[worker_id] == target
                        else "NOT_EXECUTED"
                    )
                elif op == "PASS":
                    outcome = "UNKNOWN"
                elif op == "WATER":
                    outcome = (
                        "EXECUTED"
                        if isinstance(tile, dict)
                        and tile.get("kind") == "PLANT"
                        and (
                            bool(tile.get("watered_today", False))
                            or int(tile.get("consecutive_unwatered", 0) or 0) == 0
                        )
                        else "NOT_EXECUTED"
                    )
                elif op == "FEED":
                    outcome = (
                        "EXECUTED"
                        if isinstance(tile, dict)
                        and tile.get("animal")
                        and (
                            bool(tile.get("fed_today", False))
                            or int(tile.get("consecutive_unfed", 0) or 0) == 0
                        )
                        else "NOT_EXECUTED"
                    )
                elif op == "HARVEST":
                    after_yield = (
                        int(tile.get("yield_units", 0) or 0)
                        if isinstance(tile, dict)
                        else 0
                    )
                    outcome = (
                        "EXECUTED"
                        if after_yield < int(record["yield_before"])
                        else "NOT_EXECUTED"
                    )
                elif op == "PLANT":
                    outcome = (
                        "EXECUTED"
                        if isinstance(tile, dict)
                        and tile.get("kind") == "PLANT"
                        and len(action) >= 2
                        and tile.get("crop") == action[1]
                        else "NOT_EXECUTED"
                    )
                elif op in {"BUILD_PASTURE", "BUILD_COOP"}:
                    expected = op.removeprefix("BUILD_")
                    outcome = (
                        "EXECUTED"
                        if isinstance(tile, dict) and tile.get("kind") == expected
                        else "NOT_EXECUTED"
                    )
                elif op == "PLACE" and len(action) >= 2:
                    outcome = (
                        "EXECUTED"
                        if isinstance(tile, dict) and tile.get("animal") == action[1]
                        else "NOT_EXECUTED"
                    )
                elif op == "DIG":
                    outcome = (
                        "EXECUTED"
                        if stable_payload_hash(tile) != record["tile_before_sha256"]
                        else "NOT_EXECUTED"
                    )
                elif op == "PICKUP" and len(action) >= 2:
                    item = str(action[1])
                    outcome = (
                        "EXECUTED"
                        if int(inventory.get(item, 0) or 0)
                        > int(record["inventory_before"].get(item, 0) or 0)
                        else "NOT_EXECUTED"
                    )
                elif op == "DROP":
                    before_total = sum(
                        int(value or 0)
                        for value in record["inventory_before"].values()
                    )
                    after_total = sum(int(value or 0) for value in inventory.values())
                    outcome = "EXECUTED" if after_total < before_total else "NOT_EXECUTED"
                elif op == "CARE":
                    outcome = (
                        "EXECUTED"
                        if isinstance(tile, dict) and bool(tile.get("cared_today", False))
                        else "UNKNOWN" if snapshot.clock.hour == 0 else "NOT_EXECUTED"
                    )
                else:
                    outcome = "UNKNOWN"
                record["observed_position"] = list(positions[worker_id])
                record["source_position_unchanged"] = positions[worker_id] == source
            record["outcome"] = outcome
            record["post_state_id"] = snapshot.state_id
            record["post_snapshot_fingerprint"] = snapshot.snapshot_fingerprint
            self.execution_outcomes[outcome] += 1
        self._pending_ledger = []

    def _task(
        self,
        kind: str,
        target: tuple[int, int],
        action: tuple[Any, ...],
        *,
        allowed_workers: tuple[int, ...] | None = None,
        resource: str | None = None,
    ) -> CoreTask:
        return CoreTask(
            kind,
            target,
            action,
            self._priority(kind),
            allowed_workers,
            resource,
        )

    def _structure_tasks(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        inventories: list[dict[str, Any]],
    ) -> list[CoreTask]:
        tasks: list[CoreTask] = []
        pasture_targets = [tuple(value) for value in self.config["pasture_targets"]]
        coop_targets = [tuple(value) for value in self.config["coop_targets"]]
        placed = Counter(tile["animal"] for _pos, tile in _animal_tiles(farm))
        shed = private.get("shed", {}) or {}
        held = Counter()
        for inventory in inventories:
            for animal in _ANIMALS:
                held[animal] += int(inventory.get(animal, 0) or 0)
        owned = Counter(
            {
                animal: placed[animal] + int(shed.get(animal, 0) or 0) + held[animal]
                for animal in _ANIMALS
            }
        )

        structure_sets = {
            "PASTURE": pasture_targets,
            "COOP": coop_targets,
        }
        needed = {"PASTURE": owned["COW"] + owned["SHEEP"], "COOP": owned["GOOSE"]}
        for structure, targets in structure_sets.items():
            existing = sum(
                1
                for target in targets
                if isinstance(_tile(farm, target), dict)
                and _tile(farm, target).get("kind") == structure
            )
            remaining = max(0, needed[structure] - existing)
            for target in targets:
                if remaining <= 0 or not _owned(target, farm):
                    continue
                tile = _tile(farm, target)
                if tile is None:
                    tasks.append(
                        self._task(
                            "BUILD_STRUCTURE",
                            target,
                            (f"BUILD_{structure}",),
                        )
                    )
                    remaining -= 1
                elif isinstance(tile, dict) and tile.get("kind") == "WEED":
                    tasks.append(self._task("DIG_TARGET", target, ("DIG",)))

        empty_structures = [
            (target, tile.get("kind"))
            for target in pasture_targets + coop_targets
            if isinstance((tile := _tile(farm, target)), dict)
            and tile.get("kind") in {"PASTURE", "COOP"}
            and not tile.get("animal")
        ]
        for target, structure in empty_structures:
            species = ("GOOSE",) if structure == "COOP" else ("COW", "SHEEP")
            for animal in species:
                carriers = tuple(
                    worker_id
                    for worker_id, inventory in enumerate(inventories)
                    if int(inventory.get(animal, 0) or 0) > 0
                )
                if carriers:
                    tasks.append(
                        self._task(
                            "PLACE_ANIMAL",
                            target,
                            ("PLACE", animal, 1),
                            allowed_workers=carriers,
                            resource=animal,
                        )
                    )

        capacity = {
            "COW": sum(1 for _target, kind in empty_structures if kind == "PASTURE"),
            "SHEEP": sum(1 for _target, kind in empty_structures if kind == "PASTURE"),
            "GOOSE": sum(1 for _target, kind in empty_structures if kind == "COOP"),
        }
        accesses = _shed_access(len(farm.get("tiles", []) or []))
        for animal in _ANIMALS:
            count = min(int(shed.get(animal, 0) or 0), capacity[animal] + 1)
            for index in range(count):
                target = accesses[index % len(accesses)]
                tasks.append(
                    self._task(
                        "PICKUP_ANIMAL",
                        target,
                        ("PICKUP", animal, 1),
                        resource=animal,
                    )
                )
        return tasks

    def _service_tasks(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        inventories: list[dict[str, Any]],
        board_size: int,
        day: int,
    ) -> list[CoreTask]:
        tasks: list[CoreTask] = []
        for position, tile in _crop_tiles(farm):
            crop = str(tile.get("crop", ""))
            mature = day - int(tile.get("planted_day", day)) >= int(
                CROPS.get(crop, {}).get("first_yield_day", 10**6)
            )
            if mature and int(tile.get("yield_units", 0) or 0) > 0:
                tasks.append(self._task("HARVEST", position, ("HARVEST",)))
            if day + 1 >= int(self.config["episode_steps"]) // int(
                self.config["turns_per_day"]
            ):
                continue
            if not bool(tile.get("watered_today", False)):
                kind = (
                    "CRITICAL_WATER"
                    if int(tile.get("consecutive_unwatered", 0) or 0)
                    >= int(self.config["critical_unwatered_threshold"])
                    else "WATER"
                )
                tasks.append(self._task(kind, position, ("WATER",)))

        unfed = []
        for position, tile in _animal_tiles(farm):
            if int(tile.get("yield_units", 0) or 0) > 0:
                tasks.append(self._task("HARVEST", position, ("HARVEST",)))
            if day + 1 >= int(self.config["episode_steps"]) // int(
                self.config["turns_per_day"]
            ):
                continue
            critical = (
                not bool(tile.get("fed_today", False))
                and int(tile.get("consecutive_unfed", 0) or 0)
                >= int(self.config["critical_unfed_threshold"])
            )
            if critical:
                unfed.append(position)
                carriers = tuple(
                    worker_id
                    for worker_id, inventory in enumerate(inventories)
                    if int(inventory.get("WHEAT", 0) or 0) > 0
                )
                if carriers:
                    tasks.append(
                        self._task(
                            "CRITICAL_FEED",
                            position,
                            ("FEED",),
                            allowed_workers=carriers,
                            resource="WHEAT",
                        )
                    )
        carried_wheat = sum(int(inv.get("WHEAT", 0) or 0) for inv in inventories)
        shed_wheat = int((private.get("shed", {}) or {}).get("WHEAT", 0) or 0)
        desired = min(
            len(unfed),
            int(self.config["wheat_carrier_target"])
            * int(self.config["wheat_pickup_batch"]),
        )
        shortage = max(0, desired - carried_wheat)
        accesses = _shed_access(board_size)
        pickup_count = min(
            int(self.config["wheat_carrier_target"]),
            (min(shortage, shed_wheat) + int(self.config["wheat_pickup_batch"]) - 1)
            // int(self.config["wheat_pickup_batch"]),
        )
        remaining_wheat = shed_wheat
        for index in range(pickup_count):
            quantity = min(int(self.config["wheat_pickup_batch"]), remaining_wheat)
            if quantity <= 0:
                break
            tasks.append(
                self._task(
                    "PICKUP_WHEAT",
                    accesses[index % len(accesses)],
                    ("PICKUP", "WHEAT", quantity),
                    resource="WHEAT",
                )
            )
            remaining_wheat -= quantity
        return tasks

    def _terminal_drop_tasks(
        self,
        *,
        inventories: list[dict[str, Any]],
        positions: list[tuple[int, int]],
        board_size: int,
        day: int,
    ) -> list[CoreTask]:
        if day + 1 < int(self.config["episode_steps"]) // int(
            self.config["turns_per_day"]
        ):
            return []
        accesses = _shed_access(board_size)
        tasks: list[CoreTask] = []
        for worker_id, inventory in enumerate(inventories):
            sellable = sum(
                int(quantity or 0)
                for item, quantity in inventory.items()
                if item not in _ANIMALS and item != "WHEAT"
            )
            if sellable <= 0:
                continue
            target = min(
                accesses,
                key=lambda value: (_distance(positions[worker_id], value), value),
            )
            tasks.append(
                self._task(
                    "DROP_INVENTORY",
                    target,
                    ("DROP",),
                    allowed_workers=(worker_id,),
                )
            )
        return tasks

    def _crop_choice(
        self,
        target: tuple[int, int],
        *,
        day: int,
        available_seeds: dict[str, int],
    ) -> str | None:
        wheat_targets = {tuple(value) for value in self.config["wheat_crop_targets"]}
        if target in wheat_targets and int(available_seeds.get("WHEAT", 0) or 0) > 0:
            return "WHEAT"
        for crop in ("MELON", "STRAWBERRY", "TOMATO", "CARROT", "WHEAT"):
            if day <= int(self.config["crop_cutoffs"][crop]) and int(
                available_seeds.get(crop, 0) or 0
            ) > 0:
                return crop
        return None

    def _crop_setup_tasks(
        self,
        *,
        farm: dict[str, Any],
        private: dict[str, Any],
        day: int,
    ) -> list[CoreTask]:
        if day > int(self.config["plant_cutoff_day"]):
            return []
        livestock = {
            *(tuple(value) for value in self.config["pasture_targets"]),
            *(tuple(value) for value in self.config["coop_targets"]),
        }
        seeds = dict(private.get("seeds", {}) or {})
        tasks: list[CoreTask] = []
        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                target = (x, y)
                if target in livestock or tile == "LOCKED":
                    continue
                if isinstance(tile, dict) and tile.get("kind") == "WEED":
                    tasks.append(self._task("DIG_TARGET", target, ("DIG",)))
                    continue
                if tile is not None:
                    continue
                crop = self._crop_choice(target, day=day, available_seeds=seeds)
                if crop is not None:
                    tasks.append(
                        self._task(
                            "PLANT",
                            target,
                            ("PLANT", crop),
                            resource=crop,
                        )
                    )
        return tasks

    def _assign(
        self,
        tasks: list[CoreTask],
        positions: list[tuple[int, int]],
        private: dict[str, Any],
    ) -> dict[int, CoreTask]:
        assignments: dict[int, CoreTask] = {}
        available_workers = set(range(len(positions)))
        reserved_targets: set[tuple[str, tuple[int, int]]] = set()
        remaining_seeds = Counter(private.get("seeds", {}) or {})
        remaining_shed = Counter(private.get("shed", {}) or {})
        remaining_tasks = list(tasks)
        while available_workers and remaining_tasks:
            candidates: list[tuple[int, int, int, int]] = []
            for task_index, task in enumerate(remaining_tasks):
                target_key = (task.kind, task.target)
                if target_key in reserved_targets:
                    continue
                if task.kind == "PLANT" and remaining_seeds[str(task.resource)] <= 0:
                    continue
                if task.kind in {"PICKUP_WHEAT", "PICKUP_ANIMAL"}:
                    quantity = int(task.action[2]) if len(task.action) >= 3 else 1
                    if remaining_shed[str(task.resource)] < quantity:
                        continue
                eligible = available_workers
                if task.allowed_workers is not None:
                    eligible = available_workers.intersection(task.allowed_workers)
                for worker_id in eligible:
                    candidates.append(
                        (
                            task.priority,
                            _distance(positions[worker_id], task.target)
                            - (
                                3
                                if self.last_assignments.get(worker_id) == task.identity
                                else 0
                            ),
                            worker_id,
                            task_index,
                        )
                    )
            if not candidates:
                break
            _priority, _distance_score, worker_id, task_index = min(candidates)
            task = remaining_tasks.pop(task_index)
            target_key = (task.kind, task.target)
            assignments[worker_id] = task
            available_workers.remove(worker_id)
            reserved_targets.add(target_key)
            if task.kind == "PLANT":
                remaining_seeds[str(task.resource)] -= 1
            elif task.kind in {"PICKUP_WHEAT", "PICKUP_ANIMAL"}:
                remaining_shed[str(task.resource)] -= (
                    int(task.action[2]) if len(task.action) >= 3 else 1
                )
        return assignments

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        snapshot = CodexObservationAdapter.parse(
            observation,
            configuration,
            fallback_turns_per_day=int(self.config["turns_per_day"]),
            fallback_episode_steps=int(self.config["episode_steps"]),
        )
        self._settle_pending(snapshot)
        provider = self.base_policy(observation, configuration)
        if snapshot.clock.day < int(self.config["activation_day"]):
            self.observations += 1
            return deepcopy(provider)
        farm = snapshot.farm
        private = snapshot.private
        positions = _positions(farm)
        inventories = _inventories(private, len(positions))
        board_size = int(snapshot.configuration_snapshot["boardSize"])
        tasks = [
            *self._service_tasks(
                farm,
                private,
                inventories,
                board_size,
                snapshot.clock.day,
            ),
            *self._terminal_drop_tasks(
                inventories=inventories,
                positions=positions,
                board_size=board_size,
                day=snapshot.clock.day,
            ),
        ]
        if snapshot.clock.day + 1 < int(self.config["episode_steps"]) // int(
            self.config["turns_per_day"]
        ):
            tasks.extend(self._structure_tasks(farm, private, inventories))
            tasks.extend(
                self._crop_setup_tasks(
                    farm=farm,
                    private=private,
                    day=snapshot.clock.day,
                )
            )
        assignments = self._assign(tasks, positions, private)
        unit_actions: list[list[Any]] = []
        next_assignments: dict[int, tuple[str, tuple[int, int], tuple[Any, ...]]] = {}
        for worker_id, position in enumerate(positions):
            task = assignments.get(worker_id)
            if task is None:
                emitted = ["PASS"]
            elif position == task.target:
                emitted = list(task.action)
            else:
                emitted = _move(position, task.target)
            unit_actions.append(emitted)
            self.action_counts[str(emitted[0])] += 1
            if emitted[0] in _MOVES:
                self.routing_commands += 1
            elif emitted[0] != "PASS":
                self.service_commands += 1
            if task is not None:
                self.task_counts[task.kind] += 1
                next_assignments[worker_id] = task.identity
            source_tile = _tile(farm, position)
            if emitted[0] in _MOVES:
                target = tuple(
                    value + delta
                    for value, delta in zip(
                        position,
                        {
                            "NORTH": (0, -1),
                            "SOUTH": (0, 1),
                            "EAST": (1, 0),
                            "WEST": (-1, 0),
                        }[str(emitted[0])],
                        strict=True,
                    )
                )
            else:
                target = position
            self.ledger_records.append(
                {
                    "step": snapshot.clock.step,
                    "day": snapshot.clock.day,
                    "hour": snapshot.clock.hour,
                    "worker_id": worker_id,
                    "state_id": snapshot.state_id,
                    "snapshot_fingerprint": snapshot.snapshot_fingerprint,
                    "source": list(position),
                    "target": list(target),
                    "requested": deepcopy(emitted),
                    "task_kind": task.kind if task is not None else "IDLE",
                    "tile_before_sha256": stable_payload_hash(source_tile),
                    "yield_before": (
                        int(source_tile.get("yield_units", 0) or 0)
                        if isinstance(source_tile, dict)
                        else 0
                    ),
                    "inventory_before": deepcopy(inventories[worker_id]),
                    "outcome": "PENDING_NEXT_OBSERVATION",
                }
            )
            self._pending_ledger.append(len(self.ledger_records) - 1)
        action = {
            "farmer": unit_actions[0] if unit_actions else ["PASS"],
            "hands": unit_actions[1:],
            "market": deepcopy(provider.get("market", [])),
        }
        if action["market"] != provider.get("market", []):
            self.market_mutations += 1
        self.last_assignments = next_assignments
        self.observations += 1
        if len(self.records) < 24 and action != provider:
            self.records.append(
                {
                    "step": snapshot.clock.step,
                    "day": snapshot.clock.day,
                    "hour": snapshot.clock.hour,
                    "state_id": snapshot.state_id,
                    "snapshot_fingerprint": snapshot.snapshot_fingerprint,
                    "provider_action_sha256": stable_payload_hash(provider),
                    "emitted_action_sha256": stable_payload_hash(action),
                    "task_count": len(tasks),
                    "assignments": {
                        str(worker_id): {
                            "kind": task.kind,
                            "target": list(task.target),
                            "action": list(task.action),
                        }
                        for worker_id, task in sorted(assignments.items())
                    },
                }
            )
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        for index in self._pending_ledger:
            self.ledger_records[index]["outcome"] = "UNKNOWN"
            self.execution_outcomes["UNKNOWN"] += 1
        self._pending_ledger = []
        provider = self.base_policy.codex_e17_true_reactive_instance.telemetry_snapshot()
        productive = self.service_commands
        return {
            "agent_version": self.model_spec_version,
            "base_agent_version": provider["agent_version"],
            "observations": self.observations,
            "routing_commands": self.routing_commands,
            "service_commands": self.service_commands,
            "move_per_service": self.routing_commands / productive if productive else None,
            "market_mutations": self.market_mutations,
            "action_counts": dict(self.action_counts),
            "task_counts": dict(self.task_counts),
            "execution_outcomes": dict(self.execution_outcomes),
            "ledger_record_count": len(self.ledger_records),
            "ledger_records": deepcopy(self.ledger_records),
            "decision_samples": deepcopy(self.records),
            "provider": provider,
        }


def create_codex_e17_reactive_service_routing_core(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    instance = CodexE17ReactiveServiceRoutingCore(
        run_context=run_context,
        config_path=config_path,
    )

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_e17_service_routing_core_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e17_service_routing_core_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e17_service_routing_core_instance = instance
    policy.codex_e17_service_routing_core_last_error = None
    policy.__name__ = "codex_e17_2_reactive_service_routing_core_v2_policy"
    return policy


__all__ = [
    "CORE_MODEL_SPEC_VERSION",
    "CodexE17ReactiveServiceRoutingCore",
    "CoreTask",
    "create_codex_e17_reactive_service_routing_core",
    "load_core_config",
]
