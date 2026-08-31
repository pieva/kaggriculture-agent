"""
Standalone submission file for Kaggle Kaggriculture.
Generated automatically from frozen Antigravity C2 Candidate (C2 Performance Iteration).
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any, Dict, List, Optional, Set, Tuple

# ==========================================
# --- Antigravity C2 Configuration ---
# ==========================================
"""Configuration for Antigravity C2 Model Strategy."""



@dataclass
class AntigravityC2Config:
    """Parametric configuration for Antigravity C2 Strategy Model."""

    # Land & Layout
    quadrants_owned: int = 2
    crop_working_set_target: int = 40
    pasture_allocation_target: int = 0
    livestock_headcount_target: int = 0
    livestock_species: str = "COW"

    # Workforce
    workforce_headcount: int = 10
    operating_cash_floor: float = 50.0
    endgame_shutdown_steps: int = 48

    # Lifecycle Gates & Policies
    enable_strict_harvest_gate: bool = True
    enable_recovery_dig: bool = True
    enable_preventive_dig: bool = True
    enable_day0_water_priority: bool = True

    # Crop Quotas
    crop_mix_weights: Dict[str, float] = field(
        default_factory=lambda: {"WHEAT": 0.20, "STRAWBERRY": 0.45, "MELON": 0.35}
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary representation."""
        return {
            "quadrants_owned": self.quadrants_owned,
            "crop_working_set_target": self.crop_working_set_target,
            "pasture_allocation_target": self.pasture_allocation_target,
            "livestock_headcount_target": self.livestock_headcount_target,
            "livestock_species": self.livestock_species,
            "workforce_headcount": self.workforce_headcount,
            "operating_cash_floor": self.operating_cash_floor,
            "endgame_shutdown_steps": self.endgame_shutdown_steps,
            "enable_strict_harvest_gate": self.enable_strict_harvest_gate,
            "enable_recovery_dig": self.enable_recovery_dig,
            "enable_preventive_dig": self.enable_preventive_dig,
            "enable_day0_water_priority": self.enable_day0_water_priority,
            "crop_mix_weights": dict(self.crop_mix_weights),
        }

# ==========================================
# --- Antigravity C2 Decision Policy ---
# ==========================================
"""Antigravity C2 Policy Implementation.

Implements the C2 Model Foundation specification for Antigravity:
- Strict harvest readiness gate (CRP-10) with biological max-yield maturity gating.
- Tile lifecycle classification (CRP-09) supporting 6 discrete states.
- Preventive and recovery DIG actions for working-set maintenance.
- Day-0 and urgent EOD water prioritization (100% daily watering compliance).
- Dynamic biological end-of-season rotation (Melon -> Wheat past Day 18, Strawberry -> Wheat past Day 20).
- Robust liquidity & hiring priority protecting daily workforce and maximizing gross revenue.
"""




CROPS: Dict[str, Dict[str, Any]] = {
    "WHEAT": {"first_yield_day": 2, "max_yield_day": 4, "interval": 0, "ongoing": False, "max_yield": 6, "seed": 10},
    "CARROT": {"first_yield_day": 2, "max_yield_day": 3, "interval": 0, "ongoing": False, "max_yield": 4, "seed": 20},
    "TOMATO": {"first_yield_day": 8, "max_yield_day": 8, "interval": 1, "ongoing": True, "max_yield": 4, "seed": 50},
    "STRAWBERRY": {"first_yield_day": 10, "max_yield_day": 10, "interval": 2, "ongoing": True, "max_yield": 4, "seed": 100},
    "MELON": {"first_yield_day": 10, "max_yield_day": 12, "interval": 0, "ongoing": False, "max_yield": 6, "seed": 80},
}


def _get_private(observation: Dict[str, Any], player_index: int = 0) -> Dict[str, Any]:
    """Extract private dictionary robustly whether provided as dict, Struct, or list."""
    raw_private = observation.get("private", {})
    if isinstance(raw_private, dict):
        return raw_private
    if isinstance(raw_private, list):
        if 0 <= player_index < len(raw_private) and isinstance(raw_private[player_index], dict):
            return raw_private[player_index]
        return {}
    return {}

