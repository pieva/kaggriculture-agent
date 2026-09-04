"""Build the 2026-09-04 current Top-3 strategy replay benchmark."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any

from analyze_episode_105080066 import analyze

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_REPLAY_DIR = ROOT / "data" / "replays" / "json"
OUT = ROOT / "experiments" / "e18" / "artifacts" / "discovery"
ARTIFACT = OUT / "E18_CURRENT_TOP3_STRATEGY_BENCHMARK_2026_09_04.json"
CSV_PATH = OUT / "E18_CURRENT_TOP3_STRATEGY_PROFILES_2026_09_04.csv"
E18_5_REFERENCE = (
    ROOT
    / "docs"
    / "model_specs"
    / "codex"
    / "e18"
    / "artifacts"
    / "derived"
    / "E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1.json"
)

LEADERBOARD_SNAPSHOT = {
    "observed_at": "2026-09-04T10:21:06+02:00",
    "url": "https://www.kaggle.com/competitions/kaggriculture/leaderboard",
    "entries": [
        {"rank": 1, "player": "Crop Dusta", "owner": "Rishi Gottumukkala", "rating": 3032.3},
        {"rank": 2, "player": "Giulio Ravasio", "owner": "Giulio Ravasio", "rating": 2967.3},
        {"rank": 3, "player": "Jesse Bullard", "owner": "Jesse Bullard", "rating": 2960.4},
    ],
}

CORPUS = (
    (105380550, "CROP_GIULIO"),
    (105377081, "CROP_GIULIO"),
    (105366473, "CROP_GIULIO"),
    (105341443, "CROP_GIULIO"),
    (105405557, "CROP_JESSE"),
    (105409114, "CROP_JESSE"),
    (105398548, "CROP_JESSE"),
    (105384058, "CROP_JESSE"),
    (105398563, "GIULIO_JESSE"),
    (105395068, "GIULIO_JESSE"),
    (105391568, "GIULIO_JESSE"),
)

PHASES = {
    "D01_D10": range(1, 11),
    "D11_D20": range(11, 21),
    "D21_D30": range(21, 31),
}
SNAPSHOT_DAYS = (1, 5, 10, 15, 20, 25, 30)
ACTION_FIELDS = (
    "plant",
    "water",
    "harvest",
    "dig",
    "move",
    "pass",
    "other_productive",
    "unit_actions",
)
CROP_TYPES = ("CARROT", "MELON", "STRAWBERRY", "TOMATO", "WHEAT")


def _count(mapping: dict[str, Any], key: str) -> int:
    return int(mapping.get(key, 0) or 0)


def _ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def _round(value: float) -> float:
    return round(float(value), 6)


def _sha256_json(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest().upper()


def _action_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    values = {key: sum(int(row[key]) for row in rows) for key in ACTION_FIELDS}
    productive = sum(
        values[key]
        for key in ("plant", "water", "harvest", "dig", "other_productive")
    )
    values.update(
        {
            "productive": productive,
            "move_per_productive": _round(_ratio(values["move"], productive)),
            "productive_per_move": _round(_ratio(productive, values["move"])),
        }
    )
    return values


def _first_day_at_least(rows: list[dict[str, Any]], field: str, value: int) -> int | None:
    return next(
        (int(row["display_day"]) for row in rows if int(row[field]) >= value),
        None,
    )


def _profile(
    summary: dict[str, Any],
    player: dict[str, Any],
    opponent: dict[str, Any],
    daily_rows: list[dict[str, Any]],
    action_rows: list[dict[str, Any]],
    pair: str,
) -> dict[str, Any]:
    player_index = int(player["player_index"])
    daily = [row for row in daily_rows if int(row["player_index"]) == player_index]
    actions = [row for row in action_rows if int(row["player_index"]) == player_index]
    execution = player["crop_action_execution"]
    transitions = player["transition_metrics"]["counts"]
    topology = player["final_topology"]["pasture_by_quadrant"]
    action_totals = _action_metrics(actions)
    phases = {
        name: _action_metrics(
            [row for row in actions if int(row["display_day"]) in days]
        )
        for name, days in PHASES.items()
    }
    snapshots = {
        f"D{day:02d}": {
            key: row[key]
            for key in (
                "money",
                "worker_slots",
                "quadrants",
                "crops",
                "unwatered",
                "harvest_ready",
                "weeds",
                "pastures",
                "animals",
                "crop_mix",
                "pasture_by_quadrant",
            )
        }
        for day in SNAPSHOT_DAYS
        for row in daily
        if int(row["display_day"]) == day
    }
    harvested_units = {
        crop: _count(execution["harvested_units"], crop) for crop in CROP_TYPES
    }
    planted_units = {
        crop: _count(execution["planted_units"], crop) for crop in CROP_TYPES
    }
    score = float(player["final_reward"])
    opponent_score = float(opponent["final_reward"])
    profile = {
        "episode_id": int(summary["identity"]["episode_id"]),
        "seed": int(summary["identity"]["seed"]),
        "pair": pair,
        "player_index": player_index,
        "player": player["player"],
        "opponent": opponent["player"],
        "score": score,
        "opponent_score": opponent_score,
        "margin": score - opponent_score,
        "outcome": "WIN" if score > opponent_score else "LOSS",
        "raw_sha256": summary["identity"]["raw_sha256"],
        "action_stream_sha256": player["action_stream_sha256"],
        "first_three_quadrants_display_day": player[
            "first_three_quadrants_display_day"
        ],
        "first_12_workers_display_day": _first_day_at_least(
            daily, "worker_slots", 12
        ),
        "peak_workers": max(int(row["worker_slots"]) for row in daily),
        "final_workers": int(daily[-1]["worker_slots"]),
        "final_pastures": int(player["final_topology"]["pastures"]),
        "final_animals": int(player["final_topology"]["animals"]),
        "final_pasture_topology": "-".join(
            str(_count(topology, quadrant)) for quadrant in ("Q0", "Q1", "Q2")
        ),
        "final_pasture_by_quadrant": topology,
        "peak_crops": int(player["peak_crops"]),
        "peak_crop_first_display_day": int(player["peak_crop_display_days"][0]),
        "crop_tile_days_total": int(player["crop_tile_days_total"]),
        "crop_tile_days_d21_d30": int(player["crop_tile_days_d21_d30"]),
        "unwatered_tile_days_total": int(player["unwatered_tile_days_total"]),
        "unwatered_tile_days_d21_d30": int(
            player["unwatered_tile_days_d21_d30"]
        ),
        "late_unwatered_per_crop_tile": _round(
            _ratio(
                player["unwatered_tile_days_d21_d30"],
                player["crop_tile_days_d21_d30"],
            )
        ),
        "weed_exits": _count(transitions, "expired_to_weed")
        + _count(transitions, "starved_to_weed"),
        "starved_to_weed": _count(transitions, "starved_to_weed"),
        "live_crop_rotations": _count(transitions, "dug_up_crop"),
        "harvested_units_total": int(execution["harvested_units_total"]),
        "harvested_units": harvested_units,
        "planted_units": planted_units,
        "harvest_events": execution["harvest_events"],
        "mean_units_per_harvest": execution["mean_units_per_harvest"],
        "crop_request_acknowledgement_pct": execution[
            "acknowledgement_rate_pct"
        ],
        "pass_on_actionable_tile": player["pass_on_actionable_tile"],
        "requested_sell_value": player["requested_sell_value"],
        "total_requested_sell_value": float(player["total_requested_sell_value"]),
        "requested_crop_sell_share_pct": float(
            player["requested_crop_sell_share_pct"]
        ),
        "requested_livestock_sell_share_pct": _round(
            100.0 - float(player["requested_crop_sell_share_pct"])
        ),
        "pass_on_actionable_total": sum(
            int(value) for value in player["pass_on_actionable_tile"].values()
        ),
        "actions": action_totals,
        "action_phases": phases,
        "harvested_units_per_1000_moves": _round(
            1000.0 * _ratio(execution["harvested_units_total"], action_totals["move"])
        ),
        "score_per_move": _round(_ratio(score, action_totals["move"])),
        "farm_snapshots": snapshots,
    }
    fingerprint_fields = {
        key: profile[key]
        for key in (
            "first_three_quadrants_display_day",
            "first_12_workers_display_day",
            "final_pasture_topology",
            "peak_crops",
            "crop_tile_days_d21_d30",
            "weed_exits",
            "live_crop_rotations",
            "harvested_units_total",
            "harvested_units",
            "planted_units",
        )
    }
    profile["strategy_fingerprint_sha256"] = _sha256_json(fingerprint_fields)
    profile["action_shape_sha256"] = _sha256_json(
        {"actions": action_totals, "action_phases": phases}
    )
    return profile


def _topology_mode(rows: list[dict[str, Any]]) -> list[str]:
    counts = Counter(str(row["final_pasture_topology"]) for row in rows)
    maximum = max(counts.values())
    return sorted(key for key, value in counts.items() if value == maximum)


def _phase_mean(rows: list[dict[str, Any]], phase: str, field: str) -> float:
    return _round(mean(row["action_phases"][phase][field] for row in rows))


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    outcomes = Counter(str(row["outcome"]) for row in rows)
    numeric_fields = (
        "score",
        "margin",
        "first_three_quadrants_display_day",
        "first_12_workers_display_day",
        "final_pastures",
        "final_animals",
        "peak_crops",
        "crop_tile_days_total",
        "crop_tile_days_d21_d30",
        "unwatered_tile_days_total",
        "unwatered_tile_days_d21_d30",
        "late_unwatered_per_crop_tile",
        "weed_exits",
        "live_crop_rotations",
        "harvested_units_total",
        "harvested_units_per_1000_moves",
        "score_per_move",
        "requested_crop_sell_share_pct",
        "pass_on_actionable_total",
    )
    aggregate: dict[str, Any] = {
        "profiles": len(rows),
        "wins": outcomes["WIN"],
        "losses": outcomes["LOSS"],
        "seat_0": sum(int(row["player_index"]) == 0 for row in rows),
        "seat_1": sum(int(row["player_index"]) == 1 for row in rows),
        "score_median": _round(median(float(row["score"]) for row in rows)),
        "score_min": min(float(row["score"]) for row in rows),
        "score_max": max(float(row["score"]) for row in rows),
        "topology_counts": dict(
            sorted(Counter(row["final_pasture_topology"] for row in rows).items())
        ),
        "topology_mode": _topology_mode(rows),
        "unique_strategy_fingerprints": len(
            {row["strategy_fingerprint_sha256"] for row in rows}
        ),
        "unique_action_streams": len({row["action_stream_sha256"] for row in rows}),
        "unique_action_shapes": len({row["action_shape_sha256"] for row in rows}),
        "largest_action_shape_cluster": max(
            Counter(row["action_shape_sha256"] for row in rows).values()
        ),
    }
    aggregate.update(
        {f"mean_{field}": _round(mean(row[field] for row in rows)) for field in numeric_fields}
    )
    for field in ("move", "productive", "pass", "unit_actions", "move_per_productive"):
        aggregate[f"mean_{field}"] = _round(
            mean(row["actions"][field] for row in rows)
        )
    aggregate["phase_action_means"] = {
        phase: {
            field: _phase_mean(rows, phase, field)
            for field in (
                "move",
                "productive",
                "pass",
                "move_per_productive",
                "plant",
                "water",
                "harvest",
                "dig",
                "other_productive",
            )
        }
        for phase in PHASES
    }
    aggregate["mean_harvested_units_by_crop"] = {
        crop: _round(mean(row["harvested_units"][crop] for row in rows))
        for crop in CROP_TYPES
    }
    aggregate["mean_planted_units_by_crop"] = {
        crop: _round(mean(row["planted_units"][crop] for row in rows))
        for crop in CROP_TYPES
    }
    return aggregate


def _e18_5_comparison(agent_aggregates: dict[str, Any]) -> dict[str, Any]:
    reference = json.loads(E18_5_REFERENCE.read_text(encoding="utf-8"))
    codex = reference["standings"]["CODEX_E18_5_STATE_DRIVEN_662"]
    normalized = {
        "profiles": int(codex["matches"]),
        "mean_score": float(codex["money_mean"]),
        "mean_move": float(codex["move_actions_mean"]),
        "mean_productive": float(codex["productive_actions_mean"]),
        "mean_move_per_productive": float(codex["move_per_productive_mean"]),
        "mean_harvested_units_total": float(codex["harvested_units_total_mean"]),
        "mean_harvested_units_per_1000_moves": _round(
            1000.0
            * _ratio(codex["harvested_units_total_mean"], codex["move_actions_mean"])
        ),
        "mean_score_per_move": _round(
            _ratio(codex["money_mean"], codex["move_actions_mean"])
        ),
        "topology": "6-6-2",
    }
    deltas = {
        player: {
            metric: _round(values[metric] - normalized[metric])
            for metric in (
                "mean_move",
                "mean_productive",
                "mean_move_per_productive",
                "mean_harvested_units_total",
                "mean_harvested_units_per_1000_moves",
                "mean_score_per_move",
            )
        }
        for player, values in agent_aggregates.items()
    }
    return {
        "reference_artifact": str(E18_5_REFERENCE.relative_to(ROOT)).replace("\\", "/"),
        "codex_e18_5_662": normalized,
        "top3_minus_codex_absolute": deltas,
        "comparability_boundary": [
            "Action groups and harvested-unit extraction use compatible engine semantics.",
            "The Top-3 sample is live head-to-head play; E18.5 is a fixed local development pool.",
            "Differences are descriptive and cannot be interpreted as topology causality.",
        ],
    }


def build(replay_dir: Path) -> dict[str, Any]:
    profiles: list[dict[str, Any]] = []
    corpus: list[dict[str, Any]] = []
    for episode_id, pair in CORPUS:
        summary, daily_rows, action_rows = analyze(replay_dir / f"{episode_id}.json")
        for player in summary["players"]:
            opponent = summary["players"][1 - int(player["player_index"])]
            profiles.append(
                _profile(
                    summary,
                    player,
                    opponent,
                    daily_rows,
                    action_rows,
                    pair,
                )
            )
        corpus.append(
            {
                **summary["identity"],
                "pair": pair,
                "replay_url": (
                    "https://www.kaggle.com/competitions/kaggriculture/episodes/"
                    f"{episode_id}"
                ),
            }
        )
    players = [entry["player"] for entry in LEADERBOARD_SNAPSHOT["entries"]]
    aggregates = {
        player: _aggregate([row for row in profiles if row["player"] == player])
        for player in players
    }
    return {
        "schema_version": 1,
        "benchmark_id": "E18_CURRENT_TOP3_STRATEGY_BENCHMARK_2026_09_04",
        "epistemic_role": "E18_EXTERNAL_DISCOVERY_EVIDENCE",
        "leaderboard_snapshot": LEADERBOARD_SNAPSHOT,
        "sampling_design": {
            "episodes": len(CORPUS),
            "profiles": len(profiles),
            "pair_counts": dict(sorted(Counter(pair for _, pair in CORPUS).items())),
            "selection": "Recent balanced head-to-head sample among the current Top 3.",
            "raw_replays_retained_in_repository": False,
        },
        "corpus": corpus,
        "profiles": profiles,
        "agent_aggregates": aggregates,
        "e18_5_662_comparison": _e18_5_comparison(aggregates),
        "observability": {
            "public_farms": True,
            "private_inventory": False,
            "cross_episode_state": False,
            "strategy_source_code": False,
        },
        "limitations": [
            "Eleven recent games are sufficient for reconstruction hypotheses, not causal identification.",
            "Players face only current Top-3 opponents, while E18.5 uses a local fixed control.",
            "Requested market value is quantity times observed price and is not execution-verified.",
            "Pass-on-actionable is a local tile proxy and is not equivalent to globally wasted time.",
            "Leaderboard positions and ratings are a point-in-time public snapshot.",
        ],
    }


def _write_csv(rows: list[dict[str, Any]]) -> None:
    flat_rows = []
    for row in rows:
        flat = {
            key: json.dumps(value, sort_keys=True) if isinstance(value, dict) else value
            for key, value in row.items()
        }
        flat_rows.append(flat)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(flat_rows[0]))
        writer.writeheader()
        writer.writerows(flat_rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay-dir", type=Path, default=DEFAULT_REPLAY_DIR)
    args = parser.parse_args()
    artifact = build(args.replay_dir)
    OUT.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    _write_csv(artifact["profiles"])
    print(ARTIFACT.relative_to(ROOT))
    for player, values in artifact["agent_aggregates"].items():
        print(
            f"{player}: {values['wins']}-{values['losses']} "
            f"score={values['mean_score']:.1f} "
            f"move/productive={values['mean_move_per_productive']:.3f} "
            f"harvest/1k-move={values['mean_harvested_units_per_1000_moves']:.1f}"
        )


if __name__ == "__main__":
    main()
