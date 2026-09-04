"""E18.4 V2 locality/task-aging dispatcher over the frozen V1 envelope.

The V1 task generators, topology, market coordination and lifecycle rules are
inherited unchanged.  This module replaces only worker-to-task matching.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_reactive_service_routing_core import (
    CoreTask,
    _distance,
    _inventories,
    _positions,
)
from agricola.strategy.codex.codex_e17_reactive_service_routing_v3 import (
    _SAFE_PASS,
    CodexE17ReactiveServiceRoutingV3,
)
from agricola.strategy.codex.codex_e18_state_driven_772 import (
    DEFAULT_E18_STATE_DRIVEN_CONFIG_PATH,
    CodexE18StateDriven772Agent,
    load_e18_state_driven_config,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_STATE_DRIVEN_V2_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/CODEX_E18_4_STATE_DRIVEN_772_V2.json"
)
E18_STATE_DRIVEN_V2_MODEL_SPEC_VERSION = "CODEX-E18.4-STATE-DRIVEN-772-V2"

_CLUSTERS = ("Q0_NW", "Q1_NE", "Q2_SW", "SHED_CORRIDOR")
_CLUSTER_ANCHORS = {
    "Q0_NW": (3, 3),
    "Q1_NE": (6, 3),
    "Q2_SW": (3, 6),
    "SHED_CORRIDOR": (4, 4),
}
_EMERGENCIES = frozenset({"CRITICAL_FEED", "CRITICAL_WATER"})
_SHED_TASKS = frozenset({
    "PICKUP_WHEAT",
    "PICKUP_ANIMAL",
    "DROP_INVENTORY",
})
_MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})
_ANIMALS = frozenset({"COW", "SHEEP", "GOOSE"})
_SEEDS = frozenset({"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"})
_PRODUCTS = frozenset({
    "WHEAT",
    "CARROT",
    "TOMATO",
    "STRAWBERRY",
    "MELON",
    "EGG",
    "MILK",
    "WOOL",
    "FERTILIZER",
})


@dataclass
class TaskDispatchState:
    first_seen_step: int
    last_seen_step: int
    age_steps: int = 0
    deadline_slack: int | None = None
    assigned_worker: int | None = None
    assignment_started_step: int | None = None
    preemptions: int = 0
    last_preemption_reason: str | None = None


def load_e18_state_driven_v2_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    """Load V2 and prove that every non-dispatch invariant matches V1."""

    config_path = (
        Path(path) if path is not None else DEFAULT_E18_STATE_DRIVEN_V2_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_4_STATE_DRIVEN_772_V2",
        "schema_version": "e18.codex.state_driven_772.v2",
        "model_spec_version": E18_STATE_DRIVEN_V2_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1",
        "causal_family": "STATE_DRIVEN_772_LOCALITY_TASK_AGING_DISPATCHER",
        "public_features_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")

    v1 = load_e18_state_driven_config(DEFAULT_E18_STATE_DRIVEN_CONFIG_PATH)
    changed_keys = {"candidate_id", "schema_version", "model_spec_version", "causal_family"}
    for key, value in v1.items():
        if key not in changed_keys and config.get(key) != value:
            raise ValueError(f"V2 changed frozen V1 field {key!r}")

    dispatcher = config.get("dispatcher", {})
    if tuple(dispatcher.get("clusters", ())) != _CLUSTERS:
        raise ValueError("V2 requires the four frozen dispatcher clusters")
    for key in (
        "idle_release_steps",
        "remote_backlog_age_steps",
        "remote_backlog_delta",
        "ordinary_transfers_per_cluster_day",
        "age_bucket_steps",
        "route_thrashing_window_steps",
    ):
        if int(dispatcher.get(key, 0)) <= 0:
            raise ValueError(f"dispatcher.{key} must be positive")
    return deepcopy(config)


def _task_cluster(task: CoreTask) -> str:
    if task.kind in _SHED_TASKS:
        return "SHED_CORRIDOR"
    x, y = task.target
    if x < 5 and y < 5:
        return "Q0_NW"
    if x >= 5 and y < 5:
        return "Q1_NE"
    if x < 5 and y >= 5:
        return "Q2_SW"
    return "SHED_CORRIDOR"


def _next_position(position: tuple[int, int], action: list[Any]) -> tuple[int, int]:
    if not action or action[0] not in _MOVES:
        return position
    dx, dy = {
        "NORTH": (0, -1),
        "SOUTH": (0, 1),
        "EAST": (1, 0),
        "WEST": (-1, 0),
    }[str(action[0])]
    return position[0] + dx, position[1] + dy


def _route_step(
    position: tuple[int, int], target: tuple[int, int]
) -> tuple[int, int]:
    if position[0] < target[0]:
        return position[0] + 1, position[1]
    if position[0] > target[0]:
        return position[0] - 1, position[1]
    if position[1] < target[1]:
        return position[0], position[1] + 1
    if position[1] > target[1]:
        return position[0], position[1] - 1
    return position


class CodexE18StateDriven772V2Agent(CodexE18StateDriven772Agent):
    """Persistent locality-aware dispatcher for the frozen E18.4 V1 tasks."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        # The parent is deliberately initialized with V1, then only its config
        # envelope is replaced by a V2 config proven equal on frozen fields.
        super().__init__(
            run_context=run_context,
            config_path=DEFAULT_E18_STATE_DRIVEN_CONFIG_PATH,
            base_policy=base_policy,
        )
        self.config = load_e18_state_driven_v2_config(config_path)
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = E18_STATE_DRIVEN_V2_MODEL_SPEC_VERSION
        self.home_clusters: dict[int, str] = {}
        self.worker_idle_steps: Counter[int] = Counter()
        self.task_states: dict[tuple[Any, ...], TaskDispatchState] = {}
        self.completed_task_states: list[dict[str, Any]] = []
        self.dispatch_records: list[dict[str, Any]] = []
        self.preemption_reasons: Counter[str] = Counter()
        self.cross_cluster_transfers: Counter[str] = Counter()
        self.ownership_changes: list[dict[str, Any]] = []
        self._ordinary_transfers: dict[tuple[int, str], set[int]] = {}
        self._last_dispatch_tasks: list[CoreTask] = []
        self._last_dispatch_assignments: dict[int, CoreTask] = {}
        self._last_dispatch_record_indices: dict[int, int] = {}
        self._last_moves: dict[int, tuple[int, tuple[int, int], tuple[int, int]]] = {}
        self.route_thrashing_violations: list[dict[str, Any]] = []
        self.pass_on_actionable_violations: list[dict[str, Any]] = []
        self.action_by_day_cluster: Counter[tuple[int, str, str]] = Counter()
        self.aged_task_observations: Counter[str] = Counter()
        self.task_latency_steps: dict[str, list[int]] = {}

    @property
    def _dispatcher(self) -> dict[str, Any]:
        return self.config["dispatcher"]

    def _ensure_home_clusters(
        self,
        positions: list[tuple[int, int]],
        tasks: list[CoreTask],
        step: int,
    ) -> None:
        task_load = Counter(_task_cluster(task) for task in tasks)
        load = Counter(self.home_clusters.values())
        worker_count = len(positions)
        quota = {cluster: 1 for cluster in _CLUSTERS}
        if worker_count >= 8:
            quota.update({"Q0_NW": 3, "Q1_NE": 3})
        baseline_load = {"Q0_NW": 5, "Q1_NE": 5, "Q2_SW": 2, "SHED_CORRIDOR": 1}
        while sum(quota.values()) < worker_count:
            cluster = max(
                (
                    value
                    for value in _CLUSTERS
                    if value != "SHED_CORRIDOR" or quota[value] < 2
                ),
                key=lambda value: (
                    (task_load[value] + baseline_load[value]) / (quota[value] + 1),
                    -_CLUSTERS.index(value),
                ),
            )
            quota[cluster] += 1
        for worker_id, position in enumerate(positions):
            if worker_id in self.home_clusters:
                continue
            under_quota = [
                value for value in _CLUSTERS if load[value] < quota[value]
            ]
            constrained_clusters = {
                _task_cluster(task)
                for task in tasks
                if task.allowed_workers is not None
                and worker_id in task.allowed_workers
                and not any(
                    self.home_clusters.get(owner) == _task_cluster(task)
                    and owner in task.allowed_workers
                    for owner in self.home_clusters
                )
            }
            cluster = min(
                constrained_clusters or under_quota or list(_CLUSTERS),
                key=lambda value: (
                    _distance(position, _CLUSTER_ANCHORS[value]) * 100,
                    load[value],
                    _CLUSTERS.index(value),
                ),
            )
            self.home_clusters[worker_id] = cluster
            load[cluster] += 1
            self.ownership_changes.append(
                {
                    "step": step,
                    "worker_id": worker_id,
                    "from": None,
                    "to": cluster,
                    "reason": "INITIAL_MIN_COST_OWNERSHIP",
                }
            )

    def _refresh_task_states(self, tasks: list[CoreTask], step: int) -> None:
        active = {task.identity for task in tasks}
        for identity in tuple(self.task_states):
            if identity not in active:
                state = self.task_states.pop(identity)
                self.completed_task_states.append(
                    {"identity": repr(identity), **asdict(state)}
                )
        for task in tasks:
            state = self.task_states.get(task.identity)
            if state is None:
                state = TaskDispatchState(step, step)
                self.task_states[task.identity] = state
            state.last_seen_step = step
            state.age_steps = step - state.first_seen_step
            state.deadline_slack = self._deadline_slack(task)
            for threshold in (6, 12, 24):
                if state.age_steps >= threshold:
                    self.aged_task_observations[f"GE_{threshold}"] += 1

    def _deadline_slack(self, task: CoreTask) -> int | None:
        if task.kind in _EMERGENCIES:
            return 0
        clock = getattr(self, "_routing_clock", None)
        if clock is None:
            return None
        if task.kind in {"HARVEST", "DROP_INVENTORY"}:
            remaining = int(self.config["episode_steps"]) - 1 - int(clock.step)
            return max(0, remaining)
        return None

    @staticmethod
    def _eligible(task: CoreTask, worker_id: int) -> bool:
        return task.allowed_workers is None or worker_id in task.allowed_workers

    def _carrier_affinity(
        self,
        worker_id: int,
        task: CoreTask,
        inventories: list[dict[str, Any]],
    ) -> int:
        inventory = inventories[worker_id]
        home = self.home_clusters.get(worker_id)
        cluster = _task_cluster(task)
        if int(inventory.get("WHEAT", 0) or 0) > 0 and task.kind in {
            "FEED",
            "CRITICAL_FEED",
        }:
            return 2 if home == cluster else 1
        if any(int(inventory.get(seed, 0) or 0) > 0 for seed in _SEEDS) and task.kind in {
            "PLANT",
            "DIG_TARGET",
        }:
            return 2 if home == cluster else 1
        if any(int(inventory.get(animal, 0) or 0) > 0 for animal in _ANIMALS) and task.kind == "PLACE_ANIMAL":
            return 2
        if any(int(inventory.get(item, 0) or 0) > 0 for item in _PRODUCTS) and task.kind in {
            "HARVEST",
            "DROP_INVENTORY",
        }:
            return 2 if home == cluster else 1
        return 0

    def _cross_cluster_reason(
        self,
        *,
        worker_id: int,
        task: CoreTask,
        available_workers: set[int],
        tasks: list[CoreTask],
        inventories: list[dict[str, Any]],
        day: int,
    ) -> str | None:
        home = self.home_clusters[worker_id]
        cluster = _task_cluster(task)
        if home == cluster:
            return "HOME_CLUSTER"
        positions = getattr(self, "_routing_positions", None)
        if (
            positions
            and worker_id < len(positions)
            and positions[worker_id] == task.target
        ):
            return "ON_TILE_SERVICE"
        if task.kind in _EMERGENCIES:
            home_owners = {
                value
                for value in available_workers
                if self.home_clusters.get(value) == cluster and self._eligible(task, value)
            }
            if not home_owners:
                return "REMOTE_EMERGENCY_NO_OWNER"
        if task.kind in _SHED_TASKS and self._carrier_affinity(
            worker_id, task, inventories
        ):
            return "CARRIER_SHED_TRANSFER"
        if self.worker_idle_steps[worker_id] >= int(
            self._dispatcher["idle_release_steps"]
        ):
            return "LOCAL_IDLE_RELEASE"
        state = self.task_states[task.identity]
        local_backlog = sum(_task_cluster(value) == home for value in tasks)
        remote_backlog = sum(_task_cluster(value) == cluster for value in tasks)
        if (
            state.age_steps >= int(self._dispatcher["remote_backlog_age_steps"])
            and remote_backlog - local_backlog
            >= int(self._dispatcher["remote_backlog_delta"])
        ):
            return "AGED_REMOTE_BACKLOG"
        return None

    def _assign(
        self,
        tasks: list[CoreTask],
        positions: list[tuple[int, int]],
        private: dict[str, Any],
    ) -> dict[int, CoreTask]:
        clock = self._routing_clock
        step, day = int(clock.step), int(clock.day)
        self._ensure_home_clusters(positions, tasks, step)
        self._refresh_task_states(tasks, step)
        inventories = _inventories(private, len(positions))
        self._routing_positions = list(positions)

        for worker_id in range(len(positions)):
            has_local = any(
                _task_cluster(task) == self.home_clusters[worker_id]
                and self._eligible(task, worker_id)
                for task in tasks
            )
            self.worker_idle_steps[worker_id] = 0 if has_local else self.worker_idle_steps[worker_id] + 1

        assignments: dict[int, CoreTask] = {}
        assignment_reasons: dict[int, str] = {}
        available_workers = set(range(len(positions)))
        reserved_targets: set[tuple[Any, ...]] = set()
        remaining_tasks = list(tasks)
        remaining_seeds = Counter(private.get("seeds", {}) or {})
        remaining_shed = Counter(private.get("shed", {}) or {})
        age_bucket_steps = int(self._dispatcher["age_bucket_steps"])
        transfer_limit = int(self._dispatcher["ordinary_transfers_per_cluster_day"])

        while available_workers and remaining_tasks:
            candidates: list[tuple[tuple[Any, ...], int, int, str]] = []
            for task_index, task in enumerate(remaining_tasks):
                target_key = (
                    (task.kind, task.target, task.allowed_workers)
                    if task.kind == "DROP_INVENTORY"
                    else (task.kind, task.target)
                )
                if target_key in reserved_targets:
                    continue
                if task.kind == "PLANT" and remaining_seeds[str(task.resource)] <= 0:
                    continue
                if task.kind in {"PICKUP_WHEAT", "PICKUP_ANIMAL"}:
                    quantity = int(task.action[2]) if len(task.action) >= 3 else 1
                    if remaining_shed[str(task.resource)] < quantity:
                        continue
                state = self.task_states[task.identity]
                for worker_id in sorted(available_workers):
                    if not self._eligible(task, worker_id):
                        continue
                    reason = self._cross_cluster_reason(
                        worker_id=worker_id,
                        task=task,
                        available_workers=available_workers,
                        tasks=tasks,
                        inventories=inventories,
                        day=day,
                    )
                    if reason is None:
                        continue
                    cluster = _task_cluster(task)
                    if reason in {"LOCAL_IDLE_RELEASE", "AGED_REMOTE_BACKLOG"}:
                        used = self._ordinary_transfers.setdefault((day, cluster), set())
                        if worker_id not in used and len(used) >= transfer_limit:
                            continue
                    distance = _distance(positions[worker_id], task.target)
                    previous_move = self._last_moves.get(worker_id)
                    if distance > 0 and previous_move is not None:
                        next_position = _route_step(
                            positions[worker_id], task.target
                        )
                        if (
                            step - previous_move[0]
                            <= int(self._dispatcher["route_thrashing_window_steps"])
                            and positions[worker_id] == previous_move[2]
                            and next_position == previous_move[1]
                        ):
                            continue
                    carrier = self._carrier_affinity(worker_id, task, inventories)
                    sticky = (
                        state.assigned_worker == worker_id
                        or self.last_assignments.get(worker_id) == task.identity
                    )
                    deadline = state.deadline_slack
                    key = (
                        task.priority,
                        deadline if deadline is not None else 10**9,
                        0 if distance == 0 else 1,
                        0 if sticky else 1,
                        0 if self.home_clusters[worker_id] == cluster else 1,
                        -carrier,
                        -(state.age_steps // age_bucket_steps),
                        distance,
                        worker_id,
                        task.target[1],
                        task.target[0],
                        task_index,
                    )
                    candidates.append((key, worker_id, task_index, reason))
            if not candidates:
                break
            _key, worker_id, task_index, reason = min(candidates)
            task = remaining_tasks.pop(task_index)
            target_key = (
                (task.kind, task.target, task.allowed_workers)
                if task.kind == "DROP_INVENTORY"
                else (task.kind, task.target)
            )
            assignments[worker_id] = task
            assignment_reasons[worker_id] = reason
            available_workers.remove(worker_id)
            reserved_targets.add(target_key)
            if task.kind == "PLANT":
                remaining_seeds[str(task.resource)] -= 1
            elif task.kind in {"PICKUP_WHEAT", "PICKUP_ANIMAL"}:
                remaining_shed[str(task.resource)] -= (
                    int(task.action[2]) if len(task.action) >= 3 else 1
                )
            if reason in {"LOCAL_IDLE_RELEASE", "AGED_REMOTE_BACKLOG"}:
                self._ordinary_transfers[(day, _task_cluster(task))].add(worker_id)
            if self.home_clusters[worker_id] != _task_cluster(task):
                self.cross_cluster_transfers[reason] += 1

        for worker_id, task in assignments.items():
            prior_identity = self.last_assignments.get(worker_id)
            if prior_identity is not None and prior_identity != task.identity:
                prior_state = self.task_states.get(prior_identity)
                if prior_state is not None:
                    prior_task = next(
                        (value for value in tasks if value.identity == prior_identity),
                        None,
                    )
                    if prior_task is not None and task.priority < prior_task.priority:
                        reason = f"SAFETY_{prior_task.kind}_TO_{task.kind}"
                        prior_state.preemptions += 1
                        prior_state.last_preemption_reason = reason
                        self.preemption_reasons[reason] += 1
            state = self.task_states[task.identity]
            if state.assigned_worker != worker_id:
                state.assigned_worker = worker_id
                state.assignment_started_step = step

        self._last_dispatch_tasks = list(tasks)
        self._last_dispatch_assignments = dict(assignments)
        self._last_dispatch_record_indices = {}
        for worker_id, task in sorted(assignments.items()):
            state = self.task_states[task.identity]
            inventory = inventories[worker_id]
            distance = _distance(positions[worker_id], task.target)
            record = {
                "step": step,
                "day": day,
                "worker_id": worker_id,
                "position": list(positions[worker_id]),
                "home_cluster": self.home_clusters[worker_id],
                "task_cluster": _task_cluster(task),
                "inventory": {
                    key: int(value)
                    for key, value in sorted(inventory.items())
                    if int(value or 0) > 0
                },
                "task_kind": task.kind,
                "task_identity": repr(task.identity),
                "task_age_steps": state.age_steps,
                "task_priority": task.priority,
                "deadline_slack": state.deadline_slack,
                "target": list(task.target),
                "distance": distance,
                "ownership": assignment_reasons[worker_id],
                "continuation": self.last_assignments.get(worker_id) == task.identity,
                "carrier_affinity": self._carrier_affinity(worker_id, task, inventories),
                "preemption_reason": state.last_preemption_reason,
                "choice_reason": (
                    "ON_TILE_EXECUTION"
                    if distance == 0
                    else "STICKY_CONTINUATION"
                    if self.last_assignments.get(worker_id) == task.identity
                    else assignment_reasons[worker_id]
                ),
                "emitted": None,
            }
            self.dispatch_records.append(record)
            self._last_dispatch_record_indices[worker_id] = len(self.dispatch_records) - 1
            if distance == 0 and task.action and task.action[0] not in _MOVES:
                self.task_latency_steps.setdefault(task.kind, []).append(state.age_steps)
        return assignments

    def _record_emitted_dispatch(self, action: dict[str, Any]) -> None:
        positions = _positions(self._routing_farm)
        actions = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
        step, day = int(self._routing_clock.step), int(self._routing_clock.day)
        window = int(self._dispatcher["route_thrashing_window_steps"])
        for worker_id, position in enumerate(positions):
            emitted = list(actions[worker_id]) if worker_id < len(actions) else ["PASS"]
            op = str(emitted[0]) if emitted else "PASS"
            cluster = self.home_clusters.get(worker_id, "UNASSIGNED")
            kind = "MOVE" if op in _MOVES else "PASS" if op == "PASS" else "PRODUCTIVE"
            self.action_by_day_cluster[(day, cluster, kind)] += 1
            record_index = self._last_dispatch_record_indices.get(worker_id)
            if record_index is not None:
                self.dispatch_records[record_index]["emitted"] = deepcopy(emitted)
            if op in _MOVES:
                target = _next_position(position, emitted)
                previous = self._last_moves.get(worker_id)
                if (
                    previous is not None
                    and step - previous[0] <= window
                    and position == previous[2]
                    and target == previous[1]
                ):
                    self.route_thrashing_violations.append(
                        {
                            "step": step,
                            "worker_id": worker_id,
                            "route": [list(previous[1]), list(previous[2]), list(target)],
                        }
                    )
                self._last_moves[worker_id] = (step, position, target)
            elif op == "PASS":
                reserved_targets = {
                    task.target for task in self._last_dispatch_assignments.values()
                }
                actionable = [
                    task
                    for task in self._last_dispatch_tasks
                    if task.target == position
                    and task.target not in reserved_targets
                    and self._eligible(task, worker_id)
                ]
                if actionable:
                    self.pass_on_actionable_violations.append(
                        {
                            "step": step,
                            "worker_id": worker_id,
                            "position": list(position),
                            "task_kinds": sorted({task.kind for task in actionable}),
                        }
                    )

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        day = int(observation.get("day", 0))
        if day != self.last_scheduler_day:
            self.daily_modes.append(
                {
                    "day": day,
                    "mode": (
                        "E18_2_BOOTSTRAP"
                        if day < int(self.config["activation_day"])
                        else "STATE_DRIVEN_772_V2_LOCALITY_TASK_AGING"
                    ),
                }
            )
            # Unlike V1, ownership and assignments survive the day boundary.
            self.last_scheduler_day = day
        action = CodexE17ReactiveServiceRoutingV3.__call__(
            self, observation, configuration
        )
        if day >= int(self.config["activation_day"]):
            self._record_emitted_dispatch(action)
        return action

    @staticmethod
    def _latency_summary(values: list[int]) -> dict[str, float | int | None]:
        if not values:
            return {"count": 0, "p50": None, "p90": None, "max": None}
        ordered = sorted(values)
        return {
            "count": len(ordered),
            "p50": ordered[(len(ordered) - 1) // 2],
            "p90": ordered[min(len(ordered) - 1, (9 * len(ordered) - 1) // 10)],
            "max": ordered[-1],
        }

    def telemetry_snapshot(self) -> dict[str, Any]:
        telemetry = super().telemetry_snapshot()
        action_by_day_cluster = {
            f"D{day}:{cluster}:{kind}": count
            for (day, cluster, kind), count in sorted(self.action_by_day_cluster.items())
        }
        productive = self.service_commands
        return {
            **telemetry,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "dispatcher": "LOCALITY_TASK_AGING_V2",
            "home_clusters": {str(key): value for key, value in sorted(self.home_clusters.items())},
            "task_states": {
                repr(identity): asdict(state)
                for identity, state in sorted(self.task_states.items(), key=lambda item: repr(item[0]))
            },
            "completed_task_state_count": len(self.completed_task_states),
            "dispatch_record_count": len(self.dispatch_records),
            "dispatch_records": deepcopy(self.dispatch_records),
            "move_per_productive": self.routing_commands / productive if productive else None,
            "task_latency_steps": {
                kind: self._latency_summary(values)
                for kind, values in sorted(self.task_latency_steps.items())
            },
            "aged_task_observations": dict(self.aged_task_observations),
            "preemption_reasons": dict(self.preemption_reasons),
            "cross_cluster_transfers": dict(self.cross_cluster_transfers),
            "route_thrashing_violations": len(self.route_thrashing_violations),
            "route_thrashing_records": deepcopy(self.route_thrashing_violations),
            "pass_on_actionable_violations": len(self.pass_on_actionable_violations),
            "pass_on_actionable_records": deepcopy(self.pass_on_actionable_violations),
            "ownership_changes": deepcopy(self.ownership_changes),
            "worker_idle_steps": dict(self.worker_idle_steps),
            "action_by_day_cluster": action_by_day_cluster,
        }


def create_codex_e18_state_driven_772_v2(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    """Create the fail-closed E18.4 V2 development policy."""

    instance = CodexE18StateDriven772V2Agent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_state_driven_v2_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_state_driven_v2_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_state_driven_v2_instance = instance
    policy.codex_e18_state_driven_v2_last_error = None
    policy.__name__ = "codex_e18_4_state_driven_772_v2_policy"
    return policy


__all__ = [
    "DEFAULT_E18_STATE_DRIVEN_V2_CONFIG_PATH",
    "E18_STATE_DRIVEN_V2_MODEL_SPEC_VERSION",
    "CodexE18StateDriven772V2Agent",
    "TaskDispatchState",
    "create_codex_e18_state_driven_772_v2",
    "load_e18_state_driven_v2_config",
]
