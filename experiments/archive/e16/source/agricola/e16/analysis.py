"""Reproducible Stage A/Stage B analysis and the frozen capacity gate."""

from __future__ import annotations

import hashlib
import json
import statistics
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

GATE_METRICS = (
    "completion_rate",
    "median_post_ramp_watering_execution_rate",
    "median_watering_continuity",
    "median_crop_target_attainment",
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_episode_results(
    directory: Path,
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    rows: list[dict[str, Any]] = []
    hashes: dict[str, str] = {}
    for path in sorted(directory.glob("E16-*.json")):
        rows.append(json.loads(path.read_text(encoding="utf-8")))
        hashes[path.name] = file_sha256(path)
    return rows, hashes


def _median(values: list[float]) -> float:
    return float(statistics.median(values)) if values else 0.0


def compute_stage_b_gate(
    episode_rows: list[dict[str, Any]],
    input_result_hashes: dict[str, str],
    analysis_code_hash: str,
    timestamp: str,
) -> dict[str, Any]:
    """Apply only the four frozen capacity criteria to the HIGH ladder."""

    by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in episode_rows:
        by_cell[row["cell_id"]].append(row)
    expected = {"A02": 10, "A07": 17, "A04": 25}
    metrics_by_cell: dict[str, dict[str, Any]] = {}
    eligible: list[str] = []
    for cell_id, target in expected.items():
        rows = by_cell.get(cell_id, [])
        metrics = {
            "crop_target": target,
            "episode_count": len(rows),
            "completion_rate": sum(bool(row.get("completed")) for row in rows) / 4.0,
            "median_post_ramp_watering_execution_rate": _median(
                [float(row["telemetry"]["watering_execution_rate"]) for row in rows]
            ),
            "median_watering_continuity": _median(
                [float(row["telemetry"]["watering_continuity"]) for row in rows]
            ),
            "median_crop_target_attainment": _median(
                [float(row["telemetry"]["crop_target_attainment"]) for row in rows]
            ),
            "watering_metrics_observed": len(rows) == 4
            and all(
                row["telemetry"].get("watering_metric_status") == "OBSERVED"
                for row in rows
            ),
        }
        metrics["capacity_eligible"] = (
            len(rows) == 4
            and metrics["watering_metrics_observed"]
            and metrics["completion_rate"] >= 0.80
            and metrics["median_post_ramp_watering_execution_rate"] >= 0.60
            and metrics["median_watering_continuity"] >= 0.75
            and metrics["median_crop_target_attainment"] >= 0.80
        )
        metrics_by_cell[cell_id] = metrics
        if metrics["capacity_eligible"]:
            eligible.append(cell_id)
    selected = max((expected[cell_id] for cell_id in eligible), default=None)
    return {
        "design_id": "E16_TRAINING",
        "eligible_cells": eligible,
        "metrics_by_cell": metrics_by_cell,
        "selected_C_star": selected,
        "gate_status": "STAGE_B_AUTHORIZED"
        if selected is not None
        else "STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR",
        "input_result_hashes": dict(sorted(input_result_hashes.items())),
        "analysis_code_hash": analysis_code_hash,
        "timestamp": timestamp,
    }


def validate_complete_matrix(
    rows: list[dict[str, Any]], matrix: list[dict[str, Any]]
) -> None:
    expected = {(row["cell_id"], row["seed"], row["treatment_seat"]) for row in matrix}
    actual = {(row["cell_id"], row["seed"], row["treatment_seat"]) for row in rows}
    if len(rows) != len(expected) or actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        raise RuntimeError(
            f"incomplete frozen matrix; missing={missing}, unexpected={unexpected}"
        )


def _paired_values(
    rows: list[dict[str, Any]],
    left: str,
    right: str,
    metric: str,
    transform: Callable[[float, float], float] | None = None,
) -> dict[str, Any]:
    indexed = {
        (row["cell_id"], row["seed"], row["treatment_seat"]): row for row in rows
    }
    pairs = []
    for seed in (1802163452, 1678077158):
        for seat in (0, 1):
            left_value = float(indexed[(left, seed, seat)]["telemetry"][metric])
            right_value = float(indexed[(right, seed, seat)]["telemetry"][metric])
            difference = (
                transform(left_value, right_value)
                if transform
                else left_value - right_value
            )
            pairs.append(
                {
                    "seed": seed,
                    "seat": seat,
                    "left": left_value,
                    "right": right_value,
                    "difference": difference,
                }
            )
    differences = [pair["difference"] for pair in pairs]
    signs = {0 if value == 0 else (1 if value > 0 else -1) for value in differences}
    return {
        "pairs": pairs,
        "sign_consistency": len(signs) <= 1,
        "median": _median(differences),
        "range": [min(differences), max(differences)],
        "direction_status": "UNRESOLVED" if len(signs) > 1 else "CONSISTENT",
    }


def build_contrasts(
    rows: list[dict[str, Any]], stage: str, metric: str
) -> dict[str, Any]:
    if stage == "stage_a":
        simple = {
            "A02-A01": ("A02", "A01"),
            "A04-A03": ("A04", "A03"),
            "A03-to-A06": ("A06", "A03"),
            "A06-to-A04": ("A04", "A06"),
            "A02-to-A07": ("A07", "A02"),
            "A07-to-A04": ("A04", "A07"),
        }
        output = {
            name: _paired_values(rows, left, right, metric)
            for name, (left, right) in simple.items()
        }
        first = output["A04-A03"]["pairs"]
        second = output["A02-A01"]["pairs"]
        interaction = [a["difference"] - b["difference"] for a, b in zip(first, second)]
        output["watering-by-capacity-interaction"] = {
            "pairs": [
                {"seed": pair["seed"], "seat": pair["seat"], "difference": value}
                for pair, value in zip(first, interaction)
            ],
            "sign_consistency": len(
                {0 if v == 0 else (1 if v > 0 else -1) for v in interaction}
            )
            <= 1,
            "median": _median(interaction),
            "range": [min(interaction), max(interaction)],
        }
        indexed = {
            (row["cell_id"], row["seed"], row["treatment_seat"]): row for row in rows
        }
        corner = []
        for seed in (1802163452, 1678077158):
            for seat in (0, 1):
                center = float(indexed[("A05", seed, seat)]["telemetry"][metric])
                interpolation = statistics.mean(
                    float(indexed[(cell, seed, seat)]["telemetry"][metric])
                    for cell in ("A01", "A02", "A03", "A04")
                )
                corner.append(
                    {
                        "seed": seed,
                        "seat": seat,
                        "left": center,
                        "right": interpolation,
                        "difference": center - interpolation,
                    }
                )
        values = [pair["difference"] for pair in corner]
        output["A05-vs-corner-interpolation"] = {
            "pairs": corner,
            "sign_consistency": len(
                {0 if v == 0 else (1 if v > 0 else -1) for v in values}
            )
            <= 1,
            "median": _median(values),
            "range": [min(values), max(values)],
        }
        return output

    simple = {
        "B02-B01": ("B02", "B01"),
        "B04-B03": ("B04", "B03"),
        "B02-to-B04": ("B04", "B02"),
        "B04-to-B05": ("B05", "B04"),
    }
    output = {
        name: _paired_values(rows, left, right, metric)
        for name, (left, right) in simple.items()
    }
    first = output["B04-B03"]["pairs"]
    second = output["B02-B01"]["pairs"]
    interaction = [a["difference"] - b["difference"] for a, b in zip(first, second)]
    output["pasture-by-herd-interaction"] = {
        "pairs": [
            {"seed": pair["seed"], "seat": pair["seat"], "difference": value}
            for pair, value in zip(first, interaction)
        ],
        "sign_consistency": len(
            {0 if v == 0 else (1 if v > 0 else -1) for v in interaction}
        )
        <= 1,
        "median": _median(interaction),
        "range": [min(interaction), max(interaction)],
    }
    return output


def render_analysis_markdown(rows: list[dict[str, Any]], stage: str) -> str:
    metrics = (
        "watering_execution_rate",
        "watering_continuity",
        "crop_target_attainment",
        "action_failure_rate",
    )
    lines = [
        f"# E16 {stage.replace('_', ' ').title()} Analysis",
        "",
        "Evidence role: TRAINING",
        "",
        "Raw values and paired differences are indexed by frozen seed and treatment seat. With only two seeds, inconsistent direction remains UNRESOLVED.",
        "",
    ]
    for metric in metrics:
        lines.extend(
            [
                f"## {metric}",
                "",
                "```json",
                json.dumps(
                    build_contrasts(rows, stage, metric), indent=2, sort_keys=True
                ),
                "```",
                "",
            ]
        )
    return "\n".join(lines)