SEED_COSTS: Dict[str, float] = {
    "WHEAT": 10.0,
    "STRAWBERRY": 100.0,
    "MELON": 80.0,
    "CARROT": 10.0,
    "TOMATO": 50.0,
}

SHED_TILES: Set[Tuple[int, int]] = {(4, 4), (5, 4), (4, 5), (5, 5)}
# 46 farmable crop positions in Quadrant 0 (NW) and Quadrant 1 (NE), sorted by Manhattan distance to central shed
CROP_POSITIONS: Tuple[Tuple[int, int], ...] = (
    # Distance 1
    (3, 4), (4, 3), (5, 3), (6, 4),
    # Distance 2
    (2, 4), (3, 3), (4, 2), (5, 2), (6, 3), (7, 4),
    # Distance 3
    (1, 4), (2, 3), (3, 2), (4, 1), (5, 1), (6, 2), (7, 3), (8, 4),
    # Distance 4
    (0, 4), (1, 3), (2, 2), (3, 1), (4, 0), (5, 0), (6, 1), (7, 2), (8, 3), (9, 4),
    # Distance 5
    (0, 3), (1, 2), (2, 1), (3, 0), (6, 0), (7, 1), (8, 2), (9, 3),
    # Distance 6
    (0, 2), (1, 1), (2, 0), (7, 0), (8, 1), (9, 2),
    # Distance 7
    (0, 1), (1, 0), (8, 0), (9, 1),
    # Distance 8
    (0, 0), (9, 0),
)
PASTURE_POSITIONS: Tuple[Tuple[int, int], ...] = tuple(
    (x, y) for y in (3, 4) for x in range(10) if (x, y) not in {(4, 4), (5, 4)}
)


def _fib(index: int) -> int:
    a, b = 1, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def _distance(left: Tuple[int, int], right: Tuple[int, int]) -> int:
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def _move_towards(position: Tuple[int, int], target: Tuple[int, int]) -> List[str]:
    x, y = position
    tx, ty = target
    if x < tx:
        return ["EAST"]
    if x > tx:
        return ["WEST"]
    if y < ty:
        return ["SOUTH"]
    if y > ty:
        return ["NORTH"]
    return ["PASS"]


def _quota_counts(target: int, weights: Dict[str, float]) -> Dict[str, int]:
    raw = {crop: target * weight for crop, weight in weights.items()}
    counts = {crop: math.floor(value) for crop, value in raw.items()}
    remaining = target - sum(counts.values())
    order = sorted(
        weights.keys(),
        key=lambda c: (-(raw[c] - counts[c]), list(weights.keys()).index(c)),
    )
    for crop in order[:remaining]:
        counts[crop] += 1
    return counts


def _crop_plan(target: int, weights: Dict[str, float]) -> Dict[Tuple[int, int], str]:
    quotas = _quota_counts(target, weights)
    cycle: List[str] = []
    crops_list = list(weights.keys())
    while len(cycle) < target:
        for crop in crops_list:
            if quotas[crop] > 0:
                cycle.append(crop)
                quotas[crop] -= 1
    return {position: crop for position, crop in zip(CROP_POSITIONS[:target], cycle)}


def _inventory_total(inventory: Dict[str, int]) -> int:
    return sum(int(v) for v in inventory.values())


