"""Copilot E18 opponent-reactive V2.

This controller keeps the Copilot E18 family independent and deterministic while
adding a real public-opponent snapshot, sticky regime selection, and a working
crop servicing loop that can produce a full harvest-to-sell economic chain.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agricola.core.observation_contract import CodexObservationAdapter

POLICY_VERSION = "COPILOT-E18.2-OPPONENT-REACTIVE-V2"
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "experiments"
    / "e18"
    / "configs"
    / "copilot"
    / "COPILOT_E18_2_OPPONENT_REACTIVE_V2.json"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
FAMILY_NAME = "ADAPTIVE_CROP"
CROP_YIELD_DAYS = {
    "WHEAT": 2,
    "CARROT": 2,
    "TOMATO": 8,
    "STRAWBERRY": 10,
    "MELON": 10,
}


@dataclass(frozen=True)
class CopilotE18OpponentReactiveV2Config:
    candidate_id: str
    schema_version: str
    model_spec_version: str
    family: str
    primary_crop: str
    secondary_crops: tuple[str, ...]
    snapshot_day_start: int
    snapshot_day_end: int
    balanced_pressure_threshold: int
    expansion_pressure_threshold: int
    balanced_worker_target: int
    expansion_worker_target: int
    balanced_crop_target: int
    expansion_crop_target: int
    service_worker_reserve: int
    seed_reorder_level: int
    market_sell_threshold: int
    turns_per_day: int
    episode_steps: int

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> CopilotE18OpponentReactiveV2Config:
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
            balanced_pressure_threshold=int(payload.get("balanced_pressure_threshold", 18)),
            expansion_pressure_threshold=int(payload.get("expansion_pressure_threshold", 30)),
            balanced_worker_target=int(payload.get("balanced_worker_target", 2)),
            expansion_worker_target=int(payload.get("expansion_worker_target", 3)),
            balanced_crop_target=int(payload.get("balanced_crop_target", 10)),
            expansion_crop_target=int(payload.get("expansion_crop_target", 16)),
            service_worker_reserve=int(payload.get("service_worker_reserve", 1)),
            seed_reorder_level=int(payload.get("seed_reorder_level", 6)),
            market_sell_threshold=int(payload.get("market_sell_threshold", 180)),
            turns_per_day=int(payload.get("turns_per_day", 24)),
            episode_steps=int(payload.get("episode_steps", 720)),
        )
        if config.candidate_id != "COPILOT_E18_2_OPPONENT_REACTIVE_V2":
            raise ValueError("unexpected candidate_id")
        if config.model_spec_version != POLICY_VERSION:
            raise ValueError("unexpected model_spec_version")
        if config.family != FAMILY_NAME:
            raise ValueError("unexpected family")
        if config.primary_crop not in CROP_YIELD_DAYS:
            raise ValueError("unsupported primary crop")
        if config.snapshot_day_start > config.snapshot_day_end:
            raise ValueError("snapshot window is inverted")
        if config.balanced_pressure_threshold >= config.expansion_pressure_threshold:
            raise ValueError("pressure thresholds are inconsistent")
        if config.balanced_worker_target <= 0 or config.expansion_worker_target <= 0:
            raise ValueError("worker targets must be positive")
        return config


def load_copilot_e18_opponent_reactive_v2_config(
    path: Path | str | None = None,
) -> CopilotE18OpponentReactiveV2Config:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return CopilotE18OpponentReactiveV2Config.from_mapping(payload)


def _public_opponent_snapshot(observation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(observation, dict):
        return {
            "opponent_index": -1,
            "hands_visible": 0,
            "crop_tiles": 0,
            "weed_tiles": 0,
            "animal_tiles": 0,
            "pasture_tiles": 0,
            "farm_money": 0.0,
            "pressure_score": 0,
            "quadrants": (),
        }
    farms = observation.get("farms", []) or []
    if not farms:
        return {
            "opponent_index": -1,
            "hands_visible": 0,
            "crop_tiles": 0,
            "weed_tiles": 0,
            "animal_tiles": 0,
            "pasture_tiles": 0,
            "farm_money": 0.0,
            "pressure_score": 0,
            "quadrants": (),
        }
    player_index = int(observation.get("player", 0))
    opponent_index = 1 - player_index if len(farms) > 1 else 0
    opponent = farms[opponent_index] if isinstance(farms[opponent_index], dict) else {}
    tiles = opponent.get("tiles", []) or []
    hands = opponent.get("hands", []) or []
    crop_tiles = sum(
        1
        for row in tiles
        for tile in row
        if isinstance(tile, dict) and str(tile.get("kind", "")).upper() == "PLANT"
    )
    weed_tiles = sum(
        1
        for row in tiles
        for tile in row
        if isinstance(tile, dict) and str(tile.get("kind", "")).upper() == "WEED"
    )
    animal_tiles = sum(
        1
        for row in tiles
        for tile in row
        if isinstance(tile, dict) and tile.get("animal") is not None
    )
    pasture_tiles = sum(
        1
        for row in tiles
        for tile in row
        if isinstance(tile, dict)
        and str(tile.get("kind", "")).upper() in {"PASTURE", "COOP"}
    )
    pressure_score = (
        crop_tiles * 4 + weed_tiles * 5 + len(hands) * 3 + animal_tiles * 2 + pasture_tiles
    )
    return {
        "opponent_index": opponent_index,
        "hands_visible": len(hands),
        "crop_tiles": crop_tiles,
        "weed_tiles": weed_tiles,
        "animal_tiles": animal_tiles,
        "pasture_tiles": pasture_tiles,
        "farm_money": float(opponent.get("money", 0.0) or 0.0),
        "pressure_score": pressure_score,
        "quadrants": tuple(opponent.get("unlocked_quadrants", []) or ()),
    }


class CopilotE18OpponentReactiveV2Policy:
    """Sticky public-opponent controller that maintains a working production loop."""

    def __init__(
        self,
        config: CopilotE18OpponentReactiveV2Config | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        self.config = config or load_copilot_e18_opponent_reactive_v2_config()
        self.run_context = deepcopy(run_context or {})
        self.candidate_id = self.config.candidate_id
        self.model_spec_version = self.config.model_spec_version
        self.technical_errors = 0
        self.fallback_count = 0
        self.last_exception: str | None = None
        self.last_regime = "BALANCED"
        self.regime_history: list[str] = []
        self.regime_decision_day: int | None = None
        self.regime_decision_pressure: int | None = None
        self.regime_decision_features: dict[str, Any] | None = None
        self.lifecycle_metrics = {
            "backlog": 0,
            "productive_actions": 0,
            "terminal_backlog": 0,
            "crop_peak": 0,
            "hands_peak": 0,
            "money_peak": 0.0,
            "inventory_sold": 0,
        }

    def _calculate_regime(self, snapshot: dict[str, Any]) -> str:
        score = int(snapshot.get("pressure_score", 0))
        weeds = int(snapshot.get("weed_tiles", 0))
        hands = int(snapshot.get("hands_visible", 0))
        value = score + weeds * 2 + hands * 4
        if value >= self.config.expansion_pressure_threshold:
            return "EXPANSION"
        if value <= self.config.balanced_pressure_threshold and weeds <= 3:
            return "BALANCED"
        return self.last_regime if self.last_regime in {"BALANCED", "EXPANSION"} else "BALANCED"

    def _decide_regime(self, observation: dict[str, Any], day: int) -> tuple[str, dict[str, Any]]:
        snapshot = _public_opponent_snapshot(observation)
        if self.regime_decision_day is None and self.config.snapshot_day_start <= day <= self.config.snapshot_day_end:
            regime = self._calculate_regime(snapshot)
            self.regime_decision_day = day
            self.regime_decision_pressure = int(snapshot.get("pressure_score", 0))
            self.regime_decision_features = snapshot
            self.last_regime = regime
            self.regime_history.append(regime)
            return regime, snapshot
        if self.regime_decision_day is not None:
            return self.last_regime, snapshot
        return self.last_regime, snapshot

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

    def _tile_lifecycle(self, tile: Any, day: int) -> tuple[str, str | None]:
        if tile is None:
            return "REPLANT", self.config.primary_crop
        if not isinstance(tile, dict):
            return "KEEP", None
        kind = str(tile.get("kind", "")).upper()
        if kind == "WEED":
            return "DIG", "DIG"
        if kind != "PLANT":
            return "KEEP", None
        crop = str(tile.get("crop", self.config.primary_crop)).upper()
        planted_day = int(tile.get("planted_day", day))
        age = max(0, day - planted_day)
        yield_units = int(tile.get("yield_units", 0) or 0)
        water_needed = not bool(tile.get("watered_today", False))
        if yield_units > 0 and age >= max(2, CROP_YIELD_DAYS.get(crop, 2)):
            return "HARVEST", crop
        if water_needed and age <= max(2, CROP_YIELD_DAYS.get(crop, 2)) + 1:
            return "WATER", "WATER"
        if age > 18 and yield_units == 0:
            return "DIG", "DIG"
        return "REPLANT", self.config.primary_crop

    def _task_scan(self, farm: dict[str, Any], day: int, regime: str) -> list[tuple[int, tuple[int, int], str, str]]:
        tasks: list[tuple[int, tuple[int, int], str, str]] = []
        tiles = farm.get("tiles", []) or []
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                action_key, action_value = self._tile_lifecycle(tile, day)
                if action_key == "HARVEST":
                    tasks.append((0, (x, y), "HARVEST", str(action_value or self.config.primary_crop)))
                elif action_key == "DIG":
                    tasks.append((1, (x, y), "DIG", "DIG"))
                elif action_key == "WATER":
                    tasks.append((2, (x, y), "WATER", "WATER"))
                elif action_key == "REPLANT":
                    crop = str(action_value or self.config.primary_crop).upper()
                    if day >= 1:
                        tasks.append((3, (x, y), "PLANT", crop))
        if regime == "EXPANSION":
            tasks.sort(key=lambda item: (item[0], item[1][1], item[1][0]))
        else:
            tasks.sort(key=lambda item: (item[0], item[1][1], item[1][0]))
        return tasks

    def _worker_allocation(
        self,
        farm: dict[str, Any],
        tasks: list[tuple[int, tuple[int, int], str, str]],
        regime: str,
    ) -> list[list[str]]:
        positions = [tuple(farm.get("farmer", [4, 4]))]
        positions.extend(tuple(item) for item in farm.get("hands", []) or [])
        worker_target = (
            self.config.expansion_worker_target
            if regime == "EXPANSION"
            else self.config.balanced_worker_target
        )
        worker_target = min(worker_target, max(1, len(positions)))
        actions: list[list[str]] = [["PASS"] for _ in positions]
        if not tasks:
            return actions
        used = 0
        for _, target, verb, crop in sorted(tasks, key=lambda item: (item[0], item[1][1], item[1][0])):
            if used >= worker_target:
                break
            action = [verb]
            if verb == "PLANT":
                action = ["PLANT", crop]
            elif verb == "WATER":
                action = ["WATER"]
            elif verb == "DIG":
                action = ["DIG"]
            elif verb == "HARVEST":
                action = ["HARVEST"]
            for index, position in enumerate(positions):
                if index != used:
                    continue
                if position != target:
                    actions[index] = self._move_toward(position, target)
                    if actions[index] == ["PASS"] and position == target:
                        actions[index] = action
                else:
                    actions[index] = action
                used += 1
                break
        return actions

    def _market_orders(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        regime: str,
    ) -> list[list[Any]]:
        money = float(farm.get("money", 0.0) or 0.0)
        market: list[list[Any]] = []
        inventory = private.get("inventory", {}) or private.get("products", {}) or {}
        for product, quantity in sorted(
            inventory.items(),
            key=lambda item: (item[0] != self.config.primary_crop, str(item[0])),
        ):
            if str(product).upper() in {"WHEAT", "CARROT", "STRAWBERRY", "TOMATO", "MELON"}:
                qty = int(quantity or 0)
                if qty > 0:
                    market.append(["SELL", str(product).upper(), max(1, qty)])
                    break
        seeds = private.get("seeds", {}) or {}
        primary_seed_count = int(seeds.get(self.config.primary_crop, 0) or 0)
        if money > self.config.market_sell_threshold and primary_seed_count <= self.config.seed_reorder_level:
            market.append(["BUY_SEED", self.config.primary_crop, 8])
        if not market and regime == "EXPANSION" and money > 300:
            market.append(["BUY_SEED", self.config.primary_crop, 6])
        return market[: self.config.market_sell_threshold]

    def _action_arbiter(
        self,
        observation: dict[str, Any],
        regime: str,
        farm: dict[str, Any],
        private: dict[str, Any],
        tasks: list[tuple[int, tuple[int, int], str, str]],
    ) -> dict[str, Any]:
        actions = self._worker_allocation(farm, tasks, regime)
        farmer_action = actions[0] if actions else ["PASS"]
        hand_actions = actions[1:] if len(actions) > 1 else []
        market = self._market_orders(farm, private, regime)
        return {"farmer": farmer_action, "hands": hand_actions, "market": market}

    def telemetry_snapshot(self) -> dict[str, Any]:
        return {
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "family": FAMILY_NAME,
            "current_regime": self.last_regime,
            "regime_history": list(self.regime_history),
            "decision_day": self.regime_decision_day,
            "decision_pressure": self.regime_decision_pressure,
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
            regime, _ = self._decide_regime(observation, snapshot.clock.day)
            farm = snapshot.farm
            private = snapshot.private
            tasks = self._task_scan(farm, snapshot.clock.day, regime)
            action = self._action_arbiter(observation, regime, farm, private, tasks)
            self.lifecycle_metrics["backlog"] = min(25, len(tasks))
            if snapshot.clock.day >= self.config.snapshot_day_end:
                self.lifecycle_metrics["terminal_backlog"] = min(25, len(tasks))
            self.lifecycle_metrics["productive_actions"] = sum(
                1
                for entry in action["farmer"] + [token for hand in action["hands"] for token in hand]
                if entry in {"DIG", "PLANT", "WATER", "HARVEST"}
            )
            if "SELL" in [item[0] for item in action["market"]]:
                self.lifecycle_metrics["inventory_sold"] += 1
            self.last_regime = regime
            return action
        except Exception as exc:  # noqa: BLE001 - explicit safe fallback path
            self.technical_errors += 1
            self.fallback_count += 1
            self.last_exception = f"{type(exc).__name__}: {exc}"
            return deepcopy(SAFE_PASS)


def create_copilot_e18_opponent_reactive_v2(
    *,
    config_path: Path | str | None = None,
    run_context: dict[str, Any] | None = None,
) -> CopilotE18OpponentReactiveV2Policy:
    config = load_copilot_e18_opponent_reactive_v2_config(config_path)
    return CopilotE18OpponentReactiveV2Policy(config=config, run_context=run_context)


def create_agent(
    *,
    config_path: Path | str | None = None,
    run_context: dict[str, Any] | None = None,
) -> CopilotE18OpponentReactiveV2Policy:
    return create_copilot_e18_opponent_reactive_v2(config_path=config_path, run_context=run_context)


__all__ = [
    "DEFAULT_CONFIG_PATH",
    "FAMILY_NAME",
    "POLICY_VERSION",
    "CopilotE18OpponentReactiveV2Config",
    "CopilotE18OpponentReactiveV2Policy",
    "create_agent",
    "create_copilot_e18_opponent_reactive_v2",
    "load_copilot_e18_opponent_reactive_v2_config",
]
