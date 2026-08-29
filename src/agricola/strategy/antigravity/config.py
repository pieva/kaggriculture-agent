"""Configuration for Antigravity Independent Strategy Model."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Set


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
