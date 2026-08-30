from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from agricola.core.actions import ActionBuilder
from agricola.core.state import CROPS
from agricola.strategy.copilot.c2_config import CopilotC2Config


class CopilotC2Policy:
    """Copilot C2 prevention-first decision policy.

    This policy intentionally focuses on the dominant causal failure mode from E16:
    premature HARVEST dispatch, missed WATER and irreversible target gaps caused by
    preventable tile loss. The design follows the C2 foundation semantics:

    - strict harvest_ready gate with age + yield + PLANT validation
    - WATER before irreversible missed-water loss
    - DIG only for recovery or preventive clearance
    - working-set preservation and fast replanting after valid harvests
    """

    def __init__(self, config: Optional[CopilotC2Config] = None):
        self.config = config or CopilotC2Config()

    def _crop_rule(self, crop_name: str) -> Optional[Dict[str, Any]]:
        return CROPS.get(str(crop_name).upper())

    def is_harvest_ready(self, tile: Dict[str, Any], current_day: int) -> bool:
        if not isinstance(tile, dict):
            return False
        if tile.get("kind") != "PLANT":
            return False

        crop_name = str(tile.get("crop", "")).upper()
        crop_rule = self._crop_rule(crop_name)
        if crop_rule is None:
            return False

        yield_units = int(tile.get("yield_units", 0) or 0)
        if yield_units <= 0:
            return False

        planted_day = tile.get("planted_day")
        if planted_day is None:
            return False

        age_days = int(current_day) - int(planted_day)
        first_yield_day = int(crop_rule.get("first_yield_day", 0))
        return age_days >= first_yield_day

    def classify_tile_lifecycle(
        self,
        pos: Tuple[int, int],
        tile: Any,
        current_day: int,
        engine_step: int,
    ) -> str:
        if pos is None:
            return "OUT_OF_SCOPE"

        if tile == "LOCKED":
            return "OUT_OF_SCOPE"

        if tile is None:
            return "EMPTY_ASSIGNED"

        if isinstance(tile, dict) and tile.get("kind") == "WEED":
            return "LOST_WEED"

        if not isinstance(tile, dict):
            return "OUT_OF_SCOPE"

        kind = tile.get("kind")
        if kind == "EMPTY":
            return "EMPTY_ASSIGNED"
        if kind != "PLANT":
            return "OUT_OF_SCOPE"

        if self.is_harvest_ready(tile, current_day):
            return "HARVEST_READY"

        if tile.get("yield_units", 0) == 0 and tile.get("max_lifespan_step") is not None and engine_step >= int(tile.get("max_lifespan_step", 0)):
            return "RETIREMENT_DUE"

        if tile.get("yield_units", 0) == 0 and tile.get("max_lifespan_step") is None:
            return "RETIREMENT_DUE"

        return "GROWING"

    def _safe_private(self, obs: Dict[str, Any], player_index: int) -> Dict[str, Any]:
        private = obs.get("private", [])
        if isinstance(private, list):
            if player_index < len(private):
                entry = private[player_index]
                return entry if isinstance(entry, dict) else {}
            return {}
        if isinstance(private, dict):
            return private
        return {}

    def _select_crop(self, seeds: Dict[str, int]) -> Optional[str]:
        if not isinstance(seeds, dict):
            return None
        for crop_name in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"):
            if int(seeds.get(crop_name, 0) or 0) > 0:
                return crop_name
        return None

    def decide_actions(self, obs: Dict[str, Any], player_index: int = 0) -> List[List[str]]:
        farm = obs.get("farms", [])[player_index] if isinstance(obs.get("farms", []), list) and player_index < len(obs.get("farms", [])) else {}
        tiles: List[List[Any]] = farm.get("tiles", []) if isinstance(farm, dict) else []
        farmer_pos = farm.get("farmer", [4, 4]) if isinstance(farm, dict) else [4, 4]
        hands: List[List[int]] = farm.get("hands", []) if isinstance(farm, dict) else []
        private = self._safe_private(obs, player_index)
        seeds = private.get("seeds", {}) if isinstance(private, dict) else {}

        actions: List[List[str]] = []
        fx, fy = int(farmer_pos[0]), int(farmer_pos[1])
        farmer_tile = self._tile_at(tiles, fx, fy)
        farmer_state = self.classify_tile_lifecycle((fx, fy), farmer_tile, int(obs.get("day", 0)), int(obs.get("step", 0)))

        farmer_action = self._farmer_action(farmer_tile, farmer_state, fx, fy, obs, seeds)
        actions.append(farmer_action)

        for hand_index, hand_pos in enumerate(hands):
            hx, hy = int(hand_pos[0]), int(hand_pos[1])
            hand_tile = self._tile_at(tiles, hx, hy)
            hand_state = self.classify_tile_lifecycle((hx, hy), hand_tile, int(obs.get("day", 0)), int(obs.get("step", 0)))
            actions.append(self._hand_action(hand_tile, hand_state, hx, hy, obs))

        return actions

    def _tile_at(self, tiles: List[List[Any]], x: int, y: int) -> Any:
        if not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])):
            return "LOCKED"
        return tiles[y][x]

    def _farmer_action(
        self,
        tile: Any,
        state: str,
        x: int,
        y: int,
        obs: Dict[str, Any],
        seeds: Dict[str, int],
    ) -> List[str]:
        if state in {"LOST_WEED", "RETIREMENT_DUE"}:
            return ["DIG"]

        if isinstance(tile, dict):
            if tile.get("kind") == "PLANT":
                if self.is_harvest_ready(tile, int(obs.get("day", 0))):
                    return ["HARVEST"]
                if tile.get("watered_today") is False and int(tile.get("consecutive_unwatered", 0) or 0) + 1 >= self.config.water_deadline_unwatered_days:
                    return ["WATER"]
                if tile.get("watered_today") is False:
                    return ["WATER"]
                return ["PASS"]

        crop_name = self._select_crop(seeds)
        if tile is None and crop_name is not None:
            return ["PLANT", crop_name]
        return ["PASS"]

    def _hand_action(self, tile: Any, state: str, x: int, y: int, obs: Dict[str, Any]) -> List[str]:
        if state in {"LOST_WEED", "RETIREMENT_DUE"}:
            return ["DIG"]

        if isinstance(tile, dict) and tile.get("kind") == "PLANT":
            if self.is_harvest_ready(tile, int(obs.get("day", 0))):
                return ["HARVEST"]
            if tile.get("watered_today") is False:
                return ["WATER"]
        return ["PASS"]


