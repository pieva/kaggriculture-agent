"""Capacity-governed E18.2 overlay over the proven Codex E17 V4D chassis.

The governor is deliberately asymmetric: own service capacity is the safety
constraint, while the opponent's public farm is only a secondary demand
signal.  It can delay one marginal Q2 pasture and use that cell for a crop,
or temporarily route otherwise-idle workers to an observed service backlog.
V4D remains byte-for-byte authoritative when the governor is disabled and on
terminal days 28-29.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.state import CROPS
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _SAFE_PASS,
    CodexE17TopologyCap662Agent,
    _farm,
    _positions,
    _quadrant,
    _store_unit_actions,
    _tile,
    _unit_actions,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    _public_feature_snapshot,
    _public_opponent_farm,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH = (
    REPO_ROOT
    / "experiments/e18/configs/codex/"
    / "CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1.json"
)
E18_CAPACITY_GOVERNED_MODEL_SPEC_VERSION = (
    "CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1"
)
_MODES = frozenset({"DENSE_V4D", "RECLAIM_CROP", "RECOVERY"})


def load_e18_capacity_governed_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1",
        "model_spec_version": E18_CAPACITY_GOVERNED_MODEL_SPEC_VERSION,
        "base_policy": (
            "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28"
        ),
        "causal_family": "OWN_CAPACITY_PRIMARY_PUBLIC_OPPONENT_SECONDARY",
        "public_features_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "topology_reclaim_enabled": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    if int(config.get("decision_day", -1)) < 1:
        raise ValueError("decision_day must be positive")
    if int(config.get("terminal_passthrough_day", -1)) != 28:
        raise ValueError("V4D terminal routing must remain authoritative from D28")
    if int(config.get("recovery_exit_clean_days", 0)) < 1:
        raise ValueError("recovery requires hysteresis")
    if int(config.get("mode_minimum_dwell_days", 0)) < 1:
        raise ValueError("modes require a positive minimum dwell")
    dense = {tuple(value) for value in config.get("dense_pasture_targets", [])}
    reclaim = [tuple(value) for value in config.get("reclaim_targets_in_order", [])]
    if len(dense) != 19:
        raise ValueError("the frozen V4D topology must contain nineteen targets")
    if not reclaim or len(reclaim) != len(set(reclaim)):
        raise ValueError("reclaim targets must be a non-empty unique sequence")
    if not set(reclaim).issubset(dense):
        raise ValueError("every reclaim target must be a V4D pasture")
    if reclaim != [(4, 7)]:
        raise ValueError("V1 may delay only the single marginal Q2 pasture")
    if int(config.get("reclaimed_seed_backfill_units", 0)) != len(reclaim):
        raise ValueError("seed backfill must cover the reclaim envelope")
    weights = config.get("opponent_pressure_weights", {}) or {}
    if set(weights) != {
        "extra_quadrants",
        "crops",
        "hands",
        "animals",
        "pastures",
        "weeds",
    }:
        raise ValueError("opponent pressure weights are incomplete")
    return deepcopy(config)


def _own_capacity_snapshot(observation: dict[str, Any]) -> dict[str, int]:
    farm = _farm(observation)
    counts: Counter[str] = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            kind = str(tile.get("kind", ""))
            if kind == "WEED":
                counts["weeds"] += 1
            elif kind == "PLANT":
                counts["crops"] += 1
                if int(tile.get("consecutive_unwatered", 0) or 0) > 0:
                    counts["water_stressed"] += 1
                if int(tile.get("yield_units", 0) or 0) > 0:
                    counts["harvest_ready"] += 1
            if tile.get("animal"):
                counts["animals"] += 1
                if int(tile.get("consecutive_unfed", 0) or 0) > 0:
                    counts["feed_stressed"] += 1
    hands = 1 + len(farm.get("hands", []) or [])
    hard_stress = (
        counts["weeds"] * 2
        + counts["water_stressed"]
        + counts["feed_stressed"] * 2
    )
    service_demand = hard_stress + min(counts["harvest_ready"], hands)
    return {
        "hands": hands,
        "crops": counts["crops"],
        "animals": counts["animals"],
        "weeds": counts["weeds"],
        "water_stressed": counts["water_stressed"],
        "feed_stressed": counts["feed_stressed"],
        "harvest_ready": counts["harvest_ready"],
        "hard_stress": hard_stress,
        "capacity_margin": hands - service_demand,
    }


class CodexE18CapacityGovernedV4DAgent(CodexE17TopologyCap662Agent):
    """Keep V4D dense unless live capacity can safely fund one crop reclaim."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        self.e18_config = load_e18_capacity_governed_config(config_path)
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.candidate_id = str(self.e18_config["candidate_id"])
        self.model_spec_version = E18_CAPACITY_GOVERNED_MODEL_SPEC_VERSION
        self.governor_enabled = bool(self.e18_config["governor_enabled"])
        self.dense_targets = frozenset(
            tuple(value) for value in self.e18_config["dense_pasture_targets"]
        )
        self.reclaim_order = tuple(
            tuple(value) for value in self.e18_config["reclaim_targets_in_order"]
        )
        self.pasture_targets = self.dense_targets
        self.reclaimed_crop_targets = frozenset()
        self.target_pastures_by_quadrant = self._target_counts(self.pasture_targets)
        self.q2_pasture_cap = self.target_pastures_by_quadrant["Q2"]
        self.livestock_resource_cap = len(self.pasture_targets) + 1
        self.config.update(
            {
                "reclaimed_crop_activation_day": int(
                    self.e18_config["reclaimed_crop_activation_day"]
                ),
                "reclaimed_crop_priority": list(
                    self.e18_config["reclaimed_crop_priority"]
                ),
                "reclaimed_crop_cutoffs": deepcopy(
                    self.e18_config["reclaimed_crop_cutoffs"]
                ),
                "reclaimed_seed_backfill_crop": str(
                    self.e18_config["reclaimed_seed_backfill_crop"]
                ),
                "reclaimed_seed_backfill_units": int(
                    self.e18_config["reclaimed_seed_backfill_units"]
                ),
                "reclaimed_seed_unit_cost": float(
                    self.e18_config["reclaimed_seed_unit_cost"]
                ),
                "reclaimed_seed_operating_cash_floor": float(
                    self.e18_config["reclaimed_seed_operating_cash_floor"]
                ),
                "pre_q2_livestock_resource_cap": len(self.pasture_targets),
            }
        )
        self.mode = "DENSE_V4D"
        self.mode_enter_day = 0
        self.mode_history: list[dict[str, Any]] = [
            {"day": 0, "from": None, "to": self.mode, "reason": "initial"}
        ]
        self.action_effect_modes: set[str] = {"DENSE_V4D"}
        self.committed_reclaims: set[tuple[int, int]] = set()
        self.last_observed_day: int | None = None
        self.clean_recovery_days = 0
        self.latest_own_capacity: dict[str, int] = {}
        self.latest_opponent_features: dict[str, int | float] = {}
        self.latest_opponent_pressure = 0.0
        self.capacity_history: list[dict[str, Any]] = []
        self.recovery_route_actions = 0
        self.recovery_service_commands = 0
        self.opponent_conditioned_recovery_batches = 0
        self.no_freed_work_violations = 0
        self.aborted_reclaim_batches = 0
        self.terminal_passthrough_batches = 0

    @staticmethod
    def _target_counts(
        targets: frozenset[tuple[int, int]],
    ) -> dict[str, int]:
        counts = Counter(_quadrant(target) for target in targets)
        return {quadrant: counts[quadrant] for quadrant in ("Q0", "Q1", "Q2")}

    def _opponent_pressure(self, features: dict[str, int | float]) -> float:
        weights = self.e18_config["opponent_pressure_weights"]
        return (
            max(0, int(features["quadrants"]) - 1)
            * float(weights["extra_quadrants"])
            + int(features["crops"]) * float(weights["crops"])
            + int(features["hands"]) * float(weights["hands"])
            + int(features["animals"]) * float(weights["animals"])
            + int(features["pastures"]) * float(weights["pastures"])
            + int(features["weeds"]) * float(weights["weeds"])
        )

    def _transition(self, day: int, mode: str, reason: str) -> None:
        if mode not in _MODES:
            raise ValueError(mode)
        if mode == self.mode:
            return
        previous = self.mode
        self.mode = mode
        self.mode_enter_day = day
        self.mode_history.append(
            {"day": day, "from": previous, "to": mode, "reason": reason}
        )

    def _apply_reclaim_envelope(self) -> None:
        self.pasture_targets = frozenset(
            self.dense_targets.difference(self.committed_reclaims)
        )
        self.reclaimed_crop_targets = frozenset(self.committed_reclaims)
        self.target_pastures_by_quadrant = self._target_counts(self.pasture_targets)
        self.q2_pasture_cap = self.target_pastures_by_quadrant["Q2"]
        self.livestock_resource_cap = len(self.pasture_targets) + 1
        self.config["pre_q2_livestock_resource_cap"] = len(self.pasture_targets)

    def _observe_day(self, observation: dict[str, Any]) -> None:
        day = int(observation.get("day", 0))
        if day == self.last_observed_day:
            return
        own = _own_capacity_snapshot(observation)
        opponent = _public_feature_snapshot(_public_opponent_farm(observation))
        pressure = self._opponent_pressure(opponent)
        self.latest_own_capacity = own
        self.latest_opponent_features = opponent
        self.latest_opponent_pressure = pressure
        self.capacity_history.append(
            {
                "day": day,
                "mode": self.mode,
                "own": deepcopy(own),
                "opponent_pressure": pressure,
            }
        )
        self.last_observed_day = day
        if not self.governor_enabled or day >= int(
            self.e18_config["terminal_passthrough_day"]
        ):
            return

        hard_stress = int(own["hard_stress"])
        dwell = day - self.mode_enter_day
        min_dwell = int(self.e18_config["mode_minimum_dwell_days"])
        if hard_stress >= int(self.e18_config["recovery_entry_stress"]):
            self.clean_recovery_days = 0
            if self.mode != "RECOVERY" and dwell >= min_dwell:
                self._transition(day, "RECOVERY", "own_service_stress")
            return
        if self.mode == "RECOVERY":
            self.clean_recovery_days += 1
            if (
                self.clean_recovery_days
                >= int(self.e18_config["recovery_exit_clean_days"])
                and dwell >= min_dwell
            ):
                resumed = "RECLAIM_CROP" if self.committed_reclaims else "DENSE_V4D"
                self._transition(day, resumed, "capacity_recovered")
            return

        if (
            bool(self.e18_config["topology_reclaim_enabled"])
            and
            not self.committed_reclaims
            and day >= int(self.e18_config["decision_day"])
            and int(own["hands"])
            >= int(self.e18_config["minimum_hands_for_reclaim"])
            and int(own["capacity_margin"])
            >= int(self.e18_config["minimum_capacity_margin"])
            and pressure >= float(self.e18_config["reclaim_pressure_threshold"])
            and dwell >= min_dwell
        ):
            target = self.reclaim_order[0]
            if _tile(_farm(observation), target) in {None, "LOCKED"}:
                self.committed_reclaims.add(target)
                self._apply_reclaim_envelope()
                self._transition(day, "RECLAIM_CROP", "capacity_funded_reclaim")

    def _reclaimed_crop_tasks(
        self,
        observation: dict[str, Any],
    ) -> list[tuple[int, tuple[int, int], list[Any]]]:
        if int(observation.get("day", 0)) < int(
            self.e18_config["reclaimed_crop_activation_day"]
        ):
            return []
        farm = _farm(observation)
        private = observation.get("private", {}) or {}
        day = int(observation.get("day", 0))
        seeds = Counter(private.get("seeds", {}) or {})
        tasks: list[tuple[int, tuple[int, int], list[Any]]] = []
        for target in sorted(self.reclaimed_crop_targets):
            tile = _tile(farm, target)
            if tile == "LOCKED":
                continue
            if tile is None:
                crop = self._crop_choice(day=day, seeds=seeds)
                if crop is not None:
                    tasks.append((3, target, ["PLANT", crop]))
            elif isinstance(tile, dict) and tile.get("kind") == "WEED":
                tasks.append((1, target, ["DIG"]))
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                crop = str(tile.get("crop", ""))
                mature = day - int(tile.get("planted_day", day)) >= int(
                    CROPS.get(crop, {}).get("first_yield_day", 10**6)
                )
                if mature and int(tile.get("yield_units", 0) or 0) > 0:
                    tasks.append((0, target, ["HARVEST"]))
                elif day < 28 and not bool(tile.get("watered_today", False)):
                    tasks.append((2, target, ["WATER"]))
        return tasks

    @staticmethod
    def _recovery_tasks(
        observation: dict[str, Any],
    ) -> list[tuple[int, tuple[int, int], list[Any]]]:
        farm = _farm(observation)
        day = int(observation.get("day", 0))
        tasks: list[tuple[int, tuple[int, int], list[Any]]] = []
        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict):
                    continue
                target = (x, y)
                if tile.get("kind") == "WEED":
                    tasks.append((1, target, ["DIG"]))
                elif tile.get("kind") == "PLANT":
                    crop = str(tile.get("crop", ""))
                    mature = day - int(tile.get("planted_day", day)) >= int(
                        CROPS.get(crop, {}).get("first_yield_day", 10**6)
                    )
                    if mature and int(tile.get("yield_units", 0) or 0) > 0:
                        tasks.append((0, target, ["HARVEST"]))
                    elif day < 28 and not bool(tile.get("watered_today", False)):
                        tasks.append((2, target, ["WATER"]))
        return tasks

    def _route_idle_service(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        *,
        tasks: list[tuple[int, tuple[int, int], list[Any]]],
        eligible: set[int],
        limit: int,
    ) -> set[int]:
        positions = _positions(_farm(observation))
        actions = _unit_actions(action, len(positions))
        free = {
            worker
            for worker in eligible
            if worker < len(actions) and actions[worker] == ["PASS"]
        }
        assigned: set[int] = set()
        fulfilled = {
            (positions[worker], str(command[0]))
            for worker, command in enumerate(actions)
            if worker < len(positions) and command
        }
        for _priority, target, command in sorted(
            tasks, key=lambda value: (value[0], value[1][1], value[1][0])
        ):
            if len(assigned) >= limit or not free:
                break
            if (target, str(command[0])) in fulfilled:
                continue
            on_target = [worker for worker in free if positions[worker] == target]
            if not on_target:
                continue
            worker = min(on_target)
            actions[worker] = list(command)
            self.recovery_service_commands += 1
            assigned.add(worker)
            free.remove(worker)
        _store_unit_actions(action, actions)
        return assigned

    @staticmethod
    def _pass_workers(action: dict[str, Any], count: int) -> set[int]:
        return {
            index
            for index, command in enumerate(_unit_actions(action, count))
            if command == ["PASS"]
        }

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        self._observe_day(observation)
        provider = self.base_policy(observation, configuration)
        self.observation_count += 1
        day = int(observation.get("day", 0))
        if not self.governor_enabled:
            return deepcopy(provider)
        if day >= int(self.e18_config["terminal_passthrough_day"]):
            self.terminal_passthrough_batches += 1
            return deepcopy(provider)

        action = deepcopy(provider)
        worker_count = len(_positions(_farm(observation)))
        provider_pass = self._pass_workers(provider, worker_count)
        released: set[int] = set()
        if self.committed_reclaims:
            self._observe_topology(observation)
            released = self._filter_unit_actions(action, observation)
            self._filter_market(action, observation)
            self._backfill_reclaimed_seed_market(action, observation, configuration)
            eligible = set(provider_pass).union(released)
            self._route_idle_service(
                action,
                observation,
                tasks=self._reclaimed_crop_tasks(observation),
                eligible=eligible,
                limit=int(self.e18_config["reclaim_worker_limit"]),
            )

        if self.mode == "RECOVERY":
            pressure_high = self.latest_opponent_pressure >= float(
                self.e18_config["reclaim_pressure_threshold"]
            )
            severe_own_stress = int(
                self.latest_own_capacity.get("hard_stress", 0)
            ) >= 2 * int(self.e18_config["recovery_entry_stress"])
            recovery_limit = (
                int(self.e18_config["recovery_worker_limit"])
                if pressure_high or severe_own_stress
                else 0
            )
            if pressure_high and recovery_limit:
                self.opponent_conditioned_recovery_batches += 1
            self._route_idle_service(
                action,
                observation,
                tasks=self._recovery_tasks(observation),
                eligible=set(provider_pass).union(released),
                limit=recovery_limit,
            )

        emitted_pass = self._pass_workers(action, worker_count)
        introduced_pass = emitted_pass.difference(provider_pass)
        if introduced_pass:
            self.no_freed_work_violations += len(introduced_pass)
            self.aborted_reclaim_batches += 1
            self.committed_reclaims.clear()
            self._apply_reclaim_envelope()
            self._transition(day, "DENSE_V4D", "reclaim_could_not_fund_work")
            return deepcopy(provider)
        if action != provider:
            self.override_batches += 1
            self.action_effect_modes.add(self.mode)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base_instance = getattr(
            self.base_policy,
            "codex_e17_batched_cluster_routing_instance",
            None,
        )
        return {
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "base_agent_version": getattr(base_instance, "model_spec_version", None),
            "governor_enabled": self.governor_enabled,
            "topology_reclaim_enabled": bool(
                self.e18_config["topology_reclaim_enabled"]
            ),
            "mode": self.mode,
            "mode_history": deepcopy(self.mode_history),
            "action_effect_modes": sorted(self.action_effect_modes),
            "committed_reclaims": [
                list(target) for target in sorted(self.committed_reclaims)
            ],
            "target_pastures_by_quadrant": deepcopy(
                self.target_pastures_by_quadrant
            ),
            "livestock_resource_cap": self.livestock_resource_cap,
            "latest_own_capacity": deepcopy(self.latest_own_capacity),
            "latest_opponent_features": deepcopy(self.latest_opponent_features),
            "latest_opponent_pressure": self.latest_opponent_pressure,
            "capacity_history": deepcopy(self.capacity_history),
            "override_batches": self.override_batches,
            "recovery_route_actions": self.recovery_route_actions,
            "recovery_service_commands": self.recovery_service_commands,
            "opponent_conditioned_recovery_batches": (
                self.opponent_conditioned_recovery_batches
            ),
            "no_freed_work_violations": self.no_freed_work_violations,
            "aborted_reclaim_batches": self.aborted_reclaim_batches,
            "terminal_passthrough_batches": self.terminal_passthrough_batches,
            "technical_errors": self.error_count,
            "fallbacks": self.fallback_count,
            "public_features_only": True,
            "cross_episode_memory": False,
        }


def create_codex_e18_capacity_governed_v4d(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    """Create the fail-closed E18.2 capacity-governed V4D policy."""

    instance = CodexE18CapacityGovernedV4DAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            return instance(observation, configuration)
        except Exception as exc:  # noqa: BLE001 - fail-closed episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_capacity_governed_instance = instance
    return policy
