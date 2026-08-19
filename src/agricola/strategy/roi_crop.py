"""Dynamic Crop Selection & ROI Scaling Agent (ROICropAgent).

Evolves the baseline single-tile agent by dynamically selecting the crop
with the highest net profit per day (ROI / day) based on liquid capital and
dynamic market selling prices.
"""

from typing import Dict, Any, Optional
from agricola.core.state import GameState, CROPS
from agricola.core.actions import ActionBuilder


class ROICropAgent:
    """Agent that selects crops dynamically based on expected net profit per day."""

    def __init__(self, default_crop: str = "CARROT"):
        self.default_crop = default_crop

    def calculate_net_profit_per_day(self, crop_name: str, state: GameState) -> float:
        """Calculate expected net profit per day for a given crop.
        
        Formula: (SellPrice * Yield - SeedPrice) / Days
        where:
        - SellPrice: dynamic market price from state.get_price(crop_name)
        - SeedPrice: static seed purchase cost from CROPS[crop_name]["seed"]
        - Yield: standard yield with regular watering (2 units)
        - Days: max_yield_day from CROPS[crop_name]["max_yield_day"]
        """
        crop_info = CROPS.get(crop_name)
        if not crop_info:
            return -999.0

        seed_price = float(crop_info["seed"])
        days = float(crop_info["max_yield_day"])
        sell_price = state.get_price(crop_name)

        # Fallback for sell_price if market price is 0.0 or unavailable
        if sell_price <= 0.0:
            sell_price = seed_price * 1.75

        yield_units = 2.0
        gross_revenue = sell_price * yield_units
        net_profit = gross_revenue - seed_price
        return net_profit / max(1.0, days)

    def select_best_crop(self, state: GameState) -> str:
        """Select affordable crop with the highest net profit per day."""
        best_crop = self.default_crop
        best_profit_per_day = -9999.0

        for crop_name, crop_info in CROPS.items():
            seed_cost = crop_info["seed"]
            if state.money >= seed_cost:
                profit_per_day = self.calculate_net_profit_per_day(crop_name, state)
                if profit_per_day > best_profit_per_day:
                    best_profit_per_day = profit_per_day
                    best_crop = crop_name

        return best_crop

    def act(self, state: GameState) -> Dict[str, Any]:
        """Compute action dictionary for current state."""
        actions = ActionBuilder()

        # 1. Sell ANY harvested crops available in the shed
        for crop_name in CROPS.keys():
            shed_count = state.get_shed_count(crop_name)
            if shed_count > 0:
                actions.sell(crop_name, shed_count)

        # 2. Select best crop given current capital and market prices
        target_crop = self.select_best_crop(state)
        target_crop_info = CROPS[target_crop]
        target_seed_cost = target_crop_info["seed"]

        # Check inventory for target_crop seed
        target_seeds_owned = state.get_seed_count(target_crop)

        # 3. Market order for buffer seed: if we have 0 seeds of target_crop and can afford it, buy 1
        if target_seeds_owned == 0 and state.money >= target_seed_cost:
            actions.buy_seed(target_crop, 1)
            target_seeds_owned += 1

        # 4. Farmer action on current single tile (4, 4)
        tile = state.current_tile()

        if tile is None:
            # Tile is empty: plant target_crop if seed owned, else plant any owned seed
            if target_seeds_owned > 0:
                actions.plant(target_crop)
            else:
                planted = False
                for alt_crop in CROPS.keys():
                    if state.get_seed_count(alt_crop) > 0:
                        actions.plant(alt_crop)
                        planted = True
                        break
                if not planted:
                    actions.pass_turn()
        elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
            crop = tile.get("crop", target_crop)
            crop_info = CROPS.get(crop, target_crop_info)
            age = state.day - tile.get("planted_day", state.day)
            max_yield_day = crop_info["max_yield_day"]

            if age >= max_yield_day:
                actions.harvest()
            elif not tile.get("watered_today", False):
                actions.water()
            else:
                actions.pass_turn()
        else:
            actions.pass_turn()

        return actions.build()
