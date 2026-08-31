from dataclasses import dataclass


@dataclass
class CopilotC2Config:
    """Explicit productive-capacity envelope for the Copilot C2 candidate."""

    default_crop: str = "MELON"
    water_deadline_unwatered_days: int = 2
    preventive_dig_before_lifespan: bool = True
    enable_replant_after_harvest: bool = True
    replant_preferred_crop: str = "MELON"
    weed_recovery_priority: str = "DIG"
    strict_harvest_gate: bool = True
    active_working_set_radius: int = 4
    prefer_recovery_over_plant: bool = True
    target_workforce: int = 9
    seed_reserve: int = 0
    # Endgame planting cutoff (E-C2-PERF-04): MELON has first_yield_day=10, so
    # a plant sown after day 11 in a 29-day episode has too little remaining
    # runway to be harvested, sold, and possibly re-cycled before terminal.
    # Performance verification found last_plant_day=27 (correct for WHEAT's
    # first_yield_day=2) left MELON crops stranded unharvested; day 11 is the
    # empirically identified break point that maximizes realized revenue.
    last_plant_day: int = 11

    # Land expansion (E-C2-PERF-01): disabled after performance verification
    # showed that, combined with MELON's long yield cycle, capital spent on
    # BUY_LAND could not be productively converted into harvested/sold crop
    # before the terminal day — every configuration tested with expansion
    # enabled scored lower than the same configuration with it disabled.
    # Kept as a declared, evidence-based limitation (Section 7 of the
    # MODEL_SPEC), not a silent omission.
    enable_land_expansion: bool = False
    land_expansion_reserve: float = 300.0
    max_quadrants: int = 4
    # Endgame gate (E-C2-PERF-03): never buy land too close to the terminal
    # day, since newly unlocked tiles cannot be planted, grown and harvested
    # before the episode ends (observed: day-29 SE purchase in a 30-day
    # episode stranded ~3,500 of capital with zero return). Retained as a
    # safety gate in case enable_land_expansion is re-enabled later.
    last_land_purchase_day: int = 11

    # Workforce-to-footprint co-scaling (E-C2-PERF-02): target_workforce above
    # is now a hard ceiling, not the fixed target. Actual demand is derived
    # from the active (non-locked) tile count. tiles_per_worker=6 was the
    # empirically optimal ratio for the fixed 25-tile NW footprint with MELON.
    target_tiles_per_worker: float = 6.0
    min_workforce: int = 2
