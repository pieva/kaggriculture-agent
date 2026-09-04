"""E18.6 concentrated 7-7-0 overlay over the E18.2 control.

The treatment removes only the five V4D pasture targets in Q2.  Provider
routes remain authoritative: commands are translated only when a worker is
already on a removed target, so the failed E18.3 global crop dispatcher is
not reintroduced.  Reclaimed Q2 cells follow a small Strawberry-to-Wheat
lifecycle derived from the current Top-3 discovery benchmark.
"""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.core.state import CROPS
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _PASTURE_LIVESTOCK,
    _SAFE_PASS,
    CodexE17TopologyCap662Agent,
    _farm,
    _inventories,
    _positions,
    _quadrant,
    _tile,
    _unit_actions,
)
from agricola.strategy.codex.codex_e18_capacity_governed_v4d import (
    create_codex_e18_capacity_governed_v4d,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_CONCENTRATED_770_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_6_CONCENTRATED_770_THROUGHPUT_V1.json"
)
E18_CONCENTRATED_770_MODEL_SPEC_VERSION = (
    "CODEX-E18.6-CONCENTRATED-770-THROUGHPUT-V1"
)
_DENSE_775_TARGETS = frozenset(
    {
        (3, 2),
        (4, 2),
        (3, 3),
        (4, 3),
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 2),
        (6, 2),
        (5, 3),
        (6, 3),
        (5, 4),
        (6, 4),
        (7, 4),
        (3, 5),
        (4, 5),
        (3, 6),
        (4, 6),
        (4, 7),
    }
)


def _topology_counts(targets: frozenset[tuple[int, int]]) -> dict[str, int]:
    counts = Counter(_quadrant(target) for target in targets)
    return {quadrant: counts[quadrant] for quadrant in ("Q0", "Q1", "Q2")}


def load_e18_concentrated_770_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_CONCENTRATED_770_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_6_CONCENTRATED_770_THROUGHPUT_V1",
        "model_spec_version": E18_CONCENTRATED_770_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1",
        "causal_family": "Q2_PASTURE_REMOVAL_WITH_IN_PLACE_CROP_TRANSLATION",
        "global_rerouting_enabled": False,
        "public_features_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")

    pasture_targets = frozenset(
        tuple(value) for value in config.get("pasture_targets", [])
    )
    reclaimed = frozenset(
        tuple(value) for value in config.get("reclaimed_q2_crop_targets", [])
    )
    if _topology_counts(pasture_targets) != {"Q0": 7, "Q1": 7, "Q2": 0}:
        raise ValueError("pasture targets must be exactly 7-7-0")
    if pasture_targets | reclaimed != _DENSE_775_TARGETS:
        raise ValueError("7-7-0 targets must partition the V4D 7-7-5 footprint")
    if len(reclaimed) != 5 or any(_quadrant(value) != "Q2" for value in reclaimed):
        raise ValueError("all five and only five reclaimed targets must be in Q2")
    if int(config.get("pasture_fill_target", -1)) != 14:
        raise ValueError("7-7-0 requires fourteen filled pastures")
    if int(config.get("livestock_resource_cap", -1)) != 15:
        raise ValueError("livestock cap must include one in-transit resource")
    if int(config.get("provider_idle_worker_limit", -1)) != 0:
        raise ValueError("V1 forbids global provider-idle rerouting")
    if int(config.get("persistent_fill_worker_limit", -1)) != 1:
        raise ValueError("V1 permits one persistent pasture-fill worker")
    if int(config.get("rotation_start_day", -1)) > int(
        config.get("rotation_end_day", -1)
    ):
        raise ValueError("invalid crop rotation window")
    batches = config.get("seed_batches", {}) or {}
    if set(batches) != {"STRAWBERRY", "WHEAT"}:
        raise ValueError("V1 requires exactly Strawberry and Wheat seed batches")
    if any(crop not in CROPS for crop in batches):
        raise ValueError("unknown crop in seed batches")
    return deepcopy(config)


