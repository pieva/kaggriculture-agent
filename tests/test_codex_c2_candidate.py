"""Focused lifecycle and arbitration tests for the Codex C2 candidate."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex_c2 import (
    GROWING,
    HARVEST_READY,
    RETIREMENT_DUE,
    CodexC2Agent,
    _stable_crop_plan,
    classify_tile_lifecycle,
    create_agent,
    load_candidate_config,
)


def _config(*, target: int = 1) -> dict:
    config = load_candidate_config()
    config["crop_working_set_target"] = target
    config["pasture_allocation_target"] = 0
    config["livestock_headcount_target"] = 0
    config["workforce_headcount"] = 0
    return config


def _observation(
    *,
    tile=None,
    position=(0, 0),
    day: int = 0,
    hour: int = 0,
    seeds: dict[str, int] | None = None,
    second_tile=None,
):
    tiles = []
    for y in range(10):
        row = []
        for x in range(10):
            row.append(None if y < 5 else "LOCKED")
        tiles.append(row)
    tiles[0][0] = tile
    if second_tile is not None:
        tiles[0][1] = second_tile
    farm = {
        "money": 3000,
        "farmer": list(position),
        "hands": [],
        "hires_today": 0,
        "unlocked_quadrants": ["NW", "NE"],
        "tiles": tiles,
    }
    return {
        "step": day * 24 + hour,
        "day": day,
        "hour": hour,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {
            "shed": {},
            "seeds": seeds or {},
            "inventories": [{}],
        },
        "market": {
            "prices": {"WHEAT": 10},
            "inventory": {"WHEAT": 100},
        },
    }


def _plant(
    crop: str,
    *,
    planted_day: int,
    yield_units: int,
    watered: bool = True,
    consecutive_unwatered: int = 0,
    max_lifespan_step: int = -1,
):
    return {
        "kind": "PLANT",
        "crop": crop,
        "planted_day": planted_day,
        "yield_units": yield_units,
        "watered_today": watered,
        "consecutive_unwatered": consecutive_unwatered,
        "max_lifespan_step": max_lifespan_step,
        "fertilized_until_day": -1,
    }


def _farmer_action(agent: CodexC2Agent, observation: dict) -> list[str]:
    return agent(observation, {"episodeSteps": 720, "turnsPerDay": 24})["farmer"]


def test_codex_c2_default_config_is_candidate_region_not_expansion():
    config = load_candidate_config()
    assert config["candidate_id"] == "CODEX_C2"
    assert config["crop_working_set_target"] == 17
    assert config["quadrants_owned"] == 2


def test_codex_c2_stable_plan_preserves_7_7_3_mix_at_target_17():
    config = load_candidate_config()
    crops = list(_stable_crop_plan(17, config["crop_pattern"]).values())
    assert {crop: crops.count(crop) for crop in set(crops)} == {
        "WHEAT": 7,
        "STRAWBERRY": 7,
        "MELON": 3,
    }


def test_codex_c2_rejects_premature_harvest():
    tile = _plant("WHEAT", planted_day=0, yield_units=1, watered=True)
    action = _farmer_action(CodexC2Agent(_config()), _observation(tile=tile))
    assert action == ["PASS"]


def test_codex_c2_accepts_mature_harvest():
    tile = _plant("WHEAT", planted_day=0, yield_units=2, watered=True)
    action = _farmer_action(
        CodexC2Agent(_config()), _observation(tile=tile, day=2)
    )
    assert action == ["HARVEST"]


def test_codex_c2_ongoing_intermediate_harvest_returns_to_growing():
    tile = _plant("STRAWBERRY", planted_day=0, yield_units=0, watered=True)
    assert (
        classify_tile_lifecycle(tile, in_working_set=True, day=12) == GROWING
    )


def test_codex_c2_final_ongoing_yield_precedes_retirement():
    tile = _plant(
        "STRAWBERRY",
        planted_day=0,
        yield_units=1,
        max_lifespan_step=408,
    )
    assert (
        classify_tile_lifecycle(tile, in_working_set=True, day=16)
        == HARVEST_READY
    )


def test_codex_c2_final_ongoing_harvest_becomes_preventive_dig():
    tile = _plant(
        "STRAWBERRY",
        planted_day=0,
        yield_units=0,
        watered=False,
        consecutive_unwatered=1,
        max_lifespan_step=408,
    )
    assert (
        classify_tile_lifecycle(tile, in_working_set=True, day=16)
        == RETIREMENT_DUE
    )
    action = _farmer_action(
        CodexC2Agent(_config()), _observation(tile=tile, day=16)
    )
    assert action == ["DIG"]


def test_codex_c2_max_lifespan_alone_does_not_retire_nonongoing_crop():
    tile = _plant(
        "WHEAT", planted_day=0, yield_units=0, max_lifespan_step=48
    )
    assert classify_tile_lifecycle(tile, in_working_set=True, day=2) == GROWING


def test_codex_c2_recovers_lost_weed_with_dig():
    action = _farmer_action(
        CodexC2Agent(_config()), _observation(tile={"kind": "WEED"})
    )
    assert action == ["DIG"]


def test_codex_c2_replants_empty_assigned_tile_when_water_phase_remains():
    observation = _observation(hour=22, seeds={"WHEAT": 1})
    action = _farmer_action(CodexC2Agent(_config()), observation)
    assert action == ["PLANT", "WHEAT"]


def test_codex_c2_blocks_unserviceable_last_phase_plant():
    observation = _observation(hour=23, seeds={"WHEAT": 1})
    action = _farmer_action(CodexC2Agent(_config()), observation)
    assert action == ["PASS"]


def test_codex_c2_critical_water_precedes_weed_recovery():
    critical = _plant(
        "WHEAT",
        planted_day=0,
        yield_units=1,
        watered=False,
        consecutive_unwatered=1,
    )
    observation = _observation(
        tile=critical,
        second_tile={"kind": "WEED"},
        position=(1, 0),
    )
    action = _farmer_action(CodexC2Agent(_config(target=2)), observation)
    assert action == ["WEST"]


def test_codex_c2_lifespan_harvest_precedes_same_tile_water():
    tile = _plant(
        "WHEAT",
        planted_day=0,
        yield_units=2,
        watered=False,
        consecutive_unwatered=1,
        max_lifespan_step=48,
    )
    action = _farmer_action(
        CodexC2Agent(_config()), _observation(tile=tile, day=2)
    )
    assert action == ["HARVEST"]


def test_codex_c2_invalid_crop_diagnostics_fail_closed_for_harvest():
    tile = _plant("UNKNOWN", planted_day=0, yield_units=3, watered=True)
    action = _farmer_action(
        CodexC2Agent(_config()), _observation(tile=tile, day=10)
    )
    assert action == ["PASS"]


def test_codex_c2_factory_is_invocable_and_fails_closed():
    agent = create_agent()
    assert agent.candidate_id == "CODEX_C2"
    assert agent({}, None) == {"farmer": ["PASS"], "hands": [], "market": []}