class AntigravityC2Policy:
    """Antigravity C2 Decision Policy."""

    def __init__(self, config: Optional[AntigravityC2Config] = None):
        self.config = config or AntigravityC2Config()
        self.crop_plan = _crop_plan(
            self.config.crop_working_set_target, self.config.crop_mix_weights
        )

    def is_harvest_ready(self, tile: Any, current_day: int) -> bool:
        """Evaluate canonical CRP-10 harvest_ready predicate with max-yield gating."""
        if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
            return False
        yield_units = int(tile.get("yield_units", 0))
        if yield_units <= 0:
            return False
        crop = tile.get("crop", "WHEAT")
        planted_day = int(tile.get("planted_day", 0))
        rule = CROPS.get(crop, {})
        ongoing = rule.get("ongoing", False)
        max_yield_day = rule.get("max_yield_day", 2)
        first_yield_day = rule.get("first_yield_day", 2)
        max_yield = rule.get("max_yield", 4)

        if ongoing:
            return (current_day - planted_day) >= first_yield_day
        else:
            return yield_units >= max_yield or (current_day - planted_day) >= max_yield_day or current_day >= 28

    def classify_tile_lifecycle(
        self,
        position: Tuple[int, int],
        tile: Any,
        current_day: int,
        engine_step: int,
    ) -> str:
        """Classify tile into one of the 6 canonical lifecycle states (CRP-09)."""
        if position not in self.crop_plan:
            return "OUT_OF_SCOPE"
        if tile is None:
            return "EMPTY_ASSIGNED"
        if isinstance(tile, dict):
            kind = tile.get("kind")
            if kind == "WEED":
                return "LOST_WEED"
            if kind == "PLANT":
                crop = tile.get("crop", "WHEAT")
                rule = CROPS.get(crop, {})
                is_ongoing = rule.get("ongoing", False)
                yield_units = int(tile.get("yield_units", 0))
                max_lifespan_step = tile.get("max_lifespan_step")

                # Check if retired ongoing crop
                if is_ongoing:
                    if (
                        yield_units == 0
                        and max_lifespan_step is not None
                        and int(max_lifespan_step) >= 0
                        and engine_step >= int(max_lifespan_step)
                    ):
                        return "RETIREMENT_DUE"
                else:
                    planted_day = int(tile.get("planted_day", 0))
                    first_yield_day = rule.get("first_yield_day", 2)
                    if yield_units == 0 and (current_day - planted_day) > first_yield_day:
                        return "RETIREMENT_DUE"

                # Check harvest readiness
                if self.is_harvest_ready(tile, current_day):
                    return "HARVEST_READY"

                return "GROWING"
        return "OUT_OF_SCOPE"

    def _tile(self, farm: Dict[str, Any], position: Tuple[int, int]) -> Any:
        x, y = position
        tiles = farm.get("tiles", [])
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return "LOCKED"

    def _target_action(
        self,
        worker_pos: Tuple[int, int],
        candidates: List[Tuple[Tuple[int, int], List[str]]],
        reserved: Set[Tuple[int, int]],
    ) -> Optional[List[str]]:
        """Assign best target minimizing Manhattan distance with target reservation."""
        available = [item for item in candidates if item[0] not in reserved]
        if not available:
            return None
        target_pos, action_cmd = min(
            available, key=lambda item: _distance(worker_pos, item[0])
        )
        reserved.add(target_pos)
        if worker_pos == target_pos:
            return action_cmd
        return _move_towards(worker_pos, target_pos)

    def decide_actions(
        self,
        observation: Dict[str, Any],
        player_index: int = 0,
    ) -> List[List[str]]:
        """Generate unit actions for main farmer and all farm hands."""
        farms = observation.get("farms", [])
        if player_index >= len(farms):
            return [["PASS"]]
        farm = farms[player_index]
        private = _get_private(observation, player_index)

        current_step = int(observation.get("step", 0))
        current_day = int(observation.get("day", 0))
        turns_per_day = int(observation.get("turnsPerDay", 24))
        current_hour = int(observation.get("hour", current_step % turns_per_day))
        max_steps = int(observation.get("max_steps", 720))
        shutdown = (max_steps - current_step) <= self.config.endgame_shutdown_steps
        allow_plant = not shutdown and (turns_per_day - 1 - current_hour) >= 2

        farmer_pos = tuple(farm.get("farmer", [4, 4]))
        hands_raw = farm.get("hands", [])
        hands_positions = [tuple(h) for h in hands_raw]
        all_positions: List[Tuple[int, int]] = [farmer_pos] + hands_positions

        inventories_raw = private.get("inventories", []) or []
        inventories: List[Dict[str, int]] = []
        for idx in range(len(all_positions)):
            if idx < len(inventories_raw) and isinstance(inventories_raw[idx], dict):
                inventories.append(inventories_raw[idx])
            else:
                inventories.append({})

        seeds = private.get("seeds", {}) or {}
        available_seeds = {k: int(v) for k, v in seeds.items()}

        # Task buckets
        water_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        harvest_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        plant_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        dig_targets: List[Tuple[Tuple[int, int], List[str]]] = []

        # Scan working set crop positions
        unlocked = farm.get("unlocked_quadrants", ["NW"])
        quad_count = len(unlocked) if isinstance(unlocked, list) else int(unlocked)
        effective_crop_target = min(
            self.config.crop_working_set_target, len(self.crop_plan)
        ) if quad_count >= 2 else 10

        for pos, planned_crop in list(self.crop_plan.items())[:effective_crop_target]:
            tile = self._tile(farm, pos)
            state = self.classify_tile_lifecycle(pos, tile, current_day, current_step)

            if state == "LOST_WEED":
                if self.config.enable_recovery_dig and not shutdown:
                    dig_targets.append((pos, ["DIG"]))
            elif state == "RETIREMENT_DUE":
                if self.config.enable_preventive_dig and not shutdown:
                    dig_targets.append((pos, ["DIG"]))
            elif state == "HARVEST_READY":
                harvest_targets.append((pos, ["HARVEST"]))
                if isinstance(tile, dict) and not tile.get("watered_today", False):
                    water_targets.append((pos, ["WATER"]))
            elif state == "GROWING":
                if isinstance(tile, dict) and not tile.get("watered_today", False):
                    water_targets.append((pos, ["WATER"]))
            elif state == "EMPTY_ASSIGNED":
                if allow_plant:
                    actual_crop = planned_crop
                    if actual_crop == "MELON" and current_day > 18:
                        actual_crop = "WHEAT"
                    elif actual_crop == "STRAWBERRY" and current_day > 20:
                        actual_crop = "WHEAT"

                    if available_seeds.get(actual_crop, 0) > 0:
                        plant_targets.append((pos, ["PLANT", actual_crop]))
                        available_seeds[actual_crop] -= 1
                    elif available_seeds.get("WHEAT", 0) > 0 and current_day < 26:
                        plant_targets.append((pos, ["PLANT", "WHEAT"]))
                        available_seeds["WHEAT"] -= 1

        # Dispatch actions per worker
        reserved: Set[Tuple[int, int]] = set()
        actions: List[List[str]] = []

        for worker_id, pos in enumerate(all_positions):
            inv = inventories[worker_id]
            total_inv = _inventory_total(inv)

            # 1. Handle carried items: drop at shed immediately
            if total_inv > 0:
                if pos in SHED_TILES:
                    actions.append(["DROP"])
                else:
                    actions.append(_move_towards(pos, (4, 4)))
                continue

            # 2. Action Priority Cascade: Water -> Harvest -> Plant -> Dig
            priority_groups = [
                water_targets,               # P0: 100% daily watering compliance
                harvest_targets,             # P1: Realize mature output
                plant_targets,               # P2: Replant / extend surface
                dig_targets,                 # P3: Clear retired crops & weed tiles
            ]

            action: Optional[List[str]] = None
            for group in priority_groups:
                action = self._target_action(pos, group, reserved)
                if action is not None:
                    break

            actions.append(action or ["PASS"])

        return actions

    def decide_market_orders(
        self,
        observation: Dict[str, Any],
        player_index: int = 0,
    ) -> List[List[Any]]:
        """Generate market transactions (BUY_LAND, BUY_SEED, HIRE, SELL)."""
        farms = observation.get("farms", [])
        if player_index >= len(farms):
            return []
        farm = farms[player_index]
        private = _get_private(observation, player_index)
        shed = private.get("shed", {}) or {}

        current_step = int(observation.get("step", 0))
        current_day = int(observation.get("day", 0))
        max_steps = int(observation.get("max_steps", 720))
        shutdown = (max_steps - current_step) <= self.config.endgame_shutdown_steps

        cash = float(farm.get("money", 0.0))
        floor = self.config.operating_cash_floor
        orders: List[List[Any]] = []

        def add_order(order: List[Any], cost: float = 0.0) -> bool:
            nonlocal cash
            if len(orders) >= 10:
                return False
            if cost > 0 and (cash - cost) < floor:
                return False
            orders.append(order)
            cash -= cost
            return True

        # 1. ALWAYS SELL inventory from shed first to maximize cash liquidity (0 cost)
        for item in ["MILK", "WOOL", "EGG", "MELON", "STRAWBERRY", "CARROT", "TOMATO", "WHEAT"]:
            qty = int(shed.get(item, 0))
            if qty > 0:
                add_order(["SELL", item, qty], 0.0)

        # 2. Workforce hiring ALWAYS prioritized so daily labor capacity is never compromised
        current_hands = len(farm.get("hands", []))
        hires_today = int(farm.get("hires_today", 0))
        needed_hires = max(0, self.config.workforce_headcount - (1 + current_hands))
        for offset in range(needed_hires):
            cost = float(_fib(hires_today + offset))
            if not add_order(["HIRE"], cost):
                break

        # 3. Land expansion to 2 quadrants on Day 0
        unlocked = farm.get("unlocked_quadrants", ["NW"])
        quad_count = len(unlocked) if isinstance(unlocked, list) else int(unlocked)
        if quad_count < self.config.quadrants_owned and not shutdown and cash >= 1000.0 + floor:
            add_order(["BUY_LAND"], 1000.0)

        effective_crop_target = min(
            self.config.crop_working_set_target, len(self.crop_plan)
        ) if quad_count >= 2 else 10

        # 4. Seed purchasing for working set deficit with biological rotation gating
        if not shutdown and current_day < 26:
            active_by_crop: Dict[str, int] = {k: 0 for k in self.config.crop_mix_weights}
            for pos in list(self.crop_plan.keys())[:effective_crop_target]:
                tile = self._tile(farm, pos)
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    c = tile.get("crop", "WHEAT")
                    if c in active_by_crop:
                        active_by_crop[c] += 1

            quotas = _quota_counts(
                effective_crop_target, self.config.crop_mix_weights
            )
            # Biological season cutoffs
            if current_day > 18:
                quotas["WHEAT"] = quotas.get("WHEAT", 0) + quotas.get("MELON", 0)
                quotas["MELON"] = 0
            if current_day > 20:
                quotas["WHEAT"] = quotas.get("WHEAT", 0) + quotas.get("STRAWBERRY", 0)
                quotas["STRAWBERRY"] = 0

            seeds = private.get("seeds", {}) or {}
            for crop, quota in quotas.items():
                in_seed = int(seeds.get(crop, 0))
                active = active_by_crop.get(crop, 0)
                deficit = max(0, quota - active - in_seed)
                if deficit > 0:
                    cost_per_unit = SEED_COSTS.get(crop, 10.0)
                    add_order(["BUY_SEED", crop, deficit], deficit * cost_per_unit)

        return orders

