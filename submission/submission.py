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

    def hire(self) -> "ActionBuilder":
        """Add HIRE market order."""
        self.market_orders.append(["HIRE"])
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

# --- Base HIRE NW Cluster ROI Agent Strategy ---
"""HIRE Multi-Worker Scaling Strategy Agent (HIRENWClusterROIAgent).

Scales NWClusterROIAgent by introducing 1 daily farm hand via HIRE ($1/day)
with fixed spatial partitioning (4:5) on the 9-tile NW cluster:
- Farmer (4 tiles): {(4,4), (4,3), (3,4), (3,3)}
- Hand 1 (5 tiles): {(4,2), (3,2), (2,4), (2,3), (2,2)}

Preserves E03/E04 economic strategy (ROI/day crop selection and immediate liquidation)
and spatial task prioritization (HARVEST > PLANT > WATER) with Manhattan routing.
"""



FARMER_4_TILES: Tuple[Tuple[int, int], ...] = (
    (4, 4), (4, 3), (3, 4), (3, 3),
)

HAND1_5_TILES: Tuple[Tuple[int, int], ...] = (
    (4, 2), (3, 2), (2, 4), (2, 3), (2, 2),
)

ALL_9_TILES: Tuple[Tuple[int, int], ...] = FARMER_4_TILES + HAND1_5_TILES


