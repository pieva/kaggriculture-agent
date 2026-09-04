"""Copilot E18 adaptive-crop opponent-reactive candidate.

The controller keeps the Native Copilot line independent and deterministic but
adds a real public-opponent snapshot, hysteretic regime selection, crop
lifecycle management, and a dynamic crop footprint / workforce budget.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "COPILOT-E18.1-OPPONENT-REACTIVE-V1"
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "docs" / "model_specs" / "copilot" / "e18" / "configs"
    / "COPILOT_E18_1_OPPONENT_REACTIVE_V1.json"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
FAMILY_NAME = "ADAPTIVE_CROP"
CROP_ORDER = ("WHEAT", "CARROT", "STRAWBERRY", "TOMATO", "MELON")


@dataclass(frozen=True)
class CopilotE18OpponentReactiveConfig:
    candidate_id: str
    schema_version: str
    model_spec_version: str
    family: str
    primary_crop: str
    secondary_crops: tuple[str, ...]
    snapshot_day_start: int
    snapshot_day_end: int
    pressure_low_threshold: int
    pressure_high_threshold: int
    hysteresis_band: int
    balanced_worker_target: int
    expansion_worker_target: int
    max_lifespan_step: int
    weed_exit_threshold: int
    seed_reorder_threshold: int
    max_market_orders_per_turn: int
    turns_per_day: int
    episode_steps: int

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "CopilotE18OpponentReactiveConfig":
        config = cls(
            candidate_id=str(payload["candidate_id"]),
            schema_version=str(payload["schema_version"]),
            model_spec_version=str(payload["model_spec_version"]),
            family=str(payload.get("family", FAMILY_NAME)),
            primary_crop=str(payload.get("primary_crop", "WHEAT")).upper(),
            secondary_crops=tuple(
                str(item).upper() for item in payload.get("secondary_crops", ("CARROT",))
            ),
            snapshot_day_start=int(payload.get("snapshot_day_start", 4)),
            snapshot_day_end=int(payload.get("snapshot_day_end", 8)),
            pressure_low_threshold=int(payload.get("pressure_low_threshold", 18)),
            pressure_high_threshold=int(payload.get("pressure_high_threshold", 28)),
            hysteresis_band=int(payload.get("hysteresis_band", 2)),
            balanced_worker_target=int(payload.get("balanced_worker_target", 2)),
            expansion_worker_target=int(payload.get("expansion_worker_target", 3)),
            max_lifespan_step=int(payload.get("max_lifespan_step", 18)),
            weed_exit_threshold=int(payload.get("weed_exit_threshold", 12)),
            seed_reorder_threshold=int(payload.get("seed_reorder_threshold", 8)),
            max_market_orders_per_turn=int(payload.get("max_market_orders_per_turn", 8)),
            turns_per_day=int(payload.get("turns_per_day", 24)),
            episode_steps=int(payload.get("episode_steps", 720)),
        )
        if config.candidate_id != "COPILOT_E18_1_OPPONENT_REACTIVE_V1":
            raise ValueError("unexpected candidate_id")
        if config.model_spec_version != POLICY_VERSION:
            raise ValueError("unexpected model_spec_version")
        if config.family != FAMILY_NAME:
            raise ValueError("unexpected family")
        if config.primary_crop not in CROP_ORDER:
            raise ValueError("unsupported primary crop")
        if config.snapshot_day_start > config.snapshot_day_end:
            raise ValueError("snapshot window is inverted")
        if config.pressure_low_threshold >= config.pressure_high_threshold:
            raise ValueError("pressure thresholds are inconsistent")
        return config


def load_copilot_e18_opponent_reactive_v1_config(
    path: Path | str | None = None,
) -> CopilotE18OpponentReactiveConfig:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return CopilotE18OpponentReactiveConfig.from_mapping(payload)


def _safe_tile_count(farm: dict[str, Any], kind: str) -> int:
    tiles = farm.get("tiles", []) or []
    return sum(
        1
        for row in tiles
        for tile in row
        if isinstance(tile, dict) and str(tile.get("kind", "")).upper() == kind
    )


def _public_opponent_snapshot(observation: dict[str, Any], player: int | None = None) -> dict[str, Any]:
    if not isinstance(observation, dict):
        return {"opponent_index": -1, "regime_signal": "BALANCED", "public_features": {}}
    farms = observation.get("farms", []) or []
    if not farms:
        return {"opponent_index": -1, "regime_signal": "BALANCED", "public_features": {}}
    player_id = int(observation.get("player", player if player is not None else 0))
    opponent_index = 1 - player_id if len(farms) > 1 else 0
    if not 0 <= opponent_index < len(farms):
        opponent_index = 0
    opponent = farms[opponent_index] if isinstance(farms[opponent_index], dict) else {}
    tiles = opponent.get("tiles", []) or []
    hands = opponent.get("hands", []) or []
    crop_tiles = sum(
        1
        for row in tiles
        for tile in row
        if isinstance(tile, dict) and tile.get("kind") == "PLANT"
    )
    weed_tiles = _safe_tile_count(opponent, "WEED")
    animal_tiles = sum(
        1
        for row in tiles
        for tile in row
        if isinstance(tile, dict) and tile.get("animal") is not None
    )
    pasture_tiles = _safe_tile_count(opponent, "PASTURE") + _safe_tile_count(opponent, "COOP")
    return {
        "opponent_index": opponent_index,
        "quadrants": tuple(opponent.get("unlocked_quadrants", []) or []),
        "visible_workers": 1 + len(hands),
        "hands_visible": len(hands),
        "crop_tiles": crop_tiles,
        "weed_tiles": weed_tiles,
        "animal_tiles": animal_tiles,
        "pasture_tiles": pasture_tiles,
        "farm_money": float(opponent.get("money", 0.0) or 0.0),
        "pressure_score": (
            crop_tiles * 3
            + weed_tiles * 4
            + len(hands) * 2
            + animal_tiles * 2
            + pasture_tiles
        ),
    }


class CopilotE18OpponentReactiveV1Policy:
    """Adaptive-crop policy that reacts to the opponent's public state."""

    def __init__(
        self,
        config: CopilotE18OpponentReactiveConfig | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        self.config = config or load_copilot_e18_opponent_reactive_v1_config()
        self.run_context = deepcopy(run_context or {})
        self.candidate_id = self.config.candidate_id
        self.model_spec_version = self.config.model_spec_version
        self.technical_errors = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.last_regime = "BALANCED"
        self.regime_history: list[str] = []
        self.regime_transitions = 0
        self.lifecycle_metrics = {
            "starved_to_weed": 0,
            "expired_to_weed": 0,
            "weed_exit": 0,
            "mean_peak_weed": 0.0,
            "harvested_units": 0,
            "yield_per_harvest": 0.0,
            "tile_days_alive": 0,
            "backlog": 0,
            "idle_workers": 0,
        }

    def _regime_classifier(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        score = int(snapshot.get("pressure_score", 0))
        weeds = int(snapshot.get("weed_tiles", 0))
        hands = int(snapshot.get("hands_visible", 0))
        crops = int(snapshot.get("crop_tiles", 0))
        animals = int(snapshot.get("animal_tiles", 0))
        features = {
            "pressure_score": score,
            "weed_tiles": weeds,
            "hands_visible": hands,
            "crop_tiles": crops,
            "animal_tiles": animals,
        }
        low_threshold = self.config.pressure_low_threshold
        high_threshold = self.config.pressure_high_threshold
        if score >= high_threshold or weeds >= 6 or hands >= 4:
            regime = "EXPANSION"
        elif score <= low_threshold:
            regime = "BALANCED"
        else:
            regime = self.last_regime
        confidence = 0.5 + min(0.5, abs(score - low_threshold) / max(1, high_threshold - low_threshold))
        return {"regime": regime, "confidence": float(confidence), "features": features}

    def _hysteretic_selector(self, classification: dict[str, Any]) -> str:
        candidate = classification["regime"]
        current = self.last_regime
        if candidate == current:
            return candidate
        transition_band = self.config.hysteresis_band
        score = int(classification["features"]["pressure_score"])
        if current == "BALANCED":
            if score >= self.config.pressure_high_threshold + transition_band:
                self.regime_transitions += 1
                self.last_regime = "EXPANSION"
                self.regime_history.append("EXPANSION")
                return "EXPANSION"
            return current
        if score <= self.config.pressure_low_threshold - transition_band:
            self.regime_transitions += 1
            self.last_regime = "BALANCED"
            self.regime_history.append("BALANCED")
            return "BALANCED"
        self.last_regime = current
        self.regime_history.append(current)
        return current

    def _footprint_planner(self, regime: str) -> dict[str, Any]:
        if regime == "EXPANSION":
            return {
                "mode": "EXPANSION",
                "quadrants": ("NW", "NE", "SW"),
                "worker_target": self.config.expansion_worker_target,
                "crop_mix": (self.config.primary_crop, *self.config.secondary_crops),
                "planting_bias": "aggressive",
            }
        return {
            "mode": "BALANCED",
            "quadrants": ("NW", "NE"),
            "worker_target": self.config.balanced_worker_target,
            "crop_mix": (self.config.primary_crop, self.config.secondary_crops[0] if self.config.secondary_crops else self.config.primary_crop),
            "planting_bias": "consolidated",
        }

    def _tile_is_target(self, tile: Any, quadrant: str, board_size: int, x: int, y: int) -> bool:
        half = board_size // 2
        quadrant_map = {
            "NW": (x < half and y < half),
            "NE": (x >= half and y < half),
            "SW": (x < half and y >= half),
            "SE": (x >= half and y >= half),
        }
        return quadrant_map.get(quadrant, False)

    def _lifecycle_state(self, tile: Any, day: int) -> str:
        if tile is None:
            return "REPLANT"
        if not isinstance(tile, dict):
            return "KEEP"
        kind = str(tile.get("kind", "")).upper()
        if kind == "WEED":
            return "DIG"
        if kind != "PLANT":
            return "KEEP"
        crop = str(tile.get("crop", self.config.primary_crop)).upper()
        planted_day = int(tile.get("planted_day", day))
        age = max(0, day - planted_day)
        yield_units = int(tile.get("yield_units", 0) or 0)
        first_yield = {"WHEAT": 2, "CARROT": 2, "TOMATO": 8, "STRAWBERRY": 10, "MELON": 10}.get(crop, 6)
        if yield_units > 0 and (age >= max(first_yield, self.config.max_lifespan_step // 2) or day >= 28):
            return "HARVEST"
        if age > self.config.max_lifespan_step and yield_units == 0:
            return "DIG"
        if not bool(tile.get("watered_today", False)) and age < first_yield + 1:
            return "KEEP"
        return "KEEP"

    def _public_snapshot_to_regime(self, observation: dict[str, Any]) -> dict[str, Any]:
        snapshot = _public_opponent_snapshot(observation, int(observation.get("player", 0)))
        classification = self._regime_classifier(snapshot)
        regime = self._hysteretic_selector(classification)
        return {"snapshot": snapshot, "classification": classification, "regime": regime}

    def _task_generation(self, farm: dict[str, Any], regime: str, day: int) -> list[tuple[int, tuple[int, int], str, str]]:
        tasks: list[tuple[int, tuple[int, int], str, str]] = []
        tiles = farm.get("tiles", []) or []
        plan = self._footprint_planner(regime)
        board_size = max(10, len(tiles) or 10)
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if not plan["mode"]:
                    continue
                if not self._tile_is_target(tile, "NW", board_size, x, y) and not self._tile_is_target(tile, "NE", board_size, x, y):
                    if plan["mode"] == "EXPANSION" and not self._tile_is_target(tile, "SW", board_size, x, y):
                        continue
                state = self._lifecycle_state(tile, day)
                if state == "HARVEST":
                    tasks.append((0, (x, y), "HARVEST", "HARVEST"))
                elif state == "DIG":
                    tasks.append((2, (x, y), "DIG", "DIG"))
                elif state == "REPLANT":
                    if day >= 2:
                        tasks.append((3, (x, y), "PLANT", self.config.primary_crop))
        return tasks

    def _worker_allocation(
        self,
        farm: dict[str, Any],
        tasks: list[tuple[int, tuple[int, int], str, str]],
        regime: str,
    ) -> list[list[str]]:
        positions = [tuple(farm.get("farmer", [4, 4]))]
        positions.extend(tuple(position) for position in farm.get("hands", []) or [])
        actions: list[list[str]] = [["PASS"] for _ in positions]
        if not tasks:
            return actions
        ranked = sorted(tasks, key=lambda item: (item[0], item[1][1], item[1][0]))
        target_workers = max(1, min(len(positions), self.config.balanced_worker_target if regime == "BALANCED" else self.config.expansion_worker_target))
        assignment_count = 0
        for _, target, verb, crop in ranked:
            if assignment_count >= target_workers:
                break
            for worker_id, position in enumerate(positions):
                if assignment_count >= target_workers:
                    break
                if position == target:
                    continue
                actions[worker_id] = []
                actions[worker_id].extend(self._move_toward(position, target))
                if position == target:
                    actions[worker_id] = [verb] if verb != "PLANT" else ["PLANT", crop]
                else:
                    actions[worker_id] = self._move_toward(position, target)
                assignment_count += 1
                break
        return actions

    def _move_toward(self, source: tuple[int, int], target: tuple[int, int]) -> list[str]:
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

    def _market_orders(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        regime: str,
        seed_count: int,
    ) -> list[list[Any]]:
        money = float(farm.get("money", 0.0) or 0.0)
        if money < 600:
            return []
        seeds = (private.get("seeds", {}) or {})
        primary_seed = int(seeds.get(self.config.primary_crop, 0) or 0)
        if primary_seed > self.config.seed_reorder_threshold:
            return []
        if regime == "BALANCED":
            quantity = 8
        else:
            quantity = 12
        return [["BUY_SEED", self.config.primary_crop, quantity]]

    def _action_arbiter(
        self,
        observation: dict[str, Any],
        regime: str,
        farm: dict[str, Any],
        private: dict[str, Any],
        tasks: list[tuple[int, tuple[int, int], str, str]],
    ) -> dict[str, Any]:
        action = {"farmer": ["PASS"], "hands": [], "market": []}
        positions = [tuple(farm.get("farmer", [4, 4]))]
        positions.extend(tuple(position) for position in farm.get("hands", []) or [])
        unit_actions = self._worker_allocation(farm, tasks, regime)
        action["farmer"] = unit_actions[0] if unit_actions else ["PASS"]
        action["hands"] = [
            unit_actions[index]
            for index in range(1, min(len(unit_actions), len(positions)))
        ]
        action["market"] = self._market_orders(
            farm,
            private,
            regime,
            int((private.get("seeds", {}) or {}).get(self.config.primary_crop, 0)),
        )
        return action

    def telemetry_snapshot(self) -> dict[str, Any]:
        return {
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "family": FAMILY_NAME,
            "current_regime": self.last_regime,
            "regime_history": list(self.regime_history),
            "transition_count": self.regime_transitions,
            "technical_errors": self.technical_errors,
            "fallbacks": self.fallback_count,
            "last_exception": self.last_exception,
            **self.lifecycle_metrics,
        }

    def __call__(self, observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        try:
            snapshot = CodexObservationAdapter.parse(
                observation,
                configuration,
                fallback_turns_per_day=self.config.turns_per_day,
                fallback_episode_steps=self.config.episode_steps,
            )
            public = self._public_snapshot_to_regime(observation)
            regime = public["regime"]
            farm = snapshot.farm
            private = snapshot.private
            tasks = self._task_generation(farm, regime, snapshot.clock.day)
            action = self._action_arbiter(observation, regime, farm, private, tasks)
            self.lifecycle_metrics["backlog"] = len(tasks)
            self.lifecycle_metrics["idle_workers"] = max(0, len(farm.get("hands", []) or []) + 1 - len(tasks))
            self.last_regime = regime
            if not self.regime_history or self.regime_history[-1] != regime:
                self.regime_history.append(regime)
                self.regime_transitions += 1 if self.regime_history and len(self.regime_history) > 1 else 0
            return action
        except Exception as exc:  # noqa: BLE001 - explicit failure path
            self.technical_errors += 1
            self.fallback_count += 1
            self.last_exception = f"{type(exc).__name__}: {exc}"
            return deepcopy(SAFE_PASS)


def create_copilot_e18_opponent_reactive_v1(
    *,
    config_path: Path | str | None = None,
    run_context: dict[str, Any] | None = None,
) -> CopilotE18OpponentReactiveV1Policy:
    config = load_copilot_e18_opponent_reactive_v1_config(config_path)
    return CopilotE18OpponentReactiveV1Policy(config=config, run_context=run_context)


def create_agent(
    *,
    config_path: Path | str | None = None,
    run_context: dict[str, Any] | None = None,
) -> CopilotE18OpponentReactiveV1Policy:
    return create_copilot_e18_opponent_reactive_v1(config_path=config_path, run_context=run_context)


__all__ = [
    "DEFAULT_CONFIG_PATH",
    "FAMILY_NAME",
    "POLICY_VERSION",
    "CopilotE18OpponentReactiveConfig",
    "CopilotE18OpponentReactiveV1Policy",
    "create_agent",
    "create_copilot_e18_opponent_reactive_v1",
    "load_copilot_e18_opponent_reactive_v1_config",
]
