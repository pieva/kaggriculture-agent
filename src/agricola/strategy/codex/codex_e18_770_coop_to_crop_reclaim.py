"""E18.14 exact-7-7-0 coop-to-crop reclaim.

The E18.10 V2 provider remains authoritative except for the single Q0 coop
and its Goose.  The build is translated in place to a Strawberry planting,
the Goose purchase is removed, and now-impossible Goose logistics become
PASS.  Provider movement is never changed.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _SAFE_PASS,
    _farm,
    _positions,
    _store_unit_actions,
    _tile,
    _unit_actions,
)
from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    CodexE18770WaterBeforeDigGuardV2Agent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_770_COOP_TO_CROP_RECLAIM_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e18/configs/"
    / "CODEX_E18_14_770_COOP_TO_CROP_RECLAIM_V1.json"
)
E18_770_COOP_TO_CROP_RECLAIM_MODEL_SPEC_VERSION = (
    "CODEX-E18.14-770-COOP-TO-CROP-RECLAIM-V1"
)
_MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})


def load_e18_770_coop_to_crop_reclaim_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_770_COOP_TO_CROP_RECLAIM_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_14_770_COOP_TO_CROP_RECLAIM_V1",
        "model_spec_version": E18_770_COOP_TO_CROP_RECLAIM_MODEL_SPEC_VERSION,
        "base_policy": "CODEX-E18.10-770-WATER-BEFORE-DIG-GUARD-V2",
        "causal_family": "COOP_GOOSE_TO_SINGLE_Q0_CROP",
        "pasture_topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "reclaimed_coop_target": [4, 1],
        "reclaimed_crop": "STRAWBERRY",
        "activation_day": 10,
        "remove_build_coop": True,
        "remove_goose_purchase": True,
        "remove_goose_logistics": True,
        "allow_worker_rerouting": False,
        "provider_move_authoritative": True,
        "worker_count_mutation": False,
        "livestock_cap_mutation": False,
        "public_features_only": True,
        "private_seed_inventory_used_for_local_feasibility_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    return deepcopy(config)


class CodexE18770CoopToCropReclaimAgent(
    CodexE18770WaterBeforeDigGuardV2Agent
):
    """Replace the V9 coop/Goose module with one in-place crop target."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(run_context=run_context, base_policy=base_policy)
        self.e18_14_config = load_e18_770_coop_to_crop_reclaim_config(
            config_path
        )
        self.candidate_id = str(self.e18_14_config["candidate_id"])
        self.model_spec_version = (
            E18_770_COOP_TO_CROP_RECLAIM_MODEL_SPEC_VERSION
        )
        self.reclaimed_coop_target = tuple(
            self.e18_14_config["reclaimed_coop_target"]
        )
        self.reclaimed_crop_targets = frozenset(
            {*self.reclaimed_crop_targets, self.reclaimed_coop_target}
        )
        self.guarded_targets = frozenset(
            {*self.guarded_targets, self.reclaimed_coop_target}
        )
        self.coop_builds_converted_to_crop = 0
        self.goose_market_orders_removed = 0
        self.goose_logistics_suppressed = 0
        self.provider_move_overrides = 0
        self.coop_reclaim_batches = 0

    def _apply_coop_reclaim(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> None:
        if int(observation.get("day", 0)) < int(
            self.e18_14_config["activation_day"]
        ):
            return
        changed = False
        retained_market = []
        for order in action.get("market", []) or []:
            goose_purchase = (
                isinstance(order, list)
                and len(order) >= 3
                and order[:2] == ["BUY_ANIMAL", "GOOSE"]
            )
            if goose_purchase:
                self.goose_market_orders_removed += 1
                changed = True
                continue
            retained_market.append(order)
        action["market"] = retained_market

        farm = _farm(observation)
        positions = _positions(farm)
        actions = _unit_actions(action, len(positions))
        seeds = (observation.get("private", {}) or {}).get("seeds", {}) or {}
        target = self.reclaimed_coop_target
        planted = False
        for worker, command in enumerate(actions):
            if not command or str(command[0]) in _MOVES:
                continue
            opcode = str(command[0])
            on_target = positions[worker] == target
            if (
                opcode == "BUILD_COOP"
                and on_target
                and _tile(farm, target) is None
                and int(
                    seeds.get(str(self.e18_14_config["reclaimed_crop"]), 0)
                    or 0
                )
                > 0
                and not planted
            ):
                actions[worker] = [
                    "PLANT",
                    str(self.e18_14_config["reclaimed_crop"]),
                ]
                planted = True
                self.coop_builds_converted_to_crop += 1
                changed = True
                continue
            goose_logistics = (
                opcode == "PICKUP"
                and len(command) >= 2
                and str(command[1]) == "GOOSE"
            ) or (
                opcode == "PLACE"
                and len(command) >= 2
                and str(command[1]) == "GOOSE"
            )
            if goose_logistics:
                actions[worker] = ["PASS"]
                self.goose_logistics_suppressed += 1
                changed = True
        if changed:
            self.coop_reclaim_batches += 1
            _store_unit_actions(action, actions)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        action = super().__call__(observation, configuration)
        self._apply_coop_reclaim(action, observation)
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        base = super().telemetry_snapshot()
        return {
            **base,
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "treatment": "COOP_GOOSE_TO_SINGLE_Q0_CROP",
            "reclaimed_coop_target": list(self.reclaimed_coop_target),
            "coop_builds_converted_to_crop": (
                self.coop_builds_converted_to_crop
            ),
            "goose_market_orders_removed": self.goose_market_orders_removed,
            "goose_logistics_suppressed": self.goose_logistics_suppressed,
            "provider_move_overrides": self.provider_move_overrides,
            "worker_route_mutations": 0,
            "market_mutation": "REMOVE_GOOSE_PURCHASE_ONLY",
            "worker_count_mutation": False,
            "livestock_cap_mutation": False,
        }


def create_codex_e18_770_coop_to_crop_reclaim(
    *,
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    instance = CodexE18770CoopToCropReclaimAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(observation: dict[str, Any], configuration: Any = None):
        try:
            action = instance(observation, configuration)
            policy.codex_e18_770_coop_to_crop_reclaim_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_770_coop_to_crop_reclaim_last_error = (
                instance.last_exception
            )
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_770_coop_to_crop_reclaim_instance = instance
    policy.codex_e18_770_coop_to_crop_reclaim_last_error = None
    policy.__name__ = "codex_e18_14_770_coop_to_crop_reclaim_policy"
    return policy


__all__ = [
    "DEFAULT_E18_770_COOP_TO_CROP_RECLAIM_CONFIG_PATH",
    "E18_770_COOP_TO_CROP_RECLAIM_MODEL_SPEC_VERSION",
    "CodexE18770CoopToCropReclaimAgent",
    "create_codex_e18_770_coop_to_crop_reclaim",
    "load_e18_770_coop_to_crop_reclaim_config",
]
