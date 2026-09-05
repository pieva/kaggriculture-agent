"""Analyze every completed loss of Kaggle submission 56012496 (E18.16).

The raw replay cache is intentionally outside Git.  This script reuses the
frozen E18 lifecycle parser so the external diagnosis uses the same KPI
definitions as the earlier Top-3 benchmark.
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[5]
COMMON_TOOLS = ROOT / "experiments" / "e18" / "tools" / "common"
sys.path.insert(0, str(COMMON_TOOLS))

from analyze_episode_105080066 import analyze  # noqa: E402


OWNER = "Pietro Valocchi"
SUBMISSION_ID = 56012496
REPLAY_DIR = ROOT / "data" / "replays" / "json" / "e18_16_losses"
OUT_DIR = ROOT / "docs" / "model_specs" / "codex" / "e18" / "artifacts" / "derived"
JSON_OUT = OUT_DIR / "E18_16_KAGGLE_LOSS_DIAGNOSTIC_2026_09_04.json"
CSV_OUT = OUT_DIR / "E18_16_KAGGLE_LOSS_EPISODES_2026_09_04.csv"

EPISODE_IDS = (
    105496417,
    105493733,
    105492836,
    105491963,
    105491066,
    105490149,
    105488377,
    105486567,
    105485677,
    105483909,
    105480327,
    105477657,
    105476781,
    105475877,
    105474957,
    105473174,
    105470464,
)


def _mean(values: Iterable[float]) -> float:
    materialized = list(values)
    return round(statistics.mean(materialized), 3) if materialized else 0.0


def _median(values: Iterable[float]) -> float:
    materialized = list(values)
    return round(statistics.median(materialized), 3) if materialized else 0.0


def _ratio(numerator: float, denominator: float) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _count(mapping: dict[str, Any], key: str) -> int:
    return int(mapping.get(key, 0) or 0)


def _topology(player: dict[str, Any]) -> str:
    values = player["final_topology"]["pasture_by_quadrant"]
    return "-".join(str(_count(values, quadrant)) for quadrant in ("Q0", "Q1", "Q2"))


def _profile(
    summary: dict[str, Any],
    daily_rows: list[dict[str, Any]],
    action_rows: list[dict[str, Any]],
    player_index: int,
) -> dict[str, Any]:
    player = summary["players"][player_index]
    daily = [row for row in daily_rows if row["player_index"] == player_index]
    actions = [row for row in action_rows if row["player_index"] == player_index]
    totals = Counter()
    for row in actions:
        for key in (
            "plant",
            "water",
            "harvest",
            "dig",
            "move",
            "pass",
            "other_productive",
            "unit_actions",
        ):
            totals[key] += int(row[key])
    crop_service = sum(totals[key] for key in ("plant", "water", "harvest", "dig"))
    productive = crop_service + totals["other_productive"]
    execution = player["crop_action_execution"]
    acknowledged = execution["acknowledged"]
    transitions = player["transition_metrics"]["counts"]
    late = [row for row in daily if row["display_day"] >= 21]
    by_day = {int(row["display_day"]): row for row in daily}
    return {
        "player": player["player"],
        "player_index": player_index,
        "reward": player["final_reward"],
        "action_stream_sha256": player["action_stream_sha256"],
        "topology": _topology(player),
        "final_pastures": player["final_topology"]["pastures"],
        "final_animals": player["final_topology"]["animals"],
        "peak_daily_animals": max(int(row["animals"]) for row in daily),
        "first_three_quadrants_day": player["first_three_quadrants_display_day"],
        "peak_crops": player["peak_crops"],
        "crop_tile_days": player["crop_tile_days_total"],
        "late_crop_tile_days": player["crop_tile_days_d21_d30"],
        "unwatered_tile_days": player["unwatered_tile_days_total"],
        "late_unwatered_tile_days": player["unwatered_tile_days_d21_d30"],
        "late_water_stressed_tile_days": sum(int(row["water_stressed"]) for row in late),
        "weed_exits": _count(transitions, "expired_to_weed")
        + _count(transitions, "starved_to_weed"),
        "starved_to_weed": _count(transitions, "starved_to_weed"),
        "live_crop_rotations": _count(transitions, "dug_up_crop"),
        "harvested_crop_exits": _count(transitions, "harvested"),
        "harvested_units": execution["harvested_units_total"],
        "ack_plant": _count(acknowledged, "PLANT"),
        "ack_water": _count(acknowledged, "WATER"),
        "ack_harvest": _count(acknowledged, "HARVEST"),
        "ack_dig": _count(acknowledged, "DIG"),
        "crop_service_ack": sum(
            _count(acknowledged, opcode) for opcode in ("PLANT", "WATER", "HARVEST", "DIG")
        ),
        "crop_service_requested": crop_service,
        "crop_service_ack_rate_pct": round(
            100.0
            * sum(_count(acknowledged, opcode) for opcode in ("PLANT", "WATER", "HARVEST", "DIG"))
            / crop_service
            if crop_service
            else 0.0,
            3,
        ),
        "productive_actions": productive,
        "move_actions": totals["move"],
        "pass_actions": totals["pass"],
        "unit_actions": totals["unit_actions"],
        "move_per_productive": _ratio(totals["move"], productive),
        "pass_share_pct": round(100.0 * totals["pass"] / totals["unit_actions"], 3),
        "late_plant": player["d21_d30_actions"]["plant"],
        "late_water": player["d21_d30_actions"]["water"],
        "late_harvest": player["d21_d30_actions"]["harvest"],
        "late_dig": player["d21_d30_actions"]["dig"],
        "late_move": player["d21_d30_actions"]["move"],
        "late_pass": player["d21_d30_actions"]["pass"],
        "money_d10": float(by_day[10]["money"]),
        "money_d20": float(by_day[20]["money"]),
        "money_d30": float(by_day[30]["money"]),
        "money_gain_d20_d30": float(by_day[30]["money"])
        - float(by_day[20]["money"]),
        "crop_service_requested_by_opcode": execution["requested"],
        "crop_service_ack_by_opcode": execution["acknowledged"],
        "crop_service_ack_rate_by_opcode": execution[
            "acknowledgement_rate_pct"
        ],
        "harvested_units_by_crop": execution["harvested_units"],
        "harvest_events_by_crop": execution["harvest_events"],
        "mean_units_per_harvest_by_crop": execution["mean_units_per_harvest"],
        "planted_units_by_crop": execution["planted_units"],
        "pass_on_actionable_tile": player["pass_on_actionable_tile"],
        "requested_sell_value_by_item": player["requested_sell_value"],
        "requested_sell_quantity_by_item": player["requested_sell_quantity"],
        "requested_sell_value": player["total_requested_sell_value"],
        "requested_crop_sell_value": player["requested_crop_sell_value"],
        "requested_livestock_sell_value": player[
            "requested_livestock_product_sell_value"
        ],
    }


def _paired_metric(rows: list[dict[str, Any]], metric: str) -> dict[str, float]:
    owner = [float(row["owner"][metric]) for row in rows]
    opponent = [float(row["opponent"][metric]) for row in rows]
    deltas = [left - right for left, right in zip(owner, opponent)]
    return {
        "owner_mean": _mean(owner),
        "owner_median": _median(owner),
        "opponent_mean": _mean(opponent),
        "opponent_median": _median(opponent),
        "mean_delta": _mean(deltas),
        "median_delta": _median(deltas),
    }


def _mean_nested_mapping(
    rows: list[dict[str, Any]], role: str, metric: str
) -> dict[str, float]:
    keys = sorted(
        {
            key
            for row in rows
            for key in row[role].get(metric, {})
        }
    )
    return {
        key: _mean(float(row[role].get(metric, {}).get(key, 0) or 0) for row in rows)
        for key in keys
    }


def _cashflow(raw: dict[str, Any], player_index: int) -> dict[str, float | int]:
    positive = Counter()
    negative = Counter()
    positive_events = Counter()
    negative_events = Counter()
    steps = raw["steps"]
    previous = float(
        steps[0][player_index]["observation"]["farms"][player_index].get(
            "money", 0.0
        )
        or 0.0
    )
    for step in range(1, len(steps)):
        record = steps[step][player_index]
        current = float(
            record["observation"]["farms"][player_index].get("money", 0.0)
            or 0.0
        )
        delta = current - previous
        display_day = int(record["observation"]["day"]) + 1
        phase = "d01_d10" if display_day <= 10 else "d11_d20" if display_day <= 20 else "d21_d30"
        if delta > 0:
            positive[phase] += delta
            positive_events[phase] += 1
        elif delta < 0:
            negative[phase] += -delta
            negative_events[phase] += 1
        previous = current
    total_positive_events = sum(positive_events.values())
    total_negative_events = sum(negative_events.values())
    return {
        "gross_positive_cashflow": round(sum(positive.values()), 3),
        "gross_negative_cashflow": round(sum(negative.values()), 3),
        "gross_positive_cashflow_d01_d10": round(positive["d01_d10"], 3),
        "gross_positive_cashflow_d11_d20": round(positive["d11_d20"], 3),
        "gross_positive_cashflow_d21_d30": round(positive["d21_d30"], 3),
        "gross_negative_cashflow_d01_d10": round(negative["d01_d10"], 3),
        "gross_negative_cashflow_d11_d20": round(negative["d11_d20"], 3),
        "gross_negative_cashflow_d21_d30": round(negative["d21_d30"], 3),
        "positive_cashflow_events": total_positive_events,
        "negative_cashflow_events": total_negative_events,
        "positive_cashflow_events_d21_d30": positive_events["d21_d30"],
        "negative_cashflow_events_d21_d30": negative_events["d21_d30"],
        "positive_cashflow_per_event": round(
            sum(positive.values()) / total_positive_events
            if total_positive_events
            else 0.0,
            3,
        ),
        "positive_cashflow_per_event_d21_d30": round(
            positive["d21_d30"] / positive_events["d21_d30"]
            if positive_events["d21_d30"]
            else 0.0,
            3,
        ),
    }


def build() -> dict[str, Any]:
    episodes: list[dict[str, Any]] = []
    for episode_id in EPISODE_IDS:
        path = REPLAY_DIR / f"{episode_id}.json"
        summary, daily_rows, action_rows = analyze(path)
        raw = json.loads(path.read_text(encoding="utf-8"))
        owner_index = summary["identity"]["players"].index(OWNER)
        opponent_index = 1 - owner_index
        owner = _profile(summary, daily_rows, action_rows, owner_index)
        opponent = _profile(summary, daily_rows, action_rows, opponent_index)
        owner.update(_cashflow(raw, owner_index))
        opponent.update(_cashflow(raw, opponent_index))
        if owner["reward"] >= opponent["reward"]:
            raise ValueError(f"episode {episode_id} is not an owner loss")
        episodes.append(
            {
                "episode_id": episode_id,
                "seed": summary["identity"]["seed"],
                "raw_sha256": _sha256(path),
                "owner_seat": owner_index,
                "opponent_name": opponent["player"],
                "owner_reward": owner["reward"],
                "opponent_reward": opponent["reward"],
                "reward_gap": owner["reward"] - opponent["reward"],
                "owner": owner,
                "opponent": opponent,
            }
        )

    metrics = (
        "reward",
        "money_d10",
        "money_d20",
        "money_d30",
        "money_gain_d20_d30",
        "final_pastures",
        "final_animals",
        "peak_daily_animals",
        "peak_crops",
        "crop_tile_days",
        "late_crop_tile_days",
        "unwatered_tile_days",
        "late_unwatered_tile_days",
        "late_water_stressed_tile_days",
        "weed_exits",
        "starved_to_weed",
        "live_crop_rotations",
        "harvested_units",
        "crop_service_ack",
        "crop_service_ack_rate_pct",
        "productive_actions",
        "move_actions",
        "pass_actions",
        "unit_actions",
        "move_per_productive",
        "pass_share_pct",
        "late_plant",
        "late_water",
        "late_harvest",
        "late_dig",
        "late_move",
        "late_pass",
        "requested_sell_value",
        "requested_crop_sell_value",
        "requested_livestock_sell_value",
        "gross_positive_cashflow",
        "gross_negative_cashflow",
        "gross_positive_cashflow_d21_d30",
        "gross_negative_cashflow_d21_d30",
        "positive_cashflow_events",
        "negative_cashflow_events",
        "positive_cashflow_events_d21_d30",
        "negative_cashflow_events_d21_d30",
        "positive_cashflow_per_event",
        "positive_cashflow_per_event_d21_d30",
    )
    owner_scores = [float(row["owner_reward"]) for row in episodes]
    gaps = [float(row["reward_gap"]) for row in episodes]
    artifact = {
        "schema_version": 1,
        "analysis_id": "E18_16_KAGGLE_LOSS_DIAGNOSTIC_2026_09_04",
        "submission_id": SUBMISSION_ID,
        "owner": OWNER,
        "epistemic_role": "EXTERNAL_DIAGNOSTIC_NOT_HOLDOUT",
        "episodes": episodes,
        "aggregate": {
            "losses": len(episodes),
            "owner_seat_0": sum(row["owner_seat"] == 0 for row in episodes),
            "owner_seat_1": sum(row["owner_seat"] == 1 for row in episodes),
            "unique_seeds": len({row["seed"] for row in episodes}),
            "unique_opponents": len({row["opponent_name"] for row in episodes}),
            "unique_owner_action_streams": len(
                {row["owner"]["action_stream_sha256"] for row in episodes}
            ),
            "owner_topologies": dict(
                sorted(Counter(row["owner"]["topology"] for row in episodes).items())
            ),
            "opponent_topologies": dict(
                sorted(
                    Counter(row["opponent"]["topology"] for row in episodes).items()
                )
            ),
            "owner_reward_mean": _mean(owner_scores),
            "owner_reward_median": _median(owner_scores),
            "opponent_reward_mean": _mean(
                float(row["opponent_reward"]) for row in episodes
            ),
            "mean_loss_margin": _mean(gaps),
            "median_loss_margin": _median(gaps),
            "paired_metrics": {
                metric: _paired_metric(episodes, metric) for metric in metrics
            },
            "owner_mean_harvested_units_by_crop": _mean_nested_mapping(
                episodes, "owner", "harvested_units_by_crop"
            ),
            "opponent_mean_harvested_units_by_crop": _mean_nested_mapping(
                episodes, "opponent", "harvested_units_by_crop"
            ),
            "owner_mean_harvest_events_by_crop": _mean_nested_mapping(
                episodes, "owner", "harvest_events_by_crop"
            ),
            "opponent_mean_harvest_events_by_crop": _mean_nested_mapping(
                episodes, "opponent", "harvest_events_by_crop"
            ),
            "owner_mean_planted_units_by_crop": _mean_nested_mapping(
                episodes, "owner", "planted_units_by_crop"
            ),
            "opponent_mean_planted_units_by_crop": _mean_nested_mapping(
                episodes, "opponent", "planted_units_by_crop"
            ),
            "owner_mean_crop_service_requested_by_opcode": _mean_nested_mapping(
                episodes, "owner", "crop_service_requested_by_opcode"
            ),
            "opponent_mean_crop_service_requested_by_opcode": _mean_nested_mapping(
                episodes, "opponent", "crop_service_requested_by_opcode"
            ),
            "owner_mean_crop_service_ack_by_opcode": _mean_nested_mapping(
                episodes, "owner", "crop_service_ack_by_opcode"
            ),
            "opponent_mean_crop_service_ack_by_opcode": _mean_nested_mapping(
                episodes, "opponent", "crop_service_ack_by_opcode"
            ),
            "owner_mean_pass_on_actionable_tile": _mean_nested_mapping(
                episodes, "owner", "pass_on_actionable_tile"
            ),
            "opponent_mean_pass_on_actionable_tile": _mean_nested_mapping(
                episodes, "opponent", "pass_on_actionable_tile"
            ),
            "owner_mean_requested_sell_value_by_item": _mean_nested_mapping(
                episodes, "owner", "requested_sell_value_by_item"
            ),
            "opponent_mean_requested_sell_value_by_item": _mean_nested_mapping(
                episodes, "opponent", "requested_sell_value_by_item"
            ),
            "owner_mean_requested_sell_quantity_by_item": _mean_nested_mapping(
                episodes, "owner", "requested_sell_quantity_by_item"
            ),
            "opponent_mean_requested_sell_quantity_by_item": _mean_nested_mapping(
                episodes, "opponent", "requested_sell_quantity_by_item"
            ),
        },
        "observability": {
            "replay_actions_are_requested_commands": True,
            "acknowledged_crop_service_is_state_transition_verified": True,
            "external_replays_are_training_evidence_not_holdout": True,
            "paired_opponents_are_heterogeneous_not_a_control_policy": True,
            "causal_counterfactual_not_identifiable": True,
        },
    }
    return artifact


def write_csv(artifact: dict[str, Any]) -> None:
    rows = []
    for episode in artifact["episodes"]:
        owner = episode["owner"]
        opponent = episode["opponent"]
        row = {
            "episode_id": episode["episode_id"],
            "seed": episode["seed"],
            "owner_seat": episode["owner_seat"],
            "opponent": episode["opponent_name"],
            "owner_reward": episode["owner_reward"],
            "opponent_reward": episode["opponent_reward"],
            "reward_gap": episode["reward_gap"],
            "owner_topology": owner["topology"],
            "opponent_topology": opponent["topology"],
        }
        for metric in (
            "final_animals",
            "peak_crops",
            "late_crop_tile_days",
            "late_unwatered_tile_days",
            "weed_exits",
            "live_crop_rotations",
            "harvested_units",
            "crop_service_ack",
            "productive_actions",
            "move_actions",
            "move_per_productive",
            "pass_actions",
            "late_plant",
            "late_water",
            "late_harvest",
            "late_dig",
            "late_move",
            "late_pass",
            "requested_sell_value",
            "gross_positive_cashflow",
            "gross_negative_cashflow",
            "gross_positive_cashflow_d21_d30",
            "gross_negative_cashflow_d21_d30",
            "positive_cashflow_per_event_d21_d30",
        ):
            row[f"owner_{metric}"] = owner[metric]
            row[f"opponent_{metric}"] = opponent[metric]
            row[f"delta_{metric}"] = round(
                float(owner[metric]) - float(opponent[metric]), 4
            )
        rows.append(row)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    artifact = build()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_csv(artifact)
    print(JSON_OUT)
    print(CSV_OUT)


if __name__ == "__main__":
    main()
