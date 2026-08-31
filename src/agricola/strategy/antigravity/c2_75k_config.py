"""Configuration for Antigravity C2 75K Model Strategy (Dual-Quadrant Q0+Q1 Routine)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONFIG_PATH = (
    REPO_ROOT / "configs" / "model_spec_c2" / "ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG.json"
)


@dataclass
class AntigravityC2_75K_Config:
    """Parametric configuration for Antigravity C2 75K Strategy Model."""

    candidate_id: str = "ANTIGRAVITY_C2_75K_DUAL_Q"
    schema_version: str = "model_spec_c2.antigravity.dual_q.v1"
    model_spec_version: str = "ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0"
    foundation_checkpoint: str = "f391ee2"

    # Land & Layout (Q0 + Q1, 48 productive tiles)
    quadrants_owned: int = 2
    workforce_total: int = 13
    q0_workforce_total: int = 7
    crop_working_set_target: int = 36
    crop_counts: Dict[str, int] = field(
        default_factory=lambda: {"MELON": 18, "STRAWBERRY": 16, "WHEAT": 2}
    )
    pasture_allocation_target: int = 12
    livestock_targets: Dict[str, int] = field(
        default_factory=lambda: {"COW": 6, "SHEEP": 6}
    )
    bootstrap_livestock: Dict[str, int] = field(
        default_factory=lambda: {"COW": 2, "SHEEP": 2}
    )
    q1_livestock_targets: Dict[str, int] = field(
        default_factory=lambda: {"COW": 3, "SHEEP": 3}
    )
    livestock_activation_days: Dict[str, int] = field(
        default_factory=lambda: {"COW": 7, "SHEEP": 8}
    )

    # Q1 Activation Gates
    q1_activation_min_day: int = 6
    q1_activation_max_day: int = 10
    q1_activation_cash: float = 2800.0
    q1_operating_cash_floor: float = 250.0

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
    def from_dict(cls, data: dict[str, Any]) -> "AntigravityC2_75K_Config":
        """Construct config instance from dictionary."""
        return cls(
            candidate_id=data.get("candidate_id", "ANTIGRAVITY_C2_75K_DUAL_Q"),
            schema_version=data.get("schema_version", "model_spec_c2.antigravity.dual_q.v1"),
            model_spec_version=data.get("model_spec_version", "ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0"),
            foundation_checkpoint=data.get("foundation_checkpoint", "f391ee2"),
            quadrants_owned=int(data.get("quadrants_owned", 2)),
            workforce_total=int(data.get("workforce_total", 13)),
            q0_workforce_total=int(data.get("q0_workforce_total", 7)),
            crop_working_set_target=int(data.get("crop_working_set_target", 36)),
            crop_counts={str(k): int(v) for k, v in data.get("crop_counts", {}).items()} or {"MELON": 18, "STRAWBERRY": 16, "WHEAT": 2},
            pasture_allocation_target=int(data.get("pasture_allocation_target", 12)),
            livestock_targets={str(k): int(v) for k, v in data.get("livestock_targets", {}).items()} or {"COW": 6, "SHEEP": 6},
            bootstrap_livestock={str(k): int(v) for k, v in data.get("bootstrap_livestock", {}).items()} or {"COW": 2, "SHEEP": 2},
            q1_livestock_targets={str(k): int(v) for k, v in data.get("q1_livestock_targets", {}).items()} or {"COW": 3, "SHEEP": 3},
            livestock_activation_days={str(k): int(v) for k, v in data.get("livestock_activation_days", {}).items()} or {"COW": 7, "SHEEP": 8},
            q1_activation_min_day=int(data.get("q1_activation_min_day", 6)),
            q1_activation_max_day=int(data.get("q1_activation_max_day", 10)),
            q1_activation_cash=float(data.get("q1_activation_cash", 2800.0)),
            q1_operating_cash_floor=float(data.get("q1_operating_cash_floor", 250.0)),
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
    def load(cls, path: Path | str | None = None) -> "AntigravityC2_75K_Config":
        """Load configuration from JSON file or default."""
        if path is None and "ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG" in globals():
            return cls.from_dict(globals()["ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG"])
        config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
        if not config_path.exists():
            return cls()
        with config_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)
