"""E09-01 Controlled Livestock Ablation Strategy (40 tiles, Livestock OFF)."""

from typing import Dict, Any, List, Tuple, Set, Optional
from agricola.core.state import GameState, CROPS
from agricola.core.actions import ActionBuilder
from agricola.strategy.hybrid_livestock_cluster_roi import CompetitiveConfig, TelemetryLogger


class LivestockAblationROIAgent:
    """E09-01 Livestock Subsystem Ablation Agent (40 tiles, Livestock OFF).
    
    Controlled single-variable ablation of E08 (HybridLivestockClusterROIAgent):
    - Footprint: Preserved at 40 target productive crop tiles (20 Q0 + 20 Q1).
    - Workforce: Preserved at 4 workers (1 Farmer + 3 Hands, hired at Day 1, 6, 12).
    - Land Expansion: Preserved at Day 12 BUY_LAND Q1 ($1,000).
    - Task Priority: Preserved at Water-First priority (WATER > HARVEST > PLANT).
    - Spatial Partitioning & Cross-Boundary Water Assist: Preserved from E08.
    
    ABLATED (DISABLED):
    - 0 animal purchases (target_cows=0, target_sheep=0).
    - 0 pasture construction (BUILD_PASTURE disabled).
    - 0 animal placement (PLACE COW/SHEEP disabled).
    - 0 animal feeding (FEED disabled, wheat_fed=0).
    - 0 feed safety buffer (feed_safety_buffer=0).
    - 0 livestock harvest (Milk/Wool harvesting disabled).
    - 0 livestock sales (Milk/Wool sales disabled).
    """

    def __init__(self, config: Optional[CompetitiveConfig] = None):
        self.name = "LivestockAblationROIAgent"
        self.config: CompetitiveConfig = config if config is not None else CompetitiveConfig()
        
        # Override config for controlled livestock ablation
        self.config.target_cows = 0
        self.config.target_sheep = 0
        self.config.feed_safety_buffer = 0
        
        self.telemetry: TelemetryLogger = TelemetryLogger()
        self.telemetry.configured_crop_tiles_count = self.config.target_productive_tiles
        
        self.current_phase: str = "OPENING"
        self.owned_quadrants: int = 1
        
        # --- Pastures Ablated (0 pasture tiles) ---
        self.pasture_tiles_cow: List[Tuple[int, int]] = []
        self.pasture_tiles_sheep: List[Tuple[int, int]] = []
        
        # --- Quadrant 0 Crop Tiles (20 tiles: preserved from E08) ---
        self.q0_wheat_tiles: List[Tuple[int, int]] = [(1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2)]  # 6 Wheat
        self.q0_melon_tiles: List[Tuple[int, int]] = [(2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0)]  # 8 Melon
        self.q0_carrot_tiles: List[Tuple[int, int]] = [(4, 1), (4, 2), (4, 3), (4, 4), (0, 3), (0, 4)]  # 6 Carrot
        self.q0_crop_tiles: List[Tuple[int, int]] = self.q0_wheat_tiles + self.q0_melon_tiles + self.q0_carrot_tiles
        
        # --- Quadrant 1 Crop Tiles (20 tiles: preserved from E08) ---
        self.q1_melon_tiles: List[Tuple[int, int]] = [
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4),
            (7, 0), (7, 1), (7, 2), (7, 3)
        ]  # 14 Melon
        self.q1_carrot_tiles: List[Tuple[int, int]] = [(7, 4), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4)]  # 6 Carrot
        self.q1_crop_tiles: List[Tuple[int, int]] = self.q1_melon_tiles + self.q1_carrot_tiles

    def act(self, game_state: GameState) -> Dict[str, Any]:
        """Kaggle environment entrypoint method."""
        return self.decide(game_state)

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
        
        # Diagnostics: track active productive crop tiles & backlog
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
        
        # Hiring logic (4 workers total: Hand 1 Day 1, Hand 2 Day 6, Hand 3 Day 12)
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
                
        # Land Expansion logic (Q1 Day 12, $1,000)
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

        # LIVESTOCK PURCHASES ABLATED (0 animal buys)
        # Seed Purchases
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
        
        # Spatial Partitioning (Identical to E08):
        # Worker 0 (Farmer): Q0 ($x <= 4), role "FARMER"
        # Worker 1 (Hand 1): Q0 ($x <= 4), role "Q0_CROPS" (LIVESTOCK role ablated to Q0_CROPS)
        # Worker 2 (Hand 2): Q1 ($x >= 5) if owned else Q0, role "Q1_CROPS"
        # Worker 3 (Hand 3): Q1 ($x >= 5) if owned else Q0, role "Q1_CROPS"
        
        farmer_pos = state.farmer_position
        farmer_act = self._get_worker_action(state, farmer_pos, reserved_tiles, worker_id=0, role="FARMER")
        self._apply_builder_action(builder, farmer_act, is_farmer=True)
        
        if len(hands) >= 1:
            h1_act = self._get_worker_action(state, hands[0], reserved_tiles, worker_id=1, role="Q0_CROPS")
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

        # --- A. LIVESTOCK ACTIONS ABLATED ---
        # No pasture building, no animal placement, no animal feeding, no product harvesting/dropping.

        # --- B. CROP ROLE TASKS & SPATIAL PARTITIONING (Identical to E08) ---
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

        # --- CROSS-BOUNDARY WATER ASSIST OVERRIDE (Identical to E08) ---
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

        # --- Priority 2: HARVEST mature crops (Identical to E08) ---
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

        # --- Priority 3: PLANT empty tiles (Identical to E08) ---
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
        elif cmd in ("NORTH", "SOUTH", "EAST", "WEST"):
            builder.move(cmd)
        else:
            builder.pass_turn()

    def _process_sales(self, state: GameState, builder: ActionBuilder):
        shed = state.shed
        orders_placed = 0
        max_orders = 10
        
        is_flush_phase = (state.day >= self.config.inventory_flush_start_day)
        
        # Milk and Wool sales ablated (0 produced, 0 sold)

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
        # Feed safety buffer is 0; all Wheat available for market sale
        if wheat_cnt > self.config.feed_safety_buffer and orders_placed < max_orders:
            sell_qty = wheat_cnt if is_flush_phase else (wheat_cnt - self.config.feed_safety_buffer)
            builder.sell("WHEAT", sell_qty)
            orders_placed += 1
            self.telemetry.quantities_sold["WHEAT"] += sell_qty
            self.telemetry.realized_revenue["WHEAT"] += sell_qty * 25.0

        self.telemetry.market_orders_placed += orders_placed
        self.telemetry.unsold_shed_items = sum(shed.values())
