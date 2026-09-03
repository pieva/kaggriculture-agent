"""Opponent-aware E18 topology overlay over the productive E17 6-6-2 agent.

The controller reads only the opponent's public farm.  At a preregistered
checkpoint it freezes one of two fourteen-pasture layouts: 6-6-2 for a
conservative opponent and 7-7-0 for visible expansion/crop pressure.  The
decision is episode-local and does not use names, ratings, replay IDs, seeds,
private inventories, or cross-episode state.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _PASTURE_LIVESTOCK,
    _SAFE_PASS,
    DEFAULT_TOPOLOGY_662_CONFIG_PATH,
    CodexE17TopologyCap662Agent,
    _distance,
    _farm,
    _move,
    _positions,
    _quadrant,
    _store_unit_actions,
    _tile,
    _unit_actions,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH = (
    REPO_ROOT
    / "experiments/e18/configs/codex/"
    / "CODEX_E18_1_OPPONENT_REACTIVE_662_770_V1.json"
)
E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION = (
    "CODEX-E18.1-OPPONENT-REACTIVE-662-770-V1"
)
_TOPOLOGY_MODES = frozenset({"6-6-2", "7-7-0"})


def _public_opponent_farm(observation: dict[str, Any]) -> dict[str, Any]:
    """Return the other seat's public farm without touching private state."""

    player = int(observation.get("player", 0))
    farms = observation.get("farms", []) or []
    opponent = 1 - player
    if 0 <= opponent < len(farms) and isinstance(farms[opponent], dict):
        return farms[opponent]
    return {}


def _positions_from(values: list[list[int]]) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(value) for value in values)


