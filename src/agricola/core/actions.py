"""Action builder class to assemble valid action dictionaries for Kaggriculture."""

from typing import Dict, Any, List


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
