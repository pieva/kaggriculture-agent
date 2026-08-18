"""Carrot Loop Baseline Agent.

A simple, robust, zero-crash baseline strategy focusing on continuous Carrot cultivation.
"""

from typing import Dict, Any
from agricola.core.state import GameState, CROPS
from agricola.core.actions import ActionBuilder


class CarrotLoopAgent:
    """Baseline agent executing a deterministic single-tile Carrot farming loop."""

    def __init__(self, target_crop: str = "CARROT"):
        self.target_crop = target_crop
        self.crop_info = CROPS.get(target_crop, CROPS["CARROT"])

    def act(self, state: GameState) -> Dict[str, Any]:
        """Compute action dictionary for current state."""
        actions = ActionBuilder()

        # 1. Market orders
        # Sell any harvested carrots in shed
        carrots_in_shed = state.get_shed_count(self.target_crop)
        if carrots_in_shed > 0:
            actions.sell(self.target_crop, carrots_in_shed)

        # Buy 1 seed if we have none and enough money
        seeds_owned = state.get_seed_count(self.target_crop)
        seed_cost = self.crop_info["seed"]
        if seeds_owned == 0 and state.money >= seed_cost:
            actions.buy_seed(self.target_crop, 1)
            seeds_owned += 1

        # 2. Farmer action on current tile
        tile = state.current_tile()

        if tile is None and seeds_owned > 0:
            actions.plant(self.target_crop)
        elif isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile.get("crop") == self.target_crop:
            age = state.day - tile.get("planted_day", state.day)
            max_yield_day = self.crop_info["max_yield_day"]

            if age >= max_yield_day:
                actions.harvest()
            elif not tile.get("watered_today", False):
                actions.water()
            else:
                actions.pass_turn()
        else:
            actions.pass_turn()

        return actions.build()
