"""Configuration for Antigravity C2 Livestock Strategy Variant (LS1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AntigravityC2LivestockConfig:
    """Parametric configuration for Antigravity C2 Livestock Diagnostic Variant."""

    # Land & Layout
    quadrants_owned: int = 2
    crop_working_set_target: int = 38
    pasture_allocation_target: int = 2

    # Livestock Parameters
    livestock_headcount_target: int = 2
    livestock_species: str = "COW"
    livestock_activation_day: int = 11

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
            "livestock_activation_day": self.livestock_activation_day,
            "workforce_headcount": self.workforce_headcount,
            "operating_cash_floor": self.operating_cash_floor,
            "endgame_shutdown_steps": self.endgame_shutdown_steps,
            "enable_strict_harvest_gate": self.enable_strict_harvest_gate,
            "enable_recovery_dig": self.enable_recovery_dig,
            "enable_preventive_dig": self.enable_preventive_dig,
            "enable_day0_water_priority": self.enable_day0_water_priority,
            "crop_mix_weights": dict(self.crop_mix_weights),
        }
