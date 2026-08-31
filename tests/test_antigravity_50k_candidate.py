"""Focused technical tests for the Antigravity C2 50K Compact-Q0 routine candidate."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy

from agricola.strategy.antigravity import (
    AntigravityC2_50K_Agent,
    AntigravityC2_50K_Config,
    AntigravityC2_50K_Policy,
    ANTIGRAVITY_COHORT_OFFSET,
    ANTIGRAVITY_CROP_PLAN,
    ANTIGRAVITY_CROP_POSITIONS,
    ANTIGRAVITY_CROP_ZONES,
    ANTIGRAVITY_PASTURE_POSITIONS,
    create_agent,
)
from agricola.strategy.codex_lifecycle import CodexObservationAdapter


def _plant(
    crop: str,
    *,
    planted_day: int = 0,
    yield_units: int = 0,
    watered: bool = False,
    consecutive_unwatered: int = 0,
    fertilized_until_day: int = -1,
    max_lifespan_step: int = 10_000,
) -> dict:
    return {
        "kind": "PLANT",
        "crop": crop,
        "planted_day": planted_day,
        "yield_units": yield_units,
        "watered_today": watered,
        "consecutive_unwatered": consecutive_unwatered,
        "fertilized_until_day": fertilized_until_day,
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
    tiles: list[list[Any]] | None = None,
) -> dict:
    step = day * 24 + hour
    if tiles is None:
        base_tiles = [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    else:
        base_tiles = tiles
    unit_positions = positions or [(4, 4)] * (hands + 1)
    farm = {
        "money": money,
        "tiles": deepcopy(base_tiles),
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


# 1. Config and footprint frozen invariants
def test_compact_q0_config_is_frozen():
    config = AntigravityC2_50K_Config.load()
    assert config.quadrants_owned == 1
    assert config.workforce_total == 7
    assert config.crop_counts == {"MELON": 9, "STRAWBERRY": 8, "WHEAT": 1}
    assert config.pasture_allocation_target == 6
    assert config.livestock_targets == {"COW": 3, "SHEEP": 3}
    assert config.bootstrap_livestock == {"COW": 2, "SHEEP": 2}


def test_compact_q0_uses_twenty_four_productive_positions():
    assert len(ANTIGRAVITY_CROP_POSITIONS) == 18
    assert len(ANTIGRAVITY_PASTURE_POSITIONS) == 6
    assert not set(ANTIGRAVITY_CROP_POSITIONS) & set(ANTIGRAVITY_PASTURE_POSITIONS)
    assert all(0 <= x < 5 and 0 <= y < 5 for x, y in (*ANTIGRAVITY_CROP_POSITIONS, *ANTIGRAVITY_PASTURE_POSITIONS))
    assert (4, 4) not in set(ANTIGRAVITY_CROP_POSITIONS) | set(ANTIGRAVITY_PASTURE_POSITIONS)


def test_crop_plan_and_zones_match_architecture():
    assert [len(zone) for zone in ANTIGRAVITY_CROP_ZONES] == [6, 6, 6]
    assert Counter(ANTIGRAVITY_CROP_PLAN.values()) == Counter({"MELON": 9, "STRAWBERRY": 8, "WHEAT": 1})
    melon_offsets = Counter(ANTIGRAVITY_COHORT_OFFSET[p] for p, crop in ANTIGRAVITY_CROP_PLAN.items() if crop == "MELON")
    strawberry_offsets = Counter(ANTIGRAVITY_COHORT_OFFSET[p] for p, crop in ANTIGRAVITY_CROP_PLAN.items() if crop == "STRAWBERRY")
    assert melon_offsets == Counter({0: 3, 1: 3, 2: 3})
    assert strawberry_offsets == Counter({0: 4, 2: 4})


# 2. Binding of a feed owner for every active cluster
def test_feed_owner_binding_for_active_clusters():
    policy = AntigravityC2_50K_Policy()
    
    # 1 worker: W0 owns both COW and SHEEP
    obs1 = _observation(hands=0)
    snap1 = _snapshot(obs1)
    assert policy._feed_service_species(snap1, 0, "RELIEF_LOGISTICS") == ("COW", "SHEEP")

    # 2 workers: W0 owns COW, W1 (1st hand) owns SHEEP
    obs2 = _observation(hands=1)
    snap2 = _snapshot(obs2)
    assert policy._feed_service_species(snap2, 0, "RELIEF_LOGISTICS") == ("COW",)
    assert policy._feed_service_species(snap2, 1, "CROP_ZONE_0") == ("SHEEP",)

    # 6+ workers: W4 owns COW, W5 owns SHEEP, W0 owns ()
    obs3 = _observation(hands=5)
    snap3 = _snapshot(obs3)
    assert policy._feed_service_species(snap3, 4, "LIVESTOCK_COW") == ("COW",)
    assert policy._feed_service_species(snap3, 5, "LIVESTOCK_SHEEP") == ("SHEEP",)
    assert policy._feed_service_species(snap3, 0, "RELIEF_LOGISTICS") == ()



# 3. Routing FEED without WHEAT is impossible; requires composed pickup
def test_feed_routing_requires_wheat_or_staged_pickup():
    policy = AntigravityC2_50K_Policy()
    
    tiles = [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    tiles[4][3] = {"kind": "PASTURE", "animal": "COW", "fed_today": False, "cared_today": False, "yield_units": 0}

    # Worker 1 has 0 wheat, but shed has 4 wheat
    obs = _observation(
        hands=1,
        positions=[(4, 4), (4, 4)],
        shed={"WHEAT": 4},
        inventories=[{}, {"WHEAT": 0}],
        tiles=tiles,
    )
    snap = _snapshot(obs)
    inv_tasks = policy._inventory_task(snap, 1, "LIVESTOCK_COW")
    assert len(inv_tasks) == 1
    assert inv_tasks[0]["kind"] == "FEED_STAGING"
    assert inv_tasks[0]["action"] == ["PICKUP", "WHEAT", 1]
    assert inv_tasks[0]["target"] == (4, 4)


# 4. Batch pickup sized to due feed set
def test_batch_pickup_sized_to_due_feed_set():
    policy = AntigravityC2_50K_Policy()
    
    tiles = [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    tiles[4][3] = {"kind": "PASTURE", "animal": "COW", "fed_today": False, "cared_today": False, "yield_units": 0}
    tiles[3][4] = {"kind": "PASTURE", "animal": "COW", "fed_today": False, "cared_today": False, "yield_units": 0}
    tiles[3][3] = {"kind": "PASTURE", "animal": "COW", "fed_today": False, "cared_today": False, "yield_units": 0}

    # 3 unfed cows, shed has 10 wheat -> PICKUP WHEAT 3
    obs = _observation(
        hands=1,
        positions=[(4, 4), (4, 4)],
        shed={"WHEAT": 10},
        inventories=[{}, {}],
        tiles=tiles,
    )
    snap = _snapshot(obs)
    inv_tasks = policy._inventory_task(snap, 1, "LIVESTOCK_COW")
    assert len(inv_tasks) == 1
    assert inv_tasks[0]["kind"] == "FEED_STAGING"
    assert inv_tasks[0]["action"] == ["PICKUP", "WHEAT", 3]


# 5. Feed precedence over secondary unload and fertilizer
def test_feed_precedence_over_secondary_unload_and_fertilizer():
    policy = AntigravityC2_50K_Policy()
    
    tiles = [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    tiles[4][3] = {"kind": "PASTURE", "animal": "COW", "fed_today": False, "cared_today": False, "yield_units": 1, "fertilizer_available": True}

    # Worker carries milk and fertilizer, but cow is unfed and shed has wheat
    obs = _observation(
        hands=1,
        positions=[(4, 4), (4, 4)],
        shed={"WHEAT": 5},
        inventories=[{}, {"MILK": 1, "FERTILIZER": 1, "WHEAT": 0}],
        tiles=tiles,
    )
    snap = _snapshot(obs)
    inv_tasks = policy._inventory_task(snap, 1, "LIVESTOCK_COW")
    assert len(inv_tasks) == 1
    assert inv_tasks[0]["kind"] == "FEED_STAGING"
    assert inv_tasks[0]["action"] == ["PICKUP", "WHEAT", 1]


# 6. Crop zone ownership preservation
def test_crop_zone_ownership_preservation():
    policy = AntigravityC2_50K_Policy()
    assert policy._role_for(1) == "CROP_ZONE_0"
    assert policy._role_for(2) == "CROP_ZONE_1"
    assert policy._role_for(3) == "CROP_ZONE_2"
    assert policy._role_for(4) == "LIVESTOCK_COW"
    assert policy._role_for(5) == "LIVESTOCK_SHEEP"
    assert policy._role_for(6) == "FERTILIZER_LOGISTICS"



# 7. Cross-zone assist only when origin zone is free
def test_cross_zone_assist_only_when_origin_zone_free():
    policy = AntigravityC2_50K_Policy()
    
    tiles = [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    # Zone 0 has an unwatered plant at (0,0)
    tiles[0][0] = _plant("MELON", planted_day=0, watered=False)
    # Zone 1 has an urgent unwatered plant at (3,0)
    tiles[0][3] = _plant("MELON", planted_day=0, watered=False, consecutive_unwatered=1)

    obs = _observation(
        day=2,
        hands=6,
        positions=[(4, 4), (1, 1), (3, 1), (0, 3), (3, 4), (2, 4), (4, 4)],
        tiles=tiles,
    )
    snap = _snapshot(obs)
    actions = policy.decide_unit_actions(snap)
    # W1 (CROP_ZONE_0) is at (1,1). Target should be in Zone 0 (0,0), NOT Zone 1
    w1_action = actions[1]
    assert w1_action[0] in {"WEST", "NORTH", "PASS"}



# 8. Fertilizer application only on same-day-watered crops
def test_fertilizer_application_only_same_day_watered():
    policy = AntigravityC2_50K_Policy()
    
    tiles = [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    # (0,0) is unwatered
    tiles[0][0] = _plant("MELON", planted_day=0, watered=False)
    # (1,0) is watered today
    tiles[0][1] = _plant("MELON", planted_day=0, watered=True)

    obs = _observation(
        day=2,
        hands=6,
        positions=[(4, 4)] * 7,
        inventories=[{}, {}, {}, {}, {}, {}, {"FERTILIZER": 2}],
        tiles=tiles,
    )
    snap = _snapshot(obs)
    w6_tasks = policy._inventory_task(snap, 6, "FERTILIZER_LOGISTICS")
    assert len(w6_tasks) > 0
    # Must target watered tile (1,0), never unwatered tile (0,0)
    assert w6_tasks[0]["target"] == (1, 0)
    assert w6_tasks[0]["kind"] == "FERTILIZER_APPLICATION"


# 9. Protection of wheat feed reserve
def test_wheat_reserve_protection():
    policy = AntigravityC2_50K_Policy()
    
    tiles = [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    # 2 cows + 2 sheep = 4 animals -> 2-round reserve = 8 wheat
    tiles[4][3] = {"kind": "PASTURE", "animal": "COW"}
    tiles[3][4] = {"kind": "PASTURE", "animal": "COW"}
    tiles[2][4] = {"kind": "PASTURE", "animal": "SHEEP"}
    tiles[4][2] = {"kind": "PASTURE", "animal": "SHEEP"}

    # Shed has 10 wheat -> can sell at most 2 wheat (10 - 8 = 2)
    obs = _observation(day=5, shed={"WHEAT": 10}, tiles=tiles)
    snap = _snapshot(obs)
    orders = policy.decide_market_orders(snap)
    wheat_sales = [o for o in orders if o[0] == "SELL" and o[1] == "WHEAT"]
    if wheat_sales:
        assert wheat_sales[0][2] <= 2


# 10. Player index independence
def test_player_index_independence():
    agent = AntigravityC2_50K_Agent()
    obs0 = _observation(player=0)
    obs1 = _observation(player=1)
    action0 = agent(obs0)
    action1 = agent(obs1)
    assert action0["market"] == action1["market"]
    assert action0["farmer"] == action1["farmer"]
    assert agent.error_count == 0


# 11. Opening orders bootstrap 2+2
def test_opening_orders_bootstrap_and_footprint():
    agent = AntigravityC2_50K_Agent()
    obs = _observation(day=0, hour=0)
    action = agent(obs)
    orders = action["market"]
    order_types = [(o[0], o[1] if len(o) > 1 else None) for o in orders]
    assert ("BUY_ANIMAL", "COW") in order_types
    assert ("BUY_ANIMAL", "SHEEP") in order_types
    assert ("BUY_PRODUCT", "WHEAT") in order_types
    assert ("BUY_SEED", "MELON") in order_types
