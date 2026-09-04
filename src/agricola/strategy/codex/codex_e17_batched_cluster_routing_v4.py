"""E17.2 inventory/deadline batching and optional quadrant affinity.

The V4 keeps the complete V3 D28 service and terminal market behavior.  It
changes only when a worker returns to the shed and, in the V4B ablation, how
otherwise equivalent routes are biased toward the worker's current quadrant.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_reactive_service_routing_core import (
    CoreTask,
    _animal_tiles,
    _distance,
    _inventories,
    _shed_access,
)
from agricola.strategy.codex.codex_e17_reactive_service_routing_v3 import (
    _ANIMAL_PRODUCTS,
    _SAFE_PASS,
    CodexE17ReactiveServiceRoutingV3,
    load_v3_config,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_V4A_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/configs/"
    / "CODEX_E17_2_BATCHED_ROUTING_V4A_D28.json"
)
DEFAULT_V4B_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/configs/"
    / "CODEX_E17_2_CLUSTERED_ROUTING_V4B_D28.json"
)
DEFAULT_V4C_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/configs/"
    / "CODEX_E17_2_CAPACITY_AWARE_BATCHED_ROUTING_V4C_D28.json"
)
DEFAULT_V4D_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/configs/"
    / "CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V4D_D28.json"
)
V4A_MODEL_SPEC_VERSION = "CODEX-E17.2-BATCHED-ROUTING-V4A-D28"
V4B_MODEL_SPEC_VERSION = "CODEX-E17.2-CLUSTERED-ROUTING-V4B-D28"
V4C_MODEL_SPEC_VERSION = "CODEX-E17.2-CAPACITY-AWARE-BATCHED-ROUTING-V4C-D28"
V4D_MODEL_SPEC_VERSION = "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28"
_VARIANTS = {
    "CODEX_E17_2_BATCHED_ROUTING_V4A_D28": V4A_MODEL_SPEC_VERSION,
    "CODEX_E17_2_CLUSTERED_ROUTING_V4B_D28": V4B_MODEL_SPEC_VERSION,
    "CODEX_E17_2_CAPACITY_AWARE_BATCHED_ROUTING_V4C_D28": (
        V4C_MODEL_SPEC_VERSION
    ),
    "CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V4D_D28": (
        V4D_MODEL_SPEC_VERSION
    ),
}


def load_v4_config(path: Path | str | None = None) -> dict[str, Any]:
    """Merge and validate a causally bounded V4 ablation config."""

    config_path = Path(path) if path is not None else DEFAULT_V4A_CONFIG_PATH
    overlay = json.loads(config_path.read_text(encoding="utf-8"))
    candidate_id = str(overlay.get("candidate_id", ""))
    if candidate_id not in _VARIANTS:
        raise ValueError(f"unexpected candidate_id: {candidate_id!r}")
    expected_version = _VARIANTS[candidate_id]
    if overlay.get("model_spec_version") != expected_version:
        raise ValueError("model_spec_version does not match candidate_id")
    if int(overlay.get("activation_day", -1)) != 28:
        raise ValueError("V4 must preserve the D28 handoff")
    if int(overlay.get("liquidation_day", -1)) != 29:
        raise ValueError("V4 must preserve the D29 liquidation window")
    if overlay.get("defer_d28_drop_to_eod") is not True:
        raise ValueError("V4 requires the preregistered D28 EOD batching")
    if overlay.get("terminal_harvest_before_drop") is not True:
        raise ValueError("V4 requires terminal harvest-before-drop routing")
    if candidate_id.endswith("V4A_D28") and overlay.get(
        "cluster_affinity_enabled"
    ):
        raise ValueError("V4A is the batching-only ablation")
    if candidate_id.endswith("V4B_D28") and not overlay.get(
        "cluster_affinity_enabled"
    ):
        raise ValueError("V4B requires quadrant affinity")
    if candidate_id.endswith(("V4C_D28", "V4D_D28")):
        if not overlay.get("capacity_aware_flush_enabled"):
            raise ValueError("V4C requires capacity-aware flush")
        trigger = float(overlay.get("capacity_flush_trigger_ratio", 0.0))
        target = float(overlay.get("capacity_flush_target_ratio", 0.0))
        if not 0 < target < trigger < 1:
            raise ValueError("V4C requires 0 < target < trigger < 1")
    if candidate_id.endswith("V4D_D28") and overlay.get(
        "release_wheat_carriers_after_feed_complete"
    ) is not True:
        raise ValueError("V4D requires post-feed Wheat carrier release")
    if int(overlay.get("cluster_switch_penalty", -1)) < 0:
        raise ValueError("cluster_switch_penalty must be non-negative")

    config = load_v3_config()
    config.update(overlay)
    return config


def _cluster(position: tuple[int, int], board_size: int) -> str:
    split = board_size // 2
    x, y = position
    row = "N" if y < split else "S"
    col = "W" if x < split else "E"
    return f"{row}{col}"


class CodexE17BatchedClusterRoutingV4(CodexE17ReactiveServiceRoutingV3):
    """Batch carried output until EOD/deadline and optionally stay local."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
    ) -> None:
        super().__init__(run_context=run_context)
        self.config = load_v4_config(config_path)
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = str(self.config["model_spec_version"])
        self.deferred_drop_opportunities = 0
        self.batched_harvest_services = 0
        self.deadline_drop_assignments = 0
        self.cluster_initial_assignments = 0
        self.cluster_sticky_assignments = 0
        self.cluster_switches = 0
        self.max_carried_sellable_units = 0
        self.capacity_flush_trigger_events = 0
        self.capacity_flush_active_batches = 0
        self.post_feed_wheat_carrier_releases = 0
        self._worker_cluster: dict[int, str] = {}
        self._affinity_day: int | None = None
        self._capacity_flush_latched = False

    def _sellable_units(self, inventory: dict[str, Any]) -> int:
        sellable = set(self.config["sellable_products"])
        return sum(
            max(0, int(quantity or 0))
            for item, quantity in inventory.items()
            if item in sellable
        )

    def _terminal_drop_tasks(
        self,
        *,
        inventories: list[dict[str, Any]],
        positions: list[tuple[int, int]],
        board_size: int,
        day: int,
    ) -> list[CoreTask]:
        carried = [self._sellable_units(inventory) for inventory in inventories]
        self.max_carried_sellable_units = max(
            [self.max_carried_sellable_units, *carried]
        )
        if day < int(self.config["liquidation_day"]):
            self.deferred_drop_opportunities += sum(value > 0 for value in carried)
            if bool(self.config.get("capacity_aware_flush_enabled", False)):
                feed_complete = not any(
                    not bool(tile.get("fed_today", False))
                    for _position, tile in _animal_tiles(self._routing_farm)
                )
                release_wheat = bool(
                    self.config.get(
                        "release_wheat_carriers_after_feed_complete", False
                    )
                    and feed_complete
                )
                droppable = [
                    value
                    if release_wheat
                    or int(inventory.get("WHEAT", 0) or 0) == 0
                    else 0
                    for value, inventory in zip(carried, inventories, strict=True)
                ]
                pressure = sum(
                    int(value or 0)
                    for value in (self._routing_private.get("shed", {}) or {}).values()
                ) + sum(droppable)
                trigger = int(
                    self._routing_shed_capacity
                    * float(self.config["capacity_flush_trigger_ratio"])
                )
                if not self._capacity_flush_latched and pressure >= trigger:
                    self._capacity_flush_latched = True
                    self.capacity_flush_trigger_events += 1
                if self._capacity_flush_latched and sum(droppable) > 0:
                    accesses = _shed_access(board_size)
                    tasks: list[CoreTask] = []
                    for worker_id, quantity in enumerate(droppable):
                        if quantity <= 0:
                            continue
                        if release_wheat and int(
                            inventories[worker_id].get("WHEAT", 0) or 0
                        ) > 0:
                            self.post_feed_wheat_carrier_releases += 1
                        target = min(
                            accesses,
                            key=lambda value: (
                                _distance(positions[worker_id], value),
                                value,
                            ),
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
                if sum(droppable) == 0:
                    self._capacity_flush_latched = False
            return []
        return super()._terminal_drop_tasks(
            inventories=inventories,
            positions=positions,
            board_size=board_size,
            day=day,
        )

    def _market_coordination_active(
        self,
        *,
        snapshot: Any,
        action: dict[str, Any],
    ) -> bool:
        if super()._market_coordination_active(snapshot=snapshot, action=action):
            return True
        active = bool(
            self.config.get("capacity_aware_flush_enabled", False)
            and snapshot.clock.day == int(self.config["activation_day"])
            and self._capacity_flush_latched
        )
        self.capacity_flush_active_batches += int(active)
        return active

    def _desired_sale_quantities(
        self,
        *,
        snapshot: Any,
        provider_sell: Counter[str],
        expected_available: Counter[str],
    ) -> Counter[str]:
        if snapshot.clock.day >= int(self.config["liquidation_day"]):
            return super()._desired_sale_quantities(
                snapshot=snapshot,
                provider_sell=provider_sell,
                expected_available=expected_available,
            )
        sellable = set(self.config["sellable_products"])
        shed = Counter(snapshot.private.get("shed", {}) or {})
        fixed_units = sum(
            int(quantity or 0)
            for item, quantity in shed.items()
            if item not in sellable
        )
        target_total = int(
            self._routing_shed_capacity
            * float(self.config["capacity_flush_target_ratio"])
        )
        sellable_target = max(0, target_total - fixed_units)
        required = max(0, sum(expected_available.values()) - sellable_target)
        desired = Counter({item: int(provider_sell[item]) for item in sellable})
        provider_effective = sum(
            min(int(provider_sell[item]), int(expected_available[item]))
            for item in sellable
        )
        remaining = max(0, required - provider_effective)
        prices = snapshot.market.get("prices", {}) or {}
        for item in sorted(
            sellable,
            key=lambda value: (float(prices.get(value, 0.0) or 0.0), value),
            reverse=True,
        ):
            already = min(int(desired[item]), int(expected_available[item]))
            available = max(0, int(expected_available[item]) - already)
            amount = min(available, remaining)
            if amount > 0:
                desired[item] = max(int(desired[item]), already + amount)
                remaining -= amount
            if remaining <= 0:
                break
        return desired

    def _harvest_value_score(
        self,
        task: CoreTask,
        required_actions: int,
    ) -> int:
        x, y = task.target
        tile = self._routing_farm["tiles"][y][x]
        item = str(tile.get("crop", ""))
        if tile.get("animal"):
            item = _ANIMAL_PRODUCTS[str(tile["animal"])]
        gross = float(self._routing_prices.get(item, 0.0) or 0.0) * int(
            tile.get("yield_units", 0) or 0
        )
        return -int(1000 * gross / max(1, required_actions))

    def _record_cluster_assignment(
        self,
        worker_id: int,
        task: CoreTask,
        previous_identity: tuple[str, tuple[int, int], tuple[Any, ...]] | None,
    ) -> None:
        if task.kind in {"DROP_INVENTORY", "PICKUP_WHEAT"}:
            return
        if previous_identity == task.identity:
            return
        target_cluster = _cluster(task.target, self._routing_board_size)
        prior = self._worker_cluster.get(worker_id)
        if prior is None:
            self.cluster_initial_assignments += 1
        elif prior == target_cluster:
            self.cluster_sticky_assignments += 1
        else:
            self.cluster_switches += 1
        self._worker_cluster[worker_id] = target_cluster

    def _assign(
        self,
        tasks: list[CoreTask],
        positions: list[tuple[int, int]],
        private: dict[str, Any],
    ) -> dict[int, CoreTask]:
        if self._routing_clock is None:
            return super()._assign(tasks, positions, private)
        day = int(self._routing_clock.day)
        if self._affinity_day != day:
            self._worker_cluster = {}
            self._affinity_day = day

        previous = dict(self.last_assignments)
        if day < int(self.config["liquidation_day"]):
            assignments = super()._assign(tasks, positions, private)
            for worker_id, task in assignments.items():
                self._record_cluster_assignment(
                    worker_id, task, previous.get(worker_id)
                )
            return assignments

        inventories = _inventories(private, len(positions))
        accesses = _shed_access(self._routing_board_size)
        remaining_actions = max(
            0,
            int(self.config["episode_steps"]) - 1 - self._routing_clock.step,
        )
        available_workers = set(range(len(positions)))
        remaining_tasks = list(tasks)
        reserved_targets: set[tuple[Any, ...]] = set()
        assignments: dict[int, CoreTask] = {}
        affinity_enabled = bool(self.config["cluster_affinity_enabled"])
        switch_penalty = int(self.config["cluster_switch_penalty"])

        while available_workers and remaining_tasks:
            candidates: list[tuple[int, int, int, int, int]] = []
            for task_index, task in enumerate(remaining_tasks):
                target_key = (
                    (task.kind, task.target, task.allowed_workers)
                    if task.kind == "DROP_INVENTORY"
                    else (task.kind, task.target)
                )
                if target_key in reserved_targets:
                    continue
                eligible = available_workers
                if task.allowed_workers is not None:
                    eligible = available_workers.intersection(task.allowed_workers)
                for worker_id in eligible:
                    distance = _distance(positions[worker_id], task.target)
                    required = 1
                    phase = 1 if task.kind == "DROP_INVENTORY" else 0
                    value_score = 0
                    if task.kind == "HARVEST":
                        required = (
                            distance
                            + min(
                                _distance(task.target, access)
                                for access in accesses
                            )
                            + 2
                        )
                        if required > remaining_actions:
                            continue
                        value_score = self._harvest_value_score(task, required)
                    target_cluster = _cluster(task.target, self._routing_board_size)
                    cluster_cost = 0
                    if (
                        affinity_enabled
                        and task.kind != "DROP_INVENTORY"
                        and self._worker_cluster.get(worker_id) not in {
                            None,
                            target_cluster,
                        }
                    ):
                        cluster_cost = switch_penalty
                    continuity = (
                        -3 if previous.get(worker_id) == task.identity else 0
                    )
                    candidates.append(
                        (
                            phase,
                            value_score,
                            distance + cluster_cost + continuity,
                            worker_id,
                            task_index,
                        )
                    )
            if not candidates:
                break
            _phase, _value, _route, worker_id, task_index = min(candidates)
            task = remaining_tasks.pop(task_index)
            assignments[worker_id] = task
            available_workers.remove(worker_id)
            reserved_targets.add(
                (task.kind, task.target, task.allowed_workers)
                if task.kind == "DROP_INVENTORY"
                else (task.kind, task.target)
            )

        for worker_id, task in assignments.items():
            carried = self._sellable_units(inventories[worker_id])
            if (
                task.kind == "HARVEST"
                and positions[worker_id] == task.target
                and carried > 0
            ):
                self.batched_harvest_services += 1
            if task.kind == "DROP_INVENTORY":
                self.deadline_drop_assignments += 1
            self._record_cluster_assignment(worker_id, task, previous.get(worker_id))
        return assignments

    def telemetry_snapshot(self) -> dict[str, Any]:
        telemetry = super().telemetry_snapshot()
        cluster_decisions = self.cluster_sticky_assignments + self.cluster_switches
        return {
            **telemetry,
            "agent_version": self.model_spec_version,
            "deferred_drop_opportunities": self.deferred_drop_opportunities,
            "batched_harvest_services": self.batched_harvest_services,
            "deadline_drop_assignments": self.deadline_drop_assignments,
            "cluster_initial_assignments": self.cluster_initial_assignments,
            "cluster_sticky_assignments": self.cluster_sticky_assignments,
            "cluster_switches": self.cluster_switches,
            "cluster_switch_rate": (
                self.cluster_switches / cluster_decisions
                if cluster_decisions
                else 0.0
            ),
            "max_carried_sellable_units": self.max_carried_sellable_units,
            "capacity_flush_trigger_events": self.capacity_flush_trigger_events,
            "capacity_flush_active_batches": self.capacity_flush_active_batches,
            "post_feed_wheat_carrier_releases": (
                self.post_feed_wheat_carrier_releases
            ),
        }


def create_codex_e17_batched_cluster_routing_v4(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    """Create a fail-closed V4A or V4B routing ablation."""

    instance = CodexE17BatchedClusterRoutingV4(
        run_context=run_context,
        config_path=config_path,
    )

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_e17_batched_cluster_routing_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e17_batched_cluster_routing_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e17_batched_cluster_routing_instance = instance
    policy.codex_e17_batched_cluster_routing_last_error = None
    policy.__name__ = "codex_e17_2_batched_cluster_routing_v4_policy"
    return policy


__all__ = [
    "DEFAULT_V4A_CONFIG_PATH",
    "DEFAULT_V4B_CONFIG_PATH",
    "DEFAULT_V4C_CONFIG_PATH",
    "DEFAULT_V4D_CONFIG_PATH",
    "V4A_MODEL_SPEC_VERSION",
    "V4B_MODEL_SPEC_VERSION",
    "V4C_MODEL_SPEC_VERSION",
    "V4D_MODEL_SPEC_VERSION",
    "CodexE17BatchedClusterRoutingV4",
    "create_codex_e17_batched_cluster_routing_v4",
    "load_v4_config",
]
