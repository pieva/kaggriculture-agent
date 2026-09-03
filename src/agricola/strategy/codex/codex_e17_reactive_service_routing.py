"""E17.2 state-driven service and routing over the Codex E17.1 V2 provider.

The provider retains exclusive ownership of market, acquisition, expansion,
placement and feasible structural work.  This layer observes the current farm
and routes units to biological services, replacing only idle/invalid commands
or commands pre-empted by a measurable end-of-day survival deadline.
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
from agricola.strategy.codex.codex_e17_true_reactive import (
    create_codex_e17_true_reactive_agent,
)
from agricola.strategy.codex.codex_v9_routine_data import ROUTINE_ACTIONS

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SERVICE_ROUTING_CONFIG_PATH = (
    REPO_ROOT
    / "experiments/e17/configs/codex/"
    / "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_V1.json"
)
SERVICE_ROUTING_MODEL_SPEC_VERSION = "CODEX-E17.2-REACTIVE-SERVICE-ROUTING-V1"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
_MOVES = {
    "NORTH": (0, -1),
    "SOUTH": (0, 1),
    "EAST": (1, 0),
    "WEST": (-1, 0),
}
_STRUCTURAL_OPS = {
    "PLANT",
    "DIG",
    "BUILD_COOP",
    "BUILD_PASTURE",
    "PLACE",
    "PICKUP",
    "DROP",
    "FERTILIZE",
}


@dataclass(frozen=True)
class ServiceTask:
    """One observable unit task; no hidden plan or imputed engine result."""

    kind: str
    target: tuple[int, int]
    action: tuple[Any, ...]
    critical: bool = False


@dataclass(frozen=True)
class RoutingAssignment:
    """Short-lived route to an observed task."""

    kind: str
    target: tuple[int, int]
    action: tuple[Any, ...]
    critical: bool = False
    origin: tuple[int, int] | None = None
    phase: str = "OUTBOUND"


def load_service_routing_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path) if path is not None else DEFAULT_SERVICE_ROUTING_CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_V1",
        "model_spec_version": SERVICE_ROUTING_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E17.1-TRUE-REACTIVE-V2",
        "causal_family": "REACTIVE_SERVICE_AND_ROUTING",
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    for key in (
        "turns_per_day",
        "episode_steps",
        "critical_unfed_threshold",
        "critical_unwatered_threshold",
        "deadline_buffer_steps",
        "feed_pickup_batch",
    ):
        if int(config.get(key, -1)) < 0:
            raise ValueError(f"{key} must be non-negative")
    if int(config["turns_per_day"]) <= 0 or int(config["episode_steps"]) <= 0:
        raise ValueError("clock dimensions must be positive")
    expected_priority = {
        "CRITICAL_WATER",
        "CRITICAL_FEED",
        "HARVEST",
        "WATER",
        "FEED",
        "COLLECT_FERTILIZER",
        "CARE",
    }
    if set(config.get("task_priority", [])) != expected_priority:
        raise ValueError("task_priority must contain every service kind exactly once")
    return deepcopy(config)


def _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:
    return [
        tuple(farm.get("farmer", [4, 4])),
        *(tuple(pos) for pos in farm.get("hands", []) or []),
    ]


def _inventories(private: dict[str, Any], count: int) -> list[dict[str, Any]]:
    values = [
        inv if isinstance(inv, dict) else {}
        for inv in (private.get("inventories", []) or [])
    ]
    values.extend({} for _ in range(max(0, count - len(values))))
    return values[:count]


def _unit_actions(action: dict[str, Any], count: int) -> list[list[Any]]:
    values = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
    values.extend(["PASS"] for _ in range(max(0, count - len(values))))
    return [value if isinstance(value, list) and value else ["PASS"] for value in values[:count]]


def _set_unit_action(action: dict[str, Any], worker_id: int, value: list[Any]) -> None:
    if worker_id == 0:
        action["farmer"] = value
        return
    hands = action.setdefault("hands", [])
    while len(hands) < worker_id:
        hands.append(["PASS"])
    hands[worker_id - 1] = value


def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
    x, y = position
    rows = farm.get("tiles", []) or []
    if y < 0 or y >= len(rows) or x < 0 or x >= len(rows[y]):
        return "OUT_OF_BOUNDS"
    return rows[y][x]


def _shed_access(board_size: int) -> tuple[tuple[int, int], ...]:
    half = board_size // 2
    return (
        (half - 1, half - 1),
        (half, half - 1),
        (half - 1, half),
        (half, half),
    )


def _distance(source: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(source[0] - target[0]) + abs(source[1] - target[1])


def _move_towards(source: tuple[int, int], target: tuple[int, int]) -> list[str]:
    sx, sy = source
    tx, ty = target
    # Horizontal-first is deterministic and matches the coordinate contract.
    if sx < tx:
        return ["EAST"]
    if sx > tx:
        return ["WEST"]
    if sy < ty:
        return ["SOUTH"]
    if sy > ty:
        return ["NORTH"]
    return ["PASS"]


def _is_feasible(
    unit_action: list[Any],
    *,
    position: tuple[int, int],
    inventory: dict[str, Any],
    farm: dict[str, Any],
    private: dict[str, Any],
    board_size: int,
) -> bool:
    """Mirror the public engine's local preconditions conservatively."""

    if not unit_action:
        return False
    op = str(unit_action[0])
    tile = _tile(farm, position)
    if op == "PASS":
        return True
    if op in _MOVES:
        dx, dy = _MOVES[op]
        nx, ny = position[0] + dx, position[1] + dy
        return 0 <= nx < board_size and 0 <= ny < board_size
    if op == "DROP":
        return position in _shed_access(board_size) and any(
            int(value or 0) > 0 for value in inventory.values()
        )
    if op == "PICKUP":
        if position not in _shed_access(board_size) or len(unit_action) < 2:
            return False
        return int((private.get("shed", {}) or {}).get(str(unit_action[1]), 0) or 0) > 0
    if op == "PLACE":
        if len(unit_action) < 2:
            return False
        item = str(unit_action[1])
        if (
            item in {"COW", "SHEEP", "GOOSE"}
            and isinstance(tile, dict)
            and tile.get("kind") == ("COOP" if item == "GOOSE" else "PASTURE")
            and not tile.get("animal")
        ):
            return int(inventory.get(item, 0) or 0) > 0
        return position in _shed_access(board_size) and int(inventory.get(item, 0) or 0) > 0
    if tile == "LOCKED" or tile == "OUT_OF_BOUNDS":
        return False
    if op == "PLANT":
        return (
            len(unit_action) >= 2
            and tile is None
            and int((private.get("seeds", {}) or {}).get(str(unit_action[1]), 0) or 0) > 0
        )
    if op == "DIG":
        return tile is not None and not (
            isinstance(tile, dict) and tile.get("animal")
        )
    if op in {"BUILD_COOP", "BUILD_PASTURE"}:
        return tile is None
    if op == "WATER":
        return (
            isinstance(tile, dict)
            and tile.get("kind") == "PLANT"
            and not bool(tile.get("watered_today", False))
        )
    if op == "HARVEST":
        return isinstance(tile, dict) and int(tile.get("yield_units", 0) or 0) > 0
    if op == "FERTILIZE":
        return (
            isinstance(tile, dict)
            and tile.get("kind") == "PLANT"
            and int(inventory.get("FERTILIZER", 0) or 0) > 0
        )
    if op == "FEED":
        return (
            isinstance(tile, dict)
            and bool(tile.get("animal"))
            and not bool(tile.get("fed_today", False))
            and int(inventory.get("WHEAT", 0) or 0) > 0
        )
    if op == "COLLECT_FERTILIZER":
        return (
            isinstance(tile, dict)
            and bool(tile.get("animal"))
            and bool(tile.get("fertilizer_available", False))
        )
    if op == "CARE":
        return (
            isinstance(tile, dict)
            and bool(tile.get("animal"))
            and not bool(tile.get("cared_today", False))
        )
    # Preserve unknown future engine verbs instead of claiming they are invalid.
    return True


