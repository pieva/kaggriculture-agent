"""E17.2 D28 handoff with state-driven service and terminal cash-out.

The V3 keeps the E17.1 provider's acquisition and market schedule until the
terminal liquidation window.  From day 28 it owns all unit routing, prepares
the last biological production cycle, and on day 29 sells products that are
already in the shed or are deposited by a unit earlier in the same batch.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import (
    CodexObservationAdapter,
    stable_payload_hash,
)
from agricola.core.state import CROPS
from agricola.strategy.codex.codex_e17_reactive_service_routing_core import (
    CodexE17ReactiveServiceRoutingCore,
    CoreTask,
    _animal_tiles,
    _crop_tiles,
    _distance,
    _inventories,
    _positions,
    _shed_access,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_V3_CONFIG_PATH = (
    REPO_ROOT
    / "experiments/e17/configs/codex/"
    / "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V3_D28.json"
)
V3_MODEL_SPEC_VERSION = "CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
_ANIMALS = {"COW", "SHEEP", "GOOSE"}
_ANIMAL_PRODUCTS = {"COW": "MILK", "SHEEP": "WOOL", "GOOSE": "EGG"}
_MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


def load_v3_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load the causally bounded D28 service/liquidation configuration."""

    config_path = Path(path) if path is not None else DEFAULT_V3_CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V3_D28",
        "model_spec_version": V3_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E17.1-TRUE-REACTIVE-V2",
        "causal_family": "REACTIVE_SERVICE_ROUTING_AND_TERMINAL_LIQUIDATION",
        "activation_day": 28,
        "liquidation_day": 29,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    if int(config.get("turns_per_day", 0)) <= 0:
        raise ValueError("turns_per_day must be positive")
    if int(config.get("episode_steps", 0)) <= 0:
        raise ValueError("episode_steps must be positive")
    if not config.get("sellable_products") or not config.get("task_priority"):
        raise ValueError("sellable products and task priorities are required")
    return deepcopy(config)


