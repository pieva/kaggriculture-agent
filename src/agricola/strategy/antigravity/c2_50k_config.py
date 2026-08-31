"""Configuration for Antigravity C2 50K Model Strategy (Compact Q0 Routine)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONFIG_PATH = (
    REPO_ROOT / "configs" / "model_spec_c2" / "ANTIGRAVITY_C2_50K_CONFIG.json"
)


@dataclass
class AntigravityC2_50K_Config:
    """Parametric configuration for Antigravity C2 50K Strategy Model."""

    candidate_id: str = "ANTIGRAVITY_C2"
    schema_version: str = "model_spec_c2.antigravity.compact_q0_50k.v1"
    model_spec_version: str = "ANTIGRAVITY-C2-COMPACT-Q0-50K-ROUTINE-V1.0"
    foundation_checkpoint: str = "f391ee2"

    # Land & Layout (Q0 only, 24 productive tiles + shed at (4,4))
    quadrants_owned: int = 1
    workforce_total: int = 7
    crop_working_set_target: int = 18
    crop_counts: Dict[str, int] = field(
        default_factory=lambda: {"MELON": 9, "STRAWBERRY": 8, "WHEAT": 1}
    )
    pasture_allocation_target: int = 6
    livestock_targets: Dict[str, int] = field(
        default_factory=lambda: {"COW": 3, "SHEEP": 3}
    )
    bootstrap_livestock: Dict[str, int] = field(
        default_factory=lambda: {"COW": 2, "SHEEP": 2}
    )
    livestock_activation_days: Dict[str, int] = field(
        default_factory=lambda: {"COW": 7, "SHEEP": 8}
    )

    # Cohorts
    melon_cohort_offsets: list[int] = field(default_factory=lambda: [0, 1, 2])
    strawberry_cohort_offsets: list[int] = field(default_factory=lambda: [0, 2])
    wheat_cohort_offset: int = 0

    # Economics & Buffers
    operating_cash_floor: float = 50.0
    feed_reserve_rounds: int = 2
    observed_capacity_days: int = 3
    hard_schedule_days: int = 2
    minimum_post_plant_action_phases: int = 1
    payback_cutoff_days: int = 2
    crop_horizon_margin_days: int = 1
    endgame_shutdown_days: int = 2
    max_noop_before_invalidation: int = 3
    turns_per_day: int = 24

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AntigravityC2_50K_Config":
        """Construct config instance from dictionary."""
        return cls(
            candidate_id=data.get("candidate_id", "ANTIGRAVITY_C2"),
            schema_version=data.get("schema_version", "model_spec_c2.antigravity.compact_q0_50k.v1"),
            model_spec_version=data.get("model_spec_version", "ANTIGRAVITY-C2-COMPACT-Q0-50K-ROUTINE-V1.0"),
            foundation_checkpoint=data.get("foundation_checkpoint", "f391ee2"),
            quadrants_owned=int(data.get("quadrants_owned", 1)),
            workforce_total=int(data.get("workforce_total", 7)),
            crop_working_set_target=int(data.get("crop_working_set_target", 18)),
            crop_counts={str(k): int(v) for k, v in data.get("crop_counts", {}).items()} or {"MELON": 9, "STRAWBERRY": 8, "WHEAT": 1},
            pasture_allocation_target=int(data.get("pasture_allocation_target", 6)),
            livestock_targets={str(k): int(v) for k, v in data.get("livestock_targets", {}).items()} or {"COW": 3, "SHEEP": 3},
            bootstrap_livestock={str(k): int(v) for k, v in data.get("bootstrap_livestock", {}).items()} or {"COW": 2, "SHEEP": 2},
            livestock_activation_days={str(k): int(v) for k, v in data.get("livestock_activation_days", {}).items()} or {"COW": 7, "SHEEP": 8},
            melon_cohort_offsets=list(data.get("melon_cohort_offsets", [0, 1, 2])),
            strawberry_cohort_offsets=list(data.get("strawberry_cohort_offsets", [0, 2])),
            wheat_cohort_offset=int(data.get("wheat_cohort_offset", 0)),
            operating_cash_floor=float(data.get("operating_cash_floor", 50.0)),
            feed_reserve_rounds=int(data.get("feed_reserve_rounds", 2)),
            observed_capacity_days=int(data.get("observed_capacity_days", 3)),
            hard_schedule_days=int(data.get("hard_schedule_days", 2)),
            minimum_post_plant_action_phases=int(data.get("minimum_post_plant_action_phases", 1)),
            payback_cutoff_days=int(data.get("payback_cutoff_days", 2)),
            crop_horizon_margin_days=int(data.get("crop_horizon_margin_days", 1)),
            endgame_shutdown_days=int(data.get("endgame_shutdown_days", 2)),
            max_noop_before_invalidation=int(data.get("max_noop_before_invalidation", 3)),
            turns_per_day=int(data.get("turns_per_day", 24)),
        )

    @classmethod
    def load(cls, path: Path | str | None = None) -> "AntigravityC2_50K_Config":
        """Load configuration from JSON file or default."""
        if path is None and "ANTIGRAVITY_C2_50K_CONFIG" in globals():
            return cls.from_dict(globals()["ANTIGRAVITY_C2_50K_CONFIG"])
        config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
        if not config_path.exists():
            return cls()
        with config_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)


    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary representation."""
        return {
            "candidate_id": self.candidate_id,
            "schema_version": self.schema_version,
            "model_spec_version": self.model_spec_version,
            "foundation_checkpoint": self.foundation_checkpoint,
            "quadrants_owned": self.quadrants_owned,
            "workforce_total": self.workforce_total,
            "crop_working_set_target": self.crop_working_set_target,
            "crop_counts": dict(self.crop_counts),
            "pasture_allocation_target": self.pasture_allocation_target,
            "livestock_targets": dict(self.livestock_targets),
            "bootstrap_livestock": dict(self.bootstrap_livestock),
            "livestock_activation_days": dict(self.livestock_activation_days),
            "melon_cohort_offsets": list(self.melon_cohort_offsets),
            "strawberry_cohort_offsets": list(self.strawberry_cohort_offsets),
            "wheat_cohort_offset": self.wheat_cohort_offset,
            "operating_cash_floor": self.operating_cash_floor,
            "feed_reserve_rounds": self.feed_reserve_rounds,
            "observed_capacity_days": self.observed_capacity_days,
            "hard_schedule_days": self.hard_schedule_days,
            "minimum_post_plant_action_phases": self.minimum_post_plant_action_phases,
            "payback_cutoff_days": self.payback_cutoff_days,
            "crop_horizon_margin_days": self.crop_horizon_margin_days,
            "endgame_shutdown_days": self.endgame_shutdown_days,
            "max_noop_before_invalidation": self.max_noop_before_invalidation,
            "turns_per_day": self.turns_per_day,
        }
