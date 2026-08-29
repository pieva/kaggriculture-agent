"""State wrapper to parse and query observation dictionary from Kaggle Environments."""

from typing import Dict, Any, List, Optional, Tuple

# Constants for crop parameters from kaggriculture environment
CROPS = {
    "WHEAT": {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False, "water_needed": True},
    "CARROT": {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False, "water_needed": True},
    "TOMATO": {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True, "water_needed": True},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True, "water_needed": True},
    "MELON": {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False, "water_needed": True},
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
    def inventories(self) -> List[Dict[str, int]]:
        """Return list of personal inventories for [farmer, *hands]."""
        raw_invs = self.private.get("inventories", []) if isinstance(self.private, dict) else []
        if not isinstance(raw_invs, list):
            return [{}]
        return [dict(inv) if isinstance(inv, dict) else {} for inv in raw_invs]

    def get_worker_inventory_count(self, worker_id: int, item_name: str) -> int:
        """Return amount of item_name in specific worker's inventory."""
        invs = self.inventories
        if 0 <= worker_id < len(invs):
            return invs[worker_id].get(item_name, 0)
        return 0

    @property
    def farmer_position(self) -> Tuple[int, int]:
        """Return (x, y) coordinates of the farmer."""
        return (self.farmer_x, self.farmer_y)

    @property
    def hands_positions(self) -> List[Tuple[int, int]]:
        """Return list of (x, y) coordinates for active farm hands."""
        raw_hands = self.my_farm.get("hands", []) if isinstance(self.my_farm, dict) else []
        if not isinstance(raw_hands, list):
            return []
        return [(p[0], p[1]) for p in raw_hands if isinstance(p, list) and len(p) >= 2]

    @property
    def hires_today(self) -> int:
        """Return number of hires performed today."""
        if isinstance(self.my_farm, dict):
            return int(self.my_farm.get("hires_today", 0))
        return 0

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
