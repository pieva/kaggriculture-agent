#!/usr/bin/env python3
"""Freeze the E18 6-6-2 baseline against the selected Top-3 replay profiles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
TOP3_SOURCE = (
    ROOT / "experiments/e17/artifacts/discovery/codex/E17_TOP3_REPLAY_METRICS.json"
)
TOURNAMENT_SOURCE = (
    ROOT
    / "experiments/e17/artifacts/derived/common/"
    / "E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3.json"
)
OUTPUT = (
    ROOT
    / "experiments/e18/artifacts/baseline/"
    / "E18_662_TOP3_BASELINE_BENCHMARK_V1.json"
)
TOP3_NAMES = ("tetsuya", "OceanMix", "Crop Dusta")
TARGET_MONEY = 100_000.0


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _record_index(
    matches: list[dict[str, Any]], participant: str
) -> dict[tuple[int, int, str], dict[str, Any]]:
    result: dict[tuple[int, int, str], dict[str, Any]] = {}
    for match in matches:
        for seat in (0, 1):
            if match[f"p{seat}"] != participant:
                continue
            opponent = str(match[f"p{1 - seat}"])
            result[(int(match["seed"]), seat, opponent)] = match[f"p{seat}_metrics"]
    return result


def _behavioral_equivalence(tournament: dict[str, Any]) -> dict[str, Any]:
    matches = tournament["matches"]
    v3 = _record_index(matches, "COPILOT_662_V3")
    v2 = _record_index(matches, "CODEX_662_V2_CONTROL")
    shared_opponents = ("CLAUDE_V5", "CLAUDE_V3_CONTROL")
    comparable = [key for key in v3 if key[2] in shared_opponents and key in v2]
    exact_metrics = sum(v3[key] == v2[key] for key in comparable)
    exact_action_counts = sum(
        v3[key].get("action_counts") == v2[key].get("action_counts")
        for key in comparable
    )
    return {
        "comparable_runs": len(comparable),
        "exact_complete_metric_profiles": exact_metrics,
        "exact_action_count_profiles": exact_action_counts,
        "differentiated_metric_profiles": len(comparable) - exact_metrics,
        "differentiated_action_count_profiles": len(comparable)
        - exact_action_counts,
    }


def main() -> int:
    top3 = _load(TOP3_SOURCE)
    tournament = _load(TOURNAMENT_SOURCE)
    aggregates = {
        row["player_name"]: row
        for row in top3["agent_aggregates"]
        if row.get("player_name") in TOP3_NAMES
    }
    if set(aggregates) != set(TOP3_NAMES):
        raise RuntimeError("selected Top-3 profiles are incomplete")

    standings = tournament["standings"]
    baseline = standings["CODEX_662_V2_CONTROL"]
    h2h = tournament["head_to_head"]
    vs_v5 = h2h["CLAUDE_V5_vs_CODEX_662_V2_CONTROL"]
    vs_v3 = h2h["CLAUDE_V3_CONTROL_vs_CODEX_662_V2_CONTROL"]
    self_play = h2h["COPILOT_662_V3_vs_CODEX_662_V2_CONTROL"]
    money_vs_claude = (
        float(vs_v5["CODEX_662_V2_CONTROL_money_mean"])
        + float(vs_v3["CODEX_662_V2_CONTROL_money_mean"])
    ) / 2.0
    self_play_money = float(self_play["CODEX_662_V2_CONTROL_money_mean"])
    equivalence = _behavioral_equivalence(tournament)

    top3_profiles = {
        name: {
            key: aggregates[name][key]
            for key in (
                "episodes",
                "mean_score",
                "median_q1_step",
                "median_q2_step",
                "mean_final_hands",
                "mean_peak_crops",
                "mean_peak_animals",
                "mean_moves",
                "mean_move_share_active_pct",
                "mean_owned_tile_activation_pct",
                "weed_tile_days_total",
                "escapes_total",
                "wins",
                "losses",
            )
        }
        for name in TOP3_NAMES
    }
    baseline_profile = {
        "model": "CODEX-E17.3-TOPOLOGY-FILL-662-V2",
        "topology": {"Q0": 6, "Q1": 6, "Q2": 2},
        "matches": int(baseline["matches"]),
        "money_mean_all_regimes": float(baseline["money_mean"]),
        "money_mean_vs_claude": money_vs_claude,
        "money_mean_symmetric_662": self_play_money,
        "q1_activation_day_mean": float(baseline["q1_activation_day_mean"]),
        "q2_activation_day_mean": float(baseline["q2_activation_day_mean"]),
        "three_quadrant_runs": int(baseline["three_quadrant_runs"]),
        "peak_hands_mean": float(baseline["peak_hands_mean"]),
        "peak_crops_mean": float(baseline["peak_crops_mean"]),
        "peak_animals_mean": float(baseline["peak_animals_mean"]),
        "peak_weeds_mean": float(baseline["peak_weeds_mean"]),
        "animal_escapes": int(baseline["animal_escapes"]),
        "move_actions_mean": float(baseline["move_actions_mean"]),
        "move_per_productive_mean": float(baseline["move_per_productive_mean"]),
        "target_pastures_built_mean": float(
            baseline["target_pastures_built_mean"]
        ),
        "target_pastures_filled_mean": float(
            baseline["target_pastures_filled_mean"]
        ),
        "max_q2_pastures_mean": float(baseline["max_q2_pastures_mean"]),
        "topology_cap_breaches": int(baseline["topology_cap_breaches"]),
    }
    gates = {
        "money_vs_claude_at_least_100k": {
            "threshold": TARGET_MONEY,
            "observed": money_vs_claude,
            "status": "PASS" if money_vs_claude >= TARGET_MONEY else "FAIL",
        },
        "symmetric_662_money_at_least_100k": {
            "threshold": TARGET_MONEY,
            "observed": self_play_money,
            "gap": TARGET_MONEY - self_play_money,
            "status": "PASS" if self_play_money >= TARGET_MONEY else "FAIL",
        },
        "top3_q1_timing_window": {
            "target_days": [5, 7],
            "observed": float(baseline["q1_activation_day_mean"]),
            "status": (
                "PASS"
                if 5 <= float(baseline["q1_activation_day_mean"]) <= 7
                else "FAIL"
            ),
        },
        "top3_q2_timing_window": {
            "target_days": [8, 11],
            "observed": float(baseline["q2_activation_day_mean"]),
            "status": (
                "PASS"
                if 8 <= float(baseline["q2_activation_day_mean"]) <= 11
                else "FAIL"
            ),
        },
        "top3_peak_crop_floor": {
            "threshold": 58.0,
            "observed": float(baseline["peak_crops_mean"]),
            "status": "PASS" if float(baseline["peak_crops_mean"]) >= 58 else "FAIL",
        },
        "zero_escapes": {
            "threshold": 0,
            "observed": int(baseline["animal_escapes"]),
            "status": "PASS" if int(baseline["animal_escapes"]) == 0 else "FAIL",
        },
        "pasture_fill_14_of_14": {
            "threshold": 14,
            "observed": float(baseline["target_pastures_filled_mean"]),
            "status": (
                "PASS"
                if float(baseline["target_pastures_filled_mean"]) == 14
                else "FAIL"
            ),
        },
        "reactive_action_stream_divergence": {
            "threshold": 1,
            "observed": equivalence["differentiated_action_count_profiles"],
            "status": (
                "PASS"
                if equivalence["differentiated_action_count_profiles"] >= 1
                else "FAIL"
            ),
        },
        "causal_activation_telemetry": {
            "required": [
                "regime_transitions",
                "guard_activations",
                "orders_throttled",
                "units_suppressed",
            ],
            "observed": [],
            "status": "MISSING",
        },
    }
    payload = {
        "schema_version": "E18_662_TOP3_BASELINE_BENCHMARK_V1",
        "date": "2026-09-03",
        "epistemic_role": "E18_TRAINING_BASELINE_FROM_E17_CONSUMED_EVIDENCE",
        "selected_top3_are_historical_replay_archetypes_not_live_callable_agents": True,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "sources": {
            "top3": str(TOP3_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "tournament": str(TOURNAMENT_SOURCE.relative_to(ROOT)).replace(
                "\\", "/"
            ),
        },
        "top3_profiles": top3_profiles,
        "baseline_662": baseline_profile,
        "v3_vs_v2_behavioral_equivalence": equivalence,
        "e18_entry_gates": gates,
        "planned_candidate": "CODEX-E18.1-REACTIVE-662-V1",
        "planned_causal_family": (
            "OBSERVABLE_MARKET_AND_SERVICE_REGIME_SELECTION_WITH_662_INVARIANTS"
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
