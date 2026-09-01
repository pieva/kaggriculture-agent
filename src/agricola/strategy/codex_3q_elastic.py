"""Codex V8.0: payback-gated elastic Q2 satellite over frozen V7.3."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex_compact_q0 import (
    ANIMAL_RULES,
)
from agricola.strategy.codex_dual_q0_q1 import DUAL_ROLE_SEQUENCE
from agricola.strategy.codex_dual_q1_cadence import CodexDualQ1CadenceAgent
from agricola.strategy.codex_lifecycle import CodexSnapshot

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_3Q_CONFIG_PATH = (
    REPO_ROOT / "configs" / "model_spec_c2" / "CODEX_C2_3Q_ELASTIC_CONFIG.json"
)
THREE_Q_MODEL_SPEC_VERSION = "CODEX-C2-V8.0-3Q-ELASTIC-SATELLITE"
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}

# One compact twelve-tile livestock route immediately south-west of the shed.
# The crop-only diagnostic saturated MELON.  The final capacity replay splits
# Q2 across four existing three-animal service clusters (W0/W6/W9/W12) after
# both one- and two-incremental-hand variants failed the economic gate.
Q2_PASTURE_POSITIONS: tuple[tuple[int, int], ...] = (
    (3, 5),
    (3, 6),
    (4, 6),
    (2, 5),
    (2, 6),
    (2, 7),
    (1, 5),
    (1, 6),
    (1, 7),
    (0, 5),
    (0, 6),
    (0, 7),
)
Q2_CROP_POSITIONS: tuple[tuple[int, int], ...] = ()
THREE_Q_ROLE_SEQUENCE = DUAL_ROLE_SEQUENCE


def load_3q_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path) if path is not None else DEFAULT_3Q_CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("candidate_id") != "CODEX_C2_3Q_ELASTIC":
        raise ValueError("unexpected 3Q candidate_id")
    if config.get("model_spec_version") != THREE_Q_MODEL_SPEC_VERSION:
        raise ValueError("unexpected 3Q model_spec_version")
    if int(config.get("quadrants_owned", 0)) != 3:
        raise ValueError("3Q candidate requires Q0+Q1+Q2")
    if int(config.get("workforce_total", 0)) != len(THREE_Q_ROLE_SEQUENCE):
        raise ValueError("3Q capacity replay preserves thirteen total workers")
    if int(config.get("q2_crop_working_set_target", -1)) != 0:
        raise ValueError("V8.0 cycle 2 freezes Q2 crop at zero")
    if config.get("q2_livestock_targets") != {"COW": 6, "SHEEP": 6}:
        raise ValueError("V8.0 cycle 2 requires a 6+6 Q2 livestock core")
    if int(config.get("q2_incremental_hands", -1)) != 0:
        raise ValueError("V8.0 capacity replay uses existing workers")
    return deepcopy(config)


class CodexThreeQElasticAgent(CodexDualQ1CadenceAgent):
    """Frozen Q0/Q1 core plus a four-cluster elastic Q2 satellite."""

    def __init__(
        self,
        candidate_config: dict[str, Any] | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        config = deepcopy(candidate_config or load_3q_config())
        super().__init__(config, run_context=run_context)
        self.candidate_id = "CODEX_C2_3Q_ELASTIC"
        self.model_spec_version = THREE_Q_MODEL_SPEC_VERSION
        self.expected_max_quadrants = 3

        self.q2_crop_positions = Q2_CROP_POSITIONS
        self.q2_pasture_positions = Q2_PASTURE_POSITIONS
        self.pasture_positions = (*self.pasture_positions, *self.q2_pasture_positions)
        self.pasture_positions_by_species = {
            "COW": (
                *self.pasture_positions_by_species["COW"],
                *self.q2_pasture_positions[:6],
            ),
            "SHEEP": (
                *self.pasture_positions_by_species["SHEEP"],
                *self.q2_pasture_positions[6:],
            ),
        }

        self.q2_activation_day: int | None = None
        self.q2_full_module_day: int | None = None
        self.q2_first_output_day: int | None = None
        self.q2_first_output_product: str | None = None
        self.q2_activation_records: list[dict[str, Any]] = []
        self._q2_activation_decisions: set[int] = set()

    def _role_for(self, worker_id: int) -> str:
        return THREE_Q_ROLE_SEQUENCE[
            min(worker_id, len(THREE_Q_ROLE_SEQUENCE) - 1)
        ]

    def _target_workforce(self, snapshot: CodexSnapshot) -> int:
        owned = self._owned_quadrants(snapshot.farm)
        if owned < 2:
            return int(self.config["q0_workforce_total"])
        if owned < 3:
            return int(self.config["dual_workforce_total"])
        return int(self.config["workforce_total"])

    def _crop_positions_for_role(
        self, role: str
    ) -> tuple[tuple[int, int], ...]:
        return super()._crop_positions_for_role(role)

    @staticmethod
    def _role_module(role: str) -> str | None:
        return CodexDualQ1CadenceAgent._role_module(role)

    def _module_animal_positions(
        self, module: str, species: str
    ) -> tuple[tuple[int, int], ...]:
        if module == "Q2":
            return (
                self.q2_pasture_positions[:6]
                if species == "COW"
                else self.q2_pasture_positions[6:]
            )
        return super()._module_animal_positions(module, species)

    def _module_animal_tasks(
        self, snapshot: CodexSnapshot, module: str, species: str
    ) -> list[dict[str, Any]]:
        tasks = super()._module_animal_tasks(snapshot, module, species)
        if module != "Q2":
            return tasks
        module_positions = self._module_animal_positions(module, species)
        tasks = [
            task
            for task in tasks
            if task["kind"] != "FEED"
            or int(
                (
                    self._tile(snapshot.farm, tuple(task["target"]))
                    or {}
                ).get("consecutive_unfed", 0)
            )
            >= 1
            or (
                module_positions.index(tuple(task["target"]))
                + snapshot.clock.day
            )
            % 2
            == 0
        ]
        recovery = [
            self._task(
                position,
                ["DIG"],
                kind="PASTURE_RECOVERY",
                loss_rank=1,
                value=500,
                slack=12,
            )
            for position in self._module_animal_positions(module, species)
            if isinstance(self._tile(snapshot.farm, position), dict)
            and self._tile(snapshot.farm, position).get("kind") == "WEED"
        ]
        return recovery + tasks

    def _feed_assignments(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[tuple[str, str]]:
        return super()._feed_assignments(snapshot, worker_id, role)

    def _q2_role_assignment(
        self, snapshot: CodexSnapshot, role: str
    ) -> tuple[str, tuple[tuple[int, int], ...]] | None:
        if self._owned_quadrants(snapshot.farm) < 3:
            return None
        cows = self.q2_pasture_positions[:6]
        sheep = self.q2_pasture_positions[6:]
        if role == "FLOAT_RESERVE":
            return "COW", cows[:3]
        if role == "FERTILIZER_LOGISTICS_Q0":
            return "COW", cows[3:]
        if role == "CROP_ZONE_5":
            return "SHEEP", sheep[:3]
        if role == "FERTILIZER_LOGISTICS_Q1":
            return "SHEEP", sheep[3:]
        return None

    def _feed_tasks_for_worker(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[dict[str, Any]]:
        tasks = super()._feed_tasks_for_worker(snapshot, worker_id, role)
        assignment = self._q2_role_assignment(snapshot, role)
        if assignment is None:
            return tasks
        species, positions = assignment
        allowed = set(positions)
        tasks.extend(
            task
            for task in self._module_animal_tasks(snapshot, "Q2", species)
            if task["kind"] == "FEED" and tuple(task["target"]) in allowed
        )
        return tasks

    def _inventory_task(
        self,
        snapshot: CodexSnapshot,
        worker_id: int,
        role: str,
    ) -> list[dict[str, Any]]:
        assignment = self._q2_role_assignment(snapshot, role)
        q2_species = assignment[0] if assignment is not None else None
        q2_positions = assignment[1] if assignment is not None else ()
        inventory = self._inventory(snapshot.private, worker_id)
        if q2_species and int(inventory.get(q2_species, 0)) > 0:
            return [
                self._task(
                    target,
                    ["PLACE", q2_species],
                    kind="PLACE_ANIMAL",
                    loss_rank=1,
                    value=int(ANIMAL_RULES[q2_species]["cost"]),
                    slack=12,
                )
                for target in q2_positions
                if isinstance(self._tile(snapshot.farm, target), dict)
                and self._tile(snapshot.farm, target).get("kind") == "PASTURE"
                and not self._tile(snapshot.farm, target).get("animal")
            ]

        base = super()._inventory_task(snapshot, worker_id, role)
        if base and base[0]["kind"] != "ANIMAL_STAGING":
            if assignment is not None and tuple(base[0]["target"]) == (4, 4):
                base = [{**task, "target": (4, 5)} for task in base]
            return base
        if self._owned_quadrants(snapshot.farm) < 3:
            return base

        shed = snapshot.private.get("shed", {}) or {}
        if q2_species and int(shed.get(q2_species, 0)) > 0:
            free = [
                target
                for target in q2_positions
                if isinstance(self._tile(snapshot.farm, target), dict)
                and self._tile(snapshot.farm, target).get("kind") == "PASTURE"
                and not self._tile(snapshot.farm, target).get("animal")
            ]
            if free:
                return [
                    self._task(
                        (4, 5),
                        ["PICKUP", q2_species, 1],
                        kind="ANIMAL_STAGING",
                        loss_rank=1,
                        value=int(ANIMAL_RULES[q2_species]["cost"]),
                        slack=12,
                    )
                ]
        # Core workers must not stage Q2 animals and then cross the boundary.
        if base and base[0]["kind"] == "ANIMAL_STAGING":
            return []
        return base

    def _float_reserve_candidates(
        self,
        snapshot: CodexSnapshot,
        crop_tasks: list[dict[str, Any]],
        hard_crop_tasks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        # Preserve V7.3 W0 behavior exactly while the core has any actionable
        # work.  Q2 relief is allowed only when Q0/Q1 yield no candidate.
        core = super()._float_reserve_candidates(
            snapshot, crop_tasks, hard_crop_tasks
        )
        if self._owned_quadrants(snapshot.farm) < 3:
            return core
        if hard_crop_tasks:
            return hard_crop_tasks
        bootstrap = [
            {
                **task,
                "loss_rank": 1,
                "value": 500,
            }
            for species in ("COW", "SHEEP")
            for task in self._module_animal_tasks(snapshot, "Q2", species)
            if task["kind"] in {"BUILD_PASTURE", "PASTURE_RECOVERY"}
        ]
        return bootstrap if bootstrap else core

    def _fertilizer_role_candidates(
        self,
        snapshot: CodexSnapshot,
        role: str,
        hard_crop_tasks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        # V7.2 classified every zone >=3 as Q1.  Remove Q2 from that inherited
        # fallback so W6/W12 never lose a frozen-core obligation to the satellite.
        base = super()._fertilizer_role_candidates(
            snapshot, role, hard_crop_tasks
        )
        assignment = self._q2_role_assignment(snapshot, role)
        if assignment is None or role not in {
            "FERTILIZER_LOGISTICS_Q0",
            "FERTILIZER_LOGISTICS_Q1",
        }:
            return base
        species, positions = assignment
        allowed = set(positions)
        q2_service = [
            {
                **task,
                "loss_rank": (
                    1
                    if task["kind"]
                    in {"BUILD_PASTURE", "PASTURE_RECOVERY"}
                    else int(task["loss_rank"])
                ),
                "value": (
                    500
                    if task["kind"]
                    in {"BUILD_PASTURE", "PASTURE_RECOVERY"}
                    else min(150, int(task["value"]))
                ),
            }
            for task in self._module_animal_tasks(snapshot, "Q2", species)
            if tuple(task["target"]) in allowed
            and task["kind"]
            in {
                "ANIMAL_COLLECTION",
                "CARE",
                "BUILD_PASTURE",
                "PASTURE_RECOVERY",
            }
        ]
        return base + q2_service

    def _maybe_replan_global(self, snapshot: CodexSnapshot) -> None:
        super()._maybe_replan_global(snapshot)
        if (
            self._owned_quadrants(snapshot.farm) >= 3
            and self.q2_activation_day is None
        ):
            self.q2_activation_day = snapshot.clock.day
            self.q2_activation_records.append(
                {
                    "event": "Q2_OBSERVED_ACTIVE",
                    "day": snapshot.clock.day,
                    "step": snapshot.clock.step,
                    "money": float(snapshot.farm.get("money", 0.0)),
                }
            )

    def _unit_actions(self, snapshot: CodexSnapshot) -> list[list[Any]]:
        actions = super()._unit_actions(snapshot)
        positions = self._positions(snapshot.farm)
        worker_id = 9
        if worker_id < len(positions) and actions[worker_id] == ["PASS"]:
            role = self._role_for(worker_id)
            assignment = self._q2_role_assignment(snapshot, role)
            if assignment is not None:
                species, assigned = assignment
                allowed = set(assigned)
                candidates = [
                    task
                    for task in self._module_animal_tasks(
                        snapshot, "Q2", species
                    )
                    if task["kind"] != "FEED"
                    and tuple(task["target"]) in allowed
                ]
                action = self._choose_committed_task(
                    snapshot,
                    worker_id,
                    role,
                    positions[worker_id],
                    candidates,
                    set(),
                )
                if self._eligible_unit_action(snapshot, worker_id, action):
                    actions[worker_id] = action
        return actions

    def _q2_admission_ledger(self, snapshot: CodexSnapshot) -> dict[str, Any]:
        shed = snapshot.private.get("shed", {}) or {}
        prices = snapshot.market.get("prices", {}) or {}
        sellable = ("MILK", "WOOL", "MELON", "STRAWBERRY", "FERTILIZER")
        shed_sales = sum(
            int(shed.get(item, 0)) * float(prices.get(item, 0.0))
            for item in sellable
        )
        carried_sales = sum(
            int(self._inventory(snapshot.private, worker_id).get(item, 0))
            * float(prices.get(item, 0.0))
            for worker_id in range(len(self._positions(snapshot.farm)))
            for item in sellable
        )
        prospective_sales = shed_sales + carried_sales
        available = float(snapshot.farm.get("money", 0.0)) + prospective_sales
        remaining_days = max(
            0,
            (snapshot.clock.episode_steps - snapshot.clock.step)
            // snapshot.clock.turns_per_day,
        )
        labor_cost = remaining_days * int(
            self.config["q2_incremental_daily_hire_cost"]
        )
        animal_cost = (
            6 * int(ANIMAL_RULES["COW"]["cost"])
            + 6 * int(ANIMAL_RULES["SHEEP"]["cost"])
        )
        feed_cost = (
            12 * remaining_days * float(prices.get("WHEAT", 25.0))
        )
        projected_gross = (
            6 * 10 * float(prices.get("MILK", 160.0))
            + 6 * 12 * float(prices.get("WOOL", 200.0))
        )
        projected_net = (
            projected_gross
            - int(self.config["q2_land_cost"])
            - animal_cost
            - feed_cost
            - labor_cost
        )
        admitted = (
            self.q1_full_module_day is not None
            and available
            >= float(self.config["q2_activation_cash_plus_inventory"])
            and remaining_days >= int(self.config["q2_min_remaining_days"])
            and projected_net >= float(self.config["q2_projected_net_floor"])
            and int(self.animal_escapes) == 0
        )
        return {
            "event": "Q2_ADMISSION_DECISION",
            "day": snapshot.clock.day,
            "step": snapshot.clock.step,
            "money": float(snapshot.farm.get("money", 0.0)),
            "prospective_sales": prospective_sales,
            "shed_sales": shed_sales,
            "carried_sales": carried_sales,
            "available": available,
            "land_cost": int(self.config["q2_land_cost"]),
            "remaining_days": remaining_days,
            "projected_incremental_labor_cost": labor_cost,
            "projected_animal_cost": animal_cost,
            "projected_feed_cost": feed_cost,
            "projected_gross": projected_gross,
            "projected_net": projected_net,
            "q1_full_module": self.q1_full_module_day is not None,
            "animal_escapes": int(self.animal_escapes),
            "admitted": admitted,
        }

    def _market_orders(self, snapshot: CodexSnapshot) -> list[list[Any]]:
        owned = self._owned_quadrants(snapshot.farm)
        original_targets = self.config["livestock_targets"]
        if owned < 3:
            self.config["livestock_targets"] = {"COW": 6, "SHEEP": 6}
        try:
            orders = super()._market_orders(snapshot)
        finally:
            self.config["livestock_targets"] = original_targets
        if owned != 2 or self._shutdown(snapshot):
            return orders
        day = snapshot.clock.day
        if not int(self.config["q2_activation_min_day"]) <= day <= int(
            self.config["q2_activation_max_day"]
        ):
            return orders
        ledger = self._q2_admission_ledger(snapshot)
        if day not in self._q2_activation_decisions:
            self._q2_activation_decisions.add(day)
            self.q2_activation_records.append(ledger)
        if not ledger["admitted"]:
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
                if self._owned_quadrants(snapshot.farm) >= 3
                else "NO_OP"
            )
        return super()._request_outcome(request, snapshot)

    def _record_success(
        self, request: dict[str, Any], snapshot: CodexSnapshot
    ) -> None:
        q2_adjustment: tuple[str, int] | None = None
        q2_service: tuple[str, str] | None = None
        if request.get("actor_kind") == "UNIT" and request.get("action"):
            action = request["action"]
            before_tile = request.get("before_tile")
            position = tuple(int(value) for value in request["actor_position"])
            if (
                position in set(self.q2_pasture_positions)
                and isinstance(before_tile, dict)
                and before_tile.get("animal") in ANIMAL_RULES
            ):
                species = str(before_tile["animal"])
                if action[0] in {"FEED", "CARE", "HARVEST"}:
                    q2_service = (species, action[0])
                if action[0] == "HARVEST":
                    units = int(before_tile.get("yield_units", 0))
                    q2_adjustment = (str(ANIMAL_RULES[species]["product"]), units)
        super()._record_success(request, snapshot)
        if q2_service is not None:
            species, opcode = q2_service
            self.quadrant_livestock_service[f"Q0_{species}_{opcode}"] -= 1
            self.quadrant_livestock_service[f"Q2_{species}_{opcode}"] += 1
        if q2_adjustment is not None:
            product, units = q2_adjustment
            self.quadrant_production[f"Q0_{product}"] -= units
            self.quadrant_production[f"Q2_{product}"] += units
            if units > 0 and self.q2_first_output_day is None:
                self.q2_first_output_day = snapshot.clock.day
                self.q2_first_output_product = product

    def _record_state_telemetry(self, snapshot: CodexSnapshot) -> None:
        super()._record_state_telemetry(snapshot)
        q2_animals = sum(
            1
            for position in self.q2_pasture_positions
            if isinstance(self._tile(snapshot.farm, position), dict)
            and bool(self._tile(snapshot.farm, position).get("animal"))
        )
        if self.quadrant_state_trajectory:
            self.quadrant_state_trajectory[-1]["q2_active_animals"] = q2_animals
        if self.q2_full_module_day is None and q2_animals >= len(
            self.q2_pasture_positions
        ):
            self.q2_full_module_day = snapshot.clock.day

    def telemetry_snapshot(self) -> dict[str, Any]:
        payload = super().telemetry_snapshot()
        payload.update(
            {
                "agent_version": self.model_spec_version,
                "Q2_activation_day": self.q2_activation_day,
                "Q2_full_module_day": self.q2_full_module_day,
                "Q2_first_output_day": self.q2_first_output_day,
                "Q2_first_output_product": self.q2_first_output_product,
                "Q2_activation_records": deepcopy(self.q2_activation_records),
                "Q2_MILK_units": int(self.quadrant_production["Q2_MILK"]),
                "Q2_WOOL_units": int(self.quadrant_production["Q2_WOOL"]),
            }
        )
        return payload


def create_3q_agent(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
):
    instance = CodexThreeQElasticAgent(
        load_3q_config(config_path),
        run_context=run_context,
    )

    def policy(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_3q_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_3q_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_3q_instance = instance
    policy.codex_3q_last_error = None
    policy.__name__ = "codex_3q_elastic_policy"
    return policy
