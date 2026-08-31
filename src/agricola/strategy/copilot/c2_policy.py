from __future__ import annotations

import math


from typing import Any, Dict, List, Optional, Tuple

from agricola.core.state import CROPS
from agricola.strategy.copilot.c2_config import CopilotC2Config


Position = Tuple[int, int]


class CopilotC2Policy:
    """Prevention-first crop policy sized to the serviceable NW working set."""

    def __init__(self, config: Optional[CopilotC2Config] = None):
        self.config = config or CopilotC2Config()

    def _crop_rule(self, crop_name: str) -> Optional[Dict[str, Any]]:
        return CROPS.get(str(crop_name).upper())

    def is_harvest_ready(self, tile: Dict[str, Any], current_day: int) -> bool:
        if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
            return False
        crop_rule = self._crop_rule(str(tile.get("crop", "")).upper())
        if crop_rule is None or int(tile.get("yield_units", 0) or 0) <= 0:
            return False
        planted_day = tile.get("planted_day")
        return planted_day is not None and (
            int(current_day) - int(planted_day) >= int(crop_rule["first_yield_day"])
        )

    def classify_tile_lifecycle(
        self, pos: Position, tile: Any, current_day: int, engine_step: int
    ) -> str:
        if pos is None or tile == "LOCKED":
            return "OUT_OF_SCOPE"
        if tile is None or (isinstance(tile, dict) and tile.get("kind") == "EMPTY"):
            return "EMPTY_AVAILABLE"
        if isinstance(tile, dict) and tile.get("kind") == "WEED":
            return "LOST_WEED"
        if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
            return "OUT_OF_SCOPE"
        if self.is_harvest_ready(tile, current_day):
            return "HARVEST_READY"
        if (
            int(tile.get("yield_units", 0) or 0) == 0
            and tile.get("max_lifespan_step") is not None
            and int(tile["max_lifespan_step"]) >= 0
            and engine_step >= int(tile["max_lifespan_step"])
        ):
            return "RETIREMENT_DUE"
        return "GROWING"

    def _safe_private(self, obs: Dict[str, Any], player_index: int) -> Dict[str, Any]:
        private = obs.get("private", {})
        if isinstance(private, dict):
            return private
        if isinstance(private, list) and 0 <= player_index < len(private):
            item = private[player_index]
            return item if isinstance(item, dict) else {}
        return {}

    @staticmethod
    def _tile_at(tiles: List[List[Any]], pos: Position) -> Any:
        x, y = pos
        if not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])):
            return "LOCKED"
        return tiles[y][x]

    def _working_positions(self, tiles: List[List[Any]]) -> List[Position]:
        # The active working set is every owned (non-locked) tile across all
        # unlocked quadrants, not just the initial NW 25-tile footprint. This
        # was corrected under E-C2-PERF-01: performance verification showed the
        # candidate was structurally capped at 25 tiles regardless of land
        # purchases, because this filter previously restricted x<=4,y<=4.
        return [
            (x, y)
            for y, row in enumerate(tiles)
            for x, tile in enumerate(row)
            if tile != "LOCKED"
        ]

    @staticmethod
    def _distance(origin: Position, target: Position) -> int:
        return abs(origin[0] - target[0]) + abs(origin[1] - target[1])

    @staticmethod
    def _move_toward(origin: Position, target: Position) -> List[str]:
        ox, oy = origin
        tx, ty = target
        if tx < ox:
            return ["WEST"]
        if tx > ox:
            return ["EAST"]
        if ty < oy:
            return ["NORTH"]
        if ty > oy:
            return ["SOUTH"]
        return ["PASS"]

    def _task_action(self, tile: Any, current_day: int, engine_step: int) -> List[str]:
        state = self.classify_tile_lifecycle((0, 0), tile, current_day, engine_step)
        if state in {"LOST_WEED", "RETIREMENT_DUE"}:
            return ["DIG"]
        if state == "HARVEST_READY":
            return ["HARVEST"]
        if isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile.get("watered_today") is False:
            return ["WATER"]
        return ["PASS"]

    def _task_targets(
        self, tiles: List[List[Any]], current_day: int, engine_step: int, seed_count: int
    ) -> List[Tuple[Position, List[str]]]:
        positions = self._working_positions(tiles)
        targets: List[Tuple[Position, List[str]]] = []
        for predicate, action in (
            (lambda tile: self.is_harvest_ready(tile, current_day), ["HARVEST"]),
            (
                lambda tile: isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("watered_today") is False,
                ["WATER"],
            ),
            (
                lambda tile: self.classify_tile_lifecycle(
                    (0, 0), tile, current_day, engine_step
                )
                in {"LOST_WEED", "RETIREMENT_DUE"},
                ["DIG"],
            ),
        ):
            targets.extend((pos, action) for pos in positions if predicate(self._tile_at(tiles, pos)))

        if current_day <= self.config.last_plant_day:
            plant_positions = [pos for pos in positions if self._tile_at(tiles, pos) is None]
            plant_positions.sort(
                key=lambda pos: (self._distance((4, 4), pos), pos[1], pos[0])
            )
            targets.extend(
                (pos, ["PLANT", self.config.default_crop])
                for pos in plant_positions[:seed_count]
            )
        return targets

    def _assign_targets(
        self, workers: List[Position], targets: List[Tuple[Position, List[str]]]
    ) -> List[Optional[Tuple[Position, List[str]]]]:
        remaining = list(targets)
        assignments: List[Optional[Tuple[Position, List[str]]]] = []
        for worker in workers:
            if not remaining:
                assignments.append(None)
                continue
            index, target = min(
                enumerate(remaining),
                key=lambda item: (
                    self._distance(worker, item[1][0]),
                    item[1][0][1],
                    item[1][0][0],
                ),
            )
            assignments.append(target)
            del remaining[index]
        return assignments

    def _quadrants_owned(self, farm: Dict[str, Any]) -> int:
        quads = farm.get("unlocked_quadrants", ["NW"])
        return len(quads) if isinstance(quads, list) else int(quads or 1)

    # Land price ladder observed empirically on the frozen engine: 1000 for the
    # 2nd quadrant (NE), 2000 for the 3rd (SW/SE depending on engine ordering).
    # The engine currently exposes at most 3 unlockable additional quadrants
    # beyond the starting NW (see Section 5/7 of the MODEL_SPEC revision).
    _LAND_PRICE_LADDER = (1000.0, 2000.0, 4000.0)

    def _next_land_cost(self, farm: Dict[str, Any]) -> Optional[float]:
        owned = self._quadrants_owned(farm)
        extra_owned = max(0, owned - 1)
        if extra_owned >= len(self._LAND_PRICE_LADDER):
            return None
        return self._LAND_PRICE_LADDER[extra_owned]

    def _target_workforce(self, active_tile_count: int) -> int:
        # Workforce is derived from the active (non-locked) footprint rather
        # than fixed to a historical constant (E-C2-PERF-02): oversized
        # workforce against a static 25-tile footprint produced ~31% idle
        # PASS actions in the 720-step performance benchmark.
        demand = math.ceil(active_tile_count / max(1.0, self.config.target_tiles_per_worker))
        return max(self.config.min_workforce, min(self.config.target_workforce, demand))

    def market_orders(
        self,
        farm: Dict[str, Any],
        private: Dict[str, Any],
        tiles: List[List[Any]],
        current_day: int = 0,
    ) -> List[List[Any]]:
        orders: List[List[Any]] = []
        shed = private.get("shed", {}) if isinstance(private.get("shed", {}), dict) else {}
        crop = self.config.default_crop
        quantity = int(shed.get(crop, 0) or 0)
        if quantity > 0:
            orders.append(["SELL", crop, quantity])

        active_or_empty = len(self._working_positions(tiles))
        cash = float(farm.get("money", 0.0))

        # Land expansion (E-C2-PERF-01): buy the next quadrant once the current
        # working set is materially saturated and a cash reserve survives the
        # purchase, so capital is not permanently stranded on a static 25-tile
        # footprint for the whole episode. Gated by an endgame cutoff
        # (E-C2-PERF-03): a purchase this late cannot be monetized before the
        # terminal day (no plant->grow->harvest cycle can complete), so it
        # would only strand capital.
        if self.config.enable_land_expansion and current_day <= self.config.last_land_purchase_day:
            land_cost = self._next_land_cost(farm)
            if (
                land_cost is not None
                and cash >= land_cost + self.config.land_expansion_reserve
            ):
                orders.append(["BUY_LAND"])

        hands = farm.get("hands", []) if isinstance(farm.get("hands", []), list) else []
        target_workforce = self._target_workforce(active_or_empty)
        hires_needed = max(0, target_workforce - 1 - len(hands))
        orders.extend([["HIRE"] for _ in range(hires_needed)])

        seeds = private.get("seeds", {}) if isinstance(private.get("seeds", {}), dict) else {}
        available = int(seeds.get(crop, 0) or 0)
        deficit = max(0, active_or_empty + self.config.seed_reserve - available)
        affordable = int(cash // int(CROPS[crop]["seed"]))
        if deficit and affordable:
            orders.append(["BUY_SEED", crop, min(deficit, affordable)])
        return orders[:10]

    def decide_actions(self, obs: Dict[str, Any], player_index: int = 0) -> List[List[str]]:
        farms = obs.get("farms", [])
        farm = farms[player_index] if isinstance(farms, list) and 0 <= player_index < len(farms) else {}
        if not isinstance(farm, dict):
            return [["PASS"]]
        tiles = farm.get("tiles", []) if isinstance(farm.get("tiles", []), list) else []
        private = self._safe_private(obs, player_index)
        seeds = private.get("seeds", {}) if isinstance(private.get("seeds", {}), dict) else {}
        crop_seed_count = int(seeds.get(self.config.default_crop, 0) or 0)
        current_day = int(obs.get("day", 0))
        engine_step = int(obs.get("step", 0))

        raw_workers = [farm.get("farmer", [4, 4]), *(farm.get("hands", []) or [])]
        workers = [
            (int(position[0]), int(position[1]))
            for position in raw_workers
            if isinstance(position, list) and len(position) >= 2
        ]
        targets = self._task_targets(tiles, current_day, engine_step, crop_seed_count)
        actions = []
        for worker, assignment in zip(workers, self._assign_targets(workers, targets)):
            if assignment is None:
                actions.append(["PASS"])
                continue
            target, target_action = assignment
            actions.append(target_action if worker == target else self._move_toward(worker, target))
        return actions or [["PASS"]]

    def decide(self, obs: Dict[str, Any], player_index: int) -> Dict[str, Any]:
        farms = obs.get("farms", [])
        farm = farms[player_index] if isinstance(farms, list) and 0 <= player_index < len(farms) else {}
        private = self._safe_private(obs, player_index)
        tiles = farm.get("tiles", []) if isinstance(farm, dict) else []
        current_day = int(obs.get("day", 0))
        actions = self.decide_actions(obs, player_index)
        return {
            "farmer": actions[0],
            "hands": actions[1:],
            "market": self.market_orders(farm, private, tiles, current_day) if isinstance(farm, dict) else [],
        }
