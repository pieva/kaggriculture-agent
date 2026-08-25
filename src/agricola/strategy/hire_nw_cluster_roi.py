"""HIRE Multi-Worker Scaling Strategy Agent (HIRENWClusterROIAgent).

Scales NWClusterROIAgent by introducing 1 daily farm hand via HIRE ($1/day)
with fixed spatial partitioning (4:5) on the 9-tile NW cluster:
- Farmer (4 tiles): {(4,4), (4,3), (3,4), (3,3)}
- Hand 1 (5 tiles): {(4,2), (3,2), (2,4), (2,3), (2,2)}

Preserves E03/E04 economic strategy (ROI/day crop selection and immediate liquidation)
and spatial task prioritization (HARVEST > PLANT > WATER) with Manhattan routing.
"""

from typing import Dict, Any, List, Tuple, Optional
from agricola.core.state import GameState, CROPS
from agricola.core.actions import ActionBuilder


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
