from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4A_CONFIG_PATH,
    DEFAULT_V4B_CONFIG_PATH,
    DEFAULT_V4C_CONFIG_PATH,
    DEFAULT_V4D_CONFIG_PATH,
    V4A_MODEL_SPEC_VERSION,
    V4B_MODEL_SPEC_VERSION,
    V4C_MODEL_SPEC_VERSION,
    V4D_MODEL_SPEC_VERSION,
    CodexE17BatchedClusterRoutingV4,
    create_codex_e17_batched_cluster_routing_v4,
    load_v4_config,
)
from agricola.strategy.codex.codex_e17_reactive_service_routing_core import (
    CoreTask,
)
from agricola.strategy.codex.codex_e17_reactive_service_routing_v3 import (
    create_codex_e17_reactive_service_routing_v3,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
REPLAY = REPO_ROOT / "data/replays/json/104498819.json"


def _observation(step: int) -> tuple[dict, dict]:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    return (
        deepcopy(replay["steps"][step][0]["observation"]),
        deepcopy(replay["configuration"]),
    )


def _clear_farm(observation: dict, *, hands: bool = False) -> tuple[dict, dict]:
    farm = observation["farms"][observation["player"]]
    for row in farm["tiles"]:
        for index, tile in enumerate(row):
            if tile != "LOCKED":
                row[index] = None
    if not hands:
        farm["hands"] = []
    private = observation["private"]
    private["inventories"] = [
        {} for _ in [farm["farmer"], *farm.get("hands", [])]
    ]
    return farm, private


def _mature_crop(crop: str = "TOMATO", units: int = 3) -> dict:
    return {
        "kind": "PLANT",
        "crop": crop,
        "planted_day": 0,
        "yield_units": units,
        "watered_today": False,
        "consecutive_unwatered": 0,
        "fertilized_until_day": -1,
    }


def test_v4_configs_separate_batching_and_cluster_ablation() -> None:
    v4a = load_v4_config(DEFAULT_V4A_CONFIG_PATH)
    v4b = load_v4_config(DEFAULT_V4B_CONFIG_PATH)
    v4c = load_v4_config(DEFAULT_V4C_CONFIG_PATH)
    v4d = load_v4_config(DEFAULT_V4D_CONFIG_PATH)
    assert v4a["model_spec_version"] == V4A_MODEL_SPEC_VERSION
    assert v4b["model_spec_version"] == V4B_MODEL_SPEC_VERSION
    assert v4c["model_spec_version"] == V4C_MODEL_SPEC_VERSION
    assert v4d["model_spec_version"] == V4D_MODEL_SPEC_VERSION
    assert v4a["cluster_affinity_enabled"] is False
    assert v4b["cluster_affinity_enabled"] is True
    assert v4c["capacity_aware_flush_enabled"] is True
    assert v4d["release_wheat_carriers_after_feed_complete"] is True
    assert v4a["activation_day"] == v4b["activation_day"] == 28
    assert v4c["activation_day"] == 28


def test_pre_activation_action_is_exact_v3_action() -> None:
    observation, configuration = _observation(671)
    provider = create_codex_e17_reactive_service_routing_v3()(
        deepcopy(observation), configuration
    )
    candidate = create_codex_e17_batched_cluster_routing_v4()
    assert candidate(deepcopy(observation), configuration) == provider


def test_d28_defers_explicit_drop_to_automatic_eod_deposit() -> None:
    observation, configuration = _observation(672)
    farm, private = _clear_farm(observation)
    farm["farmer"] = [4, 4]
    private["inventories"] = [{"MILK": 3}]
    candidate = create_codex_e17_batched_cluster_routing_v4()
    assert candidate(observation, configuration)["farmer"] == ["PASS"]
    instance = candidate.codex_e17_batched_cluster_routing_instance
    assert instance.deferred_drop_opportunities == 1


def test_d29_batches_another_harvest_before_drop_when_return_is_feasible() -> None:
    observation, configuration = _observation(697)
    farm, private = _clear_farm(observation)
    farm["farmer"] = [4, 4]
    farm["tiles"][3][4] = _mature_crop()
    private["inventories"] = [{"MILK": 2}]
    candidate = create_codex_e17_batched_cluster_routing_v4()
    assert candidate(observation, configuration)["farmer"] == ["NORTH"]


def test_d29_deadline_forces_drop_instead_of_unfinishable_harvest() -> None:
    observation, configuration = _observation(718)
    farm, private = _clear_farm(observation)
    farm["farmer"] = [4, 4]
    farm["tiles"][3][4] = _mature_crop()
    private["inventories"] = [{"MILK": 2}]
    candidate = create_codex_e17_batched_cluster_routing_v4()
    assert candidate(observation, configuration)["farmer"] == ["DROP"]


def test_v4c_capacity_pressure_routes_drop_and_presells_shed_room() -> None:
    observation, configuration = _observation(680)
    farm, private = _clear_farm(observation)
    farm["farmer"] = [0, 0]
    private["shed"] = {"TOMATO": 80}
    private["inventories"] = [{"MILK": 30}]
    candidate = create_codex_e17_batched_cluster_routing_v4(
        config_path=DEFAULT_V4C_CONFIG_PATH
    )
    action = candidate(observation, configuration)
    assert action["farmer"][0] in {"EAST", "SOUTH"}
    assert sum(
        int(order[2])
        for order in action["market"]
        if order[0] == "SELL" and order[1] == "TOMATO"
    ) >= 30
    instance = candidate.codex_e17_batched_cluster_routing_instance
    assert instance.capacity_flush_trigger_events == 1


def test_v4d_releases_wheat_carrier_only_after_feed_is_complete() -> None:
    observation, configuration = _observation(680)
    farm, private = _clear_farm(observation)
    farm["farmer"] = [0, 0]
    private["shed"] = {"TOMATO": 80}
    private["inventories"] = [{"WHEAT": 6, "MILK": 24}]
    candidate = create_codex_e17_batched_cluster_routing_v4(
        config_path=DEFAULT_V4D_CONFIG_PATH
    )
    action = candidate(observation, configuration)
    assert action["farmer"][0] in {"EAST", "SOUTH"}
    assert any(order[0] == "SELL" for order in action["market"])
    instance = candidate.codex_e17_batched_cluster_routing_instance
    assert instance.post_feed_wheat_carrier_releases > 0


def test_v4b_quadrant_affinity_breaks_equal_value_route_tie() -> None:
    candidate = CodexE17BatchedClusterRoutingV4(
        config_path=DEFAULT_V4B_CONFIG_PATH
    )
    candidate._routing_clock = SimpleNamespace(day=29, step=700)
    candidate._routing_board_size = 10
    candidate._affinity_day = 29
    candidate._worker_cluster = {0: "NW"}
    candidate._routing_prices = {"TOMATO": 10.0, "CARROT": 10.0}
    rows: list[list[object]] = [[None for _ in range(10)] for _ in range(10)]
    rows[4][5] = _mature_crop("TOMATO", 3)  # NE, required=3, gross=30
    rows[4][3] = _mature_crop("CARROT", 4)  # NW, required=4, gross=40
    candidate._routing_farm = {"tiles": rows}
    tasks = [
        CoreTask("HARVEST", (5, 4), ("HARVEST",), 2),
        CoreTask("HARVEST", (3, 4), ("HARVEST",), 2),
    ]
    assignment = candidate._assign(tasks, [(4, 4)], {"inventories": [{}]})
    assert assignment[0].target == (3, 4)
    assert candidate.cluster_sticky_assignments == 1


def test_full_episode_batches_harvest_and_preserves_safety() -> None:
    candidate = create_codex_e17_batched_cluster_routing_v4()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": 26090101, "turnsPerDay": 24},
        debug=True,
    )
    env.run([candidate, inert_pass_policy])
    instance = candidate.codex_e17_batched_cluster_routing_instance
    telemetry = instance.telemetry_snapshot()
    assert instance.error_count == 0
    assert instance.fallback_count == 0
    assert telemetry["deferred_drop_opportunities"] > 0
    assert telemetry["batched_harvest_services"] > 0
    assert telemetry["action_counts"].get("DROP", 0) > 0
    assert telemetry["non_sell_preservation_failures"] == 0
    assert sum(telemetry["execution_outcomes"].values()) == telemetry[
        "ledger_record_count"
    ]
    terminal_private = env.steps[-1][0]["observation"]["private"]
    sellable = set(load_v4_config()["sellable_products"])
    assert not any(
        int(quantity or 0) > 0 and item in sellable
        for item, quantity in terminal_private["shed"].items()
    )
    assert not any(
        int(quantity or 0) > 0 and item in sellable
        for inventory in terminal_private["inventories"]
        for item, quantity in inventory.items()
    )
