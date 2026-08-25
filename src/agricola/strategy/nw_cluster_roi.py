"""NW Cluster Scaling Strategy Agent (NWClusterROIAgent).

Scales MultiTileROIAgent from a 4-tile cluster (2x2) to a compact 9-tile cluster (3x3)
in the initial unlocked NW quadrant:
{(4,4), (4,3), (4,2), (3,4), (3,3), (3,2), (2,4), (2,3), (2,2)}.

Preserves E03 economic strategy (ROI/day crop selection and immediate liquidation)
and spatial task prioritization (HARVEST > PLANT > WATER) with Manhattan routing.
"""

from typing import Dict, Any, List, Tuple, Optional
from agricola.core.state import GameState, CROPS
from agricola.core.actions import ActionBuilder


DEFAULT_NW_9_TILES: Tuple[Tuple[int, int], ...] = (
    (4, 4), (4, 3), (4, 2),
    (3, 4), (3, 3), (3, 2),
    (2, 4), (2, 3), (2, 2),
)


class NWClusterROIAgent:
    """Agent managing multi-tile farming on a compact 3x3 grid cluster (9 tiles) using ROI crop selection."""

    def __init__(
        self,
        default_crop: str = "CARROT",
        managed_tiles: Tuple[Tuple[int, int], ...] = DEFAULT_NW_9_TILES,
    ):
        self.default_crop = default_crop
        self.managed_tiles = list(managed_tiles)

    def calculate_net_profit_per_day(self, crop_name: str, state: GameState) -> float:
        """Calculate expected net profit per day for a given crop using E02/E03 formula.
        
        Formula: (SellPrice * Yield - SeedPrice) / Days
        where Yield = 2.0.
        """
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

    def act(self, state: GameState) -> Dict[str, Any]:
        """Compute action dictionary for current state."""
        actions = ActionBuilder()

        # 1. Market Phase: Sell ANY harvested crops in shed immediately
        for crop_name in CROPS.keys():
            shed_count = state.get_shed_count(crop_name)
            if shed_count > 0:
                actions.sell(crop_name, shed_count)

        # 2. Select highest ROI crop
        target_crop = self.select_best_crop(state)
        target_crop_info = CROPS[target_crop]
        target_seed_cost = target_crop_info["seed"]

        # Count empty managed tiles and identify candidates
        empty_managed_tiles: List[Tuple[int, int]] = []
        harvest_candidate_tiles: List[Tuple[int, int]] = []
        water_candidate_tiles: List[Tuple[int, int]] = []

        for pos in self.managed_tiles:
            tile = state.get_tile(pos[0], pos[1])
            if tile is None:
                empty_managed_tiles.append(pos)
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                crop = tile.get("crop", target_crop)
                crop_info = CROPS.get(crop, target_crop_info)
                age = state.day - tile.get("planted_day", state.day)
                max_yield_day = crop_info["max_yield_day"]

                if age >= max_yield_day:
                    harvest_candidate_tiles.append(pos)
                elif not tile.get("watered_today", False):
                    water_candidate_tiles.append(pos)

        # Market Order for Seeds: Buy seeds matched to empty managed tiles count
        target_seeds_owned = state.get_seed_count(target_crop)
        needed_seeds = max(0, len(empty_managed_tiles) - target_seeds_owned)

        if needed_seeds > 0 and state.money >= target_seed_cost:
            buy_qty = min(needed_seeds, int(state.money // target_seed_cost))
            if buy_qty > 0:
                actions.buy_seed(target_crop, buy_qty)
                target_seeds_owned += buy_qty

        # 3. Spatial Priority Task Hierarchy (HARVEST > PLANT > WATER)
        curr_pos = state.farmer_position
        target_pos: Optional[Tuple[int, int]] = None
        task: Optional[str] = None

        def select_nearest(candidates: List[Tuple[int, int]]) -> Tuple[int, int]:
            # Sort by (Manhattan distance, y, x) for deterministic tie-breaking
            return min(
                candidates,
                key=lambda p: (abs(p[0] - curr_pos[0]) + abs(p[1] - curr_pos[1]), p[1], p[0]),
            )

        if harvest_candidate_tiles:
            target_pos = select_nearest(harvest_candidate_tiles)
            task = "HARVEST"
        elif empty_managed_tiles and target_seeds_owned > 0:
            target_pos = select_nearest(empty_managed_tiles)
            task = "PLANT"
        elif water_candidate_tiles:
            target_pos = select_nearest(water_candidate_tiles)
            task = "WATER"

        # 4. Action Execution
        if target_pos is None:
            actions.pass_turn()
        elif target_pos == curr_pos:
            if task == "HARVEST":
                actions.harvest()
            elif task == "PLANT":
                if target_seeds_owned > 0:
                    actions.plant(target_crop)
                else:
                    # Fallback to plant any owned seed
                    planted = False
                    for alt_crop in CROPS.keys():
                        if state.get_seed_count(alt_crop) > 0:
                            actions.plant(alt_crop)
                            planted = True
                            break
                    if not planted:
                        actions.pass_turn()
            elif task == "WATER":
                actions.water()
            else:
                actions.pass_turn()
        else:
            # Move 1 step towards target_pos
            step_dir = self._get_step_direction(curr_pos, target_pos)
            if step_dir != "PASS":
                actions.move(step_dir)
            else:
                actions.pass_turn()

        return actions.build()
