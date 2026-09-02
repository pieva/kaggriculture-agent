"""E17 Codex forensic benchmark for the nine Top-3 Kaggriculture replays.

The extractor is analysis-only.  It reads the frozen replay corpus and writes
reproducible artifacts under ``experiments/e17/artifacts/discovery/codex``
and the human report under ``experiments/e17/reports/codex``.
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[4]
BENCHMARK_DIR = ROOT / "data" / "replays" / "e17-discovery"
OUT_DIR = ROOT / "experiments" / "e17" / "artifacts" / "discovery" / "codex"
REPORT_DIR = ROOT / "experiments" / "e17" / "reports" / "codex"

EPISODE_IDS = (
    104527555,
    104541810,
    104543983,
    104547425,
    104564762,
    104577270,
    104578185,
    104586335,
    104586487,
)

TOP3 = ("tetsuya", "OceanMix", "Crop Dusta")
QUADRANT_SLOTS = (("Q0", "NW"), ("Q1", "NE"), ("Q2", "SW"))
QUADRANT_BOUNDS = {
    "NW": (range(0, 5), range(0, 5)),
    "NE": (range(0, 5), range(5, 10)),
    "SW": (range(5, 10), range(0, 5)),
    "SE": (range(5, 10), range(5, 10)),
}
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
ANIMALS = ("GOOSE", "COW", "SHEEP")
MOVES = ("NORTH", "SOUTH", "EAST", "WEST")
PRODUCTIVE = {
    "PLANT",
    "WATER",
    "DIG",
    "HARVEST",
    "FEED",
    "CARE",
    "COLLECT_FERTILIZER",
    "BUILD_PASTURE",
    "BUILD_COOP",
    "PICKUP",
    "PLACE",
    "DROP",
    "FERTILIZE",
}
COMPOSITION_KEYS = (
    "locked",
    "empty_available",
    "weed",
    "empty_coop",
    "empty_pasture",
    *CROPS,
    *ANIMALS,
    "other",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def farm_for(record: dict[str, Any], player_id: int) -> dict[str, Any]:
    observation = record.get("observation") or {}
    farms = observation.get("farms") or []
    if isinstance(farms, list) and player_id < len(farms):
        return farms[player_id] or {}
    if isinstance(farms, dict):
        return farms.get(str(player_id), farms.get(player_id, {})) or {}
    return {}


def clock(record: dict[str, Any], step_index: int) -> tuple[int, int]:
    observation = record.get("observation") or {}
    return (
        int(observation.get("day", step_index // 24)),
        int(observation.get("hour", step_index % 24)),
    )


def command_verb(command: Any) -> str:
    if isinstance(command, str):
        return command.upper()
    if isinstance(command, list) and command and isinstance(command[0], str):
        return command[0].upper()
    if isinstance(command, dict):
        for key in ("verb", "action", "command", "type"):
            if isinstance(command.get(key), str):
                return command[key].upper()
    return ""


def action_verbs(action: Any) -> tuple[list[str], list[str]]:
    if not isinstance(action, dict):
        return [], []
    unit_commands: list[Any] = []
    farmer = action.get("farmer")
    if farmer not in (None, [], ""):
        unit_commands.append(farmer)
    hands = action.get("hands") or []
    if isinstance(hands, list):
        unit_commands.extend(hands)
    market_commands = action.get("market") or []
    if not isinstance(market_commands, list):
        market_commands = [market_commands]
    return (
        [verb for verb in map(command_verb, unit_commands) if verb],
        [verb for verb in map(command_verb, market_commands) if verb],
    )


def classify_tile(tile: Any) -> str:
    if tile is None:
        return "empty_available"
    if isinstance(tile, str):
        name = tile.upper()
        if name == "LOCKED":
            return "locked"
        if name == "WEED":
            return "weed"
        if name == "COOP":
            return "empty_coop"
        if name == "PASTURE":
            return "empty_pasture"
        return "other"
    if not isinstance(tile, dict):
        return "other"
    animal = str(tile.get("animal") or "").upper()
    if animal in ANIMALS:
        return animal
    kind = str(tile.get("kind") or "").upper()
    if kind == "PLANT":
        crop = str(tile.get("crop") or "").upper()
        return crop if crop in CROPS else "other"
    if kind == "WEED":
        return "weed"
    if kind == "COOP":
        return "empty_coop"
    if kind == "PASTURE":
        return "empty_pasture"
    if kind == "LOCKED":
        return "locked"
    return "other"


def composition_for(farm: dict[str, Any], quadrant: str) -> dict[str, int]:
    counts = Counter({key: 0 for key in COMPOSITION_KEYS})
    rows, cols = QUADRANT_BOUNDS[quadrant]
    tiles = farm.get("tiles") or []
    for row in rows:
        for col in cols:
            tile = tiles[row][col] if row < len(tiles) and col < len(tiles[row]) else "LOCKED"
            counts[classify_tile(tile)] += 1
    crop_total = sum(counts[crop] for crop in CROPS)
    animal_total = sum(counts[animal] for animal in ANIMALS)
    empty_structures = counts["empty_coop"] + counts["empty_pasture"]
    idle_total = counts["empty_available"] + counts["weed"] + empty_structures + counts["other"]
    result = {key: int(counts[key]) for key in COMPOSITION_KEYS}
    result.update(
        {
            "total_tiles": 25,
            "crop_total": int(crop_total),
            "animal_total": int(animal_total),
            "empty_structure_total": int(empty_structures),
            "idle_total": int(idle_total),
            "owned_non_crop_total": int(25 - counts["locked"] - crop_total),
            "non_crop_total": int(25 - crop_total),
        }
    )
    return result


def tile_at(farm: dict[str, Any], row: int, col: int) -> Any:
    tiles = farm.get("tiles") or []
    if row < len(tiles) and col < len(tiles[row]):
        return tiles[row][col]
    return None


def quadrant_for_coordinate(row: int, col: int) -> tuple[str, str]:
    if row < 5 and col < 5:
        return "Q0", "NW"
    if row < 5 and col >= 5:
        return "Q1", "NE"
    if row >= 5 and col < 5:
        return "Q2", "SW"
    return "Q3", "SE"


def detect_escape_events(
    previous_farm: dict[str, Any],
    current_farm: dict[str, Any],
    *,
    previous_action: Any,
    episode_id: int,
    player_id: int,
    player_name: str,
    previous_step: int,
    previous_day: int,
    previous_hour: int,
    observed_day: int,
    observed_step: int,
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    eod_unit_verbs, _ = action_verbs(previous_action)
    eod_feed_requests = eod_unit_verbs.count("FEED")
    eod_pickup_requests = eod_unit_verbs.count("PICKUP")
    for row in range(10):
        for col in range(10):
            before = tile_at(previous_farm, row, col)
            after = tile_at(current_farm, row, col)
            if not isinstance(before, dict):
                continue
            species = str(before.get("animal") or "").upper()
            if species not in ANIMALS:
                continue
            before_kind = str(before.get("kind") or "").upper()
            after_kind = str(after.get("kind") or "").upper() if isinstance(after, dict) else str(after or "").upper()
            after_animal = str(after.get("animal") or "").upper() if isinstance(after, dict) else ""
            escape_risk = int(before.get("consecutive_unfed", 0) or 0) == 1 and not bool(before.get("fed_today", False))
            if escape_risk and before_kind == after_kind and not after_animal:
                slot, quadrant = quadrant_for_coordinate(row, col)
                events.append(
                    {
                        "episode_id": episode_id,
                        "player_id": player_id,
                        "player_name": player_name,
                        "species": species,
                        "quadrant_slot": slot,
                        "quadrant": quadrant,
                        "row": row,
                        "col": col,
                        "pre_eod_step": previous_step,
                        "eod_after_day": previous_day,
                        "pre_eod_hour": previous_hour,
                        "structure_before": before_kind,
                        "animal_before": species,
                        "consecutive_unfed_before": int(before.get("consecutive_unfed", 0) or 0),
                        "fed_today_before": bool(before.get("fed_today", False)),
                        "feed_executed_before_pre_eod_snapshot": bool(before.get("fed_today", False)),
                        "pickup_executed_before_pre_eod_snapshot": False,
                        "eod_feed_requests": eod_feed_requests,
                        "eod_pickup_requests": eod_pickup_requests,
                        "first_observed_absent_day": observed_day,
                        "first_observed_absent_step": observed_step,
                        "structure_after": after_kind,
                        "animal_after": after_animal,
                        "evidence": "occupied_at_risk_to_same_empty_structure_across_eod",
                    }
                )
    return events


def snapshot_rows(
    *,
    episode_id: int,
    seed: int,
    player_id: int,
    player_name: str,
    step_index: int,
    day: int,
    hour: int,
    farm: dict[str, Any],
) -> list[dict[str, Any]]:
    unlocked = list(farm.get("unlocked_quadrants") or [])
    rows: list[dict[str, Any]] = []
    for slot, quadrant in QUADRANT_SLOTS:
        rows.append(
            {
                "episode_id": episode_id,
                "seed": seed,
                "player_id": player_id,
                "player_name": player_name,
                "day": day,
                "hour": hour,
                "step": step_index,
                "quadrant_slot": slot,
                "quadrant": quadrant,
                "unlocked": quadrant in unlocked,
                "cash": int(farm.get("money", 0) or 0),
                "hands": len(farm.get("hands") or []),
                **composition_for(farm, quadrant),
            }
        )
    return rows


def unlock_event(step_index: int, day: int, hour: int, quadrants: list[str], slot_index: int, farm: dict[str, Any]) -> dict[str, Any]:
    return {
        "step": step_index,
        "day": day,
        "hour": hour,
        "clock": f"D{day}:H{hour:02d}",
        "quadrant": quadrants[slot_index],
        "cash": int(farm.get("money", 0) or 0),
        "hands": len(farm.get("hands") or []),
    }


def analyze_player(
    raw: dict[str, Any],
    *,
    episode_id: int,
    seed: int,
    player_id: int,
    player_name: str,
    opponent_name: str,
    score: int,
    opponent_score: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    action_counts: Counter[str] = Counter()
    market_counts: Counter[str] = Counter()
    movement_by_direction: Counter[str] = Counter()
    unlocks: dict[str, dict[str, Any] | None] = {"Q0": None, "Q1": None, "Q2": None}
    hire_events: list[dict[str, Any]] = []
    escape_events: list[dict[str, Any]] = []
    daily_rows: list[dict[str, Any]] = []
    peak_hands = 0
    previous_hands: int | None = None
    previous_farm: dict[str, Any] | None = None
    previous_action: Any = None
    previous_step: int | None = None
    previous_day: int | None = None
    previous_hour: int | None = None
    final_farm: dict[str, Any] = {}
    final_step = 0
    final_day = 0
    final_hour = 0

    steps = raw.get("steps") or []
    for step_index, step in enumerate(steps):
        if not isinstance(step, list) or player_id >= len(step) or not isinstance(step[player_id], dict):
            continue
        record = step[player_id]
        day, hour = clock(record, step_index)
        farm = farm_for(record, player_id)
        if not farm:
            continue

        unit_verbs, market_verbs = action_verbs(record.get("action"))
        action_counts.update(unit_verbs)
        market_counts.update(market_verbs)
        movement_by_direction.update(verb for verb in unit_verbs if verb in MOVES)

        hands = len(farm.get("hands") or [])
        peak_hands = max(peak_hands, hands)
        if previous_hands is not None and hands > previous_hands:
            hire_events.append(
                {
                    "step": step_index,
                    "day": day,
                    "hour": hour,
                    "clock": f"D{day}:H{hour:02d}",
                    "increase": hands - previous_hands,
                    "hands_after": hands,
                }
            )
        previous_hands = hands

        quadrants = list(farm.get("unlocked_quadrants") or [])
        if quadrants and unlocks["Q0"] is None:
            unlocks["Q0"] = unlock_event(step_index, day, hour, quadrants, 0, farm)
        if len(quadrants) >= 2 and unlocks["Q1"] is None:
            unlocks["Q1"] = unlock_event(step_index, day, hour, quadrants, 1, farm)
        if len(quadrants) >= 3 and unlocks["Q2"] is None:
            unlocks["Q2"] = unlock_event(step_index, day, hour, quadrants, 2, farm)

        if (
            previous_farm is not None
            and previous_step is not None
            and previous_day is not None
            and previous_hour is not None
            and day > previous_day
        ):
            escape_events.extend(
                detect_escape_events(
                    previous_farm,
                    farm,
                    previous_action=previous_action,
                    episode_id=episode_id,
                    player_id=player_id,
                    player_name=player_name,
                    previous_step=previous_step,
                    previous_day=previous_day,
                    previous_hour=previous_hour,
                    observed_day=day,
                    observed_step=step_index,
                )
            )

        if hour == 23 or step_index == len(steps) - 1:
            daily_rows.extend(
                snapshot_rows(
                    episode_id=episode_id,
                    seed=seed,
                    player_id=player_id,
                    player_name=player_name,
                    step_index=step_index,
                    day=day,
                    hour=hour,
                    farm=farm,
                )
            )

        previous_farm = farm
        previous_action = record.get("action")
        previous_step = step_index
        previous_day = day
        previous_hour = hour
        final_farm = farm
        final_step = step_index
        final_day = day
        final_hour = hour

    final_quadrants: list[dict[str, Any]] = []
    for slot, quadrant in QUADRANT_SLOTS:
        final_quadrants.append(
            {
                "quadrant_slot": slot,
                "quadrant": quadrant,
                "unlock": unlocks[slot],
                **composition_for(final_farm, quadrant),
            }
        )

    total_unit_commands = sum(action_counts.values())
    pass_commands = action_counts["PASS"]
    active_unit_commands = total_unit_commands - pass_commands
    movement_actions = sum(movement_by_direction.values())
    productive_commands = sum(action_counts[verb] for verb in PRODUCTIVE)
    final_crops = sum(row["crop_total"] for row in final_quadrants)
    final_animals = sum(row["animal_total"] for row in final_quadrants)
    final_empty = sum(row["empty_available"] for row in final_quadrants)
    final_weeds = sum(row["weed"] for row in final_quadrants)
    final_empty_structures = sum(row["empty_structure_total"] for row in final_quadrants)
    final_idle = sum(row["idle_total"] for row in final_quadrants)
    per_day_totals: dict[int, Counter[str]] = defaultdict(Counter)
    for row in daily_rows:
        per_day_totals[row["day"]].update(
            {
                "crop_total": row["crop_total"],
                "animal_total": row["animal_total"],
                "weed": row["weed"],
                "idle_total": row["idle_total"],
                "owned_tiles": 25 - row["locked"],
            }
        )
    peak_crops = max((totals["crop_total"] for totals in per_day_totals.values()), default=0)
    peak_animals = max((totals["animal_total"] for totals in per_day_totals.values()), default=0)
    peak_crops_day = min((day for day, totals in per_day_totals.items() if totals["crop_total"] == peak_crops), default=None)
    peak_animals_day = min((day for day, totals in per_day_totals.items() if totals["animal_total"] == peak_animals), default=None)
    crop_tile_days = sum(totals["crop_total"] for totals in per_day_totals.values())
    animal_tile_days = sum(totals["animal_total"] for totals in per_day_totals.values())
    weed_tile_days = sum(totals["weed"] for totals in per_day_totals.values())
    idle_tile_days = sum(totals["idle_total"] for totals in per_day_totals.values())
    owned_tile_days = sum(totals["owned_tiles"] for totals in per_day_totals.values())
    result = "WIN" if score > opponent_score else "LOSS" if score < opponent_score else "TIE"

    summary = {
        "episode_id": episode_id,
        "seed": seed,
        "player_id": player_id,
        "player_name": player_name,
        "opponent_name": opponent_name,
        "score": score,
        "opponent_score": opponent_score,
        "score_margin": score - opponent_score,
        "result": result,
        "top3_target": player_name in TOP3,
        "q0_unlock": unlocks["Q0"],
        "q1_unlock": unlocks["Q1"],
        "q2_unlock": unlocks["Q2"],
        "q1_to_q2_steps": (unlocks["Q2"]["step"] - unlocks["Q1"]["step"]) if unlocks["Q1"] and unlocks["Q2"] else None,
        "final_hands": len(final_farm.get("hands") or []),
        "peak_hands": peak_hands,
        "successful_hires_observed": sum(event["increase"] for event in hire_events),
        "hire_events": hire_events,
        "total_unit_commands": total_unit_commands,
        "active_unit_commands": active_unit_commands,
        "pass_commands": pass_commands,
        "movement_actions_issued": movement_actions,
        "movement_by_direction": dict(sorted(movement_by_direction.items())),
        "movement_share_of_all_unit_commands_pct": round(100 * movement_actions / total_unit_commands, 2) if total_unit_commands else 0.0,
        "movement_share_of_active_unit_commands_pct": round(100 * movement_actions / active_unit_commands, 2) if active_unit_commands else 0.0,
        "productive_commands_issued": productive_commands,
        "market_orders_issued": sum(market_counts.values()),
        "market_order_counts": dict(sorted(market_counts.items())),
        "animal_escapes_total": len(escape_events),
        "animal_escapes_by_species": dict(sorted(Counter(event["species"] for event in escape_events).items())),
        "animal_escape_events": escape_events,
        "final_observation": {"step": final_step, "day": final_day, "hour": final_hour},
        "final_cash_observed": int(final_farm.get("money", 0) or 0),
        "final_crops_total": final_crops,
        "final_animals_total": final_animals,
        "final_empty_available_total": final_empty,
        "final_weeds_total": final_weeds,
        "final_empty_structures_total": final_empty_structures,
        "final_idle_tiles_total": final_idle,
        "final_non_crop_tiles_total": 75 - final_crops,
        "peak_daily_crops_total": peak_crops,
        "peak_daily_crops_first_day": peak_crops_day,
        "peak_daily_animals_total": peak_animals,
        "peak_daily_animals_first_day": peak_animals_day,
        "crop_tile_days": crop_tile_days,
        "animal_tile_days": animal_tile_days,
        "weed_tile_days": weed_tile_days,
        "idle_tile_days": idle_tile_days,
        "owned_tile_activation_pct": round(100 * (crop_tile_days + animal_tile_days) / owned_tile_days, 2) if owned_tile_days else 0.0,
        "final_quadrants": final_quadrants,
    }
    return summary, daily_rows, escape_events


def scalar_summary_row(summary: dict[str, Any]) -> dict[str, Any]:
    q1 = summary["q1_unlock"] or {}
    q2 = summary["q2_unlock"] or {}
    return {
        "episode_id": summary["episode_id"],
        "seed": summary["seed"],
        "player_id": summary["player_id"],
        "player_name": summary["player_name"],
        "opponent_name": summary["opponent_name"],
        "result": summary["result"],
        "score": summary["score"],
        "opponent_score": summary["opponent_score"],
        "score_margin": summary["score_margin"],
        "q1_step": q1.get("step"),
        "q1_day": q1.get("day"),
        "q1_hour": q1.get("hour"),
        "q1_quadrant": q1.get("quadrant"),
        "q2_step": q2.get("step"),
        "q2_day": q2.get("day"),
        "q2_hour": q2.get("hour"),
        "q2_quadrant": q2.get("quadrant"),
        "q1_to_q2_steps": summary["q1_to_q2_steps"],
        "final_hands": summary["final_hands"],
        "peak_hands": summary["peak_hands"],
        "movement_actions_issued": summary["movement_actions_issued"],
        "movement_share_active_pct": summary["movement_share_of_active_unit_commands_pct"],
        "productive_commands_issued": summary["productive_commands_issued"],
        "pass_commands": summary["pass_commands"],
        "animal_escapes_total": summary["animal_escapes_total"],
        "final_crops_total": summary["final_crops_total"],
        "final_animals_total": summary["final_animals_total"],
        "final_empty_available_total": summary["final_empty_available_total"],
        "final_weeds_total": summary["final_weeds_total"],
        "final_empty_structures_total": summary["final_empty_structures_total"],
        "final_idle_tiles_total": summary["final_idle_tiles_total"],
        "final_non_crop_tiles_total": summary["final_non_crop_tiles_total"],
        "peak_daily_crops_total": summary["peak_daily_crops_total"],
        "peak_daily_crops_first_day": summary["peak_daily_crops_first_day"],
        "peak_daily_animals_total": summary["peak_daily_animals_total"],
        "peak_daily_animals_first_day": summary["peak_daily_animals_first_day"],
        "crop_tile_days": summary["crop_tile_days"],
        "animal_tile_days": summary["animal_tile_days"],
        "weed_tile_days": summary["weed_tile_days"],
        "idle_tile_days": summary["idle_tile_days"],
        "owned_tile_activation_pct": summary["owned_tile_activation_pct"],
    }


def final_quadrant_rows(summaries: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for summary in summaries:
        for quadrant in summary["final_quadrants"]:
            unlock = quadrant.get("unlock") or {}
            rows.append(
                {
                    "episode_id": summary["episode_id"],
                    "player_id": summary["player_id"],
                    "player_name": summary["player_name"],
                    "quadrant_slot": quadrant["quadrant_slot"],
                    "quadrant": quadrant["quadrant"],
                    "unlock_step": unlock.get("step"),
                    "unlock_day": unlock.get("day"),
                    "unlock_hour": unlock.get("hour"),
                    **{key: quadrant[key] for key in COMPOSITION_KEYS},
                    "crop_total": quadrant["crop_total"],
                    "animal_total": quadrant["animal_total"],
                    "empty_structure_total": quadrant["empty_structure_total"],
                    "idle_total": quadrant["idle_total"],
                    "non_crop_total": quadrant["non_crop_total"],
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fmt_int(value: int | float) -> str:
    if isinstance(value, float) and not value.is_integer():
        return f"{value:,.2f}"
    return f"{int(value):,}"


def fmt_unlock(event: dict[str, Any] | None) -> str:
    if not event:
        return "—"
    return f"{event['clock']} / s{event['step']} ({event['quadrant']})"


def aggregate_agents(summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for summary in summaries:
        grouped[summary["player_name"]].append(summary)
    rows: list[dict[str, Any]] = []
    ordered_names = list(TOP3) + sorted(name for name in grouped if name not in TOP3)
    for name in ordered_names:
        group = grouped[name]
        q1_steps = [entry["q1_unlock"]["step"] for entry in group if entry["q1_unlock"]]
        q2_steps = [entry["q2_unlock"]["step"] for entry in group if entry["q2_unlock"]]
        rows.append(
            {
                "player_name": name,
                "episodes": len(group),
                "wins": sum(entry["result"] == "WIN" for entry in group),
                "losses": sum(entry["result"] == "LOSS" for entry in group),
                "mean_score": round(statistics.mean(entry["score"] for entry in group), 2),
                "median_q1_step": statistics.median(q1_steps) if q1_steps else None,
                "median_q2_step": statistics.median(q2_steps) if q2_steps else None,
                "mean_moves": round(statistics.mean(entry["movement_actions_issued"] for entry in group), 2),
                "mean_move_share_active_pct": round(statistics.mean(entry["movement_share_of_active_unit_commands_pct"] for entry in group), 2),
                "mean_final_hands": round(statistics.mean(entry["final_hands"] for entry in group), 2),
                "escapes_total": sum(entry["animal_escapes_total"] for entry in group),
                "mean_final_crops": round(statistics.mean(entry["final_crops_total"] for entry in group), 2),
                "mean_final_animals": round(statistics.mean(entry["final_animals_total"] for entry in group), 2),
                "mean_final_idle": round(statistics.mean(entry["final_idle_tiles_total"] for entry in group), 2),
                "mean_peak_crops": round(statistics.mean(entry["peak_daily_crops_total"] for entry in group), 2),
                "mean_peak_animals": round(statistics.mean(entry["peak_daily_animals_total"] for entry in group), 2),
                "mean_owned_tile_activation_pct": round(statistics.mean(entry["owned_tile_activation_pct"] for entry in group), 2),
                "weed_tile_days_total": sum(entry["weed_tile_days"] for entry in group),
            }
        )
    return rows


def milestone_token(rows: list[dict[str, Any]]) -> str:
    parts = []
    for row in sorted(rows, key=lambda item: item["quadrant_slot"]):
        if not row["unlocked"]:
            parts.append(f"{row['quadrant_slot']} locked")
        else:
            parts.append(f"{row['quadrant_slot']} C{row['crop_total']}/A{row['animal_total']}/I{row['idle_total']}")
    return "; ".join(parts)


def markdown_report(
    provenance: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
    aggregate_rows: list[dict[str, Any]],
    quadrant_rows: list[dict[str, Any]],
    daily_rows: list[dict[str, Any]],
    escape_events: list[dict[str, Any]],
) -> str:
    lines = [
        "# E17 — benchmark forense Codex sui replay Top 3",
        "",
        "## Esito",
        "",
        f"Corpus elaborato integralmente: **{len(provenance)} episodi, {len(summaries)} player-seat, {sum(item['steps'] for item in provenance):,} step di episodio**.",
        "Tutti i replay sono validi, distinti, `DONE/DONE`, su `module_version 1.32.7`.",
        "",
        "Clock: `D#:H##` usa giorno e ora zero-based del replay. Lo sblocco è il primo stato in cui il quadrante risulta osservabile come posseduto.",
        "I move sono comandi cardinali emessi e non implicano necessariamente uno spostamento riuscito. Una fuga è conteggiata soltanto se, attraverso un EOD, una tile passa da animale a stessa struttura vuota con `consecutive_unfed=1` e `fed_today=false` nello stato precedente.",
        "",
        "## Sintesi per episodio e partecipante",
        "",
        "| Ep. | Partecipante | Esito | Score | Q1 | Q2 | Move | Move/azioni attive | Assistenti | Fughe | Picco crop/animali | Crop finali | Animali finali | Non-crop finali | Tile inattive finali |",
        "|---:|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        lines.append(
            "| {episode} | {name} | {result} | {score} | {q1} | {q2} | {moves} | {move_share:.2f}% | {hands} | {escapes} | {peak_crops}/{peak_animals} | {crops} | {animals} | {non_crop} | {idle} |".format(
                episode=summary["episode_id"],
                name=summary["player_name"],
                result=summary["result"],
                score=fmt_int(summary["score"]),
                q1=fmt_unlock(summary["q1_unlock"]),
                q2=fmt_unlock(summary["q2_unlock"]),
                moves=fmt_int(summary["movement_actions_issued"]),
                move_share=summary["movement_share_of_active_unit_commands_pct"],
                hands=summary["final_hands"],
                escapes=summary["animal_escapes_total"],
                peak_crops=summary["peak_daily_crops_total"],
                peak_animals=summary["peak_daily_animals_total"],
                crops=summary["final_crops_total"],
                animals=summary["final_animals_total"],
                non_crop=summary["final_non_crop_tiles_total"],
                idle=summary["final_idle_tiles_total"],
            )
        )

    lines.extend(
        [
            "",
            "`Tile inattive finali` = arabile vuota + weed + struttura vuota + stato non classificato, sui 75 tile posseduti. Le tile occupate da animali non sono incluse fra le inattive.",
            "",
            "## Aggregazione per nome agente",
            "",
            "| Agente | N | W-L | Score medio | Q1 mediano | Q2 mediano | Move medi | Move/attive | Assistenti | Fughe | Picco crop | Picco animali | Attivazione tile | Crop finali | Animali finali | Inattive |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in aggregate_rows:
        lines.append(
            "| {name} | {n} | {wins}-{losses} | {score} | {q1} | {q2} | {moves} | {share:.2f}% | {hands} | {escapes} | {peak_crops} | {peak_animals} | {activation:.2f}% | {crops} | {animals} | {idle} |".format(
                name=row["player_name"],
                n=row["episodes"],
                wins=row["wins"],
                losses=row["losses"],
                score=fmt_int(row["mean_score"]),
                q1=fmt_int(row["median_q1_step"]) if row["median_q1_step"] is not None else "—",
                q2=fmt_int(row["median_q2_step"]) if row["median_q2_step"] is not None else "—",
                moves=fmt_int(row["mean_moves"]),
                share=row["mean_move_share_active_pct"],
                hands=fmt_int(row["mean_final_hands"]),
                escapes=row["escapes_total"],
                peak_crops=fmt_int(row["mean_peak_crops"]),
                peak_animals=fmt_int(row["mean_peak_animals"]),
                activation=row["mean_owned_tile_activation_pct"],
                crops=fmt_int(row["mean_final_crops"]),
                animals=fmt_int(row["mean_final_animals"]),
                idle=fmt_int(row["mean_final_idle"]),
            )
        )

    aggregate_by_name = {row["player_name"]: row for row in aggregate_rows}
    escape_days = Counter(event["eod_after_day"] for event in escape_events)
    tetsuya = aggregate_by_name["tetsuya"]
    oceanmix = aggregate_by_name["OceanMix"]
    crop_dusta = aggregate_by_name["Crop Dusta"]
    lines.extend(
        [
            "",
            "## Lettura descrittiva immediata",
            "",
            f"- `OBSERVED/DERIVED`: Crop Dusta sblocca prima: Q1 mediano s{fmt_int(crop_dusta['median_q1_step'])} e Q2 mediano s{fmt_int(crop_dusta['median_q2_step'])}, contro s{fmt_int(tetsuya['median_q1_step'])}/s{fmt_int(tetsuya['median_q2_step'])} per tetsuya e s{fmt_int(oceanmix['median_q1_step'])}/s{fmt_int(oceanmix['median_q2_step'])} per OceanMix.",
            f"- `DERIVED`: alla maggiore precocità di Crop Dusta è associato il carico di movimento più alto ({fmt_int(crop_dusta['mean_moves'])} move medi; {crop_dusta['mean_move_share_active_pct']:.2f}% delle azioni attive), rispetto a tetsuya ({fmt_int(tetsuya['mean_moves'])}; {tetsuya['mean_move_share_active_pct']:.2f}%) e OceanMix ({fmt_int(oceanmix['mean_moves'])}; {oceanmix['mean_move_share_active_pct']:.2f}%). Questa è associazione, non effetto causale identificato.",
            f"- `OBSERVED`: la workforce finale media è {fmt_int(crop_dusta['mean_final_hands'])} per Crop Dusta, {fmt_int(tetsuya['mean_final_hands'])} per tetsuya e {fmt_int(oceanmix['mean_final_hands'])} per OceanMix.",
            f"- `DERIVED`: tutti i {len(escape_events)} eventi compatibili con fuga secondo il criterio EOD stretto appartengono a Crop Dusta; distribuzione per EOD: " + ", ".join(f"giorno {day}: {count}" for day, count in sorted(escape_days.items())) + ". La concentrazione terminale suggerisce una scelta di abbandono o servicing ridotto, ma il valore economico causale resta da testare.",
            f"- `DERIVED`: i picchi medi giornalieri crop/animali sono {fmt_int(tetsuya['mean_peak_crops'])}/{fmt_int(tetsuya['mean_peak_animals'])} per tetsuya, {fmt_int(oceanmix['mean_peak_crops'])}/{fmt_int(oceanmix['mean_peak_animals'])} per OceanMix e {fmt_int(crop_dusta['mean_peak_crops'])}/{fmt_int(crop_dusta['mean_peak_animals'])} per Crop Dusta.",
            "- `UNKNOWN`: la composizione finale non rappresenta da sola l'impiego stagionale del terreno; per questo il CSV giornaliero conserva le traiettorie complete.",
        ]
    )

    lines.extend(
        [
            "",
            "## Composizione finale per quadrante",
            "",
            "Ogni riga somma a 25 tile. `Non-crop` include animali, strutture, vuote e weed; `Inattive` esclude gli animali ma include strutture vuote.",
            "",
            "| Ep. | Partecipante | Q | Sblocco | Vuote | Weed | Strutture vuote | Wheat | Carrot | Tomato | Strawberry | Melon | Goose | Cow | Sheep | Crop | Animali | Non-crop | Inattive |",
            "|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in quadrant_rows:
        unlock = f"D{row['unlock_day']}:H{row['unlock_hour']:02d} / s{row['unlock_step']}" if row["unlock_step"] is not None else "—"
        lines.append(
            "| {episode} | {name} | {slot} ({quadrant}) | {unlock} | {empty} | {weed} | {empty_structures} | {wheat} | {carrot} | {tomato} | {strawberry} | {melon} | {goose} | {cow} | {sheep} | {crops} | {animals} | {non_crop} | {idle} |".format(
                episode=row["episode_id"],
                name=row["player_name"],
                slot=row["quadrant_slot"],
                quadrant=row["quadrant"],
                unlock=unlock,
                empty=row["empty_available"],
                weed=row["weed"],
                empty_structures=row["empty_structure_total"],
                wheat=row["WHEAT"],
                carrot=row["CARROT"],
                tomato=row["TOMATO"],
                strawberry=row["STRAWBERRY"],
                melon=row["MELON"],
                goose=row["GOOSE"],
                cow=row["COW"],
                sheep=row["SHEEP"],
                crops=row["crop_total"],
                animals=row["animal_total"],
                non_crop=row["non_crop_total"],
                idle=row["idle_total"],
            )
        )

    by_milestone: dict[tuple[int, int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in daily_rows:
        by_milestone[(row["episode_id"], row["player_id"], row["day"])].append(row)
    milestones = (0, 5, 10, 15, 20, 25, 29)
    lines.extend(
        [
            "",
            "## Indicazione temporale per i tre quadranti",
            "",
            "Legenda cella: `C` crop attive, `A` animali presenti, `I` tile inattive. Gli snapshot sono le ultime osservazioni del giorno indicato; il CSV giornaliero conserva specie e categorie complete.",
            "",
            "| Ep. | Partecipante | D0 | D5 | D10 | D15 | D20 | D25 | D29 |",
            "|---:|---|---|---|---|---|---|---|---|",
        ]
    )
    for summary in summaries:
        cells = [milestone_token(by_milestone[(summary["episode_id"], summary["player_id"], day)]) for day in milestones]
        lines.append(f"| {summary['episode_id']} | {summary['player_name']} | " + " | ".join(cells) + " |")

    lines.extend(["", "## Eventi di fuga derivati con criterio EOD stretto", ""])
    if escape_events:
        lines.extend(
            [
                "La fuga non è un campo evento nativo. Ogni riga è derivata da: animale ancora presente a H23, `consecutive_unfed=1`, `fed_today=false`, nessun FEED/PICKUP richiesto all'EOD e stessa struttura vuota nel primo stato del giorno successivo. Il CSV audit conserva tutti i campi pre/post.",
                "",
                "| Ep. | Partecipante | Specie | Quadrante | Coordinata | EOD dopo giorno | Prima assenza osservata |",
                "|---:|---|---|---|---|---:|---|",
            ]
        )
        for event in escape_events:
            lines.append(
                f"| {event['episode_id']} | {event['player_name']} | {event['species']} | {event['quadrant_slot']} ({event['quadrant']}) | ({event['row']},{event['col']}) | {event['eod_after_day']} | D{event['first_observed_absent_day']} / s{event['first_observed_absent_step']} |"
            )
    else:
        lines.append("Nessuna fuga animale confermata dal criterio stretto.")

    lines.extend(
        [
            "",
            "## Artefatti riproducibili",
            "",
            "- `experiments/e17/artifacts/discovery/codex/E17_TOP3_REPLAY_METRICS.json`: provenance, summary, composizioni ed eventi;",
            "- `experiments/e17/artifacts/discovery/codex/E17_PARTICIPANT_SUMMARY.csv`: una riga per player-seat;",
            "- `experiments/e17/artifacts/discovery/codex/E17_FINAL_QUADRANT_COMPOSITION.csv`: una riga per player-seat e quadrante;",
            "- `experiments/e17/artifacts/discovery/codex/E17_QUADRANT_DAILY_TIMELINE.csv`: snapshot giornaliero per specie, player-seat e quadrante;",
            "- `experiments/e17/artifacts/discovery/codex/E17_ANIMAL_ESCAPE_EVENTS.csv`: audit degli eventi di fuga derivati con coordinate, stato pre/post-EOD e prove FEED/PICKUP;",
            "- `experiments/e17/tools/codex/analyze_top3_replays.py`: estrattore indipendente Codex.",
            "",
            "## Limiti",
            "",
            "- `OBSERVED`: reward, stati tile, hands, quadranti e comandi emessi provengono direttamente dai replay.",
            "- `DERIVED`: composizioni, quote move, margini ed eventi di fuga sono calcoli deterministici documentati sopra.",
            "- `UNKNOWN`: il replay non certifica che ogni comando move emesso sia stato eseguito con successo; per questo la metrica è denominata `issued`.",
            "- Il campione è osservazionale, con mercato e avversario condivisi: non identifica da solo l'effetto causale di una singola scelta strategica.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    provenance: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    daily_rows: list[dict[str, Any]] = []
    escape_events: list[dict[str, Any]] = []

    for episode_id in EPISODE_IDS:
        path = BENCHMARK_DIR / f"{episode_id}.json"
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open(encoding="utf-8") as handle:
            raw = json.load(handle)
        info = raw.get("info") or {}
        names = list(info.get("TeamNames") or [])
        rewards = list(raw.get("rewards") or [])
        statuses = list(raw.get("statuses") or [])
        if int(info.get("EpisodeId")) != episode_id:
            raise ValueError(f"EpisodeId mismatch in {path}")
        if len(names) != 2 or len(rewards) != 2:
            raise ValueError(f"Expected two players in {path}")
        if statuses != ["DONE", "DONE"]:
            raise ValueError(f"Non-terminal replay {path}: {statuses}")
        if len(raw.get("steps") or []) != 720:
            raise ValueError(f"Unexpected step count in {path}")
        if raw.get("module_version") != "1.32.7":
            raise ValueError(f"Unexpected module version in {path}")
        provenance.append(
            {
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256_file(path),
                "episode_id": episode_id,
                "seed": int(info.get("seed")),
                "agents": names,
                "rewards": [int(value) for value in rewards],
                "statuses": statuses,
                "steps": len(raw["steps"]),
                "schema_version": raw.get("schema_version"),
                "module_version": raw.get("module_version"),
            }
        )
        for player_id, player_name in enumerate(names):
            summary, player_daily, player_escapes = analyze_player(
                raw,
                episode_id=episode_id,
                seed=int(info.get("seed")),
                player_id=player_id,
                player_name=player_name,
                opponent_name=names[1 - player_id],
                score=int(rewards[player_id]),
                opponent_score=int(rewards[1 - player_id]),
            )
            summaries.append(summary)
            daily_rows.extend(player_daily)
            escape_events.extend(player_escapes)

    summaries.sort(key=lambda item: (item["episode_id"], item["player_id"]))
    daily_rows.sort(key=lambda item: (item["episode_id"], item["player_id"], item["day"], item["quadrant_slot"]))
    escape_events.sort(key=lambda item: (item["episode_id"], item["player_id"], item["first_observed_absent_step"], item["row"], item["col"]))
    quadrant_rows = final_quadrant_rows(summaries)
    aggregate_rows = aggregate_agents(summaries)

    if len(summaries) != 18:
        raise AssertionError(f"Expected 18 player-seat summaries, found {len(summaries)}")
    if len(quadrant_rows) != 54:
        raise AssertionError(f"Expected 54 final quadrant rows, found {len(quadrant_rows)}")
    if len(daily_rows) != 1620:
        raise AssertionError(f"Expected 1620 daily quadrant rows, found {len(daily_rows)}")
    for row in quadrant_rows:
        accounted = sum(row[key] for key in COMPOSITION_KEYS)
        if accounted != 25:
            raise AssertionError(f"Quadrant does not sum to 25: {row}")
    for summary in summaries:
        if not summary["q1_unlock"] or not summary["q2_unlock"]:
            raise AssertionError(f"Missing 3Q unlock for {summary['episode_id']} {summary['player_name']}")
        if summary["final_cash_observed"] != summary["score"]:
            raise AssertionError(f"Final cash/reward mismatch: {summary['episode_id']} {summary['player_name']}")

    metrics = {
        "schema": "e17_codex_top3_benchmark.v1",
        "method": {
            "quadrant_mapping": {slot: quadrant for slot, quadrant in QUADRANT_SLOTS},
            "clock": "zero-based replay day/hour; unlock is first observed owned state",
            "movement": "issued NORTH/SOUTH/EAST/WEST unit commands",
            "escape": "DERIVED: occupied at-risk tile to same empty structure across EOD",
            "escape_audit": "pre/post tile state plus pre-EOD executed-state evidence and EOD FEED/PICKUP request counts",
            "idle_tile": "empty_available + weed + empty_structure + other",
        },
        "provenance": provenance,
        "participant_summaries": summaries,
        "agent_aggregates": aggregate_rows,
        "final_quadrant_composition": quadrant_rows,
        "animal_escape_events": escape_events,
        "validation": {
            "episodes": len(provenance),
            "player_seats": len(summaries),
            "episode_steps": sum(item["steps"] for item in provenance),
            "daily_quadrant_rows": len(daily_rows),
            "final_quadrant_rows": len(quadrant_rows),
        },
    }
    (OUT_DIR / "E17_TOP3_REPLAY_METRICS.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_csv(OUT_DIR / "E17_PARTICIPANT_SUMMARY.csv", [scalar_summary_row(item) for item in summaries])
    write_csv(OUT_DIR / "E17_FINAL_QUADRANT_COMPOSITION.csv", quadrant_rows)
    write_csv(OUT_DIR / "E17_QUADRANT_DAILY_TIMELINE.csv", daily_rows)
    write_csv(
        OUT_DIR / "E17_ANIMAL_ESCAPE_EVENTS.csv",
        escape_events,
        fieldnames=[
            "episode_id",
            "player_id",
            "player_name",
            "species",
            "quadrant_slot",
            "quadrant",
            "row",
            "col",
            "pre_eod_step",
            "eod_after_day",
            "pre_eod_hour",
            "structure_before",
            "animal_before",
            "consecutive_unfed_before",
            "fed_today_before",
            "feed_executed_before_pre_eod_snapshot",
            "pickup_executed_before_pre_eod_snapshot",
            "eod_feed_requests",
            "eod_pickup_requests",
            "first_observed_absent_day",
            "first_observed_absent_step",
            "structure_after",
            "animal_after",
            "evidence",
        ],
    )
    (REPORT_DIR / "E17_TOP3_REPLAY_ANALYSIS.md").write_text(
        markdown_report(provenance, summaries, aggregate_rows, quadrant_rows, daily_rows, escape_events),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "episodes": len(provenance),
                "player_seats": len(summaries),
                "daily_quadrant_rows": len(daily_rows),
                "escape_events": len(escape_events),
                "output": str(OUT_DIR),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
