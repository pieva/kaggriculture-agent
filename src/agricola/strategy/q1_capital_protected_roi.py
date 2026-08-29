"""E10-01 Q1 Expansion Capital Protection Strategy (40 tiles, Livestock OFF)."""

from typing import Dict, Any, List, Optional, Tuple, Set
from agricola.core.state import GameState, CROPS
from agricola.core.actions import ActionBuilder
from agricola.strategy.hybrid_livestock_cluster_roi import CompetitiveConfig, TelemetryLogger
from agricola.strategy.livestock_ablation_roi import LivestockAblationROIAgent


class Q1CapitalProtectedROIAgent(LivestockAblationROIAgent):
    """E10-01 Q1 Expansion Capital Protected Strategy.

    Inherits 100% of E09-01 invariants:
    - 40 target productive crop tiles (20 Q0 + 20 Q1)
    - Livestock OFF (0 animals, 0 pastures, 0 placement, 0 feed, 0 products)
    - 4 workers maximum (Farmer + 3 Hands hired at Day 1, 6, 12)
    - Water-First priority (WATER > HARVEST > PLANT)
    - Spatial worker partitioning & Cross-boundary water assist
    - Crop ratios: 22 Melon, 12 Carrot, 6 Wheat

    SINGLE EXPERIMENTAL VARIABLE CHANGE (E09 -> E10):
    - Q1 Expansion Capital Protection:
      Prior to Q1 land expansion (while owned_quadrants < 2 and day >= 8), discretionary seed
      purchases must protect the $1,000 capital floor required for BUY_LAND Q1.
      On Day 12, BUY_LAND Q1 executes as soon as cash >= $1,000.
      Once Q1 is owned, capital protection is released and normal $300 cash reserve resumes.
    """

    def __init__(self, config: Optional[CompetitiveConfig] = None):
        super().__init__(config=config)
        self.name = "Q1CapitalProtectedROIAgent"

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
        # On or after Day 12, execute BUY_LAND Q1 as soon as cash >= $1,000
        if day >= self.config.expansion_day and self.owned_quadrants < self.config.target_quadrants:
            land_cost = 1000.0
            if cash >= land_cost:
                builder.buy_land()
                self.owned_quadrants = 2
                self.telemetry.spending_land += land_cost
                self.telemetry.owned_tiles_count = 50
                self.telemetry.q1_owned = 25
                self.telemetry.q1_productive = len(self.q1_crop_tiles)
                self.telemetry.buy_land_executed_step = state.step
                self.telemetry.log_event("BUY_LAND", state.step, day, hour, cash, "Bought Q1 (50 tiles total)")
                cash -= land_cost

        # Seed Purchases with Q1 Capital Protection
        self._buy_seeds_if_needed(state, builder, cash, reserve)

    def _buy_seeds_if_needed(self, state: GameState, builder: ActionBuilder, cash: float, reserve: float):
        day = state.day
        if day > self.config.all_plant_cutoff_day:
            return
            
        # Q1 Capital Protection Rule:
        # While Q1 is unowned and starting Day 8 (pre-expansion capital accumulation),
        # discretionary seed purchases must protect the $1,000 land cost floor.
        if self.owned_quadrants < 2 and day >= 8:
            effective_reserve = max(reserve, 1000.0)
        else:
            effective_reserve = reserve
            
        if state.get_seed_count("WHEAT") < 4 and cash - 60.0 >= effective_reserve:
            builder.buy_seed("WHEAT", 6)
            self.telemetry.spending_seeds += 60.0
            self.telemetry.wheat_bought += 6
            cash -= 60.0
            
        if state.get_seed_count("CARROT") < 4 and cash - 120.0 >= effective_reserve:
            builder.buy_seed("CARROT", 6)
            self.telemetry.spending_seeds += 120.0
            cash -= 120.0

        if day <= self.config.melon_plant_cutoff_day and state.get_seed_count("MELON") < 4 and cash - 320.0 >= effective_reserve:
            builder.buy_seed("MELON", 4)
            self.telemetry.spending_seeds += 320.0
            cash -= 320.0