class CodexE18Concentrated770ThroughputAgent(CodexE17TopologyCap662Agent):
    """Keep E18.2 routes while concentrating livestock in mature quadrants."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        self.e18_770_config = load_e18_concentrated_770_config(config_path)
        provider = (
            base_policy
            if base_policy is not None
            else create_codex_e18_capacity_governed_v4d(
                run_context=run_context
            )
        )
        super().__init__(run_context=run_context, base_policy=provider)
        self.candidate_id = str(self.e18_770_config["candidate_id"])
        self.model_spec_version = E18_CONCENTRATED_770_MODEL_SPEC_VERSION
        self.pasture_targets = frozenset(
            tuple(value) for value in self.e18_770_config["pasture_targets"]
        )
        self.reclaimed_crop_targets = frozenset(
            tuple(value)
            for value in self.e18_770_config["reclaimed_q2_crop_targets"]
        )
        self.target_pastures_by_quadrant = _topology_counts(
            self.pasture_targets
        )
        self.q2_pasture_cap = 0
        self.livestock_resource_cap = int(
            self.e18_770_config["livestock_resource_cap"]
        )
        self.config.update(
            {
                "pre_q2_livestock_resource_cap": int(
                    self.e18_770_config["pre_q2_livestock_resource_cap"]
                ),
                "livestock_resource_cap": self.livestock_resource_cap,
                "pasture_fill_target": int(
                    self.e18_770_config["pasture_fill_target"]
                ),
                "pasture_fill_mission_day": int(
                    self.e18_770_config["pasture_fill_mission_day"]
                ),
                "pasture_fill_mission_worker_limit": int(
                    self.e18_770_config["pasture_fill_mission_worker_limit"]
                ),
                "pasture_fill_quadrant_priority": list(
                    self.e18_770_config["pasture_fill_quadrant_priority"]
                ),
                "pasture_fill_species_priority": list(
                    self.e18_770_config["pasture_fill_species_priority"]
                ),
                "fill_purchase_cutoff_day": int(
                    self.e18_770_config["fill_purchase_cutoff_day"]
                ),
                "fill_operating_cash_floor": float(
                    self.e18_770_config["fill_operating_cash_floor"]
                ),
                "animal_costs": deepcopy(
                    self.e18_770_config["animal_costs"]
                ),
                "reclaimed_crop_activation_day": int(
                    self.e18_770_config["reclaimed_crop_activation_day"]
                ),
            }
        )
        self.seed_batches_requested: set[str] = set()
        self.rotation_dig_commands = 0
        self.phase_crop_commands: Counter[str] = Counter()
        self.persistent_fill_override_batches = 0

    def _desired_crop(self, day: int, seeds: Counter[str]) -> str | None:
        if (
            day <= int(self.e18_770_config["strawberry_cutoff_day"])
            and seeds["STRAWBERRY"] > 0
        ):
            seeds["STRAWBERRY"] -= 1
            return "STRAWBERRY"
        if (
            day <= int(self.e18_770_config["wheat_cutoff_day"])
            and seeds["WHEAT"] > 0
        ):
            seeds["WHEAT"] -= 1
            return "WHEAT"
        return None

    def _reclaimed_crop_tasks(
        self,
        observation: dict[str, Any],
    ) -> list[tuple[int, tuple[int, int], list[Any]]]:
        day = int(observation.get("day", 0))
        if day < int(self.e18_770_config["reclaimed_crop_activation_day"]):
            return []
        farm = _farm(observation)
        seeds = Counter((observation.get("private", {}) or {}).get("seeds", {}))
        tasks: list[tuple[int, tuple[int, int], list[Any]]] = []
        for target in sorted(self.reclaimed_crop_targets, key=lambda p: (p[1], p[0])):
            tile = _tile(farm, target)
            if tile == "LOCKED":
                continue
            if tile is None:
                crop = self._desired_crop(day, seeds)
                if crop is not None:
                    tasks.append((3, target, ["PLANT", crop]))
                continue
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "WEED":
                tasks.append((1, target, ["DIG"]))
                continue
            if tile.get("kind") != "PLANT":
                continue
            crop = str(tile.get("crop", ""))
            mature = day - int(tile.get("planted_day", day)) >= int(
                CROPS.get(crop, {}).get("first_yield_day", 10**6)
            )
            if mature and int(tile.get("yield_units", 0) or 0) > 0:
                tasks.append((0, target, ["HARVEST"]))
            elif (
                int(self.e18_770_config["rotation_start_day"])
                <= day
                <= int(self.e18_770_config["rotation_end_day"])
                and crop == "STRAWBERRY"
            ):
                tasks.append((1, target, ["DIG"]))
            elif day < int(self.e18_770_config["terminal_passthrough_day"]) and not bool(
                tile.get("watered_today", False)
            ):
                tasks.append((2, target, ["WATER"]))
        return tasks

    def _backfill_reclaimed_seed_market(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        configuration: Any,
    ) -> None:
        day = int(observation.get("day", 0))
        batches = self.e18_770_config["seed_batches"]
        market = action.setdefault("market", [])
        max_orders = (
            int(configuration.get("maxMarketOrdersPerTurn", 10))
            if isinstance(configuration, dict)
            else int(getattr(configuration, "maxMarketOrdersPerTurn", 10) or 10)
        )
        money = float(_farm(observation).get("money", 0.0) or 0.0)
        floor = float(self.e18_770_config["seed_operating_cash_floor"])
        for crop in ("STRAWBERRY", "WHEAT"):
            batch = batches[crop]
            if crop in self.seed_batches_requested or day < int(batch["day"]):
                continue
            if len(market) >= max_orders:
                break
            units = int(batch["units"])
            cost = units * float(batch["unit_cost"])
            if money - cost < floor:
                continue
            market.append(["BUY_SEED", crop, units])
            money -= cost
            self.seed_batches_requested.add(crop)
            self.reclaimed_seed_backfill_requested = True
            self.reclaimed_seed_backfill_units += units

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        before_rotation = self.reclaimed_crop_actions["DIG"]
        action = super().__call__(observation, configuration)
        day = int(observation.get("day", 0))
        if day <= int(self.e18_770_config["fill_purchase_cutoff_day"]):
            positions = _positions(_farm(observation))
            pass_workers = [
                worker
                for worker, command in enumerate(
                    _unit_actions(action, len(positions))
                )
                if command == ["PASS"]
            ]
            eligible = set(
                pass_workers[
                    : int(self.e18_770_config["persistent_fill_worker_limit"])
                ]
            )
            built_targets = sum(
                isinstance((tile := _tile(_farm(observation), target)), dict)
                and tile.get("kind") == "PASTURE"
                for target in self.pasture_targets
            )
            if built_targets == len(self.pasture_targets):
                inventories = _inventories(
                    observation.get("private", {}) or {}, len(positions)
                )
                eligible.update(
                    worker
                    for worker, inventory in enumerate(inventories)
                    if any(
                        int(inventory.get(species, 0) or 0) > 0
                        for species in _PASTURE_LIVESTOCK
                    )
                )
            before_fill = deepcopy(action)
            self._route_pasture_fill(
                action,
                observation,
                eligible_workers=eligible,
            )
            if action != before_fill:
                self.persistent_fill_override_batches += 1
        self.rotation_dig_commands += max(
            0, self.reclaimed_crop_actions["DIG"] - before_rotation
        )
        for opcode in ("PLANT", "WATER", "HARVEST", "DIG"):
            self.phase_crop_commands[opcode] = self.reclaimed_crop_actions[opcode]
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        provider = getattr(
            self.base_policy,
            "codex_e18_capacity_governed_instance",
            None,
        )
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "topology_mode": "7-7-0",
            "target_pastures_by_quadrant": self.target_pastures_by_quadrant,
            "pasture_target_count": len(self.pasture_targets),
            "reclaimed_q2_crop_targets": [
                list(value) for value in sorted(self.reclaimed_crop_targets)
            ],
            "seed_batches_requested": sorted(self.seed_batches_requested),
            "rotation_dig_commands": self.rotation_dig_commands,
            "phase_crop_commands": dict(self.phase_crop_commands),
            "persistent_fill_override_batches": (
                self.persistent_fill_override_batches
            ),
            "global_rerouting_enabled": False,
            "provider": provider.telemetry_snapshot() if provider else {},
        }


def create_codex_e18_concentrated_770_throughput(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18Concentrated770ThroughputAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_concentrated_770_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_concentrated_770_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_concentrated_770_instance = instance
    policy.codex_e18_concentrated_770_last_error = None
    policy.__name__ = "codex_e18_6_concentrated_770_throughput_policy"
    return policy


__all__ = [
    "DEFAULT_E18_CONCENTRATED_770_CONFIG_PATH",
    "E18_CONCENTRATED_770_MODEL_SPEC_VERSION",
    "CodexE18Concentrated770ThroughputAgent",
    "create_codex_e18_concentrated_770_throughput",
    "load_e18_concentrated_770_config",
]
