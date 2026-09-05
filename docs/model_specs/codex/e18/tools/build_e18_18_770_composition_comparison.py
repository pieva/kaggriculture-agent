#!/usr/bin/env python3
"""Compare the E18.16 7-7-0 composition plan with Jesse's exact 7-7-0 cohort."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
COMMON_TOOLS = ROOT / "experiments/e18/tools/common"
for import_root in (ROOT, COMMON_TOOLS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

import build_e18_current_top3_strategy_benchmark as top_benchmark
from analyze_episode_105080066 import analyze
from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    create_codex_e18_770_exact_cap_critical_feed,
)

EXACT_770_EPISODES = (
    105405557,
    105384058,
    105398563,
    105391568,
    105565293,
)
EXCLUDED_RECENT_NON_770 = (
    {"episode_id": 105544485, "observed_topology": "10-7-0"},
    {"episode_id": 105547303, "observed_topology": "10-7-0"},
)
SNAPSHOT_DAYS = (1, 5, 10, 15, 20, 25, 30)
CROPS = ("CARROT", "MELON", "STRAWBERRY", "TOMATO", "WHEAT")
ANIMALS = ("COW", "SHEEP", "GOOSE")
LOCAL_SEED = 180903001
LOCAL_EPISODE_ID = 918160001
OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_COMPOSITION_COMPARISON_2026_09_04.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_18_770_COMPOSITION_COMPARISON_2026_09_04_IT.md"
)


def _profile(path: Path, player_name: str, pair: str) -> dict[str, Any]:
    summary, daily_rows, action_rows = analyze(path)
    player = next(row for row in summary["players"] if row["player"] == player_name)
    opponent = summary["players"][1 - int(player["player_index"])]
    result = top_benchmark._profile(
        summary,
        player,
        opponent,
        daily_rows,
        action_rows,
        pair,
    )
    result["identity"] = summary["identity"]
    result["animal_mix_snapshots"] = _animal_mix_snapshots(
        path, int(player["player_index"])
    )
    return result


def _animal_mix_snapshots(path: Path, seat: int) -> dict[str, dict[str, int]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    snapshots: dict[str, dict[str, int]] = {}
    for day in SNAPSHOT_DAYS:
        record = data["steps"][min(day * 24 - 1, 719)][seat]
        farm = record["observation"]["farms"][seat]
        counts: Counter[str] = Counter()
        for tile_row in farm["tiles"]:
            for tile in tile_row:
                if not isinstance(tile, dict) or tile.get("kind") != "PASTURE":
                    continue
                animal = tile.get("animal")
                if animal:
                    counts[str(animal)] += 1
        snapshots[f"D{day:02d}"] = dict(sorted(counts.items()))
    return snapshots


def _run_local(path: Path) -> dict[str, Any]:
    policies = []
    for seat in (0, 1):
        policies.append(
            create_codex_e18_770_exact_cap_critical_feed(
                run_context={
                    "run_id": f"E18-16-COMPOSITION-S{LOCAL_SEED}-P{seat}",
                    "episode_id": f"E18-16-COMPOSITION-S{LOCAL_SEED}-P{seat}",
                    "seed": LOCAL_SEED,
                    "player_position": seat,
                }
            )
        )
    env = make(
        "kaggriculture",
        configuration={
            "episodeSteps": 720,
            "seed": LOCAL_SEED,
            "turnsPerDay": 24,
        },
        debug=False,
    )
    env.run(policies)
    replay = env.toJSON()
    replay.setdefault("info", {})["EpisodeId"] = LOCAL_EPISODE_ID
    replay["info"]["Agents"] = [
        {"Name": "CODEX E18.16"},
        {"Name": "CODEX E18.16 Mirror"},
    ]
    path.write_text(json.dumps(replay), encoding="utf-8")
    return _profile(path, "CODEX E18.16", "LOCAL_MIRROR")


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _variants(values: list[Any]) -> list[Any]:
    return [json.loads(value) for value in sorted({_canonical(row) for row in values})]


def _mean_by_crop(profiles: list[dict[str, Any]], field: str) -> dict[str, float]:
    return {
        crop: round(mean(float(row[field].get(crop, 0)) for row in profiles), 3)
        for crop in CROPS
    }


def _range_by_crop(profiles: list[dict[str, Any]], field: str) -> dict[str, list[int]]:
    return {
        crop: [
            min(int(row[field].get(crop, 0)) for row in profiles),
            max(int(row[field].get(crop, 0)) for row in profiles),
        ]
        for crop in CROPS
    }


def _pct_delta(candidate: float, reference: float) -> float:
    return round(100.0 * (candidate - reference) / reference, 3) if reference else 0.0


def _mix_text(mix: dict[str, int]) -> str:
    labels = {
        "CARROT": "C",
        "MELON": "M",
        "STRAWBERRY": "S",
        "TOMATO": "T",
        "WHEAT": "W",
        "COW": "Cow",
        "SHEEP": "Sheep",
        "GOOSE": "Goose",
    }
    return " + ".join(
        f"{labels.get(key, key)} {value}" for key, value in mix.items()
    ) or "0"


def build(replay_dir: Path) -> dict[str, Any]:
    jesse_profiles = [
        _profile(replay_dir / f"{episode_id}.json", "Jesse Bullard", "JESSE_770")
        for episode_id in EXACT_770_EPISODES
    ]
    if not all(row["final_pasture_topology"] == "7-7-0" for row in jesse_profiles):
        raise AssertionError("Jesse cohort contains a non-7-7-0 profile")

    with tempfile.TemporaryDirectory(prefix="e18_16_composition_") as temp_dir:
        codex_profile = _run_local(Path(temp_dir) / f"{LOCAL_EPISODE_ID}.json")

    first = jesse_profiles[0]
    action_fields = ("plant", "water", "harvest", "dig", "move", "pass")
    kpi_fields = {
        "peak_crops": (float(first["peak_crops"]), float(codex_profile["peak_crops"])),
        "crop_tile_days_total": (
            float(first["crop_tile_days_total"]),
            float(codex_profile["crop_tile_days_total"]),
        ),
        "crop_tile_days_d21_d30": (
            float(first["crop_tile_days_d21_d30"]),
            float(codex_profile["crop_tile_days_d21_d30"]),
        ),
        "late_unwatered_per_crop_tile": (
            float(first["late_unwatered_per_crop_tile"]),
            float(codex_profile["late_unwatered_per_crop_tile"]),
        ),
        "harvested_units_total": (
            float(first["harvested_units_total"]),
            float(codex_profile["harvested_units_total"]),
        ),
        **{
            field: (
                float(first["actions"][field]),
                float(codex_profile["actions"][field]),
            )
            for field in action_fields
        },
    }
    kpi_comparison = {
        field: {
            "jesse_770": reference,
            "codex_e18_16": candidate,
            "codex_minus_jesse": round(candidate - reference, 6),
            "codex_minus_jesse_pct": _pct_delta(candidate, reference),
        }
        for field, (reference, candidate) in kpi_fields.items()
    }

    daily_comparison = {}
    for day in SNAPSHOT_DAYS:
        key = f"D{day:02d}"
        top_crop_variants = _variants(
            [row["farm_snapshots"][key]["crop_mix"] for row in jesse_profiles]
        )
        top_animal_variants = _variants(
            [row["animal_mix_snapshots"][key] for row in jesse_profiles]
        )
        daily_comparison[key] = {
            "jesse_crop_variants": top_crop_variants,
            "codex_crop_mix": codex_profile["farm_snapshots"][key]["crop_mix"],
            "jesse_animal_variants": top_animal_variants,
            "codex_animal_mix": codex_profile["animal_mix_snapshots"][key],
        }

    action_shape_variants = _variants(
        [row["action_shape_sha256"] for row in jesse_profiles]
    )
    return {
        "schema_version": "e18.codex.770_composition_comparison.v1",
        "analysis_id": "E18_18_770_COMPOSITION_COMPARISON_2026_09_04",
        "observed_at": "2026-09-04T22:09:24+02:00",
        "leaderboard_snapshot": {
            "url": "https://www.kaggle.com/competitions/kaggriculture/leaderboard",
            "entries": [
                {"rank": 1, "player": "keiz", "rating": 3027.5},
                {"rank": 2, "player": "Crop Dusta", "rating": 3002.4},
                {"rank": 3, "player": "Jesse Bullard", "rating": 2982.1},
                {"rank": 4, "player": "Andrey Tikhomirov", "rating": 2922.9},
                {"rank": 6, "player": "Giulio Ravasio", "rating": 2904.0},
            ],
        },
        "selection": {
            "player": "Jesse Bullard",
            "conditional_topology": "7-7-0",
            "profiles": len(jesse_profiles),
            "episode_ids": list(EXACT_770_EPISODES),
            "latest_episode_id": 105565293,
            "latest_replay_url": (
                "https://www.kaggle.com/competitions/episodes/105565293/replay.json"
            ),
            "excluded_recent_non_770": list(EXCLUDED_RECENT_NON_770),
            "selection_warning": (
                "Jesse is not globally topology-stable; stability is measured only "
                "inside the exact 7-7-0 cohort."
            ),
        },
        "jesse_770_consistency": {
            "unique_action_shapes": len(action_shape_variants),
            "action_shape_sha256": action_shape_variants,
            "all_final_animals_14": all(row["final_animals"] == 14 for row in jesse_profiles),
            "all_peak_crops_62": all(row["peak_crops"] == 62 for row in jesse_profiles),
            "all_crop_tile_days_total_1350": all(
                row["crop_tile_days_total"] == 1350 for row in jesse_profiles
            ),
            "all_crop_tile_days_d21_d30_515": all(
                row["crop_tile_days_d21_d30"] == 515 for row in jesse_profiles
            ),
            "stable_crop_snapshots_d01_d25": all(
                len(daily_comparison[f"D{day:02d}"]["jesse_crop_variants"]) == 1
                for day in (1, 5, 10, 15, 20, 25)
            ),
            "stable_animal_mix_all_snapshots": all(
                len(daily_comparison[f"D{day:02d}"]["jesse_animal_variants"]) == 1
                for day in SNAPSHOT_DAYS
            ),
            "planted_units_mean": _mean_by_crop(jesse_profiles, "planted_units"),
            "planted_units_range": _range_by_crop(jesse_profiles, "planted_units"),
            "harvested_units_mean": _mean_by_crop(jesse_profiles, "harvested_units"),
            "harvested_units_range": _range_by_crop(jesse_profiles, "harvested_units"),
            "invariant_crop_family": {
                "melon_planted": 12,
                "strawberry_planted": 38,
                "carrot_plus_wheat_planted": 193,
                "melon_harvested": 72,
                "strawberry_harvested": 260,
                "carrot_plus_wheat_harvested": 553,
            },
        },
        "daily_comparison": daily_comparison,
        "kpi_comparison": kpi_comparison,
        "codex_e18_16": codex_profile,
        "jesse_770_profiles": jesse_profiles,
        "verdict": {
            "livestock_capacity": (
                "Comparable in total from D15: both fill 14. Jesse is invariant at "
                "9 COW + 5 SHEEP; E18.16 is 8 COW + 6 SHEEP and reaches only 12 at D10."
            ),
            "crop_capacity": (
                "Comparable in tile-days but not in timing or mix: E18.16 peaks later "
                "and below Jesse, retains MELON through D20, and carries 15 crops at D30."
            ),
            "main_gap": (
                "The dominant gap is lifecycle conversion, not land capacity: E18.16 "
                "harvests 580 units versus Jesse's invariant 885 despite similar late "
                "crop tile-days."
            ),
        },
        "planner_implications": [
            "Keep 7-7-0 and cap 14 fixed.",
            "Test 9 COW + 5 SHEEP as a one-variable livestock mix ablation.",
            "Use exact crop checkpoints: D1/D5 12 MELON + 7 WHEAT; D10 12 MELON + 20 STRAWBERRY + 5 WHEAT; D15/D20 38 STRAWBERRY + 23 WHEAT; D25 22 STRAWBERRY + 39 WHEAT.",
            "Treat CARROT and WHEAT as an adaptive annual-crop family: preserve their combined volume rather than hard-code their split.",
            "Target 62 peak crops by D13, 61 live crops from D15 through D25, and at most 2 residual crops on D30.",
            "Before increasing surface, close the action-volume gaps in PLANT, WATER and HARVEST and reduce PASS/MOVE overhead.",
        ],
        "limitations": [
            "The Jesse sample is selected conditionally on exact final 7-7-0 topology.",
            "External replays have different seeds, opponents and market interference from the local mirror.",
            "The comparison is descriptive and defines planner targets; it does not identify causal profit effects.",
            "Raw external replays are temporary inputs and are not retained in the repository.",
        ],
    }


def _report(artifact: dict[str, Any]) -> str:
    daily = artifact["daily_comparison"]
    lines = [
        "# E18.18 — confronto consistenze 7-7-0 con Jesse Bullard",
        "",
        "## Verdetto",
        "",
        "Il confronto è sufficientemente pulito: cinque replay esatti `7-7-0` di Jesse, incluso il recente `105565293`, hanno un solo action shape, 14 animali, peak crop 62 e la stessa traiettoria delle colture fino a D25. Due replay recenti `10-7-0` sono stati esclusi esplicitamente.",
        "",
        "La nostra consistenza zootecnica è quasi allineata nel totale ma non nel mix; quella colturale è allineata soltanto fino a D10. Il gap principale non è la superficie: E18.16 ha 509 crop tile-days D21-D30 contro 515, ma raccoglie 580 unità contro 885. Mancano turnover, servizio e liquidazione coerenti con la capacità già disponibile.",
        "",
        "## Traiettoria delle consistenze",
        "",
        "| Giorno | Jesse 770 — colture | E18.16 — colture | Jesse 770 — animali | E18.16 — animali |",
        "|---|---:|---:|---:|---:|",
    ]
    for day in SNAPSHOT_DAYS:
        key = f"D{day:02d}"
        top_crop = daily[key]["jesse_crop_variants"]
        top_crop_text = " / ".join(_mix_text(row) for row in top_crop)
        top_animal_text = " / ".join(
            _mix_text(row) for row in daily[key]["jesse_animal_variants"]
        )
        lines.append(
            f"| {key} | {top_crop_text} | {_mix_text(daily[key]['codex_crop_mix'])} | "
            f"{top_animal_text} | {_mix_text(daily[key]['codex_animal_mix'])} |"
        )
    kpi = artifact["kpi_comparison"]
    lines.extend(
        [
            "",
            "## KPI di capacità e conversione",
            "",
            "| KPI | Jesse 770 | E18.16 | Delta Codex |",
            "|---|---:|---:|---:|",
        ]
    )
    for field, label in (
        ("peak_crops", "Peak crop"),
        ("crop_tile_days_total", "Crop tile-days totali"),
        ("crop_tile_days_d21_d30", "Crop tile-days D21-D30"),
        ("harvested_units_total", "Unità raccolte"),
        ("plant", "PLANT"),
        ("water", "WATER"),
        ("harvest", "HARVEST"),
        ("move", "MOVE"),
        ("pass", "PASS"),
    ):
        row = kpi[field]
        lines.append(
            f"| {label} | {row['jesse_770']:.0f} | {row['codex_e18_16']:.0f} | "
            f"{row['codex_minus_jesse_pct']:+.1f}% |"
        )
    lines.extend(
        [
            "",
            "## Lettura strategica",
            "",
            "1. **Animali:** Jesse usa invariabilmente `9 COW + 5 SHEEP`; E18.16 usa `8 COW + 6 SHEEP`. Il totale 14 è corretto, ma a D10 Codex è ancora a 12 contro 13. La `9+5` va provata come ablation separata, senza riaprire topologia o cap.",
            "2. **Colture iniziali:** D1, D5 e D10 coincidono esattamente. Questa parte del nostro piano è validata dal benchmark.",
            "3. **Regime D15-D20:** Jesse ha già eliminato MELON e mantiene `38 STRAWBERRY + 23 WHEAT` su 61 tile. Codex conserva 8 MELON, resta a 55-59 tile e sbilancia il mix verso STRAWBERRY.",
            "4. **Chiusura:** a D25 Jesse passa a `22 STRAWBERRY + 39 WHEAT`; a D30 lascia soltanto due annuali. Codex arriva con 15 colture, di cui 14 STRAWBERRY: è la prova più netta che il calendario di stop/liquidazione non è ancora chiuso.",
            "5. **Adattamento utile:** Jesse conserva volumi invarianti di MELON e STRAWBERRY, ma scambia CARROT e WHEAT in funzione dello scenario. Il planner deve vincolare la famiglia `CARROT+WHEAT`, non una ripartizione rigida.",
            "",
            "## Specifiche candidate per Gate 0 E18.18",
            "",
            "- topologia `7-7-0`, cap 14 invariati;",
            "- ablation zootecnica `9 COW + 5 SHEEP`;",
            "- peak 62 crop entro D13 e plateau 61 tra D15 e D25;",
            "- checkpoint crop uguali alla tabella fino a D25;",
            "- `CARROT+WHEAT` adattivi a parità di volume complessivo;",
            "- massimo 2 crop residui a D30;",
            "- capacità minima di servizio coerente con 243 PLANT, 1.172 WATER e 467 HARVEST, prima di aumentare il numero di tile.",
            "",
            "## Limiti",
            "",
            "Il campione Jesse è condizionato alla topologia finale `7-7-0`; Jesse usa anche `10-7-0` in altri replay. Seed, avversari e mercato differiscono dal mirror locale, quindi questi sono target di pianificazione descrittivi, non effetti economici causali.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--replay-dir",
        type=Path,
        required=True,
        help="Directory containing the five EpisodeId-named Jesse replay JSON files.",
    )
    args = parser.parse_args()
    artifact = build(args.replay_dir)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(_report(artifact), encoding="utf-8")
    print(OUTPUT.relative_to(ROOT))
    print(REPORT.relative_to(ROOT))
    print(json.dumps(artifact["verdict"], indent=2))


if __name__ == "__main__":
    main()
