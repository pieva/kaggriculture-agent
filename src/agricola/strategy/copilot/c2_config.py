from dataclasses import dataclass


@dataclass
class CopilotC2Config:
    """Explicit productive-capacity envelope for the Copilot C2 candidate."""

    default_crop: str = "WHEAT"
    water_deadline_unwatered_days: int = 2
    preventive_dig_before_lifespan: bool = True
    enable_replant_after_harvest: bool = True
    replant_preferred_crop: str = "WHEAT"
    weed_recovery_priority: str = "DIG"
    strict_harvest_gate: bool = True
    active_working_set_radius: int = 4
    prefer_recovery_over_plant: bool = True
    target_workforce: int = 9
    seed_reserve: int = 2
    last_plant_day: int = 27
