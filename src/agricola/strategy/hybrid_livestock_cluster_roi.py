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
from typing import Dict, Any, List, Set, Tuple, Optional
import math

from agricola.core.state import GameState, CROPS
from agricola.core.actions import ActionBuilder


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


class HybridLivestockClusterROIAgent:
    """E08 Configurable Productive Scale Agent."""

    def __init__(self, config: Optional[CompetitiveConfig] = None):
        self.name = "HybridLivestockClusterROIAgent"
        self.config: CompetitiveConfig = config if config is not None else CompetitiveConfig()
        self.telemetry: TelemetryLogger = TelemetryLogger()
        self.telemetry.configured_crop_tiles_count = self.config.target_productive_tiles
        
        self.current_phase: str = "OPENING"
        self.owned_quadrants: int = 1
        
        # --- Pasture Tiles (5 tiles in Q0) ---
        self.pasture_tiles_cow: List[Tuple[int, int]] = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.pasture_tiles_sheep: List[Tuple[int, int]] = [(0, 2)]
        
        # --- Quadrant 0 Crop Tiles (20 tiles: x in [0..4], y in [0..4] excluding pastures) ---
        self.q0_wheat_tiles: List[Tuple[int, int]] = [(1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2)] # 6 Wheat
        self.q0_melon_tiles: List[Tuple[int, int]] = [(2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0)] # 8 Melon
        self.q0_carrot_tiles: List[Tuple[int, int]] = [(4, 1), (4, 2), (4, 3), (4, 4), (0, 3), (0, 4)] # 6 Carrot
        self.q0_crop_tiles: List[Tuple[int, int]] = self.q0_wheat_tiles + self.q0_melon_tiles + self.q0_carrot_tiles
        
        # --- Quadrant 1 Crop Tiles (20 tiles: x in [5..8], y in [0..4]) ---
        self.q1_melon_tiles: List[Tuple[int, int]] = [
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4),
            (7, 0), (7, 1), (7, 2), (7, 3)
        ] # 14 Melon
        self.q1_carrot_tiles: List[Tuple[int, int]] = [(7, 4), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4)] # 6 Carrot
        self.q1_crop_tiles: List[Tuple[int, int]] = self.q1_melon_tiles + self.q1_carrot_tiles

    def decide(self, game_state: GameState) -> Dict[str, Any]:
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
        
        # Diagnostics: track active productive tiles & backlog
        self._record_diagnostics(game_state)
        
        self._update_phase(game_state)
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
        
        available_crop_tiles = list(self.q0_crop_tiles)
        if self.owned_quadrants >= 2:
            available_crop_tiles.extend(self.q1_crop_tiles)
            
        for (tx, ty) in available_crop_tiles:
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
            new_phase = "OPENING"
        elif day < 16:
            new_phase = "SCALE"
        elif day < self.config.inventory_flush_start_day:
            new_phase = "PRODUCE"
        else:
            new_phase = "LIQUIDATE"
            
        if new_phase != old_phase:
            self.telemetry.log_phase_change(
                state.step, state.day, state.hour, old_phase, new_phase, state.money
            )
            self.current_phase = new_phase

    def _process_market_decisions(self, state: GameState, builder: ActionBuilder, current_workers: int):
        day = state.day
        hour = state.hour
        cash = state.money
        reserve = self.config.cash_reserve
        
        if day >= 12:
            target_hands = 3
        elif day >= 6:
            target_hands = 2
        elif day >= 1:
            target_hands = 1
        else:
            target_hands = 0
            
        hires_needed = target_hands - state.hires_today
        if hour == 0 and hires_needed > 0:
            current_hires = state.hires_today
            fibs = [1, 1, 2, 3, 5, 8]
            for _ in range(hires_needed):
                hire_cost = float(fibs[min(current_hires, len(fibs) - 1)])
                if cash - hire_cost >= self.config.minimum_cash_after_hire:
                    builder.hire()
                    self.telemetry.spending_workforce += hire_cost
                    self.telemetry.hires_count += 1
                    self.telemetry.hire_attempted += 1
                    self.telemetry.hire_accepted += 1
                    self.telemetry.log_event("HIRE", state.step, day, hour, cash, f"Hired Hand (Total today: {current_hires + 1})")
                    current_hires += 1
                    cash -= hire_cost
                else:
                    break
                
        if day >= self.config.expansion_day and self.owned_quadrants < self.config.target_quadrants:
            land_cost = 1000.0
            if cash - land_cost >= reserve:
                builder.buy_land()
                self.owned_quadrants = 2
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_tiles_count = 50
                self.telemetry.q1_owned = 25
                self.telemetry.q1_productive = len(self.q1_crop_tiles)
                self.telemetry.buy_land_executed_step = state.step
                self.telemetry.log_event("BUY_LAND", state.step, day, hour, cash, "Bought Q1 (50 tiles total)")
                cash -= land_cost

        # Livestock Purchase Decisions (Guarded by $1500 cash float, shed space < 95, and Day 6+)
        cows_in_shed = state.get_shed_count("COW")
        cows_in_inv = sum(state.get_worker_inventory_count(w, "COW") for w in range(4))
        cows_placed = sum(
            1 for y in range(len(state.tiles)) for x in range(len(state.tiles[y]))
            if isinstance(state.tiles[y][x], dict) and state.tiles[y][x].get("animal") == "COW"
        )
        cows_owned = cows_in_shed + cows_in_inv + cows_placed
        self.telemetry.cows_acquired = cows_owned
        
        sheep_in_shed = state.get_shed_count("SHEEP")
        sheep_in_inv = sum(state.get_worker_inventory_count(w, "SHEEP") for w in range(4))
        sheep_placed = sum(
            1 for y in range(len(state.tiles)) for x in range(len(state.tiles[y]))
            if isinstance(state.tiles[y][x], dict) and state.tiles[y][x].get("animal") == "SHEEP"
        )
        sheep_owned = sheep_in_shed + sheep_in_inv + sheep_placed
        self.telemetry.sheep_acquired = sheep_owned
        
        shed_total = sum(state.shed.values())
        has_shed_space = (shed_total <= 95)
        
        wheat_in_shed = state.get_shed_count("WHEAT")
        wheat_seeds = state.get_seed_count("WHEAT")
        total_wheat_supply = wheat_in_shed + wheat_seeds + 6
        animal_count = cows_owned + sheep_owned
        feed_demand = animal_count + 1
        
        has_feed_buffer = (total_wheat_supply >= feed_demand + self.config.feed_safety_buffer)
        
        if day >= 6 and cash >= 1500.0 and has_feed_buffer and has_shed_space:
            # Buy Cows ($400)
            if cows_owned < self.config.target_cows and day <= self.config.stop_cow_buy_day:
                cow_cost = 400.0
                if cash - cow_cost >= reserve:
                    builder.buy_animal("COW", 1)
                    self.telemetry.spending_livestock += cow_cost
                    self.telemetry.log_event("BUY_ANIMAL", state.step, day, hour, cash, "Bought COW")
                    cash -= cow_cost
            
            # Buy Sheep ($500)
            elif sheep_owned < self.config.target_sheep and day <= self.config.stop_sheep_buy_day:
                sheep_cost = 500.0
                if cash - sheep_cost >= reserve:
                    builder.buy_animal("SHEEP", 1)
                    self.telemetry.spending_livestock += sheep_cost
                    self.telemetry.log_event("BUY_ANIMAL", state.step, day, hour, cash, "Bought SHEEP")
                    cash -= sheep_cost

        self._buy_seeds_if_needed(state, builder, cash, reserve)

    def _buy_seeds_if_needed(self, state: GameState, builder: ActionBuilder, cash: float, reserve: float):
        day = state.day
        if day > self.config.all_plant_cutoff_day:
            return
            
        # Staggered Seed Purchasing respecting $300 cash floor
        if state.get_seed_count("WHEAT") < 4 and cash - 10.0 >= reserve:
            builder.buy_seed("WHEAT", 6)
            self.telemetry.spending_seeds += 60.0
            self.telemetry.wheat_bought += 6
            cash -= 60.0
            
        if state.get_seed_count("CARROT") < 4 and cash - 20.0 >= reserve:
            builder.buy_seed("CARROT", 6)
            self.telemetry.spending_seeds += 120.0
            cash -= 120.0

        if day <= self.config.melon_plant_cutoff_day and state.get_seed_count("MELON") < 4 and cash - 80.0 >= reserve:
            builder.buy_seed("MELON", 4)
            self.telemetry.spending_seeds += 320.0
            cash -= 320.0

    def _dispatch_worker_actions(self, state: GameState, builder: ActionBuilder, hands: List[Tuple[int, int]]):
        reserved_tiles: Set[Tuple[int, int]] = set()
        
        # Spatial Partitioning:
        # Worker 0 (Farmer): Q0 ($x <= 4), role "FARMER"
        # Worker 1 (Hand 1): Q0 ($x <= 4), role "LIVESTOCK" / Q0 crops
        # Worker 2 (Hand 2): Q1 ($x >= 5) if owned else Q0, role "Q1_CROPS"
        # Worker 3 (Hand 3): Q1 ($x >= 5) if owned else Q0, role "Q1_CROPS"
        
        farmer_pos = state.farmer_position
        farmer_act = self._get_worker_action(state, farmer_pos, reserved_tiles, worker_id=0, role="FARMER")
        self._apply_builder_action(builder, farmer_act, is_farmer=True)
        
        if len(hands) >= 1:
            h1_act = self._get_worker_action(state, hands[0], reserved_tiles, worker_id=1, role="LIVESTOCK")
            builder.add_hand_action(h1_act)
            
        if len(hands) >= 2:
            h2_role = "Q1_CROPS" if self.owned_quadrants >= 2 else "Q0_CROPS"
            h2_act = self._get_worker_action(state, hands[1], reserved_tiles, worker_id=2, role=h2_role)
            builder.add_hand_action(h2_act)

        if len(hands) >= 3:
            h3_role = "Q1_CROPS" if self.owned_quadrants >= 2 else "Q0_CROPS"
            h3_act = self._get_worker_action(state, hands[2], reserved_tiles, worker_id=3, role=h3_role)
            builder.add_hand_action(h3_act)

    def _get_worker_action(
        self, state: GameState, pos: Tuple[int, int], reserved: Set[Tuple[int, int]], worker_id: int, role: str
    ) -> List[str]:
        px, py = pos
        day = state.day
        shed = state.shed
        all_pastures = self.pasture_tiles_cow + self.pasture_tiles_sheep
        shed_access_tile = (4, 4)

        # --- A. FARMER EXCLUSIVE: PASTURE BUILDING & ANIMAL PLACEMENT ---
        if role == "FARMER":
            farmer_inv_cow = state.get_worker_inventory_count(0, "COW")
            cows_in_shed = shed.get("COW", 0)
            
            if farmer_inv_cow > 0:
                for (tx, ty) in self.pasture_tiles_cow:
                    if (tx, ty) in reserved:
                        continue
                    tile = state.get_tile(tx, ty)
                    if tile is None:
                        reserved.add((tx, ty))
                        dist = abs(px - tx) + abs(py - ty)
                        if dist == 0:
                            self.telemetry.pastures_built += 1
                            self.telemetry.record_worker_step(worker_id, "productive")
                            return ["BUILD_PASTURE"]
                        self.telemetry.record_worker_step(worker_id, "movement")
                        return self._move_towards(px, py, (tx, ty))
                    elif isinstance(tile, dict) and tile.get("kind") == "PASTURE" and "animal" not in tile:
                        reserved.add((tx, ty))
                        dist = abs(px - tx) + abs(py - ty)
                        if dist == 0:
                            self.telemetry.animals_placed += 1
                            self.telemetry.record_worker_step(worker_id, "productive")
                            return ["PLACE", "COW"]
                        self.telemetry.record_worker_step(worker_id, "movement")
                        return self._move_towards(px, py, (tx, ty))
            elif cows_in_shed > 0:
                dist = abs(px - shed_access_tile[0]) + abs(py - shed_access_tile[1])
                if dist == 0:
                    self.telemetry.record_worker_step(worker_id, "productive")
                    return ["PICKUP", "COW", 1]
                self.telemetry.record_worker_step(worker_id, "movement")
                return self._move_towards(px, py, shed_access_tile)

            # Check Sheep placement
            sheep_in_inv = state.get_worker_inventory_count(0, "SHEEP")
            sheep_in_shed = shed.get("SHEEP", 0)
            
            if sheep_in_inv > 0:
                for (tx, ty) in self.pasture_tiles_sheep:
                    if (tx, ty) in reserved:
                        continue
                    tile = state.get_tile(tx, ty)
                    if tile is None:
                        reserved.add((tx, ty))
                        dist = abs(px - tx) + abs(py - ty)
                        if dist == 0:
                            self.telemetry.pastures_built += 1
                            self.telemetry.record_worker_step(worker_id, "productive")
                            return ["BUILD_PASTURE"]
                        self.telemetry.record_worker_step(worker_id, "movement")
                        return self._move_towards(px, py, (tx, ty))
                    elif isinstance(tile, dict) and tile.get("kind") == "PASTURE" and "animal" not in tile:
                        reserved.add((tx, ty))
                        dist = abs(px - tx) + abs(py - ty)
                        if dist == 0:
                            self.telemetry.animals_placed += 1
                            self.telemetry.record_worker_step(worker_id, "productive")
                            return ["PLACE", "SHEEP"]
                        self.telemetry.record_worker_step(worker_id, "movement")
                        return self._move_towards(px, py, (tx, ty))
            elif sheep_in_shed > 0:
                dist = abs(px - shed_access_tile[0]) + abs(py - shed_access_tile[1])
                if dist == 0:
                    self.telemetry.record_worker_step(worker_id, "productive")
                    return ["PICKUP", "SHEEP", 1]
                self.telemetry.record_worker_step(worker_id, "movement")
                return self._move_towards(px, py, shed_access_tile)

        # --- B. ANIMAL FEEDING & PRODUCT HARVEST (Farmer or Livestock Hand) ---
        if role in ("FARMER", "LIVESTOCK"):
            # Check if any placed animal needs feeding
            unfed_pastures = []
            for (tx, ty) in all_pastures:
                tile = state.get_tile(tx, ty)
                if isinstance(tile, dict) and "animal" in tile and not tile.get("fed_today", False):
                    unfed_pastures.append((tx, ty))

            if unfed_pastures:
                worker_inv_wheat = state.get_worker_inventory_count(worker_id, "WHEAT")
                wheat_in_shed = shed.get("WHEAT", 0)
                
                if worker_inv_wheat > 0:
                    unfed_candidates = []
                    for (tx, ty) in unfed_pastures:
                        if (tx, ty) in reserved:
                            continue
                        dist = abs(px - tx) + abs(py - ty)
                        unfed_candidates.append((dist, (tx, ty)))
                    if unfed_candidates:
                        unfed_candidates.sort(key=lambda x: x[0])
                        best_dist, best_tile = unfed_candidates[0]
                        reserved.add(best_tile)
                        if best_dist == 0:
                            self.telemetry.feed_attempted += 1
                            self.telemetry.feed_successful += 1
                            self.telemetry.feed_consumed += 1
                            self.telemetry.wheat_fed += 1
                            self.telemetry.record_worker_step(worker_id, "productive")
                            return ["FEED"]
                        else:
                            self.telemetry.record_worker_step(worker_id, "movement")
                            return self._move_towards(px, py, best_tile)
                elif wheat_in_shed > 0:
                    dist = abs(px - shed_access_tile[0]) + abs(py - shed_access_tile[1])
                    if dist == 0:
                        pickup_qty = min(5, wheat_in_shed)
                        self.telemetry.record_worker_step(worker_id, "productive")
                        return ["PICKUP", "WHEAT", pickup_qty]
                    else:
                        self.telemetry.record_worker_step(worker_id, "movement")
                        return self._move_towards(px, py, shed_access_tile)

            # Check if any animal has Milk/Wool yield to HARVEST
            harvest_pastures = []
            for (tx, ty) in all_pastures:
                if (tx, ty) in reserved:
                    continue
                tile = state.get_tile(tx, ty)
                if isinstance(tile, dict) and "animal" in tile and tile.get("yield_units", 0) > 0:
                    harvest_pastures.append((tx, ty))

            if harvest_pastures:
                harvest_candidates = []
                for (tx, ty) in harvest_pastures:
                    dist = abs(px - tx) + abs(py - ty)
                    harvest_candidates.append((dist, (tx, ty)))
                harvest_candidates.sort(key=lambda x: x[0])
                best_dist, best_tile = harvest_candidates[0]
                reserved.add(best_tile)
                if best_dist == 0:
                    tile = state.get_tile(best_tile[0], best_tile[1])
                    animal_type = tile.get("animal")
                    units = tile.get("yield_units", 1)
                    if animal_type == "COW":
                        self.telemetry.milk_harvested += units
                    elif animal_type == "SHEEP":
                        self.telemetry.wool_harvested += units
                    self.telemetry.record_worker_step(worker_id, "productive")
                    return ["HARVEST"]
                else:
                    self.telemetry.record_worker_step(worker_id, "movement")
                    return self._move_towards(px, py, best_tile)

            # Check if worker inventory has MILK or WOOL to DROP into shed
            worker_milk = state.get_worker_inventory_count(worker_id, "MILK")
            worker_wool = state.get_worker_inventory_count(worker_id, "WOOL")
            if worker_milk > 0 or worker_wool > 0:
                dist = abs(px - shed_access_tile[0]) + abs(py - shed_access_tile[1])
                if dist == 0:
                    self.telemetry.record_worker_step(worker_id, "productive")
                    return ["DROP"]
                else:
                    self.telemetry.record_worker_step(worker_id, "movement")
                    return self._move_towards(px, py, shed_access_tile)

        # --- C. CROP ROLE TASKS & SPATIAL PARTITIONING ---
        if role == "Q1_CROPS" and self.owned_quadrants >= 2:
            target_crop_tiles = list(self.q1_crop_tiles)
            other_crop_tiles = list(self.q0_crop_tiles)
        else:
            target_crop_tiles = list(self.q0_crop_tiles)
            other_crop_tiles = list(self.q1_crop_tiles) if self.owned_quadrants >= 2 else []

        # --- Priority 1: WATER dry crops (Water-First priority) ---
        water_candidates = []
        for (tx, ty) in target_crop_tiles:
            if (tx, ty) in reserved:
                continue
            tile = state.get_tile(tx, ty)
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                if not tile.get("watered_today", False):
                    dist = abs(px - tx) + abs(py - ty)
                    water_candidates.append((dist, (tx, ty)))
                    
        if water_candidates:
            water_candidates.sort(key=lambda item: item[0])
            best_dist, best_tile = water_candidates[0]
            reserved.add(best_tile)
            if best_tile[0] >= 5:
                self.telemetry.q1_worked += 1
            else:
                self.telemetry.q0_worked += 1
                
            if best_dist == 0:
                self.telemetry.crops_watered += 1
                self.telemetry.record_worker_step(worker_id, "productive")
                return ["WATER"]
            else:
                self.telemetry.record_worker_step(worker_id, "movement")
                return self._move_towards(px, py, best_tile)

        # --- CROSS-BOUNDARY WATER ASSIST OVERRIDE ---
        # If assigned quadrant has 0 WATER tasks, check if opposite quadrant has dry crops needing water!
        if self.config.cross_boundary_water_assist and other_crop_tiles:
            cross_water_candidates = []
            for (tx, ty) in other_crop_tiles:
                if (tx, ty) in reserved:
                    continue
                tile = state.get_tile(tx, ty)
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    if not tile.get("watered_today", False):
                        dist = abs(px - tx) + abs(py - ty)
                        cross_water_candidates.append((dist, (tx, ty)))
                        
            if cross_water_candidates:
                cross_water_candidates.sort(key=lambda item: item[0])
                best_dist, best_tile = cross_water_candidates[0]
                reserved.add(best_tile)
                if best_tile[0] >= 5:
                    self.telemetry.q1_worked += 1
                else:
                    self.telemetry.q0_worked += 1
                    
                if best_dist == 0:
                    self.telemetry.crops_watered += 1
                    self.telemetry.record_worker_step(worker_id, "productive")
                    return ["WATER"]
                else:
                    self.telemetry.record_worker_step(worker_id, "movement")
                    return self._move_towards(px, py, best_tile)

        # --- Priority 2: HARVEST mature crops ---
        harvest_candidates = []
        for (tx, ty) in target_crop_tiles:
            if (tx, ty) in reserved:
                continue
            tile = state.get_tile(tx, ty)
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                crop_type = tile.get("crop", "WHEAT")
                crop_info = CROPS.get(crop_type, CROPS["WHEAT"])
                planted_d = tile.get("planted_day", day)
                age = day - planted_d
                max_yield_day = crop_info["max_yield_day"]
                if age >= max_yield_day:
                    dist = abs(px - tx) + abs(py - ty)
                    harvest_candidates.append((dist, (tx, ty)))

        if harvest_candidates:
            harvest_candidates.sort(key=lambda item: item[0])
            best_dist, best_tile = harvest_candidates[0]
            reserved.add(best_tile)
            if best_tile[0] >= 5:
                self.telemetry.q1_harvested += 1
            else:
                self.telemetry.q0_harvested += 1
                
            if best_dist == 0:
                tile = state.get_tile(best_tile[0], best_tile[1])
                if isinstance(tile, dict) and tile.get("crop") == "WHEAT":
                    units = tile.get("yield_units", 6)
                    self.telemetry.wheat_harvested += units
                self.telemetry.crops_harvested += 1
                self.telemetry.record_worker_step(worker_id, "productive")
                return ["HARVEST"]
            else:
                self.telemetry.record_worker_step(worker_id, "movement")
                return self._move_towards(px, py, best_tile)

        # --- Priority 3: PLANT empty tiles ---
        if day <= self.config.all_plant_cutoff_day:
            plant_candidates = []
            for (tx, ty) in target_crop_tiles:
                if (tx, ty) in reserved:
                    continue
                tile = state.get_tile(tx, ty)
                if tile is None or (isinstance(tile, dict) and tile.get("kind") == "WEED"):
                    dist = abs(px - tx) + abs(py - ty)
                    plant_candidates.append((dist, (tx, ty)))

            if plant_candidates:
                plant_candidates.sort(key=lambda item: item[0])
                best_dist, best_tile = plant_candidates[0]
                reserved.add(best_tile)
                if best_tile[0] >= 5:
                    self.telemetry.q1_worked += 1
                else:
                    self.telemetry.q0_worked += 1
                    
                if best_dist == 0:
                    current_t = state.get_tile(px, py)
                    if isinstance(current_t, dict) and current_t.get("kind") == "WEED":
                        self.telemetry.crops_weed_losses += 1
                        self.telemetry.record_worker_step(worker_id, "productive")
                        return ["DIG"]
                        
                    if best_tile in self.q0_wheat_tiles:
                        crop_to_plant = "WHEAT"
                    elif day <= self.config.melon_plant_cutoff_day and state.get_seed_count("MELON") > 0:
                        crop_to_plant = "MELON"
                    elif state.get_seed_count("CARROT") > 0:
                        crop_to_plant = "CARROT"
                    elif state.get_seed_count("WHEAT") > 0:
                        crop_to_plant = "WHEAT"
                    else:
                        crop_to_plant = "WHEAT"
                        
                    self.telemetry.crops_planted += 1
                    self.telemetry.record_worker_step(worker_id, "productive")
                    return ["PLANT", crop_to_plant]
                else:
                    self.telemetry.record_worker_step(worker_id, "movement")
                    return self._move_towards(px, py, best_tile)

        # Priority 4: Default IDLE / PASS
        self.telemetry.record_worker_step(worker_id, "idle")
        return ["PASS"]

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
        elif cmd == "PICKUP" and len(act) >= 2:
            qty = int(act[2]) if len(act) >= 3 else 1
            builder.pickup(act[1], qty)
        elif cmd == "FEED":
            builder.feed()
        elif cmd in ("NORTH", "SOUTH", "EAST", "WEST"):
            builder.move(cmd)
        else:
            builder.pass_turn()

    def _process_sales(self, state: GameState, builder: ActionBuilder):
        shed = state.shed
        orders_placed = 0
        max_orders = 10
        
        is_flush_phase = (state.day >= self.config.inventory_flush_start_day)
        
        milk_cnt = shed.get("MILK", 0)
        if milk_cnt > 0 and orders_placed < max_orders:
            sell_qty = milk_cnt if is_flush_phase else min(milk_cnt, max_orders - orders_placed)
            builder.sell("MILK", sell_qty)
            orders_placed += 1
            self.telemetry.quantities_sold["MILK"] += sell_qty
            self.telemetry.realized_revenue["MILK"] += sell_qty * 160.0

        wool_cnt = shed.get("WOOL", 0)
        if wool_cnt > 0 and orders_placed < max_orders:
            sell_qty = wool_cnt if is_flush_phase else min(wool_cnt, max_orders - orders_placed)
            builder.sell("WOOL", sell_qty)
            orders_placed += 1
            self.telemetry.quantities_sold["WOOL"] += sell_qty
            self.telemetry.realized_revenue["WOOL"] += sell_qty * 200.0

        melon_cnt = shed.get("MELON", 0)
        if melon_cnt > 0 and orders_placed < max_orders:
            sell_qty = melon_cnt if is_flush_phase else min(melon_cnt, max_orders - orders_placed)
            builder.sell("MELON", sell_qty)
            orders_placed += 1
            self.telemetry.quantities_sold["MELON"] += sell_qty
            self.telemetry.realized_revenue["MELON"] += sell_qty * 250.0

        carrot_cnt = shed.get("CARROT", 0)
        if carrot_cnt > 0 and orders_placed < max_orders:
            sell_qty = carrot_cnt if is_flush_phase else min(carrot_cnt, max_orders - orders_placed)
            builder.sell("CARROT", sell_qty)
            orders_placed += 1
            self.telemetry.quantities_sold["CARROT"] += sell_qty
            self.telemetry.realized_revenue["CARROT"] += sell_qty * 35.0

        wheat_cnt = shed.get("WHEAT", 0)
        if wheat_cnt > self.config.feed_safety_buffer and orders_placed < max_orders:
            sell_qty = wheat_cnt if is_flush_phase else (wheat_cnt - self.config.feed_safety_buffer)
            builder.sell("WHEAT", sell_qty)
            orders_placed += 1
            self.telemetry.quantities_sold["WHEAT"] += sell_qty
            self.telemetry.realized_revenue["WHEAT"] += sell_qty * 25.0

        self.telemetry.market_orders_placed += orders_placed
        self.telemetry.unsold_shed_items = sum(shed.values())