class CopilotC2Agent:
    """Kaggle-callable entrypoint for the Copilot C2 policy candidate."""

    def __init__(self, config: Optional[CopilotC2Config] = None):
        self.config = config or CopilotC2Config()
        self.policy = CopilotC2Policy(config=self.config)

    def __call__(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        decisions = self.policy.decide_actions(obs, player_index=0)
        if not decisions:
            return {"farmer": ["PASS"], "hands": [], "market": []}

        farmer_action = decisions[0]
        hand_actions = decisions[1:]
        return {
            "farmer": farmer_action,
            "hands": hand_actions,
            "market": [],
        }

    def act(self, state: Any) -> Dict[str, Any]:
        obs = state.raw_obs if hasattr(state, "raw_obs") else state
        return self.__call__(obs)

    def decide(self, state: Any) -> Dict[str, Any]:
        return self.act(state)


if __name__ == "__main__":
    # Minimal smoke-run convenience check for direct invocation.
    sample = {
        "step": 0,
        "day": 0,
        "hour": 0,
        "farms": [{
            "money": 1000.0,
            "farmer": [4, 4],
            "hands": [],
            "tiles": [[None for _ in range(10)] for _ in range(10)],
        }],
        "private": [{"seeds": {"WHEAT": 5}, "inventories": [{}]}],
    }
    print(CopilotC2Policy().decide_actions(sample, player_index=0))
