"""E18.3 fixed-topology ablations with persistent labor handoff.

V4D remains the common provider.  Every smaller topology uses the same
translation layer: pasture work outside the fixed target set is suppressed,
livestock acquisition is capped, and every released or otherwise-idle worker
is immediately offered fill, harvest, rotation, weed, plant, or water work.
The 7-7-5 arm measures the scheduler effect without reclaiming a tile.
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
    _distance,
    _farm,
    _positions,
    _quadrant,
    _store_unit_actions,
    _unit_actions,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_LABOR_CONSERVING_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1.json"
)
E18_LABOR_CONSERVING_MODEL_SPEC_VERSION = (
    "CODEX-E18.3-LABOR-CONSERVING-TOPOLOGY-ABLATION-V1"
)
TOPOLOGY_MODES = ("7-7-5", "7-7-2", "6-6-2", "7-7-0", "6-7-0")


def _topology_counts(targets: set[tuple[int, int]]) -> dict[str, int]:
    counts = Counter(_quadrant(target) for target in targets)
    return {quadrant: int(counts[quadrant]) for quadrant in ("Q0", "Q1", "Q2")}


def load_e18_labor_conserving_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_LABOR_CONSERVING_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1",
        "model_spec_version": E18_LABOR_CONSERVING_MODEL_SPEC_VERSION,
        "base_policy": (
            "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28"
        ),
        "causal_family": "FIXED_TOPOLOGY_WITH_PERSISTENT_LABOR_HANDOFF",
        "public_features_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    dense = {tuple(value) for value in config.get("dense_pasture_targets", [])}
    if len(dense) != 19 or _topology_counts(dense) != {"Q0": 7, "Q1": 7, "Q2": 5}:
        raise ValueError("dense control must be 7-7-5")
    topologies = config.get("topologies", {}) or {}
    if tuple(topologies) != TOPOLOGY_MODES:
        raise ValueError("topology modes or ordering changed")
    for mode in TOPOLOGY_MODES:
        targets = {tuple(value) for value in topologies[mode]["pasture_targets"]}
        expected_counts = {
            quadrant: int(value)
            for quadrant, value in zip(("Q0", "Q1", "Q2"), mode.split("-"), strict=True)
        }
        if not targets or not targets.issubset(dense):
            raise ValueError(f"{mode} is not a non-empty V4D subset")
        if _topology_counts(targets) != expected_counts:
            raise ValueError(f"{mode} target counts do not match its name")
    if int(config.get("provider_idle_worker_limit", -1)) < 0:
        raise ValueError("provider idle worker limit must be non-negative")
    if int(config.get("rotation_start_day", -1)) > int(
        config.get("rotation_end_day", -1)
    ):
        raise ValueError("invalid rotation window")
    return deepcopy(config)


class CodexE18LaborConservingTopologyAgent(CodexE17TopologyCap662Agent):
    """One fixed topology with labor-conserving crop reassignment."""

    def __init__(
        self,
        *,
        topology_mode: str,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        if topology_mode not in TOPOLOGY_MODES:
            raise ValueError(f"unknown topology_mode: {topology_mode}")
        self.e18_config = load_e18_labor_conserving_config(config_path)
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.topology_mode = topology_mode
        self.candidate_id = f"CODEX_E18_3_LABOR_{topology_mode.replace('-', '')}_V1"
        self.model_spec_version = E18_LABOR_CONSERVING_MODEL_SPEC_VERSION
        dense = {
            tuple(value) for value in self.e18_config["dense_pasture_targets"]
        }
        self.pasture_targets = frozenset(
            tuple(value)
            for value in self.e18_config["topologies"][topology_mode][
                "pasture_targets"
            ]
        )
        self.reclaimed_crop_targets = frozenset(
            dense.difference(self.pasture_targets)
        )
        self.expected_target_quadrants = frozenset(
            _quadrant(position) for position in self.pasture_targets
        )
        self.q2_pasture_cap = _topology_counts(set(self.pasture_targets))["Q2"]
        self.livestock_resource_cap = len(self.pasture_targets) + int(
            self.e18_config["livestock_in_transit_buffer"]
        )
        self.config.update(
            {
                "pre_q2_livestock_resource_cap": len(self.pasture_targets),
                "livestock_resource_cap": self.livestock_resource_cap,
                "pasture_fill_target": len(self.pasture_targets),
                "fill_purchase_cutoff_day": int(
                    self.e18_config["fill_purchase_cutoff_day"]
                ),
                "fill_operating_cash_floor": float(
                    self.e18_config["fill_operating_cash_floor"]
                ),
                "pasture_fill_species_priority": list(
                    self.e18_config["pasture_fill_species_priority"]
                ),
                "pasture_fill_quadrant_priority": list(
                    self.e18_config["pasture_fill_quadrant_priority"]
                ),
                "animal_costs": deepcopy(self.e18_config["animal_costs"]),
            }
        )
        self.rotation_targets: set[tuple[int, int]] = set()
        self.seed_batches_requested: set[str] = set()
        self.persistent_fill_batches = 0
        self.labor_handoff_batches = 0
        self.released_workers_total = 0
        self.released_workers_without_work = 0
        self.global_crop_commands: Counter[str] = Counter()

    def _desired_crop(
        self,
        *,
        day: int,
        seeds: Counter[str],
    ) -> str | None:
        early = str(self.e18_config["early_crop"])
        rotation = str(self.e18_config["rotation_crop"])
        if (
            day <= int(self.e18_config["early_crop_cutoff_day"])
            and seeds[early] > 0
        ):
            return early
        if (
            day <= int(self.e18_config["rotation_crop_cutoff_day"])
            and seeds[rotation] > 0
        ):
            return rotation
        return None

    def _crop_tasks(
        self,
        observation: dict[str, Any],
    ) -> list[tuple[int, tuple[int, int], list[Any]]]:
        day = int(observation.get("day", 0))
        if day < int(self.e18_config["reclaimed_crop_activation_day"]):
            return []
        farm = _farm(observation)
        private = observation.get("private", {}) or {}
        seeds = Counter(private.get("seeds", {}) or {})
        tasks: list[tuple[int, tuple[int, int], list[Any]]] = []
        for y, row in enumerate(farm.get("tiles", []) or []):
            for x, tile in enumerate(row):
                target = (x, y)
                reclaimed = target in self.reclaimed_crop_targets
                if tile == "LOCKED" or target in self.pasture_targets:
                    continue
                if tile is None:
                    if target not in self.rotation_targets and not reclaimed:
                        continue
                    crop = self._desired_crop(day=day, seeds=seeds)
                    if crop is not None:
                        tasks.append((3, target, ["PLANT", crop]))
                    continue
                if isinstance(tile, dict) and tile.get("kind") == "WEED":
                    tasks.append((1, target, ["DIG"]))
                    continue
                if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                    continue
                crop = str(tile.get("crop", ""))
                mature = day - int(tile.get("planted_day", day)) >= int(
                    CROPS.get(crop, {}).get("first_yield_day", 10**6)
                )
                if mature and int(tile.get("yield_units", 0) or 0) > 0:
                    tasks.append((0, target, ["HARVEST"]))
                    continue
                if (
                    int(self.e18_config["rotation_start_day"])
                    <= day
                    <= int(self.e18_config["rotation_end_day"])
                    and crop == str(self.e18_config["early_crop"])
                ):
                    self.rotation_targets.add(target)
                    tasks.append((1, target, ["DIG"]))
                    continue
                if day < 29 and not bool(tile.get("watered_today", False)):
                    tasks.append((2, target, ["WATER"]))
        return tasks

    def _route_tasks(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        *,
        eligible: set[int],
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
            if worker < len(positions) and command and command[0] != "PASS"
        }
        for _priority, target, command in sorted(
            self._crop_tasks(observation),
            key=lambda value: (value[0], value[1][1], value[1][0]),
        ):
            if not free:
                break
            if (target, str(command[0])) in fulfilled:
                continue
            worker = min(
                free,
                key=lambda value: (_distance(positions[value], target), value),
            )
            actions[worker] = (
                list(command)
                if positions[worker] == target
                else self._move_towards(positions[worker], target)
            )
            self.global_crop_commands[str(actions[worker][0])] += 1
            assigned.add(worker)
            free.remove(worker)
            fulfilled.add((target, str(command[0])))
        _store_unit_actions(action, actions)
        return assigned

    @staticmethod
    def _move_towards(
        source: tuple[int, int], target: tuple[int, int]
    ) -> list[str]:
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

    @staticmethod
    def _max_market_orders(configuration: Any) -> int:
        if isinstance(configuration, dict):
            return int(configuration.get("maxMarketOrdersPerTurn", 10) or 10)
        return int(getattr(configuration, "maxMarketOrdersPerTurn", 10) or 10)

    def _backfill_seed_market(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        configuration: Any,
    ) -> None:
        day = int(observation.get("day", 0))
        requests: list[tuple[str, int]] = []
        early = str(self.e18_config["early_crop"])
        rotation = str(self.e18_config["rotation_crop"])
        reclaimed = len(self.reclaimed_crop_targets)
        if reclaimed and day >= int(self.e18_config["reclaimed_crop_activation_day"]):
            requests.append((early, reclaimed))
        if reclaimed and day >= int(self.e18_config["rotation_start_day"]):
            requests.append((rotation, reclaimed))
        market = action.setdefault("market", [])
        max_orders = self._max_market_orders(configuration)
        money = float(_farm(observation).get("money", 0.0) or 0.0)
        floor = float(self.e18_config["seed_operating_cash_floor"])
        for crop, units in requests:
            if crop in self.seed_batches_requested or len(market) >= max_orders:
                continue
            cost = units * float(self.e18_config["seed_unit_costs"][crop])
            if money - cost < floor:
                continue
            market.append(["BUY_SEED", crop, units])
            money -= cost
            self.seed_batches_requested.add(crop)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        self._observe_topology(observation)
        provider = self.base_policy(observation, configuration)
        if self.topology_mode == "7-7-5":
            self.observation_count += 1
            return deepcopy(provider)
        action = deepcopy(provider)
        positions = _positions(_farm(observation))
        provider_actions = _unit_actions(provider, len(positions))
        provider_pass = {
            worker
            for worker, command in enumerate(provider_actions)
            if command == ["PASS"]
        }
        released = self._filter_unit_actions(action, observation)
        self.released_workers_total += len(released)
        self._filter_market(action, observation)
        self._backfill_livestock_market(action, observation, configuration)
        self._backfill_seed_market(action, observation, configuration)

        eligible = set(released)
        eligible.update(
            sorted(provider_pass)[: int(self.e18_config["provider_idle_worker_limit"])]
        )
        fill_workers: set[int] = set()
        if int(observation.get("day", 0)) <= int(
            self.e18_config["fill_purchase_cutoff_day"]
        ):
            before = deepcopy(action)
            fill_workers = self._route_pasture_fill(
                action,
                observation,
                eligible_workers=eligible,
            )
            if action != before:
                self.persistent_fill_batches += 1
        assigned = self._route_tasks(
            action,
            observation,
            eligible=eligible.difference(fill_workers),
        )
        if assigned or fill_workers:
            self.labor_handoff_batches += 1
        final_actions = _unit_actions(action, len(positions))
        self.released_workers_without_work += sum(
            final_actions[worker] == ["PASS"] for worker in released
        )
        self.observation_count += 1
        if action != provider:
            self.override_batches += 1
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "topology_mode": self.topology_mode,
            "target_pastures_by_quadrant": _topology_counts(
                set(self.pasture_targets)
            ),
            "pasture_target_count": len(self.pasture_targets),
            "reclaimed_crop_target_count": len(self.reclaimed_crop_targets),
            "rotation_targets": [
                list(value) for value in sorted(self.rotation_targets)
            ],
            "seed_batches_requested": sorted(self.seed_batches_requested),
            "persistent_fill_batches": self.persistent_fill_batches,
            "labor_handoff_batches": self.labor_handoff_batches,
            "released_workers_total": self.released_workers_total,
            "released_workers_without_work": self.released_workers_without_work,
            "global_crop_commands": dict(self.global_crop_commands),
            "public_features_only": True,
            "cross_episode_memory": False,
        }


def create_codex_e18_labor_conserving_topology(
    *,
    topology_mode: str,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18LaborConservingTopologyAgent(
        topology_mode=topology_mode,
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_labor_conserving_last_error = None
            return action
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_labor_conserving_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_labor_conserving_instance = instance
    policy.codex_e18_labor_conserving_last_error = None
    policy.__name__ = f"codex_e18_3_labor_{topology_mode.replace('-', '')}_policy"
    return policy


__all__ = [
    "DEFAULT_E18_LABOR_CONSERVING_CONFIG_PATH",
    "E18_LABOR_CONSERVING_MODEL_SPEC_VERSION",
    "TOPOLOGY_MODES",
    "CodexE18LaborConservingTopologyAgent",
    "create_codex_e18_labor_conserving_topology",
    "load_e18_labor_conserving_config",
]
