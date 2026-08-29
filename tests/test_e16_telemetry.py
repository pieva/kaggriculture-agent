"""Ledger lifecycle and derived-metric tests."""

from __future__ import annotations

import pytest

from agricola.e16.config import load_frozen_config, resolve_cell
from agricola.e16.runner import run_instrumentation_probe
from agricola.e16.telemetry import (
    LEDGER_REQUIRED_FIELDS,
    derive_episode_telemetry,
    detect_t0,
    validate_ledger_schema,
)


@pytest.fixture(scope="module")
def probe_events():
    return run_instrumentation_probe(load_frozen_config())


def test_e16_event_ledger_schema(probe_events):
    assert not validate_ledger_schema(probe_events)
    assert all(LEDGER_REQUIRED_FIELDS <= set(event) for event in probe_events)


@pytest.mark.parametrize("treatment_seat", [0, 1])
def test_e16_unit_events_are_attributed_for_both_seats(treatment_seat):
    events = run_instrumentation_probe(
        load_frozen_config(), treatment_seat=treatment_seat
    )
    unit_events = [
        event for event in events if event["actor_or_order_type"] != "market_order"
    ]
    assert unit_events
    assert {event["player"] for event in unit_events} == {0, 1}
    assert all(event["player"] != -1 for event in unit_events)
    assert all(event["seat"] == event["player"] for event in unit_events)
    assert all(event["attribution_status"] == "attributed" for event in unit_events)
    assert all(
        event["actor_role"]
        == ("treatment" if event["player"] == treatment_seat else "opponent")
        for event in unit_events
    )
    assert all(
        event["unit_index"] == 0 and event["actor_or_order_type"] == "farmer"
        for event in unit_events
    )


def test_e16_requested_and_executed_are_distinct(probe_events):
    partial = next(
        event
        for event in probe_events
        if event["execution_status"] == "partially_executed"
    )
    assert partial["requested_quantity"] > partial["executed_quantity"] > 0
    assert partial["requested_payload"] != partial["executed_payload"]


def test_e16_lifecycle_status_coverage(probe_events):
    finals = {event["execution_status"] for event in probe_events}
    lifecycle = {
        state for event in probe_events for state in event["lifecycle_statuses"]
    }
    assert {"executed", "partially_executed", "failed", "no_op"} <= finals
    assert {"requested", "accepted"} <= lifecycle


def test_e16_market_price_value_and_cash_reconcile(probe_events):
    for event in probe_events:
        if (
            event["actor_or_order_type"] != "market_order"
            or not event["executed_quantity"]
        ):
            continue
        assert event["realized_value"] == pytest.approx(
            event["realized_price"] * event["executed_quantity"]
        )
        delta = event["cash_after"] - event["cash_before"]
        expected = (
            event["realized_value"]
            if event["requested_payload"][0] == "SELL"
            else -event["realized_value"]
        )
        assert delta == pytest.approx(expected)


def _step(step, day, quadrants, plant_positions=()):
    tiles = [[None for _ in range(10)] for _ in range(10)]
    for x, y in plant_positions:
        tiles[y][x] = {
            "kind": "PLANT",
            "crop": "WHEAT",
            "watered_today": True,
            "consecutive_unwatered": 0,
            "yield_units": 1,
        }
    farm = {
        "unlocked_quadrants": quadrants,
        "tiles": tiles,
        "farmer": [4, 4],
        "hands": [],
        "money": 1000,
    }
    obs = {
        "step": step,
        "day": day,
        "hour": step % 24,
        "player": 0,
        "farms": [farm, farm],
        "private": {"shed": {}, "inventories": [{}]},
        "market": {"prices": {}},
    }
    return [{"observation": obs}, {"observation": {**obs, "player": 1}}]


def _water_event(day, position):
    return {
        "player": 0,
        "day": day,
        "target_tile_or_commodity": list(position),
        "actor_or_order_type": "farmer",
        "requested_payload": ["WATER"],
        "engine_applied_payload": ["WATER"],
        "execution_status": "executed",
        "attribution_status": "attributed",
    }


def test_e16_t0_detection_from_verified_state_transition():
    steps = [_step(0, 0, ["NW"]), _step(1, 0, ["NW", "NE"])]
    assert detect_t0(steps, 0) == 1


def test_e16_derived_metric_formulas():
    steps = [
        _step(0, 0, ["NW"]),
        _step(1, 0, ["NW", "NE"]),
        _step(70, 3, ["NW", "NE"], plant_positions=[(0, 0)]),
    ]
    ledger = [_water_event(3, (0, 0))]
    telemetry = derive_episode_telemetry(
        steps, ledger, 0, resolve_cell(load_frozen_config(), "stage_a", "A02"), 120
    )
    assert telemetry["watering_execution_rate"] == 1.0
    assert telemetry["watering_continuity"] == 1.0
    assert telemetry["watering_metric_status"] == "OBSERVED"
    assert telemetry["crop_target_attainment"] == pytest.approx(0.1)
    assert "non-cash" in telemetry["unsold_inventory_value_method"]


def test_e16_execution_rate_is_global_effects_over_needs():
    day3 = [(0, 0)]
    day4 = [(x, 0) for x in range(9)]
    steps = [
        _step(0, 0, ["NW"]),
        _step(1, 0, ["NW", "NE"]),
        _step(72, 3, ["NW", "NE"], plant_positions=day3),
        _step(96, 4, ["NW", "NE"], plant_positions=day4),
    ]
    telemetry = derive_episode_telemetry(
        steps,
        [_water_event(3, (0, 0))],
        0,
        resolve_cell(load_frozen_config(), "stage_a", "A02"),
        240,
    )
    assert telemetry["watering_need_denominator"] == 10
    assert telemetry["successful_watering_effects"] == 1
    assert telemetry["watering_execution_rate"] == pytest.approx(0.10)
    assert telemetry["watering_continuity"] == pytest.approx(0.50)


def test_e16_continuity_has_known_temporal_result_and_deduplicates_effects():
    positions = [(x, 0) for x in range(10)]
    steps = [
        _step(0, 0, ["NW"]),
        _step(1, 0, ["NW", "NE"]),
        _step(72, 3, ["NW", "NE"], plant_positions=positions),
        _step(96, 4, ["NW", "NE"], plant_positions=positions),
        _step(120, 5, ["NW", "NE"], plant_positions=positions),
    ]
    ledger = [
        *[_water_event(3, position) for position in positions[:6]],
        *[_water_event(4, position) for position in positions[:4]],
        *[_water_event(5, position) for position in positions[:5]],
        _water_event(5, positions[0]),
    ]
    telemetry = derive_episode_telemetry(
        steps,
        ledger,
        0,
        resolve_cell(load_frozen_config(), "stage_a", "A02"),
        240,
    )
    assert telemetry["successful_watering_effects"] == 15
    assert telemetry["watering_execution_rate"] == pytest.approx(0.50)
    assert telemetry["watering_continuity"] == pytest.approx(2 / 3)
    assert 0.0 <= telemetry["watering_execution_rate"] <= 1.0
    assert 0.0 <= telemetry["watering_continuity"] <= 1.0
