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

    def build_pasture(self) -> "ActionBuilder":
        """Set farmer action to BUILD_PASTURE current tile."""
        self.farmer_action = ["BUILD_PASTURE"]
        return self

    def place(self, item_name: str) -> "ActionBuilder":
        """Set farmer action to PLACE item on current tile."""
        self.farmer_action = ["PLACE", item_name]
        return self

    def pickup(self, item_name: str, quantity: int = 1) -> "ActionBuilder":
        """Set farmer action to PICKUP item from shed."""
        self.farmer_action = ["PICKUP", item_name, int(quantity)]
        return self

    def feed(self) -> "ActionBuilder":
        """Set farmer action to FEED animal on current tile."""
        self.farmer_action = ["FEED"]
        return self

    def move(self, direction: str) -> "ActionBuilder":
        """Set farmer action to move in direction ('NORTH', 'SOUTH', 'EAST', 'WEST' or 'N', 'S', 'E', 'W')."""
        dir_map = {
            "N": "NORTH", "NORTH": "NORTH",
            "S": "SOUTH", "SOUTH": "SOUTH",
            "E": "EAST", "EAST": "EAST",
            "W": "WEST", "WEST": "WEST",
        }
        target_dir = dir_map.get(direction.upper(), direction.upper())
        self.farmer_action = [target_dir]
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

    def buy_product(self, product_name: str, quantity: int) -> "ActionBuilder":
        """Add BUY_PRODUCT market order."""
        if quantity > 0:
            self.market_orders.append(["BUY_PRODUCT", product_name, int(quantity)])
        return self

    def hire(self) -> "ActionBuilder":
        """Add HIRE market order."""
        self.market_orders.append(["HIRE"])
        return self

    def buy_land(self) -> "ActionBuilder":
        """Add BUY_LAND market order."""
        self.market_orders.append(["BUY_LAND"])
        return self

    def buy_animal(self, animal_name: str, quantity: int = 1) -> "ActionBuilder":
        """Add BUY_ANIMAL market order."""
        if quantity > 0:
            self.market_orders.append(["BUY_ANIMAL", animal_name, int(quantity)])
        return self

    def add_hand_action(self, action_list: List[str]) -> "ActionBuilder":
        """Append action list for a farm hand."""
        self.hands_actions.append(action_list)
        return self

    def build(self) -> Dict[str, Any]:
        """Return the action dictionary formatted for Kaggle Environments."""
        return {
            "farmer": self.farmer_action,
            "hands": self.hands_actions,
            "market": self.market_orders,
        }