# ==========================================
# --- Antigravity C2 Agent Class ---
# ==========================================
"""Antigravity C2 Strategy Agent.

Callable candidate for the MODEL_SPEC C2 tournament.
"""




class AntigravityC2Agent:
    """Antigravity C2 Tournament Candidate Agent."""

    def __init__(self, config: Optional[AntigravityC2Config] = None):
        self.config = config or AntigravityC2Config()
        self.policy = AntigravityC2Policy(config=self.config)
        self.last_exception: Optional[Exception] = None
        self.error_count: int = 0

    def act(self, observation: Dict[str, Any], player_index: int = 0) -> Dict[str, Any]:
        """Generate action dict for environment."""
        unit_actions = self.policy.decide_actions(observation, player_index=player_index)
        farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        hands_actions = unit_actions[1:] if len(unit_actions) > 1 else []
        market_orders = self.policy.decide_market_orders(observation, player_index=player_index)
        return {
            "farmer": farmer_action,
            "hands": hands_actions,
            "market": market_orders,
        }

    def __call__(
        self,
        observation: Dict[str, Any],
        configuration: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Standard Kaggle-compatible callable entrypoint."""
        try:
            player_index = int(observation.get("player", 0))
            return self.act(observation, player_index=player_index)
        except Exception as exc:
            self.last_exception = exc
            self.error_count += 1
            return {"farmer": ["PASS"], "hands": [], "market": []}

# ==========================================
# --- Kaggle Entrypoint ---
# ==========================================
_agent_instance = AntigravityC2Agent()


def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point for Antigravity C2 Strategy Agent."""
    return _agent_instance(observation, configuration)
