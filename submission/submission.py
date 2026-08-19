"""
Standalone submission file for Kaggle Kaggriculture.
Generated automatically by scripts/build_submission.py
"""

from typing import Dict, Any, List, Optional, Tuple

# --- Core State Wrapper ---
"""State wrapper to parse and query observation dictionary from Kaggle Environments."""


# Constants for crop parameters from kaggriculture environment
CROPS = {
    "WHEAT": {"seed": 10, "max_yield_day": 4, "water_needed": True},
    "CARROT": {"seed": 20, "max_yield_day": 3, "water_needed": True},
    "TOMATO": {"seed": 50, "max_yield_day": 8, "water_needed": True},
    "STRAWBERRY": {"seed": 100, "max_yield_day": 10, "water_needed": True},
    "MELON": {"seed": 80, "max_yield_day": 12, "water_needed": True},
}


class GameState:
    """Helper class to query the current turn observation safely."""

    def __init__(self, observation: Dict[str, Any]):
        self.raw_obs = observation
        self.step: int = observation.get("step", 0)
        self.day: int = observation.get("day", 0)
        self.hour: int = observation.get("hour", 0)
        self.player_id: int = observation.get("player", 0)
        self.remaining_overage_time: float = observation.get("remainingOverageTime", 60.0)

        farms: List[Dict[str, Any]] = observation.get("farms", [])
        if farms and self.player_id < len(farms):
            self.my_farm = farms[self.player_id]
            self.opponent_farm = farms[1 - self.player_id] if len(farms) > 1 else {}
        else:
            self.my_farm = {}
            self.opponent_farm = {}

        self.money: float = self.my_farm.get("money", 0.0)
        farmer_pos = self.my_farm.get("farmer", [4, 4])
        self.farmer_x: int = farmer_pos[0]
        self.farmer_y: int = farmer_pos[1]
        self.tiles: List[List[Any]] = self.my_farm.get("tiles", [])

        self.private: Dict[str, Any] = observation.get("private", {}) or {}
        self.shed: Dict[str, int] = self.private.get("shed", {}) or {}
        self.seeds: Dict[str, int] = self.private.get("seeds", {}) or {}

        self.market: Dict[str, Any] = observation.get("market", {}) or {}
        self.market_prices: Dict[str, float] = self.market.get("prices", {}) or {}
        self.market_inventory: Dict[str, int] = self.market.get("inventory", {}) or {}

    @property
    def farmer_position(self) -> Tuple[int, int]:
        """Return (x, y) coordinates of the farmer."""
        return (self.farmer_x, self.farmer_y)

    def get_tile(self, x: int, y: int) -> Any:
        """Return tile info at (x, y). null/None if empty, 'LOCKED' if locked, or dict if tile content."""
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]):
            return self.tiles[y][x]
        return "LOCKED"

    def current_tile(self) -> Any:
        """Return tile under farmer's current position."""
        return self.get_tile(self.farmer_x, self.farmer_y)

    def get_shed_count(self, item_name: str) -> int:
        """Return amount of item_name stored in shed."""
        return self.shed.get(item_name, 0)

    def get_seed_count(self, crop_name: str) -> int:
        """Return amount of crop_name seeds owned."""
        return self.seeds.get(crop_name, 0)

    def get_price(self, item_name: str) -> float:
        """Return current market price for item_name."""
        return self.market_prices.get(item_name, 0.0)

# --- Action Builder ---
"""Action builder class to assemble valid action dictionaries for Kaggriculture."""



class ActionBuilder:
    """Helper builder to construct valid action dictionaries."""

    def __init__(self):
        self.farmer_action: List[str] = ["PASS"]
        self.hands_actions: List[List[str]] = []
        self.market_orders: List[List[Any]] = []

    def pass_turn(self) -> "ActionBuilder":
        """Set farmer action to PASS."""
        self.farmer_action = ["PASS"]
        return self

    def plant(self, crop_name: str) -> "ActionBuilder":
        """Set farmer action to PLANT crop."""
        self.farmer_action = ["PLANT", crop_name]
        return self

    def water(self) -> "ActionBuilder":
        """Set farmer action to WATER current tile."""
        self.farmer_action = ["WATER"]
        return self

    def harvest(self) -> "ActionBuilder":
        """Set farmer action to HARVEST current tile."""
        self.farmer_action = ["HARVEST"]
        return self

    def move(self, direction: str) -> "ActionBuilder":
        """Set farmer action to MOVE in direction ('N', 'S', 'E', 'W')."""
        self.farmer_action = ["MOVE", direction]
        return self

    def sell(self, product_name: str, quantity: int) -> "ActionBuilder":
        """Add SELL market order."""
        if quantity > 0:
            self.market_orders.append(["SELL", product_name, int(quantity)])
        return self

    def buy_seed(self, crop_name: str, quantity: int) -> "ActionBuilder":
        """Add BUY_SEED market order."""
        if quantity > 0:
            self.market_orders.append(["BUY_SEED", crop_name, int(quantity)])
        return self

    def build(self) -> Dict[str, Any]:
        """Return the action dictionary formatted for Kaggle Environments."""
        return {
            "farmer": self.farmer_action,
            "hands": self.hands_actions,
            "market": self.market_orders,
        }

# --- ROI Crop Agent Strategy ---
"""Dynamic Crop Selection & ROI Scaling Agent (ROICropAgent).

Evolves the baseline single-tile agent by dynamically selecting the crop
with the highest net profit per day (ROI / day) based on liquid capital and
dynamic market selling prices.
"""



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

# --- Kaggle Entrypoint ---
_agent_instance = ROICropAgent()

def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point."""
    try:
        state = GameState(observation)
        return _agent_instance.act(state)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