class CodexE17ReactiveServiceRoutingV3(CodexE17ReactiveServiceRoutingCore):
    """Own D28+ unit work and complete same-batch terminal liquidation."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
    ) -> None:
        # Initialize the stable provider and telemetry without changing the
        # frozen V2 loader, then bind the independently validated V3 config.
        super().__init__(run_context=run_context)
        self.config = load_v3_config(config_path)
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = V3_MODEL_SPEC_VERSION
        self.coordinated_market_batches = 0
        self.coordinated_sell_orders = 0
        self.coordinated_sell_units_requested = 0
        self.non_sell_preservation_failures = 0
        self.market_execution_outcomes: Counter[str] = Counter()
        self.market_ledger_records: list[dict[str, Any]] = []
        self._pending_market_ledger: list[int] = []
        self._routing_clock: Any = None
        self._routing_board_size = 10
        self._routing_farm: dict[str, Any] = {}
        self._routing_prices: dict[str, float] = {}
        self._routing_private: dict[str, Any] = {}
        self._routing_shed_capacity = 100

    def _settle_pending(self, snapshot: Any) -> None:
        pending = list(self._pending_ledger)
        super()._settle_pending(snapshot)
        for index in pending:
            record = self.ledger_records[index]
            requested = record.get("requested", [])
            if (
                record.get("hour") == int(self.config["turns_per_day"]) - 1
                and requested
                and requested[0] in _MOVES
                and record.get("outcome") == "NOT_EXECUTED"
            ):
                # EOD resets every worker to the shed before the next callback;
                # the post-state cannot distinguish an executed move from a no-op.
                record["outcome"] = "UNKNOWN"
                record["outcome_note"] = "EOD_POSITION_RESET_OBSCURES_MOVE"
                self.execution_outcomes["NOT_EXECUTED"] -= 1
                self.execution_outcomes["UNKNOWN"] += 1

    def _structure_tasks(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        inventories: list[dict[str, Any]],
    ) -> list[CoreTask]:
        del farm, private, inventories
        return []

    def _crop_setup_tasks(
        self,
        *,
        farm: dict[str, Any],
        private: dict[str, Any],
        day: int,
    ) -> list[CoreTask]:
        del farm, private, day
        return []

    def _service_tasks(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        inventories: list[dict[str, Any]],
        board_size: int,
        day: int,
    ) -> list[CoreTask]:
        tasks: list[CoreTask] = []
        final_day = int(self.config["episode_steps"]) // int(
            self.config["turns_per_day"]
        ) - 1
        terminal_day = day >= final_day

        for position, tile in _crop_tiles(farm):
            crop = str(tile.get("crop", ""))
            planted_day = int(tile.get("planted_day", day))
            mature = day - planted_day >= int(
                CROPS.get(crop, {}).get("first_yield_day", 10**6)
            )
            if mature and int(tile.get("yield_units", 0) or 0) > 0:
                tasks.append(self._task("HARVEST", position, ("HARVEST",)))
            if terminal_day or bool(tile.get("watered_today", False)):
                continue
            kind = (
                "CRITICAL_WATER"
                if int(tile.get("consecutive_unwatered", 0) or 0)
                >= int(self.config["critical_unwatered_threshold"])
                else "WATER"
            )
            tasks.append(self._task(kind, position, ("WATER",)))

        unfed: list[tuple[int, int]] = []
        carriers = tuple(
            worker_id
            for worker_id, inventory in enumerate(inventories)
            if int(inventory.get("WHEAT", 0) or 0) > 0
        )
        for position, tile in _animal_tiles(farm):
            if int(tile.get("yield_units", 0) or 0) > 0:
                tasks.append(self._task("HARVEST", position, ("HARVEST",)))
            if terminal_day:
                continue
            if not bool(tile.get("fed_today", False)):
                unfed.append(position)
                kind = (
                    "CRITICAL_FEED"
                    if int(tile.get("consecutive_unfed", 0) or 0)
                    >= int(self.config["critical_unfed_threshold"])
                    else "FEED"
                )
                if carriers:
                    tasks.append(
                        self._task(
                            kind,
                            position,
                            ("FEED",),
                            allowed_workers=carriers,
                            resource="WHEAT",
                        )
                    )
            if bool(tile.get("fertilizer_available", False)):
                tasks.append(
                    self._task(
                        "COLLECT_FERTILIZER",
                        position,
                        ("COLLECT_FERTILIZER",),
                    )
                )

        if terminal_day:
            return tasks

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
        if day < int(self.config["activation_day"]):
            return []
        sellable = set(self.config["sellable_products"])
        if day < int(self.config["liquidation_day"]):
            sellable.discard("WHEAT")
        accesses = _shed_access(board_size)
        tasks: list[CoreTask] = []
        for worker_id, inventory in enumerate(inventories):
            if (
                day < int(self.config["liquidation_day"])
                and int(inventory.get("WHEAT", 0) or 0) > 0
            ):
                continue
            if not any(
                item in sellable and int(quantity or 0) > 0
                for item, quantity in inventory.items()
            ):
                continue
            target = min(
                accesses,
                key=lambda value: (
                    abs(positions[worker_id][0] - value[0])
                    + abs(positions[worker_id][1] - value[1]),
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

    def _assign(
        self,
        tasks: list[CoreTask],
        positions: list[tuple[int, int]],
        private: dict[str, Any],
    ) -> dict[int, CoreTask]:
        if self._routing_clock is None or self._routing_clock.day < int(
            self.config["liquidation_day"]
        ):
            assignments = super()._assign(tasks, positions, private)
            for task in tasks:
                if task.kind != "DROP_INVENTORY" or not task.allowed_workers:
                    continue
                worker_id = task.allowed_workers[0]
                assignments[worker_id] = task
            return assignments

        assignments: dict[int, CoreTask] = {}
        available_workers = set(range(len(positions)))
        reserved_targets: set[tuple[Any, ...]] = set()
        remaining_tasks = list(tasks)
        remaining_actions = max(
            0,
            int(self.config["episode_steps"]) - 1 - self._routing_clock.step,
        )
        accesses = _shed_access(self._routing_board_size)
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
                    required = 1
                    if task.kind == "HARVEST":
                        return_distance = min(
                            _distance(task.target, access) for access in accesses
                        )
                        required = (
                            _distance(positions[worker_id], task.target)
                            + return_distance
                            + 2
                        )
                        if required > remaining_actions:
                            continue
                    value_score = 0
                    if task.kind == "HARVEST":
                        x, y = task.target
                        tile = self._routing_farm["tiles"][y][x]
                        item = str(tile.get("crop", ""))
                        if tile.get("animal"):
                            item = _ANIMAL_PRODUCTS[str(tile["animal"])]
                        gross = float(self._routing_prices.get(item, 0.0) or 0.0) * int(
                            tile.get("yield_units", 0) or 0
                        )
                        value_score = -int(1000 * gross / max(1, required))
                    candidates.append(
                        (
                            task.priority,
                            value_score,
                            _distance(positions[worker_id], task.target)
                            - (
                                3
                                if self.last_assignments.get(worker_id)
                                == task.identity
                                else 0
                            ),
                            worker_id,
                            task_index,
                        )
                    )
            if not candidates:
                break
            _priority, _value_score, _distance_score, worker_id, task_index = min(
                candidates
            )
            task = remaining_tasks.pop(task_index)
            assignments[worker_id] = task
            available_workers.remove(worker_id)
            reserved_targets.add(
                (task.kind, task.target, task.allowed_workers)
                if task.kind == "DROP_INVENTORY"
                else (task.kind, task.target)
            )
        return assignments

    def _predicted_drop(
        self,
        *,
        action: dict[str, Any],
        snapshot: Any,
    ) -> Counter[str]:
        positions = _positions(snapshot.farm)
        inventories = _inventories(snapshot.private, len(positions))
        unit_actions = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
        accesses = set(_shed_access(int(snapshot.configuration_snapshot["boardSize"])))
        sellable = set(self.config["sellable_products"])
        shed = Counter(snapshot.private.get("shed", {}) or {})
        room = max(
            0,
            int(snapshot.configuration_snapshot["shedCapacity"])
            - sum(int(value or 0) for value in shed.values()),
        )
        predicted: Counter[str] = Counter()
        for worker_id, unit_action in enumerate(unit_actions):
            if (
                worker_id >= len(positions)
                or not isinstance(unit_action, list)
                or not unit_action
                or unit_action[0] != "DROP"
                or positions[worker_id] not in accesses
            ):
                continue
            for item, quantity in inventories[worker_id].items():
                amount = min(max(0, int(quantity or 0)), room)
                if amount <= 0:
                    continue
                room -= amount
                if item in sellable:
                    predicted[item] += amount
        return predicted

    def _settle_market_pending(self, snapshot: Any) -> None:
        post_shed = Counter(snapshot.private.get("shed", {}) or {})
        for index in self._pending_market_ledger:
            record = self.market_ledger_records[index]
            requested = Counter(record["requested_sell_quantities"])
            expected = Counter(record["expected_available_after_drop"])
            observed_sold: dict[str, int] = {}
            complete = True
            any_observed = False
            for item, quantity in requested.items():
                target = min(int(quantity), int(expected[item]))
                sold = max(0, int(expected[item]) - int(post_shed[item]))
                observed_sold[item] = sold
                any_observed = any_observed or sold > 0
                complete = complete and sold >= target
            outcome = "EXECUTED" if complete else "UNKNOWN" if any_observed else "NOT_EXECUTED"
            record["outcome"] = outcome
            record["observed_sold_units"] = observed_sold
            record["post_state_id"] = snapshot.state_id
            record["post_snapshot_fingerprint"] = snapshot.snapshot_fingerprint
            self.market_execution_outcomes[outcome] += 1
        self._pending_market_ledger = []

    def _market_coordination_active(
        self,
        *,
        snapshot: Any,
        action: dict[str, Any],
    ) -> bool:
        del action
        return snapshot.clock.day >= int(self.config["liquidation_day"])

    def _desired_sale_quantities(
        self,
        *,
        snapshot: Any,
        provider_sell: Counter[str],
        expected_available: Counter[str],
    ) -> Counter[str]:
        del snapshot
        return Counter(
            {
                item: max(int(provider_sell[item]), int(expected_available[item]))
                for item in self.config["sellable_products"]
            }
        )

    def _coordinate_terminal_market(
        self,
        action: dict[str, Any],
        *,
        snapshot: Any,
    ) -> dict[str, Any]:
        if not self._market_coordination_active(snapshot=snapshot, action=action):
            return action

        original = deepcopy(action.get("market", []) or [])
        sellable_order = list(self.config["sellable_products"])
        sellable = set(sellable_order)
        provider_sell: Counter[str] = Counter()
        for order in original:
            if (
                isinstance(order, list)
                and len(order) >= 3
                and order[0] == "SELL"
                and order[1] in sellable
            ):
                provider_sell[str(order[1])] += max(0, int(order[2]))

        predicted_drop = self._predicted_drop(action=action, snapshot=snapshot)
        shed = Counter(snapshot.private.get("shed", {}) or {})
        expected_available = Counter(
            {
                item: int(shed[item]) + int(predicted_drop[item])
                for item in sellable_order
            }
        )
        desired = self._desired_sale_quantities(
            snapshot=snapshot,
            provider_sell=provider_sell,
            expected_available=expected_available,
        )

        rebuilt: list[Any] = []
        emitted_sell: set[str] = set()
        for raw_order in original:
            if not (
                isinstance(raw_order, list)
                and len(raw_order) >= 3
                and raw_order[0] == "SELL"
                and raw_order[1] in sellable
            ):
                rebuilt.append(deepcopy(raw_order))
                continue
            item = str(raw_order[1])
            if item in emitted_sell or desired[item] <= 0:
                continue
            rebuilt.append(["SELL", item, int(desired[item]), *raw_order[3:]])
            emitted_sell.add(item)

        prices = snapshot.market.get("prices", {}) or {}
        additions = sorted(
            (
                (float(prices.get(item, 0.0) or 0.0), item)
                for item in sellable_order
                if desired[item] > 0 and item not in emitted_sell
            ),
            reverse=True,
        )
        max_orders = int(snapshot.configuration_snapshot["maxMarketOrdersPerTurn"])
        for _price, item in additions:
            if len(rebuilt) >= max_orders:
                break
            rebuilt.append(["SELL", item, int(desired[item])])
            emitted_sell.add(item)

        non_sell_before = [
            order
            for order in original
            if not (isinstance(order, list) and order and order[0] == "SELL")
        ]
        non_sell_after = [
            order
            for order in rebuilt
            if not (isinstance(order, list) and order and order[0] == "SELL")
        ]
        if non_sell_after != non_sell_before:
            self.non_sell_preservation_failures += 1

        action["market"] = rebuilt
        if rebuilt == original:
            return action

        emitted_quantities: Counter[str] = Counter()
        for order in rebuilt:
            if (
                isinstance(order, list)
                and len(order) >= 3
                and order[0] == "SELL"
                and order[1] in sellable
            ):
                emitted_quantities[str(order[1])] += max(0, int(order[2]))
        incremental = Counter(
            {
                item: max(0, emitted_quantities[item] - provider_sell[item])
                for item in sellable_order
                if emitted_quantities[item] > provider_sell[item]
            }
        )
        self.coordinated_market_batches += 1
        self.coordinated_sell_orders += sum(1 for value in incremental.values() if value > 0)
        self.coordinated_sell_units_requested += sum(incremental.values())
        self.market_ledger_records.append(
            {
                "step": snapshot.clock.step,
                "day": snapshot.clock.day,
                "hour": snapshot.clock.hour,
                "state_id": snapshot.state_id,
                "snapshot_fingerprint": snapshot.snapshot_fingerprint,
                "provider_market_sha256": stable_payload_hash(original),
                "emitted_market_sha256": stable_payload_hash(rebuilt),
                "provider_market": original,
                "emitted_market": deepcopy(rebuilt),
                "shed_before": dict(shed),
                "predicted_drop": dict(predicted_drop),
                "expected_available_after_drop": dict(expected_available),
                "requested_sell_quantities": dict(emitted_quantities),
                "incremental_sell_quantities": dict(incremental),
                "outcome": "PENDING_NEXT_OBSERVATION",
            }
        )
        self._pending_market_ledger.append(len(self.market_ledger_records) - 1)
        return action

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        snapshot = CodexObservationAdapter.parse(
            observation,
            configuration,
            fallback_turns_per_day=int(self.config["turns_per_day"]),
            fallback_episode_steps=int(self.config["episode_steps"]),
        )
        self._routing_clock = snapshot.clock
        self._routing_board_size = int(snapshot.configuration_snapshot["boardSize"])
        self._routing_farm = snapshot.farm
        self._routing_prices = snapshot.market.get("prices", {}) or {}
        self._routing_private = snapshot.private
        self._routing_shed_capacity = int(
            snapshot.configuration_snapshot["shedCapacity"]
        )
        self._settle_market_pending(snapshot)
        action = super().__call__(observation, configuration)
        return self._coordinate_terminal_market(action, snapshot=snapshot)

    def telemetry_snapshot(self) -> dict[str, Any]:
        for index in self._pending_market_ledger:
            self.market_ledger_records[index]["outcome"] = "UNKNOWN"
            self.market_execution_outcomes["UNKNOWN"] += 1
        self._pending_market_ledger = []
        telemetry = super().telemetry_snapshot()
        return {
            **telemetry,
            "agent_version": self.model_spec_version,
            "coordinated_market_batches": self.coordinated_market_batches,
            "coordinated_sell_orders": self.coordinated_sell_orders,
            "coordinated_sell_units_requested": self.coordinated_sell_units_requested,
            "non_sell_preservation_failures": self.non_sell_preservation_failures,
            "market_execution_outcomes": dict(self.market_execution_outcomes),
            "market_ledger_record_count": len(self.market_ledger_records),
            "market_ledger_records": deepcopy(self.market_ledger_records),
        }


def create_codex_e17_reactive_service_routing_v3(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    """Create the fail-closed D28 service/routing/liquidation policy."""

    instance = CodexE17ReactiveServiceRoutingV3(
        run_context=run_context,
        config_path=config_path,
    )

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_e17_service_routing_v3_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e17_service_routing_v3_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e17_service_routing_v3_instance = instance
    policy.codex_e17_service_routing_v3_last_error = None
    policy.__name__ = "codex_e17_2_service_routing_core_v3_d28_policy"
    return policy


__all__ = [
    "DEFAULT_V3_CONFIG_PATH",
    "V3_MODEL_SPEC_VERSION",
    "CodexE17ReactiveServiceRoutingV3",
    "create_codex_e17_reactive_service_routing_v3",
    "load_v3_config",
]