class CodexE17ReactiveServiceRoutingAgent:
    """Auditable state-driven unit dispatcher with an immutable V2 provider."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
    ) -> None:
        self.config = load_service_routing_config(config_path)
        self.run_context = deepcopy(run_context or {})
        self.base_policy = create_codex_e17_true_reactive_agent(
            run_context=self.run_context
        )
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = SERVICE_ROUTING_MODEL_SPEC_VERSION
        self.assignments: dict[int, RoutingAssignment] = {}
        self.observation_count = 0
        self.override_batches = 0
        self.override_commands = 0
        self.routing_overrides = 0
        self.service_overrides = 0
        self.idle_repairs = 0
        self.invalid_repairs = 0
        self.critical_overrides = 0
        self.market_mutations = 0
        self.feasible_structural_mutations = 0
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.override_reasons: Counter[str] = Counter()
        self.override_tasks: Counter[str] = Counter()
        self.execution_outcomes: Counter[str] = Counter()
        self.override_records: list[dict[str, Any]] = []
        self._pending_records: list[int] = []

    def _tasks(self, farm: dict[str, Any]) -> list[ServiceTask]:
        tasks: list[ServiceTask] = []
        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict):
                    continue
                position = (x, y)
                if tile.get("kind") == "PLANT" and not bool(
                    tile.get("watered_today", False)
                ):
                    critical = int(tile.get("consecutive_unwatered", 0) or 0) >= int(
                        self.config["critical_unwatered_threshold"]
                    )
                    if critical:
                        tasks.append(
                            ServiceTask(
                                "CRITICAL_WATER",
                                position,
                                ("WATER",),
                                True,
                            )
                        )
                if tile.get("animal") and not bool(tile.get("fed_today", False)):
                    critical = int(tile.get("consecutive_unfed", 0) or 0) >= int(
                        self.config["critical_unfed_threshold"]
                    )
                    if critical:
                        tasks.append(
                            ServiceTask(
                                "CRITICAL_FEED",
                                position,
                                ("FEED",),
                                True,
                            )
                        )
        priority = {
            name: rank for rank, name in enumerate(self.config["task_priority"])
        }
        return sorted(tasks, key=lambda task: (priority[task.kind], task.target))

    def _assignment_due(
        self,
        assignment: RoutingAssignment,
        *,
        position: tuple[int, int],
        farm: dict[str, Any],
        inventory: dict[str, Any],
    ) -> bool:
        if assignment.phase == "RETURN":
            return position != assignment.target
        if assignment.kind == "STAGE_FEED":
            return int(inventory.get("WHEAT", 0) or 0) <= 0
        tile = _tile(farm, assignment.target)
        if not isinstance(tile, dict):
            return False
        if assignment.kind in {"WATER", "CRITICAL_WATER"}:
            return tile.get("kind") == "PLANT" and not bool(
                tile.get("watered_today", False)
            )
        if assignment.kind in {"FEED", "CRITICAL_FEED"}:
            return bool(tile.get("animal")) and not bool(tile.get("fed_today", False))
        if assignment.kind == "HARVEST":
            return int(tile.get("yield_units", 0) or 0) > 0
        if assignment.kind == "COLLECT_FERTILIZER":
            return bool(tile.get("animal")) and bool(
                tile.get("fertilizer_available", False)
            )
        if assignment.kind == "CARE":
            return bool(tile.get("animal")) and not bool(tile.get("cared_today", False))
        return False

    def _critical_pressure(
        self,
        task: ServiceTask,
        *,
        position: tuple[int, int],
        inventory: dict[str, Any],
        farm: dict[str, Any],
        private: dict[str, Any],
        board_size: int,
        hour: int,
    ) -> bool:
        if not task.critical or not self.config["enable_deadline_routing"]:
            return False
        required = _distance(position, task.target) + 1
        if task.kind == "CRITICAL_FEED" and int(inventory.get("WHEAT", 0) or 0) <= 0:
            shed_wheat = int((private.get("shed", {}) or {}).get("WHEAT", 0) or 0)
            if shed_wheat <= 0:
                return False
            accesses = _shed_access(board_size)
            required = min(
                _distance(position, access)
                + 1
                + _distance(access, task.target)
                + 1
                for access in accesses
            )
        remaining_actions = int(self.config["turns_per_day"]) - hour
        return required + int(self.config["deadline_buffer_steps"]) >= remaining_actions

    @staticmethod
    def _task_for_assignment(
        task: ServiceTask, origin: tuple[int, int]
    ) -> RoutingAssignment:
        return RoutingAssignment(
            task.kind,
            task.target,
            task.action,
            task.critical,
            origin,
            "OUTBOUND",
        )

    @staticmethod
    def _scheduled_action(step: int, worker_id: int) -> list[Any]:
        if not 0 <= step < len(ROUTINE_ACTIONS):
            return ["PASS"]
        action = ROUTINE_ACTIONS[step]
        if worker_id == 0:
            value = action.get("farmer", ["PASS"])
        else:
            hands = action.get("hands", []) or []
            value = hands[worker_id - 1] if worker_id - 1 < len(hands) else ["PASS"]
        return value if isinstance(value, list) and value else ["PASS"]

    def _pass_window(self, step: int, worker_id: int) -> int:
        window = 0
        for future_step in range(step, len(ROUTINE_ACTIONS)):
            action = self._scheduled_action(future_step, worker_id)
            if not action or action[0] != "PASS":
                break
            window += 1
        return window

    def _scheduled_service_coverage(
        self,
        *,
        snapshot: Any,
        positions: list[tuple[int, int]],
        inventories: list[dict[str, Any]],
        current_units: list[list[Any]],
        board_size: int,
    ) -> set[tuple[str, tuple[int, int]]]:
        """Conservatively project services already covered by the provider today."""

        shadow_positions = list(positions)
        shadow_wheat = [int(inv.get("WHEAT", 0) or 0) for inv in inventories]
        shed_wheat = int((snapshot.private.get("shed", {}) or {}).get("WHEAT", 0) or 0)
        coverage: set[tuple[str, tuple[int, int]]] = set()
        day_end = min(
            len(ROUTINE_ACTIONS) - 1,
            (snapshot.clock.day + 1) * int(self.config["turns_per_day"]) - 1,
        )
        for step in range(snapshot.clock.step, day_end + 1):
            for worker_id in range(len(shadow_positions)):
                unit_action = (
                    current_units[worker_id]
                    if step == snapshot.clock.step
                    else self._scheduled_action(step, worker_id)
                )
                op = str(unit_action[0]) if unit_action else "PASS"
                position = shadow_positions[worker_id]
                if op in _MOVES:
                    dx, dy = _MOVES[op]
                    nx, ny = position[0] + dx, position[1] + dy
                    if 0 <= nx < board_size and 0 <= ny < board_size:
                        shadow_positions[worker_id] = (nx, ny)
                elif op == "PICKUP" and len(unit_action) >= 2 and unit_action[1] == "WHEAT":
                    requested = int(unit_action[2]) if len(unit_action) >= 3 else 1
                    picked = min(max(0, requested), shed_wheat)
                    shadow_wheat[worker_id] += picked
                    shed_wheat -= picked
                elif op == "WATER":
                    coverage.add(("CRITICAL_WATER", position))
                elif op == "FEED" and shadow_wheat[worker_id] > 0:
                    coverage.add(("CRITICAL_FEED", position))
                    shadow_wheat[worker_id] -= 1
        return coverage

    def _select_task(
        self,
        *,
        worker_id: int,
        position: tuple[int, int],
        inventory: dict[str, Any],
        tasks: list[ServiceTask],
        reserved: set[tuple[str, tuple[int, int]]],
        critical_only: bool,
        max_round_trip_distance: int,
    ) -> RoutingAssignment | None:
        priority = {
            name: rank for rank, name in enumerate(self.config["task_priority"])
        }
        candidates = []
        for task in tasks:
            if critical_only and not task.critical:
                continue
            if (task.kind, task.target) in reserved:
                continue
            if task.kind in {"FEED", "CRITICAL_FEED"} and int(
                inventory.get("WHEAT", 0) or 0
            ) <= 0:
                continue
            if _distance(position, task.target) > max_round_trip_distance:
                continue
            candidates.append(
                (priority[task.kind], _distance(position, task.target), task.target, task)
            )
        if not candidates:
            return None
        return self._task_for_assignment(min(candidates)[3], position)

    def _feed_staging_assignment(
        self,
        *,
        position: tuple[int, int],
        tasks: list[ServiceTask],
        private: dict[str, Any],
        board_size: int,
    ) -> RoutingAssignment | None:
        if int((private.get("shed", {}) or {}).get("WHEAT", 0) or 0) <= 0:
            return None
        if not any(task.kind == "CRITICAL_FEED" for task in tasks):
            return None
        if position not in _shed_access(board_size):
            return None
        target = min(
            _shed_access(board_size),
            key=lambda access: (_distance(position, access), access),
        )
        return RoutingAssignment(
            "STAGE_FEED",
            target,
            ("PICKUP", "WHEAT"),
            True,
            position,
            "OUTBOUND",
        )

    def _emit_assignment(
        self,
        assignment: RoutingAssignment,
        *,
        position: tuple[int, int],
        private: dict[str, Any],
    ) -> list[Any]:
        if assignment.phase == "RETURN":
            return _move_towards(position, assignment.target)
        if position != assignment.target:
            return _move_towards(position, assignment.target)
        if assignment.kind == "STAGE_FEED":
            available = int((private.get("shed", {}) or {}).get("WHEAT", 0) or 0)
            quantity = min(available, int(self.config["feed_pickup_batch"]))
            return ["PICKUP", "WHEAT", quantity] if quantity > 0 else ["PASS"]
        return list(assignment.action)

    def _settle_pending(self, snapshot: Any) -> None:
        for index in self._pending_records:
            record = self.override_records[index]
            worker_id = int(record["worker_id"])
            positions = _positions(snapshot.farm)
            inventories = _inventories(snapshot.private, len(positions))
            if worker_id >= len(positions):
                outcome = "UNKNOWN"
            else:
                action = record["emitted_unit_action"]
                op = str(action[0]) if action else "PASS"
                current_position = positions[worker_id]
                target = tuple(record["target"])
                tile = _tile(snapshot.farm, target)
                if op in _MOVES:
                    dx, dy = _MOVES[op]
                    expected = (
                        int(record["source_position"][0]) + dx,
                        int(record["source_position"][1]) + dy,
                    )
                    outcome = "EXECUTED" if current_position == expected else "NOT_EXECUTED"
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
                elif op == "CARE":
                    outcome = (
                        "EXECUTED"
                        if isinstance(tile, dict)
                        and tile.get("animal")
                        and bool(tile.get("cared_today", False))
                        else "UNKNOWN" if snapshot.clock.hour == 0 else "NOT_EXECUTED"
                    )
                elif op == "COLLECT_FERTILIZER":
                    outcome = (
                        "EXECUTED"
                        if isinstance(tile, dict)
                        and tile.get("animal")
                        and not bool(tile.get("fertilizer_available", False))
                        else "UNKNOWN" if snapshot.clock.hour == 0 else "NOT_EXECUTED"
                    )
                elif op == "HARVEST":
                    before_yield = int(record.get("target_yield_before", 0) or 0)
                    after_yield = int(tile.get("yield_units", 0) or 0) if isinstance(tile, dict) else 0
                    outcome = "EXECUTED" if after_yield < before_yield else "NOT_EXECUTED"
                elif op == "PICKUP":
                    before_wheat = int(record.get("worker_wheat_before", 0) or 0)
                    after_wheat = int(inventories[worker_id].get("WHEAT", 0) or 0)
                    outcome = "EXECUTED" if after_wheat > before_wheat else "NOT_EXECUTED"
                else:
                    outcome = "UNKNOWN"
            record["outcome"] = outcome
            record["post_state_id"] = snapshot.state_id
            record["post_snapshot_fingerprint"] = snapshot.snapshot_fingerprint
            self.execution_outcomes[outcome] += 1
            assignment = self.assignments.get(worker_id)
            if (
                outcome == "EXECUTED"
                and assignment is not None
                and assignment.phase == "OUTBOUND"
                and assignment.origin is not None
                and op not in _MOVES
            ):
                self.assignments[worker_id] = RoutingAssignment(
                    "RETURN",
                    assignment.origin,
                    ("PASS",),
                    assignment.critical,
                    assignment.origin,
                    "RETURN",
                )
        self._pending_records = []

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
        provider_action = self.base_policy(observation, configuration)
        action = deepcopy(provider_action)
        positions = _positions(snapshot.farm)
        inventories = _inventories(snapshot.private, len(positions))
        provider_units = _unit_actions(provider_action, len(positions))
        board_size = int(snapshot.configuration_snapshot["boardSize"])
        tasks = self._tasks(snapshot.farm)
        scheduled_coverage = self._scheduled_service_coverage(
            snapshot=snapshot,
            positions=positions,
            inventories=inventories,
            current_units=provider_units,
            board_size=board_size,
        )
        tasks = [
            task
            for task in tasks
            if (task.kind, task.target) not in scheduled_coverage
        ]
        reserved: set[tuple[str, tuple[int, int]]] = set()
        changed_this_batch = False

        for worker_id, (position, inventory, proposed) in enumerate(
            zip(positions, inventories, provider_units, strict=True)
        ):
            feasible = _is_feasible(
                proposed,
                position=position,
                inventory=inventory,
                farm=snapshot.farm,
                private=snapshot.private,
                board_size=board_size,
            )
            op = str(proposed[0]) if proposed else "PASS"
            structural_feasible = op in _STRUCTURAL_OPS and feasible
            pass_window = self._pass_window(snapshot.clock.step, worker_id)
            max_detour_distance = max(0, (pass_window - 1) // 2)

            assignment = self.assignments.get(worker_id)
            if assignment and not self._assignment_due(
                assignment,
                position=position,
                farm=snapshot.farm,
                inventory=inventory,
            ):
                if assignment.origin is not None and position != assignment.origin:
                    assignment = RoutingAssignment(
                        "RETURN",
                        assignment.origin,
                        ("PASS",),
                        assignment.critical,
                        assignment.origin,
                        "RETURN",
                    )
                    self.assignments[worker_id] = assignment
                else:
                    self.assignments.pop(worker_id, None)
                    assignment = None

            pressured = [
                task
                for task in tasks
                if self._critical_pressure(
                    task,
                    position=position,
                    inventory=inventory,
                    farm=snapshot.farm,
                    private=snapshot.private,
                    board_size=board_size,
                    hour=snapshot.clock.hour,
                )
                and (task.kind, task.target) not in reserved
            ]
            if pressured and op == "PASS":
                assignment = self._select_task(
                    worker_id=worker_id,
                    position=position,
                    inventory=inventory,
                    tasks=pressured,
                    reserved=reserved,
                    critical_only=True,
                    max_round_trip_distance=max_detour_distance,
                )
                if assignment is None and self.config["enable_normal_service"]:
                    assignment = self._feed_staging_assignment(
                        position=position,
                        tasks=pressured,
                        private=snapshot.private,
                        board_size=board_size,
                    )
            elif structural_feasible:
                # A valid build/plant/place/logistics command remains provider-owned.
                continue
            elif assignment is not None and op != "PASS":
                # A detour is admitted only inside a provider PASS window.  If
                # an unexpected provider command appears, it keeps ownership.
                continue
            elif assignment is None and (
                (op == "PASS" and self.config["enable_idle_repair"])
                or (not feasible and self.config["enable_invalid_repair"])
            ):
                if self.config["enable_normal_service"]:
                    assignment = self._select_task(
                        worker_id=worker_id,
                        position=position,
                        inventory=inventory,
                        tasks=tasks,
                        reserved=reserved,
                        critical_only=False,
                        max_round_trip_distance=max_detour_distance,
                    )
                if assignment is None:
                    assignment = self._feed_staging_assignment(
                        position=position,
                        tasks=tasks,
                        private=snapshot.private,
                        board_size=board_size,
                    )

            if assignment is None:
                continue
            emitted = self._emit_assignment(
                assignment,
                position=position,
                private=snapshot.private,
            )
            if emitted == proposed or emitted == ["PASS"]:
                reserved.add((assignment.kind, assignment.target))
                self.assignments[worker_id] = assignment
                continue

            _set_unit_action(action, worker_id, emitted)
            self.assignments[worker_id] = assignment
            reserved.add((assignment.kind, assignment.target))
            reason = (
                "CRITICAL_DEADLINE_OVERRIDE"
                if assignment.critical
                else "IDLE_SERVICE_REPAIR"
                if op == "PASS"
                else "INVALID_SERVICE_REPAIR"
                if not feasible
                else "ASSIGNMENT_CONTINUATION"
            )
            self.override_reasons[reason] += 1
            self.override_tasks[assignment.kind] += 1
            self.override_commands += 1
            self.critical_overrides += int(assignment.critical)
            self.idle_repairs += int(op == "PASS")
            self.invalid_repairs += int(not feasible and op != "PASS")
            if emitted[0] in _MOVES:
                self.routing_overrides += 1
            else:
                self.service_overrides += 1
            if structural_feasible:
                self.feasible_structural_mutations += 1
            target_tile = _tile(snapshot.farm, assignment.target)
            record = {
                "step": snapshot.clock.step,
                "day": snapshot.clock.day,
                "hour": snapshot.clock.hour,
                "worker_id": worker_id,
                "source_position": list(position),
                "target": list(assignment.target),
                "task_kind": assignment.kind,
                "critical": assignment.critical,
                "reason": reason,
                "provider_unit_action": deepcopy(proposed),
                "emitted_unit_action": deepcopy(emitted),
                "provider_action_sha256": stable_payload_hash(provider_action),
                "emitted_action_sha256": None,
                "state_id": snapshot.state_id,
                "snapshot_fingerprint": snapshot.snapshot_fingerprint,
                "target_yield_before": (
                    int(target_tile.get("yield_units", 0) or 0)
                    if isinstance(target_tile, dict)
                    else 0
                ),
                "worker_wheat_before": int(inventory.get("WHEAT", 0) or 0),
                "outcome": "PENDING_NEXT_OBSERVATION",
            }
            self.override_records.append(record)
            self._pending_records.append(len(self.override_records) - 1)
            changed_this_batch = True

        if action.get("market", []) != provider_action.get("market", []):
            self.market_mutations += 1
        if changed_this_batch:
            emitted_hash = stable_payload_hash(action)
            for index in self._pending_records:
                self.override_records[index]["emitted_action_sha256"] = emitted_hash
            self.override_batches += 1
        self.observation_count += 1
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        # The engine does not invoke the policy on its terminal observation, so
        # a last-step intervention has no next callback on which to settle.
        for index in self._pending_records:
            record = self.override_records[index]
            record["outcome"] = "UNKNOWN"
            self.execution_outcomes["UNKNOWN"] += 1
        self._pending_records = []
        provider = self.base_policy.codex_e17_true_reactive_instance.telemetry_snapshot()
        return {
            "agent_version": self.model_spec_version,
            "base_agent_version": provider["agent_version"],
            "observations": self.observation_count,
            "override_batches": self.override_batches,
            "override_commands": self.override_commands,
            "routing_overrides": self.routing_overrides,
            "service_overrides": self.service_overrides,
            "idle_repairs": self.idle_repairs,
            "invalid_repairs": self.invalid_repairs,
            "critical_overrides": self.critical_overrides,
            "market_mutations": self.market_mutations,
            "feasible_structural_mutations": self.feasible_structural_mutations,
            "override_reasons": dict(self.override_reasons),
            "override_tasks": dict(self.override_tasks),
            "execution_outcomes": dict(self.execution_outcomes),
            "open_assignments": {
                str(worker_id): {
                    "kind": assignment.kind,
                    "target": list(assignment.target),
                    "critical": assignment.critical,
                }
                for worker_id, assignment in sorted(self.assignments.items())
            },
            "override_records": deepcopy(self.override_records),
            "provider": provider,
        }


def create_codex_e17_reactive_service_routing_agent(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    """Create the fail-closed Kaggle-compatible E17.2 development policy."""

    instance = CodexE17ReactiveServiceRoutingAgent(
        run_context=run_context,
        config_path=config_path,
    )

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_e17_service_routing_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e17_service_routing_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e17_service_routing_instance = instance
    policy.codex_e17_service_routing_last_error = None
    policy.__name__ = "codex_e17_2_reactive_service_routing_v1_policy"
    return policy


__all__ = [
    "SERVICE_ROUTING_MODEL_SPEC_VERSION",
    "CodexE17ReactiveServiceRoutingAgent",
    "RoutingAssignment",
    "ServiceTask",
    "create_codex_e17_reactive_service_routing_agent",
    "load_service_routing_config",
]
