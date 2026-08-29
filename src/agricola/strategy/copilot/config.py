"""Configuration for the Copilot isolated strategy model."""

from dataclasses import dataclass


@dataclass
class CopilotConfig:
    """Minimal isolated configuration for Copilot's independent model."""

    enable_land_expansion: bool = True
    target_quadrants: int = 2
    target_cows: int = 7
    target_sheep: int = 4
    max_hands: int = 6
    stop_hire_day: int = 1
    opening_day_seed_budget: int = 18
    opening_melon_seed_budget: int = 11
    opening_strawberry_seed_budget: int = 10
    opening_cash_buffer: float = 1200.0
    low_capacity_cash_floor: float = 1200.0
    active_crop_floor: int = 12
    pasture_floor: int = 6
