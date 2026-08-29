"""Capacity-gate and paired-analysis tests."""

from __future__ import annotations

import inspect

from agricola.e16.analysis import compute_stage_b_gate


def rows_for(metrics_by_cell):
    rows = []
    for cell_id, metrics in metrics_by_cell.items():
        for seed in (1802163452, 1678077158):
            for seat in (0, 1):
                rows.append(
                    {
                        "cell_id": cell_id,
                        "seed": seed,
                        "treatment_seat": seat,
                        "completed": metrics[0],
                        "telemetry": {
                            "watering_execution_rate": metrics[1],
                            "watering_continuity": metrics[2],
                            "crop_target_attainment": metrics[3],
                            "watering_metric_status": "OBSERVED",
                        },
                    }
                )
    return rows


def test_e16_gate_excludes_performance_outcome_from_implementation():
    assert "final_money" not in inspect.getsource(compute_stage_b_gate).lower()


def test_e16_gate_selects_largest_eligible_capacity():
    rows = rows_for(
        {
            "A02": (True, 0.7, 0.8, 0.9),
            "A07": (True, 0.7, 0.8, 0.9),
            "A04": (True, 0.5, 0.8, 0.9),
        }
    )
    gate = compute_stage_b_gate(rows, {"x": "abc"}, "code", "2026-01-01T00:00:00Z")
    assert gate["eligible_cells"] == ["A02", "A07"]
    assert gate["selected_C_star"] == 17
    assert gate["gate_status"] == "STAGE_B_AUTHORIZED"


def test_e16_gate_blocks_without_capacity_anchor():
    rows = rows_for(
        {
            "A02": (True, 0.5, 0.8, 0.9),
            "A07": (True, 0.7, 0.7, 0.9),
            "A04": (True, 0.7, 0.8, 0.7),
        }
    )
    gate = compute_stage_b_gate(rows, {}, "code", "2026-01-01T00:00:00Z")
    assert gate["selected_C_star"] is None
    assert gate["gate_status"] == "STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR"


def test_e16_gate_blocks_unobserved_watering_metric():
    rows = rows_for(
        {
            "A02": (True, 0.7, 0.8, 0.9),
            "A07": (True, 0.7, 0.8, 0.9),
            "A04": (True, 0.7, 0.8, 0.9),
        }
    )
    rows[0]["telemetry"]["watering_metric_status"] = "NO_STEADY_PRODUCTIVE_DAYS"
    gate = compute_stage_b_gate(rows, {}, "code", "2026-01-01T00:00:00Z")
    assert "A02" not in gate["eligible_cells"]


def test_e16_gate_is_deterministic_for_identical_inputs():
    rows = rows_for(
        {
            "A02": (True, 0.7, 0.8, 0.9),
            "A07": (True, 0.7, 0.8, 0.9),
            "A04": (True, 0.7, 0.8, 0.9),
        }
    )
    args = (rows, {"b": "2", "a": "1"}, "code", "2026-01-01T00:00:00Z")
    assert compute_stage_b_gate(*args) == compute_stage_b_gate(*args)
