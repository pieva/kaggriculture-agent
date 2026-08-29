"""
Standalone submission file for Kaggle Kaggriculture.
Generated automatically by scripts/build_submission.py
Strategy: E12-X1.12 Truebelief Economic Engine Reconstruction ProductiveMassROIAgent
"""

from typing import Dict, Any, List, Optional, Tuple, Set

# --- Core State Wrapper ---
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

# --- Shared Config & Telemetry ---
"""HybridLivestockClusterROIAgent — E08 Productive Scale Optimization Agent.

Integrates:
- Productive Scale Expansion to 40 tiles (80% land utilization of 50 owned tiles Q0+Q1)
- Spatial Worker Partitioning Scheme (Workers 0-1 -> Q0, Workers 2-3 -> Q1)
- Cross-Boundary Emergency Water Assist Override
- Staggered Seed Purchasing with $300 liquid cash floor
- 4-Phase Lifecycle Management (OPENING -> SCALE -> PRODUCE -> LIQUIDATE)
- Capital Allocation with liquid cash reserve buffer
- Land Expansion (BUY_LAND Q1, 50-tile tracking)
- Multi-Worker Scaling (1 Farmer + up to 3 Hands hired daily when cash permits)
- Multi-Crop Allocation (6 Wheat FEED, 22 Melon CASH, 12 Carrot FLEX)
- Livestock Engine & Feed Balance Guard (Cows, Sheep, Wheat feed loop)
- Complete Livestock Lifecycle Execution (Farmer BUILD_PASTURE & PLACE, Workers FEED & HARVEST)
- Task Dispatcher (WATER > FEED_ANIMALS > HARVEST > PLANT)
- Market Brokerage (Order cap 10/turn, shed capacity 100, Premium-First queue)
- End-Game Horizon Cutoffs & Inventory Liquidation (No animal/land/structure sales)
- Telemetry & Backlog Instrumentation (water, harvest, plant pending, minimum cash)
"""

from dataclasses import dataclass, field
import math



@dataclass
class CompetitiveConfig:
    """Centralized, open-parameter configuration model for E08 strategy."""
    target_quadrants: int = 2               # Q0=25, Q1=50 tiles total
    expansion_day: int = 12                 # Target day for BUY_LAND Q1 (max D12)
    
    target_productive_tiles: int = 40       # Scaled from 24 to 40 productive crop tiles
    wheat_tiles: int = 6                    # Dedicated FEED crop tiles (1-day growth)
    melon_tiles: int = 22                   # Dedicated CASH crop tiles (12-day growth)
    carrot_tiles: int = 12                  # Dedicated FLEX liquidity crop tiles (3-day growth)
    
    target_cows: int = 4                    # Cow target ($400 cost, Milk product $160)
    target_sheep: int = 2                   # Sheep target ($500 cost, Wool product $200)
    feed_safety_buffer: int = 3             # Min extra Wheat units required in shed/crop
    stop_sheep_buy_day: int = 18            # Cutoff day for Sheep acquisition
    stop_cow_buy_day: int = 20              # Cutoff day for Cow acquisition
    
    target_workers: int = 4                 # Farmer Principal + up to 3 Farm Hands
    minimum_cash_after_hire: float = 200.0  # Min cash float remaining after HIRE
    
    cash_reserve: float = 300.0             # Minimum liquid bank float ($300 floor)
    
    melon_plant_cutoff_day: int = 18        # Day cutoff for Melon planting (12d growth)
    all_plant_cutoff_day: int = 26          # Day cutoff for all crop planting
    inventory_flush_start_day: int = 27     # Day to commence 100% shed inventory flush
    
    spatial_partitioning: bool = True       # Enable spatial worker dispatcher (Q0 vs Q1)
    cross_boundary_water_assist: bool = True # Enable emergency water assist across boundary


class TelemetryLogger:
    """Diagnostic event logger and episode telemetry accumulator."""
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        
        self.starting_money: float = 0.0
        self.final_money: float = 0.0
        self.minimum_cash: float = 999999.0
        
        self.spending_seeds: float = 0.0
        self.spending_workforce: float = 0.0
        self.spending_land: float = 0.0
        self.spending_livestock: float = 0.0
        
        self.realized_revenue: Dict[str, float] = {
            "MILK": 0.0, "WOOL": 0.0, "MELON": 0.0, "CARROT": 0.0, "WHEAT": 0.0, "EGG": 0.0
        }
        
        self.owned_tiles_count: int = 25
        self.configured_crop_tiles_count: int = 40
        self.peak_productive_tiles: int = 0
        self.daily_productive_tiles_history: List[int] = []
        self.buy_land_executed_step: Optional[int] = None
        
        self.q0_owned: int = 25
        self.q0_productive: int = 20
        self.q0_worked: int = 0
        self.q0_harvested: int = 0
        
        self.q1_owned: int = 0
        self.q1_productive: int = 0
        self.q1_worked: int = 0
        self.q1_harvested: int = 0
        
        self.worker_stats: Dict[int, Dict[str, int]] = {
            w: {"productive": 0, "movement": 0, "idle": 0} for w in range(4)
        }
        
        self.hires_count: int = 0
        self.hire_attempted: int = 0
        self.hire_accepted: int = 0
        self.peak_simultaneous_workers: int = 1
        self.worker_days: int = 0
        self.worker_hours: int = 0
        
        self.worker_idle_steps: int = 0
        self.worker_movement_steps: int = 0
        self.worker_action_steps: int = 0
        
        self.crops_planted: int = 0
        self.crops_watered: int = 0
        self.crops_harvested: int = 0
        self.crops_weed_losses: int = 0
        
        self.backlog_history: Dict[str, List[int]] = {
            "needs_water": [],
            "harvest_ready": [],
            "plant_pending": []
        }
        
        self.cows_acquired: int = 0
        self.sheep_acquired: int = 0
        self.pastures_built: int = 0
        self.animals_placed: int = 0
        self.feed_attempted: int = 0
        self.feed_successful: int = 0
        self.feed_consumed: int = 0
        self.missed_feed_events: int = 0
        self.milk_produced: int = 0
        self.wool_produced: int = 0
        self.milk_harvested: int = 0
        self.wool_harvested: int = 0
        
        self.wheat_harvested: int = 0
        self.wheat_bought: int = 0
        self.wheat_fed: int = 0
        
        self.market_orders_placed: int = 0
        self.quantities_sold: Dict[str, int] = {
            "MILK": 0, "WOOL": 0, "MELON": 0, "CARROT": 0, "WHEAT": 0, "EGG": 0
        }
        self.unsold_shed_items: int = 0
        
        self.phase_history: List[Dict[str, Any]] = []

    def log_event(self, event_type: str, step: int, day: int, hour: int, cash: float, details: str):
        evt = {
            "event": event_type,
            "step": step,
            "day": day,
            "hour": hour,
            "cash": cash,
            "details": details
        }
        self.events.append(evt)

    def log_phase_change(self, step: int, day: int, hour: int, old_phase: str, new_phase: str, cash: float):
        entry = {
            "step": step,
            "day": day,
            "hour": hour,
            "from": old_phase,
            "to": new_phase,
            "cash": cash
        }
        self.phase_history.append(entry)
        self.log_event("PHASE_CHANGE", step, day, hour, cash, f"{old_phase} -> {new_phase}")

    def record_worker_step(self, worker_id: int, step_type: str):
        if worker_id not in self.worker_stats:
            self.worker_stats[worker_id] = {"productive": 0, "movement": 0, "idle": 0}
        self.worker_stats[worker_id][step_type] = self.worker_stats[worker_id].get(step_type, 0) + 1
        if step_type == "productive":
            self.worker_action_steps += 1
        elif step_type == "movement":
            self.worker_movement_steps += 1
        elif step_type == "idle":
            self.worker_idle_steps += 1

    def to_dict(self) -> Dict[str, Any]:
        avg_daily_productive = (
            sum(self.daily_productive_tiles_history) / max(1, len(self.daily_productive_tiles_history))
        )
        avg_water_backlog = (
            sum(self.backlog_history["needs_water"]) / max(1, len(self.backlog_history["needs_water"]))
        )
        avg_harvest_backlog = (
            sum(self.backlog_history["harvest_ready"]) / max(1, len(self.backlog_history["harvest_ready"]))
        )
        avg_plant_pending = (
            sum(self.backlog_history["plant_pending"]) / max(1, len(self.backlog_history["plant_pending"]))
        )
        
        return {
            "starting_money": self.starting_money,
            "final_money": self.final_money,
            "minimum_cash": self.minimum_cash if self.minimum_cash < 999999 else 0.0,
            "spending": {
                "seeds": self.spending_seeds,
                "workforce": self.spending_workforce,
                "land": self.spending_land,
                "livestock": self.spending_livestock
            },
            "realized_revenue": self.realized_revenue,
            "land_breakdown": {
                "configured_crop_tiles": self.configured_crop_tiles_count,
                "peak_productive_tiles": self.peak_productive_tiles,
                "mean_daily_productive_tiles": round(avg_daily_productive, 2),
                "q0": {"owned": self.q0_owned, "productive": self.q0_productive, "worked": self.q0_worked, "harvested": self.q0_harvested},
                "q1": {"owned": self.q1_owned, "productive": self.q1_productive, "worked": self.q1_worked, "harvested": self.q1_harvested},
                "buy_land_step": self.buy_land_executed_step
            },
            "workforce": {
                "hires_count": self.hires_count,
                "hire_attempted": self.hire_attempted,
                "hire_accepted": self.hire_accepted,
                "peak_simultaneous_workers": self.peak_simultaneous_workers,
                "worker_stats": self.worker_stats,
                "action_steps": self.worker_action_steps,
                "movement_steps": self.worker_movement_steps,
                "idle_steps": self.worker_idle_steps
            },
            "backlog": {
                "mean_needs_water": round(avg_water_backlog, 2),
                "mean_harvest_ready": round(avg_harvest_backlog, 2),
                "mean_plant_pending": round(avg_plant_pending, 2)
            },
            "crops": {
                "planted": self.crops_planted,
                "watered": self.crops_watered,
                "harvested": self.crops_harvested,
                "weed_losses": self.crops_weed_losses
            },
            "livestock": {
                "cows": self.cows_acquired,
                "sheep": self.sheep_acquired,
                "pastures_built": self.pastures_built,
                "animals_placed": self.animals_placed,
                "feed_attempted": self.feed_attempted,
                "feed_successful": self.feed_successful,
                "feed_consumed": self.feed_consumed,
                "missed_feeds": self.missed_feed_events,
                "milk_harvested": self.milk_harvested,
                "wool_harvested": self.wool_harvested
            },
            "wheat_accounting": {
                "harvested": self.wheat_harvested,
                "bought": self.wheat_bought,
                "fed": self.wheat_fed,
                "sold": self.quantities_sold.get("WHEAT", 0)
            },
            "market": {
                "orders_placed": self.market_orders_placed,
                "quantities_sold": self.quantities_sold,
                "unsold_shed_items": self.unsold_shed_items
            },
            "phase_history": self.phase_history,
            "event_count": len(self.events)
        }

# --- E11 Productive Mass ROI Agent Strategy ---
"""E11 Productive Mass Expansion Strategy (100 tiles, 8-12 workers, Livestock ON).

E11-01: Productive Mass Baseline (protect_expansion_capital=False)
E11-02: Expansion Capital Protection (protect_expansion_capital=True, expansion_gate_mode="LEGACY_SATURATION")
E11-03: Expansion Gate Unlock (protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", capital_release_mode="BINARY")
E11-04: Seed-Expansion Synchronization (protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", capital_release_mode="SYNCHRONIZED")
E11-05: Staged Expansion Capital Release (protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", capital_release_mode="STAGED")
E11-06: Workforce-Land Co-Scaling (protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", capital_release_mode="BINARY", workforce_scaling_mode="LAND_CO_SCALING")
"""

from dataclasses import dataclass, field
import math



@dataclass
class ProductiveMassConfig:
    """Centralized, fully open parameter configuration model for E11 Productive Mass Expansion."""
    # Land & Quadrant Expansion Parameters
    target_quadrants: int = 4                # Q0=25, Q1=50, Q2=75, Q3=100 tiles
    stop_expansion_day: int = 18             # Day after which land expansion is disabled

    # Expansion Gate Readiness Parameters (E11-03)
    expansion_gate_mode: str = "MIN_OPERATIONAL"  # Mode: "LEGACY_SATURATION" (E11-01/02) vs "MIN_OPERATIONAL" (E11-03/04/05/06)
    q1_expansion_min_q0_active: int = 6           # Min active planted tiles in Q0 to unlock Q1
    q2_expansion_min_active: int = 8              # Min total active tiles to unlock Q2 (was 15 in E11-02, 20 in E11-01)
    q3_expansion_min_active: int = 12             # Min total active tiles to unlock Q3 (was 25 in E11-02, 35 in E11-01)

    # Capital Release Mode & Staged Economic Parameters
    capital_release_mode: str = "BINARY"         # Mode: "BINARY" (E11-03/06), "SYNCHRONIZED" (E11-04), "STAGED" (E11-05)
    protect_expansion_capital: bool = True       # Protect land cost prior to buying next quadrant
    expansion_operating_buffer: float = 100.0   # Minimal float needed after BUY_LAND ($1,100 threshold)
    imminent_land_cash_threshold: float = 900.0  # Cash threshold above which land purchase is imminent in SYNCHRONIZED mode
    
    # E11-X1 3Q Capital Accumulation Parameters
    accumulation_3q_mode: str = "LEGACY_LOCK"         # Mode: "LEGACY_LOCK" (VB1 default $1300) vs "DISCIPLINED_ACCUMULATION" (X1)
    accumulation_3q_optional_reserve: float = 500.0  # Reserve floor for discretionary seed buys during 3Q land accumulation ($500 float)
    
    # E11-X1.2 & E11-X1.3 E06 Productive Core Restoration & EPU Replication Parameters
    productive_core_mode: str = "LEGACY"             # Mode: "LEGACY", "E06_RESTORED", "E06_REPLICATED"
    epu_level: int = 1                               # EPU Scaling Level (1=9t, 2=18t, 3=27t)
    enable_land_expansion: bool = True               # Enable land expansion (False for X1.3-A 1x EPU)
    multi_hire_mode: str = "SINGLE_PER_DAY"          # Mode: "SINGLE_PER_DAY" vs "CORRECTED_MULTI"
    land_buy_mode: str = "IMMEDIATE"                 # Mode: "IMMEDIATE" vs "PRODUCTIVE_SURPLUS"
    surplus_land_threshold: float = 1300.0           # Cash threshold before land buy in PRODUCTIVE_SURPLUS mode
    compact_footprint_size: int = 9                  # Pre-expansion compact managed tiles (E06 9-tile NW cluster)
    
    # Productive Window Parameters (E11-05 State B)
    productive_window_budget_cap: float = 600.0  # Max seed spending budget allowed during PRODUCTIVE_WINDOW
    productive_window_max_day: int = 11          # Max day before PRODUCTIVE_WINDOW forces exit to ACCUMULATE_Q3

    # Safeguards
    prefer_land_before_optional_hire: bool = False  # E11-03/06: Allow hiring down to operating reserve ($300)
    prefer_land_before_livestock: bool = True       # Block livestock purchases while accumulating for land

    # Workforce Scaling & Co-Scaling Parameters (E11-06)
    workforce_scaling_mode: str = "LEGACY"           # Mode: "LEGACY" (E11-01..05) vs "LAND_CO_SCALING" (E11-06)
    pre_land_hiring_enabled: bool = True             # Enable hiring during land accumulation
    max_pre_land_hiring_cost: float = 25.0           # Max single hire cost permitted during land accumulation ($21 Hand 8)
    max_workers: int = 10                            # Target workforce size (1 Farmer + up to 9 Hands)
    target_tiles_per_worker: float = 7.0             # Target active productive tiles per worker (was 7.0 in E11-01..05)
    operating_reserve: float = 300.0                 # Inviolable minimum liquid cash float
    minimum_cash_after_hire: float = 200.0           # Min cash float remaining after HIRE
    max_hires_per_day: int = 4                       # Max hires per day to manage hiring capital cadence
    stop_hire_day: int = 26                          # Day after which hiring is disabled

    # Worker Locality Parameters
    locality_enabled: bool = True            # Enable quadrant locality preference
    cross_quadrant_spillover: bool = True    # Allow workers to assist adjacent quadrants when primary is idle

    # Crop Portfolio Allocation Parameters
    target_productive_tiles: int = 80        # Scaled productive crop tiles across 4 quadrants
    liquidity_crop: str = "CARROT"           # 3-day growth fast cash generator
    growth_crop_1: str = "TOMATO"            # 8-day growth mid-game cash generator
    growth_crop_2: str = "STRAWBERRY"        # 10-day growth high-yield generator
    growth_crop_3: str = "MELON"             # 12-day growth peak cash dump
    feed_crop: str = "WHEAT"                 # 4-day growth feed crop
    
    wheat_feed_tiles_target: int = 12        # Dedicated feed crop tiles
    melon_plant_cutoff_day: int = 18         # Cutoff day for Melon planting
    strawberry_plant_cutoff_day: int = 20    # Cutoff day for Strawberry planting
    tomato_plant_cutoff_day: int = 22        # Cutoff day for Tomato planting
    all_plant_cutoff_day: int = 26           # Cutoff day for all crop planting

    # Livestock Subsystem Parameters
    livestock_enabled: bool = True           # Enable Livestock subsystem
    target_cows: int = 6                     # Target Cow herd size ($400 ea)
    target_sheep: int = 4                    # Target Sheep herd size ($500 ea)
    feed_safety_buffer: int = 4              # Extra Wheat units required in shed/crop before buying
    stop_sheep_buy_day: int = 18             # Cutoff day for Sheep acquisition
    stop_cow_buy_day: int = 20               # Cutoff day for Cow acquisition
    cow_cost: float = 400.0                  # Cow purchase cost
    sheep_cost: float = 500.0                # Sheep purchase cost

    # E12-X1.13 Dynamic Allocation Parameters
    x113_variant: str = "E"                  # A/B/C/D/E counterfactual selector
    x113_livestock_safety_cow_cap: int = 6   # Technical cap, not a strategic target
    x113_livestock_safety_sheep_cap: int = 3 # Technical cap, not a strategic target
    x113_q2_enabled: bool = True             # Allow Q2 only through gated X1.13 policy
    x113_max_hands: int = 12                 # Technical upper bound for workload-based HIRE
    x114_variant: str = "D"                  # A/B/C/D/E/F fast workforce capacity counterfactual
    x114_max_hands: int = 12                 # Technical cap for Workforce Capacity First
    x115_variant: str = "A"                  # A/B/C/D Codex independent competitive build selector
    x115_max_hands: int = 12                 # Technical cap for X1.15 workload/land branch
    x115_antigravity_variant: str = "A"      # A/B/C Antigravity competitive candidate variant
    x115_antigravity_target_cows: int = 14   # Target Cow herd size for Antigravity X1.15
    x115_antigravity_target_sheep: int = 4   # Target Sheep herd size for Antigravity X1.15

    # Capital Reinvestment & Market Broker Parameters
    reinvestment_threshold: float = 1500.0   # Cash threshold triggering aggressive asset reinvestment
    inventory_flush_start_day: int = 27      # Day to commence 100% shed inventory flush


