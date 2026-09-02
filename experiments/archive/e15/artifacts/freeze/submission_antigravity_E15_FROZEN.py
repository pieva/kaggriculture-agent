"""
Standalone submission file for Kaggle Kaggriculture.
Generated automatically for Antigravity Independent Strategy Model (E14).
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
import math

# ==========================================
# --- Core State Wrapper ---
# ==========================================
"""State wrapper to parse and query observation dictionary from Kaggle Environments."""


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

# ==========================================
# --- Action Builder ---
# ==========================================
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

# ==========================================
# --- Antigravity Strategy Config & Agent ---
# ==========================================
"""Configuration for Antigravity Independent Strategy Model."""



@dataclass
class AntigravityConfig:
    """Parametric configuration for Antigravity Strategy Model."""
    # Farm & Land Architecture
    enable_land_expansion: bool = True
    target_quadrants: int = 3                # Q0, Q1, Q2 (75 tiles)
    q1_unlock_day: int = 5                   # Minimum day to unlock Q1 if cash >= $1,000
    q2_unlock_day: int = 8                   # Minimum day to unlock Q2 if cash >= $2,000
    q1_reserve_cash: float = 1000.0          # Cash protected when unlocking Q1
    q2_reserve_cash: float = 2000.0          # Cash protected when unlocking Q2
    
    # Workforce Strategy
    max_hands: int = 12                      # Maximum workforce capacity
    workforce_ramp_hours: Tuple[int, ...] = (0, 1)  # Stagger hires across H0 and H1 to respect 10 orders/turn limit
    stop_hire_day: int = 31                  # Day to stop hiring (31 = active all game)
    
    # Livestock Engine
    target_cows: int = 14                    # Target cow herd size across 3 quadrants
    target_sheep: int = 4                    # Target sheep herd size across 3 quadrants
    cow_cost: float = 400.0
    sheep_cost: float = 500.0
    feed_buffer_multiplier: int = 3          # Buffer factor for wheat feed relative to animal count
    min_feed_buffer: int = 10                # Minimum wheat feed buffer units
    
    # Opening Day 1 Configuration
    opening_hands: int = 5
    opening_cows: int = 2
    opening_sheep: int = 2
    opening_wheat_feed: int = 10
    opening_wheat_seeds: int = 10
    opening_melon_seeds: int = 8
    
    # Crop Strategy & Rotation
    stop_planting_day: int = 26              # Stop planting crops after Day 26 (no time to mature)
    liquidation_day: int = 28                # Liquidate all stored Wheat feed from Day 28 onwards
    
    # Telemetry / Diagnostic tracking
    track_telemetry: bool = True

"""Antigravity Independent Strategy Agent."""




class AntigravityROIAgent:
    """Independent Strategy Agent by Antigravity (Q0->Q1->Q2 75t Integrated Architecture)."""

    def __init__(self, config: Optional[AntigravityConfig] = None):
        self.config = config or AntigravityConfig()
        self.owned_quadrants: int = 1
        self.shed_tiles: Set[Tuple[int, int]] = {(4, 4), (5, 4), (4, 5), (5, 5)}
        self.livestock_core_tiles: List[Tuple[int, int]] = [(3, 3), (3, 4), (4, 3), (4, 4)]
        self.realized_revenue: Dict[str, float] = {}

    def _move_towards(self, px: int, py: int, target: Tuple[int, int]) -> List[str]:
        tx, ty = target
        if tx < px:
            return ["WEST"]
        if tx > px:
            return ["EAST"]
        if ty < py:
            return ["NORTH"]
        if ty > py:
            return ["SOUTH"]
        return ["PASS"]

    def _owned_quadrants(self, state: GameState) -> int:
        raw_quads = state.my_farm.get("unlocked_quadrants", ["NW"])
        return len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)

    def _owned_tiles(self, state: GameState) -> List[Tuple[int, int]]:
        tiles = []
        for y in range(10):
            for x in range(10):
                if state.get_tile(x, y) != "LOCKED":
                    tiles.append((x, y))
        return tiles

    def _pasture_tiles(self, state: GameState) -> List[Tuple[int, int]]:
        tiles = []
        for y in range(10):
            for x in range(10):
                tile = state.get_tile(x, y)
                if isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                    tiles.append((x, y))
        return tiles

    def _animal_tiles(self, state: GameState) -> List[Tuple[int, int]]:
        out = []
        for y in range(10):
            for x in range(10):
                tile = state.get_tile(x, y)
                if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and tile.get("animal"):
                    out.append((x, y))
        return out

    def _animal_counts(self, state: GameState) -> Dict[str, int]:
        counts = {"COW": 0, "SHEEP": 0}
        for pos in self._animal_tiles(state):
            tile = state.get_tile(pos[0], pos[1])
            animal = tile.get("animal")
            if animal in counts:
                counts[animal] += 1
        for animal in counts:
            counts[animal] += state.get_shed_count(animal)
            for worker_id in range(1 + len(state.hands_positions)):
                counts[animal] += state.get_worker_inventory_count(worker_id, animal)
        return counts

    def _crop_counts(self, state: GameState) -> Dict[str, int]:
        counts = {crop: 0 for crop in CROPS.keys()}
        for y in range(10):
            for x in range(10):
                tile = state.get_tile(x, y)
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    crop = tile.get("crop", "WHEAT")
                    if crop in counts:
                        counts[crop] += 1
        return counts

    def _inventory_total(self, state: GameState, item: str) -> int:
        return state.get_shed_count(item) + sum(
            state.get_worker_inventory_count(worker_id, item)
            for worker_id in range(1 + len(state.hands_positions))
        )

    def _pasture_positions(self) -> List[Tuple[int, int]]:
        """Pasture coordinates clustered around center crossroads for fast feeding and milking."""
        return [
            # Q0 Core (4 pastures)
            (3, 3), (3, 4), (4, 3), (3, 2),
            # Q1 Extension (6 pastures)
            (5, 3), (5, 2), (6, 3), (6, 2), (7, 3), (7, 2),
            # Q2 Extension (8 pastures)
            (3, 5), (2, 5), (3, 6), (2, 6), (3, 7), (2, 7), (4, 6), (4, 7),
        ]

    def _crop_positions(self, state: GameState) -> List[Tuple[int, int]]:
        """All owned tiles in Q0, Q1, Q2 excluding pasture tiles and shed access."""
        pastures = set(self._pasture_positions())
        owned = self._owned_quadrants(state)
        tiles = []
        for p in self._owned_tiles(state):
            if p in pastures or p in self.shed_tiles:
                continue
            if owned == 1 and (p[0] >= 5 or p[1] >= 5):
                continue
            if owned == 2 and p[1] >= 5:
                continue
            tiles.append(p)
        return tiles

    def _target_crop_counts(self, state: GameState) -> Dict[str, int]:
        owned = self._owned_quadrants(state)
        day = state.day + 1
        if owned < 2:
            return {"WHEAT": 8, "MELON": 8, "STRAWBERRY": 4, "CARROT": 0, "TOMATO": 0}
        elif owned < 3:
            return {"WHEAT": 12, "MELON": 10, "STRAWBERRY": 14, "CARROT": 0, "TOMATO": 0}
        else:
            if day <= 16:
                return {"WHEAT": 16, "MELON": 12, "STRAWBERRY": 22, "CARROT": 0, "TOMATO": 0}
            elif day <= 22:
                return {"WHEAT": 18, "MELON": 8, "STRAWBERRY": 22, "CARROT": 0, "TOMATO": 0}
            elif day <= 26:
                return {"WHEAT": 18, "MELON": 0, "STRAWBERRY": 20, "CARROT": 6, "TOMATO": 0}
            else:
                return {"WHEAT": 8, "MELON": 0, "STRAWBERRY": 0, "CARROT": 0, "TOMATO": 0}

    def _desired_hands(self, state: GameState) -> int:
        day = state.day + 1
        if day >= 30 and state.hour >= 20:
            return 8
        owned = self._owned_quadrants(state)
        if day <= 4:
            return self.config.opening_hands
        if owned < 2:
            return 6
        if owned == 2:
            return 8 if day < 8 else 10
        # 3 Quadrants owned
        if day <= 12:
            return 10
        return self.config.max_hands

    def _select_crop_for_tile(
        self,
        state: GameState,
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
    ) -> Optional[str]:
        targets = self._target_crop_counts(state)
        owned = self._owned_quadrants(state)
        day = state.day + 1
        if owned < 2:
            order = ["WHEAT", "MELON", "STRAWBERRY"]
        elif owned < 3:
            order = ["STRAWBERRY", "MELON", "WHEAT"]
        elif day <= 22:
            order = ["STRAWBERRY", "WHEAT", "MELON"]
        else:
            order = ["WHEAT", "STRAWBERRY", "CARROT"]
        for crop in order:
            if virtual_seeds.get(crop, 0) > 0 and virtual_crop_counts.get(crop, 0) < targets.get(crop, 0):
                virtual_seeds[crop] -= 1
                virtual_crop_counts[crop] = virtual_crop_counts.get(crop, 0) + 1
                return crop
        for crop in ("STRAWBERRY", "WHEAT", "MELON", "CARROT"):
            if virtual_seeds.get(crop, 0) > 0:
                virtual_seeds[crop] -= 1
                virtual_crop_counts[crop] = virtual_crop_counts.get(crop, 0) + 1
                return crop
        return None

    def _worker_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        crop_tiles: List[Tuple[int, int]],
        pasture_targets: List[Tuple[int, int]],
        reserved: Set[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
    ) -> List[str]:
        px, py = pos
        products = ["MILK", "WOOL", "FERTILIZER", "WHEAT", "MELON", "STRAWBERRY", "CARROT", "TOMATO"]
        animals = ["COW", "SHEEP"]
        inv_total = sum(state.get_worker_inventory_count(worker_id, item) for item in products + animals)
        animal_in_hand = next((animal for animal in animals if state.get_worker_inventory_count(worker_id, animal) > 0), None)
        animal_tiles = self._animal_tiles(state)
        pasture_tiles = self._pasture_tiles(state)

        # 1. Deposit goods at shed
        carried_non_feed = sum(
            state.get_worker_inventory_count(worker_id, item)
            for item in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO")
        )
        carried_wheat = state.get_worker_inventory_count(worker_id, "WHEAT")
        has_unfed_animals = any(
            isinstance(state.get_tile(p[0], p[1]), dict)
            and not state.get_tile(p[0], p[1]).get("fed_today", False)
            for p in animal_tiles
        )

        if animal_in_hand is None and (px, py) in self.shed_tiles:
            for item in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO"):
                count = state.get_worker_inventory_count(worker_id, item)
                if count > 0:
                    return ["PLACE", item, count]
            if carried_wheat > 0 and (not has_unfed_animals or state.hour >= 22):
                return ["PLACE", "WHEAT", carried_wheat]

        # Return to shed if carrying non-feed items, inventory full, or late in the day before contracts expire
        if animal_in_hand is None:
            if carried_non_feed > 0:
                return self._move_towards(px, py, (4, 4))
            if state.hour >= 21 and inv_total > 0:
                return self._move_towards(px, py, (4, 4))
            if carried_wheat > 0 and not has_unfed_animals:
                return self._move_towards(px, py, (4, 4))

        # 2. Place Animal in hand into free pasture
        if animal_in_hand:
            free_pastures = [
                p for p in pasture_targets
                if p not in reserved
                and isinstance(state.get_tile(p[0], p[1]), dict)
                and state.get_tile(p[0], p[1]).get("kind") == "PASTURE"
                and "animal" not in state.get_tile(p[0], p[1])
            ]
            if free_pastures:
                target = min(free_pastures, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                reserved.add(target)
                return ["PLACE", animal_in_hand] if target == (px, py) else self._move_towards(px, py, target)
            return self._move_towards(px, py, (4, 4))

        # 3. Pickup Animal from shed if free pasture exists
        for animal in ("COW", "SHEEP"):
            if state.get_shed_count(animal) > 0 and inv_total == 0:
                free_pastures = [
                    p for p in pasture_targets
                    if p not in reserved
                    and isinstance(state.get_tile(p[0], p[1]), dict)
                    and state.get_tile(p[0], p[1]).get("kind") == "PASTURE"
                    and "animal" not in state.get_tile(p[0], p[1])
                ]
                if free_pastures:
                    target = min(free_pastures, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                    reserved.add(target)
                    return ["PICKUP", animal, 1] if (px, py) in self.shed_tiles else self._move_towards(px, py, (4, 4))

        # 4. Build Pasture ON-DEMAND ONLY (when existing pastures < total animals owned)
        total_animals_owned = len(animal_tiles) + sum(state.get_shed_count(a) for a in animals) + sum(state.get_worker_inventory_count(w, a) for w in range(1 + len(state.hands_positions)) for a in animals)
        existing_pastures = len(pasture_tiles)
        if existing_pastures < total_animals_owned and inv_total == 0:
            owned = self._owned_quadrants(state)
            missing_pastures = [
                p for p in pasture_targets[:total_animals_owned]
                if p not in reserved
                and state.get_tile(p[0], p[1]) is None
                and (owned >= 3 or (owned >= 2 and p[1] < 5) or (owned == 1 and p[0] < 5 and p[1] < 5))
            ]
            if missing_pastures:
                target = min(missing_pastures, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                reserved.add(target)
                return ["BUILD_PASTURE"] if target == (px, py) else self._move_towards(px, py, target)

        # 5. Harvest Animal Yield (MILK & WOOL - top revenue priority)
        ready_animals = [
            p for p in animal_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("yield_units", 0) > 0
        ]
        if ready_animals and inv_total < 5:
            target = min(ready_animals, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            return ["HARVEST"] if target == (px, py) else self._move_towards(px, py, target)

        # 6. Harvest Mature Crops
        ready_crops = [
            p for p in crop_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("kind") == "PLANT"
            and state.get_tile(p[0], p[1]).get("yield_units", 0) > 0
        ]
        if ready_crops and inv_total < 5:
            target = min(ready_crops, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            return ["HARVEST"] if target == (px, py) else self._move_towards(px, py, target)

        # 7. Feed Unfed Animals
        unfed = [
            p for p in animal_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and not state.get_tile(p[0], p[1]).get("fed_today", False)
        ]
        if unfed:
            if carried_wheat <= 0:
                if state.get_shed_count("WHEAT") > 0 and inv_total < 3:
                    return ["PICKUP", "WHEAT", min(8, state.get_shed_count("WHEAT"))] if (px, py) in self.shed_tiles else self._move_towards(px, py, (4, 4))
            else:
                target = min(unfed, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                reserved.add(target)
                return ["FEED"] if target == (px, py) else self._move_towards(px, py, target)

        # 8. Care for Animals (cows/sheep fed today but not cared)
        careable = [
            p for p in animal_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("fed_today", False)
            and not state.get_tile(p[0], p[1]).get("cared_today", False)
        ]
        if careable:
            target = min(careable, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            return ["CARE"] if target == (px, py) else self._move_towards(px, py, target)

        # 9. Emergency Watering (consecutive unwatered >= 1)
        emergency_water = [
            p for p in crop_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("kind") == "PLANT"
            and state.get_tile(p[0], p[1]).get("consecutive_unwatered", 0) >= 1
        ]
        if emergency_water:
            target = min(emergency_water, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            return ["WATER"] if target == (px, py) else self._move_towards(px, py, target)

        # 10. Weed Digging (Clear weeds immediately to maintain high productive land area)
        weeds = [
            p for p in crop_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("kind") == "WEED"
        ]
        if weeds:
            target = min(weeds, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            return ["DIG"] if target == (px, py) else self._move_towards(px, py, target)

        # 11. General Watering
        unwatered = [
            p for p in crop_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("kind") == "PLANT"
            and not state.get_tile(p[0], p[1]).get("watered_today", False)
        ]
        if unwatered:
            target = min(unwatered, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            return ["WATER"] if target == (px, py) else self._move_towards(px, py, target)

        # 12. Planting
        if state.day + 1 <= self.config.stop_planting_day:
            plantable = [
                p for p in crop_tiles
                if p not in reserved
                and state.get_tile(p[0], p[1]) is None
            ]
            if plantable:
                crop = self._select_crop_for_tile(state, dict(virtual_seeds), dict(virtual_crop_counts))
                if crop:
                    target = min(plantable, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                    reserved.add(target)
                    if target != (px, py):
                        return self._move_towards(px, py, target)
                    actual_crop = self._select_crop_for_tile(state, virtual_seeds, virtual_crop_counts)
                    return ["PLANT", actual_crop] if actual_crop else ["PASS"]

        # 13. Fertilizer Collection
        fert_tiles = [
            p for p in animal_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("fertilizer_available", False)
        ]
        if fert_tiles and inv_total < 5:
            target = min(fert_tiles, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            return ["COLLECT_FERTILIZER"] if target == (px, py) else self._move_towards(px, py, target)

        return ["PASS"]

    def act(self, state: GameState) -> Dict[str, Any]:
        """Main agent decision entry point per turn."""
        builder = ActionBuilder()
        hands = state.hands_positions
        self.owned_quadrants = max(self.owned_quadrants, self._owned_quadrants(state))

        day = state.day + 1
        cash = state.money
        crop_tiles = self._crop_positions(state)
        pasture_targets = self._pasture_positions()
        animal_counts = self._animal_counts(state)
        animal_tiles = self._animal_tiles(state)
        pasture_count = len(self._pasture_tiles(state))
        crop_counts = self._crop_counts(state)
        crop_targets = self._target_crop_counts(state)

        # 1. Critical Priority: BUY_LAND (first order to guarantee execution within 10 market orders limit)
        if self.config.enable_land_expansion and day > 1 and state.hour == 0:
            if self.owned_quadrants < 2 and day >= self.config.q1_unlock_day and cash >= self.config.q1_reserve_cash:
                builder.buy_land()
                cash -= self.config.q1_reserve_cash
                self.owned_quadrants = 2
            elif self.owned_quadrants == 2 and day >= self.config.q2_unlock_day and cash >= self.config.q2_reserve_cash:
                builder.buy_land()
                cash -= self.config.q2_reserve_cash
                self.owned_quadrants = 3

        # 2. Market Sales: Instant sell of all shed goods
        for product in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO"):
            count = state.get_shed_count(product)
            if count > 0 and len(builder.market_orders) < 8:
                builder.sell(product, count)
                revenue = count * state.get_price(product)
                self.realized_revenue[product] = self.realized_revenue.get(product, 0.0) + revenue

        # Wheat selling: keep feed buffer until day 28
        wheat_reserve = max(8, len(animal_tiles) * self.config.feed_buffer_multiplier + 4)
        wheat_shed = state.get_shed_count("WHEAT")
        wheat_to_sell = wheat_shed if day >= self.config.liquidation_day else max(0, wheat_shed - wheat_reserve)
        if wheat_to_sell > 0 and len(builder.market_orders) < 8:
            builder.sell("WHEAT", wheat_to_sell)
            revenue = wheat_to_sell * state.get_price("WHEAT")
            self.realized_revenue["WHEAT"] = self.realized_revenue.get("WHEAT", 0.0) + revenue

        # 3. Workforce Hiring (Staggered across Hours 0 and 1 to support up to 12 hands within 10 orders/turn limit)
        desired_hands = self._desired_hands(state)
        current_hands = len(hands)
        if state.hour in self.config.workforce_ramp_hours and current_hands < desired_hands and cash >= 5.0:
            hires_needed = desired_hands - current_hands
            available_slots = max(0, 10 - len(builder.market_orders))
            max_hires = min(hires_needed, available_slots)
            for _ in range(max_hires):
                builder.hire()

        # 4. Market Purchases (Day 0 Turn 1 Opening vs Ongoing)
        if state.step == 0:
            # Universal Day 1 Opening: 5 Hands, 2 Cows ($800), 2 Sheep ($1000), 10 Wheat feed ($250), 10 Wheat seeds ($100), 8 Melon seeds ($640)
            builder.buy_animal("COW", self.config.opening_cows)
            builder.buy_animal("SHEEP", self.config.opening_sheep)
            builder.buy_product("WHEAT", self.config.opening_wheat_feed)
            builder.buy_seed("WHEAT", self.config.opening_wheat_seeds)
            builder.buy_seed("MELON", self.config.opening_melon_seeds)
            cash -= (800.0 + 1000.0 + 250.0 + 100.0 + 640.0)
        elif day > 1:
            # Livestock Acquisition Scaling
            target_cows = 2
            target_sheep = 2
            if day >= 4:
                target_cows = 3
                target_sheep = 3
            if self.owned_quadrants >= 2:
                target_cows = 6 if self.owned_quadrants < 3 and day < 12 else 8
                target_sheep = 3
            if self.owned_quadrants >= 3:
                target_cows = min(self.config.target_cows, 14)
                target_sheep = min(self.config.target_sheep, 4)

            # When saving for Q2 on days 8-12, protect a cash reserve of $2,000 for Q2
            land_reserve = 0.0
            if self.owned_quadrants == 2 and 8 <= day <= 14:
                land_reserve = max(0.0, 2000.0 - cash)

            # Buy Cows
            cow_reserve = 150.0 if self.owned_quadrants >= 3 else (400.0 + land_reserve)
            if day <= 22 and pasture_count >= 2 and animal_counts["COW"] < target_cows and cash >= 400.0 + cow_reserve and len(builder.market_orders) < 9:
                qty = min(target_cows - animal_counts["COW"], max(1, int((cash - cow_reserve) // 400.0)), 3)
                if qty > 0:
                    builder.buy_animal("COW", qty)
                    cash -= qty * 400.0

            # Buy Sheep
            sheep_reserve = 150.0 if self.owned_quadrants >= 3 else (500.0 + land_reserve)
            if day <= 22 and pasture_count >= 4 and animal_counts["SHEEP"] < target_sheep and cash >= 500.0 + sheep_reserve and len(builder.market_orders) < 9:
                qty = min(target_sheep - animal_counts["SHEEP"], max(1, int((cash - sheep_reserve) // 500.0)), 2)
                if qty > 0:
                    builder.buy_animal("SHEEP", qty)
                    cash -= qty * 500.0

            # Feed buffer management (Buy Wheat product if buffer is low)
            wheat_total = self._inventory_total(state, "WHEAT") + crop_counts.get("WHEAT", 0) * 2
            wheat_need = max(self.config.min_feed_buffer, len(animal_tiles) * self.config.feed_buffer_multiplier + 8)
            if day >= 2 and wheat_total < wheat_need and cash >= 60.0 and len(builder.market_orders) < 9:
                qty = min(16, max(2, wheat_need - wheat_total), int((cash - 40.0) // max(1.0, state.get_price("WHEAT"))))
                if qty > 0:
                    builder.buy_product("WHEAT", qty)
                    cash -= qty * state.get_price("WHEAT")

            # Seed Purchasing
            virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
            open_slots = sum(1 for p in crop_tiles if state.get_tile(p[0], p[1]) is None)
            deficits = {
                crop: max(0, crop_targets.get(crop, 0) - crop_counts.get(crop, 0) - virtual_seeds.get(crop, 0))
                for crop in CROPS.keys()
            }
            seed_reserve = 50.0 if self.owned_quadrants >= 3 else (150.0 + land_reserve)
            if day <= self.config.stop_planting_day:
                for crop in ("STRAWBERRY", "MELON", "WHEAT", "CARROT"):
                    if open_slots <= 0 or len(builder.market_orders) >= 9:
                        break
                    qty = min(deficits.get(crop, 0), open_slots, 20)
                    cost = CROPS[crop]["seed"] * qty
                    if qty > 0 and cash >= cost + seed_reserve:
                        builder.buy_seed(crop, qty)
                        cash -= cost
                        virtual_seeds[crop] += qty
                        open_slots -= qty

        # 5. Dispatch Worker Actions
        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        virtual_crop_counts = self._crop_counts(state)
        reserved: Set[Tuple[int, int]] = set()

        unit_positions = [state.farmer_position] + hands
        unit_actions = [
            self._worker_action(
                state, pos, worker_id, crop_tiles, pasture_targets, reserved, virtual_seeds, virtual_crop_counts
            )
            for worker_id, pos in enumerate(unit_positions)
        ]
        builder.farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        for act in unit_actions[1:]:
            builder.add_hand_action(act)

        return builder.build()

# ==========================================
# --- Kaggle Entrypoint ---
# ==========================================
_antigravity_config = AntigravityConfig()
_antigravity_agent = AntigravityROIAgent(config=_antigravity_config)

def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point for Antigravity Independent Strategy Agent."""
    try:
        state = GameState(observation)
        return _antigravity_agent.act(state)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