def load_e18_opponent_reactive_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    config_path = (
        Path(path)
        if path is not None
        else DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    expected = {
        "candidate_id": "CODEX_E18_1_OPPONENT_REACTIVE_662_770_V1",
        "model_spec_version": E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION,
        "base_candidate_id": "CODEX_E17_3_TOPOLOGY_FILL_662_V2",
        "causal_family": "PUBLIC_OPPONENT_REGIME_AND_DYNAMIC_TOPOLOGY_CONTROL",
        "mode_below_threshold": "6-6-2",
        "mode_at_or_above_threshold": "7-7-0",
        "public_features_only": True,
        "cross_episode_memory": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"unexpected {key}: {config.get(key)!r}")
    if int(config.get("decision_day", -1)) < 1:
        raise ValueError("decision_day must be positive")
    if int(config.get("dynamic_build_worker_limit", 0)) < 1:
        raise ValueError("dynamic build routing requires at least one worker")
    if int(config.get("livestock_resource_cap", 0)) != 14:
        raise ValueError("E18 must cap livestock resources at fourteen")
    if tuple(config.get("delayed_placement_target", [])) != (2, 4):
        raise ValueError("the service-risk pasture must remain explicit")
    if int(config.get("high_pressure_placement_release_day", -1)) != 28:
        raise ValueError("the high-pressure placement release must remain D28")
    if int(config.get("fill_purchase_cutoff_day", -1)) not in range(12, 30):
        raise ValueError("fill_purchase_cutoff_day must be in the service window")
    weights = config.get("pressure_weights", {}) or {}
    if set(weights) != {
        "extra_quadrants",
        "crops",
        "hands",
        "animals",
        "pastures",
        "weeds",
    }:
        raise ValueError("pressure weights do not match the public feature set")
    topologies = config.get("topologies", {}) or {}
    if set(topologies) != _TOPOLOGY_MODES:
        raise ValueError("both 6-6-2 and 7-7-0 must be configured")
    all_targets: dict[str, frozenset[tuple[int, int]]] = {}
    all_reclaimed: dict[str, frozenset[tuple[int, int]]] = {}
    for mode in sorted(_TOPOLOGY_MODES):
        payload = topologies[mode]
        targets = _positions_from(payload.get("pasture_targets", []))
        reclaimed = _positions_from(payload.get("reclaimed_crop_targets", []))
        counts = Counter(_quadrant(position) for position in targets)
        declared = {
            key: int(value)
            for key, value in payload.get("quadrant_pasture_caps", {}).items()
        }
        if len(targets) != 14 or counts["Q3"]:
            raise ValueError(f"{mode} must define fourteen non-Q3 pastures")
        if declared != {key: counts[key] for key in ("Q0", "Q1", "Q2")}:
            raise ValueError(f"{mode} declared caps do not match its targets")
        if mode != f"{counts['Q0']}-{counts['Q1']}-{counts['Q2']}":
            raise ValueError(f"{mode} name does not match its topology")
        if len(reclaimed) != 5 or targets.intersection(reclaimed):
            raise ValueError(f"{mode} must reclaim five disjoint crop cells")
        all_targets[mode] = targets
        all_reclaimed[mode] = reclaimed
    dynamic = _positions_from(config.get("dynamic_cells", []))
    if dynamic != all_targets["6-6-2"].symmetric_difference(
        all_targets["7-7-0"]
    ):
        raise ValueError("dynamic_cells must be the topology target difference")
    if all_targets["6-6-2"].union(all_reclaimed["6-6-2"]) != (
        all_targets["7-7-0"].union(all_reclaimed["7-7-0"])
    ):
        raise ValueError("the two modes must partition the same V4D cells")
    return deepcopy(config)


def _public_feature_snapshot(farm: dict[str, Any]) -> dict[str, int | float]:
    counts: Counter[str] = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("animal"):
                counts["animals"] += 1
            kind = str(tile.get("kind", ""))
            if kind == "PLANT":
                counts["crops"] += 1
            elif kind == "PASTURE":
                counts["pastures"] += 1
            elif kind == "WEED":
                counts["weeds"] += 1
    return {
        "quadrants": len(farm.get("unlocked_quadrants", []) or []),
        "hands": len(farm.get("hands", []) or []),
        "crops": counts["crops"],
        "animals": counts["animals"],
        "pastures": counts["pastures"],
        "weeds": counts["weeds"],
        "money": float(farm.get("money", 0.0) or 0.0),
    }


class CodexE18OpponentReactiveTopologyAgent(CodexE17TopologyCap662Agent):
    """Freeze a 6-6-2 or 7-7-0 layout from live public opponent pressure."""

    def __init__(
        self,
        *,
        run_context: dict[str, Any] | None = None,
        config_path: Path | str | None = None,
        base_policy=None,
    ) -> None:
        super().__init__(
            run_context=run_context,
            config_path=DEFAULT_TOPOLOGY_662_CONFIG_PATH,
            base_policy=base_policy,
        )
        self.e18_config = load_e18_opponent_reactive_config(config_path)
        self.candidate_id = str(self.e18_config["candidate_id"])
        self.model_spec_version = E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION
        self.config["fill_purchase_cutoff_day"] = int(
            self.e18_config["fill_purchase_cutoff_day"]
        )
        self.livestock_resource_cap = int(
            self.e18_config["livestock_resource_cap"]
        )
        self.config["pre_q2_livestock_resource_cap"] = self.livestock_resource_cap
        self.topology_mode: str | None = None
        self.mode_decision_day: int | None = None
        self.mode_decision_pressure: float | None = None
        self.mode_decision_features: dict[str, int | float] | None = None
        self.mode_decisions = 0
        self.dynamic_build_route_actions = 0
        self.dynamic_build_commands = 0
        self.persistent_fill_batches = 0
        self.delayed_livestock_placements = 0
        self.regime_observations: Counter[str] = Counter()
        self.regime_transitions: list[dict[str, Any]] = []
        self.opponent_feature_hashes: set[str] = set()
        self.last_regime: str | None = None
        self.last_observed_opponent_day: int | None = None
        self.latest_opponent_features: dict[str, int | float] = {}

        common = self._targets("6-6-2").intersection(self._targets("7-7-0"))
        static_reclaimed = self._reclaimed("6-6-2").intersection(
            self._reclaimed("7-7-0")
        )
        self._apply_targets(common, static_reclaimed, q2_cap=0)

    def _targets(self, mode: str) -> frozenset[tuple[int, int]]:
        return _positions_from(
            self.e18_config["topologies"][mode]["pasture_targets"]
        )

    def _reclaimed(self, mode: str) -> frozenset[tuple[int, int]]:
        return _positions_from(
            self.e18_config["topologies"][mode]["reclaimed_crop_targets"]
        )

    def _apply_targets(
        self,
        targets: frozenset[tuple[int, int]],
        reclaimed: frozenset[tuple[int, int]],
        *,
        q2_cap: int,
    ) -> None:
        self.pasture_targets = targets
        self.reclaimed_crop_targets = reclaimed
        counts = Counter(_quadrant(position) for position in targets)
        self.target_pastures_by_quadrant = {
            quadrant: counts[quadrant] for quadrant in ("Q0", "Q1", "Q2")
        }
        self.q2_pasture_cap = q2_cap

    def _pressure(self, features: dict[str, int | float]) -> float:
        weights = self.e18_config["pressure_weights"]
        return (
            max(0, int(features["quadrants"]) - 1)
            * float(weights["extra_quadrants"])
            + int(features["crops"]) * float(weights["crops"])
            + int(features["hands"]) * float(weights["hands"])
            + int(features["animals"]) * float(weights["animals"])
            + int(features["pastures"]) * float(weights["pastures"])
            + int(features["weeds"]) * float(weights["weeds"])
        )

    @staticmethod
    def _regime(features: dict[str, int | float]) -> str:
        if int(features["quadrants"]) >= 3 or int(features["crops"]) >= 20:
            return "EXPANSION_CROP_PRESSURE"
        if (
            int(features["quadrants"]) >= 2
            or int(features["crops"]) >= 8
            or int(features["hands"]) >= 4
        ):
            return "DEVELOPING"
        return "CONSERVATIVE"

    def _observe_public_opponent(self, observation: dict[str, Any]) -> None:
        day = int(observation.get("day", 0))
        if day == self.last_observed_opponent_day:
            return
        features = _public_feature_snapshot(_public_opponent_farm(observation))
        regime = self._regime(features)
        payload = json.dumps(features, sort_keys=True, separators=(",", ":"))
        feature_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
        self.opponent_feature_hashes.add(feature_hash)
        self.regime_observations[regime] += 1
        if regime != self.last_regime:
            self.regime_transitions.append(
                {"day": day, "from": self.last_regime, "to": regime}
            )
            self.last_regime = regime
        self.latest_opponent_features = features
        self.last_observed_opponent_day = day

    def _maybe_decide(self, observation: dict[str, Any]) -> None:
        if self.topology_mode is not None:
            return
        day = int(observation.get("day", 0))
        if day < int(self.e18_config["decision_day"]):
            return
        features = deepcopy(self.latest_opponent_features)
        pressure = self._pressure(features)
        threshold = float(self.e18_config["expansion_pressure_threshold"])
        mode = str(
            self.e18_config[
                "mode_at_or_above_threshold"
                if pressure >= threshold
                else "mode_below_threshold"
            ]
        )
        targets = self._targets(mode)
        reclaimed = self._reclaimed(mode)
        q2_cap = int(
            self.e18_config["topologies"][mode]["quadrant_pasture_caps"]["Q2"]
        )
        self._apply_targets(targets, reclaimed, q2_cap=q2_cap)
        self.topology_mode = mode
        self.mode_decision_day = day
        self.mode_decision_pressure = pressure
        self.mode_decision_features = features
        self.mode_decisions += 1

    def _route_dynamic_pasture_builds(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
        released: set[int],
    ) -> None:
        if self.topology_mode is None:
            return
        farm = _farm(observation)
        positions = _positions(farm)
        actions = _unit_actions(action, len(positions))
        dynamic = _positions_from(self.e18_config["dynamic_cells"])
        missing = [
            target
            for target in sorted(self.pasture_targets.intersection(dynamic))
            if _tile(farm, target) is None
        ]
        if not missing:
            return
        reserved = {
            positions[index]
            for index, command in enumerate(actions)
            if index < len(positions)
            and command
            and command[0] == "BUILD_PASTURE"
            and positions[index] in missing
        }
        free = [
            index
            for index, command in enumerate(actions)
            if index not in released
            and command
            and command[0] == "PASS"
        ]
        free.extend(sorted(released - set(free)))
        limit = int(self.e18_config["dynamic_build_worker_limit"])
        used = 0
        for target in missing:
            if target in reserved or not free or used >= limit:
                continue
            worker_id = min(
                free,
                key=lambda value: (_distance(positions[value], target), value),
            )
            actions[worker_id] = (
                ["BUILD_PASTURE"]
                if positions[worker_id] == target
                else _move(positions[worker_id], target)
            )
            if positions[worker_id] == target:
                self.dynamic_build_commands += 1
            else:
                self.dynamic_build_route_actions += 1
            free.remove(worker_id)
            reserved.add(target)
            used += 1
        _store_unit_actions(action, actions)

    def _filter_unit_actions(
        self,
        action: dict[str, Any],
        observation: dict[str, Any],
    ) -> set[int]:
        released = super()._filter_unit_actions(action, observation)
        target = tuple(self.e18_config["delayed_placement_target"])
        day = int(observation.get("day", 0))
        should_delay = self.topology_mode is None or (
            self.topology_mode == "7-7-0"
            and day
            < int(self.e18_config["high_pressure_placement_release_day"])
        )
        if should_delay:
            positions = _positions(_farm(observation))
            actions = _unit_actions(action, len(positions))
            for worker_id, command in enumerate(actions):
                if (
                    positions[worker_id] == target
                    and command
                    and command[0] == "PLACE"
                    and len(command) >= 2
                    and str(command[1]) in _PASTURE_LIVESTOCK
                ):
                    actions[worker_id] = ["PASS"]
                    released.add(worker_id)
                    self.delayed_livestock_placements += 1
            _store_unit_actions(action, actions)
        self._route_dynamic_pasture_builds(action, observation, released)
        return released

    def _empty_pastures(
        self,
        farm: dict[str, Any],
    ) -> list[tuple[int, int]]:
        empty = super()._empty_pastures(farm)
        target = tuple(self.e18_config["delayed_placement_target"])
        day = self.last_observed_opponent_day or 0
        should_delay = self.topology_mode is None or (
            self.topology_mode == "7-7-0"
            and day
            < int(self.e18_config["high_pressure_placement_release_day"])
        )
        return [position for position in empty if not (should_delay and position == target)]

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        self._observe_public_opponent(observation)
        self._maybe_decide(observation)
        action = super().__call__(observation, configuration)
        day = int(observation.get("day", 0))
        if 12 <= day <= int(self.config["fill_purchase_cutoff_day"]):
            actions = _unit_actions(action, len(_positions(_farm(observation))))
            eligible = {
                worker_id
                for worker_id, command in enumerate(actions)
                if command and command[0] == "PASS"
            }
            if eligible:
                before = deepcopy(action)
                self._route_pasture_fill(
                    action,
                    observation,
                    eligible_workers=eligible,
                )
                if action != before:
                    self.persistent_fill_batches += 1
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        telemetry = super().telemetry_snapshot()
        telemetry.update(
            {
                "agent_version": self.model_spec_version,
                "candidate_id": self.candidate_id,
                "topology_mode": self.topology_mode,
                "mode_decision_day": self.mode_decision_day,
                "mode_decision_pressure": self.mode_decision_pressure,
                "mode_decision_features": deepcopy(self.mode_decision_features),
                "mode_decisions": self.mode_decisions,
                "regime_observations": dict(self.regime_observations),
                "regime_transitions": deepcopy(self.regime_transitions),
                "unique_regimes": len(self.regime_observations),
                "unique_public_opponent_snapshots": len(
                    self.opponent_feature_hashes
                ),
                "latest_opponent_features": deepcopy(
                    self.latest_opponent_features
                ),
                "dynamic_build_route_actions": (
                    self.dynamic_build_route_actions
                ),
                "dynamic_build_commands": self.dynamic_build_commands,
                "persistent_fill_batches": self.persistent_fill_batches,
                "delayed_livestock_placements": (
                    self.delayed_livestock_placements
                ),
                "public_features_only": True,
                "cross_episode_memory": False,
            }
        )
        return telemetry


def create_codex_e18_opponent_reactive_topology(
    run_context: dict[str, Any] | None = None,
    config_path: Path | str | None = None,
    base_policy=None,
):
    """Create the fail-closed E18 public-opponent-reactive candidate."""

    instance = CodexE18OpponentReactiveTopologyAgent(
        run_context=run_context,
        config_path=config_path,
        base_policy=base_policy,
    )

    def policy(
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        try:
            action = instance(observation, configuration)
            policy.codex_e18_opponent_reactive_last_error = None
            return action
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001 - fail closed at episode boundary
            instance.error_count += 1
            instance.fallback_count += 1
            instance.last_exception = f"{type(exc).__name__}: {exc}"
            policy.codex_e18_opponent_reactive_last_error = instance.last_exception
            return deepcopy(_SAFE_PASS)

    policy.codex_e18_opponent_reactive_instance = instance
    policy.codex_e18_opponent_reactive_last_error = None
    policy.__name__ = "codex_e18_1_opponent_reactive_662_770_policy"
    return policy


__all__ = [
    "DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH",
    "E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION",
    "CodexE18OpponentReactiveTopologyAgent",
    "create_codex_e18_opponent_reactive_topology",
    "load_e18_opponent_reactive_config",
]