class ProductiveMassROIAgent:
    """E11 Productive Mass Expansion Agent.

    Architectural core:
    - 4 Quadrants (100 tiles total) unlocked via dynamic economic & productive triggers.
    - Expansion Capital Protection (E11-02) to prevent discretionary spending from locking land expansion.
    - Expansion Gate Unlock (E11-03) using Minimum Operational Readiness instead of rigid saturation.
    - Staged Expansion Capital Release (E11-05) via an explicit Economic State Machine.
    - Workforce-Land Co-Scaling (E11-06): Scaling workforce alongside land acquisition (4-6 workers @ 50t, 6-8 @ 75t, 8-10 @ 100t)
      with early bootstrap hiring allowed down to $300 reserve.
    - Scaled workforce up to 10-12 workers with Quadrant Locality Dispatching.
    - 3-Tier Dynamic Crop Portfolio (Liquidity, Growth, Feed).
    - Scaled Livestock Engine (Cows & Sheep) with dedicated labor and daily product processing.
    - Continuous capital reinvestment model with inviolable $300 Operating Reserve.
    - 5-Tier Action Dispatch Hierarchy (Urgent -> Continuity -> Strategic -> Prep -> Pass).
    - Comprehensive Telemetry Logger instrumentation.
    """

    def __init__(self, config: Optional[ProductiveMassConfig] = None):
        self.name = "ProductiveMassROIAgent"
        self.config: ProductiveMassConfig = config if config is not None else ProductiveMassConfig()

        self.telemetry: TelemetryLogger = TelemetryLogger()
        self.telemetry.configured_crop_tiles_count = self.config.target_productive_tiles
        self.telemetry.livestock_counts = {"COW": 0, "SHEEP": 0}

        self.current_phase: str = "BOOTSTRAP"
        self.economic_state: str = "ACCUMULATE_Q2"
        self.owned_quadrants: int = 1  # Start with Q0 (25 tiles)
        self.cow_count: int = 0
        self.sheep_count: int = 0

        # E11-05 Staged Capital Release trackers
        self.window_seed_spending: float = 0.0
        self.q2_purchase_day: Optional[int] = None
        self.q3_purchase_day: Optional[int] = None

        # E11-06 Co-Scaling Telemetry Trackers
        self.workforce_at_50: Optional[int] = None
        self.workforce_at_75: Optional[int] = None
        self.workforce_at_100: Optional[int] = None
        self.active_at_50: Optional[int] = None
        self.active_at_75: Optional[int] = None
        self.active_at_100: Optional[int] = None

        # Dynamic quadrant tile definition maps
        self.q0_tiles: List[Tuple[int, int]] = [(x, y) for x in range(5) for y in range(5)]
        self.q1_tiles: List[Tuple[int, int]] = [(x, y) for x in range(5, 10) for y in range(5)]
        self.q2_tiles: List[Tuple[int, int]] = [(x, y) for x in range(5) for y in range(5, 10)]
        self.q3_tiles: List[Tuple[int, int]] = [(x, y) for x in range(5, 10) for y in range(5, 10)]

        self.livestock_core_tiles: List[Tuple[int, int]] = [(3, 3), (3, 4), (4, 3), (4, 4)]

        # Defined productive crop tile layouts per quadrant
        if "E12" in self.config.productive_core_mode:
            self.q0_crop_tiles: List[Tuple[int, int]] = [
                (1, 1), (1, 2), (1, 3), (1, 4),
                (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                (3, 0), (3, 1), (3, 2),
                (4, 0), (4, 1), (4, 2), (0, 4)
            ]  # 16 non-livestock Q0 tiles
        else:
            self.q0_crop_tiles: List[Tuple[int, int]] = [
                (1, 1), (1, 2), (1, 3), (1, 4),
                (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (0, 4)
            ]  # 20 tiles
        
        self.q1_crop_tiles: List[Tuple[int, int]] = [
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4),
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4),
            (8, 0), (8, 1), (8, 2), (8, 3), (8, 4)
        ]  # 20 tiles

        self.q2_crop_tiles: List[Tuple[int, int]] = [
            (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
            (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
            (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
            (3, 5), (3, 6), (3, 7), (3, 8), (3, 9)
        ]  # 20 tiles

        self.q3_crop_tiles: List[Tuple[int, int]] = [
            (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
            (6, 5), (6, 6), (6, 7), (6, 8), (6, 9),
            (7, 5), (7, 6), (7, 7), (7, 8), (7, 9),
            (8, 5), (8, 6), (8, 7), (8, 8), (8, 9)
        ]  # 20 tiles
        
        # B3 EPU1 3x3 block for pre-expansion core
        self.e06_compact_tiles: List[Tuple[int, int]] = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]  # 9 tiles

    def act(self, game_state: GameState) -> Dict[str, Any]:
        """Kaggle environment entrypoint method."""
        return self.decide(game_state)

    def decide(self, game_state: GameState) -> Dict[str, Any]:
        if self.config.productive_core_mode == "E12_Q0Q1_80K_ENGINE_X111":
            return self._decide_e12_q0q1_80k_engine_x111(game_state)
        if self.config.productive_core_mode == "E12_TRUEBELIEF_ENGINE_X112":
            return self._decide_e12_truebelief_engine_x112(game_state)
        if self.config.productive_core_mode == "E12_DYNAMIC_ALLOCATION_X113":
            return self._decide_e12_dynamic_allocation_x113(game_state)
        if self.config.productive_core_mode == "E12_WORKFORCE_CAPACITY_X114":
            return self._decide_e12_workforce_capacity_x114(game_state)
        if self.config.productive_core_mode == "E12_X115_COPILOT_INDEPENDENT":
            return self._decide_e12_x115_copilot_independent(game_state)
        if self.config.productive_core_mode == "E12_X115_ANTIGRAVITY_INDEPENDENT":
            return self._decide_e12_x115_antigravity_independent(game_state)
        if self.config.productive_core_mode == "E12_X115_CODEX_INDEPENDENT":
            return self._decide_e12_x115_codex_independent(game_state)
        if self.config.productive_core_mode == "E12_CONTINUOUS_SURFACE_X110":
            return self._decide_e12_continuous_surface_x110(game_state)
        if self.config.productive_core_mode == "E12_GROWTH_FIRST_X19":
            return self._decide_e12_growth_first_x19(game_state)
        if self.config.productive_core_mode == "E12_LIVESTOCK_FIRST_X18":
            return self._decide_e12_livestock_first_x18(game_state)
        if self.config.productive_core_mode == "E12_HYBRID_STAGED_LOCALITY":
            return self._decide_e12_hybrid_staged_locality(game_state)
        if self.config.productive_core_mode == "E12_HYBRID_FULL_SCALING":
            return self._decide_e12_hybrid_full_scaling(game_state)
        if self.config.productive_core_mode == "E12_HYBRID_RECOVERY":
            return self._decide_e12_hybrid_recovery(game_state)
        if self.config.productive_core_mode == "E12_CENTERED_HYBRID":
            return self._decide_e12_centered_hybrid(game_state)
        if self.config.productive_core_mode == "EPU_CORNER_PRUNED_CENTER_OUT":
            return self._decide_epu_corner_pruned_center_out(game_state)
        if self.config.productive_core_mode == "E06_PROGRESSIVE":
            return self._decide_e06_progressive(game_state)
        if self.config.productive_core_mode == "E06_CENTERED":
            return self._decide_e06_centered(game_state)
        if self.config.productive_core_mode == "E06_DENSIFIED":
            return self._decide_e06_densified(game_state)
        if self.config.productive_core_mode == "E06_REPLICATED":
            return self._decide_e06_replicated(game_state)

        if game_state.step == 0:
            self.telemetry.starting_money = game_state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, game_state.money)
        self.telemetry.final_money = game_state.money

        hands = game_state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(game_state)
        self._update_phase(game_state)
        self._update_economic_state(game_state)

        builder = ActionBuilder()
        self._process_market_decisions(game_state, builder, total_workers)
        self._dispatch_worker_actions(game_state, builder, hands)
        self._process_sales(game_state, builder)

        return builder.build()

    def _record_diagnostics(self, state: GameState):
        day = state.day
        active_tiles = 0
        needs_water_count = 0
        harvest_ready_count = 0
        plant_pending_count = 0

        available_tiles = list(self.q0_crop_tiles)
        if self.owned_quadrants >= 2:
            available_tiles.extend(self.q1_crop_tiles)
        if self.owned_quadrants >= 3:
            available_tiles.extend(self.q2_crop_tiles)
        if self.owned_quadrants >= 4:
            available_tiles.extend(self.q3_crop_tiles)

        for (tx, ty) in available_tiles:
            tile = state.get_tile(tx, ty)
            if tile is None or (isinstance(tile, dict) and tile.get("kind") == "WEED"):
                plant_pending_count += 1
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                active_tiles += 1
                if not tile.get("watered_today", False):
                    needs_water_count += 1
                crop_type = tile.get("crop", "WHEAT")
                crop_info = CROPS.get(crop_type, CROPS["WHEAT"])
                planted_d = tile.get("planted_day", day)
                if (day - planted_d) >= crop_info["max_yield_day"]:
                    harvest_ready_count += 1

        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, active_tiles)
        self.telemetry.daily_productive_tiles_history.append(active_tiles)
        self.telemetry.backlog_history["needs_water"].append(needs_water_count)
        self.telemetry.backlog_history["harvest_ready"].append(harvest_ready_count)
        self.telemetry.backlog_history["plant_pending"].append(plant_pending_count)

    def _update_phase(self, state: GameState):
        day = state.day
        old_phase = self.current_phase

        if day < 5:
            new_phase = "BOOTSTRAP"
        elif day < 10:
            new_phase = "FIRST_EXPANSION"
        elif day < 18:
            new_phase = "MASS_SCALING"
        elif day < self.config.inventory_flush_start_day:
            new_phase = "FULL_MASS_ENGINE"
        else:
            new_phase = "LIQUIDATION"

        if new_phase != old_phase:
            self.telemetry.log_phase_change(
                state.step, state.day, state.hour, old_phase, new_phase, state.money
            )
            self.current_phase = new_phase

    def _update_economic_state(self, state: GameState):
        """E11-05 Economic State Machine transitions."""
        if self.config.capital_release_mode != "STAGED":
            return

        old_state = self.economic_state
        day = state.day

        # State 1: ACCUMULATE_Q2 -> PRODUCTIVE_WINDOW upon Q2 purchase (owned_quadrants >= 2)
        if self.economic_state == "ACCUMULATE_Q2":
            if self.owned_quadrants >= 2:
                self.economic_state = "PRODUCTIVE_WINDOW"
                self.q2_purchase_day = day
                self.telemetry.log_event("STATE_CHANGE", state.step, day, state.hour, state.money, "Entered PRODUCTIVE_WINDOW (Q2 purchased)")

        # State 2: PRODUCTIVE_WINDOW -> ACCUMULATE_Q3 upon budget cap reached OR max window day OR cash building up for Q3
        elif self.economic_state == "PRODUCTIVE_WINDOW":
            if self.window_seed_spending >= self.config.productive_window_budget_cap or day >= self.config.productive_window_max_day or self.owned_quadrants >= 3:
                self.economic_state = "ACCUMULATE_Q3"
                self.telemetry.log_event("STATE_CHANGE", state.step, day, state.hour, state.money, f"Entered ACCUMULATE_Q3 (Window seed spend: ${self.window_seed_spending:.0f})")

        # State 3: ACCUMULATE_Q3 -> MASS_ACTIVATION upon Q3 purchase (owned_quadrants >= 4)
        elif self.economic_state == "ACCUMULATE_Q3":
            if self.owned_quadrants >= 4:
                self.economic_state = "MASS_ACTIVATION"
                self.q3_purchase_day = day
                self.telemetry.log_event("STATE_CHANGE", state.step, day, state.hour, state.money, "Entered MASS_ACTIVATION (Q3 purchased)")

    def _process_market_decisions(self, state: GameState, builder: ActionBuilder, current_workers: int):
        day = state.day
        hour = state.hour
        cash = state.money
        reserve = self.config.operating_reserve

        is_expansion_pending = (
            self.config.protect_expansion_capital and
            self.owned_quadrants < self.config.target_quadrants and
            day <= self.config.stop_expansion_day
        )

        # Calculate optional_reserve for discretionary spending (seeds/livestock)
        if self.config.capital_release_mode == "STAGED":
            if self.economic_state in ("ACCUMULATE_Q2", "ACCUMULATE_Q3"):
                optional_reserve = reserve + 1000.0
            elif self.economic_state == "PRODUCTIVE_WINDOW":
                optional_reserve = reserve
            else:
                optional_reserve = reserve
        elif self.config.capital_release_mode == "SYNCHRONIZED":
            optional_reserve = (reserve + 1000.0) if (is_expansion_pending and cash >= self.config.imminent_land_cash_threshold) else reserve
        elif self.config.accumulation_3q_mode == "DISCIPLINED_ACCUMULATION" and self.owned_quadrants == 2:
            optional_reserve = self.config.accumulation_3q_optional_reserve
        else:  # BINARY (E11-02/03/06/VB1)
            optional_reserve = (reserve + 1000.0) if is_expansion_pending else reserve

        # Determine active tile thresholds based on expansion gate mode
        if self.config.expansion_gate_mode == "MIN_OPERATIONAL":
            q1_gate = self.config.q1_expansion_min_q0_active
            q2_gate = self.config.q2_expansion_min_active
            q3_gate = self.config.q3_expansion_min_active
        else:
            q1_gate = 10
            q2_gate = 15
            q3_gate = 25

        # --- A. Dynamic Land Expansion Triggers (Q1, Q2, Q3) ---
        if day <= self.config.stop_expansion_day and hour == 0:
            active_tiles = self.telemetry.daily_productive_tiles_history[-1] if self.telemetry.daily_productive_tiles_history else 0

            # Q1 Buy Trigger (2Q / 50 tiles)
            if self.owned_quadrants == 1 and active_tiles >= q1_gate:
                if self.config.land_buy_mode == "PRODUCTIVE_SURPLUS":
                    buy_threshold = self.config.surplus_land_threshold
                else:
                    buy_threshold = 1000.0 + (self.config.expansion_operating_buffer if self.config.protect_expansion_capital else reserve)
                if cash >= buy_threshold:
                    builder.buy_land()
                    self.owned_quadrants = 2
                    self.telemetry.spending_land += 1000.0
                    self.telemetry.buy_land_executed_step = state.step
                    self.telemetry.log_event("BUY_LAND", state.step, day, hour, cash, "Unlocked Q1 (50 tiles total)")
                    cash -= 1000.0
                    self.workforce_at_50 = current_workers
                    self.active_at_50 = active_tiles

            # Q2 Buy Trigger (3Q / 75 tiles)
            elif self.owned_quadrants == 2 and active_tiles >= q2_gate:
                buy_threshold = 1000.0 + (self.config.expansion_operating_buffer if self.config.protect_expansion_capital else reserve)
                if cash >= buy_threshold:
                    builder.buy_land()
                    self.owned_quadrants = 3
                    self.telemetry.spending_land += 1000.0
                    self.telemetry.log_event("BUY_LAND", state.step, day, hour, cash, "Unlocked Q2 (75 tiles total)")
                    cash -= 1000.0
                    self.workforce_at_75 = current_workers
                    self.active_at_75 = active_tiles

            # Q3 Buy Trigger (4Q / 100 tiles)
            elif self.owned_quadrants == 3 and active_tiles >= q3_gate:
                buy_threshold = 1000.0 + (self.config.expansion_operating_buffer if self.config.protect_expansion_capital else reserve)
                if cash >= buy_threshold:
                    builder.buy_land()
                    self.owned_quadrants = 4
                    self.telemetry.spending_land += 1000.0
                    self.telemetry.log_event("BUY_LAND", state.step, day, hour, cash, "Unlocked Q3 (100 tiles total)")
                    cash -= 1000.0
                    self.workforce_at_100 = current_workers
                    self.active_at_100 = active_tiles

        # Update state machine after land purchases
        self._update_economic_state(state)

        # --- B. Dynamic Workforce Scaling & Co-Scaling (HIRE) ---
        if day <= self.config.stop_hire_day and hour == 0 and state.hires_today < self.config.max_hires_per_day:
            if current_workers < self.config.max_workers:
                active_tiles = self.telemetry.daily_productive_tiles_history[-1] if self.telemetry.daily_productive_tiles_history else 0
                
                # Determine quad worker cap
                if self.config.workforce_scaling_mode == "LAND_CO_SCALING":
                    if self.owned_quadrants == 1:
                        quad_worker_cap = 4
                    elif self.owned_quadrants == 2:
                        quad_worker_cap = 6
                    elif self.owned_quadrants == 3:
                        quad_worker_cap = 8
                    else:
                        quad_worker_cap = self.config.max_workers
                else:
                    quad_worker_cap = self.config.max_workers

                if self.config.multi_hire_mode == "CORRECTED_MULTI":
                    if self.config.productive_core_mode == "E06_RESTORED" and self.owned_quadrants == 1:
                        target_workers = 2  # E06 compact core: 1 Farmer + 1 Hand
                    else:
                        target_workers = min(quad_worker_cap, max(2, int(math.ceil(active_tiles / max(1.0, self.config.target_tiles_per_worker)))))
                    
                    hires_needed = max(0, target_workers - current_workers)
                    fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
                    current_hires = state.hires_today
                    
                    for _ in range(hires_needed):
                        if current_hires < self.config.max_hires_per_day:
                            hire_cost = float(fibs[min(current_hires, len(fibs) - 1)])
                            if cash - hire_cost >= reserve:
                                builder.hire()
                                current_hires += 1
                                current_workers += 1
                                self.telemetry.spending_workforce += hire_cost
                                self.telemetry.hires_count += 1
                                self.telemetry.log_event("HIRE", state.step, day, hour, cash, f"Hired Hand (Worker {current_workers})")
                                cash -= hire_cost
                else:
                    tiles_per_worker = active_tiles / max(1, current_workers)
                    should_hire = (
                        current_workers < quad_worker_cap and (
                            tiles_per_worker >= self.config.target_tiles_per_worker or
                            current_workers < max(2, self.owned_quadrants * 2)
                        )
                    )

                    if should_hire:
                        current_hires = state.hires_today
                        fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
                        hire_cost = float(fibs[min(current_hires, len(fibs) - 1)])

                        if self.config.workforce_scaling_mode == "LAND_CO_SCALING" and self.config.pre_land_hiring_enabled:
                            if is_expansion_pending and cash >= 950.0:
                                hire_reserve = 1020.0
                            else:
                                hire_reserve = reserve
                        else:
                            hire_reserve = optional_reserve if self.config.prefer_land_before_optional_hire else reserve

                        if cash - hire_cost >= hire_reserve:
                            builder.hire()
                            self.telemetry.spending_workforce += hire_cost
                            self.telemetry.hires_count += 1
                            self.telemetry.log_event("HIRE", state.step, day, hour, cash, f"Hired Hand (Worker {current_workers + 1})")
                            cash -= hire_cost

        # --- C. Seed Purchasing ---
        self._buy_seeds_if_needed(state, builder, cash, reserve, optional_reserve)

        # --- D. Livestock Purchasing ---
        self._buy_livestock_if_needed(state, builder, cash, optional_reserve)

    def _hire_workers_if_needed(self, state: GameState, builder: ActionBuilder, cash: float, reserve: float) -> float:
        day, hour = state.day, state.hour
        hands = state.hands_positions
        current_workers = 1 + len(hands)
        has_hire = any(isinstance(cmd, list) and cmd[0] == "HIRE" for cmd in builder.market_orders)
        if day <= self.config.stop_hire_day and state.hires_today < self.config.max_hires_per_day and not has_hire:
            active_tiles = sum(1 for y in range(10) for x in range(10) if isinstance(state.get_tile(x,y), dict) and state.get_tile(x,y).get("kind") == "PLANT")
            target_workers = min(self.config.max_workers, max(2, int(math.ceil(active_tiles / max(1.0, self.config.target_tiles_per_worker)))))
            if self.owned_quadrants == 1 and target_workers < 3:
                target_workers = 3
            elif self.owned_quadrants == 2 and target_workers < 5:
                target_workers = 5
            elif self.owned_quadrants >= 3 and target_workers < 6:
                target_workers = 6
            
            if current_workers < target_workers:
                fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
                hire_cost = float(fibs[min(state.hires_today, len(fibs) - 1)])
                if cash - hire_cost >= reserve:
                    builder.market_orders.insert(0, ["HIRE"])
                    self.telemetry.spending_workforce += hire_cost
                    self.telemetry.hires_count += 1
                    self.telemetry.log_event("HIRE", state.step, day, hour, cash, f"Hired Hand #{current_workers + 1}")
                    cash -= hire_cost
        return cash

    def _buy_seeds_if_needed(self, state: GameState, builder: ActionBuilder, cash: float, reserve: float, optional_reserve: float):
        day = state.day
        if day > self.config.all_plant_cutoff_day:
            return

        seed_spend_this_step = 0.0
        target_seed_cap = 12
        target_high_cap = 8

        # Protect Cow #1 purchase capital ($400 float) if Cow #1 is pending acquisition
        total_w = 1 + len(getattr(state, "hands_positions", []))
        if hasattr(state, "get_worker_inventory_count"):
            wheat_avail = state.get_shed_count("WHEAT") + sum(state.get_worker_inventory_count(w, "WHEAT") for w in range(total_w))
            cows_owned = state.get_shed_count("COW") + sum(state.get_worker_inventory_count(w, "COW") for w in range(total_w))
        else:
            wheat_avail = state.get_shed_count("WHEAT")
            cows_owned = state.get_shed_count("COW")
        cow_1_pending = (getattr(self.telemetry, "cows_acquired", 0) == 0 and cows_owned == 0 and wheat_avail >= 1)
        if cow_1_pending:
            reserve = max(reserve, 450.0)
            optional_reserve = max(optional_reserve, 450.0)

        is_expansion_pending = (
            self.config.protect_expansion_capital and
            self.owned_quadrants < self.config.target_quadrants and
            day <= self.config.stop_expansion_day
        )
        essential_reserve = 1100.0 if (is_expansion_pending and cash >= self.config.imminent_land_cash_threshold) else reserve

        # Essential Wheat & Carrot seeds (feed & liquidity)
        wheat_thresh = 6
        carrot_thresh = 6
        essential_seed_reserve = 20.0

        if state.get_seed_count("WHEAT") < wheat_thresh and cash - 60.0 >= essential_seed_reserve:
            builder.buy_seed("WHEAT", 6)
            self.telemetry.spending_seeds += 60.0
            cash -= 60.0

        if state.get_seed_count("CARROT") < carrot_thresh and cash - 120.0 >= essential_seed_reserve:
            builder.buy_seed("CARROT", 6)
            self.telemetry.spending_seeds += 120.0
            cash -= 120.0

        # Discretionary Melon seeds (Peak ROI crop: $94.67/action) - Day 0 to 16
        if day <= 16 and state.get_seed_count("MELON") < 4:
            if cash - 320.0 >= optional_reserve:
                builder.buy_seed("MELON", 4)
                self.telemetry.spending_seeds += 320.0
                cash -= 320.0
            elif cash - 80.0 >= optional_reserve:
                builder.buy_seed("MELON", 1)
                self.telemetry.spending_seeds += 80.0
                cash -= 80.0

        # Discretionary Strawberry seeds (growth tier 2) - checked against optional_reserve (post-Q1)
        if day <= self.config.strawberry_plant_cutoff_day and state.get_seed_count("STRAWBERRY") < target_high_cap:
            if cash - 400.0 >= optional_reserve:
                builder.buy_seed("STRAWBERRY", 4)
                self.telemetry.spending_seeds += 400.0
                cash -= 400.0
            elif cash - 100.0 >= optional_reserve:
                builder.buy_seed("STRAWBERRY", 1)
                self.telemetry.spending_seeds += 100.0
                cash -= 100.0

        # Discretionary Melon seeds (growth tier 3) - checked against optional_reserve
        if self.owned_quadrants >= 2 and day <= self.config.melon_plant_cutoff_day and state.get_seed_count("MELON") < target_high_cap:
            if cash - 320.0 >= optional_reserve:
                builder.buy_seed("MELON", 4)
                self.telemetry.spending_seeds += 320.0
                cash -= 320.0
            elif cash - 80.0 >= optional_reserve:
                builder.buy_seed("MELON", 1)
                self.telemetry.spending_seeds += 80.0
                cash -= 80.0

        # Flexible single/double/bulk seed buying fallback for CARROT/WHEAT when cash is tight
        if day <= self.config.all_plant_cutoff_day and state.get_seed_count("CARROT") < target_seed_cap and cash - 120.0 >= optional_reserve:
            builder.buy_seed("CARROT", 6)
            self.telemetry.spending_seeds += 120.0
            cash -= 120.0
        elif day <= self.config.all_plant_cutoff_day and state.get_seed_count("CARROT") < 2 and cash - 20.0 >= optional_reserve:
            builder.buy_seed("CARROT", 1)
            self.telemetry.spending_seeds += 20.0
            cash -= 20.0
        elif state.get_seed_count("WHEAT") < 2 and cash - 10.0 >= optional_reserve:
            builder.buy_seed("WHEAT", 1)
            self.telemetry.spending_seeds += 10.0
            cash -= 10.0

        if self.economic_state == "PRODUCTIVE_WINDOW":
            self.window_seed_spending += seed_spend_this_step

    def _buy_livestock_if_needed(self, state: GameState, builder: ActionBuilder, cash: float, optional_reserve: float):
        if not self.config.livestock_enabled:
            return
        day = state.day
        live_reserve = 50.0 if day <= 5 else 150.0

        # Scale Cows up to 4 in 2x2 centered core [(3,3), (3,4), (4,3), (4,4)]
        if self.cow_count < 4 and day <= 24:
            if self.cow_count == 0:
                if cash >= 400.0:
                    builder.buy_animal("COW", 1)
                    self.cow_count += 1
                    self.telemetry.spending_livestock += self.config.cow_cost
                    self.telemetry.livestock_counts["COW"] = self.cow_count
                    self.telemetry.log_event("BUY_COW", state.step, day, state.hour, cash, f"Bought Cow #{self.cow_count}")
                    cash -= self.config.cow_cost
            else:
                wheat_count = state.get_shed_count("WHEAT") + state.get_seed_count("WHEAT")
                if wheat_count >= self.cow_count * 2 + 1:
                    if cash - self.config.cow_cost >= live_reserve:
                        builder.buy_animal("COW", 1)
                        self.cow_count += 1
                        self.telemetry.spending_livestock += self.config.cow_cost
                        self.telemetry.livestock_counts["COW"] = self.cow_count
                        self.telemetry.log_event("BUY_COW", state.step, day, state.hour, cash, f"Bought Cow #{self.cow_count}")
                        cash -= self.config.cow_cost

            if self.sheep_count < self.config.target_sheep and day <= self.config.stop_sheep_buy_day:
                if cash - self.config.sheep_cost >= live_reserve:
                    builder.buy_animal("SHEEP", 1)
                    self.sheep_count += 1
                    self.telemetry.spending_livestock += self.config.sheep_cost
                    self.telemetry.livestock_counts["SHEEP"] = self.sheep_count
                    self.telemetry.log_event("BUY_SHEEP", state.step, day, state.hour, cash, f"Bought Sheep #{self.sheep_count}")
                    cash -= self.config.sheep_cost

    def _dispatch_worker_actions(self, state: GameState, builder: ActionBuilder, hands: List[Tuple[int, int]]):
        reserved_tiles: Set[Tuple[int, int]] = set()

        # Worker 0 (Farmer): Preferred Q0
        farmer_pos = state.farmer_position
        farmer_act = self._get_worker_action(state, farmer_pos, reserved_tiles, worker_id=0, preferred_quadrant=0)
        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        # Hands 1..N: Locality-guided preferred quadrant assignment
        quadrant_assignments = [0, 1, 1, 2, 2, 3, 3, 3, 3, 3]

        for idx, hand_pos in enumerate(hands):
            worker_id = idx + 1
            pref_q = quadrant_assignments[min(idx, len(quadrant_assignments) - 1)]
            if pref_q >= self.owned_quadrants:
                pref_q = 0  # Fallback to Q0 if quadrant not yet owned
            h_act = self._get_worker_action(state, hand_pos, reserved_tiles, worker_id=worker_id, preferred_quadrant=pref_q)
            builder.add_hand_action(h_act)

    def _get_worker_action(
        self, state: GameState, pos: Tuple[int, int], reserved: Set[Tuple[int, int]], worker_id: int, preferred_quadrant: int, virtual_seeds: Dict[str, int] = None
    ) -> List[str]:
        px, py = pos
        day = state.day

        # Define primary crop tiles for this worker's preferred quadrant
        if preferred_quadrant == 1 and self.owned_quadrants >= 2:
            primary_tiles = list(self.q1_crop_tiles)
        elif preferred_quadrant == 2 and self.owned_quadrants >= 3:
            primary_tiles = list(self.q2_crop_tiles)
        elif preferred_quadrant == 3 and self.owned_quadrants >= 4:
            primary_tiles = list(self.q3_crop_tiles)
        else:
            if self.config.productive_core_mode == "E06_RESTORED" and self.owned_quadrants == 1:
                primary_tiles = list(self.e06_compact_tiles)
            else:
                primary_tiles = list(self.q0_crop_tiles)

        # Collect secondary tiles for spillover assist
        secondary_tiles = []
        if self.config.cross_quadrant_spillover:
            all_tiles = list(self.q0_crop_tiles)
            if self.owned_quadrants >= 2:
                all_tiles.extend(self.q1_crop_tiles)
            if self.owned_quadrants >= 3:
                all_tiles.extend(self.q2_crop_tiles)
            if self.owned_quadrants >= 4:
                all_tiles.extend(self.q3_crop_tiles)
            secondary_tiles = [t for t in all_tiles if t not in primary_tiles]

        # --- Tier 1: URGENT WATER (Water-First priority) ---
        water_act = self._find_best_task_action(state, px, py, primary_tiles, secondary_tiles, reserved, worker_id, task_type="WATER", virtual_seeds=virtual_seeds)
        if water_act:
            return water_act

        # --- Tier 1B: URGENT HARVEST MATURE CROPS ---
        harvest_act = self._find_best_task_action(state, px, py, primary_tiles, secondary_tiles, reserved, worker_id, task_type="HARVEST", virtual_seeds=virtual_seeds)
        if harvest_act:
            return harvest_act

        # --- Tier 2: PRODUCTIVE CONTINUITY (PLANT EMPTY TILES) ---
        if day <= self.config.all_plant_cutoff_day:
            plant_act = self._find_best_task_action(state, px, py, primary_tiles, secondary_tiles, reserved, worker_id, task_type="PLANT", virtual_seeds=virtual_seeds)
            if plant_act:
                return plant_act

        # --- Tier 4: PREPARATION / DIG WEEDS ---
        dig_act = self._find_best_task_action(state, px, py, primary_tiles, secondary_tiles, reserved, worker_id, task_type="DIG", virtual_seeds=virtual_seeds)
        if dig_act:
            return dig_act

        # --- Tier 5: PASS (Idle Fallback) ---
        self.telemetry.record_worker_step(worker_id, "idle")
        return ["PASS"]

    def _find_best_task_action(
        self, state: GameState, px: int, py: int, primary: List[Tuple[int, int]], secondary: List[Tuple[int, int]], reserved: Set[Tuple[int, int]], worker_id: int, task_type: str, virtual_seeds: Dict[str, int] = None
    ) -> Optional[List[str]]:
        day = state.day
        candidates = []

        # Check primary quadrant tiles first
        for (tx, ty) in primary:
            if (tx, ty) in reserved:
                continue
            tile = state.get_tile(tx, ty)
            if self._tile_matches_task(state, tile, tx, ty, day, task_type):
                dist = abs(px - tx) + abs(py - ty)
                candidates.append((dist, (tx, ty), True))

        # If no primary candidates, check secondary spillover tiles
        if not candidates and secondary:
            for (tx, ty) in secondary:
                if (tx, ty) in reserved:
                    continue
                tile = state.get_tile(tx, ty)
                if self._tile_matches_task(state, tile, tx, ty, day, task_type):
                    dist = abs(px - tx) + abs(py - ty)
                    candidates.append((dist, (tx, ty), False))

        if not candidates:
            return None

        candidates.sort(key=lambda item: item[0])
        best_dist, best_tile, is_primary = candidates[0]

        # Locality pinning: do not walk cross-map for distant secondary tasks
        if not is_primary:
            if task_type == "WATER" and best_dist > 5:
                return None
            elif task_type != "WATER" and best_dist > 3:
                return None

        reserved.add(best_tile)

        if best_tile[0] >= 5 or best_tile[1] >= 5:
            self.telemetry.q1_worked += 1
        else:
            self.telemetry.q0_worked += 1

        if best_dist == 0:
            self.telemetry.record_worker_step(worker_id, "productive")
            if task_type in ("WATER", "EMERGENCY_WATER"):
                self.telemetry.crops_watered += 1
                return ["WATER"]
            elif task_type == "HARVEST":
                target_t = state.get_tile(best_tile[0], best_tile[1])
                if isinstance(target_t, dict) and target_t.get("kind") == "PLANT":
                    self.telemetry.crops_harvested += 1
                return ["HARVEST"]
            elif task_type == "PLANT":
                crop = self._select_crop_to_plant(state, day, best_tile, virtual_seeds)
                if crop is None:
                    return None
                if virtual_seeds and crop in virtual_seeds and virtual_seeds[crop] > 0:
                    virtual_seeds[crop] -= 1
                self.telemetry.crops_planted += 1
                return ["PLANT", crop]
            elif task_type == "DIG":
                self.telemetry.crops_weed_losses += 1
                return ["DIG"]
        else:
            self.telemetry.record_worker_step(worker_id, "movement")
            return self._move_towards(px, py, best_tile)

        return None

    def _tile_matches_task(self, state: GameState, tile: Any, tx: int, ty: int, day: int, task_type: str) -> bool:
        if task_type == "EMERGENCY_WATER":
            return (
                isinstance(tile, dict) and
                tile.get("kind") == "PLANT" and
                not tile.get("watered_today", False) and
                tile.get("consecutive_unwatered", 0) >= 1
            )
        elif task_type == "WATER":
            return isinstance(tile, dict) and tile.get("kind") == "PLANT" and not tile.get("watered_today", False)
        elif task_type == "HARVEST":
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                crop_type = tile.get("crop", "WHEAT")
                crop_info = CROPS.get(crop_type, CROPS["WHEAT"])
                planted_d = tile.get("planted_day", day)
                first_yield_day = crop_info.get("first_yield_day", crop_info["max_yield_day"])
                return tile.get("yield_units", 0) > 0 and (day - planted_d) >= first_yield_day
            return False
        elif task_type == "PLANT":
            return tile is None or (isinstance(tile, dict) and tile.get("kind") in ("EMPTY", "SOIL"))
        elif task_type == "DIG":
            return isinstance(tile, dict) and tile.get("kind") == "WEED"
        return False

    def _select_crop_to_plant(self, state: GameState, day: int, tile: Tuple[int, int], virtual_seeds: Dict[str, int] = None) -> Optional[str]:
        v_seeds = virtual_seeds if virtual_seeds is not None else {c: state.get_seed_count(c) for c in CROPS.keys()}
        if self.config.productive_core_mode in ("E12_CENTERED_HYBRID", "E12_HYBRID_RECOVERY", "E12_HYBRID_FULL_SCALING", "E12_HYBRID_STAGED_LOCALITY"):
            is_feed_tile = tile in [(3, 1), (3, 2), (4, 1), (4, 2), (2, 3), (2, 4), (1, 3), (1, 4)]
        else:
            is_feed_tile = tile in [(1, 1), (1, 2)]

        # Dedicated Feed WHEAT Allocation for E12 Hybrid modes (Feed Tile Priority Lock)
        if is_feed_tile:
            owned_wheat = state.get_seed_count("WHEAT") if state is not None else 0
            if v_seeds.get("WHEAT", 0) > 0 or owned_wheat > 0:
                return "WHEAT"
            # FEED TILE PRIORITY LOCK: Strictly forbid CARROT or cash crop fallbacks on feed tiles!
            return None

        # Fast liquidity crop fallback when cash is very tight (< $100) and no high-value seeds available
        cash = getattr(state, "money", 1000.0)
        if cash < 100.0 and v_seeds.get("MELON", 0) == 0 and v_seeds.get("STRAWBERRY", 0) == 0:
            if v_seeds.get("CARROT", 0) > 0:
                return "CARROT"
            if v_seeds.get("WHEAT", 0) > 0:
                return "WHEAT"

        # High value crops based on horizon (Audit B verified ROIs: MELON $94.67/act, STRAWBERRY $29.23/act)
        if day <= 16 and v_seeds.get("MELON", 0) > 0:
            return "MELON"
        if day <= 20 and v_seeds.get("STRAWBERRY", 0) > 0:
            return "STRAWBERRY"
        if day <= 22 and v_seeds.get("TOMATO", 0) > 0:
            return "TOMATO"
        if v_seeds.get("CARROT", 0) > 0:
            return "CARROT"
        if v_seeds.get("WHEAT", 0) > 0:
            return "WHEAT"
        return None

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

    def _apply_builder_action(self, builder: ActionBuilder, act: List[str], is_farmer: bool):
        if not is_farmer or not act:
            return
        cmd = act[0]
        if cmd == "WATER":
            builder.water()
        elif cmd == "HARVEST":
            builder.harvest()
        elif cmd == "PLANT" and len(act) >= 2:
            builder.plant(act[1])
        elif cmd == "BUILD_PASTURE":
            builder.build_pasture()
        elif cmd == "PLACE" and len(act) >= 2:
            builder.place(act[1])
        elif cmd == "PICKUP" and len(act) >= 3:
            builder.pickup(act[1], int(act[2]))
        elif cmd == "FEED":
            builder.feed()
        elif cmd == "DIG":
            builder.farmer_action = ["DIG"]
        elif cmd in ("NORTH", "SOUTH", "EAST", "WEST"):
            builder.move(cmd)
        else:
            builder.farmer_action = list(act)

    def _process_sales(self, state: GameState, builder: ActionBuilder):
        shed = state.shed
        orders_placed = 0
        max_orders = 10
        is_flush_phase = (state.day >= self.config.inventory_flush_start_day)

        for product, unit_price in [
            ("MELON", 250.0),
            ("STRAWBERRY", 100.0),
            ("TOMATO", 50.0),
            ("CARROT", 35.0),
            ("WHEAT", 25.0),
            ("MILK", 160.0),
            ("WOOL", 200.0)
        ]:
            cnt = shed.get(product, 0)
            if cnt > 0 and orders_placed < max_orders:
                sell_qty = cnt if is_flush_phase else min(cnt, max_orders - orders_placed)
                builder.sell(product, sell_qty)
                orders_placed += 1
                self.telemetry.quantities_sold[product] = self.telemetry.quantities_sold.get(product, 0) + sell_qty
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + (sell_qty * unit_price)

        self.telemetry.market_orders_placed += orders_placed
        self.telemetry.unsold_shed_items = sum(shed.values())

    def _decide_e12_centered_hybrid(self, state: GameState) -> Dict[str, Any]:
        """E12-X1.0 Centered Hybrid Farm Scaling Strategy (Cow-First + Progressive 2x2 Livestock Core + Dynamic Feed Loop)."""
        if state.step == 0:
            self.telemetry.starting_money = state.money
            self.epu1_densified = False
            self.epu2_densified = False
            setattr(self.telemetry, "turn_telemetry_1_24", [])

        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(state)

        raw_quads = state.my_farm.get("unlocked_quadrants", 1)
        owned_quadrants = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        self.owned_quadrants = max(self.owned_quadrants, owned_quadrants)

    def _record_action_budget(self, state: GameState, act: Optional[List[str]]):
        if not hasattr(self.telemetry, "action_budget"):
            setattr(self.telemetry, "action_budget", {
                "MOVEMENT": 0, "LIVESTOCK_SETUP": 0, "LIVESTOCK_MAINTENANCE": 0,
                "FEED_PRODUCTION": 0, "CROP_SETUP": 0, "CROP_MAINTENANCE": 0,
                "CROP_HARVEST": 0, "MARKET_SHED": 0, "PASS_OTHER": 0
            })
        budget = getattr(self.telemetry, "action_budget")
        if not act or act[0] == "PASS":
            budget["PASS_OTHER"] += 1
        elif act[0] in ("NORTH", "SOUTH", "EAST", "WEST"):
            budget["MOVEMENT"] += 1
        elif act[0] in ("BUILD_PASTURE", "PLACE", "PICKUP"):
            if len(act) > 1 and act[1] == "COW":
                budget["LIVESTOCK_SETUP"] += 1
            else:
                budget["MARKET_SHED"] += 1
        elif act[0] == "FEED":
            budget["LIVESTOCK_MAINTENANCE"] += 1
        elif act[0] == "WATER":
            budget["CROP_MAINTENANCE"] += 1
        elif act[0] == "HARVEST":
            budget["CROP_HARVEST"] += 1
        elif act[0] == "PLANT":
            if len(act) > 1 and act[1] == "WHEAT":
                budget["FEED_PRODUCTION"] += 1
            else:
                budget["CROP_SETUP"] += 1
        else:
            budget["PASS_OTHER"] += 1

    def _decide_e12_hybrid_recovery(self, state: GameState) -> Dict[str, Any]:
        """
        E12-X1.2 — Hybrid Crop Recovery strategy.
        Maintains E12-X1.1 validated livestock opening (Cow #1 + Feed ring), then immediately
        triggers CROP_RECOVERY phase to scale E11-X1.7 centered crop mass (Melons/ROI crops).
        """
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(state)

        raw_quads = state.my_farm.get("unlocked_quadrants", 1)
        owned_quadrants = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        self.owned_quadrants = max(self.owned_quadrants, owned_quadrants)

        livestock_core_reserved = [(3, 3), (3, 4), (4, 3), (4, 4)]
        shed_access_tile = (4, 4)

        builder = ActionBuilder()

        # 1. Market Phase: Sell MILK and non-WHEAT crops immediately (keep WHEAT feed buffer in shed)
        for product in [c for c in CROPS.keys() if c != "WHEAT"] + ["MILK", "WOOL"]:
            shed_count = state.get_shed_count(product)
            if shed_count > 0:
                builder.sell(product, shed_count)
                price = state.get_price(product)
                if product in CROPS:
                    unit_price = price if price > 0 else CROPS[product]["seed"] * 1.75
                elif product == "MILK":
                    unit_price = price if price > 0 else 160.0
                elif product == "WOOL":
                    unit_price = price if price > 0 else 200.0
                else:
                    unit_price = 100.0
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + (shed_count * unit_price)

        # Sell excess WHEAT over 10 units
        wheat_shed_count = state.get_shed_count("WHEAT")
        if wheat_shed_count > 10:
            excess_wheat = wheat_shed_count - 10
            builder.sell("WHEAT", excess_wheat)
            price = state.get_price("WHEAT")
            unit_price = price if price > 0 else CROPS["WHEAT"]["seed"] * 1.75
            self.telemetry.realized_revenue["WHEAT"] = self.telemetry.realized_revenue.get("WHEAT", 0.0) + (excess_wheat * unit_price)

        cumulative_realized_revenue = sum(self.telemetry.realized_revenue.values())
        startup_seed_price = CROPS["TOMATO"]["seed"]  # $50.00
        operating_reserve = 50.0

        # 2. Count Livestock Inventory & Placed State
        cows_in_shed = state.get_shed_count("COW")
        cows_in_inv = sum(state.get_worker_inventory_count(w, "COW") for w in range(total_workers))
        placed_cow_tiles: List[Tuple[int, int]] = []
        active_pasture_tiles: List[Tuple[int, int]] = []

        for y in range(len(state.tiles)):
            for x in range(len(state.tiles[y])):
                t = state.tiles[y][x]
                if isinstance(t, dict) and t.get("kind") == "PASTURE":
                    active_pasture_tiles.append((x, y))
                    if t.get("animal") == "COW":
                        placed_cow_tiles.append((x, y))

        cows_owned = cows_in_shed + cows_in_inv + len(placed_cow_tiles)
        setattr(self.telemetry, "cows_acquired", cows_owned)
        setattr(self.telemetry, "active_cow_count", len(placed_cow_tiles))
        setattr(self.telemetry, "active_pasture_count", len(active_pasture_tiles))

        cash = state.money
        wheat_shed = state.get_shed_count("WHEAT")
        milk_harv = getattr(self.telemetry, "milk_harvested", 0)
        milk_rev = self.telemetry.realized_revenue.get("MILK", 0.0)

        # Macro-Phase State Machine logic
        if getattr(self, "x12_macro_phase", None) is None:
            self.x12_macro_phase = "HYBRID_BOOTSTRAP"

        if self.x12_macro_phase == "HYBRID_BOOTSTRAP" and wheat_shed >= 1:
            self.x12_macro_phase = "FEED_READY"
            self.telemetry.log_event("STATE_CHANGE", state.step, state.day, state.hour, cash, "Phase -> FEED_READY")

        if self.x12_macro_phase in ("HYBRID_BOOTSTRAP", "FEED_READY") and (wheat_shed >= 1 or milk_harv >= 1 or milk_rev > 0 or cows_owned >= 1):
            self.x12_macro_phase = "CROP_RECOVERY"
            self.telemetry.log_event("STATE_CHANGE", state.step, state.day, state.hour, cash, "Phase -> CROP_RECOVERY (Crop Engine Re-activated)")

        active_crop_tiles_count = sum(
            1 for y in range(10) for x in range(10)
            if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "PLANT"
        )
        if self.x12_macro_phase == "CROP_RECOVERY" and active_crop_tiles_count >= 18:
            self.x12_macro_phase = "HYBRID_STEADY_STATE"

        # 3. Progressive Cow Gate for X1.2 (Cow #1 mandatory; Cow #2 ONLY IF active_crop_tiles >= 18 and wheat_shed >= 4; Cow #3/#4 disabled)
        if cows_owned < 2 and cows_in_shed == 0 and cows_in_inv == 0:
            cow_cost = 400.0
            if cows_owned == 0 and wheat_shed >= 1 and cash >= cow_cost:
                can_buy_cow = True
            elif cows_owned == 1 and active_crop_tiles_count >= 18 and wheat_shed >= 4 and cash >= cow_cost + 300.0:
                can_buy_cow = True
            else:
                can_buy_cow = False

            if can_buy_cow:
                builder.buy_animal("COW", 1)
                self.telemetry.spending_livestock += cow_cost
                cows_owned += 1
                cows_in_shed += 1
                cash -= cow_cost
                if getattr(self.telemetry, "day_first_cow", None) is None:
                    setattr(self.telemetry, "day_first_cow", state.day)
                    setattr(self.telemetry, "turn_first_cow", state.step + 1)
                self.telemetry.log_event("BUY_COW", state.step, state.day, state.hour, state.money, f"Purchased Cow #{cows_owned}")

        # 4. Land Expansion Triggers (Q1 and Q2)
        if self.config.enable_land_expansion and owned_quadrants < 2 and state.day >= 1:
            land_cost = 1000.0
            if state.hour == 0 and (wheat_shed >= 1 or milk_harv >= 1) and cash >= land_cost + 150.0:
                builder.buy_land()
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_quadrants = 2
                self.owned_quadrants = 2
                self.telemetry.buy_land_executed_step = state.step
                setattr(self.telemetry, "buy_land_day", state.day)
                cash -= land_cost
                self.telemetry.log_event("BUY_LAND", state.step, state.day, state.hour, state.money, f"Unlocked Q1 Land (Cash: ${cash:.2f})")

        if self.config.enable_land_expansion and self.owned_quadrants == 2 and state.day >= 5:
            q2_cost = 1000.0
            if state.hour == 0 and cash >= q2_cost + 300.0:
                builder.buy_land()
                self.telemetry.spending_land += q2_cost
                self.telemetry.owned_quadrants = 3
                self.owned_quadrants = 3
                setattr(self.telemetry, "q2_buy_land_day", state.day)
                cash -= q2_cost
                self.telemetry.log_event("BUY_LAND_Q2", state.step, state.day, state.hour, state.money, f"Unlocked Q2 Land (Cash: ${cash:.2f})")

        # 5. Tile Partitions & Centered EPU Clusters (Reusing E11-X1.7)
        epu1_crop_tiles = [(2, 2), (2, 3), (2, 4), (3, 2), (4, 2), (1, 3), (1, 4), (3, 1), (4, 1)]
        epu2_crop_tiles = [(5, 2), (5, 3), (5, 4), (6, 2), (6, 3), (6, 4), (7, 2), (7, 3), (7, 4)]
        epu3_crop_tiles = [(2, 5), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (4, 5), (4, 6), (4, 7)]

        farmer_tiles = epu1_crop_tiles
        hand1_tiles = [(2, 3), (2, 4), (1, 3), (1, 4), (3, 1), (4, 1)] + (epu2_crop_tiles if self.owned_quadrants >= 2 else [])
        hand2_tiles = epu2_crop_tiles if self.owned_quadrants >= 2 else []
        hand3_tiles = epu3_crop_tiles if self.owned_quadrants >= 3 else []

        # 6. Workforce Scaling & HIRE Trigger (Up to 4 workers as active tiles scale)
        current_hands = len(hands)
        target_hands = 1
        if active_crop_tiles_count >= 12 or self.owned_quadrants >= 3:
            target_hands = 3
        elif active_crop_tiles_count >= 6 or self.owned_quadrants >= 2:
            target_hands = 2

        if state.hour == 0 and current_hands < target_hands and state.hires_today == 0 and cash >= 50.0:
            fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
            hire_cost = float(fibs[min(current_hands, len(fibs) - 1)])
            if cash - hire_cost >= operating_reserve:
                builder.hire()
                self.telemetry.spending_workforce += hire_cost
                self.telemetry.hires_count += 1
                self.telemetry.log_event("HIRE", state.step, state.day, state.hour, state.money, f"Hired Hand #{current_hands + 1}")
                cash -= hire_cost

        # 7. Seed Purchasing (WHEAT feed reserve + ROI Melons / Crops)
        virtual_seeds: Dict[str, int] = {
            crop: state.get_seed_count(crop) for crop in CROPS.keys()
        }

        if virtual_seeds.get("WHEAT", 0) < 4 and cash >= 10.0:
            buy_qty = min(4 - virtual_seeds.get("WHEAT", 0), int(cash // 10.0))
            if buy_qty > 0:
                builder.buy_seed("WHEAT", buy_qty)
                self.telemetry.spending_seeds += buy_qty * 10.0
                cash -= buy_qty * 10.0
                virtual_seeds["WHEAT"] = virtual_seeds.get("WHEAT", 0) + buy_qty

        available_seed_cash = max(0.0, cash - 150.0)
        target_crop = "MELON"
        target_seed_cost = CROPS[target_crop]["seed"]
        if available_seed_cash >= target_seed_cost and virtual_seeds.get(target_crop, 0) < 6:
            buy_qty = min(6 - virtual_seeds.get(target_crop, 0), int(available_seed_cash // target_seed_cost))
            if buy_qty > 0:
                builder.buy_seed(target_crop, buy_qty)
                self.telemetry.spending_seeds += buy_qty * target_seed_cost
                cash -= buy_qty * target_seed_cost
                virtual_seeds[target_crop] = virtual_seeds.get(target_crop, 0) + buy_qty

        # 8. Worker Action Dispatcher (Farmer + Hands)
        farmer_pos = state.farmer_position
        farmer_act = None

        if cows_in_shed > 0:
            dist_to_shed = abs(farmer_pos[0] - shed_access_tile[0]) + abs(farmer_pos[1] - shed_access_tile[1])
            if dist_to_shed == 0:
                farmer_act = ["PICKUP", "COW", 1]
            else:
                farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], shed_access_tile)

        elif cows_in_inv > 0:
            target_pasture = (3, 3) if len(active_pasture_tiles) == 0 else (3, 4)
            tile_state = state.get_tile(target_pasture[0], target_pasture[1])
            dist = abs(farmer_pos[0] - target_pasture[0]) + abs(farmer_pos[1] - target_pasture[1])

            if tile_state is None or (isinstance(tile_state, dict) and tile_state.get("kind") != "PASTURE"):
                if dist == 0:
                    farmer_act = ["BUILD_PASTURE"]
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], target_pasture)
            else:
                if dist == 0:
                    farmer_act = ["PLACE", "COW"]
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], target_pasture)

        if farmer_act is None and placed_cow_tiles:
            unfed_cow_tiles = [pos for pos in placed_cow_tiles if isinstance(state.get_tile(pos[0], pos[1]), dict) and not state.get_tile(pos[0], pos[1]).get("fed_today", False)]
            if unfed_cow_tiles:
                farmer_wheat = state.get_worker_inventory_count(0, "WHEAT")
                if farmer_wheat > 0:
                    best_tile = min(unfed_cow_tiles, key=lambda p: abs(farmer_pos[0] - p[0]) + abs(farmer_pos[1] - p[1]))
                    dist = abs(farmer_pos[0] - best_tile[0]) + abs(farmer_pos[1] - best_tile[1])
                    if dist == 0:
                        farmer_act = ["FEED"]
                        setattr(self.telemetry, "feed_consumed", getattr(self.telemetry, "feed_consumed", 0) + 1)
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], best_tile)
                elif state.get_shed_count("WHEAT") > 0:
                    dist = abs(farmer_pos[0] - shed_access_tile[0]) + abs(farmer_pos[1] - shed_access_tile[1])
                    if dist == 0:
                        farmer_act = ["PICKUP", "WHEAT", min(5, state.get_shed_count("WHEAT"))]
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], shed_access_tile)

        if farmer_act is None:
            milk_ready_tiles = [pos for pos in placed_cow_tiles if isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("yield_units", 0) > 0]
            if milk_ready_tiles:
                best_tile = min(milk_ready_tiles, key=lambda p: abs(farmer_pos[0] - p[0]) + abs(farmer_pos[1] - p[1]))
                dist = abs(farmer_pos[0] - best_tile[0]) + abs(farmer_pos[1] - best_tile[1])
                if dist == 0:
                    farmer_act = ["HARVEST"]
                    setattr(self.telemetry, "milk_harvested", getattr(self.telemetry, "milk_harvested", 0) + 1)
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], best_tile)

        if farmer_act is None:
            farmer_act, _ = self._compute_e06_worker_action(
                farmer_pos, farmer_tiles, target_crop, target_seed_cost, virtual_seeds, state, worker_id=0
            )

        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        if len(hands) >= 1:
            hand1_pos = hands[0]
            hand1_act, _ = self._compute_e06_worker_action(
                hand1_pos, hand1_tiles, target_crop, target_seed_cost, virtual_seeds, state, worker_id=1
            )
            builder.add_hand_action(hand1_act)

        if len(hands) >= 2 and self.owned_quadrants >= 2 and len(hand2_tiles) > 0:
            hand2_pos = hands[1]
            hand2_act, _ = self._compute_e06_worker_action(
                hand2_pos, hand2_tiles, target_crop, target_seed_cost, virtual_seeds, state, worker_id=2
            )
            builder.add_hand_action(hand2_act)

        if len(hands) >= 3 and self.owned_quadrants >= 3 and len(hand3_tiles) > 0:
            hand3_pos = hands[2]
            hand3_act, _ = self._compute_e06_worker_action(
                hand3_pos, hand3_tiles, target_crop, target_seed_cost, virtual_seeds, state, worker_id=3
            )
            builder.add_hand_action(hand3_act)

        self._record_action_budget(state, farmer_act)

        return builder.build()

    def _get_worker_action_hybrid(
        self, state: GameState, pos: Tuple[int, int], reserved: Set[Tuple[int, int]], worker_id: int, preferred_quadrant: int, q0_tiles: List[Tuple[int, int]], virtual_seeds: Dict[str, int] = None, allow_plant: bool = True
    ) -> List[str]:
        px, py = pos
        day = state.day

        if preferred_quadrant == 1 and self.owned_quadrants >= 2:
            primary_tiles = list(self.q1_crop_tiles)
        elif preferred_quadrant == 2 and self.owned_quadrants >= 3:
            primary_tiles = list(self.q2_crop_tiles)
        elif preferred_quadrant == 3 and self.owned_quadrants >= 4:
            primary_tiles = list(self.q3_crop_tiles)
        else:
            primary_tiles = list(q0_tiles)

        # Inventory Dropoff: Return to shed (4,4) and DROP produce/milk when inventory capacity is reached
        all_products = ["MILK", "WOOL", "WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"]
        worker_inv_total = sum(state.get_worker_inventory_count(worker_id, item) for item in all_products)
        min_dropoff_thresh = 1 if worker_id == 0 else 4  # Farmer drops milk immediately; Hands batch 4 items
        if worker_inv_total >= min_dropoff_thresh:
            shed_access = (4, 4)
            if (px, py) == shed_access:
                for item_name in all_products:
                    cnt = state.get_worker_inventory_count(worker_id, item_name)
                    if cnt > 0:
                        self.telemetry.record_worker_step(worker_id, "productive")
                        return ["DROP", item_name, cnt]
            else:
                self.telemetry.record_worker_step(worker_id, "movement")
                return self._move_towards(px, py, shed_access)

        secondary_tiles = []

        # Zero-distance priority: water current standing tile immediately if unwatered
        curr_tile = state.get_tile(px, py)
        if isinstance(curr_tile, dict) and curr_tile.get("kind") == "PLANT" and not curr_tile.get("watered_today", False):
            if (px, py) not in reserved:
                reserved.add((px, py))
                self.telemetry.record_worker_step(worker_id, "productive")
                self.telemetry.crops_watered += 1
                return ["WATER"]

        # 1. EMERGENCY WATER priority: consecutive_unwatered >= 1 (ABSOLUTE PRIORITY #1)
        emergency_water_act = self._find_best_task_action(state, px, py, primary_tiles, secondary_tiles, reserved, worker_id, task_type="EMERGENCY_WATER", virtual_seeds=virtual_seeds)
        if emergency_water_act:
            return emergency_water_act

        # 2. TIME-CRITICAL HARVEST
        harvest_act = self._find_best_task_action(state, px, py, primary_tiles, secondary_tiles, reserved, worker_id, task_type="HARVEST", virtual_seeds=virtual_seeds)
        if harvest_act:
            return harvest_act

        # 3. WORKING-SET WEED RECOVERY (DIG on WEED in working set)
        dig_act = self._find_best_task_action(state, px, py, primary_tiles, secondary_tiles, reserved, worker_id, task_type="DIG", virtual_seeds=virtual_seeds)
        if dig_act:
            return dig_act

        # 4. NORMAL WATER
        water_act = self._find_best_task_action(state, px, py, primary_tiles, secondary_tiles, reserved, worker_id, task_type="WATER", virtual_seeds=virtual_seeds)
        if water_act:
            return water_act

        # 5. REPLANT / PLANT (Strictly gated by working_set_capacity = 4 * active_workers and allow_plant)
        if allow_plant:
            active_workers = 1 + len(getattr(state, "hands_positions", []))
            total_active_plants = sum(1 for y in range(10) for x in range(10) if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "PLANT")
            if total_active_plants < 4 * active_workers:
                plant_act = self._find_best_task_action(state, px, py, primary_tiles, secondary_tiles, reserved, worker_id, task_type="PLANT", virtual_seeds=virtual_seeds)
                if plant_act:
                    return plant_act

        if isinstance(curr_tile, dict) and curr_tile.get("kind") == "PLANT":
            self.telemetry.record_worker_step(worker_id, "productive")
            return ["WATER"]

        if curr_tile is None or (isinstance(curr_tile, dict) and curr_tile.get("kind") in ("EMPTY", "SOIL")):
            self.telemetry.record_worker_step(worker_id, "productive")
            return ["DIG"]

        self.telemetry.record_worker_step(worker_id, "idle")
        return ["PASS"]

    def _decide_e12_hybrid_full_scaling(self, state: GameState) -> Dict[str, Any]:
        """
        E12-X1.3 — Hybrid Full Crop Scaling strategy.
        Preserves E12-X1.2 validated livestock opening (Cow #1 + Feed ring + WHEAT buffer),
        then fully connects the E11-X1.7 crop scaling engine across all 21 Q0 non-livestock tiles
        plus Q1 (25 tiles) and Q2 (25 tiles) to reach 24-26+ active crop tiles.
        """
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        raw_quads = state.my_farm.get("unlocked_quadrants", [0])
        owned_quadrants = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        self.owned_quadrants = max(self.owned_quadrants, owned_quadrants)
        self.telemetry.owned_quadrants = self.owned_quadrants

        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(state)

        livestock_core_reserved = [(3, 3), (3, 4), (4, 3), (4, 4)]
        shed_access_tile = (4, 4)

        builder = ActionBuilder()

        # 1. Market Phase: Sell MILK and non-WHEAT crops immediately (keep WHEAT feed buffer in shed)
        for product in [c for c in CROPS.keys() if c != "WHEAT"] + ["MILK", "WOOL"]:
            shed_count = state.get_shed_count(product)
            if shed_count > 0:
                builder.sell(product, shed_count)
                price = state.get_price(product)
                if product in CROPS:
                    unit_price = price if price > 0 else CROPS[product]["seed"] * 1.75
                elif product == "MILK":
                    unit_price = price if price > 0 else 160.0
                elif product == "WOOL":
                    unit_price = price if price > 0 else 200.0
                else:
                    unit_price = 100.0
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + (shed_count * unit_price)

        # Sell excess WHEAT over 10 units
        wheat_shed_count = state.get_shed_count("WHEAT")
        if wheat_shed_count > 10:
            excess_wheat = wheat_shed_count - 10
            builder.sell("WHEAT", excess_wheat)
            price = state.get_price("WHEAT")
            unit_price = price if price > 0 else CROPS["WHEAT"]["seed"] * 1.75
            self.telemetry.realized_revenue["WHEAT"] = self.telemetry.realized_revenue.get("WHEAT", 0.0) + (excess_wheat * unit_price)

        cash = state.money
        wheat_shed = state.get_shed_count("WHEAT")
        milk_harv = getattr(self.telemetry, "milk_harvested", 0)

        # 2. Count Livestock Inventory & Placed State
        cows_in_shed = state.get_shed_count("COW")
        cows_in_inv = sum(state.get_worker_inventory_count(w, "COW") for w in range(total_workers))
        placed_cow_tiles: List[Tuple[int, int]] = []
        active_pasture_tiles: List[Tuple[int, int]] = []

        for y in range(len(state.tiles)):
            for x in range(len(state.tiles[y])):
                t = state.tiles[y][x]
                if isinstance(t, dict) and t.get("kind") == "PASTURE":
                    active_pasture_tiles.append((x, y))
                    if t.get("animal") == "COW":
                        placed_cow_tiles.append((x, y))

        cows_owned = cows_in_shed + cows_in_inv + len(placed_cow_tiles)
        setattr(self.telemetry, "cows_acquired", cows_owned)
        setattr(self.telemetry, "active_cow_count", len(placed_cow_tiles))
        setattr(self.telemetry, "active_pasture_count", len(active_pasture_tiles))

        active_crop_tiles_count = sum(
            1 for y in range(10) for x in range(10)
            if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "PLANT"
        )

        # 3. Progressive Cow Gate for X1.3 (Cow #1 mandatory; Cow #2 ONLY IF active_crop_tiles >= 24)
        if cows_owned < 2 and cows_in_shed == 0 and cows_in_inv == 0:
            cow_cost = 400.0
            if cows_owned == 0 and wheat_shed >= 1 and cash >= cow_cost:
                can_buy_cow = True
            elif cows_owned == 1 and active_crop_tiles_count >= 24 and wheat_shed >= 4 and cash >= cow_cost + 500.0:
                can_buy_cow = True
            else:
                can_buy_cow = False

            if can_buy_cow:
                builder.buy_animal("COW", 1)
                self.telemetry.spending_livestock += cow_cost
                cows_owned += 1
                cows_in_shed += 1
                cash -= cow_cost
                if getattr(self.telemetry, "day_first_cow", None) is None:
                    setattr(self.telemetry, "day_first_cow", state.day)
                    setattr(self.telemetry, "turn_first_cow", state.step + 1)
                self.telemetry.log_event("BUY_COW", state.step, state.day, state.hour, state.money, f"Purchased Cow #{cows_owned}")

        # 4. Dynamic Land Expansion Triggers (Q1, Q2, Q3)
        if self.config.enable_land_expansion and self.owned_quadrants < 2 and state.day >= 1:
            land_cost = 1000.0
            if cash >= land_cost + 50.0:
                if not any(isinstance(cmd, list) and cmd[0] == "BUY_LAND" for cmd in builder.market_orders):
                    builder.market_orders.append(["BUY_LAND"])
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_quadrants = 2
                self.owned_quadrants = 2
                self.telemetry.buy_land_executed_step = state.step
                setattr(self.telemetry, "buy_land_day", state.day)
                cash -= land_cost
                self.telemetry.log_event("BUY_LAND", state.step, state.day, state.hour, state.money, f"Unlocked Q1 Land (Cash: ${cash:.2f})")

        if self.config.enable_land_expansion and self.owned_quadrants == 2 and state.day >= 3:
            q2_cost = 1000.0
            if cash >= q2_cost + 50.0:
                if not any(isinstance(cmd, list) and cmd[0] == "BUY_LAND" for cmd in builder.market_orders):
                    builder.market_orders.append(["BUY_LAND"])
                self.telemetry.spending_land += q2_cost
                self.telemetry.owned_quadrants = 3
                self.owned_quadrants = 3
                setattr(self.telemetry, "q2_buy_land_day", state.day)
                cash -= q2_cost
                self.telemetry.log_event("BUY_LAND_Q2", state.step, state.day, state.hour, state.money, f"Unlocked Q2 Land (Cash: ${cash:.2f})")

        if self.config.enable_land_expansion and self.owned_quadrants == 3 and state.day >= 7:
            q3_cost = 1000.0
            if cash >= q3_cost + 50.0:
                if not any(isinstance(cmd, list) and cmd[0] == "BUY_LAND" for cmd in builder.market_orders):
                    builder.market_orders.append(["BUY_LAND"])
                self.telemetry.spending_land += q3_cost
                self.telemetry.owned_quadrants = 4
                self.owned_quadrants = 4
                cash -= q3_cost
                self.telemetry.log_event("BUY_LAND_Q3", state.step, state.day, state.hour, state.money, f"Unlocked Q3 Land (Cash: ${cash:.2f})")

        # 5. Workforce Scaling (Multi-hire workforce as active tiles and land scale)
        operating_reserve = 50.0
        cash = self._hire_workers_if_needed(state, builder, cash, operating_reserve)

        # 6. Full Seed Purchasing Logic ($50 operating reserve)
        operating_reserve = 50.0
        self._buy_seeds_if_needed(state, builder, cash, operating_reserve, operating_reserve)

        # 7. Worker Action Dispatcher (Farmer + Hands)
        farmer_pos = state.farmer_position
        farmer_act = None

        if cows_in_shed > 0:
            dist_to_shed = abs(farmer_pos[0] - shed_access_tile[0]) + abs(farmer_pos[1] - shed_access_tile[1])
            if dist_to_shed == 0:
                farmer_act = ["PICKUP", "COW", 1]
            else:
                farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], shed_access_tile)

        elif cows_in_inv > 0:
            target_pasture = (3, 3) if len(active_pasture_tiles) == 0 else (3, 4)
            tile_state = state.get_tile(target_pasture[0], target_pasture[1])
            dist = abs(farmer_pos[0] - target_pasture[0]) + abs(farmer_pos[1] - target_pasture[1])

            if tile_state is None or (isinstance(tile_state, dict) and tile_state.get("kind") != "PASTURE"):
                if dist == 0:
                    farmer_act = ["BUILD_PASTURE"]
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], target_pasture)
            else:
                if dist == 0:
                    farmer_act = ["PLACE", "COW"]
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], target_pasture)

        if farmer_act is None and placed_cow_tiles:
            unfed_cow_tiles = [pos for pos in placed_cow_tiles if isinstance(state.get_tile(pos[0], pos[1]), dict) and not state.get_tile(pos[0], pos[1]).get("fed_today", False)]
            if unfed_cow_tiles:
                farmer_wheat = state.get_worker_inventory_count(0, "WHEAT")
                if farmer_wheat > 0:
                    best_tile = min(unfed_cow_tiles, key=lambda p: abs(farmer_pos[0] - p[0]) + abs(farmer_pos[1] - p[1]))
                    dist = abs(farmer_pos[0] - best_tile[0]) + abs(farmer_pos[1] - best_tile[1])
                    if dist == 0:
                        farmer_act = ["FEED"]
                        setattr(self.telemetry, "feed_consumed", getattr(self.telemetry, "feed_consumed", 0) + 1)
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], best_tile)
                elif state.get_shed_count("WHEAT") > 0:
                    dist = abs(farmer_pos[0] - shed_access_tile[0]) + abs(farmer_pos[1] - shed_access_tile[1])
                    if dist == 0:
                        farmer_act = ["PICKUP", "WHEAT", min(5, state.get_shed_count("WHEAT"))]
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], shed_access_tile)

        if farmer_act is None:
            milk_ready_tiles = [pos for pos in placed_cow_tiles if isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("yield_units", 0) > 0]
            if milk_ready_tiles:
                best_tile = min(milk_ready_tiles, key=lambda p: abs(farmer_pos[0] - p[0]) + abs(farmer_pos[1] - p[1]))
                dist = abs(farmer_pos[0] - best_tile[0]) + abs(farmer_pos[1] - best_tile[1])
                if dist == 0:
                    farmer_act = ["HARVEST"]
                    setattr(self.telemetry, "milk_harvested", getattr(self.telemetry, "milk_harvested", 0) + 1)
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], best_tile)

        reserved_tiles: Set[Tuple[int, int]] = set(livestock_core_reserved)
        q0_hybrid_crop_tiles = [t for t in self.q0_crop_tiles if t not in livestock_core_reserved]
        virtual_seeds: Dict[str, int] = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}

        if farmer_act is None:
            farmer_act = self._get_worker_action_hybrid(state, farmer_pos, reserved_tiles, worker_id=0, preferred_quadrant=0, q0_tiles=q0_hybrid_crop_tiles, virtual_seeds=virtual_seeds)

        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        quadrant_assignments = [0, 1, 1, 2, 2, 3, 3]

        for idx, hand_pos in enumerate(hands):
            worker_id = idx + 1
            pref_q = quadrant_assignments[min(idx, len(quadrant_assignments) - 1)]
            if pref_q >= self.owned_quadrants:
                pref_q = 0
            h_act = self._get_worker_action_hybrid(state, hand_pos, reserved_tiles, worker_id=worker_id, preferred_quadrant=pref_q, q0_tiles=q0_hybrid_crop_tiles, virtual_seeds=virtual_seeds)
            builder.add_hand_action(h_act)

        self._record_action_budget(state, farmer_act)

        return builder.build()

    def _is_expansion_ready(self, state: GameState, target_quadrant: int, cash: float) -> bool:
        if self.owned_quadrants >= target_quadrant:
            return False

        land_cost = 1000.0
        operating_reserve = 50.0
        financial_required = land_cost + operating_reserve

        # 1. Financial Readiness
        if cash < financial_required:
            return False

        # 2. Harvest Yield / Production Control
        harvested_count = self.telemetry.crops_harvested
        if target_quadrant == 2 and harvested_count < 6:
            return False
        elif target_quadrant == 3 and harvested_count < 20:
            return False
        elif target_quadrant == 4 and harvested_count < 40:
            return False

        # 3. Local Saturation
        active_crops = sum(
            1 for y in range(10) for x in range(10)
            if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "PLANT"
        )

        if target_quadrant == 2 and active_crops < 3:
            return False
        elif target_quadrant == 3 and active_crops < 8:
            return False
        elif target_quadrant == 4 and active_crops < 16:
            return False

        # 4. Crop Control (Water Backlog)
        unwatered_count = 0
        for y in range(10):
            for x in range(10):
                t = state.get_tile(x, y)
                if isinstance(t, dict) and t.get("kind") == "PLANT" and not t.get("watered_today", False):
                    unwatered_count += 1
        if unwatered_count > 2:
            return False

        return True

    def _next_land_cost(self, state: GameState) -> Optional[float]:
        raw_quads = state.my_farm.get("unlocked_quadrants", ["NW"])
        owned = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        land_prices = [1000.0, 2000.0, 4000.0]
        extra_owned = max(0, owned - 1)
        if extra_owned >= len(land_prices):
            return None
        return land_prices[extra_owned]

    def _x19_owned_tiles(self, state: GameState) -> List[Tuple[int, int]]:
        tiles = []
        for y in range(10):
            for x in range(10):
                if state.get_tile(x, y) != "LOCKED":
                    tiles.append((x, y))
        return tiles

    def _x19_center_distance(self, pos: Tuple[int, int]) -> float:
        x, y = pos
        return min(abs(x - cx) + abs(y - cy) for cx, cy in self.livestock_core_tiles)

    def _x19_q0_external_tiles(self) -> List[Tuple[int, int]]:
        return [
            (3, 2), (4, 2), (2, 3), (2, 4),
            (2, 2), (3, 1), (4, 1), (1, 3), (1, 4),
            (1, 2), (2, 1), (1, 1), (0, 3), (0, 4), (3, 0), (4, 0),
            (0, 0), (1, 0), (2, 0), (0, 1), (0, 2),
        ]

    def _x19_centered_crop_tiles(self, state: GameState) -> List[Tuple[int, int]]:
        return sorted(
            [pos for pos in self._x19_owned_tiles(state) if pos not in self.livestock_core_tiles and pos not in self._x19_extra_pasture_tiles()],
            key=lambda p: (self._x19_center_distance(p), abs(p[0] - 4) + abs(p[1] - 4), p[1], p[0])
        )

    def _x19_extra_pasture_tiles(self) -> List[Tuple[int, int]]:
        return [(5, 4), (4, 5), (5, 3), (3, 5), (6, 4), (4, 6), (5, 2), (2, 5)]

    def _x110_core_a(self) -> List[Tuple[int, int]]:
        return [(3, 3), (3, 4), (4, 3), (4, 4)]

    def _x110_core_b(self) -> List[Tuple[int, int]]:
        return [(5, 3), (5, 4), (6, 3), (6, 4)]

    def _x110_livestock_tiles(self) -> List[Tuple[int, int]]:
        return self._x110_core_a() + self._x110_core_b()

    def _x110_owned_radius_tiles(self, state: GameState, radius: int = 5) -> List[Tuple[int, int]]:
        targets = []
        for pos in self._x19_owned_tiles(state):
            if pos in self._x110_livestock_tiles():
                continue
            if self._x19_center_distance(pos) <= radius:
                targets.append(pos)
        return sorted(targets, key=lambda p: (self._x19_center_distance(p), abs(p[0] - 4) + abs(p[1] - 4), p[1], p[0]))

    def _x110_productive_radius_utilization(self, state: GameState) -> float:
        targets = self._x110_owned_radius_tiles(state)
        if not targets:
            return 1.0
        productive = 0
        for x, y in targets:
            tile = state.get_tile(x, y)
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                productive += 1
        return productive / len(targets)

    def _x110_crop_value_rank(self, state: GameState) -> List[str]:
        if state.day <= 4:
            return ["CARROT", "TOMATO", "STRAWBERRY", "MELON"]
        if state.day <= 9:
            return ["MELON", "TOMATO", "CARROT", "STRAWBERRY"]
        if state.day <= 12:
            return ["TOMATO", "CARROT", "STRAWBERRY", "MELON"]
        if state.day <= 22:
            return ["TOMATO", "STRAWBERRY", "CARROT", "MELON"]
        return ["TOMATO", "STRAWBERRY", "CARROT", "MELON"]
        scored = []
        for crop, data in CROPS.items():
            if crop == "WHEAT":
                continue
            price = max(1.0, state.get_price(crop))
            if data.get("ongoing"):
                # Approximate the first 30-day window while favoring lower replant burden.
                remaining = max(1, 30 - max(0, state.day))
                cycles = max(1, (remaining - data["first_yield_day"]) // max(1, data.get("interval", 1)) + 1)
                units = min(data["max_yield"], cycles)
                burden = 1.0 + 1.0 / max(1, data["first_yield_day"])
                tile_day_value = (price * units / max(1, remaining)) / burden
            else:
                tile_day_value = price * data.get("max_yield", 1) / max(1, data["max_yield_day"])
            scored.append((tile_day_value, crop))
        scored.sort(reverse=True)
        return [crop for _, crop in scored]

    def _x110_required_wheat_buffer(self, state: GameState) -> int:
        active_animals = len(self._x19_animal_tiles(state))
        near_term = max(8, active_animals * 3)
        return near_term + 8

    def _x110_select_crop(self, state: GameState, virtual_seeds: Dict[str, int], wheat_targets_remaining: int) -> Optional[str]:
        if wheat_targets_remaining > 0 and virtual_seeds.get("WHEAT", 0) > 0:
            return "WHEAT"
        for crop in self._x110_crop_value_rank(state):
            if virtual_seeds.get(crop, 0) > 0:
                return crop
        if virtual_seeds.get("CARROT", 0) > 0:
            return "CARROT"
        if virtual_seeds.get("WHEAT", 0) > 0:
            return "WHEAT"
        return None

    def _x110_worker_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        target_tiles: List[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
        reserved: Set[Tuple[int, int]],
        wheat_targets_remaining: int,
    ) -> Tuple[List[str], int]:
        px, py = pos
        products = ["MILK", "WHEAT", "MELON", "CARROT", "TOMATO", "STRAWBERRY"]
        inv_total = sum(state.get_worker_inventory_count(worker_id, item) for item in products)
        if inv_total >= 4 or (state.day >= 28 and inv_total > 0):
            if (px, py) == (4, 4):
                for item in products:
                    count = state.get_worker_inventory_count(worker_id, item)
                    if count > 0:
                        return ["DROP", item, count], wheat_targets_remaining
            return self._move_towards(px, py, (4, 4)), wheat_targets_remaining

        current = state.get_tile(px, py)
        if (px, py) in target_tiles and current is None:
            crop = self._x110_select_crop(state, virtual_seeds, wheat_targets_remaining)
            if crop:
                reserved.add((px, py))
                virtual_seeds[crop] -= 1
                if crop == "WHEAT" and wheat_targets_remaining > 0:
                    wheat_targets_remaining -= 1
                return ["PLANT", crop], wheat_targets_remaining
        if (
            (px, py) in target_tiles
            and isinstance(current, dict)
            and current.get("kind") == "WEED"
        ):
            reserved.add((px, py))
            return ["DIG"], wheat_targets_remaining
        if (
            (px, py) in target_tiles
            and isinstance(current, dict)
            and current.get("kind") == "PLANT"
            and not current.get("watered_today", False)
        ):
            reserved.add((px, py))
            return ["WATER"], wheat_targets_remaining

        task_candidates = []
        productive_now = sum(
            1 for tx, ty in target_tiles
            if isinstance(state.get_tile(tx, ty), dict) and state.get_tile(tx, ty).get("kind") == "PLANT"
        )
        below_cps_target = productive_now / max(1, len(target_tiles)) < 0.95
        harvest_priority = 1 if below_cps_target else 0
        plant_priority = 0 if below_cps_target else 3
        weed_priority = 0 if below_cps_target else 2
        for target in target_tiles:
            if target in reserved:
                continue
            tile = state.get_tile(target[0], target[1])
            if state.day < 29 and isinstance(tile, dict) and tile.get("kind") == "PLANT" and self._tile_matches_task(state, tile, target[0], target[1], state.day, "HARVEST"):
                task_candidates.append((harvest_priority, abs(px - target[0]) + abs(py - target[1]), target, "HARVEST"))
            elif state.day == 0 and tile is None:
                crop = self._x110_select_crop(state, virtual_seeds, wheat_targets_remaining)
                if crop:
                    task_candidates.append((1, abs(px - target[0]) + abs(py - target[1]), target, "PLANT"))
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT" and not tile.get("watered_today", False):
                task_candidates.append((1, abs(px - target[0]) + abs(py - target[1]), target, "WATER"))
            elif isinstance(tile, dict) and tile.get("kind") == "WEED":
                task_candidates.append((weed_priority, abs(px - target[0]) + abs(py - target[1]), target, "DIG"))
            elif tile is None:
                crop = self._x110_select_crop(state, virtual_seeds, wheat_targets_remaining)
                if crop:
                    task_candidates.append((plant_priority, abs(px - target[0]) + abs(py - target[1]), target, "PLANT"))

        if not task_candidates:
            return ["PASS"], wheat_targets_remaining
        _, _, target, task = min(task_candidates, key=lambda item: (item[0], item[1], self._x19_center_distance(item[2]), item[2][1], item[2][0]))
        reserved.add(target)
        if target != (px, py):
            return self._move_towards(px, py, target), wheat_targets_remaining
        if task == "PLANT":
            crop = self._x110_select_crop(state, virtual_seeds, wheat_targets_remaining)
            if crop:
                virtual_seeds[crop] -= 1
                if crop == "WHEAT" and wheat_targets_remaining > 0:
                    wheat_targets_remaining -= 1
                return ["PLANT", crop], wheat_targets_remaining
            return ["PASS"], wheat_targets_remaining
        return [task], wheat_targets_remaining

    def _x110_livestock_action(self, state: GameState) -> List[str]:
        fx, fy = state.farmer_position
        livestock_products = ["MILK", "WHEAT", "MELON", "CARROT", "TOMATO", "STRAWBERRY"]
        if state.day >= 28:
            for item in livestock_products:
                count = state.get_worker_inventory_count(0, item)
                if count > 0:
                    return ["DROP", item, count] if state.farmer_position == (4, 4) else self._move_towards(fx, fy, (4, 4))
            return ["PASS"]
        cow_in_shed = state.get_shed_count("COW")
        cow_in_inv = state.get_worker_inventory_count(0, "COW")
        animals = self._x19_animal_tiles(state)

        target_core = self._x110_core_a() if len(self._x18_core_pastures(state)) < 4 or state.day <= 1 else self._x110_livestock_tiles()
        missing_pastures = [
            pos for pos in target_core
            if state.get_tile(pos[0], pos[1]) is None
        ]
        if missing_pastures and cow_in_inv == 0:
            target = missing_pastures[0]
            return ["BUILD_PASTURE"] if target == state.farmer_position else self._move_towards(fx, fy, target)

        if state.day == 0:
            return ["PASS"]

        unfed = [
            pos for pos in animals
            if isinstance(state.get_tile(pos[0], pos[1]), dict)
            and not state.get_tile(pos[0], pos[1]).get("fed_today", False)
        ]
        if unfed:
            if state.get_worker_inventory_count(0, "WHEAT") <= 0:
                if state.get_shed_count("WHEAT") > 0:
                    return ["PICKUP", "WHEAT", min(8, state.get_shed_count("WHEAT"))] if state.farmer_position == (4, 4) else self._move_towards(fx, fy, (4, 4))
            else:
                target = min(unfed, key=lambda p: (abs(fx - p[0]) + abs(fy - p[1]), self._x19_center_distance(p)))
                return ["FEED"] if target == state.farmer_position else self._move_towards(fx, fy, target)

        if cow_in_shed > 0 and cow_in_inv == 0:
            return ["PICKUP", "COW", 1] if state.farmer_position == (4, 4) else self._move_towards(fx, fy, (4, 4))
        if cow_in_inv > 0:
            free = [
                pos for pos in self._x110_livestock_tiles()
                if isinstance(state.get_tile(pos[0], pos[1]), dict)
                and state.get_tile(pos[0], pos[1]).get("kind") == "PASTURE"
                and "animal" not in state.get_tile(pos[0], pos[1])
            ]
            if free:
                target = free[0]
                return ["PLACE", "COW"] if target == state.farmer_position else self._move_towards(fx, fy, target)

        milk_ready = [
            pos for pos in animals
            if isinstance(state.get_tile(pos[0], pos[1]), dict)
            and state.get_tile(pos[0], pos[1]).get("yield_units", 0) > 0
        ]
        if milk_ready and state.day < 29:
            target = min(milk_ready, key=lambda p: (abs(fx - p[0]) + abs(fy - p[1]), self._x19_center_distance(p)))
            return ["HARVEST"] if target == state.farmer_position else self._move_towards(fx, fy, target)
        return ["PASS"]

    def _x110_cps_stable_for_q2(self, state: GameState) -> bool:
        if self._x18_owned_quadrants(state) != 2:
            return False
        if not hasattr(self, "_x110_stable_days"):
            self._x110_stable_days = set()
        if state.hour == 23:
            util = self._x110_productive_radius_utilization(state)
            if util >= 0.95:
                self._x110_stable_days.add(state.day)
        return any(
            day in self._x110_stable_days and day - 1 in self._x110_stable_days
            for day in self._x110_stable_days
            if day <= state.day
        )

    def _decide_e12_q0q1_80k_engine_x111(self, state: GameState) -> Dict[str, Any]:
        """E12-X1.11 — Q0+Q1 80k Economic Engine.

        4 Pillars:
        1. Early Livestock Bootstrap (Day 2-6) + Economic Gate 4→8 cows
        2. Dynamic Wheat Feed Sizing + Emergency-only retail wheat
        3. Phased Dynamic Crop Allocation (Net EV/Tile-Day) + Endgame Sprint
        4. 6-worker team with locality dispatch, harvest-first priority
        """
        return self._decide_e12_q0q1_verified_epu_x111(state)

    def _decide_e12_q0q1_verified_epu_x111(self, state: GameState) -> Dict[str, Any]:
        """X1.11 production route: verified E06/EPU crop core, Q0+Q1 capped.

        Local iterations showed that adding generic dense tiling and early
        livestock reduced revenue sharply. The best reproducible Q0+Q1 engine
        in this repository is the E06 replicated core at EPU level 3, so X1.11
        routes through that mechanism while preserving a distinct strategy mode
        and telemetry surface for ceiling analysis.
        """
        original_mode = self.config.productive_core_mode
        original_epu_level = self.config.epu_level
        original_enable_land_expansion = self.config.enable_land_expansion
        original_multi_hire_mode = self.config.multi_hire_mode

        self.config.productive_core_mode = "E06_REPLICATED"
        self.config.epu_level = 3
        self.config.enable_land_expansion = True
        self.config.multi_hire_mode = "CORRECTED_MULTI"
        try:
            result = self._decide_e06_replicated(state)
        finally:
            self.config.productive_core_mode = original_mode
            self.config.epu_level = original_epu_level
            self.config.enable_land_expansion = original_enable_land_expansion
            self.config.multi_hire_mode = original_multi_hire_mode

        self.owned_quadrants = min(self.owned_quadrants, 2)
        self.telemetry.owned_quadrants = self.owned_quadrants
        if not hasattr(self, "_x111_milk_revenue_total"):
            self._x111_milk_revenue_total = 0.0
            self._x111_crop_revenue_total = sum(self.telemetry.realized_revenue.values())
            self._x111_retail_wheat_spend = 0.0
            self._x111_harvests_count = self.telemetry.crops_harvested
            self._x111_milk_sold_total = 0
            self._x111_milk_harvested_count = 0
            self._x111_wheat_fed_count = 0
            self._x111_movement_steps = self.telemetry.worker_movement_steps
            self._x111_action_steps = self.telemetry.worker_action_steps
            self._x111_pastures_built = 0
            self._x111_cows_bought = 0
            self._x111_seeds_spent = self.telemetry.spending_seeds
        else:
            self._x111_crop_revenue_total = sum(self.telemetry.realized_revenue.values())
            self._x111_harvests_count = self.telemetry.crops_harvested
            self._x111_movement_steps = self.telemetry.worker_movement_steps
            self._x111_action_steps = self.telemetry.worker_action_steps
            self._x111_seeds_spent = self.telemetry.spending_seeds
        return result

    def _decide_e12_q0q1_dense_epu_x111(self, state: GameState) -> Dict[str, Any]:
        """Q0+Q1-only dense crop engine derived from the verified E06/EPU core.

        The first X1.11 BUILD draft replaced the profitable E06 dispatcher with a
        generic pasture-first scheduler and collapsed to sub-$1k. This engine
        restores the proven water/harvest/plant EPU loop, caps land at Q1, and
        scales to six actors over 45 crop tiles.
        """
        if state.step == 0:
            self.telemetry.starting_money = state.money
            self._x111_milk_revenue_total = 0.0
            self._x111_crop_revenue_total = 0.0
            self._x111_retail_wheat_spend = 0.0
            self._x111_harvests_count = 0
            self._x111_milk_sold_total = 0
            self._x111_milk_harvested_count = 0
            self._x111_wheat_fed_count = 0
            self._x111_movement_steps = 0
            self._x111_action_steps = 0
            self._x111_pastures_built = 0
            self._x111_cows_bought = 0
            self._x111_seeds_spent = 0.0

        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        builder = ActionBuilder()
        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(self.telemetry.peak_simultaneous_workers, total_workers)
        self.telemetry.worker_hours += total_workers
        self.owned_quadrants = max(self.owned_quadrants, self._x18_owned_quadrants(state))
        self.telemetry.owned_quadrants = self.owned_quadrants

        owned = self._x18_owned_quadrants(state)
        cash = state.money

        # Sell shed inventory immediately; final money is cash-only in local eval.
        for crop_name in CROPS.keys():
            count = state.get_shed_count(crop_name)
            if count > 0:
                builder.sell(crop_name, count)
                price = state.get_price(crop_name)
                unit_price = price if price > 0 else CROPS[crop_name]["seed"] * 1.75
                revenue = count * unit_price
                self._x111_crop_revenue_total += revenue
                self.telemetry.realized_revenue[crop_name] = self.telemetry.realized_revenue.get(crop_name, 0.0) + revenue
                self.telemetry.quantities_sold[crop_name] = self.telemetry.quantities_sold.get(crop_name, 0) + count

        # Buy Q1 only, after there is enough cash to keep the crop loop alive.
        if self.config.enable_land_expansion and owned < 2 and state.day >= 1 and state.hour == 0 and cash >= 1450.0:
            builder.buy_land()
            cash -= 1000.0
            self.telemetry.spending_land += 1000.0
            self.telemetry.owned_quadrants = 2
            self.owned_quadrants = 2
            self.telemetry.buy_land_executed_step = state.step
            self.telemetry.log_event("BUY_LAND", state.step, state.day, state.hour, state.money, "X1.11 bought Q1; Q2 disabled")
            owned = 2

        partitions = self._x111_dense_epu_partitions(owned)
        managed_tiles = [tile for tiles in partitions for tile in tiles]
        active_tiles = sum(
            1 for x, y in managed_tiles
            if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "PLANT"
        )
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, active_tiles)

        # Hire to the number of active partitions, capped at five hands.
        target_hands = max(0, min(5, len(partitions) - 1))
        current_hands = len(hands)
        if state.hour == 0 and current_hands < target_hands:
            hire_cap = min(target_hands - current_hands, self.config.max_hires_per_day)
            for _ in range(hire_cap):
                if cash >= 75.0:
                    builder.hire()
                    cash -= 1.0
                    self.telemetry.spending_workforce += 1.0
                    self.telemetry.hires_count += 1

        # On-demand seed buying for empty slots. This mirrors E06 but leaves a
        # cash floor for Q1 and avoids the failed fixed bulk buy from the draft.
        target_crop = self._x111_best_dense_crop(state, cash)
        target_seed_cost = CROPS[target_crop]["seed"]
        empty_tiles = [pos for pos in managed_tiles if state.get_tile(pos[0], pos[1]) is None]
        target_seeds_owned = state.get_seed_count(target_crop)
        needed = max(0, len(empty_tiles) - target_seeds_owned)
        reserve = 1200.0 if owned < 2 and state.day <= 8 else 50.0
        if needed > 0 and cash >= reserve + target_seed_cost:
            buy_qty = min(needed, int((cash - reserve) // target_seed_cost))
            if buy_qty > 0:
                builder.buy_seed(target_crop, buy_qty)
                spend = buy_qty * target_seed_cost
                cash -= spend
                target_seeds_owned += buy_qty
                self._x111_seeds_spent += spend
                self.telemetry.spending_seeds += spend

        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        virtual_seeds[target_crop] = max(virtual_seeds.get(target_crop, 0), target_seeds_owned)

        actor_positions = [state.farmer_position] + hands
        for actor_idx, assigned_tiles in enumerate(partitions[:len(actor_positions)]):
            action, _ = self._compute_e06_worker_action(
                actor_positions[actor_idx],
                assigned_tiles,
                target_crop,
                target_seed_cost,
                virtual_seeds,
                state,
                worker_id=actor_idx,
            )
            if actor_idx == 0:
                self._apply_builder_action(builder, action, is_farmer=True)
            else:
                builder.add_hand_action(action)
            if action and action[0] in ("WATER", "HARVEST", "PLANT", "DIG"):
                self._x111_action_steps += 1
                if action[0] == "HARVEST":
                    self._x111_harvests_count += 1
            elif action and action[0] in ("NORTH", "SOUTH", "EAST", "WEST"):
                self._x111_movement_steps += 1

        return builder.build()

    def _x111_dense_epu_partitions(self, owned_quadrants: int) -> List[List[Tuple[int, int]]]:
        """Actor-local Q0+Q1 tile partitions, capped at six actors."""
        partitions = [
            [(0, 0), (0, 1), (0, 2), (1, 0)],
            [(1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
        ]
        if owned_quadrants >= 2:
            partitions.extend([
                [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)],
                [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)],
                [(5, 3), (6, 3), (7, 3), (8, 3), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4)],
                [(0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4), (3, 3), (3, 4), (4, 3)],
            ])
        return partitions

    def _x111_best_dense_crop(self, state: GameState, cash: float) -> str:
        """Pick a crop by expected cash density with horizon guard."""
        if state.day >= 23:
            affordable = ["CARROT", "WHEAT"]
        elif state.day >= 19:
            affordable = ["TOMATO", "CARROT", "WHEAT"]
        elif state.day <= 16:
            affordable = ["MELON", "STRAWBERRY", "TOMATO", "CARROT", "WHEAT"]
        else:
            affordable = ["TOMATO", "STRAWBERRY", "CARROT", "WHEAT"]

        best_crop = "CARROT"
        best_score = -9999.0
        for crop in affordable:
            info = CROPS[crop]
            if cash < info["seed"]:
                continue
            price = max(1.0, state.get_price(crop))
            first = max(1, info["first_yield_day"])
            remaining = max(1, 30 - state.day)
            if info.get("ongoing"):
                interval = max(1, info.get("interval", 1))
                yields = max(0, 1 + (remaining - first) // interval) if remaining >= first else 0
                units = min(info["max_yield"], yields)
            else:
                units = info["max_yield"] if remaining >= first else 0
            score = (price * units - info["seed"]) / first
            if score > best_score:
                best_score = score
                best_crop = crop
        return best_crop

    # ═══════════════════════════════════════════════════════════════════
    # X1.11 Helper Methods
    # ═══════════════════════════════════════════════════════════════════

    def _x111_economic_gate_4to8(self, state: GameState) -> bool:
        """Economic Gate for 4 → 8 Cows expansion (Pillar 1).

        Gate conditions:
        - Cash >= $800 post-purchase
        - Internal wheat feed >= 8
        - Milk pipeline operational (milk sold > 0 or day < 12)
        - Remaining horizon >= 10 days
        - Expected milk ROI > crop opportunity cost
        """
        if state.money < 800.0:
            return False
        if state.day < 5 or state.day > 18:
            return False
        wheat_supply = self._x19_inventory_total(state, "WHEAT")
        if wheat_supply < 8:
            return False
        remaining = 29 - state.day
        if remaining < 10:
            return False
        # Gate: milk pipeline must be working (or still warming up)
        milk_sold = getattr(self, '_x111_milk_sold_total', 0)
        if state.day >= 12 and milk_sold == 0:
            return False  # Pipeline broken — don't invest more
        return True

    def _x111_dynamic_wheat_feed_reserve(self, state: GameState) -> int:
        """Dynamic wheat feed reserve = f(cows, remaining_days).

        Keep enough wheat to feed all cows for ~3 days, capped at 30.
        """
        active_cows = len(self._x19_animal_tiles(state))
        remaining_days = max(1, 29 - state.day)
        # 1 wheat per cow per day, keep 3-day buffer
        reserve = min(active_cows * 3, active_cows * remaining_days)
        return min(30, max(4, reserve))

    def _x111_buy_seeds_phased(self, state: GameState, builder: ActionBuilder, cash: float) -> float:
        """Phased seed purchasing (Pillar 3).

        Phase 1 (Day 0-6):  WHEAT + CARROT for fast turnover
        Phase 2 (Day 7-18): MELON + TOMATO + CARROT for high net EV
        Phase 3 (Day 19+):  CARROT + WHEAT for guaranteed harvest
        """
        day = state.day

        # Phase 1: Bootstrap — Fast 2-day crops
        if day <= 6:
            crops_to_buy = [("WHEAT", 12, 120.0), ("CARROT", 12, 240.0)]
        # Phase 2: Growth — High Net EV mix
        elif day <= 18:
            crops_to_buy = [
                ("MELON", 8, 640.0),
                ("TOMATO", 6, 300.0),
                ("CARROT", 12, 240.0),
                ("WHEAT", 8, 80.0),
            ]
        # Phase 3: Endgame Sprint — Fast crops only
        else:
            crops_to_buy = [("CARROT", 12, 240.0), ("WHEAT", 8, 80.0)]

        # Minimum cash floor to protect livestock and operations
        cash_floor = 400.0 if day <= 6 else 600.0

        for crop, qty, cost in crops_to_buy:
            if state.get_seed_count(crop) < qty and cash >= cash_floor + cost:
                builder.buy_seed(crop, qty)
                cash -= cost
                self._x111_seeds_spent += cost
                self.telemetry.spending_seeds += cost
                break  # One purchase per turn to prevent cash crash

        return cash

    def _x111_select_crop_for_tile(self, state: GameState, target: Tuple[int, int], virtual_seeds: Dict[str, int]) -> Optional[str]:
        """Net EV / Tile-Day crop selection (Pillar 3).

        Accounts for:
        - Time-to-cash: 2-day crops (Wheat $25, Carrot $35) vs 10-day (Melon $250)
        - Remaining horizon: Don't plant 10-day crops after Day 18
        - Feed tiles: Always WHEAT on designated feed positions
        """
        day = state.day

        # Dedicated feed tiles — always WHEAT
        feed_tiles = self._x111_feed_tile_positions()
        if target in feed_tiles:
            if virtual_seeds.get("WHEAT", 0) > 0:
                virtual_seeds["WHEAT"] -= 1
                return "WHEAT"
            return None  # Don't plant cash crops on feed tiles

        # Phase 1: Bootstrap (Day 0-6) — Fast turnover
        if day <= 6:
            for crop in ["CARROT", "WHEAT"]:
                if virtual_seeds.get(crop, 0) > 0:
                    virtual_seeds[crop] -= 1
                    return crop
            return None

        # Phase 3: Endgame Sprint (Day 19+) — Only fast crops
        if day >= 19:
            for crop in ["CARROT", "WHEAT"]:
                if virtual_seeds.get(crop, 0) > 0:
                    virtual_seeds[crop] -= 1
                    return crop
            return None

        # Phase 2: Growth (Day 7-18) — Net EV ranked
        # Melon: $250 yield, 10-day, Net EV ~$17/tile-day (only if day <= 18)
        # Tomato: $50 yield * ongoing, 8-day, Net EV ~$5/tile-day
        # Carrot: $35 yield * 4, 2-day, Net EV ~$50/tile-day
        # Wheat: $25 yield * 6, 2-day, Net EV ~$62.5/tile-day (but we grow for feed)
        ranked = []
        remaining = 29 - day
        if remaining >= 10 and day <= 18 and virtual_seeds.get("MELON", 0) > 0:
            ranked.append("MELON")
        if remaining >= 8 and day <= 20 and virtual_seeds.get("TOMATO", 0) > 0:
            ranked.append("TOMATO")
        if virtual_seeds.get("CARROT", 0) > 0:
            ranked.append("CARROT")
        if virtual_seeds.get("WHEAT", 0) > 0:
            ranked.append("WHEAT")

        if ranked:
            crop = ranked[0]
            virtual_seeds[crop] -= 1
            return crop
        return None

    def _x111_feed_tile_positions(self) -> List[Tuple[int, int]]:
        """Tiles reserved for growing wheat feed (dynamically sized)."""
        # 4 tiles in Q0 near shed — enough to sustain ~4 cows
        return [(1, 1), (1, 2), (2, 1), (2, 2)]

    def _x111_pasture_positions(self) -> List[Tuple[int, int]]:
        """Target pasture positions for up to 8 cows spanning Q0-Q1 border."""
        return [
            (3, 3), (3, 4), (4, 3), (4, 4),   # Q0 core pastures (first 4 cows)
            (5, 3), (5, 4), (6, 3), (6, 4),   # Q1 border pastures (cows 5-8)
        ]

    def _x111_get_crop_tiles(self, state: GameState) -> List[Tuple[int, int]]:
        """Get all owned tiles available for crops (excluding pastures and shed)."""
        owned = self._x19_owned_tiles(state)
        pasture_positions = set(self._x111_pasture_positions())
        livestock_tiles = set(self._x19_pasture_tiles(state))
        # Exclude pasture zone AND (4,4) shed
        excluded = pasture_positions | livestock_tiles | {(4, 4)}
        result = [p for p in owned if p not in excluded]
        # Sort by proximity to shed for efficient dropoff
        return sorted(result, key=lambda p: (abs(p[0] - 4) + abs(p[1] - 4), p[1], p[0]))

    def _x111_process_sales(self, state: GameState, builder: ActionBuilder):
        """Market sales: immediate crops, staggered milk, dynamic wheat surplus."""
        if state.day <= 0:
            return

        # Sell all crop products immediately
        for product in ("MELON", "CARROT", "TOMATO", "STRAWBERRY"):
            count = state.get_shed_count(product)
            if count > 0:
                builder.sell(product, count)
                price_map = {"MELON": 250.0, "CARROT": 35.0, "TOMATO": 50.0, "STRAWBERRY": 100.0}
                self._x111_crop_revenue_total += count * price_map.get(product, 0.0)
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + count * price_map.get(product, 0.0)
                self.telemetry.quantities_sold[product] = self.telemetry.quantities_sold.get(product, 0) + count

        # Staggered Milk Sales (preserve market price — max 4/turn)
        milk_in_shed = state.get_shed_count("MILK")
        if milk_in_shed > 0:
            sell_qty = min(4, milk_in_shed)
            builder.sell("MILK", sell_qty)
            self._x111_milk_sold_total += sell_qty
            self._x111_milk_revenue_total += sell_qty * 160.0
            self.telemetry.realized_revenue["MILK"] = self.telemetry.realized_revenue.get("MILK", 0.0) + sell_qty * 160.0
            self.telemetry.quantities_sold["MILK"] = self.telemetry.quantities_sold.get("MILK", 0) + sell_qty

        # Wheat: sell excess above feed reserve (or all on Day 27+)
        feed_reserve = self._x111_dynamic_wheat_feed_reserve(state)
        wheat_in_shed = state.get_shed_count("WHEAT")
        if state.day >= 27:
            excess = wheat_in_shed
        else:
            excess = max(0, wheat_in_shed - feed_reserve)
        if excess > 0:
            builder.sell("WHEAT", excess)
            self._x111_crop_revenue_total += excess * 25.0
            self.telemetry.realized_revenue["WHEAT"] = self.telemetry.realized_revenue.get("WHEAT", 0.0) + excess * 25.0
            self.telemetry.quantities_sold["WHEAT"] = self.telemetry.quantities_sold.get("WHEAT", 0) + excess

    def _x111_worker_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        reserved: Set[Tuple[int, int]],
        crop_tiles: List[Tuple[int, int]],
        pasture_tiles: List[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
    ) -> List[str]:
        """Unified worker task dispatch (Pillar 4).

        Priority hierarchy:
        1. Shed dropoff (carrying milk OR >= 3 items)
        2. Animal placement (COW in inventory or shed)
        3. Pasture building (if < target pastures and day >= 2)
        4. HARVEST FIRST — Milk collection
        5. HARVEST FIRST — Mature crops
        6. Animal feeding (unfed cows)
        7. Emergency watering (consecutive_unwatered >= 1)
        8. Planting (empty tiles)
        9. Watering (unwatered plants)
        10. Weed clearing
        """
        px, py = pos
        products = ["MILK", "WHEAT", "MELON", "CARROT", "TOMATO", "STRAWBERRY"]
        inv_total = sum(state.get_worker_inventory_count(worker_id, item) for item in products)
        milk_in_hand = state.get_worker_inventory_count(worker_id, "MILK")

        # ——— 1. SHED DROPOFF ———
        # Route to shed (4,4) if carrying any milk or inventory >= 3
        if milk_in_hand > 0 or inv_total >= 3:
            if (px, py) == (4, 4):
                for item in products:
                    count = state.get_worker_inventory_count(worker_id, item)
                    if count > 0:
                        return ["DROP", item, count]
            self._x111_movement_steps += 1
            return self._move_towards(px, py, (4, 4))

        # ——— 2. ANIMAL PLACEMENT ———
        cow_in_inv = state.get_worker_inventory_count(worker_id, "COW")
        cow_in_shed = state.get_shed_count("COW")
        if cow_in_shed > 0 and cow_in_inv == 0 and inv_total < 4:
            if (px, py) == (4, 4):
                return ["PICKUP", "COW", 1]
            self._x111_movement_steps += 1
            return self._move_towards(px, py, (4, 4))
        if cow_in_inv > 0:
            empty_pastures = [
                p for p in pasture_tiles
                if p not in reserved
                and isinstance(state.get_tile(p[0], p[1]), dict)
                and state.get_tile(p[0], p[1]).get("kind") == "PASTURE"
                and "animal" not in state.get_tile(p[0], p[1])
            ]
            if empty_pastures:
                target = min(empty_pastures, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                reserved.add(target)
                if (px, py) == target:
                    return ["PLACE", "COW"]
                self._x111_movement_steps += 1
                return self._move_towards(px, py, target)

        # ——— 3. PASTURE BUILDING ———
        target_pasture_count = 4 if state.day < 5 else 8
        current_pasture_count = len(pasture_tiles)
        if current_pasture_count < target_pasture_count and state.day >= 2:
            pasture_targets = self._x111_pasture_positions()
            buildable = [
                p for p in pasture_targets
                if p not in reserved
                and (state.get_tile(p[0], p[1]) is None
                     or (isinstance(state.get_tile(p[0], p[1]), str) and state.get_tile(p[0], p[1]) not in ("LOCKED",)))
            ]
            if buildable:
                target = min(buildable, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                reserved.add(target)
                if (px, py) == target:
                    self._x111_pastures_built += 1
                    return ["BUILD_PASTURE"]
                self._x111_movement_steps += 1
                return self._move_towards(px, py, target)

        # ——— 4. HARVEST FIRST — MILK ———
        animal_tiles = self._x19_animal_tiles(state)
        milk_ready = [
            p for p in animal_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("yield_units", 0) > 0
        ]
        if milk_ready:
            target = min(milk_ready, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            if (px, py) == target:
                self._x111_milk_harvested_count += 1
                self._x111_action_steps += 1
                return ["HARVEST"]
            self._x111_movement_steps += 1
            return self._move_towards(px, py, target)

        # ——— 5. HARVEST FIRST — MATURE CROPS ———
        harvest_ready = []
        for p in crop_tiles:
            if p in reserved:
                continue
            tile = state.get_tile(p[0], p[1])
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue
            if tile.get("yield_units", 0) <= 0:
                continue
            crop_type = tile.get("crop", "WHEAT")
            crop_info = CROPS.get(crop_type, CROPS["WHEAT"])
            planted_day = tile.get("planted_day", 0)
            if (state.day - planted_day) >= crop_info.get("first_yield_day", 2):
                harvest_ready.append(p)
        if harvest_ready:
            target = min(harvest_ready, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            if (px, py) == target:
                self._x111_harvests_count += 1
                self._x111_action_steps += 1
                return ["HARVEST"]
            self._x111_movement_steps += 1
            return self._move_towards(px, py, target)

        # ——— 6. ANIMAL FEEDING ———
        unfed_cows = [
            p for p in animal_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and not state.get_tile(p[0], p[1]).get("fed_today", False)
        ]
        if unfed_cows:
            wheat_in_hand = state.get_worker_inventory_count(worker_id, "WHEAT")
            if wheat_in_hand <= 0:
                if state.get_shed_count("WHEAT") > 0 and inv_total < 4:
                    if (px, py) == (4, 4):
                        return ["PICKUP", "WHEAT", min(8, state.get_shed_count("WHEAT"))]
                    self._x111_movement_steps += 1
                    return self._move_towards(px, py, (4, 4))
            else:
                target = min(unfed_cows, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                reserved.add(target)
                if (px, py) == target:
                    self._x111_wheat_fed_count += 1
                    self._x111_action_steps += 1
                    return ["FEED"]
                self._x111_movement_steps += 1
                return self._move_towards(px, py, target)

        # ——— 7. EMERGENCY WATERING (consecutive_unwatered >= 1) ———
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
            if (px, py) == target:
                self._x111_action_steps += 1
                return ["WATER"]
            self._x111_movement_steps += 1
            return self._move_towards(px, py, target)

        # ——— 8. PLANTING ———
        if state.day < 27:  # Don't plant after day 26 (no time to harvest)
            plantable = [
                p for p in crop_tiles
                if p not in reserved
                and p not in set(pasture_tiles)
                and state.get_tile(p[0], p[1]) is None
            ]
            if plantable:
                target = min(plantable, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                selected_crop = self._x111_select_crop_for_tile(state, target, virtual_seeds)
                if selected_crop:
                    reserved.add(target)
                    if (px, py) == target:
                        self._x111_action_steps += 1
                        return ["PLANT", selected_crop]
                    self._x111_movement_steps += 1
                    return self._move_towards(px, py, target)

        # ——— 9. WATERING ———
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
            if (px, py) == target:
                self._x111_action_steps += 1
                return ["WATER"]
            self._x111_movement_steps += 1
            return self._move_towards(px, py, target)

        # ——— 10. WEED CLEARING ———
        weeds = [
            p for p in crop_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("kind") == "WEED"
        ]
        if weeds:
            target = min(weeds, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
            reserved.add(target)
            if (px, py) == target:
                self._x111_action_steps += 1
                return ["DIG"]
            self._x111_movement_steps += 1
            return self._move_towards(px, py, target)

        return ["PASS"]

    def _x111_track_diagnostics(self, state: GameState, crop_tiles: List[Tuple[int, int]]):
        """Track contribution ladder diagnostic KPIs per step."""
        active_crop_count = 0
        for p in crop_tiles:
            tile = state.get_tile(p[0], p[1])
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                active_crop_count += 1
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, active_crop_count)

    def _x112_pasture_positions(self) -> List[Tuple[int, int]]:
        return [
            (4, 4), (3, 4), (4, 3), (3, 3),
            (5, 4), (5, 3), (6, 4), (6, 3),
            (5, 2), (4, 2), (2, 4),
        ]

    def _x112_opening_action(self, state: GameState) -> Optional[Dict[str, Any]]:
        opening = {
            0: (["PASS"], [], []),
            1: (["BUILD_PASTURE"], [], [["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"], ["BUY_SEED", "MELON", 11], ["BUY_SEED", "STRAWBERRY", 10], ["BUY_SEED", "WHEAT", 9], ["BUY_SEED", "WHEAT", 9]]),
            2: (["WEST"], [["WEST"], ["NORTH"], ["WEST"], ["NORTH"], ["WEST"]], []),
            3: (["BUILD_PASTURE"], [["WEST"], ["NORTH"], ["WEST"], ["BUILD_PASTURE"], ["WEST"]], []),
            4: (["WEST"], [["NORTH"], ["NORTH"], ["WEST"], ["WEST"], ["WEST"]], []),
            5: (["NORTH"], [["PLANT", "WHEAT"], ["PLANT", "WHEAT"], ["WEST"], ["NORTH"], ["BUILD_PASTURE"]], []),
            6: (["PLANT", "WHEAT"], [["WATER"], ["WATER"], ["NORTH"], ["PLANT", "WHEAT"], ["WEST"]], []),
            7: (["WATER"], [["WEST"], ["NORTH"], ["PLANT", "WHEAT"], ["WATER"], ["WEST"]], []),
            8: (["NORTH"], [["WEST"], ["PLANT", "WHEAT"], ["WATER"], ["NORTH"], ["PLANT", "MELON"]], []),
            9: (["PLANT", "MELON"], [["PLANT", "MELON"], ["WATER"], ["WEST"], ["PLANT", "MELON"], ["WATER"]], []),
            10: (["WATER"], [["WATER"], ["NORTH"], ["NORTH"], ["WATER"], ["NORTH"]], []),
            11: (["WEST"], [["NORTH"], ["PLANT", "MELON"], ["PLANT", "STRAWBERRY"], ["WEST"], ["NORTH"]], []),
            12: (["PLANT", "MELON"], [["NORTH"], ["WATER"], ["WATER"], ["PLANT", "MELON"], ["PLANT", "STRAWBERRY"]], []),
            13: (["WATER"], [["PLANT", "STRAWBERRY"], ["WEST"], ["NORTH"], ["WATER"], ["WATER"]], []),
            14: (["NORTH"], [["WATER"], ["PLANT", "MELON"], ["NORTH"], ["NORTH"], ["NORTH"]], []),
            15: (["NORTH"], [["PASS"], ["WATER"], ["PLANT", "STRAWBERRY"], ["PLANT", "STRAWBERRY"], ["NORTH"]], []),
            16: (["PLANT", "STRAWBERRY"], [["PASS"], ["PASS"], ["WATER"], ["WATER"], ["PLANT", "STRAWBERRY"]], []),
            17: (["WATER"], [["PASS"], ["PASS"], ["PASS"], ["PASS"], ["WATER"]], []),
        }
        if state.step not in opening:
            return None
        farmer, hands, market = opening[state.step]
        return {"farmer": farmer, "hands": hands, "market": market}

    def _x112_crop_positions(self, state: GameState) -> List[Tuple[int, int]]:
        owned = self._x19_owned_tiles(state)
        day = state.day + 1
        target_pastures = 4 if day <= 10 else min(11, max(4, self.config.target_cows + self.config.target_sheep))
        excluded = set(self._x112_pasture_positions()[:target_pastures])
        return [
            p for p in owned
            if p not in excluded
            and p[1] < 5
        ]

    def _x112_animal_tiles(self, state: GameState) -> List[Tuple[int, int]]:
        out = []
        for y in range(10):
            for x in range(10):
                tile = state.get_tile(x, y)
                if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and tile.get("animal"):
                    out.append((x, y))
        return out

    def _x112_animal_counts(self, state: GameState) -> Dict[str, int]:
        counts = {"COW": 0, "SHEEP": 0}
        for pos in self._x112_animal_tiles(state):
            tile = state.get_tile(pos[0], pos[1])
            animal = tile.get("animal")
            if animal in counts:
                counts[animal] += 1
        for animal in counts:
            counts[animal] += state.get_shed_count(animal)
            for worker_id in range(1 + len(state.hands_positions)):
                counts[animal] += state.get_worker_inventory_count(worker_id, animal)
        return counts

    def _x112_inventory_total(self, state: GameState, item: str) -> int:
        return state.get_shed_count(item) + sum(
            state.get_worker_inventory_count(worker_id, item)
            for worker_id in range(1 + len(state.hands_positions))
        )

    def _x112_crop_counts(self, state: GameState) -> Dict[str, int]:
        counts = {crop: 0 for crop in CROPS.keys()}
        for y in range(10):
            for x in range(10):
                tile = state.get_tile(x, y)
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    crop = tile.get("crop", "WHEAT")
                    if crop in counts:
                        counts[crop] += 1
        return counts

    def _x112_target_crop_counts(self, state: GameState) -> Dict[str, int]:
        day = state.day + 1
        owned = self._x18_owned_quadrants(state)
        if owned < 2:
            return {"WHEAT": 6, "MELON": 8, "STRAWBERRY": 7, "CARROT": 0, "TOMATO": 0}
        if day <= 17:
            return {"WHEAT": 10, "MELON": 10, "STRAWBERRY": 19, "CARROT": 0, "TOMATO": 0}
        if day <= 20:
            return {"WHEAT": 17, "MELON": 10, "STRAWBERRY": 12, "CARROT": 0, "TOMATO": 0}
        if day <= 24:
            return {"WHEAT": 18, "MELON": max(0, 25 - day), "STRAWBERRY": 12, "CARROT": 0, "TOMATO": 0}
        if day <= 27:
            return {"WHEAT": 18, "MELON": 0, "STRAWBERRY": 12, "CARROT": 0, "TOMATO": 0}
        return {"WHEAT": 8, "MELON": 0, "STRAWBERRY": 0, "CARROT": 0, "TOMATO": 0}

    def _x112_select_crop_for_tile(
        self,
        state: GameState,
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
    ) -> Optional[str]:
        targets = self._x112_target_crop_counts(state)
        order = ["WHEAT", "MELON", "STRAWBERRY"] if self._x18_owned_quadrants(state) < 2 else ["STRAWBERRY", "MELON", "WHEAT"]
        if state.day + 1 >= 21:
            order = ["WHEAT", "STRAWBERRY", "MELON"]
        if state.day + 1 >= 25:
            order = ["WHEAT", "CARROT", "STRAWBERRY"]
        for crop in order:
            if virtual_seeds.get(crop, 0) > 0 and virtual_crop_counts.get(crop, 0) < targets.get(crop, 0):
                virtual_seeds[crop] -= 1
                virtual_crop_counts[crop] = virtual_crop_counts.get(crop, 0) + 1
                return crop
        for crop in ("STRAWBERRY", "MELON", "WHEAT", "CARROT"):
            if virtual_seeds.get(crop, 0) > 0:
                virtual_seeds[crop] -= 1
                virtual_crop_counts[crop] = virtual_crop_counts.get(crop, 0) + 1
                return crop
        return None

    def _x112_desired_hands(self, state: GameState) -> int:
        day = state.day + 1
        owned = self._x18_owned_quadrants(state)
        if day >= 29:
            return 0
        if owned < 2:
            return 5
        if day <= 12:
            return 6
        if day <= 13:
            return 9
        if day <= 18:
            return 10
        if day <= 28:
            return 12 if day in (20, 22, 24) else 11
        return 0

    def _x113_quadrant(self, pos: Tuple[int, int]) -> str:
        x, y = pos
        if x < 5 and y < 5:
            return "Q0"
        if x >= 5 and y < 5:
            return "Q1"
        if x < 5 and y >= 5:
            return "Q2"
        return "Q3"

    def _x113_crop_positions(self, state: GameState) -> List[Tuple[int, int]]:
        if self._x18_owned_quadrants(state) < 3:
            return self._x112_crop_positions(state)
        owned = self._x19_owned_tiles(state)
        day = state.day + 1
        target_pastures = 4 if day <= 10 else min(
            9,
            max(4, len(self._x112_animal_tiles(state)) + state.get_shed_count("COW") + state.get_shed_count("SHEEP") + 1),
        )
        excluded = set(self._x112_pasture_positions()[:target_pastures])
        if self.config.x113_variant in ("D", "E"):
            return [p for p in owned if p not in excluded and p[1] < 10]
        return [p for p in owned if p not in excluded and p[1] < 5]

    def _x113_target_crop_counts(self, state: GameState) -> Dict[str, int]:
        owned = self._x18_owned_quadrants(state)
        day = state.day + 1
        if owned < 3:
            return self._x112_target_crop_counts(state)
        if day <= 22:
            return {"WHEAT": 24, "MELON": 12, "STRAWBERRY": 22, "CARROT": 0, "TOMATO": 0}
        if day <= 27:
            return {"WHEAT": 24, "MELON": 0, "STRAWBERRY": 18, "CARROT": 0, "TOMATO": 0}
        return {"WHEAT": 10, "MELON": 0, "STRAWBERRY": 0, "CARROT": 0, "TOMATO": 0}

    def _x113_select_crop_for_tile(
        self,
        state: GameState,
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
    ) -> Optional[str]:
        targets = self._x113_target_crop_counts(state)
        owned = self._x18_owned_quadrants(state)
        day = state.day + 1
        if owned < 2:
            order = ["WHEAT", "MELON", "STRAWBERRY"]
        elif day <= 20:
            order = ["STRAWBERRY", "WHEAT", "MELON"]
        elif day <= 24:
            order = ["WHEAT", "STRAWBERRY", "MELON"]
        else:
            order = ["WHEAT", "STRAWBERRY", "CARROT"]
        for crop in order:
            if virtual_seeds.get(crop, 0) > 0 and virtual_crop_counts.get(crop, 0) < targets.get(crop, 0):
                virtual_seeds[crop] -= 1
                virtual_crop_counts[crop] = virtual_crop_counts.get(crop, 0) + 1
                return crop
        for crop in ("WHEAT", "STRAWBERRY", "MELON", "CARROT"):
            if virtual_seeds.get(crop, 0) > 0:
                virtual_seeds[crop] -= 1
                virtual_crop_counts[crop] = virtual_crop_counts.get(crop, 0) + 1
                return crop
        return None

    def _x113_backlog_metrics(self, state: GameState, crop_tiles: Optional[List[Tuple[int, int]]] = None) -> Dict[str, Any]:
        crop_tiles = crop_tiles if crop_tiles is not None else self._x113_crop_positions(state)
        crop_counts = self._x112_crop_counts(state)
        crop_targets = self._x113_target_crop_counts(state)
        weeds = 0
        harvested_empty = 0
        unwatered = 0
        harvest_ready = 0
        plant_pending = 0
        active_crops = 0
        productive_by_quadrant = {"Q0": 0, "Q1": 0, "Q2": 0, "Q3": 0}
        owned_by_quadrant = {"Q0": 0, "Q1": 0, "Q2": 0, "Q3": 0}
        for p in crop_tiles:
            quad = self._x113_quadrant(p)
            owned_by_quadrant[quad] += 1
            tile = state.get_tile(p[0], p[1])
            if tile is None:
                plant_pending += 1
                harvested_empty += 1
            elif isinstance(tile, dict) and tile.get("kind") == "WEED":
                weeds += 1
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                active_crops += 1
                productive_by_quadrant[quad] += 1
                if tile.get("yield_units", 0) > 0:
                    harvest_ready += 1
                if not tile.get("watered_today", False):
                    unwatered += 1

        for crop, target in crop_targets.items():
            plant_pending += max(0, target - crop_counts.get(crop, 0) - state.get_seed_count(crop))

        animal_tiles = self._x112_animal_tiles(state)
        feed = 0
        care = 0
        livestock_harvest = 0
        fertilizer = 0
        for p in animal_tiles:
            tile = state.get_tile(p[0], p[1])
            if not isinstance(tile, dict):
                continue
            if not tile.get("fed_today", False):
                feed += 1
            if tile.get("fed_today", False) and not tile.get("cared_today", False):
                care += 1
            if tile.get("yield_units", 0) > 0:
                livestock_harvest += 1
            if tile.get("fertilizer_available", False):
                fertilizer += 1

        total_workers = 1 + len(state.hands_positions)
        logistics = 0
        for worker_id in range(total_workers):
            for item in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO", "WHEAT", "COW", "SHEEP"):
                if state.get_worker_inventory_count(worker_id, item) > 0:
                    logistics += 1
                    break

        crop_backlog = weeds * 2 + harvested_empty + unwatered + harvest_ready
        livestock_backlog = feed * 2 + care + livestock_harvest + fertilizer
        total_backlog = crop_backlog + livestock_backlog + logistics
        return {
            "active_crops": active_crops,
            "pastures": len(self._x19_pasture_tiles(state)),
            "weeds": weeds,
            "harvested_empty": harvested_empty,
            "unwatered": unwatered,
            "harvest_ready": harvest_ready,
            "plant_pending": plant_pending,
            "feed": feed,
            "care": care,
            "livestock_harvest": livestock_harvest,
            "fertilizer": fertilizer,
            "logistics": logistics,
            "crop_backlog": crop_backlog,
            "livestock_backlog": livestock_backlog,
            "total_backlog": total_backlog,
            "backlog_per_worker": total_backlog / max(1, total_workers),
            "crop_backlog_per_worker": crop_backlog / max(1, total_workers),
            "productive_by_quadrant": productive_by_quadrant,
            "owned_by_quadrant": owned_by_quadrant,
        }

    def _x113_desired_hands(self, state: GameState, metrics: Dict[str, Any]) -> int:
        day = state.day + 1
        if day >= 29:
            return 0
        if self.config.x113_variant in ("A", "B"):
            return self._x112_desired_hands(state)
        owned = self._x18_owned_quadrants(state)
        base = 5 if owned < 2 else (7 if owned < 3 else 9)
        backlog_target = math.ceil(metrics["total_backlog"] / 3.0)
        crop_pressure = math.ceil(metrics["crop_backlog"] / 3.0)
        desired = max(base, backlog_target, crop_pressure)
        if day <= 10:
            desired = min(desired, 7)
        elif day <= 20:
            desired = min(desired, self.config.x113_max_hands)
        else:
            desired = min(desired, max(6, self.config.x113_max_hands - 2))
        return max(0, desired)

    def _x113_livestock_gate(self, state: GameState, animal: str, metrics: Dict[str, Any], cash: float) -> bool:
        if self.config.x113_variant == "A":
            return True
        day = state.day + 1
        remaining = 30 - day
        if remaining < (9 if animal == "COW" else 7):
            return False
        total_workers = 1 + len(state.hands_positions)
        if metrics["crop_backlog_per_worker"] > 2.2 or metrics["weeds"] > 3 or metrics["unwatered"] > max(6, total_workers):
            return False
        animal_tiles = len(self._x112_animal_tiles(state))
        wheat_available = self._x112_inventory_total(state, "WHEAT") + self._x112_crop_counts(state).get("WHEAT", 0) * 2
        if wheat_available < max(10, animal_tiles * 3 + 8):
            return False
        cost = self.config.cow_cost if animal == "COW" else self.config.sheep_cost
        product = "MILK" if animal == "COW" else "WOOL"
        expected_cycles = max(0, remaining - (8 if animal == "COW" else 6))
        expected_value = expected_cycles * max(80.0, state.get_price(product))
        operating_drag = (metrics["livestock_backlog"] + metrics["logistics"] + animal_tiles) * 20.0
        reserve = 1200.0 if self._x18_owned_quadrants(state) < 3 else 700.0
        return cash >= cost + reserve and expected_value > cost + operating_drag

    def _x113_should_buy_q2(self, state: GameState, metrics: Dict[str, Any], cash: float) -> bool:
        if self.config.x113_variant not in ("D", "E") or not self.config.x113_q2_enabled:
            return False
        if self._x18_owned_quadrants(state) != 2 or state.hour != 0:
            return False
        remaining = 30 - (state.day + 1)
        if remaining < 9:
            return False
        land_cost = self._next_land_cost(state)
        if land_cost is None:
            return False
        total_workers = 1 + len(state.hands_positions)
        q0q1_capacity = max(1, metrics["owned_by_quadrant"]["Q0"] + metrics["owned_by_quadrant"]["Q1"])
        q0q1_active = metrics["productive_by_quadrant"]["Q0"] + metrics["productive_by_quadrant"]["Q1"]
        utilization = q0q1_active / q0q1_capacity
        expected_tile_days = min(20, total_workers * 2) * max(0, remaining - 4)
        expected_value = expected_tile_days * 55.0
        activation_cost = 900.0
        working_capital = 1800.0
        if utilization < 0.68 or metrics["crop_backlog_per_worker"] > 1.7:
            return False
        if metrics["weeds"] > 2 or metrics["harvested_empty"] > 10:
            return False
        if total_workers < 8:
            return False
        return cash >= land_cost + working_capital + activation_cost and expected_value > land_cost + activation_cost

    def _x113_crop_sla_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        crop_tiles: List[Tuple[int, int]],
        reserved: Set[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
    ) -> List[str]:
        px, py = pos
        for task in ("HARVEST", "WATER", "DIG", "PLANT"):
            candidates = []
            for target in crop_tiles:
                if target in reserved:
                    continue
                tile = state.get_tile(target[0], target[1])
                if task == "PLANT":
                    if state.day + 1 >= 28 or tile is not None:
                        continue
                    crop = self._x113_select_crop_for_tile(state, dict(virtual_seeds), dict(virtual_crop_counts))
                    if crop is None:
                        continue
                elif task == "DIG":
                    if not (isinstance(tile, dict) and tile.get("kind") == "WEED"):
                        continue
                elif not self._tile_matches_task(state, tile, target[0], target[1], state.day, task):
                    continue
                urgency = 0 if task in ("HARVEST", "WATER") else 1
                candidates.append((urgency, abs(px - target[0]) + abs(py - target[1]), target))
            if not candidates:
                continue
            _, _, target = min(candidates, key=lambda item: (item[0], item[1], item[2][1], item[2][0]))
            reserved.add(target)
            if target != (px, py):
                return self._move_towards(px, py, target)
            if task == "PLANT":
                crop = self._x113_select_crop_for_tile(state, virtual_seeds, virtual_crop_counts)
                return ["PLANT", crop] if crop else ["PASS"]
            return [task]
        return ["PASS"]

    def _x113_worker_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        crop_tiles: List[Tuple[int, int]],
        pasture_targets: List[Tuple[int, int]],
        reserved: Set[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
        metrics: Dict[str, Any],
    ) -> List[str]:
        if self.config.x113_variant == "E":
            inventory_load = sum(
                state.get_worker_inventory_count(worker_id, item)
                for item in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO", "WHEAT", "COW", "SHEEP")
            )
            crop_pressure = metrics["crop_backlog_per_worker"] > 1.4 or metrics["weeds"] > 1 or metrics["unwatered"] > 4
            if crop_pressure and inventory_load == 0:
                crop_action = self._x113_crop_sla_action(
                    state, pos, worker_id, crop_tiles, reserved, virtual_seeds, virtual_crop_counts
                )
                if crop_action != ["PASS"]:
                    return crop_action
        return self._x112_worker_action(
            state, pos, worker_id, crop_tiles, pasture_targets, reserved, virtual_seeds, virtual_crop_counts
        )

    def _decide_e12_dynamic_allocation_x113(self, state: GameState) -> Dict[str, Any]:
        if self.config.x113_variant == "A":
            return self._decide_e12_truebelief_engine_x112(state)

        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        builder = ActionBuilder()
        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(self.telemetry.peak_simultaneous_workers, total_workers)
        self.telemetry.worker_hours += total_workers
        self.owned_quadrants = max(self.owned_quadrants, self._x18_owned_quadrants(state))
        self.telemetry.owned_quadrants = self.owned_quadrants

        day = state.day + 1
        cash = state.money
        crop_tiles = self._x113_crop_positions(state)
        metrics = self._x113_backlog_metrics(state, crop_tiles)
        active_crops = metrics["active_crops"]
        animal_counts = self._x112_animal_counts(state)
        animal_tiles = self._x112_animal_tiles(state)
        pasture_count = metrics["pastures"]
        crop_counts = self._x112_crop_counts(state)
        crop_targets = self._x113_target_crop_counts(state)

        if not hasattr(self, "_x113_daily_metrics"):
            self._x113_daily_metrics = []
        if state.hour == 23:
            self._x113_daily_metrics.append({"day": day, **metrics, "cash": cash, "workers": total_workers})

        if not hasattr(self, "_x112_market_revenue"):
            self._x112_market_revenue = {item: 0.0 for item in ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "MILK", "WOOL", "FERTILIZER"]}

        for product in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO"):
            count = state.get_shed_count(product)
            if count > 0:
                builder.sell(product, count)
                revenue = count * state.get_price(product)
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + revenue
                self._x112_market_revenue[product] += revenue

        wheat_reserve = max(8, len(animal_tiles) * 3 + 4)
        wheat_shed = state.get_shed_count("WHEAT")
        wheat_to_sell = wheat_shed if day >= 28 else max(0, wheat_shed - wheat_reserve)
        if wheat_to_sell > 0:
            builder.sell("WHEAT", wheat_to_sell)
            revenue = wheat_to_sell * state.get_price("WHEAT")
            self.telemetry.realized_revenue["WHEAT"] = self.telemetry.realized_revenue.get("WHEAT", 0.0) + revenue
            self._x112_market_revenue["WHEAT"] += revenue

        desired_hands = self._x113_desired_hands(state, metrics)
        hire_reserve = 450.0 if self._x18_owned_quadrants(state) < 3 else 900.0
        if state.hour == 0 and len(hands) < desired_hands and cash >= hire_reserve:
            max_new_hires = 2 if self.config.x113_variant in ("C", "D", "E") else desired_hands - len(hands)
            for _ in range(min(desired_hands - len(hands), max_new_hires)):
                builder.hire()

        if state.step == 0:
            builder.buy_seed("WHEAT", 18)
            builder.buy_seed("MELON", 11)
            builder.buy_seed("STRAWBERRY", 10)
            cash -= 1980.0
        elif day > 1:
            if self.owned_quadrants < 2 and day >= 10 and state.hour == 0 and cash >= 1000.0:
                builder.buy_land()
                self.telemetry.spending_land += 1000.0
                cash -= 1000.0
                self.owned_quadrants = 2
                self.telemetry.owned_quadrants = 2
            elif self._x113_should_buy_q2(state, metrics, cash):
                land_cost = self._next_land_cost(state) or 2000.0
                builder.buy_land()
                self.telemetry.spending_land += land_cost
                cash -= land_cost
                self.owned_quadrants = 3
                self.telemetry.owned_quadrants = 3
                setattr(self.telemetry, "q2_buy_land_day", state.day)

            target_cows = 0
            target_sheep = 0
            if day >= 5:
                target_cows = 1
            if day >= 9:
                target_cows = 2
            if day >= 11 and self.owned_quadrants >= 2:
                target_cows = self.config.x113_livestock_safety_cow_cap
            if day >= 14 and self.owned_quadrants >= 2:
                target_sheep = self.config.x113_livestock_safety_sheep_cap

            crop_guard = metrics["crop_backlog_per_worker"] <= 2.2 and metrics["weeds"] <= 3
            animal_reserve = max(1200.0, 2600.0 if self.owned_quadrants >= 2 and day <= 15 and active_crops < 34 else 500.0)
            if (
                crop_guard
                and pasture_count > 0
                and animal_counts["COW"] < target_cows
                and self._x113_livestock_gate(state, "COW", metrics, cash)
            ):
                qty = min(target_cows - animal_counts["COW"], max(1, int((cash - animal_reserve) // 400.0)), 2)
                if qty > 0:
                    builder.buy_animal("COW", qty)
                    cash -= qty * 400.0
                    self.telemetry.spending_livestock += qty * 400.0

            if (
                crop_guard
                and self.owned_quadrants >= 2
                and pasture_count >= 5
                and active_crops >= 24
                and animal_counts["SHEEP"] < target_sheep
                and self._x113_livestock_gate(state, "SHEEP", metrics, cash)
            ):
                sheep_reserve = 1200.0 if day <= 18 else 600.0
                qty = min(target_sheep - animal_counts["SHEEP"], max(1, int((cash - sheep_reserve) // 500.0)), 2)
                if qty > 0:
                    builder.buy_animal("SHEEP", qty)
                    cash -= qty * 500.0
                    self.telemetry.spending_livestock += qty * 500.0

            wheat_total = self._x112_inventory_total(state, "WHEAT") + crop_counts.get("WHEAT", 0) * 2
            wheat_need = max(10, len(animal_tiles) * 3 + metrics["feed"] * 2 + 8)
            if day >= 8 and wheat_total < wheat_need and cash >= 80.0:
                qty = min(16, max(1, wheat_need - wheat_total), int((cash - 100.0) // max(1.0, state.get_price("WHEAT"))))
                if qty > 0:
                    builder.buy_product("WHEAT", qty)
                    cash -= qty * state.get_price("WHEAT")

            virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
            open_slots = sum(1 for p in crop_tiles if state.get_tile(p[0], p[1]) is None)
            deficits = {
                crop: max(0, crop_targets.get(crop, 0) - crop_counts.get(crop, 0) - virtual_seeds.get(crop, 0))
                for crop in CROPS.keys()
            }
            seed_reserve = 50.0 if self.owned_quadrants < 3 else 800.0
            if day <= 27:
                for crop in ("WHEAT", "MELON", "STRAWBERRY", "CARROT"):
                    if open_slots <= 0:
                        break
                    qty = min(deficits.get(crop, 0), open_slots, 20)
                    cost = CROPS[crop]["seed"] * qty
                    if qty > 0 and cash >= cost + seed_reserve:
                        builder.buy_seed(crop, qty)
                        cash -= cost
                        virtual_seeds[crop] += qty
                        self.telemetry.spending_seeds += cost
                        open_slots -= qty

        pasture_targets = self._x112_pasture_positions()
        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        virtual_crop_counts = self._x112_crop_counts(state)
        reserved: Set[Tuple[int, int]] = set()

        unit_positions = [state.farmer_position] + hands
        unit_actions = [
            self._x113_worker_action(
                state, pos, worker_id, crop_tiles, pasture_targets, reserved, virtual_seeds, virtual_crop_counts, metrics
            )
            for worker_id, pos in enumerate(unit_positions)
        ]
        builder.farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        for act in unit_actions[1:]:
            builder.add_hand_action(act)

        productive_tiles = metrics["active_crops"] + metrics["pastures"]
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, productive_tiles)
        self.telemetry.livestock_counts = animal_counts
        return builder.build()

    def _x114_desired_hands(self, state: GameState, metrics: Dict[str, Any]) -> int:
        if self.config.x114_variant == "A":
            return self._x112_desired_hands(state)
        day = state.day + 1
        if day >= 29:
            return 0

        owned = self._x18_owned_quadrants(state)
        base = 7 if owned < 2 else 9
        if self.config.x114_variant in ("C", "D", "F"):
            base += 1
        if self.config.x114_variant in ("E", "F") and owned < 2 and day >= 8:
            base = min(base, self._x112_desired_hands(state))
        if day >= 13:
            base = max(base, 10)
        if day >= 20:
            base = max(base, 11)
        if day >= 27:
            base = min(base, 8)

        backlog_pressure = math.ceil(
            (
                metrics["weeds"] * 1.5
                + metrics["harvested_empty"]
                + metrics["unwatered"] * 0.5
                + metrics["harvest_ready"] * 0.5
                + metrics["livestock_backlog"] * 0.35
                + metrics["logistics"] * 0.25
            )
            / 3.0
        )
        desired = max(base, 1 + backlog_pressure)
        return max(0, min(self.config.x114_max_hands, desired))

    def _x114_crop_maintenance_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        crop_tiles: List[Tuple[int, int]],
        reserved: Set[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
    ) -> List[str]:
        px, py = pos
        for task in ("HARVEST", "DIG", "PLANT", "WATER"):
            candidates = []
            for target in crop_tiles:
                if target in reserved:
                    continue
                tile = state.get_tile(target[0], target[1])
                if task == "PLANT":
                    if state.day + 1 >= 28 or tile is not None:
                        continue
                    crop = self._x112_select_crop_for_tile(state, dict(virtual_seeds), dict(virtual_crop_counts))
                    if crop is None:
                        continue
                elif task == "DIG":
                    if not (isinstance(tile, dict) and tile.get("kind") == "WEED"):
                        continue
                elif not self._tile_matches_task(state, tile, target[0], target[1], state.day, task):
                    continue
                candidates.append((abs(px - target[0]) + abs(py - target[1]), target))
            if not candidates:
                continue
            _, target = min(candidates, key=lambda item: (item[0], item[1][1], item[1][0]))
            reserved.add(target)
            if target != (px, py):
                return self._move_towards(px, py, target)
            if task == "PLANT":
                crop = self._x112_select_crop_for_tile(state, virtual_seeds, virtual_crop_counts)
                return ["PLANT", crop] if crop else ["PASS"]
            return [task]
        return ["PASS"]

    def _x114_worker_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        crop_tiles: List[Tuple[int, int]],
        pasture_targets: List[Tuple[int, int]],
        reserved: Set[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
        metrics: Dict[str, Any],
    ) -> List[str]:
        if self.config.x114_variant in ("C", "D", "F"):
            inventory_load = sum(
                state.get_worker_inventory_count(worker_id, item)
                for item in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO", "WHEAT", "COW", "SHEEP")
            )
            crop_pressure = (
                metrics["weeds"] > 0
                or metrics["harvested_empty"] > 0
                or metrics["unwatered"] > max(4, 1 + len(state.hands_positions))
                or metrics["harvest_ready"] > max(4, len(state.hands_positions))
            )
            if crop_pressure and inventory_load == 0:
                crop_action = self._x114_crop_maintenance_action(
                    state, pos, crop_tiles, reserved, virtual_seeds, virtual_crop_counts
                )
                if crop_action != ["PASS"]:
                    return crop_action
        return self._x112_worker_action(
            state, pos, worker_id, crop_tiles, pasture_targets, reserved, virtual_seeds, virtual_crop_counts
        )

    def _x114_livestock_brake(self, metrics: Dict[str, Any], workers: int) -> bool:
        if self.config.x114_variant not in ("D", "F"):
            return False
        return (
            metrics["weeds"] > 2
            or metrics["harvested_empty"] > max(5, workers)
            or metrics["unwatered"] > max(8, workers * 2)
            or metrics["crop_backlog_per_worker"] > 2.0
        )

    def _x115_pasture_positions(self) -> List[Tuple[int, int]]:
        return self._x112_pasture_positions() + [
            (0, 5), (1, 5), (2, 5), (3, 5),
        ]

    def _x115_crop_positions(self, state: GameState) -> List[Tuple[int, int]]:
        if self._x18_owned_quadrants(state) < 3:
            return self._x112_crop_positions(state)
        pastures = set(self._x115_pasture_positions())
        return [
            p for p in self._x19_owned_tiles(state)
            if p not in pastures
            and (p[1] < 5 or (p[0] < 5 and p[1] >= 5))
        ]

    def _x115_target_crop_counts(self, state: GameState) -> Dict[str, int]:
        owned = self._x18_owned_quadrants(state)
        day = state.day + 1
        if owned < 3:
            return self._x112_target_crop_counts(state)
        if day <= 17:
            return {"WHEAT": 18, "MELON": 12, "STRAWBERRY": 25, "CARROT": 0, "TOMATO": 0}
        if day <= 22:
            return {"WHEAT": 22, "MELON": 8, "STRAWBERRY": 25, "CARROT": 0, "TOMATO": 0}
        if day <= 27:
            return {"WHEAT": 20, "MELON": 0, "STRAWBERRY": 22, "CARROT": 6, "TOMATO": 0}
        return {"WHEAT": 10, "MELON": 0, "STRAWBERRY": 0, "CARROT": 0, "TOMATO": 0}

    def _x115_select_crop_for_tile(
        self,
        state: GameState,
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
    ) -> Optional[str]:
        targets = self._x115_target_crop_counts(state)
        owned = self._x18_owned_quadrants(state)
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

    def _x115_desired_hands(self, state: GameState, metrics: Dict[str, Any]) -> int:
        day = state.day + 1
        if day >= 29:
            return 0
        owned = self._x18_owned_quadrants(state)
        if owned < 3:
            base = self._x112_desired_hands(state)
            if self.config.x115_variant == "C" and owned == 1 and day <= 9:
                base = min(8, base + 1)
            return min(self.config.x115_max_hands, base)
        if day <= 13:
            base = 10
        elif day <= 24:
            base = 12
        else:
            base = 10
        backlog = math.ceil((metrics["crop_backlog"] + metrics["livestock_backlog"] * 0.5 + metrics["logistics"]) / 4.0)
        return max(0, min(self.config.x115_max_hands, max(base, backlog)))

    def _x115_should_buy_q2(self, state: GameState, metrics: Dict[str, Any], cash: float) -> bool:
        if self.config.x115_variant == "A":
            return False
        if self._x18_owned_quadrants(state) != 2 or state.hour != 0:
            return False
        day = state.day + 1
        if day < 11 or day > 18:
            return False
        land_cost = self._next_land_cost(state)
        if land_cost is None:
            return False
        total_workers = 1 + len(state.hands_positions)
        active_crops = metrics["active_crops"]
        if self.config.x115_variant == "B":
            return cash >= land_cost + 700.0 and total_workers >= 7 and active_crops >= 24 and metrics["weeds"] <= 8
        if self.config.x115_variant == "D":
            return cash >= land_cost + 300.0 and total_workers >= 6 and active_crops >= 14 and metrics["weeds"] <= 12
        return cash >= land_cost + 1200.0 and total_workers >= 8 and active_crops >= 28 and metrics["weeds"] <= 5

    def _x115_crop_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        crop_tiles: List[Tuple[int, int]],
        reserved: Set[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
    ) -> List[str]:
        px, py = pos
        for task in ("HARVEST", "WATER", "DIG", "PLANT"):
            candidates = []
            for target in crop_tiles:
                if target in reserved:
                    continue
                tile = state.get_tile(target[0], target[1])
                if task == "PLANT":
                    if state.day + 1 >= 28 or tile is not None:
                        continue
                    crop = self._x115_select_crop_for_tile(state, dict(virtual_seeds), dict(virtual_crop_counts))
                    if crop is None:
                        continue
                elif task == "DIG":
                    if not (isinstance(tile, dict) and tile.get("kind") == "WEED"):
                        continue
                elif not self._tile_matches_task(state, tile, target[0], target[1], state.day, task):
                    continue
                candidates.append((abs(px - target[0]) + abs(py - target[1]), target))
            if not candidates:
                continue
            _, target = min(candidates, key=lambda item: (item[0], item[1][1], item[1][0]))
            reserved.add(target)
            if target != (px, py):
                return self._move_towards(px, py, target)
            if task == "PLANT":
                crop = self._x115_select_crop_for_tile(state, virtual_seeds, virtual_crop_counts)
                return ["PLANT", crop] if crop else ["PASS"]
            return [task]
        return ["PASS"]

    def _x115_worker_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        crop_tiles: List[Tuple[int, int]],
        pasture_targets: List[Tuple[int, int]],
        reserved: Set[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
        virtual_crop_counts: Dict[str, int],
        metrics: Dict[str, Any],
    ) -> List[str]:
        inventory_load = sum(
            state.get_worker_inventory_count(worker_id, item)
            for item in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO", "WHEAT", "COW", "SHEEP")
        )
        q2_owned = self._x18_owned_quadrants(state) >= 3
        crop_pressure = q2_owned and inventory_load == 0 and (
            metrics["harvested_empty"] > 8
            or metrics["weeds"] > 2
            or metrics["unwatered"] > max(8, len(state.hands_positions))
        )
        if crop_pressure:
            crop_action = self._x115_crop_action(state, pos, crop_tiles, reserved, virtual_seeds, virtual_crop_counts)
            if crop_action != ["PASS"]:
                return crop_action
        return self._x112_worker_action(
            state, pos, worker_id, crop_tiles, pasture_targets, reserved, virtual_seeds, virtual_crop_counts
        )

    def _x115_ag_pasture_positions(self) -> List[Tuple[int, int]]:
        """Pasture coordinates clustered around center crossroads for fast feeding and milking."""
        return [
            # Q0 Core (4 pastures)
            (3, 3), (3, 4), (4, 3), (3, 2),
            # Q1 Extension (6 pastures)
            (5, 3), (5, 2), (6, 3), (6, 2), (7, 3), (7, 2),
            # Q2 Extension (8 pastures)
            (3, 5), (2, 5), (3, 6), (2, 6), (3, 7), (2, 7), (4, 6), (4, 7),
        ]

    def _x115_ag_crop_positions(self, state: GameState) -> List[Tuple[int, int]]:
        """All owned tiles in Q0, Q1, Q2 excluding pasture tiles and shed access."""
        pastures = set(self._x115_ag_pasture_positions())
        shed_tiles = {(4, 4), (5, 4), (4, 5), (5, 5)}
        owned = self._x18_owned_quadrants(state)
        tiles = []
        for p in self._x19_owned_tiles(state):
            if p in pastures or p in shed_tiles:
                continue
            if owned == 1 and (p[0] >= 5 or p[1] >= 5):
                continue
            if owned == 2 and p[1] >= 5:
                continue
            tiles.append(p)
        return tiles

    def _x115_ag_target_crop_counts(self, state: GameState) -> Dict[str, int]:
        owned = self._x18_owned_quadrants(state)
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

    def _x115_ag_desired_hands(self, state: GameState) -> int:
        day = state.day + 1
        if day >= 30 and state.hour >= 20:
            return 8
        owned = self._x18_owned_quadrants(state)
        if day <= 4:
            return 5
        if owned < 2:
            return 6
        if owned == 2:
            return 8 if day < 8 else 10
        # 3 Quadrants owned
        if day <= 12:
            return 10
        return 12

    def _x115_ag_worker_action(
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
        shed_tiles = {(4, 4), (5, 4), (4, 5), (5, 5)}
        products = ["MILK", "WOOL", "FERTILIZER", "WHEAT", "MELON", "STRAWBERRY", "CARROT", "TOMATO"]
        animals = ["COW", "SHEEP"]
        inv_total = sum(state.get_worker_inventory_count(worker_id, item) for item in products + animals)
        animal_in_hand = next((animal for animal in animals if state.get_worker_inventory_count(worker_id, animal) > 0), None)
        animal_tiles = self._x112_animal_tiles(state)
        pasture_tiles = self._x19_pasture_tiles(state)

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

        if animal_in_hand is None and (px, py) in shed_tiles:
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
                    return ["PICKUP", animal, 1] if (px, py) in shed_tiles else self._move_towards(px, py, (4, 4))

        # 4. Build Pasture ON-DEMAND ONLY (when existing pastures < total animals owned)
        total_animals_owned = len(animal_tiles) + sum(state.get_shed_count(a) for a in animals) + sum(state.get_worker_inventory_count(w, a) for w in range(1 + len(state.hands_positions)) for a in animals)
        existing_pastures = len(pasture_tiles)
        if existing_pastures < total_animals_owned and inv_total == 0:
            owned = self._x18_owned_quadrants(state)
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
                    return ["PICKUP", "WHEAT", min(8, state.get_shed_count("WHEAT"))] if (px, py) in shed_tiles else self._move_towards(px, py, (4, 4))
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
        if state.day + 1 <= 26:
            plantable = [
                p for p in crop_tiles
                if p not in reserved
                and state.get_tile(p[0], p[1]) is None
            ]
            if plantable:
                crop = self._x115_select_crop_for_tile(state, dict(virtual_seeds), dict(virtual_crop_counts))
                if crop:
                    target = min(plantable, key=lambda p: abs(px - p[0]) + abs(py - p[1]))
                    reserved.add(target)
                    if target != (px, py):
                        return self._move_towards(px, py, target)
                    actual_crop = self._x115_select_crop_for_tile(state, virtual_seeds, virtual_crop_counts)
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

    def _decide_e12_x115_antigravity_independent(self, state: GameState) -> Dict[str, Any]:
        """Independent Competitive Build X1.15 by Antigravity (Q0->Q1->Q2 75t Livestock-First Architecture)."""
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        builder = ActionBuilder()
        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(self.telemetry.peak_simultaneous_workers, total_workers)
        self.telemetry.worker_hours += total_workers
        self.owned_quadrants = max(self.owned_quadrants, self._x18_owned_quadrants(state))
        self.telemetry.owned_quadrants = self.owned_quadrants

        day = state.day + 1
        cash = state.money
        crop_tiles = self._x115_ag_crop_positions(state)
        pasture_targets = self._x115_ag_pasture_positions()
        animal_counts = self._x112_animal_counts(state)
        animal_tiles = self._x112_animal_tiles(state)
        pasture_count = len(self._x19_pasture_tiles(state))
        crop_counts = self._x112_crop_counts(state)
        crop_targets = self._x115_ag_target_crop_counts(state)

        # 1. Critical Priority: BUY_LAND (must always be first to guarantee execution within 10 market orders limit)
        bought_land_this_turn = False
        if day > 1 and state.hour == 0:
            if self.owned_quadrants < 2 and day >= 5 and cash >= 1000.0:
                builder.buy_land()
                cash -= 1000.0
                self.owned_quadrants = 2
                self.telemetry.owned_quadrants = 2
                self.telemetry.spending_land += 1000.0
                setattr(self.telemetry, "buy_land_day", state.day)
                bought_land_this_turn = True
            elif self.owned_quadrants == 2 and day >= 8 and cash >= 2000.0:
                builder.buy_land()
                cash -= 2000.0
                self.owned_quadrants = 3
                self.telemetry.owned_quadrants = 3
                self.telemetry.spending_land += 2000.0
                setattr(self.telemetry, "q2_buy_land_day", state.day)
                bought_land_this_turn = True

        # 2. Market Sales: Instant sell of all shed goods
        for product in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO"):
            count = state.get_shed_count(product)
            if count > 0 and len(builder.market_orders) < 8:
                builder.sell(product, count)
                revenue = count * state.get_price(product)
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + revenue

        # Wheat selling: keep feed buffer until day 28
        wheat_reserve = max(8, len(animal_tiles) * 3 + 4)
        wheat_shed = state.get_shed_count("WHEAT")
        wheat_to_sell = wheat_shed if day >= 28 else max(0, wheat_shed - wheat_reserve)
        if wheat_to_sell > 0 and len(builder.market_orders) < 8:
            builder.sell("WHEAT", wheat_to_sell)
            revenue = wheat_to_sell * state.get_price("WHEAT")
            self.telemetry.realized_revenue["WHEAT"] = self.telemetry.realized_revenue.get("WHEAT", 0.0) + revenue

        # 3. Workforce Hiring (Hours 0 and 1 to support up to 12 hands within 10 orders/turn limit)
        desired_hands = self._x115_ag_desired_hands(state)
        current_hands = len(hands)
        if state.hour in (0, 1) and current_hands < desired_hands and cash >= 5.0:
            hires_needed = desired_hands - current_hands
            available_slots = max(0, 10 - len(builder.market_orders))
            max_hires = min(hires_needed, available_slots)
            for _ in range(max_hires):
                builder.hire()

        # 4. Market Purchases (Day 0 Turn 1 Opening vs Ongoing)
        if state.step == 0:
            # Universal Day 1 Opening: 5 Hands, 2 Cows ($800), 2 Sheep ($1000), 10 Wheat feed ($250), 10 Wheat seeds ($100), 8 Melon seeds ($640)
            builder.buy_animal("COW", 2)
            builder.buy_animal("SHEEP", 2)
            builder.buy_product("WHEAT", 10)
            builder.buy_seed("WHEAT", 10)
            builder.buy_seed("MELON", 8)
            cash -= (800.0 + 1000.0 + 250.0 + 100.0 + 640.0)
            self.telemetry.spending_livestock += 1800.0
            self.telemetry.spending_seeds += 740.0
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
                target_cows = min(self.config.x115_antigravity_target_cows, 14)
                target_sheep = min(self.config.x115_antigravity_target_sheep, 4)

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
                    self.telemetry.spending_livestock += qty * 400.0

            # Buy Sheep
            sheep_reserve = 150.0 if self.owned_quadrants >= 3 else (500.0 + land_reserve)
            if day <= 22 and pasture_count >= 4 and animal_counts["SHEEP"] < target_sheep and cash >= 500.0 + sheep_reserve and len(builder.market_orders) < 9:
                qty = min(target_sheep - animal_counts["SHEEP"], max(1, int((cash - sheep_reserve) // 500.0)), 2)
                if qty > 0:
                    builder.buy_animal("SHEEP", qty)
                    cash -= qty * 500.0
                    self.telemetry.spending_livestock += qty * 500.0

            # Feed buffer management (Buy Wheat product if buffer is low)
            wheat_total = self._x112_inventory_total(state, "WHEAT") + crop_counts.get("WHEAT", 0) * 2
            wheat_need = max(10, len(animal_tiles) * 3 + 8)
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
            if day <= 26:
                for crop in ("STRAWBERRY", "MELON", "WHEAT", "CARROT"):
                    if open_slots <= 0 or len(builder.market_orders) >= 9:
                        break
                    qty = min(deficits.get(crop, 0), open_slots, 20)
                    cost = CROPS[crop]["seed"] * qty
                    if qty > 0 and cash >= cost + seed_reserve:
                        builder.buy_seed(crop, qty)
                        cash -= cost
                        virtual_seeds[crop] += qty
                        self.telemetry.spending_seeds += cost
                        open_slots -= qty

        # 4. Dispatch Worker Actions
        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        virtual_crop_counts = self._x112_crop_counts(state)
        reserved: Set[Tuple[int, int]] = set()

        unit_positions = [state.farmer_position] + hands
        unit_actions = [
            self._x115_ag_worker_action(
                state, pos, worker_id, crop_tiles, pasture_targets, reserved, virtual_seeds, virtual_crop_counts
            )
            for worker_id, pos in enumerate(unit_positions)
        ]
        builder.farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        for act in unit_actions[1:]:
            builder.add_hand_action(act)

        productive_tiles = self._x19_crop_count(state) + len(self._x19_pasture_tiles(state))
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, productive_tiles)
        self.telemetry.livestock_counts = animal_counts
        return builder.build()

    def _decide_e12_x115_codex_independent(self, state: GameState) -> Dict[str, Any]:
        if self.config.x115_variant == "A":
            return self._decide_e12_truebelief_engine_x112(state)

        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        builder = ActionBuilder()
        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(self.telemetry.peak_simultaneous_workers, total_workers)
        self.telemetry.worker_hours += total_workers
        self.owned_quadrants = max(self.owned_quadrants, self._x18_owned_quadrants(state))
        self.telemetry.owned_quadrants = self.owned_quadrants

        day = state.day + 1
        cash = state.money
        crop_tiles = self._x115_crop_positions(state)
        metrics = self._x113_backlog_metrics(state, crop_tiles)
        active_crops = metrics["active_crops"]
        animal_counts = self._x112_animal_counts(state)
        animal_tiles = self._x112_animal_tiles(state)
        pasture_count = len(self._x19_pasture_tiles(state))
        crop_counts = self._x112_crop_counts(state)
        crop_targets = self._x115_target_crop_counts(state)

        if not hasattr(self, "_x112_market_revenue"):
            self._x112_market_revenue = {item: 0.0 for item in ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "MILK", "WOOL", "FERTILIZER"]}

        for product in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO"):
            count = state.get_shed_count(product)
            if count > 0:
                builder.sell(product, count)
                revenue = count * state.get_price(product)
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + revenue
                self._x112_market_revenue[product] += revenue

        wheat_reserve = max(8, len(animal_tiles) * 3 + 4)
        wheat_shed = state.get_shed_count("WHEAT")
        wheat_to_sell = wheat_shed if day >= 28 else max(0, wheat_shed - wheat_reserve)
        if wheat_to_sell > 0:
            builder.sell("WHEAT", wheat_to_sell)
            revenue = wheat_to_sell * state.get_price("WHEAT")
            self.telemetry.realized_revenue["WHEAT"] = self.telemetry.realized_revenue.get("WHEAT", 0.0) + revenue
            self._x112_market_revenue["WHEAT"] += revenue

        desired_hands = self._x115_desired_hands(state, metrics)
        if state.hour == 0 and len(hands) < desired_hands and cash >= 200.0:
            max_new_hires = desired_hands - len(hands) if self._x18_owned_quadrants(state) < 3 else 3
            for _ in range(min(desired_hands - len(hands), max_new_hires)):
                builder.hire()

        if state.step == 0:
            builder.buy_seed("WHEAT", 18)
            builder.buy_seed("MELON", 11)
            builder.buy_seed("STRAWBERRY", 10)
            cash -= 1980.0
        elif day > 1:
            q1_start_day = 6 if self.config.x115_variant == "D" else 10
            if self.owned_quadrants < 2 and day >= q1_start_day and state.hour == 0 and cash >= 1000.0:
                builder.buy_land()
                cash -= 1000.0
                self.owned_quadrants = 2
                self.telemetry.owned_quadrants = 2
            elif self._x115_should_buy_q2(state, metrics, cash):
                land_cost = self._next_land_cost(state) or 2000.0
                builder.buy_land()
                self.telemetry.spending_land += land_cost
                cash -= land_cost
                self.owned_quadrants = 3
                self.telemetry.owned_quadrants = 3
                setattr(self.telemetry, "q2_buy_land_day", state.day)

            target_cows = 0
            target_sheep = 0
            if day >= 5:
                target_cows = 1
            if day >= 9:
                target_cows = 2
            if day >= 11 and self.owned_quadrants >= 2:
                target_cows = 7
            if day >= 13 and self.owned_quadrants >= 2:
                target_sheep = 4
            if self.owned_quadrants >= 3 and day <= 21:
                target_cows = max(target_cows, 10 if self.config.x115_variant == "B" else 9)
                target_sheep = max(target_sheep, 5 if self.config.x115_variant == "B" else 4)
            if self.config.x115_variant == "D" and self.owned_quadrants < 3 and day <= 18:
                target_cows = min(target_cows, 3)
                target_sheep = 0
            if self.config.x115_variant == "D" and self.owned_quadrants >= 3:
                target_cows = max(target_cows, 12)
                target_sheep = max(target_sheep, 3)
            target_cows = min(target_cows, self.config.target_cows)
            target_sheep = min(target_sheep, self.config.target_sheep)

            crop_engine_reserve = 1800.0 if self.owned_quadrants >= 2 and day <= 15 and active_crops < 35 else 250.0
            if self.owned_quadrants == 2 and day <= 16:
                crop_engine_reserve = max(crop_engine_reserve, 1600.0)
            animal_reserve = max(crop_engine_reserve, 500.0 if self.owned_quadrants < 2 else 250.0)
            if pasture_count > 0 and animal_counts["COW"] < target_cows and cash >= 400.0 + animal_reserve:
                qty = min(target_cows - animal_counts["COW"], max(1, int((cash - animal_reserve) // 400.0)), 3)
                if qty > 0:
                    builder.buy_animal("COW", qty)
                    cash -= qty * 400.0
                    self.telemetry.spending_livestock += qty * 400.0
            if self.owned_quadrants >= 2 and pasture_count >= 6 and active_crops >= 20 and animal_counts["SHEEP"] < target_sheep and cash >= 650.0:
                sheep_reserve = 900.0 if day <= 17 else 250.0
                qty = min(target_sheep - animal_counts["SHEEP"], max(1, int((cash - sheep_reserve) // 500.0)), 3)
                if qty > 0:
                    builder.buy_animal("SHEEP", qty)
                    cash -= qty * 500.0
                    self.telemetry.spending_livestock += qty * 500.0

            wheat_total = self._x112_inventory_total(state, "WHEAT") + crop_counts.get("WHEAT", 0) * 2
            wheat_need = max(10, len(animal_tiles) * 3 + metrics["feed"] * 2 + 8)
            if day >= 8 and wheat_total < wheat_need and cash >= 80.0:
                qty = min(16, max(1, wheat_need - wheat_total), int((cash - 75.0) // max(1.0, state.get_price("WHEAT"))))
                if qty > 0:
                    builder.buy_product("WHEAT", qty)
                    cash -= qty * state.get_price("WHEAT")

            virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
            open_slots = sum(1 for p in crop_tiles if state.get_tile(p[0], p[1]) is None)
            deficits = {
                crop: max(0, crop_targets.get(crop, 0) - crop_counts.get(crop, 0) - virtual_seeds.get(crop, 0))
                for crop in CROPS.keys()
            }
            seed_reserve = 50.0 if self.owned_quadrants < 3 else 350.0
            if day <= 27:
                for crop in ("WHEAT", "MELON", "STRAWBERRY", "CARROT"):
                    if open_slots <= 0:
                        break
                    qty = min(deficits.get(crop, 0), open_slots, 24)
                    cost = CROPS[crop]["seed"] * qty
                    if qty > 0 and cash >= cost + seed_reserve:
                        builder.buy_seed(crop, qty)
                        cash -= cost
                        virtual_seeds[crop] += qty
                        self.telemetry.spending_seeds += cost
                        open_slots -= qty

        pasture_targets = self._x115_pasture_positions()
        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        virtual_crop_counts = self._x112_crop_counts(state)
        reserved: Set[Tuple[int, int]] = set()

        unit_positions = [state.farmer_position] + hands
        unit_actions = [
            self._x115_worker_action(state, pos, worker_id, crop_tiles, pasture_targets, reserved, virtual_seeds, virtual_crop_counts, metrics)
            for worker_id, pos in enumerate(unit_positions)
        ]
        builder.farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        for act in unit_actions[1:]:
            builder.add_hand_action(act)

        productive_tiles = self._x19_crop_count(state) + len(self._x19_pasture_tiles(state))
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, productive_tiles)
        self.telemetry.livestock_counts = animal_counts
        return builder.build()

    def _decide_e12_workforce_capacity_x114(self, state: GameState) -> Dict[str, Any]:
        if self.config.x114_variant == "A":
            return self._decide_e12_truebelief_engine_x112(state)

        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        builder = ActionBuilder()
        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(self.telemetry.peak_simultaneous_workers, total_workers)
        self.telemetry.worker_hours += total_workers
        self.owned_quadrants = max(self.owned_quadrants, self._x18_owned_quadrants(state))
        self.telemetry.owned_quadrants = self.owned_quadrants

        day = state.day + 1
        cash = state.money
        crop_tiles = self._x112_crop_positions(state)
        metrics = self._x113_backlog_metrics(state, crop_tiles)
        active_crops = self._x19_crop_count(state)
        animal_counts = self._x112_animal_counts(state)
        animal_tiles = self._x112_animal_tiles(state)
        pasture_count = len(self._x19_pasture_tiles(state))
        crop_counts = self._x112_crop_counts(state)
        crop_targets = self._x112_target_crop_counts(state)

        if not hasattr(self, "_x112_market_revenue"):
            self._x112_market_revenue = {item: 0.0 for item in ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "MILK", "WOOL", "FERTILIZER"]}

        for product in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO"):
            count = state.get_shed_count(product)
            if count > 0:
                builder.sell(product, count)
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + count * state.get_price(product)
                self._x112_market_revenue[product] += count * state.get_price(product)

        wheat_reserve = max(6, len(animal_tiles) * 2 + 2)
        wheat_shed = state.get_shed_count("WHEAT")
        wheat_to_sell = wheat_shed if day >= 28 else max(0, wheat_shed - wheat_reserve)
        if wheat_to_sell > 0:
            builder.sell("WHEAT", wheat_to_sell)
            self.telemetry.realized_revenue["WHEAT"] = self.telemetry.realized_revenue.get("WHEAT", 0.0) + wheat_to_sell * state.get_price("WHEAT")
            self._x112_market_revenue["WHEAT"] += wheat_to_sell * state.get_price("WHEAT")

        desired_hands = self._x114_desired_hands(state, metrics)
        hire_cash_floor = 100.0
        if self.config.x114_variant in ("E", "F") and self.owned_quadrants < 2 and day >= 8:
            hire_cash_floor = 1200.0
        if state.hour == 0 and len(hands) < desired_hands and cash >= hire_cash_floor:
            for _ in range(desired_hands - len(hands)):
                builder.hire()

        if state.step == 0:
            builder.buy_seed("WHEAT", 18)
            builder.buy_seed("MELON", 11)
            builder.buy_seed("STRAWBERRY", 10)
            cash -= 1980.0
        elif day > 1:
            if self.owned_quadrants < 2 and day >= 10 and state.hour == 0 and cash >= 1000.0:
                builder.buy_land()
                cash -= 1000.0
                self.owned_quadrants = 2
                self.telemetry.owned_quadrants = 2

            target_cows = 0
            target_sheep = 0
            if day >= 5:
                target_cows = 1
            if day >= 9:
                target_cows = 2
            if day >= 11 and self.owned_quadrants >= 2:
                target_cows = 7
            if day >= 12 and self.owned_quadrants >= 2:
                target_cows = 9
                target_sheep = 5
            target_cows = min(target_cows, self.config.target_cows)
            target_sheep = min(target_sheep, self.config.target_sheep)

            livestock_braked = self._x114_livestock_brake(metrics, total_workers)
            crop_engine_reserve = 2600.0 if self.owned_quadrants >= 2 and day <= 15 and active_crops < 35 else 100.0
            animal_reserve = max(crop_engine_reserve, 450.0 if self.owned_quadrants < 2 else 100.0)
            if not livestock_braked and pasture_count > 0 and animal_counts["COW"] < target_cows and cash >= 400.0 + animal_reserve:
                qty = min(target_cows - animal_counts["COW"], max(1, int((cash - animal_reserve) // 400.0)), 5)
                if qty > 0:
                    builder.buy_animal("COW", qty)
                    cash -= qty * 400.0
                    self.telemetry.spending_livestock += qty * 400.0
            if (
                not livestock_braked
                and self.owned_quadrants >= 2
                and pasture_count >= 6
                and active_crops >= 20
                and animal_counts["SHEEP"] < target_sheep
                and cash >= 600.0
            ):
                sheep_reserve = 800.0 if day <= 16 else 100.0
                qty = min(target_sheep - animal_counts["SHEEP"], max(1, int((cash - sheep_reserve) // 500.0)), 5)
                if qty > 0:
                    builder.buy_animal("SHEEP", qty)
                    cash -= qty * 500.0
                    self.telemetry.spending_livestock += qty * 500.0

            wheat_total = self._x112_inventory_total(state, "WHEAT") + crop_counts.get("WHEAT", 0) * 2
            wheat_need = max(8, len(animal_tiles) * 3 + 8)
            if day >= 10 and wheat_total < wheat_need and cash >= 80.0:
                qty = min(14, max(1, wheat_need - wheat_total), int((cash - 50.0) // max(1.0, state.get_price("WHEAT"))))
                if qty > 0:
                    builder.buy_product("WHEAT", qty)
                    cash -= qty * state.get_price("WHEAT")

            virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
            open_slots = sum(1 for p in crop_tiles if state.get_tile(p[0], p[1]) is None)
            deficits = {
                crop: max(0, crop_targets.get(crop, 0) - crop_counts.get(crop, 0) - virtual_seeds.get(crop, 0))
                for crop in CROPS.keys()
            }
            if day <= 27:
                for crop in ("WHEAT", "MELON", "STRAWBERRY", "CARROT"):
                    if open_slots <= 0:
                        break
                    qty = min(deficits.get(crop, 0), open_slots, 20)
                    if qty > 0 and cash >= CROPS[crop]["seed"] * qty + 50.0:
                        builder.buy_seed(crop, qty)
                        cash -= CROPS[crop]["seed"] * qty
                        virtual_seeds[crop] += qty
                        self.telemetry.spending_seeds += CROPS[crop]["seed"] * qty
                        open_slots -= qty

        pasture_targets = self._x112_pasture_positions()
        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        virtual_crop_counts = self._x112_crop_counts(state)
        reserved: Set[Tuple[int, int]] = set()

        unit_positions = [state.farmer_position] + hands
        unit_actions = [
            self._x114_worker_action(
                state, pos, worker_id, crop_tiles, pasture_targets, reserved, virtual_seeds, virtual_crop_counts, metrics
            )
            for worker_id, pos in enumerate(unit_positions)
        ]
        builder.farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        for act in unit_actions[1:]:
            builder.add_hand_action(act)

        productive_tiles = self._x19_crop_count(state) + len(self._x19_pasture_tiles(state))
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, productive_tiles)
        self.telemetry.livestock_counts = animal_counts
        return builder.build()

    def _x112_worker_action(
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
        shed_tiles = {(4, 4), (5, 4), (4, 5), (5, 5)}
        products = ["MILK", "WOOL", "FERTILIZER", "WHEAT", "MELON", "STRAWBERRY", "CARROT", "TOMATO"]
        animals = ["COW", "SHEEP"]
        inv_total = sum(state.get_worker_inventory_count(worker_id, item) for item in products + animals)
        animal_in_hand = next((animal for animal in animals if state.get_worker_inventory_count(worker_id, animal) > 0), None)
        animals_on_tiles = self._x112_animal_tiles(state)
        has_unfed_animals = any(
            isinstance(state.get_tile(p[0], p[1]), dict)
            and not state.get_tile(p[0], p[1]).get("fed_today", False)
            for p in animals_on_tiles
        )

        carried_non_feed = sum(
            state.get_worker_inventory_count(worker_id, item)
            for item in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO")
        )
        carried_wheat = state.get_worker_inventory_count(worker_id, "WHEAT")
        if animal_in_hand is None and (px, py) in shed_tiles:
            for item in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO"):
                count = state.get_worker_inventory_count(worker_id, item)
                if count > 0:
                    return ["PLACE", item, count]
            if carried_wheat > 0 and not has_unfed_animals:
                return ["PLACE", "WHEAT", carried_wheat]

        if animal_in_hand:
            cow_slots = min(self.config.target_cows, len(pasture_targets))
            animal_slots = pasture_targets[:cow_slots] if animal_in_hand == "COW" else pasture_targets[cow_slots:cow_slots + self.config.target_sheep]
            free = [
                p for p in animal_slots
                if p not in reserved
                and isinstance(state.get_tile(p[0], p[1]), dict)
                and state.get_tile(p[0], p[1]).get("kind") == "PASTURE"
                and "animal" not in state.get_tile(p[0], p[1])
            ]
            if free:
                target = min(free, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), pasture_targets.index(p)))
                reserved.add(target)
                return ["PLACE", animal_in_hand] if target == (px, py) else self._move_towards(px, py, target)
            if (px, py) not in shed_tiles:
                return self._move_towards(px, py, (4, 4))

        if carried_non_feed > 0 and (inv_total >= 4 or state.get_worker_inventory_count(worker_id, "WHEAT") == 0 or not has_unfed_animals):
            return self._move_towards(px, py, (4, 4))
        if carried_wheat > 0 and not has_unfed_animals and (inv_total >= 4 or len(animals_on_tiles) == 0):
            return self._move_towards(px, py, (4, 4))

        for animal in animals:
            if state.get_shed_count(animal) > 0:
                cow_slots = min(self.config.target_cows, len(pasture_targets))
                animal_slots = pasture_targets[:cow_slots] if animal == "COW" else pasture_targets[cow_slots:cow_slots + self.config.target_sheep]
                active_animals = {"COW": 0, "SHEEP": 0}
                for animal_pos in self._x112_animal_tiles(state):
                    animal_tile = state.get_tile(animal_pos[0], animal_pos[1])
                    placed_animal = animal_tile.get("animal")
                    if placed_animal in active_animals:
                        active_animals[placed_animal] += 1
                active_crops = self._x19_crop_count(state)
                if animal == "COW":
                    allowed_active = 2 if state.day + 1 <= 11 else (3 if state.day + 1 == 12 else (5 if state.day + 1 == 13 else 7))
                    if active_animals["COW"] >= allowed_active and active_crops < 24:
                        continue
                if animal == "SHEEP":
                    allowed_active = 0 if state.day + 1 <= 13 else (2 if state.day + 1 <= 15 else 4)
                    if active_animals["SHEEP"] >= allowed_active or active_crops < 20:
                        continue
                free_exists = any(
                    isinstance(state.get_tile(p[0], p[1]), dict)
                    and state.get_tile(p[0], p[1]).get("kind") == "PASTURE"
                    and "animal" not in state.get_tile(p[0], p[1])
                    for p in animal_slots
                )
                if free_exists and inv_total == 0:
                    return ["PICKUP", animal, 1] if (px, py) in shed_tiles else self._move_towards(px, py, (4, 4))

        unfed = [
            p for p in animals_on_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and not state.get_tile(p[0], p[1]).get("fed_today", False)
        ]
        if unfed:
            if state.get_worker_inventory_count(worker_id, "WHEAT") <= 0:
                if state.get_shed_count("WHEAT") > 0 and inv_total == 0:
                    return ["PICKUP", "WHEAT", min(6, state.get_shed_count("WHEAT"))] if (px, py) in shed_tiles else self._move_towards(px, py, (4, 4))
            else:
                target = min(unfed, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), pasture_targets.index(p) if p in pasture_targets else 99))
                reserved.add(target)
                return ["FEED"] if target == (px, py) else self._move_towards(px, py, target)

        careable = [
            p for p in animals_on_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("fed_today", False)
            and not state.get_tile(p[0], p[1]).get("cared_today", False)
        ]
        if careable:
            target = min(careable, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), pasture_targets.index(p) if p in pasture_targets else 99))
            reserved.add(target)
            return ["CARE"] if target == (px, py) else self._move_towards(px, py, target)

        ready_animals = [
            p for p in animals_on_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("yield_units", 0) > 0
        ]
        if ready_animals:
            target = min(ready_animals, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), pasture_targets.index(p) if p in pasture_targets else 99))
            reserved.add(target)
            return ["HARVEST"] if target == (px, py) else self._move_towards(px, py, target)

        fert_ready = [
            p for p in animals_on_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("fertilizer_available", False)
        ]
        if False and fert_ready and worker_id != 0:
            target = min(fert_ready, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), pasture_targets.index(p) if p in pasture_targets else 99))
            reserved.add(target)
            return ["COLLECT_FERTILIZER"] if target == (px, py) else self._move_towards(px, py, target)

        careable = [
            p for p in animals_on_tiles
            if p not in reserved
            and isinstance(state.get_tile(p[0], p[1]), dict)
            and state.get_tile(p[0], p[1]).get("fed_today", False)
            and not state.get_tile(p[0], p[1]).get("cared_today", False)
        ]
        if False and careable and worker_id != 0:
            target = min(careable, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), pasture_targets.index(p) if p in pasture_targets else 99))
            reserved.add(target)
            return ["CARE"] if target == (px, py) else self._move_towards(px, py, target)

        missing_pastures = [
            p for p in pasture_targets
            if p not in reserved
            and state.get_tile(p[0], p[1]) is None
            and (self._x18_owned_quadrants(state) >= 2 or p[0] < 5)
        ]
        max_pastures = len(pasture_targets) if self.config.productive_core_mode == "E12_X115_CODEX_INDEPENDENT" else 11
        target_pastures = 4 if state.day + 1 <= 10 else min(max_pastures, max(4, self.config.target_cows + self.config.target_sheep))
        remaining_pastures = target_pastures - len(self._x19_pasture_tiles(state)) - sum(
            1 for p in reserved if p in pasture_targets and state.get_tile(p[0], p[1]) is None
        )
        if missing_pastures and remaining_pastures > 0:
            target = min(missing_pastures, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), pasture_targets.index(p)))
            reserved.add(target)
            return ["BUILD_PASTURE"] if target == (px, py) else self._move_towards(px, py, target)

        for task in ("HARVEST", "WATER", "DIG", "PLANT"):
            candidates = []
            for target in crop_tiles:
                if target in reserved:
                    continue
                tile = state.get_tile(target[0], target[1])
                if task == "PLANT":
                    if state.day + 1 >= 28 or tile is not None:
                        continue
                    crop = self._x112_select_crop_for_tile(state, dict(virtual_seeds), dict(virtual_crop_counts))
                    if crop is None:
                        continue
                elif task == "DIG":
                    if not (isinstance(tile, dict) and tile.get("kind") == "WEED"):
                        continue
                elif not self._tile_matches_task(state, tile, target[0], target[1], state.day, task):
                    continue
                candidates.append((abs(px - target[0]) + abs(py - target[1]), target))
            if not candidates:
                continue
            _, target = min(candidates, key=lambda item: (item[0], item[1][1], item[1][0]))
            reserved.add(target)
            if target != (px, py):
                return self._move_towards(px, py, target)
            if task == "PLANT":
                crop = self._x112_select_crop_for_tile(state, virtual_seeds, virtual_crop_counts)
                return ["PLANT", crop] if crop else ["PASS"]
            return [task]

        if fert_ready and worker_id != 0 and state.day + 1 >= 16:
            target = min(fert_ready, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), pasture_targets.index(p) if p in pasture_targets else 99))
            reserved.add(target)
            return ["COLLECT_FERTILIZER"] if target == (px, py) else self._move_towards(px, py, target)

        if careable and worker_id != 0 and state.day + 1 >= 16:
            target = min(careable, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), pasture_targets.index(p) if p in pasture_targets else 99))
            reserved.add(target)
            return ["CARE"] if target == (px, py) else self._move_towards(px, py, target)

        return ["PASS"]

    def _decide_e12_x115_copilot_independent(self, state: GameState) -> Dict[str, Any]:
        original_cows = self.config.target_cows
        original_sheep = self.config.target_sheep

        day = state.day + 1
        owned = self._x18_owned_quadrants(state)
        active_crops = self._x19_crop_count(state)
        animal_tiles = len(self._x112_animal_tiles(state))
        pasture_count = len(self._x19_pasture_tiles(state))
        cash = state.money

        # Release animal capacity only when the current working set can fund it.
        if day <= 8:
            target_cows, target_sheep = 1, 0
        elif owned < 2 and (active_crops < 12 or cash < 1200.0):
            target_cows, target_sheep = 1, 0
        elif owned < 2:
            target_cows, target_sheep = 2, 0
        elif active_crops < 22 or pasture_count < 6 or cash < 1800.0:
            target_cows, target_sheep = 4, 1
        elif day < 18:
            target_cows, target_sheep = 6, 3
        else:
            target_cows, target_sheep = 7, 4

        # Animal inventory already in the world is part of the capacity test.
        target_cows = max(target_cows, min(7, animal_tiles))
        target_sheep = max(target_sheep, min(4, max(0, animal_tiles - target_cows)))
        self.config.target_cows = target_cows
        self.config.target_sheep = target_sheep
        try:
            return self._decide_e12_truebelief_engine_x112(state)
        finally:
            self.config.target_cows = original_cows
            self.config.target_sheep = original_sheep

    def _decide_e12_truebelief_engine_x112(self, state: GameState) -> Dict[str, Any]:
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        builder = ActionBuilder()
        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(self.telemetry.peak_simultaneous_workers, total_workers)
        self.telemetry.worker_hours += total_workers
        self.owned_quadrants = max(self.owned_quadrants, self._x18_owned_quadrants(state))
        self.telemetry.owned_quadrants = self.owned_quadrants

        day = state.day + 1
        cash = state.money
        active_crops = self._x19_crop_count(state)
        animal_counts = self._x112_animal_counts(state)
        animal_tiles = self._x112_animal_tiles(state)
        pasture_count = len(self._x19_pasture_tiles(state))
        crop_counts = self._x112_crop_counts(state)
        crop_targets = self._x112_target_crop_counts(state)

        if not hasattr(self, "_x112_market_revenue"):
            self._x112_market_revenue = {item: 0.0 for item in ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "MILK", "WOOL", "FERTILIZER"]}

        for product in ("MILK", "WOOL", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT", "TOMATO"):
            count = state.get_shed_count(product)
            if count > 0:
                builder.sell(product, count)
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + count * state.get_price(product)
                self._x112_market_revenue[product] += count * state.get_price(product)

        wheat_reserve = max(6, len(animal_tiles) * 2 + 2)
        wheat_shed = state.get_shed_count("WHEAT")
        wheat_to_sell = wheat_shed if day >= 28 else max(0, wheat_shed - wheat_reserve)
        if wheat_to_sell > 0:
            builder.sell("WHEAT", wheat_to_sell)
            self.telemetry.realized_revenue["WHEAT"] = self.telemetry.realized_revenue.get("WHEAT", 0.0) + wheat_to_sell * state.get_price("WHEAT")
            self._x112_market_revenue["WHEAT"] += wheat_to_sell * state.get_price("WHEAT")

        desired_hands = self._x112_desired_hands(state)
        if state.hour == 0 and len(hands) < desired_hands:
            for _ in range(desired_hands - len(hands)):
                builder.hire()

        if state.step == 0:
            builder.buy_seed("WHEAT", 18)
            builder.buy_seed("MELON", 11)
            builder.buy_seed("STRAWBERRY", 10)
            cash -= 1980.0
        elif day > 1:
            if self.owned_quadrants < 2 and day >= 10 and state.hour == 0 and cash >= 1000.0:
                builder.buy_land()
                cash -= 1000.0
                self.owned_quadrants = 2
                self.telemetry.owned_quadrants = 2

            target_cows = 0
            target_sheep = 0
            if day >= 5:
                target_cows = 1
            if day >= 9:
                target_cows = 2
            if day >= 11 and self.owned_quadrants >= 2:
                target_cows = 7
            if day >= 12 and self.owned_quadrants >= 2:
                target_cows = 9
                target_sheep = 5
            target_cows = min(target_cows, self.config.target_cows)
            target_sheep = min(target_sheep, self.config.target_sheep)

            crop_engine_reserve = 2600.0 if self.owned_quadrants >= 2 and day <= 15 and active_crops < 35 else 100.0
            animal_reserve = max(crop_engine_reserve, 450.0 if self.owned_quadrants < 2 else 100.0)
            if pasture_count > 0 and animal_counts["COW"] < target_cows and cash >= 400.0 + animal_reserve:
                qty = min(target_cows - animal_counts["COW"], max(1, int((cash - animal_reserve) // 400.0)), 5)
                if qty > 0:
                    builder.buy_animal("COW", qty)
                    cash -= qty * 400.0
                    self.telemetry.spending_livestock += qty * 400.0
            if self.owned_quadrants >= 2 and pasture_count >= 6 and active_crops >= 20 and animal_counts["SHEEP"] < target_sheep and cash >= 600.0:
                sheep_reserve = 800.0 if day <= 16 else 100.0
                qty = min(target_sheep - animal_counts["SHEEP"], max(1, int((cash - sheep_reserve) // 500.0)), 5)
                if qty > 0:
                    builder.buy_animal("SHEEP", qty)
                    cash -= qty * 500.0
                    self.telemetry.spending_livestock += qty * 500.0

            wheat_total = self._x112_inventory_total(state, "WHEAT") + crop_counts.get("WHEAT", 0) * 2
            wheat_need = max(8, len(animal_tiles) * 3 + 8)
            if day >= 10 and wheat_total < wheat_need and cash >= 80.0:
                qty = min(14, max(1, wheat_need - wheat_total), int((cash - 50.0) // max(1.0, state.get_price("WHEAT"))))
                if qty > 0:
                    builder.buy_product("WHEAT", qty)
                    cash -= qty * state.get_price("WHEAT")

            virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
            open_slots = sum(1 for p in self._x112_crop_positions(state) if state.get_tile(p[0], p[1]) is None)
            deficits = {
                crop: max(0, crop_targets.get(crop, 0) - crop_counts.get(crop, 0) - virtual_seeds.get(crop, 0))
                for crop in CROPS.keys()
            }
            if day <= 27:
                for crop in ("WHEAT", "MELON", "STRAWBERRY", "CARROT"):
                    if open_slots <= 0:
                        break
                    qty = min(deficits.get(crop, 0), open_slots, 20)
                    if qty > 0 and cash >= CROPS[crop]["seed"] * qty + 50.0:
                        builder.buy_seed(crop, qty)
                        cash -= CROPS[crop]["seed"] * qty
                        virtual_seeds[crop] += qty
                        self.telemetry.spending_seeds += CROPS[crop]["seed"] * qty
                        open_slots -= qty

        pasture_targets = self._x112_pasture_positions()
        crop_tiles = self._x112_crop_positions(state)
        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        virtual_crop_counts = self._x112_crop_counts(state)
        reserved: Set[Tuple[int, int]] = set()

        unit_positions = [state.farmer_position] + hands
        unit_actions = [
            self._x112_worker_action(state, pos, worker_id, crop_tiles, pasture_targets, reserved, virtual_seeds, virtual_crop_counts)
            for worker_id, pos in enumerate(unit_positions)
        ]
        builder.farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        for act in unit_actions[1:]:
            builder.add_hand_action(act)

        productive_tiles = self._x19_crop_count(state) + len(self._x19_pasture_tiles(state))
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, productive_tiles)
        self.telemetry.livestock_counts = animal_counts
        return builder.build()

    def _decide_e12_continuous_surface_x110(self, state: GameState) -> Dict[str, Any]:
        if state.step == 0:
            self.telemetry.starting_money = state.money
            self._x110_stable_days = set()
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        builder = ActionBuilder()
        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(self.telemetry.peak_simultaneous_workers, total_workers)
        self.telemetry.worker_hours += total_workers
        self.owned_quadrants = max(self.owned_quadrants, self._x18_owned_quadrants(state))
        self.telemetry.owned_quadrants = self.owned_quadrants

        cash = state.money
        owned = self._x18_owned_quadrants(state)
        if state.day == 0:
            desired_hands = 4
        elif owned == 1:
            desired_hands = 6
        elif state.day >= 8 and cash >= 800.0:
            desired_hands = 8
        elif state.day <= 10 or cash < 1800.0:
            desired_hands = 6
        else:
            desired_hands = 8
        if state.hour == 0 and state.hires_today < desired_hands:
            for _ in range(desired_hands - state.hires_today):
                builder.hire()

        if state.day == 0 and state.step == 0:
            builder.buy_seed("WHEAT", 24)
        elif state.day > 0:
            required_wheat = self._x110_required_wheat_buffer(state)
            current_wheat = self._x19_inventory_total(state, "WHEAT")
            wheat_plants = sum(
                1 for y in range(10) for x in range(10)
                if isinstance(state.get_tile(x, y), dict)
                and state.get_tile(x, y).get("kind") == "PLANT"
                and state.get_tile(x, y).get("crop") == "WHEAT"
            )
            if current_wheat + wheat_plants * 2 < required_wheat and state.get_seed_count("WHEAT") < 8:
                builder.buy_seed("WHEAT", 12)
            for crop in self._x110_crop_value_rank(state):
                seed_floor = 14 if crop == "CARROT" and state.day <= 8 else 8
                seed_cash_floor = 300.0 if state.day <= 4 else 650.0
                if state.get_seed_count(crop) < seed_floor and cash >= seed_cash_floor:
                    qty = 14 if crop == "CARROT" and state.day <= 8 else 6
                    builder.buy_seed(crop, qty)
                    break
            if current_wheat < max(6, len(self._x19_animal_tiles(state))) and state.get_shed_count("WHEAT") < 6:
                builder.buy_product("WHEAT", 4)

        if state.day >= 1 and owned == 1 and cash >= 1250.0 and self._x19_crop_count(state) >= 18:
            builder.buy_land()
            cash -= 1000.0
        elif state.day >= 1 and owned == 2 and self._x110_cps_stable_for_q2(state):
            land_cost = self._next_land_cost(state)
            if land_cost is not None and cash >= land_cost + 300.0:
                builder.buy_land()
                cash -= land_cost

        pasture_count = len(self._x19_pasture_tiles(state))
        active_animals = len(self._x19_animal_tiles(state))
        pending_cows = state.get_shed_count("COW") + state.get_worker_inventory_count(0, "COW")
        if (
            state.day >= 20
            and (owned >= 3 or state.day >= 27)
            and active_animals + pending_cows < min(8, pasture_count)
            and self._x110_productive_radius_utilization(state) >= 0.90
            and self._x19_inventory_total(state, "WHEAT") >= max(8, active_animals + 4)
            and cash >= self.config.cow_cost + 300.0
        ):
            builder.buy_animal("COW", 1)
            cash -= self.config.cow_cost

        if state.day > 0:
            for product in ("MILK", "MELON", "CARROT", "TOMATO", "STRAWBERRY"):
                count = state.get_shed_count(product)
                if count > 0:
                    builder.sell(product, count)
            if state.day >= 28:
                excess_wheat = state.get_shed_count("WHEAT")
            else:
                excess_wheat = max(0, state.get_shed_count("WHEAT") - self._x110_required_wheat_buffer(state))
            if excess_wheat > 0:
                builder.sell("WHEAT", excess_wheat)

        reserved: Set[Tuple[int, int]] = set(self._x110_livestock_tiles())
        farmer_act = self._x110_livestock_action(state)
        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        target_tiles = self._x19_q0_external_tiles() if state.day == 0 else self._x110_owned_radius_tiles(state)
        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        required_wheat = self._x110_required_wheat_buffer(state)
        wheat_capacity = self._x19_inventory_total(state, "WHEAT")
        wheat_targets_remaining = max(0, math.ceil((required_wheat - wheat_capacity) / 2))
        for idx, hand_pos in enumerate(hands):
            hand_act = ["PASS"]
            if 0 < state.day < 28:
                hand_act = self._x19_hand_livestock_support_action(state, hand_pos, idx + 1, reserved)
            if hand_act == ["PASS"]:
                hand_act, wheat_targets_remaining = self._x110_worker_action(
                    state, hand_pos, idx + 1, target_tiles, virtual_seeds, reserved, wheat_targets_remaining
                )
            builder.add_hand_action(hand_act)

        return builder.build()

    def _x19_pasture_tiles(self, state: GameState) -> List[Tuple[int, int]]:
        out = []
        for y in range(10):
            for x in range(10):
                tile = state.get_tile(x, y)
                if isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                    out.append((x, y))
        return out

    def _x19_animal_tiles(self, state: GameState) -> List[Tuple[int, int]]:
        out = []
        for y in range(10):
            for x in range(10):
                tile = state.get_tile(x, y)
                if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and tile.get("animal") == "COW":
                    out.append((x, y))
        return out

    def _x19_inventory_total(self, state: GameState, item: str) -> int:
        total_workers = 1 + len(state.hands_positions)
        return state.get_shed_count(item) + sum(state.get_worker_inventory_count(w, item) for w in range(total_workers))

    def _x19_crop_count(self, state: GameState) -> int:
        return sum(
            1 for y in range(10) for x in range(10)
            if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "PLANT"
        )

    def _x19_desired_hands(self, state: GameState) -> int:
        owned = self._x18_owned_quadrants(state)
        if state.day == 0:
            return 4
        if owned >= 3:
            return 8
        if owned >= 2:
            return 6
        return 5

    def _x19_select_crop(self, state: GameState, pos: Tuple[int, int], virtual_seeds: Dict[str, int]) -> Optional[str]:
        if state.day <= 6:
            return "WHEAT" if virtual_seeds.get("WHEAT", 0) > 0 else None
        if state.day <= self.config.melon_plant_cutoff_day and virtual_seeds.get("MELON", 0) > 0:
            return "MELON"
        if state.day <= self.config.tomato_plant_cutoff_day and virtual_seeds.get("TOMATO", 0) > 0:
            return "TOMATO"
        if virtual_seeds.get("CARROT", 0) > 0:
            return "CARROT"
        if virtual_seeds.get("WHEAT", 0) > 0:
            return "WHEAT"
        return None

    def _x19_crop_worker_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        working_set: List[Tuple[int, int]],
        virtual_seeds: Dict[str, int],
        reserved: Set[Tuple[int, int]],
    ) -> List[str]:
        px, py = pos
        products = ["MILK", "WHEAT", "MELON", "CARROT", "TOMATO", "STRAWBERRY"]
        inv_total = sum(state.get_worker_inventory_count(worker_id, item) for item in products)
        if inv_total >= 4:
            if (px, py) == (4, 4):
                for item in products:
                    count = state.get_worker_inventory_count(worker_id, item)
                    if count > 0:
                        return ["DROP", item, count]
            return self._move_towards(px, py, (4, 4))

        current = state.get_tile(px, py)
        if (
            (px, py) not in self.livestock_core_tiles
            and isinstance(current, dict)
            and current.get("kind") == "PLANT"
            and not current.get("watered_today", False)
        ):
            reserved.add((px, py))
            return ["WATER"]

        if state.day == 0:
            candidates = []
            for target in working_set:
                if target in reserved or target in self.livestock_core_tiles:
                    continue
                tile = state.get_tile(target[0], target[1])
                if tile is None and virtual_seeds.get("WHEAT", 0) > 0:
                    candidates.append((abs(px - target[0]) + abs(py - target[1]), 0, target))
                elif isinstance(tile, dict) and tile.get("kind") == "PLANT" and not tile.get("watered_today", False):
                    candidates.append((abs(px - target[0]) + abs(py - target[1]), 1, target))
            if candidates:
                _, mode, target = min(candidates, key=lambda item: (item[0], item[1], working_set.index(item[2])))
                reserved.add(target)
                if target != (px, py):
                    return self._move_towards(px, py, target)
                if mode == 0:
                    virtual_seeds["WHEAT"] -= 1
                    return ["PLANT", "WHEAT"]
                return ["WATER"]

        for task in ("DIG", "HARVEST", "WATER", "PLANT"):
            candidates = []
            for target in working_set:
                if target in reserved or target in self.livestock_core_tiles:
                    continue
                tile = state.get_tile(target[0], target[1])
                if task == "PLANT":
                    if tile is not None:
                        continue
                    crop = self._x19_select_crop(state, target, virtual_seeds)
                    if crop is None:
                        continue
                elif task == "DIG":
                    if not (isinstance(tile, dict) and tile.get("kind") == "WEED"):
                        continue
                elif not self._tile_matches_task(state, tile, target[0], target[1], state.day, task):
                    continue
                dist = abs(px - target[0]) + abs(py - target[1])
                candidates.append((dist, self._x19_center_distance(target), target))
            if not candidates:
                continue
            _, _, target = min(candidates, key=lambda item: (item[0], item[1], item[2][1], item[2][0]))
            reserved.add(target)
            if target != (px, py):
                return self._move_towards(px, py, target)
            if task == "PLANT":
                crop = self._x19_select_crop(state, target, virtual_seeds)
                if crop:
                    virtual_seeds[crop] -= 1
                    return ["PLANT", crop]
                return ["PASS"]
            return [task]
        return ["PASS"]

    def _x19_livestock_action(self, state: GameState) -> List[str]:
        fx, fy = state.farmer_position
        animal_tiles = self._x19_animal_tiles(state)
        cow_in_shed = state.get_shed_count("COW")
        cow_in_inv = state.get_worker_inventory_count(0, "COW")

        missing_core = [
            pos for pos in self.livestock_core_tiles
            if not (isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("kind") == "PASTURE")
        ]
        if missing_core and cow_in_inv == 0:
            target = missing_core[0]
            return ["BUILD_PASTURE"] if target == state.farmer_position else self._move_towards(fx, fy, target)

        if state.day == 0:
            return ["PASS"]

        products = ["MILK", "WHEAT"]
        inv_total = sum(state.get_worker_inventory_count(0, item) for item in products)
        if inv_total >= 6:
            if state.farmer_position == (4, 4):
                for item in products:
                    count = state.get_worker_inventory_count(0, item)
                    if count > 0:
                        return ["DROP", item, count]
            return self._move_towards(fx, fy, (4, 4))

        unfed = [
            pos for pos in animal_tiles
            if isinstance(state.get_tile(pos[0], pos[1]), dict)
            and not state.get_tile(pos[0], pos[1]).get("fed_today", False)
        ]
        if unfed:
            if state.get_worker_inventory_count(0, "WHEAT") <= 0:
                if state.get_shed_count("WHEAT") > 0:
                    qty = min(8, state.get_shed_count("WHEAT"))
                    return ["PICKUP", "WHEAT", qty] if state.farmer_position == (4, 4) else self._move_towards(fx, fy, (4, 4))
            else:
                target = min(unfed, key=lambda p: (abs(fx - p[0]) + abs(fy - p[1]), self._x19_center_distance(p)))
                return ["FEED"] if target == state.farmer_position else self._move_towards(fx, fy, target)

        if cow_in_shed > 0 and cow_in_inv == 0:
            return ["PICKUP", "COW", 1] if state.farmer_position == (4, 4) else self._move_towards(fx, fy, (4, 4))

        if cow_in_inv > 0:
            free = [
                pos for pos in self._x19_pasture_tiles(state)
                if isinstance(state.get_tile(pos[0], pos[1]), dict)
                and state.get_tile(pos[0], pos[1]).get("kind") == "PASTURE"
                and "animal" not in state.get_tile(pos[0], pos[1])
            ]
            if free:
                target = min(free, key=lambda p: (self._x19_center_distance(p), abs(fx - p[0]) + abs(fy - p[1])))
                return ["PLACE", "COW"] if target == state.farmer_position else self._move_towards(fx, fy, target)

        milk_ready = [
            pos for pos in animal_tiles
            if isinstance(state.get_tile(pos[0], pos[1]), dict)
            and state.get_tile(pos[0], pos[1]).get("yield_units", 0) > 0
        ]
        if milk_ready:
            target = min(milk_ready, key=lambda p: (abs(fx - p[0]) + abs(fy - p[1]), self._x19_center_distance(p)))
            return ["HARVEST"] if target == state.farmer_position else self._move_towards(fx, fy, target)

        if self._x18_owned_quadrants(state) >= 2 and len(self._x19_pasture_tiles(state)) < 8:
            buildable = [
                pos for pos in self._x19_extra_pasture_tiles()
                if state.get_tile(pos[0], pos[1]) is None
            ]
            if buildable:
                target = min(buildable, key=lambda p: (self._x19_center_distance(p), abs(fx - p[0]) + abs(fy - p[1])))
                return ["BUILD_PASTURE"] if target == state.farmer_position else self._move_towards(fx, fy, target)

        return ["PASS"]

    def _x19_hand_livestock_support_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        reserved: Set[Tuple[int, int]],
    ) -> List[str]:
        if state.day == 0 or len(self._x19_animal_tiles(state)) < 1:
            return ["PASS"]
        px, py = pos
        unfed = [
            animal_pos for animal_pos in self._x19_animal_tiles(state)
            if (animal_pos not in reserved or animal_pos in self.livestock_core_tiles)
            and isinstance(state.get_tile(animal_pos[0], animal_pos[1]), dict)
            and not state.get_tile(animal_pos[0], animal_pos[1]).get("fed_today", False)
        ]
        if not unfed:
            return ["PASS"]
        if state.get_worker_inventory_count(worker_id, "WHEAT") <= 0:
            if state.get_shed_count("WHEAT") <= 0:
                return ["PASS"]
            return ["PICKUP", "WHEAT", min(6, state.get_shed_count("WHEAT"))] if (px, py) == (4, 4) else self._move_towards(px, py, (4, 4))
        target = min(unfed, key=lambda p: (abs(px - p[0]) + abs(py - p[1]), self._x19_center_distance(p)))
        reserved.add(target)
        return ["FEED"] if target == (px, py) else self._move_towards(px, py, target)

    def _decide_e12_growth_first_x19(self, state: GameState) -> Dict[str, Any]:
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        builder = ActionBuilder()
        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(self.telemetry.peak_simultaneous_workers, total_workers)
        self.telemetry.worker_hours += total_workers
        self.owned_quadrants = max(self.owned_quadrants, self._x18_owned_quadrants(state))
        self.telemetry.owned_quadrants = self.owned_quadrants

        cash = state.money
        desired_hands = self._x19_desired_hands(state)
        if state.hour == 0 and state.hires_today < desired_hands and cash > 20.0:
            for _ in range(desired_hands - state.hires_today):
                builder.hire()

        if state.day == 0 and state.step == 0:
            builder.buy_seed("WHEAT", 24 - state.get_seed_count("WHEAT"))
        elif state.day > 0:
            crop_count = self._x19_crop_count(state)
            next_land_cost = self._next_land_cost(state) or 0.0
            land_reserve = next_land_cost + 450.0 if self._x18_owned_quadrants(state) < 3 else 700.0
            if state.get_seed_count("WHEAT") < 10 and self._x19_inventory_total(state, "WHEAT") < 20 and cash >= land_reserve + 200.0:
                builder.buy_seed("WHEAT", 20)
            if state.day <= self.config.melon_plant_cutoff_day and crop_count >= 18 and state.get_seed_count("MELON") < 8 and cash >= land_reserve + 800.0:
                builder.buy_seed("MELON", 8)
            if state.get_seed_count("CARROT") < 8 and cash >= land_reserve + 400.0:
                builder.buy_seed("CARROT", 8)

        if state.day > 0 and len(self._x19_animal_tiles(state)) > 0 and self._x19_inventory_total(state, "WHEAT") < max(12, len(self._x19_animal_tiles(state)) * 3) and cash >= 50.0:
            builder.buy_product("WHEAT", 4)

        if state.day >= 1:
            owned = self._x18_owned_quadrants(state)
            land_cost = self._next_land_cost(state)
            active_crops = self._x19_crop_count(state)
            reserve = 250.0 if owned < 3 else 350.0
            if land_cost is not None and owned < 3 and cash >= land_cost + reserve and active_crops >= 16:
                builder.buy_land()
                cash -= land_cost

        pasture_count = len(self._x19_pasture_tiles(state))
        active_animals = len(self._x19_animal_tiles(state))
        pending_cows = state.get_shed_count("COW") + state.get_worker_inventory_count(0, "COW")
        target_animals = 1 if state.day < 3 else (2 if state.day < 5 else (4 if state.day < 8 else 8))
        next_land_cost = self._next_land_cost(state) or 0.0
        livestock_reserve = next_land_cost + 300.0 if self._x18_owned_quadrants(state) < 3 else 500.0
        if (
            state.day >= 1
            and active_animals + pending_cows < min(target_animals, pasture_count, 8)
            and self._x19_inventory_total(state, "WHEAT") >= max(4, (active_animals + 1) * 2)
            and cash >= self.config.cow_cost + livestock_reserve
        ):
            builder.buy_animal("COW", 1)
            cash -= self.config.cow_cost

        if state.day > 0:
            for product in ("MILK", "MELON", "CARROT", "TOMATO", "STRAWBERRY"):
                count = state.get_shed_count(product)
                if count > 0:
                    builder.sell(product, count)
            excess_wheat = max(0, state.get_shed_count("WHEAT") - max(16, len(self._x19_animal_tiles(state)) * 4))
            if excess_wheat > 0:
                builder.sell("WHEAT", excess_wheat)

        reserved: Set[Tuple[int, int]] = set(self.livestock_core_tiles)
        farmer_act = self._x19_livestock_action(state)
        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        if state.day == 0:
            working_set = self._x19_q0_external_tiles()
        else:
            desired_tiles = 21 + max(0, self._x18_owned_quadrants(state) - 1) * 18
            working_set = self._x19_centered_crop_tiles(state)[:desired_tiles]

        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        for idx, hand_pos in enumerate(hands):
            hand_act = ["PASS"]
            if state.day > 0:
                hand_act = self._x19_hand_livestock_support_action(state, hand_pos, idx + 1, reserved)
            if hand_act == ["PASS"]:
                hand_act = self._x19_crop_worker_action(state, hand_pos, idx + 1, working_set, virtual_seeds, reserved)
            builder.add_hand_action(hand_act)

        return builder.build()

    def _x18_core_pastures(self, state: GameState) -> List[Tuple[int, int]]:
        return [
            pos for pos in self.livestock_core_tiles
            if isinstance(state.get_tile(pos[0], pos[1]), dict)
            and state.get_tile(pos[0], pos[1]).get("kind") == "PASTURE"
        ]

    def _x18_core_cows(self, state: GameState) -> List[Tuple[int, int]]:
        return [
            pos for pos in self.livestock_core_tiles
            if isinstance(state.get_tile(pos[0], pos[1]), dict)
            and state.get_tile(pos[0], pos[1]).get("kind") == "PASTURE"
            and state.get_tile(pos[0], pos[1]).get("animal") == "COW"
        ]

    def _x18_wheat_available(self, state: GameState) -> int:
        total_workers = 1 + len(state.hands_positions)
        return state.get_shed_count("WHEAT") + sum(
            state.get_worker_inventory_count(w, "WHEAT") for w in range(total_workers)
        )

    def _x18_milk_available(self, state: GameState) -> int:
        total_workers = 1 + len(state.hands_positions)
        return state.get_shed_count("MILK") + sum(
            state.get_worker_inventory_count(w, "MILK") for w in range(total_workers)
        )

    def _x18_feed_tiles(self) -> List[Tuple[int, int]]:
        return [(3, 2), (4, 2), (2, 3), (2, 4)]

    def _x18_ring_tiles(self) -> List[Tuple[int, int]]:
        return [
            (2, 2), (3, 2), (4, 2),
            (2, 3), (2, 4),
            (1, 3), (1, 4), (3, 1), (4, 1),
            (1, 2), (2, 1), (1, 1),
            (0, 3), (0, 4), (3, 0), (4, 0),
        ]

    def _x18_owned_quadrants(self, state: GameState) -> int:
        raw_quads = state.my_farm.get("unlocked_quadrants", ["NW"])
        return len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)

    def _x18_crop_workers_target(self, phase: str, active_crops: int, active_cows: int, state: GameState) -> int:
        if phase in ("CORE_BUILDING", "FIRST_COW_BOOTSTRAP"):
            return 0
        if phase == "FEED_STABILIZATION":
            return 1
        if phase == "CROP_BOOTSTRAP":
            return 2
        if phase == "LIVESTOCK_SCALING":
            return 2 if active_cows < 3 else 3
        if phase == "CROP_EXPANSION":
            return min(4, max(2, math.ceil(active_crops / 4)))
        return min(4, max(2, math.ceil(active_crops / 4)))

    def _x18_phase(self, state: GameState) -> str:
        core_pastures = self._x18_core_pastures(state)
        core_cows = self._x18_core_cows(state)
        active_crops = self._x18_active_crops(state)
        working_weeds = self._x18_working_weeds(state, self._x18_ring_tiles())
        wheat_available = self._x18_wheat_available(state)
        milk_available = self._x18_milk_available(state)

        if len(core_pastures) < 4:
            return "CORE_BUILDING"
        if not core_cows:
            return "FIRST_COW_BOOTSTRAP"
        if state.day < 10 or wheat_available < 3:
            return "FEED_STABILIZATION"
        if active_crops < 8:
            return "CROP_BOOTSTRAP"
        if len(core_cows) < 4:
            return "LIVESTOCK_SCALING"
        if self._x18_owned_quadrants(state) < 2 and active_crops >= 16 and not working_weeds and milk_available >= 1:
            return "LAND_EXPANSION"
        return "CROP_EXPANSION"

    def _x18_active_crops(self, state: GameState) -> int:
        return sum(
            1 for y in range(10) for x in range(10)
            if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "PLANT"
        )

    def _x18_working_weeds(self, state: GameState, working_set: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        return [
            pos for pos in working_set
            if isinstance(state.get_tile(pos[0], pos[1]), dict)
            and state.get_tile(pos[0], pos[1]).get("kind") == "WEED"
        ]

    def _x18_select_crop(self, state: GameState, pos: Tuple[int, int], phase: str, virtual_seeds: Dict[str, int]) -> Optional[str]:
        if pos in self._x18_feed_tiles() or phase in ("FEED_STABILIZATION", "CROP_BOOTSTRAP"):
            return "WHEAT" if virtual_seeds.get("WHEAT", 0) > 0 else None
        if state.day <= 18 and virtual_seeds.get("MELON", 0) > 0:
            return "MELON"
        if virtual_seeds.get("CARROT", 0) > 0:
            return "CARROT"
        if virtual_seeds.get("WHEAT", 0) > 0:
            return "WHEAT"
        return None

    def _x18_worker_action(
        self,
        state: GameState,
        pos: Tuple[int, int],
        worker_id: int,
        working_set: List[Tuple[int, int]],
        phase: str,
        virtual_seeds: Dict[str, int],
        reserved: Set[Tuple[int, int]],
        can_plant: bool,
    ) -> List[str]:
        px, py = pos
        products = ["MILK", "WHEAT", "MELON", "CARROT", "TOMATO", "STRAWBERRY"]
        inv_total = sum(state.get_worker_inventory_count(worker_id, item) for item in products)
        if inv_total >= (1 if worker_id == 0 else 4):
            if (px, py) == (4, 4):
                for item in products:
                    count = state.get_worker_inventory_count(worker_id, item)
                    if count > 0:
                        return ["DROP", item, count]
            return self._move_towards(px, py, (4, 4))

        current = state.get_tile(px, py)
        if isinstance(current, dict) and current.get("kind") == "PLANT" and not current.get("watered_today", False) and (px, py) in working_set:
            return ["WATER"]

        tasks = ("WATER", "HARVEST", "DIG", "PLANT")
        for task in tasks:
            if task == "PLANT" and not can_plant:
                continue
            candidates = []
            for target in working_set:
                if target in reserved or target in self.livestock_core_tiles:
                    continue
                tile = state.get_tile(target[0], target[1])
                if task == "PLANT":
                    if tile is not None:
                        continue
                    crop = self._x18_select_crop(state, target, phase, virtual_seeds)
                    if crop is None:
                        continue
                elif not self._tile_matches_task(state, tile, target[0], target[1], state.day, task):
                    continue
                dist = abs(px - target[0]) + abs(py - target[1])
                candidates.append((dist, target))
            if not candidates:
                continue
            candidates.sort(key=lambda item: (item[0], item[1][1], item[1][0]))
            _, target = candidates[0]
            reserved.add(target)
            if target != (px, py):
                return self._move_towards(px, py, target)
            if task == "WATER":
                return ["WATER"]
            if task == "HARVEST":
                return ["HARVEST"]
            if task == "DIG":
                return ["DIG"]
            crop = self._x18_select_crop(state, target, phase, virtual_seeds)
            if crop:
                virtual_seeds[crop] -= 1
                return ["PLANT", crop]
        return ["PASS"]

    def _x18_livestock_action(self, state: GameState) -> List[str]:
        farmer_pos = state.farmer_position
        fx, fy = farmer_pos
        core_pastures = self._x18_core_pastures(state)
        core_cows = self._x18_core_cows(state)
        cow_in_shed = state.get_shed_count("COW")
        cow_in_inv = state.get_worker_inventory_count(0, "COW")

        missing_pastures = [
            pos for pos in self.livestock_core_tiles
            if not (
                isinstance(state.get_tile(pos[0], pos[1]), dict)
                and state.get_tile(pos[0], pos[1]).get("kind") == "PASTURE"
            )
        ]
        if missing_pastures and cow_in_inv == 0:
            target = missing_pastures[0]
            return ["BUILD_PASTURE"] if target == farmer_pos else self._move_towards(fx, fy, target)

        if cow_in_shed > 0 and cow_in_inv == 0:
            return ["PICKUP", "COW", 1] if farmer_pos == (4, 4) else self._move_towards(fx, fy, (4, 4))

        if cow_in_inv > 0:
            free_pastures = [
                pos for pos in self.livestock_core_tiles
                if pos not in core_cows
                and isinstance(state.get_tile(pos[0], pos[1]), dict)
                and state.get_tile(pos[0], pos[1]).get("kind") == "PASTURE"
                and "animal" not in state.get_tile(pos[0], pos[1])
            ]
            if free_pastures:
                target = free_pastures[0]
                return ["PLACE", "COW"] if target == farmer_pos else self._move_towards(fx, fy, target)

        unfed = [
            pos for pos in core_cows
            if isinstance(state.get_tile(pos[0], pos[1]), dict)
            and not state.get_tile(pos[0], pos[1]).get("fed_today", False)
        ]
        if unfed:
            if state.get_worker_inventory_count(0, "WHEAT") <= 0:
                if state.get_shed_count("WHEAT") > 0:
                    return ["PICKUP", "WHEAT", min(6, state.get_shed_count("WHEAT"))] if farmer_pos == (4, 4) else self._move_towards(fx, fy, (4, 4))
            else:
                target = min(unfed, key=lambda p: abs(fx - p[0]) + abs(fy - p[1]))
                return ["FEED"] if target == farmer_pos else self._move_towards(fx, fy, target)

        milk_ready = [
            pos for pos in core_cows
            if isinstance(state.get_tile(pos[0], pos[1]), dict)
            and state.get_tile(pos[0], pos[1]).get("yield_units", 0) > 0
        ]
        if milk_ready:
            target = min(milk_ready, key=lambda p: abs(fx - p[0]) + abs(fy - p[1]))
            return ["HARVEST"] if target == farmer_pos else self._move_towards(fx, fy, target)

        return ["PASS"]

    def _decide_e12_livestock_first_x18(self, state: GameState) -> Dict[str, Any]:
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        builder = ActionBuilder()
        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(self.telemetry.peak_simultaneous_workers, total_workers)
        self.telemetry.worker_hours += total_workers
        self.owned_quadrants = max(self.owned_quadrants, self._x18_owned_quadrants(state))
        self.telemetry.owned_quadrants = self.owned_quadrants

        phase = self._x18_phase(state)
        setattr(self.telemetry, "x18_phase", phase)

        core_cows = self._x18_core_cows(state)
        active_crops = self._x18_active_crops(state)
        wheat_available = self._x18_wheat_available(state)
        milk_available = self._x18_milk_available(state)
        cash = state.money

        if phase not in ("CORE_BUILDING", "FIRST_COW_BOOTSTRAP", "FEED_STABILIZATION"):
            for product in ("MILK", "MELON", "CARROT", "TOMATO", "STRAWBERRY"):
                count = state.get_shed_count(product)
                if count > 0:
                    builder.sell(product, count)
                    cash += count * max(1.0, state.get_price(product))
        elif state.get_shed_count("MILK") > 0:
            builder.sell("MILK", state.get_shed_count("MILK"))

        core_complete = len(self._x18_core_pastures(state)) == 4
        cows_pending = state.get_shed_count("COW") + state.get_worker_inventory_count(0, "COW")

        if core_complete and len(core_cows) + cows_pending < 1 and cash >= 400.0:
            builder.buy_animal("COW", 1)
            cash -= 400.0
            self.telemetry.spending_livestock += 400.0
        elif core_complete and len(core_cows) < 4 and cows_pending == 0 and phase == "LIVESTOCK_SCALING":
            needed_buffer = (len(core_cows) + 1) * 4
            free_pasture = len(self._x18_core_pastures(state)) - len(core_cows)
            previous_productive = milk_available > 0 or any(
                isinstance(state.get_tile(x, y), dict)
                and state.get_tile(x, y).get("animal") == "COW"
                and state.get_tile(x, y).get("placed_day", state.day) <= state.day - 8
                for x, y in core_cows
            )
            if free_pasture > 0 and wheat_available >= needed_buffer and previous_productive and cash >= 700.0:
                builder.buy_animal("COW", 1)
                cash -= 400.0
                self.telemetry.spending_livestock += 400.0

        if phase in ("FIRST_COW_BOOTSTRAP", "FEED_STABILIZATION", "CROP_BOOTSTRAP", "LIVESTOCK_SCALING", "CROP_EXPANSION"):
            if wheat_available < 8 and cash >= 25.0:
                qty = min(8 - wheat_available, int(cash // 25.0))
                if qty > 0:
                    builder.buy_product("WHEAT", qty)
                    cash -= qty * 25.0
            if state.get_seed_count("WHEAT") < 6 and cash >= 60.0:
                builder.buy_seed("WHEAT", 6)
                cash -= 60.0
                self.telemetry.spending_seeds += 60.0
        if phase in ("CROP_BOOTSTRAP", "LIVESTOCK_SCALING", "CROP_EXPANSION") and state.day <= 18:
            if state.get_seed_count("MELON") < 4 and cash >= 320.0:
                builder.buy_seed("MELON", 4)
                cash -= 320.0
                self.telemetry.spending_seeds += 320.0
            if state.get_seed_count("CARROT") < 4 and cash >= 80.0:
                builder.buy_seed("CARROT", 4)
                cash -= 80.0
                self.telemetry.spending_seeds += 80.0

        crop_workers_target = self._x18_crop_workers_target(phase, active_crops, len(core_cows), state)
        if state.hour <= 3 and state.hires_today < crop_workers_target and cash >= 1.0:
            for _ in range(crop_workers_target - state.hires_today):
                builder.hire()

        if phase == "LAND_EXPANSION":
            land_cost = self._next_land_cost(state)
            working_weeds = self._x18_working_weeds(state, self._x18_ring_tiles())
            if land_cost is not None and state.hour == 0 and cash >= land_cost + 1000.0 and not working_weeds:
                builder.buy_land()
                self.telemetry.spending_land += land_cost

        reserved: Set[Tuple[int, int]] = set(self.livestock_core_tiles)
        farmer_act = self._x18_livestock_action(state)
        if farmer_act == ["PASS"] and phase in ("CROP_BOOTSTRAP", "LIVESTOCK_SCALING", "CROP_EXPANSION", "LAND_EXPANSION"):
            virtual = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
            farmer_act = self._x18_worker_action(
                state, state.farmer_position, 0, self._x18_feed_tiles(), phase, virtual, reserved, can_plant=False
            )
        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        crop_workers_current = len(hands)
        capacity = 4 * crop_workers_current
        base_working = self._x18_feed_tiles() if phase == "FEED_STABILIZATION" else self._x18_ring_tiles()
        working_limit = max(4, capacity)
        if phase in ("CORE_BUILDING", "FIRST_COW_BOOTSTRAP"):
            working_limit = 0
        elif phase == "CROP_BOOTSTRAP":
            working_limit = min(8, working_limit)
        elif phase == "LIVESTOCK_SCALING":
            working_limit = min(12, working_limit)
        else:
            working_limit = min(16, working_limit)
        working_set = [pos for pos in base_working if pos not in self.livestock_core_tiles][:working_limit]

        virtual_seeds = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        virtual_active_crops = self._x18_active_crops(state)
        for idx, hand_pos in enumerate(hands):
            can_plant = virtual_active_crops < capacity
            hand_act = self._x18_worker_action(
                state, hand_pos, idx + 1, working_set, phase, virtual_seeds, reserved, can_plant=can_plant
            )
            if hand_act and hand_act[0] == "PLANT":
                virtual_active_crops += 1
            builder.add_hand_action(hand_act)

        return builder.build()

    def _decide_e12_hybrid_staged_locality(self, state: GameState) -> Dict[str, Any]:
        """
        E12-X1.4 — Worker Locality & Readiness-Gated Expansion Strategy.
        Preserves E12-X1.2 validated livestock opening (Cow #1 + Feed Ring + WHEAT buffer),
        implements strict regional worker locality pinning to eliminate travel overhead,
        gates land expansion via 5-factor EXPANSION_READY policy, and maintains $300 operating reserve.
        """
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        raw_quads = state.my_farm.get("unlocked_quadrants", [0])
        owned_quadrants = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        self.owned_quadrants = max(self.owned_quadrants, owned_quadrants)
        self.telemetry.owned_quadrants = self.owned_quadrants

        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(state)

        builder = ActionBuilder()
        cash = state.money
        cows_in_shed = state.get_shed_count("COW")
        cows_in_inv = sum(state.get_worker_inventory_count(w, "COW") for w in range(total_workers))
        active_cows = sum(1 for y in range(10) for x in range(10) if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "PASTURE" and state.get_tile(x, y).get("animal") == "COW")
        cows_owned = cows_in_shed + cows_in_inv + active_cows
        active_pasture_tiles = [t for t in self.q0_tiles if isinstance(state.get_tile(t[0], t[1]), dict) and state.get_tile(t[0], t[1]).get("kind") == "PASTURE"]
        shed_access_tile = (4, 4)

        # 1. Market Sales: Send top 1 highest value product sale order per turn
        sell_candidates = []
        for product in ["MELON", "WOOL", "MILK", "STRAWBERRY", "TOMATO", "CARROT", "WHEAT"]:
            shed_count = state.get_shed_count(product)
            if product == "WHEAT":
                shed_count = max(0, shed_count - 10)
            if shed_count > 0:
                price = state.market_prices.get(product, 0.0)
                unit_price = price if price > 0 else (160.0 if product == "MILK" else CROPS.get(product, {}).get("seed", 10) * 1.75)
                revenue = shed_count * unit_price
                sell_candidates.append((revenue, product, shed_count, unit_price))

        if sell_candidates:
            sell_candidates.sort(key=lambda x: x[0], reverse=True)
            for item in sell_candidates[:2]:
                best_rev, best_product, best_qty, best_unit_price = item
                builder.sell(best_product, best_qty)
                self.telemetry.realized_revenue[best_product] = self.telemetry.realized_revenue.get(best_product, 0.0) + best_rev

        # 2. Placed Cow & Pasture Discovery
        placed_cow_tiles: List[Tuple[int, int]] = []
        livestock_core_reserved = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for (px, py) in self.q0_tiles:
            t = state.get_tile(px, py)
            if isinstance(t, dict) and t.get("kind") == "PASTURE" and t.get("animal") == "COW":
                placed_cow_tiles.append((px, py))

        # 3. Cow #1 Acquisition Trigger
        if cows_owned == 0:
            if cash >= 400.0:
                builder.buy_animal("COW", 1)
                self.telemetry.spending_livestock += 400.0
                self.telemetry.cows_acquired += 1
                cows_owned += 1
                cash -= 400.0
                if getattr(self.telemetry, "turn_first_cow", None) is None:
                    setattr(self.telemetry, "turn_first_cow", state.step + 1)
                self.telemetry.log_event("BUY_COW", state.step, state.day, state.hour, state.money, f"Purchased Cow #{cows_owned}")

        # 4. Readiness-Gated Land Expansion Triggers (Q1, Q2, Q3)
        if self.config.enable_land_expansion and self.owned_quadrants < 2:
            if self._is_expansion_ready(state, 2, cash):
                if not any(isinstance(cmd, list) and cmd[0] == "BUY_LAND" for cmd in builder.market_orders):
                    builder.market_orders.append(["BUY_LAND"])
                self.telemetry.spending_land += 1000.0
                self.telemetry.owned_quadrants = 2
                self.owned_quadrants = 2
                self.telemetry.buy_land_executed_step = state.step
                setattr(self.telemetry, "buy_land_day", state.day)
                self.telemetry.log_event("QUADRANT_UNLOCK", state.step, state.day, state.hour, state.money, "Unlocked Q1 (50t) via EXPANSION_READY")
                cash -= 1000.0

        if self.config.enable_land_expansion and self.owned_quadrants == 2:
            if self._is_expansion_ready(state, 3, cash):
                if not any(isinstance(cmd, list) and cmd[0] == "BUY_LAND" for cmd in builder.market_orders):
                    builder.market_orders.append(["BUY_LAND"])
                self.telemetry.spending_land += 1000.0
                self.telemetry.owned_quadrants = 3
                self.owned_quadrants = 3
                setattr(self.telemetry, "q2_buy_land_day", state.day)
                self.telemetry.log_event("QUADRANT_UNLOCK", state.step, state.day, state.hour, state.money, "Unlocked Q2 (75t) via EXPANSION_READY")
                cash -= 1000.0

        if self.config.enable_land_expansion and self.owned_quadrants == 3:
            if self._is_expansion_ready(state, 4, cash):
                if not any(isinstance(cmd, list) and cmd[0] == "BUY_LAND" for cmd in builder.market_orders):
                    builder.market_orders.append(["BUY_LAND"])
                self.telemetry.spending_land += 1000.0
                self.telemetry.owned_quadrants = 4
                self.owned_quadrants = 4
                self.telemetry.log_event("QUADRANT_UNLOCK", state.step, state.day, state.hour, state.money, "Unlocked Q3 (100t) via EXPANSION_READY")
                cash -= 1000.0

        # 5. Workforce Scaling ($300 operating reserve)
        operating_reserve = 300.0 if state.day >= 3 else 50.0
        cash = self._hire_workers_if_needed(state, builder, cash, operating_reserve)

        # 6. Seed Purchasing Logic ($300 operating reserve)
        self._buy_seeds_if_needed(state, builder, cash, operating_reserve, operating_reserve)

        # 7. Regional Worker Locality Dispatching (Farmer + Hands)
        farmer_pos = state.farmer_position
        farmer_act = None

        if cows_in_shed > 0:
            dist_to_shed = abs(farmer_pos[0] - shed_access_tile[0]) + abs(farmer_pos[1] - shed_access_tile[1])
            if dist_to_shed == 0:
                farmer_act = ["PICKUP", "COW", 1]
            else:
                farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], shed_access_tile)

        elif cows_in_inv > 0:
            pasture_core_tiles = [(3, 3), (3, 4), (4, 3), (4, 4)]
            unoccupied_pasture_tiles = [p for p in pasture_core_tiles if p not in placed_cow_tiles]
            target_pasture = unoccupied_pasture_tiles[0] if unoccupied_pasture_tiles else (3, 3)
            tile_state = state.get_tile(target_pasture[0], target_pasture[1])
            dist = abs(farmer_pos[0] - target_pasture[0]) + abs(farmer_pos[1] - target_pasture[1])

            if tile_state is None or (isinstance(tile_state, dict) and tile_state.get("kind") != "PASTURE"):
                if dist == 0:
                    farmer_act = ["BUILD_PASTURE"]
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], target_pasture)
            else:
                if dist == 0:
                    farmer_act = ["PLACE", "COW"]
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], target_pasture)

        if farmer_act is None and placed_cow_tiles:
            unfed_cow_tiles = [pos for pos in placed_cow_tiles if isinstance(state.get_tile(pos[0], pos[1]), dict) and not state.get_tile(pos[0], pos[1]).get("fed_today", False)]
            if unfed_cow_tiles:
                farmer_wheat = state.get_worker_inventory_count(0, "WHEAT")
                if farmer_wheat > 0:
                    best_tile = min(unfed_cow_tiles, key=lambda p: abs(farmer_pos[0] - p[0]) + abs(farmer_pos[1] - p[1]))
                    dist = abs(farmer_pos[0] - best_tile[0]) + abs(farmer_pos[1] - best_tile[1])
                    if dist == 0:
                        farmer_act = ["FEED"]
                        setattr(self.telemetry, "feed_consumed", getattr(self.telemetry, "feed_consumed", 0) + 1)
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], best_tile)
                elif state.get_shed_count("WHEAT") > 0:
                    dist = abs(farmer_pos[0] - shed_access_tile[0]) + abs(farmer_pos[1] - shed_access_tile[1])
                    if dist == 0:
                        farmer_act = ["PICKUP", "WHEAT", min(5, state.get_shed_count("WHEAT"))]
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], shed_access_tile)

        if farmer_act is None and placed_cow_tiles:
            milk_ready_tiles = [pos for pos in placed_cow_tiles if isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("yield_units", 0) > 0]
            if milk_ready_tiles:
                best_tile = min(milk_ready_tiles, key=lambda p: abs(farmer_pos[0] - p[0]) + abs(farmer_pos[1] - p[1]))
                dist = abs(farmer_pos[0] - best_tile[0]) + abs(farmer_pos[1] - best_tile[1])
                if dist == 0:
                    farmer_act = ["HARVEST"]
                    setattr(self.telemetry, "milk_harvested", getattr(self.telemetry, "milk_harvested", 0) + 1)
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], best_tile)

        # Pre-build core pasture tiles [(3,3), (3,4), (4,3), (4,4)]
        pasture_core_tiles = [(3, 3), (3, 4), (4, 3), (4, 4)]
        unbuilt_core_tiles = [p for p in pasture_core_tiles if not (isinstance(state.get_tile(p[0], p[1]), dict) and state.get_tile(p[0], p[1]).get("kind") == "PASTURE")]
        if farmer_act is None and unbuilt_core_tiles and cows_in_inv == 0 and cows_in_shed == 0:
            target_pasture = unbuilt_core_tiles[0]
            dist = abs(farmer_pos[0] - target_pasture[0]) + abs(farmer_pos[1] - target_pasture[1])
            if dist == 0:
                farmer_act = ["BUILD_PASTURE"]
            else:
                farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], target_pasture)

        reserved_tiles: Set[Tuple[int, int]] = set(livestock_core_reserved)
        q0_hybrid_crop_tiles = [t for t in self.q0_crop_tiles if t not in livestock_core_reserved]
        virtual_seeds: Dict[str, int] = {crop: state.get_seed_count(crop) for crop in CROPS.keys()}
        q0_east_farmer_tiles = [(3, 2), (4, 2)]

        core_pasture_count = sum(1 for p in pasture_core_tiles if isinstance(state.get_tile(p[0], p[1]), dict) and state.get_tile(p[0], p[1]).get("kind") == "PASTURE")
        livestock_core_operational = (core_pasture_count >= 1 and len(placed_cow_tiles) >= 1)

        if farmer_act is None:
            farmer_act = self._get_worker_action_hybrid(
                state, farmer_pos, reserved_tiles, worker_id=0,
                preferred_quadrant=0, q0_tiles=q0_east_farmer_tiles, virtual_seeds=virtual_seeds,
                allow_plant=livestock_core_operational
            )

        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        # 4-Tile Compact 2x2 Worker Grids for working_set_capacity = 4 * active_workers
        q0_clusters = [
            [(1, 1), (1, 2), (2, 1), (2, 2)],  # Hand 1: Q0 NW 2x2 (4 tiles)
            [(1, 3), (1, 4), (2, 3), (2, 4)],  # Hand 2: Q0 SW 2x2 (4 tiles)
        ]
        q1_clusters = [
            [(5, 3), (5, 4), (6, 3), (6, 4)],  # Hand 3: Q1 SW 2x2 (4 tiles)
            [(5, 1), (5, 2), (6, 1), (6, 2)],  # Hand 4: Q1 NW 2x2 (4 tiles)
            [(7, 1), (7, 2), (8, 1), (8, 2)],  # Hand 5: Q1 NE 2x2 (4 tiles)
        ]

        for idx, hand_pos in enumerate(hands):
            worker_id = idx + 1
            if idx == 0:
                cluster_tiles = q0_clusters[0]
                pref_q = 0
            elif idx == 1:
                cluster_tiles = q0_clusters[1]
                pref_q = 0
            elif idx == 2 and self.owned_quadrants >= 2:
                cluster_tiles = q1_clusters[0]
                pref_q = 1
            elif idx == 3 and self.owned_quadrants >= 2:
                cluster_tiles = q1_clusters[1]
                pref_q = 1
            elif idx == 4 and self.owned_quadrants >= 2:
                cluster_tiles = q1_clusters[2]
                pref_q = 1
            else:
                cluster_tiles = q0_clusters[idx % len(q0_clusters)]
                pref_q = 0

            h_act = self._get_worker_action_hybrid(
                state, hand_pos, reserved_tiles, worker_id=worker_id,
                preferred_quadrant=pref_q,
                q0_tiles=cluster_tiles, virtual_seeds=virtual_seeds,
                allow_plant=livestock_core_operational
            )
            builder.add_hand_action(h_act)

        self._record_action_budget(state, farmer_act)

        return builder.build()

    def _process_sales(self, state: GameState, builder: ActionBuilder):
        orders_placed = 0
        max_orders = 10

        if not hasattr(self.telemetry, "quantities_sold"):
            self.telemetry.quantities_sold = {"MILK": 0, "WOOL": 0, "MELON": 0, "CARROT": 0, "WHEAT": 0, "EGG": 0}
        if not hasattr(self.telemetry, "realized_revenue"):
            self.telemetry.realized_revenue = {"MILK": 0.0, "WOOL": 0.0, "MELON": 0.0, "CARROT": 0.0, "WHEAT": 0.0, "EGG": 0.0}

        milk_cnt = state.get_shed_count("MILK")
        if milk_cnt > 0 and orders_placed < max_orders:
            builder.sell("MILK", milk_cnt)
            orders_placed += 1
            self.telemetry.quantities_sold["MILK"] = self.telemetry.quantities_sold.get("MILK", 0) + milk_cnt
            self.telemetry.realized_revenue["MILK"] = self.telemetry.realized_revenue.get("MILK", 0.0) + milk_cnt * 160.0

        wool_cnt = state.get_shed_count("WOOL")
        if wool_cnt > 0 and orders_placed < max_orders:
            builder.sell("WOOL", wool_cnt)
            orders_placed += 1
            self.telemetry.quantities_sold["WOOL"] = self.telemetry.quantities_sold.get("WOOL", 0) + wool_cnt
            self.telemetry.realized_revenue["WOOL"] = self.telemetry.realized_revenue.get("WOOL", 0.0) + wool_cnt * 200.0

        melon_cnt = state.get_shed_count("MELON")
        if melon_cnt > 0 and orders_placed < max_orders:
            builder.sell("MELON", melon_cnt)
            orders_placed += 1
            self.telemetry.quantities_sold["MELON"] = self.telemetry.quantities_sold.get("MELON", 0) + melon_cnt
            self.telemetry.realized_revenue["MELON"] = self.telemetry.realized_revenue.get("MELON", 0.0) + melon_cnt * 250.0

        strawberry_cnt = state.get_shed_count("STRAWBERRY")
        if strawberry_cnt > 0 and orders_placed < max_orders:
            builder.sell("STRAWBERRY", strawberry_cnt)
            orders_placed += 1
            self.telemetry.quantities_sold["STRAWBERRY"] = self.telemetry.quantities_sold.get("STRAWBERRY", 0) + strawberry_cnt
            self.telemetry.realized_revenue["STRAWBERRY"] = self.telemetry.realized_revenue.get("STRAWBERRY", 0.0) + strawberry_cnt * 175.0

        tomato_cnt = state.get_shed_count("TOMATO")
        if tomato_cnt > 0 and orders_placed < max_orders:
            builder.sell("TOMATO", tomato_cnt)
            orders_placed += 1
            self.telemetry.quantities_sold["TOMATO"] = self.telemetry.quantities_sold.get("TOMATO", 0) + tomato_cnt
            self.telemetry.realized_revenue["TOMATO"] = self.telemetry.realized_revenue.get("TOMATO", 0.0) + tomato_cnt * 100.0

        carrot_cnt = state.get_shed_count("CARROT")
        if carrot_cnt > 0 and orders_placed < max_orders:
            builder.sell("CARROT", carrot_cnt)
            orders_placed += 1
            self.telemetry.quantities_sold["CARROT"] = self.telemetry.quantities_sold.get("CARROT", 0) + carrot_cnt
            self.telemetry.realized_revenue["CARROT"] = self.telemetry.realized_revenue.get("CARROT", 0.0) + carrot_cnt * 35.0

        wheat_cnt = state.get_shed_count("WHEAT")
        feed_buffer = self.config.feed_safety_buffer
        if wheat_cnt > feed_buffer and orders_placed < max_orders:
            sell_qty = wheat_cnt - feed_buffer
            builder.sell("WHEAT", sell_qty)
            orders_placed += 1
            self.telemetry.quantities_sold["WHEAT"] = self.telemetry.quantities_sold.get("WHEAT", 0) + sell_qty
            self.telemetry.realized_revenue["WHEAT"] = self.telemetry.realized_revenue.get("WHEAT", 0.0) + sell_qty * 25.0

    def _decide_e12_centered_hybrid(self, state: GameState) -> Dict[str, Any]:

        # 1. Market Phase: Sell MILK and ALL harvested crops immediately
        for product in list(CROPS.keys()) + ["MILK", "WOOL"]:
            shed_count = state.get_shed_count(product)
            if shed_count > 0:
                builder.sell(product, shed_count)
                price = state.get_price(product)
                if product in CROPS:
                    unit_price = price if price > 0 else CROPS[product]["seed"] * 1.75
                elif product == "MILK":
                    unit_price = price if price > 0 else 160.0
                elif product == "WOOL":
                    unit_price = price if price > 0 else 200.0
                else:
                    unit_price = 100.0
                self.telemetry.realized_revenue[product] = self.telemetry.realized_revenue.get(product, 0.0) + (shed_count * unit_price)

        cumulative_realized_revenue = sum(self.telemetry.realized_revenue.values())
        startup_seed_price = CROPS["TOMATO"]["seed"]  # $50.00
        operating_reserve = 50.0  # Aggressive opening cash reserve

        # 2. Count Livestock Inventory & Placed State
        cows_in_shed = state.get_shed_count("COW")
        cows_in_inv = sum(state.get_worker_inventory_count(w, "COW") for w in range(total_workers))
        placed_cow_tiles: List[Tuple[int, int]] = []
        active_pasture_tiles: List[Tuple[int, int]] = []

        for y in range(len(state.tiles)):
            for x in range(len(state.tiles[y])):
                t = state.tiles[y][x]
                if isinstance(t, dict) and t.get("kind") == "PASTURE":
                    active_pasture_tiles.append((x, y))
                    if t.get("animal") == "COW":
                        placed_cow_tiles.append((x, y))

        cows_owned = cows_in_shed + cows_in_inv + len(placed_cow_tiles)
        setattr(self.telemetry, "cows_acquired", cows_owned)
        setattr(self.telemetry, "active_cow_count", len(placed_cow_tiles))
        setattr(self.telemetry, "active_pasture_count", len(active_pasture_tiles))

        cash = state.money

        # 3. Progressive Livestock Acquisition Gate (Cow #1 -> Production Gate -> Cow #2..#4)
        if cows_owned < 4 and cows_in_shed == 0 and cows_in_inv == 0:
            cow_cost = 400.0
            wheat_shed = state.get_shed_count("WHEAT")
            milk_harv = getattr(self.telemetry, "milk_harvested", 0)
            milk_rev = self.telemetry.realized_revenue.get("MILK", 0.0)

            # Cow #1: Purchased ONLY WHEN harvested wheat feed is ready in shed (wheat_shed >= 1)
            # Cow #2..#4: Purchased ONLY AFTER Cow N has passed production gate (milk harvested >= 1 and wheat buffer >= 4)
            if cows_owned == 0 and wheat_shed >= 1 and cash >= cow_cost:
                can_buy_cow = True
            elif cows_owned > 0 and len(placed_cow_tiles) == cows_owned:
                gate_passed = (milk_harv >= 1 and wheat_shed >= 4)
                can_buy_cow = gate_passed and (cash >= cow_cost + 200.0)
            else:
                can_buy_cow = False

            if can_buy_cow:
                builder.buy_animal("COW", 1)
                self.telemetry.spending_livestock += cow_cost
                cows_owned += 1
                cows_in_shed += 1
                cash -= cow_cost
                if getattr(self.telemetry, "day_first_cow", None) is None:
                    setattr(self.telemetry, "day_first_cow", state.day)
                    setattr(self.telemetry, "turn_first_cow", state.step + 1)
                self.telemetry.log_event("BUY_COW", state.step, state.day, state.hour, state.money, f"Progressively Purchased Cow #{cows_owned}")

        # 4. Land Expansion Triggers (Q1 & Sustainable Q2 Reinvestment)
        # Gate 1 (Q1): Gated strictly on Feed-First Production Gate (milk harvest >= 1 or milk revenue > 0)
        if self.config.enable_land_expansion and owned_quadrants < 2 and state.day >= 1:
            land_cost = 1000.0
            milk_harv = getattr(self.telemetry, "milk_harvested", 0)
            milk_rev = self.telemetry.realized_revenue.get("MILK", 0.0)
            feed_gate = (milk_harv >= 1 or milk_rev > 0.0)
            
            if state.hour == 0 and feed_gate and cash >= land_cost + 300.0:
                builder.buy_land()
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_quadrants = 2
                self.owned_quadrants = 2
                self.telemetry.buy_land_executed_step = state.step
                setattr(self.telemetry, "buy_land_day", state.day)
                cash -= land_cost
                self.telemetry.log_event("BUY_LAND", state.step, state.day, state.hour, state.money, f"Unlocked Q1 Land (Cash: ${cash:.2f})")

        # Sustainable Q2 Reinvestment: Unlocked when cash >= Q2_COST ($2000) + Next Cycle Costs + $300 reserve
        if self.config.enable_land_expansion and self.owned_quadrants == 2 and state.day >= 5:
            q2_cost = 2000.0
            next_cycle_cost = startup_seed_price * 9  # $450
            if state.hour == 0 and cash >= q2_cost + next_cycle_cost + 300.0:
                builder.buy_land()
                self.telemetry.spending_land += q2_cost
                self.telemetry.owned_quadrants = 3
                self.owned_quadrants = 3
                setattr(self.telemetry, "q2_buy_land_day", state.day)
                cash -= q2_cost
                self.telemetry.log_event("BUY_LAND_Q2", state.step, state.day, state.hour, state.money, f"Sustainable Reinvestment Unlocked Q2 Land (Cash: ${cash:.2f})")

        # 5. Determine Active Managed Tile Partitions per Worker
        epu2_target_13 = [(5, 2), (5, 3), (5, 4), (6, 2), (6, 3), (6, 4), (7, 2), (7, 3), (7, 4), (5, 1), (6, 1), (8, 3), (8, 4)]
        farmer_tiles = [(2, 2), (3, 2), (4, 2)]
        hand1_tiles = [(2, 3), (2, 4), (1, 3), (1, 4), (3, 1), (4, 1), (5, 2), (5, 3), (5, 4), (6, 2), (6, 3), (6, 4)] if self.owned_quadrants >= 2 else [(2, 3), (2, 4), (1, 3), (1, 4), (3, 1), (4, 1)]
        hand2_tiles = epu2_target_13 if self.owned_quadrants >= 2 else []

        # 6. Workload-driven HIRE Trigger (Hire Hand 1 immediately in opening for crop tasks)
        target_hands = 1
        if self.owned_quadrants >= 2:
            target_hands = 2

        current_hands = len(hands)
        if state.hour == 0 and current_hands < target_hands and state.hires_today == 0 and cash >= 50.0:
            builder.hire()
            self.telemetry.spending_workforce += 50.0
            self.telemetry.hires_count += 1
            cash -= 50.0
            self.telemetry.log_event("HIRE", state.step, state.day, state.hour, state.money, f"Hired Hand ({current_hands + 1})")

        # 7. Planted Count & Milestone Telemetry Tracking
        active_managed_tiles = list(farmer_tiles) + list(hand1_tiles) + list(hand2_tiles) + livestock_core_reserved
        active_planted_count = sum(
            1 for pos in active_managed_tiles
            if state.get_tile(pos[0], pos[1]) is not None and isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("kind") == "PLANT"
        )
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, active_planted_count)

        virtual_seeds: Dict[str, int] = {
            crop: state.get_seed_count(crop) for crop in CROPS.keys()
        }

        # Dynamic Wheat Feed Sizing (Ensure WHEAT seeds are bought FIRST for feed security)
        needed_wheat_seeds = max(4, int(cows_owned * 3) + 2)
        current_wheat_seeds = virtual_seeds.get("WHEAT", 0)
        if current_wheat_seeds < needed_wheat_seeds and cash >= 10.0:
            buy_qty = min(needed_wheat_seeds - current_wheat_seeds, int(cash // 10.0))
            if buy_qty > 0:
                builder.buy_seed("WHEAT", buy_qty)
                self.telemetry.spending_seeds += buy_qty * 10.0
                cash -= buy_qty * 10.0
                virtual_seeds["WHEAT"] = current_wheat_seeds + buy_qty

        target_crop = self.select_best_crop_roi(state, cash)
        target_seed_cost = CROPS[target_crop]["seed"]

        all_empty_crop_tiles: List[Tuple[int, int]] = []
        for pos in farmer_tiles + hand1_tiles + hand2_tiles:
            if pos not in livestock_core_reserved and state.get_tile(pos[0], pos[1]) is None:
                all_empty_crop_tiles.append(pos)

        target_seeds_owned = virtual_seeds.get(target_crop, 0)
        needed_seeds = max(0, len(all_empty_crop_tiles) - target_seeds_owned)
        available_seed_cash = max(0.0, cash - 150.0)

        if needed_seeds > 0 and available_seed_cash >= target_seed_cost:
            buy_qty = min(needed_seeds, int(available_seed_cash // target_seed_cost))
            if buy_qty > 0:
                builder.buy_seed(target_crop, buy_qty)
                self.telemetry.spending_seeds += buy_qty * target_seed_cost
                target_seeds_owned += buy_qty
                cash -= buy_qty * target_seed_cost
                virtual_seeds[target_crop] = target_seeds_owned

        # 8. Compute Worker Actions (Prioritizing Pasture Building, Cow Placement, Feeding & Milk Harvest)
        farmer_pos = state.farmer_position
        farmer_inv_cow = state.get_worker_inventory_count(0, "COW")
        farmer_act = None

        if farmer_inv_cow > 0:
            for (tx, ty) in livestock_core_reserved:
                tile = state.get_tile(tx, ty)
                if tile is None:
                    dist = abs(farmer_pos[0] - tx) + abs(farmer_pos[1] - ty)
                    if dist == 0:
                        farmer_act = ["BUILD_PASTURE"]
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], (tx, ty))
                    break
                elif isinstance(tile, dict) and tile.get("kind") == "PASTURE" and "animal" not in tile:
                    dist = abs(farmer_pos[0] - tx) + abs(farmer_pos[1] - ty)
                    if dist == 0:
                        farmer_act = ["PLACE", "COW"]
                        setattr(self.telemetry, "animals_placed", getattr(self.telemetry, "animals_placed", 0) + 1)
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], (tx, ty))
                    break
        elif cows_in_shed > 0 and farmer_inv_cow == 0:
            dist = abs(farmer_pos[0] - shed_access_tile[0]) + abs(farmer_pos[1] - shed_access_tile[1])
            if dist == 0:
                farmer_act = ["PICKUP", "COW", 1]
            else:
                farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], shed_access_tile)

        # Feeding & Milk Harvesting Loop (High Priority for Any Worker)
        if farmer_act is None:
            # Check Feeding candidate first to prevent cow starvation
            unfed_cow_tiles = [pos for pos in placed_cow_tiles if isinstance(state.get_tile(pos[0], pos[1]), dict) and not state.get_tile(pos[0], pos[1]).get("fed_today", False)]
            if unfed_cow_tiles:
                farmer_wheat = state.get_worker_inventory_count(0, "WHEAT")
                if farmer_wheat > 0:
                    best_tile = min(unfed_cow_tiles, key=lambda p: abs(farmer_pos[0] - p[0]) + abs(farmer_pos[1] - p[1]))
                    dist = abs(farmer_pos[0] - best_tile[0]) + abs(farmer_pos[1] - best_tile[1])
                    if dist == 0:
                        farmer_act = ["FEED"]
                        setattr(self.telemetry, "feed_consumed", getattr(self.telemetry, "feed_consumed", 0) + 1)
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], best_tile)
                elif state.get_shed_count("WHEAT") > 0:
                    dist = abs(farmer_pos[0] - shed_access_tile[0]) + abs(farmer_pos[1] - shed_access_tile[1])
                    if dist == 0:
                        farmer_act = ["PICKUP", "WHEAT", min(5, state.get_shed_count("WHEAT"))]
                    else:
                        farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], shed_access_tile)

        if farmer_act is None:
            # Check Milk harvest candidate
            milk_ready_tiles = [pos for pos in placed_cow_tiles if isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("yield_units", 0) > 0]
            if milk_ready_tiles:
                best_tile = min(milk_ready_tiles, key=lambda p: abs(farmer_pos[0] - p[0]) + abs(farmer_pos[1] - p[1]))
                dist = abs(farmer_pos[0] - best_tile[0]) + abs(farmer_pos[1] - best_tile[1])
                if dist == 0:
                    farmer_act = ["HARVEST"]
                    setattr(self.telemetry, "milk_harvested", getattr(self.telemetry, "milk_harvested", 0) + 1)
                else:
                    farmer_act = self._move_towards(farmer_pos[0], farmer_pos[1], best_tile)

        if farmer_act is None:
            farmer_act, _ = self._compute_e06_worker_action(
                farmer_pos, farmer_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )

        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        if len(hands) >= 1:
            hand1_pos = hands[0]
            hand1_act, _ = self._compute_e06_worker_action(
                hand1_pos, hand1_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand1_act)

        if len(hands) >= 2 and self.owned_quadrants >= 2 and len(hand2_tiles) > 0:
            hand2_pos = hands[1]
            hand2_act, _ = self._compute_e06_worker_action(
                hand2_pos, hand2_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand2_act)

        # 9. Record Turn-by-Turn Telemetry for Turns 1-24
        if state.step < 24:
            turn_telemetry = getattr(self.telemetry, "turn_telemetry_1_24", [])
            wheat_count = sum(1 for pos in active_managed_tiles if isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("crop") == "WHEAT")
            other_crop_count = active_planted_count - wheat_count
            
            turn_record = {
                "turn": state.step + 1,
                "day": state.day,
                "hour": state.hour,
                "cash": state.money,
                "farmer_pos": state.farmer_position,
                "farmer_act": farmer_act,
                "owned_quadrants": self.owned_quadrants,
                "active_pastures": len(active_pasture_tiles),
                "active_cows": len(placed_cow_tiles),
                "cows_owned": cows_owned,
                "wheat_tiles": wheat_count,
                "other_crop_tiles": other_crop_count,
                "wheat_inventory": state.get_seed_count("WHEAT") + state.get_shed_count("WHEAT"),
                "milk_inventory": state.get_shed_count("MILK"),
                "feed_consumed_cum": getattr(self.telemetry, "feed_consumed", 0),
                "milk_harvested_cum": getattr(self.telemetry, "milk_harvested", 0),
                "milk_revenue_cum": self.telemetry.realized_revenue.get("MILK", 0.0),
                "total_revenue_cum": cumulative_realized_revenue,
            }
            turn_telemetry.append(turn_record)
            setattr(self.telemetry, "turn_telemetry_1_24", turn_telemetry)

        return builder.build()

    def _decide_epu_corner_pruned_center_out(self, state: GameState) -> Dict[str, Any]:
        """E11-X1.7 Corner-Pruned Center-Out EPU Scaling Strategy (26 tiles max: 9 -> 13 -> BUY_LAND -> 22 -> 26)."""
        if state.step == 0:
            self.telemetry.starting_money = state.money
            self.epu1_densified = False
            self.epu2_densified = False

        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(state)

        raw_quads = state.my_farm.get("unlocked_quadrants", 1)
        owned_quadrants = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        self.owned_quadrants = max(self.owned_quadrants, owned_quadrants)

        # Prescriptive coordinate definitions (0-indexed, origin/shed at (4,4))
        epu1_core_3x3 = [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4)]
        epu1_extension = [(1, 3), (1, 4), (3, 1), (4, 1)]
        epu1_target_13 = epu1_core_3x3 + epu1_extension

        epu2_core_3x3 = [(5, 2), (5, 3), (5, 4), (6, 2), (6, 3), (6, 4), (7, 2), (7, 3), (7, 4)]
        epu2_extension = [(5, 1), (6, 1), (8, 3), (8, 4)]
        epu2_target_13 = epu2_core_3x3 + epu2_extension

        builder = ActionBuilder()

        # 1. Market Phase: Sell ANY harvested crops in shed immediately
        for crop_name in CROPS.keys():
            shed_count = state.get_shed_count(crop_name)
            if shed_count > 0:
                builder.sell(crop_name, shed_count)
                price = state.get_price(crop_name)
                unit_price = price if price > 0 else CROPS[crop_name]["seed"] * 1.75
                self.telemetry.realized_revenue[crop_name] = self.telemetry.realized_revenue.get(crop_name, 0.0) + (shed_count * unit_price)

        cumulative_realized_revenue = sum(self.telemetry.realized_revenue.values())
        startup_seed_price = CROPS["TOMATO"]["seed"]  # $50.00
        operating_reserve = self.config.operating_reserve  # $300.00

        # 2. Gate 1: EPU1 3x3 -> 13t Corner-Pruned Extension Trigger (4 tiles)
        if not getattr(self, "epu1_densified", False) and cumulative_realized_revenue > 0.0:
            current_seeds = sum(state.get_seed_count(c) for c in CROPS.keys()) + sum(state.get_shed_count(c) for c in CROPS.keys())
            needed_ext_seeds = max(0, 4 - current_seeds)
            epu1_ext_cost = needed_ext_seeds * startup_seed_price
            required_cash_epu1_ext = epu1_ext_cost + operating_reserve
            if state.money >= required_cash_epu1_ext:
                self.epu1_densified = True
                setattr(self.telemetry, "epu1_densification_start_day", state.day)
                self.telemetry.log_event("PRUNED_EXTEND_EPU1", state.step, state.day, state.hour, state.money, f"Opened Gate EPU1 9t -> 13t Corner-Pruned Extension")

        # 3. Gate 2: BUY_LAND Q1 Trigger (Post-surplus revenue)
        if self.config.enable_land_expansion and owned_quadrants < 2 and state.day >= 1:
            land_cost = 1000.0
            current_seeds = sum(state.get_seed_count(c) for c in CROPS.keys()) + sum(state.get_shed_count(c) for c in CROPS.keys())
            epu2_core_seeds_needed = max(0, 9 - current_seeds)
            epu2_core_startup = epu2_core_seeds_needed * startup_seed_price
            required_cash_for_q1 = land_cost + epu2_core_startup + operating_reserve

            if state.hour == 0 and cumulative_realized_revenue > 0.0 and state.money >= required_cash_for_q1:
                builder.buy_land()
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_quadrants = 2
                self.owned_quadrants = 2
                self.telemetry.buy_land_executed_step = state.step
                setattr(self.telemetry, "buy_land_day", state.day)
                setattr(self.telemetry, "actual_trigger_value", required_cash_for_q1)
                self.telemetry.log_event("BUY_LAND", state.step, state.day, state.hour, state.money, f"Bought Q1 Land for Pruned EPU2 Post-Surplus (Rev: ${cumulative_realized_revenue:.2f}, Trigger: ${required_cash_for_q1:.2f})")

        # 4. Gate 3: EPU2 3x3 -> 13t Corner-Pruned Extension Trigger (4 tiles)
        if owned_quadrants >= 2 and getattr(self, "epu1_densified", False) and not getattr(self, "epu2_densified", False):
            current_seeds = sum(state.get_seed_count(c) for c in CROPS.keys()) + sum(state.get_shed_count(c) for c in CROPS.keys())
            needed_epu2_ext_seeds = max(0, 4 - current_seeds)
            epu2_ext_cost = needed_epu2_ext_seeds * startup_seed_price
            required_cash_epu2_ext = epu2_ext_cost + operating_reserve
            if state.money >= required_cash_epu2_ext:
                self.epu2_densified = True
                setattr(self.telemetry, "epu2_densification_start_day", state.day)
                self.telemetry.log_event("PRUNED_EXTEND_EPU2", state.step, state.day, state.hour, state.money, f"Opened Gate EPU2 9t -> 13t Corner-Pruned Extension")

        # 5. Determine Active Managed Tile Partitions per Worker
        if getattr(self, "epu1_densified", False):
            farmer_tiles = [(1, 3), (1, 4), (2, 2), (2, 3), (2, 4), (3, 2), (3, 3)]
            hand1_tiles = [(3, 1), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4)]
        else:
            farmer_tiles = [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3)]
            hand1_tiles = [(3, 4), (4, 2), (4, 3), (4, 4)]

        if owned_quadrants >= 2:
            if getattr(self, "epu2_densified", False):
                hand2_tiles = epu2_target_13
            else:
                hand2_tiles = epu2_core_3x3
        else:
            hand2_tiles = []

        # 6. Workload-driven Daily HIRE Trigger
        target_hands = 1
        if owned_quadrants >= 2:
            target_hands = 2

        current_hands = len(hands)
        hires_needed = max(0, target_hands - current_hands - state.hires_today)

        if state.hour == 0 and hires_needed > 0:
            hire_cap = 1 if self.config.multi_hire_mode == "SINGLE_PER_DAY" else hires_needed
            for _ in range(min(hires_needed, hire_cap)):
                if state.money >= 1.0:
                    builder.hire()
                    self.telemetry.spending_workforce += 1.0
                    self.telemetry.hires_count += 1
                    hand_idx = current_hands + 1
                    if hand_idx == 2:
                        setattr(self.telemetry, "epu2_activation_day", state.day)
                    self.telemetry.log_event("HIRE", state.step, state.day, state.hour, state.money, f"Hired Hand ({hand_idx})")

        # 7. Planted Count & Milestone Telemetry Tracking
        active_managed_tiles = list(farmer_tiles) + list(hand1_tiles) + list(hand2_tiles)
        active_planted_count = sum(
            1 for pos in active_managed_tiles
            if state.get_tile(pos[0], pos[1]) is not None and isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("kind") == "PLANT"
        )
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, active_planted_count)
        if active_planted_count >= 9 and getattr(self.telemetry, "day_reaching_9_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_9_active_tiles", state.day)
        if active_planted_count >= 13 and getattr(self.telemetry, "day_reaching_13_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_13_active_tiles", state.day)
        if active_planted_count >= 22 and getattr(self.telemetry, "day_reaching_22_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_22_active_tiles", state.day)
        if active_planted_count >= 26 and getattr(self.telemetry, "day_reaching_26_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_26_active_tiles", state.day)

        cash = state.money
        target_crop = self.select_best_crop_roi(state, cash)
        target_crop_info = CROPS[target_crop]
        target_seed_cost = target_crop_info["seed"]

        all_empty_tiles: List[Tuple[int, int]] = []
        for pos in active_managed_tiles:
            tile = state.get_tile(pos[0], pos[1])
            if tile is None:
                all_empty_tiles.append(pos)

        target_seeds_owned = state.get_seed_count(target_crop)
        needed_seeds = max(0, len(all_empty_tiles) - target_seeds_owned)

        if needed_seeds > 0 and cash >= target_seed_cost:
            buy_qty = min(needed_seeds, int(cash // target_seed_cost))
            if buy_qty > 0:
                builder.buy_seed(target_crop, buy_qty)
                self.telemetry.spending_seeds += buy_qty * target_seed_cost
                target_seeds_owned += buy_qty

        virtual_seeds: Dict[str, int] = {
            crop: state.get_seed_count(crop) for crop in CROPS.keys()
        }
        virtual_seeds[target_crop] = target_seeds_owned

        # 8. Compute Worker Actions
        farmer_pos = state.farmer_position
        farmer_act, _ = self._compute_e06_worker_action(
            farmer_pos, farmer_tiles, target_crop, target_seed_cost, virtual_seeds, state
        )
        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        if len(hands) >= 1:
            hand1_pos = hands[0]
            hand1_act, _ = self._compute_e06_worker_action(
                hand1_pos, hand1_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand1_act)

        if len(hands) >= 2 and owned_quadrants >= 2 and len(hand2_tiles) > 0:
            hand2_pos = hands[1]
            hand2_act, _ = self._compute_e06_worker_action(
                hand2_pos, hand2_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand2_act)

        return builder.build()

    def _decide_e06_progressive(self, state: GameState) -> Dict[str, Any]:
        """E11-X1.6 Progressive Center-Out 3x3 -> 4x4 EPU Scaling Strategy (32 tiles max)."""
        if state.step == 0:
            self.telemetry.starting_money = state.money
            self.epu1_densified = False
            self.epu2_densified = False

        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(state)

        raw_quads = state.my_farm.get("unlocked_quadrants", 1)
        owned_quadrants = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        self.owned_quadrants = max(self.owned_quadrants, owned_quadrants)

        # Coordinate definitions (0-indexed, center adjacent)
        epu1_3x3 = [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4)]
        epu1_4x4 = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4),
                    (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4)]

        epu2_3x3 = [(5, 2), (5, 3), (5, 4), (6, 2), (6, 3), (6, 4), (7, 2), (7, 3), (7, 4)]
        epu2_4x4 = [(5, 1), (5, 2), (5, 3), (5, 4), (6, 1), (6, 2), (6, 3), (6, 4),
                    (7, 1), (7, 2), (7, 3), (7, 4), (8, 1), (8, 2), (8, 3), (8, 4)]

        builder = ActionBuilder()

        # 1. Market Phase: Sell ANY harvested crops in shed immediately
        for crop_name in CROPS.keys():
            shed_count = state.get_shed_count(crop_name)
            if shed_count > 0:
                builder.sell(crop_name, shed_count)
                price = state.get_price(crop_name)
                unit_price = price if price > 0 else CROPS[crop_name]["seed"] * 1.75
                self.telemetry.realized_revenue[crop_name] = self.telemetry.realized_revenue.get(crop_name, 0.0) + (shed_count * unit_price)

        cumulative_realized_revenue = sum(self.telemetry.realized_revenue.values())
        startup_seed_price = CROPS["TOMATO"]["seed"]  # $50.00
        operating_reserve = self.config.operating_reserve  # $300.00

        # 2. Gate 1: EPU1 3x3 -> 4x4 Densification Trigger (7 ring tiles)
        if not getattr(self, "epu1_densified", False) and cumulative_realized_revenue > 0.0:
            current_seeds = sum(state.get_seed_count(c) for c in CROPS.keys()) + sum(state.get_shed_count(c) for c in CROPS.keys())
            needed_ring_seeds = max(0, 7 - current_seeds)
            epu1_ring_cost = needed_ring_seeds * startup_seed_price
            required_cash_epu1_densify = epu1_ring_cost + operating_reserve
            if state.money >= required_cash_epu1_densify:
                self.epu1_densified = True
                setattr(self.telemetry, "epu1_densification_start_day", state.day)
                self.telemetry.log_event("DENSIFY_EPU1", state.step, state.day, state.hour, state.money, f"Opened Gate EPU1 3x3 -> 4x4 Densification Ring")

        # 3. Gate 2: BUY_LAND Q1 Trigger (Post-surplus revenue)
        if self.config.enable_land_expansion and owned_quadrants < 2 and state.day >= 1:
            land_cost = 1000.0
            current_seeds = sum(state.get_seed_count(c) for c in CROPS.keys()) + sum(state.get_shed_count(c) for c in CROPS.keys())
            epu2_core_seeds_needed = max(0, 9 - current_seeds)
            epu2_core_startup = epu2_core_seeds_needed * startup_seed_price
            required_cash_for_q1 = land_cost + epu2_core_startup + operating_reserve

            if state.hour == 0 and cumulative_realized_revenue > 0.0 and state.money >= required_cash_for_q1:
                builder.buy_land()
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_quadrants = 2
                self.owned_quadrants = 2
                self.telemetry.buy_land_executed_step = state.step
                setattr(self.telemetry, "buy_land_day", state.day)
                setattr(self.telemetry, "actual_trigger_value", required_cash_for_q1)
                self.telemetry.log_event("BUY_LAND", state.step, state.day, state.hour, state.money, f"Bought Q1 Land for Progressive EPU2 Post-Surplus (Rev: ${cumulative_realized_revenue:.2f}, Trigger: ${required_cash_for_q1:.2f})")

        # 4. Gate 3: EPU2 3x3 -> 4x4 Densification Trigger (7 ring tiles)
        if owned_quadrants >= 2 and getattr(self, "epu1_densified", False) and not getattr(self, "epu2_densified", False):
            current_seeds = sum(state.get_seed_count(c) for c in CROPS.keys()) + sum(state.get_shed_count(c) for c in CROPS.keys())
            needed_epu2_ring_seeds = max(0, 7 - current_seeds)
            epu2_ring_cost = needed_epu2_ring_seeds * startup_seed_price
            required_cash_epu2_densify = epu2_ring_cost + operating_reserve
            if state.money >= required_cash_epu2_densify:
                self.epu2_densified = True
                setattr(self.telemetry, "epu2_densification_start_day", state.day)
                self.telemetry.log_event("DENSIFY_EPU2", state.step, state.day, state.hour, state.money, f"Opened Gate EPU2 3x3 -> 4x4 Densification Ring")

        # 5. Determine Active Managed Tile Partitions per Worker
        if getattr(self, "epu1_densified", False):
            farmer_tiles = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4)]
            hand1_tiles = [(3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4)]
        else:
            farmer_tiles = [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3)]
            hand1_tiles = [(3, 4), (4, 2), (4, 3), (4, 4)]

        if owned_quadrants >= 2:
            if getattr(self, "epu2_densified", False):
                hand2_tiles = epu2_4x4
            else:
                hand2_tiles = epu2_3x3
        else:
            hand2_tiles = []

        # 6. Workload-driven Daily HIRE Trigger
        target_hands = 1
        if owned_quadrants >= 2:
            target_hands = 2

        current_hands = len(hands)
        hires_needed = max(0, target_hands - current_hands - state.hires_today)

        if state.hour == 0 and hires_needed > 0:
            hire_cap = 1 if self.config.multi_hire_mode == "SINGLE_PER_DAY" else hires_needed
            for _ in range(min(hires_needed, hire_cap)):
                if state.money >= 1.0:
                    builder.hire()
                    self.telemetry.spending_workforce += 1.0
                    self.telemetry.hires_count += 1
                    hand_idx = current_hands + 1
                    if hand_idx == 2:
                        setattr(self.telemetry, "epu2_activation_day", state.day)
                    self.telemetry.log_event("HIRE", state.step, state.day, state.hour, state.money, f"Hired Hand ({hand_idx})")

        # 7. Planted Count & Milestone Telemetry Tracking
        active_managed_tiles = list(farmer_tiles) + list(hand1_tiles) + list(hand2_tiles)
        active_planted_count = sum(
            1 for pos in active_managed_tiles
            if state.get_tile(pos[0], pos[1]) is not None and isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("kind") == "PLANT"
        )
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, active_planted_count)
        if active_planted_count >= 9 and getattr(self.telemetry, "day_reaching_9_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_9_active_tiles", state.day)
        if active_planted_count >= 16 and getattr(self.telemetry, "day_reaching_16_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_16_active_tiles", state.day)
        if active_planted_count >= 25 and getattr(self.telemetry, "day_reaching_25_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_25_active_tiles", state.day)
        if active_planted_count >= 30 and getattr(self.telemetry, "day_reaching_30_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_30_active_tiles", state.day)
        if active_planted_count >= 32 and getattr(self.telemetry, "day_reaching_32_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_32_active_tiles", state.day)

        cash = state.money
        target_crop = self.select_best_crop_roi(state, cash)
        target_crop_info = CROPS[target_crop]
        target_seed_cost = target_crop_info["seed"]

        all_empty_tiles: List[Tuple[int, int]] = []
        for pos in active_managed_tiles:
            tile = state.get_tile(pos[0], pos[1])
            if tile is None:
                all_empty_tiles.append(pos)

        target_seeds_owned = state.get_seed_count(target_crop)
        needed_seeds = max(0, len(all_empty_tiles) - target_seeds_owned)

        if needed_seeds > 0 and cash >= target_seed_cost:
            buy_qty = min(needed_seeds, int(cash // target_seed_cost))
            if buy_qty > 0:
                builder.buy_seed(target_crop, buy_qty)
                self.telemetry.spending_seeds += buy_qty * target_seed_cost
                target_seeds_owned += buy_qty

        virtual_seeds: Dict[str, int] = {
            crop: state.get_seed_count(crop) for crop in CROPS.keys()
        }
        virtual_seeds[target_crop] = target_seeds_owned

        # 8. Compute Worker Actions
        farmer_pos = state.farmer_position
        farmer_act, _ = self._compute_e06_worker_action(
            farmer_pos, farmer_tiles, target_crop, target_seed_cost, virtual_seeds, state
        )
        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        if len(hands) >= 1:
            hand1_pos = hands[0]
            hand1_act, _ = self._compute_e06_worker_action(
                hand1_pos, hand1_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand1_act)

        if len(hands) >= 2 and owned_quadrants >= 2 and len(hand2_tiles) > 0:
            hand2_pos = hands[1]
            hand2_act, _ = self._compute_e06_worker_action(
                hand2_pos, hand2_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand2_act)

        return builder.build()

    def _decide_e06_centered(self, state: GameState) -> Dict[str, Any]:
        """E11-X1.5 Centered 2x4x4 Productive Core Strategy (32 tiles across 2 EPUs)."""
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(state)

        raw_quads = state.my_farm.get("unlocked_quadrants", 1)
        owned_quadrants = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        self.owned_quadrants = max(self.owned_quadrants, owned_quadrants)

        # Centered EPU1 4x4 Partition (x=1..4, y=1..4 in Q0)
        farmer_tiles = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4)]
        hand1_tiles = [(3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4)]

        # Centered EPU2 4x4 Partition (x=5..8, y=1..4 in Q1)
        hand2_tiles = [(5, 1), (5, 2), (5, 3), (5, 4), (6, 1), (6, 2), (6, 3), (6, 4),
                       (7, 1), (7, 2), (7, 3), (7, 4), (8, 1), (8, 2), (8, 3), (8, 4)]

        builder = ActionBuilder()

        # 1. Market Phase: Sell ANY harvested crops in shed immediately
        for crop_name in CROPS.keys():
            shed_count = state.get_shed_count(crop_name)
            if shed_count > 0:
                builder.sell(crop_name, shed_count)
                price = state.get_price(crop_name)
                unit_price = price if price > 0 else CROPS[crop_name]["seed"] * 1.75
                self.telemetry.realized_revenue[crop_name] = self.telemetry.realized_revenue.get(crop_name, 0.0) + (shed_count * unit_price)

        # 2. Derived Dynamic Land Expansion Trigger for EPU2 (Q1)
        cumulative_realized_revenue = sum(self.telemetry.realized_revenue.values())
        if self.config.enable_land_expansion and owned_quadrants < 2 and state.day >= 1:
            land_cost = 1000.0
            startup_seed_price = CROPS["TOMATO"]["seed"]
            current_seeds = sum(state.get_seed_count(c) for c in CROPS.keys()) + sum(state.get_shed_count(c) for c in CROPS.keys())
            epu2_seeds_needed = max(0, 16 - current_seeds)
            epu2_actual_startup = epu2_seeds_needed * startup_seed_price
            operating_reserve = self.config.operating_reserve  # $300.00
            required_cash_for_q1 = land_cost + epu2_actual_startup + operating_reserve

            if state.hour == 0 and cumulative_realized_revenue > 0.0 and state.money >= required_cash_for_q1:
                builder.buy_land()
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_quadrants = 2
                self.owned_quadrants = 2
                self.telemetry.buy_land_executed_step = state.step
                setattr(self.telemetry, "buy_land_day", state.day)
                setattr(self.telemetry, "actual_trigger_value", required_cash_for_q1)
                self.telemetry.log_event("BUY_LAND", state.step, state.day, state.hour, state.money, f"Bought Q1 Land for Centered EPU2 4x4 Post-Surplus (Rev: ${cumulative_realized_revenue:.2f}, Trigger: ${required_cash_for_q1:.2f})")

        # 3. Workload-driven Daily HIRE Trigger (2 Hands max for 2 EPUs)
        target_hands = 1
        if owned_quadrants >= 2:
            target_hands = 2

        current_hands = len(hands)
        hires_needed = max(0, target_hands - current_hands - state.hires_today)

        if state.hour == 0 and hires_needed > 0:
            hire_cap = 1 if self.config.multi_hire_mode == "SINGLE_PER_DAY" else hires_needed
            for _ in range(min(hires_needed, hire_cap)):
                if state.money >= 1.0:
                    builder.hire()
                    self.telemetry.spending_workforce += 1.0
                    self.telemetry.hires_count += 1
                    hand_idx = current_hands + 1
                    if hand_idx == 2:
                        setattr(self.telemetry, "epu2_activation_day", state.day)
                    self.telemetry.log_event("HIRE", state.step, state.day, state.hour, state.money, f"Hired Hand ({hand_idx})")

        # 4. Dynamic ROI Crop Selection & Seed Buying
        active_managed_tiles = list(farmer_tiles) + list(hand1_tiles)
        if owned_quadrants >= 2:
            active_managed_tiles.extend(hand2_tiles)

        active_planted_count = sum(
            1 for pos in active_managed_tiles
            if state.get_tile(pos[0], pos[1]) is not None and isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("kind") == "PLANT"
        )
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, active_planted_count)
        if active_planted_count >= 16 and getattr(self.telemetry, "day_reaching_16_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_16_active_tiles", state.day)
        if active_planted_count >= 24 and getattr(self.telemetry, "day_reaching_24_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_24_active_tiles", state.day)
        if active_planted_count >= 30 and getattr(self.telemetry, "day_reaching_30_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_30_active_tiles", state.day)
        if active_planted_count >= 32 and getattr(self.telemetry, "day_reaching_32_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_32_active_tiles", state.day)

        cash = state.money
        target_crop = self.select_best_crop_roi(state, cash)
        target_crop_info = CROPS[target_crop]
        target_seed_cost = target_crop_info["seed"]

        all_empty_tiles: List[Tuple[int, int]] = []
        for pos in active_managed_tiles:
            tile = state.get_tile(pos[0], pos[1])
            if tile is None:
                all_empty_tiles.append(pos)

        target_seeds_owned = state.get_seed_count(target_crop)
        needed_seeds = max(0, len(all_empty_tiles) - target_seeds_owned)

        if needed_seeds > 0 and cash >= target_seed_cost:
            buy_qty = min(needed_seeds, int(cash // target_seed_cost))
            if buy_qty > 0:
                builder.buy_seed(target_crop, buy_qty)
                self.telemetry.spending_seeds += buy_qty * target_seed_cost
                target_seeds_owned += buy_qty

        virtual_seeds: Dict[str, int] = {
            crop: state.get_seed_count(crop) for crop in CROPS.keys()
        }
        virtual_seeds[target_crop] = target_seeds_owned

        # 5. Compute Worker Actions per EPU Partition
        farmer_pos = state.farmer_position
        farmer_act, _ = self._compute_e06_worker_action(
            farmer_pos, farmer_tiles, target_crop, target_seed_cost, virtual_seeds, state
        )
        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        if len(hands) >= 1:
            hand1_pos = hands[0]
            hand1_act, _ = self._compute_e06_worker_action(
                hand1_pos, hand1_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand1_act)

        if len(hands) >= 2 and owned_quadrants >= 2:
            hand2_pos = hands[1]
            hand2_act, _ = self._compute_e06_worker_action(
                hand2_pos, hand2_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand2_act)

        return builder.build()

    def _decide_e06_densified(self, state: GameState) -> Dict[str, Any]:
        """E11-X1.4 2x3x5 EPU Densification Strategy (30 tiles across 2 EPUs)."""
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(state)

        raw_quads = state.my_farm.get("unlocked_quadrants", 1)
        owned_quadrants = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        self.owned_quadrants = max(self.owned_quadrants, owned_quadrants)

        # Base 9-tile core partitions for EPU1
        farmer_tiles = [(0, 0), (0, 1), (0, 2), (1, 0)]
        hand1_tiles = [(1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

        # Check operational status of EPU1 core (count planted tiles in core)
        core_planted = sum(
            1 for pos in (farmer_tiles + hand1_tiles)
            if state.get_tile(pos[0], pos[1]) is not None and isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("kind") == "PLANT"
        )
        if core_planted >= 4 and getattr(self.telemetry, "epu1_9t_activation_day", None) is None:
            setattr(self.telemetry, "epu1_9t_activation_day", state.day)

        # EPU1 Densification to 15 tiles (y=3, 4)
        if core_planted >= 5 or getattr(self.telemetry, "epu1_15t_activation_day", None) is not None:
            farmer_tiles.extend([(0, 3), (0, 4), (1, 3)])
            hand1_tiles.extend([(1, 4), (2, 3), (2, 4)])
            if getattr(self.telemetry, "epu1_15t_activation_day", None) is None:
                setattr(self.telemetry, "epu1_15t_activation_day", state.day)

        # EPU2 15-tile Partition
        hand2_tiles = [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                       (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
                       (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)]

        builder = ActionBuilder()

        # 1. Market Phase: Sell ANY harvested crops in shed immediately
        for crop_name in CROPS.keys():
            shed_count = state.get_shed_count(crop_name)
            if shed_count > 0:
                builder.sell(crop_name, shed_count)
                price = state.get_price(crop_name)
                unit_price = price if price > 0 else CROPS[crop_name]["seed"] * 1.75
                self.telemetry.realized_revenue[crop_name] = self.telemetry.realized_revenue.get(crop_name, 0.0) + (shed_count * unit_price)

        # 2. Derived Dynamic Land Expansion Trigger for EPU2 (Q1)
        cumulative_realized_revenue = sum(self.telemetry.realized_revenue.values())
        if self.config.enable_land_expansion and owned_quadrants < 2 and state.day >= 1:
            land_cost = 1000.0
            startup_seed_price = CROPS["TOMATO"]["seed"]
            current_seeds = sum(state.get_seed_count(c) for c in CROPS.keys()) + sum(state.get_shed_count(c) for c in CROPS.keys())
            epu2_seeds_needed = max(0, 15 - current_seeds)
            epu2_actual_startup = epu2_seeds_needed * startup_seed_price
            operating_reserve = self.config.operating_reserve  # $300.00
            required_cash_for_q1 = land_cost + epu2_actual_startup + operating_reserve

            if state.hour == 0 and cumulative_realized_revenue > 0.0 and state.money >= required_cash_for_q1:
                builder.buy_land()
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_quadrants = 2
                self.owned_quadrants = 2
                self.telemetry.buy_land_executed_step = state.step
                setattr(self.telemetry, "buy_land_day", state.day)
                setattr(self.telemetry, "actual_trigger_value", required_cash_for_q1)
                self.telemetry.log_event("BUY_LAND", state.step, state.day, state.hour, state.money, f"Bought Q1 Land for EPU2 3x5 Post-Surplus (Rev: ${cumulative_realized_revenue:.2f}, Trigger: ${required_cash_for_q1:.2f})")

        # 3. Workload-driven Daily HIRE Trigger (2 Hands max for 2 EPUs)
        target_hands = 1
        if owned_quadrants >= 2:
            target_hands = 2

        current_hands = len(hands)
        hires_needed = max(0, target_hands - current_hands - state.hires_today)

        if state.hour == 0 and hires_needed > 0:
            hire_cap = 1 if self.config.multi_hire_mode == "SINGLE_PER_DAY" else hires_needed
            for _ in range(min(hires_needed, hire_cap)):
                if state.money >= 1.0:
                    builder.hire()
                    self.telemetry.spending_workforce += 1.0
                    self.telemetry.hires_count += 1
                    hand_idx = current_hands + 1
                    if hand_idx == 2:
                        setattr(self.telemetry, "epu2_activation_day", state.day)
                    self.telemetry.log_event("HIRE", state.step, state.day, state.hour, state.money, f"Hired Hand ({hand_idx})")

        # 4. Dynamic ROI Crop Selection & Seed Buying
        active_managed_tiles = list(farmer_tiles) + list(hand1_tiles)
        if owned_quadrants >= 2:
            active_managed_tiles.extend(hand2_tiles)

        active_planted_count = sum(
            1 for pos in active_managed_tiles
            if state.get_tile(pos[0], pos[1]) is not None and isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("kind") == "PLANT"
        )
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, active_planted_count)
        if active_planted_count >= 27 and getattr(self.telemetry, "day_reaching_27_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_27_active_tiles", state.day)
        if active_planted_count >= 30 and getattr(self.telemetry, "day_reaching_30_active_tiles", None) is None:
            setattr(self.telemetry, "day_reaching_30_active_tiles", state.day)

        cash = state.money
        target_crop = self.select_best_crop_roi(state, cash)
        target_crop_info = CROPS[target_crop]
        target_seed_cost = target_crop_info["seed"]

        all_empty_tiles: List[Tuple[int, int]] = []
        for pos in active_managed_tiles:
            tile = state.get_tile(pos[0], pos[1])
            if tile is None:
                all_empty_tiles.append(pos)

        target_seeds_owned = state.get_seed_count(target_crop)
        needed_seeds = max(0, len(all_empty_tiles) - target_seeds_owned)

        if needed_seeds > 0 and cash >= target_seed_cost:
            buy_qty = min(needed_seeds, int(cash // target_seed_cost))
            if buy_qty > 0:
                builder.buy_seed(target_crop, buy_qty)
                self.telemetry.spending_seeds += buy_qty * target_seed_cost
                target_seeds_owned += buy_qty

        virtual_seeds: Dict[str, int] = {
            crop: state.get_seed_count(crop) for crop in CROPS.keys()
        }
        virtual_seeds[target_crop] = target_seeds_owned

        # 5. Compute Worker Actions per EPU Partition
        farmer_pos = state.farmer_position
        farmer_act, _ = self._compute_e06_worker_action(
            farmer_pos, farmer_tiles, target_crop, target_seed_cost, virtual_seeds, state
        )
        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        if len(hands) >= 1:
            hand1_pos = hands[0]
            hand1_act, _ = self._compute_e06_worker_action(
                hand1_pos, hand1_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand1_act)

        if len(hands) >= 2 and owned_quadrants >= 2:
            hand2_pos = hands[1]
            hand2_act, _ = self._compute_e06_worker_action(
                hand2_pos, hand2_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand2_act)

        return builder.build()

    def _decide_e06_replicated(self, state: GameState) -> Dict[str, Any]:
        """Run 100% exact E06 mechanism replication inside ProductiveMassROIAgent."""
        if state.step == 0:
            self.telemetry.starting_money = state.money
        self.telemetry.minimum_cash = min(self.telemetry.minimum_cash, state.money)
        self.telemetry.final_money = state.money

        hands = state.hands_positions
        total_workers = 1 + len(hands)
        self.telemetry.peak_simultaneous_workers = max(
            self.telemetry.peak_simultaneous_workers, total_workers
        )
        self.telemetry.worker_hours += total_workers

        self._record_diagnostics(state)

        raw_quads = state.my_farm.get("unlocked_quadrants", 1)
        owned_quadrants = len(raw_quads) if isinstance(raw_quads, list) else int(raw_quads)
        self.owned_quadrants = max(self.owned_quadrants, owned_quadrants)

        # Define EPU Tile Partitions (B3 Fixed 3x3 Strip Layout)
        farmer_tiles = [(0, 0), (0, 1), (0, 2), (1, 0)]
        hand1_tiles = [(1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        hand2_tiles = [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)]
        hand3_tiles = [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)]

        builder = ActionBuilder()

        # 1. Market Phase: Sell ANY harvested crops in shed immediately on every step
        for crop_name in CROPS.keys():
            shed_count = state.get_shed_count(crop_name)
            if shed_count > 0:
                builder.sell(crop_name, shed_count)
                price = state.get_price(crop_name)
                unit_price = price if price > 0 else CROPS[crop_name]["seed"] * 1.75
                self.telemetry.realized_revenue[crop_name] = self.telemetry.realized_revenue.get(crop_name, 0.0) + (shed_count * unit_price)

        # 2. Derived Dynamic Land Expansion Trigger (Requires Realized EPU1 Production Revenue > 0)
        cumulative_realized_revenue = sum(self.telemetry.realized_revenue.values())
        if self.config.enable_land_expansion and self.config.epu_level >= 2 and owned_quadrants < 2 and state.day >= 1:
            land_cost = 1000.0
            
            # E06 startup crop is TOMATO ($50 seed price)
            startup_seed_price = CROPS["TOMATO"]["seed"]
            
            # Total seeds currently owned in inventory/shed
            current_seeds = sum(state.get_seed_count(c) for c in CROPS.keys()) + sum(state.get_shed_count(c) for c in CROPS.keys())
            
            # Dynamic actual startup capital calculation for EPU2 and EPU3 taking inventory into account
            epu2_seeds_needed = max(0, 9 - current_seeds)
            epu2_actual_startup = epu2_seeds_needed * startup_seed_price
            
            rem_inventory = max(0, current_seeds - 9)
            epu3_seeds_needed = max(0, 9 - rem_inventory) if self.config.epu_level >= 3 else 0
            epu3_actual_startup = epu3_seeds_needed * startup_seed_price
            
            protected_startup = epu2_actual_startup + epu3_actual_startup
            operating_reserve = self.config.operating_reserve  # $300.00
            
            required_cash_for_q1 = land_cost + protected_startup + operating_reserve
            
            # Key Gate: LAND CAN ONLY BE BOUGHT POST-SURPLUS (after realized EPU1 revenue > 0)
            if state.hour == 0 and cumulative_realized_revenue > 0.0 and state.money >= required_cash_for_q1:
                builder.buy_land()
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_quadrants = 2
                self.owned_quadrants = 2
                self.telemetry.buy_land_executed_step = state.step
                setattr(self.telemetry, "buy_land_day", state.day)
                setattr(self.telemetry, "actual_trigger_value", required_cash_for_q1)
                self.telemetry.log_event("BUY_LAND", state.step, state.day, state.hour, state.money, f"Bought Q1 Land for EPU2/3 Post-Surplus (Rev: ${cumulative_realized_revenue:.2f}, Trigger: ${required_cash_for_q1:.2f})")

        # 3. Workload-driven Daily HIRE Trigger
        target_hands = 1  # 1 Hand for EPU1 (2 workers total)
        if self.config.epu_level >= 2 and owned_quadrants >= 2:
            target_hands = 2  # 2 Hands for EPU1+EPU2 (3 workers total)
        if self.config.epu_level >= 3 and owned_quadrants >= 2:
            target_hands = 3  # 3 Hands for EPU1+EPU2+EPU3 (4 workers total in Q0+Q1)

        current_hands = len(hands)
        hires_needed = max(0, target_hands - current_hands - state.hires_today)

        if state.hour == 0 and hires_needed > 0:
            hire_cap = 1 if self.config.multi_hire_mode == "SINGLE_PER_DAY" else hires_needed
            for _ in range(min(hires_needed, hire_cap)):
                if state.money >= 1.0:
                    builder.hire()
                    self.telemetry.spending_workforce += 1.0
                    self.telemetry.hires_count += 1
                    hand_idx = current_hands + 1
                    if hand_idx == 2:
                        setattr(self.telemetry, "epu2_activation_day", state.day)
                    elif hand_idx == 3:
                        setattr(self.telemetry, "epu3_activation_day", state.day)
                    self.telemetry.log_event("HIRE", state.step, state.day, state.hour, state.money, f"Hired Hand ({hand_idx})")

        # 4. Dynamic ROI Crop Selection & On-Demand Seed Buying across active EPUs
        active_managed_tiles = list(farmer_tiles) + list(hand1_tiles)
        if self.config.epu_level >= 2 and owned_quadrants >= 2:
            active_managed_tiles.extend(hand2_tiles)
        if self.config.epu_level >= 3 and owned_quadrants >= 2:
            active_managed_tiles.extend(hand3_tiles)

        # Telemetry: calculate active productive tiles and full 27 activation time
        active_planted_count = sum(
            1 for pos in active_managed_tiles
            if state.get_tile(pos[0], pos[1]) is not None and isinstance(state.get_tile(pos[0], pos[1]), dict) and state.get_tile(pos[0], pos[1]).get("kind") == "PLANT"
        )
        self.telemetry.peak_productive_tiles = max(self.telemetry.peak_productive_tiles, active_planted_count)
        if active_planted_count >= 27 and getattr(self.telemetry, "full_27_tiles_day", None) is None:
            setattr(self.telemetry, "full_27_tiles_step", state.step)
            setattr(self.telemetry, "full_27_tiles_day", state.day)
            buy_day = getattr(self.telemetry, "buy_land_day", None)
            if buy_day is not None:
                setattr(self.telemetry, "time_to_full_27_tiles_days", state.day - buy_day)

        cash = state.money
        target_crop = self.select_best_crop_roi(state, cash)
        target_crop_info = CROPS[target_crop]
        target_seed_cost = target_crop_info["seed"]

        all_empty_tiles: List[Tuple[int, int]] = []
        for pos in active_managed_tiles:
            tile = state.get_tile(pos[0], pos[1])
            if tile is None:
                all_empty_tiles.append(pos)

        target_seeds_owned = state.get_seed_count(target_crop)
        needed_seeds = max(0, len(all_empty_tiles) - target_seeds_owned)

        if needed_seeds > 0 and cash >= target_seed_cost:
            buy_qty = min(needed_seeds, int(cash // target_seed_cost))
            if buy_qty > 0:
                builder.buy_seed(target_crop, buy_qty)
                self.telemetry.spending_seeds += buy_qty * target_seed_cost
                target_seeds_owned += buy_qty

        virtual_seeds: Dict[str, int] = {
            crop: state.get_seed_count(crop) for crop in CROPS.keys()
        }
        virtual_seeds[target_crop] = target_seeds_owned

        # 5. Compute Worker Actions per EPU Spatial Partition
        farmer_pos = state.farmer_position
        farmer_act, _ = self._compute_e06_worker_action(
            farmer_pos, farmer_tiles, target_crop, target_seed_cost, virtual_seeds, state
        )
        self._apply_builder_action(builder, farmer_act, is_farmer=True)

        if len(hands) >= 1:
            hand1_pos = hands[0]
            hand1_act, _ = self._compute_e06_worker_action(
                hand1_pos, hand1_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand1_act)

        if len(hands) >= 2 and self.config.epu_level >= 2 and owned_quadrants >= 2:
            hand2_pos = hands[1]
            hand2_act, _ = self._compute_e06_worker_action(
                hand2_pos, hand2_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand2_act)

        if len(hands) >= 3 and self.config.epu_level >= 3 and owned_quadrants >= 2:
            hand3_pos = hands[2]
            hand3_act, _ = self._compute_e06_worker_action(
                hand3_pos, hand3_tiles, target_crop, target_seed_cost, virtual_seeds, state
            )
            builder.add_hand_action(hand3_act)

        return builder.build()

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

    def select_best_crop_roi(self, state: GameState, cash: float) -> str:
        """Select affordable crop with the highest net profit per day."""
        best_crop = self.config.liquidity_crop
        best_profit_per_day = -9999.0

        for crop_name, crop_info in CROPS.items():
            seed_cost = crop_info["seed"]
            if cash >= seed_cost:
                profit_per_day = self.calculate_net_profit_per_day(crop_name, state)
                if profit_per_day > best_profit_per_day:
                    best_profit_per_day = profit_per_day
                    best_crop = crop_name

        return best_crop

    def _compute_e06_worker_action(
        self,
        curr_pos: Tuple[int, int],
        assigned_tiles: List[Tuple[int, int]],
        target_crop: str,
        target_seed_cost: float,
        virtual_seeds: Dict[str, int],
        state: GameState,
        worker_id: int = 0,
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

        # Priority WATER > HARVEST > PLANT
        if water_candidate_tiles:
            target_pos = select_nearest(water_candidate_tiles)
            task = "WATER"
        elif harvest_candidate_tiles:
            target_pos = select_nearest(harvest_candidate_tiles)
            task = "HARVEST"
        elif empty_tiles and (sum(virtual_seeds.values()) > 0 or any(state.get_seed_count(c) > 0 for c in CROPS.keys())):
            target_pos = select_nearest(empty_tiles)
            task = "PLANT"

        if target_pos is None:
            return ["PASS"], None
        elif target_pos == curr_pos:
            if task == "WATER":
                self.telemetry.crops_watered += 1
                return ["WATER"], None
            elif task == "HARVEST":
                self.telemetry.crops_harvested += 1
                return ["HARVEST"], None
            elif task == "PLANT":
                plant_crop = self._select_crop_to_plant(state, state.day, target_pos, virtual_seeds)
                if virtual_seeds.get(plant_crop, 0) > 0:
                    virtual_seeds[plant_crop] -= 1
                    self.telemetry.crops_planted += 1
                    return ["PLANT", plant_crop], plant_crop
                elif target_seeds_owned > 0:
                    virtual_seeds[target_crop] -= 1
                    self.telemetry.crops_planted += 1
                    return ["PLANT", target_crop], target_crop
                else:
                    for alt_crop in CROPS.keys():
                        if virtual_seeds.get(alt_crop, 0) > 0 or state.get_seed_count(alt_crop) > 0:
                            if virtual_seeds.get(alt_crop, 0) > 0:
                                virtual_seeds[alt_crop] -= 1
                            self.telemetry.crops_planted += 1
                            return ["PLANT", alt_crop], alt_crop
                    return ["PASS"], None
            else:
                return ["PASS"], None
        else:
            step_dir = self._get_step_direction(curr_pos, target_pos)
            if step_dir != "PASS":
                return [step_dir], None
            return ["PASS"], None

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

# --- Kaggle Entrypoint ---
_config = ProductiveMassConfig(
    productive_core_mode="E12_TRUEBELIEF_ENGINE_X112",
    enable_land_expansion=True,
    target_cows=7,
    target_sheep=4,
    max_workers=6,
    stop_hire_day=1,
)
_agent_instance = ProductiveMassROIAgent(config=_config)

def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point for E12-X1.12 baseline candidate."""
    try:
        state = GameState(observation)
        return _agent_instance.act(state)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
