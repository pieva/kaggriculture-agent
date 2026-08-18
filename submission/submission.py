"""
Standalone submission file for Kaggle Kaggriculture.
Generated automatically by scripts/build_submission.py
"""

from typing import Dict, Any, List, Optional, Tuple

# --- Core State Wrapper ---
"""State wrapper to parse and query observation dictionary from Kaggle Environments."""


# Constants for crop parameters from kaggriculture environment
CROPS = {
    "WHEAT": {"seed": 10, "max_yield_day": 2, "water_needed": True},
    "CARROT": {"seed": 15, "max_yield_day": 3, "water_needed": True},
    "TOMATO": {"seed": 25, "max_yield_day": 4, "water_needed": True},
    "STRAWBERRY": {"seed": 50, "max_yield_day": 5, "water_needed": True},
    "MELON": {"seed": 100, "max_yield_day": 7, "water_needed": True},
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

# --- Carrot Loop Agent ---
"""Carrot Loop Baseline Agent.

A simple, robust, zero-crash baseline strategy focusing on continuous Carrot cultivation.
"""



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

# --- Kaggle Entrypoint ---
_agent_instance = CarrotLoopAgent()

def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point."""
    try:
        state = GameState(observation)
        return _agent_instance.act(state)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
