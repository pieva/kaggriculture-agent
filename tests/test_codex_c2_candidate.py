"""Focused lifecycle and arbitration tests for the Codex C2 candidate."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex_c2 import (
    CODEX_CROP_POSITIONS,
    GROWING,
    HARVEST_READY,
    RETIREMENT_DUE,
    YIELD_ACCUMULATING,
    CodexC2Agent,
    _stable_crop_plan,
    classify_tile_lifecycle,
    create_agent,
    load_candidate_config,
)


def _config(*, target: int = 1) -> dict:
    config = load_candidate_config()
    config["crop_working_set_target"] = target
    config["bootstrap_crop_target"] = min(target, config["bootstrap_crop_target"])
    config["pasture_allocation_target"] = 0
    config["livestock_headcount_target"] = 0
    config["workforce_headcount"] = 0
    config["bootstrap_workforce_headcount"] = 0
    return config


def _observation(
    *,
    tile=None,
    position=None,
    day: int = 0,
    hour: int = 0,
    seeds: dict[str, int] | None = None,
    second_tile=None,
    player: int = 0,
    quadrants: int = 2,
    money: float = 3000,
):
    first_position = CODEX_CROP_POSITIONS[0]
    second_position = CODEX_CROP_POSITIONS[1]
    if position is None:
        position = first_position
    tiles = []
    for y in range(10):
        row = []
        for x in range(10):
            row.append(None if y < 5 else "LOCKED")
        tiles.append(row)
    tiles[first_position[1]][first_position[0]] = tile
    if second_tile is not None:
        tiles[second_position[1]][second_position[0]] = second_tile
    farm = {
        "money": money,
        "farmer": list(position),
        "hands": [],
        "hires_today": 0,
        "unlocked_quadrants": ["NW", "NE"][:quadrants],
        "tiles": tiles,
    }
    return {
        "step": day * 24 + hour,
        "day": day,
        "hour": hour,
        "player": player,
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
    assert config["crop_working_set_target"] == 25
    assert config["bootstrap_crop_target"] == 10
    assert config["max_wheat_plants_per_day"] == 2
    assert config["schema_version"] == "model_spec_c2.codex.v3"
    assert config["quadrants_owned"] == 2


def test_codex_c2_phase_plans_preserve_bootstrap_and_full_mix():
    config = load_candidate_config()
    bootstrap = list(
        _stable_crop_plan(10, config["bootstrap_crop_pattern"]).values()
    )
    assert {crop: bootstrap.count(crop) for crop in set(bootstrap)} == {
        "WHEAT": 6,
        "STRAWBERRY": 2,
        "MELON": 2,
    }
    full = list(_stable_crop_plan(25, config["crop_pattern"]).values())
    assert {crop: full.count(crop) for crop in set(full)} == {
        "WHEAT": 10,
        "STRAWBERRY": 5,
        "MELON": 10,
    }


def test_codex_c2_caps_same_day_wheat_plant_cohort_at_two():
    observation = _observation(seeds={"WHEAT": 10})
    positions = CODEX_CROP_POSITIONS[:6]
    observation["farms"][0]["farmer"] = list(positions[0])
    observation["farms"][0]["hands"] = [list(position) for position in positions[1:]]
    observation["private"]["inventories"] = [{} for _ in positions]

    result = CodexC2Agent(_config(target=6))(
        observation, {"episodeSteps": 720, "turnsPerDay": 24}
    )
    actions = [result["farmer"], *result["hands"]]
    assert actions.count(["PLANT", "WHEAT"]) == 2


def test_codex_c2_reopens_wheat_cohort_slots_on_next_day():
    observation = _observation(day=0, seeds={"WHEAT": 10})
    positions = CODEX_CROP_POSITIONS[:6]
    for position in positions[:2]:
        x, y = position
        observation["farms"][0]["tiles"][y][x] = _plant(
            "WHEAT", planted_day=0, yield_units=1
        )
    observation["farms"][0]["farmer"] = list(positions[5])
    observation["farms"][0]["hands"] = [list(position) for position in positions[:5]]
    observation["private"]["inventories"] = [{} for _ in positions]

    agent = CodexC2Agent(_config(target=6))
    same_day = agent(observation, {"episodeSteps": 720, "turnsPerDay": 24})
    same_day_actions = [same_day["farmer"], *same_day["hands"]]
    assert ["PLANT", "WHEAT"] not in same_day_actions

    next_day = deepcopy(observation)
    next_day["step"] = 24
    next_day["day"] = 1
    next_day_result = agent(next_day, {"episodeSteps": 720, "turnsPerDay": 24})
    next_day_actions = [next_day_result["farmer"], *next_day_result["hands"]]
    assert next_day_actions.count(["PLANT", "WHEAT"]) == 1


def test_codex_c2_rejects_premature_harvest():
    tile = _plant("WHEAT", planted_day=0, yield_units=1, watered=True)
    action = _farmer_action(CodexC2Agent(_config()), _observation(tile=tile))
    assert action == ["PASS"]


def test_codex_c2_accumulates_wheat_after_engine_maturity():
    tile = _plant("WHEAT", planted_day=0, yield_units=2, watered=True)
    assert (
        classify_tile_lifecycle(tile, in_working_set=True, day=2)
        == YIELD_ACCUMULATING
    )
    action = _farmer_action(
        CodexC2Agent(_config()), _observation(tile=tile, day=2)
    )
    assert action == ["PASS"]


def test_codex_c2_harvests_wheat_at_economic_day():
    tile = _plant("WHEAT", planted_day=0, yield_units=4, watered=True)
    assert (
        classify_tile_lifecycle(tile, in_working_set=True, day=4)
        == HARVEST_READY
    )
    action = _farmer_action(
        CodexC2Agent(_config()), _observation(tile=tile, day=4)
    )
    assert action == ["HARVEST"]


def test_codex_c2_final_yield_water_precedes_economic_harvest():
    tile = _plant(
        "WHEAT", planted_day=0, yield_units=2, watered=False,
        consecutive_unwatered=0,
    )
    action = _farmer_action(
        CodexC2Agent(_config()), _observation(tile=tile, day=4)
    )
    assert action == ["WATER"]


def test_codex_c2_harvests_minimum_economic_yield_before_decay():
    tile = _plant(
        "WHEAT", planted_day=0, yield_units=3, watered=False,
        consecutive_unwatered=0,
    )
    action = _farmer_action(
        CodexC2Agent(_config()), _observation(tile=tile, day=4)
    )
    assert action == ["HARVEST"]


def test_codex_c2_yield_window_water_precedes_other_economic_harvest():
    accumulating = _plant(
        "WHEAT", planted_day=2, yield_units=1, watered=False,
        consecutive_unwatered=0,
    )
    ready = _plant("WHEAT", planted_day=0, yield_units=4, watered=True)
    observation = _observation(
        tile=accumulating,
        second_tile=ready,
        position=CODEX_CROP_POSITIONS[1],
        day=4,
    )
    action = _farmer_action(CodexC2Agent(_config(target=2)), observation)
    assert action == ["SOUTH"]


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


def test_codex_c2_terminal_horizon_blocks_new_plant_but_services_existing_crop():
    agent = CodexC2Agent(_config())
    empty = _observation(day=12, seeds={"WHEAT": 1})
    assert agent(empty, {"episodeSteps": 360, "turnsPerDay": 24})["farmer"] == [
        "PASS"
    ]

    mature = _observation(
        tile=_plant("WHEAT", planted_day=0, yield_units=2), day=12
    )
    assert agent(mature, {"episodeSteps": 360, "turnsPerDay": 24})[
        "farmer"
    ] == ["HARVEST"]


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
        position=CODEX_CROP_POSITIONS[1],
    )
    action = _farmer_action(CodexC2Agent(_config(target=2)), observation)
    assert action == ["SOUTH"]


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
    assert agent({"player": "invalid"}, None) == {
        "farmer": ["PASS"],
        "hands": [],
        "market": [],
    }
    assert agent.codex_c2_instance.error_count == 1
    assert agent.codex_c2_instance.fallback_count == 1


def test_codex_c2_reads_the_farm_bound_to_player_one():
    observation = _observation(
        tile=_plant("WHEAT", planted_day=0, yield_units=4),
        day=4,
        player=1,
    )
    first_x, first_y = CODEX_CROP_POSITIONS[0]
    observation["farms"][0]["tiles"][first_y][first_x] = None
    action = _farmer_action(CodexC2Agent(_config()), observation)
    assert action == ["HARVEST"]


def test_codex_c2_delays_land_until_bootstrap_surface_is_realized():
    agent = CodexC2Agent(load_candidate_config())
    initial = _observation(quadrants=1)
    first_action = agent(initial, {"episodeSteps": 720, "turnsPerDay": 24})
    assert "BUY_LAND" not in {order[0] for order in first_action["market"]}

    established = _observation(quadrants=1)
    for x, y in CODEX_CROP_POSITIONS[:8]:
        established["farms"][0]["tiles"][y][x] = _plant(
            "WHEAT", planted_day=0, yield_units=0
        )
    second_action = agent(
        established, {"episodeSteps": 720, "turnsPerDay": 24}
    )
    assert "BUY_LAND" in {order[0] for order in second_action["market"]}
