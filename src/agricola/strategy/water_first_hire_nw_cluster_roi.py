"""Water-First Priority Strategy Agent (WaterFirstHIRENWClusterROIAgent).

Subclasses HIRENWClusterROIAgent from E05 to evaluate the single experimental variable:
swapping worker task priority from HARVEST > PLANT > WATER to WATER > HARVEST > PLANT.

All other components (9-tile NW footprint, 1 Farmer + 1 daily Hand at $1/day,
fixed 4:5 spatial partitioning, E03 ROI crop selection, Manhattan routing) remain 100% identical.
"""

from typing import Dict, Any, List, Tuple, Optional
from agricola.core.state import GameState, CROPS
from agricola.strategy.hire_nw_cluster_roi import HIRENWClusterROIAgent, FARMER_4_TILES, HAND1_5_TILES


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
