"""Focused technical tests for the Codex compact-Q0 routine candidate."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy

from agricola.strategy.codex_c2 import (
    CODEX_COHORT_OFFSET,
    CODEX_CROP_PLAN,
    CODEX_CROP_POSITIONS,
    CODEX_CROP_ZONES,
    CODEX_PASTURE_POSITIONS,
    HARVEST_READY,
    RETIREMENT_DUE,
    YIELD_ACCUMULATING,
    CodexC2Agent,
    classify_tile_lifecycle,
    create_agent,
    load_candidate_config,
)
from agricola.strategy.codex_lifecycle import CodexObservationAdapter


def _plant(
    crop: str,
    *,
    planted_day: int = 0,
    yield_units: int = 0,
    watered: bool = False,
    consecutive_unwatered: int = 0,
    max_lifespan_step: int = 10_000,
) -> dict:
    return {
        "kind": "PLANT",
        "crop": crop,
        "planted_day": planted_day,
        "yield_units": yield_units,
        "watered_today": watered,
        "consecutive_unwatered": consecutive_unwatered,
        "fertilized_until_day": -1,
        "max_lifespan_step": max_lifespan_step,
    }


def _observation(
    *,
    day: int = 0,
    hour: int = 0,
    money: float = 3000.0,
    player: int = 0,
    hands: int = 0,
    positions: list[tuple[int, int]] | None = None,
    seeds: dict[str, int] | None = None,
    shed: dict[str, int] | None = None,
    inventories: list[dict[str, int]] | None = None,
) -> dict:
    step = day * 24 + hour
    tiles = [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    unit_positions = positions or [(4, 4)] * (hands + 1)
    farm = {
        "money": money,
        "tiles": deepcopy(tiles),
        "farmer": list(unit_positions[0]),
        "hands": [list(position) for position in unit_positions[1:]],
        "unlocked_quadrants": ["NW"],
        "hires_today": 0,
    }
    other_farm = deepcopy(farm)
    base_shed = {
        "WHEAT": 0,
        "CARROT": 0,
        "TOMATO": 0,
        "STRAWBERRY": 0,
        "MELON": 0,
        "EGG": 0,
        "MILK": 0,
        "WOOL": 0,
        "FERTILIZER": 0,
        "GOOSE": 0,
        "COW": 0,
        "SHEEP": 0,
    }
    base_shed.update(shed or {})
    private = {
        "shed": base_shed,
        "seeds": {"WHEAT": 0, "CARROT": 0, "TOMATO": 0, "STRAWBERRY": 0, "MELON": 0},
        "inventories": inventories or [{} for _ in range(hands + 1)],
    }
    private["seeds"].update(seeds or {})
    return {
        "step": step,
        "day": day,
        "hour": hour,
        "player": player,
        "farms": [farm, other_farm],
        "private": private,
        "market": {
            "inventory": {item: 10_000 for item in base_shed},
            "prices": {
                "WHEAT": 25,
                "STRAWBERRY": 120,
                "MELON": 250,
                "MILK": 160,
                "WOOL": 200,
                "FERTILIZER": 100,
            },
        },
        "town": {"unlocked_shops": []},
    }


def _snapshot(observation: dict, *, steps: int = 720):
    return CodexObservationAdapter.parse(
        observation,
        {"episodeSteps": steps, "turnsPerDay": 24},
        fallback_turns_per_day=24,
        fallback_episode_steps=steps,
    )


def test_compact_q0_config_is_frozen():
    config = load_candidate_config()
    assert config["quadrants_owned"] == 1
    assert config["workforce_total"] == 7
    assert config["crop_counts"] == {"MELON": 9, "STRAWBERRY": 8, "WHEAT": 1}
    assert config["pasture_allocation_target"] == 6
    assert config["livestock_targets"] == {"COW": 3, "SHEEP": 3}
    assert config["bootstrap_livestock"] == {"COW": 2, "SHEEP": 2}


def test_compact_q0_uses_exactly_twenty_four_productive_positions():
    assert len(CODEX_CROP_POSITIONS) == 18
    assert len(CODEX_PASTURE_POSITIONS) == 6
    assert not set(CODEX_CROP_POSITIONS) & set(CODEX_PASTURE_POSITIONS)
    assert all(0 <= x < 5 and 0 <= y < 5 for x, y in (*CODEX_CROP_POSITIONS, *CODEX_PASTURE_POSITIONS))
    assert (4, 4) not in set(CODEX_CROP_POSITIONS) | set(CODEX_PASTURE_POSITIONS)


def test_crop_plan_and_zones_match_preregistered_architecture():
    assert [len(zone) for zone in CODEX_CROP_ZONES] == [6, 6, 6]
    assert Counter(CODEX_CROP_PLAN.values()) == Counter({"MELON": 9, "STRAWBERRY": 8, "WHEAT": 1})
    melon_offsets = Counter(CODEX_COHORT_OFFSET[p] for p, crop in CODEX_CROP_PLAN.items() if crop == "MELON")
    strawberry_offsets = Counter(CODEX_COHORT_OFFSET[p] for p, crop in CODEX_CROP_PLAN.items() if crop == "STRAWBERRY")
    assert melon_offsets == Counter({0: 3, 1: 3, 2: 3})
    assert strawberry_offsets == Counter({0: 4, 2: 4})


def test_opening_orders_are_q0_only_and_bootstrap_two_plus_two():
    agent = CodexC2Agent(load_candidate_config())
    action = agent(_observation(), {"episodeSteps": 720, "turnsPerDay": 24})
    orders = action["market"]
    assert len([order for order in orders if order[0] == "HIRE"]) == 6
    assert ["BUY_ANIMAL", "COW", 2] in orders
    assert ["BUY_ANIMAL", "SHEEP", 2] in orders
    assert ["BUY_PRODUCT", "WHEAT", 10] in orders
    assert ["BUY_SEED", "MELON", 3] in orders
    assert not any(order[0] == "BUY_LAND" for order in orders)
    assert len(orders) <= 10


def test_role_mapping_is_persistent_and_complete():
    agent = CodexC2Agent(load_candidate_config())
    agent._update_roles(7)
    assert agent._roles == {
        0: "FLOAT_RESERVE",
        1: "CROP_ZONE_0",
        2: "CROP_ZONE_1",
        3: "CROP_ZONE_2",
        4: "LIVESTOCK_COW",
        5: "LIVESTOCK_SHEEP",
        6: "FERTILIZER_LOGISTICS",
    }
    agent._update_roles(7)
    assert agent.role_changes == 0


def test_critical_water_has_explicit_hard_interrupt_reason():
    observation = _observation(day=3, hour=20, hands=6)
    x, y = CODEX_CROP_POSITIONS[0]
    observation["farms"][0]["tiles"][y][x] = _plant(
        "MELON", planted_day=0, consecutive_unwatered=1
    )
    tasks = CodexC2Agent(load_candidate_config())._crop_tasks(_snapshot(observation))
    task = next(task for task in tasks if tuple(task["target"]) == (x, y))
    assert task["action"] == ["WATER"]
    assert task["loss_rank"] == 0
    assert task["hard_reason"] == "CROP_WATER_LOSS"


def test_feed_becomes_hard_before_escape_boundary():
    observation = _observation(day=4, hour=18, hands=6)
    x, y = CODEX_PASTURE_POSITIONS[0]
    observation["farms"][0]["tiles"][y][x] = {
        "kind": "PASTURE",
        "animal": "COW",
        "placed_day": 0,
        "yield_units": 0,
        "consecutive_unfed": 1,
        "fed_today": False,
        "cared_today": False,
        "fertilizer_available": False,
    }
    tasks = CodexC2Agent(load_candidate_config())._animal_tasks(_snapshot(observation), "COW")
    feed = next(task for task in tasks if task["kind"] == "FEED")
    care = next(task for task in tasks if task["kind"] == "CARE")
    assert feed["hard_reason"] == "ANIMAL_ESCAPE_PREVENTION"
    assert care["hard_reason"] is None


def test_unstaffed_bootstrap_herd_has_executable_fallback_feed_binding():
    observation = _observation(day=4, hour=0, hands=0, shed={"WHEAT": 4})
    bootstrap_positions = (
        *CODEX_PASTURE_POSITIONS[:2],
        *CODEX_PASTURE_POSITIONS[3:5],
    )
    for position, species in zip(
        bootstrap_positions,
        ("COW", "COW", "SHEEP", "SHEEP"),
    ):
        x, y = position
        observation["farms"][0]["tiles"][y][x] = {
            "kind": "PASTURE",
            "animal": species,
            "placed_day": 0,
            "yield_units": 0,
            "consecutive_unfed": 1,
            "fed_today": False,
            "cared_today": False,
            "fertilizer_available": False,
        }
    agent = CodexC2Agent(load_candidate_config())
    snapshot = _snapshot(observation)

    assert agent._feed_service_species(snapshot, 0, "FLOAT_RESERVE") == (
        "COW",
        "SHEEP",
    )
    assert agent._unit_actions(snapshot)[0] == ["PICKUP", "WHEAT", 4]


def test_non_owner_never_routes_to_remote_feed_without_wheat():
    observation = _observation(day=4, hour=20, hands=6, shed={"WHEAT": 0})
    x, y = CODEX_PASTURE_POSITIONS[0]
    observation["farms"][0]["tiles"][y][x] = {
        "kind": "PASTURE",
        "animal": "COW",
        "placed_day": 0,
        "yield_units": 0,
        "consecutive_unfed": 1,
        "fed_today": False,
        "cared_today": False,
        "fertilizer_available": False,
    }
    agent = CodexC2Agent(load_candidate_config())

    assert agent._unit_actions(_snapshot(observation))[1] == ["PASS"]


def test_fertilizer_application_requires_same_day_water():
    observation = _observation(
        day=5,
        hands=6,
        inventories=[{}, {}, {}, {}, {}, {}, {"FERTILIZER": 1}],
    )
    position = next(p for p, crop in CODEX_CROP_PLAN.items() if crop == "MELON")
    x, y = position
    observation["farms"][0]["tiles"][y][x] = _plant("MELON", watered=False)
    agent = CodexC2Agent(load_candidate_config())
    assert not any(
        task["kind"] == "FERTILIZER_APPLICATION"
        for task in agent._inventory_task(_snapshot(observation), 6, "FERTILIZER_LOGISTICS")
    )
    observation["farms"][0]["tiles"][y][x]["watered_today"] = True
    assert any(
        task["kind"] == "FERTILIZER_APPLICATION"
        for task in agent._inventory_task(_snapshot(observation), 6, "FERTILIZER_LOGISTICS")
    )


def test_capacity_admission_rejects_growth_without_three_day_history():
    observation = _observation(day=7, hands=6, money=5000, shed={"WHEAT": 12})
    admitted, reason, capacity = CodexC2Agent(load_candidate_config())._capacity_admission(
        _snapshot(observation), "COW"
    )
    assert admitted is False
    assert reason == "OBSERVED_CAPACITY_INSUFFICIENT_HISTORY"
    assert capacity["observed_capacity"] is None


def test_capacity_admission_can_pass_observed_action_gate():
    observation = _observation(day=7, hands=6, money=5000, shed={"WHEAT": 12})
    agent = CodexC2Agent(load_candidate_config())
    for day in (4, 5, 6):
        agent.daily_completed[day] = Counter({"WATER": 30, "MOVE": 30, "PLACE": 4})
    admitted, reason, capacity = agent._capacity_admission(_snapshot(observation), "COW")
    assert admitted is True
    assert reason == "ADMITTED"
    assert capacity["minimum_slack"] >= 0


def test_atomic_commitment_persists_while_target_remains_valid():
    observation = _observation(day=2, hands=6, seeds={"MELON": 9, "STRAWBERRY": 8, "WHEAT": 1})
    agent = CodexC2Agent(load_candidate_config())
    snapshot = _snapshot(observation)
    agent._update_roles(7)
    first = agent._unit_actions(snapshot)
    commitment = deepcopy(agent._commitments[1])
    second = agent._unit_actions(snapshot)
    assert first[1] == second[1]
    assert agent._commitments[1]["target"] == commitment["target"]
    assert agent.retarget_count == 0


def test_wheat_market_sale_preserves_two_feed_rounds():
    observation = _observation(day=4, hands=6, shed={"WHEAT": 20})
    for position, species in zip(CODEX_PASTURE_POSITIONS[:4], ("COW", "COW", "SHEEP", "SHEEP")):
        x, y = position
        observation["farms"][0]["tiles"][y][x] = {
            "kind": "PASTURE",
            "animal": species,
            "yield_units": 0,
            "consecutive_unfed": 0,
            "fed_today": True,
            "cared_today": True,
            "fertilizer_available": False,
        }
    orders = CodexC2Agent(load_candidate_config())._market_orders(_snapshot(observation))
    assert ["SELL", "WHEAT", 12] in orders


def test_lifecycle_classification_preserves_engine_guards():
    assert classify_tile_lifecycle(
        _plant("WHEAT", planted_day=0, yield_units=1), in_working_set=True, day=2
    ) == YIELD_ACCUMULATING
    assert classify_tile_lifecycle(
        _plant("WHEAT", planted_day=0, yield_units=3), in_working_set=True, day=4
    ) == HARVEST_READY
    assert classify_tile_lifecycle(
        _plant("STRAWBERRY", planted_day=0, yield_units=0, max_lifespan_step=380),
        in_working_set=True,
        day=16,
    ) == RETIREMENT_DUE


def test_duplicate_snapshot_is_idempotent():
    observation = _observation()
    agent = CodexC2Agent(load_candidate_config())
    first = agent(observation, {"episodeSteps": 720, "turnsPerDay": 24})
    requests = dict(agent.action_requests_by_opcode)
    second = agent(deepcopy(observation), {"episodeSteps": 720, "turnsPerDay": 24})
    assert first == second
    assert dict(agent.action_requests_by_opcode) == requests


def test_factory_fails_closed_on_invalid_observation():
    agent = create_agent()
    assert agent({"player": "invalid"}, None) == {
        "farmer": ["PASS"],
        "hands": [],
        "market": [],
    }
    assert agent.codex_c2_instance.error_count == 1
    assert agent.codex_c2_instance.fallback_count == 1


def test_player_one_reads_player_one_farm():
    observation = _observation(player=1, hands=0, day=10)
    position = CODEX_CROP_POSITIONS[0]
    x, y = position
    observation["farms"][1]["tiles"][y][x] = _plant(
        "MELON", planted_day=0, yield_units=6, watered=True
    )
    snapshot = _snapshot(observation)
    tasks = CodexC2Agent(load_candidate_config())._crop_tasks(snapshot)
    assert any(task["action"] == ["HARVEST"] and tuple(task["target"]) == position for task in tasks)


def test_candidate_never_emits_drop_or_buy_land():
    observation = _observation(
        day=3,
        hands=6,
        inventories=[{"MELON": 2}, {}, {}, {}, {}, {}, {}],
    )
    action = CodexC2Agent(load_candidate_config())(
        observation, {"episodeSteps": 720, "turnsPerDay": 24}
    )
    flattened = [action["farmer"], *action["hands"], *action["market"]]
    assert all(item[0] not in {"DROP", "BUY_LAND"} for item in flattened if item)


def test_telemetry_exposes_all_mandatory_leading_indicators():
    agent = CodexC2Agent(load_candidate_config())
    agent(_observation(), {"episodeSteps": 720, "turnsPerDay": 24})
    telemetry = agent.telemetry_snapshot()
    for field in (
        "ON_TIME_CROP_SERVICE_RATIO",
        "HARD_DEADLINE_MISSES",
        "HIGH_VALUE_CROP_UNITS_VS_COHORT_PLAN",
        "MOVE_PER_PRODUCTIVE_ACTION",
        "RETARGET_COUNT_PER_WORKER_DAY",
        "ROLE_CHANGES",
        "CROSS_ZONE_ASSISTS",
    ):
        assert field in telemetry
