"""Read-only forensic reconstruction for completed E16 Stage A-R1 episodes.

The script never writes into the experimental input directories. Generated
diagnostic artifacts are confined to results/e16/diagnostics.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from collections import Counter, defaultdict, deque
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "results" / "e16" / "stage_a_r1"
OUTPUT_DIR = (
    ROOT
    / "results"
    / "e16"
    / "diagnostics"
    / "e16_a_r1_crop_attainment"
)
RUN_MANIFEST = INPUT_DIR / "E16_STAGE_A_R1_RUN_MANIFEST.json"
R1_CONFIG = ROOT / "configs" / "e16" / "E16_R1_FROZEN_CONFIG.json"

MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
PRODUCTIVE_OPS = {
    "WATER",
    "HARVEST",
    "PLANT",
    "DIG",
    "BUILD_PASTURE",
    "FEED",
    "CARE",
    "COLLECT_FERTILIZER",
    "PICKUP",
    "DROP",
    "PLACE",
}
CROP_NAMES = {"WHEAT", "STRAWBERRY", "MELON"}
CROP_POSITIONS = tuple((x, y) for y in range(3) for x in range(10))
FIRST_YIELD_DAY = {"WHEAT": 2, "STRAWBERRY": 10, "MELON": 10}
FLOOR = 300.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def median(values: Iterable[float]) -> float | None:
    items = list(values)
    return float(statistics.median(items)) if items else None


def mean(values: Iterable[float]) -> float | None:
    items = list(values)
    return float(statistics.fmean(items)) if items else None


def quantile(values: Iterable[float], probability: float) -> float | None:
    items = sorted(values)
    if not items:
        return None
    if len(items) == 1:
        return float(items[0])
    index = (len(items) - 1) * probability
    low = math.floor(index)
    high = math.ceil(index)
    if low == high:
        return float(items[low])
    weight = index - low
    return float(items[low] * (1.0 - weight) + items[high] * weight)


def ratio(numerator: float, denominator: float) -> float | None:
    return numerator / denominator if denominator else None


def first_op(event: dict[str, Any]) -> str | None:
    payload = event.get("engine_applied_payload")
    if isinstance(payload, list) and payload:
        return str(payload[0])
    return None


def requested_op(event: dict[str, Any]) -> str | None:
    payload = event.get("requested_payload")
    if isinstance(payload, list) and payload:
        return str(payload[0])
    return None


def tile_position(event: dict[str, Any]) -> tuple[int, int] | None:
    before = event.get("relevant_state_before") or {}
    position = before.get("position")
    if isinstance(position, list) and len(position) == 2:
        return int(position[0]), int(position[1])
    target = event.get("target_tile_or_commodity")
    if isinstance(target, list) and len(target) == 2:
        return int(target[0]), int(target[1])
    return None


def seed_inventory(event: dict[str, Any], side: str = "before") -> dict[str, int]:
    state = event.get(f"relevant_state_{side}") or {}
    seeds = state.get("seeds") or {}
    return {crop: int(seeds.get(crop, 0)) for crop in sorted(CROP_NAMES)}


def total_seeds(event: dict[str, Any], side: str = "before") -> int:
    return sum(seed_inventory(event, side).values())


def actor_events_for_treatment(
    events: list[dict[str, Any]], treatment_seat: int
) -> list[dict[str, Any]]:
    return [
        event
        for event in events
        if int(event.get("player", -1)) == treatment_seat
        and event.get("actor_or_order_type") != "market_order"
    ]


def market_events_for_treatment(
    events: list[dict[str, Any]], treatment_seat: int
) -> list[dict[str, Any]]:
    return [
        event
        for event in events
        if int(event.get("player", -1)) == treatment_seat
        and event.get("actor_or_order_type") == "market_order"
    ]


def is_crop_harvest(event: dict[str, Any]) -> bool:
    tile = (event.get("relevant_state_before") or {}).get("tile")
    return (
        first_op(event) == "HARVEST"
        and isinstance(tile, dict)
        and tile.get("kind") == "PLANT"
    )


def state_value_at(
    state_by_step: dict[int, dict[str, Any]], step: int, key: str
) -> Any:
    row = state_by_step.get(step)
    return row.get(key) if row else None


def canonical_state_step(row: dict[str, Any]) -> int:
    """Use seat-stable day/hour because seat-1 observation.step stays zero."""

    return int(row["day"]) * 24 + int(row["hour"])


def reconstruct_harvest_replant(
    actor_events: list[dict[str, Any]], steady_end: int
) -> dict[str, Any]:
    open_harvests: dict[tuple[int, int], deque[int]] = defaultdict(deque)
    first_planted_positions: set[tuple[int, int]] = set()
    initial_plants = 0
    replants = 0
    latencies: list[int] = []
    crop_harvest_executed = 0
    crop_harvest_failed = 0
    crop_harvest_failed_immature = 0
    dig_attempted = 0
    dig_executed = 0

    for event in actor_events:
        op = first_op(event)
        status = event.get("execution_status")
        position = tile_position(event)
        if op == "DIG":
            dig_attempted += 1
            dig_executed += int(status == "executed")
        if is_crop_harvest(event):
            if status == "executed":
                crop_harvest_executed += 1
                if position is not None:
                    open_harvests[position].append(int(event["step"]))
            else:
                crop_harvest_failed += 1
                tile = (event.get("relevant_state_before") or {}).get("tile") or {}
                crop = tile.get("crop")
                planted_day = tile.get("planted_day")
                if (
                    crop in FIRST_YIELD_DAY
                    and planted_day is not None
                    and int(event["day"]) - int(planted_day) < FIRST_YIELD_DAY[crop]
                ):
                    crop_harvest_failed_immature += 1
        if op != "PLANT" or status != "executed" or position is None:
            continue
        if open_harvests[position]:
            harvest_step = open_harvests[position].popleft()
            latencies.append(int(event["step"]) - harvest_step)
            replants += 1
        elif position not in first_planted_positions:
            initial_plants += 1
        else:
            # The preceding removal was not an executed HARVEST in the ledger,
            # so this is a recovery/replant with unresolved removal cause.
            replants += 1
        first_planted_positions.add(position)

    unmatched_pre_shutdown = sum(
        sum(step < steady_end for step in steps) for steps in open_harvests.values()
    )
    return {
        "initial_plant_count": initial_plants,
        "replant_count": replants,
        "crop_harvest_executed": crop_harvest_executed,
        "crop_harvest_failed": crop_harvest_failed,
        "crop_harvest_failure_rate": ratio(
            crop_harvest_failed, crop_harvest_executed + crop_harvest_failed
        ),
        "crop_harvest_failed_immature": crop_harvest_failed_immature,
        "crop_harvest_failed_immature_fraction_of_failures": ratio(
            crop_harvest_failed_immature, crop_harvest_failed
        ),
        "dig_attempted": dig_attempted,
        "dig_executed": dig_executed,
        "harvest_to_replant_n": len(latencies),
        "harvest_to_replant_median_steps": median(latencies),
        "harvest_to_replant_p90_steps": quantile(latencies, 0.90),
        "harvest_to_replant_max_steps": max(latencies) if latencies else None,
        "unmatched_harvests_before_shutdown": unmatched_pre_shutdown,
    }


def threshold_step(
    rows: list[dict[str, Any]], target: int, threshold: float, t0_step: int
) -> int | None:
    required = math.ceil(target * threshold)
    for row in rows:
        if int(row["active_crop_surface"]) >= required:
            return int(row["_canonical_step"]) - t0_step
    return None


def event_step_samples(
    actor_events: list[dict[str, Any]], start_step: int, end_step: int
) -> dict[int, dict[str, Any]]:
    samples: dict[int, dict[str, Any]] = {}
    for event in actor_events:
        step = int(event["step"])
        if start_step <= step < end_step and step not in samples:
            samples[step] = event
    return samples


def episode_metrics(
    result: dict[str, Any], events: list[dict[str, Any]], source_path: Path
) -> dict[str, Any]:
    telemetry = result["telemetry"]
    config = result["cell_config"]
    target = int(config["crop_working_set_target"])
    t0_step_reported = int(telemetry["t0_step"])
    steady_start_day = int(telemetry["steady_window"]["start_day"])
    steady_start = steady_start_day * 24
    steady_end = int(telemetry["steady_window"]["end_step_exclusive"])
    rows = [
        {**row, "_canonical_step": canonical_state_step(row)}
        for row in telemetry["state_rows"]
    ]
    raw_state_steps = {int(row["step"]) for row in rows}
    raw_state_step_reliable = len(raw_state_steps) > 1
    # Paired seat-0 runs locate T0 at actual step 1. Seat-1 summaries report
    # zero because their observation.step field is frozen at zero.
    t0_step = t0_step_reported if raw_state_step_reliable else 1
    analysis_rows = [
        row for row in rows if t0_step <= int(row["_canonical_step"]) < steady_end
    ]
    steady_rows = [
        row
        for row in rows
        if steady_start <= int(row["_canonical_step"]) < steady_end
    ]
    actor_events = actor_events_for_treatment(events, int(result["treatment_seat"]))
    market_events = market_events_for_treatment(events, int(result["treatment_seat"]))
    steady_actor = [
        event
        for event in actor_events
        if steady_start <= int(event["step"]) < steady_end
    ]
    steady_market = [
        event
        for event in market_events
        if steady_start <= int(event["step"]) < steady_end
    ]

    gaps = [max(0, target - int(row["active_crop_surface"])) for row in steady_rows]
    max_active = max((int(row["active_crop_surface"]) for row in analysis_rows), default=0)
    peak_step = next(
        (
            int(row["_canonical_step"]) - t0_step
            for row in analysis_rows
            if int(row["active_crop_surface"]) == max_active
        ),
        None,
    )
    steady_final_active = (
        int(steady_rows[-1]["active_crop_surface"]) if steady_rows else None
    )

    applied_counts = Counter(first_op(event) or "UNOBSERVED" for event in steady_actor)
    status_counts = Counter(str(event.get("execution_status")) for event in steady_actor)
    movement = sum(applied_counts[move] for move in MOVES)
    productive = sum(applied_counts[op] for op in PRODUCTIVE_OPS)
    pass_noop = applied_counts["PASS"] + status_counts["no_op"] - sum(
        first_op(event) == "PASS" and event.get("execution_status") == "no_op"
        for event in steady_actor
    )

    samples = event_step_samples(actor_events, steady_start, steady_end)
    gap_steps = [
        int(row["_canonical_step"])
        for row in steady_rows
        if max(0, target - int(row["active_crop_surface"])) > 0
        and int(row["_canonical_step"]) in samples
    ]
    gap_seed_totals = [total_seeds(samples[step]) for step in gap_steps]
    gap_all_seed_types = [
        all(value > 0 for value in seed_inventory(samples[step]).values())
        for step in gap_steps
    ]
    gap_cash = [float(samples[step].get("cash_before") or 0.0) for step in gap_steps]
    gap_actor = [
        event
        for event in steady_actor
        if int(event["step"]) in set(gap_steps)
    ]
    gap_noops = sum(
        first_op(event) == "PASS" or event.get("execution_status") == "no_op"
        for event in gap_actor
    )
    full_capacity_gap_steps = [
        int(row["_canonical_step"])
        for row in steady_rows
        if int(row["worker_capacity"]) == 11
        and max(0, target - int(row["active_crop_surface"])) > 0
    ]
    full_capacity_gap_step_set = set(full_capacity_gap_steps)
    full_capacity_gap_actor = [
        event
        for event in steady_actor
        if int(event["step"]) in full_capacity_gap_step_set
    ]
    full_capacity_gap_noops = sum(
        first_op(event) == "PASS" or event.get("execution_status") == "no_op"
        for event in full_capacity_gap_actor
    )
    full_capacity_gaps = [
        max(0, target - int(row["active_crop_surface"]))
        for row in steady_rows
        if int(row["worker_capacity"]) == 11
    ]

    seed_buys = [event for event in market_events if requested_op(event) == "BUY_SEED"]
    seed_buys_executed = [
        event for event in seed_buys if event.get("execution_status") == "executed"
    ]
    plant_events = [
        event
        for event in actor_events
        if first_op(event) == "PLANT" and event.get("execution_status") == "executed"
    ]
    last_plant_step = max((int(event["step"]) for event in plant_events), default=None)
    buys_after_last_plant = (
        [event for event in seed_buys_executed if int(event["step"]) > last_plant_step]
        if last_plant_step is not None
        else seed_buys_executed
    )
    final_seed_inventory = (
        total_seeds(actor_events[-1], "after") if actor_events else None
    )

    worker_capacity_sum = sum(int(row["worker_capacity"]) for row in steady_rows)
    worker_days = worker_capacity_sum / 24.0
    lifecycle = reconstruct_harvest_replant(actor_events, steady_end)
    cash_samples = [float(event.get("cash_before") or 0.0) for event in samples.values()]
    flow = telemetry.get("realized_cash_flow_by_category", {})

    working_set = set(CROP_POSITIONS[:target])
    weed_observations: list[tuple[int, tuple[int, int]]] = []
    for event in actor_events:
        for side in ("before", "after"):
            state = event.get(f"relevant_state_{side}") or {}
            position = state.get("position")
            tile = state.get("tile")
            if (
                isinstance(position, list)
                and len(position) == 2
                and isinstance(tile, dict)
                and tile.get("kind") == "WEED"
            ):
                observed_position = (int(position[0]), int(position[1]))
                if observed_position in working_set:
                    weed_observations.append((int(event["step"]), observed_position))
    unique_weed_positions = {position for _, position in weed_observations}

    reached_80_step = next(
        (
            int(row["_canonical_step"])
            for row in analysis_rows
            if int(row["active_crop_surface"]) >= math.ceil(target * 0.8)
        ),
        None,
    )
    first_below_50_after_80 = None
    if reached_80_step is not None:
        first_below_50_after_80 = next(
            (
                int(row["_canonical_step"]) - t0_step
                for row in analysis_rows
                if int(row["_canonical_step"]) > reached_80_step
                and int(row["active_crop_surface"]) < math.ceil(target * 0.5)
            ),
            None,
        )

    daily_active: dict[int, list[int]] = defaultdict(list)
    for row in steady_rows:
        daily_active[int(row["day"])].append(int(row["active_crop_surface"]))
    reconstructed_attainment = median(
        statistics.median(values) / target for values in daily_active.values()
    )
    steady_days = sorted(daily_active)
    daily_need = telemetry.get("daily_watering_need_denominator", {})
    daily_effect = telemetry.get("daily_successful_watering_effects", {})
    watering_days = [day for day in steady_days if int(daily_need.get(str(day), 0)) > 0]
    reconstructed_water_needs = sum(int(daily_need.get(str(day), 0)) for day in watering_days)
    reconstructed_water_effects = sum(
        int(daily_effect.get(str(day), 0)) for day in watering_days
    )
    reconstructed_watering_execution = ratio(
        reconstructed_water_effects, reconstructed_water_needs
    )
    reconstructed_watering_continuity = ratio(
        sum(
            int(daily_effect.get(str(day), 0))
            / int(daily_need.get(str(day), 0))
            >= 0.5
            for day in watering_days
        ),
        len(watering_days),
    )

    output: dict[str, Any] = {
        "episode_id": result["episode_id"],
        "cell": result["cell_id"],
        "seed": int(result["seed"]),
        "treatment_seat": int(result["treatment_seat"]),
        "water_priority": float(config["watering_dispatch_priority"]),
        "crop_target": target,
        "completed": bool(result["completed"]),
        "total_steps": int(result["total_steps"]),
        "final_money": float(telemetry["final_money_observational_only"]),
        "crop_target_attainment": float(telemetry["crop_target_attainment"]),
        "reconstructed_crop_target_attainment": reconstructed_attainment,
        "reconstructed_minus_reported_attainment": (
            reconstructed_attainment - float(telemetry["crop_target_attainment"])
            if reconstructed_attainment is not None
            else None
        ),
        "watering_execution_rate": float(telemetry["watering_execution_rate"]),
        "watering_continuity": float(telemetry["watering_continuity"]),
        "reconstructed_watering_execution_rate": reconstructed_watering_execution,
        "reconstructed_watering_continuity": reconstructed_watering_continuity,
        "t0_step_reported": t0_step_reported,
        "t0_step_reconstructed": t0_step,
        "raw_state_step_reliable": raw_state_step_reliable,
        "raw_state_step_unique_count": len(raw_state_steps),
        "steady_start_step": steady_start,
        "steady_end_step_exclusive": steady_end,
        "first_50pct_steps_after_t0": threshold_step(
            analysis_rows, target, 0.50, t0_step
        ),
        "first_80pct_steps_after_t0": threshold_step(
            analysis_rows, target, 0.80, t0_step
        ),
        "first_100pct_steps_after_t0": threshold_step(
            analysis_rows, target, 1.00, t0_step
        ),
        "steady_fraction_at_or_above_50pct": ratio(
            sum(int(row["active_crop_surface"]) >= math.ceil(target * 0.50) for row in steady_rows),
            len(steady_rows),
        ),
        "steady_fraction_at_or_above_80pct": ratio(
            sum(int(row["active_crop_surface"]) >= math.ceil(target * 0.80) for row in steady_rows),
            len(steady_rows),
        ),
        "steady_fraction_at_or_above_100pct": ratio(
            sum(int(row["active_crop_surface"]) >= target for row in steady_rows),
            len(steady_rows),
        ),
        "max_active_pre_shutdown": max_active,
        "peak_active_fraction": ratio(max_active, target),
        "peak_step_after_t0": peak_step,
        "steady_mean_active": mean(
            float(row["active_crop_surface"]) for row in steady_rows
        ),
        "steady_final_active": steady_final_active,
        "post_peak_active_decay": (
            max_active - steady_final_active if steady_final_active is not None else None
        ),
        "first_below_50pct_after_reaching_80pct_steps_after_t0": first_below_50_after_80,
        "steady_median_target_gap": median(float(value) for value in gaps),
        "steady_max_target_gap": max(gaps) if gaps else None,
        "steady_cumulative_target_gap_tile_steps": sum(gaps),
        "crop_losses": int(telemetry["crop_losses"]),
        "working_set_weed_observation_events": len(weed_observations),
        "unique_working_set_weed_tiles_observed": len(unique_weed_positions),
        "first_working_set_weed_observation_step": (
            min(step for step, _ in weed_observations) if weed_observations else None
        ),
        "last_working_set_weed_observation_step": (
            max(step for step, _ in weed_observations) if weed_observations else None
        ),
        "worker_capacity_peak": int(telemetry["worker_capacity"]),
        "steady_worker_capacity_median": median(
            float(row["worker_capacity"]) for row in steady_rows
        ),
        "steady_worker_capacity_mean": mean(
            float(row["worker_capacity"]) for row in steady_rows
        ),
        "steady_worker_capacity_min": min(
            (int(row["worker_capacity"]) for row in steady_rows), default=None
        ),
        "steady_full_11_worker_capacity_fraction": ratio(
            sum(int(row["worker_capacity"]) == 11 for row in steady_rows),
            len(steady_rows),
        ),
        "steady_single_worker_capacity_fraction": ratio(
            sum(int(row["worker_capacity"]) == 1 for row in steady_rows),
            len(steady_rows),
        ),
        "full_capacity_median_target_gap": median(
            float(value) for value in full_capacity_gaps
        ),
        "full_capacity_gap_actor_pass_or_noop_share": ratio(
            full_capacity_gap_noops, len(full_capacity_gap_actor)
        ),
        "telemetry_worker_utilization": float(telemetry["worker_utilization"]),
        "steady_total_actor_slots": len(steady_actor),
        "steady_movement_actions": movement,
        "steady_movement_share": ratio(movement, len(steady_actor)),
        "steady_productive_actions": productive,
        "steady_productive_share": ratio(productive, len(steady_actor)),
        "steady_productive_actions_per_worker_day": ratio(productive, worker_days),
        "steady_pass_or_noop_actions": pass_noop,
        "steady_pass_or_noop_share": ratio(pass_noop, len(steady_actor)),
        "steady_failed_action_share": ratio(status_counts["failed"], len(steady_actor)),
        "steady_movement_per_executed_crop_action": ratio(
            movement,
            sum(
                event.get("execution_status") == "executed"
                and first_op(event) in {"WATER", "HARVEST", "PLANT", "DIG"}
                for event in steady_actor
            ),
        ),
        "gap_steps_with_seed_sample": len(gap_steps),
        "gap_steps_any_seed_available_fraction": ratio(
            sum(value > 0 for value in gap_seed_totals), len(gap_seed_totals)
        ),
        "gap_steps_all_mix_seed_types_available_fraction": ratio(
            sum(gap_all_seed_types), len(gap_all_seed_types)
        ),
        "gap_step_seed_inventory_median": median(
            float(value) for value in gap_seed_totals
        ),
        "gap_action_slots_pass_or_noop_share": ratio(gap_noops, len(gap_actor)),
        "seed_buy_order_count": len(seed_buys),
        "seed_buy_executed_count": len(seed_buys_executed),
        "seed_buy_executed_quantity": sum(
            int(event.get("executed_quantity") or 0) for event in seed_buys_executed
        ),
        "seed_buy_failed_count": sum(
            event.get("execution_status") != "executed" for event in seed_buys
        ),
        "last_plant_step": last_plant_step,
        "seed_buy_quantity_after_last_plant": sum(
            int(event.get("executed_quantity") or 0) for event in buys_after_last_plant
        ),
        "final_seed_inventory": final_seed_inventory,
        "steady_cash_min": min(cash_samples) if cash_samples else None,
        "steady_cash_median": median(cash_samples),
        "gap_steps_cash_at_floor_fraction": ratio(
            sum(value <= FLOOR for value in gap_cash), len(gap_cash)
        ),
        "gap_steps_cash_above_floor_fraction": ratio(
            sum(value > FLOOR for value in gap_cash), len(gap_cash)
        ),
        "market_order_count": len(market_events),
        "steady_market_order_count": len(steady_market),
        "crop_product_revenue": float(flow.get("crop_product_revenue", 0.0)),
        "livestock_product_revenue": float(
            flow.get("livestock_product_revenue", 0.0)
        ),
        "source_artifact": str(source_path.relative_to(ROOT)).replace("\\", "/"),
    }
    output.update(lifecycle)
    return output


def aggregate_cell(rows: list[dict[str, Any]]) -> dict[str, Any]:
    cell = rows[0]["cell"]
    output: dict[str, Any] = {
        "cell": cell,
        "episode_count": len(rows),
        "water_priority": rows[0]["water_priority"],
        "crop_target": rows[0]["crop_target"],
        "completion_rate": mean(float(row["completed"]) for row in rows),
    }
    excluded = {
        "episode_id",
        "cell",
        "seed",
        "treatment_seat",
        "water_priority",
        "crop_target",
        "completed",
        "source_artifact",
    }
    for key in rows[0]:
        if key in excluded:
            continue
        values = [row[key] for row in rows if isinstance(row[key], (int, float))]
        output[f"median_{key}"] = median(float(value) for value in values)
        output[f"min_{key}"] = min(values) if values else None
        output[f"max_{key}"] = max(values) if values else None
    output["source_artifact"] = ";".join(row["source_artifact"] for row in rows)
    return output


def aggregate_target(rows: list[dict[str, Any]]) -> dict[str, Any]:
    target = int(rows[0]["crop_target"])
    output: dict[str, Any] = {
        "crop_target": target,
        "episode_count": len(rows),
        "cells": ";".join(sorted({str(row["cell"]) for row in rows})),
        "aggregation_role": "observational target scaling; water levels are mixed",
    }
    excluded = {
        "episode_id",
        "cell",
        "seed",
        "treatment_seat",
        "water_priority",
        "crop_target",
        "completed",
        "source_artifact",
    }
    for key in rows[0]:
        if key in excluded:
            continue
        values = [row[key] for row in rows if isinstance(row[key], (int, float))]
        output[f"median_{key}"] = median(float(value) for value in values)
        output[f"min_{key}"] = min(values) if values else None
        output[f"max_{key}"] = max(values) if values else None
    output["source_artifact"] = ";".join(row["source_artifact"] for row in rows)
    return output


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def format_value(value: Any) -> str:
    if value is None:
        return "UNRESOLVED"
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def evidence_rows(
    cell_rows: list[dict[str, Any]], episode_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    definitions = [
        (
            "crop_target_attainment",
            "WORKING_SET",
            "DERIVED",
            "Observed frozen attainment metric.",
            "PLANTING_REPLANTING_LOOP",
            "",
        ),
        (
            "peak_active_fraction",
            "PLANTING / REPLANTING LOOP",
            "DERIVED",
            "Separates initial attainment from later maintenance.",
            "PLANTING_REPLANTING_LOOP",
            "FAILURE_TO_ATTAIN_ONLY",
        ),
        (
            "post_peak_active_decay",
            "PLANTING / REPLANTING LOOP",
            "DERIVED",
            "Active tiles lost between observed peak and steady-window end.",
            "PLANTING_REPLANTING_LOOP",
            "FAILURE_TO_ATTAIN_ONLY",
        ),
        (
            "crop_losses",
            "PLANTING / REPLANTING LOOP",
            "DERIVED",
            "Telemetry-counted active-tile removals not reconciled to HARVEST/DIG.",
            "PLANTING_REPLANTING_LOOP",
            "WATER_PRIMARY_WHEN_HIGH_CONTINUITY",
        ),
        (
            "unique_working_set_weed_tiles_observed",
            "PLANTING / REPLANTING LOOP",
            "DIRECT",
            "Unique nominal crop positions directly observed as WEED in ledger snapshots.",
            "PLANTING_REPLANTING_LOOP",
            "NO_BLOCKED_TILE_STATE",
        ),
        (
            "crop_harvest_failure_rate",
            "PLANTING / REPLANTING LOOP",
            "DERIVED",
            "Failed crop HARVEST attempts divided by all applied crop HARVEST attempts.",
            "HARVEST_READINESS_MISMATCH",
            "EFFICIENT_HARVEST_LOOP",
        ),
        (
            "crop_harvest_failed_immature_fraction_of_failures",
            "PLANTING / REPLANTING LOOP",
            "DERIVED",
            "Share of failed crop HARVEST attempts occurring before engine first_yield_day.",
            "HARVEST_READINESS_MISMATCH",
            "FAILURES_UNRELATED_TO_MATURITY",
        ),
        (
            "dig_executed",
            "PLANTING / REPLANTING LOOP",
            "DIRECT",
            "Executed DIG events in treatment ledger.",
            "PLANTING_REPLANTING_LOOP",
            "WEED_RECOVERY_PRESENT",
        ),
        (
            "steady_movement_share",
            "ROUTING / TRANSIT OVERHEAD",
            "DERIVED",
            "Applied movement actions divided by treatment actor slots.",
            "ROUTING_TRANSIT",
            "",
        ),
        (
            "gap_action_slots_pass_or_noop_share",
            "WORKFORCE / ACTION CAPACITY",
            "DERIVED",
            "Idle/no-op actor slots while active crop count is below target.",
            "DISPATCH_OR_LOOP_GAP",
            "PURE_WORKFORCE_SATURATION",
        ),
        (
            "steady_worker_capacity_mean",
            "WORKFORCE / ACTION CAPACITY",
            "DERIVED",
            "Mean available farmer-plus-hand count in the steady window.",
            "INTERMITTENT_WORKFORCE_CAPACITY",
            "CONTINUOUS_NOMINAL_WORKFORCE",
        ),
        (
            "full_capacity_median_target_gap",
            "WORKFORCE / ACTION CAPACITY",
            "DERIVED",
            "Median target gap on state rows with all 11 actors available.",
            "GAP_PERSISTS_AT_FULL_CAPACITY",
            "PURE_WORKFORCE_AVAILABILITY",
        ),
        (
            "gap_steps_any_seed_available_fraction",
            "SEED REPLENISHMENT",
            "DERIVED",
            "Fraction of sampled deficit steps with positive crop-seed inventory.",
            "INPUT_AVAILABLE_DURING_GAP",
            "TOTAL_SEED_STOCKOUT_PRIMARY",
        ),
        (
            "seed_buy_quantity_after_last_plant",
            "SEED REPLENISHMENT",
            "DERIVED",
            "Executed seed purchases after the final successful PLANT.",
            "INPUT_AVAILABLE_BUT_NOT_ACTIVATED",
            "SEED_ACQUISITION_ABSENT",
        ),
        (
            "gap_steps_cash_above_floor_fraction",
            "MARKET PACING / CAPITAL AVAILABILITY",
            "DERIVED",
            "Fraction of sampled deficit steps with cash above the frozen floor.",
            "CAPITAL_AVAILABLE_DURING_GAP",
            "CAPITAL_PRIMARY",
        ),
        (
            "watering_execution_rate",
            "WATER DISPATCH",
            "DERIVED",
            "Corrected global HIGH/LOW watering execution measurement.",
            "WATER_REALIZATION",
            "WATER_PRIMARY_WHEN_HIGH_AND_GAP_PERSISTS",
        ),
    ]
    output: list[dict[str, Any]] = []
    finding_number = 1
    for cell in cell_rows:
        for metric, bottleneck, evidence_class, interpretation, supports, contradicts in definitions:
            key = f"median_{metric}"
            output.append(
                {
                    "finding_id": f"CELL-{finding_number:03d}",
                    "cell": cell["cell"],
                    "episode/seed": "4 preregistered seed-seat episodes",
                    "time_window": "steady window unless metric is terminal/full-episode",
                    "candidate_bottleneck": bottleneck,
                    "metric/evidence": metric,
                    "value": format_value(cell.get(key)),
                    "evidence_class": evidence_class,
                    "interpretation": interpretation,
                    "supports": supports,
                    "contradicts": contradicts,
                    "source_artifact": cell["source_artifact"],
                }
            )
            finding_number += 1
    output.append(
        {
            "finding_id": "CODE-001",
            "cell": "ALL",
            "episode/seed": "frozen treatment build",
            "time_window": "policy definition",
            "candidate_bottleneck": "PLANTING / REPLANTING LOOP",
            "metric/evidence": "dispatcher_has_DIG_branch",
            "value": "FALSE",
            "evidence_class": "DIRECT",
            "interpretation": (
                "The frozen dispatcher creates PLANT tasks only for None tiles and "
                "contains no DIG task for WEED tiles."
            ),
            "supports": "PLANTING_REPLANTING_LOOP",
            "contradicts": "WEED_RECOVERY_PRESENT",
            "source_artifact": "experiments/archive/e16/artifacts/manifests/E16_TREATMENT_BUILD_R1.py",
        }
    )
    output.extend(
        [
            {
                "finding_id": "GLOBAL-001",
                "cell": "ALL",
                "episode/seed": "28/28 episodes",
                "time_window": "full episode",
                "candidate_bottleneck": "PLANTING / REPLANTING LOOP",
                "metric/evidence": "weed_observed_and_DIG_executed",
                "value": (
                    f"weed_positive_episodes={sum(row['unique_working_set_weed_tiles_observed'] > 0 for row in episode_rows)};"
                    f"DIG_executed={sum(row['dig_executed'] for row in episode_rows)}"
                ),
                "evidence_class": "DIRECT",
                "interpretation": "Every episode exposes a WEED sink in the nominal working set; no recovery action executes.",
                "supports": "PLANTING_REPLANTING_LOOP",
                "contradicts": "WEED_RECOVERY_PRESENT",
                "source_artifact": "28 R1 event ledgers",
            },
            {
                "finding_id": "GLOBAL-002",
                "cell": "ALL",
                "episode/seed": "28/28 episodes",
                "time_window": "full episode",
                "candidate_bottleneck": "PLANTING / REPLANTING LOOP",
                "metric/evidence": "failed_crop_HARVEST_before_first_yield_day",
                "value": (
                    f"{sum(row['crop_harvest_failed_immature'] for row in episode_rows):.0f}/"
                    f"{sum(row['crop_harvest_failed'] for row in episode_rows):.0f} failed attempts"
                ),
                "evidence_class": "DERIVED",
                "interpretation": "All failed crop HARVEST attempts occur before the engine maturity precondition.",
                "supports": "HARVEST_READINESS_MISMATCH",
                "contradicts": "EFFICIENT_HARVEST_LOOP",
                "source_artifact": "28 R1 event ledgers; engine crop preconditions",
            },
            {
                "finding_id": "OBS-001",
                "cell": "ALL",
                "episode/seed": "14 treatment-seat-1 episodes",
                "time_window": "full state-row series",
                "candidate_bottleneck": "OBSERVABILITY",
                "metric/evidence": "state_rows.step_unique_count",
                "value": (
                    f"unreliable={sum(not row['raw_state_step_reliable'] for row in episode_rows)}/28;"
                    "all 14 are seat 1"
                ),
                "evidence_class": "DIRECT",
                "interpretation": "Seat-1 state-row step is constant zero; day/hour and ledger step support deterministic reconstruction.",
                "supports": "DIAGNOSTIC_TIME_RECONSTRUCTION_REQUIRED",
                "contradicts": "STATE_STEP_SEAT_INVARIANT",
                "source_artifact": "14 seat-1 R1 summaries and ledgers",
            },
        ]
    )
    return output


def representative(rows: list[dict[str, Any]]) -> dict[str, Any]:
    money_median = statistics.median(row["final_money"] for row in rows)
    attainment_median = statistics.median(
        row["crop_target_attainment"] for row in rows
    )
    money_span = max(row["final_money"] for row in rows) - min(
        row["final_money"] for row in rows
    )
    attainment_span = max(row["crop_target_attainment"] for row in rows) - min(
        row["crop_target_attainment"] for row in rows
    )

    def score(row: dict[str, Any]) -> tuple[float, str]:
        money_distance = abs(row["final_money"] - money_median) / (money_span or 1.0)
        attainment_distance = abs(
            row["crop_target_attainment"] - attainment_median
        ) / (attainment_span or 1.0)
        return money_distance + attainment_distance, row["episode_id"]

    selected = min(rows, key=score)
    selected = dict(selected)
    selected["selection_score"] = score(selected)[0]
    selected["cell_median_final_money"] = float(money_median)
    selected["cell_median_attainment"] = float(attainment_median)
    return selected


def selected_trace_rows(
    result: dict[str, Any], events: list[dict[str, Any]], selection_reason: str
) -> list[dict[str, Any]]:
    telemetry = result["telemetry"]
    target = int(result["cell_config"]["crop_working_set_target"])
    state_rows = telemetry["state_rows"]
    state_by_step = {canonical_state_step(row): row for row in state_rows}
    actor_events = actor_events_for_treatment(events, int(result["treatment_seat"]))
    market_events = market_events_for_treatment(events, int(result["treatment_seat"]))
    plant_events = [
        event
        for event in actor_events
        if first_op(event) == "PLANT" and event.get("execution_status") == "executed"
    ]
    crop_harvests = [
        event
        for event in actor_events
        if is_crop_harvest(event) and event.get("execution_status") == "executed"
    ]
    seed_buys = [
        event
        for event in market_events
        if requested_op(event) == "BUY_SEED"
        and event.get("execution_status") == "executed"
    ]
    last_plant = max((int(event["step"]) for event in plant_events), default=-1)

    chosen: list[tuple[str, dict[str, Any]]] = []
    for role, candidates in (
        ("FIRST_PLANT", plant_events[:1]),
        ("LAST_PLANT", plant_events[-1:]),
        ("FIRST_CROP_HARVEST", crop_harvests[:1]),
        ("LAST_CROP_HARVEST", crop_harvests[-1:]),
        ("FIRST_SEED_BUY", seed_buys[:1]),
        ("LAST_SEED_BUY", seed_buys[-1:]),
        (
            "SEED_BUY_AFTER_LAST_PLANT",
            [event for event in seed_buys if int(event["step"]) > last_plant][:3],
        ),
    ):
        chosen.extend((role, event) for event in candidates)

    max_active = max(int(row["active_crop_surface"]) for row in state_rows)
    state_milestones: list[tuple[str, dict[str, Any]]] = []
    for role, predicate in (
        ("FIRST_50PCT_STATE", lambda row: int(row["active_crop_surface"]) >= math.ceil(target * 0.5)),
        ("FIRST_80PCT_STATE", lambda row: int(row["active_crop_surface"]) >= math.ceil(target * 0.8)),
        ("FIRST_100PCT_STATE", lambda row: int(row["active_crop_surface"]) >= target),
        ("FIRST_PEAK_STATE", lambda row: int(row["active_crop_surface"]) == max_active),
    ):
        row = next((item for item in state_rows if predicate(item)), None)
        if row is not None:
            state_milestones.append((role, row))

    output: list[dict[str, Any]] = []
    source = f"results/e16/stage_a_r1/{result['episode_id']}.events.jsonl"
    for role, event in chosen:
        step = int(event["step"])
        state = state_by_step.get(step, {})
        before_seeds = total_seeds(event, "before")
        after_seeds = total_seeds(event, "after")
        op = first_op(event) if event.get("actor_or_order_type") != "market_order" else requested_op(event)
        output.append(
            {
                "episode_id": result["episode_id"],
                "cell": result["cell_id"],
                "selection_reason": selection_reason,
                "step": step,
                "day": int(event["day"]),
                "hour": int(event["hour"]),
                "actor_type": event["actor_or_order_type"],
                "unit_index": event.get("unit_index"),
                "operation": op,
                "status": event.get("execution_status"),
                "tile_or_commodity": json.dumps(event.get("target_tile_or_commodity")),
                "cash_before": event.get("cash_before"),
                "cash_after": event.get("cash_after"),
                "seed_total_before": before_seeds,
                "seed_total_after": after_seeds,
                "active_crop_count": state.get("active_crop_surface"),
                "target_gap": (
                    target - int(state["active_crop_surface"])
                    if state.get("active_crop_surface") is not None
                    else None
                ),
                "event_role": role,
                "source_artifact": source,
            }
        )
    for role, row in state_milestones:
        output.append(
            {
                "episode_id": result["episode_id"],
                "cell": result["cell_id"],
                "selection_reason": selection_reason,
                "step": canonical_state_step(row),
                "day": int(row["day"]),
                "hour": int(row["hour"]),
                "actor_type": "state_row",
                "unit_index": None,
                "operation": "STATE_MILESTONE",
                "status": "observed",
                "tile_or_commodity": None,
                "cash_before": None,
                "cash_after": None,
                "seed_total_before": None,
                "seed_total_after": None,
                "active_crop_count": int(row["active_crop_surface"]),
                "target_gap": target - int(row["active_crop_surface"]),
                "event_role": role,
                "source_artifact": f"results/e16/stage_a_r1/{result['episode_id']}.json",
            }
        )
    return sorted(output, key=lambda row: (int(row["step"]), str(row["event_role"])))


def daily_trace_markdown(
    result: dict[str, Any], events: list[dict[str, Any]], selection: dict[str, Any]
) -> str:
    telemetry = result["telemetry"]
    target = int(result["cell_config"]["crop_working_set_target"])
    actor_events = actor_events_for_treatment(events, int(result["treatment_seat"]))
    market_events = market_events_for_treatment(events, int(result["treatment_seat"]))
    by_day_state: dict[int, list[dict[str, Any]]] = defaultdict(list)
    by_day_actor: dict[int, list[dict[str, Any]]] = defaultdict(list)
    by_day_market: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in telemetry["state_rows"]:
        by_day_state[int(row["day"])].append(row)
    for event in actor_events:
        by_day_actor[int(event["day"])].append(event)
    for event in market_events:
        by_day_market[int(event["day"])].append(event)

    lines = [
        f"## {result['cell_id']} - `{result['episode_id']}`",
        "",
        (
            "Selection: minimum normalized distance from the cell medians of "
            f"final money (${selection['cell_median_final_money']:.2f}) and attainment "
            f"({selection['cell_median_attainment']:.4f}); score "
            f"{selection['selection_score']:.4f}."
        ),
        "",
        "Daily aggregation below is reconstructed from event-level ledger rows; counts use `engine_applied_payload` for actor operations.",
        "",
        "| Day | Active median [min,max] | Gap median | Move | Water X/F | Crop harvest X/F | Plant X/F | Dig X/F | Pass/no-op | Seed buy qty | Cash median | Seeds median |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for day in sorted(by_day_state):
        states = by_day_state[day]
        actors = by_day_actor[day]
        markets = by_day_market[day]
        active_values = [int(row["active_crop_surface"]) for row in states]
        gap_values = [max(0, target - value) for value in active_values]
        moves = sum(first_op(event) in MOVES for event in actors)

        def executed_failed(
            actor_rows: list[dict[str, Any]], op: str, crop_only: bool = False
        ) -> tuple[int, int]:
            candidates = [event for event in actor_rows if first_op(event) == op]
            if crop_only:
                candidates = [event for event in candidates if is_crop_harvest(event)]
            return (
                sum(event.get("execution_status") == "executed" for event in candidates),
                sum(event.get("execution_status") != "executed" for event in candidates),
            )

        water = executed_failed(actors, "WATER")
        harvest = executed_failed(actors, "HARVEST", crop_only=True)
        plant = executed_failed(actors, "PLANT")
        dig = executed_failed(actors, "DIG")
        passes = sum(
            first_op(event) == "PASS" or event.get("execution_status") == "no_op"
            for event in actors
        )
        seed_qty = sum(
            int(event.get("executed_quantity") or 0)
            for event in markets
            if requested_op(event) == "BUY_SEED"
            and event.get("execution_status") == "executed"
        )
        samples = event_step_samples(actors, day * 24, (day + 1) * 24)
        cash = [float(event.get("cash_before") or 0.0) for event in samples.values()]
        seeds = [float(total_seeds(event)) for event in samples.values()]
        lines.append(
            "| "
            + " | ".join(
                [
                    str(day),
                    f"{statistics.median(active_values):.1f} [{min(active_values)},{max(active_values)}]",
                    f"{statistics.median(gap_values):.1f}",
                    str(moves),
                    f"{water[0]}/{water[1]}",
                    f"{harvest[0]}/{harvest[1]}",
                    f"{plant[0]}/{plant[1]}",
                    f"{dig[0]}/{dig[1]}",
                    str(passes),
                    str(seed_qty),
                    f"{statistics.median(cash):.1f}" if cash else "NA",
                    f"{statistics.median(seeds):.1f}" if seeds else "NA",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Ledger sequence summary: movement precedes dispersed productive actions throughout the ramp; successful harvests and replants occur, but no `DIG` event is observed. Exact selected milestones are in `E16_A_R1_SELECTED_EVENT_TRACE.csv`.",
            "",
        ]
    )
    return "\n".join(lines)


def verify_integrity(
    manifest: dict[str, Any], config: dict[str, Any]
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    for run in manifest["runs"]:
        path = ROOT / run["result_path"]
        actual = sha256(path)
        checks.append(
            {
                "artifact": run["result_path"],
                "expected_sha256": run["result_sha256"],
                "actual_sha256": actual,
                "match": actual == run["result_sha256"],
            }
        )
    frozen_refs = [
        (config["frozen_design_path"], config["frozen_design_sha256"]),
        (
            config["semantic_clarification_path"],
            config["semantic_clarification_sha256"],
        ),
        (config["predecessor_config_path"], config["predecessor_config_sha256"]),
        (
            config["predecessor_treatment_build_path"],
            config["predecessor_treatment_build_sha256"],
        ),
        (config["treatment_build_path"], config["treatment_build_sha256"]),
        (config["opponent_path"], config["opponent_sha256"]),
    ]
    for relative_path, expected in frozen_refs:
        path = ROOT / relative_path
        actual = sha256(path)
        checks.append(
            {
                "artifact": relative_path,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "match": actual == expected,
            }
        )
    checks.append(
        {
            "artifact": str(R1_CONFIG.relative_to(ROOT)).replace("\\", "/"),
            "expected_sha256": "embedded configuration_sha256 in all R1 episodes",
            "actual_sha256": sha256(R1_CONFIG),
            "match": all(
                json.loads((ROOT / run["result_path"]).read_text(encoding="utf-8"))[
                    "configuration_sha256"
                ]
                == sha256(R1_CONFIG)
                for run in manifest["runs"]
            ),
        }
    )
    return {
        "manifest_status": manifest["status"],
        "manifest_episode_count": manifest["episode_count"],
        "completed_run_count": sum(run["status"] == "COMPLETED" for run in manifest["runs"]),
        "summary_json_count": len(list(INPUT_DIR.glob("E16-A-R1-*.json"))),
        "event_ledger_count": len(list(INPUT_DIR.glob("E16-A-R1-*.events.jsonl"))),
        "all_checks_pass": all(check["match"] for check in checks),
        "checks": checks,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(RUN_MANIFEST.read_text(encoding="utf-8"))
    config = json.loads(R1_CONFIG.read_text(encoding="utf-8"))
    integrity = verify_integrity(manifest, config)
    if not integrity["all_checks_pass"]:
        raise RuntimeError("R1 integrity verification failed")
    if integrity["manifest_episode_count"] != 28:
        raise RuntimeError("R1 manifest does not contain exactly 28 episodes")

    episode_rows: list[dict[str, Any]] = []
    result_by_episode: dict[str, dict[str, Any]] = {}
    events_by_episode: dict[str, list[dict[str, Any]]] = {}
    for run in manifest["runs"]:
        result_path = ROOT / run["result_path"]
        result = json.loads(result_path.read_text(encoding="utf-8"))
        ledger_path = result_path.with_suffix(".events.jsonl")
        with ledger_path.open(encoding="utf-8") as handle:
            events = [json.loads(line) for line in handle if line.strip()]
        episode_id = result["episode_id"]
        result_by_episode[episode_id] = result
        events_by_episode[episode_id] = events
        episode_rows.append(episode_metrics(result, events, result_path))

    episode_rows.sort(key=lambda row: (row["cell"], row["seed"], row["treatment_seat"]))
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in episode_rows:
        grouped[row["cell"]].append(row)
    cell_rows = [aggregate_cell(grouped[cell]) for cell in sorted(grouped)]
    grouped_target: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in episode_rows:
        grouped_target[int(row["crop_target"])].append(row)
    target_rows = [
        aggregate_target(grouped_target[target]) for target in sorted(grouped_target)
    ]

    write_csv(OUTPUT_DIR / "E16_A_R1_EPISODE_DIAGNOSTIC_SUMMARY.csv", episode_rows)
    write_csv(OUTPUT_DIR / "E16_A_R1_CELL_DIAGNOSTIC_SUMMARY.csv", cell_rows)
    write_csv(OUTPUT_DIR / "E16_A_R1_TARGET_DIAGNOSTIC_SUMMARY.csv", target_rows)
    write_csv(
        OUTPUT_DIR / "E16_A_R1_EVIDENCE_TABLE.csv",
        evidence_rows(cell_rows, episode_rows),
    )

    selected: list[dict[str, Any]] = []
    trace_csv: list[dict[str, Any]] = []
    trace_sections = [
        "# E16 A-R1 Selected Event-Level Traces",
        "",
        "These traces are diagnostic reconstructions from completed R1 ledgers. They are not new gameplay evidence.",
        "",
    ]
    for cell in ("A02", "A07", "A04"):
        selection = representative(grouped[cell])
        selected.append(selection)
        episode_id = selection["episode_id"]
        result = result_by_episode[episode_id]
        events = events_by_episode[episode_id]
        reason = (
            "minimum normalized distance to cell medians of final money and "
            "crop-target attainment"
        )
        trace_csv.extend(selected_trace_rows(result, events, reason))
        trace_sections.append(daily_trace_markdown(result, events, selection))

    write_csv(OUTPUT_DIR / "E16_A_R1_SELECTED_EVENT_TRACE.csv", trace_csv)
    (OUTPUT_DIR / "E16_A_R1_SELECTED_EVENT_TRACES.md").write_text(
        "\n".join(trace_sections), encoding="utf-8"
    )
    (OUTPUT_DIR / "E16_A_R1_DIAGNOSTIC_INTEGRITY.json").write_text(
        json.dumps(integrity, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (OUTPUT_DIR / "E16_A_R1_SELECTED_EPISODES.json").write_text(
        json.dumps(selected, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Wrote diagnostics for {len(episode_rows)} episodes to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