class HIRENWClusterROIAgent:
    """Agent managing 9-tile NW cluster with 1 Farmer (4 tiles) and 1 daily Hand (5 tiles)."""

    def __init__(
        self,
        default_crop: str = "CARROT",
        farmer_tiles: Tuple[Tuple[int, int], ...] = FARMER_4_TILES,
        hand1_tiles: Tuple[Tuple[int, int], ...] = HAND1_5_TILES,
    ):
        self.default_crop = default_crop
        self.farmer_tiles = list(farmer_tiles)
        self.hand1_tiles = list(hand1_tiles)
        self.all_managed_tiles = list(ALL_9_TILES)

    def calculate_net_profit_per_day(self, crop_name: str, state: GameState) -> float:
        """Calculate expected net profit per day for a given crop using E02/E03 formula."""
        crop_info = CROPS.get(crop_name)
        if not crop_info:
            return -999.0

        seed_price = float(crop_info["seed"])
        days = float(crop_info["max_yield_day"])
        sell_price = state.get_price(crop_name)

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

    def _get_step_direction(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> str:
        """Compute single-step movement direction ('NORTH', 'SOUTH', 'EAST', 'WEST') towards target."""
        fx, fy = from_pos
        tx, ty = to_pos
        if ty < fy:
            return "NORTH"
        elif ty > fy:
            return "SOUTH"
        elif tx > fx:
            return "EAST"
        elif tx < fx:
            return "WEST"
        return "PASS"

    def _compute_worker_action(
        self,
        curr_pos: Tuple[int, int],
        assigned_tiles: List[Tuple[int, int]],
        target_crop: str,
        target_seed_cost: float,
        virtual_seeds: Dict[str, int],
        state: GameState,
    ) -> Tuple[List[str], Optional[str]]:
        """Compute action for a worker given assigned tiles and priority HARVEST > PLANT > WATER."""
        target_crop_info = CROPS[target_crop]

        empty_tiles: List[Tuple[int, int]] = []
        harvest_candidate_tiles: List[Tuple[int, int]] = []
        water_candidate_tiles: List[Tuple[int, int]] = []

        for pos in assigned_tiles:
            tile = state.get_tile(pos[0], pos[1])
            if tile is None:
                empty_tiles.append(pos)
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                crop = tile.get("crop", target_crop)
                crop_info = CROPS.get(crop, target_crop_info)
                age = state.day - tile.get("planted_day", state.day)
                max_yield_day = crop_info["max_yield_day"]

                if age >= max_yield_day:
                    harvest_candidate_tiles.append(pos)
                elif not tile.get("watered_today", False):
                    water_candidate_tiles.append(pos)

        def select_nearest(candidates: List[Tuple[int, int]]) -> Tuple[int, int]:
            return min(
                candidates,
                key=lambda p: (abs(p[0] - curr_pos[0]) + abs(p[1] - curr_pos[1]), p[1], p[0]),
            )

        target_pos: Optional[Tuple[int, int]] = None
        task: Optional[str] = None
        target_seeds_owned = virtual_seeds.get(target_crop, 0)

        if harvest_candidate_tiles:
            target_pos = select_nearest(harvest_candidate_tiles)
            task = "HARVEST"
        elif empty_tiles and target_seeds_owned > 0:
            target_pos = select_nearest(empty_tiles)
            task = "PLANT"
        elif water_candidate_tiles:
            target_pos = select_nearest(water_candidate_tiles)
            task = "WATER"

        if target_pos is None:
            return ["PASS"], None
        elif target_pos == curr_pos:
            if task == "HARVEST":
                return ["HARVEST"], None
            elif task == "PLANT":
                if target_seeds_owned > 0:
                    virtual_seeds[target_crop] -= 1
                    return ["PLANT", target_crop], target_crop
                else:
                    # Fallback to plant any owned virtual seed
                    for alt_crop in CROPS.keys():
                        if virtual_seeds.get(alt_crop, 0) > 0:
                            virtual_seeds[alt_crop] -= 1
                            return ["PLANT", alt_crop], alt_crop
                    return ["PASS"], None
            elif task == "WATER":
                return ["WATER"], None
            else:
                return ["PASS"], None
        else:
            step_dir = self._get_step_direction(curr_pos, target_pos)
            if step_dir != "PASS":
                return [step_dir], None
            return ["PASS"], None

    def act(self, state: GameState) -> Dict[str, Any]:
        """Compute action dictionary for current state."""
        actions = ActionBuilder()

        # 1. Market Phase: Sell ANY harvested crops in shed immediately
        for crop_name in CROPS.keys():
            shed_count = state.get_shed_count(crop_name)
            if shed_count > 0:
                actions.sell(crop_name, shed_count)

        # 2. Daily HIRE Trigger: Hire 1 hand on hour == 0 if no hands active today
        active_hands = state.hands_positions
        if state.hour == 0 and len(active_hands) == 0 and state.hires_today == 0:
            if state.money >= 1.0:
                actions.hire()

        # 3. Select best ROI crop
        target_crop = self.select_best_crop(state)
        target_crop_info = CROPS[target_crop]
        target_seed_cost = target_crop_info["seed"]

        # Count total empty tiles across all 9 managed tiles
        all_empty_tiles: List[Tuple[int, int]] = []
        for pos in self.all_managed_tiles:
            tile = state.get_tile(pos[0], pos[1])
            if tile is None:
                all_empty_tiles.append(pos)

        target_seeds_owned = state.get_seed_count(target_crop)
        needed_seeds = max(0, len(all_empty_tiles) - target_seeds_owned)

        if needed_seeds > 0 and state.money >= target_seed_cost:
            buy_qty = min(needed_seeds, int(state.money // target_seed_cost))
            if buy_qty > 0:
                actions.buy_seed(target_crop, buy_qty)
                target_seeds_owned += buy_qty

        # Build virtual seeds dict for shared seed reservation between workers
        virtual_seeds: Dict[str, int] = {
            crop: state.get_seed_count(crop) for crop in CROPS.keys()
        }
        virtual_seeds[target_crop] = target_seeds_owned

        # 4. Compute Worker Actions
        # Farmer action (4-tile partition)
        farmer_pos = state.farmer_position
        farmer_action, _ = self._compute_worker_action(
            farmer_pos, self.farmer_tiles, target_crop, target_seed_cost, virtual_seeds, state
        )
        actions.farmer_action = farmer_action

        # Hand 1 action (5-tile partition) if hand is active in state
        if active_hands:
            hand1_pos = active_hands[0]
            hand1_action, _ = self._compute_worker_action(
                hand1_pos, self.hand1_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            actions.add_hand_action(hand1_action)

        return actions.build()

# --- E06 Water-First HIRE NW Cluster ROI Agent Strategy ---
"""Water-First Priority Strategy Agent (WaterFirstHIRENWClusterROIAgent).

Subclasses HIRENWClusterROIAgent from E05 to evaluate the single experimental variable:
swapping worker task priority from HARVEST > PLANT > WATER to WATER > HARVEST > PLANT.

All other components (9-tile NW footprint, 1 Farmer + 1 daily Hand at $1/day,
fixed 4:5 spatial partitioning, E03 ROI crop selection, Manhattan routing) remain 100% identical.
"""



class WaterFirstHIRENWClusterROIAgent(HIRENWClusterROIAgent):
    """Subclass of HIRENWClusterROIAgent implementing WATER > HARVEST > PLANT task priority."""

    def _compute_worker_action(
        self,
        curr_pos: Tuple[int, int],
        assigned_tiles: List[Tuple[int, int]],
        target_crop: str,
        target_seed_cost: float,
        virtual_seeds: Dict[str, int],
        state: GameState,
    ) -> Tuple[List[str], Optional[str]]:
        """Compute action for a worker given assigned tiles and priority WATER > HARVEST > PLANT."""
        target_crop_info = CROPS[target_crop]

        empty_tiles: List[Tuple[int, int]] = []
        harvest_candidate_tiles: List[Tuple[int, int]] = []
        water_candidate_tiles: List[Tuple[int, int]] = []

        for pos in assigned_tiles:
            tile = state.get_tile(pos[0], pos[1])
            if tile is None:
                empty_tiles.append(pos)
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                crop = tile.get("crop", target_crop)
                crop_info = CROPS.get(crop, target_crop_info)
                age = state.day - tile.get("planted_day", state.day)
                max_yield_day = crop_info["max_yield_day"]

                if age >= max_yield_day:
                    harvest_candidate_tiles.append(pos)
                elif not tile.get("watered_today", False):
                    water_candidate_tiles.append(pos)

        def select_nearest(candidates: List[Tuple[int, int]]) -> Tuple[int, int]:
            return min(
                candidates,
                key=lambda p: (abs(p[0] - curr_pos[0]) + abs(p[1] - curr_pos[1]), p[1], p[0]),
            )

        target_pos: Optional[Tuple[int, int]] = None
        task: Optional[str] = None
        target_seeds_owned = virtual_seeds.get(target_crop, 0)

        # Single Experimental Intervention: WATER > HARVEST > PLANT
        if water_candidate_tiles:
            target_pos = select_nearest(water_candidate_tiles)
            task = "WATER"
        elif harvest_candidate_tiles:
            target_pos = select_nearest(harvest_candidate_tiles)
            task = "HARVEST"
        elif empty_tiles and target_seeds_owned > 0:
            target_pos = select_nearest(empty_tiles)
            task = "PLANT"

        if target_pos is None:
            return ["PASS"], None
        elif target_pos == curr_pos:
            if task == "WATER":
                return ["WATER"], None
            elif task == "HARVEST":
                return ["HARVEST"], None
            elif task == "PLANT":
                if target_seeds_owned > 0:
                    virtual_seeds[target_crop] -= 1
                    return ["PLANT", target_crop], target_crop
                else:
                    # Fallback to plant any owned virtual seed
                    for alt_crop in CROPS.keys():
                        if virtual_seeds.get(alt_crop, 0) > 0:
                            virtual_seeds[alt_crop] -= 1
                            return ["PLANT", alt_crop], alt_crop
                    return ["PASS"], None
            else:
                return ["PASS"], None
        else:
            step_dir = self._get_step_direction(curr_pos, target_pos)
            if step_dir != "PASS":
                return [step_dir], None
            return ["PASS"], None

# --- Kaggle Entrypoint ---
_agent_instance = WaterFirstHIRENWClusterROIAgent()

def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point."""
    try:
        state = GameState(observation)
        return _agent_instance.act(state)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
