"""Productive 6-6-2 topology overlay over Codex E17.2 V4D.

The overlay converts all five cells removed from the V4D 7-7-5 pasture layout
into crops, including the three reclaimed Q2 cells.  Reclaimed work is
translated in place so V4D worker trajectories remain synchronized.  The
pasture census targets fourteen occupied structures and permits one in-transit
livestock resource while a removed Q0 placement returns to the shed.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.state import CROPS
from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4D_CONFIG_PATH,
    create_codex_e17_batched_cluster_routing_v4,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_TOPOLOGY_662_CONFIG_PATH = (
    REPO_ROOT
    / "experiments/e17/configs/codex/CODEX_E17_3_TOPOLOGY_CAP_662_V1.json"
)
TOPOLOGY_662_MODEL_SPEC_VERSION = "CODEX-E17.3-TOPOLOGY-FILL-662-V2"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
_PASTURE_LIVESTOCK = frozenset({"COW", "SHEEP"})
_MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})
_ANIMAL_ONLY_SERVICES = frozenset(
    {"FEED", "CARE", "COLLECT_FERTILIZER", "FERTILIZE"}
)


def _quadrant(position: tuple[int, int]) -> str:
    x, y = position
    if x < 5 and y < 5:
        return "Q0"
    if x >= 5 and y < 5:
        return "Q1"
    if x < 5 and y >= 5:
        return "Q2"
    return "Q3"


def load_topology_662_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load the explicit 6-6-2 topology and validate its hard caps."""

    config_path = (
        Path(path) if path is not None else DEFAULT_TOPOLOGY_662_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E17_3_TOPOLOGY_FILL_662_V2",
        "model_spec_version": TOPOLOGY_662_MODEL_SPEC_VERSION,
        "base_policy": (
            "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28"
        ),
        "causal_family": "RECLAIMED_CROP_AND_PASTURE_FILL_CONTROL",
        "q2_pasture_cap": 2,
        "allow_q2_zero_future_variant": True,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")

    targets = [tuple(value) for value in config.get("pasture_targets", [])]
    if len(targets) != len(set(targets)):
        raise ValueError("pasture targets must be unique")
    counts = Counter(_quadrant(position) for position in targets)
    declared = {
        key: int(value)
        for key, value in config.get("quadrant_pasture_caps", {}).items()
    }
    if declared != {"Q0": 6, "Q1": 6, "Q2": 2}:
        raise ValueError(f"unexpected declared caps: {declared!r}")
    if counts["Q0"] != 6 or counts["Q1"] != 6 or counts["Q3"]:
        raise ValueError(f"topology violates the 6-6-Q2 envelope: {dict(counts)!r}")
    if counts["Q2"] > int(config["q2_pasture_cap"]):
        raise ValueError("Q2 pasture targets exceed the hard cap")
    if int(config["pasture_fill_target"]) != len(targets):
        raise ValueError("fill target must equal available pasture targets")
    if int(config["pre_q2_livestock_resource_cap"]) != len(targets):
        raise ValueError("the pre-Q2 livestock cap must equal the fill target")
    if int(config["livestock_in_transit_buffer"]) != 1:
        raise ValueError("the topology requires one in-transit livestock slot")
    if int(config["livestock_resource_cap"]) != len(targets) + 1:
        raise ValueError("livestock cap must include the in-transit buffer")
    reclaimed = [
        tuple(value) for value in config.get("reclaimed_crop_targets", [])
    ]
    blocked = [
        tuple(value) for value in config.get("blocked_v4d_pasture_targets", [])
    ]
    q2_reclaimed = [
        tuple(value)
        for value in config.get("q2_reclaimed_crop_targets", [])
    ]
    if len(reclaimed) != 5 or len(reclaimed) != len(set(reclaimed)):
        raise ValueError("exactly five unique V4D pasture cells must be reclaimed")
    if set(reclaimed) != set(blocked):
        raise ValueError("every blocked V4D pasture must become a crop target")
    if set(reclaimed).intersection(targets):
        raise ValueError("pasture and reclaimed crop targets must be disjoint")
    if len(q2_reclaimed) != 3 or set(q2_reclaimed) != {
        value for value in reclaimed if _quadrant(value) == "Q2"
    }:
        raise ValueError("the three reclaimed Q2 cells must be explicit")
    crop_priority = list(config.get("reclaimed_crop_priority", []))
    crop_cutoffs = config.get("reclaimed_crop_cutoffs", {}) or {}
    if not crop_priority or any(crop not in CROPS for crop in crop_priority):
        raise ValueError("reclaimed crop priority contains an unknown crop")
    if any(int(crop_cutoffs.get(crop, -1)) < 0 for crop in crop_priority):
        raise ValueError("every reclaimed crop requires a non-negative cutoff")
    if crop_priority != [str(config.get("reclaimed_seed_backfill_crop"))]:
        raise ValueError("reclaimed crops must use the dedicated seed backfill")
    if int(config.get("reclaimed_seed_backfill_units", 0)) != len(reclaimed):
        raise ValueError("seed backfill must cover every reclaimed crop target")
    if int(config.get("pasture_fill_mission_worker_limit", 0)) <= 0:
        raise ValueError("pasture fill mission requires at least one worker")
    if list(config.get("pasture_fill_quadrant_priority", [])) != [
        "Q1",
        "Q2",
        "Q0",
    ]:
        raise ValueError("fill priority must repair Q1 and Q2 before Q0")
    return deepcopy(config)


def _farm(observation: dict[str, Any]) -> dict[str, Any]:
    player = int(observation.get("player", 0))
    farms = observation.get("farms", []) or []
    return farms[player] if 0 <= player < len(farms) else {}


def _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:
    return [
        tuple(farm.get("farmer", [4, 4])),
        *(tuple(position) for position in farm.get("hands", []) or []),
    ]


def _inventories(private: dict[str, Any], count: int) -> list[dict[str, Any]]:
    values = [
        value if isinstance(value, dict) else {}
        for value in (private.get("inventories", []) or [])
    ]
    values.extend({} for _ in range(max(0, count - len(values))))
    return values[:count]


def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
    x, y = position
    rows = farm.get("tiles", []) or []
    if not 0 <= y < len(rows) or not 0 <= x < len(rows[y]):
        return "LOCKED"
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


def _unit_actions(action: dict[str, Any], count: int) -> list[list[Any]]:
    actions = [
        list(action.get("farmer", ["PASS"]) or ["PASS"]),
        *(list(value or ["PASS"]) for value in action.get("hands", []) or []),
    ]
    actions.extend(["PASS"] for _ in range(max(0, count - len(actions))))
    return actions[:count]


def _store_unit_actions(action: dict[str, Any], actions: list[list[Any]]) -> None:
    action["farmer"] = actions[0] if actions else ["PASS"]
    action["hands"] = actions[1:]


def _pasture_livestock_resources(observation: dict[str, Any]) -> int:
    """Count COW/SHEEP on tiles, in the shed, and in unit inventories."""

    total = 0
    farm = _farm(observation)
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal") in _PASTURE_LIVESTOCK:
                total += 1

    private = observation.get("private", {}) or {}
    shed = private.get("shed", {}) or {}
    total += sum(max(0, int(shed.get(item, 0))) for item in _PASTURE_LIVESTOCK)
    for inventory in private.get("inventories", []) or []:
        if not isinstance(inventory, dict):
            continue
        total += sum(
            max(0, int(inventory.get(item, 0))) for item in _PASTURE_LIVESTOCK
        )
    return total


class CodexE17TopologyCap662Agent:
    """Reallocate removed pasture work to crops and fill all allowed pastures."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy: Callable[..., dict[str, Any]] | None = None,
    ) -> None:
        self.config = load_topology_662_config(config_path)
        self.run_context = deepcopy(run_context or {})
        self.base_policy = (
            base_policy
            if base_policy is not None
            else create_codex_e17_batched_cluster_routing_v4(
                run_context=self.run_context,
                config_path=DEFAULT_V4D_CONFIG_PATH,
            )
        )
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = TOPOLOGY_662_MODEL_SPEC_VERSION
        self.pasture_targets = frozenset(
            tuple(value) for value in self.config["pasture_targets"]
        )
        self.reclaimed_crop_targets = frozenset(
            tuple(value) for value in self.config["reclaimed_crop_targets"]
        )
        target_counts = Counter(
            _quadrant(position) for position in self.pasture_targets
        )
        self.target_pastures_by_quadrant = {
            quadrant: int(target_counts[quadrant])
            for quadrant in ("Q0", "Q1", "Q2")
        }
        self.q2_pasture_cap = int(self.config["q2_pasture_cap"])
        self.livestock_resource_cap = int(self.config["livestock_resource_cap"])
        self.fill_mission_workers: set[int] = set()
        self.fill_mission_started = False
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.observation_count = 0
        self.override_batches = 0
        self.blocked_builds: Counter[tuple[int, int]] = Counter()
        self.blocked_placements: Counter[tuple[int, int]] = Counter()
        self.clamped_animal_units: Counter[str] = Counter()
        self.reclaimed_crop_actions: Counter[str] = Counter()
        self.reassigned_blocked_worker_actions = 0
        self.pasture_fill_route_actions = 0
        self.pasture_fill_place_commands = 0
        self.pasture_fill_pickup_commands = 0
        self.pasture_fill_purchase_units: Counter[str] = Counter()
        self.reclaimed_seed_backfill_requested = False
        self.reclaimed_seed_backfill_units = 0
        self.max_observed_q2_pastures = 0
        self.max_active_reclaimed_crops = 0
        self.latest_target_pastures_built = 0
        self.latest_target_pastures_filled = 0
        self.latest_empty_target_pastures = 0
        self.topology_cap_breaches = 0

    def _observe_topology(self, observation: dict[str, Any]) -> None:
        farm = _farm(observation)
        q2_pastures = 0
        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                if (
                    x < 5
                    and y >= 5
                    and isinstance(tile, dict)
                    and tile.get("kind") == "PASTURE"
                ):
                    q2_pastures += 1
        self.max_observed_q2_pastures = max(
            self.max_observed_q2_pastures, q2_pastures
        )
        if q2_pastures > self.q2_pasture_cap:
            self.topology_cap_breaches += 1
        target_tiles = [_tile(farm, target) for target in self.pasture_targets]
        self.latest_target_pastures_built = sum(
            isinstance(tile, dict) and tile.get("kind") == "PASTURE"
            for tile in target_tiles
        )
        self.latest_target_pastures_filled = sum(
            isinstance(tile, dict)
            and tile.get("kind") == "PASTURE"
            and tile.get("animal") in _PASTURE_LIVESTOCK
            for tile in target_tiles
        )
        self.latest_empty_target_pastures = (
            self.latest_target_pastures_built
            - self.latest_target_pastures_filled
        )
        active_reclaimed = sum(
            isinstance(_tile(farm, target), dict)
            and _tile(farm, target).get("kind") == "PLANT"
            for target in self.reclaimed_crop_targets
        )
        self.max_active_reclaimed_crops = max(
            self.max_active_reclaimed_crops,
            active_reclaimed,
        )

    def _filter_unit_actions(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> set[int]:
        farm = _farm(observation)
        positions = _positions(farm)
        unit_actions = _unit_actions(action, len(positions))
        crop_tasks = {
            target: command
            for _priority, target, command in self._reclaimed_crop_tasks(
                observation
            )
        }
        claimed_crop_targets: set[tuple[int, int]] = set()
        released: set[int] = set()
        for index, command in enumerate(unit_actions):
            if index >= len(positions) or not command:
                continue
            position = positions[index]
            opcode = str(command[0])
            blocked = False
            if opcode == "BUILD_PASTURE" and position not in self.pasture_targets:
                self.blocked_builds[position] += 1
                blocked = True
            elif (
                opcode == "PLACE"
                and len(command) >= 2
                and str(command[1]) in _PASTURE_LIVESTOCK
                and position not in self.pasture_targets
            ):
                self.blocked_placements[position] += 1
                blocked = True
            elif (
                position in self.reclaimed_crop_targets
                and opcode in _ANIMAL_ONLY_SERVICES
            ):
                blocked = True

            desired_crop = crop_tasks.get(position)
            if (
                desired_crop is not None
                and position not in claimed_crop_targets
                and opcode not in _MOVES
            ):
                unit_actions[index] = list(desired_crop)
                claimed_crop_targets.add(position)
                self.reclaimed_crop_actions[str(desired_crop[0])] += 1
                if blocked or opcode == "PASS":
                    self.reassigned_blocked_worker_actions += 1
                released.add(index)
                continue

            if not blocked:
                continue
            unit_actions[index] = ["PASS"]
            released.add(index)
        _store_unit_actions(action, unit_actions)
        return released

    def _empty_pastures(self, farm: dict[str, Any]) -> list[tuple[int, int]]:
        priority = {
            quadrant: rank
            for rank, quadrant in enumerate(
                self.config["pasture_fill_quadrant_priority"]
            )
        }
        return sorted(
            (
                target
                for target in self.pasture_targets
                if isinstance((tile := _tile(farm, target)), dict)
                and tile.get("kind") == "PASTURE"
                and not tile.get("animal")
            ),
            key=lambda value: (priority[_quadrant(value)], value[1], value[0]),
        )

    def _route_pasture_fill(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        eligible_workers: set[int] | None = None,
    ) -> set[int]:
        farm = _farm(observation)
        private = observation.get("private", {}) or {}
        positions = _positions(farm)
        inventories = _inventories(private, len(positions))
        actions = _unit_actions(action, len(positions))
        empty = self._empty_pastures(farm)
        assigned: set[int] = set()
        reserved: set[tuple[int, int]] = set()
        species_priority = list(self.config["pasture_fill_species_priority"])

        carriers: list[tuple[int, str]] = []
        carried_units = 0
        for worker_id, inventory in enumerate(inventories):
            for species in species_priority:
                quantity = max(0, int(inventory.get(species, 0) or 0))
                carried_units += quantity
                if (
                    quantity
                    and (eligible_workers is None or worker_id in eligible_workers)
                    and not any(value[0] == worker_id for value in carriers)
                ):
                    carriers.append((worker_id, species))

        for worker_id, species in carriers:
            candidates = [target for target in empty if target not in reserved]
            if not candidates:
                break
            target = min(
                candidates,
                key=lambda value: (
                    self.config["pasture_fill_quadrant_priority"].index(
                        _quadrant(value)
                    ),
                    _distance(positions[worker_id], value),
                    value,
                ),
            )
            if positions[worker_id] == target:
                actions[worker_id] = ["PLACE", species, 1]
                self.pasture_fill_place_commands += 1
            else:
                actions[worker_id] = _move(positions[worker_id], target)
                self.pasture_fill_route_actions += 1
            assigned.add(worker_id)
            reserved.add(target)

        pickup_needed = max(0, len(empty) - carried_units)
        if pickup_needed and int(observation.get("day", 0)) <= int(
            self.config["fill_purchase_cutoff_day"]
        ):
            shed = private.get("shed", {}) or {}
            free_workers = [
                worker_id
                for worker_id, command in enumerate(actions)
                if worker_id not in assigned
                and (eligible_workers is None or worker_id in eligible_workers)
                and command
                and (
                    command[0] == "PASS"
                    or eligible_workers is not None
                )
            ]
            board_size = len(farm.get("tiles", []) or []) or 10
            accesses = _shed_access(board_size)
            for species in species_priority:
                available = min(
                    max(0, int(shed.get(species, 0) or 0)),
                    pickup_needed,
                )
                for _ in range(available):
                    if not free_workers:
                        break
                    worker_id = min(
                        free_workers,
                        key=lambda value: min(
                            _distance(positions[value], access)
                            for access in accesses
                        ),
                    )
                    target = min(
                        accesses,
                        key=lambda value: (
                            _distance(positions[worker_id], value),
                            value,
                        ),
                    )
                    actions[worker_id] = (
                        ["PICKUP", species, 1]
                        if positions[worker_id] == target
                        else _move(positions[worker_id], target)
                    )
                    if positions[worker_id] == target:
                        self.pasture_fill_pickup_commands += 1
                    else:
                        self.pasture_fill_route_actions += 1
                    assigned.add(worker_id)
                    free_workers.remove(worker_id)
                    pickup_needed -= 1
                if pickup_needed <= 0 or not free_workers:
                    break
        _store_unit_actions(action, actions)
        return assigned

    def _crop_choice(
        self,
        *,
        day: int,
        seeds: Counter[str],
    ) -> str | None:
        cutoffs = self.config["reclaimed_crop_cutoffs"]
        for crop in self.config["reclaimed_crop_priority"]:
            if day <= int(cutoffs[crop]) and seeds[crop] > 0:
                seeds[crop] -= 1
                return str(crop)
        return None

    def _reclaimed_crop_tasks(
        self,
        observation: dict[str, Any],
    ) -> list[tuple[int, tuple[int, int], list[Any]]]:
        farm = _farm(observation)
        private = observation.get("private", {}) or {}
        day = int(observation.get("day", 0))
        if (
            day < int(self.config["reclaimed_crop_activation_day"])
            or not self.reclaimed_seed_backfill_requested
        ):
            return []
        seeds = Counter(private.get("seeds", {}) or {})
        tasks: list[tuple[int, tuple[int, int], list[Any]]] = []
        for target in sorted(self.reclaimed_crop_targets, key=lambda p: (p[1], p[0])):
            tile = _tile(farm, target)
            if tile == "LOCKED":
                continue
            if tile is None:
                crop = self._crop_choice(day=day, seeds=seeds)
                if crop is not None:
                    tasks.append((3, target, ["PLANT", crop]))
                continue
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "WEED":
                tasks.append((2, target, ["DIG"]))
                continue
            if tile.get("kind") != "PLANT":
                continue
            crop = str(tile.get("crop", ""))
            mature = day - int(tile.get("planted_day", day)) >= int(
                CROPS.get(crop, {}).get("first_yield_day", 10**6)
            )
            if mature and int(tile.get("yield_units", 0) or 0) > 0:
                tasks.append((0, target, ["HARVEST"]))
            elif day < 29 and not bool(tile.get("watered_today", False)):
                tasks.append((1, target, ["WATER"]))
        return tasks

    def _service_reclaimed_crops(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        unavailable_workers: set[int],
        eligible_workers: set[int] | None = None,
    ) -> None:
        farm = _farm(observation)
        positions = _positions(farm)
        actions = _unit_actions(action, len(positions))
        tasks = self._reclaimed_crop_tasks(observation)

        remaining: list[tuple[int, tuple[int, int], list[Any]]] = []
        for task in tasks:
            _priority, target, command = task
            fulfilled = any(
                worker_id not in unavailable_workers
                and positions[worker_id] == target
                and actions[worker_id]
                and actions[worker_id][0] == command[0]
                for worker_id in range(len(positions))
            )
            if not fulfilled:
                remaining.append(task)

        free_workers = {
            worker_id
            for worker_id, command in enumerate(actions)
            if worker_id not in unavailable_workers
            and (eligible_workers is None or worker_id in eligible_workers)
            and command
            and (command[0] == "PASS" or eligible_workers is not None)
        }
        for _priority, target, command in sorted(
            remaining,
            key=lambda value: (value[0], value[1][1], value[1][0]),
        ):
            if not free_workers:
                break
            worker_id = min(
                free_workers,
                key=lambda value: (
                    _distance(positions[value], target),
                    value,
                ),
            )
            actions[worker_id] = (
                command if positions[worker_id] == target else _move(positions[worker_id], target)
            )
            if positions[worker_id] == target:
                self.reclaimed_crop_actions[str(command[0])] += 1
            else:
                self.reclaimed_crop_actions[str(actions[worker_id][0])] += 1
            free_workers.remove(worker_id)
        _store_unit_actions(action, actions)

    def _filter_market(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        unlocked = len(_farm(observation).get("unlocked_quadrants", []) or [])
        effective_cap = (
            self.livestock_resource_cap
            if unlocked >= 3
            else int(self.config["pre_q2_livestock_resource_cap"])
        )
        remaining = max(
            0,
            effective_cap - _pasture_livestock_resources(observation),
        )
        rebuilt: list[Any] = []
        for order in action.get("market", []) or []:
            if not (
                isinstance(order, list)
                and len(order) >= 3
                and order[0] == "BUY_ANIMAL"
                and str(order[1]) in _PASTURE_LIVESTOCK
            ):
                rebuilt.append(order)
                continue
            requested = max(0, int(order[2]))
            admitted = min(requested, remaining)
            remaining -= admitted
            if admitted:
                rebuilt.append([*order[:2], admitted, *order[3:]])
            if admitted < requested:
                self.clamped_animal_units[str(order[1])] += requested - admitted
        action["market"] = rebuilt

    def _backfill_livestock_market(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        configuration: Any,
    ) -> None:
        day = int(observation.get("day", 0))
        if day > int(self.config["fill_purchase_cutoff_day"]):
            return
        farm = _farm(observation)
        if len(farm.get("unlocked_quadrants", []) or []) < 3:
            return
        built = sum(
            isinstance(_tile(farm, target), dict)
            and _tile(farm, target).get("kind") == "PASTURE"
            for target in self.pasture_targets
        )
        resources = _pasture_livestock_resources(observation)
        planned = sum(
            max(0, int(order[2]))
            for order in action.get("market", []) or []
            if isinstance(order, list)
            and len(order) >= 3
            and order[0] == "BUY_ANIMAL"
            and str(order[1]) in _PASTURE_LIVESTOCK
        )
        shortage = max(0, min(built, self.livestock_resource_cap) - resources - planned)
        if shortage <= 0:
            return
        max_orders = (
            int(configuration.get("maxMarketOrdersPerTurn", 10))
            if isinstance(configuration, dict)
            else int(getattr(configuration, "maxMarketOrdersPerTurn", 10) or 10)
        )
        if len(action.get("market", []) or []) >= max_orders:
            return
        money = float(farm.get("money", 0.0) or 0.0)
        floor = float(self.config["fill_operating_cash_floor"])
        for species in self.config["pasture_fill_species_priority"]:
            cost = max(1.0, float(self.config["animal_costs"][species]))
            affordable = max(0, int((money - floor) // cost))
            quantity = min(shortage, affordable)
            if quantity <= 0:
                continue
            action.setdefault("market", []).append(
                ["BUY_ANIMAL", str(species), quantity]
            )
            self.pasture_fill_purchase_units[str(species)] += quantity
            break

    def _backfill_reclaimed_seed_market(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        configuration: Any,
    ) -> None:
        if self.reclaimed_seed_backfill_requested or int(
            observation.get("day", 0)
        ) < int(self.config["reclaimed_crop_activation_day"]):
            return
        farm = _farm(observation)
        max_orders = (
            int(configuration.get("maxMarketOrdersPerTurn", 10))
            if isinstance(configuration, dict)
            else int(getattr(configuration, "maxMarketOrdersPerTurn", 10) or 10)
        )
        if len(action.get("market", []) or []) >= max_orders:
            return
        units = int(self.config["reclaimed_seed_backfill_units"])
        cost = float(self.config["reclaimed_seed_unit_cost"])
        floor = float(self.config["reclaimed_seed_operating_cash_floor"])
        money = float(farm.get("money", 0.0) or 0.0)
        if money < floor + units * cost:
            return
        action.setdefault("market", []).append(
            ["BUY_SEED", str(self.config["reclaimed_seed_backfill_crop"]), units]
        )
        self.reclaimed_seed_backfill_requested = True
        self.reclaimed_seed_backfill_units += units

    def _activate_fill_mission(self, observation: dict[str, Any]) -> None:
        if self.fill_mission_started or int(observation.get("day", 0)) != int(
            self.config["pasture_fill_mission_day"]
        ):
            return
        farm = _farm(observation)
        if len(farm.get("unlocked_quadrants", []) or []) < 3:
            return
        positions = _positions(farm)
        accesses = set(_shed_access(len(farm.get("tiles", []) or []) or 10))
        candidates = [
            worker_id
            for worker_id, position in enumerate(positions)
            if position in accesses
        ]
        limit = min(
            int(self.config["pasture_fill_mission_worker_limit"]),
            len(self._empty_pastures(farm)),
        )
        self.fill_mission_workers = set(candidates[:limit])
        self.fill_mission_started = bool(self.fill_mission_workers)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        self._observe_topology(observation)
        provider = self.base_policy(observation, configuration)
        action = deepcopy(provider)
        self._filter_unit_actions(action, observation)
        self._filter_market(action, observation)
        self._backfill_livestock_market(action, observation, configuration)
        self._backfill_reclaimed_seed_market(
            action,
            observation,
            configuration,
        )
        self._activate_fill_mission(observation)
        if (
            self.fill_mission_workers
            and int(observation.get("day", 0))
            == int(self.config["pasture_fill_mission_day"])
        ):
            actions = _unit_actions(action, len(_positions(_farm(observation))))
            for worker_id in self.fill_mission_workers:
                if worker_id < len(actions):
                    actions[worker_id] = ["PASS"]
            _store_unit_actions(action, actions)
            fill_workers = self._route_pasture_fill(
                action,
                observation,
                eligible_workers=self.fill_mission_workers,
            )
            self._service_reclaimed_crops(
                action,
                observation,
                unavailable_workers=fill_workers,
                eligible_workers=self.fill_mission_workers,
            )
        self.observation_count += 1
        if action != provider:
            self.override_batches += 1
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base_instance = getattr(
            self.base_policy,
            "codex_e17_batched_cluster_routing_instance",
            None,
        )
        base = (
            base_instance.telemetry_snapshot()
            if base_instance is not None
            else {}
        )
        return {
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "base_agent_version": base.get("agent_version"),
            "target_pastures_by_quadrant": self.target_pastures_by_quadrant,
            "q2_pasture_cap": self.q2_pasture_cap,
            "livestock_resource_cap": self.livestock_resource_cap,
            "reclaimed_crop_targets": [
                list(position) for position in sorted(self.reclaimed_crop_targets)
            ],
            "override_batches": self.override_batches,
            "blocked_builds": {
                str(position): count for position, count in self.blocked_builds.items()
            },
            "blocked_placements": {
                str(position): count
                for position, count in self.blocked_placements.items()
            },
            "clamped_animal_units": dict(self.clamped_animal_units),
            "reclaimed_crop_actions": dict(self.reclaimed_crop_actions),
            "reassigned_blocked_worker_actions": (
                self.reassigned_blocked_worker_actions
            ),
            "fill_mission_workers": sorted(self.fill_mission_workers),
            "fill_mission_started": self.fill_mission_started,
            "pasture_fill_route_actions": self.pasture_fill_route_actions,
            "pasture_fill_place_commands": self.pasture_fill_place_commands,
            "pasture_fill_pickup_commands": self.pasture_fill_pickup_commands,
            "pasture_fill_purchase_units": dict(
                self.pasture_fill_purchase_units
            ),
            "reclaimed_seed_backfill_requested": (
                self.reclaimed_seed_backfill_requested
            ),
            "reclaimed_seed_backfill_units": self.reclaimed_seed_backfill_units,
            "max_active_reclaimed_crops": self.max_active_reclaimed_crops,
            "latest_target_pastures_built": self.latest_target_pastures_built,
            "latest_target_pastures_filled": self.latest_target_pastures_filled,
            "latest_empty_target_pastures": self.latest_empty_target_pastures,
            "max_observed_q2_pastures": self.max_observed_q2_pastures,
            "topology_cap_breaches": self.topology_cap_breaches,
            "provider": base,
        }


def create_codex_e17_topology_cap_662(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy: Callable[..., dict[str, Any]] | None = None,
):
    """Create the fail-closed productive 6-6-2 Kaggle candidate."""

    instance = CodexE17TopologyCap662Agent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_e17_topology_662_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e17_topology_662_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e17_topology_662_instance = instance
    policy.codex_e17_topology_662_last_error = None
    policy.__name__ = "codex_e17_3_topology_fill_662_policy"
    return policy


__all__ = [
    "DEFAULT_TOPOLOGY_662_CONFIG_PATH",
    "TOPOLOGY_662_MODEL_SPEC_VERSION",
    "CodexE17TopologyCap662Agent",
    "create_codex_e17_topology_cap_662",
    "load_topology_662_config",
]
