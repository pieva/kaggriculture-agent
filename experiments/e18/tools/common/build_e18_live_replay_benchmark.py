"""Build the E18 lifecycle benchmark from owner-acquired Kaggle replays."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from analyze_episode_105080066 import analyze

ROOT = Path(__file__).resolve().parents[4]
REPLAY_DIR = ROOT / "data" / "replays" / "json"
OUT = ROOT / "experiments" / "e18" / "artifacts" / "discovery"
ARTIFACT = OUT / "E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_V1.json"
CSV_PATH = OUT / "E18_LIVE_TOP3_AND_CODEX_REPLAY_PROFILES_V1.csv"

CORPUS = (
    {
        "episode_id": 105080066,
        "cohort": "CODEX_662_EXTERNAL",
        "target": "Pietro Valocchi",
        "sha256": "7AAEE0B4F43FFA5187C37FE8AEFF3FB9892D482CA20506C69B0C905552513F2C",
    },
    {
        "episode_id": 105084394,
        "cohort": "CODEX_662_EXTERNAL",
        "target": "Pietro Valocchi",
        "sha256": "92715897D1D4EA495893C4ACEA757DE2B92AD5C422ABFF2CA32D5A3595911F5D",
    },
    {
        "episode_id": 105075696,
        "cohort": "CODEX_662_EXTERNAL",
        "target": "Pietro Valocchi",
        "sha256": "516A4F8C218CCB7307BD5AF8860D1068A1A5571E609D8FF6175CB1BD4556B514",
    },
    {
        "episode_id": 105089826,
        "cohort": "LIVE_TOP3_TARGET",
        "target": "Crop Dusta",
        "sha256": "AEECD456138E4D68AA4B6B8A45D87EEB5C3E65854ADE950775B55A198674AF39",
    },
    {
        "episode_id": 105088610,
        "cohort": "LIVE_TOP3_TARGET",
        "target": "3정훈",
        "sha256": "F91D6DB6D6060DA2B930EA519C453C2BE33DA4ABA3C1731DC66C9D1B1F622AC3",
    },
    {
        "episode_id": 105090557,
        "cohort": "LIVE_TOP3_TARGET",
        "target": "sbol ball",
        "sha256": "4070E283C0BA385BA5B70B68DCCD5127751A1ABDE157C3E26FE1FDC4EA1793B2",
    },
    {
        "episode_id": 105100853,
        "cohort": "LIVE_TOP3_TARGET",
        "target": "Crop Dusta",
        "sha256": "16005ED98E9E8ACA878F69C0335311E26CEE385635F00730ABDC895E065327A7",
    },
    {
        "episode_id": 105101421,
        "cohort": "LIVE_TOP3_TARGET",
        "target": "3정훈",
        "sha256": "CC67346508AE25E28EA383921858019FD6F1C99E1D8AD21C8DB507F9656FD1E9",
    },
    {
        "episode_id": 105102327,
        "cohort": "LIVE_TOP3_TARGET",
        "target": "sbol ball",
        "sha256": "38BE4D52332E78E655C3D2F846E14D7BB7D2F9D7EF79B4966C446A00AD7E53AE",
    },
    {
        "episode_id": 105107425,
        "cohort": "LIVE_TOP3_TARGET",
        "target": "3정훈",
        "sha256": "DEAA14B2DDC296960C523ECE827FFC8059CC539736500D3A3761C8F74151CB81",
    },
    {
        "episode_id": 105107748,
        "cohort": "LIVE_TOP3_TARGET",
        "target": "sbol ball",
        "sha256": "5B12DFC3D46647D2D290B31E3B6C052FB877AF0624D60B966378B7F89C484ABA",
    },
)

LIFECYCLE_FINGERPRINT_FIELDS = (
    "first_three_quadrants_display_day",
    "final_pastures",
    "final_animals",
    "final_pasture_topology",
    "peak_crops",
    "peak_crop_first_display_day",
    "crop_tile_days_d21_d30",
    "unwatered_tile_days_d21_d30",
    "weed_exits",
    "starved_to_weed",
    "live_crop_rotations",
    "harvested_units_total",
    "harvested_wheat_units",
    "harvested_strawberry_units",
    "harvested_melon_units",
    "wheat_harvest_events",
    "mean_wheat_units_per_harvest",
    "last_acked_plant_display_day",
    "last_acked_water_display_day",
    "last_acked_harvest_display_day",
    "d21_d30_plant_commands",
    "d21_d30_water_commands",
    "d21_d30_harvest_commands",
    "final_crops",
    "final_weeds",
    "final_crop_mix",
)


def _count(mapping: dict[str, Any], key: str) -> int:
    return int(mapping.get(key, 0) or 0)


def _last_ack_day(execution: dict[str, Any], opcode: str) -> int | None:
    days = [
        int(day)
        for day, counts in execution["acknowledged_by_display_day"].items()
        if _count(counts, opcode) > 0
    ]
    return max(days) if days else None


def _sha256_json(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest().upper()


def _profile(
    *,
    summary: dict[str, Any],
    player: dict[str, Any],
    opponent: dict[str, Any],
    cohort: str,
    target: bool,
) -> dict[str, Any]:
    transitions = player["transition_metrics"]["counts"]
    execution = player["crop_action_execution"]
    final = player["late_daily"][-1]
    topology = player["final_topology"]["pasture_by_quadrant"]
    wheat_events = _count(execution["harvest_events"], "WHEAT")
    wheat_units = _count(execution["harvested_units"], "WHEAT")
    profile = {
        "episode_id": summary["identity"]["episode_id"],
        "seed": summary["identity"]["seed"],
        "cohort": cohort,
        "is_target_profile": target,
        "player_index": player["player_index"],
        "player": player["player"],
        "opponent": opponent["player"],
        "score": player["final_reward"],
        "opponent_score": opponent["final_reward"],
        "margin": player["final_reward"] - opponent["final_reward"],
        "outcome": "WIN" if player["final_reward"] > opponent["final_reward"] else "LOSS",
        "action_stream_sha256": player["action_stream_sha256"],
        "first_three_quadrants_display_day": player[
            "first_three_quadrants_display_day"
        ],
        "final_pastures": player["final_topology"]["pastures"],
        "final_animals": player["final_topology"]["animals"],
        "final_pasture_topology": "-".join(
            str(_count(topology, quadrant)) for quadrant in ("Q0", "Q1", "Q2")
        ),
        "final_q2_pastures": _count(topology, "Q2"),
        "peak_crops": player["peak_crops"],
        "peak_crop_first_display_day": player["peak_crop_display_days"][0],
        "crop_tile_days_d21_d30": player["crop_tile_days_d21_d30"],
        "unwatered_tile_days_d21_d30": player["unwatered_tile_days_d21_d30"],
        "weed_exits": _count(transitions, "expired_to_weed")
        + _count(transitions, "starved_to_weed"),
        "starved_to_weed": _count(transitions, "starved_to_weed"),
        "live_crop_rotations": _count(transitions, "dug_up_crop"),
        "harvested_units_total": execution["harvested_units_total"],
        "harvested_wheat_units": wheat_units,
        "harvested_strawberry_units": _count(
            execution["harvested_units"], "STRAWBERRY"
        ),
        "harvested_melon_units": _count(execution["harvested_units"], "MELON"),
        "wheat_harvest_events": wheat_events,
        "mean_wheat_units_per_harvest": round(
            wheat_units / wheat_events if wheat_events else 0.0, 3
        ),
        "last_acked_plant_display_day": _last_ack_day(execution, "PLANT"),
        "last_acked_water_display_day": _last_ack_day(execution, "WATER"),
        "last_acked_harvest_display_day": _last_ack_day(execution, "HARVEST"),
        "d21_d30_plant_commands": player["d21_d30_actions"]["plant"],
        "d21_d30_water_commands": player["d21_d30_actions"]["water"],
        "d21_d30_harvest_commands": player["d21_d30_actions"]["harvest"],
        "final_crops": final["crops"],
        "final_weeds": final["weeds"],
        "final_crop_mix": final["crop_mix"],
        "raw_sha256": summary["identity"]["raw_sha256"],
    }
    profile["lifecycle_fingerprint_sha256"] = _sha256_json(
        {field: profile[field] for field in LIFECYCLE_FINGERPRINT_FIELDS}
    )
    return profile


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    outcomes = Counter(row["outcome"] for row in rows)
    return {
        "profiles": len(rows),
        "unique_lifecycle_profiles": len(
            {row["lifecycle_fingerprint_sha256"] for row in rows}
        ),
        "unique_action_streams": len({row["action_stream_sha256"] for row in rows}),
        "all_q2_zero": all(row["final_q2_pastures"] == 0 for row in rows),
        "q2_zero_profiles": sum(row["final_q2_pastures"] == 0 for row in rows),
        "unique_pasture_topologies": len(
            {row["final_pasture_topology"] for row in rows}
        ),
        "wins": outcomes["WIN"],
        "losses": outcomes["LOSS"],
        "mean_score": mean(row["score"] for row in rows),
        "mean_margin": mean(row["margin"] for row in rows),
        "target_100k_attainment": sum(row["score"] >= 100000 for row in rows),
        "mean_peak_crops": mean(row["peak_crops"] for row in rows),
        "mean_crop_tile_days_d21_d30": mean(
            row["crop_tile_days_d21_d30"] for row in rows
        ),
        "mean_unwatered_tile_days_d21_d30": mean(
            row["unwatered_tile_days_d21_d30"] for row in rows
        ),
        "mean_weed_exits": mean(row["weed_exits"] for row in rows),
        "mean_live_crop_rotations": mean(row["live_crop_rotations"] for row in rows),
        "mean_harvested_units_total": mean(
            row["harvested_units_total"] for row in rows
        ),
        "mean_harvested_wheat_units": mean(
            row["harvested_wheat_units"] for row in rows
        ),
        "mean_wheat_units_per_harvest": mean(
            row["mean_wheat_units_per_harvest"] for row in rows
        ),
    }


def build() -> dict[str, Any]:
    profiles: list[dict[str, Any]] = []
    corpus_rows = []
    for replay in CORPUS:
        episode_id = int(replay["episode_id"])
        summary, _daily, _actions = analyze(
            REPLAY_DIR / f"{episode_id}.json",
            expected_sha256=str(replay["sha256"]),
        )
        target_index = next(
            player["player_index"]
            for player in summary["players"]
            if player["player"] == replay["target"]
        )
        for player in summary["players"]:
            opponent = summary["players"][1 - player["player_index"]]
            profiles.append(
                _profile(
                    summary=summary,
                    player=player,
                    opponent=opponent,
                    cohort=str(replay["cohort"]),
                    target=player["player_index"] == target_index,
                )
            )
        corpus_rows.append(
            {
                "episode_id": episode_id,
                "seed": summary["identity"]["seed"],
                "players": summary["identity"]["players"],
                "rewards": summary["identity"]["rewards"],
                "target": replay["target"],
                "target_seat": target_index,
                "cohort": replay["cohort"],
                "raw_sha256": replay["sha256"],
            }
        )
    targets = [row for row in profiles if row["is_target_profile"]]
    cohorts = {
        cohort: _aggregate([row for row in targets if row["cohort"] == cohort])
        for cohort in sorted({row["cohort"] for row in targets})
    }
    top3_targets = [row for row in targets if row["cohort"] == "LIVE_TOP3_TARGET"]
    return {
        "schema_version": 1,
        "benchmark_id": "E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_V1",
        "epistemic_role": "E18_TRAINING_EVIDENCE",
        "corpus": corpus_rows,
        "profiles": profiles,
        "target_profiles": targets,
        "cohort_aggregates": cohorts,
        "top3_agent_aggregates": {
            player: _aggregate([row for row in top3_targets if row["player"] == player])
            for player in sorted({row["player"] for row in top3_targets})
        },
        "online_observability": {
            "opponent_public_farm": True,
            "opponent_private_inventory": False,
            "submission_rating": False,
            "opponent_rating": False,
            "agent_identity": False,
            "cross_episode_state_contract": False,
        },
        "limitations": [
            "The three live Top-3 teams have two replays each.",
            "Leaderboard rating and episode money are different quantities.",
            "The sample is discovery evidence, not a causal or holdout estimate.",
            "Seat is still unbalanced for 3정훈 and sbol ball in the acquired sample.",
        ],
    }


def _write_csv(rows: list[dict[str, Any]]) -> None:
    serializable = [
        {
            key: json.dumps(value, sort_keys=True) if isinstance(value, dict) else value
            for key, value in row.items()
        }
        for row in rows
    ]
    with CSV_PATH.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(serializable[0]))
        writer.writeheader()
        writer.writerows(serializable)


def main() -> None:
    artifact = build()
    OUT.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    _write_csv(artifact["profiles"])
    print(ARTIFACT.relative_to(ROOT))
    for cohort, values in artifact["cohort_aggregates"].items():
        print(
            f"{cohort}: score={values['mean_score']:.2f} "
            f"harvest={values['mean_harvested_units_total']:.2f} "
            f"weed_exits={values['mean_weed_exits']:.2f}"
        )


if __name__ == "__main__":
    main()
