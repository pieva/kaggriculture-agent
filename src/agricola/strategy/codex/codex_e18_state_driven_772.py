"""E18.4 native state-driven 7-7-2 scheduler over the E18.2 bootstrap.

E18.2 remains authoritative through day 10.  From day 11 every unit command
is rebuilt from the current observation, while provider land, hire and input
orders are preserved.  Sales are reconstructed from the observed shed (plus
same-batch terminal drops), closing the production-to-cash loop that failed in
the first early-handoff prototype.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.state import CROPS
from agricola.strategy.codex.codex_e17_reactive_service_routing_core import (
    CodexE17ReactiveServiceRoutingCore,
    CoreTask,
    _animal_tiles,
    _inventories,
    _positions,
    _shed_access,
)
from agricola.strategy.codex.codex_e17_reactive_service_routing_v3 import (
    _SAFE_PASS,
    CodexE17ReactiveServiceRoutingV3,
)
from agricola.strategy.codex.codex_e18_capacity_governed_v4d import (
    create_codex_e18_capacity_governed_v4d,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_STATE_DRIVEN_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/CODEX_E18_4_STATE_DRIVEN_772_V1.json"
)
E18_STATE_DRIVEN_MODEL_SPEC_VERSION = "CODEX-E18.4-STATE-DRIVEN-772-V1"
_PASTURE_ANIMALS = frozenset({"COW", "SHEEP"})


def load_e18_state_driven_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    """Load and validate the frozen E18.4 causal envelope."""

    config_path = Path(path) if path is not None else DEFAULT_E18_STATE_DRIVEN_CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_4_STATE_DRIVEN_772_V1",
        "model_spec_version": E18_STATE_DRIVEN_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1",
        "causal_family": (
            "STATE_DRIVEN_UNIT_SCHEDULER_WITH_OBSERVED_MARKET_LEDGER"
        ),
        "public_features_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "activation_day": 11,
        "liquidation_day": 29,
        "pasture_livestock_cap": 16,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    targets = {tuple(value) for value in config.get("pasture_targets", [])}
    q0 = sum(x < 5 and y < 5 for x, y in targets)
    q1 = sum(x >= 5 and y < 5 for x, y in targets)
    q2 = sum(x < 5 and y >= 5 for x, y in targets)
    if len(targets) != 16 or (q0, q1, q2) != (7, 7, 2):
        raise ValueError("E18.4 pasture target must be exactly 7-7-2")
    if {tuple(value) for value in config.get("coop_targets", [])} != {(4, 1)}:
        raise ValueError("E18.4 requires the frozen NW coop target")
    if not config.get("sellable_products") or not config.get("task_priority"):
        raise ValueError("sellable products and task priorities are required")
    return deepcopy(config)


def _pasture_livestock_resources(snapshot: Any) -> int:
    placed = sum(
        str(tile.get("animal", "")) in _PASTURE_ANIMALS
        for _position, tile in _animal_tiles(snapshot.farm)
    )
    shed = snapshot.private.get("shed", {}) or {}
    stored = sum(int(shed.get(animal, 0) or 0) for animal in _PASTURE_ANIMALS)
    carried = sum(
        int(inventory.get(animal, 0) or 0)
        for inventory in (snapshot.private.get("inventories", []) or [])
        if isinstance(inventory, dict)
        for animal in _PASTURE_ANIMALS
    )
    return placed + stored + carried


class CodexE18StateDriven772Agent(CodexE17ReactiveServiceRoutingV3):
    """Replan the complete 7-7-2 farm from observation after a stable opening."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context)
        self.config = load_e18_state_driven_config(config_path)
        self.run_context = deepcopy(run_context or {})
        self.base_policy = base_policy or create_codex_e18_capacity_governed_v4d(
            run_context=self.run_context
        )
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = E18_STATE_DRIVEN_MODEL_SPEC_VERSION
        self.last_scheduler_day: int | None = None
        self.market_cap_clamped_units: Counter[str] = Counter()
        self.market_reordered_batches = 0
        self.reclaimed_seed_requested = False
        self.observed_sale_units = 0
        self.sale_deferred_since: dict[str, int] = {}
        self.sale_deferral_batches = 0
        self.daily_modes: list[dict[str, Any]] = []

    def _structure_tasks(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        inventories: list[dict[str, Any]],
    ) -> list[CoreTask]:
        return CodexE17ReactiveServiceRoutingCore._structure_tasks(
            self, farm, private, inventories
        )

    def _crop_setup_tasks(
        self,
        *,
        farm: dict[str, Any],
        private: dict[str, Any],
        day: int,
    ) -> list[CoreTask]:
        return CodexE17ReactiveServiceRoutingCore._crop_setup_tasks(
            self, farm=farm, private=private, day=day
        )

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

        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                    continue
                crop = str(tile.get("crop", ""))
                crop_data = CROPS[crop]
                age = day - int(tile.get("planted_day", day))
                units = int(tile.get("yield_units", 0) or 0)
                if crop_data["ongoing"]:
                    harvest_ready = units >= int(crop_data["max_yield"])
                else:
                    harvest_ready = (
                        units >= int(crop_data["max_yield"])
                        or age >= int(crop_data["max_yield_day"])
                    )
                if units > 0 and (harvest_ready or day >= final_day):
                    tasks.append(self._task("HARVEST", (x, y), ("HARVEST",)))
                if day >= final_day or bool(tile.get("watered_today", False)):
                    continue
                kind = (
                    "CRITICAL_WATER"
                    if int(tile.get("consecutive_unwatered", 0) or 0)
                    >= int(self.config["critical_unwatered_threshold"])
                    else "WATER"
                )
                tasks.append(self._task(kind, (x, y), ("WATER",)))

        unfed: list[tuple[int, int]] = []
        carriers = tuple(
            worker_id
            for worker_id, inventory in enumerate(inventories)
            if int(inventory.get("WHEAT", 0) or 0) > 0
        )
        for position, tile in _animal_tiles(farm):
            if int(tile.get("yield_units", 0) or 0) >= 4 or (
                day >= final_day and int(tile.get("yield_units", 0) or 0) > 0
            ):
                tasks.append(self._task("HARVEST", position, ("HARVEST",)))
            if day >= final_day:
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
            elif not bool(tile.get("cared_today", False)):
                tasks.append(self._task("CARE", position, ("CARE",)))
            if bool(tile.get("fertilizer_available", False)):
                tasks.append(
                    self._task(
                        "COLLECT_FERTILIZER",
                        position,
                        ("COLLECT_FERTILIZER",),
                    )
                )

        if day >= final_day:
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
        # Inventories are deposited automatically at each EOD.  Sending units
        # back earlier only burns labor; explicit drops are required on D29 so
        # the final harvest can still be sold in the same batch.
        if day < int(self.config["liquidation_day"]):
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
        del action
        return snapshot.clock.day >= int(self.config["activation_day"])

    def _wheat_reserve(self, snapshot: Any) -> int:
        if snapshot.clock.day >= int(self.config["liquidation_day"]):
            return 0
        inventories = _inventories(snapshot.private, len(_positions(snapshot.farm)))
        carried = sum(int(value.get("WHEAT", 0) or 0) for value in inventories)
        animals = list(_animal_tiles(snapshot.farm))
        unfed = sum(
            not bool(tile.get("fed_today", False))
            for _position, tile in animals
        )
        return max(
            0,
            max(len(animals), unfed - carried)
            + int(self.config["wheat_safety_buffer"]),
        )

    def _desired_sale_quantities(
        self,
        *,
        snapshot: Any,
        provider_sell: Counter[str],
        expected_available: Counter[str],
    ) -> Counter[str]:
        del provider_sell
        available = Counter(
            {
                item: max(0, int(expected_available[item]))
                for item in self.config["sellable_products"]
            }
        )
        available["WHEAT"] = max(
            0,
            int(expected_available["WHEAT"]) - self._wheat_reserve(snapshot),
        )
        desired: Counter[str] = Counter()
        terminal = snapshot.clock.day >= int(self.config["liquidation_day"])
        shed_total = sum(
            int(value or 0)
            for value in (snapshot.private.get("shed", {}) or {}).values()
        )
        forced_capacity_release = shed_total >= int(
            int(snapshot.configuration_snapshot["shedCapacity"])
            * float(self.config["sale_release_shed_ratio"])
        )
        emergency = float(snapshot.farm.get("money", 0.0) or 0.0) < float(
            self.config["emergency_cash_floor"]
        )
        prices = snapshot.market.get("prices", {}) or {}
        for item, quantity in available.items():
            if quantity <= 0:
                self.sale_deferred_since.pop(item, None)
                continue
            started = self.sale_deferred_since.get(item)
            deferral_expired = (
                started is not None
                and snapshot.clock.step - started
                >= int(self.config["max_sale_deferral_steps"])
            )
            reference = float(self.config["reference_prices"][item])
            low_price = float(prices.get(item, 0.0) or 0.0) < (
                reference * float(self.config["low_output_price_ratio"])
            )
            if (
                low_price
                and not terminal
                and not forced_capacity_release
                and not emergency
                and not deferral_expired
            ):
                self.sale_deferred_since.setdefault(item, snapshot.clock.step)
                self.sale_deferral_batches += 1
                continue
            desired[item] = quantity
            self.sale_deferred_since.pop(item, None)
        return desired

    def _filter_market_acquisitions(
        self,
        action: dict[str, Any],
        *,
        snapshot: Any,
    ) -> None:
        remaining = max(
            0,
            int(self.config["pasture_livestock_cap"])
            - _pasture_livestock_resources(snapshot),
        )
        inventories = _inventories(snapshot.private, len(_positions(snapshot.farm)))
        wheat_stock = int(
            (snapshot.private.get("shed", {}) or {}).get("WHEAT", 0) or 0
        ) + sum(int(value.get("WHEAT", 0) or 0) for value in inventories)
        wheat_purchase_remaining = max(
            0,
            len(_animal_tiles(snapshot.farm))
            + int(self.config["wheat_safety_buffer"])
            - wheat_stock,
        )
        rebuilt: list[Any] = []
        for order in action.get("market", []) or []:
            if (
                isinstance(order, list)
                and len(order) >= 3
                and order[:2] == ["BUY_PRODUCT", "WHEAT"]
            ):
                admitted = min(max(0, int(order[2])), wheat_purchase_remaining)
                wheat_purchase_remaining -= admitted
                if admitted:
                    rebuilt.append([*order[:2], admitted, *order[3:]])
                continue
            if not (
                isinstance(order, list)
                and len(order) >= 3
                and order[0] == "BUY_ANIMAL"
                and str(order[1]) in _PASTURE_ANIMALS
            ):
                rebuilt.append(deepcopy(order))
                continue
            requested = max(0, int(order[2]))
            admitted = min(requested, remaining)
            remaining -= admitted
            if admitted:
                rebuilt.append([*order[:2], admitted, *order[3:]])
            if admitted < requested:
                self.market_cap_clamped_units[str(order[1])] += requested - admitted

        if (
            not self.reclaimed_seed_requested
            and snapshot.clock.day >= int(self.config["activation_day"])
            and len(rebuilt)
            < int(snapshot.configuration_snapshot["maxMarketOrdersPerTurn"])
        ):
            units = int(self.config["reclaimed_seed_units"])
            crop = str(self.config["reclaimed_seed_crop"])
            cost = units * float(CROPS[crop]["seed"])
            money = float(snapshot.farm.get("money", 0.0) or 0.0)
            if money - cost >= float(self.config["reclaimed_seed_cash_floor"]):
                rebuilt.append(["BUY_SEED", crop, units])
                self.reclaimed_seed_requested = True

        day = int(snapshot.clock.day)
        if int(self.config["activation_day"]) <= day <= int(
            self.config["plant_cutoff_day"]
        ):
            livestock = {
                *(tuple(value) for value in self.config["pasture_targets"]),
                *(tuple(value) for value in self.config["coop_targets"]),
            }
            open_crop_cells = sum(
                (x, y) not in livestock
                and tile != "LOCKED"
                and (
                    tile is None
                    or (isinstance(tile, dict) and tile.get("kind") == "WEED")
                )
                for y, row in enumerate(snapshot.farm.get("tiles", []) or [])
                for x, tile in enumerate(row)
            )
            seed_stock = sum(
                int(value or 0)
                for value in (snapshot.private.get("seeds", {}) or {}).values()
            )
            planned_seed_units = sum(
                max(0, int(order[2]))
                for order in rebuilt
                if isinstance(order, list)
                and len(order) >= 3
                and order[0] == "BUY_SEED"
            )
            shortage = max(
                0,
                min(open_crop_cells, int(self.config["seed_reorder_batch"]))
                - seed_stock
                - planned_seed_units,
            )
            if (
                shortage > 0
                and seed_stock < int(self.config["seed_inventory_floor"])
                and len(rebuilt)
                < int(snapshot.configuration_snapshot["maxMarketOrdersPerTurn"])
            ):
                crop = (
                    "MELON"
                    if day <= int(self.config["crop_cutoffs"]["MELON"])
                    else "STRAWBERRY"
                    if day <= int(self.config["crop_cutoffs"]["STRAWBERRY"])
                    else "TOMATO"
                    if day <= int(self.config["crop_cutoffs"]["TOMATO"])
                    else "WHEAT"
                )
                unit_cost = float(CROPS[crop]["seed"])
                money = float(snapshot.farm.get("money", 0.0) or 0.0)
                affordable = max(
                    0,
                    int(
                        (money - float(self.config["reclaimed_seed_cash_floor"]))
                        // unit_cost
                    ),
                )
                quantity = min(shortage, affordable)
                if quantity > 0:
                    rebuilt.append(["BUY_SEED", crop, quantity])
        action["market"] = rebuilt

    def _coordinate_terminal_market(
        self,
        action: dict[str, Any],
        *,
        snapshot: Any,
    ) -> dict[str, Any]:
        self._filter_market_acquisitions(action, snapshot=snapshot)
        coordinated = super()._coordinate_terminal_market(
            action, snapshot=snapshot
        )
        if snapshot.clock.day < int(self.config["activation_day"]):
            return coordinated
        original = list(coordinated.get("market", []) or [])
        sells = [
            order
            for order in original
            if isinstance(order, list) and order and order[0] == "SELL"
        ]
        non_sells = [
            order
            for order in original
            if not (isinstance(order, list) and order and order[0] == "SELL")
        ]
        reordered = [*sells, *non_sells]
        if reordered != original:
            self.market_reordered_batches += 1
            coordinated["market"] = reordered
        self.observed_sale_units += sum(int(order[2]) for order in sells)
        return coordinated

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        day = int(observation.get("day", 0))
        if day != self.last_scheduler_day:
            self.last_assignments = {}
            self.daily_modes.append(
                {
                    "day": day,
                    "mode": (
                        "E18_2_BOOTSTRAP"
                        if day < int(self.config["activation_day"])
                        else "STATE_DRIVEN_772"
                    ),
                }
            )
            self.last_scheduler_day = day
        return super().__call__(observation, configuration)

    def telemetry_snapshot(self) -> dict[str, Any]:
        for index in self._pending_ledger:
            self.ledger_records[index]["outcome"] = "UNKNOWN"
            self.execution_outcomes["UNKNOWN"] += 1
        self._pending_ledger = []
        for index in self._pending_market_ledger:
            self.market_ledger_records[index]["outcome"] = "UNKNOWN"
            self.market_execution_outcomes["UNKNOWN"] += 1
        self._pending_market_ledger = []
        provider_instance = getattr(
            self.base_policy, "codex_e18_capacity_governed_instance", None
        )
        provider = (
            provider_instance.telemetry_snapshot()
            if provider_instance is not None
            else None
        )
        return {
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "base_agent_version": (
                provider.get("agent_version") if provider is not None else None
            ),
            "observations": self.observations,
            "activation_day": int(self.config["activation_day"]),
            "topology_mode": "7-7-2",
            "pasture_target_count": len(self.config["pasture_targets"]),
            "daily_modes": deepcopy(self.daily_modes),
            "routing_commands": self.routing_commands,
            "service_commands": self.service_commands,
            "action_counts": dict(self.action_counts),
            "task_counts": dict(self.task_counts),
            "execution_outcomes": dict(self.execution_outcomes),
            "ledger_record_count": len(self.ledger_records),
            "coordinated_market_batches": self.coordinated_market_batches,
            "market_execution_outcomes": dict(self.market_execution_outcomes),
            "market_cap_clamped_units": dict(self.market_cap_clamped_units),
            "market_reordered_batches": self.market_reordered_batches,
            "requested_sale_units": self.observed_sale_units,
            "sale_deferral_batches": self.sale_deferral_batches,
            "deferred_sale_items": dict(self.sale_deferred_since),
            "reclaimed_seed_requested": self.reclaimed_seed_requested,
            "technical_errors": self.error_count,
            "fallbacks": self.fallback_count,
            "public_features_only": True,
            "cross_episode_memory": False,
            "provider": provider,
        }


def create_codex_e18_state_driven_772(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    """Create the fail-closed E18.4 state-driven 7-7-2 policy."""

    instance = CodexE18StateDriven772Agent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_state_driven_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_state_driven_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_state_driven_instance = instance
    policy.codex_e18_state_driven_last_error = None
    policy.__name__ = "codex_e18_4_state_driven_772_v1_policy"
    return policy


__all__ = [
    "DEFAULT_E18_STATE_DRIVEN_CONFIG_PATH",
    "E18_STATE_DRIVEN_MODEL_SPEC_VERSION",
    "CodexE18StateDriven772Agent",
    "create_codex_e18_state_driven_772",
    "load_e18_state_driven_config",
]
