"""Read-only lifecycle audit over the completed E16 Stage A-R1 ledgers.

Inputs are never modified. All generated artifacts are written under
results/e16/diagnostics/tile_lifecycle_feature.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "results" / "e16" / "stage_a_r1"
OUTPUT_DIR = ROOT / "results" / "e16" / "diagnostics" / "tile_lifecycle_feature"

TURNS_PER_DAY = 24
CROP_POSITIONS = tuple((x, y) for y in range(3) for x in range(10))
CROPS = {
    "WHEAT": {
        "first_yield_day": 2,
        "max_yield_day": 4,
        "interval": 0,
        "max_yield": 6,
        "ongoing": False,
    },
    "STRAWBERRY": {
        "first_yield_day": 10,
        "max_yield_day": 10,
        "interval": 2,
        "max_yield": 4,
        "ongoing": True,
    },
    "MELON": {
        "first_yield_day": 10,
        "max_yield_day": 12,
        "interval": 0,
        "max_yield": 6,
        "ongoing": False,
    },
}


@dataclass
class Snapshot:
    step: int
    day: int
    hour: int
    position: tuple[int, int]
    tile: Any
    sequence: int
    phase: str


def tile_kind(tile: Any) -> str:
    if tile is None:
        return "EMPTY"
    if tile == "LOCKED":
        return "LOCKED"
    if isinstance(tile, dict):
        return str(tile.get("kind", "STRUCTURE"))
    return "UNKNOWN"


def state_position(state: dict[str, Any]) -> tuple[int, int] | None:
    position = state.get("position")
    if not isinstance(position, list) or len(position) != 2:
        return None
    return int(position[0]), int(position[1])


def crop_harvest(event: dict[str, Any]) -> bool:
    payload = event.get("engine_applied_payload")
    tile = (event.get("relevant_state_before") or {}).get("tile")
    return (
        isinstance(payload, list)
        and bool(payload)
        and payload[0] == "HARVEST"
        and isinstance(tile, dict)
        and tile.get("kind") == "PLANT"
    )


def harvest_ready(tile: Any, day: int) -> bool:
    if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
        return False
    crop = tile.get("crop")
    if crop not in CROPS:
        return False
    age = day - int(tile.get("planted_day", day))
    return int(tile.get("yield_units", 0)) > 0 and age >= CROPS[crop]["first_yield_day"]


def lifecycle_state(tile: Any, day: int) -> str:
    kind = tile_kind(tile)
    if kind == "EMPTY":
        return "EMPTY_ASSIGNED"
    if kind == "WEED":
        return "LOST_WEED"
    if kind != "PLANT":
        return "OUT_OF_SCOPE"
    return "HARVEST_READY" if harvest_ready(tile, day) else "GROWING"


def care_due(tile: Any) -> bool:
    return (
        isinstance(tile, dict)
        and tile.get("kind") == "PLANT"
        and not bool(tile.get("watered_today", False))
    )


def water_loss_boundary(tile: Any) -> bool:
    return care_due(tile) and int(tile.get("consecutive_unwatered", 0)) + 1 >= 2


def decay_due_on_step(tile: Any, step: int) -> bool:
    if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
        return False
    max_lifespan = int(tile.get("max_lifespan_step", -1))
    return (
        max_lifespan >= 0
        and step >= max_lifespan
        and (step - max_lifespan) % 2 == 0
    )


def classify_weed_entry(source: Snapshot, destination: Snapshot) -> str:
    source_kind = tile_kind(source.tile)
    end_of_day = destination.day > source.day
    if source_kind == "PLANT":
        # Engine order is lifespan decay first, then end-of-day water refresh.
        # The R1 ledger step counter is one observation phase behind day/hour at
        # some boundaries, so test the destination counter for the intervening
        # decay tick and retain day/hour for end-of-day detection.
        if decay_due_on_step(source.tile, destination.step) and int(
            source.tile.get("yield_units", 0)
        ) <= 1:
            return "LIFESPAN_DECAY__DETERMINISTIC_PREVENTABLE"
        if end_of_day and water_loss_boundary(source.tile):
            return "MISSED_WATER__DETERMINISTIC_PREVENTABLE"
        return "PLANT_TO_WEED__UNRESOLVED"
    if source_kind == "EMPTY" and end_of_day:
        return "EMPTY_SPAWN__STOCHASTIC_PARTIALLY_PREVENTABLE"
    return f"{source_kind}_TO_WEED__UNRESOLVED"


def first_op(event: dict[str, Any]) -> str | None:
    payload = event.get("engine_applied_payload")
    if isinstance(payload, list) and payload:
        return str(payload[0])
    return None


def ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def episode_audit(summary_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    episode_id = str(summary["episode_id"])
    treatment_seat = int(summary["treatment_seat"])
    target = int(summary["cell_config"]["crop_working_set_target"])
    working_set = set(CROP_POSITIONS[:target])

    snapshots_by_position: dict[tuple[int, int], list[Snapshot]] = defaultdict(list)
    actor_events = 0
    premature_harvests = 0
    valid_harvests = 0
    failed_harvests_other = 0
    dig_attempts = 0
    weed_snapshot_positions: set[tuple[int, int]] = set()
    lifecycle_observations: Counter[str] = Counter()
    care_due_observations = 0
    water_boundary_observations = 0

    ledger_path = summary_path.with_suffix(".events.jsonl")
    with ledger_path.open(encoding="utf-8") as handle:
        for sequence, line in enumerate(handle):
            if not line.strip():
                continue
            event = json.loads(line)
            if (
                int(event.get("player", -1)) != treatment_seat
                or event.get("actor_or_order_type") == "market_order"
            ):
                continue
            actor_events += 1
            op = first_op(event)
            if op == "DIG":
                dig_attempts += 1

            if crop_harvest(event):
                tile = (event.get("relevant_state_before") or {}).get("tile")
                if harvest_ready(tile, int(event["day"])):
                    valid_harvests += 1
                elif event.get("execution_status") in {"failed", "no_op"}:
                    crop = tile.get("crop") if isinstance(tile, dict) else None
                    age = int(event["day"]) - int(tile.get("planted_day", event["day"]))
                    if crop in CROPS and age < CROPS[crop]["first_yield_day"]:
                        premature_harvests += 1
                    else:
                        failed_harvests_other += 1

            step = int(event["step"])
            day = int(event["day"])
            hour = int(event["hour"])
            for phase_index, phase in enumerate(("before", "after")):
                state = event.get(f"relevant_state_{phase}") or {}
                position = state_position(state)
                if position is None or position not in working_set:
                    continue
                tile = state.get("tile")
                snapshot = Snapshot(
                    step=step,
                    day=day,
                    hour=hour,
                    position=position,
                    tile=tile,
                    sequence=sequence * 2 + phase_index,
                    phase=phase,
                )
                snapshots_by_position[position].append(snapshot)
                lifecycle_observations[lifecycle_state(tile, day)] += 1
                care_due_observations += int(care_due(tile))
                water_boundary_observations += int(water_loss_boundary(tile))
                if tile_kind(tile) == "WEED":
                    weed_snapshot_positions.add(position)

    unique_position_steps = 0
    exact_intervals = 0
    gapped_intervals = 0
    exact_changed_intervals = 0
    ambiguous_changed_intervals = 0
    exact_weed_entries: Counter[str] = Counter()
    ambiguous_weed_entries = 0
    ambiguous_weed_from_plant = 0
    ambiguous_weed_from_empty = 0
    ambiguous_weed_from_other = 0
    left_censored_weed_positions = 0
    transition_rows: list[dict[str, Any]] = []

    for position, snapshots in snapshots_by_position.items():
        by_step: dict[int, list[Snapshot]] = defaultdict(list)
        for snapshot in snapshots:
            by_step[snapshot.step].append(snapshot)
        ordered_steps = sorted(by_step)
        unique_position_steps += len(ordered_steps)
        if ordered_steps and tile_kind(min(by_step[ordered_steps[0]], key=lambda x: x.sequence).tile) == "WEED":
            left_censored_weed_positions += 1
        for previous_step, current_step in zip(ordered_steps, ordered_steps[1:]):
            source = max(by_step[previous_step], key=lambda item: item.sequence)
            destination = min(by_step[current_step], key=lambda item: item.sequence)
            source_kind = tile_kind(source.tile)
            destination_kind = tile_kind(destination.tile)
            if current_step - previous_step == 1:
                exact_intervals += 1
                if source_kind != destination_kind:
                    exact_changed_intervals += 1
                    cause = (
                        classify_weed_entry(source, destination)
                        if destination_kind == "WEED"
                        else "NOT_A_WEED_ENTRY"
                    )
                    transition_rows.append(
                        {
                            "episode_id": episode_id,
                            "cell_id": summary["cell_id"],
                            "treatment_seat": treatment_seat,
                            "position_x": position[0],
                            "position_y": position[1],
                            "source_step": previous_step,
                            "source_day": source.day,
                            "source_hour": source.hour,
                            "destination_step": current_step,
                            "destination_day": destination.day,
                            "destination_hour": destination.hour,
                            "step_gap": 1,
                            "source_kind": source_kind,
                            "destination_kind": destination_kind,
                            "source_crop": source.tile.get("crop")
                            if isinstance(source.tile, dict)
                            else None,
                            "source_watered_today": source.tile.get("watered_today")
                            if isinstance(source.tile, dict)
                            else None,
                            "source_consecutive_unwatered": source.tile.get(
                                "consecutive_unwatered"
                            )
                            if isinstance(source.tile, dict)
                            else None,
                            "source_yield_units": source.tile.get("yield_units")
                            if isinstance(source.tile, dict)
                            else None,
                            "source_max_lifespan_step": source.tile.get(
                                "max_lifespan_step"
                            )
                            if isinstance(source.tile, dict)
                            else None,
                            "classification": cause,
                        }
                    )
                    if destination_kind == "WEED":
                        exact_weed_entries[cause] += 1
            else:
                gapped_intervals += 1
                if source_kind != destination_kind:
                    ambiguous_changed_intervals += 1
                    if destination_kind == "WEED":
                        ambiguous_weed_entries += 1
                        if source_kind == "PLANT":
                            ambiguous_weed_from_plant += 1
                        elif source_kind == "EMPTY":
                            ambiguous_weed_from_empty += 1
                        else:
                            ambiguous_weed_from_other += 1

    exact_total = exact_intervals + gapped_intervals
    changed_total = exact_changed_intervals + ambiguous_changed_intervals
    result = {
        "episode_id": episode_id,
        "cell_id": summary["cell_id"],
        "seed": int(summary["seed"]),
        "treatment_seat": treatment_seat,
        "crop_working_set_target": target,
        "actor_events": actor_events,
        "unique_observed_tiles": len(snapshots_by_position),
        "unique_tile_step_observations": unique_position_steps,
        "exact_consecutive_step_intervals": exact_intervals,
        "gapped_intervals": gapped_intervals,
        "exact_interval_coverage": ratio(exact_intervals, exact_total),
        "exact_changed_intervals": exact_changed_intervals,
        "ambiguous_changed_intervals": ambiguous_changed_intervals,
        "exact_changed_interval_coverage": ratio(exact_changed_intervals, changed_total),
        "exact_weed_entries": sum(exact_weed_entries.values()),
        "weed_missed_water": exact_weed_entries[
            "MISSED_WATER__DETERMINISTIC_PREVENTABLE"
        ],
        "weed_lifespan_decay": exact_weed_entries[
            "LIFESPAN_DECAY__DETERMINISTIC_PREVENTABLE"
        ],
        "weed_empty_stochastic": exact_weed_entries[
            "EMPTY_SPAWN__STOCHASTIC_PARTIALLY_PREVENTABLE"
        ],
        "weed_exact_unresolved": sum(
            count for cause, count in exact_weed_entries.items() if cause.endswith("UNRESOLVED")
        ),
        "ambiguous_weed_entries": ambiguous_weed_entries,
        "ambiguous_weed_from_plant": ambiguous_weed_from_plant,
        "ambiguous_weed_from_empty": ambiguous_weed_from_empty,
        "ambiguous_weed_from_other": ambiguous_weed_from_other,
        "left_censored_weed_positions": left_censored_weed_positions,
        "unique_working_set_weed_tiles_observed": len(weed_snapshot_positions),
        "premature_crop_harvest_attempts": premature_harvests,
        "valid_crop_harvest_attempts": valid_harvests,
        "other_failed_crop_harvest_attempts": failed_harvests_other,
        "dig_attempts": dig_attempts,
        "reported_crop_losses": int(summary["telemetry"]["crop_losses"]),
        "growing_snapshot_observations": lifecycle_observations["GROWING"],
        "harvest_ready_snapshot_observations": lifecycle_observations["HARVEST_READY"],
        "empty_assigned_snapshot_observations": lifecycle_observations["EMPTY_ASSIGNED"],
        "lost_weed_snapshot_observations": lifecycle_observations["LOST_WEED"],
        "care_due_snapshot_observations": care_due_observations,
        "water_loss_boundary_snapshot_observations": water_boundary_observations,
    }
    return result, transition_rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summed_fields = [
        "actor_events",
        "unique_observed_tiles",
        "unique_tile_step_observations",
        "exact_consecutive_step_intervals",
        "gapped_intervals",
        "exact_changed_intervals",
        "ambiguous_changed_intervals",
        "exact_weed_entries",
        "weed_missed_water",
        "weed_lifespan_decay",
        "weed_empty_stochastic",
        "weed_exact_unresolved",
        "ambiguous_weed_entries",
        "ambiguous_weed_from_plant",
        "ambiguous_weed_from_empty",
        "ambiguous_weed_from_other",
        "left_censored_weed_positions",
        "unique_working_set_weed_tiles_observed",
        "premature_crop_harvest_attempts",
        "valid_crop_harvest_attempts",
        "other_failed_crop_harvest_attempts",
        "dig_attempts",
        "reported_crop_losses",
        "growing_snapshot_observations",
        "harvest_ready_snapshot_observations",
        "empty_assigned_snapshot_observations",
        "lost_weed_snapshot_observations",
        "care_due_snapshot_observations",
        "water_loss_boundary_snapshot_observations",
    ]
    totals = {field: sum(int(row[field]) for row in rows) for field in summed_fields}
    all_intervals = totals["exact_consecutive_step_intervals"] + totals["gapped_intervals"]
    changed_intervals = totals["exact_changed_intervals"] + totals["ambiguous_changed_intervals"]
    exact_weed = totals["exact_weed_entries"]
    classified_weed = exact_weed - totals["weed_exact_unresolved"]
    return {
        "episode_count": len(rows),
        "assigned_working_set_tiles": sum(
            int(row["crop_working_set_target"]) for row in rows
        ),
        **totals,
        "episodes_with_working_set_weed": sum(
            int(row["unique_working_set_weed_tiles_observed"] > 0) for row in rows
        ),
        "exact_interval_coverage": ratio(
            totals["exact_consecutive_step_intervals"], all_intervals
        ),
        "exact_changed_interval_coverage": ratio(
            totals["exact_changed_intervals"], changed_intervals
        ),
        "exact_weed_cause_classification_rate": ratio(classified_weed, exact_weed),
        "weed_entries_with_prior_state_coverage": ratio(
            totals["exact_weed_entries"] + totals["ambiguous_weed_entries"],
            totals["exact_weed_entries"]
            + totals["ambiguous_weed_entries"]
            + totals["left_censored_weed_positions"],
        ),
        "observed_working_set_tile_coverage": ratio(
            totals["unique_observed_tiles"],
            sum(int(row["crop_working_set_target"]) for row in rows),
        ),
        "premature_fraction_of_crop_harvest_attempts": ratio(
            totals["premature_crop_harvest_attempts"],
            totals["premature_crop_harvest_attempts"]
            + totals["valid_crop_harvest_attempts"]
            + totals["other_failed_crop_harvest_attempts"],
        ),
        "notes": [
            "Coverage is for actor-local working-set tile snapshots, not the full board.",
            "Exact intervals require observations of the same tile on consecutive engine steps.",
            "Reported crop_losses is retained only as source telemetry; seat-1 step attribution prevents treating it as exact tile-cause evidence.",
        ],
    }


def main() -> None:
    summary_paths = sorted(INPUT_DIR.glob("E16-A-R1-*.json"))
    if len(summary_paths) != 28:
        raise RuntimeError(f"expected 28 R1 summaries, found {len(summary_paths)}")
    audits = [episode_audit(path) for path in summary_paths]
    rows = [audit[0] for audit in audits]
    transition_rows = [item for audit in audits for item in audit[1]]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUT_DIR / "E16_R1_TILE_LIFECYCLE_COVERAGE.csv", rows)
    if transition_rows:
        write_csv(OUTPUT_DIR / "E16_R1_EXACT_TILE_STATE_CHANGES.csv", transition_rows)
    (OUTPUT_DIR / "E16_R1_TILE_LIFECYCLE_COVERAGE_SUMMARY.json").write_text(
        json.dumps(aggregate(rows), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
